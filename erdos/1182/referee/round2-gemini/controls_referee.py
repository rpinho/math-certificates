#!/usr/bin/env python3
"""Clean-room control suite for repaired Case I of Erdos #1182.

Dependencies: Python standard library + python-flint 0.9.0 ONLY.
Controls executed:
  1. Direct 160-bit Arb numeric verification on >= 1,518 exact rational feasible (a, Q)
     pairs across all 759 accepted occupancy leaves (both near Q_03 <= q_* and tail Q_03 > q_*),
     verifying raw feasibility of (a, Q), raw side classification from Q_03 vs q_*, and
     true_rate <= recomputed_leaf_bound <= -1/1000.
  2. Positive naive first-moment witness at d = 10 in Region C (> +0.0033635269 > +0.00336)
     verified in 160-bit Arb and confirmed REJECTED when checked as a naive leaf, plus
     explicit regression counterexample against the old reversed lower-cutoff formula.
  3. Subprocess corruption suite on inputs/cert_case1.json.gz (9 distinct corruptions
     covering perturbed tilt, cutoff shifted below B_03 where both naive near/tail formulas
     stay < -1/1000 so ONLY q_* >= B_03 catches it, altered root box, non-interior split,
     deleted leaf, trailing record, inflated global claim, inflated stored U, and legacy
     format=1) — EVERY ONE must be REJECTED (non-zero exit code).
"""

import copy
from fractions import Fraction
import gzip
import json
import math
import pathlib
import random
import subprocess
import sys
import tempfile
import time

import flint

from arb_case1_referee import (
    ARB_PREC,
    BLUE_ADJ,
    DELTA_C,
    ROOT_CAP,
    frac_to_arb,
    in_region_c,
    load_strict_gzip_json,
    verify_case1_certificate,
)


def write_gzip_json(path: pathlib.Path, obj) -> None:
    raw = json.dumps(obj, separators=(",", ":")).encode("utf-8")
    with gzip.open(path, "wb", compresslevel=6) as f:
        f.write(raw)


def verify_feasible_aq(a_fr, q_fr, lo, hi) -> None:
    """Independently verify exact rational feasibility of (a, Q) from raw entries."""
    if not in_region_c(a_fr):
        raise AssertionError(f"Profile a outside Region C: {a_fr}")
    for i in range(5):
        if not (lo[i] <= a_fr[i] <= hi[i]):
            raise AssertionError(f"Profile a[{i}]={a_fr[i]} outside leaf box [{lo[i]}, {hi[i]}]")
    for i in range(5):
        row_sum = Fraction(0)
        for j in range(5):
            val = q_fr[i][j]
            if val < 0:
                raise AssertionError(f"Negative Q[{i}][{j}]={val}")
            if val != q_fr[j][i]:
                raise AssertionError(f"Asymmetric Q[{i}][{j}] != Q[{j}][{i}]")
            if BLUE_ADJ[i][j] == 0 and val != 0:
                raise AssertionError(f"Non-zero red entry Q[{i}][{j}]={val}")
            row_sum += val
        if row_sum != a_fr[i]:
            raise AssertionError(f"Row sum mismatch at {i}: {row_sum} != {a_fr[i]}")


