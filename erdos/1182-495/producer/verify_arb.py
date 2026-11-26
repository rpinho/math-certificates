"""Standalone 180-bit Arb verifier and controls for the (9, 10)-bidegree Erdos #1182 proof (c = 99/20)."""

import argparse
from fractions import Fraction
import gzip
from itertools import product
import json
from pathlib import Path
import sys

from flint import arb, ctx

# Use 180-bit Arb ball precision (> 160 bits required). Zero IEEE binary64 conversions anywhere.
ctx.prec = 180

GRID = 10_000 * 2**20
MAX_PART = 4_001 * 2**20
MIN_GAP = 1_500 * 2**20  # exact 3/20
SCALE = 10**12
LIMIT = -1_500_000_000   # exact -3/2000 = -0.0015
N0 = 450_000
C_NUM = 99
C_DEN = 20

LABELS = ("naive_ab", "case1", "case2")
ROOT_BOUNDS = [[0, MAX_PART] for _ in range(5)]
BLUE = tuple((i, j) for i in range(5) for j in range(5) if (j - i) % 5 in (0, 2, 3))
OFF_DIAG_BLUE = ((0, 2), (0, 3), (1, 3), (1, 4), (2, 4))

# Exact rational endpoints of alpha_9(n) = 2*ceil(n/20)/n for all integers n >= N0:
ALPHA9_LO = Fraction(1, 10)
ALPHA9_HI = Fraction(1, 10) + Fraction(19, 10 * N0)
THETA_LO = 1 - ALPHA9_HI
THETA_HI = 1 - ALPHA9_LO
DBAR_LO = 10 - ALPHA9_HI
DBAR_HI = 10 - ALPHA9_LO  # exact 99/10


def require(condition, message):
    if not condition:
        raise ValueError(message)


def arb_rat(q: Fraction) -> arb:
    require(isinstance(q, Fraction), "expected exact Fraction")
    return arb(q.numerator) / arb(q.denominator)


ALPHA9_IV = arb_rat(ALPHA9_LO).union(arb_rat(ALPHA9_HI))
THETA_IV = arb(1) - ALPHA9_IV
DBAR_IV = arb(10) - ALPHA9_IV
ALPHA9_HI_ARB = arb_rat(ALPHA9_HI)
DBAR_LO_ARB = arb_rat(DBAR_LO)
DBAR_HI_ARB = arb_rat(DBAR_HI)
SPLIT_ENT_IV = ALPHA9_IV * ALPHA9_IV.log() + THETA_IV * THETA_IV.log()


def entropy_term(x: arb) -> arb:
    if x.is_zero():
        return arb(0)
    return x * x.log()


def clip_region(bounds, region):
    intervals = [[int(a), int(b)] for a, b in bounds]
    if region == "A":
        inequalities = ((0, 1, 0), (1, 2, 0), (1, 3, 0), (1, 4, 0))
    else:
        inequalities = tuple((i, j, 0) for i in (0, 2) for j in (1, 3, 4)) + ((3, 4, 0),)
        if region == "C":
            inequalities += ((0, 3, MIN_GAP), (2, 3, MIN_GAP))
    for _ in range(3):
        for i, j, diff in inequalities:
            intervals[i][0] = max(intervals[i][0], intervals[j][0] + diff)
            intervals[j][1] = min(intervals[j][1], intervals[i][1] - diff)
        for i, iv in enumerate(intervals):
            others = [intervals[j] for j in range(5) if j != i]
            iv[0] = max(iv[0], GRID - sum(o[1] for o in others))
            iv[1] = min(iv[1], GRID - sum(o[0] for o in others))
        if any(lo > hi for lo, hi in intervals):
            return None
        if sum(lo for lo, _ in intervals) > GRID or sum(hi for _, hi in intervals) < GRID:
            return None
    if region == "B" and min(intervals[0][0], intervals[2][0]) - intervals[3][1] > MIN_GAP:
        return None
    return intervals


def hull_bounds(bounds, case_label):
    if case_label != "naive_ab":
        return clip_region(bounds, "C")
    parts = [reg for letter in ("A", "B") if (reg := clip_region(bounds, letter)) is not None]
    if parts:
        return [[min(p[i][0] for p in parts), max(p[i][1] for p in parts)] for i in range(5)]
    return None


def sliced_box_vertices(bounds):
    points = set()
    for free in range(5):
        endpoints = [pair if i != free else (0,) for i, pair in enumerate(bounds)]
        for pt in product(*endpoints):
            rest = GRID - sum(pt)
            if bounds[free][0] <= rest <= bounds[free][1]:
                points.add(pt[:free] + (rest,) + pt[free + 1:])
    return sorted(points)


def exact_region_c_vertices(bounds):
    """Exact 4D Chernikova halfspace-clipping extreme-point enumeration of Region C polytope."""
    # Start from the 16 vertices of the 4D box [lo_0, hi_0] x ... x [lo_3, hi_3] on sum(x) = GRID.
    # Track bitmask of active facet equalities; in 4D every 1-face (edge) satisfies >= 3 common equalities!
    poly = []
    for idx0, x0 in enumerate(bounds[0]):
        for idx1, x1 in enumerate(bounds[1]):
            for idx2, x2 in enumerate(bounds[2]):
                for idx3, x3 in enumerate(bounds[3]):
                    mask = (1 << (2 * 0 + idx0)) | (1 << (2 * 1 + idx1)) | (1 << (2 * 2 + idx2)) | (1 << (2 * 3 + idx3))
                    if bounds[0][0] == bounds[0][1]:
                        mask |= 0b11
                    if bounds[1][0] == bounds[1][1]:
                        mask |= (0b11 << 2)
                    if bounds[2][0] == bounds[2][1]:
                        mask |= (0b11 << 4)
                    if bounds[3][0] == bounds[3][1]:
                        mask |= (0b11 << 6)
                    p = (Fraction(x0), Fraction(x1), Fraction(x2), Fraction(x3), Fraction(GRID - x0 - x1 - x2 - x3))
                    poly.append((p, mask))
    # Deduplicate initial points while merging masks:
    merged = {}
    for p, m in poly:
        merged[p] = merged.get(p, 0) | m
    poly = list(merged.items())

    halfspaces = [
        (8, lambda p: p[4] - bounds[4][0]),
        (9, lambda p: bounds[4][1] - p[4]),
        (10, lambda p: p[0] - p[1]),
        (11, lambda p: p[0] - p[3] - MIN_GAP),
        (12, lambda p: p[0] - p[4]),
        (13, lambda p: p[2] - p[1]),
        (14, lambda p: p[2] - p[3] - MIN_GAP),
        (15, lambda p: p[2] - p[4]),
        (16, lambda p: p[3] - p[4]),
    ]
    for bit_id, fn in halfspaces:
        bit = 1 << bit_id
        pos, neg, next_map = [], [], {}
        for p, m in poly:
            v = fn(p)
            if v > 0:
                pos.append((p, m, v))
                next_map[p] = next_map.get(p, 0) | m
            elif v == 0:
                next_map[p] = next_map.get(p, 0) | m | bit
            else:
                neg.append((p, m, v))
        for p, mp, vp in pos:
            for q, mq, vq in neg:
                common = mp & mq
                if common.bit_count() >= 3:
                    lam = vp / (vp - vq)
                    inter = tuple(p[k] + lam * (q[k] - p[k]) for k in range(5))
                    next_map[inter] = next_map.get(inter, 0) | common | bit
        poly = list(next_map.items())
        if not poly:
            return []
    return [p for p, _ in poly]


