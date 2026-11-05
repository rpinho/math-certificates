"""Publication arithmetic of round-10 ablations, conditional on its stated premises.

Adapted from round10/frozen_final/verify_b.py's integer recurrence, with switches
for the two degree-six ceilings. This computes scalar sensitivities and decimal
renderings; it neither rechecks the finite classification inputs nor supplies a
clean-room replay. All calculations are integer/rational, including rounding.
"""
from fractions import Fraction as Q
import json


def recurrence(first=True, second=True, first_cap=12):
    previous = {1: 1, 2: 4, 3: 10, 4: 22}
    for d in range(5, 97):
        k = d - 1
        G = 1 << (d - 2)
        square = G * G
        C = previous[k]
        B = max([G] + [G // 2 + (previous[t] + 1) * (1 << (d-t-2)) for t in range(1, k)])
        zmax = (2*d*square) // (6*G-2)
        low = {2*G-(G >> j) for j in range(k)}
        test = set(low) | {2*G}
        for a in range(4*k, (2*k*zmax)//G+2):
            start = (a*G+2*k-1)//(2*k)
            test.update((start, start+1))
            test.add(((2*a+1)*G+4*k-1)//(4*k))
        for a in range((4*k*zmax)//(3*G)+2):
            start = (3*a*G+4*k-1)//(4*k)
            if start >= 2*G:
                test.update((start, start+1))
        for integer in range(2, zmax//G+1):
            test.add(integer*G)
        test = {z for z in test if G <= z <= zmax and (z >= 2*G or z in low)}

        def at(z):
            h = (2*k*z)//G
            if z % G and (2*k*z) % G == 0:
                h -= 1
            if d == 5 and 2*z == 3*G:
                h = min(h, 10)
            if first and d == 6 and 2*z == 3*G:
                h = min(h, first_cap)
            if second and d == 6 and 4*z == 7*G:
                h = min(h, 13)
            if k >= 3 and z > G and 4*k*z-2*h*G < G:
                h -= 1
            cut = min(h, (4*k*z)//(3*G))
            best = -1
            for t in (cut, h):
                numerator = (2*C+t+1)*square-C*z
                if z > G and 3*t*G > 4*k*z:
                    numerator += min(0, (2*B-C-2*G)*G)
                best = max(best, min(numerator//square, (2*d*square)//z))
            return best
        previous[d] = max(at(z) for z in test)
    return Q(previous[96]+9508, 1 << 96), previous


def fixed(q, places, upward=False):
    scale = 10**places
    x = q*scale
    n = -((-x.numerator)//x.denominator) if upward else (x+Q(1, 2)).numerator//(x+Q(1, 2)).denominator
    s = str(n).zfill(places+1)
    return s[:-places]+'.'+s[-places:]


def main():
    base, bcounts = recurrence()
    fallback, fcounts = recurrence(False, False)
    dropfirst, _ = recurrence(False, True)
    dropsecond, _ = recurrence(True, False)
    partial, pcounts = recurrence(True, True, first_cap=13)
    assert base == Q(79671833529611582591986228957, 2**95)
    assert fallback == Q(161352209230323853459003893907, 2**96)
    assert fallback == dropfirst == dropsecond
    assert bcounts[6] == 107 and fcounts[6] == 109 and pcounts[6] == 108
    print(json.dumps({'scope': 'conditional round-10 scalar recurrence only; no new bound or proof replay',
                      'base': str(base), 'base_nearest_5dp': fixed(base, 5),
                      'fallback': str(fallback), 'fallback_up_10dp': fixed(fallback, 10, True),
                      'fallback_nearest_4dp': fixed(fallback, 4), 'fallback_nearest_5dp': fixed(fallback, 5),
                      'partial': str(partial), 'partial_nearest_5dp': fixed(partial, 5),
                      'R6': [bcounts[6], fcounts[6], pcounts[6]]}, indent=2))


if __name__ == '__main__':
    main()
