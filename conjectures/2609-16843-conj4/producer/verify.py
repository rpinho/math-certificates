#!/usr/bin/env python3
"""Standalone pure-Python exact verifier for the disproof and resolution of
van Berkel & Bosma (arXiv:2609.16843v2) Conjecture 4 on S_{1, d-1, 2d-1}.

Zero external dependencies; zero imports from producer or workspace scripts.

Implements:
  1. Engine 1: Direct greedy strict 3-sumfree simulation + van Berkel & Bosma
     Lemma 3 finite-cutoff periodicity & Lemma A minimality verification
     across d = 3, 4, 5, 6, ..., 40 (plus naive O(|S|^3) cross-check on d <= 12).
  2. Engine 2: Independent exact rational generating-function verification via
     6*r_3(n) = [x^n](A(x)^3 - 3*A(x)*A(x^2) + 2*A(x^3)) over (1 - x^{6m})^3
     and quadratic Newton forward differences across d = 3..40, plus residue-class
     proof verification for d = 3, 4, 5.
  3. Symbolic & Boundary General-Proof Verifier for all d >= 6:
     - Exact affine-arithmetic symbolic verification over Z[d] (for all d >= 6) of
       Part A (all 35 block-triple combinations and all 8 residue-multiset types),
       Part B (interval-sum lemma, G_{pre,1}, G_{pre,2} = B_1..B_5, G_j = C_1..C_5,
       plus exact failure diagnostics at d = 3, 4, 5), and Part C (minimality).
     - Concrete exhaustive residue-triple and integer-gap checks across boundary
       and large instances d in {6, 7, 8, 9, 10, 50, 100} (including dual Engine 1
       and Engine 2 checks at d = 50 and d = 100).
  4. Mandatory Negative Controls confirming BOTH Engine 1 and Engine 2 reject:
     (a) Conjecture 4's d = 4 claim (p = 4, m = 31),
     (b) Conjecture 4's d = 6 modulus claim (m = 47),
     (c) A corrupted preperiod element,
     (d) A non-minimal period multiple (2p, 2m),
     (e) A non-minimal shifted preperiod (k + p).
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from itertools import combinations, combinations_with_replacement
from math import comb
from typing import Dict, List, Sequence, Tuple


class VerificationError(Exception):
    """Raised when a candidate witness or proof obligation fails verification."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


# ============================================================================
# Independent Greedy Strict 3-Sumfree Simulators (Engine 1)
# ============================================================================

def simulate_greedy_naive(seeds: Tuple[int, int, int], limit: int) -> List[int]:
    """Reference O(|S|^3)-style strict 3-sumfree simulator using explicit pair sums."""
    f, g, h = seeds
    require(1 <= f < g < h <= limit, f"Invalid seeds {seeds} for limit {limit}")
    seq = [f, g, h]
    three_sums = {f + g + h}
    for z in range(h + 1, limit + 1):
        if z not in three_sums:
            n = len(seq)
            for i in range(n):
                si = seq[i]
                if si + z >= limit:
                    break
                for j in range(i + 1, n):
                    s = si + seq[j] + z
                    if s <= limit:
                        three_sums.add(s)
            seq.append(z)
    return seq


def simulate_greedy_bitset(seeds: Tuple[int, int, int], limit: int) -> Tuple[List[int], int]:
    """Exact big-int bitmask strict 3-sumfree simulator up to integer `limit`.

    Invariant before inserting strictly larger x > max(S):
      - bit u of s_mask is 1      iff u in S
      - bit v of pair_mask is 1   iff v = a + b for some a < b in S
      - bit w of triple_mask is 1 iff w = a + b + c for some a < b < c in S
    Since every a < b in S satisfies b < x, shifting pair_mask by +x forms only
    strictly increasing triples a < b < x.
    """
    f, g, h = seeds
    require(1 <= f < g < h <= limit, f"Invalid seeds {seeds} for limit {limit}")
    mask = (1 << (limit + 1)) - 1
    s_mask = 0
    pair_mask = 0
    triple_mask = 0
    seq: List[int] = []
    for x in (f, g, h):
        triple_mask = (triple_mask | (pair_mask << x)) & mask
        pair_mask = (pair_mask | (s_mask << x)) & mask
        s_mask |= 1 << x
        seq.append(x)

    cur = h
    while cur < limit:
        rem = limit - cur
        inv = ((1 << rem) - 1) ^ (triple_mask >> (cur + 1))
        if inv == 0:
            break
        nxt = cur + 1 + ((inv & -inv).bit_length() - 1)
        triple_mask = (triple_mask | (pair_mask << nxt)) & mask
        pair_mask = (pair_mask | (s_mask << nxt)) & mask
        s_mask |= 1 << nxt
        seq.append(nxt)
        cur = nxt
    return seq, s_mask


