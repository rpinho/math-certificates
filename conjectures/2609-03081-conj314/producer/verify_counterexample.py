#!/usr/bin/env python3
"""
Zero-dependency pure-Python exact integer verifier for Lewis & Won (arXiv:2609.03081v1)
Conjecture 3.14 (conj:maxlayered) and Conjecture 3.9 (conj:skewmerged) witnesses.

Uses only Python standard library modules (json, pathlib, sys) and exact arbitrary-precision
integer arithmetic throughout. Builds crossword grids and across/down word bipartite graphs
directly from Section 2 and Section 3.2 of Lewis & Won (arXiv:2609.03081v1), cross-checking
exact Gray-code Ryser permanent against two independent word-level memoized backtracking
permanent solvers (across-word order and down-word order).
"""

import json
from pathlib import Path
import sys


def build_crossword_grid_from_perm(w):
    """Return n x n matrix G where G[r][c] == 1 iff square (r+1, c+1) is black."""
    n = len(w)
    if sorted(w) != list(range(1, n + 1)):
        raise ValueError(f"Not a valid permutation of 1..{n}: {w}")
    grid = []
    for r in range(n):
        row = [0] * n
        row[w[r] - 1] = 1
        grid.append(row)
    return grid


def extract_words_and_biadjacency(grid):
    """
    Directly apply Section 2 definitions of Lewis & Won (arXiv:2609.03081v1):
    - An across word is a maximal contiguous sequence of white (0) squares in a row.
    - A down word is a maximal contiguous sequence of white (0) squares in a column.
    - Biadjacency matrix B has B[i][j] = 1 iff across word i and down word j share a square.
    """
    m_rows = len(grid)
    n_cols = len(grid[0]) if m_rows > 0 else 0

    across_words = []
    for r in range(m_rows):
        c = 0
        while c < n_cols:
            if grid[r][c] == 0:
                cells = set()
                while c < n_cols and grid[r][c] == 0:
                    cells.add((r, c))
                    c += 1
                across_words.append(cells)
            else:
                c += 1

    down_words = []
    for c in range(n_cols):
        r = 0
        while r < m_rows:
            if grid[r][c] == 0:
                cells = set()
                while r < m_rows and grid[r][c] == 0:
                    cells.add((r, c))
                    r += 1
                down_words.append(cells)
            else:
                r += 1

    num_a = len(across_words)
    num_d = len(down_words)
    biadj = []
    for i in range(num_a):
        row = []
        a_cells = across_words[i]
        for j in range(num_d):
            row.append(1 if (a_cells & down_words[j]) else 0)
        biadj.append(row)

    return across_words, down_words, biadj


def perm_ryser_exact(biadj):
    """Exact integer Gray-code Ryser permanent of a square {0,1}-matrix."""
    num_a = len(biadj)
    if num_a == 0:
        return 1
    num_d = len(biadj[0])
    if num_a != num_d:
        return 0
    m = num_a

    col_rows = [[] for _ in range(m)]
    for i in range(m):
        for j in range(m):
            if biadj[i][j]:
                col_rows[j].append(i)

    row_sums = [0] * m
    zero_cnt = m
    total = 0
    gray = 0
    sign = 1 if (m % 2 == 0) else -1

    for step in range(1, 1 << m):
        new_gray = step ^ (step >> 1)
        diff = gray ^ new_gray
        col_idx = diff.bit_length() - 1
        adding = (new_gray & diff) != 0
        gray = new_gray
        sign = -sign

        if adding:
            for r in col_rows[col_idx]:
                if row_sums[r] == 0:
                    zero_cnt -= 1
                row_sums[r] += 1
        else:
            for r in col_rows[col_idx]:
                row_sums[r] -= 1
                if row_sums[r] == 0:
                    zero_cnt += 1

        if zero_cnt == 0:
            prod = 1
            for s in row_sums:
                prod *= s
            total += sign * prod

    return total


def perm_backtrack_exact(biadj):
    """
    Exact memoized backtracking permanent directly on biadjacency matrix B.
    Places 1 rook in each row i = 0..m-1 (choosing an unmatched column j with B[i][j] == 1).
    Any column j whose last nonzero row is i must be matched by step i (else permanent is 0),
    and once matched and past its last nonzero row, its bit is retired from the memo key.
    """
    num_a = len(biadj)
    if num_a == 0:
        return 1
    num_d = len(biadj[0])
    if num_a != num_d:
        return 0
    m = num_a

    row_neighbors = [0] * m
    last_row_for_col = [-1] * m
    for i in range(m):
        mask = 0
        for j in range(m):
            if biadj[i][j]:
                mask |= (1 << j)
                last_row_for_col[j] = i
        row_neighbors[i] = mask

    for j in range(m):
        if last_row_for_col[j] == -1:
            return 0

    expire_mask_at_row = [0] * m
    for j in range(m):
        expire_mask_at_row[last_row_for_col[j]] |= (1 << j)

    states = {0: 1}
    for i in range(m):
        nbrs = row_neighbors[i]
        exp_mask = expire_mask_at_row[i]
        keep_mask = ((1 << m) - 1) ^ exp_mask
        next_states = {}

        for matched_mask, ways in states.items():
            avail = nbrs & (~matched_mask)
            while avail:
                bit = avail & (-avail)
                avail ^= bit
                new_matched = matched_mask | bit
                if (new_matched & exp_mask) != exp_mask:
                    continue
                proj_mask = new_matched & keep_mask
                next_states[proj_mask] = next_states.get(proj_mask, 0) + ways

        states = next_states
        if not states:
            return 0

    return states.get(0, 0)