def rho_arb(lo_i_int: int) -> arb:
    require(type(lo_i_int) is int and lo_i_int > 0, "rho requires positive integer lower bound")
    a_lo_fr = Fraction(lo_i_int, GRID)
    if a_lo_fr <= ALPHA9_HI:
        return arb(1) / arb(9)
    a_lo = arb(lo_i_int) / GRID
    return a_lo / (10 * a_lo - ALPHA9_HI_ARB)


def q_cap_fraction(hi_i_int: int, hi_j_int: int) -> Fraction:
    s_i = min(Fraction(10 * hi_i_int, GRID), Fraction(9 * hi_i_int, GRID) + THETA_HI)
    s_j = min(Fraction(10 * hi_j_int, GRID), Fraction(9 * hi_j_int, GRID) + THETA_HI)
    return min(s_i, s_j) / DBAR_LO


def eval_dual_on_points(points, encoded_tilt, encoded_eta, s03=None, s02=None, lin0=None, lin2=None):
    require(isinstance(encoded_tilt, list) and len(encoded_tilt) == 5
            and all(type(v) is int and v > 0 for v in encoded_tilt), "invalid tilt vector")
    require(type(encoded_eta) is int, "noninteger eta")
    require(bool(points), "empty vertex set on non-empty leaf")

    tilt = [arb(v) / SCALE for v in encoded_tilt]
    eta = arb(encoded_eta) / SCALE
    exp_eta_m1 = (eta - 1).exp()

    partition = arb(0)
    for i, j in BLUE:
        term = tilt[i] * tilt[j]
        if s03 is not None and ((i == 0 and j == 3) or (i == 3 and j == 0)):
            term = term * s03
        elif s02 is not None and ((i == 0 and j == 2) or (i == 2 and j == 0)):
            term = term * s02
        partition += term
    require(partition > 0, "nonpositive partition function")

    const_base = SPLIT_ENT_IV + (DBAR_IV / 2) * partition.log() - eta * ALPHA9_IV
    c_ti = [-10 * (DBAR_IV * ti).log() for ti in tilt]
    cache = {}

    def coord_term(i, v_coord):
        if v_coord == 0:
            return arb(0)
        key = (i, v_coord)
        if key not in cache:
            a_i = (arb_rat(v_coord) / GRID) if isinstance(v_coord, Fraction) else (arb(v_coord) / GRID)
            require(a_i > 0, "nonpositive coordinate in vertex")
            kappa = (DBAR_IV * tilt[i] * exp_eta_m1) / a_i
            rad = ((8 + kappa) ** 2 + 36).sqrt()
            y = arb(18) / ((8 + kappa) + rad)
            xi = (2 * kappa) / ((10 + kappa) + rad)
            val = a_i * (9 * a_i.log() + c_ti[i] + 10 * (9 + y).log() - y.log() + xi)
            if i == 0 and lin0 is not None:
                val += a_i * lin0
            elif i == 2 and lin2 is not None:
                val += a_i * lin2
            cache[key] = val
        return cache[key]

    max_val = arb(-1000)
    for pt in points:
        rate = const_base
        for i in range(5):
            rate += coord_term(i, pt[i])
        max_val = max_val.max(rate.upper())
    return max_val, tilt, partition


def prove_upper_tail(two_h: arb, two_b: arb, upper_rate: arb, claim_limit: arb) -> arb:
    require(two_h > two_b and two_h <= 1, "upper tail cutoff on wrong side of reference mass or > 1")
    comp = 1 - two_h
    div = entropy_term(two_h) + entropy_term(comp) - two_h * two_b.log() - comp * (1 - two_b).log()
    require(div > 0, "nonpositive binary KL divergence")
    tail_rate = upper_rate - (DBAR_LO_ARB / 2) * div
    require(tail_rate <= claim_limit, "edge-divergence tail exceeds claim")
    return tail_rate


def verify_c1_leaf(clipped, encoded_tilt, encoded_eta, u_list, claim_limit: arb, also_exact_poly=False) -> arb:
    require(isinstance(u_list, list) and len(u_list) == 3
            and all(type(x) is int and 0 < x < SCALE for x in u_list), "invalid C1 tangent parameters")
    require(clipped[0][0] > 0 and clipped[2][0] > 0, "zero lower bound on V0 or V2 in C1 leaf")

    r0 = rho_arb(clipped[0][0])
    r2 = rho_arb(clipped[2][0])
    bgs = []
    for ui in u_list:
        u = arb(ui) / SCALE
        f = 1 - (1 - u) ** 10
        beta = 10 * ((1 - u) ** 9) / f
        gamma = f.log() - beta * u
        require(beta > 0 and gamma < 0, "invalid C1 occupancy tangent sign")
        bgs.append((beta, gamma))
    (b1, g1), (b2, g2), (b3, g3) = bgs
    s03 = (r0 * b1).exp()
    s02 = (r0 * b2 + r2 * b3).exp()
    require(s03 > 1 and s02 > 1, "C1 edge tilts must exceed 1")

    pts = sliced_box_vertices(clipped)
    max_ub, _, _ = eval_dual_on_points(pts, encoded_tilt, encoded_eta, s03=s03, s02=s02, lin0=g1 + g2, lin2=g3)
    require(max_ub <= claim_limit, "C1 leaf vertex exceeds claim")

    if also_exact_poly:
        exact_pts = exact_region_c_vertices(clipped)
        require(bool(exact_pts), "empty exact Region C polytope on C1 leaf")
        exact_ub, _, _ = eval_dual_on_points(exact_pts, encoded_tilt, encoded_eta, s03=s03, s02=s02, lin0=g1 + g2, lin2=g3)
        require(exact_ub <= claim_limit, "C1 exact Region C polytope exceeds claim")
    return max_ub


