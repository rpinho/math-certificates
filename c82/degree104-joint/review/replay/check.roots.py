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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', nargs='?', default='inputs/certificates/certificate.json')
    parser.add_argument('--prec', type=int, default=256)
    parser.add_argument('--target', default='0.2519744488')
    parser.add_argument('--roots-only', action='store_true')
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
    raise NotImplementedError('quadrature not yet implemented')


if __name__ == '__main__':
    main()