def transpose_matrix(mat):
    if not mat:
        return []
    rows = len(mat)
    cols = len(mat[0])
    return [[mat[r][c] for r in range(rows)] for c in range(cols)]


def count_rook_placements_verified(w, check_ryser=False):
    """Compute |RP(Grid(w))| via two independent exact word-backtracking orders (+ Ryser if requested)."""
    grid = build_crossword_grid_from_perm(w)
    across_words, down_words, biadj = extract_words_and_biadjacency(grid)
    if len(w) >= 2:
        assert len(across_words) == 2 * len(w) - 2
        assert len(down_words) == 2 * len(w) - 2
    c_across = perm_backtrack_exact(biadj)
    c_down = perm_backtrack_exact(transpose_matrix(biadj))
    if c_across != c_down:
        raise AssertionError(f"Mismatch across={c_across} vs down={c_down} on {w}")
    if check_ryser:
        c_ryser = perm_ryser_exact(biadj)
        if c_ryser != c_across:
            raise AssertionError(f"Mismatch ryser={c_ryser} vs backtrack={c_across} on {w}")
    return c_across


def stirling_second_kind_table(max_n):
    s = [[0] * (max_n + 1) for _ in range(max_n + 1)]
    s[0][0] = 1
    for i in range(1, max_n + 1):
        for k in range(1, i + 1):
            s[i][k] = k * s[i - 1][k] + s[i - 1][k - 1]
    return s


def factorial_int(k):
    res = 1
    for i in range(2, k + 1):
        res *= i
    return res


def prop_3_15_count_layered(n, m1, m2, stirling_tbl):
    """Exact Proposition 3.15 formula for layered permutation of shape (m1, 1, ..., 1, m2)."""
    if m1 <= 0 or m2 <= 0 or m1 + m2 > n:
        raise ValueError(f"Invalid (n, m1, m2) = ({n}, {m1}, {m2})")
    m = m1 if m1 < m2 else m2
    exp_mid = n - m1 - m2
    total = 0
    for k in range(1, m + 1):
        term = (k ** exp_mid) * factorial_int(k)
        total += stirling_tbl[m1][k] * stirling_tbl[m2][k] * (term * term)
    return total


def build_layered_from_composition(comp):
    w = []
    offset = 0
    for block_sz in comp:
        for x in range(block_sz, 0, -1):
            w.append(offset + x)
        offset += block_sz
    return w


