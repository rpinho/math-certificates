#!/usr/bin/env python3
"""Verifier B: Separate clean-room python-flint (Arb) lower-bound verifier (same agent, separate implementation).

Deliberately distinct from Verifier A in three ways:
  1. Uses 160-bit Arb ball arithmetic (python-flint) instead of scaled integers.
  2. Uses a 64 x 48 outer grid on (u, z) in [0, 1]^2 and 7 v-iterations.
  3. Evaluates the squared separation inequality directly in ball arithmetic
       4*h^2 - R^2 + a*h^2*(R^2 - h^2) - 2*h^2*R*x' > U_* * (2*A_2 + U_*)
     with 3-variable adaptive bisection in (h, R, x') (bypassing Verifier A's
     (h, R) and x' monotonicity reduction completely).

Explicitly verifies both analytic preconditions (c-precondition and index precondition),
checks v_- > 0 strictly before division, rejects any NaN/infinite/indeterminate comparison
(never treating indeterminate as pass), survives boundary boxes (t=0, t=t_max where P=0,
z=0, z=1), and runs the full control + diagnostic suite.
"""
from fractions import Fraction
import json
import time
import flint

ARB_PREC = 160


def strict_gt(a: flint.arb, b: flint.arb) -> bool:
    if not (a.is_finite() and b.is_finite()):
        return False
    return bool(a > b)


def strict_lt(a: flint.arb, b: flint.arb) -> bool:
    if not (a.is_finite() and b.is_finite()):
        return False
    return bool(a < b)


def strict_ge(a: flint.arb, b: flint.arb) -> bool:
    if not (a.is_finite() and b.is_finite()):
        return False
    return bool(a >= b)


def strict_le(a: flint.arb, b: flint.arb) -> bool:
    if not (a.is_finite() and b.is_finite()):
        return False
    return bool(a <= b)


def frac_to_arb(x: Fraction) -> flint.arb:
    return flint.arb(x.numerator) / flint.arb(x.denominator)


def split_arb(x: flint.arb):
    """Split a closed Arb ball x into two closed balls [lo, mid] and [mid, hi] covering x with zero gap."""
    lo = flint.arb(x.lower())
    hi = flint.arb(x.upper())
    mid = flint.arb(x.mid())
    return lo.union(mid), mid.union(hi)


def check_preconditions_arb(q: Fraction, c: Fraction):
    """Verify all preconditions strictly in Arb ball arithmetic."""
    ZERO = flint.arb(0)
    ONE = flint.arb(1)
    HALF = ONE / 2
    QUARTER = ONE / 4

    q_b = frac_to_arb(q)
    c_b = frac_to_arb(c)
    r_b = ONE / flint.arb(2).sqrt()

    reasons = []
    p1 = strict_gt(q_b, HALF) and strict_lt(q_b, r_b)
    if not p1:
        reasons.append("FAIL_RANGE_Q: requires 1/2 < q < 1/sqrt(2)")

    p2_range = strict_gt(c_b, ZERO) and strict_lt(c_b, ONE)
    if p2_range:
        c_rhs = 2 * c_b * (ONE - c_b * c_b).sqrt()
        p2 = strict_lt(q_b, c_rhs)
    else:
        p2 = False
    if not p2:
        reasons.append("FAIL_C_PRECONDITION: requires 0 < c < 1 and q < 2*c*sqrt(1-c^2)")

    xi_b = q_b * q_b - QUARTER
    if strict_ge(xi_b, ZERO):
        p3 = strict_le(r_b + xi_b.sqrt() + QUARTER, ONE)
    else:
        p3 = False
    if not p3:
        reasons.append("FAIL_INDEX_PRECONDITION: requires r + sqrt(q^2 - 1/4) + 1/4 <= 1")

    return {
        "ok": len(reasons) == 0,
        "p1_q_in_range": p1,
        "p2_c_precondition": p2,
        "p3_index_precondition": p3,
        "reasons": reasons,
    }


