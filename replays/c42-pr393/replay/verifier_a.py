#!/usr/bin/env python3
"""Verifier A: Clean-room exact integer/rational outward-rounded verifier (Python stdlib only, zero floats in bounds).

Implements Theorem 1 / Lemma 3 from inputs/tex/argument.tex and inputs/tex/verification.tex:
- Exact Fraction precondition verification:
    (P1) 1/2 < q < r = 1/sqrt(2)
    (P2) 0 < c < 1 and q < 2*c*sqrt(1 - c^2)
    (P3) r + sqrt(q^2 - 1/4) + 1/4 <= 1
- Scaled integer outward-rounded interval arithmetic with scale S = 10^24 (no floats in any bound).
- Outer 48 x 32 closed grid on (u, z) in [0, 1]^2 where u = r*t/(q - 1/2), including boundary points
  t = 0, t = t_max (where P = 0), z = 0, z = 1.
- 5-step (configurable) v-iteration with explicit v_- > 0 check before every division.
- Full monotonicity check on (h, R) AND 0 < A_1 < 2*A_2 across the entire (x', a) rectangle at (h_-, R_+).
- Adaptive bisection of the wider of h and R up to max_depth.
- Primitive unit tests (>= 10^4 random rationals verified against 100-digit mpmath).
- Full control suite (red preconditions, red separation, red m0:=0 mutation, positive drop v_-^2 D_0^2 control)
  and diagnostics (bisected certified q_max, U_* inflation margin delta).
"""
from fractions import Fraction
import json
import math
import random
import time

SCALE = 10 ** 24  # exact integer scale; all bounds are int representing n / SCALE


# ---------------------------------------------------------------------------
# Exact integer outward-rounded primitives (NO floats anywhere in bounds!)
# ---------------------------------------------------------------------------
def floor_div(a: int, b: int) -> int:
    assert b > 0
    return a // b


