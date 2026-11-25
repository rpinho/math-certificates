#!/usr/bin/env python3
"""T2-lite: Data and hypotheses check for Theorem 2 (Theorem 4 in PDF, C_42 <= 0.6863607438).

Checks:
  1. SHA-256 of inputs/upper99-tight.json against manuscript hash 0d28149b...
  2. Exact knot set equality against {j^2/18432 : 0<=j<=96} U {1/73728, 1/36864, 1/9216}.
  3. Rational T = 3431803719/5000000000 = 0.6863607438 consistency.
  4. Phase and knot diff vs Vatopoulos's whitelisted public data file results/A_D96_4.json (if fetched).
  5. 256-bit Arb check of Re(gamma) >= 0 and sup|d_0| < 1 via |d_0(v)| = 2*T*|sin((phi(0)-phi(v))/2)|
     across all 99 piecewise-linear segments and on (1/2, 1].
  6. Two red controls:
       - Red 1: rotated phi(0) making Re(gamma) < 0 (must fail Re(gamma) >= 0).
       - Red 2: shifted phase making sup|d_0| >= 1 (must fail sup|d_0| < 1).
  7. Exact rational + Arb recomputation of 0.197467474154 / 0.287702168300 vs 0.686360743542159 and T.

Verdict scope: "hypotheses checked; F < T not replayed".
"""
from fractions import Fraction
import hashlib
import json
import os
import time
import flint

EXPECTED_SHA256 = "0d28149baf0accae7dc073a36417fdb7151c502704de2db5b3293aa815ce0eb0"
EXPECTED_T = Fraction(3431803719, 5000000000)


def strict_gt(a: flint.arb, b: flint.arb) -> bool:
    return a.is_finite() and b.is_finite() and bool(a > b)


def strict_ge(a: flint.arb, b: flint.arb) -> bool:
    return a.is_finite() and b.is_finite() and bool(a >= b)


def strict_lt(a: flint.arb, b: flint.arb) -> bool:
    return a.is_finite() and b.is_finite() and bool(a < b)


def frac_to_arb(x: Fraction) -> flint.arb:
    return flint.arb(x.numerator) / flint.arb(x.denominator)


def check_hypotheses_arb(T_frac: Fraction, phases_str, prec: int = 256):
    """Verify Re(gamma) >= 0 and sup_{v in (0,1]} |d_0(v)| < 1 rigorously in Arb."""
    old_prec = flint.ctx.prec
    flint.ctx.prec = prec
    try:
        ZERO = flint.arb(0)
        ONE = flint.arb(1)
        TWO = flint.arb(2)

        T_b = frac_to_arb(T_frac)
        phi_balls = [frac_to_arb(Fraction(p)) for p in phases_str]
        phi0 = phi_balls[0]

        # gamma = T * exp(i * phi(0)) => Re(gamma) = T * cos(phi(0))
        re_gamma = T_b * phi0.cos()
        re_gamma_ge_0 = strict_ge(re_gamma, ZERO)
        re_gamma_gt_0 = strict_gt(re_gamma, ZERO)

        # On (0, 1/2]: |d_0(v)| = 2 * T * |sin((phi(0) - phi(v)) / 2)|
        # Since phi is linear on each segment [v_k, v_{k+1}], phi(v) lies in union(phi_k, phi_{k+1})
        seg_max_upper = ZERO
        all_segs_lt_1 = True
        first_fail_seg = None
        for k in range(len(phi_balls) - 1):
            seg_phi = phi_balls[k].union(phi_balls[k + 1])
            half_diff = (phi0 - seg_phi) / TWO
            d0_seg = TWO * T_b * abs(half_diff.sin())
            if not strict_lt(d0_seg, ONE):
                all_segs_lt_1 = False
                if first_fail_seg is None:
                    first_fail_seg = {"seg": k, "d0_lower": float(d0_seg.lower()), "d0_upper": float(d0_seg.upper())}
            u = flint.arb(d0_seg.upper())
            if strict_gt(u, seg_max_upper):
                seg_max_upper = u

        # On (1/2, 1]: |d_0(v)| = |gamma| = T
        second_half_lt_1 = strict_lt(T_b, ONE)
        sup_d0_upper = seg_max_upper.max(flint.arb(T_b.upper()))
        sup_d0_lt_1 = all_segs_lt_1 and second_half_lt_1

        return {
            "passed": bool(re_gamma_ge_0 and sup_d0_lt_1),
            "re_gamma_ge_0": re_gamma_ge_0,
            "re_gamma_gt_0": re_gamma_gt_0,
            "re_gamma_lower": float(re_gamma.lower()),
            "re_gamma_upper": float(re_gamma.upper()),
            "first_half_max_d0_upper": float(seg_max_upper.upper()),
            "second_half_d0_T": float(T_b.upper()),
            "sup_d0_upper": float(sup_d0_upper.upper()),
            "all_99_segments_lt_1": all_segs_lt_1,
            "second_half_lt_1": second_half_lt_1,
            "sup_d0_lt_1": sup_d0_lt_1,
            "first_fail_seg": first_fail_seg,
            "num_segments": len(phi_balls) - 1,
        }
    finally:
        flint.ctx.prec = old_prec


