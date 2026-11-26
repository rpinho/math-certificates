#!/usr/bin/env python3
"""Standalone clean-room 160-bit Arb verifier for repaired Case I of Erdos #1182.

Dependencies: Python standard library + python-flint 0.9.0 ONLY.
Audits:
  1. SHA-256 hash locks on staged certificate archives in inputs/.
  2. Full tree reconstruction of cert_case1.json.gz from exact root [0, 4001/10000]^5
     (strictly interior splits, zero uncovered regions, zero truncated/trailing records,
     full canonical Region C coverage).
  3. Independent 160-bit outward-rounded Arb recomputation on every leaf from exact
     rational polytope vertices (both tightened sliced-box superset H(B') and exact
     Region C polytope P_C(B)), tilts, and cutoffs ONLY (stored bounds are never trusted,
     and are additionally checked for internal consistency against inflation/deflation).
  4. Strict interval enforcement of q_* >= B_03 on EVERY occupancy leaf, binary-KL
     tail bound on Q_03 > q_*, occupancy bound on Q_03 <= q_*, and leaf upper bound
     <= -1/1000 on every leaf.
  5. Independent 160-bit Arb recomputation of the finite-n bound at n_0 = 550,000.
"""

import argparse
from fractions import Fraction
import gzip
import hashlib
import json
import pathlib
import sys
import time

import flint

ARB_PREC = 160

EXPECTED_SHA256 = {
    "cert_naive_ab.json.gz": "b4cbc312f5f1a042990c031df8b35542eb6f192639ea93edf024b61002ec5989",
    "cert_case2.json.gz": "c68d3339047880b19de426b6bde3114630ce10ad853ecc409926f621d5c3bab8",
}

# Blue adjacency on Z_5: A_{ij} = 1 iff (i - j) mod 5 in {0, 2, 3}
BLUE_ADJ = tuple(
    tuple(1 if ((i - j) % 5) in (0, 2, 3) else 0 for j in range(5))
    for i in range(5)
)

DELTA_C = Fraction(3, 20)
ROOT_CAP = Fraction(4001, 10000)

# Region C pairwise difference constraints: a_i - a_j >= c
REGION_C_DIFFS = (
    (0, 1, Fraction(0)),
    (2, 1, Fraction(0)),
    (0, 3, DELTA_C),
    (2, 3, DELTA_C),
    (3, 4, Fraction(0)),
    (0, 4, DELTA_C),
    (2, 4, DELTA_C),
)

# Region C defining halfspaces: sum_j coeff[j] * a_j >= rhs
REGION_C_HALFSPACES = (
    ((1, -1, 0, 0, 0), Fraction(0)),
    ((0, -1, 1, 0, 0), Fraction(0)),
    ((1, 0, 0, -1, 0), DELTA_C),
    ((0, 0, 1, -1, 0), DELTA_C),
    ((0, 0, 0, 1, -1), Fraction(0)),
)


class VerificationError(Exception):
    """Raised whenever any structural, arithmetic, or certificate check fails."""


def is_exact_int(val) -> bool:
    return isinstance(val, int) and not isinstance(val, bool)


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def verify_hash_locks(inputs_dir: pathlib.Path) -> dict:
    hashes = {}
    for name in ("cert_naive_ab.json.gz", "cert_case2.json.gz", "cert_case1.json.gz"):
        p = inputs_dir / name
        if not p.is_file():
            raise VerificationError(f"Missing required input file: {p}")
        digest = sha256_file(p)
        hashes[name] = digest
        if name in EXPECTED_SHA256 and digest != EXPECTED_SHA256[name]:
            raise VerificationError(
                f"SHA-256 mismatch for {name}: got {digest}, expected {EXPECTED_SHA256[name]}"
            )
    return hashes


def frac_to_arb(fr: Fraction) -> flint.arb:
    return flint.arb(fr.numerator) / flint.arb(fr.denominator)


def in_region_c(pt) -> bool:
    if len(pt) != 5:
        return False
    if sum(pt) != Fraction(1):
        return False
    for x in pt:
        if x < 0 or x > ROOT_CAP:
            return False
    m02 = min(pt[0], pt[2])
    if m02 < max(pt[1], pt[3], pt[4]):
        return False
    if pt[3] < pt[4]:
        return False
    if m02 - pt[3] < DELTA_C:
        return False
    return True


