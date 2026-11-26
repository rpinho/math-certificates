#!/usr/bin/env python3
r"""
Clean-room standalone exact integer verifier for Banerjee-Smoot (arXiv:2611.09681v1),
Section 6, Conjecture 6.1 (\label{conj:families}).

Zero external dependencies (Python standard library only).

Computes coefficients of
    P_{a,b}(q) = (-q;q)_inf^a / (q;q)_inf^b = prod_{m>=1} (1 + q^m)^a (1 - q^m)^{-b}
where b=1 gives P^{[1]}_a(q) and b=5 gives P^{[2]}_a(q), using independent exact integer methods:
  - Method A1 (elementary truncated product): factor-by-factor shift/add passes for
    prod_{m=1}^N (1 + q^m)^a (1 - q^m)^{-b} mod q^{N+1}.
  - Method A2 (factored truncated product): expands single factor U(x) = (1+x)^a (1-x)^{-b}
    and multiplies prod_{m=1}^N U(q^m) mod q^{N+1} in O(N^2) exact integer arithmetic.
  - Method B (Euler logarithmic-derivative recurrence):
    n * c_n = sum_{k=1}^n s_{a,b}(k) * c_{n-k}, where
    s_{a,b}(k) = sum_{m | k} m * (b + a * (-1)^{(k//m) - 1}).
  - Method C (Euler pentagonal recurrence grid scanner): steps a -> a +- 1 via
    (-q;q)_inf = (q^2;q^2)_inf / (q;q)_inf using generalized pentagonal numbers,
    enabling fast exact scan over a in [-50, 100], alpha in {1, 2, 3}, n in {0..5},
    with key series and minimal/claimed counterexamples independently cross-verified
    by Methods A and B.
"""


import gzip
import json

def _gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

def _comb(n, k):
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    r = 1
    for i in range(1, k + 1):
        r = r * (n - k + i) // i
    return r
import os
import resource
import sys
import time
from typing import Dict, List, Optional, Tuple


def get_peak_rss_mib() -> int:
    ru = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return ru // (1024 * 1024)
    return ru // 1024


# ---------------------------------------------------------------------------
# Method A: Direct Truncated Product Multiplication
#   prod_{m=1}^N (1 + q^m)^a (1 - q^m)^{-b} mod q^{N+1}
# ---------------------------------------------------------------------------

def series_product_elementary(a: int, b: int, n_max: int) -> List[int]:
    """
    Pure elementary factor-by-factor truncated product expansion of
    prod_{m=1}^{n_max} (1 + q^m)^a (1 - q^m)^{-b} mod q^{n_max + 1}.
    """
    if b < 0:
        raise ValueError("Expected non-negative b in denominator (q;q)_inf^b")
    c = [0] * (n_max + 1)
    c[0] = 1
    for m in range(1, n_max + 1):
        if a > 0:
            for _ in range(a):
                for k in range(n_max, m - 1, -1):
                    c[k] += c[k - m]
        elif a < 0:
            for _ in range(-a):
                for k in range(m, n_max + 1):
                    c[k] -= c[k - m]
        for _ in range(b):
            for k in range(m, n_max + 1):
                c[k] += c[k - m]
    return c


def series_product_factored(a: int, b: int, n_max: int) -> List[int]:
    """
    Direct truncated product prod_{m=1}^{n_max} U(q^m) mod q^{n_max + 1},
    where U(x) = (1 + x)^a (1 - x)^{-b} mod x^{n_max + 1}.
    Complexity is (pi^2 / 12) * n_max^2 exact integer ops independent of |a|, b.
    """
    # Expand 1-variable factor U(x) = (1 + x)^a (1 - x)^{-b} mod x^{n_max + 1}
    u = [0] * (n_max + 1)
    u[0] = 1
    if a > 0:
        for _ in range(a):
            for j in range(n_max, 0, -1):
                u[j] += u[j - 1]
    elif a < 0:
        for _ in range(-a):
            for j in range(1, n_max + 1):
                u[j] -= u[j - 1]
    for _ in range(b):
        for j in range(1, n_max + 1):
            u[j] += u[j - 1]

    # Multiply prod_{m=1}^{n_max} U(q^m) mod q^{n_max + 1}
    c = [0] * (n_max + 1)
    c[0] = 1
    for m in range(1, n_max + 1):
        max_j = n_max // m
        if max_j == 1:
            u1 = u[1]
            if u1 != 0:
                for k in range(n_max, m - 1, -1):
                    c[k] += u1 * c[k - m]
        else:
            for k in range(n_max, m - 1, -1):
                acc = c[k]
                jm = m
                j = 1
                while jm <= k:
                    acc += u[j] * c[k - jm]
                    j += 1
                    jm += m
                c[k] = acc
    return c


