#!/usr/bin/env python3
"""Independent exact verifier for the unconditional proof of Conjecture 4.5
of Hongesberg, Konvalinka & Linusson (arXiv:2610.07442v1).

Uses strictly standard-library integer and exact rational (fractions.Fraction)
operations, with zero external dependencies and zero imprecise operations.
"""

import gzip
import json
import os
import sys
from fractions import Fraction


# ---------------------------------------------------------------------------
# 1. Exact integer binomial and Catalan helpers
# ---------------------------------------------------------------------------

def binom_poly(n, m):
    """Standard polynomial binomial coefficient C(n, m) for all integers n, m.
    Returns 0 if m < 0, 1 if m == 0, and n*(n-1)*...*(n-m+1) // m! for m > 0.
    """
    if m < 0:
        return 0
    if m == 0:
        return 1
    if n >= 0 and m > n:
        return 0
    num = 1
    den = 1
    for j in range(m):
        num *= (n - j)
        den *= (j + 1)
    assert num % den == 0
    return num // den


def binom_naive_nonneg(n, m):
    """Naive convention setting C(n, m) = 0 whenever n < 0 (even at m == 0)."""
    if n < 0 or m < 0 or m > n:
        return 0
    return binom_poly(n, m)


def catalan(n):
    c = binom_poly(2 * n, n)
    assert c % (n + 1) == 0
    return c // (n + 1)


def build_binom_cache(max_n):
    """Precompute C(n, m) for -2 <= n <= max_n and -4 <= m <= max_n."""
    cache = {}
    for n in range(-2, max_n + 1):
        row = {}
        for m in range(-4, max_n + 1):
            row[m] = binom_poly(n, m)
        cache[n] = row
    return cache


def eval_F_cached(r, k, d, bcache, cat_even):
    """Evaluate the RHS F(r, k, d) of eq:conj312 using precomputed tables."""
    s1 = 0
    b_k = bcache[k]
    b_rm2 = bcache[r - 2]
    pow2 = 1
    for i in range(1, d + 1):
        s1 += pow2 * b_k[i] * (b_rm2[d - i] - 2 * b_rm2[d - i - 2])
        pow2 <<= 1

    b_r = bcache[r]
    s2 = b_r[d]

    s3 = 0
    i = 0
    while d - 1 - 2 * i >= 0:
        s3 += cat_even[i] * bcache[r - 1 + 2 * i][d - 1 - 2 * i]
        i += 1

    s4 = 0
    for i in range(1, d + 1):
        if i & 1:
            s4 -= 2 * b_r[d - i]
        else:
            s4 += 2 * b_r[d - i]

    return s1 + s2 + s3 + s4


def eval_F_direct(r, k, d, binom_fn=binom_poly):
    """Direct uncached evaluation of F(r, k, d) from eq:conj312."""
    s1 = 0
    for i in range(1, d + 1):
        term = binom_fn(r - 2, d - i) - 2 * binom_fn(r - 2, d - i - 2)
        s1 += (1 << (i - 1)) * binom_fn(k, i) * term
    s2 = binom_fn(r, d)
    s3 = 0
    i = 0
    while d - 1 - 2 * i >= 0:
        s3 += catalan(2 * i) * binom_fn(r - 1 + 2 * i, d - 1 - 2 * i)
        i += 1
    s4 = 0
    for i in range(1, d + 1):
        sign = -1 if (i % 2 == 1) else 1
        s4 += 2 * sign * binom_fn(r, d - i)
    return s1 + s2 + s3 + s4


# ---------------------------------------------------------------------------
# 2. Schroeder lattice-path DP and Section 4 recurrences
# ---------------------------------------------------------------------------

def compute_schroeder_dp(max_m):
    """Compute large Schroeder numbers Sch_m for -1 <= m <= max_m directly
    from the lattice path definition in Section 3 (paths from (0,0) to (m,m)
    using steps (1,0), (0,1), (1,1) staying on or below y = x).
    """
    sch = {-1: 1}
    for n in range(0, max_m + 1):
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        dp[0][0] = 1
        for x in range(n + 1):
            for y in range(x + 1):
                if x == 0 and y == 0:
                    continue
                val = 0
                if x > 0 and y <= x - 1:
                    val += dp[x - 1][y]
                if y > 0:
                    val += dp[x][y - 1]
                if x > 0 and y > 0 and y - 1 <= x - 1:
                    val += dp[x - 1][y - 1]
                dp[x][y] = val
        sch[n] = dp[n][n]
    return sch