def tighten_box_region_c(lo, hi):
    """Sound exact rational interval propagation on sum(a)=1 and Region C inequalities.

    Every point a in B intersect Region C satisfies tlo[i] <= a[i] <= thi[i].
    Returns (tlo, thi) as tuples of Fraction, or None if provably empty.
    """
    tlo = list(lo)
    thi = list(hi)
    while True:
        changed = False
        for i in range(5):
            other_hi = sum(thi[j] for j in range(5) if j != i)
            other_lo = sum(tlo[j] for j in range(5) if j != i)
            new_lo = max(tlo[i], Fraction(1) - other_hi)
            new_hi = min(thi[i], Fraction(1) - other_lo)
            if new_lo > tlo[i]:
                tlo[i] = new_lo
                changed = True
            if new_hi < thi[i]:
                thi[i] = new_hi
                changed = True
        for i, j, c in REGION_C_DIFFS:
            if tlo[j] + c > tlo[i]:
                tlo[i] = tlo[j] + c
                changed = True
            if thi[i] - c < thi[j]:
                thi[j] = thi[i] - c
                changed = True
        for i in range(5):
            if tlo[i] > thi[i]:
                return None
        if not changed:
            break
    if sum(tlo) > Fraction(1) or sum(thi) < Fraction(1):
        return None
    return tuple(tlo), tuple(thi)


def enumerate_sliced_box_vertices(tlo, thi):
    """Enumerate ALL extreme points of H(B') = {a in prod [tlo_i, thi_i] : sum(a) = 1}.

    By convexity/linearity, any point of H(B') with >= 2 strictly interior coordinates
    can be perturbed +/- eps*(e_j - e_k), so EVERY extreme point of H(B') has >= 4
    coordinates at box endpoints (valid in all dimensions, with zero non-degeneracy assumptions).
    """
    verts = set()
    for free in range(5):
        others = [j for j in range(5) if j != free]
        for mask in range(16):
            pt = [None] * 5
            partial = Fraction(0)
            for bit, j in enumerate(others):
                val = thi[j] if ((mask >> bit) & 1) else tlo[j]
                pt[j] = val
                partial += val
            rem = Fraction(1) - partial
            if tlo[free] <= rem <= thi[free]:
                pt[free] = rem
                verts.add(tuple(pt))
    return sorted(verts)


def enumerate_exact_region_c_vertices(lo, hi, tlo, thi):
    """Independently enumerate the exact extreme points of P_C(B) = B intersect Region C.

    Starts from H(B') with exact active inequality bitmasks on non-fixed coordinates
    and clips sequentially by the 5 Region C halfspaces using exact Fukuda-Prodon
    combinatorial edge adjacency in arbitrary dimension. Every surviving vertex is
    independently verified against lo <= v <= hi and Region C constraints.
    """
    nonfixed = [j for j in range(5) if tlo[j] < thi[j]]
    d_cur = len(nonfixed) - 1
    base_verts = enumerate_sliced_box_vertices(tlo, thi)
    if not base_verts:
        return []
    if d_cur <= 0:
        return [v for v in base_verts if in_region_c(v) and all(lo[i] <= v[i] <= hi[i] for i in range(5))]

    verts = []
    next_bit = 2 * len(nonfixed)
    for pt in base_verts:
        fmask = 0
        for idx_j, j in enumerate(nonfixed):
            if pt[j] == tlo[j]:
                fmask |= 1 << idx_j
            if pt[j] == thi[j]:
                fmask |= 1 << (len(nonfixed) + idx_j)
        verts.append((pt, fmask))

    for coeffs, rhs in REGION_C_HALFSPACES:
        vals = [sum(coeffs[j] * pt[j] for j in range(5)) - rhs for pt, _ in verts]
        pos = [k for k, v in enumerate(vals) if v > 0]
        zer = [k for k, v in enumerate(vals) if v == 0]
        neg = [k for k, v in enumerate(vals) if v < 0]
        if not neg:
            verts = [
                (pt, m | ((1 << next_bit) if vals[k] == 0 else 0))
                for k, (pt, m) in enumerate(verts)
            ]
            next_bit += 1
            continue
        if not pos and not zer:
            return []
        if not pos and zer:
            verts = [(verts[k][0], verts[k][1] | (1 << next_bit)) for k in zer]
            d_cur = max(0, d_cur - 1)
            next_bit += 1
            continue

        all_masks = [m for _, m in verts]
        min_common = max(0, d_cur - 1)
        new_verts = [verts[k] for k in pos] + [
            (verts[k][0], verts[k][1] | (1 << next_bit)) for k in zer
        ]
        for ip in pos:
            pt_p, mp = verts[ip]
            vp = vals[ip]
            for ineg in neg:
                pt_n, mn = verts[ineg]
                common = mp & mn
                if common.bit_count() < min_common:
                    continue
                adj = True
                for k, mk in enumerate(all_masks):
                    if k != ip and k != ineg and (mk & common) == common:
                        adj = False
                        break
                if adj:
                    vn = -vals[ineg]
                    denom = vp + vn
                    pt_new = tuple(
                        (vn * pt_p[j] + vp * pt_n[j]) / denom for j in range(5)
                    )
                    new_verts.append((pt_new, common | (1 << next_bit)))
        verts = new_verts
        next_bit += 1

    out = sorted({pt for pt, _ in verts})
    for pt in out:
        if not in_region_c(pt):
            raise VerificationError(f"Exact polytope vertex failed Region C check: {pt}")
        for i in range(5):
            if not (lo[i] <= pt[i] <= hi[i]):
                raise VerificationError(f"Exact polytope vertex outside leaf box: {pt}")
    return out