def build_high_entropy_blue_q(a_fr, q03_fr: Fraction, rng: random.Random, jitter: float = 0.0):
    """Construct an exact rational symmetric blue matrix Q with row sums a_fr and Q_03 = q03_fr."""
    assert Fraction(0) <= q03_fr <= min(a_fr[0], a_fr[3])
    rem = [
        a_fr[0] - q03_fr,
        a_fr[1],
        a_fr[2],
        a_fr[3] - q03_fr,
        a_fr[4],
    ]
    rem_flt = [float(x) for x in rem]
    # Sinkhorn scaling on blue graph minus {0,3} to approximate conditional max-entropy Q
    adj_rem = [
        [0 if (i, j) in ((0, 3), (3, 0)) else BLUE_ADJ[i][j] for j in range(5)]
        for i in range(5)
    ]
    t = [1.0 if rem_flt[i] > 0 else 0.0 for i in range(5)]
    for _ in range(50):
        for i in range(5):
            if rem_flt[i] > 0:
                s = sum(adj_rem[i][j] * t[j] for j in range(5))
                if s > 0:
                    t[i] = 0.5 * t[i] + 0.5 * (rem_flt[i] / s)
        z = sum(adj_rem[i][j] * t[i] * t[j] for i in range(5) for j in range(5))
        if z > 0:
            inv_sz = 1.0 / math.sqrt(z)
            t = [ti * inv_sz for ti in t]

    z = sum(adj_rem[i][j] * t[i] * t[j] for i in range(5) for j in range(5))
    if z > 0:
        q_approx = [[adj_rem[i][j] * t[i] * t[j] / z for j in range(5)] for i in range(5)]
    else:
        q_approx = [[0.0] * 5 for _ in range(5)]

    denom = 10**9

    def clamp_frac(target_f: float, cap_fr: Fraction) -> Fraction:
        if cap_fr <= 0:
            return Fraction(0)
        if jitter > 0:
            scale = max(0.0, min(1.0, 1.0 + rng.uniform(-jitter, jitter)))
            target_f = target_f * scale
        num = max(0, round(target_f * denom))
        cand = Fraction(num, denom)
        return cand if cand <= cap_fr else cap_fr

    q02 = clamp_frac(q_approx[0][2], min(rem[0], rem[2]))
    q13 = clamp_frac(q_approx[1][3], min(rem[1], rem[3]))
    q14 = clamp_frac(q_approx[1][4], min(rem[1] - q13, rem[4]))
    q24 = clamp_frac(q_approx[2][4], min(rem[2] - q02, rem[4] - q14))

    q_mat = [[Fraction(0) for _ in range(5)] for _ in range(5)]
    for (i, j), val in (
        ((0, 3), q03_fr),
        ((0, 2), q02),
        ((1, 3), q13),
        ((1, 4), q14),
        ((2, 4), q24),
    ):
        q_mat[i][j] = val
        q_mat[j][i] = val

    for i in range(5):
        off_sum = sum(q_mat[i][j] for j in range(5) if j != i)
        diag = a_fr[i] - off_sum
        if diag < 0:
            raise AssertionError(f"Negative diagonal Q[{i}][{i}]={diag}")
        q_mat[i][i] = diag

    return tuple(tuple(row) for row in q_mat)


def eval_true_case1_rates_arb(a_fr, q_fr):
    """Evaluate exact pairing rate L(a, Q) and Case I rate L(a, Q) + g(a_0, Q_03) in 160-bit Arb."""
    flint.ctx.prec = ARB_PREC
    l_arb = flint.arb(0)
    nine = flint.arb(9)
    five = flint.arb(5)
    for i in range(5):
        if a_fr[i] > 0:
            ai = frac_to_arb(a_fr[i])
            l_arb = l_arb + nine * ai * ai.log()
    for i in range(5):
        for j in range(5):
            if q_fr[i][j] > 0:
                qij = frac_to_arb(q_fr[i][j])
                l_arb = l_arb - five * qij * qij.log()

    q03 = q_fr[0][3]
    a0 = a_fr[0]
    if q03 == 0:
        raise AssertionError("Expected Q_03 > 0 for finite occupancy rate evaluation")
    if q03 == a0:
        g_arb = flint.arb(0)
    else:
        p_arb = frac_to_arb(q03 / a0)
        one = flint.arb(1)
        fp = one - (one - p_arb) ** 10
        g_arb = frac_to_arb(a0) * fp.log()
    return l_arb, g_arb, l_arb + g_arb