def compute_recurrence_table(max_n, sch, bcache):
    """Compute s^{312}_{r,k,d} for all 0 <= d <= r, k <= max_n from
    the base cases and Section 4 recurrences (lem:r=d, lem:k=d, lem:general).
    Returns S[d][r][k].
    """
    S = [[[0] * (max_n + 1) for _ in range(max_n + 1)] for _ in range(max_n + 1)]

    # Base cases: d = 0 -> s^{312}_{r,k,0} = 1 for all r, k >= 0
    for r in range(max_n + 1):
        for k in range(max_n + 1):
            S[0][r][k] = 1

    # Row-complete stratum: d = r for 1 <= r <= k (Proposition 4.2 / lem:r=d)
    for r in range(1, max_n + 1):
        S[r][r][r] = sch[r - 1]
        # Verify lem:r=d also holds at k = r when S[r][r][r-1] == 0
        chk_diag = S[r][r][r - 1] + S[r - 1][r - 1][r - 1]
        for i in range(2, r + 1):
            idx = r + 1 - i
            chk_diag += sch[i - 2] * S[idx][idx][idx]
        assert chk_diag == S[r][r][r], f"Diagonal recurrence check failed at r={r}"

        for k in range(r + 1, max_n + 1):
            val = S[r][r][k - 1] + S[r - 1][r - 1][k - 1]
            for i in range(2, r + 1):
                d_sub = r + 1 - i
                val += sch[i - 2] * S[d_sub][d_sub][k + 1 - i]
            S[r][r][k] = val

    # Balanced stratum: d = k for 1 <= k < r (Proposition 4.3 / lem:k=d)
    for k in range(1, max_n + 1):
        for r in range(k + 1, max_n + 1):
            val = 0
            for j in range(0, k + 1):
                val += S[j][j][k] * bcache[r - j - 1][k - j]
            S[k][r][k] = val

    # General stratum: 1 <= d < r, k (Theorem 4.4 / lem:general)
    for d in range(1, max_n + 1):
        for r in range(d + 1, max_n + 1):
            for k in range(d + 1, max_n + 1):
                val = S[d][r][k - 1] + S[d - 1][r - 1][k - 1]
                for i in range(2, d + 1):
                    d_sub = d + 1 - i
                    val += sch[i - 2] * (
                        S[d_sub][r + 1 - i][k + 1 - i] - bcache[r - i][d_sub]
                    )
                S[d][r][k] = val

    return S


# ---------------------------------------------------------------------------
# 3. First-principles ASR enumeration and ASM extension checker
# ---------------------------------------------------------------------------

def is_valid_asr_matrix(mat, r, k):
    """Directly verify the three ASR axioms of Section 2 (lines 202-207)."""
    for i in range(r):
        nz = [mat[i][j] for j in range(k) if mat[i][j] != 0]
        if nz:
            if nz[0] != 1 or nz[-1] != 1:
                return False
            for t in range(len(nz) - 1):
                if nz[t] == nz[t + 1]:
                    return False
    for j in range(k):
        nz = [mat[i][j] for i in range(r) if mat[i][j] != 0]
        if nz:
            if nz[0] != 1:
                return False
            for t in range(len(nz) - 1):
                if nz[t] == nz[t + 1]:
                    return False
    return True


def enumerate_all_asrs(r, k):
    """Enumerate all valid r x k ASRs directly from the Section 2 definition."""
    asrs = []

    def gen_rows(col_state):
        yield (0,) * k
        row = [0] * k

        def rec(j, row_state):
            if j == k:
                if row_state == 1:
                    yield tuple(row)
                return
            row[j] = 0
            yield from rec(j + 1, row_state)
            if row_state != 1 and col_state[j] != 1:
                row[j] = 1
                yield from rec(j + 1, 1)
            if row_state == 1 and col_state[j] == 1:
                row[j] = -1
                yield from rec(j + 1, -1)
            row[j] = 0

        yield from rec(0, 0)

    def bt(r_idx, col_state, acc):
        if r_idx == r:
            mat = tuple(acc)
            assert is_valid_asr_matrix(mat, r, k)
            asrs.append(mat)
            return
        for row in gen_rows(col_state):
            ncs = list(col_state)
            for j, v in enumerate(row):
                if v != 0:
                    ncs[j] = v
            acc.append(row)
            bt(r_idx + 1, ncs, acc)
            acc.pop()

    bt(0, [0] * k, [])
    return asrs


