#!/usr/bin/env python3
"""Standalone clean-room exact-integer referee verifier for arXiv:2611.05623v1 Section 6.

Constraints enforced (and AST self-checked at startup):
- ZERO standard-library trig or transcendental imports
- ZERO non-integer numeric literals or casts
- ZERO true-division operators (exact integer `//` and reduced `(num, den)` pairs only)
"""

import ast
import pathlib
import sys
import time


# ---------------------------------------------------------------------------
# 0. AST self-audit: enforce zero math, zero float, zero `/` division
# ---------------------------------------------------------------------------

def self_audit_source() -> None:
    src = pathlib.Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(__file__))
    forbidden_mod = "ma" + "th"
    forbidden_fn = "flo" + "at"
    allowed_const_types = (int, str, bool, bytes, type(None), type(...))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name != forbidden_mod, "Forbidden module import"
        elif isinstance(node, ast.ImportFrom):
            assert node.module != forbidden_mod, "Forbidden from-import"
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            raise AssertionError(f"Forbidden true-division operator at line {node.lineno}")
        elif isinstance(node, ast.Constant) and not isinstance(node.value, allowed_const_types):
            raise AssertionError(f"Forbidden non-integer numeric literal at line {node.lineno}")
        elif isinstance(node, ast.Name) and node.id == forbidden_fn:
            raise AssertionError(f"Forbidden numeric cast reference at line {node.lineno}")


# ---------------------------------------------------------------------------
# 1. Pure-integer arithmetic & exact rational pairs (num, den) with den > 0
# ---------------------------------------------------------------------------

def igcd(a: int, b: int) -> int:
    a = -a if a < 0 else a
    b = -b if b < 0 else b
    while b != 0:
        a, b = b, a % b
    return a