def main():
    t0 = time.time()
    path = "inputs/upper99-tight.json"
    raw = open(path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    sha_ok = (sha == EXPECTED_SHA256)

    data = json.loads(raw.decode("utf-8"))
    breaks_f = [Fraction(b) for b in data["breaks"]]
    phases_s = data["phases"]

    # Expected knot set: {j^2/18432 : 0 <= j <= 96} U {1/73728, 1/36864, 1/9216}
    expected_knots = sorted(
        {Fraction(j * j, 18432) for j in range(97)}
        | {Fraction(1, 73728), Fraction(1, 36864), Fraction(1, 9216)}
    )
    knots_exact_match = (breaks_f == expected_knots)
    knots_strictly_increasing = all(breaks_f[i] < breaks_f[i + 1] for i in range(len(breaks_f) - 1))

    # T check
    T_f = Fraction(data["T"])
    C_f = Fraction(data["C"])
    T_exact_match = (T_f == EXPECTED_T) and (C_f == EXPECTED_T)

    # Phase diff vs Vatopoulos's A_D96_4.json (if downloaded into ./vatopoulos_A_D96_4.json)
    vat_path = "vatopoulos_A_D96_4.json"
    vat_comparison = {"available": False}
    if os.path.exists(vat_path):
        vat_raw = open(vat_path, "rb").read()
        vat_sha = hashlib.sha256(vat_raw).hexdigest()
        vat_data = json.loads(vat_raw.decode("utf-8"))
        # Inspect schema of A_D96_4.json dynamically (handles breaks/knots and phases/phi keys)
        vat_keys = list(vat_data.keys())
        vat_phases = vat_data.get("phases") or vat_data.get("phi")
        vat_breaks = vat_data.get("breaks") or vat_data.get("knots")
        phase_diffs = None
        max_phase_diff = None
        exact_phase_str_match = None
        knots_match_vat = None
        if vat_phases is not None and len(vat_phases) == len(phases_s):
            exact_phase_str_match = ([str(p) for p in vat_phases] == [str(p) for p in phases_s])
            diffs = [abs(Fraction(str(a)) - Fraction(str(b))) for a, b in zip(vat_phases, phases_s)]
            max_phase_diff = float(max(diffs))
            phase_diffs = sum(1 for d in diffs if d != 0)
        if vat_breaks is not None and len(vat_breaks) == len(breaks_f):
            knots_match_vat = ([Fraction(str(b)) for b in vat_breaks] == breaks_f)
        vat_comparison = {
            "available": True,
            "sha256": vat_sha,
            "keys": vat_keys,
            "vat_T": vat_data.get("T"),
            "vat_C": vat_data.get("C"),
            "num_phases_vat": len(vat_phases) if vat_phases is not None else None,
            "exact_phase_str_match": exact_phase_str_match,
            "nonzero_phase_diffs": phase_diffs,
            "max_phase_diff": max_phase_diff,
            "knots_match_vat": knots_match_vat,
        }

    # Arb hypotheses check on upper99-tight.json
    hyp_main = check_hypotheses_arb(T_f, phases_s, prec=256)

    # Red control 1: rotate phi(0) so Re(gamma) < 0 (e.g. shift phi(0) by -0.5 rad -> -1.9346 < -pi/2)
    phases_red1 = list(phases_s)
    phases_red1[0] = str(Fraction(phases_s[0]) - Fraction(1, 2))
    hyp_red1 = check_hypotheses_arb(T_f, phases_red1, prec=256)

    # Red control 2: shift last phase so |phi(0) - phi(1/2)| = 2.0 rad => 2*T*sin(1) ~ 1.155 > 1
    phases_red2 = list(phases_s)
    phases_red2[-1] = str(Fraction(phases_s[0]) + Fraction(2, 1))
    hyp_red2 = check_hypotheses_arb(T_f, phases_red2, prec=256)

    # Recompute 0.197467474154 / 0.287702168300 in exact Fraction and 256-bit Arb
    num_f = Fraction("0.197467474154")
    den_f = Fraction("0.287702168300")
    ratio_f = num_f / den_f
    flint.ctx.prec = 256
    ratio_arb = frac_to_arb(num_f) / frac_to_arb(den_f)
    claim_upper = Fraction("0.686360743542159")

    ratio_check = {
        "num": "0.197467474154",
        "den": "0.287702168300",
        "ratio_decimal_20": f"{float(ratio_arb.mid()):.18f}",
        "ratio_arb_str": str(ratio_arb),
        "ratio_lt_claimed_0.686360743542159": bool(ratio_f < claim_upper),
        "ratio_lt_T": bool(ratio_f < T_f),
        "margin_to_T": float(T_f - ratio_f),
        "note": "Exact quotient of reported rounded bounds 0.197467474154/0.287702168300 vs manuscript eq. (16) (full interval endpoints)",
    }

    report = {
        "verdict": "hypotheses checked; F < T not replayed",
        "sha256": sha,
        "sha256_matches_manuscript": sha_ok,
        "num_knots": len(breaks_f),
        "num_segments": len(breaks_f) - 1,
        "knots_exact_match": knots_exact_match,
        "knots_strictly_increasing": knots_strictly_increasing,
        "T_exact_str": str(T_f),
        "T_matches_3431803719_over_5000000000": T_exact_match,
        "vatopoulos_A_D96_4_comparison": vat_comparison,
        "hypotheses_arb_main": hyp_main,
        "red_control_1_rotated_phi0": hyp_red1,
        "red_control_2_shifted_phase": hyp_red2,
        "ratio_recomputation": ratio_check,
        "elapsed_sec": round(time.time() - t0, 4),
    }

    with open("t2_lite_results.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"SHA-256 match: {sha_ok} ({sha})")
    print(f"Knots exact match ({len(breaks_f)} knots, {len(breaks_f)-1} segments): {knots_exact_match}")
    print(f"T exact match ({T_f}): {T_exact_match}")
    print(f"Vatopoulos A_D96_4.json comparison: {vat_comparison}")
    print(f"Arb hypotheses (main): passed={hyp_main['passed']} | Re(gamma) in [{hyp_main['re_gamma_lower']:.8f}, {hyp_main['re_gamma_upper']:.8f}] | first_half_max|d_0| <= {hyp_main['first_half_max_d0_upper']:.8f} | second_half|d_0| = {hyp_main['second_half_d0_T']:.10f}")
    print(f"Red control 1 (rotated phi0): passed={hyp_red1['passed']} | re_gamma_ge_0={hyp_red1['re_gamma_ge_0']} (Re(gamma)={hyp_red1['re_gamma_upper']:.6f})")
    print(f"Red control 2 (shifted phase): passed={hyp_red2['passed']} | sup_d0_lt_1={hyp_red2['sup_d0_lt_1']} (sup|d_0|={hyp_red2['sup_d0_upper']:.6f}, first_fail={hyp_red2['first_fail_seg']})")
    print(f"Ratio 0.197467474154/0.287702168300 = {ratio_check['ratio_decimal_20']} | < 0.686360743542159: {ratio_check['ratio_lt_claimed_0.686360743542159']} | < T: {ratio_check['ratio_lt_T']} (margin {ratio_check['margin_to_T']:.3e})")


if __name__ == "__main__":
    main()