def eval_ut_vertices_arb(verts, t_arb, z_arb):
    """Evaluate U_t(v) = 9 sum a_i log a_i - 10 sum a_i log t_i + 5 log Z at all vertices in 160-bit Arb."""
    if not verts:
        raise VerificationError("Empty vertex list on leaf")
    log_t = [ti.log() for ti in t_arb]
    five_log_z = flint.arb(5) * z_arb.log()
    nine = flint.arb(9)
    ten = flint.arb(10)
    max_upper = None
    for v in verts:
        acc = five_log_z
        for i in range(5):
            vi = v[i]
            if vi < 0:
                raise VerificationError(f"Negative coordinate in vertex: {v}")
            if vi > 0:
                ai = frac_to_arb(vi)
                acc = acc + nine * ai * ai.log() - ten * ai * log_t[i]
        up = acc.upper()
        if not up.is_finite():
            raise VerificationError(f"Non-finite Arb U_t upper bound at vertex {v}")
        if max_upper is None or up > max_upper:
            max_upper = up
    return flint.arb(max_upper)


def load_strict_gzip_json(path: pathlib.Path):
    try:
        raw_bytes = gzip.decompress(path.read_bytes())
    except Exception as exc:
        raise VerificationError(f"Failed to decompress gzip {path}: {exc}") from exc
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"Invalid UTF-8 in {path}: {exc}") from exc
    decoder = json.JSONDecoder()
    stripped = text.lstrip()
    if not stripped:
        raise VerificationError(f"Empty JSON payload in {path}")
    try:
        obj, end_idx = decoder.raw_decode(stripped)
    except json.JSONDecodeError as exc:
        raise VerificationError(f"Malformed JSON in {path}: {exc}") from exc
    if stripped[end_idx:].strip():
        raise VerificationError(f"Trailing non-whitespace bytes after JSON root in {path}")
    return obj