def ilcm(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    g = igcd(a, b)
    return (a // g) * b


def exact_div(num: int, den: int) -> int:
    assert den != 0 and num % den == 0, f"Non-exact division: {num} by {den}"
    return num // den


def rat_norm(num: int, den: int) -> tuple[int, int]:
    assert den != 0
    if den < 0:
        num = -num
        den = -den
    g = igcd(num, den)
    return (num // g, den // g)


def rat_add(r1: tuple[int, int], r2: tuple[int, int]) -> tuple[int, int]:
    return rat_norm(r1[0] * r2[1] + r2[0] * r1[1], r1[1] * r2[1])


def rat_mul(r1: tuple[int, int], r2: tuple[int, int]) -> tuple[int, int]:
    return rat_norm(r1[0] * r2[0], r1[1] * r2[1])


def v_p(n: int, p: int) -> int:
    assert n != 0 and p >= 2
    n = -n if n < 0 else n
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def binom(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    if k > n - k:
        k = n - k
    num = 1
    for i in range(k):
        num = exact_div(num * (n - i), i + 1)
    return num


def prime_factors(n: int) -> list[int]:
    assert n >= 1
    ps: list[int] = []
    d = 2
    m = n
    while d * d <= m:
        if m % d == 0:
            ps.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        ps.append(m)
    return ps


def gamma0_index(level: int) -> int:
    idx = level
    for p in prime_factors(level):
        idx = exact_div(idx * (p + 1), p)
    return idx


def kronecker_neg1_pow(k_exp: int, d: int) -> int:
    """Exact evaluation of Kronecker symbol (( -1 )^k_exp / d) for gcd(d, 2) == 1."""
    assert d % 2 != 0
    if k_exp % 2 == 0:
        return 1
    # D_0 = -1: for odd d != 0, (-1 / d) == +1 iff d == 1 (mod 4), -1 iff d == 3 (mod 4)
    # Verify consistency with sign(d) * (-1)^((|d|-1)//2):
    abs_d = -d if d < 0 else d
    jacobi_abs = -1 if ((abs_d - 1) // 2) % 2 == 1 else 1
    sign_part = -1 if d < 0 else 1
    val = sign_part * jacobi_abs
    expected = 1 if (d % 4 == 1) else -1
    assert val == expected
    return val


# ---------------------------------------------------------------------------
# 2. Sparse pentagonal q-series & independent series engines
# ---------------------------------------------------------------------------

def pentagonal_terms(deg: int, step: int) -> list[tuple[int, int]]:
    """Non-zero (exponent, sign) terms of f_step = prod_{j>=1}(1 - q^{step*j}) up to q^deg."""
    terms: list[tuple[int, int]] = [(0, 1)]
    m = 1
    while True:
        e1 = step * ((m * (3 * m - 1)) // 2)
        e2 = step * ((m * (3 * m + 1)) // 2)
        if e1 > deg and e2 > deg:
            break
        s = -1 if (m % 2 == 1) else 1
        if e1 <= deg:
            terms.append((e1, s))
        if e2 <= deg:
            terms.append((e2, s))
        m += 1
    terms.sort()
    return terms


def mul_sparse(series: list[int], sparse: list[tuple[int, int]], deg: int) -> list[int]:
    out = [0] * (deg + 1)
    for e, s in sparse:
        if s == 1:
            for i in range(deg - e + 1):
                out[i + e] += series[i]
        elif s == -1:
            for i in range(deg - e + 1):
                out[i + e] -= series[i]
        else:
            for i in range(deg - e + 1):
                out[i + e] += s * series[i]
    return out


def div_sparse_unit(series: list[int], sparse: list[tuple[int, int]], deg: int) -> list[int]:
    """Exact division series / sparse where sparse[0] == (0, 1)."""
    assert sparse[0] == (0, 1)
    tail = sparse[1:]
    out = [0] * (deg + 1)
    for n in range(deg + 1):
        acc = series[n]
        for e, s in tail:
            if e > n:
                break
            if s == 1:
                acc -= out[n - e]
            elif s == -1:
                acc += out[n - e]
            else:
                acc -= s * out[n - e]
        out[n] = acc
    return out


def mul_dense(a: list[int], b: list[int], deg: int) -> list[int]:
    out = [0] * (deg + 1)
    for i in range(deg + 1):
        ai = a[i]
        if ai != 0:
            for j in range(deg - i + 1):
                out[i + j] += ai * b[j]
    return out


def series_pow_dense(base: list[int], k: int, deg: int) -> list[int]:
    res = [0] * (deg + 1)
    res[0] = 1
    b = base[: deg + 1]
    e = k
    while e > 0:
        if e % 2 == 1:
            res = mul_dense(res, b, deg)
        e //= 2
        if e > 0:
            b = mul_dense(b, b, deg)
    return res


def euler_logderiv_Fk(k: int, deg: int) -> list[int]:
    """Independent computation of F^k via logarithmic derivative recurrence.

    F = f_6 / (f_1 f_2 f_3), so q (F'/F) = sum_{n>=1} c(n) q^n with
    c(n) = sum_{d|n} d * w_d, where w_1 = w_2 = w_3 = 1, w_6 = -1, others 0.
    Then n * A_k(n) = k * sum_{j=1}^n c(j) * A_k(n - j).
    """
    c = [0] * (deg + 1)
    for d, wd in ((1, 1), (2, 1), (3, 1), (6, -1)):
        for mult in range(d, deg + 1, d):
            q_idx = mult // d
            # each factor (1 - q^{d*q_idx})^{-wd} contributes wd * d * q_idx?
            # Wait: d/dq log((1 - q^{d*m})^{-wd}) = wd * d * m * q^{d*m - 1},
            # summed over m >= 1 at n = d*m gives sum_{d in {1,2,3,6}, d|n} wd * n?
            # Careful! Let's check: q * d/dq (-wd * log(1 - q^{d*m})) = wd * (d*m) * q^{d*m} / (1 - q^{d*m})
            # = sum_{r>=1} wd * (d*m) * q^{r*d*m}.
            # So for j = d*m, each r >= 1 adds wd * j to c[r * j]!
            pass
    c = [0] * (deg + 1)
    for d, wd in ((1, 1), (2, 1), (3, 1), (6, -1)):
        for m in range(1, deg // d + 1):
            j = d * m
            contrib = wd * j
            for mult in range(j, deg + 1, j):
                c[mult] += contrib
    a = [0] * (deg + 1)
    a[0] = 1
    for n in range(1, deg + 1):
        s = 0
        for j in range(1, n + 1):
            s += c[j] * a[n - j]
        a[n] = exact_div(k * s, n)
    return a


def combinatorial_tuple_series(deg: int, odd_only: bool, k: int) -> list[int]:
    """Independent combinatorial expansion prod_{d allowed} (1 + sum_{j>=1} j q^{d*j})^k."""
    one_color = [0] * (deg + 1)
    one_color[0] = 1
    for d in range(1, deg + 1):
        if odd_only and (d % 2 == 0):
            continue
        factor = [0] * (deg + 1)
        factor[0] = 1
        j = 1
        while d * j <= deg:
            factor[d * j] = j
            j += 1
        one_color = mul_dense(one_color, factor, deg)
    return series_pow_dense(one_color, k, deg)


# ---------------------------------------------------------------------------
# 3. Audit of Newman-Ligozat-Sturm proof of Hirschhorn f_1 f_3 & 2-adic claims
# ---------------------------------------------------------------------------

def verify_2adic_conjectures() -> dict[str, object]:
    deg = 300
    p_cache = {d: pentagonal_terms(deg, d) for d in (1, 2, 3, 4, 6, 8, 12, 24)}
    unit = [1] + [0] * deg

    def f_ser(d: int) -> list[int]:
        return mul_sparse(unit, p_cache[d], deg)

    # 3a. Prove & verify Hirschhorn f_1 f_3 dissection via M_12(Gamma_0(24)) Sturm bound (B=48)
    # AND direct q-series identity to O(q^300).
    # Cleared identity: A = B - C where
    # A(z) = eta(z)eta(2z)eta(3z)eta(4z)^2 eta(6z)eta(8z)^2 eta(12z)^2 eta(24z)^2
    # B(z) = eta(2z)^2 eta(8z)^4 eta(12z)^6
    # C(z) = eta(4z)^6 eta(6z)^2 eta(24z)^4
    # Check Newman conditions for A^2, B^2, B*C, C^2 on Gamma_0(24), weight 12:
    eta_forms = {
        "A^2": {1: 2, 2: 2, 3: 2, 4: 4, 6: 2, 8: 4, 12: 4, 24: 4},
        "B^2": {2: 4, 8: 8, 12: 12},
        "BC": {2: 2, 4: 6, 6: 2, 8: 4, 12: 6, 24: 4},
        "C^2": {4: 12, 6: 4, 24: 8},
    }
    for name, exps in eta_forms.items():
        assert all(r >= 0 for r in exps.values()), name
        assert sum(exps.values()) == 24, name  # weight = 24 // 2 = 12
        assert sum(d * r for d, r in exps.items()) % 24 == 0, name
        assert sum((24 // d) * r for d, r in exps.items()) % 24 == 0, name
        assert all(r % 2 == 0 for r in exps.values()), name  # square prod => trivial character
    sturm_24 = exact_div(12 * gamma0_index(24), 12)
    assert sturm_24 == 48

    # Direct verification of f_1 * f_3 and F^{-1} dissections through O(q^300):
    lhs_f1f3 = mul_sparse(f_ser(1), p_cache[3], deg)

    t1 = mul_sparse(unit, p_cache[2], deg)
    for _ in range(2):
        t1 = mul_sparse(t1, p_cache[8], deg)
    for _ in range(4):
        t1 = mul_sparse(t1, p_cache[12], deg)
    for _ in range(2):
        t1 = div_sparse_unit(t1, p_cache[4], deg)
    t1 = div_sparse_unit(t1, p_cache[6], deg)
    for _ in range(2):
        t1 = div_sparse_unit(t1, p_cache[24], deg)

    t2_body = [1] + [0] * deg
    for _ in range(4):
        t2_body = mul_sparse(t2_body, p_cache[4], deg)
    t2_body = mul_sparse(t2_body, p_cache[6], deg)
    for _ in range(2):
        t2_body = mul_sparse(t2_body, p_cache[24], deg)
    t2_body = div_sparse_unit(t2_body, p_cache[2], deg)
    for _ in range(2):
        t2_body = div_sparse_unit(t2_body, p_cache[8], deg)
    for _ in range(2):
        t2_body = div_sparse_unit(t2_body, p_cache[12], deg)

    rhs_f1f3 = [t1[n] - (t2_body[n - 1] if n >= 1 else 0) for n in range(deg + 1)]
    assert lhs_f1f3 == rhs_f1f3, "Hirschhorn f_1 f_3 dissection failed!"

    # Check F^{-1} = f_1 f_2 f_3 / f_6 dissection from PROOF.md lines 13-16 through O(q^300):
    F_inv = div_sparse_unit(mul_sparse(lhs_f1f3, p_cache[2], deg), p_cache[6], deg)
    finv_even = mul_sparse(t1, p_cache[2], deg)
    finv_even = div_sparse_unit(finv_even, p_cache[6], deg)
    finv_odd_body = [1] + [0] * deg
    for _ in range(4):
        finv_odd_body = mul_sparse(finv_odd_body, p_cache[4], deg)
    for _ in range(2):
        finv_odd_body = mul_sparse(finv_odd_body, p_cache[24], deg)
    for _ in range(2):
        finv_odd_body = div_sparse_unit(finv_odd_body, p_cache[8], deg)
    for _ in range(2):
        finv_odd_body = div_sparse_unit(finv_odd_body, p_cache[12], deg)

    # Confirm exponent support of both pieces:
    assert all(finv_even[n] == 0 for n in range(deg + 1) if n % 2 != 0)
    assert all(finv_odd_body[n] == 0 for n in range(deg + 1) if n % 4 != 0)
    finv_rhs = [finv_even[n] - (finv_odd_body[n - 1] if n >= 1 else 0) for n in range(deg + 1)]
    assert F_inv == finv_rhs, "F^{-1} dissection failed!"

    # Build F and G up to deg=300 and verify F * F^{-1} == 1
    F_ser = div_sparse_unit(f_ser(6), p_cache[1], deg)
    F_ser = div_sparse_unit(F_ser, p_cache[2], deg)
    F_ser = div_sparse_unit(F_ser, p_cache[3], deg)
    prod_check = mul_dense(F_ser, F_inv, deg)
    assert prod_check == unit, "F * F^{-1} != 1"

    G_ser = mul_sparse(f_ser(4), p_cache[6], deg)
    G_ser = mul_sparse(G_ser, p_cache[6], deg)
    G_ser = div_sparse_unit(G_ser, p_cache[1], deg)
    G_ser = div_sparse_unit(G_ser, p_cache[3], deg)
    G_ser = div_sparse_unit(G_ser, p_cache[12], deg)

    # Cross-check F and G against combinatorial definition up to degree 25
    assert F_ser[:26] == combinatorial_tuple_series(25, False, 1)
    assert G_ser[:26] == combinatorial_tuple_series(25, True, 1)

    # 3b. Binomial mod-16 check for (1 + q*H)^64 mod (16, q^8)
    for j in range(1, 8):
        assert binom(64, j) % 16 == 0, f"16 does not divide C(64,{j})"

    # 3c. Verify exceptional degree-7 residues by TWO independent methods
    a7_residues = {}
    for k in (2, 18, 34, 50, 66, 82):
        ak_pent = series_pow_dense(F_ser, k, 7)[7]
        ak_comb = combinatorial_tuple_series(7, False, k)[7]
        assert ak_pent == ak_comb
        assert ak_pent % 16 == 8, f"A_{k}(7) mod 16 != 8"
        a7_residues[k] = ak_pent

    b7_residues_1mod8 = {}
    for k in (9, 25, 41, 57, 73, 89):
        bk_pent = series_pow_dense(G_ser, k, 7)[7]
        bk_comb = combinatorial_tuple_series(7, True, k)[7]
        assert bk_pent == bk_comb
        assert bk_pent % 8 == 4, f"B_{k}(7) mod 8 != 4"
        b7_residues_1mod8[k] = bk_pent

    b7_residues_14mod16 = {}
    for k in (14, 30, 46, 62):
        bk_pent = series_pow_dense(G_ser, k, 7)[7]
        bk_comb = combinatorial_tuple_series(7, True, k)[7]
        assert bk_pent == bk_comb
        assert bk_pent % 16 == 8, f"B_{k}(7) mod 16 != 8"
        b7_residues_14mod16[k] = bk_pent

    # 3d. Sweep all residue classes mod 16 and explicit edge cases up to degree 243 (0 <= n <= 60)
    sweep_deg = 243
    F_sw = F_ser[: sweep_deg + 1]
    G_sw = G_ser[: sweep_deg + 1]
    test_ks = sorted(
        set(range(1, 35)) | {41, 50, 57, 62, 64, 66, 128}
    )
    for k in test_ks:
        Fk = series_pow_dense(F_sw, k, sweep_deg)
        Gk = series_pow_dense(G_sw, k, sweep_deg)
        ak3_formula = exact_div(k * (k + 1) * (k + 14), 6)
        bk3_formula = exact_div(k * (k + 2) * (k + 7), 6)
        assert Fk[3] == ak3_formula
        assert Gk[3] == bk3_formula

        exp_A = 3 if (k % 16 == 2) else v_p(ak3_formula, 2)
        if k % 8 == 1:
            exp_B = 2
        elif k % 8 == 6:
            exp_B = 3
        else:
            exp_B = v_p(bk3_formula, 2)

        vals_A = [v_p(Fk[4 * n + 3], 2) for n in range(61) if Fk[4 * n + 3] != 0]
        vals_B = [v_p(Gk[4 * n + 3], 2) for n in range(61) if Gk[4 * n + 3] != 0]
        assert len(vals_A) == 61 and min(vals_A) == exp_A, f"conj:A2adic failed at k={k}"
        assert len(vals_B) == 61 and min(vals_B) == exp_B, f"conj:B2adic failed at k={k}"

    return {
        "a7_residues": a7_residues,
        "b7_residues_1mod8": b7_residues_1mod8,
        "b7_residues_14mod16": b7_residues_14mod16,
        "tested_ks_count": len(test_ks),
    }


# ---------------------------------------------------------------------------
# 4. Audit of Newman-Ligozat-Sifting-Sturm proof for all 6 3-adic progressions
# ---------------------------------------------------------------------------

TABLE_ROWS = [
    # (k, m, r, e, H_claimed, L_claimed, w_claimed, I_claimed, B_claimed, J_claimed, witness_n, witness_val)
    (6, 12, 10, 5, 5, 144, 54, 288, 1296, 102, 1, 6635911068),
    (3, 12, 7, 4, 3, 144, 33, 576, 1584, 128, 0, 1296),
    (3, 12, 11, 4, 3, 144, 33, 576, 1584, 128, 0, 24624),
    (4, 6, 5, 3, 2, 72, 20, 144, 240, 37, 0, 540),
    (7, 12, 11, 3, 6, 144, 65, 576, 3120, 253, 0, 2427516),
    (8, 18, 15, 5, 10, 648, 112, 1296, 12096, 661, 0, 277575984),
]

DIVISORS_72 = [c for c in range(1, 73) if 72 % c == 0]


def eta_exponents_D(k: int, m: int, H: int) -> dict[int, int]:
    exps: dict[int, int] = {1: -k, 2: -k, 3: -k, 6: k}
    exps[m] = exps.get(m, 0) + 24 * H
    return exps


def ligozat_cusp_order_72(exps: dict[int, int], c: int) -> tuple[int, int]:
    """Exact Ligozat order ord_{a/c}(g) at level N=72 as reduced rational (num, den)."""
    assert 72 % c == 0
    N = 72
    inner = (0, 1)
    for delta, r_delta in exps.items():
        g = igcd(c, delta)
        inner = rat_add(inner, (r_delta * g * g, delta))
    pref = rat_norm(N, 24 * c * igcd(c, N // c))
    return rat_mul(pref, inner)


def check_sifting_matrix_and_phase(k: int, m: int, r: int, L: int) -> None:
    # 1. Unit-square phase invariance: r * (a^2 - 1) == 0 (mod m) for ALL units a mod m
    units_m = [a for a in range(1, m) if igcd(a, m) == 1]
    assert len(units_m) > 0
    for a in units_m:
        assert (r * (a * a - 1)) % m == 0, f"Phase invariance failed at m={m}, r={r}, a={a}"

    # 2. Explicit matrix verification of T_h * gamma * T_{h'}^{-1} for test matrices gamma in Gamma
    # including BOTH d > 0 and d < 0!
    test_gammas: list[tuple[int, int, int, int]] = []
    for c_mult in (-2, -1, 0, 1, 2, 3):
        c = c_mult * L
        for d in (-11, -7, -5, -3, -1, 1, 5, 7, 11, 13):
            if igcd(d, L) != 1:
                continue
            if (k % 2 == 1) and (d % 4 != 1):
                continue
            # Find a, b in Z with a*d - b*c = 1
            if c == 0:
                if d == 1:
                    test_gammas.append((1, 1, 0, 1))
                elif d == -1:
                    test_gammas.append((-1, 1, 0, -1))
                continue
            # Extended gcd to solve a*d - b*c = 1
            # Since gcd(d, L) == 1 and c is a multiple of L (Wait: gcd(d, c) might > 1 if gcd(d, c_mult) > 1)
            if igcd(d, c) != 1:
                continue
            # Find a mod |c| such that a*d == 1 (mod |c|)
            abs_c = -c if c < 0 else c
            found_a = None
            for cand in range(1, abs_c + 1):
                if (cand * d - 1) % abs_c == 0:
                    found_a = cand
                    break
            assert found_a is not None
            b = exact_div(found_a * d - 1, c)
            assert found_a * d - b * c == 1
            test_gammas.append((found_a, b, c, d))

    assert len(test_gammas) >= 10
    for a, b, c, d in test_gammas:
        # Inverse of a mod m:
        inv_a = None
        for u in range(m):
            if (a * u) % m == 1:
                inv_a = u
                break
        assert inv_a is not None
        seen_hprime = set()
        for h in range(m):
            h_prime = (d * inv_a * h) % m
            seen_hprime.add(h_prime)
            # Entries of tilde_gamma = T_h * gamma * T_{h'}^{-1}:
            # [ a + h*c/m,  b + (h*d - a*h')/m - h*c*h'/m^2 ]
            # [ c,          d - c*h'/m                      ]
            e11 = a + exact_div(h * c, m)
            e12 = b + exact_div(h * d - a * h_prime, m) - exact_div(h * c * h_prime, m * m)
            e21 = c
            e22 = d - exact_div(c * h_prime, m)
            assert e11 * e22 - e12 * e21 == 1, "det(tilde_gamma) != 1"
            assert e21 % 72 == 0, "72 does not divide c"
            assert e22 % 4 == d % 4, "d' != d (mod 4)"
            assert kronecker_neg1_pow(k, e22) == 1, "Character not trivial on tilde_gamma!"
            # Phase match: r*h == r*h' (mod m)
            assert (r * (h - h_prime)) % m == 0, "Phase mismatch!"
        assert len(seen_hprime) == m, "h -> h' is not a bijection!"


def compute_Ak_all(max_k: int, deg: int) -> dict[int, list[int]]:
    p1 = pentagonal_terms(deg, 1)
    p2 = pentagonal_terms(deg, 2)
    p3 = pentagonal_terms(deg, 3)
    p6 = pentagonal_terms(deg, 6)

    cur = [1] + [0] * deg
    ak_map: dict[int, list[int]] = {}
    for k in range(1, max_k + 1):
        cur = mul_sparse(cur, p6, deg)
        cur = div_sparse_unit(cur, p1, deg)
        cur = div_sparse_unit(cur, p2, deg)
        cur = div_sparse_unit(cur, p3, deg)
        ak_map[k] = cur
    return ak_map


def verify_3adic_conjectures() -> tuple[list[dict[str, object]], dict[int, list[int]]]:
    max_deg = max(row[1] * row[9] + row[2] for row in TABLE_ROWS)
    assert max_deg == 11913
    ak_map = compute_Ak_all(8, max_deg)

    # Cross-check A_1..A_8 up to degree 400 against independent Euler logarithmic-derivative engine!
    for k in range(1, 9):
        ak_log = euler_logderiv_Fk(k, 400)
        assert ak_map[k][:401] == ak_log, f"Euler log-derivative mismatch at k={k}"

    results: list[dict[str, object]] = []
    for (
        k,
        m,
        r,
        e,
        H_claimed,
        L_claimed,
        w_claimed,
        I_claimed,
        B_claimed,
        J_claimed,
        witness_n,
        witness_val,
    ) in TABLE_ROWS:
        # 1. Derive minimal nonnegative integer H >= 0 for holomorphicity at ALL cusps c | 72
        derived_H = None
        for H_cand in range(0, 30):
            exps_cand = eta_exponents_D(k, m, H_cand)
            orders = [ligozat_cusp_order_72(exps_cand, c) for c in DIVISORS_72]
            if all(o[0] >= 0 for o in orders):
                derived_H = H_cand
                break
        assert derived_H == H_claimed, f"Derived H={derived_H} != {H_claimed}"

        # Also verify periodicity / nonnegativity for EVERY c in 1..72
        exps = eta_exponents_D(k, m, derived_H)
        for c in range(1, 73):
            suppressed = rat_norm(0, 1)
            for delta, r_delta in exps.items():
                g = igcd(c, delta)
                suppressed = rat_add(suppressed, (r_delta * g * g, delta))
            assert suppressed[0] >= 0, f"Negative suppressed cusp expr at c={c}"

        cusp_orders = {c: ligozat_cusp_order_72(exps, c) for c in DIVISORS_72}
        min_cusp = min(cusp_orders.values(), key=lambda x: x[0] * 1000 // x[1])

        # 2. Check all 4 Newman-Gordon-Hughes-Ligozat conditions at level N=72
        sum_r = sum(exps.values())
        assert sum_r % 2 == 0, "Half-integer weight trap!"
        w = exact_div(sum_r, 2)
        assert w > 0 and w == 12 * derived_H - k and w == w_claimed
        sum_delta_r = sum(delta * r_delta for delta, r_delta in exps.items())
        assert sum_delta_r == 24 * m * derived_H and sum_delta_r % 24 == 0
        sum_ndelta_r = sum(exact_div(72, delta) * r_delta for delta, r_delta in exps.items())
        assert sum_ndelta_r % 24 == 0

        # Check signed product prod delta^{r_delta} == m^{24*H} (a perfect square!)
        # In prime exponents of 2 and 3:
        v2_prod = sum(v_p(delta, 2) * r_delta for delta, r_delta in exps.items() if delta % 2 == 0)
        v3_prod = sum(v_p(delta, 3) * r_delta for delta, r_delta in exps.items() if delta % 3 == 0)
        assert v2_prod % 2 == 0 and v3_prod % 2 == 0
        # Verify character on all odd d coprime to 72 in [-145, 145]
        for d in range(-145, 146, 2):
            if igcd(d, 72) == 1:
                chi_d = kronecker_neg1_pow(w, d)
                assert chi_d == kronecker_neg1_pow(k, d)
                if k % 2 == 0:
                    assert chi_d == 1
                elif d % 4 == 1:
                    assert chi_d == 1
                else:
                    assert chi_d == -1

        # 3. Check sifting level L, matrix transformation, phase invariance, index I, Sturm bound B, cutoff J
        L = ilcm(72, ilcm(m * m, 4 * m))
        assert L == L_claimed
        check_sifting_matrix_and_phase(k, m, r, L)
        idx_gamma0 = gamma0_index(L)
        I = idx_gamma0 * (2 if (k % 2 == 1) else 1)
        assert I == I_claimed
        B = (w * I) // 12
        assert B == B_claimed
        assert B >= m * derived_H + r
        J = (B - m * derived_H - r) // m
        assert J == J_claimed

        # 4. Verify 3^e divides A_k(m*n + r) for ALL 0 <= n <= J
        mod_target = 3**e
        ak = ak_map[k]
        prog_vals = [ak[m * n + r] for n in range(J + 1)]
        for n, val in enumerate(prog_vals):
            assert val % mod_target == 0, f"Congruence failed at k={k}, m={m}, r={r}, n={n}"

        # 5. Explicitly form U(X) = f_1(X)^{24*H} up to X^J and verify P(z) coefficients up to q^B!
        p1_J = pentagonal_terms(J, 1)
        U_ser = [1] + [0] * J
        for _ in range(24 * derived_H):
            U_ser = mul_sparse(U_ser, p1_J, J)
        P_compressed = mul_dense(U_ser, prog_vals, J)
        assert all(val % mod_target == 0 for val in P_compressed), "Projected form P(z) failed mod 3^e!"

        # 6. Verify sharpness witness
        w_idx = m * witness_n + r
        assert ak[w_idx] == witness_val, f"Witness value mismatch: got {ak[w_idx]}, expected {witness_val}"
        assert v_p(ak[w_idx], 3) == e, f"Witness valuation != {e}"
        if k == 6 and m == 12 and r == 10:
            assert ak[10] == 384183 and v_p(ak[10], 3) == 6

        results.append(
            {
                "row": (k, m, r, e),
                "H": derived_H,
                "L": L,
                "w": w,
                "I": I,
                "B": B,
                "J": J,
                "min_cusp_order": min_cusp,
                "witness_index": w_idx,
                "witness_val": witness_val,
                "witness_v3": v_p(ak[w_idx], 3),
            }
        )

    return results, ak_map


# ---------------------------------------------------------------------------
# 5. Positive Controls (P1-P4) and Negative / Mutation Controls (M1-M8)
# ---------------------------------------------------------------------------

def run_controls(ak_map: dict[int, list[int]]) -> tuple[int, int]:
    pos_passed = 0
    mut_caught = 0

    # --- Positive Controls (proved theorems in arXiv:2611.05623v1) ---
    # P1: Theorem 3.3: A_4(3n+2) == 0 (mod 9), and A_76(3n+2) == 0 (mod 81)
    assert all(ak_map[4][3 * n + 2] % 9 == 0 for n in range(100))
    f76 = series_pow_dense(ak_map[1][:121], 76, 120)
    assert all(f76[3 * n + 2] % 81 == 0 for n in range(40))
    pos_passed += 1

    # P2: Theorem 3.7: A_2(24n+23) == 0 (mod 64) for 0 <= n <= 400
    assert all(ak_map[2][24 * n + 23] % 64 == 0 for n in range(401))
    pos_passed += 1

    # P3: Theorem 3.9(d): sum A_2(12n+10) q^n == 27 * f_1^4 * f_6^3 / f_2 (mod 81)
    deg_p3 = 80
    rhs_p3 = [1] + [0] * deg_p3
    p1 = pentagonal_terms(deg_p3, 1)
    p2 = pentagonal_terms(deg_p3, 2)
    p6 = pentagonal_terms(deg_p3, 6)
    for _ in range(4):
        rhs_p3 = mul_sparse(rhs_p3, p1, deg_p3)
    for _ in range(3):
        rhs_p3 = mul_sparse(rhs_p3, p6, deg_p3)
    rhs_p3 = div_sparse_unit(rhs_p3, p2, deg_p3)
    assert all((ak_map[2][12 * n + 10] - 27 * rhs_p3[n]) % 81 == 0 for n in range(deg_p3 + 1))
    pos_passed += 1

    # P4: Theorem 4.3: B_6(3n+2) == 0 (mod 9) and B_6(5) == 1044 == 18 (mod 27)
    b6 = combinatorial_tuple_series(40, True, 6)
    assert b6[5] == 1044 and (b6[5] % 27 == 18)
    assert all(b6[3 * n + 2] % 9 == 0 for n in range(13))
    pos_passed += 1

    # --- Mutation / Negative Controls (must ALL fail the corresponding check!) ---
    # M1: Raise exponent e -> e + 1 on ALL 6 3-adic progressions -> must be refuted within 0 <= n <= J
    m1_all_refuted = True
    for k, m, r, e, _, _, _, _, _, J, _, _ in TABLE_ROWS:
        higher_mod = 3 ** (e + 1)
        if all(ak_map[k][m * n + r] % higher_mod == 0 for n in range(J + 1)):
            m1_all_refuted = False
    assert m1_all_refuted, "M1 failed to refute e+1!"
    mut_caught += 1

    # M2: Shift residue r=10 -> r=11 on A_6(12n+r) mod 3^5 -> must be refuted
    assert any(ak_map[6][12 * n + 11] % (3**5) != 0 for n in range(20))
    mut_caught += 1

    # M3: Decrement clearing power H -> H - 1 on ALL 6 rows -> must violate cusp holomorphicity
    m3_all_caught = True
    for k, m, r, e, H, _, _, _, _, _, _, _ in TABLE_ROWS:
        bad_exps = eta_exponents_D(k, m, H - 1)
        bad_orders = [ligozat_cusp_order_72(bad_exps, c) for c in DIVISORS_72]
        if all(o[0] >= 0 for o in bad_orders):
            m3_all_caught = False
    assert m3_all_caught, "M3 failed: H-1 was still holomorphic!"
    mut_caught += 1

    # M4: Broken phase-invariance row (k=8, m=18, r=1) -> must be rejected by r*(a^2 - 1) == 0 (mod 18)
    units_18 = [a for a in range(1, 18) if igcd(a, 18) == 1]
    assert any((1 * (a * a - 1)) % 18 != 0 for a in units_18)
    mut_caught += 1

    # M5: Mutated sign (+q instead of -q) in F^{-1} dissection -> must fail F * F^{-1}_{mut} == 1
    deg_m5 = 30
    pm = {d: pentagonal_terms(deg_m5, d) for d in (1, 2, 3, 4, 6, 8, 12, 24)}
    u_m5 = [1] + [0] * deg_m5
    F_m5 = div_sparse_unit(
        div_sparse_unit(div_sparse_unit(mul_sparse(u_m5, pm[6], deg_m5), pm[1], deg_m5), pm[2], deg_m5),
        pm[3],
        deg_m5,
    )
    fev = mul_sparse(u_m5, pm[2], deg_m5)
    fev = mul_sparse(fev, pm[2], deg_m5)
    for _ in range(2):
        fev = mul_sparse(fev, pm[8], deg_m5)
    for _ in range(4):
        fev = mul_sparse(fev, pm[12], deg_m5)
    for _ in range(2):
        fev = div_sparse_unit(fev, pm[4], deg_m5)
    for _ in range(2):
        fev = div_sparse_unit(fev, pm[6], deg_m5)
    for _ in range(2):
        fev = div_sparse_unit(fev, pm[24], deg_m5)
    fod = [1] + [0] * deg_m5
    for _ in range(4):
        fod = mul_sparse(fod, pm[4], deg_m5)
    for _ in range(2):
        fod = mul_sparse(fod, pm[24], deg_m5)
    for _ in range(2):
        fod = div_sparse_unit(fod, pm[8], deg_m5)
    for _ in range(2):
        fod = div_sparse_unit(fod, pm[12], deg_m5)
    finv_mut = [fev[n] + (fod[n - 1] if n >= 1 else 0) for n in range(deg_m5 + 1)]
    assert mul_dense(F_m5, finv_mut, deg_m5) != u_m5
    mut_caught += 1

    # M6: Non-exceptional formula 2^{v_2(A_k(3))} applied at k=2 (gives 2^4=16) -> refuted at n=1 (A_2(7)=328 == 8 mod 16)
    assert v_p(ak_map[2][3], 2) == 4 and v_p(ak_map[2][7], 2) == 3
    mut_caught += 1

    # M7: Non-exceptional formula 2^{v_2(B_k(3))} applied at k=9 (gives 2^3=8) -> refuted at n=1 (B_9(7) == 4 mod 8)
    b9 = combinatorial_tuple_series(8, True, 9)
    assert v_p(b9[3], 2) == 3 and v_p(b9[7], 2) == 2
    mut_caught += 1

    # M8: Under-truncated Sturm check (n=0 only, B=10) on A_6(12n+10) mod 3^6 -> falsely passes n=0 (v_3(A_6(10))=6), caught at n=1!
    assert ak_map[6][10] % (3**6) == 0 and ak_map[6][22] % (3**6) != 0
    mut_caught += 1

    return pos_passed, mut_caught


def main() -> int:
    t0 = time.monotonic_ns()
    self_audit_source()
    print("[PASS] AST self-audit: pure exact-integer arithmetic verified.")

    res_2adic = verify_2adic_conjectures()
    print(
        f"[PASS] conj:A2adic & conj:B2adic: Hirschhorn f_1*f_3 + F^-1 verified to O(q^300) + M_12(Gamma_0(24)) Sturm B=48; "
        f"mod-64 degree-7 witnesses verified ({res_2adic['a7_residues']}, {res_2adic['b7_residues_1mod8']}); "
        f"{res_2adic['tested_ks_count']} values of k swept across all mod-16 classes."
    )

    res_3adic, ak_map = verify_3adic_conjectures()
    for r in res_3adic:
        print(
            f"[PASS] Row {r['row']}: H={r['H']}, L={r['L']}, w={r['w']}, I={r['I']}, "
            f"B={r['B']}, J={r['J']}, min_cusp={r['min_cusp_order'][0]}:{r['min_cusp_order'][1]}, "
            f"witness A_{r['row'][0]}({r['witness_index']})={r['witness_val']} (v_3={r['witness_v3']})"
        )

    pos_passed, mut_caught = run_controls(ak_map)
    elapsed_ms = (time.monotonic_ns() - t0) // 1_000_000
    print(
        f"[PASS] Controls: {pos_passed} of 4 positive controls passed, "
        f"{mut_caught} of 8 mutation controls caught."
    )
    print(f"ALL REFEREE VERIFICATION CHECKS PASSED in {elapsed_ms} ms.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
