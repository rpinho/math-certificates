#!/usr/bin/env python3
"""Independent exact/Arb replay of the supplied C82 certificate."""
import argparse
import hashlib
import json
import os
import sys
import time
from fractions import Fraction
from flint import arb, acb, fmpz_poly, acb_poly, ctx


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a, b):
    return a // gcd(a, b) * b


def ball(q):
    q = Fraction(q)
    return arb(q.numerator) / q.denominator


def validate(cert):
    rows = []
    denominators = []
    numerators = []
    D = 0
    a = Fraction(0)
    b = 1
    for kind in ('denominator', 'numerator'):
        for row in cert[kind]:
            c = row['coeffs']
            if not isinstance(c, list) or not c or any(type(x) is not int for x in c) or not c[0]:
                raise ValueError('nonzero canonical integer coefficients required')
            p = fmpz_poly(c[::-1])
            if kind == 'denominator':
                m = row['multiplicity']
                if c[0] != 1 or p.degree() < 1 or type(m) is not int or m <= 0:
                    raise ValueError('denominator must be monic, nonconstant, positive integer multiplicity')
                D += m * p.degree()
                denominators.append((p, m))
                rows.append((row['name'], p, Fraction(-m), True))
            else:
                if not isinstance(row['q_rational'], str):
                    raise ValueError('rational exponent must be an exact string')
                q = Fraction(row['q_rational'])
                if q < 0:
                    raise ValueError('negative exponent')
                if q:
                    a += q * p.degree()
                    b = lcm(b, q.denominator)
                    numerators.append((p, q))
                    rows.append((row['name'], p, q, False))
    if not denominators or not a < D:
        raise ValueError('strict degree condition failed')
    pairs = 0
    for s, q in numerators:
        for r, m in denominators:
            if s.gcd(r) != 1:
                raise ValueError('active numerator and denominator not coprime')
            pairs += 1
    facts = {'D': str(D), 'a': str(a), 'a_over_D': str(a / D),
             'degree_gap': str(D-a), 'b': str(b), 'active_gcd_pairs': pairs,
             'denominators': len(denominators), 'active_numerators': len(numerators)}
    return rows, D, facts