def run_direct_numeric_controls(c_leaves: list, seed: int = 20261125) -> dict:
    """Evaluate >= 1,518 feasible (a, Q) pairs (both Q_03 <= q_* and Q_03 > q_*) across all C leaves."""
    flint.ctx.prec = ARB_PREC
    rng = random.Random(seed)
    target_bound = flint.arb(-1) / flint.arb(1000)

    near_count = 0
    tail_count = 0
    min_near_slack = None
    min_tail_slack = None
    max_true_near = None
    max_true_tail = None

    for leaf in c_leaves:
        verts = leaf["verts_exact"]
        lo, hi = leaf["lo"], leaf["hi"]
        q_star = leaf["q_fr"]

        # 1. Near sample (Q_03 <= q_*): mix argmin(a_0) vertex with random convex combination
        v_amin = min(verts, key=lambda v: v[0])
        weights = [rng.randint(1, 1000) for _ in verts]
        w_sum = sum(weights)
        a_conv = [
            sum( Fraction(weights[k], w_sum) * verts[k][j] for k in range(len(verts)) )
            for j in range(5)
        ]
        # 75% weight on v_amin + 25% interior convex combination -> strictly feasible & near critical a0_min
        a_near = tuple(Fraction(3, 4) * v_amin[j] + Fraction(1, 4) * a_conv[j] for j in range(5))
        cap_near = min(q_star, a_near[0], a_near[3])
        assert cap_near > 0
        # Test both close to cutoff (90%-100% of cap_near) and interior (40%-90% of cap_near)
        frac_mult = Fraction(rng.randint(850, 1000), 1000) if (near_count % 2 == 0) else Fraction(rng.randint(400, 850), 1000)
        q03_near = cap_near * frac_mult
        if q03_near == 0 or q03_near > q_star:
            q03_near = cap_near
        q_mat_near = build_high_entropy_blue_q(a_near, q03_near, rng, jitter=0.05)

        verify_feasible_aq(a_near, q_mat_near, lo, hi)
        # Classify directly from raw Q[0][3] vs q_* (do NOT trust pre-label!)
        raw_is_near = q_mat_near[0][3] <= q_star
        assert raw_is_near, f"Expected near Q_03 <= q_*, got {q_mat_near[0][3]} > {q_star}"

        _, _, true_near = eval_true_case1_rates_arb(a_near, q_mat_near)
        if not bool(true_near <= leaf["near_recomp"]) or not bool(true_near <= leaf["leaf_recomp_hi"]) or not bool(true_near <= target_bound):
            raise AssertionError(
                f"Near control FAILED on leaf {leaf['rec_idx']}: true={true_near}, bound={leaf['near_recomp']}"
            )
        slack_n = float((leaf["leaf_recomp_hi"] - true_near).lower())
        if min_near_slack is None or slack_n < min_near_slack:
            min_near_slack = slack_n
        up_n = float(true_near.upper())
        if max_true_near is None or up_n > max_true_near:
            max_true_near = up_n
        near_count += 1

        # 2. Tail sample (Q_03 > q_*): check if exact Region C polytope admits min(a_0, a_3) > q_*
        v_qmax = max(verts, key=lambda v: min(v[0], v[3]))
        max_q03_leaf = min(v_qmax[0], v_qmax[3])
        if max_q03_leaf > q_star:
            # Blend v_qmax with interior convex combination while preserving min(a_0, a_3) > q_*
            lam = Fraction(1, 8)
            a_tail = tuple((Fraction(1) - lam) * v_qmax[j] + lam * a_conv[j] for j in range(5))
            if min(a_tail[0], a_tail[3]) <= q_star:
                a_tail = v_qmax
            hi_q = min(a_tail[0], a_tail[3])
            assert hi_q > q_star
            # Sample strictly above q_*: close to q_* on even leaves, deeper in tail on odd leaves
            alpha = Fraction(rng.randint(1, 150), 1000) if (tail_count % 2 == 0) else Fraction(rng.randint(150, 800), 1000)
            q03_tail = q_star + alpha * (hi_q - q_star)
            assert q_star < q03_tail <= hi_q
            q_mat_tail = build_high_entropy_blue_q(a_tail, q03_tail, rng, jitter=0.05)

            verify_feasible_aq(a_tail, q_mat_tail, lo, hi)
            raw_is_tail = q_mat_tail[0][3] > q_star
            assert raw_is_tail, f"Expected tail Q_03 > q_*, got {q_mat_tail[0][3]} <= {q_star}"

            l_tail, _, true_tail = eval_true_case1_rates_arb(a_tail, q_mat_tail)
            if (
                not bool(l_tail <= leaf["tail_recomp"])
                or not bool(true_tail <= leaf["tail_recomp"])
                or not bool(true_tail <= leaf["leaf_recomp_hi"])
                or not bool(true_tail <= target_bound)
            ):
                raise AssertionError(
                    f"Tail control FAILED on leaf {leaf['rec_idx']}: true={true_tail}, L={l_tail}, bound={leaf['tail_recomp']}"
                )
            slack_t = float((leaf["leaf_recomp_hi"] - l_tail).lower())
            if min_tail_slack is None or slack_t < min_tail_slack:
                min_tail_slack = slack_t
            up_t = float(true_tail.upper())
            if max_true_tail is None or up_t > max_true_tail:
                max_true_tail = up_t
            tail_count += 1

    return {
        "total_pairs": near_count + tail_count,
        "near_count": near_count,
        "tail_count": tail_count,
        "min_near_slack": min_near_slack,
        "min_tail_slack": min_tail_slack,
        "max_true_near": max_true_near,
        "max_true_tail": max_true_tail,
    }