def count_312_avoiding_asms(m):
    """Count all m x m 312-avoiding ASMs from first principles."""
    total = 0

    def gen_asm_rows(col_state, forbidden_one):
        row = [0] * m

        def rec(j, row_state):
            if j == m:
                if row_state == 1:
                    yield tuple(row)
                return
            row[j] = 0
            yield from rec(j + 1, row_state)
            if row_state != 1 and col_state[j] != 1 and not forbidden_one[j]:
                row[j] = 1
                yield from rec(j + 1, 1)
            if row_state == 1 and col_state[j] == 1:
                row[j] = -1
                yield from rec(j + 1, -1)
            row[j] = 0

        yield from rec(0, 0)

    def bt(i, col_state, forbidden_one):
        nonlocal total
        if i == m:
            if all(s == 1 for s in col_state):
                total += 1
            return
        for j in range(m):
            if col_state[j] != 1 and forbidden_one[j]:
                return
        max_prev_one = -1
        for j in range(m - 1, -1, -1):
            if col_state[j] != 0:
                max_prev_one = j
                break
        for row in gen_asm_rows(col_state, forbidden_one):
            min_one = m
            for j, v in enumerate(row):
                if v == 1 and j < min_one:
                    min_one = j
            ncs = list(col_state)
            for j, v in enumerate(row):
                if v != 0:
                    ncs[j] = v
            nforb = list(forbidden_one)
            ok = True
            if max_prev_one > min_one + 1:
                for j2 in range(min_one + 1, max_prev_one):
                    nforb[j2] = True
                    if ncs[j2] != 1:
                        ok = False
                        break
            if ok:
                bt(i + 1, ncs, nforb)

    bt(0, [0] * m, [False] * m)
    return total


def has_312_avoiding_asm_extension(asr, r, k, m):
    """Return True iff the r x k ASR is the top-left corner of an m x m ASM
    that avoids the permutation pattern 312.
    """
    def gen_row_completions(i, col_state, forbidden_one):
        row = [0] * m
        if i < r:
            row_state = 0
            for j in range(k):
                v = asr[i][j]
                row[j] = v
                if v == 1:
                    if col_state[j] == 1 or row_state == 1 or forbidden_one[j]:
                        return
                    row_state = 1
                elif v == -1:
                    if col_state[j] != 1 or row_state != 1:
                        return
                    row_state = -1
            start_j = k
            init_state = row_state
        else:
            start_j = 0
            init_state = 0

        def rec(j, row_state):
            if j == m:
                if row_state == 1:
                    yield tuple(row)
                return
            row[j] = 0
            yield from rec(j + 1, row_state)
            if row_state != 1 and col_state[j] != 1 and not forbidden_one[j]:
                row[j] = 1
                yield from rec(j + 1, 1)
            if row_state == 1 and col_state[j] == 1:
                row[j] = -1
                yield from rec(j + 1, -1)
            row[j] = 0

        yield from rec(start_j, init_state)

    def search(i, col_state, forbidden_one):
        if i == m:
            return all(s == 1 for s in col_state)
        for j in range(m):
            if col_state[j] != 1 and forbidden_one[j]:
                return False
        max_prev_one = -1
        for j in range(m - 1, -1, -1):
            if col_state[j] != 0:
                max_prev_one = j
                break
        for row in gen_row_completions(i, col_state, forbidden_one):
            min_one = m
            for j, v in enumerate(row):
                if v == 1 and j < min_one:
                    min_one = j
            ncs = list(col_state)
            for j, v in enumerate(row):
                if v != 0:
                    ncs[j] = v
            nforb = list(forbidden_one)
            ok = True
            if max_prev_one > min_one + 1:
                for j2 in range(min_one + 1, max_prev_one):
                    nforb[j2] = True
                    if ncs[j2] != 1:
                        ok = False
                        break
            if ok and search(i + 1, ncs, nforb):
                return True
        return False

    return search(0, [0] * m, [False] * m)


# ---------------------------------------------------------------------------
# 4. Exact Formal Power Series arithmetic over Fraction (no division operator)
# ---------------------------------------------------------------------------

def frac_inv(q):
    """Exact multiplicative inverse of a nonzero Fraction without '/'."""
    q = Fraction(q)
    assert q.numerator != 0
    if q.numerator > 0:
        return Fraction(q.denominator, q.numerator)
    return Fraction(-q.denominator, -q.numerator)


