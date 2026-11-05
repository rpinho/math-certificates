#!/usr/bin/env python3
"""Independent C82 replay: exact polynomials, certified roots, Cauchy/Taylor balls.
Only Python's standard library and python-flint are used. All decimal data are strings.
The proof of the integration remainder is in replay/report.md.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import time
from flint import arb, acb, arb_poly, acb_poly, acb_series, fmpq, fmpz_poly, ctx


def gcd_int(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def lcm_int(a, b):
    return a // gcd_int(a, b) * b


def ball(q):
    return arb(str(q))


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def exact_poly(row):
    c = row['coeffs']
    require(isinstance(c, list) and len(c) > 0, 'empty coefficient list')
    require(all(type(v) is int for v in c), 'noninteger coefficient')
    require(c[0] != 0, 'leading zero / zero polynomial')
    return fmpz_poly(list(reversed(c)))


def hypotheses(cert):
    denominators, numerators = [], []
    D, a, b = 0, fmpq(0), 1
    for row in cert['denominator']:
        p = exact_poly(row)
        m = row['multiplicity']
        require(p.degree() > 0 and p.leading_coefficient() == 1, 'denominator is not nonconstant monic')
        require(type(m) is int and m > 0, 'multiplicity is not a positive integer')
        denominators.append((row['name'], p, fmpq(m)))
        D += m * p.degree()
    require(D > 0, 'empty denominator')
    for row in cert['numerator']:
        p = exact_poly(row)
        require(isinstance(row['q_rational'], str), 'exponent must be an exact rational string')
        q = fmpq(row['q_rational'])
        require(q >= 0, 'negative exponent')
        if q:
            numerators.append((row['name'], p, q))
            a += q * p.degree()
            b = lcm_int(b, int(q.q))
    require(a < D, 'strict degree condition fails')
    pairs = 0
    for _, s, _ in numerators:
        for _, r, _ in denominators:
            require(s.gcd(r).degree() == 0, 'nontrivial numerator/denominator gcd')
            pairs += 1
    return denominators, numerators, D, {'D': D, 'a': str(a), 'slack': str(D-a), 'b': b,
        'degree_A': str(a*b), 'degree_Q_power_b': b*D, 'active_gcd_pairs': pairs,
        'denominator_count': len(denominators), 'active_numerator_count': len(numerators)}


class Factor:
    def __init__(self, name, p, weight, denominator):
        self.name, self.p, self.weight, self.denominator = name, p, weight, denominator
        self.coeffs = [int(c) for c in reversed(p.coeffs())]
        self.composed = p(fmpz_poly([0, 1, -1]))
        self.point_poly = acb_poly(self.composed)
        self.roots = self.composed.complex_roots()
        require(sum(mult for _, mult in self.roots) == self.composed.degree(), 'incomplete roots')
        require(all(z.is_finite() for z, _ in self.roots), 'nonfinite root enclosure')
        self.degree = self.composed.degree()
        self.log_leading = arb(abs(int(self.composed.leading_coefficient()))).log()
        self.mahler = self.log_leading
        for z, mult in self.roots:
            self.mahler += mult * abs(z).max(arb(1)).log()

    def log_range(self, z):
        # Product of squared distances gives a bound even at a numerator zero.
        v = arb(abs(int(self.composed.leading_coefficient()))) ** 2
        for r, mult in self.roots:
            d = z - r
            v *= (d.real**2 + d.imag**2) ** mult
        if v > 0:
            return v.log()/2, None
        if self.denominator:
            return None, None
        upper = v.upper()
        if upper > 0:
            return None, upper.log()/2
        return None, None

    def series(self, x):
        y = acb_series([self.coeffs[0]])
        for c in self.coeffs[1:]:
            y = y*x + c
        return y.log()


class Integrand:
    def __init__(self, cert, verbose=True):
        den, num, self.D, self.exact = hypotheses(cert)
        self.factors = []
        self.H = arb(0)
        self.root_count = 0
        for isden, rows in [(True, den), (False, num)]:
            for name, p, q in rows:
                weight = ball((-q if isden else q) / self.D)
                f = Factor(name, p, weight, isden)
                self.factors.append(f)
                self.root_count += f.degree
                if isden:
                    self.H -= weight*f.mahler
                if verbose:
                    print('ROOTS', name, f.degree, 'logM', f.mahler.str(32), flush=True)
        self.exact['composed_root_count_with_multiplicity'] = self.root_count
        self.twopi = 2*arb.pi()

    def singular_upper(self, mid, half):
        z = acb(0, self.twopi*arb(mid, half)).exp()
        upper = arb(0)
        for f in self.factors:
            v, hi = f.log_range(z)
            if v is not None:
                upper += f.weight*v
            elif hi is not None and not f.denominator:
                upper += f.weight*hi
            else:
                return None
        return upper.upper()

    def taylor(self, mid, half, order):
        z0 = acb(0, self.twopi*mid).exp()
        # Disk |u| <= 4 in normalized panel coordinate t = mid + half*u.
        delta = (4*self.twopi*half).expm1()
        M = arb(0)
        for f in self.factors:
            if f.degree == 0:
                continue
            distances = [abs(z0-r).lower() for r, _ in f.roots]
            d = min(distances)
            rho = delta/d
            if not rho < 1:
                return None
            # Conservative per-factor bound for log(P(z)/P(z0)).
            M += abs(f.weight)*f.degree*(-(1-rho).log())
        remainder = M / (4**(order+1)) * arb(4)/3
        ctx.cap = order+1
        z = acb_series([0, acb(0, self.twopi*half)]).exp()*z0
        x = z*(1-z)
        coeffs = [arb(0) for _ in range(order+1)]
        for f in self.factors:
            s = f.series(x)
            for k in range(order+1):
                coeffs[k] += f.weight*s[k].real
        require(all(c.is_finite() for c in coeffs), 'nonfinite Taylor coefficient')
        error = remainder.upper()
        valrange = arb_poly(coeffs)(arb(0, 1)) + arb(0, error)
        integral_mean = sum((coeffs[k]/(k+1) for k in range(0, order+1, 2)), arb(0))
        integral = 2*half*(integral_mean+arb(0, error))
        return valrange, integral


def integrate(g, tol, order, verbose=True):
    # Real coefficients imply g(1-t)=g(t); cover [0,1/2], then double.
    stack = [(0, 0)]  # panel [k/2^(level+1), (k+1)/2^(level+1)]
    result = arb(0)
    covered = fmpq(0)
    stats = {'visited': 0, 'negative': 0, 'positive': 0, 'crossing': 0,
             'singular_negative': 0, 'max_level': 0}
    while stack:
        k, level = stack.pop()
        half = arb(1)/2**(level+2)
        mid = (2*k+1)*half
        stats['visited'] += 1
        stats['max_level'] = max(stats['max_level'], level)
        require(level < 160, 'unresolved singularity or sign change')
        t = g.taylor(mid, half, order)
        if t is None:
            upper = g.singular_upper(mid, half)
            if upper is not None and upper < 0:
                stats['singular_negative'] += 1
                covered += fmpq(1, 2**(level+1))
                continue
        else:
            valrange, integral = t
            if valrange <= 0:
                stats['negative'] += 1
                covered += fmpq(1, 2**(level+1))
                continue
            if valrange > 0 and integral.rad() < tol*half:
                result += integral
                stats['positive'] += 1
                covered += fmpq(1, 2**(level+1))
                continue
            cap = valrange.max(arb(0))*2*half
            if cap.is_finite() and cap.rad() < tol/65536:
                result += cap
                stats['crossing'] += 1
                covered += fmpq(1, 2**(level+1))
                continue
        stack.append((2*k+1, level+1))
        stack.append((2*k, level+1))
        if verbose and stats['visited'] % 100 == 0:
            print('PANELS', json.dumps(stats), 'partial_J', (2*result).str(24), flush=True)
    J = result*2
    require(covered == fmpq(1, 2), 'dyadic panels do not cover the integration domain')
    stats['covered_length'] = str(covered)
    require(J.rad() < tol, 'accumulated integration radius exceeds tolerance')
    return J, stats


def endpoints(x, digits=30):
    # Outward decimal rounding from exact dyadic lower/upper bounds.
    scale = 10**digits
    lo = x.lower().fmpq()*scale
    hi = x.upper().fmpq()*scale
    l = int(lo.p)//int(lo.q)
    u = -((-int(hi.p))//int(hi.q))
    def fmt(n):
        sign = '-' if n < 0 else ''
        n = abs(n)
        return sign+str(n//scale)+'.'+str(n % scale).zfill(digits)
    return [fmt(l), fmt(u)]


def controls(cert, B, order):
    out = {}
    def rejected(label, mutated):
        try:
            hypotheses(mutated)
        except (ValueError, TypeError) as e:
            out[label] = {'status': 'PASS', 'rejection': str(e)}
        else:
            raise ValueError('control was not rejected: '+label)
    c = copy.deepcopy(cert)
    c['denominator'][0]['coeffs'][0] += 1
    rejected('perturbed_coefficient', c)
    c = copy.deepcopy(cert)
    c['numerator'][0]['q_rational'] = '-1'
    rejected('perturbed_exponent', c)
    c = copy.deepcopy(cert)
    c['numerator'][0]['q_rational'] = str(B.D+1)
    rejected('degree_failure', c)
    c = copy.deepcopy(cert)
    c['numerator'].append({'name': 'shared_factor_control',
        'coeffs': c['denominator'][0]['coeffs'][:], 'q_rational': '1'})
    rejected('gcd_failure', c)
    for constant in [1, 16]:
        analytic = {'denominator': [{'name': 'X_minus_3', 'coeffs': [1,-3], 'multiplicity': 1}],
                    'numerator': [{'name': 'constant', 'coeffs': [constant], 'q_rational': '1'}]}
        g = Integrand(analytic, verbose=False)
        J, stats = integrate(g, arb('1e-20'), order, verbose=False)
        value = g.H+J
        known = arb(3 if constant == 1 else 16).log()
        require(value.overlaps(known), 'analytic known answer missed')
        require(value.rad() < arb('1e-20'), 'analytic case insufficient accuracy')
        out['analytic_constant_'+str(constant)] = {'status':'PASS', 'expected': 'log('+str(3 if constant == 1 else 16)+')',
                'B': endpoints(value), 'J': endpoints(J), 'panels': stats}
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', nargs='?', default='inputs/certificates/certificate.json')
    parser.add_argument('--prec', type=int, default=384)
    parser.add_argument('--order', type=int, default=40)
    parser.add_argument('--tol', default='1e-21')
    parser.add_argument('--target', default='0.2519923410')
    parser.add_argument('--output', default='replay/result.json')
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    require(args.prec >= 192, 'precision below 192 bits')
    require(args.order >= 8, 'Taylor order below 8')
    ctx.prec, ctx.threads = args.prec, 1
    begin = time.monotonic_ns()
    print('PID', os.getpid(), 'PRECISION', ctx.prec, 'THREADS', ctx.threads, flush=True)
    raw = Path(args.certificate).read_bytes()
    cert = json.loads(raw, parse_float=str)
    g = Integrand(cert)
    print('EXACT', json.dumps(g.exact), 'H', g.H.str(45), flush=True)
    J, stats = integrate(g, arb(args.tol), args.order)
    B = g.H+J
    target = arb(args.target)
    passed = B < target
    result = {'status': 'PASS' if passed else 'FAIL', 'target': args.target, 'precision_bits': ctx.prec,
        'taylor_order': args.order, 'integration_tolerance': args.tol,
        'certificate_sha256': hashlib.sha256(raw).hexdigest(), 'exact': g.exact,
        'H': endpoints(g.H), 'J': endpoints(J), 'B': endpoints(B),
        'B_ball': B.str(50), 'panels': stats, 'controls': {}}
    if args.controls:
        result['controls'] = controls(cert, g, args.order)
        false_target = arb('0.2519923409')
        require(B > false_target, 'false target not rigorously contradicted')
        result['controls']['false_target'] = {'status':'PASS', 'target': '0.2519923409',
            'decision':'REJECT', 'reason':'target is strictly below the rigorous lower endpoint of B'}
    result['elapsed_ns'] = time.monotonic_ns()-begin
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2), flush=True)
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
