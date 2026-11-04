#!/usr/bin/env python3
"""Independent C82 certificate checker: standard library and python-flint only.

No producer code or numerical search values are used. See report.md for the
mathematical reduction and the validated integration construction.
"""
import argparse
import copy
import hashlib
import json
import os
import re
import sys
import time
from fractions import Fraction
from pathlib import Path

for _env in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_env] = '1'
from flint import arb, acb, fmpq, fmpz_poly, ctx


def ball(q):
    q = Fraction(q)
    return arb(q.numerator) / q.denominator


def require(ok, message):
    if not ok:
        raise ValueError(message)


def exact_checks(c):
    require(isinstance(c, dict), 'certificate must be an object')
    ds, ns = [], []
    for kind, result in [('denominator', ds), ('numerator', ns)]:
        require(isinstance(c.get(kind), list), kind + ' must be a list')
        for item in c[kind]:
            cs = item['coeffs']
            require(isinstance(cs, list) and len(cs) > 1, 'nonconstant polynomial required')
            require(all(type(v) is int for v in cs) and cs[0] != 0,
                    'coefficients must be exact integers; leading coefficient nonzero')
            p = fmpz_poly(cs[::-1])
            if kind == 'denominator':
                require(cs[0] == 1, 'denominator is not monic')
                w = item['multiplicity']
                require(type(w) is int and w > 0, 'multiplicity must be a positive integer')
            else:
                s = item['q_rational']
                require(isinstance(s, str) and re.fullmatch(r'-?\d+/[1-9]\d*', s),
                        'exponent must be an exact rational string')
                w = Fraction(s)
                require(w >= 0, 'negative exponent')
            result.append((item['name'], p, w))
    require(ds, 'no denominators')
    D = sum(p.degree() * w for _, p, w in ds)
    A = sum((p.degree() * w for _, p, w in ns), Fraction(0))
    require(A < D, 'weighted numerator degree is not below D')
    pairs = 0
    for _, p, _ in ds:
        for _, q, _ in ns:
            require(p.gcd(q).degree() == 0, 'numerator and denominator not coprime')
            pairs += 1
    den_pairs = 0
    for i, (_, p, _) in enumerate(ds):
        for _, q, _ in ds[:i]:
            require(p.gcd(q).degree() == 0, 'denominators not pairwise coprime')
            den_pairs += 1
    factors = []
    for name, p, _ in ds + ns:
        content, fs = p.factor()
        product = fmpz_poly([content])
        for f, e in fs:
            product *= f ** e
        require(product == p, 'factorization identity failed')
        factors.append({'name': name, 'content': int(content),
                        'factors': [{'degree': f.degree(), 'multiplicity': e} for f, e in fs],
                        'irreducible': len(fs) == 1 and fs[0][1] == 1})
    return ds, ns, D, {'D': D, 'weighted_numerator_degree': str(A),
                      'degree_slack': str(D-A), 'coprime_pairs': pairs,
                      'denominator_coprime_pairs': den_pairs, 'factorizations': factors}