# ---------------------------------------------------------------------------
# Method B: Euler Logarithmic-Derivative Divisor-Sum Recurrence
#   q * F'(q) / F(q) = sum_{k>=1} s_{a,b}(k) q^k
#   n * c_n = sum_{k=1}^n s_{a,b}(k) * c_{n-k}
# ---------------------------------------------------------------------------

def series_logderiv(a: int, b: int, n_max: int) -> List[int]:
    """
    Computes [q^0 .. q^{n_max}] of (-q;q)_inf^a / (q;q)_inf^b via Euler's
    logarithmic-derivative recurrence with exact integer division check.
    """
    s = [0] * (n_max + 1)
    for m in range(1, n_max + 1):
        r = 1
        for k in range(m, n_max + 1, m):
            # (-1)^{r-1} is +1 when r is odd, -1 when r is even
            sign = 1 if (r & 1) else -1
            s[k] += m * (b + a * sign)
            r += 1

    c = [0] * (n_max + 1)
    c[0] = 1
    for n in range(1, n_max + 1):
        total = 0
        for k in range(1, n + 1):
            total += s[k] * c[n - k]
        if total % n != 0:
            raise AssertionError(f"Non-integral division at n={n} for (a={a}, b={b})")
        c[n] = total // n
    return c


# ---------------------------------------------------------------------------
# Method C: Euler Pentagonal Number Theorem Grid Scanner
#   (q;q)_inf = 1 + sum_{j>=1} (-1)^j (q^{j(3j-1)/2} + q^{j(3j+1)/2})
#   (-q;q)_inf = (q^2;q^2)_inf / (q;q)_inf
# ---------------------------------------------------------------------------

