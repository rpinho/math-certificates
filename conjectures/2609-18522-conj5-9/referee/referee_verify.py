#!/usr/bin/env python3
"""Clean-room independent referee verifier for arXiv:2609.18522v1 Conjectures 5 & 9.

Arithmetic policy:
- Pure Python standard library ONLY.
- Exact `int` and `fractions.Fraction` arithmetic ONLY.
- ZERO `float` literals, ZERO `float()` calls, ZERO `/` division operators, ZERO `math` imports
  (enforced at startup via an AST self-inspection of this file).
"""

import ast
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys


ALLOWED_IMPORTS = {
    "ast",
    "fractions",
    "gzip",
    "hashlib",
    "json",
    "pathlib",
    "re",
    "sys",
}


def self_audit_ast(source_path: Path) -> None:
    """Verify this script contains zero float literals/calls, zero `/` ops, and zero math imports."""
    src = source_path.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(source_path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root not in ALLOWED_IMPORTS:
                    raise AssertionError(f"Forbidden import: {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            mod = (node.module or "").split(".")[0]
            if mod not in ALLOWED_IMPORTS:
                raise AssertionError(f"Forbidden from-import: {node.module}")
        elif isinstance(node, ast.Constant) and type(node.value).__name__ == "float":
            raise AssertionError(f"Forbidden float literal at line {node.lineno}: {node.value!r}")
        elif isinstance(node, ast.Name) and node.id == "float":
            raise AssertionError(f"Forbidden reference to `float` at line {node.lineno}")
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            raise AssertionError(f"Forbidden `/` operator at line {node.lineno}; use `//` or `Fraction`")


# ---------------------------------------------------------------------------
# 1. Exact Verbatim Formula Evaluators (Definitions 3 and 8 of 2609.18522v1)
# ---------------------------------------------------------------------------

def eval_L(f: int, d: int) -> Fraction:
    """Evaluate Definition 3 (\\LL_f(d), main.tex lines 285-344) in exact arithmetic."""
    if f < 1 or d < 1:
        raise ValueError(f"Invalid parameters f={f}, d={d}")
    q_minus = f // 2
    q_plus = (f + 1) // 2
    assert q_minus + q_plus == f

    if d <= f - 1:
        val = f
    else:
        # Lines 294-295: blocks of length 2f for every k >= 1:
        # block k covers [(2k-1)f, (2k+1)f - 1].
        k = (d + f) // (2 * f)
        assert k >= 1
        assert (2 * k - 1) * f <= d <= (2 * k + 1) * f - 1

        if (2 * k - 1) * f <= d <= (2 * k - 1) * f + q_minus:
            # Clause (2), line 297
            j = d - (2 * k - 1) * f
            val = k * (f + 1 + j)
        elif (f % 2 == 1) and d == (2 * k - 1) * f + q_plus:
            # Clause (3), line 298
            val = q_plus
        elif (2 * k - 1) * f + q_plus + 1 <= d <= (2 * k - 1) * f + q_plus + 1 + q_minus + 1:
            # Clause (4), line 300
            j = d - ((2 * k - 1) * f + q_plus + 1)
            val = k * (f + 1 + q_minus) + q_plus + 1 - j * (k - 1)
        elif 2 * k * f + 3 <= d <= (2 * k + 1) * f - 1:
            # Clause (5), lines 303-305
            val = (k + 1) * (f - 1) + 3
            if k == 1:
                val += 1
            if k == 2 and d == 4 * f + 3:
                val = 3 * f + 1
        else:
            raise AssertionError(f"Uncovered (f, d)=({f}, {d}) in block k={k}")

        # Lines 301-302: "with the correction that, if f <= 4 or k > 1 then k
        # is to be subtracted from \LL_f(2kf - 1);"
        if d == 2 * k * f - 1 and (f <= 4 or k > 1):
            val -= k

    out = Fraction(val)

    # Small-f modifications, lines 307-343
    if f == 1:
        if d == 3:
            out = Fraction(4)
        if d % 2 == 1 and d >= 7:
            out += Fraction(d + 7, 2)
    elif f == 2:
        if d == 2:
            out = Fraction(1)
        elif d == 6:
            out = Fraction(2)
        if d % 4 == 3:
            out += Fraction(d + 5, 4)
        if d % 4 == 0:
            out += Fraction(1)
    elif f == 3:
        if d % 6 == 5:
            out = Fraction(2)
        if d == 6:
            out = Fraction(4)
        elif d == 7:
            out = Fraction(2)
        elif d == 8:
            out = Fraction(4)
        elif d == 9:
            out = Fraction(4)
        elif d == 10:
            out = Fraction(5)
        elif d == 15:
            out = Fraction(26)
        if d % 6 == 4 and d >= 16:
            out += Fraction(d + 20, 6)
        if d % 6 == 3 and d >= 21:
            out += Fraction(4)
    elif f == 4:
        if d == 5:
            out = Fraction(2)
        elif d == 36:
            out = Fraction(5)
        if d % 8 == 4 and d >= 44:
            out += Fraction(d + 44, 8)

    return out


def eval_K_all(f: int, d: int) -> list[Fraction]:
    """Evaluate Definition 8 (\\KK_r(d, f), main.tex lines 510-703).

    Returns a list of all matching values (length 1 everywhere except f=2, r=2, h in {0,1,2}
    where main.tex line 607 prints `h >= 0` overlapping `h=0, 1, 2`).
    """
    if f < 1 or d < 1:
        raise ValueError(f"Invalid parameters f={f}, d={d}")
    r = ((d - 1) % (2 * f)) + 1
    h = (d - r) // (2 * f)
    assert 1 <= r <= 2 * f and h >= 0 and d == r + 2 * f * h

    if f >= 5:
        if r == 1:
            val = Fraction((2 * f + 1) * h + (2 * f + 7))
        elif r == 2:
            val = Fraction((2 * f) * h + (2 * f + 7))
        elif 3 <= r <= f - 1:
            val = Fraction((f + 1) * h + (3 * f + 1 + r))
        elif r == f:
            val = Fraction((4 * f + 1) * h + (5 * f - 3))
        elif r == f + 1:
            val = Fraction((2 * f + 3) * h + (2 * f + 7))
        elif r == f + 2:
            if d % (4 * f) == (f + 2) % (4 * f):
                val = Fraction((4 * f + 9) * h * h + (4 * f + 9) * h)
            elif d % (4 * f) == (3 * f + 2) % (4 * f):
                val = Fraction((4 * f + 9) * h * h + (4 * f + 9) * h - 1)
            else:
                raise AssertionError("Unreachable mod 4f branch")
        elif f + 3 <= r <= 2 * f - 2:
            q = (f + 1) // 2
            s = r - (f + q)
            if f % 2 == 0:
                if s == 0:
                    val = (
                        Fraction(9 * f + 14, 4) * h * h
                        + Fraction(15 * f + 42, 4) * h
                        + Fraction(3 * f + 2, 2)
                    )
                elif s > 0:
                    val = (
                        Fraction(9 * f + 16 - 2 * s, 4) * h * h
                        + Fraction(15 * f + 40 + 10 * s, 4) * h
                        + Fraction(3 * f + 2 * s, 2)
                    )
                else:
                    val = (
                        Fraction(9 * f + 16 + 2 * s, 4) * h * h
                        + Fraction(15 * f + 42 + 6 * s, 4) * h
                        + Fraction(3 * f + 2 + 2 * s, 2)
                    )
            else:
                if s == 0:
                    val = (
                        Fraction(9 * f + 15, 4) * h * h
                        + Fraction(15 * f + 45, 4) * h
                        + Fraction(3 * f - 1, 2)
                    )
                elif s > 0:
                    val = (
                        Fraction(9 * f + 15 - 2 * s, 4) * h * h
                        + Fraction(15 * f + 45 + 10 * s, 4) * h
                        + Fraction(3 * f + 1 + 2 * s, 2)
                    )
                else:
                    val = (
                        Fraction(9 * f + 15 + 2 * s, 4) * h * h
                        + Fraction(15 * f + 45 + 6 * s, 4) * h
                        + Fraction(3 * f + 3 + 2 * s, 2)
                    )
        elif r == 2 * f - 1:
            val = Fraction(f * h + (2 * f + 1))
        elif r == 2 * f:
            val = Fraction(f * h + (f + 2))
        else:
            raise AssertionError(f"Uncovered residue r={r} for f={f}")

        # Clause (k) corrections, lines 565-572
        if h == 0:
            val -= Fraction(2 * f + r)
        if h == 1:
            val -= Fraction(3 * f + r)
        if r == 1 and h == 0:
            val += Fraction(f - 5)
        if r == 1 and h == 1:
            val -= Fraction(5)
        if r == 1 and h == 2:
            val -= Fraction(4 * f + 7)
        if r == 2 and h == 0:
            val += Fraction(f - 4)
        if r == 2 and h == 1:
            val -= Fraction(3)
        if r == 3 and h == 2:
            val += Fraction(4 * f + 1)
        return [val]

    if f == 1:
        if r == 1:
            if h == 0:
                return [Fraction(2)]
            if h == 1:
                return [Fraction(4)]
            if h == 2:
                return [Fraction(5)]
            return [Fraction(h + 4)]
        return [Fraction(0) if h == 0 else Fraction(1)]

    if f == 2:
        if r == 1:
            if h == 0:
                return [Fraction(3)]
            if h == 1:
                return [Fraction(4)]
            if h == 2:
                return [Fraction(6)]
            return [Fraction(5 * h + 11)]
        if r == 2:
            out: list[Fraction] = []
            if h == 0:
                out.append(Fraction(2))
            elif h == 1:
                out.append(Fraction(5))
            elif h == 2:
                out.append(Fraction(7))
            # Line 607 literally states `5h+11, if h >= 0.`
            if h >= 0:
                out.append(Fraction(5 * h + 11))
            return out
        if r == 3:
            return [Fraction(2 * h + 5)]
        return [Fraction(2 * h + 6)]

    if f == 3:
        if r == 1:
            if h == 0:
                return [Fraction(4)]
            if h == 1:
                return [Fraction(5)]
            if h == 2:
                return [Fraction(8)]
            return [Fraction(7 * h + 13)]
        if r == 2:
            if h == 0:
                return [Fraction(4)]
            if h == 1:
                return [Fraction(5)]
            return [Fraction(6 * h + 13)]
        if r == 3:
            if h == 0:
                return [Fraction(4)]
            if h == 1:
                return [Fraction(19)]
            if h == 2:
                return [Fraction(36)]
            if h == 3:
                return [Fraction(81)]
            return [Fraction(10 * h + 19)]
        if r == 4:
            return [Fraction(4) if h == 0 else Fraction(9 * h + 14)]
        if r == 5:
            if h == 0:
                return [Fraction(9)]
            if h == 1:
                return [Fraction(26)]
            return [Fraction(21, 2) * h * h + Fraction(27, 2) * h]
        return [Fraction(3 * h + 5)]

    # f == 4
    if r == 1:
        if h == 0:
            return [Fraction(5)]
        if h == 1:
            return [Fraction(6)]
        if h == 2:
            return [Fraction(10)]
        return [Fraction(9 * h + 15)]
    if r == 2:
        if h == 0:
            return [Fraction(5)]
        if h == 1:
            return [Fraction(6)]
        return [Fraction(8 * h + 15)]
    if r == 3:
        if h == 0:
            return [Fraction(5)]
        if h == 1:
            return [Fraction(6)]
        if h == 2:
            return [Fraction(43)]
        return [Fraction(5 * h + 16)]
    if r == 4:
        if h == 0:
            return [Fraction(5)]
        if h == 1:
            return [Fraction(12)]
        if h == 2:
            return [Fraction(116)]
        if h == 3:
            return [Fraction(112)]
        if h == 4:
            return [Fraction(193)]
        return [Fraction(32 * h + 40)]
    if r == 5:
        if h == 0:
            return [Fraction(5)]
        if h == 1:
            return [Fraction(13)]
        return [Fraction(11 * h + 15)]
    if r == 6:
        if h == 0:
            return [Fraction(5)]
        if h == 1:
            return [Fraction(14)]
        if h == 2:
            return [Fraction(20)]
        if h == 3:
            return [Fraction(51)]
        if h % 2 == 0:
            return [Fraction(25, 4) * h * h - Fraction(7)]
        return [Fraction(25, 4) * h * h - Fraction(29, 4)]
    if r == 7:
        return [Fraction(11) if h == 0 else Fraction(4 * h + 9)]
    return [Fraction(4 * h + 6)]


# ---------------------------------------------------------------------------
# 2. Independent Greedy 2-Sumfree Sequence Generators (Two Separate Engines)
# ---------------------------------------------------------------------------

def generate_naive_prefix(f: int, g: int, max_n: int) -> tuple[list[int], list[int]]:
    """Reference O(|S|^2) strict greedy 2-sumfree generator up to integer `max_n`.

    Returns `(terms, char_bits)` where `char_bits` is 1-indexed of length `max_n + 1`
    (`char_bits[0] == 0`, `char_bits[n] == 1` iff `n in S_{f,g}` for `1 <= n <= max_n`).
    """
    if not (1 <= f < g <= max_n):
        raise ValueError(f"Require 1 <= f < g <= max_n, got ({f}, {g}, {max_n})")
    terms = [f, g]
    char_bits = [0] * (max_n + 1)
    char_bits[f] = 1
    char_bits[g] = 1
    sums: set[int] = {f + g}
    for n in range(g + 1, max_n + 1):
        if n not in sums:
            for prev in terms:
                s = prev + n
                if s <= max_n:
                    sums.add(s)
            terms.append(n)
            char_bits[n] = 1
    return terms, char_bits


def generate_bitmask_prefix(f: int, g: int, max_n: int) -> tuple[list[int], list[int]]:
    """Fast exact Python-int bitmask strict greedy 2-sumfree generator up to `max_n`."""
    if not (1 <= f < g <= max_n):
        raise ValueError(f"Require 1 <= f < g <= max_n, got ({f}, {g}, {max_n})")
    block = 4096
    block_mask = (1 << block) - 1
    window_mask = (1 << (max_n + 1)) - 1
    s_mask = (1 << f) | (1 << g)
    s_low = s_mask & block_mask
    sums_mask = (1 << (f + g)) if (f + g) <= max_n else 0
    terms = [f, g]
    char_bits = [0] * (max_n + 1)
    char_bits[f] = 1
    char_bits[g] = 1

    start_n = g + 1
    chunk_base = (start_n // block) * block
    chunk = (sums_mask >> chunk_base) & block_mask
    for n in range(start_n, max_n + 1):
        j = n - chunk_base
        if j == block:
            chunk_base = n
            chunk = (sums_mask >> chunk_base) & block_mask
            j = 0
        if not ((chunk >> j) & 1):
            sums_mask = (sums_mask | (s_mask << n)) & window_mask
            chunk = (chunk | (s_low << j)) & block_mask
            s_mask |= 1 << n
            if n < block:
                s_low |= 1 << n
            terms.append(n)
            char_bits[n] = 1
    return terms, char_bits


# ---------------------------------------------------------------------------
# 3. Proof Method I: Authors' Theorem 15 Five-Block Cutoff + Minimality
# ---------------------------------------------------------------------------

def verify_via_theorem15(
    f: int,
    g: int,
    preperiod_terms: list[int],
    period_terms: list[int],
    m: int,
    M: int,
    use_naive_crosscheck: bool = True,
) -> tuple[bool, str]:
    """Verify `(preperiod_terms, period_terms, m, M)` using Theorem 15 + minimality."""
    k = len(preperiod_terms)
    p = len(period_terms)
    if p < 1 or m < 1 or M < 1:
        return False, "Non-positive p, m, or M"
    if M % m != 0:
        return False, f"M={M} is not a multiple of m={m}"

    cutoff = 5 * M
    terms, char_bits = generate_bitmask_prefix(f, g, cutoff)
    if use_naive_crosscheck:
        terms2, char_bits2 = generate_naive_prefix(f, g, cutoff)
        if terms != terms2 or char_bits != char_bits2:
            return False, "Internal generator mismatch between bitmask and naive"

    # 1. Check Theorem 15 hypothesis on 1-indexed C[1..5M]:
    # M_j = char_bits[j*M + 1 : (j+1)*M + 1] for j = 0..4.
    blocks = [char_bits[j * M + 1 : (j + 1) * M + 1] for j in range(5)]
    ones_in_m1 = sum(blocks[1])
    if ones_in_m1 == 0:
        return False, "Block M_1 is all zeros (violates non-nullity in Theorem 15)"
    for j in (2, 3, 4):
        if blocks[j] != blocks[1]:
            return False, f"Theorem 15 block mismatch: M_{j} != M_1"

    # By Theorem 15, c_{u + M} == c_u for ALL u >= M + 1.
    # Now check that the proposed infinite word (preperiod_terms + period_terms + r*m)
    # is strictly increasing, agrees with C[1..5M], AND already has period m on [M+1..2M].
    all_seed = preperiod_terms + period_terms
    for idx in range(len(all_seed) - 1):
        if not (all_seed[idx] < all_seed[idx + 1]):
            return False, "Proposed preperiod+period terms are not strictly increasing"
    if all_seed and all_seed[0] < 1:
        return False, "Proposed terms must be positive integers"
    if period_terms[-1] >= period_terms[0] + m:
        return False, "Period block spans >= m (overlapping translates)"
    if period_terms[0] > M + 1:
        # Even if period_terms[0] > M + 1, M_1 = M_2 would force period M earlier; check [1..5M] directly.
        pass

    proposed_bits = [0] * (cutoff + 1)
    for x in preperiod_terms:
        if x <= cutoff:
            proposed_bits[x] = 1
    r = 0
    while period_terms[0] + r * m <= cutoff:
        for b in period_terms:
            val = b + r * m
            if val <= cutoff:
                if proposed_bits[val] == 1:
                    return False, f"Duplicate proposed element at {val}"
                proposed_bits[val] = 1
        r += 1

    if proposed_bits != char_bits:
        for u in range(1, cutoff + 1):
            if proposed_bits[u] != char_bits[u]:
                return False, f"Proposed word disagrees with C_{{{f},{g}}} at n={u}"

    # Ensure the proposed word is already purely m-periodic on u >= M + 1
    # (so its tail beyond 5M agrees with Theorem 15's M-periodic continuation).
    if k > 0 and preperiod_terms[-1] >= M + 1:
        return False, f"Last preperiod term {preperiod_terms[-1]} >= M+1={M+1}"
    for u in range(M + 1, 4 * M + 1):
        if proposed_bits[u + m] != proposed_bits[u]:
            return False, f"Proposed word not m-periodic at u={u} >= M+1"

    # 2. Prove minimality of p and k on D_{f,g}
    ok_min, msg_min = check_minimality(preperiod_terms, period_terms, m)
    if not ok_min:
        return False, msg_min

    return True, f"Theorem 15 verified (5M={cutoff}, ones(M_1)={ones_in_m1}) + minimal (k={k}, p={p}, m={m})"


def check_minimality(preperiod_terms: list[int], period_terms: list[int], m: int) -> tuple[bool, str]:
    """Prove that `p = len(period_terms)` and `k = len(preperiod_terms)` are minimal."""
    k = len(preperiod_terms)
    p = len(period_terms)
    next_period_start = period_terms[0] + m
    period_diffs = [
        (period_terms[i + 1] if i + 1 < p else next_period_start) - period_terms[i]
        for i in range(p)
    ]
    if sum(period_diffs) != m:
        return False, f"Sum of period_diffs {sum(period_diffs)} != m={m}"

    # Minimality of period length p: no proper divisor d | p can repeat to form period_diffs.
    for div in range(1, p):
        if p % div == 0:
            if all(period_diffs[i] == period_diffs[i % div] for i in range(p)):
                return False, f"Period p={p} is not minimal; divisible by smaller period {div}"

    # Minimality of preperiod length k:
    # In D_{f,g}, d_k = period_terms[0] - preperiod_terms[k-1] (when k >= 2), while
    # d_{k+p} = period_diffs[-1] = (period_terms[0] + m) - period_terms[p-1].
    # Note: for k == 1, D_{f,g} = (d_1, d_2, ...) has d_1 = s_1 - s_0 = period_terms[0] - preperiod_terms[0],
    # so k == 0 iff d_1 == d_{1+p} == period_diffs[-1]!
    if k >= 1:
        d_k = period_terms[0] - preperiod_terms[k - 1]
        d_k_plus_p = period_diffs[-1]
        if d_k == d_k_plus_p:
            return (
                False,
                f"Preperiod k={k} is not minimal: d_{k}={d_k} equals cyclic predecessor d_{k+p}={d_k_plus_p}",
            )

    return True, "Minimal (k, p) confirmed"


# ---------------------------------------------------------------------------
# 4. Proof Method II: Independent Rational Generating-Function Identity
# ---------------------------------------------------------------------------

def poly_add(a: list[int], b: list[int]) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i, v in enumerate(a):
        out[i] += v
    for i, v in enumerate(b):
        out[i] += v
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_sub(a: list[int], b: list[int]) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i, v in enumerate(a):
        out[i] += v
    for i, v in enumerate(b):
        out[i] -= v
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_mul(a: list[int], b: list[int]) -> list[int]:
    if not a or not b:
        return [0]
    out = [0] * (len(a) + len(b) - 1)
    for i, va in enumerate(a):
        if va != 0:
            for j, vb in enumerate(b):
                out[i + j] += va * vb
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_shift(a: list[int], shift: int) -> list[int]:
    if a == [0]:
        return [0]
    return ([0] * shift) + list(a)


def poly_dilate2(a: list[int]) -> list[int]:
    """Return A(z^2) given A(z)."""
    if a == [0]:
        return [0]
    out = [0] * (2 * len(a) - 1)
    for i, v in enumerate(a):
        out[2 * i] = v
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def verify_via_generating_function(
    f: int,
    g: int,
    preperiod_terms: list[int],
    period_terms: list[int],
    m: int,
) -> tuple[bool, str, dict[str, int]]:
    """Prove `T = S_{f,g}` for ALL n >= 1 via A(z)^2 - A(z^2) = H(z) / (1 - z^{2m})^2.

    Uses zero periodicity theorems from the paper.
    """
    k = len(preperiod_terms)
    p = len(period_terms)
    info: dict[str, int] = {}
    if p < 1 or m < 1:
        return False, "Non-positive p or m", info

    all_seed = preperiod_terms + period_terms
    if not all_seed or all_seed[0] < 1:
        return False, "Need non-empty positive terms", info
    for idx in range(len(all_seed) - 1):
        if not (all_seed[idx] < all_seed[idx + 1]):
            return False, "Terms are not strictly increasing", info
    if period_terms[-1] >= period_terms[0] + m:
        return False, "Period block spans >= m; A(z) would not be a {0,1}-series", info

    # Build P(z) and B(z)
    p_poly = [0] * ((preperiod_terms[-1] + 1) if preperiod_terms else 1)
    for x in preperiod_terms:
        p_poly[x] = 1
    b_poly = [0] * (period_terms[-1] + 1)
    for b in period_terms:
        b_poly[b] = 1

    # N(z) = (1 - z^m) P(z) + B(z), so A(z) = N(z) / (1 - z^m)
    n_poly = poly_add(poly_sub(p_poly, poly_shift(p_poly, m)), b_poly)
    deg_n = len(n_poly) - 1

    # H(z) = N(z)^2 (1 + z^m)^2 - N(z^2) (1 - z^{2m})
    one_plus_zm = [0] * (m + 1)
    one_plus_zm[0] = 1
    one_plus_zm[m] = 1
    one_minus_z2m = [0] * (2 * m + 1)
    one_minus_z2m[0] = 1
    one_minus_z2m[2 * m] = -1

    term1 = poly_mul(poly_mul(n_poly, n_poly), poly_mul(one_plus_zm, one_plus_zm))
    term2 = poly_mul(poly_dilate2(n_poly), one_minus_z2m)
    h_poly = poly_sub(term1, term2)
    deg_h = len(h_poly) - 1
    formal_affine_start = 2 * deg_n + 2 * m + 1
    affine_start = max(g + 1, period_terms[0], deg_h + 1, formal_affine_start)
    stride = 2 * m

    info["deg_N"] = deg_n
    info["deg_H"] = deg_h
    info["formal_affine_start"] = formal_affine_start
    info["stride"] = stride

    # Expand u_n = [z^n] (H(z) / (1 - z^{2m})^2) via exact recurrence:
    # u_n = h_n + 2 u_{n - 2m} - u_{n - 4m}.
    # We need values up to `affine_start + 2*stride - 1` so we can check both u_{n_r} and
    # Delta_r = u_{n_r + 2m} - u_{n_r} (plus cross-check u_{n_r + 4m} == u_{n_r} + 2*Delta_r).
    max_eval = affine_start + 3 * stride
    u = [0] * (max_eval + 1)
    for n in range(max_eval + 1):
        hn = h_poly[n] if n <= deg_h else 0
        prev1 = u[n - stride] if n >= stride else 0
        prev2 = u[n - 2 * stride] if n >= 2 * stride else 0
        u[n] = hn + 2 * prev1 - prev2

    # Membership oracle for proposed set T
    pre_set = set(preperiod_terms)
    per_residues = {b % m for b in period_terms}
    b0 = period_terms[0]

    def in_t(n: int) -> bool:
        if n < b0:
            return n in pre_set
        return (n % m) in per_residues

    # Check 1: T intersect [1..g] == {f, g}
    for n in range(1, g + 1):
        if in_t(n) != (n == f or n == g):
            return False, f"Seed mismatch in [1..g] at n={n}", info

    # Check 2: Initial window g < n < affine_start
    for n in range(g + 1, affine_start):
        if u[n] < 0 or (u[n] % 2 != 0):
            return False, f"Invalid representation count u[{n}]={u[n]}", info
        if in_t(n):
            if u[n] != 0:
                return False, f"Member n={n} has nonzero representation count 2*rho={u[n]}", info
        else:
            if u[n] < 2:
                return False, f"Non-member n={n} has zero representation count", info

    # Check 3: All 2m residue classes starting at `affine_start` (where n_r > deg_H and n_r >= b0)
    # Since n_r > deg_H, for ALL j >= 0: u[n_r + j*(2m)] = u[n_r] + j * Delta_r,
    # and membership in_t(n_r + j*(2m)) == in_t(n_r) since n_r >= b0 and 2m is a multiple of m.
    for offset in range(stride):
        nr = affine_start + offset
        u0 = u[nr]
        u1 = u[nr + stride]
        u2 = u[nr + 2 * stride]
        delta = u1 - u0
        if u2 - u1 != delta:
            return False, f"Non-affine residue at nr={nr}: {u0}, {u1}, {u2}", info
        if u0 < 0 or (u0 % 2 != 0) or (delta % 2 != 0):
            return False, f"Parity/sign error at nr={nr}: u0={u0}, delta={delta}", info
        if in_t(nr):
            if u0 != 0 or delta != 0:
                return (
                    False,
                    f"Member residue nr={nr} fails eternal sumfreeness: u0={u0}, delta={delta}",
                    info,
                )
        else:
            if u0 < 2 or delta < 0:
                return (
                    False,
                    f"Non-member residue nr={nr} fails eternal coverage: u0={u0}, delta={delta}",
                    info,
                )

    ok_min, msg_min = check_minimality(preperiod_terms, period_terms, m)
    if not ok_min:
        return False, msg_min, info

    return (
        True,
        f"GF verified (deg_H={deg_h}, affine_start={formal_affine_start}, stride={stride}) + minimal (k={k}, p={p}, m={m})",
        info,
    )


# ---------------------------------------------------------------------------
# 5. Recovery Helper for Positive Controls & Table Audits
# ---------------------------------------------------------------------------

def discover_and_certify(f: int, d: int, max_m_search: int = 80000) -> tuple[int, int, int, int, list[int], list[int]]:
    """Independently discover minimal `(k, p, m, M, preperiod_terms, period_terms)` from `(f, g=f+d)`."""
    g = f + d
    limit = max(500, 20 * g)
    while limit <= 5 * max_m_search:
        terms, char_bits = generate_bitmask_prefix(f, g, limit)
        next_limit = limit * 2
        if len(terms) >= 20:
            diffs = [terms[i] - terms[i - 1] for i in range(1, len(terms))]
            n_d = len(diffs)
            for cand_p in range(1, n_d // 4 + 1):
                win = max(4 * cand_p, min(n_d, 40))
                if win > n_d:
                    continue
                tail = diffs[n_d - win :]
                if not all(tail[i] == tail[i % cand_p] for i in range(win)):
                    continue
                cand_m = sum(diffs[n_d - cand_p :])
                k_idx = n_d - cand_p
                while k_idx >= 1 and diffs[k_idx - 1] == diffs[k_idx - 1 + cand_p]:
                    k_idx -= 1
                pre_terms = terms[:k_idx]
                per_terms = terms[k_idx : k_idx + cand_p]
                onset_c = 1
                for u in range(min(limit - cand_m, per_terms[0]), 0, -1):
                    if char_bits[u] != char_bits[u + cand_m]:
                        onset_c = u + 1
                        break
                mult = max(1, (max(onset_c - 1, 1) + cand_m - 1) // cand_m)
                while mult * cand_m + 1 < onset_c:
                    mult += 1
                cand_M = mult * cand_m
                if 5 * cand_M <= limit:
                    ok, _ = verify_via_theorem15(
                        f, g, pre_terms, per_terms, cand_m, cand_M, use_naive_crosscheck=False
                    )
                    if ok:
                        return k_idx, cand_p, cand_m, cand_M, pre_terms, per_terms
                elif 5 * cand_M <= 5 * max_m_search:
                    next_limit = max(next_limit, 5 * cand_M)
                    break
        limit = next_limit
    raise RuntimeError(f"Failed to certify (f={f}, d={d}) within max_m_search={max_m_search}")


# ---------------------------------------------------------------------------
# 6. Adversarial Mutation / Negative Controls
# ---------------------------------------------------------------------------

def run_negative_controls(
    label: str,
    f: int,
    g: int,
    preperiod_terms: list[int],
    period_terms: list[int],
    m: int,
    M: int,
    formula_val: int,
    is_period_conjecture: bool,
) -> list[tuple[str, bool, bool]]:
    """Construct 8 adversarial mutants for a witness and verify ALL are rejected."""
    mutants: list[tuple[str, list[int], list[int], int, int]] = []

    # 1. Claimed formula value forced onto period or preperiod
    if is_period_conjecture:
        # Claim p = formula_val = 9 by taking first 9 period terms with sum of first 9 diffs
        trunc_per = period_terms[:formula_val]
        trunc_m = period_terms[formula_val] - period_terms[0]
        mutants.append(("printed_wrong_period_p9", preperiod_terms, trunc_per, trunc_m, 3 * trunc_m))
    else:
        # Claim k = formula_val = 7 by corrupting preperiod with an extra bogus term (19) before 20
        mutants.append(("printed_wrong_preperiod_k7_bogus_term", preperiod_terms + [period_terms[0] - 1], period_terms, m, M))

    # 2. Doubled period (2p, 2m): valid set, MUST fail minimality of p
    doubled_per = period_terms + [x + m for x in period_terms]
    mutants.append(("doubled_period_2p", preperiod_terms, doubled_per, 2 * m, 2 * M))

    # 3. Delayed onset (k + 1): valid set, MUST fail minimality of k (note for S_{5,10} this is ALSO k = 7 = formula_val!)
    delayed_pre = preperiod_terms + [period_terms[0]]
    delayed_per = period_terms[1:] + [period_terms[0] + m]
    mutants.append(("delayed_onset_k_plus_1", delayed_pre, delayed_per, m, M))

    # 4. Premature onset (k - 1): shifts period 1 step too early
    premature_pre = preperiod_terms[:-1]
    premature_per = [preperiod_terms[-1]] + period_terms[:-1]
    mutants.append(("premature_onset_k_minus_1", premature_pre, premature_per, m, M))

    # 5. Corrupted last preperiod term (+1)
    bad_pre = list(preperiod_terms)
    bad_pre[-1] += 1
    mutants.append(("corrupted_preperiod_term", bad_pre, period_terms, m, M))

    # 6. Corrupted last period term (+1)
    bad_per = list(period_terms)
    bad_per[-1] += 1
    mutants.append(("corrupted_tail_term", preperiod_terms, bad_per, m, M))

    # 7. Corrupted modulus (m + 1)
    mutants.append(("corrupted_modulus_m_plus_1", preperiod_terms, period_terms, m + 1, (M // m) * (m + 1)))

    # 8. Corrupted periodic gap swap (swap first two distinct adjacent gaps inside period)
    diffs = [
        (period_terms[i + 1] if i + 1 < len(period_terms) else period_terms[0] + m) - period_terms[i]
        for i in range(len(period_terms))
    ]
    swap_idx = 0
    for idx in range(len(diffs) - 1):
        if diffs[idx] != diffs[idx + 1]:
            swap_idx = idx
            break
    diffs[swap_idx], diffs[swap_idx + 1] = diffs[swap_idx + 1], diffs[swap_idx]
    swapped_per = [period_terms[0]]
    for d_step in diffs[:-1]:
        swapped_per.append(swapped_per[-1] + d_step)
    mutants.append(("swapped_period_gaps", preperiod_terms, swapped_per, m, M))

    results: list[tuple[str, bool, bool]] = []
    for name, m_pre, m_per, m_mod, m_M in mutants:
        ok_t15, _ = verify_via_theorem15(f, g, m_pre, m_per, m_mod, m_M, use_naive_crosscheck=False)
        ok_gf, _, _ = verify_via_generating_function(f, g, m_pre, m_per, m_mod)
        if ok_t15 or ok_gf:
            raise AssertionError(
                f"[{label}] Mutant {name!r} WAS NOT REJECTED! (thm15={ok_t15}, gf={ok_gf})"
            )
        results.append((name, ok_t15, ok_gf))
    return results


# ---------------------------------------------------------------------------
# 7. Primary-Source TeX & Printed-Table Audit
# ---------------------------------------------------------------------------

def load_primary_tex(gz_path: Path) -> tuple[str, str, list[str]]:
    with gzip.open(gz_path, "rt", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not (isinstance(payload, list) and len(payload) == 1 and len(payload[0]) == 2):
        raise AssertionError("Unexpected JSON structure in 2609.18522v1.tex.json.gz")
    tex_name, tex_content = payload[0]
    return tex_name, tex_content, tex_content.splitlines()


def extract_ints(text: str) -> list[int]:
    return [int(x) for x in re.findall(r"-?\d+", text)]


def audit_printed_tables_and_examples(lines: list[str]) -> dict[str, object]:
    """Audit printed arrays, bitstrings, and Example 18 claims in main.tex."""
    summary: dict[str, object] = {}

    # 1. 20x20 preperiod matrix K(d, f), lines 178-197
    k_mat = [extract_ints(lines[ln - 1]) for ln in range(178, 198)]
    assert len(k_mat) == 20 and all(len(row) == 20 for row in k_mat)

    # 2. 20x20 period matrix P(d, f), lines 207-226
    p_mat = [extract_ints(lines[ln - 1]) for ln in range(207, 227)]
    assert len(p_mat) == 20 and all(len(row) == 20 for row in p_mat)

    # 3. Six 25-entry period rows, lines 412-417
    p_rows: dict[int, list[int]] = {}
    for f_idx, ln in enumerate(range(412, 418), 1):
        rhs = lines[ln - 1].split("=", 1)[1]
        vals = extract_ints(rhs)
        assert len(vals) == 25, f"Expected 25 ints at line {ln}, got {len(vals)}"
        p_rows[f_idx] = vals

    # 4. Six 25-entry preperiod rows, lines 718-735
    q_block = "\n".join(lines[717:736])
    q_parts = q_block.split("],")
    q_rows: dict[int, list[int]] = {}
    for f_idx in range(1, 7):
        rhs = q_parts[f_idx - 1].split("=", 1)[1]
        vals = extract_ints(rhs)
        assert len(vals) == 25, f"Expected 25 ints for Q[1..25,{f_idx}], got {len(vals)}"
        q_rows[f_idx] = vals

    # 5. f=19 period arrays: lines 375-379 (94), 385-386 (38), 392-394 (38) => 170 entries
    f19_vals = (
        extract_ints("\n".join(lines[374:380]))
        + extract_ints("\n".join(lines[384:387]))
        + extract_ints("\n".join(lines[391:395]))
    )
    assert len(f19_vals) == 170

    # 6. f=12 period arrays: lines 446-448 (59), 453-454 (24), 458-459 (24) => 107 entries
    f12_vals = (
        extract_ints("\n".join(lines[445:449]))
        + extract_ints("\n".join(lines[452:455]))
        + extract_ints("\n".join(lines[457:460]))
    )
    assert len(f12_vals) == 107

    # 7. f=9 preperiod array: lines 750-759 => 234 entries
    f9_vals = extract_ints("\n".join(lines[749:760]))
    assert len(f9_vals) == 234

    # 8. f=9 residue lines: lines 768-785 => 18 * 13 = 234 entries
    f9_res_entries: list[tuple[int, int]] = []
    for r_idx, ln in enumerate(range(768, 786), 1):
        # Strip `d \equiv r \bmod 18:` prefix and trailing `(slope)` or `((second_diff))`
        body = lines[ln - 1].split(":", 1)[1].split(r"\cdots")[0]
        vals = extract_ints(body)
        assert len(vals) == 13, f"Expected 13 entries at line {ln}, got {len(vals)}"
        for h_idx, v in enumerate(vals):
            d_val = r_idx + 18 * h_idx
            f9_res_entries.append((d_val, v))
    assert len(f9_res_entries) == 234

    # Certify all unique (f, d) pairs needed across all 1,845 displayed entries
    needed_pairs: set[tuple[int, int]] = set()
    for d in range(1, 21):
        for f in range(1, 21):
            needed_pairs.add((f, d))
    for f in range(1, 7):
        for d in range(1, 26):
            needed_pairs.add((f, d))
    for d in range(1, 171):
        needed_pairs.add((19, d))
    for d in range(1, 108):
        needed_pairs.add((12, d))
    for d in range(1, 235):
        needed_pairs.add((9, d))

    cert_cache: dict[tuple[int, int], tuple[int, int]] = {}
    for f, d in sorted(needed_pairs):
        k_c, p_c, _, _, _, _ = discover_and_certify(f, d)
        cert_cache[(f, d)] = (k_c, p_c)

    def check_p_display(entries: list[tuple[int, int, int]]) -> tuple[int, int, int]:
        match_seq = 0
        disagree_formula = 0
        for f, d, disp in entries:
            _, p_true = cert_cache[(f, d)]
            if disp == p_true:
                match_seq += 1
            if Fraction(disp) != eval_L(f, d):
                disagree_formula += 1
        return len(entries), match_seq, disagree_formula

    def check_k_display(entries: list[tuple[int, int, int]]) -> tuple[int, int, int]:
        match_seq = 0
        disagree_formula = 0
        for f, d, disp in entries:
            k_true, _ = cert_cache[(f, d)]
            if disp == k_true:
                match_seq += 1
            if all(Fraction(disp) != kv for kv in eval_K_all(f, d)):
                disagree_formula += 1
        return len(entries), match_seq, disagree_formula

    summary["k_20x20"] = check_k_display(
        [(f, d, k_mat[d - 1][f - 1]) for d in range(1, 21) for f in range(1, 21)]
    )
    summary["p_20x20"] = check_p_display(
        [(f, d, p_mat[d - 1][f - 1]) for d in range(1, 21) for f in range(1, 21)]
    )
    summary["p_6x25"] = check_p_display(
        [(f, d, p_rows[f][d - 1]) for f in range(1, 7) for d in range(1, 26)]
    )
    summary["q_6x25"] = check_k_display(
        [(f, d, q_rows[f][d - 1]) for f in range(1, 7) for d in range(1, 26)]
    )
    summary["p_f19"] = check_p_display([(19, d, f19_vals[d - 1]) for d in range(1, 171)])
    summary["p_f12"] = check_p_display([(12, d, f12_vals[d - 1]) for d in range(1, 108)])
    summary["q_f9"] = check_k_display([(9, d, f9_vals[d - 1]) for d in range(1, 235)])
    summary["q_f9_res"] = check_k_display([(9, d, v) for d, v in f9_res_entries])

    # Check S_{3,7} characteristic prefix at TeX line 100
    line100 = lines[99].split("%")[0].strip().strip("$").rstrip(",")
    printed_c37: list[int] = []
    for tok in line100.split(","):
        tok = tok.strip()
        if "^" in tok:
            b_str, exp_str = tok.split("^")
            printed_c37.extend([int(b_str)] * int(exp_str))
        else:
            printed_c37.append(int(tok))
    _, true_c37 = generate_bitmask_prefix(3, 7, len(printed_c37))
    c37_mismatches = [
        i for i in range(1, len(printed_c37) + 1) if printed_c37[i - 1] != true_c37[i]
    ]
    summary["c37_line100_len"] = len(printed_c37)
    summary["c37_line100_mismatch_count"] = len(c37_mismatches)
    summary["c37_line100_first_mismatch"] = c37_mismatches[0] if c37_mismatches else None

    # Check (f=8, d=59) half-integer preperiod prediction and certified k
    k_8_59, p_8_59, _, _, _, _ = discover_and_certify(8, 59)
    summary["case_8_59"] = {
        "formula_K": str(eval_K_all(8, 59)[0]),
        "certified_k": k_8_59,
        "certified_p": p_8_59,
    }

    # Check Example 18 claims: S_{3,248} (f=3,d=245), S_{3,497} (f=3,d=494), S_{3,500} (f=3,d=497)
    k_3_248, p_3_248, _, _, _, _ = discover_and_certify(3, 245, max_m_search=200000)
    k_3_497, p_3_497, _, _, _, _ = discover_and_certify(3, 494, max_m_search=200000)
    k_3_500, p_3_500, _, _, _, _ = discover_and_certify(3, 497, max_m_search=600000)
    summary["example18"] = {
        "S_3_248": (k_3_248, p_3_248, str(eval_K_all(3, 245)[0]), str(eval_L(3, 245))),
        "S_3_497": (k_3_497, p_3_497, str(eval_K_all(3, 494)[0]), str(eval_L(3, 494))),
        "S_3_500": (k_3_500, p_3_500, str(eval_K_all(3, 497)[0]), str(eval_L(3, 497))),
    }
    return summary


# ---------------------------------------------------------------------------
# 8. Main Referee Verification Driver
# ---------------------------------------------------------------------------

def main() -> int:
    here = Path(__file__).resolve().parent
    self_audit_ast(Path(__file__).resolve())
    print("[PASS] AST self-audit: zero float literals/calls, zero `/` ops, zero forbidden imports.")

    inputs_dir = here.joinpath("inputs")
    tex_gz_path = inputs_dir.joinpath("2609.18522v1.tex.json.gz")
    witness_path = inputs_dir.joinpath("witness.json")
    defs_path = inputs_dir.joinpath("definitions.tex")

    # 1. Load & verify primary TeX source and definitions.tex
    tex_name, tex_content, tex_lines = load_primary_tex(tex_gz_path)
    tex_sha256 = hashlib.sha256(tex_content.encode("utf-8")).hexdigest()
    assert tex_name == "main.tex", f"Expected main.tex, got {tex_name}"
    assert len(tex_lines) == 1043, f"Expected 1043 lines, got {len(tex_lines)}"

    expected_defs = "\n".join(tex_lines[284:344] + tex_lines[509:703]) + "\n"
    actual_defs = defs_path.read_text(encoding="utf-8")
    if actual_defs.rstrip("\n") != expected_defs.rstrip("\n"):
        raise AssertionError("inputs/definitions.tex does not match main.tex Definitions 3 & 8 verbatim!")
    print(f"[PASS] Primary source main.tex loaded (1043 lines, sha256={tex_sha256[:16]}...), definitions.tex matches verbatim.")

    # 2. Full field-by-field audit of inputs/witness.json
    witness = json.loads(witness_path.read_text(encoding="utf-8"))
    expected_top_keys = {"source", "tex_sha256", "cases"}
    if set(witness.keys()) != expected_top_keys:
        raise AssertionError(f"Unexpected witness.json top-level keys: {set(witness.keys())}")
    assert witness["source"] == "2609.18522v1 / main.tex"
    assert witness["tex_sha256"] == tex_sha256, "witness.json tex_sha256 mismatch!"
    assert isinstance(witness["cases"], list) and len(witness["cases"]) == 2

    expected_case_keys = {
        "f",
        "d",
        "g",
        "k",
        "p",
        "m",
        "M",
        "cutoff",
        "preperiod_terms",
        "period_terms",
        "preperiod_differences",
        "period_differences",
        "conjecture",
        "formula_value",
        "tex_lines",
    }

    for idx, case in enumerate(witness["cases"]):
        if set(case.keys()) != expected_case_keys:
            raise AssertionError(f"Case {idx} key mismatch: {set(case.keys()) ^ expected_case_keys}")
        f = case["f"]
        d = case["d"]
        g = case["g"]
        k = case["k"]
        p = case["p"]
        m = case["m"]
        M = case["M"]
        cutoff = case["cutoff"]
        pre_t = case["preperiod_terms"]
        per_t = case["period_terms"]
        pre_d = case["preperiod_differences"]
        per_d = case["period_differences"]
        conj = case["conjecture"]
        f_val = case["formula_value"]

        assert g == f + d, f"Case {idx}: g != f + d"
        assert cutoff == 5 * M, f"Case {idx}: cutoff != 5*M"
        assert len(pre_t) == k and len(per_t) == p
        assert len(pre_d) == k and len(per_d) == p

        # Verify differences match terms identically
        joined = pre_t + per_t + [per_t[0] + m]
        recomputed_diffs = [joined[i + 1] - joined[i] for i in range(k + p)]
        assert recomputed_diffs[:k] == pre_d, f"Case {idx}: preperiod_differences mismatch"
        assert recomputed_diffs[k:] == per_d, f"Case {idx}: period_differences mismatch"
        assert sum(per_d) == m, f"Case {idx}: sum(period_differences) != m"

        # Verify every quoted TeX line verbatim against main.tex
        for ln_str, quoted in case["tex_lines"].items():
            ln_no = int(ln_str)
            raw_line = tex_lines[ln_no - 1]
            if raw_line != quoted:
                raise AssertionError(
                    f"Case {idx} TeX line {ln_no} mismatch!\n  witness: {quoted!r}\n  main.tex: {raw_line!r}"
                )

        # Verify formula evaluation
        if conj == 5:
            calc = eval_L(f, d)
            assert calc == Fraction(f_val), f"L_{f}({d}) = {calc} != {f_val}"
            assert Fraction(p) != calc, "Period p did not refute Conjecture 5!"
        elif conj == 9:
            calcs = eval_K_all(f, d)
            assert calcs == [Fraction(f_val)], f"K_r({d},{f}) = {calcs} != [{f_val}]"
            assert Fraction(k) != calcs[0], "Preperiod k did not refute Conjecture 9!"
        else:
            raise AssertionError(f"Unexpected conjecture number: {conj}")

        # Verify BOTH independent proofs (Theorem 15 AND Rational Generating Function) + minimality
        ok_t15, msg_t15 = verify_via_theorem15(f, g, pre_t, per_t, m, M, use_naive_crosscheck=True)
        if not ok_t15:
            raise AssertionError(f"Case {idx} failed Theorem 15 proof: {msg_t15}")

        ok_gf, msg_gf, gf_info = verify_via_generating_function(f, g, pre_t, per_t, m)
        if not ok_gf:
            raise AssertionError(f"Case {idx} failed Generating Function proof: {msg_gf}")

        # Independent discovery from (f, d) alone must recover identical (k, p, m, pre_t, per_t)
        dk, dp, dm, _, d_pre, d_per = discover_and_certify(f, d)
        assert (dk, dp, dm, d_pre, d_per) == (k, p, m, pre_t, per_t), (
            f"Independent discovery mismatch for S_{{{f},{g}}}"
        )

        # Run 8 adversarial negative controls / mutants
        neg_results = run_negative_controls(
            f"S_{{{f},{g}}}", f, g, pre_t, per_t, m, M, f_val, is_period_conjecture=(conj == 5)
        )

        print(f"[PASS] Witness S_{{{f},{g}}} (f={f}, d={d}) refutes Conjecture {conj}:")
        print(f"       Formula = {f_val}, Certified (k, p, m) = ({k}, {p}, {m})")
        print(f"       Proof I : {msg_t15}")
        print(f"       Proof II: {msg_gf}")
        print(f"       Mutants : {len(neg_results)}/8 adversarial mutations rejected.")

    # 3. Verify S_{12,30} (f=12, d=18) worked example from main.tex lines 465-481
    k12, p12, m12, M12, pre12, per12 = discover_and_certify(12, 18)
    ok12_t15, _ = verify_via_theorem15(12, 30, pre12, per12, m12, M12, use_naive_crosscheck=True)
    ok12_gf, _, _ = verify_via_generating_function(12, 30, pre12, per12, m12)
    assert ok12_t15 and ok12_gf
    assert (k12, p12, m12) == (36, 19, 71), f"Unexpected S_{{12,30}} triple: {(k12, p12, m12)}"
    l12_18 = eval_L(12, 18)
    k12_18 = eval_K_all(12, 18)
    assert l12_18 == Fraction(19) and k12_18 == [Fraction(-23)]
    printed_pre12 = extract_ints("\n".join(tex_lines[471:476]))
    printed_per12 = extract_ints("\n".join(tex_lines[478:481]))
    assert pre12 == printed_pre12 and per12 == printed_per12
    print(
        f"[PASS] S_{{12,30}} (f=12, d=18): certified (k, p, m) = ({k12}, {p12}, {m12}), "
        f"matches main.tex lines 472-480; L_12(18)={l12_18}, K_18(18,12)={k12_18[0]} (negative!)."
    )

    # 4. Verify 14 Positive Controls where BOTH Definitions 3 & 8 hold + S_{5,11} (Def 3 holds, Def 8 fails!)
    positive_controls = [
        (1, 2),
        (1, 3),
        (2, 3),
        (2, 4),
        (2, 5),
        (2, 8),
        (3, 6),
        (3, 7),
        (4, 10),
        (4, 12),
        (5, 9),
        (5, 35),
        (5, 36),
        (6, 11),
    ]
    for f, g in positive_controls:
        d = g - f
        kc, pc, mc, Mc, pre_c, per_c = discover_and_certify(f, d)
        ok_a, msg_a = verify_via_theorem15(f, g, pre_c, per_c, mc, Mc, use_naive_crosscheck=True)
        ok_b, msg_b, _ = verify_via_generating_function(f, g, pre_c, per_c, mc)
        assert ok_a, f"Positive control S_{{{f},{g}}} failed Thm 15: {msg_a}"
        assert ok_b, f"Positive control S_{{{f},{g}}} failed GF: {msg_b}"
        l_val = eval_L(f, d)
        k_vals = eval_K_all(f, d)
        assert l_val == Fraction(pc), f"Positive control S_{{{f},{g}}}: L_{f}({d})={l_val} != p={pc}"
        assert Fraction(kc) in k_vals, f"Positive control S_{{{f},{g}}}: k={kc} not in K={k_vals}"

    # Also explicitly check S_{5,11} (f=5, d=6) from the prompt's example list:
    # Def 3 holds (L_5(6) = 7 == p), while Def 8 gives K_6(6,5) = 1 != 6 = k (another Conj 9 failure!)
    k511, p511, m511, M511, pre511, per511 = discover_and_certify(5, 6)
    assert verify_via_theorem15(5, 11, pre511, per511, m511, M511, use_naive_crosscheck=True)[0]
    assert verify_via_generating_function(5, 11, pre511, per511, m511)[0]
    assert (k511, p511) == (6, 7) and eval_L(5, 6) == Fraction(7) and eval_K_all(5, 6) == [Fraction(1)]
    print(
        f"[PASS] {len(positive_controls)} full positive controls verified via Thm 15 + GF and matched Definitions 3 & 8 "
        f"(plus S_{{5,11}}: (k,p)=(6,7), L_5(6)=7 matches, K_6(6,5)=1 is another Conj 9 failure)."
    )

    # 5. Audit printed tables, line 100 bitstring, and Example 18 in main.tex against REPORT.md
    if "--skip-tables" not in sys.argv:
        tbl = audit_printed_tables_and_examples(tex_lines)
        assert tbl["k_20x20"] == (400, 400, 115), f"k_20x20 mismatch: {tbl['k_20x20']}"
        assert tbl["p_20x20"] == (400, 400, 1), f"p_20x20 mismatch: {tbl['p_20x20']}"
        assert tbl["p_6x25"] == (150, 150, 1), f"p_6x25 mismatch: {tbl['p_6x25']}"
        assert tbl["q_6x25"] == (150, 150, 27), f"q_6x25 mismatch: {tbl['q_6x25']}"
        assert tbl["p_f19"] == (170, 170, 0), f"p_f19 mismatch: {tbl['p_f19']}"
        assert tbl["p_f12"] == (107, 107, 0), f"p_f12 mismatch: {tbl['p_f12']}"
        assert tbl["q_f9"] == (234, 234, 87), f"q_f9 mismatch: {tbl['q_f9']}"
        assert tbl["q_f9_res"] == (234, 234, 87), f"q_f9_res mismatch: {tbl['q_f9_res']}"
        assert tbl["c37_line100_len"] == 64
        assert tbl["c37_line100_mismatch_count"] == 7
        assert tbl["c37_line100_first_mismatch"] == 46
        assert tbl["case_8_59"] == {"formula_K": "645/2", "certified_k": 265, "certified_p": 61} or (
            tbl["case_8_59"]["formula_K"] == "645/2" and tbl["case_8_59"]["certified_k"] == 265
        )
        ex18 = tbl["example18"]
        assert ex18["S_3_248"] == (17340, 2, "17340", "2"), f"S_3_248 mismatch: {ex18['S_3_248']}"
        assert ex18["S_3_497"] == (505, 251, "505", "251"), f"S_3_497 mismatch: {ex18['S_3_497']}"
        assert ex18["S_3_500"] == (71709, 2, "71709", "2"), f"S_3_500 mismatch: {ex18['S_3_500']}"
        print(
            "[PASS] All 1,845 displayed entries in main.tex, line-100 bitstring (7/64 errors, first at 46), "
            "(f,d)=(8,59) (K=645/2 vs k=265), and Example 18 (S_{3,248}, S_{3,497}, S_{3,500}) verified!"
        )

    print("ALL REFEREE CHECKS PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
