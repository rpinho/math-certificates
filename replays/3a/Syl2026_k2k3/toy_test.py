#!/usr/bin/env python3
"""Brute-force test of the three combinatorial inequalities used by ghr_check.py, on toy parameters.
   M = <2,3> ∩ [0,B], q even > B, block length k, ell blocks, type N_r = floor(ell x^c(r) / Z), N_h = 0.
   U = { sum_j a_j q^j : a_j in M, sum a_j <= L }, L = C/2.
   Checks: |U-U| >= ell!/(N_0! prod N_r!) ; |U+U| <= x^{-C} P(x)^{k ell} ; |U-U| < 2 max U + 1."""
import itertools, math, sys
from fractions import Fraction

def run(gens, B, q, k, ell, x):
    ok = [False] * (B + 1); ok[0] = True
    for n in range(1, B + 1):
        ok[n] = any(n >= g and ok[n - g] for g in gens)
    M = [n for n in range(B + 1) if ok[n]]
    Q = q ** k
    kap = {}
    for a in M:
        for b in M:
            s = a + b; d = a - b
            if d not in kap or s < kap[d]: kap[d] = s
    Dl = sorted(kap)
    # c_k(r) by definition
    c = {}
    for ds in itertools.product(Dl, repeat=k):
        r = sum(d * q ** i for i, d in enumerate(ds)) % Q
        s = sum(kap[d] for d in ds)
        if r not in c or s < c[r]: c[r] = s
    assert len(c) == Q, 'not all residues covered'
    h = Q // 2 if Q % 2 == 0 else -1
    Z = sum(x ** c[r] for r in range(Q))
    N = {}
    for r in range(Q):
        if r in (0, h): continue
        N[r] = math.floor(ell * x ** c[r] / Z)
    assert all(N[r] == N[(-r) % Q] for r in N)
    n0 = ell - sum(N.values())
    assert n0 >= 0
    C = sum(N[r] * c[r] for r in N)
    assert C % 2 == 0, C
    L = C // 2
    nd = k * ell
    # U by DP over digits: set of values with digit sum <= L
    cur = {0: 0}   # value -> min digit sum
    for j in range(nd):
        nxt = {}
        for v, s in cur.items():
            for a in M:
                s2 = s + a
                if s2 > L: break
                v2 = v + a * q ** j
                if v2 not in nxt or s2 < nxt[v2]: nxt[v2] = s2
        cur = nxt
    U = sorted(cur)
    Us = set(U)
    UU = {a + b for a in U for b in U}
    UD = {a - b for a in U for b in U}
    P = sum(x ** s for s in {a + b for a in M for b in M})
    lnM = math.lgamma(ell + 1) - math.lgamma(n0 + 1) - sum(math.lgamma(N[r] + 1) for r in N)
    lnS = -C * math.log(x) + nd * math.log(P)
    r1 = len(UD) >= math.exp(lnM) * (1 - 1e-9)
    r2 = len(UU) <= math.exp(lnS) * (1 + 1e-9)
    r3 = (max(U) == 0) or len(UD) < 2 * max(U) + 1
    return dict(M=len(M), L=L, C=C, n0=n0, U=len(U), UD=len(UD), UU=len(UU), calM=math.exp(lnM), S=math.exp(lnS), ok_diff=r1, ok_sum=r2, ok_range=r3)

DEFAULT = [([1], 3, 4, 1, 8, 0.9), ([1], 3, 4, 1, 9, 0.8), ([2, 3], 5, 6, 1, 7, 0.9), ([2, 3], 5, 6, 1, 8, 0.7)]

if __name__ == '__main__':
    allok = True
    import ast
    cases = ast.literal_eval(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    for (gens, B, q, k, ell, x) in cases:
        r = run(gens, B, q, k, ell, x)
        print((gens, B, q, k, ell, x), r)
        allok &= r['ok_diff'] and r['ok_sum'] and r['ok_range']
    print('ALL OK' if allok else 'FAILURE')
