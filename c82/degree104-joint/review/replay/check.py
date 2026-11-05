#!/usr/bin/env python3
"""Independent C82 checker: exact polynomial algebra and Arb enclosures only.

The integral of the positive part is certified on an adaptive dyadic tiling.
Strictly positive neighboring panels are joined and integrated using a rootwise
Li_2 primitive. Negative panels contribute zero. Undecided panels contribute
[0, width*max(0, upper(g))]; their total is explicitly included, never dropped.
"""
import argparse
import copy
import hashlib
import json
import os
import time
from fractions import Fraction
from pathlib import Path
from flint import arb, acb, fmpz_poly, ctx


def ball(q):
    q = Fraction(q)
    return arb(q.numerator) / q.denominator


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a, b):
    return a // gcd(a, b) * b


def require(ok, message):
    if not ok:
        raise ValueError(message)


def exact(c):
    den, num = [], []
    for kind, dest in [('denominator', den), ('numerator', num)]:
        require(isinstance(c[kind], list), 'factor list required')
        for f in c[kind]:
            v = f['coeffs']
            require(isinstance(v, list) and len(v) > 0, 'empty coefficients')
            require(all(type(x) is int for x in v), 'noninteger coefficient')
            require(v[0] != 0, 'zero leading coefficient')
            p = fmpz_poly(list(reversed(v)))
            if kind == 'denominator':
                m = f['multiplicity']
                require(p.degree() > 0 and v[0] == 1, 'denominator must be nonconstant and monic')
                require(type(m) is int and m > 0, 'multiplicity must be positive integer')
                dest.append((f['name'], p, Fraction(m)))
            else:
                require(type(f['q_rational']) in (str, int), 'exponent must be exact rational')
                q = Fraction(f['q_rational'])
                require(q >= 0, 'negative exponent')
                if q:
                    dest.append((f['name'], p, q))
    require(len(den) > 0, 'empty denominator')
    D = sum(int(m) * p.degree() for _, p, m in den)
    a = sum((q * p.degree() for _, p, q in num), Fraction(0))
    require(a < D, 'strict degree condition failed')
    pairs = 0
    for _, s, _ in num:
        for _, r, _ in den:
            require(s.gcd(r).degree() == 0, 'numerator/denominator gcd failed')
            pairs += 1
    b = 1
    for _, _, q in num:
        b = lcm(b, q.denominator)
    require(all((q*b).denominator == 1 for _, _, q in num), 'denominator clearing failed')
    info = dict(D=D, a=str(a), slack=str(D-a), common_denominator=b,
                active_pairs=pairs, denominators=len(den), active_numerators=len(num))
    return den, num, D, info


# All ambiguous unit-modulus roots in this input are accounted for by these
# exact factors. These polynomials have precisely the stated roots of unity.
CIRCLE = [fmpz_poly([-1, 1]), fmpz_poly([1, -1, 1]),
          fmpz_poly([1, -1, 1, -1, 1])]


def isolate(p):
    """Separate known cyclotomic factors exactly; certify all remaining radii."""
    roots = []
    for cyclo in CIRCLE:
        mult = 0
        while p.degree() >= cyclo.degree():
            quo, rem = divmod(p, cyclo)
            if rem:
                break
            p = quo
            mult += 1
        if mult:
            for r, m in cyclo.complex_roots():
                roots.append((r, m*mult, 'circle'))
    if p.degree() > 0:
        rest = p.complex_roots()
        require(sum(m for _, m in rest) == p.degree(), 'incomplete root count')
        for r, m in rest:
            radius = abs(r)
            require(radius < 1 or radius > 1, 'unresolved unit-circle root')
            roots.append((r, m, 'inside' if radius < 1 else 'outside'))
    return roots