def ceil_div(a: int, b: int) -> int:
    assert b > 0
    return -((-a) // b)


def frac_lo(x: Fraction) -> int:
    return floor_div(x.numerator * SCALE, x.denominator)


def frac_hi(x: Fraction) -> int:
    return ceil_div(x.numerator * SCALE, x.denominator)


def mul_lo(a: int, b: int) -> int:
    return floor_div(a * b, SCALE)


def mul_hi(a: int, b: int) -> int:
    return ceil_div(a * b, SCALE)


def div_lo(a: int, b: int) -> int:
    if b <= 0:
        raise ValueError("Non-positive divisor")
    return floor_div(a * SCALE, b)


def div_hi(a: int, b: int) -> int:
    if b <= 0:
        raise ValueError("Non-positive divisor")
    return ceil_div(a * SCALE, b)


def sqrt_lo(a: int) -> int:
    if a < 0:
        raise ValueError("Negative radicand in sqrt_lo")
    return math.isqrt(a * SCALE)


def sqrt_hi(a: int) -> int:
    if a < 0:
        raise ValueError("Negative radicand in sqrt_hi")
    n = a * SCALE
    k = math.isqrt(n)
    return k if k * k == n else k + 1


def r_enclosure():
    """Exact outward enclosure of r = 1/sqrt(2) = sqrt(1/2)."""
    half = SCALE // 2
    assert 2 * half == SCALE
    r_lo = sqrt_lo(half)
    r_hi = sqrt_hi(half)
    # Self-check exact mathematical inequalities: 2*r_lo^2 <= SCALE^2 <= 2*r_hi^2
    assert 2 * r_lo * r_lo <= SCALE * SCALE <= 2 * r_hi * r_hi
    return r_lo, r_hi


# ---------------------------------------------------------------------------
# Exact Fraction precondition checks
# ---------------------------------------------------------------------------
def check_preconditions(q: Fraction, c: Fraction):
    """Exact rational verification of all analytic preconditions."""
    reasons = []
    # P1: 1/2 < q < 1/sqrt(2)
    p1_gt_half = q > Fraction(1, 2)
    p1_lt_r = (q > 0) and (2 * q * q < 1)
    if not (p1_gt_half and p1_lt_r):
        reasons.append("FAIL_RANGE_Q: requires 1/2 < q < 1/sqrt(2)")

    # P2: 0 < c < 1 and q < 2*c*sqrt(1 - c^2) <=> q^2 < 4*c^2*(1 - c^2)
    p2_c_range = Fraction(0) < c < Fraction(1)
    p2_c_cond = p2_c_range and (q * q < 4 * c * c * (1 - c * c))
    if not p2_c_cond:
        reasons.append("FAIL_C_PRECONDITION: requires 0 < c < 1 and q < 2*c*sqrt(1-c^2)")

    # P3: r + sqrt(xi) + 1/4 <= 1 <=> sqrt(xi) <= 3/4 - 1/sqrt(2)
    # Exact check: 3/4 - 1/sqrt(2) > 0 since 9/16 > 1/2.
    # Square once: xi <= 9/16 + 1/2 - 3/(2*sqrt(2)) = 17/16 - 3/(2*sqrt(2))
    # <=> 3/(2*sqrt(2)) <= 17/16 - xi
    # <=> (17/16 - xi > 0) AND (9/8 <= (17/16 - xi)^2).
    xi = q * q - Fraction(1, 4)
    rhs = Fraction(17, 16) - xi
    p3_idx_cond = (xi >= 0) and (rhs > 0) and (Fraction(9, 8) <= rhs * rhs)
    # Also verify via outward-rounded scaled integers (extra belt-and-suspenders check)
    r_lo, r_hi = r_enclosure()
    if xi >= 0:
        xi_hi = frac_hi(xi)
        p3_scaled = (r_hi + sqrt_hi(xi_hi) + SCALE // 4) <= SCALE
    else:
        p3_scaled = False
    if not (p3_idx_cond and p3_scaled):
        reasons.append("FAIL_INDEX_PRECONDITION: requires r + sqrt(q^2 - 1/4) + 1/4 <= 1")

    return {
        "ok": len(reasons) == 0,
        "p1_q_in_range": p1_gt_half and p1_lt_r,
        "p2_c_precondition": p2_c_cond,
        "p3_index_precondition": p3_idx_cond and p3_scaled,
        "reasons": reasons,
    }


# ---------------------------------------------------------------------------
# Core Verifier A engine
# ---------------------------------------------------------------------------
def verify_theorem1_a(
    q: Fraction,
    c: Fraction = Fraction(9657, 10000),
    n_t: int = 48,
    n_z: int = 32,
    v_iters: int = 5,
    max_depth: int = 12,
    zero_m0: bool = False,
    drop_vD0: bool = False,
    delta_inflate: Fraction = Fraction(0),
    bypass_preconditions: bool = False,
):
    """Run exact integer outward-rounded interval exclusion.

    Returns a dictionary with status ('CERTIFIED', 'PRECONDITION_FAILED', or 'INCONCLUSIVE'),
    box counts, depth, minimum certified leaf margin, and failure details if any.
    """
    t0 = time.time()
    pre = check_preconditions(q, c)
    if not pre["ok"] and not bypass_preconditions:
        return {
            "status": "PRECONDITION_FAILED",
            "q": str(q),
            "c": str(c),
            "preconditions": pre,
            "elapsed_sec": round(time.time() - t0, 4),
        }

    r_lo, r_hi = r_enclosure()
    q_lo = frac_lo(q)
    q_hi = frac_hi(q)
    q2 = q * q
    q2_lo = frac_lo(q2)
    q2_hi = frac_hi(q2)
    xi = q2 - Fraction(1, 4)
    if xi < 0:
        return {"status": "INCONCLUSIVE", "reason": "xi < 0", "q": str(q), "c": str(c)}
    xi_hi = frac_hi(xi)
    sqrt_xi_hi = sqrt_hi(xi_hi)

    c_lo = frac_lo(c)
    if c_lo <= 0 or c_lo > SCALE:
        return {"status": "INCONCLUSIVE", "reason": "invalid c", "q": str(q), "c": str(c)}
    delta_hi = frac_hi(delta_inflate)

    # q - 1/2 exact
    q_minus_half = q - Fraction(1, 2)
    if q_minus_half <= 0:
        return {"status": "INCONCLUSIVE", "reason": "q <= 1/2", "q": str(q), "c": str(c)}

    # Precompute outer t-cells: u = r*t/(q - 1/2) in [i/n_t, (i+1)/n_t]
    # Note t = u * (q - 1/2) / r
    t_cells = []
    for i in range(n_t):
        u_lo_f = Fraction(i, n_t) * q_minus_half
        u_hi_f = Fraction(i + 1, n_t) * q_minus_half
        # t_lo = floor((u_lo_f / r_hi)) where r_hi represents r_hi / SCALE
        # Exact: u_lo_f / (r_hi / SCALE) = (u_lo_f.num * SCALE) / (u_lo_f.den * r_hi), then scaled by SCALE:
        t_min = floor_div(u_lo_f.numerator * SCALE * SCALE, u_lo_f.denominator * r_hi)
        t_max = ceil_div(u_hi_f.numerator * SCALE * SCALE, u_hi_f.denominator * r_lo)

        s_lo = r_lo + t_min
        s_hi = r_hi + t_max
        # I = t / (1 - r) <= t_max / (1 - r_hi)
        one_minus_r_lo = SCALE - r_hi
        if one_minus_r_lo <= 0:
            return {"status": "INCONCLUSIVE", "reason": "1 - r_hi <= 0"}
        I_hi = div_hi(t_max, one_minus_r_lo)

        # v-iteration: start with v_+ = s_hi
        v_hi = s_hi
        v_lo = 0
        b_hi = 0
        # 3*r_lo <= r + 1/r = 3*r <= 3*r_hi (exact because r^2 = 1/2 => 1/r = 2*r)
        denom_v_lo = 3 * r_lo
        denom_v_hi = 3 * r_hi
        for _ in range(v_iters):
            # b_* <= r*I + sqrt(2*xi*v^2 + 2*t*v)
            v2_hi = mul_hi(v_hi, v_hi)
            rad_b = 2 * mul_hi(xi_hi, v2_hi) + 2 * mul_hi(t_max, v_hi)
            b_hi = mul_hi(r_hi, I_hi) + sqrt_hi(rad_b)
            # v_- = (1 - b) / (r + 1/r) >= (1 - b_hi) / (3*r_hi)
            if SCALE - b_hi <= 0:
                return {
                    "status": "INCONCLUSIVE",
                    "reason": f"v_- <= 0 in t-cell {i} (b_hi >= 1)",
                    "q": str(q),
                    "c": str(c),
                    "preconditions": pre,
                }
            v_lo = div_lo(SCALE - b_hi, denom_v_hi)
            if v_lo <= 0:
                return {
                    "status": "INCONCLUSIVE",
                    "reason": f"v_- <= 0 in t-cell {i}",
                    "q": str(q),
                    "c": str(c),
                    "preconditions": pre,
                }
            # v_+ = (1 + b + t/r) / (r + 1/r) <= (1 + b_hi + t_max/r_lo) / (3*r_lo)
            v_hi_new = div_hi(SCALE + b_hi + div_hi(t_max, r_lo), denom_v_lo)
            if v_hi_new < v_hi:
                v_hi = v_hi_new

        if v_lo <= 0 or v_hi <= 0:
            return {"status": "INCONCLUSIVE", "reason": f"invalid v bounds in t-cell {i}"}

        R_lo = div_lo(s_lo, v_hi)
        R_hi = div_hi(s_hi, v_lo)
        m1_hi = mul_hi(r_hi, v_hi) + b_hi
        # L = (r*s + sqrt(xi))*I / v_-
        L_hi = div_hi(mul_hi(mul_hi(r_hi, s_hi) + sqrt_xi_hi, I_hi), v_lo)

        # P = q^2 - s^2 / 2 >= 0 (exact theorem (3)/(7); clamp negative rounding at t_max to 0)
        s2_lo = mul_lo(s_lo, s_lo)
        s2_hi = mul_hi(s_hi, s_hi)
        P_lo = max(0, q2_lo - ceil_div(s2_hi, 2))
        P_hi = max(0, q2_hi - floor_div(s2_lo, 2))

        t_cells.append((t_min, t_max, s_lo, s_hi, s2_lo, s2_hi, v_lo, v_hi, b_hi, R_lo, R_hi, m1_hi, L_hi, P_lo, P_hi))

    visited = 0
    leaves = 0
    max_depth_seen = 0
    min_margin = None  # integer scaled by SCALE
    m0_exclusions = 0
    edge_boxes_checked = {"t_zero": 0, "t_max": 0, "z_zero": 0, "z_one": 0}

    for i_t, cell in enumerate(t_cells):
        (t_min, t_max, s_lo, s_hi, s2_lo, s2_hi, v_lo, v_hi, b_hi, R0_lo, R0_hi, m1_hi, L_hi, P_lo, P_hi) = cell
        v_lo2 = mul_lo(v_lo, v_lo)
        r_v_lo = mul_lo(r_lo, v_lo)
        if r_v_lo <= 0:
            return {"status": "INCONCLUSIVE", "reason": "r_lo * v_lo <= 0"}
        qb_hi = mul_hi(q_hi, b_hi)

        for i_z in range(n_z):
            z_lo = frac_lo(Fraction(i_z, n_z))
            z_hi = frac_hi(Fraction(i_z + 1, n_z))
            if i_z == 0:
                z_lo = 0
            if i_z == n_z - 1:
                z_hi = SCALE

            # sigma^2 = (1 - z) * P <= (1 - z_lo) * P_hi
            sigma2_hi = mul_hi(SCALE - z_lo, P_hi)
            # a = |mu|^2 = (s^2/2 + z*P)/r^2 = s^2 + 2*z*P, also <= 2*q^2
            a_lo = s2_lo + 2 * mul_lo(z_lo, P_lo)
            a_hi = min(s2_hi + 2 * mul_hi(z_hi, P_hi), 2 * q2_hi)
            sqrt_a_lo = sqrt_lo(a_lo)

            # Re(mu) in [(s - sqrt(2*z*P))/(2*r), (s + sqrt(2*z*P))/(2*r)]
            two_zP_hi = 2 * mul_hi(z_hi, P_hi)
            sqrt_2zP_hi = sqrt_hi(two_zP_hi)
            # Note: s - sqrt(2*z*P) can be positive; if negative, div_lo by 2*r_lo vs 2*r_hi matters!
            num_x_lo = s_lo - sqrt_2zP_hi
            if num_x_lo >= 0:
                x_lo = div_lo(num_x_lo, 2 * r_hi)
            else:
                x_lo = div_lo(num_x_lo, 2 * r_lo)
            num_x_hi = s_hi + sqrt_2zP_hi
            x_hi = div_hi(num_x_hi, 2 * r_lo)

            # Adaptive stack over (h_lo, h_hi, R_lo, R_hi, depth)
            stack = [(c_lo, SCALE, R0_lo, R0_hi, 0)]
            while stack:
                h_lo, h_hi, R_lo, R_hi, depth = stack.pop()
                visited += 1
                if depth > max_depth_seen:
                    max_depth_seen = depth

                # Track edge coverage
                if i_t == 0:
                    edge_boxes_checked["t_zero"] += 1
                if i_t == n_t - 1:
                    edge_boxes_checked["t_max"] += 1
                if i_z == 0:
                    edge_boxes_checked["z_zero"] += 1
                if i_z == n_z - 1:
                    edge_boxes_checked["z_one"] += 1

                # Step 1: Lemma 2 bounds (D_0, E, m_0)
                D0_lo = max(0, R_lo - h_hi)
                if drop_vD0:
                    var_H_hi = m1_hi
                else:
                    D0_lo2 = mul_lo(D0_lo, D0_lo)
                    var_H_hi = max(0, m1_hi - mul_lo(v_lo2, D0_lo2))
                E_hi = div_hi(qb_hi + sqrt_hi(mul_hi(sigma2_hi, var_H_hi)), r_v_lo)
                if zero_m0:
                    m0_lo = 0
                else:
                    m0_lo = max(0, mul_lo(sqrt_a_lo, D0_lo) - E_hi)

                if (not zero_m0) and (m0_lo > q_hi):
                    leaves += 1
                    m0_exclusions += 1
                    continue

                # Step 2: Upper bound U_*
                one_minus_h2_hi = max(0, SCALE - mul_lo(h_lo, h_lo))
                q2_minus_m02_hi = max(0, q2_hi - mul_lo(m0_lo, m0_lo))
                cov_hi = sqrt_hi(mul_hi(one_minus_h2_hi, q2_minus_m02_hi))
                U_hi = L_hi + mul_hi(h_hi, E_hi) + cov_hi + delta_hi

                # Step 3: Check (h, R) monotonicity conditions & full (x', a) rectangle 0 < A_1 < 2*A_2
                excluded = False
                margin = None
                h_hi2 = mul_hi(h_hi, h_hi)
                cond_mono1 = (x_lo > 0) and (mul_hi(R_hi, a_hi) < 2 * x_lo)
                cond_mono2 = R_lo > mul_hi(h_hi2, x_hi)
                cond_mono3 = mul_hi(h_hi2, a_hi) < mul_lo(R_lo, x_lo)

                if cond_mono1 and cond_mono2 and cond_mono3:
                    # Evaluate at (h_lo, R_hi) over the entire rectangle [x_lo, x_hi] x [a_lo, a_hi]
                    h_lo2_lo = mul_lo(h_lo, h_lo)
                    h_lo2_hi = mul_hi(h_lo, h_lo)
                    h_lo4_lo = mul_lo(h_lo2_lo, h_lo2_lo)
                    h_lo4_hi = mul_hi(h_lo2_hi, h_lo2_hi)
                    R_hi2_lo = mul_lo(R_hi, R_hi)
                    R_hi2_hi = mul_hi(R_hi, R_hi)

                    # Minimum radicand of A1^2 / h^2 over (x', a) is at (x_hi, a_lo)
                    A1_rad_min_lo = 4 * SCALE - 4 * mul_hi(R_hi, x_hi) + mul_lo(a_lo, R_hi2_lo)
                    # Minimum radicand of A2^2 at (h_lo, R_hi) over (x', a) is at (x_hi, a_lo)
                    A2_rad_min_lo = R_hi2_lo - 2 * mul_hi(R_hi, mul_hi(h_lo2_hi, x_hi)) + mul_lo(a_lo, h_lo4_lo)
                    # Maximum radicand of A1^2 / h^2 over (x', a) is at (x_lo, a_hi)
                    A1_rad_max_hi = 4 * SCALE - 4 * mul_lo(R_hi, x_lo) + mul_hi(a_hi, R_hi2_hi)

                    if A1_rad_min_lo > 0 and A2_rad_min_lo > 0 and A1_rad_max_hi > 0:
                        # Check A1_max^2 < 4 * A2_min^2 on the full (x', a) rectangle
                        if mul_hi(h_lo2_hi, A1_rad_max_hi) < 4 * A2_rad_min_lo:
                            # Monotonicity in x' certified! Evaluate at x' = x_hi:
                            # A1 >= h_lo * sqrt(A1_rad_min_lo) (uses a_lo)
                            # A2 <= sqrt(R_hi^2 - 2*R_hi*h_lo^2*x_hi + a_hi*h_lo^4) (uses a_hi)
                            A1_lo = mul_lo(h_lo, sqrt_lo(A1_rad_min_lo))
                            A2_rad_xhi_hi = R_hi2_hi - 2 * mul_lo(R_hi, mul_lo(h_lo2_lo, x_hi)) + mul_hi(a_hi, h_lo4_hi)
                            if A2_rad_xhi_hi >= 0:
                                A2_hi = sqrt_hi(A2_rad_xhi_hi)
                                margin = (A1_lo - A2_hi) - U_hi
                                if margin > 0:
                                    excluded = True

                if excluded:
                    leaves += 1
                    if min_margin is None or margin < min_margin:
                        min_margin = margin
                else:
                    if depth >= max_depth:
                        return {
                            "status": "INCONCLUSIVE",
                            "reason": "max_depth reached on undecided box",
                            "q": str(q),
                            "c": str(c),
                            "preconditions": pre,
                            "visited": visited,
                            "leaves": leaves,
                            "failed_cell": {"i_t": i_t, "i_z": i_z, "depth": depth,
                                            "h": [h_lo / SCALE, h_hi / SCALE],
                                            "R": [R_lo / SCALE, R_hi / SCALE],
                                            "margin": margin / SCALE if margin is not None else None},
                            "elapsed_sec": round(time.time() - t0, 4),
                        }
                    # Bisect the wider of h and R into two closed halves
                    if (h_hi - h_lo) >= (R_hi - R_lo):
                        mid = (h_lo + h_hi) // 2
                        if mid == h_lo or mid == h_hi:
                            return {"status": "INCONCLUSIVE", "reason": "h interval indivisible"}
                        stack.append((h_lo, mid, R_lo, R_hi, depth + 1))
                        stack.append((mid, h_hi, R_lo, R_hi, depth + 1))
                    else:
                        mid = (R_lo + R_hi) // 2
                        if mid == R_lo or mid == R_hi:
                            return {"status": "INCONCLUSIVE", "reason": "R interval indivisible"}
                        stack.append((h_lo, h_hi, R_lo, mid, depth + 1))
                        stack.append((h_lo, h_hi, mid, R_hi, depth + 1))

    return {
        "status": "CERTIFIED",
        "q": str(q),
        "c": str(c),
        "preconditions": pre,
        "grid": [n_t, n_z],
        "v_iters": v_iters,
        "visited": visited,
        "leaves": leaves,
        "binary_tree_check": (visited == 2 * leaves - n_t * n_z),
        "max_depth_seen": max_depth_seen,
        "m0_exclusions": m0_exclusions,
        "min_margin_exact_int": min_margin,
        "min_margin_float": (min_margin / SCALE) if min_margin is not None else None,
        "edge_boxes_checked": edge_boxes_checked,
        "elapsed_sec": round(time.time() - t0, 4),
    }


# ---------------------------------------------------------------------------
# Primitive unit tests (>= 10^4 random rationals against 100-digit mpmath)
# ---------------------------------------------------------------------------
def run_primitive_unit_tests(n_trials: int = 12000):
    import mpmath
    mpmath.mp.dps = 100
    mpmath.iv.dps = 100
    S_iv = mpmath.iv.mpf(SCALE)
    rng = random.Random(20261125)

    # 1. r enclosure
    r_lo, r_hi = r_enclosure()
    r_true_iv = mpmath.iv.mpf(1) / mpmath.iv.sqrt(mpmath.iv.mpf(2))
    r_scaled_iv = r_true_iv * S_iv
    assert mpmath.iv.mpf(r_lo) <= r_scaled_iv and r_scaled_iv <= mpmath.iv.mpf(r_hi)
    assert (r_hi - r_lo) <= 1

    # 2. Random rationals for frac_lo/hi, sqrt_lo/hi, mul_lo/hi, div_lo/hi, isqrt
    for idx in range(n_trials):
        den1 = rng.randint(1, 10 ** 9)
        num1 = rng.randint(0, 10 ** 10)
        den2 = rng.randint(1, 10 ** 9)
        num2 = rng.randint(1, 10 ** 10)
        f1 = Fraction(num1, den1)
        f2 = Fraction(num2, den2)

        # frac_lo / frac_hi (exact integer check + 100-digit mpmath.iv check)
        lo1, hi1 = frac_lo(f1), frac_hi(f1)
        assert lo1 * den1 <= num1 * SCALE <= hi1 * den1
        x1_scaled_iv = (mpmath.iv.mpf(num1) * S_iv) / mpmath.iv.mpf(den1)
        assert (mpmath.iv.mpf(lo1) <= x1_scaled_iv) or (lo1 in x1_scaled_iv)
        assert (x1_scaled_iv <= mpmath.iv.mpf(hi1)) or (hi1 in x1_scaled_iv)
        assert hi1 - lo1 <= 1

        # Exact square root on scaled integer (including exact squares)
        if idx % 20 == 0:
            k_sq = rng.randint(0, 10 ** 12)
            a_int = k_sq * k_sq
        else:
            a_int = lo1
        slo, shi = sqrt_lo(a_int), sqrt_hi(a_int)
        assert slo * slo <= a_int * SCALE <= shi * shi
        sx_scaled_iv = mpmath.iv.sqrt(mpmath.iv.mpf(a_int) * S_iv)
        assert (mpmath.iv.mpf(slo) <= sx_scaled_iv) or (slo in sx_scaled_iv)
        assert (sx_scaled_iv <= mpmath.iv.mpf(shi)) or (shi in sx_scaled_iv)
        assert shi - slo <= 1
        k_isq = math.isqrt(a_int)
        assert k_isq * k_isq <= a_int < (k_isq + 1) * (k_isq + 1)

        # Signed multiplication
        sign1 = -1 if (idx % 3 == 0) else 1
        sign2 = -1 if (idx % 5 == 0) else 1
        a_s = sign1 * lo1
        b_s = sign2 * frac_lo(f2)
        mlo, mhi = mul_lo(a_s, b_s), mul_hi(a_s, b_s)
        assert mlo * SCALE <= a_s * b_s <= mhi * SCALE
        prod_scaled_iv = (mpmath.iv.mpf(a_s) * mpmath.iv.mpf(b_s)) / S_iv
        assert (mpmath.iv.mpf(mlo) <= prod_scaled_iv) or (mlo in prod_scaled_iv)
        assert (prod_scaled_iv <= mpmath.iv.mpf(mhi)) or (mhi in prod_scaled_iv)
        assert mhi - mlo <= 1

        # Signed numerator / positive denominator division
        b_pos = max(1, frac_lo(f2))
        dlo, dhi = div_lo(a_s, b_pos), div_hi(a_s, b_pos)
        assert dlo * b_pos <= a_s * SCALE <= dhi * b_pos
        quot_scaled_iv = (mpmath.iv.mpf(a_s) * S_iv) / mpmath.iv.mpf(b_pos)
        assert (mpmath.iv.mpf(dlo) <= quot_scaled_iv) or (dlo in quot_scaled_iv)
        assert (quot_scaled_iv <= mpmath.iv.mpf(dhi)) or (dhi in quot_scaled_iv)
        assert dhi - dlo <= 1

    return {
        "n_trials": n_trials,
        "mpmath_iv_dps": 100,
        "r_lo": r_lo,
        "r_hi": r_hi,
        "r_width_scaled": r_hi - r_lo,
        "all_passed": True,
    }


def main():
    out = {}
    print("Running primitive unit tests (12,000 random rationals vs 100-digit mpmath)...")
    out["unit_tests"] = run_primitive_unit_tests(12000)
    print("  Unit tests PASSED:", out["unit_tests"]["n_trials"], "trials")

    # Main claim: q = 501/1000, c = 9657/10000
    print("\nRunning Verifier A main check (q = 501/1000, c = 9657/10000)...")
    out["main_501"] = verify_theorem1_a(Fraction(501, 1000), Fraction(9657, 10000))
    print(f"  main_501: {out['main_501']['status']} | visited={out['main_501'].get('visited')} "
          f"leaves={out['main_501'].get('leaves')} depth={out['main_501'].get('max_depth_seen')} "
          f"min_margin={out['main_501'].get('min_margin_float'):.3e} ({out['main_501']['elapsed_sec']}s)")

    # Also test q = 5001/10000 (1x1 single box)
    out["main_5001_1box"] = verify_theorem1_a(Fraction(5001, 10000), Fraction(9657, 10000), n_t=1, n_z=1, v_iters=1, max_depth=0)
    print(f"  main_5001_1box: {out['main_5001_1box']['status']} | min_margin={out['main_5001_1box'].get('min_margin_float'):.6f}")

    # Controls
    print("\nRunning controls...")
    controls = {}
    # Red preconditions
    controls["red_pre_q05016"] = verify_theorem1_a(Fraction(5016, 10000), Fraction(9657, 10000))
    controls["red_pre_q05019"] = verify_theorem1_a(Fraction(5019, 10000), Fraction(9657, 10000))
    controls["red_pre_q05019_c096_index_only"] = verify_theorem1_a(Fraction(5019, 10000), Fraction(96, 100))
    controls["red_pre_c099"] = verify_theorem1_a(Fraction(501, 1000), Fraction(99, 100))
    # Also verify that c=0.99 WOULD pass separation if preconditions were bypassed (demonstrating why precondition check is critical!)
    controls["red_pre_c099_bypassed_sep"] = verify_theorem1_a(Fraction(501, 1000), Fraction(99, 100), bypass_preconditions=True)
    # Red separation
    controls["red_sep_q05012"] = verify_theorem1_a(Fraction(5012, 10000), Fraction(9657, 10000), max_depth=8)
    controls["red_sep_c095"] = verify_theorem1_a(Fraction(501, 1000), Fraction(95, 100), max_depth=8)
    # Red mutation: m0 := 0
    controls["red_mut_m0_zero"] = verify_theorem1_a(Fraction(501, 1000), Fraction(9657, 10000), zero_m0=True, max_depth=8)
    # Positive control: drop v_-^2 D_0^2
    controls["pos_drop_vD0"] = verify_theorem1_a(Fraction(501, 1000), Fraction(9657, 10000), drop_vD0=True, max_depth=12)

    for k, v in controls.items():
        print(f"  {k:28s}: {v['status']} (pre_ok={v.get('preconditions', {}).get('ok')}, "
              f"reason={v.get('reason', v.get('preconditions', {}).get('reasons'))}, "
              f"visited={v.get('visited')}, leaves={v.get('leaves')})")
    out["controls"] = controls

    # Diagnostics:
    # 1. Bisect certified q_max at c = 9657/10000
    print("\nBisecting certified q_max (Verifier A)...")
    q_lo_b = Fraction(50100, 100000)
    q_hi_b = Fraction(50120, 100000)
    q_steps = []
    for _ in range(16):
        q_mid = (q_lo_b + q_hi_b) / 2
        res = verify_theorem1_a(q_mid, Fraction(9657, 10000), max_depth=10)
        q_steps.append({"q": float(q_mid), "status": res["status"], "leaves": res.get("leaves")})
        if res["status"] == "CERTIFIED":
            q_lo_b = q_mid
        else:
            q_hi_b = q_mid
    out["diag_q_max"] = {"q_certified_lo": float(q_lo_b), "q_failed_hi": float(q_hi_b), "steps": q_steps}
    print(f"  q_max in [{float(q_lo_b):.8f}, {float(q_hi_b):.8f}]")

    # 2. Bisect U_* inflation margin delta at q = 501/1000
    print("Bisecting U_* inflation margin delta (Verifier A)...")
    d_lo = Fraction(0)
    d_hi = Fraction(1, 100)  # 0.01
    d_steps = []
    for _ in range(16):
        d_mid = (d_lo + d_hi) / 2
        res = verify_theorem1_a(Fraction(501, 1000), Fraction(9657, 10000), max_depth=10, delta_inflate=d_mid)
        d_steps.append({"delta": float(d_mid), "status": res["status"], "leaves": res.get("leaves")})
        if res["status"] == "CERTIFIED":
            d_lo = d_mid
        else:
            d_hi = d_mid
    out["diag_delta_margin"] = {"delta_certified_lo": float(d_lo), "delta_failed_hi": float(d_hi), "steps": d_steps}
    print(f"  delta_margin in [{float(d_lo):.8f}, {float(d_hi):.8f}]")

    with open("verifier_a_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nSaved verifier_a_results.json")


if __name__ == "__main__":
    main()