def is_layered_m_1_m(w):
    n = len(w)
    if w == list(range(1, n + 1)):
        return True
    for m in range(1, (n // 2) + 1):
        comp = [m] + [1] * (n - 2 * m) + [m]
        if w == build_layered_from_composition(comp):
            return True
    return False


def contains_2143_or_3412(w):
    n = len(w)
    for a in range(n):
        wa = w[a]
        for b in range(a + 1, n):
            wb = w[b]
            for c in range(b + 1, n):
                wc = w[c]
                for d in range(c + 1, n):
                    wd = w[d]
                    if wb < wa < wd < wc:
                        return True, "2143", (a + 1, b + 1, c + 1, d + 1)
                    if wc < wd < wa < wb:
                        return True, "3412", (a + 1, b + 1, c + 1, d + 1)
    return False, None, None


def run_sanity_controls():
    print("[Controls] Running positive and negative sanity controls...")
    stirling = stirling_second_kind_table(25)

    # 1. Non-permutation grids from Equation (2.1) of Lewis & Won (must admit 0 rook placements)
    g_unequal = [[0, 0, 1], [0, 0, 0], [0, 1, 0]]
    _, _, b_unequal = extract_words_and_biadjacency(g_unequal)
    assert perm_ryser_exact(b_unequal) == 0 and perm_backtrack_exact(b_unequal) == 0

    g_hall_fail = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    _, _, b_hall = extract_words_and_biadjacency(g_hall_fail)
    assert perm_ryser_exact(b_hall) == 0 and perm_backtrack_exact(b_hall) == 0

    # 2. Baseline r(1..10) layered (m, 1*, m) values with Ryser cross-check for n <= 9
    expected_r = {
        1: (1, [1]),
        2: (1, [1, 1]),
        3: (1, [1, 1, 1]),
        4: (5, [2, 2]),
        5: (17, [2, 1, 2]),
        6: (73, [3, 3]),
        7: (469, [3, 1, 3]),
        8: (3493, [3, 1, 1, 3]),
        9: (28549, [3, 1, 1, 1, 3]),
        10: (255569, [4, 1, 1, 4]),
    }
    for n, (exp_val, comp) in expected_r.items():
        w = build_layered_from_composition(comp)
        rp = count_rook_placements_verified(w, check_ryser=(n <= 9))
        assert rp == exp_val, f"Control r({n}) failed: got {rp}, expected {exp_val}"
        if n >= 2:
            m = comp[0]
            f_val = prop_3_15_count_layered(n, m, m, stirling)
            assert f_val == exp_val

    # 3. Zenodo 10.5281/zenodo.22679647 Conjecture 3.10 witness (n=8 -> 155)
    rp_155 = count_rook_placements_verified([2, 7, 4, 8, 1, 6, 3, 5], check_ryser=True)
    assert rp_155 == 155, f"Expected 155, got {rp_155}"

    # 4. Theorem 3.7 and Proposition 3.8 examples from the paper
    assert count_rook_placements_verified([5, 1, 3, 4, 2, 6], check_ryser=True) == 1
    assert count_rook_placements_verified([1, 3, 7, 6, 2, 4, 5], check_ryser=True) == 2
    assert count_rook_placements_verified([5, 4, 1, 2, 6, 7, 3], check_ryser=True) == 2

    # 5. Negative control at n=16: 2-shell layered (5, 2, 1, 1, 2, 5) does NOT beat L(16)
    w16_comp = build_layered_from_composition([5, 2, 1, 1, 2, 5])
    rp16_comp = count_rook_placements_verified(w16_comp, check_ryser=False)
    l16 = prop_3_15_count_layered(16, 5, 5, stirling)
    assert rp16_comp == 4250088142445 and l16 == 4493953750501 and rp16_comp < l16

    print("[Controls] All positive and negative controls PASSED.")


def verify_witness_file(witness_path):
    data = json.loads(Path(witness_path).read_text(encoding="utf-8"))
    conjecture = data["conjecture"]
    n = data["n"]
    w = data["permutation"]
    claimed_rp = data["rook_placements"]

    if not isinstance(n, int) or len(w) != n or not all(isinstance(x, int) for x in w):
        raise ValueError("Invalid witness format.")

    actual_rp = count_rook_placements_verified(w, check_ryser=(n <= 9))
    if actual_rp != claimed_rp:
        raise AssertionError(f"Claimed RP {claimed_rp} != verified exact RP {actual_rp}")

    if conjecture == "3.14":
        stirling = stirling_second_kind_table(n + 2)
        max_sym_layered = 0
        best_m = None
        all_sym_values = {}
        for m in range(1, (n // 2) + 1):
            val_formula = prop_3_15_count_layered(n, m, m, stirling)
            w_m = build_layered_from_composition([m] + [1] * (n - 2 * m) + [m])
            val_grid = count_rook_placements_verified(w_m, check_ryser=(n <= 9))
            if val_formula != val_grid:
                raise AssertionError(f"Prop 3.15 mismatch at m={m}: {val_formula} vs {val_grid}")
            all_sym_values[m] = val_formula
            if val_formula > max_sym_layered:
                max_sym_layered = val_formula
                best_m = m

        # Also check all asymmetric (m1, 1, ..., 1, m2) via Proposition 3.15
        max_asym_layered = 0
        for m1 in range(1, n):
            for m2 in range(1, n - m1 + 1):
                val = prop_3_15_count_layered(n, m1, m2, stirling)
                if val > max_asym_layered:
                    max_asym_layered = val
        assert max_asym_layered == max_sym_layered

        if is_layered_m_1_m(w):
            raise AssertionError("Witness itself has shape (m, 1, ..., 1, m)!")
        if actual_rp <= max_sym_layered:
            raise AssertionError(
                f"NOT a counterexample to Conj 3.14: |RP(Grid(w))| = {actual_rp} <= {max_sym_layered}"
            )

        diff = actual_rp - max_sym_layered
        print("[Verified Conjecture 3.14 Counterexample]")
        print(f"  n = {n}")
        print(f"  w = {w}")
        print(f"  |RP(Grid(w))|                    = {actual_rp}")
        print(f"  max_(m,1*,m) |RP| (at m = {best_m})     = {max_sym_layered}")
        print(f"  strict excess over (m,1,...,1,m) = +{diff}")
        for m, v in sorted(all_sym_values.items()):
            print(f"    shape ({m}, 1^{n - 2 * m}, {m}): |RP| = {v}")

    elif conjecture == "3.9":
        has_pat, pat_name, idx4 = contains_2143_or_3412(w)
        if not has_pat:
            raise AssertionError("Witness avoids 2143 and 3412 (it IS skew-merged)!")
        if actual_rp not in (1, 2):
            raise AssertionError(f"Witness has |RP| = {actual_rp}, not in {{1, 2}}!")
        print("[Verified Conjecture 3.9 Counterexample]")
        print(f"  n = {n}, w = {w}, pattern {pat_name} at {idx4}, |RP(Grid(w))| = {actual_rp}")
    else:
        raise ValueError(f"Unknown conjecture id: {conjecture}")


def main():
    run_sanity_controls()
    witness_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("witness.json")
    verify_witness_file(witness_path)
    print("ALL VERIFICATION CHECKS PASSED.")


if __name__ == "__main__":
    main()