def verify_theorem1_b(
    q: Fraction,
    c: Fraction = Fraction(9657, 10000),
    n_t: int = 64,
    n_z: int = 48,
    v_iters: int = 7,
    max_depth: int = 14,
    zero_m0: bool = False,
    drop_vD0: bool = False,
    delta_inflate: Fraction = Fraction(0),
    bypass_preconditions: bool = False,
    prec: int = ARB_PREC,
):
    old_prec = flint.ctx.prec
    flint.ctx.prec = prec
    t0 = time.time()
    try:
        pre = check_preconditions_arb(q, c)
        if not pre["ok"] and not bypass_preconditions:
            return {
                "status": "PRECONDITION_FAILED",
                "q": str(q),
                "c": str(c),
                "preconditions": pre,
                "elapsed_sec": round(time.time() - t0, 4),
            }

        ZERO = flint.arb(0)
        ONE = flint.arb(1)
        TWO = flint.arb(2)
        FOUR = flint.arb(4)
        HALF = ONE / TWO

        q_b = frac_to_arb(q)
        q2_b = q_b * q_b
        c_b = frac_to_arb(c)
        r_b = ONE / TWO.sqrt()
        denom_v_b = r_b + ONE / r_b  # = 3*r
        xi_b = q2_b - ONE / FOUR
        if not strict_ge(xi_b, ZERO):
            return {"status": "INCONCLUSIVE", "reason": "xi not certified >= 0"}
        sqrt_xi_b = xi_b.sqrt()
        delta_b = frac_to_arb(delta_inflate)
        q_minus_half = q_b - HALF
        if not strict_gt(q_minus_half, ZERO):
            return {"status": "INCONCLUSIVE", "reason": "q - 1/2 not > 0"}

        c_lo = flint.arb(c_b.lower())
        h0_ball = c_lo.union(ONE)

        # Precompute outer t-cells
        t_cells = []
        for i_t in range(n_t):
            u_lo = flint.arb(i_t) / flint.arb(n_t)
            u_hi = flint.arb(i_t + 1) / flint.arb(n_t)
            u_ball = u_lo.union(u_hi)
            t_ball = u_ball * q_minus_half / r_b
            t_hi = flint.arb(t_ball.upper())
            s_ball = r_b + t_ball
            s_hi = flint.arb(s_ball.upper())
            I_hi = flint.arb((t_hi / (ONE - r_b)).upper())

            v_hi = s_hi
            v_lo = ZERO
            b_hi = ZERO
            for _ in range(v_iters):
                rad_b = TWO * xi_b * v_hi * v_hi + TWO * t_hi * v_hi
                if not strict_ge(rad_b, ZERO):
                    return {"status": "INCONCLUSIVE", "reason": f"rad_b < 0 in t-cell {i_t}"}
                b_hi = flint.arb((r_b * I_hi + rad_b.sqrt()).upper())
                v_lo_ball = (ONE - b_hi) / denom_v_b
                if not strict_gt(v_lo_ball, ZERO):
                    return {
                        "status": "INCONCLUSIVE",
                        "reason": f"v_- <= 0 in t-cell {i_t}",
                        "q": str(q),
                        "c": str(c),
                        "preconditions": pre,
                    }
                v_lo = flint.arb(v_lo_ball.lower())
                v_hi_new = flint.arb(((ONE + b_hi + t_hi / r_b) / denom_v_b).upper())
                v_hi = v_hi.min(v_hi_new)

            if not (strict_gt(v_lo, ZERO) and strict_gt(v_hi, ZERO)):
                return {"status": "INCONCLUSIVE", "reason": f"invalid v bounds in t-cell {i_t}"}

            v_ball = v_lo.union(v_hi)
            R0_ball = s_ball / v_ball
            m1_hi = flint.arb((r_b * v_hi + b_hi).upper())
            L_hi = flint.arb(((r_b * s_hi + sqrt_xi_b) * I_hi / v_lo).upper())

            # P = q^2 - s^2/2 >= 0 (theorem (3)/(7)); nonnegative_part handles boundary t=t_max where 0 in P
            P_raw = q2_b - (s_ball * s_ball) / TWO
            if not strict_ge(flint.arb(P_raw.upper()), ZERO):
                # Entire cell has s > q/r strictly (infeasible)
                continue
            P_ball = P_raw.nonnegative_part()
            t_cells.append((i_t, s_ball, v_lo, b_hi, R0_ball, m1_hi, L_hi, P_ball))

        visited = 0
        leaves = 0
        max_depth_seen = 0
        min_sq_margin = None
        m0_exclusions = 0
        edge_boxes_checked = {"t_zero": 0, "t_max": 0, "z_zero": 0, "z_one": 0}

        for (i_t, s_ball, v_lo, b_hi, R0_ball, m1_hi, L_hi, P_ball) in t_cells:
            v_lo2 = v_lo * v_lo
            r_v_lo = r_b * v_lo
            qb_hi = flint.arb((q_b * b_hi).upper())
            P_hi = flint.arb(P_ball.upper())

            for i_z in range(n_z):
                z_lo_b = flint.arb(i_z) / flint.arb(n_z)
                z_hi_b = flint.arb(i_z + 1) / flint.arb(n_z)
                z_ball = z_lo_b.union(z_hi_b)

                sigma2_hi = flint.arb(((ONE - z_lo_b) * P_hi).upper())
                # a = |mu|^2 = (s^2/2 + z*P)/r^2 = s^2 + 2*z*P, bounded above by 2*q^2
                a_raw = (s_ball * s_ball / TWO + z_ball * P_ball) / (r_b * r_b)
                a_lo_b = flint.arb(a_raw.lower()).max(ZERO)
                a_hi_b = flint.arb(a_raw.upper()).min(flint.arb((TWO * q2_b).upper()))
                a_ball = a_lo_b.union(a_hi_b)
                sqrt_a_lo = a_lo_b.sqrt()

                # x' = Re(mu) in [(s - sqrt(2*z*P))/(2*r), (s + sqrt(2*z*P))/(2*r)]
                two_zP_hi = flint.arb((TWO * z_hi_b * P_hi).upper())
                sqrt_2zP_hi = two_zP_hi.sqrt()
                x_lo_b = flint.arb(((flint.arb(s_ball.lower()) - sqrt_2zP_hi) / (TWO * r_b)).lower())
                x_hi_b = flint.arb(((flint.arb(s_ball.upper()) + sqrt_2zP_hi) / (TWO * r_b)).upper())
                x0_ball = x_lo_b.union(x_hi_b)

                stack = [(h0_ball, R0_ball, x0_ball, 0)]
                while stack:
                    h_b, R_b, x_b, depth = stack.pop()
                    visited += 1
                    if depth > max_depth_seen:
                        max_depth_seen = depth

                    if i_t == 0:
                        edge_boxes_checked["t_zero"] += 1
                    if i_t == n_t - 1:
                        edge_boxes_checked["t_max"] += 1
                    if i_z == 0:
                        edge_boxes_checked["z_zero"] += 1
                    if i_z == n_z - 1:
                        edge_boxes_checked["z_one"] += 1

                    h_lo = flint.arb(h_b.lower())
                    h_hi = flint.arb(h_b.upper())
                    R_lo = flint.arb(R_b.lower())

                    # Lemma 2: D_0, E, m_0
                    D0_lo = flint.arb((R_lo - h_hi).lower()).max(ZERO)
                    if drop_vD0:
                        var_H_hi = m1_hi
                    else:
                        var_H_hi = flint.arb((m1_hi - v_lo2 * D0_lo * D0_lo).upper()).max(ZERO)
                    E_hi = flint.arb(((qb_hi + (sigma2_hi * var_H_hi).sqrt()) / r_v_lo).upper())
                    if zero_m0:
                        m0_lo = ZERO
                    else:
                        m0_lo = flint.arb((sqrt_a_lo * D0_lo - E_hi).lower()).max(ZERO)

                    if (not zero_m0) and strict_gt(m0_lo, q_b):
                        leaves += 1
                        m0_exclusions += 1
                        continue

                    # U_* upper bound
                    one_m_h2_hi = flint.arb((ONE - h_lo * h_lo).upper()).max(ZERO)
                    q2_m_m02_hi = flint.arb((q2_b - m0_lo * m0_lo).upper()).max(ZERO)
                    U_hi = flint.arb((L_hi + h_hi * E_hi + (one_m_h2_hi * q2_m_m02_hi).sqrt() + delta_b).upper())

                    # Squared inequality directly in Arb ball arithmetic:
                    # 4*h^2 - R^2 + a*h^2*(R^2 - h^2) - 2*h^2*R*x'
                    #   = h^2*(4 - a*h^2) - R^2*(1 - a*h^2) - 2*h^2*R*x'
                    # (algebraically identical, eliminates opposing-sign R^2 dependency)
                    h2 = h_b * h_b
                    R2 = R_b * R_b
                    ah2 = a_ball * h2
                    lhs = h2 * (FOUR - ah2) - R2 * (ONE - ah2) - TWO * h2 * R_b * x_b
                    A2_rad = R2 - TWO * R_b * h2 * x_b + ah2 * h2

                    excluded = False
                    sq_margin = None
                    if strict_ge(A2_rad, ZERO):
                        A2_b = A2_rad.sqrt()
                        rhs = U_hi * (TWO * A2_b + U_hi)
                        diff = lhs - rhs
                        if strict_gt(diff, ZERO):
                            excluded = True
                            sq_margin = float(diff.lower())

                    if excluded:
                        leaves += 1
                        if min_sq_margin is None or sq_margin < min_sq_margin:
                            min_sq_margin = sq_margin
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
                                "failed_cell": {
                                    "i_t": i_t, "i_z": i_z, "depth": depth,
                                    "h": [float(h_lo), float(h_hi)],
                                    "R": [float(R_lo), float(R_b.upper())],
                                    "x": [float(x_b.lower()), float(x_b.upper())],
                                },
                                "elapsed_sec": round(time.time() - t0, 4),
                            }
                        # Floating-point heuristic selects splitting coordinate among h, R, x'
                        wh = float(h_b.rad())
                        wR = float(R_b.rad())
                        wx = float(x_b.rad())
                        if wh >= wR and wh >= wx:
                            h1, h2_s = split_arb(h_b)
                            stack.append((h1, R_b, x_b, depth + 1))
                            stack.append((h2_s, R_b, x_b, depth + 1))
                        elif wR >= wx:
                            R1, R2_s = split_arb(R_b)
                            stack.append((h_b, R1, x_b, depth + 1))
                            stack.append((h_b, R2_s, x_b, depth + 1))
                        else:
                            x1, x2_s = split_arb(x_b)
                            stack.append((h_b, R_b, x1, depth + 1))
                            stack.append((h_b, R_b, x2_s, depth + 1))

        return {
            "status": "CERTIFIED",
            "q": str(q),
            "c": str(c),
            "prec_bits": prec,
            "preconditions": pre,
            "grid": [n_t, n_z],
            "v_iters": v_iters,
            "visited": visited,
            "leaves": leaves,
            "binary_tree_check": (visited == 2 * leaves - n_t * n_z),
            "max_depth_seen": max_depth_seen,
            "m0_exclusions": m0_exclusions,
            "min_sq_margin_float": min_sq_margin,
            "edge_boxes_checked": edge_boxes_checked,
            "elapsed_sec": round(time.time() - t0, 4),
        }
    finally:
        flint.ctx.prec = old_prec