def arb_kl_cell_lb(lo_num: int, hi_num: int, denom: int, two_b: arb) -> arb:
    """Rigorous lower bound on D(2*Q, 2*B) for Q in [lo_num/denom, hi_num/denom]."""
    two_lo = arb(2 * lo_num) / arb(denom)
    two_hi = arb(2 * hi_num) / arb(denom)
    if two_lo > two_b and two_lo <= 1:
        comp = 1 - two_lo
        val = entropy_term(two_lo) + entropy_term(comp) - two_lo * two_b.log() - comp * (1 - two_b).log()
        return val if val > 0 else arb(0)
    if two_hi < two_b and two_hi >= 0:
        comp = 1 - two_hi
        val = entropy_term(two_hi) + entropy_term(comp) - two_hi * two_b.log() - comp * (1 - two_b).log()
        return val if val > 0 else arb(0)
    return arb(0)


def verify_c2_leaf(clipped, encoded_tilt, encoded_eta, encoded_upper, payload, claim_limit: arb) -> arb:
    require(type(encoded_upper) is int, "noninteger C2 profile upper bound")
    require(isinstance(payload, list) and len(payload) == 3
            and all(type(x) is int for x in payload), "invalid C2 payload")
    h02_int, h24_int, u_int = payload
    require(0 < h02_int <= GRID and 0 < h24_int <= GRID and 0 < u_int < SCALE,
            "C2 parameters out of range")
    require(clipped[0][0] > 0 and clipped[2][0] > 0, "zero lower bound on V0 or V2 in C2 leaf")

    pts = sliced_box_vertices(clipped)
    recomp_ub, tilt, part = eval_dual_on_points(pts, encoded_tilt, encoded_eta)
    upper_rate = arb(encoded_upper) / SCALE
    require(recomp_ub <= upper_rate, "C2 stored profile bound understates recomputed vertex bound")

    s2_min_fr = max(Fraction(9 * clipped[2][0], GRID), Fraction(10 * clipped[2][0], GRID) - ALPHA9_HI)
    require(s2_min_fr > 0, "nonpositive Row-2 stub lower bound")
    s2_min_a = arb_rat(s2_min_fr)

    worst = arb(-1000)
    for i, j, h_int in ((0, 2, h02_int), (2, 4, h24_int)):
        if Fraction(h_int, GRID) < q_cap_fraction(clipped[i][1], clipped[j][1]):
            t_rate = prove_upper_tail(2 * arb(h_int) / GRID, 2 * tilt[i] * tilt[j] / part, upper_rate, claim_limit)
            worst = worst.max(t_rate.upper())

    u = arb(u_int) / SCALE
    f = 1 - (1 - u) ** 10
    beta = 10 * ((1 - u) ** 9) / f
    gamma = f.log() - beta * u
    require(beta > 0 and gamma < 0, "invalid C2 tangent sign")

    r0 = rho_arb(clipped[0][0])
    w_a = (beta * r0).exp()
    require(w_a > 1, "C2 moment weight w must exceed 1")
    a0_lo = arb(clipped[0][0]) / GRID
    a2_iv = (arb(clipped[2][0]) / GRID).union(arb(clipped[2][1]) / GRID)
    two_b02 = 2 * tilt[0] * tilt[2] / part
    two_b24 = 2 * tilt[2] * tilt[4] / part

    kl02_a = [arb_kl_cell_lb(i * h02_int, (i + 1) * h02_int, 8 * GRID, two_b02) for i in range(8)]
    kl24_a = [arb_kl_cell_lb(j * h24_int, (j + 1) * h24_int, 8 * GRID, two_b24) for j in range(8)]
    q0_hi_a = [
        arb(1) if DBAR_HI * Fraction((i + 1) * h02_int, 8 * GRID) >= s2_min_fr
        else (DBAR_HI_ARB * arb((i + 1) * h02_int) / arb(8 * GRID)) / s2_min_a
        for i in range(8)
    ]
    q4_hi_a = [
        arb(1) if DBAR_HI * Fraction((j + 1) * h24_int, 8 * GRID) >= s2_min_fr
        else (DBAR_HI_ARB * arb((j + 1) * h24_int) / arb(8 * GRID)) / s2_min_a
        for j in range(8)
    ]

    for i in range(8):
        q0_c = q0_hi_a[i]
        for j in range(8):
            q4_c = q4_hi_a[j]
            m_val = ((1 + (w_a - 1) * q0_c) ** 10
                     - (1 - q4_c + (w_a - 1) * q0_c) ** 10
                     + (1 - q4_c) ** 10
                     - (1 - q0_c) ** 10)
            require(m_val > 0, "nonpositive M10 polynomial on C2 cell")
            base_02 = upper_rate - (DBAR_LO_ARB / 2) * kl02_a[i]
            base_24 = upper_rate - (DBAR_LO_ARB / 2) * kl24_a[j]
            base_cell = base_02 if base_02.upper() <= base_24.upper() else base_24
            cell_rate = base_cell + a0_lo * gamma + a2_iv * m_val.log()
            require(cell_rate <= claim_limit, "C2 cell occupancy bound exceeds claim")
            worst = worst.max(cell_rate.upper())
    return worst


