#!/usr/bin/env python3
"""Clean-room referee check for the clause 4*pen(x)^2 + T(y) + hep(z) of OEIS A270594(ii).

T(y) = y(y+1)/2, pen(x) = x(3x+1)/2, hep(z) = z(5z+3)/2, x, y, z over all integers.
Exact Python integers only (no floats). Stdlib only.

Usage: python3 referee_check.py [--limit L] [--seed S]
"""
import argparse
import math
import random
import sys

N_CLAIM = 1_782_381


def T(y):
    return y * (y + 1) // 2


def pen(x):
    return x * (3 * x + 1) // 2


def hep(z):
    return z * (5 * z + 3) // 2


def is_tri(t):
    """t >= 0 is triangular iff 8t+1 is a perfect square. Returns y >= 0 with T(y) = t, else None."""
    if t < 0:
        return None
    s = math.isqrt(8 * t + 1)
    if s * s != 8 * t + 1:
        return None
    y = (s - 1) // 2
    assert T(y) == t
    return y


def int_range(f, n):
    """All integers k (both signs) with f(k) <= n, for f = pen or hep (quadratics with positive
    leading coefficient, nonnegative on Z). Walk outward from 0 in both directions until f > n."""
    ks = []
    k = 0
    while f(k) <= n:
        ks.append(k)
        k += 1
    k = -1
    while f(k) <= n:
        ks.append(k)
        k -= 1
    return ks


def xs_for(n, xsign="all"):
    xs = [x for x in int_range(pen, n) if 4 * pen(x) ** 2 <= n] if n >= 0 else []
    # int_range(pen, n) is a superset (pen(x)<=n is implied by 4pen^2<=n when pen>=1); filter is exact.
    # but pen(x) <= n may stop before 4*pen(x)^2 > n only if pen(x) > n, which implies 4pen^2 > n. OK.
    if xsign == "nonneg":
        xs = [x for x in xs if x >= 0]
    return xs


def zs_for(n, zsign="all"):
    zs = int_range(hep, n)
    if zsign == "nonneg":
        zs = [z for z in zs if z >= 0]
    return zs


def find_reps(n, xsign="all", zsign="all", first_only=False):
    """Direct enumeration: every integer x, z with 4pen(x)^2 <= n, hep(z) <= n; test remainder triangular.
    Returns list of (x, y, z) with y >= 0 (T(y) = T(-1-y), so y<0 adds nothing new)."""
    out = []
    for x in xs_for(n, xsign):
        a = 4 * pen(x) ** 2
        for z in zs_for(n - a, zsign):
            y = is_tri(n - a - hep(z))
            if y is not None:
                out.append((x, y, z))
                if first_only:
                    return out
    return out


def sieve(limit, xsign="all", zsign="all"):
    """Bitset sieve over 0..limit: bit m set iff m = 4pen(x)^2 + T(y) + hep(z). Exact big-int bit ops."""
    mask = (1 << (limit + 1)) - 1
    tri = 0
    y = 0
    while T(y) <= limit:
        tri |= 1 << T(y)
        y += 1
    a_vals = sorted({4 * pen(x) ** 2 for x in xs_for(limit, xsign)})
    b = 0
    for a in a_vals:
        b |= tri << a
    b &= mask
    h_vals = sorted({hep(z) for z in zs_for(limit, zsign)})
    rep = 0
    for h in h_vals:
        rep |= b << h
    rep &= mask
    return rep, a_vals, h_vals


def unrepresented(rep, limit):
    inv = ~rep & ((1 << (limit + 1)) - 1)
    out = []
    while inv:
        low = inv & -inv
        out.append(low.bit_length() - 1)
        inv ^= low
    return out