def verify_case1_certificate(
    cert_obj: dict,
    check_exact_polytope: bool = True,
    collect_c_leaves: bool = False,
) -> dict:
    """Verify a Case I certificate dictionary in 160-bit outward-rounded Arb."""
    flint.ctx.prec = ARB_PREC
    if flint.ctx.prec != ARB_PREC:
        raise VerificationError(f"Failed to set Arb precision to {ARB_PREC}")

    if not isinstance(cert_obj, dict):
        raise VerificationError("Certificate root must be a JSON object")
    expected_keys = {"format", "case", "root", "grid", "tilt_scale", "claim", "records"}
    if set(cert_obj.keys()) != expected_keys:
        raise VerificationError(
            f"Unexpected top-level keys: got {sorted(cert_obj.keys())}, expected {sorted(expected_keys)}"
        )

    fmt = cert_obj["format"]
    if not is_exact_int(fmt) or fmt != 2:
        raise VerificationError(f"Invalid Case I format {fmt!r}: expected exact int 2")
    if cert_obj["case"] != "case1":
        raise VerificationError(f"Invalid case {cert_obj['case']!r}: expected 'case1'")

    grid = cert_obj["grid"]
    tilt_scale = cert_obj["tilt_scale"]
    claim_int = cert_obj["claim"]
    if not is_exact_int(grid) or grid <= 0:
        raise VerificationError(f"Invalid grid: {grid!r}")
    if not is_exact_int(tilt_scale) or tilt_scale <= 0:
        raise VerificationError(f"Invalid tilt_scale: {tilt_scale!r}")
    if not is_exact_int(claim_int):
        raise VerificationError(f"Invalid top-level claim: {claim_int!r}")

    target_bound = flint.arb(-1) / flint.arb(1000)
    target_frac = Fraction(-1, 1000)
    tscale_arb = flint.arb(tilt_scale)
    global_claim_frac = Fraction(claim_int, tilt_scale)
    global_claim = flint.arb(claim_int) / tscale_arb
    if global_claim_frac > target_frac:
        raise VerificationError(
            f"Top-level claim {global_claim_frac} exceeds required target -1/1000"
        )

    root = cert_obj["root"]
    if (
        not isinstance(root, list)
        or len(root) != 2
        or not isinstance(root[0], list)
        or not isinstance(root[1], list)
        or len(root[0]) != 5
        or len(root[1]) != 5
        or not all(is_exact_int(x) for x in root[0] + root[1])
    ):
        raise VerificationError(f"Malformed root box: {root!r}")

    root_lo = tuple(Fraction(x, grid) for x in root[0])
    root_hi = tuple(Fraction(x, grid) for x in root[1])
    if root_lo != (Fraction(0),) * 5 or root_hi != (ROOT_CAP,) * 5:
        raise VerificationError(
            f"Root box mismatch: got [{root_lo}, {root_hi}], expected [0, 4001/10000]^5"
        )

    records = cert_obj["records"]
    if not isinstance(records, list) or len(records) == 0:
        raise VerificationError("Certificate records must be a non-empty list")

    state = {
        "idx": 0,
        "splits": 0,
        "n_leaves": 0,
        "c_leaves": 0,
        "x_leaves": 0,
        "outer_c_vertices": 0,
        "exact_c_vertices": 0,
        "c_tail_active": 0,
        "max_recomp_outer": None,
        "max_recomp_exact": None,
        "max_storedU_bound": None,
        "max_naive_outer": None,
        "max_occ_near_outer": None,
        "max_occ_tail_outer": None,
        "min_q_minus_b03": None,
        "c_leaf_details": [],
    }

    def update_max(key: str, val_arf):
        cur = state[key]
        if cur is None or val_arf > cur:
            state[key] = val_arf

    def update_min(key: str, val_arf):
        cur = state[key]
        if cur is None or val_arf < cur:
            state[key] = val_arf

    def parse_tilt(t_raw, rec_idx: int):
        if (
            not isinstance(t_raw, list)
            or len(t_raw) != 5
            or not all(is_exact_int(x) and x > 0 for x in t_raw)
        ):
            raise VerificationError(f"Invalid tilt vector at record {rec_idx}: {t_raw!r}")
        t_arb = [flint.arb(x) / tscale_arb for x in t_raw]
        z_arb = flint.arb(0)
        for i in range(5):
            for j in range(5):
                if BLUE_ADJ[i][j]:
                    z_arb = z_arb + t_arb[i] * t_arb[j]
        if not bool(z_arb > 0):
            raise VerificationError(f"Non-positive partition function Z at record {rec_idx}")
        return t_arb, z_arb

    def walk(lo, hi):
        rec_idx = state["idx"]
        if rec_idx >= len(records):
            raise VerificationError(
                f"Truncated record stream at index {rec_idx}: uncovered box [{lo}, {hi}]"
            )
        rec = records[rec_idx]
        state["idx"] += 1

        if not isinstance(rec, list) or len(rec) == 0 or not isinstance(rec[0], str):
            raise VerificationError(f"Malformed record at index {rec_idx}: {rec!r}")

        kind = rec[0]
        if kind == "S":
            if len(rec) != 3 or not is_exact_int(rec[1]) or not is_exact_int(rec[2]):
                raise VerificationError(f"Malformed split record at index {rec_idx}: {rec!r}")
            dim, sp_int = rec[1], rec[2]
            if not (0 <= dim < 5):
                raise VerificationError(f"Invalid split dimension {dim} at index {rec_idx}")
            sp = Fraction(sp_int, grid)
            if not (lo[dim] < sp < hi[dim]):
                raise VerificationError(
                    f"Non-interior split at index {rec_idx} on dim {dim}: {sp} not in ({lo[dim]}, {hi[dim]})"
                )
            state["splits"] += 1
            hi_left = list(hi)
            hi_left[dim] = sp
            lo_right = list(lo)
            lo_right[dim] = sp
            walk(tuple(lo), tuple(hi_left))
            walk(tuple(lo_right), tuple(hi))
            return

        if kind == "X":
            if len(rec) != 1:
                raise VerificationError(f"Malformed X record at index {rec_idx}: {rec!r}")
            if tighten_box_region_c(lo, hi) is not None:
                raise VerificationError(
                    f"Unjustified X leaf at index {rec_idx}: Region C tightening is non-empty"
                )
            state["x_leaves"] += 1
            return

        if kind not in ("N", "C"):
            raise VerificationError(f"Unknown record kind {kind!r} at index {rec_idx}")

        tightened = tighten_box_region_c(lo, hi)
        if tightened is None:
            raise VerificationError(f"Empty tightened Region C box on {kind} leaf at index {rec_idx}")
        tlo, thi = tightened
        if tlo[0] <= 0:
            raise VerificationError(f"Non-positive tightened a0_min={tlo[0]} at index {rec_idx}")

        verts_outer = enumerate_sliced_box_vertices(tlo, thi)
        if not verts_outer:
            raise VerificationError(f"Zero sliced-box vertices at index {rec_idx}")

        verts_exact = None
        if check_exact_polytope:
            verts_exact = enumerate_exact_region_c_vertices(lo, hi, tlo, thi)
            if not verts_exact:
                raise VerificationError(f"Zero exact Region C polytope vertices at index {rec_idx}")

        if kind == "N":
            if len(rec) != 4 or not is_exact_int(rec[2]) or not is_exact_int(rec[3]):
                raise VerificationError(f"Malformed N leaf at index {rec_idx}: {rec!r}")
            t_arb, z_arb = parse_tilt(rec[1], rec_idx)
            u_stored_frac = Fraction(rec[2], tilt_scale)
            leaf_claim_frac = Fraction(rec[3], tilt_scale)
            u_stored = flint.arb(rec[2]) / tscale_arb
            leaf_claim = flint.arb(rec[3]) / tscale_arb

            if leaf_claim_frac > global_claim_frac or leaf_claim_frac > target_frac:
                raise VerificationError(
                    f"N leaf {rec_idx} claim {leaf_claim_frac} exceeds global/target bound"
                )

            u_outer = eval_ut_vertices_arb(verts_outer, t_arb, z_arb)
            if not bool(u_outer <= target_bound):
                raise VerificationError(
                    f"N leaf {rec_idx} recomputed U {u_outer} exceeds -1/1000"
                )
            if not bool(u_outer <= leaf_claim):
                raise VerificationError(
                    f"N leaf {rec_idx} recomputed U {u_outer} exceeds leaf claim {leaf_claim}"
                )
            if not bool(u_outer <= u_stored):
                raise VerificationError(
                    f"N leaf {rec_idx} stored U {u_stored} understates recomputed U {u_outer}"
                )
            if u_stored_frac > leaf_claim_frac:
                raise VerificationError(
                    f"N leaf {rec_idx} stored U {u_stored_frac} exceeds leaf claim {leaf_claim_frac}"
                )

            state["n_leaves"] += 1
            update_max("max_recomp_outer", u_outer.upper())
            update_max("max_naive_outer", u_outer.upper())
            update_max("max_storedU_bound", u_stored.upper())

            if check_exact_polytope:
                u_exact = eval_ut_vertices_arb(verts_exact, t_arb, z_arb)
                if not bool(u_exact <= target_bound):
                    raise VerificationError(
                        f"N leaf {rec_idx} exact-polytope U {u_exact} exceeds -1/1000"
                    )
                update_max("max_recomp_exact", u_exact.upper())
            return

        # Occupancy leaf 'C'
        if (
            len(rec) != 5
            or not is_exact_int(rec[2])
            or not isinstance(rec[3], list)
            or len(rec[3]) != 1
            or not is_exact_int(rec[3][0])
            or rec[3][0] <= 0
            or not is_exact_int(rec[4])
        ):
            raise VerificationError(f"Malformed C leaf at index {rec_idx}: {rec!r}")

        t_arb, z_arb = parse_tilt(rec[1], rec_idx)
        u_stored = flint.arb(rec[2]) / tscale_arb
        q_int = rec[3][0]
        q_fr = Fraction(q_int, grid)
        q_arb = frac_to_arb(q_fr)
        leaf_claim_frac = Fraction(rec[4], tilt_scale)
        leaf_claim = flint.arb(rec[4]) / tscale_arb

        if leaf_claim_frac > global_claim_frac or leaf_claim_frac > target_frac:
            raise VerificationError(
                f"C leaf {rec_idx} claim {leaf_claim_frac} exceeds global/target bound"
            )
        if not (Fraction(0) < 2 * q_fr < Fraction(1)):
            raise VerificationError(
                f"C leaf {rec_idx} invalid cutoff q_*={q_fr}: 2*q_* not in (0, 1)"
            )

        u_outer = eval_ut_vertices_arb(verts_outer, t_arb, z_arb)
        if not bool(u_outer <= u_stored):
            raise VerificationError(
                f"C leaf {rec_idx} stored U {u_stored} understates recomputed U {u_outer}"
            )

        # Tilted expectation B_03 = t_0 * t_3 / Z and strict cutoff check q_* >= B_03
        b03_arb = (t_arb[0] * t_arb[3]) / z_arb
        if not bool(b03_arb > 0) or not bool(flint.arb(2) * b03_arb < 1):
            raise VerificationError(
                f"C leaf {rec_idx} invalid B_03 interval: {b03_arb}"
            )
        if not bool(q_arb >= b03_arb):
            raise VerificationError(
                f"C leaf {rec_idx} violates cutoff condition q_* >= B_03: q_*={q_arb}, B_03={b03_arb}"
            )
        update_min("min_q_minus_b03", (q_arb - b03_arb).lower())

        # Occupancy bound on near cell Q_03 <= q_*: U + a_{0,min} * log f(min(1, q_* / a_{0,min}))
        a0_min_fr = tlo[0]
        a0_min_arb = frac_to_arb(a0_min_fr)
        p_fr = min(Fraction(1), q_fr / a0_min_fr)
        if p_fr == Fraction(1):
            g_outer = flint.arb(0)
        else:
            p_arb = frac_to_arb(p_fr)
            fp_arb = flint.arb(1) - (flint.arb(1) - p_arb) ** 10
            if not bool(fp_arb > 0):
                raise VerificationError(f"C leaf {rec_idx} non-positive f(p)={fp_arb}")
            g_outer = a0_min_arb * fp_arb.log()

        near_recomp = u_outer + g_outer
        near_stored_u = u_stored + g_outer
        if not bool(near_recomp <= target_bound):
            raise VerificationError(
                f"C leaf {rec_idx} recomputed near bound {near_recomp} exceeds -1/1000"
            )
        if not bool(near_recomp <= leaf_claim) or not bool(near_stored_u <= leaf_claim):
            raise VerificationError(
                f"C leaf {rec_idx} near bound ({near_recomp} / {near_stored_u}) exceeds leaf claim {leaf_claim}"
            )
        update_max("max_occ_near_outer", near_recomp.upper())

        # Binary-KL tail bound on Q_03 > q_*: U - 5 * D(2*q_*, 2*B_03)
        cap_q_fr = min(thi[0], thi[3])
        x_arb = flint.arb(2) * q_arb
        b_arb = flint.arb(2) * b03_arb
        one = flint.arb(1)
        dkl_arb = x_arb * (x_arb / b_arb).log() + (one - x_arb) * ((one - x_arb) / (one - b_arb)).log()
        if not bool(dkl_arb >= 0):
            raise VerificationError(
                f"C leaf {rec_idx} negative binary KL interval {dkl_arb}"
            )
        tail_recomp = u_outer - flint.arb(5) * dkl_arb
        tail_stored_u = u_stored - flint.arb(5) * dkl_arb

        if q_fr < cap_q_fr:
            state["c_tail_active"] += 1
            if not bool(tail_recomp <= target_bound):
                raise VerificationError(
                    f"C leaf {rec_idx} recomputed tail bound {tail_recomp} exceeds -1/1000"
                )
            if not bool(tail_recomp <= leaf_claim) or not bool(tail_stored_u <= leaf_claim):
                raise VerificationError(
                    f"C leaf {rec_idx} tail bound ({tail_recomp} / {tail_stored_u}) exceeds leaf claim {leaf_claim}"
                )
            leaf_recomp_hi = max(near_recomp.upper(), tail_recomp.upper())
            leaf_stored_hi = max(near_stored_u.upper(), tail_stored_u.upper())
            update_max("max_occ_tail_outer", tail_recomp.upper())
        else:
            leaf_recomp_hi = near_recomp.upper()
            leaf_stored_hi = near_stored_u.upper()

        state["c_leaves"] += 1
        state["outer_c_vertices"] += len(verts_outer)
        update_max("max_recomp_outer", leaf_recomp_hi)
        update_max("max_storedU_bound", leaf_stored_hi)

        if check_exact_polytope:
            state["exact_c_vertices"] += len(verts_exact)
            u_exact = eval_ut_vertices_arb(verts_exact, t_arb, z_arb)
            a0_min_exact_fr = min(v[0] for v in verts_exact)
            p_ex_fr = min(Fraction(1), q_fr / a0_min_exact_fr)
            if p_ex_fr == Fraction(1):
                g_exact = flint.arb(0)
            else:
                p_ex_arb = frac_to_arb(p_ex_fr)
                fp_ex = one - (one - p_ex_arb) ** 10
                if not bool(fp_ex > 0):
                    raise VerificationError(f"C leaf {rec_idx} exact-polytope f(p)<=0")
                g_exact = frac_to_arb(a0_min_exact_fr) * fp_ex.log()
            near_exact = u_exact + g_exact
            if not bool(near_exact <= target_bound):
                raise VerificationError(
                    f"C leaf {rec_idx} exact-polytope near bound {near_exact} exceeds -1/1000"
                )
            cap_exact_fr = max(min(v[0], v[3]) for v in verts_exact)
            if q_fr < cap_exact_fr:
                tail_exact = u_exact - flint.arb(5) * dkl_arb
                if not bool(tail_exact <= target_bound):
                    raise VerificationError(
                        f"C leaf {rec_idx} exact-polytope tail bound {tail_exact} exceeds -1/1000"
                    )
                exact_hi = max(near_exact.upper(), tail_exact.upper())
            else:
                exact_hi = near_exact.upper()
            update_max("max_recomp_exact", exact_hi)

        if collect_c_leaves:
            state["c_leaf_details"].append(
                {
                    "rec_idx": rec_idx,
                    "lo": lo,
                    "hi": hi,
                    "tlo": tlo,
                    "thi": thi,
                    "verts_exact": verts_exact if verts_exact is not None else [v for v in verts_outer if in_region_c(v)],
                    "t_int": list(rec[1]),
                    "q_fr": q_fr,
                    "b03_arb": b03_arb,
                    "u_recomp": u_outer,
                    "near_recomp": near_recomp,
                    "tail_recomp": tail_recomp,
                    "leaf_recomp_hi": flint.arb(leaf_recomp_hi),
                }
            )

    walk(root_lo, root_hi)
    if state["idx"] != len(records):
        raise VerificationError(
            f"Trailing records after tree completion: consumed {state['idx']} of {len(records)}"
        )
    total_leaves = state["n_leaves"] + state["c_leaves"] + state["x_leaves"]
    if total_leaves != state["splits"] + 1:
        raise VerificationError(
            f"Binary tree leaf/split mismatch: leaves={total_leaves}, splits={state['splits']}"
        )
    return state