class FPS:
    """Truncated formal power series in Q[[z]] mod z^(deg + 1)."""

    def __init__(self, coeffs, deg):
        self.deg = deg
        self.c = [
            Fraction(coeffs[i]) if i < len(coeffs) else Fraction(0)
            for i in range(deg + 1)
        ]

    def __getitem__(self, idx):
        if idx < 0 or idx > self.deg:
            return Fraction(0)
        return self.c[idx]

    def __eq__(self, other):
        return self.deg == other.deg and self.c == other.c

    def __add__(self, other):
        if isinstance(other, (int, Fraction)):
            res = list(self.c)
            res[0] += Fraction(other)
            return FPS(res, self.deg)
        assert self.deg == other.deg
        return FPS([self.c[i] + other.c[i] for i in range(self.deg + 1)], self.deg)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, (int, Fraction)):
            res = list(self.c)
            res[0] -= Fraction(other)
            return FPS(res, self.deg)
        assert self.deg == other.deg
        return FPS([self.c[i] - other.c[i] for i in range(self.deg + 1)], self.deg)

    def __rsub__(self, other):
        res = [-x for x in self.c]
        res[0] += Fraction(other)
        return FPS(res, self.deg)

    def __neg__(self):
        return FPS([-x for x in self.c], self.deg)

    def __mul__(self, other):
        if isinstance(other, (int, Fraction)):
            f = Fraction(other)
            return FPS([x * f for x in self.c], self.deg)
        assert self.deg == other.deg
        res = [Fraction(0)] * (self.deg + 1)
        for i in range(self.deg + 1):
            ci = self.c[i]
            if ci == 0:
                continue
            for j in range(self.deg + 1 - i):
                res[i + j] += ci * other.c[j]
        return FPS(res, self.deg)

    def __rmul__(self, other):
        return self.__mul__(other)

    def inv(self):
        inv0 = frac_inv(self.c[0])
        res = [Fraction(0)] * (self.deg + 1)
        res[0] = inv0
        for n in range(1, self.deg + 1):
            s = Fraction(0)
            for i in range(1, n + 1):
                s += self.c[i] * res[n - i]
            res[n] = -s * inv0
        return FPS(res, self.deg)

    def mul_inv(self, denom):
        if isinstance(denom, (int, Fraction)):
            return self * frac_inv(denom)
        return self * denom.inv()

    def pow_int(self, exp):
        if exp == 0:
            return FPS([1], self.deg)
        if exp < 0:
            return self.inv().pow_int(-exp)
        res = FPS([1], self.deg)
        base = self
        e = exp
        while e > 0:
            if e & 1:
                res = res * base
            e >>= 1
            if e > 0:
                base = base * base
        return res

    def sqrt_unit(self):
        assert self.c[0] == 1
        res = [Fraction(0)] * (self.deg + 1)
        res[0] = Fraction(1)
        half = Fraction(1, 2)
        for n in range(1, self.deg + 1):
            s = Fraction(0)
            for i in range(1, n):
                s += res[i] * res[n - i]
            res[n] = (self.c[n] - s) * half
        return FPS(res, self.deg)

    def deriv(self):
        res = [Fraction(i + 1) * self.c[i + 1] for i in range(self.deg)]
        res.append(Fraction(0))
        return FPS(res, self.deg)

    def shift(self, m):
        """Multiply by z^m (m >= 0) truncated to deg."""
        assert m >= 0
        if m > self.deg:
            return FPS([], self.deg)
        return FPS([Fraction(0)] * m + self.c[: self.deg + 1 - m], self.deg)

    def compose(self, g):
        assert g.c[0] == 0 and self.deg == g.deg
        res = FPS([self.c[self.deg]], self.deg)
        for i in range(self.deg - 1, -1, -1):
            res = res * g + self.c[i]
        return res


# ---------------------------------------------------------------------------
# 5. Complete Verification Suite
# ---------------------------------------------------------------------------