class Construction:
    def __init__(self, cert):
        rows, self.D, self.facts = validate(cert)
        self.factors = []
        self.roots = []
        self.H = arb(0)
        self.constant = arb(0)
        T = fmpz_poly([0, 1, -1])
        count = 0
        for name, p, w, isden in rows:
            start = time.monotonic_ns()
            comp = p(T)
            roots = comp.complex_roots()
            if sum(m for r, m in roots) != comp.degree():
                raise ValueError('incomplete certified roots')
            lead = abs(int(comp.leading_coefficient()))
            lm = arb(lead).log()
            wnorm = ball(w / self.D)
            unit_possible = 0
            for r, m in roots:
                if not r.is_finite():
                    raise ValueError('nonfinite root')
                modulus = abs(r)
                lm += m * modulus.max(1).log()
                if modulus.contains(1):
                    unit_possible += m
                self.roots.append((r, wnorm * m))
            if isden:
                if unit_possible:
                    raise ValueError('denominator root possibly on unit circle')
                self.H -= wnorm * lm
            self.constant += wnorm * arb(lead).log()
            self.factors.append((acb_poly(comp), wnorm, isden))
            count += sum(m for r, m in roots)
            print(json.dumps({'factor': name, 'degree': comp.degree(),
                              'possible_unit_roots': unit_possible,
                              'milliseconds': (time.monotonic_ns()-start)//1000000}), flush=True)
        self.facts['composed_roots'] = count
        print('H',self.H.str(60), flush=True)

    def root_g(self, t):
        z = (acb(0, 2 * arb.pi()) * t).exp()
        v = self.constant
        for r, w in self.roots:
            v += w * abs(z-r).log()
        return v

    def poly_g(self, t):
        z = (acb(0, 2 * arb.pi()) * t).exp()
        v = arb(0)
        for p, w, isden in self.factors:
            v += w * abs(p(z)).log()
        return v

    def upper_g(self, left, right):
        """Finite upper bound, including numerator logarithmic singularities."""
        t = arb((left + right)/2, (right-left)/2)
        z = (acb(0, 2 * arb.pi()) * t).exp()
        v = self.constant
        for r, w in self.roots:
            d = abs(z-r)
            if w > 0:
                if not d.upper() > 0:
                    return arb('-inf')
                v += w * d.upper().log()
            else:
                if not d.lower() > 0:
                    return arb('inf')
                v += w * d.lower().log()
        return v.upper()

    def panel(self, left, right, order):
        """Range and signed integral of g; None if the local series cannot apply."""
        mid = (left + right)/2
        h = (right-left)*arb.pi()
        z = (acb(0, 2*arb.pi())*mid).exp()
        local = []
        for r, w in self.roots:
            d = z-r
            if not abs(d).lower() > 0:
                return None
            p = z/d
            rho = abs(p)*h
            if not rho < ball(Fraction(3, 4)):
                return None
            local.append((d, p, rho, w))
        value = self.constant
        coeff = [acb(0) for _ in range(order+1)]
        tail = arb(0)
        for d, p, rho, w in local:
            value += w*abs(d).log()
            power = acb(w)
            for k in range(1, order+1):
                power *= p
                coeff[k] += power
            tail += abs(w)*rho**(order+1)/((order+1)*(1-rho))
        for k in range(1, order+1):
            coeff[k] *= Fraction((-1)**(k+1), k).numerator
            coeff[k] /= k
        eps = arb(0, tail.upper())
        delta = acb(0, arb(0, h.upper())).exp()-1
        v = coeff[order]
        for k in range(order-1, 0, -1):
            v = v*delta + coeff[k]
        enclosure = value + (v*delta).real + eps
        # Integrate only when the panel is certified positive.
        if not enclosure > 0:
            return enclosure, None
        average = value
        for k, moment in enumerate(moments(h, order)):
            if k:
                average += coeff[k].real*moment
        integral = (right-left)*(average+eps)
        return enclosure, integral


_moment_coefficients = {}


def moments(h, order):
    """Rigorous normalized integrals of (exp(i*delta)-1)^k on [-h,h]."""
    limit = 2*order+32
    if order not in _moment_coefficients:
        stirling = [[0]*(order+1) for _ in range(limit+1)]
        stirling[0][0] = 1
        factorial = [1]
        for n in range(1, limit+2):
            factorial.append(factorial[-1]*n)
            if n <= limit:
                for k in range(1, min(n, order)+1):
                    stirling[n][k] = k*stirling[n-1][k]+stirling[n-1][k-1]
        cs = []
        for k in range(order+1):
            cs.append([(n, Fraction((-1)**(n//2)*factorial[k]*stirling[n][k],
                                     factorial[n]*(n+1)))
                       for n in range(2, limit+1, 2) if n >= k])
        _moment_coefficients[order] = (cs, factorial[limit+1])
    cs, fac = _moment_coefficients[order]
    powers = [arb(1)]
    for n in range(1, limit+1):
        powers.append(powers[-1]*h)
    yield arb(1)
    for k in range(1, order+1):
        value = sum((powers[n]*ball(c) for n, c in cs[k]), arb(0))
        rem = (1 << k)*(k*h).exp()*(k*h)**(limit+1)/fac
        yield value+arb(0, rem.upper())


def integrate(obj, tol, order):
    # Real integer polynomials give g(1-t)=g(t).
    stack = [(arb(0), arb(1)/2, 0)]
    result = arb(0)
    stats = {'visited': 0, 'negative_series': 0, 'negative_distance': 0,
             'positive': 0, 'unresolved_bounded': 0, 'max_depth': 0}
    start = time.monotonic_ns()
    last = start
    while stack:
        left, right, depth = stack.pop()
        stats['visited'] += 1
        stats['max_depth'] = max(stats['max_depth'], depth)
        panel = obj.panel(left, right, order)
        contribution = None
        if panel is None:
            upper = obj.upper_g(left, right)
            if upper <= 0:
                contribution = arb(0)
                stats['negative_distance'] += 1
        else:
            enclosure, signed = panel
            if enclosure <= 0:
                contribution = arb(0)
                stats['negative_series'] += 1
            elif signed is not None and signed.rad() <= tol*(right-left):
                contribution = signed
                stats['positive'] += 1
            elif enclosure.is_finite():
                upper = enclosure.upper().max(0)
                lower = enclosure.lower().max(0)
                rough = arb(lower).union(upper)*(right-left)
                if rough.rad() <= tol*(right-left):
                    contribution = rough
                    stats['unresolved_bounded'] += 1
        if contribution is None:
            if depth >= 100:
                raise ValueError('maximum subdivision depth reached')
            mid = (left+right)/2
            stack.extend(((mid, right, depth+1), (left, mid, depth+1)))
        else:
            result += contribution
        now = time.monotonic_ns()
        if now-last > 30000000000:
            print('quadrature',json.dumps(stats),'elapsed_seconds',(now-start)//1000000000,
                  'pending',len(stack),'J_partial',(2*result).str(30),flush=True)
            last = now
    return 2*result, stats


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', nargs='?', default='inputs/certificates/certificate.json')
    parser.add_argument('--prec', type=int, default=256)
    parser.add_argument('--target', default='0.2519744488')
    parser.add_argument('--roots-only', action='store_true')
    parser.add_argument('--tol', default='1e-22')
    parser.add_argument('--order', type=int, default=16)
    args = parser.parse_args()
    if args.prec < 192:
        raise ValueError('at least 192 bits required')
    ctx.prec = args.prec
    ctx.threads = 1
    print('PID',os.getpid(),'precision',ctx.prec,flush=True)
    with open(args.certificate) as f:
        cert = json.load(f, parse_float=str)
    obj = Construction(cert)
    print(json.dumps(obj.facts,sort_keys=True), flush=True)
    for j in (1, 7, 17, 37, 71, 127):
        t = arb(j)/257
        gr = obj.root_g(t)
        gp = obj.poly_g(t)
        print('probe',j,gr.str(25),gp.str(25),'overlap',gr.overlaps(gp),flush=True)
    if args.roots_only:
        return
    J, stats = integrate(obj, arb(args.tol), args.order)
    B = obj.H + J
    print('J', J.str(60), flush=True)
    print('B', B.str(60), flush=True)
    print('quadrature_final', json.dumps(stats),flush=True)
    print('PASS' if B < ball(Fraction(args.target)) else 'FAIL',flush=True)


if __name__ == '__main__':
    main()