def verify_finite_bound_arb(n0: int = 550000) -> dict:
    """Independently compute and verify the finite-n bound at n_0 in 160-bit Arb."""
    flint.ctx.prec = ARB_PREC
    n = flint.arb(n0)
    d_stubs = flint.arb(10) * n

    # Case I alone: <= 10 orientations * (n+1)^4 profiles * (10n+1)^5 types
    #   * 3^6 (10n+1)^3 pairing Stirling factor * (10n+1) n^19 20^19 occupancy factor * exp(-n/1000)
    case1_pref = (
        flint.arb(10)
        * (flint.arb(3) ** 6)
        * ((n + 1) ** 4)
        * ((d_stubs + 1) ** 9)
        * (n ** 19)
        * (flint.arb(20) ** 19)
    )
    rate_term = (-n / flint.arb(1000)).exp()
    case1_only = case1_pref * rate_term

    # Full 3-term bound across A/B naive + C Case I + C Case II (PROOF.md eq. 35):
    # E[X_rigid] <= 30 * 3^6 * (n+1)^4 * (10n+1)^10 * n^19 * 20^19 * exp(-n/1000)
    total_pref = (
        flint.arb(30)
        * (flint.arb(3) ** 6)
        * ((n + 1) ** 4)
        * ((d_stubs + 1) ** 10)
        * (n ** 19)
        * (flint.arb(20) ** 19)
    )
    e_x_rigid = total_pref * rate_term

    disc_coarse = flint.arb(3) / flint.arb(13)
    e_const = flint.arb(1).exp()
    disc_tight = e_const / (flint.arb(16) - e_const)

    sum_coarse = e_x_rigid + disc_coarse
    sum_tight = e_x_rigid + disc_tight
    log_deriv_upper = flint.arb(33) / n - flint.arb(1) / flint.arb(1000)

    # Integer threshold checks at n >= n0
    cap_at_n0 = Fraction(2, 5) + Fraction(3, 5 * n0)
    gap_at_n0 = DELTA_C * n0
    v0_min_at_n0 = DELTA_C * n0

    if not (cap_at_n0 <= ROOT_CAP):
        raise VerificationError(f"Cap condition failed at n0={n0}: {cap_at_n0} > {ROOT_CAP}")
    if not (gap_at_n0 >= 2):
        raise VerificationError(f"Region C gap condition failed at n0={n0}: {gap_at_n0} < 2")
    if not (v0_min_at_n0 >= 38):
        raise VerificationError(f"Case I v0 >= 2b=38 failed at n0={n0}: {v0_min_at_n0} < 38")
    if not bool(e_x_rigid < flint.arb("4.261e-11")):
        raise VerificationError(f"E[X_rigid] bound {e_x_rigid} exceeded 4.261e-11")
    if not bool(sum_coarse < 1) or not bool(sum_tight < 1):
        raise VerificationError(f"Total failure probability >= 1: {sum_coarse}")
    if not bool(log_deriv_upper < 0):
        raise VerificationError(f"Log-derivative upper bound >= 0 at n0={n0}: {log_deriv_upper}")

    return {
        "n0": n0,
        "case1_only": case1_only,
        "e_x_rigid": e_x_rigid,
        "disc_coarse": disc_coarse,
        "disc_tight": disc_tight,
        "sum_coarse": sum_coarse,
        "sum_tight": sum_tight,
        "log_deriv_upper": log_deriv_upper,
        "cap_at_n0": cap_at_n0,
        "gap_at_n0": gap_at_n0,
        "v0_min_at_n0": v0_min_at_n0,
    }


