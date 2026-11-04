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
from flint import arb, acb, acb_series, fmpz_poly, ctx, __version__ as flint_version


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
            require(isinstance(cs, list) and len(cs) >= 1, 'nonzero polynomial required')
            require(kind != 'denominator' or len(cs) > 1, 'nonconstant denominator required')
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
        self.polynomials = []
        self.all_roots = []
        self.weight_mass = arb(0)
        self.H = arb(0)
        self.root_records = []
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
                min_radial_gap = None
                max_root_radius = arb(0)
                for j, (r, m) in enumerate(isolated):
                    require(r.is_finite(), 'nonfinite isolated root')
                    require(abs(r) < 1 or abs(r) > 1,
                            'unhandled unit-circle or insufficiently isolated root in ' + name)
                    for s, _ in isolated[:j]:
                        require(not r.overlaps(s), 'root isolating rectangles overlap')
                    gap = abs(abs(r)-1).lower()
                    min_radial_gap = gap if min_radial_gap is None else min(min_radial_gap, gap)
                    max_root_radius = max_root_radius.max(r.real.rad()).max(r.imag.rad())
                roots += isolated
                require(sum(m for _, m in roots) == pt.degree(), 'root degree mismatch')
                lm = arb(abs(int(pt.leading_coefficient()))).log()
                for r, m in roots:
                    lm += m * abs(r).max(arb(1)).log()
                w = ball(Fraction(weight, D))
                if denominator:
                    self.H += w * lm
                    w = -w
                self.polynomials.append((w, [int(a) for a in reversed(p.coeffs())]))
                self.all_roots.extend(r for r, _ in roots)
                self.weight_mass += abs(w) * pt.degree()
                # Each squared distance is an entire function of complex t.
                terms = [(1+r.real*r.real+r.imag*r.imag, -2*r.real, -2*r.imag, m)
                         for r, m in roots]
                lc = arb(abs(int(pt.leading_coefficient()))).log()
                self.groups.append((w, lc, terms, roots))
                self.root_records.append({'name': name, 'degree_composed': pt.degree(),
                                          'roots_counted': sum(m for _, m in roots),
                                          'circle_roots': circle_count, 'log_mahler': str(lm),
                                          'minimum_noncircle_radial_gap': str(min_radial_gap),
                                          'maximum_root_coordinate_radius': str(max_root_radius)})
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

    def taylor_cell(self, lo, hi, order):
        """Enclose g and its integral on a real cell, including all tails.

        Write t=m+h*x, |x|<=1. On the complex t-disk of radius R=4h,
        |exp(2*pi*i*t)-exp(2*pi*i*m)| <= exp(2*pi*R)-1 = delta.
        If delta < d/2, where d bounds every center-to-root distance below,
        each logarithm of (z-r)/(z0-r) is holomorphic and has modulus at most
        -log(1-delta/d). The real Taylor-coefficient extension of g-g(m)
        thus has modulus <= M=weight_mass*(-log(1-delta/d)) on that disk.
        Cauchy's estimate bounds the discarded degree >= order terms on
        |x|<=1 by M*4**(-order)/(1-1/4).

        Series coefficients come independently from exact integer polynomials
        evaluated at T(exp(2*pi*i*(m+h*x))). Only their real parts enter g.
        """
        mid, half = (lo+hi)/2, (hi-lo)/2
        z0 = (acb(0, 2)*arb.pi()*ball(mid)).exp()
        d = min(abs(z0-r).lower() for r in self.all_roots)
        delta = (8*arb.pi()*ball(half)).expm1()
        if not (d > 0 and delta < d/2):
            return None
        M = -self.weight_mass * (1-delta/d).log()
        tail = M * arb(4)**(1-order) / 3
        x = acb_series([acb(0,2)*arb.pi()*ball(mid),
                        acb(0,2)*arb.pi()*ball(half)], order)
        z = x.exp()
        Tz = z*(1-z)
        coefficients = [arb(0) for _ in range(order)]
        for weight, cs in self.polynomials:
            value = acb_series([0], order)
            for a in cs:
                value = value*Tz + a
            logarithm = value.log()
            for k in range(order):
                coefficients[k] += weight*logarithm[k].real
        require(all(a.is_finite() for a in coefficients), 'nonfinite Taylor coefficient')
        # Horner on [-1,1] encloses the full Taylor polynomial.
        unit = arb(0, 1)
        gbox = coefficients[-1]
        for a in reversed(coefficients[:-1]):
            gbox = gbox*unit+a
        gbox += arb(0, tail.upper())
        integral = 2*ball(half)*sum((coefficients[k]/(k+1)
                                    for k in range(0, order, 2)), arb(0))
        integral += arb(0, (2*ball(half)*tail).upper())
        return gbox, integral, tail

    def integrate(self, tol, order=40):
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
        counts = {'attempted': 0, 'geometry_splits': 0, 'sign_splits': 0,
                  'positive': 0, 'negative': 0, 'crossing_boxes': 0}
        crossing_error = arb(0)
        max_tail = arb(0)
        # At most 100000 accepted cells, each crossing box has width <=
        # tol/1000000. The final computed enclosure width is checked as well.
        crossing_budget = tol/1000000
        for lo, hi in intervals:
            print('INTEGRATE', str(lo), str(hi), flush=True)
            stack = [(lo, hi, 0)]
            v = arb(0)
            while stack:
                a, b, depth = stack.pop()
                counts['attempted'] += 1
                require(counts['attempted'] <= 200000 and depth <= 100,
                        'adaptive integration resource limit')
                cell = self.taylor_cell(a, b, order)
                split = False
                if cell is None:
                    counts['geometry_splits'] += 1
                    split = True
                else:
                    gbox, iv, tail = cell
                    max_tail = max_tail.max(tail)
                    if gbox < 0:
                        counts['negative'] += 1
                    elif gbox > 0:
                        v += iv
                        counts['positive'] += 1
                    else:
                        upper = ball(b-a)*gbox.upper().max(arb(0))
                        if upper < crossing_budget:
                            v += arb(0).union(upper)
                            crossing_error += upper
                            counts['crossing_boxes'] += 1
                        else:
                            counts['sign_splits'] += 1
                            split = True
                if split:
                    m = (a+b)/2
                    stack.append((m, b, depth+1))
                    stack.append((a, m, depth+1))
                if counts['attempted'] % 500 == 0:
                    print('CELLS', counts, 'seconds', round(time.monotonic()-self.start, 1), flush=True)
            total += v
            parts.append({'lo': str(lo), 'hi': str(hi), 'integral': str(v)})
            print('PART', str(v), flush=True)
        return 2*total, {'singular_neighborhoods': exclusions, 'parts': parts,
                         'cells': counts, 'taylor_order': order,
                         'maximum_pointwise_tail': str(max_tail),
                         'crossing_integral_upper_half_domain': str(crossing_error)}