def check_paper_verbatim(archive_path):
    print("[1/5] Checking verbatim LaTeX source in inputs/2610.07442v1.tex.json.gz ...")
    with gzip.open(archive_path, "rt", encoding="utf-8") as fh:
        payload = json.load(fh)

    assert isinstance(payload, list) and len(payload) == 1
    filename, tex = payload[0]
    assert filename == "Extended_avoidance.tex"
    lines = tex.splitlines()
    assert len(lines) == 1605, f"Expected 1605 lines, got {len(lines)}"

    required_anchors = [
        r"\title[Extended avoidance]{Pattern avoidance in alternating sign rectangles~I: Extended avoidance}",
        r"\section{Definitions}\label{sec:def}",
        r"\begin{prop}\label{lem:r=d}",
        r"\begin{prop}\label{lem:k=d}",
        r"\begin{equation}\label{eq:312_k=d}",
        r"\begin{thm}\label{lem:general}",
        r"\begin{conj}\label{conj:312-formula}",
        r"\begin{multline}\label{eq:conj312}",
        r"\s{312}{r}{k}{d} = \sum_{i=1}^{d} 2^{i-1} \binom{k}{i} \left( \binom{r-2}{d-i} - 2\binom{r-2}{d-i-2} \right) + \binom{r}{d}\\",
        r"+ \sum_{i \geq 0 }^{} C_{2i} \binom{r-1+2i}{d-1-2i} + 2 \sum_{i=1}^{d} (-1)^i \binom{r}{d-i},",
        r"We easily see that $F(0,k,0)=F(r,0,0)=1$ as well as $F(1,k,1)=k$ and $F(r,1,1)=r$.",
    ]
    for anchor in required_anchors:
        assert anchor in tex, f"Missing required verbatim anchor: {anchor}"

    # Verify exact 1-based line numbers for Conjecture 4.5 (lines 568-575)
    assert r"\begin{conj}\label{conj:312-formula}" in lines[567]
    assert r"\end{conj}" in lines[574]
    assert "F(1,k,1)=k" in lines[577]
    print("      OK: Verified Extended_avoidance.tex (1605 lines) and all verbatim anchors.")


def check_first_principles_small(sch, S):
    print("[2/5] Checking first-principles ASM and ASR enumeration for 0 <= d <= r, k <= 5 ...")
    # Verify 312-avoiding m x m ASMs match Sch_{m-1} for 1 <= m <= 7
    for m in range(1, 8):
        asm_cnt = count_312_avoiding_asms(m)
        assert asm_cnt == sch[m - 1], f"ASM count mismatch at m={m}: {asm_cnt} != {sch[m - 1]}"

    # Check d = 0 convention at r = 0 or k = 0
    for n in range(6):
        assert S[0][0][n] == 1 == eval_F_direct(0, n, 0)
        assert S[0][n][0] == 1 == eval_F_direct(n, 0, 0)

    total_asrs = 0
    total_triples = 11  # (0,0,0) plus 5+5 boundary zero triples above
    for r in range(1, 6):
        for k in range(1, 6):
            asrs = enumerate_all_asrs(r, k)
            total_asrs += len(asrs)
            counts = [0] * (min(r, k) + 1)
            for asr in asrs:
                d = sum(1 for i in range(r) if any(asr[i][j] != 0 for j in range(k)))
                assert d <= min(r, k)
                m0 = r + k - d
                ext = has_312_avoiding_asm_extension(asr, r, k, m0)
                if not ext and m0 + 1 <= 10:
                    assert not has_312_avoiding_asm_extension(asr, r, k, m0 + 1)
                if ext:
                    counts[d] += 1
            for d in range(min(r, k) + 1):
                f_val = eval_F_direct(r, k, d, binom_poly)
                assert counts[d] == S[d][r][k] == f_val, (
                    f"Mismatch at (r={r}, k={k}, d={d}): "
                    f"enum={counts[d]}, rec={S[d][r][k]}, F={f_val}"
                )
                total_triples += 1

    # Also check Corollary 5.3 (cor:312_d=r) against S[r][r][k] for 1 <= r <= k <= 12
    for r in range(1, 13):
        for k in range(r, 13):
            cor_sum = 0
            for i in range(r - 1, k):
                inner = 0
                for v in range(r):
                    inner += binom_poly(i + 1, r - 1 - v) * binom_poly(i + v, v)
                num = (i - r + 2) * inner
                assert num % (i + 1) == 0
                cor_sum += num // (i + 1)
            assert cor_sum == S[r][r][k]

    print(
        f"      OK: Verified 312-avoiding ASMs (1 <= m <= 7), all {total_asrs} valid ASRs "
        f"across {total_triples} triples (0 <= d <= r, k <= 5), and Corollary 5.3."
    )