def verify_doc(cert: dict, check_exact_poly=False, quiet=False):
    require(isinstance(cert, dict), "certificate must be JSON object")
    case = cert.get("case")
    require(case in LABELS, "unexpected certificate case label")
    require(
        cert.get("format") == 3
        and cert.get("model") == "bidegree_9_10"
        and cert.get("c_num") == C_NUM
        and cert.get("c_den") == C_DEN
        and cert.get("n0") == N0
        and cert.get("root") == [[0] * 5, [MAX_PART] * 5]
        and cert.get("grid") == GRID
        and cert.get("tilt_scale") == SCALE
        and cert.get("claim") == LIMIT,
        "certificate header metadata mismatch",
    )

    records = iter(cert["records"])
    counts = {"split": 0, "empty": 0, "naive": 0, "occupancy": 0}
    max_bound = arb(-1000)
    claim_limit = arb(LIMIT) / SCALE

    def walk(bounds):
        nonlocal max_bound
        rec = next(records, None)
        require(isinstance(rec, list) and bool(rec), "truncated or malformed tree node")
        op, *vals = rec
        clipped = hull_bounds(bounds, case)
        if op == "X":
            require(not vals and clipped is None, "unjustified empty leaf X")
            counts["empty"] += 1
            return
        require(clipped is not None, "empty box must be marked X")
        if op == "S":
            require(len(vals) == 2 and all(type(x) is int for x in vals), "malformed split node")
            axis, cut = vals
            widths = [b - a for a, b in clipped]
            require(0 <= axis < 5 and axis == widths.index(max(widths)) and cut == (clipped[axis][0] + clipped[axis][1]) // 2,
                    "split coordinate or midpoint mismatch")
            lo_ax, hi_ax = bounds[axis]
            require(lo_ax < cut < hi_ax, "non-interior split")
            left = [pair[:] for pair in bounds]
            right = [pair[:] for pair in bounds]
            left[axis] = [lo_ax, cut]
            right[axis] = [cut, hi_ax]
            counts["split"] += 1
            walk(left)
            walk(right)
            return

        if op == "N":
            require(len(vals) == 4, "malformed naive leaf N")
            t_enc, eta_enc, upper_enc, leaf_claim = vals
            require(type(upper_enc) is int and type(leaf_claim) is int and leaf_claim == LIMIT, "invalid N leaf claim")
            require(upper_enc <= LIMIT, "N leaf stored upper exceeds claim")
            pts = sliced_box_vertices(clipped)
            recomp_ub, _, _ = eval_dual_on_points(pts, t_enc, eta_enc)
            require(recomp_ub <= arb(upper_enc) / SCALE, "N leaf vertex exceeds stored upper")
            require(recomp_ub <= claim_limit, "N leaf vertex exceeds global claim")
            max_bound = max_bound.max(recomp_ub.upper())
            counts["naive"] += 1
            return

        if op == "C1":
            require(case == "case1" and len(vals) == 4, "unexpected or malformed C1 leaf")
            t_enc, eta_enc, u_list, leaf_claim = vals
            require(type(leaf_claim) is int and leaf_claim == LIMIT, "invalid C1 leaf claim")
            ub = verify_c1_leaf(clipped, t_enc, eta_enc, u_list, claim_limit, also_exact_poly=check_exact_poly)
            max_bound = max_bound.max(ub.upper())
            counts["occupancy"] += 1
            return

        if op == "C2":
            require(case == "case2" and len(vals) == 5, "unexpected or malformed C2 leaf")
            t_enc, eta_enc, upper_enc, payload, leaf_claim = vals
            require(type(leaf_claim) is int and leaf_claim == LIMIT, "invalid C2 leaf claim")
            ub = verify_c2_leaf(clipped, t_enc, eta_enc, upper_enc, payload, claim_limit)
            max_bound = max_bound.max(ub.upper())
            counts["occupancy"] += 1
            return

        raise ValueError(f"unknown opcode {op!r}")

    walk(ROOT_BOUNDS)
    sentinel = object()
    require(next(records, sentinel) is sentinel, "trailing records after root cover")
    leaves = counts["empty"] + counts["naive"] + counts["occupancy"]
    require(leaves == counts["split"] + 1, "binary tree leaf/split identity failed")
    require(max_bound <= claim_limit, "global max bound exceeds claim")
    if not quiet:
        print(f"{case} PASS coverage=100% leaves={leaves} recomputed_max_upper={max_bound.str(28)} counts={counts}",
              flush=True)
    return case, max_bound, counts


def verify_file(path: Path, check_exact_poly=False, quiet=False):
    with gzip.open(path, "rt", encoding="utf-8") as src:
        cert = json.load(src)
    return verify_doc(cert, check_exact_poly=check_exact_poly, quiet=quiet)