class Evaluator:
    def __init__(self, ds, ns, D):
        self.groups = []
        self.H = arb(0)
        self.root_records = []
        self.calls = 0
        self.start = time.monotonic()
        T = fmpz_poly([0, 1, -1])
        # Exact cyclotomic factors containing every numerator circle root here.
        cyclo = [(fmpz_poly([-1, 1]), [Fraction(0)]),
                 (fmpz_poly([1, -1, 1]), [Fraction(1, 6), Fraction(5, 6)]),
                 (fmpz_poly([1, -1, 1, -1, 1]),
                  [Fraction(1, 10), Fraction(3, 10), Fraction(7, 10), Fraction(9, 10)])]
        self.singularities = set()
        for denominator, items in [(True, ds), (False, ns)]:
            for name, p, weight in items:
                if not weight:
                    continue
                pt = p(T)
                residual = pt
                roots = []
                circle_count = 0
                if not denominator:
                    for phi, ts in cyclo:
                        while True:
                            quotient, remainder = divmod(residual, phi)
                            if remainder:
                                break
                            residual = quotient
                            for t in ts:
                                r = (acb(0, 2) * arb.pi() * ball(t)).exp()
                                roots.append((r, 1))
                                circle_count += 1
                                if t <= Fraction(1, 2):
                                    self.singularities.add(t)
                isolated = residual.complex_roots()
                require(sum(m for _, m in isolated) == residual.degree(), 'incomplete root isolation')
                for r, m in isolated:
                    require(r.is_finite(), 'nonfinite isolated root')
                    require(abs(r) < 1 or abs(r) > 1,
                            'unhandled unit-circle or insufficiently isolated root in ' + name)
                roots += isolated
                require(sum(m for _, m in roots) == pt.degree(), 'root degree mismatch')
                lm = arb(abs(int(pt.leading_coefficient()))).log()
                for r, m in roots:
                    lm += m * abs(r).max(arb(1)).log()
                w = ball(Fraction(weight, D))
                if denominator:
                    self.H += w * lm
                    w = -w
                # Each squared distance is an entire function of complex t.
                terms = [(1+r.real*r.real+r.imag*r.imag, -2*r.real, -2*r.imag, m)
                         for r, m in roots]
                lc = arb(abs(int(pt.leading_coefficient()))).log()
                self.groups.append((w, lc, terms, roots))
                self.root_records.append({'name': name, 'degree_composed': pt.degree(),
                                          'roots_counted': sum(m for _, m in roots),
                                          'circle_roots': circle_count, 'log_mahler': str(lm)})
        print('ROOTS_READY H=' + str(self.H), flush=True)

    def upper_g(self, lo, hi):
        """One-sided bound, valid even at numerator logarithmic singularities."""
        t = ball(lo).union(ball(hi))
        z = (acb(0, 2) * arb.pi() * t).exp()
        result = arb(0)
        for w, lc, _, roots in self.groups:
            s = lc
            for r, m in roots:
                a = abs(z-r)
                if w > 0:
                    endpoint = a.upper()
                else:
                    endpoint = a.lower()
                    require(endpoint > 0, 'denominator distance not separated from zero')
                s += m * endpoint.log()
            result += w * s
        return result

    def g(self, t, analytic):
        theta = t * (2 * arb.pi())
        sn, co = theta.sin_cos()
        result = acb(0)
        for w, lc, terms, _ in self.groups:
            prod = acb(1)
            for c, a, b, m in terms:
                v = c + a*co + b*sn
                prod *= v if m == 1 else v ** m
            result += w * (lc + prod.log(analytic=analytic) / 2)
        return result

    def positive(self, t, analytic):
        self.calls += 1
        if self.calls % 10000 == 0:
            print('CALLS', self.calls, 'seconds', round(time.monotonic()-self.start, 1), flush=True)
        return self.g(t, analytic).real_max(acb(0), analytic=analytic)

    def integrate(self, tol):
        # Remove tiny neighborhoods only after proving max(0,g) is identically 0.
        cuts, exclusions = [], []
        eps = Fraction(1, 2**40)
        for t in sorted(self.singularities):
            lo, hi = max(Fraction(0), t-eps), min(Fraction(1,2), t+eps)
            bound = self.upper_g(lo, hi)
            require(bound < 0, 'cannot prove numerator singular neighborhood negative')
            cuts.append((lo, hi))
            exclusions.append({'lo': str(lo), 'hi': str(hi), 'g_upper': str(bound)})
        intervals = []
        left = Fraction(0)
        for lo, hi in cuts:
            if left < lo:
                intervals.append((left, lo))
            left = max(left, hi)
        if left < Fraction(1,2):
            intervals.append((left, Fraction(1,2)))
        total = arb(0)
        parts = []
        for lo, hi in intervals:
            print('INTEGRATE', str(lo), str(hi), flush=True)
            v = acb.integral(self.positive, ball(lo), ball(hi),
                             abs_tol=tol/len(intervals)/2, rel_tol=tol,
                             eval_limit=100000, depth_limit=100)
            require(v.is_finite() and v.imag.contains(0), 'validated integral nonfinite')
            total += v.real
            parts.append({'lo': str(lo), 'hi': str(hi), 'integral': str(v.real)})
            print('PART', str(v), flush=True)
        return 2*total, {'singular_neighborhoods': exclusions, 'parts': parts,
                         'function_evaluations': self.calls}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--certificate', default=str(Path(__file__).resolve().parents[1]/'inputs/certificates/certificate.json'))
    ap.add_argument('--precision', type=int, default=256)
    ap.add_argument('--target', default='0.252404806')
    ap.add_argument('--tol', default='1e-20')
    ap.add_argument('--output', default=str(Path(__file__).resolve().parent/'result.json'))
    args = ap.parse_args()
    require(args.precision >= 192, 'precision must be at least 192 bits')
    ctx.prec = args.precision
    ctx.threads = 1
    print('PID', os.getpid(), 'PRECISION', ctx.prec, flush=True)
    start = time.monotonic()
    c = json.loads(Path(args.certificate).read_text())
    ds, ns, D, algebra = exact_checks(c)
    e = Evaluator(ds, ns, D)
    J, integration = e.integrate(arb(args.tol))
    B = e.H + J
    passed = B < arb(args.target)
    result = {'status': 'PASS' if passed else 'FAIL', 'precision_bits': ctx.prec,
              'H': str(e.H), 'J': str(J), 'B': str(B), 'target': args.target,
              'certificate_sha256': hashlib.sha256(Path(args.certificate).read_bytes()).hexdigest(),
              'algebra': algebra, 'root_checks': e.root_records, 'integration': integration,
              'seconds': time.monotonic()-start}
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['status','H','J','B','seconds']}, indent=2), flush=True)
    return 0 if passed else 1

if __name__ == '__main__':
    sys.exit(main())