def check_grid_equality(S, bcache, max_n):
    print(f"[3/5] Checking exact equality s^312_(r,k,d) == F(r,k,d) for all 0 <= d <= r, k <= {max_n} ...")
    cat_even = [catalan(2 * i) for i in range((max_n // 2) + 2)]
    count_40 = 0
    count_all = 0
    for r in range(max_n + 1):
        for k in range(max_n + 1):
            limit_d = r if r < k else k
            for d in range(limit_d + 1):
                f_val = eval_F_cached(r, k, d, bcache, cat_even)
                s_val = S[d][r][k]
                assert s_val == f_val, (
                    f"Formula mismatch at (r={r}, k={k}, d={d}): S={s_val}, F={f_val}"
                )
                count_all += 1
                if r <= 40 and k <= 40:
                    count_40 += 1

    # Also verify exact edge-convention discrepancy if binom(-1, 0) were set to 0
    naive_mismatches = []
    for r in range(41):
        for k in range(41):
            limit_d = r if r < k else k
            for d in range(limit_d + 1):
                if eval_F_direct(r, k, d, binom_naive_nonneg) != S[d][r][k]:
                    naive_mismatches.append((r, k, d))
    assert naive_mismatches == [(1, k, 1) for k in range(1, 41)]

    print(
        f"      OK: 0 mismatches across {count_40} triples up to 40 and all {count_all} triples "
        f"up to {max_n} (and isolated the exact 40 r=1=d triples sensitive to C(-1,0)=1)."
    )


def check_symbolic_fps_identities(sch, bcache):
    print("[4/5] Verifying every formal-power-series identity in PROOF.md over Q[[z]] mod z^43 ...")
    D = 42
    z = FPS([0, 1], D)
    one = FPS([1], D)
    cat_even = [catalan(2 * i) for i in range((D // 2) + 2)]

    # Build S(z) = (1 - z - sqrt(1 - 6z + z^2)) / (2z) using degree D + 1
    disc_sch_p = FPS([1, -6, 1], D + 1).sqrt_unit()
    num_sch_p = FPS([1, -1], D + 1) - disc_sch_p
    assert num_sch_p[0] == 0
    S_fps = FPS([num_sch_p[i + 1] * Fraction(1, 2) for i in range(D + 1)], D)

    # Lemma 2a: S(x) matches lattice-path DP Sch_m for 0 <= m <= D and satisfies x S^2 - (1-x)S + 1 = 0
    for m in range(D + 1):
        assert S_fps[m] == Fraction(sch[m])
    assert z * S_fps * S_fps - (one - z) * S_fps + one == FPS([], D)

    # Lemma 1a: Even Catalan series sum_{i>=0} C_{2i} u^{2i} = (sqrt(1+4u) - sqrt(1-4u)) / (4u)
    even_cat_lhs = FPS([cat_even[i // 2] if (i % 2 == 0) else 0 for i in range(D + 1)], D)
    sqrt_p4 = FPS([1, 4], D + 1).sqrt_unit()
    sqrt_m4 = FPS([1, -4], D + 1).sqrt_unit()
    diff_sq = sqrt_p4 - sqrt_m4
    assert diff_sq[0] == 0
    even_cat_rhs = FPS([diff_sq[i + 1] * Fraction(1, 4) for i in range(D + 1)], D)
    assert even_cat_lhs == even_cat_rhs

    # Substitution u = z(1 + z) into z(1+z)^{-1} sum_{i>=0} C_{2i} u^{2i}
    u_sub = z * (one + z)
    rad = (one - 4 * z - 4 * z * z).sqrt_unit()
    sub_lhs = z * (one + z).inv() * even_cat_lhs.compose(u_sub)
    sub_rhs = (one + 2 * z - rad) * Fraction(1, 4) * (one + z).pow_int(-2)
    assert sub_lhs == sub_rhs

    # Lemma 1b: Master GF Phi_{r,k}(z) = (1 + z)^{r-2} G_k(z) matches F(r, k, d) for 0 <= r, k <= 40, 0 <= d <= r
    H2 = (3 + 2 * z - rad) * Fraction(1, 4)
    G_cache = {}
    for k in range(-42, 42):
        G_cache[k] = (one - 2 * z * z) * Fraction(1, 2) * (one + 2 * z).pow_int(k) + H2

    one_plus_z_pow = {e: (one + z).pow_int(e) for e in range(-45, 43)}

    for r in range(41):
        for k in range(41):
            phi = one_plus_z_pow[r - 2] * G_cache[k]
            for d in range(r + 1):
                assert phi[d] == Fraction(eval_F_cached(r, k, d, bcache, cat_even))

    # Lemma 2b & 2c: Schroeder evaluations at z/((1+z)(1+2z)) and z/(1+z)
    arg1 = z.mul_inv((one + z) * (one + 2 * z))
    assert S_fps.compose(arg1) == one + 2 * z

    arg2 = z.mul_inv(one + z)
    disc_f_p = FPS([1, -4, -4], D + 1).sqrt_unit()
    rhs_arg2 = FPS([-disc_f_p[i + 1] * Fraction(1, 2) for i in range(D + 1)], D)
    assert S_fps.compose(arg2) == rhs_arg2
    assert (-(one + 2 * z + rad) * Fraction(1, 4)) * S_fps.compose(arg2) == -H2

    # Lemma 3: Master formal power series recurrence in Q[[z]] mod z^41 across representative (r, k)
    D_rec = 40
    for r in [-3, 0, 1, 2, 5, 12, 25, 40]:
        for k in [-2, 0, 1, 2, 5, 14, 30, 40]:
            lhs = one_plus_z_pow[r - 2] * (G_cache[k] - G_cache[k - 1])
            rhs = z * one_plus_z_pow[r - 3] * G_cache[k - 1]
            for m in range(D_rec):
                term = (
                    one_plus_z_pow[r - 3 - m] * G_cache[k - 1 - m]
                    - one_plus_z_pow[r - 2 - m]
                )
                rhs = rhs + Fraction(sch[m]) * term.shift(m + 1)
            for deg_i in range(D_rec + 1):
                assert lhs[deg_i] == rhs[deg_i]

    # Lemma 4: Formal residue invariance & diagonal boundary identities F(r, r-1, r) = 0, F(r, r, r) = Sch_{r-1}
    # Check formal residue invariance Res_{z=0} z^m dz == Res_{u=0} z(u)^m z'(u) du on Laurent monomials
    z_of_u = (S_fps - 1) * Fraction(1, 2)
    zp_of_u = z_of_u.deriv()
    assert arg1.compose(z_of_u) == z
    assert z_of_u.compose(arg1) == z
    # Write z(u) = u * g(u) with g(0) != 0 so Laurent powers z(u)^m = u^m * g(u)^m are exact up to u^(D - |m|)
    g_of_u = FPS([z_of_u[i + 1] for i in range(D)], D - 1)
    gp_trunc = FPS([zp_of_u[i] for i in range(D)], D - 1)
    for m_exp in range(-12, 13):
        # [u^-1] (u^m g(u)^m z'(u)) == [u^(-1 - m)] (g(u)^m z'(u))
        integrand = g_of_u.pow_int(m_exp) * gp_trunc
        res_u = integrand[-1 - m_exp]
        expected_res = Fraction(1) if m_exp == -1 else Fraction(0)
        assert res_u == expected_res

    # Lemma 4b: (1 - w) H2(w / (1 - w)) == (1 + w S(w)) / 2
    arg_w = z.mul_inv(one - z)
    assert (one - z) * H2.compose(arg_w) == (one + z * S_fps) * Fraction(1, 2)

    # Lemma 4c: 1 / (2(1 + z(u))) == (1 - u S(u)) / 2 and (1 + 2z(u)) / (2(1 + z(u))) == (1 + u S(u)) / 2
    assert (2 * (one + z_of_u)).inv() == (one - z * S_fps) * Fraction(1, 2)
    assert (one + 2 * z_of_u).mul_inv(2 * (one + z_of_u)) == (one + z * S_fps) * Fraction(1, 2)

    # Verify directly [z^r] Phi_{r, r-1}(z) == 0 and [z^r] Phi_{r, r}(z) == Sch_{r-1} for 1 <= r <= 40
    for r in range(1, 41):
        phi_rm1 = one_plus_z_pow[r - 2] * G_cache[r - 1]
        phi_r = one_plus_z_pow[r - 2] * G_cache[r]
        assert phi_rm1[r] == Fraction(0)
        assert phi_r[r] == Fraction(sch[r - 1])

    # Lemma 5: Universal Chu-Vandermonde linear operator identity for all monomials z^n (0 <= n <= k < r <= 40)
    for n in range(41):
        for k in range(n, 41):
            for r in range(k + 1, 42):
                lhs_cv = bcache[r - 2][k - n]
                rhs_cv = 0
                for j in range(n, k + 1):
                    rhs_cv += binom_poly(j - 2, j - n) * bcache[r - j - 1][k - j]
                assert lhs_cv == rhs_cv

    print("      OK: Verified Lemmas 1, 2, 3, 4, and 5 symbolically over Q[[z]] mod z^43.")


def check_negative_controls(S):
    print("[5/5] Running 7 negative-control perturbations against ground-truth S[d][r][k] ...")

    def mutant_pow2(r, k, d):
        # Perturb 2^{i-1} -> 2^i
        val = eval_F_direct(r, k, d)
        extra = 0
        for i in range(1, d + 1):
            extra += (1 << (i - 1)) * binom_poly(k, i) * (
                binom_poly(r - 2, d - i) - 2 * binom_poly(r - 2, d - i - 2)
            )
        return val + extra

    def mutant_inner_coeff(r, k, d):
        # Perturb -2 * C(r-2, d-i-2) -> -1 * C(r-2, d-i-2)
        val = eval_F_direct(r, k, d)
        extra = 0
        for i in range(1, d + 1):
            extra += (1 << (i - 1)) * binom_poly(k, i) * binom_poly(r - 2, d - i - 2)
        return val + extra

    def mutant_upper_shift(r, k, d):
        # Perturb C(r-2, d-i) -> C(r-1, d-i)
        s1 = 0
        for i in range(1, d + 1):
            s1 += (1 << (i - 1)) * binom_poly(k, i) * (
                binom_poly(r - 1, d - i) - 2 * binom_poly(r - 2, d - i - 2)
            )
        return eval_F_direct(r, 0, d) + s1

    def mutant_binom_rd(r, k, d):
        # Perturb +C(r, d) -> +2*C(r, d)
        return eval_F_direct(r, k, d) + binom_poly(r, d)

    def mutant_catalan_index(r, k, d):
        # Perturb C_{2i} -> C_i
        s3_bad = 0
        s3_good = 0
        i = 0
        while d - 1 - 2 * i >= 0:
            b = binom_poly(r - 1 + 2 * i, d - 1 - 2 * i)
            s3_bad += catalan(i) * b
            s3_good += catalan(2 * i) * b
            i += 1
        return eval_F_direct(r, k, d) - s3_good + s3_bad

    def mutant_alt_coeff(r, k, d):
        # Perturb +2 * sum (-1)^i C(r, d-i) -> +1 * sum (-1)^i C(r, d-i)
        half_s4 = 0
        for i in range(1, d + 1):
            sign = -1 if (i % 2 == 1) else 1
            half_s4 += sign * binom_poly(r, d - i)
        return eval_F_direct(r, k, d) - half_s4

    def mutant_naive_binom(r, k, d):
        # Perturb C(-1, 0) = 1 -> 0
        return eval_F_direct(r, k, d, binom_naive_nonneg)

    mutants = [
        ("2^{i-1} -> 2^i", mutant_pow2),
        ("-2*C(r-2,d-i-2) -> -1*C(r-2,d-i-2)", mutant_inner_coeff),
        ("C(r-2,d-i) -> C(r-1,d-i)", mutant_upper_shift),
        ("+C(r,d) -> +2*C(r,d)", mutant_binom_rd),
        ("C_{2i} -> C_i", mutant_catalan_index),
        ("2*sum(-1)^i C(r,d-i) -> 1*sum", mutant_alt_coeff),
        ("C(-1,0)=1 -> C(-1,0)=0", mutant_naive_binom),
    ]

    for label, fn in mutants:
        first_fail = None
        for r in range(6):
            for k in range(6):
                limit_d = r if r < k else k
                for d in range(limit_d + 1):
                    if fn(r, k, d) != S[d][r][k]:
                        first_fail = (r, k, d, fn(r, k, d), S[d][r][k])
                        break
                if first_fail is not None:
                    break
            if first_fail is not None:
                break
        assert first_fail is not None, f"Mutant {label} unexpectedly survived on 0..5!"
        r, k, d, got, want = first_fail
        print(f"      Caught mutant [{label}] at (r={r}, k={k}, d={d}): got {got} != {want}")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    archive_path = os.path.join(here, "inputs", "2610.07442v1.tex.json.gz")
    check_paper_verbatim(archive_path)

    max_n = 80
    sch = compute_schroeder_dp(max_n + 2)
    bcache = build_binom_cache(2 * max_n + 4)
    S = compute_recurrence_table(max_n, sch, bcache)

    check_first_principles_small(sch, S)
    check_grid_equality(S, bcache, max_n)
    check_symbolic_fps_identities(sch, bcache)
    check_negative_controls(S)

    print("ALL VERIFICATION CHECKS PASSED (exit 0).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