def check(xyz, m):
    x, y, z = xyz
    return 4 * pen(x) ** 2 + T(y) + hep(z) == m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=2_000_000)
    ap.add_argument("--seed", type=int, default=20261127)
    args = ap.parse_args()
    n = N_CLAIM
    L = max(args.limit, n)

    print("== 0. Ranges at n ==")
    xs = xs_for(n)
    zs = zs_for(n)
    print(f"x values with 4pen(x)^2 <= n: {len(xs)}  min {min(xs)} max {max(xs)}  negatives: {sum(1 for x in xs if x < 0)}")
    print(f"z values with hep(z) <= n:    {len(zs)}  min {min(zs)} max {max(zs)}  negatives: {sum(1 for z in zs if z < 0)}")
    # coverage sanity: the next value out on each side exceeds n
    assert 4 * pen(max(xs) + 1) ** 2 > n and 4 * pen(min(xs) - 1) ** 2 > n
    assert hep(max(zs) + 1) > n and hep(min(zs) - 1) > n
    # pen, hep nonnegative on all of Z (roots of x(3x+1), z(5z+3) lie in (-1, 0])
    assert all(pen(k) >= 0 and hep(k) >= 0 for k in range(-5000, 5001))

    print("\n== 1. Direct check of n = 1,782,381 ==")
    pairs = sum(len(zs_for(n - 4 * pen(x) ** 2)) for x in xs)
    reps = find_reps(n)
    print(f"(x, z) pairs tested: {pairs}; representations found: {len(reps)} {reps[:5]}")
    # Brute-force variant independent of int_range: wide fixed box, ignoring the bounds logic
    box_hits = 0
    for x in range(-40, 41):
        a = 4 * pen(x) ** 2
        if a > n:
            continue
        for z in range(-1000, 1001):
            r = n - a - hep(z)
            if r >= 0 and is_tri(r) is not None:
                box_hits += 1
    print(f"wide-box brute force (x in [-40,40], z in [-1000,1000]) hits: {box_hits}")
    # Third route, no triangular test: loop y and z, check whether the remainder is 4*p^2 with p a
    # generalized pentagonal number (p = pen(x) for some integer x iff 24p+1 is a square).
    alt_hits = 0
    y = 0
    while T(y) <= n:
        for z in zs:
            r = n - T(y) - hep(z)
            if r >= 0 and r % 4 == 0:
                p = math.isqrt(r // 4)
                if p * p == r // 4 and math.isqrt(24 * p + 1) ** 2 == 24 * p + 1:
                    alt_hits += 1
        y += 1
    print(f"y,z loop with generalized-pentagonal test on the remainder: hits {alt_hits} (y in [0,{y-1}])")

    print(f"\n== 2. Sieve over 0..{L} (all integers x, y, z) ==")
    rep, a_vals, h_vals = sieve(L)
    bad = unrepresented(rep, L)
    print(f"distinct 4pen^2 values: {len(a_vals)}, distinct hep values: {len(h_vals)}")
    print(f"unrepresented m in [0, {L}]: {len(bad)} -> {bad[:20]}")
    print(f"smallest unrepresented: {bad[0] if bad else None}; equals claim: {bool(bad) and bad[0] == n}")
    print(f"unrepresented below n: {sum(1 for m in bad if m < n)}")
    # cross-check sieve against direct enumeration on 0..20000 and on n-200..n+200
    mism = 0
    for m in list(range(0, 20001)) + list(range(n - 200, n + 201)):
        d = bool(find_reps(m, first_only=True))
        s = bool((rep >> m) & 1)
        mism += d != s
    print(f"sieve vs direct on 0..20000 and n+-200: mismatches {mism}")
    for m in [0, 1, 2, 3, n - 1, n + 1]:
        w = find_reps(m, first_only=True)
        print(f"witness m={m}: (x,y,z)={w[0] if w else None} ok={check(w[0], m) if w else None}")

    print("\n== 3. Controls ==")
    rng = random.Random(args.seed)
    ctrl = sorted(rng.randrange(0, n) for _ in range(25))
    allok = True
    for m in ctrl:
        w = find_reps(m, first_only=True)
        ok = bool(w) and check(w[0], m)
        allok &= ok
        print(f"  m={m:>8} (x,y,z)={w[0] if w else None} 4pen^2={4*pen(w[0][0])**2 if w else ''} T={T(w[0][1]) if w else ''} hep={hep(w[0][2]) if w else ''} ok={ok}")
    print(f"all {len(ctrl)} random controls represented with checked witness: {allok}")
    # negative-branch use: values below n that need a negative x or negative z
    rep_xnn, _, _ = sieve(n, xsign="nonneg")
    rep_znn, _, _ = sieve(n, zsign="nonneg")
    full_n = rep & ((1 << (n + 1)) - 1)
    need_negx = unrepresented(rep_xnn, n)
    need_negz = unrepresented(rep_znn, n)
    nx = [m for m in need_negx if (full_n >> m) & 1]
    nz = [m for m in need_negz if (full_n >> m) & 1]
    print(f"m <= n represented only with some x < 0: {len(nx)} (first {nx[:5]})")
    for m in nx[:3]:
        w = find_reps(m)
        print(f"   m={m} all reps {w}")
    print(f"m <= n represented only with some z < 0: {len(nz)} (first {nz[:5]})")
    for m in nz[:3]:
        w = find_reps(m)
        print(f"   m={m} all reps {w}")

    print("\n== 4. Other readings ==")
    print("natural numbers from 1: 0 = 4pen(0)^2+T(0)+hep(0) is represented, so the smallest exception is unchanged.")
    rep_nn, _, _ = sieve(n, xsign="nonneg", zsign="nonneg")
    bad_nn = unrepresented(rep_nn, n)
    print(f"x, y, z >= 0 only: {len(bad_nn)} unrepresented in [0, n], first 10: {bad_nn[:10]}")
    print(f"x >= 0 only (z all): first 10 unrepresented: {need_negx[:10]} (count {len(need_negx)})")
    print(f"z >= 0 only (x all): first 10 unrepresented: {need_negz[:10]} (count {len(need_negz)})")
    print("y sign: T(y) = T(-1-y), so restricting y >= 0 changes nothing.")


if __name__ == "__main__":
    sys.exit(main())