def verify_finite_threshold():
    """Verify explicit finite-n existence inequality for every integer n >= N0 = 450,000."""
    # 1. Exact rational side conditions at N0:
    cap_at_n0 = Fraction(2, 5) + Fraction(3, 5 * N0)
    require(cap_at_n0 <= Fraction(MAX_PART, GRID), "part capacity exceeds 4001/10000 at N0")
    gap_vertices = Fraction(3, 20) * N0
    require(gap_vertices >= 38, "Region C transfer/exemption gap fails at N0")
    require(DBAR_LO > Fraction(49, 5), "average degree lower bound fails")
    require(Fraction(38, N0) < Fraction(-LIMIT, SCALE), "first-moment bound not decreasing at N0")

    # 2. Verify parity and edge count identity 5n - ceil(n/20) == floor(99n/20) on all residues mod 40:
    for r in range(40):
        n_test = N0 + r
        k = (n_test + 19) // 20
        n9 = 2 * k
        n10 = n_test - n9
        d_stubs = 9 * n9 + 10 * n10
        require(n9 % 2 == 0 and d_stubs % 2 == 0, "odd stub count")
        require(d_stubs // 2 == (99 * n_test) // 20, "multiedge floor(99n/20) identity failed")
        alpha9_n = Fraction(n9, n_test)
        require(ALPHA9_LO <= alpha9_n <= ALPHA9_HI, "alpha9(n) outside certified interval")

    # 3. 180-bit Arb evaluation of B(N0) and disconnection geometric series:
    n_a = arb(N0)
    d_max_a = 10 * n_a
    # B(n) = 30 * 3^9 * (n+1)^8 * (10n+1)^11 * n^19 * 200^19 * exp(-3n/2000)
    log_b = (
        arb(30 * 3**9).log()
        + 8 * (n_a + 1).log()
        + 11 * (d_max_a + 1).log()
        + 19 * n_a.log()
        + 19 * arb(200).log()
        - (3 * n_a) / 2000
    )
    require(log_b < -arb(35), "log first-moment bound too large at N0")
    b_val = log_b.exp()

    # Disconnection bound: sum_{k>=1} rho_disc^k = rho_disc / (1 - rho_disc),
    # where rho_disc = e * (50/49)^(9/2) * 2^(-7/2).
    e_const = arb(1).exp()
    ratio_50_49 = (arb(50) / arb(49)) ** (arb(9) / arb(2))
    two_pow = arb(2) ** (arb(-7) / arb(2))
    rho_disc = e_const * ratio_50_49 * two_pow
    require(rho_disc > 0 and rho_disc < arb(3) / arb(10), "unexpected rho_disc range")
    p_disc = rho_disc / (1 - rho_disc)
    require(p_disc < arb(1) / arb(2), "disconnection probability >= 1/2")

    total_fail = b_val + p_disc
    require(total_fail < arb(1), "total failure probability >= 1")
    deriv_ub = arb(38) / n_a - arb(3) / arb(2000)
    require(deriv_ub < 0, "log derivative not strictly negative")

    print(f"FINITE PASS n0={N0} (all integers n >= {N0}, even and odd)", flush=True)
    print(f"  log_B(n0)        = {log_b.str(24)}", flush=True)
    print(f"  B(n0)            = {b_val.str(24)}", flush=True)
    print(f"  rho_disc         = {rho_disc.str(24)}", flush=True)
    print(f"  P(disconnected) <= {p_disc.str(24)}", flush=True)
    print(f"  total_fail(n0)  <= {total_fail.str(24)} < 1", flush=True)
    print(f"  d/dn log B(n)   <= {deriv_ub.str(24)} < 0 for all n >= {N0}", flush=True)


def exact_primal_rate_arb(a9_fr, a10_fr, q_fr):
    """Evaluate exact L_bideg(a9, a10, Q) from raw exact Fraction inputs after verifying all constraints."""
    alpha9 = sum(a9_fr)
    theta = sum(a10_fr)
    require(alpha9 + theta == 1 and ALPHA9_LO <= alpha9 <= ALPHA9_HI, "primal witness alpha9 out of range")
    d_bar = 9 * alpha9 + 10 * theta
    s_tilde = [(9 * a9_fr[i] + 10 * a10_fr[i]) / d_bar for i in range(5)]
    for i in range(5):
        require(a9_fr[i] >= 0 and a10_fr[i] >= 0, "negative part split")
        require(sum(q_fr[i]) == s_tilde[i], "Q row sum mismatch against raw s_tilde")
        for j in range(5):
            require(q_fr[i][j] == q_fr[j][i] and q_fr[i][j] >= 0, "Q asymmetric or negative")
            if (i, j) not in BLUE:
                require(q_fr[i][j] == 0, "nonzero red entry in Q")

    alpha9_a = arb_rat(alpha9)
    theta_a = arb_rat(theta)
    d_a = arb_rat(d_bar)
    val = entropy_term(alpha9_a) + entropy_term(theta_a)
    for i in range(5):
        val -= entropy_term(arb_rat(a9_fr[i])) + entropy_term(arb_rat(a10_fr[i]))
        val += d_a * entropy_term(arb_rat(s_tilde[i]))
        for j in range(5):
            val -= (d_a / 2) * entropy_term(arb_rat(q_fr[i][j]))
    return val


def build_feasible_q_fraction(s_tilde):
    """Construct an exact rational symmetric nonnegative blue matrix Q with row sums s_tilde (when feasible)."""
    # Greedy/convex blue flow: for Region C (a0, a2 >= max(a1, a3, a4)), put diagonal + off-diagonal blue mass!
    # Simpler exact construction: solve Sinkhorn in rationals? Even simpler:
    # Notice ALLOWED has diagonal 1 on ALL 5 vertices!
    # So Q = diag(s_tilde) ALWAYS has exact row sums s_tilde, is symmetric, nonnegative, and supported on BLUE!!
    # AND to test non-diagonal Q (with positive Q03, Q02, Q24!), mix diag(s_tilde) with valid symmetric edge transfers:
    # For any off-diagonal blue pair (i, j) and 0 <= w <= min(s_tilde[i], s_tilde[j]), subtracting w from Q[i][i] & Q[j][j]
    # and adding w to Q[i][j] & Q[j][i] preserves symmetry, row sums, nonnegativity, and blue support!
    q = [[Fraction(0) for _ in range(5)] for _ in range(5)]
    for i in range(5):
        q[i][i] = s_tilde[i]
    return q


def add_blue_edge_mass(q, i, j, w: Fraction):
    require((i, j) in BLUE and i != j and w >= 0, "invalid blue transfer")
    require(q[i][i] >= w and q[j][j] >= w, "insufficient diagonal slack for edge transfer")
    out = [row[:] for row in q]
    out[i][i] -= w
    out[j][j] -= w
    out[i][j] += w
    out[j][i] += w
    return out


def run_controls(cert_dir: Path):
    print("=== RUNNING CONTROLS ===", flush=True)
    docs = {}
    for label in LABELS:
        with gzip.open(cert_dir.joinpath(f"cert_{label}.json.gz"), "rt", encoding="utf-8") as src:
            docs[label] = json.load(src)

    # ------------------------------------------------------------------
    # Control 1: Positive Bare First-Moment Witness at c = 4.95 (alpha9 = 1/10)
    # ------------------------------------------------------------------
    # Construct exact rational Region C witness near (2/5, 0.00014, 2/5, 0.1871, 0.01276)
    scale_w = 10**8
    a_wit = [Fraction(40_000_000, scale_w), Fraction(13_884, scale_w), Fraction(40_000_000, scale_w),
             Fraction(18_711_729, scale_w), Fraction(1_274_387, scale_w)]
    require(sum(a_wit) == 1 and max(a_wit) <= Fraction(2, 5), "witness outside cap")
    require(min(a_wit[0], a_wit[2]) - a_wit[3] >= Fraction(3, 20) and a_wit[3] >= a_wit[4], "witness not in Region C")
    alpha9_w = Fraction(1, 10)
    a9_wit = [alpha9_w * x for x in a_wit]
    a10_wit = [(1 - alpha9_w) * x for x in a_wit]
    d_w = Fraction(99, 10)
    s_wit = [(9 * a9_wit[i] + 10 * a10_wit[i]) / d_w for i in range(5)]  # equals a_wit!
    off_w = [Fraction(16_804_449, scale_w), Fraction(12_730, scale_w), Fraction(1_206_998, scale_w),
             Fraction(10_352_983, scale_w), Fraction(1_134, scale_w)]
    q_wit = build_feasible_q_fraction(s_wit)
    for idx, w_val in enumerate(off_w):
        q_wit = add_blue_edge_mass(q_wit, idx, (idx + 2) % 5, w_val)
    wit_rate = exact_primal_rate_arb(a9_wit, a10_wit, q_wit)
    require(wit_rate > arb(14) / arb(1000), "bare c=4.95 witness should exceed +0.014")
    print(f"Control 1a PASS: bare c=4.95 naive witness L_bideg = {wit_rate.str(24)} > +0.014", flush=True)

    # Locate the leaf in cert_case1 covering a_wit and confirm mutating C1 -> N is REJECTED!
    wit_grid = [x * GRID for x in a_wit]
    recs_c1 = docs["case1"]["records"]
    idx_ptr = 0
    found_c1_idx = None

    def find_covering_leaf(bounds):
        nonlocal idx_ptr, found_c1_idx
        my_idx = idx_ptr
        rec = recs_c1[idx_ptr]
        idx_ptr += 1
        op = rec[0]
        if op == "X":
            return
        if op == "S":
            _, ax, cut = rec
            left = [p[:] for p in bounds]; right = [p[:] for p in bounds]
            left[ax] = [bounds[ax][0], cut]; right[ax] = [cut, bounds[ax][1]]
            find_covering_leaf(left)
            find_covering_leaf(right)
            return
        if all(bounds[k][0] <= wit_grid[k] <= bounds[k][1] for k in range(5)):
            found_c1_idx = my_idx

    find_covering_leaf(ROOT_BOUNDS)
    require(found_c1_idx is not None and recs_c1[found_c1_idx][0] == "C1",
            "positive naive witness must land in a C1 occupancy leaf")
    mut_wit = json.loads(json.dumps(docs["case1"]))
    old_c1 = mut_wit["records"][found_c1_idx]
    mut_wit["records"][found_c1_idx] = ["N", old_c1[1], old_c1[2], LIMIT, LIMIT]
    rejected_wit = False
    try:
        verify_doc(mut_wit, quiet=True)
    except ValueError:
        rejected_wit = True
    require(rejected_wit, "mutating positive-witness C1 leaf to N was not rejected")
    print(f"Control 1b PASS: covering C1 leaf record[{found_c1_idx}] rejected when mutated to naive N", flush=True)

    # ------------------------------------------------------------------
    # Control 2: Direct Primal Evaluation on Exact Rational Tuples Across Leaves
    # ------------------------------------------------------------------
    checked_n, checked_c1, checked_c2_near, checked_c2_tail = 0, 0, 0, 0
    claim_lim = arb(LIMIT) / SCALE

    for label in LABELS:
        it = iter(docs[label]["records"])

        def check_leaves(bounds):
            nonlocal checked_n, checked_c1, checked_c2_near, checked_c2_tail
            rec = next(it)
            op, *vals = rec
            clipped = hull_bounds(bounds, label)
            if op == "X":
                return
            if op == "S":
                ax, cut = vals
                left = [p[:] for p in bounds]; right = [p[:] for p in bounds]
                left[ax] = [bounds[ax][0], cut]; right[ax] = [cut, bounds[ax][1]]
                check_leaves(left)
                check_leaves(right)
                return
            pts = sliced_box_vertices(clipped)
            # Average all vertices in exact Fraction to get an interior rational point a_fr in clipped:
            m_pts = len(pts)
            a_fr = [Fraction(sum(p[k] for p in pts), m_pts * GRID) for k in range(5)]
            require(sum(a_fr) == 1, "interior rational profile sum != 1")
            a9_fr = [ALPHA9_LO * x for x in a_fr]
            a10_fr = [THETA_HI * x for x in a_fr]
            s_fr = [(9 * a9_fr[k] + 10 * a10_fr[k]) / DBAR_HI for k in range(5)]

            if op == "N" and checked_n < 200:
                q_fr = build_feasible_q_fraction(s_fr)
                w02 = min(s_fr[0], s_fr[2]) / 3
                q_fr = add_blue_edge_mass(q_fr, 0, 2, w02)
                primal = exact_primal_rate_arb(a9_fr, a10_fr, q_fr)
                leaf_ub, _, _ = eval_dual_on_points(pts, vals[0], vals[1])
                require(primal <= leaf_ub and leaf_ub <= claim_lim, "Control 2 N leaf primal violation")
                checked_n += 1

            elif op == "C1":
                # Construct feasible Q with positive Q03 >= s0/20 and Q02 >= s0/10
                w03 = min(s_fr[0] / 6, s_fr[3] / 2)
                w02 = min(s_fr[0] / 3, s_fr[2] / 2)
                if w03 > 0 and w02 > 0 and w03 + w02 <= s_fr[0]:
                    q_fr = build_feasible_q_fraction(s_fr)
                    q_fr = add_blue_edge_mass(q_fr, 0, 3, w03)
                    q_fr = add_blue_edge_mass(q_fr, 0, 2, w02)
                    primal_L = exact_primal_rate_arb(a9_fr, a10_fr, q_fr)
                    p3 = arb_rat(w03 / s_fr[0])
                    p2 = arb_rat(w02 / s_fr[0])
                    q2 = arb_rat(w02 / s_fr[2])
                    a0_a = arb_rat(a_fr[0])
                    a2_a = arb_rat(a_fr[2])
                    true_c1 = (primal_L
                               + a0_a * (1 - (1 - p3) ** 10).log()
                               + a0_a * (1 - (1 - p2) ** 10).log()
                               + a2_a * (1 - (1 - q2) ** 10).log())
                    leaf_ub = verify_c1_leaf(clipped, vals[0], vals[1], vals[2], claim_lim)
                    require(true_c1 <= leaf_ub and leaf_ub <= claim_lim, "Control 2 C1 primal violation")
                    checked_c1 += 1

            elif op == "C2":
                t_enc, eta_enc, upper_enc, (h02_int, h24_int, u_int), _ = vals
                leaf_ub = verify_c2_leaf(clipped, t_enc, eta_enc, upper_enc, [h02_int, h24_int, u_int], claim_lim)
                h02_fr = Fraction(h02_int, GRID)
                h24_fr = Fraction(h24_int, GRID)
                # Near sample: Q02 <= h02, Q24 <= h24 with positive entries
                w02 = min(h02_fr, s_fr[0] / 3, s_fr[2] / 3)
                w24 = min(h24_fr, (s_fr[2] - w02) / 2, s_fr[4] / 2)
                q_near = build_feasible_q_fraction(s_fr)
                q_near = add_blue_edge_mass(q_near, 0, 2, w02)
                q_near = add_blue_edge_mass(q_near, 2, 4, w24)
                primal_near = exact_primal_rate_arb(a9_fr, a10_fr, q_near)
                u_a = arb(u_int) / SCALE
                f_a = 1 - (1 - u_a) ** 10
                b_a = 10 * ((1 - u_a) ** 9) / f_a
                g_a = f_a.log() - b_a * u_a
                r0_pt = arb_rat(a_fr[0]) / arb_rat(DBAR_HI * s_fr[0])
                w_pt = (b_a * r0_pt).exp()
                q0_pt = arb_rat(w02 / s_fr[2])
                q4_pt = arb_rat(w24 / s_fr[2])
                m_pt = ((1 + (w_pt - 1) * q0_pt) ** 10
                        - (1 - q4_pt + (w_pt - 1) * q0_pt) ** 10
                        + (1 - q4_pt) ** 10
                        - (1 - q0_pt) ** 10)
                true_c2_near = primal_near + arb_rat(a_fr[0]) * g_a + arb_rat(a_fr[2]) * m_pt.log()
                require(true_c2_near <= leaf_ub and leaf_ub <= claim_lim, "Control 2 C2 near violation")
                checked_c2_near += 1

                # Tail sample (check Q24 > h24 or Q02 > h02 whenever feasible at a_fr):
                cap02_pt = min(s_fr[0], s_fr[2])
                cap24_pt = min(s_fr[2], s_fr[4])
                if cap24_pt > h24_fr:
                    w24_tail = (h24_fr + cap24_pt) / 2
                    q_tail = build_feasible_q_fraction(s_fr)
                    q_tail = add_blue_edge_mass(q_tail, 2, 4, w24_tail)
                    require(q_tail[2][4] > h24_fr, "tail label mismatch against raw Q24")
                    primal_tail = exact_primal_rate_arb(a9_fr, a10_fr, q_tail)
                    require(primal_tail <= claim_lim, "Control 2 C2 tail violation")
                    checked_c2_tail += 1
                elif cap02_pt > h02_fr:
                    w02_tail = (h02_fr + cap02_pt) / 2
                    q_tail = build_feasible_q_fraction(s_fr)
                    q_tail = add_blue_edge_mass(q_tail, 0, 2, w02_tail)
                    require(q_tail[0][2] > h02_fr, "tail label mismatch against raw Q02")
                    primal_tail = exact_primal_rate_arb(a9_fr, a10_fr, q_tail)
                    require(primal_tail <= claim_lim, "Control 2 C2 tail violation")
                    checked_c2_tail += 1

        check_leaves(ROOT_BOUNDS)

    require(checked_n > 0 and checked_c1 > 0 and checked_c2_near > 0 and checked_c2_tail > 0,
            "Control 2 missed a leaf category")
    print(f"Control 2 PASS: direct exact-rational primal <= leaf_bound <= -3/2000 on "
          f"N={checked_n}, C1={checked_c1}, C2_near={checked_c2_near}, C2_tail={checked_c2_tail}", flush=True)

    # ------------------------------------------------------------------
    # Control 3: Small-Degree Exact Brute-Force Combinatorial Check (d in {2, 3}, v0=2, v2=2)
    # ------------------------------------------------------------------
    # Verify exact row-0 conditional probability of {n3>=1 and n2>=1 on all vertices} <= 27*(D+1)^2 * (f_d(p3)*f_d(p2))^v0
    # and exact Case II hot-stub moment E[w^R | K] <= (1 + (K02/(S2-K24))*(w-1))^( (d-1)*K24 ) across ALL cells!
    c3_cells = 0
    for d_small in (2, 3):
        v_cnt = 2
        s_tot = d_small * v_cnt
        all_words = list(product((0, 2, 3), repeat=s_tot))
        by_k = {}
        for w in all_words:
            k_tup = (w.count(0), w.count(2), w.count(3))
            by_k.setdefault(k_tup, []).append(w)
        for (k0, k2, k3), words in by_k.items():
            good = sum(
                1 for w in words
                if all((2 in w[u * d_small:(u + 1) * d_small]) and (3 in w[u * d_small:(u + 1) * d_small])
                       for u in range(v_cnt))
            )
            exact_p = Fraction(good, len(words))
            if exact_p > 0:
                p2_s = Fraction(k2, s_tot)
                p3_s = Fraction(k3, s_tot)
                fd_p2 = 1 - (1 - p2_s) ** d_small
                fd_p3 = 1 - (1 - p3_s) ** d_small
                bound_p = 27 * ((2 * s_tot + 1) ** 2) * ((fd_p2 * fd_p3) ** v_cnt)
                require(exact_p <= bound_p, "Control 3 small-degree Case I bound violated")
                c3_cells += 1

        # Case II Row-2 exact trinomial M_d(q0, q4; w) check on {0, 2, 4}^s_tot with exact w = 3/2:
        w_val = Fraction(3, 2)
        words2 = list(product((0, 2, 4), repeat=s_tot))
        by_k2 = {}
        for w in words2:
            k_tup = (w.count(0), w.count(2), w.count(4))
            by_k2.setdefault(k_tup, []).append(w)
        for (k20, k22, k24), words in by_k2.items():
            exact_mom = Fraction(0)
            for w in words:
                ok_n0 = True
                r_hot = 0
                for v_idx in range(v_cnt):
                    blk = w[v_idx * d_small:(v_idx + 1) * d_small]
                    if 0 not in blk:
                        ok_n0 = False
                        break
                    if 4 in blk:
                        r_hot += blk.count(0)
                if ok_n0:
                    exact_mom += w_val ** r_hot
            exact_mom /= len(words)
            if exact_mom > 0:
                q0_s = Fraction(k20, s_tot)
                q4_s = Fraction(k24, s_tot)
                md_val = ((1 + (w_val - 1) * q0_s) ** d_small
                          - (1 - q4_s + (w_val - 1) * q0_s) ** d_small
                          + (1 - q4_s) ** d_small
                          - (1 - q0_s) ** d_small)
                bound_mom = 27 * ((2 * s_tot + 1) ** 2) * (md_val ** v_cnt)
                require(exact_mom <= bound_mom, "Control 3 small-degree Case II M_d bound violated")
                c3_cells += 1
    print(f"Control 3 PASS: {c3_cells} exact brute-force combinatorial cells verified at d=2,3 (0 violations)", flush=True)

    # ------------------------------------------------------------------
    # Control 4: 14 Surgical Certificate Corruption Mutants (All Must Reject)
    # ------------------------------------------------------------------
    def clone(label):
        return json.loads(json.dumps(docs[label]))

    def first_idx(label, op):
        for idx, rec in enumerate(docs[label]["records"]):
            if rec[0] == op:
                return idx
        raise RuntimeError(f"missing {op} in {label}")

    def tightest_idx(label, op):
        best_i, best_v = None, None
        it_t = iter(enumerate(docs[label]["records"]))

        def scan(bounds):
            nonlocal best_i, best_v
            idx, rec = next(it_t)
            rop, *vals = rec
            clipped = hull_bounds(bounds, label)
            if rop == "X":
                return
            if rop == "S":
                ax, cut = vals
                l_b = [p[:] for p in bounds]; r_b = [p[:] for p in bounds]
                l_b[ax] = [bounds[ax][0], cut]; r_b[ax] = [cut, bounds[ax][1]]
                scan(l_b); scan(r_b)
                return
            if rop != op:
                return
            if rop == "N":
                ub, _, _ = eval_dual_on_points(sliced_box_vertices(clipped), vals[0], vals[1])
            elif rop == "C1":
                ub = verify_c1_leaf(clipped, vals[0], vals[1], vals[2], claim_lim)
            else:
                ub = verify_c2_leaf(clipped, vals[0], vals[1], vals[2], vals[3], claim_lim)
            if best_v is None or ub.upper() > best_v.upper():
                best_i, best_v = idx, ub

        scan(ROOT_BOUNDS)
        return best_i

    idx_n = tightest_idx("naive_ab", "N")
    idx_c1 = tightest_idx("case1", "C1")
    idx_c2 = tightest_idx("case2", "C2")
    idx_s = first_idx("naive_ab", "S")

    mutants = []

    # 1. Perturb tilt on tightest N leaf (zero out asymmetry -> uniform tilt)
    m1 = clone("naive_ab")
    m1["records"][idx_n][1] = [SCALE] * 5
    mutants.append(("mutant_01_uniform_tilt_N", m1))

    # 2. Perturb eta by +20*SCALE on tightest N leaf
    m2 = clone("naive_ab")
    m2["records"][idx_n][2] += 20 * SCALE
    mutants.append(("mutant_02_shifted_eta_N", m2))

    # 3. Replace N leaf by false empty X
    m3 = clone("naive_ab")
    m3["records"][idx_n] = ["X"]
    mutants.append(("mutant_03_false_empty_X", m3))

    # 4. Non-interior split (cut = 0)
    m4 = clone("naive_ab")
    m4["records"][idx_s] = ["S", m4["records"][idx_s][1], 0]
    mutants.append(("mutant_04_non_interior_split", m4))

    # 5. Truncated stream (pop last leaf)
    m5 = clone("case1")
    m5["records"].pop()
    mutants.append(("mutant_05_truncated_records", m5))

    # 6. Trailing record
    m6 = clone("case1")
    m6["records"].append(["X"])
    mutants.append(("mutant_06_trailing_record", m6))

    # 7. Altered root cap
    m7 = clone("case1")
    m7["root"] = [[0] * 5, [MAX_PART - 1] * 5]
    mutants.append(("mutant_07_altered_root", m7))

    # 8. Weakened global & leaf claim (-1499999999 > LIMIT)
    m8 = clone("case1")
    m8["claim"] = LIMIT + 1
    mutants.append(("mutant_08_weakened_claim", m8))

    # 9. Perturbed u_ints -> near 1 on tightest C1 leaf
    m9 = clone("case1")
    m9["records"][idx_c1][3] = [SCALE - 1, SCALE - 1, SCALE - 1]
    mutants.append(("mutant_09_bad_tangents_C1", m9))

    # 10. Nonpositive tilt entry in C1 leaf
    m10 = clone("case1")
    m10["records"][idx_c1][1][0] = 0
    mutants.append(("mutant_10_zero_tilt_C1", m10))

    # 11. Wrong-side KL cutoff h02 = 1 (< B02) on tightest C2 leaf
    m11 = clone("case2")
    m11["records"][idx_c2][4][0] = 1
    mutants.append(("mutant_11_cutoff_below_B02_C2", m11))

    # 12. Out-of-domain h24 = GRID + 1 (> GRID) on tightest C2 leaf
    m12 = clone("case2")
    m12["records"][idx_c2][4][1] = GRID + 1
    mutants.append(("mutant_12_h24_out_of_range_C2", m12))

    # 13. Valid interior tangent perturbation on tightest C1 leaf (tests C1 rate inequality directly)
    m13 = clone("case1")
    m13["records"][idx_c1][3] = [SCALE // 20, SCALE // 20, SCALE // 20]
    mutants.append(("mutant_13_interior_tangent_C1", m13))

    # 14. Valid interior tangent perturbation on tightest C2 leaf (tests C2 8x8 cell rate inequality directly)
    m14 = clone("case2")
    m14["records"][idx_c2][4][2] = SCALE // 50
    mutants.append(("mutant_14_interior_tangent_C2", m14))

    for name, m_doc in mutants:
        rejected = False
        reason = ""
        try:
            verify_doc(m_doc, quiet=True)
        except ValueError as exc:
            rejected = True
            reason = str(exc)
        require(rejected, f"mutant {name} WAS ACCEPTED")
        print(f"Control 4 PASS: {name} REJECTED ({reason})", flush=True)

    print(f"ALL CONTROLS PASSED ({len(mutants)}/{len(mutants)} mutants rejected)", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--cert-dir", type=Path, default=Path("certificates"))
    parser.add_argument("--exact-poly", action="store_true", help="also check exact 4D Region C polytope vertices on C1")
    parser.add_argument("--no-finite", action="store_true")
    parser.add_argument("--controls", action="store_true")
    parser.add_argument("--no-controls", action="store_true")
    args = parser.parse_args()

    paths = args.files if args.files else [args.cert_dir.joinpath(f"cert_{lbl}.json.gz") for lbl in LABELS]
    seen = []
    for p in paths:
        case, _, _ = verify_file(p, check_exact_poly=args.exact_poly)
        seen.append(case)
    full_cover = sorted(seen) == sorted(LABELS)
    if not args.no_finite and full_cover:
        verify_finite_threshold()
    if args.controls or (not args.no_controls and full_cover):
        run_controls(args.cert_dir)


if __name__ == "__main__":
    try:
        main()
    except (ArithmeticError, KeyError, OSError, TypeError, ValueError) as err:
        sys.exit(f"VERIFICATION FAILED: {err}")