def pentagonal_terms(n_max: int, scale: int = 1) -> List[Tuple[int, int]]:
    """Non-zero (exponent, sign) terms of (q^scale; q^scale)_inf up to n_max."""
    terms: List[Tuple[int, int]] = []
    j = 1
    while True:
        g1 = scale * (j * (3 * j - 1) // 2)
        g2 = scale * (j * (3 * j + 1) // 2)
        if g1 > n_max:
            break
        sign = -1 if (j & 1) else 1
        terms.append((g1, sign))
        if g2 <= n_max:
            terms.append((g2, sign))
        j += 1
    return terms


def mul_sparse_eta(series: List[int], terms: List[Tuple[int, int]], n_max: int) -> List[int]:
    out = series[:]
    for n in range(n_max, 0, -1):
        acc = out[n]
        for g, sign in terms:
            if g > n:
                break
            if sign == 1:
                acc += series[n - g]
            else:
                acc -= series[n - g]
        out[n] = acc
    return out


def div_sparse_eta(series: List[int], terms: List[Tuple[int, int]], n_max: int) -> List[int]:
    out = [0] * (n_max + 1)
    out[0] = series[0]
    for n in range(1, n_max + 1):
        acc = series[n]
        for g, sign in terms:
            if g > n:
                break
            if sign == 1:
                acc -= out[n - g]
            else:
                acc += out[n - g]
        out[n] = acc
    return out


# ---------------------------------------------------------------------------
# Arithmetic Progression Helpers for Conjecture 6.1
# ---------------------------------------------------------------------------

def delta_conjecture(part: int, a: int, alpha: int) -> int:
    """
    Unique representative delta in {0, ..., 11^alpha - 1} solving:
      Part 1: 24 * delta == 1 - a (mod 11^alpha)
      Part 2: 24 * delta == 5 - a (mod 11^alpha)
    """
    mod = 11 ** alpha
    rhs = (1 - a) if part == 1 else (5 - a)
    inv24 = pow(24, -1, mod)
    return (rhs * inv24) % mod


def modulus_conjecture(alpha: int) -> int:
    """11^{ceil(alpha / 2)}."""
    return 11 ** ((alpha + 1) // 2)


def is_admissible_a(part: int, a: int) -> bool:
    r = a % 11
    if part == 1:
        return r in (3, 5, 7)
    if part == 2:
        return r not in (1, 3, 5)
    raise ValueError(f"Unknown part {part}")


def audit_verbatim_tex(tex_gz_path: str) -> Dict[str, object]:
    """Verifies verbatim presence of key lines in inputs/2611.09681v1.tex.json.gz."""
    with gzip.open(tex_gz_path, "rt", encoding="utf-8") as f:
        payload = json.load(f)
    fname, content = payload[0][0], payload[0][1]
    lines = content.splitlines()
    checks = {
        "filename": fname,
        "line_count": len(lines),
        "L140_thm12": r"\begin{theorem}\label{Thm12}" in lines[139],
        "L141_thm12_hyp": r"8n\equiv 1\pmod{11^{\alpha}}" in lines[140],
        "L783_a_in_Z": r"For $a\in\mathbb{Z}$ define $p^{[1]}_a(n)$ and $p^{[2]}_a(n)$ by" in lines[782],
        "L785_P1_def": r"P^{[1]}_a(q):=\frac{(-q;q)_\infty^a}{(q;q)_\infty}=:\sum_{n\ge0}p^{[1]}_a(n)q^n" in lines[784],
        "L787_P2_def": r"P^{[2]}_a(q):=\frac{(-q;q)_\infty^a}{(q;q)_\infty^5}=:\sum_{n\ge0}p^{[2]}_a(n)q^n" in lines[786],
        "L791_conj_label": r"\begin{conjecture}\label{conj:families}" in lines[790],
        "L792_quantifiers": r"Let $\alpha\in\mathbb{N}$ and $n\in\mathbb{N}_0$." in lines[791],
        "L794_part1_hyp": r"If $a\equiv3,5,7\pmod{11}$" in lines[793],
        "L796_part1_cong": r"24\,\delta^{[1]}_{a,\alpha}\equiv1-a\ \left(\textnormal{mod}\ 11^\alpha\right)" in lines[795],
        "L798_part2_hyp": r"If $a\not\equiv1,3,5\pmod{11}$" in lines[797],
        "L800_part2_cong": r"24\,\delta^{[2]}_{a,\alpha}\equiv5-a\ \left(\textnormal{mod}\ 11^\alpha\right)" in lines[799],
    }
    for k, v in checks.items():
        if isinstance(v, bool) and not v:
            raise AssertionError(f"Verbatim TeX check failed: {k}")
    return checks


def main() -> None:
    t0 = time.monotonic_ns()
    print("=== Clean-Room Referee Verifier: Banerjee-Smoot (arXiv:2611.09681v1) Conjecture 6.1 ===")

    # 1. Verbatim TeX check
    tex_checks = audit_verbatim_tex("inputs/2611.09681v1.tex.json.gz")
    print(f"[PASS] Verbatim TeX audit ({tex_checks['filename']}, {tex_checks['line_count']} lines): all exact definitions confirmed.")

    # 2. Verify Claimed Counterexamples via Elementary Product (A1), Factored Product (A2), and Euler Recurrence (B)
    expected_c1 = 62043410886974649205238011198
    expected_c2 = 66134580699742235651549220246110

    # Part (1): a=36, b=1, alpha=3, n=0 => delta=54, mod=121
    assert is_admissible_a(1, 36) and (36 % 11 == 3)
    d1_36_3 = delta_conjecture(1, 36, 3)
    assert d1_36_3 == 54 and (24 * 54 - (1 - 36)) % 1331 == 0
    s36_a1 = series_product_elementary(36, 1, 100)
    s36_a2 = series_product_factored(36, 1, 100)
    s36_b = series_logderiv(36, 1, 100)
    assert s36_a1 == s36_a2 == s36_b, "Method mismatch on P^{[1]}_{36}"
    c1_val = s36_a1[54]
    c1_rem = c1_val % 121
    assert c1_val == expected_c1, f"Part (1) value mismatch: got {c1_val}"
    assert c1_rem == 33, f"Part (1) mod 121 mismatch: got {c1_rem}"
    print(f"[PASS] Claimed Counterexample Part (1): a=36 (36 == 3 mod 11), alpha=3, n=0, delta={d1_36_3}")
    print(f"       p^[1]_36(54) = {c1_val}")
    print(f"       Exact match across Methods A1, A2, B; mod 121 = {c1_rem} (!= 0).")

    # Part (2): a=40, b=5, alpha=3, n=0 => delta=54, mod=121
    assert is_admissible_a(2, 40) and (40 % 11 == 7)
    d2_40_3 = delta_conjecture(2, 40, 3)
    assert d2_40_3 == 54 and (24 * 54 - (5 - 40)) % 1331 == 0
    s40_a1 = series_product_elementary(40, 5, 100)
    s40_a2 = series_product_factored(40, 5, 100)
    s40_b = series_logderiv(40, 5, 100)
    assert s40_a1 == s40_a2 == s40_b, "Method mismatch on P^{[2]}_{40}"
    c2_val = s40_a1[54]
    c2_rem = c2_val % 121
    assert c2_val == expected_c2, f"Part (2) value mismatch: got {c2_val}"
    assert c2_rem == 55, f"Part (2) mod 121 mismatch: got {c2_rem}"
    print(f"[PASS] Claimed Counterexample Part (2): a=40 (40 == 7 mod 11), alpha=3, n=0, delta={d2_40_3}")
    print(f"       p^[2]_40(54) = {c2_val}")
    print(f"       Exact match across Methods A1, A2, B; mod 121 = {c2_rem} (!= 0).")

    # 3. Positive Controls
    # 3a. Theorem 1.2: a=2, b=5 (P^{[2]}_2(q) = D_2(q)), alpha=1,2,3, n=0..5 (and n=0..20 for alpha=1)
    n_thm12 = 1331 * 5 + delta_conjecture(2, 2, 3)
    d2_series_a2 = series_product_factored(2, 5, n_thm12)
    d2_series_b = series_logderiv(2, 5, n_thm12)
    assert d2_series_a2 == d2_series_b, "Method mismatch on Theorem 1.2 series D_2(q)"
    assert d2_series_a2[:101] == series_product_elementary(2, 5, 100)

    thm12_summary = {}
    for alpha in (1, 2, 3):
        delta = delta_conjecture(2, 2, alpha)
        assert (8 * delta - 1) % (11 ** alpha) == 0
        mod = modulus_conjecture(alpha)
        max_n = 20 if alpha == 1 else (10 if alpha == 2 else 5)
        tested = []
        for n in range(max_n + 1):
            idx = (11 ** alpha) * n + delta
            val = d2_series_b[idx]
            assert val % mod == 0, f"Theorem 1.2 failed at alpha={alpha}, n={n}, idx={idx}!"
            if n <= 3:
                tested.append({"n": n, "k": idx, "val_mod": val % mod, "v11": _v11(val)})
        thm12_summary[alpha] = {"delta": delta, "mod": mod, "max_n_checked": max_n, "samples": tested}
    print(f"[PASS] Positive Control 1 (Theorem 1.2, a=2, b=5): verified for alpha=1 (n<=20, delta=7, mod 11), "
          f"alpha=2 (n<=10, delta={thm12_summary[2]['delta']}, mod 11), "
          f"alpha=3 (n<=5, delta={thm12_summary[3]['delta']}, mod 121) via Methods A2 & B.")

    # 3b. Ordinary partitions (a=0, b=1): OEIS A000041 + Ramanujan congruences mod 5, 7, 11, 121, 1331
    n_part = 1331 * 2 + 721
    part_a2 = series_product_factored(0, 1, n_part)
    part_b = series_logderiv(0, 1, n_part)
    assert part_a2 == part_b
    assert part_b[:101] == series_product_elementary(0, 1, 100)
    oeis_a000041 = {0: 1, 1: 1, 2: 2, 3: 3, 4: 5, 5: 7, 10: 42, 20: 627, 50: 204226, 100: 190569292, 200: 3972999029388}
    for k, v in oeis_a000041.items():
        assert part_b[k] == v, f"Partition mismatch at k={k}: {part_b[k]} != {v}"
    for n in range(30):
        assert part_b[5 * n + 4] % 5 == 0
        assert part_b[7 * n + 5] % 7 == 0
        assert part_b[11 * n + 6] % 11 == 0
    for n in range(15):
        assert part_b[121 * n + 116] % 121 == 0
    for n in range(3):
        assert part_b[1331 * n + 721] % 1331 == 0
    print("[PASS] Positive Control 2 (Ordinary partitions, a=0, b=1): OEIS A000041 values up to p(200) and Ramanujan mod 5, 7, 11, 121, 1331 verified.")

    # 3c. Overpartitions (a=1, b=1): OEIS A015128 + parity
    over_a1 = series_product_elementary(1, 1, 200)
    over_b = series_logderiv(1, 1, 200)
    assert over_a1 == over_b
    oeis_a015128 = [1, 2, 4, 8, 14, 24, 40, 64, 100, 154, 232]
    assert over_b[:11] == oeis_a015128
    assert all(over_b[k] % 2 == 0 for k in range(1, 201))
    print("[PASS] Positive Control 3 (Overpartitions, a=1, b=1): OEIS A015128 values and parity verified.")

    # 4. Negative / Mutation Controls (verifying that mutated parameters ARE caught)
    mutations = []
    # M1: Wrong delta (shift delta=7 -> 8 in Theorem 1.2 at alpha=1)
    m1_rem = d2_series_b[8] % 11
    assert m1_rem != 0, "Mutant M1 failed to be caught!"
    mutations.append({"id": "M1_wrong_delta", "desc": "a=2,b=5,alpha=1, delta=8 instead of 7", "k": 8, "val": d2_series_b[8], "mod": 11, "rem": m1_rem})

    # M2: Wrong prime modulus (13 instead of 11 in Theorem 1.2 at alpha=1, delta=7)
    m2_rem = d2_series_b[7] % 13
    assert m2_rem != 0, "Mutant M2 failed to be caught!"
    mutations.append({"id": "M2_wrong_modulus_prime", "desc": "a=2,b=5,alpha=1,delta=7, mod 13 instead of 11", "k": 7, "val": d2_series_b[7], "mod": 13, "rem": m2_rem})

    # M3: Wrong exponent (11^alpha = 121 instead of 11^{ceil(alpha/2)} = 11 at a=2,b=5,alpha=2)
    d2_alpha2 = delta_conjecture(2, 2, 2)  # 106
    m3_rems = [(n, d2_series_b[121 * n + d2_alpha2] % 121) for n in range(6)]
    m3_caught = any(r != 0 for _, r in m3_rems)
    assert m3_caught, "Mutant M3 failed to be caught!"
    first_m3 = next((n, r) for n, r in m3_rems if r != 0)
    mutations.append({"id": "M3_wrong_exponent_power", "desc": "a=2,b=5,alpha=2,delta=106, mod 11^2=121 instead of 11^1=11", "first_fail_n": first_m3[0], "k": 121 * first_m3[0] + d2_alpha2, "mod": 121, "rem": first_m3[1]})

    # M4: Excluded residue classes a in {1, 3, 5} for Part (2) at alpha=1
    m4_details = {}
    for bad_a in (1, 3, 5):
        sb = series_logderiv(bad_a, 5, 60)
        d_bad = delta_conjecture(2, bad_a, 1)
        rems = [sb[11 * n + d_bad] % 11 for n in range(5)]
        assert any(r != 0 for r in rems), f"Mutant M4 failed to catch excluded a={bad_a}"
        m4_details[bad_a] = {"delta": d_bad, "rems_n0_4": rems}
    mutations.append({"id": "M4_excluded_residue_part2", "desc": "Excluded a in {1,3,5} in Part (2) at alpha=1 mod 11", "details": m4_details})

    # M5: Excluded residue classes a in {1, 2, 4} for Part (1) at alpha=1
    m5_details = {}
    for bad_a in (1, 2, 4):
        sb = series_logderiv(bad_a, 1, 60)
        d_bad = delta_conjecture(1, bad_a, 1)
        rems = [sb[11 * n + d_bad] % 11 for n in range(5)]
        assert any(r != 0 for r in rems), f"Mutant M5 failed to catch excluded a={bad_a}"
        m5_details[bad_a] = {"delta": d_bad, "rems_n0_4": rems}
    mutations.append({"id": "M5_excluded_residue_part1", "desc": "Excluded a in {1,2,4} in Part (1) at alpha=1 mod 11", "details": m5_details})

    # M6: Wrong denominator exponent b=4 instead of b=5 at a=2, alpha=1, delta=7
    s_b4 = series_logderiv(2, 4, 30)
    m6_rem = s_b4[7] % 11
    assert m6_rem != 0, "Mutant M6 failed to be caught!"
    mutations.append({"id": "M6_wrong_b_exponent", "desc": "a=2, b=4 instead of b=5 at alpha=1, k=7 mod 11", "k": 7, "val": s_b4[7], "mod": 11, "rem": m6_rem})
    print(f"[PASS] Negative/Mutation Controls: all {len(mutations)} mutated checks caught cleanly (M1..M6).")

    # 5. Full Clean-Room Scan: a in [-50, 100], alpha in {1, 2, 3}, n in {0..5}
    a_min, a_max = -50, 100
    n_scan_max = 1331 * 5 + 1330  # 7985, covers every delta < 1331 and n in 0..5
    print(f"[SCAN] Running full exact scan for a in [{a_min}, {a_max}], alpha in {{1,2,3}}, n in {{0..5}} (N_max = {n_scan_max})...")
    t_scan0 = time.monotonic_ns()

    pent1 = pentagonal_terms(n_scan_max, scale=1)
    pent2 = pentagonal_terms(n_scan_max, scale=2)

    # Anchor at a=0: P^{[1]}_0(q) = 1 / (q;q)_inf
    one = [0] * (n_scan_max + 1)
    one[0] = 1
    p1_zero = div_sparse_eta(one, pent1, n_scan_max)
    assert p1_zero[:n_part + 1] == part_b, "Pentagonal anchor P^{[1]}_0 mismatch!"

    p1_by_a: Dict[int, List[int]] = {0: p1_zero}
    cur = p1_zero
    for a in range(1, a_max + 1):
        # Multiply by (-q;q)_inf = (q^2;q^2)_inf / (q;q)_inf
        cur = div_sparse_eta(mul_sparse_eta(cur, pent2, n_scan_max), pent1, n_scan_max)
        p1_by_a[a] = cur

    cur = p1_zero
    for a in range(-1, a_min - 1, -1):
        # Divide by (-q;q)_inf = multiply by (q;q)_inf / (q^2;q^2)_inf
        cur = div_sparse_eta(mul_sparse_eta(cur, pent1, n_scan_max), pent2, n_scan_max)
        p1_by_a[a] = cur

    # Spot-check boundaries of p1_by_a against Method B & Method A2
    for check_a in (a_min, -19, -8, 3, 14, 25, 36, a_max):
        ref_b = series_logderiv(check_a, 1, 250)
        ref_a2 = series_product_factored(check_a, 1, 250)
        assert p1_by_a[check_a][:251] == ref_b == ref_a2, f"Spot-check failed at a={check_a} for Part 1"

    part1_counterexamples = []
    part2_counterexamples = []
    part1_all_residues = {}
    part2_all_residues = {}

    for a in range(a_min, a_max + 1):
        s1 = p1_by_a[a]
        # P^{[2]}_a(q) = P^{[1]}_a(q) / (q;q)_inf^4
        s2 = s1
        for _ in range(4):
            s2 = div_sparse_eta(s2, pent1, n_scan_max)

        if a in (a_min, -18, 0, 2, 7, 18, 29, 40, a_max):
            ref2_b = series_logderiv(a, 5, 250)
            ref2_a2 = series_product_factored(a, 5, 250)
            assert s2[:251] == ref2_b == ref2_a2, f"Spot-check failed at a={a} for Part 2"

        # Evaluate Part 1 across alpha=1,2,3 and n=0..5
        p1_status = {}
        for alpha in (1, 2, 3):
            delta = delta_conjecture(1, a, alpha)
            mod = modulus_conjecture(alpha)
            fails = []
            for n in range(6):
                k = (11 ** alpha) * n + delta
                rem = s1[k] % mod
                if rem != 0:
                    fails.append({"n": n, "k": k, "rem": rem, "v11": _v11(s1[k]), "digits": len(str(abs(s1[k]))),
                                  "exact_val": str(s1[k]) if k <= 300 else None})
            p1_status[alpha] = {"delta": delta, "mod": mod, "pass_n0_5": len(fails) == 0, "fails": fails}
            if is_admissible_a(1, a) and fails:
                part1_counterexamples.append({
                    "a": a,
                    "a_mod_11": a % 11,
                    "alpha": alpha,
                    "delta": delta,
                    "mod": mod,
                    "first_fail": fails[0],
                    "fail_count_n0_5": len(fails),
                    "all_rems_n0_5": [(n, (11 ** alpha) * n + delta, s1[(11 ** alpha) * n + delta] % mod) for n in range(6)],
                })
        part1_all_residues[a] = {
            "admissible": is_admissible_a(1, a),
            "a_mod_11": a % 11,
            "alpha_pass": {alpha: p1_status[alpha]["pass_n0_5"] for alpha in (1, 2, 3)},
            "details": p1_status,
        }

        # Evaluate Part 2 across alpha=1,2,3 and n=0..5
        p2_status = {}
        for alpha in (1, 2, 3):
            delta = delta_conjecture(2, a, alpha)
            mod = modulus_conjecture(alpha)
            fails = []
            for n in range(6):
                k = (11 ** alpha) * n + delta
                rem = s2[k] % mod
                if rem != 0:
                    fails.append({"n": n, "k": k, "rem": rem, "v11": _v11(s2[k]), "digits": len(str(abs(s2[k]))),
                                  "exact_val": str(s2[k]) if k <= 300 else None})
            p2_status[alpha] = {"delta": delta, "mod": mod, "pass_n0_5": len(fails) == 0, "fails": fails}
            if is_admissible_a(2, a) and fails:
                part2_counterexamples.append({
                    "a": a,
                    "a_mod_11": a % 11,
                    "alpha": alpha,
                    "delta": delta,
                    "mod": mod,
                    "first_fail": fails[0],
                    "fail_count_n0_5": len(fails),
                    "all_rems_n0_5": [(n, (11 ** alpha) * n + delta, s2[(11 ** alpha) * n + delta] % mod) for n in range(6)],
                })
        part2_all_residues[a] = {
            "admissible": is_admissible_a(2, a),
            "a_mod_11": a % 11,
            "alpha_pass": {alpha: p2_status[alpha]["pass_n0_5"] for alpha in (1, 2, 3)},
            "details": p2_status,
        }

        # Drop large s1 reference once processed to keep RSS tiny
        p1_by_a[a] = []

    t_scan1 = time.monotonic_ns()
    print(f"[DONE] Full scan completed in {t_scan1 - t_scan0}s (Peak RSS: {get_peak_rss_mib()} MiB).")

    # 6. Summarize Counterexamples & Cross-Verify Key Minimal Counterexamples with Methods A2 & B!
    print("\n=== SUMMARY OF COUNTEREXAMPLES IN a in [-50, 100], alpha in {1,2,3}, n in {0..5} ===")
    for part, cex_list, b_pow in ((1, part1_counterexamples, 1), (2, part2_counterexamples, 5)):
        by_alpha = {al: [x for x in cex_list if x["alpha"] == al] for al in (1, 2, 3)}
        pos_cex = [x for x in cex_list if x["a"] > 0]
        nonneg_cex = [x for x in cex_list if x["a"] >= 0]
        neg_cex = [x for x in cex_list if x["a"] < 0]
        print(f"\n--- Part ({part}) [b={b_pow}] ---")
        print(f"Total failing (a, alpha) pairs for admissible a in [-50, 100]: {len(cex_list)}")
        for al in (1, 2, 3):
            al_pos = [x["a"] for x in by_alpha[al] if x["a"] > 0]
            al_nonpos = [x["a"] for x in by_alpha[al] if x["a"] <= 0]
            print(f"  alpha={al}: {len(by_alpha[al])} failing a values | positive a: {al_pos} | non-positive a: {al_nonpos}")

        # Identify minimal positive counterexample (by smallest a > 0, then smallest alpha; and by smallest alpha first, then smallest a > 0)
        key_targets = []
        if pos_cex:
            min_pos_by_a = min(pos_cex, key=lambda x: (x["a"], x["alpha"]))
            min_pos_by_alpha = min(pos_cex, key=lambda x: (x["alpha"], x["a"]))
            min_pos_k = min(pos_cex, key=lambda x: (x["first_fail"]["k"], x["a"], x["alpha"]))
            key_targets.extend([
                ("smallest_positive_a", min_pos_by_a),
                ("smallest_alpha_then_pos_a", min_pos_by_alpha),
                ("smallest_index_k_pos_a", min_pos_k),
            ])
        if nonneg_cex and nonneg_cex[0]["a"] == 0:
            key_targets.append(("a_equals_0", min([x for x in nonneg_cex if x["a"] == 0], key=lambda x: x["alpha"])))
        if neg_cex:
            min_abs_neg = min(neg_cex, key=lambda x: (abs(x["a"]), x["alpha"]))
            key_targets.append(("smallest_abs_negative_a", min_abs_neg))

        seen = set()
        for label, item in key_targets:
            key = (item["a"], item["alpha"])
            print(f"  * {label}: a={item['a']} (a mod 11 = {item['a_mod_11']}), alpha={item['alpha']}, "
                  f"delta={item['delta']}, mod={item['mod']}, first_fail={item['first_fail']}")
            if key not in seen:
                seen.add(key)
                k_fail = item["first_fail"]["k"]
                va = series_product_factored(item["a"], b_pow, k_fail)[k_fail]
                vb = series_logderiv(item["a"], b_pow, k_fail)[k_fail]
                assert va == vb, f"Cross-check mismatch at Part {part}, a={item['a']}, k={k_fail}"
                assert va % item["mod"] == item["first_fail"]["rem"]
                if k_fail <= 200:
                    va_elem = series_product_elementary(item["a"], b_pow, k_fail)[k_fail]
                    assert va_elem == va
                item["verified_exact_val_first_fail"] = str(va)
                print(f"    [CROSS-VERIFIED A & B] exact coeff at k={k_fail} ({len(str(abs(va)))} digits): "
                      f"{str(va) if len(str(abs(va))) <= 80 else str(va)[:35] + '...' + str(va)[-20:]} "
                      f"== {va % item['mod']} (mod {item['mod']})")

    # Print behavior table for small non-negative a in 0..45
    print("\n=== EXACT BEHAVIOR FOR a in [0, 45] (alpha=1,2,3; n=0..5) ===")
    print("  a | a%11 | P1 adm | P1(a1,a2,a3) | P2 adm | P2(a1,a2,a3)")
    for a in range(0, 46):
        r1 = part1_all_residues[a]
        r2 = part2_all_residues[a]
        p1s = "".join("P" if r1["alpha_pass"][al] else "F" for al in (1, 2, 3))
        p2s = "".join("P" if r2["alpha_pass"][al] else "F" for al in (1, 2, 3))
        print(f" {a:2d} |  {a%11:2d}  |   {'Y' if r1['admissible'] else '.'}    |     {p1s}      |   {'Y' if r2['admissible'] else '.'}    |     {p2s}")

    # Save structured JSON summary
    summary_out = {
        "verbatim_tex_checks": tex_checks,
        "claimed_counterexamples": {
            "part1_a36_alpha3_n0": {
                "a": 36, "b": 1, "alpha": 3, "n": 0, "delta": d1_36_3, "modulus": 121,
                "exact_value": str(c1_val),
                "residue_mod_121": c1_rem,
                "v11": _v11(c1_val),
                "residues_n0_5": next(x["all_rems_n0_5"] for x in part1_counterexamples if x["a"] == 36 and x["alpha"] == 3),
            },
            "part2_a40_alpha3_n0": {
                "a": 40, "b": 5, "alpha": 3, "n": 0, "delta": d2_40_3, "modulus": 121,
                "exact_value": str(c2_val),
                "residue_mod_121": c2_rem,
                "v11": _v11(c2_val),
                "residues_n0_5": next(x["all_rems_n0_5"] for x in part2_counterexamples if x["a"] == 40 and x["alpha"] == 3),
            },
        },
        "positive_controls": {
            "theorem_1_2_a2_b5": thm12_summary,
            "ordinary_partitions_a0_b1": "PASS (OEIS A000041 up to k=200 + Ramanujan mod 5,7,11,121,1331)",
            "overpartitions_a1_b1": "PASS (OEIS A015128 up to k=10 + even parity up to k=200)",
        },
        "mutation_controls": mutations,
        "scan_range": {"a_min": a_min, "a_max": a_max, "alphas": [1, 2, 3], "n_range": [0, 5], "n_scan_max": n_scan_max},
        "part1_admissible_counterexamples": part1_counterexamples,
        "part2_admissible_counterexamples": part2_counterexamples,
        "peak_rss_mib": int(get_peak_rss_mib()),
        "wall_seconds": int(time.monotonic_ns() - t0),
    }
    with open("verification_results.json", "w", encoding="utf-8") as f:
        json.dump(summary_out, f, indent=2)

    print(f"\n[COMPLETE] All checks passed in {summary_out['wall_seconds']}s, Peak RSS = {summary_out['peak_rss_mib']} MiB.")


def _v11(val: int) -> Optional[int]:
    if val == 0:
        return None
    v = 0
    x = abs(val)
    while x % 11 == 0:
        x //= 11
        v += 1
    return v


if __name__ == "__main__":
    main()