class Integral:
    def __init__(self, c, verbose=True):
        den, num, self.D, self.info = exact(c)
        self.roots = []
        self.constant = arb(0)
        self.H = arb(0)
        self.twopi = 2 * arb.pi()
        T = fmpz_poly([0, 1, -1])
        count, circle = 0, 0
        for kind, factors in [('denominator', den), ('numerator', num)]:
            for name, p, weight in factors:
                composed = p(T)
                roots = isolate(composed)
                require(sum(m for _, m, _ in roots) == composed.degree(), 'root count mismatch')
                lead = arb(abs(composed.leading_coefficient())).log()
                measure = lead
                sign = -1 if kind == 'denominator' else 1
                w = ball(weight / self.D)
                self.constant += sign*w*lead
                for r, m, location in roots:
                    require(r.is_finite(), 'nonfinite root ball')
                    if location == 'outside':
                        measure += m*abs(r).log()
                    if location == 'circle':
                        circle += m
                    self.roots.append((r, sign*w*m, location))
                    count += m
                if kind == 'denominator':
                    self.H += w*measure
                if verbose:
                    print('ROOTS', kind, name, composed.degree(), 'logM', measure, flush=True)
        self.info.update(composed_roots=count, circle_roots=circle)
        self.verbose = verbose

    def range(self, left, right):
        """A direct range and a mean-value range; either may prove the sign.

        Positive-weight singularities are allowed in the direct upper bound.
        Denominator singularities would force subdivision (none in this input).
        """
        mid = (left+right)/2
        half = (right-left)/2
        theta = self.twopi * arb(ball(mid), ball(half))
        z = acb(0, theta).exp()
        z0 = acb(0, self.twopi*ball(mid)).exp()
        upper = self.constant
        lower = self.constant
        center = self.constant
        derivative = acb(0)
        smooth = True
        lower_finite = True
        for r, w, _ in self.roots:
            diff = z-r
            size = abs(diff)
            hi = size.upper()
            lo = size.lower()
            if w > 0:
                upper += w*hi.log()
                if lo > 0:
                    lower += w*lo.log()
                else:
                    lower_finite = False
            else:
                if not lo > 0:
                    return None, None
                upper += w*lo.log()
                lower += w*hi.log()
            if not lo > 0:
                smooth = False
            if smooth:
                center += w*abs(z0-r).log()
                derivative += w/diff
        hi = upper.upper()
        low = lower.lower() if lower_finite else None
        if smooth:
            slope = (acb(0, self.twopi)*z*derivative).real.abs_upper()
            variation = ball(half)*slope
            mh = (center+variation).upper()
            ml = (center-variation).lower()
            if mh < hi:
                hi = mh
            if low is None or ml > low:
                low = ml
        return low, hi

    def primitive_difference(self, left, right):
        """Integral g(t) dt from left to right via Li_2, in ball arithmetic.

        Inside/circle: log|e^(i theta)-r| = log|1-r e^(-i theta)|.
        Outside: log|r| + log|1-e^(i theta)/r|.
        Primitives in theta are respectively +Im Li_2 and -Im Li_2.
        The inside/circle primitive is continuous, including r e^(-i theta)=1.
        """
        za = acb(0, self.twopi*ball(left)).exp()
        zb = acb(0, self.twopi*ball(right)).exp()
        width = ball(right-left)
        result = self.constant*width
        for r, w, location in self.roots:
            if location == 'outside':
                term = abs(r).log()*width - ((zb/r).polylog(2) - (za/r).polylog(2)).imag/self.twopi
            else:
                term = ((r/zb).polylog(2) - (r/za).polylog(2)).imag/self.twopi
            require(term.is_finite(), 'nonfinite dilogarithm enclosure')
            result += w*term
        return result

    def run(self, tolerance):
        # Real coefficients give g(1-t)=g(t). Cover the entire half circle.
        stack = [(Fraction(0), Fraction(1, 2), 0)]
        positive = []
        uncertain = arb(0)
        counts = dict(negative=0, positive=0, uncertain=0, evaluated=0, max_depth=0)
        started = time.monotonic_ns()
        while stack:
            left, right, depth = stack.pop()
            lo, hi = self.range(left, right)
            counts['evaluated'] += 1
            counts['max_depth'] = max(depth, counts['max_depth'])
            if hi is not None and hi <= 0:
                counts['negative'] += 1
            elif lo is not None and lo > 0:
                counts['positive'] += 1
                if positive and positive[-1][1] == left:
                    positive[-1] = (positive[-1][0], right)
                else:
                    positive.append((left, right))
            elif hi is not None and 2*ball(right-left)*hi.max(0) < ball(tolerance) / 1024:
                # A local stopping budget only; the actual summed enclosure
                # is carried into J, so no error is silently discarded.
                uncertain += 2*ball(right-left)*hi.max(0)
                counts['uncertain'] += 1
            else:
                require(depth < 160, 'tiling depth limit')
                mid = (left+right)/2
                stack.append((mid, right, depth+1))
                stack.append((left, mid, depth+1))
            if self.verbose and counts['evaluated'] % 1000 == 0:
                print('TILING', counts, 'seconds', (time.monotonic_ns()-started)//10**9, flush=True)
        J = arb(0)
        for index, (left, right) in enumerate(positive):
            value = 2*self.primitive_difference(left, right)
            J += value
            if self.verbose:
                print('ARC', index, str(left), str(right), 'integral', value, flush=True)
        error = uncertain.upper()
        J += arb(error/2, error/2)
        B = self.H+J
        require(B.is_finite(), 'nonfinite result')
        counts.update(positive_arcs=len(positive), unresolved_integral_upper=str(error))
        return B, J, counts


def out_interval(x, places=30):
    scale = 10**places
    low = int((x.lower()*scale).floor().unique_fmpz())
    high = int((x.upper()*scale).ceil().unique_fmpz())
    def fmt(n):
        sign = '-' if n < 0 else ''
        n = abs(n)
        return sign+str(n//scale)+'.'+str(n%scale).zfill(places)
    return [fmt(low), fmt(high)]


def controls(c):
    result = {}
    bad = copy.deepcopy(c)
    bad['denominator'][0]['coeffs'][0] += 1
    try:
        exact(bad)
    except ValueError as e:
        result['perturbed_coefficient'] = 'REJECTED: '+str(e)
    else:
        raise ValueError('coefficient control accepted')
    bad = copy.deepcopy(c)
    bad['numerator'][0]['q_rational'] = '-1'
    try:
        exact(bad)
    except ValueError as e:
        result['perturbed_exponent'] = 'REJECTED: '+str(e)
    else:
        raise ValueError('exponent control accepted')
    # Q=X-3 has both composed roots of modulus sqrt(3), hence H=log(3).
    # On the unit circle |T-3|<=5. With A=5 the max is identically log(5),
    # so B=log(5), J=log(5/3). This exercises a nonzero positive integral.
    analytic = {'denominator':[{'name':'analytic', 'coeffs':[1,-3], 'multiplicity':1}],
                'numerator':[{'name':'constant', 'coeffs':[5], 'q_rational':'1'}]}
    obj = Integral(analytic, verbose=False)
    B, J, stats = obj.run(Fraction(1,10**16))
    require(B.contains(arb(5).log()), 'analytic log(5) case failed')
    require(J.contains((arb(5)/3).log()), 'analytic log(5/3) case failed')
    require(B.rad() < ball('1/100000000000000'), 'analytic enclosure too wide')
    result['analytic_positive'] = dict(B=out_interval(B), expected='log(5)',
                                      J=out_interval(J), stats=stats)
    # S=X, q=1/2 gives a numerator singularity at z=1. On the circle,
    # Re T=1+c-2c^2<=9/8, so |T-3|>=15/8>sqrt(2)>=sqrt(|T|).
    analytic['numerator'] = [{'name':'singular', 'coeffs':[1,0], 'q_rational':'1/2'}]
    obj = Integral(analytic, verbose=False)
    B, J, stats = obj.run(Fraction(1,10**16))
    require(B.contains(arb(3).log()), 'analytic singular case failed')
    require(J == 0, 'negative singular case has nonzero J')
    result['analytic_singular'] = dict(B=out_interval(B), expected='log(3)', J=str(J), stats=stats)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('certificate', nargs='?', default=str(Path(__file__).resolve().parents[1]/'inputs/certificates/certificate.json'))
    ap.add_argument('--prec', type=int, default=256)
    ap.add_argument('--target', default='0.2519964890')
    ap.add_argument('--tolerance', default='1/100000000000000000000')
    ap.add_argument('--controls', action='store_true')
    ap.add_argument('--output')
    args = ap.parse_args()
    require(args.prec >= 192, 'precision below 192 bits')
    ctx.prec = args.prec
    ctx.threads = 1
    print('PID',os.getpid(),'precision',ctx.prec,'threads',ctx.threads,flush=True)
    started = time.monotonic_ns()
    c = json.loads(Path(args.certificate).read_text(), parse_float=str)
    obj = Integral(c)
    print('EXACT',json.dumps(obj.info,sort_keys=True),flush=True)
    B, J, counts = obj.run(Fraction(args.tolerance))
    target = ball(Fraction(args.target))
    passed = B.upper() < target
    result = dict(status='PASS' if passed else 'FAIL', precision=ctx.prec,
                  target=args.target, B=out_interval(B), H=out_interval(obj.H),
                  J=out_interval(J), exact=obj.info, tiling=counts,
                  seconds=(time.monotonic_ns()-started)//10**9,
                  certificate_sha256=hashlib.sha256(Path(args.certificate).read_bytes()).hexdigest())
    if args.controls:
        result['controls'] = controls(c)
        require(B.lower() > ball('0.2519964889'), 'false target control not separated')
        result['controls']['false_target'] = 'REJECTED: lower endpoint exceeds 0.2519964889'
    if args.output:
        Path(args.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True),flush=True)
    raise SystemExit(0 if passed else 1)


if __name__ == '__main__':
    main()