def run_nan_and_indeterminate_unit_tests():
    """Verify explicitly that NaN, Inf, and overlapping Arb balls NEVER pass strict comparisons."""
    flint.ctx.prec = ARB_PREC
    nan_b = flint.arb("nan")
    inf_b = flint.arb("inf")
    ninf_b = flint.arb("-inf")
    one = flint.arb(1)
    overlap_a = flint.arb("1.0", "0.2")
    overlap_b = flint.arb("1.1", "0.2")
    disjoint_a = flint.arb("1.0", "0.01")
    disjoint_b = flint.arb("1.1", "0.01")

    assert not strict_gt(nan_b, one)
    assert not strict_gt(one, nan_b)
    assert not strict_lt(nan_b, one)
    assert not strict_ge(nan_b, one)
    assert not strict_le(nan_b, one)
    assert not strict_gt(inf_b, one)
    assert not strict_lt(ninf_b, one)
    assert not strict_gt(overlap_b, overlap_a)
    assert not strict_lt(overlap_a, overlap_b)
    assert strict_gt(disjoint_b, disjoint_a)
    assert strict_lt(disjoint_a, disjoint_b)
    # Also test sqrt of negative ball yields NaN and fails strict_gt
    neg_sqrt = flint.arb("-0.1", "0.01").sqrt()
    assert not strict_gt(neg_sqrt, flint.arb(-100))
    return {"all_passed": True}