def decimal_enclosure(x, digits=28):
    """Outward decimal rounding using exact rational endpoints of an Arb ball."""
    scale = 10**digits
    lo = Fraction(str(x.lower().fmpq()))*scale
    hi = Fraction(str(x.upper().fmpq()))*scale
    lower = lo.numerator//lo.denominator
    upper = -((-hi.numerator)//hi.denominator)
    def show(n):
        sign = '-' if n < 0 else ''
        a, b = divmod(abs(n), scale)
        return sign+str(a)+'.'+str(b).zfill(digits)
    return [show(lower), show(upper)]


def run_controls(c, B, e):
    results = {}
    def rejected(name, altered):
        try:
            exact_checks(altered)
        except ValueError as exc:
            results[name] = {'status': 'REJECTED', 'reason': str(exc)}
        else:
            raise ValueError('negative control incorrectly accepted: '+name)
    altered = copy.deepcopy(c)
    altered['denominator'][0]['coeffs'][-1] = 0
    rejected('perturbed_constant_coefficient', altered)
    altered = copy.deepcopy(c)
    altered['denominator'][0]['coeffs'][0] += 1
    rejected('nonmonic_leading_coefficient', altered)
    altered = copy.deepcopy(c)
    D = sum(v['multiplicity']*(len(v['coeffs'])-1) for v in c['denominator'])
    altered['numerator'][0]['q_rational'] = str(D)+'/1'
    rejected('perturbed_nonnegative_exponent', altered)
    altered = copy.deepcopy(c)
    altered['numerator'][0]['q_rational'] = '-1/1'
    rejected('negative_exponent', altered)
    altered = copy.deepcopy(c)
    altered['denominator'][0]['multiplicity'] = 0
    rejected('zero_multiplicity', altered)
    require(B > arb('0.25240480595'), 'false target was not strictly refuted')
    results['false_target'] = {'target': '0.25240480595', 'status': 'REJECTED',
                               'reason': 'certified lower endpoint of B exceeds target'}

    # Compare the exact-polynomial path with the independently root-factored
    # expression at deterministic points; no floating point seeds or grid values.
    point_checks = []
    for t in [Fraction(123,1000), Fraction(211,1000), Fraction(41,100)]:
        z = (acb(0,2)*arb.pi()*ball(t)).exp()
        Tz = z*(1-z)
        direct = arb(0)
        for w, cs in e.polynomials:
            v = acb(0)
            for a in cs:
                v = v*Tz+a
            direct += w*abs(v).log()
        roots = e.g(acb(ball(t)), False).real
        require(direct.overlaps(roots), 'root/polynomial point check disagrees')
        require((direct-roots).abs_upper() < arb('1e-25'), 'point check too wide')
        point_checks.append({'t': str(t), 'direct': str(direct), 'roots': str(roots)})
    results['root_polynomial_crosschecks'] = point_checks

    # Known cases exercise the same algebra, root and Taylor integration path.
    # R=X+1: |R(T(e^it))|^2=3-2*cos(2t)>=1 and log M=log(phi).
    # A constant numerator 10 makes g>0 everywhere, giving B=log(10).
    # R=X+10, S=X, q=1/2: |T+10|>=8, |T|<=2, so g<0,
    # including at the numerator singularity; both denominator roots are outside
    # the unit circle and their product has modulus 10, so B=log(10).
    phi_log = ((1+arb(5).sqrt())/2).log()
    cases = [
        ('golden_ratio_zero_positive_part', [1,1], [], phi_log),
        ('constant_numerator_positive_integral', [1,1],
         [{'name':'ten', 'coeffs':[10], 'q_rational':'1/1'}], arb(10).log()),
        ('numerator_log_singularity_zero_integral', [1,10],
         [{'name':'X', 'coeffs':[1,0], 'q_rational':'1/2'}], arb(10).log())]
    analytic = []
    for name, cs, ns, known in cases:
        synthetic = {'denominator':[{'name':'R', 'coeffs':cs, 'multiplicity':1}],
                     'numerator':ns}
        ds, ns, D, _ = exact_checks(synthetic)
        evaluator = Evaluator(ds, ns, D)
        J, integration = evaluator.integrate(arb('1e-20'))
        value = evaluator.H+J
        require(value.overlaps(known), 'analytic case disagrees: '+name)
        require((value-known).abs_upper() < arb('1e-18'), 'analytic case too wide: '+name)
        analytic.append({'name':name, 'B':str(value), 'known_answer':str(known),
                         'J':str(J), 'integration':integration, 'status':'PASS'})
    results['analytic_cases'] = analytic
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--certificate', default=str(Path(__file__).resolve().parents[1]/'inputs/certificates/certificate.json'))
    ap.add_argument('--precision', type=int, default=384)
    ap.add_argument('--target', default='0.252404806')
    ap.add_argument('--tol', default='1e-20')
    ap.add_argument('--controls', action='store_true')
    ap.add_argument('--output', default=str(Path(__file__).resolve().parent/'result.json'))
    args = ap.parse_args()
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(args.output).write_text(json.dumps({'status':'PARTIAL', 'pid':os.getpid(),
        'reason':'checker started; no enclosure accepted yet',
        'checker_sha256':source_hash}, indent=2)+'\n')
    require(args.precision >= 192, 'precision must be at least 192 bits')
    ctx.prec = args.precision
    ctx.threads = 1
    ctx.cap = 40
    print('PID', os.getpid(), 'PRECISION', ctx.prec, flush=True)
    start = time.monotonic()
    c = json.loads(Path(args.certificate).read_text())
    ds, ns, D, algebra = exact_checks(c)
    e = Evaluator(ds, ns, D)
    J, integration = e.integrate(arb(args.tol))
    B = e.H + J
    require(B.is_finite() and 2*B.rad() < arb(args.tol),
            'final enclosure exceeds requested tolerance')
    passed = B < arb(args.target)
    controls = run_controls(c, B, e) if args.controls else None
    result = {'status': 'PASS' if passed else 'FAIL', 'precision_bits': ctx.prec,
              'checker_sha256': source_hash, 'python_flint_version': flint_version,
              'H': str(e.H), 'J': str(J), 'B': str(B), 'target': args.target,
              'B_decimal': decimal_enclosure(B),
              'certificate_sha256': hashlib.sha256(Path(args.certificate).read_bytes()).hexdigest(),
              'algebra': algebra, 'root_checks': e.root_records, 'integration': integration,
              'controls': controls,
              'seconds': time.monotonic()-start}
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['status','H','J','B','seconds']}, indent=2), flush=True)
    return 0 if passed else 1

if __name__ == '__main__':
    sys.exit(main())