def format_finite_report(res: dict) -> str:
    lines = [
        f"=== Finite-n Arb Verification (prec={ARB_PREC} bits) ===",
        f"n0 = {res['n0']} (even and odd n supported since D = 10n is always even)",
        f"Cap check at n0: 2/5 + 3/(5*n0) = {res['cap_at_n0']} <= {ROOT_CAP} : PASS (holds for all n >= 6000)",
        f"Gap check at n0: (3/20)*n0 = {res['gap_at_n0']} >= 2 : PASS (holds for all n >= 14)",
        f"Case I exemption check at n0: v0 >= (3/20)*n0 = {res['v0_min_at_n0']} >= 38 : PASS (holds for all n >= 254)",
        f"Case I term alone upper bound at n0: {res['case1_only']}",
        f"  upper arf: {res['case1_only'].upper()}",
        f"Combined E[X_rigid] upper bound at n0: {res['e_x_rigid']}",
        f"  upper arf: {res['e_x_rigid'].upper()} (< 4.261e-11: PASS)",
        f"Disconnection bound (coarse 3/13): {res['disc_coarse']} (~{res['disc_coarse'].upper()})",
        f"Disconnection bound (tight e/(16-e)): {res['disc_tight']} (~{res['disc_tight'].upper()})",
        f"Total Pr(X_rigid > 0) + Pr(disconnected) [with 3/13]: {res['sum_coarse']} (< 1: PASS)",
        f"Total Pr(X_rigid > 0) + Pr(disconnected) [with e/(16-e)]: {res['sum_tight']} (< 1: PASS)",
        f"Logarithmic derivative upper bound 33/n0 - 1/1000: {res['log_deriv_upper']} (< 0 for all n >= n0: PASS)",
        "FINITE_CHECK: PASS",
    ]
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Clean-room 160-bit Arb verifier for Erdos #1182 repaired Case I."
    )
    parser.add_argument(
        "--cert",
        type=pathlib.Path,
        default=pathlib.Path("inputs/cert_case1.json.gz"),
        help="Path to Case I gzipped JSON certificate.",
    )
    parser.add_argument(
        "--inputs-dir",
        type=pathlib.Path,
        default=pathlib.Path("inputs"),
        help="Directory containing staged clean-room archives for SHA-256 lock check.",
    )
    parser.add_argument(
        "--skip-hash-locks",
        action="store_true",
        help="Skip staged inputs/ SHA-256 check (used when testing mutated temp certificates).",
    )
    parser.add_argument(
        "--fast-outer-only",
        action="store_true",
        help="Check tightened sliced-box superset H(B') only (skips secondary exact P_C(B) enumeration).",
    )
    parser.add_argument(
        "--finite-only",
        action="store_true",
        help="Run only the 160-bit Arb finite-n verification at n0=550,000.",
    )
    parser.add_argument(
        "--also-finite",
        action="store_true",
        help="Also run and print the 160-bit Arb finite-n verification at n0=550,000.",
    )
    args = parser.parse_args(argv)

    t0 = time.monotonic()
    try:
        if args.finite_only:
            fres = verify_finite_bound_arb(550000)
            print(format_finite_report(fres))
            return 0

        print(f"=== Erdos #1182 Clean-Room Case I Arb Verifier (flint {flint.__version__}, prec={ARB_PREC} bits) ===")
        if not args.skip_hash_locks:
            hashes = verify_hash_locks(args.inputs_dir)
            print("SHA-256 hash locks:")
            for name, digest in hashes.items():
                lock_note = " (LOCKED MATCH)" if name in EXPECTED_SHA256 else " (RECORDED CASE I)"
                print(f"  {name}: {digest}{lock_note}")

        cert_sha = sha256_file(args.cert)
        cert_obj = load_strict_gzip_json(args.cert)
        stats = verify_case1_certificate(
            cert_obj,
            check_exact_polytope=not args.fast_outer_only,
            collect_c_leaves=False,
        )
        elapsed = time.monotonic() - t0
        total_leaves = stats["n_leaves"] + stats["c_leaves"] + stats["x_leaves"]
        print(f"Certificate: {args.cert} (sha256={cert_sha})")
        print(f"Root domain: [0, 4001/10000]^5 (exact rational grid={cert_obj['grid']}, tilt_scale={cert_obj['tilt_scale']})")
        print(
            f"Tree summary: records={len(cert_obj['records'])}, splits={stats['splits']}, "
            f"leaves={total_leaves} (N={stats['n_leaves']}, C={stats['c_leaves']}, X={stats['x_leaves']})"
        )
        print(
            f"Occupancy leaves: {stats['c_leaves']} total, {stats['c_tail_active']} with active tail q_* < min(a0_max, a3_max), "
            f"outer sliced-box vertices checked={stats['outer_c_vertices']}"
        )
        print(
            f"Cutoff check q_* >= B_03: PASS on all {stats['c_leaves']}/{stats['c_leaves']} C leaves "
            f"(min (q_* - B_03) lower bound = {stats['min_q_minus_b03']})"
        )
        print(
            f"Max recomputed leaf bound [outer H(B')]: {stats['max_recomp_outer']} "
            f"(exact arf: {stats['max_recomp_outer']})"
        )
        print(
            f"  Max N leaf [outer H(B')]:      {stats['max_naive_outer']}"
        )
        print(
            f"  Max C near [outer H(B')]:      {stats['max_occ_near_outer']}"
        )
        print(
            f"  Max C KL-tail [outer H(B')]:   {stats['max_occ_tail_outer']}"
        )
        if not args.fast_outer_only:
            print(
                f"Max recomputed leaf bound [exact P_C(B), {stats['exact_c_vertices']} C vertices]: "
                f"{stats['max_recomp_exact']} (exact arf: {stats['max_recomp_exact']})"
            )
        print(
            f"Max leaf bound using stored U_t: {stats['max_storedU_bound']} (<= -0.001: PASS)"
        )
        print(f"Elapsed: {elapsed:.2f}s")
        print("CASE1_VERIFICATION: PASS")

        if args.also_finite:
            print()
            fres = verify_finite_bound_arb(550000)
            print(format_finite_report(fres))

        return 0
    except VerificationError as exc:
        print(f"CASE1_VERIFICATION: REJECTED — {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