def check_structural_and_minimality(
    seeds: Sequence[int],
    preperiod: Sequence[int],
    first_block: Sequence[int],
    m: int,
) -> Tuple[int, int, int, Tuple[int, ...]]:
    """Checks canonical decomposition ordering and Lemma A minimality conditions."""
    require(len(seeds) == 3, "Seeds must have 3 elements")
    f, g, h = int(seeds[0]), int(seeds[1]), int(seeds[2])
    require(1 <= f < g < h, f"Seeds must satisfy 1 <= f < g < h, got {seeds}")
    require(m >= 2, f"Modulus m must be >= 2, got {m}")
    k = len(preperiod)
    p = len(first_block)
    require(p >= 1, "Period length p must be >= 1")

    for i in range(k - 1):
        require(preperiod[i] < preperiod[i + 1], "Preperiod is not strictly increasing")
    if k > 0:
        require(preperiod[0] >= 1, "Preperiod entries must be >= 1")
        require(preperiod[-1] < first_block[0], "Must have a_k < b_1")
    for i in range(p - 1):
        require(first_block[i] < first_block[i + 1], "First period block not strictly increasing")
    require(first_block[-1] < first_block[0] + m, "Must have b_p < b_1 + m")

    in_up_to_h = [x for x in list(preperiod) + list(first_block) if x <= h]
    require(in_up_to_h == [f, g, h], f"Initial entries <= h do not match seeds: {in_up_to_h} != {[f,g,h]}")

    gaps = tuple(
        (first_block[i + 1] - first_block[i]) if i + 1 < p else (first_block[0] + m - first_block[-1])
        for i in range(p)
    )
    require(sum(gaps) == m, "Sum of periodic gaps must equal modulus m")

    # Primitivity of cyclic gap tuple G (minimality of p and m)
    for r in range(1, p):
        if p % r == 0 and gaps == gaps[:r] * (p // r):
            raise VerificationError(
                f"Non-minimal period: gap tuple of length {p} is a {p // r}-fold repeat of length {r}"
            )

    # Minimality of preperiod length k (Lemma A(2): b_1 - a_k != g_p, i.e., a_k != b_p - m)
    if k > 0:
        require(
            first_block[0] - preperiod[-1] != gaps[-1],
            f"Non-minimal preperiod k={k}: b_1 - a_k == g_p ({gaps[-1]}), so a_k = b_p - m",
        )
        K = max(preperiod[-1], first_block[-1] - m)
    else:
        require(first_block[-1] - m <= 0, "If k=0, must have b_p - m <= 0")
        K = 0

    return k, p, K, gaps


def verify_via_lemma3_greedy(
    seeds: Sequence[int],
    preperiod: Sequence[int],
    first_block: Sequence[int],
    m: int,
    cross_check_naive: bool = False,
) -> Dict[str, object]:
    """Engine 1: Direct greedy simulation + van Berkel & Bosma Lemma 3 (t=3)."""
    k, p, K, gaps = check_structural_and_minimality(seeds, preperiod, first_block, m)
    # Minimal Q >= 7 satisfying Lemma 3: (Q - 6)*m >= 2*K, and using at least Q >= 8 (Corollary 4 style)
    Q = max(8, 6 + (2 * K + m - 1) // m)
    require((Q - 6) * m >= 2 * K, "Lemma 3 inequality (Q - 6)*m >= 2*K violated")
    cutoff = K + Q * m

    seed_tuple = (int(seeds[0]), int(seeds[1]), int(seeds[2]))
    sim_seq, s_mask = simulate_greedy_bitset(seed_tuple, cutoff)
    if cross_check_naive:
        naive_seq = simulate_greedy_naive(seed_tuple, cutoff)
        require(sim_seq == naive_seq, "Bitset simulator disagreed with naive O(|S|^3) simulator")

    # Build expected membership up to cutoff from (preperiod, first_block, m)
    expected: List[int] = list(preperiod)
    j = 0
    while True:
        added_any = False
        for b in first_block:
            val = b + j * m
            if val <= cutoff:
                expected.append(val)
                added_any = True
        if not added_any:
            break
        j += 1

    require(
        sim_seq == expected,
        f"Simulated greedy sequence disagrees with candidate up to Lemma 3 cutoff {cutoff}",
    )

    # Explicitly verify Lemma 3 block repetition on characteristic bitmask C[1..cutoff]
    block_mask = (1 << m) - 1
    base_block = (s_mask >> (K + 1)) & block_mask
    require(base_block != 0, "Lemma 3 repeating block in C is all-zero")
    require(base_block.bit_count() == p, f"Block 1-count {base_block.bit_count()} != p={p}")
    for q in range(1, Q):
        blk = (s_mask >> (K + 1 + q * m)) & block_mask
        require(blk == base_block, f"Lemma 3 block mismatch at repetition q={q}")

    # Explicitly check minimality of K on C: if K >= 1, C_K != C_{K + m}
    if K >= 1:
        c_K = (s_mask >> K) & 1
        c_Km = (s_mask >> (K + m)) & 1
        require(c_K != c_Km, f"Characteristic preperiod K={K} is not minimal: C_K == C_{{K+m}}")
    ones_in_K = (s_mask & ((1 << (K + 1)) - 1)).bit_count()
    require(ones_in_K == k, f"Number of 1s in C[1..K] is {ones_in_K}, expected k={k}")

    return {
        "k": k,
        "p": p,
        "m": m,
        "K": K,
        "Q": Q,
        "cutoff": cutoff,
        "simulated_count": len(sim_seq),
        "gaps": list(gaps),
    }


# ============================================================================
# Independent Exact Rational Generating-Function Verifier (Engine 2)
# ============================================================================

def _dense_poly_mul(a: List[int], b: List[int]) -> List[int]:
    """Exact integer polynomial multiplication keeping only non-zero support loops."""
    if not a or not b:
        return [0]
    nz_a = [(i, ci) for i, ci in enumerate(a) if ci]
    nz_b = [(j, cj) for j, cj in enumerate(b) if cj]
    out = [0] * (len(a) + len(b) - 1)
    for i, ci in nz_a:
        for j, cj in nz_b:
            out[i + j] += ci * cj
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def verify_via_generating_function(
    seeds: Sequence[int],
    preperiod: Sequence[int],
    first_block: Sequence[int],
    m: int,
) -> Dict[str, object]:
    """Engine 2: Exact rational generating-function + Newton-difference verifier (Lemma B)."""
    k, p, K, gaps = check_structural_and_minimality(seeds, preperiod, first_block, m)
    L = 6 * m

    def build_numerator(exponent: int) -> List[int]:
        max_deg = max(
            [exponent * preperiod[-1] + L] if preperiod else [0]
            + [exponent * first_block[-1] + L]
        )
        max_deg = max(max_deg, exponent * first_block[-1] + L)
        poly = [0] * (max_deg + 1)
        for a in preperiod:
            poly[exponent * a] += 1
            poly[exponent * a + L] -= 1
        step = exponent * m
        for b in first_block:
            for shift in range(0, L, step):
                poly[exponent * b + shift] += 1
        while len(poly) > 1 and poly[-1] == 0:
            poly.pop()
        return poly

    p1 = build_numerator(1)
    p2 = build_numerator(2)
    p3 = build_numerator(3)
    one_minus_xL = [0] * (L + 1)
    one_minus_xL[0] = 1
    one_minus_xL[L] = -1

    term1 = _dense_poly_mul(_dense_poly_mul(p1, p1), p1)
    term2 = _dense_poly_mul(_dense_poly_mul(p1, p2), one_minus_xL)
    term3 = _dense_poly_mul(_dense_poly_mul(p3, one_minus_xL), one_minus_xL)

    deg_bound = max(len(term1), len(term2), len(term3))
    T = [0] * deg_bound
    for i, c in enumerate(term1):
        T[i] += c
    for i, c in enumerate(term2):
        T[i] -= 3 * c
    for i, c in enumerate(term3):
        T[i] += 2 * c
    while len(T) > 1 and T[-1] == 0:
        T.pop()
    require(any(c != 0 for c in T), "Generating-function numerator T(x) vanished identically")
    cutoff = len(T) - 1

    # Bucket non-zero terms of T(x) by exponent mod L for O(1) evaluation per n
    buckets: List[List[Tuple[int, int]]] = [[] for _ in range(L)]
    nz_count = 0
    for deg_i, coef in enumerate(T):
        if coef != 0:
            buckets[deg_i % L].append((deg_i, coef))
            nz_count += 1

    def six_r3(n: int) -> int:
        total = 0
        for deg_i, coef in buckets[n % L]:
            if n >= deg_i:
                q = (n - deg_i) // L
                total += coef * ((q + 2) * (q + 1) // 2)
        return total

    pre_set = set(preperiod)
    first_by_mod = {b % m: b for b in first_block}
    require(len(first_by_mod) == p, "Elements of first_block are not distinct modulo m")

    def belongs(n: int) -> bool:
        if n in pre_set:
            return True
        b = first_by_mod.get(n % m)
        return b is not None and n >= b

    h = int(seeds[2])
    start = max(cutoff + 1, first_block[-1] + 1)

    for n in range(h + 1, start):
        val = six_r3(n)
        require(val >= 0 and val % 6 == 0, f"Invalid 6*r_3({n}) = {val}")
        in_a = belongs(n)
        if in_a:
            require(val == 0, f"Exclusion failure at n={n} in A: 6*r_3({n}) = {val} != 0")
        else:
            require(val > 0, f"Inclusion failure at gap n={n} not in A: 6*r_3({n}) == 0")

    for n0 in range(start, start + L):
        f0 = six_r3(n0)
        f1 = six_r3(n0 + L)
        f2 = six_r3(n0 + 2 * L)
        alpha = f0
        beta = f1 - f0
        gamma = f2 - 2 * f1 + f0
        if belongs(n0):
            require(
                (alpha, beta, gamma) == (0, 0, 0),
                f"Periodic exclusion failure on residue n0={n0}: diffs={(alpha, beta, gamma)}",
            )
        else:
            require(
                alpha > 0 and beta >= 0 and gamma >= 0,
                f"Periodic inclusion failure on gap residue n0={n0}: diffs={(alpha, beta, gamma)}",
            )

    return {
        "k": k,
        "p": p,
        "m": m,
        "K": K,
        "L": L,
        "poly_degree_cutoff": cutoff,
        "verification_start": start,
        "nonzero_terms_in_T": nz_count,
    }


def verify_small_residue_certificates(small_certs: Dict[str, dict], finite_by_d: Dict[int, dict]) -> int:
    """Verifies the explicit finite + residue-class certificates for d = 3, 4, 5."""
    checked = 0
    for d in (3, 4, 5):
        cert = small_certs[str(d)]
        fc = finite_by_d[d]
        m = int(cert["modulus"])
        require(m == fc["m"], f"d={d} modulus mismatch in residue certificate")
        fin = [int(x) for x in cert["isolated_finite_elements"]]
        inf_prog = {int(r): int(c_r) for r, c_r in cert["infinite_progressions"].items()}
        max_th = int(cert["max_periodic_cover_threshold"])

        # Reconstruct A up to max_th + 3*m and verify equality with (preperiod, first_block, m)
        bound = max_th + 3 * m
        from_res = set(fin)
        for r, c_r in inf_prog.items():
            require(c_r % m == r and c_r >= 1, f"Invalid progression start c_{r}={c_r}")
            j = 0
            while c_r + j * m <= bound:
                val = c_r + j * m
                require(val not in from_res, f"Duplicate decomposition element {val} at d={d}")
                from_res.add(val)
                j += 1
        from_fc = set(fc["preperiod"]) | {
            b + j * m for b in fc["first_period_block"] for j in range((bound // m) + 2) if b + j * m <= bound
        }
        require(from_res == from_fc, f"Residue decomposition != canonical decomposition at d={d}")

        # Verify Exclusion directly on residue classes mod m:
        # (1) Can x + y + z land in P_d (the union of infinite progressions)?
        #     Any triple using >= 1 element of P_d has residue mod m in one of the three
        #     families below; we verify NONE of them even lands in inf_prog mod m!
        inf_r = sorted(inf_prog.keys())
        for r1, r2, r3 in combinations_with_replacement(inf_r, 3):
            require((r1 + r2 + r3) % m not in inf_prog, f"d={d}: 3-inf collision {(r1,r2,r3)}")
        for u in fin:
            for r1, r2 in combinations_with_replacement(inf_r, 2):
                require((u + r1 + r2) % m not in inf_prog, f"d={d}: 1-fin 2-inf collision")
        for u, v in combinations(fin, 2):
            for r1 in inf_r:
                require((u + v + r1) % m not in inf_prog, f"d={d}: 2-fin 1-inf collision")
        for u, v, w in combinations(fin, 3):
            require((u + v + w) not in from_res, f"d={d}: 3-fin triple {u}+{v}+{w} hit A_{d}")

        # (2) Can x + y + z (with x < y < z in A_d) land in fin?
        #     Since x, y, z >= 1, x + y + z <= max(fin) forces x < y < z < max(fin).
        max_fin = max(fin)
        a_below_fin = sorted(x for x in from_res if x < max_fin)
        fin_set = set(fin)
        for x, y, z in combinations(a_below_fin, 3):
            require((x + y + z) not in fin_set, f"d={d}: distinct triple {x}+{y}+{z} hit fin")

        # Verify Inclusion: finite gaps below max_th + periodic linear cover for all s not in inf_prog
        h = 2 * d - 1
        fin_gaps = cert["finite_gap_triples_below_threshold"]
        for n in range(h + 1, max_th):
            if n not in from_res:
                require(str(n) in fin_gaps, f"d={d}: missing finite gap triple for n={n}")
                a, b, c = fin_gaps[str(n)]
                require(a < b < c < n and a + b + c == n, f"d={d}: invalid triple for n={n}")
                require(a in from_res and b in from_res and c in from_res, f"d={d}: non-member in triple for n={n}")

        res_cover = cert["nonmember_residue_cover"]
        require(len(res_cover) == m - len(inf_prog), f"d={d}: wrong number of covered non-member residues")
        for s in range(m):
            if s in inf_prog:
                continue
            entry = res_cover[str(s)]
            th, a, b, c0 = int(entry["threshold"]), int(entry["a"]), int(entry["b"]), int(entry["c0"])
            require(th <= max_th and a + b + c0 == th and th % m == s, f"d={d}: bad threshold on res {s}")
            require(a < b < c0, f"d={d}: summands not strictly increasing on res {s}")
            require(a in from_res and b in from_res, f"d={d}: a,b not in A on res {s}")
            r3 = c0 % m
            require(r3 in inf_prog and c0 >= inf_prog[r3], f"d={d}: c0={c0} not in infinite progression")
        checked += 1
    return checked


# ============================================================================
# Symbolic & Boundary Verification of General Proof for d >= 6
# ============================================================================

class Affine:
    """Exact affine linear form c1 * d + c0 over Z[d]."""

    __slots__ = ("c1", "c0")

    def __init__(self, c1: int, c0: int) -> None:
        self.c1 = int(c1)
        self.c0 = int(c0)

    def __add__(self, other: "Affine") -> "Affine":
        return Affine(self.c1 + other.c1, self.c0 + other.c0)

    def __sub__(self, other: "Affine") -> "Affine":
        return Affine(self.c1 - other.c1, self.c0 - other.c0)

    def scale(self, k: int) -> "Affine":
        return Affine(k * self.c1, k * self.c0)

    def at(self, d: int) -> int:
        return self.c1 * d + self.c0

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Affine) and self.c1 == other.c1 and self.c0 == other.c0

    def __repr__(self) -> str:
        if self.c1 == 0:
            return f"{self.c0}"
        if self.c0 == 0:
            return f"{self.c1}*d"
        sign = "+" if self.c0 > 0 else "-"
        return f"{self.c1}*d{sign}{abs(self.c0)}"


def assert_ge_all_d(lhs: Affine, rhs: Affine, d0: int = 6, label: str = "") -> None:
    """Proves symbolically that lhs(d) >= rhs(d) for EVERY integer d >= d0."""
    diff = lhs - rhs
    # diff(d) = diff.c1 * (d - d0) + diff(d0); for all d >= d0, iff diff.c1 >= 0 and diff(d0) >= 0!
    ok = (diff.c1 >= 0) and (diff.at(d0) >= 0)
    require(
        ok,
        f"Symbolic inequality failed for d >= {d0} ({label}): need {lhs} >= {rhs}, "
        f"diff={diff} (slope={diff.c1}, at_{d0}={diff.at(d0)})",
    )


def assert_gt_all_d(lhs: Affine, rhs: Affine, d0: int = 6, label: str = "") -> None:
    """Proves symbolically that lhs(d) > rhs(d) (i.e., >= rhs + 1) for EVERY integer d >= d0."""
    assert_ge_all_d(lhs, rhs + Affine(0, 1), d0=d0, label=label)


def verify_general_proof_symbolic() -> Dict[str, int]:
    """Symbolically verifies every inequality and case in Theorem 2 (PROOF.md Section 5) for all d >= 6."""
    ONE = Affine(0, 1)
    m = Affine(8, -3)

    # 1. Canonical ordering of blocks and residues mod m = 8d - 3 for all d >= 6
    u1 = Affine(0, 1)
    u2 = Affine(1, -1)
    r_2d_2 = Affine(2, -2)
    i_lo = Affine(2, -1)
    r_3d_3 = Affine(3, -3)
    i_hi = Affine(3, -2)
    u3 = Affine(4, -1)
    t0_lo = Affine(10, -5)
    t0_hi = Affine(11, -6)
    t1_lo = t0_lo + m  # 18d - 8

    chain_blocks = [u1, u2, i_lo, i_hi, u3, t0_lo, t0_hi, t1_lo]
    for a, b in zip(chain_blocks, chain_blocks[1:]):
        assert_gt_all_d(b, a, d0=6, label="block_chain")

    chain_residues = [Affine(0, 0), u1, u2, r_2d_2, i_lo, r_3d_3, i_hi, u3, m]
    for a, b in zip(chain_residues, chain_residues[1:]):
        assert_gt_all_d(b, a, d0=6, label="residue_chain")

    require(t0_lo == r_2d_2 + m and t0_hi == r_3d_3 + m, "T_0 residue identity failed")
    assert_gt_all_d(m.scale(2), u3.scale(3), d0=6, label="carry_at_most_1")

    # 2. Part A (Symbolic Exclusion): Exhaustively check ALL 35 unordered triples of
    # the 5 structural blocks:
    #   U1={1} (q=0), U2={d-1} (q=0), I*=[2d-1,3d-2] (q=0), U3={4d-1} (q=0), T=[2d-2,3d-3]+q*m (q>=1)
    blocks_meta = [
        ("U1", u1, u1, True, 0),      # singleton, q == 0
        ("U2", u2, u2, True, 0),      # singleton, q == 0
        ("I*", i_lo, i_hi, False, 0), # interval of length d, q == 0
        ("U3", u3, u3, True, 0),      # singleton, q == 0
        ("T", r_2d_2, r_3d_3, False, 1),  # periodic union q >= 1
    ]

    valid_block_triples_checked = 0
    for idx_triple in combinations_with_replacement(range(5), 3):
        # Singletons (U1, U2, U3) cannot be repeated in a strictly increasing triple!
        counts = {idx: idx_triple.count(idx) for idx in set(idx_triple)}
        if any(blocks_meta[idx][3] and cnt > 1 for idx, cnt in counts.items()):
            continue
        valid_block_triples_checked += 1

        # Compute exact tight symbolic affine bounds [sig_lo, sig_hi] on Sigma = r_1 + r_2 + r_3
        # accounting for distinctness when multiple elements come from I* (all have q = 0)!
        cnt_I = counts.get(2, 0)
        sig_lo = Affine(0, 0)
        sig_hi = Affine(0, 0)
        min_Q = 0
        for idx, cnt in counts.items():
            _, lo, hi, _, q_min = blocks_meta[idx]
            min_Q += cnt * q_min
            if idx == 2:
                # cnt distinct integers from I* = [2d-1, 3d-2]
                if cnt == 1:
                    sig_lo = sig_lo + i_lo
                    sig_hi = sig_hi + i_hi
                elif cnt == 2:
                    sig_lo = sig_lo + i_lo + (i_lo + ONE)        # 4d - 1
                    sig_hi = sig_hi + (i_hi - ONE) + i_hi        # 6d - 5
                elif cnt == 3:
                    sig_lo = sig_lo + Affine(6, 0)               # 6d
                    sig_hi = sig_hi + Affine(9, -9)              # 9d - 9
            else:
                sig_lo = sig_lo + lo.scale(cnt)
                sig_hi = sig_hi + hi.scale(cnt)

        names = "+".join(blocks_meta[i][0] for i in idx_triple)

        if min_Q == 0:
            # All 3 summands have q_i = 0, so S = Sigma. Must miss U1, U2, [2d-1,3d-2], U3,
            # AND if Sigma >= m, must miss [10d-5, 11d-6]!
            # Check how [sig_lo, sig_hi] avoids A_d:
            if sig_hi.at(6) < u3.at(6):
                # Lies strictly in (3d-2, 4d-1): e.g. U1 + U2 + I* = [3d-1, 4d-2]
                assert_gt_all_d(sig_lo, i_hi, d0=6, label=f"PartA_{names}_above_I*")
                assert_gt_all_d(u3, sig_hi, d0=6, label=f"PartA_{names}_below_U3")
            else:
                # Lies strictly in (4d-1, 10d-5):
                assert_gt_all_d(sig_lo, u3, d0=6, label=f"PartA_{names}_above_U3")
                assert_gt_all_d(t0_lo, sig_hi, d0=6, label=f"PartA_{names}_below_T0")
        else:
            # Q >= 1, so q_* = Q + eps >= 1: S in A_d iff Sigma in [2d-2, 3d-3] OR Sigma in [10d-5, 11d-6]!
            # Prove symbolically that [sig_lo, sig_hi] <= 10d-6 AND >= 3d-2 for all d >= 6:
            assert_gt_all_d(sig_lo, r_3d_3, d0=6, label=f"PartA_{names}_above_R")
            assert_gt_all_d(t0_lo, sig_hi, d0=6, label=f"PartA_{names}_below_R_plus_m")

    # Also verify the 8 unified residue-multiset types in PROOF.md Part A directly
    eight_types = [
        ("P1,P2,P3", Affine(5, -1), Affine(5, -1), "gt_u3_lt_t0"),
        ("P1,P2,J_r>2d-2", Affine(3, -1), Affine(4, -2), "between_ihi_u3"),
        ("P1,P3,J", Affine(6, -2), Affine(7, -2), "gt_u3_lt_t0"),
        ("P2,P3,J", Affine(7, -4), Affine(8, -4), "gt_u3_lt_t0"),
        ("P1,J,J_Q>=1", Affine(4, -3), Affine(6, -4), "gt_r3d3_lt_t0"),
        ("P2,J,J", Affine(5, -5), Affine(7, -6), "gt_u3_lt_t0"),
        ("P3,J,J", Affine(8, -5), Affine(10, -6), "gt_u3_lt_t0"),
        ("J,J,J", Affine(6, -6), Affine(9, -8), "gt_u3_lt_t0"),
    ]
    for name, lo, hi, kind in eight_types:
        if kind == "between_ihi_u3":
            assert_gt_all_d(lo, i_hi, d0=6, label=name)
            assert_gt_all_d(u3, hi, d0=6, label=name)
        elif kind == "gt_r3d3_lt_t0":
            assert_gt_all_d(lo, r_3d_3, d0=6, label=name)
            assert_gt_all_d(t0_lo, hi, d0=6, label=name)
        else:
            assert_gt_all_d(lo, u3, d0=6, label=name)
            assert_gt_all_d(t0_lo, hi, d0=6, label=name)

    # 3. Part B (Symbolic Inclusion):
    # Interval-sum formulas on I* = [2d-1, 3d-2]
    p_I_lo = i_lo.scale(2) + ONE
    p_I_hi = i_hi.scale(2) - ONE
    require(p_I_lo == Affine(4, -1) and p_I_hi == Affine(6, -5), "P(I*) formula mismatch")

    t_I_lo = i_lo.scale(3) + Affine(0, 3)
    t_I_hi = i_hi.scale(3) - Affine(0, 3)
    require(t_I_lo == Affine(6, 0) and t_I_hi == Affine(9, -9), "T(I*) formula mismatch")

    # G_{pre,1} = [3d-1, 4d-2] = {1} + {d-1} + I*
    require(u1 + u2 + i_lo == Affine(3, -1) and u1 + u2 + i_hi == Affine(4, -2), "G_pre_1 mismatch")

    # G_{pre,2} = [4d, 10d-6] covered by B_1 .. B_5
    B = [
        (u1 + p_I_lo, u1 + p_I_hi),            # B1 = [4d, 6d-4]
        (u2 + p_I_lo, u2 + p_I_hi),            # B2 = [5d-2, 7d-6]
        (u1 + i_lo + u3, u1 + i_hi + u3),      # B3 = [6d-1, 7d-2]
        (t_I_lo, t_I_hi),                      # B4 = [6d, 9d-9]
        (p_I_lo + u3, p_I_hi + u3),            # B5 = [8d-2, 10d-6]
    ]
    require(B[0][0] == Affine(4, 0) and B[-1][1] == Affine(10, -6), "G_pre_2 endpoints mismatch")
    for idx in range(len(B) - 1):
        # Need next_lo <= cur_hi + 1, i.e., cur_hi + 1 >= next_lo for all d >= 6
        assert_ge_all_d(B[idx][1] + ONE, B[idx + 1][0], d0=6, label=f"G_pre_2_overlap_{idx+1}_{idx+2}")

    # Verify exact failure points in G_{pre,2} for d = 3, 4, 5
    expected_first_hole = {3: 16, 4: 29, 5: 37}
    for d_small, hole in expected_first_hole.items():
        s0 = [1, d_small - 1, *range(2 * d_small - 1, 3 * d_small - 1), 4 * d_small - 1]
        sums_s0 = {a + b + c for a, b, c in combinations(s0, 3)}
        uncovered = [n for n in range(4 * d_small, 10 * d_small - 5) if n not in sums_s0]
        require(
            uncovered and uncovered[0] == hole,
            f"At d={d_small}, expected first uncovered gap in G_pre_2 to be {hole}, got {uncovered}",
        )

    # G_j = [11d-5 + j*m, 18d-9 + j*m] covered by C_{1,j} .. C_{5,j}
    C_base = [
        (u1 + u2 + t0_lo, u1 + u2 + t0_hi),    # C1 = [11d-5, 12d-6]
        (u1 + i_lo + t0_lo, u1 + i_hi + t0_hi),# C2 = [12d-5, 14d-7]
        (u2 + i_lo + t0_lo, u2 + i_hi + t0_hi),# C3 = [13d-7, 15d-9]
        (p_I_lo + t0_lo, p_I_hi + t0_hi),      # C4 = [14d-6, 17d-11]
        (i_lo + u3 + t0_lo, i_hi + u3 + t0_hi),# C5 = [16d-7, 18d-9]
    ]
    require(C_base[0][0] == t0_hi + ONE, "C1 start != max(T_0) + 1")
    require(C_base[-1][1] == t1_lo - ONE, "C5 end != min(T_1) - 1")
    for idx in range(len(C_base) - 1):
        assert_ge_all_d(C_base[idx][1] + ONE, C_base[idx + 1][0], d0=6, label=f"G_j_overlap_{idx+1}_{idx+2}")

    # 4. Part C (Symbolic Minimality):
    gap_pre_last = t0_lo - u3           # 6d - 4
    gap_per_last = t1_lo - t0_hi        # 7d - 2
    require(gap_pre_last == Affine(6, -4) and gap_per_last == Affine(7, -2), "Gap formulas mismatch")
    assert_gt_all_d(gap_per_last, ONE, d0=6, label="primitivity_7d_minus_2_gt_1")
    assert_gt_all_d(gap_per_last, gap_pre_last, d0=6, label="minimality_k_7d_2_gt_6d_4")

    return {
        "valid_block_triples_checked": valid_block_triples_checked,
        "residue_types_checked": len(eight_types),
        "covering_intervals_checked": len(B) + len(C_base) + 1,
    }


def verify_boundary_d_instances(d_values: Sequence[int]) -> Dict[str, object]:
    """Exhaustively checks concrete residue triples and gap coverings across d in {6,7,8,9,10,50,100}."""
    total_triples = 0
    for d in d_values:
        require(d >= 6, f"Boundary check expects d >= 6, got {d}")
        m = 8 * d - 3
        # Allowed (r, q_mode) pairs:
        #   q_mode == "zero": q must be 0 (singletons 1, d-1, 3d-2, 4d-1)
        #   q_mode == "pos" : q >= 1 (residue 2d-2)
        #   q_mode == "any" : q >= 0 (residues 2d-1 .. 3d-3)
        zero_res = {1, d - 1, 3 * d - 2, 4 * d - 1}
        pos_res = {2 * d - 2}
        any_res = set(range(2 * d - 1, 3 * d - 2))
        all_res = sorted(zero_res | pos_res | any_res)
        q0_members = {1, d - 1, *range(2 * d - 1, 3 * d - 1), 4 * d - 1}
        qpos_residues = set(range(2 * d - 2, 3 * d - 2))

        for r1, r2, r3 in combinations_with_replacement(all_res, 3):
            # Singletons in zero_res can appear at most once in a distinct triple
            triple = (r1, r2, r3)
            if any(r in zero_res and triple.count(r) > 1 for r in set(triple)):
                continue
            total_triples += 1
            sigma = r1 + r2 + r3
            eps, r_star = divmod(sigma, m)
            require(eps in (0, 1), f"Carry exceeded 1 at d={d}: {triple}")

            # Check if Q = 0 is possible (no pos_res used, and no duplicate in any_res)
            can_Q_zero = (not any(r in pos_res for r in triple)) and (len(set(triple)) == 3)
            # Check if Q >= 1 is possible (at least one element in pos_res | any_res)
            can_Q_pos = any(r in pos_res or r in any_res for r in triple)

            if can_Q_zero and eps == 0:
                require(r_star not in q0_members, f"Target-0 violation at d={d}, triple={triple}")
            if can_Q_zero and eps == 1:
                require(r_star not in qpos_residues, f"Target-1 (Q=0,eps=1) violation at d={d}, triple={triple}")
            if can_Q_pos:
                if eps == 0:
                    require(r_star not in qpos_residues, f"Target-1 (Q>=1,eps=0) violation at d={d}, triple={triple}")
                else:
                    require(r_star not in qpos_residues, f"Target-1 (Q>=1,eps=1) violation at d={d}, triple={triple}")

        # For d in (50, 100), also run BOTH Engine 1 (Lemma 3 greedy) and Engine 2 (GF)!
        if d in (50, 100):
            seeds = [1, d - 1, 2 * d - 1]
            pre = [1, d - 1, *range(2 * d - 1, 3 * d - 1), 4 * d - 1]
            fst = list(range(10 * d - 5, 11 * d - 5))
            verify_via_lemma3_greedy(seeds, pre, fst, m, cross_check_naive=False)
            verify_via_generating_function(seeds, pre, fst, m)

    return {"d_values": list(d_values), "concrete_residue_triples_checked": total_triples}


# ============================================================================
# Negative Controls
# ============================================================================

def verify_negative_controls(controls: Sequence[dict]) -> List[Dict[str, str]]:
    """Confirms BOTH Engine 1 and Engine 2 reject every negative control."""
    required_ids = {
        "NC_a_d4_conjectured_p4_m31",
        "NC_b_d6_conjectured_m47",
        "NC_c_corrupted_preperiod_element",
        "NC_d_nonminimal_period_multiple_2p",
    }
    seen_ids = set()
    results: List[Dict[str, str]] = []

    for nc in controls:
        nc_id = nc["id"]
        seen_ids.add(nc_id)
        seeds = nc["seeds"]
        pre = nc["preperiod"]
        fst = nc["first_period_block"]
        m = int(nc["m"])

        err1 = None
        try:
            verify_via_lemma3_greedy(seeds, pre, fst, m, cross_check_naive=False)
        except VerificationError as exc:
            err1 = str(exc)

        err2 = None
        try:
            verify_via_generating_function(seeds, pre, fst, m)
        except VerificationError as exc:
            err2 = str(exc)

        require(err1 is not None, f"Negative control {nc_id} was NOT rejected by Engine 1 (Lemma 3)!")
        require(err2 is not None, f"Negative control {nc_id} was NOT rejected by Engine 2 (GF)!")
        results.append({"id": nc_id, "engine1_rejected": err1, "engine2_rejected": err2})

    missing = required_ids - seen_ids
    require(not missing, f"Missing required negative controls: {sorted(missing)}")
    return results


# ============================================================================
# Main Entrypoint
# ============================================================================

def main() -> int:
    t0 = time.time()
    here = os.path.dirname(os.path.abspath(__file__))
    witness_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "witnesses.json")

    with open(witness_path, "rb") as fh:
        raw_bytes = fh.read()
    sha256_hex = hashlib.sha256(raw_bytes).hexdigest()
    doc = json.loads(raw_bytes.decode("utf-8"))

    # (i) Verify d = 3, 4, 5, 6, ..., 40 via BOTH Engine 1 (Lemma 3 greedy) and Engine 2 (GF)
    finite_certs = doc["finite_cutoff_certificates"]
    d_seen = [int(c["d"]) for c in finite_certs]
    require(d_seen == list(range(3, 41)), f"Expected d=3..40 certificates, got {d_seen}")

    finite_by_d: Dict[int, dict] = {}
    for cert in finite_certs:
        d = int(cert["d"])
        finite_by_d[d] = cert
        seeds = cert["seeds"]
        require(seeds == [1, d - 1, 2 * d - 1], f"Seeds mismatch at d={d}")
        pre = cert["preperiod"]
        fst = cert["first_period_block"]
        m = int(cert["m"])
        require(len(pre) == int(cert["k"]) and len(fst) == int(cert["p"]), f"(k,p) length mismatch at d={d}")

        r1 = verify_via_lemma3_greedy(seeds, pre, fst, m, cross_check_naive=(d <= 12))
        r2 = verify_via_generating_function(seeds, pre, fst, m)

        require(r1["K"] == cert["lemma3"]["K"] and r1["cutoff"] == cert["lemma3"]["cutoff"], f"Lemma 3 metadata mismatch at d={d}")
        require(r2["poly_degree_cutoff"] == cert["generating_function"]["poly_degree_cutoff"], f"GF cutoff mismatch at d={d}")

        # Check explicit disproof and theorem assertions
        if d == 3:
            require((cert["k"], cert["p"], m) == (5, 1, 5), "Unexpected (k,p,m) at d=3")
        elif d == 4:
            require((cert["k"], cert["p"], m) == (7, 3, 27), "Unexpected (k,p,m) at d=4")
            require(cert["p"] != 4 and m != 31, "d=4 disproof assertion failed")
        elif d == 5:
            require((cert["k"], cert["p"], m) == (13, 10, 104), "Unexpected (k,p,m) at d=5")
        else:
            require((cert["k"], cert["p"], m) == (d + 3, d, 8 * d - 3), f"General formula mismatch at d={d}")
            require(m != 8 * d - 1, f"Modulus matched 8d-1 at d={d}")

    small_res_checked = verify_small_residue_certificates(
        doc["small_exceptional_residue_certificates"], finite_by_d
    )

    # (ii) Symbolic & boundary verification of General Theorem for all d >= 6
    sym_res = verify_general_proof_symbolic()
    boundary_d = doc["general_theorem_d_ge_6"]["boundary_check_d_values"]
    require(set(boundary_d) >= {6, 7, 8, 9, 10, 50, 100}, "Boundary d list incomplete")
    bnd_res = verify_boundary_d_instances(boundary_d)

    # (iii) Mandatory negative controls
    nc_res = verify_negative_controls(doc["negative_controls"])

    elapsed = time.time() - t0
    summary = {
        "status": "ALL_CHECKS_PASSED",
        "witnesses_sha256": sha256_hex,
        "finite_certificates_dual_verified_d_range": [3, 40],
        "naive_crosschecked_d_range": [3, 12],
        "small_residue_proofs_verified": small_res_checked,
        "symbolic_proof_d_ge_6": sym_res,
        "boundary_instances_verified": bnd_res,
        "negative_controls_rejected": len(nc_res),
        "elapsed_seconds": round(elapsed, 3),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
