#!/usr/bin/env python3
"""Check OEIS A270594(ii) at an explicit integer, or verify its first hole.

This program has no imports from the search. For a single n it evaluates the
original form directly, using 8*t+1 to decide if a remainder is triangular.
"""
import argparse
from math import isqrt


N = 1_782_381


def pentagonal_square_times_four(x):
    return (x * (3*x+1))**2


def heptagonal(z):
    return z*(5*z+3)//2


def witnesses(n):
    tested = 0
    answers = []
    # For |x|>=1, |x(3x+1)| >= 2*x*x.
    x_limit = isqrt(isqrt(n)//2)
    # For |z|>=1, z(5z+3)/2 >= z*z.
    for x in range(-x_limit, x_limit+1):
        a = pentagonal_square_times_four(x)
        if a > n:
            continue
        z_limit = isqrt(n-a)
        for z in range(-z_limit, z_limit+1):
            leftover = n-a-heptagonal(z)
            if leftover < 0:
                continue
            tested += 1
            discriminant = 8*leftover+1
            root = isqrt(discriminant)
            if root*root == discriminant:
                y = (root-1)//2
                # y and -1-y produce the same triangular number.
                answers.extend(((x,y,z), (x,-y-1,z)))
    return tested, answers


def first_missing(bound):
    # Independent finite coverage check. Every set is mapped to a Python
    # integer with bit k representing k. Nonnegative indices give all
    # triangular values because T(-1-y) = T(y).
    triangular = sum(1 << (y*(y+1)//2)
                     for y in range(isqrt(2*bound)+1) if y*(y+1)//2 <= bound)
    mask = (1 << (bound+1))-1
    pair = 0
    for z in range(-isqrt(bound),isqrt(bound)+1):
        h = heptagonal(z)
        if h <= bound:
            pair |= (triangular << h) & mask
    all_sums = 0
    limit = isqrt(isqrt(bound)//2)
    for x in range(-limit,limit+1):
        f = pentagonal_square_times_four(x)
        if f <= bound:
            all_sums |= (pair << f) & mask
    missing = mask ^ all_sums
    return (missing & -missing).bit_length()-1 if missing else None, missing.bit_count()


def check_literal():
    # For these two displayed formulas, every nonzero y gives a contribution
    # of at least 3, and every |z|>=1 contributes at least 1. Enumerate the
    # full possible range using the respective expression and a safe bound.
    for n, mode in ((2,1), (4,2)):
        def f(y):
            pent = y*(3*y+1)//2
            return pent*pent+2*pent if mode == 1 else 2*pent*pent+y*(y+1)//2
        got = [(y,z) for y in range(-n,n+1) for z in range(-n,n+1)
               if f(y)+z*(3*z+2) == n]
        if got:
            raise SystemExit(f'Literal clause {mode} has a witness {got}')
        print(f'Literal clause {mode}: {n}, zero representations')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--minimality', action='store_true')
    parser.add_argument('--literal', action='store_true')
    args = parser.parse_args()
    for n in (N-1, N, N+1):
        tested, answers = witnesses(n)
        print(f'{n}: {tested} admissible (x,z) pairs, {len(answers)} witnesses, first={answers[:1]}')
        if bool(answers) != (n != N):
            raise SystemExit('Unexpected direct-check result')
    if args.minimality:
        first, count = first_missing(N)
        print(f'[0,{N}]: {count} missing, first={first}')
        if (first,count) != (N,1):
            raise SystemExit('Unexpected interval result')
    if args.literal:
        check_literal()
