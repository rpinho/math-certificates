#!/usr/bin/env python3
"""Independent C82 checker: exact polynomials, certified roots, Arb intervals.

No producer implementation is used. See report.md for the mathematical bounds.
All certificate decimals outside the exact fields are parsed as inert strings.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import resource
import time
from fractions import Fraction
from flint import arb, acb, fmpz_poly, acb_poly, ctx


def require(ok, message):
    if not ok:
        raise ValueError(message)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a, b):
    return a // gcd(a, b) * b


def ball(q):
    if isinstance(q, Fraction):
        return arb(q.numerator) / q.denominator
    return arb(q)


def log(message):
    print(message, flush=True)


def enclosure(x):
    # Exact rational endpoints, not rounded decimal strings.
    return {'ball': x.str(45), 'lower': str(x.lower().fmpq()),
            'upper': str(x.upper().fmpq())}


def parse(cert):
    den, num = [], []
    for category, dest in [('denominator', den), ('numerator', num)]:
        require(type(cert[category]) is list, 'factor list required')
        for item in cert[category]:
            c = item['coeffs']
            require(type(c) is list and len(c) > 0, 'empty coefficients')
            require(all(type(v) is int for v in c), 'noninteger coefficient')
            require(c[0] != 0, 'leading zero')
            p = fmpz_poly(list(reversed(c)))
            if category == 'denominator':
                w = item['multiplicity']
                require(len(c) > 1 and c[0] == 1, 'denominator not monic/nonconstant')
                require(type(w) is int and w > 0, 'nonpositive integer multiplicity')
            else:
                require(type(item['q_rational']) is str, 'rational string required')
                w = Fraction(item['q_rational'])
                require(w >= 0, 'negative exponent')
                if not w:
                    continue
            dest.append((p, w, item.get('name', category)))
    require(len(den) > 0, 'no denominators')
    D = sum(p.degree() * w for p, w, _ in den)
    a = sum((p.degree() * w for p, w, _ in num), Fraction(0))
    require(a < D, 'degree condition fails')
    b = 1
    for p, q, _ in num:
        b = lcm(b, q.denominator)
        for r, _, _ in den:
            require(p.gcd(r).degree() == 0, 'nontrivial numerator/denominator gcd')
    return den, num, D, a, b


class Integrand:
    def __init__(self, den, num, D):
        T = fmpz_poly([0, 1, -1])
        self.factors = []
        self.roots = []
        self.H = arb(0)
        self.constant = arb(0)
        self.unit_candidates = []
        for kind, factors in [('den', den), ('num', num)]:
            for p, q, name in factors:
                f = p(T)
                rr = f.complex_roots()
                require(sum(m for r, m in rr) == f.degree(), 'incomplete root isolation')
                require(all(r.is_finite() for r, m in rr), 'nonfinite roots')
                w = ball(Fraction(q, D))
                if kind == 'den':
                    w = -w
                lc = arb(abs(int(f.leading_coefficient()))).log()
                self.constant += w * lc
                mh = lc
                stored = []
                for r, m in rr:
                    mod = abs(r)
                    mh += m * mod.max(1).log()
                    stored.append((r, mod, m))
                    self.roots.append((r, mod, w * m))
                    if mod.contains(1):
                        self.unit_candidates.append({'factor': name, 'kind': kind,
                                                     'root': str(r), 'multiplicity': m})
                        require(kind != 'den', 'denominator root possibly on circle: unsupported')
                if kind == 'den':
                    self.H += -w * mh
                self.factors.append((acb_poly(f), acb_poly(f.derivative()), w, lc, stored))
                log('ROOTS '+kind+' '+name+' degree='+str(f.degree()))
        self.twopi = 2 * arb.pi()
        self.calls = 0

    def point(self, t):
        if not self.factors:
            return self.constant, arb(0)
        z = acb(0, self.twopi * ball(t)).exp()
        g, gp = arb(0), arb(0)
        for f, df, w, lc, rr in self.factors:
            v = f(z)
            g += w * abs(v).log()
            gp += w * (acb(0, 1) * z * df(z) / v).real * self.twopi
        return g, gp

    def range(self, left, right):
        """Second-order Taylor enclosure, or rootwise upper bound near zeros."""
        self.calls += 1
        mid = (left + right) / 2
        h = ball((right - left) / 2)
        z = acb(0, self.twopi * ball(mid)).exp()
        chord = (self.twopi * h).upper()  # arc length bounds chord
        M2 = arb(0)
        upper = self.constant
        regular = True
        for r, mod, w in self.roots:
            d = abs(z - r)
            low = (d - chord).lower()
            high = (d + chord).upper()
            if w > 0:
                upper += w * high.log()
            else:
                if not low > 0:
                    return None, None
                upper += w * low.log()
            if low > 0:
                # |(d/dtheta)^2 log|e^(i theta)-r|| <= |r|/distance^2.
                M2 += abs(w) * mod / (low * low)
            else:
                regular = False
        if upper < 0:
            return None, upper
        if not regular:
            return None, upper
        g, gp = self.point(mid)
        error = (abs(gp) * h + M2 * (self.twopi * h)**2 / 2).upper()
        return g - error, (g + error).min(upper)

    def primitive_integral(self, left, right):
        """Integral of g on [left,right], by Li_2 entirely inside unit disc.

        Inside root: log|z-r|=Re log(1-r/z).
        Outside root: log|z-r|=log|r|+Re log(1-z/r).
        The derivative of Li_2 gives the integral, with no cut crossing.
        An interval root that straddles |r|=1 is allowed only if exact
        polynomial algebra has separately established it as a unit root;
        otherwise this method refuses it.
        """
        L, R = ball(left), ball(right)
        zl = acb(0, self.twopi * L).exp()
        zr = acb(0, self.twopi * R).exp()
        ans = self.constant * (R - L)
        for r, mod, w in self.roots:
            if mod < 1:
                v = ((r / zr).polylog(2) - (r / zl).polylog(2)).imag / self.twopi
            elif mod > 1:
                v = mod.log() * (R - L)
                v -= ((zr / r).polylog(2) - (zl / r).polylog(2)).imag / self.twopi
            else:
                # Use interval analytic primitive where the endpoint discs
                # avoid [1,infinity). Unit modulus is not required: if r
                # is slightly outside, real(log z)=0 still gives the identity
                # locally, and no branch discontinuity on the path is allowed.
                # Conservatively integrate such roots only by a separate
                # exact unit-root certificate set in certify_unit_roots().
                require(self.unit_proven(r), 'unproved unit root for primitive')
                v = ((r / zr).polylog(2) - (r / zl).polylog(2)).imag / self.twopi
            require(v.is_finite(), 'nonfinite dilogarithm primitive')
            ans += w * v
        return ans

    def certify_unit_roots(self):
        # Cyclotomic factors are proved exactly, not inferred from a modulus
        # numerically close to one. Every ambiguous root must match a root
        # of such a factor, which divides the exact composed polynomial.
        self.proven_units = []
        for f, df, w, lc, rr in self.factors:
            exact_f = fmpz_poly([int(c.real.fmpz()) for c in f.coeffs()])
            reverse = fmpz_poly(exact_f.coeffs()[::-1])
            common = exact_f.gcd(reverse)
            known = []
            for factor, multiplicity in common.factor()[1]:
                if factor.is_cyclotomic():
                    known.extend(s for s, k in factor.complex_roots())
            for s in known:
                require(sum(r.overlaps(s) for r, mod, m in rr) == 1,
                        'cyclotomic enclosure must match one isolated root')
            for r, mod, m in rr:
                if mod.contains(1):
                    require(sum(r.overlaps(s) for s in known) == 1,
                            'unknown root on circle')
                    self.proven_units.append(r)
        require(len(self.proven_units) == len(self.unit_candidates), 'unit root count')

    def unit_proven(self, r):
        return any(r is s for s in self.proven_units)

    def integrate_positive(self, eps):
        # Symmetry about 1/2 holds for real polynomial coefficients.
        stack = [(Fraction(0), Fraction(1, 2), 0)]
        positive = []
        uncertain = arb(0)
        neg_count = 0
        uncertain_count = 0
        while stack:
            l, r, depth = stack.pop()
            low, high = self.range(l, r)
            if high is not None and high <= 0:
                neg_count += 1
            elif low is not None and low > 0:
                if positive and positive[-1][1] == l:
                    positive[-1] = (positive[-1][0], r)
                else:
                    positive.append((l, r))
            elif high is not None and high.is_finite() and high < eps:
                # This covers sign changes, without assuming root counts or
                # dropping a neighborhood. Total uncertainty <= eps/2.
                cap = high.max(0) * ball(r - l)
                uncertain += arb(0).union(cap)
                uncertain_count += 1
            else:
                require(depth < 160, 'subdivision depth exhausted')
                m = (l + r) / 2
                stack.append((m, r, depth + 1))
                stack.append((l, m, depth + 1))
            if self.calls % 1000 == 0:
                log('PANELS '+str(self.calls)+' positive_intervals='+str(len(positive))+
                    ' negative='+str(neg_count)+' uncertain='+str(uncertain_count))
        total = uncertain
        log('SIGN PARTITION COMPLETE intervals='+str(len(positive)))
        for n, (l, r) in enumerate(positive):
            v = self.primitive_integral(l, r)
            require(v.upper() >= 0, 'negative integral on positive interval')
            total += v
            log('INTEGRAL '+str(n+1)+'/'+str(len(positive)))
        return 2 * total, {'range_calls': self.calls, 'negative_panels': neg_count,
                          'uncertain_panels': uncertain_count,
                          'positive_intervals': [[str(l),str(r)] for l,r in positive],
                          'unresolved_contribution': enclosure(2 * uncertain)}


def controls(cert):
    out = {}
    bad = copy.deepcopy(cert)
    bad['denominator'][0]['coeffs'][0] += 1
    try:
        parse(bad)
    except ValueError as e:
        out['perturbed_coefficient'] = str(e)
    require('perturbed_coefficient' in out, 'coefficient control not rejected')
    bad = copy.deepcopy(cert)
    bad['numerator'][0]['q_rational'] = '-1'
    try:
        parse(bad)
    except ValueError as e:
        out['perturbed_exponent'] = str(e)
    require('perturbed_exponent' in out, 'exponent control not rejected')
    # Nontrivial exact gcd and degree attacks.
    bad = copy.deepcopy(cert)
    bad['numerator'].append({'coeffs': cert['denominator'][0]['coeffs'],
                             'q_rational':'1'})
    try:
        parse(bad)
    except ValueError as e:
        out['shared_factor'] = str(e)
    require('shared_factor' in out, 'gcd control not rejected')
    bad = copy.deepcopy(cert)
    bad['numerator'][0]['q_rational'] = str(10**30)
    try:
        parse(bad)
    except ValueError as e:
        out['degree_violation'] = str(e)
    require('degree_violation' in out, 'degree control not rejected')
    # R=X-5, S=X-1, q=1/2: |R(T)|>=3, |S(T)|<=3,
    # so J=0; both roots of R(T) have modulus sqrt(5), hence B=log(5).
    analytic = {'denominator':[{'coeffs':[1,-5],'multiplicity':1}],
                'numerator':[{'coeffs':[1,-1],'q_rational':'1/2'}]}
    d,n,D,a,b = parse(analytic)
    f = Integrand(d,n,D)
    f.certify_unit_roots()
    J, stats = f.integrate_positive(arb('1e-20'))
    require(J.contains(0) and J.rad() == 0, 'analytic J is not exactly zero')
    require(f.H.overlaps(arb(5).log()), 'analytic Mahler answer mismatch')
    out['analytic_log5'] = enclosure(f.H + J)
    # Test the dilogarithm primitive against Jensen over the full circle,
    # including unit roots, outside roots, and an inside root.
    full = f.primitive_integral(Fraction(0), Fraction(1))
    require(full.overlaps(-arb(5).log()), 'full-circle Jensen mismatch')
    out['analytic_full_circle'] = enclosure(full)
    f.constant = arb(2).log()
    f.roots = []
    f.factors = []
    J, stats = f.integrate_positive(arb('1e-20'))
    require(J.overlaps(arb(2).log()), 'constant-positive integral mismatch')
    out['analytic_constant_positive'] = enclosure(J)
    # Exercise the inside-root primitive separately: the half-circle
    # mean for a real root 1/2 is zero by Jensen and conjugation symmetry.
    f.constant = arb(0)
    f.roots = [(acb(arb(1)/2), arb(1)/2, arb(1))]
    inside = f.primitive_integral(Fraction(0), Fraction(1,2))
    require(inside.contains(0), 'inside-root Jensen mismatch')
    out['analytic_inside_root'] = enclosure(inside)
    # A nonconstant everywhere-positive g: R=X-5 and S=100, q=1.
    # |R(T)|<=7<100; H+J=log(100) by Jensen.
    positive = {'denominator':[{'coeffs':[1,-5],'multiplicity':1}],
                'numerator':[{'coeffs':[100],'q_rational':'1'}]}
    d,n,D,a,b = parse(positive)
    f = Integrand(d,n,D)
    f.certify_unit_roots()
    J, stats = f.integrate_positive(arb('1e-22'))
    require((f.H+J).overlaps(arb(100).log()), 'positive analytic answer mismatch')
    out['analytic_log100'] = enclosure(f.H+J)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--certificate', default='inputs/certificates/certificate.json')
    ap.add_argument('--target', default='0.2519696460')
    ap.add_argument('--prec', type=int, default=384)
    ap.add_argument('--eps', default='1e-22')
    ap.add_argument('--output', default='replay/result.json')
    ap.add_argument('--controls-only', action='store_true')
    args = ap.parse_args()
    require(args.prec >= 192, 'precision less than 192')
    ctx.prec = args.prec
    ctx.threads = 1
    # Peak RSS is checked below and monitored externally with ps.
    started = time.monotonic_ns()
    log('PID '+str(os.getpid())+' precision='+str(ctx.prec))
    cert = json.loads(Path(args.certificate).read_text(), parse_float=str)
    d,n,D,a,b = parse(cert)
    log('EXACT D='+str(D)+' a='+str(a)+' b='+str(b)+' gcd_pairs='+str(len(d)*len(n)))
    red = controls(cert)
    log('CONTROLS '+json.dumps(red, sort_keys=True))
    if args.controls_only:
        return
    f = Integrand(d,n,D)
    f.certify_unit_roots()
    log('H '+f.H.str(60)+' unit_roots='+str(len(f.proven_units)))
    J, stats = f.integrate_positive(arb(args.eps))
    B = f.H + J
    false = Fraction('0.2519696459')
    require(B.lower() > ball(false), 'false target not rejected by lower endpoint')
    red['false_target'] = 'rejected: B lower endpoint exceeds '+str(false)
    target = ball(Fraction(args.target))
    status = 'PASS' if B < target else 'FAIL'
    usage = resource.getrusage(resource.RUSAGE_SELF)
    require(usage.ru_maxrss < 1000**3, 'RSS exceeded 1 GiB')
    result = {'status':status, 'precision_bits':ctx.prec, 'D':D, 'a':str(a),
              'b':b, 'degree_slack':str(D-a), 'gcd_pairs':len(d)*len(n),
              'composed_root_count':sum(len(rr) for f,df,w,lc,rr in f.factors),
              'unit_roots':f.unit_candidates, 'H':enclosure(f.H), 'J':enclosure(J),
              'B':enclosure(B), 'target':args.target, 'controls':red,
              'integration':stats, 'pid':os.getpid(), 'peak_rss_bytes':usage.ru_maxrss,
              'elapsed_ns':time.monotonic_ns()-started,
              'certificate_sha256':hashlib.sha256(Path(args.certificate).read_bytes()).hexdigest()}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    log('B '+B.str(60))
    log(status)
    require(status == 'PASS', 'target not proved')


if __name__ == '__main__':
    main()