def main():
    out = {}
    out["nan_indeterminate_tests"] = run_nan_and_indeterminate_unit_tests()
    print("NaN / indeterminate comparison tests PASSED.")

    print("\nRunning Verifier B main check (q = 501/1000, c = 9657/10000, 160-bit Arb, squared inequality)...")
    out["main_501"] = verify_theorem1_b(Fraction(501, 1000), Fraction(9657, 10000))
    print(f"  main_501: {out['main_501']['status']} | visited={out['main_501'].get('visited')} "
          f"leaves={out['main_501'].get('leaves')} depth={out['main_501'].get('max_depth_seen')} "
          f"min_sq_margin={out['main_501'].get('min_sq_margin_float'):.3e} ({out['main_501']['elapsed_sec']}s)")

    print("\nRunning Verifier B controls...")
    controls = {}
    controls["red_pre_q05016"] = verify_theorem1_b(Fraction(5016, 10000), Fraction(9657, 10000))
    controls["red_pre_q05019"] = verify_theorem1_b(Fraction(5019, 10000), Fraction(9657, 10000))
    controls["red_pre_q05019_c096_index_only"] = verify_theorem1_b(Fraction(5019, 10000), Fraction(96, 100))
    controls["red_pre_c099"] = verify_theorem1_b(Fraction(501, 1000), Fraction(99, 100))
    controls["red_pre_c099_bypassed_sep"] = verify_theorem1_b(Fraction(501, 1000), Fraction(99, 100), bypass_preconditions=True)
    controls["red_sep_q05012"] = verify_theorem1_b(Fraction(5012, 10000), Fraction(9657, 10000), max_depth=12)
    controls["red_sep_c095"] = verify_theorem1_b(Fraction(501, 1000), Fraction(95, 100), max_depth=12)
    controls["red_mut_m0_zero"] = verify_theorem1_b(Fraction(501, 1000), Fraction(9657, 10000), zero_m0=True, max_depth=12)
    controls["pos_drop_vD0"] = verify_theorem1_b(Fraction(501, 1000), Fraction(9657, 10000), drop_vD0=True, max_depth=18)

    for k, v in controls.items():
        print(f"  {k:28s}: {v['status']} (pre_ok={v.get('preconditions', {}).get('ok')}, "
              f"reason={v.get('reason', v.get('preconditions', {}).get('reasons'))}, "
              f"visited={v.get('visited')}, leaves={v.get('leaves')}, t={v.get('elapsed_sec')}s)")
    out["controls"] = controls

    print("\nBisecting certified q_max (Verifier B)...")
    q_lo_b = Fraction(50100, 100000)
    q_hi_b = Fraction(50120, 100000)
    q_steps = []
    for _ in range(14):
        q_mid = (q_lo_b + q_hi_b) / 2
        res = verify_theorem1_b(q_mid, Fraction(9657, 10000), max_depth=14)
        q_steps.append({"q": float(q_mid), "status": res["status"], "leaves": res.get("leaves")})
        if res["status"] == "CERTIFIED":
            q_lo_b = q_mid
        else:
            q_hi_b = q_mid
    out["diag_q_max"] = {"q_certified_lo": float(q_lo_b), "q_failed_hi": float(q_hi_b), "steps": q_steps}
    print(f"  q_max in [{float(q_lo_b):.8f}, {float(q_hi_b):.8f}]")

    print("Bisecting U_* inflation margin delta (Verifier B)...")
    d_lo = Fraction(0)
    d_hi = Fraction(1, 100)
    d_steps = []
    for _ in range(14):
        d_mid = (d_lo + d_hi) / 2
        res = verify_theorem1_b(Fraction(501, 1000), Fraction(9657, 10000), max_depth=14, delta_inflate=d_mid)
        d_steps.append({"delta": float(d_mid), "status": res["status"], "leaves": res.get("leaves")})
        if res["status"] == "CERTIFIED":
            d_lo = d_mid
        else:
            d_hi = d_mid
    out["diag_delta_margin"] = {"delta_certified_lo": float(d_lo), "delta_failed_hi": float(d_hi), "steps": d_steps}
    print(f"  delta_margin in [{float(d_lo):.8f}, {float(d_hi):.8f}]")

    with open("verifier_b_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nSaved verifier_b_results.json")


if __name__ == "__main__":
    main()