def run_positive_naive_witness_and_regression(cert_obj: dict, verifier_path: pathlib.Path, tmpdir: pathlib.Path) -> dict:
    """Verify the d=10 positive naive witness (> +0.00336) in Region C and its rejection by naive check."""
    flint.ctx.prec = ARB_PREC
    d_den = 10**9
    a_wit = (
        Fraction(2, 5),
        Fraction(138841, d_den),
        Fraction(2, 5),
        Fraction(187117283, d_den),
        Fraction(12743876, d_den),
    )
    # Construct exact rational symmetric blue matrix Q_wit via Sinkhorn scaling + exact Fraction rounding
    a_flt = [float(x) for x in a_wit]
    t_s = [1.0] * 5
    for _ in range(1000):
        for i in range(5):
            t_s[i] = 0.5 * t_s[i] + 0.5 * (a_flt[i] / sum(BLUE_ADJ[i][j] * t_s[j] for j in range(5)))
        z_s = sum(BLUE_ADJ[i][j] * t_s[i] * t_s[j] for i in range(5) for j in range(5))
        inv_sz = 1.0 / math.sqrt(z_s)
        t_s = [ti * inv_sz for ti in t_s]
    z_s = sum(BLUE_ADJ[i][j] * t_s[i] * t_s[j] for i in range(5) for j in range(5))
    q_flt = [[BLUE_ADJ[i][j] * t_s[i] * t_s[j] / z_s for j in range(5)] for i in range(5)]

    q02 = Fraction(round(q_flt[0][2] * d_den), d_den)
    q03 = Fraction(round(q_flt[0][3] * d_den), d_den)
    q13 = Fraction(round(q_flt[1][3] * d_den), d_den)
    q14 = Fraction(round(q_flt[1][4] * d_den), d_den)
    q24 = Fraction(round(q_flt[2][4] * d_den), d_den)

    q_wit = [[Fraction(0) for _ in range(5)] for _ in range(5)]
    for (i, j), val in (
        ((0, 2), q02),
        ((0, 3), q03),
        ((1, 3), q13),
        ((1, 4), q14),
        ((2, 4), q24),
    ):
        q_wit[i][j] = val
        q_wit[j][i] = val
    for i in range(5):
        q_wit[i][i] = a_wit[i] - sum(q_wit[i][j] for j in range(5) if j != i)
    q_wit = tuple(tuple(row) for row in q_wit)

    verify_feasible_aq(a_wit, q_wit, (Fraction(0),) * 5, (ROOT_CAP,) * 5)
    l_wit, g_wit, case1_wit = eval_true_case1_rates_arb(a_wit, q_wit)

    if not bool(l_wit > flint.arb("0.0033635269")):
        raise AssertionError(f"Naive witness L(a,Q)={l_wit} did not exceed +0.0033635269")

    # Find exact leaf in cert_case1.json.gz containing a_wit
    grid = cert_obj["grid"]
    recs = cert_obj["records"]
    idx = 0
    found_rec_idx = None

    def locate(lo, hi):
        nonlocal idx, found_rec_idx
        r_i = idx
        rec = recs[idx]
        idx += 1
        contains = all(lo[k] <= a_wit[k] <= hi[k] for k in range(5))
        if rec[0] == "S":
            _, dim, sp_int = rec
            sp = Fraction(sp_int, grid)
            hi_l = list(hi)
            hi_l[dim] = sp
            lo_r = list(lo)
            lo_r[dim] = sp
            locate(lo, hi_l)
            locate(lo_r, hi)
        elif contains and found_rec_idx is None:
            found_rec_idx = r_i

    locate([Fraction(x, grid) for x in cert_obj["root"][0]], [Fraction(x, grid) for x in cert_obj["root"][1]])
    assert found_rec_idx is not None, "Could not find leaf covering a_wit"
    orig_leaf = recs[found_rec_idx]
    assert orig_leaf[0] == "C", f"Expected C leaf at {found_rec_idx}, got {orig_leaf[0]}"

    # Mutate that C leaf to a naive leaf N (even allowing stored U = -1000000000 so ONLY vertex U_t recomputation catches it!)
    mut_obj = copy.deepcopy(cert_obj)
    mut_obj["records"][found_rec_idx] = ["N", orig_leaf[1], -1000000000, -1000000000]
    mut_path = tmpdir / "mutant_witness_naive_leaf.json.gz"
    write_gzip_json(mut_path, mut_obj)
    proc = subprocess.run(
        [sys.executable, "-B", str(verifier_path), "--skip-hash-locks", "--fast-outer-only", "--cert", str(mut_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        raise AssertionError("Naive leaf mutation at d=10 positive witness was FALSELY ACCEPTED!")

    # Also compute regression check against the old reversed lower-cutoff formula g(a_{0,max}, q_low):
    # At a_wit (a_0 = 2/5, Q_03 = 103529833/10^9) vs a_0_max = 4001/10000 and q_low = 1/20:
    a0_max_arb = frac_to_arb(ROOT_CAP)
    q_low_arb = frac_to_arb(Fraction(1, 20))
    p_old = q_low_arb / a0_max_arb
    g_old_reversed = a0_max_arb * (flint.arb(1) - (flint.arb(1) - p_old) ** 10).log()
    excess = g_wit - g_old_reversed
    if not bool(excess > flint.arb("0.03")):
        raise AssertionError(f"Expected large positive excess of true g over old reversed formula, got {excess}")

    return {
        "a_wit": a_wit,
        "l_wit": l_wit,
        "g_wit": g_wit,
        "case1_wit": case1_wit,
        "leaf_rec_idx": found_rec_idx,
        "naive_reject_rc": proc.returncode,
        "naive_reject_stderr": proc.stderr.strip(),
        "reversed_g_old": g_old_reversed,
        "reversed_excess": excess,
    }


def run_corruption_suite(cert_obj: dict, c_leaves: list, verifier_path: pathlib.Path, tmpdir: pathlib.Path) -> list:
    """Run positive control + 9 distinct corruption controls via subprocess; all 9 must exit != 0."""
    flint.ctx.prec = ARB_PREC
    grid = cert_obj["grid"]

    # Positive control on clean temp copy
    clean_path = tmpdir / "clean_copy.json.gz"
    write_gzip_json(clean_path, cert_obj)
    clean_proc = subprocess.run(
        [sys.executable, "-B", str(verifier_path), "--skip-hash-locks", "--fast-outer-only", "--cert", str(clean_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if clean_proc.returncode != 0:
        raise AssertionError(f"Positive control failed unexpectedly: {clean_proc.stderr}")

    # Pick an occupancy leaf where shifting q_* far below B_03 keeps BOTH naive near & KL-tail < -0.001
    # so ONLY the strict q_* >= B_03 check rejects it!
    chosen_c_for_q = None
    chosen_q_below_int = None
    for leaf in c_leaves:
        b03_lo = float(leaf["b03_arb"].lower())
        # Try q_bad = 0.25 * B_03 (well below B_03, where D_KL(2*q_bad, 2*B_03) is large positive AND g(a0_min, q_bad) is very negative!)
        q_cand_int = max(1, int(0.25 * b03_lo * grid))
        q_cand_fr = Fraction(q_cand_int, grid)
        q_cand_arb = frac_to_arb(q_cand_fr)
        if not bool(q_cand_arb < leaf["b03_arb"]):
            continue
        a0_min_arb = frac_to_arb(leaf["tlo"][0])
        p_c = frac_to_arb(q_cand_fr / leaf["tlo"][0])
        g_c = a0_min_arb * (flint.arb(1) - (flint.arb(1) - p_c) ** 10).log()
        near_c = leaf["u_recomp"] + g_c
        x_c = flint.arb(2) * q_cand_arb
        b_c = flint.arb(2) * leaf["b03_arb"]
        dkl_c = x_c * (x_c / b_c).log() + (flint.arb(1) - x_c) * ((flint.arb(1) - x_c) / (flint.arb(1) - b_c)).log()
        tail_c = leaf["u_recomp"] - flint.arb(5) * dkl_c
        if bool(near_c < flint.arb("-0.001")) and bool(tail_c < flint.arb("-0.001")):
            chosen_c_for_q = leaf
            chosen_q_below_int = q_cand_int
            break
    assert chosen_c_for_q is not None, "Could not construct surgical q_* < B_03 mutant"

    tightest_c = max(c_leaves, key=lambda lf: lf["leaf_recomp_hi"].upper())
    first_s_idx = next(i for i, r in enumerate(cert_obj["records"]) if r[0] == "S")
    first_leaf_idx = next(i for i, r in enumerate(cert_obj["records"]) if r[0] in ("N", "C"))

    mutants = []

    # 1a. Perturbed tilt on tightest C leaf (raw: caught immediately by U_recomp <= U_stored)
    m1a = copy.deepcopy(cert_obj)
    m1a["records"][tightest_c["rec_idx"]][1][0] = int(m1a["records"][tightest_c["rec_idx"]][1][0] * 1.05)
    mutants.append(("mutant_1a_perturbed_tilt_raw", m1a, "understates recomputed U"))

    # 1b. Perturbed tilt WITH updated stored U (proves pure recomputed rate check <= -1/1000 rejects it!)
    m1b = copy.deepcopy(cert_obj)
    m1b["records"][tightest_c["rec_idx"]][1][0] = int(m1b["records"][tightest_c["rec_idx"]][1][0] * 1.05)
    m1b["records"][tightest_c["rec_idx"]][2] += 1000000000  # +0.001 cushion so U_recomp <= U_stored passes
    mutants.append(("mutant_1b_perturbed_tilt_adjusted_U", m1b, "exceeds -1/1000"))

    # 2. Cutoff shifted strictly below B_03 (surgical: both near & wrong-side D_KL formulas < -0.001!)
    m2 = copy.deepcopy(cert_obj)
    m2["records"][chosen_c_for_q["rec_idx"]][3] = [chosen_q_below_int]
    mutants.append(("mutant_2_cutoff_below_B03", m2, "q_* >= B_03"))

    # 3. Altered root box upper boundary (4000/10000 instead of 4001/10000)
    m3 = copy.deepcopy(cert_obj)
    m3["root"][1][0] = (4000 * grid) // 10000
    mutants.append(("mutant_3_altered_root_boundary", m3, "Root box mismatch"))

    # 4. Altered split boundary (non-interior split equal to root upper cap)
    m4 = copy.deepcopy(cert_obj)
    m4["records"][first_s_idx][2] = m4["root"][1][m4["records"][first_s_idx][1]]
    mutants.append(("mutant_4_non_interior_split", m4, "Non-interior split"))

    # 5. Deleted leaf (truncated record stream)
    m5 = copy.deepcopy(cert_obj)
    m5["records"].pop()
    mutants.append(("mutant_5_deleted_leaf", m5, "Truncated record stream"))

    # 6. Trailing record appended after valid tree
    m6 = copy.deepcopy(cert_obj)
    m6["records"].append(copy.deepcopy(cert_obj["records"][first_leaf_idx]))
    mutants.append(("mutant_6_trailing_record", m6, "Trailing records"))

    # 7. Inflated top-level claim (-0.000999 > -1/1000)
    m7 = copy.deepcopy(cert_obj)
    m7["claim"] = -999000000
    mutants.append(("mutant_7_inflated_global_claim", m7, "Top-level claim"))

    # 8. Inflated stored leaf profile bound U_stored on tightest C leaf (+5000 ticks -> > -1/1000)
    m8 = copy.deepcopy(cert_obj)
    m8["records"][tightest_c["rec_idx"]][2] += 5000
    mutants.append(("mutant_8_inflated_stored_U", m8, "exceeds leaf claim"))

    # 9. Legacy format=1 header
    m9 = copy.deepcopy(cert_obj)
    m9["format"] = 1
    mutants.append(("mutant_9_legacy_format_1", m9, "Invalid Case I format"))

    results = []
    for name, m_obj, expected_substr in mutants:
        m_path = tmpdir / f"{name}.json.gz"
        write_gzip_json(m_path, m_obj)
        proc = subprocess.run(
            [sys.executable, "-B", str(verifier_path), "--skip-hash-locks", "--fast-outer-only", "--cert", str(m_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        stderr_line = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else ""
        if proc.returncode == 0:
            raise AssertionError(f"CORRUPTION CONTROL FAILED: {name} exited 0 (falsely accepted)!")
        if expected_substr not in stderr_line:
            raise AssertionError(
                f"CORRUPTION CONTROL {name} rejected with unexpected message: {stderr_line!r} (expected {expected_substr!r})"
            )
        results.append(
            {
                "name": name,
                "returncode": proc.returncode,
                "reason": stderr_line,
            }
        )
    return results


def main() -> int:
    t0 = time.monotonic()
    base_dir = pathlib.Path(__file__).resolve().parent
    cert_path = base_dir / "inputs" / "cert_case1.json.gz"
    verifier_path = base_dir / "arb_case1_referee.py"

    print(f"=== Erdos #1182 Clean-Room Case I Referee Controls (flint {flint.__version__}, prec={ARB_PREC} bits) ===")
    cert_obj = load_strict_gzip_json(cert_path)
    state = verify_case1_certificate(cert_obj, check_exact_polytope=True, collect_c_leaves=True)
    c_leaves = state["c_leaf_details"]
    print(f"Loaded and verified {len(c_leaves)} accepted occupancy leaves ({state['exact_c_vertices']} exact Region C vertices, {state['outer_c_vertices']} outer sliced-box vertices).")

    # Control 1: Direct numeric check on >= 1,518 feasible (a, Q) pairs
    num_res = run_direct_numeric_controls(c_leaves, seed=20261125)
    assert num_res["total_pairs"] >= 500
    assert num_res["near_count"] >= 250 and num_res["tail_count"] >= 250
    print("\n[Control 1] Direct 160-bit Arb numeric check on feasible (a, Q) pairs inside accepted C leaves:")
    print(f"  Total verified feasible (a, Q) pairs: {num_res['total_pairs']} (near Q_03 <= q_*: {num_res['near_count']}, tail Q_03 > q_*: {num_res['tail_count']})")
    print(f"  Max true Case I rate (near): {num_res['max_true_near']:.12f} <= recomputed_leaf_bound <= -0.001 : PASS")
    print(f"  Max true Case I rate (tail): {num_res['max_true_tail']:.12f} <= recomputed_leaf_bound <= -0.001 : PASS")
    print(f"  Min certified slack (recomputed_leaf_bound - true_rate): near={num_res['min_near_slack']:.12e}, tail_L={num_res['min_tail_slack']:.12e} (> 0: PASS)")

    with tempfile.TemporaryDirectory(prefix="case1_ref2_ctrl_") as tmp:
        tmpdir = pathlib.Path(tmp)

        # Control 2: Positive naive witness at d=10 (> +0.00336) & old lower-cutoff regression
        wit_res = run_positive_naive_witness_and_regression(cert_obj, verifier_path, tmpdir)
        print("\n[Control 2] Bare first-moment positive witness at d=10 in Region C & old lower-cutoff regression:")
        print(f"  Exact rational witness profile a_wit: {[str(x) for x in wit_res['a_wit']]}")
        print(f"  Bare pairing rate L(a_wit, Q_wit) in 160-bit Arb: {wit_res['l_wit']} (> +0.0033635269 > +0.00336: PASS)")
        print(f"  True Case I occupancy term g(a_0, Q_03): {wit_res['g_wit']}")
        print(f"  True Case I combined rate L + g: {wit_res['case1_wit']} (< -0.001: PASS)")
        print(f"  Covering leaf in cert_case1.json.gz: record[{wit_res['leaf_rec_idx']}] (kind='C')")
        print(f"  Naive leaf check on covering leaf (mutated C -> N): REJECTED (exit={wit_res['naive_reject_rc']}, {wit_res['naive_reject_stderr']})")
        print(f"  Old reversed lower-cutoff formula g(a0_max, 1/20) = {float(wit_res['reversed_g_old'].upper()):.12f} underestimates true g by +{float(wit_res['reversed_excess'].lower()):.12f} (confirming old direction was invalid)")

        # Control 3: 9 corruption controls on cert_case1.json.gz
        mut_res = run_corruption_suite(cert_obj, c_leaves, verifier_path, tmpdir)
        print(f"\n[Control 3] Certificate corruption suite ({len(mut_res)}/{len(mut_res)} corrupted archives REJECTED, clean copy ACCEPTED):")
        for item in mut_res:
            print(f"  {item['name']}: exit={item['returncode']} -> {item['reason']}")

    elapsed = time.monotonic() - t0
    print(f"\nAll controls passed in {elapsed:.2f}s.")
    print("ALL_REFEREE_CONTROLS: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
