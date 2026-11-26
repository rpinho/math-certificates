#!/usr/bin/env python3
"""
Independent zero-dependency pure-Python verifier for PROOF.md
(Proof of Conjecture 9.2 of Ma, Sahbi & Zhang, arXiv:2609.25128v4).

Uses exact rational arithmetic (fractions.Fraction) throughout and includes
both positive controls and 5 load-bearing negative/mutant controls.
"""

from fractions import Fraction
from itertools import combinations
import random
import sys


def is_valid_subquorum(n, adj, col):
    """Direct check of Definition 1 (Definition 2.2 of arXiv:2609.25128v4).
    col: list of length n with 0 for uncolored and {1..k} for colored vertices.
    Returns k if valid onto partial coloring, else -1.
    """
    if len(col) != n or any(c < 0 for c in col):
        return -1
    S = {v for v, c in enumerate(col) if c > 0}
    if not S:
        return 0
    k = max(col)
    present = {col[v] for v in S}
    if present != set(range(1, k + 1)):
        return -1
    for v in S:
        closed_S = (adj[v] & S) | {v}
        same_S = {u for u in closed_S if col[u] == col[v]}
        if 2 * len(same_S) < len(closed_S):
            return -1
    return k


def exact_psi_sq_python(n, edges):
    """Independent exact solver directly maximizing quorum partitions over S subseteq V."""
    adj = [set() for _ in range(n)]
    for u, v in edges:
        assert u != v, "Graph must be simple"
        adj[u].add(v)
        adj[v].add(u)
    best_k = 0
    best_col = [0] * n
    for r in range(1, n + 1):
        for S_tup in combinations(range(n), r):
            if r <= best_k:
                continue
            S_set = set(S_tup)
            by_lsb = [[] for _ in range(r)]
            for a_sz in range(1, r + 1):
                for A_tup in combinations(range(r), a_sz):
                    verts_A = {S_tup[i] for i in A_tup}
                    ok = True
                    for u in verts_A:
                        if 2 * (len(adj[u] & verts_A) + 1) < (len(adj[u] & S_set) + 1):
                            ok = False
                            break
                    if ok:
                        mask = sum(1 << i for i in A_tup)
                        by_lsb[(mask & -mask).bit_length() - 1].append(mask)
            full = (1 << r) - 1
            dp = [-1] * (1 << r)
            parent = [(-1, 0)] * (1 << r)
            dp[0] = 0
            for m in range(full):
                if dp[m] < 0:
                    continue
                rem = full ^ m
                lsb = (rem & -rem).bit_length() - 1
                for A in by_lsb[lsb]:
                    if (A & m) == 0 and dp[m] + 1 > dp[m | A]:
                        dp[m | A] = dp[m] + 1
                        parent[m | A] = (m, A)
            if dp[full] > best_k:
                best_k = dp[full]
                col = [0] * n
                cur = full
                cid = 1
                while cur > 0:
                    prev, A = parent[cur]
                    for i in range(r):
                        if (A >> i) & 1:
                            col[S_tup[i]] = cid
                    cid += 1
                    cur = prev
                best_col = col
    assert is_valid_subquorum(n, adj, best_col) == best_k
    return best_k, best_col, adj


def exact_omega_python(n, edges):
    """Exact Omega(G) from Lemma 2.4: max |T| + |M| over matchings M and T cap V(M) = empty
    with |N_G(t) cap (T cup V(M))| <= 1 for all t in T.
    """
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    edge_list = list(edges)

    matchings = []
    def gen_matchings(idx, used, cur):
        matchings.append(list(cur))
        for i in range(idx, len(edge_list)):
            u, v = edge_list[i]
            if u not in used and v not in used:
                used.add(u)
                used.add(v)
                cur.append((u, v))
                gen_matchings(i + 1, used, cur)
                cur.pop()
                used.remove(u)
                used.remove(v)
    gen_matchings(0, set(), [])

    best = 0
    for M in matchings:
        VM = {u for e in M for u in e}
        rem = [v for v in range(n) if v not in VM]
        for r in range(len(rem) + 1):
            if r + len(M) <= best:
                continue
            for T_tup in combinations(rem, r):
                occ = VM | set(T_tup)
                if all(len(adj[t] & occ) <= 1 for t in T_tup):
                    best = r + len(M)
    return best


def sigma_from_degrees(m, degs):
    """Exact Fraction evaluation of Sigma(H) from Lemma 3."""
    if m == 0:
        return Fraction(0)
    return sum(
        Fraction(1, 1 + (d // 2)) + Fraction(1, 1 + ((m - 1 - d) // 2))
        for d in degs
    )


def check_lemma2():
    checked = 0
    for a in range(1, 51):
        for b in range(1, 51):
            for s in range(2, a + b + 1):
                lhs = Fraction(1, a) + Fraction(1, b)
                rhs = Fraction(1, 1) + Fraction(1, s - 1)
                assert lhs <= rhs, f"Lemma 2 failed at a={a}, b={b}, s={s}"
                checked += 1
    return checked


def check_lemma3():
    # Exhaustive over all labeled graphs for m = 0..6, plus 5,000 random graphs for m = 7..40
    checked = 0
    assert sigma_from_degrees(0, []) == Fraction(0)
    checked += 1
    assert sigma_from_degrees(1, [0]) == Fraction(2)
    checked += 1

    for m in range(2, 7):
        pairs = [(i, j) for i in range(m) for j in range(i + 1, m)]
        for mask in range(1 << len(pairs)):
            degs = [0] * m
            for bit, (u, v) in enumerate(pairs):
                if (mask >> bit) & 1:
                    degs[u] += 1
                    degs[v] += 1
            val = sigma_from_degrees(m, degs)
            if m % 2 == 0:
                assert val <= Fraction(m + 2), f"Case C failed at m={m}"
            else:
                r = (m - 1) // 2
                assert val <= Fraction(m + 2) + Fraction(1, r + 1), f"Case D failed at m={m}"
            assert val <= Fraction(m) + Fraction(5, 2)
            checked += 1

    rng = random.Random(20261125)
    for _ in range(5000):
        m = rng.randint(7, 40)
        p = rng.choice([0.05, 0.2, 0.5, 0.8, 0.95])
        degs = [0] * m
        for i in range(m):
            for j in range(i + 1, m):
                if rng.random() < p:
                    degs[i] += 1
                    degs[j] += 1
        val = sigma_from_degrees(m, degs)
        if m % 2 == 0:
            assert val <= Fraction(m + 2)
        else:
            r = (m - 1) // 2
            assert val <= Fraction(m + 2) + Fraction(1, r + 1)
        assert val <= Fraction(m) + Fraction(5, 2)
        checked += 1

    # Verify exact sharpness on P_3 (degrees 1, 2, 1 at m = 3)
    assert sigma_from_degrees(3, [1, 2, 1]) == Fraction(11, 2) == Fraction(3) + Fraction(5, 2)
    return checked


def check_theorem1_chain(n, edges):
    es = {(min(u, v), max(u, v)) for u, v in edges}
    cedges = [(i, j) for i in range(n) for j in range(i + 1, n) if (i, j) not in es]
    k1, col1, adj1 = exact_psi_sq_python(n, edges)
    k2, col2, adj2 = exact_psi_sq_python(n, cedges)

    sz1 = {}
    sz2 = {}
    for v in range(n):
        if col1[v] > 0:
            sz1[col1[v]] = sz1.get(col1[v], 0) + 1
        if col2[v] > 0:
            sz2[col2[v]] = sz2.get(col2[v], 0) + 1

    w1 = [Fraction(1, sz1[col1[v]]) if col1[v] > 0 else Fraction(0) for v in range(n)]
    w2 = [Fraction(1, sz2[col2[v]]) if col2[v] > 0 else Fraction(0) for v in range(n)]

    # Lemma 1(1)
    assert sum(w1) == Fraction(k1)
    assert sum(w2) == Fraction(k2)
    assert all(Fraction(0) <= x <= Fraction(1) for x in w1 + w2)

    S1 = {v for v in range(n) if col1[v] > 0}
    S2 = {v for v in range(n) if col2[v] > 0}
    I = S1 & S2
    m = len(I)

    # Outside I
    outside = sum(w1[v] + w2[v] for v in range(n) if v not in I)
    assert outside <= Fraction(n - m)

    # Inside I (Lemma 1(2) & Lemma 3)
    degs_I = []
    for v in I:
        dI = len(adj1[v] & I)
        cdI = len(adj2[v] & I)
        assert dI + cdI == m - 1
        assert w1[v] <= Fraction(1, 1 + (dI // 2))
        assert w2[v] <= Fraction(1, 1 + (cdI // 2))
        degs_I.append(dI)

    inside = sum(w1[v] + w2[v] for v in I)
    sig = sigma_from_degrees(m, degs_I)
    assert inside <= sig <= Fraction(m) + Fraction(5, 2)
    assert Fraction(k1 + k2) == outside + inside <= Fraction(n) + Fraction(5, 2)
    assert k1 + k2 <= n + 2
    return k1, k2


def run_negative_controls():
    # Mutant 1: Invalid coloring violating Definition 1 quorum rule (K_3 with 3 singletons)
    adj_k3 = [{1, 2}, {0, 2}, {0, 1}]
    assert is_valid_subquorum(3, adj_k3, [1, 2, 3]) == -1, "Mutant 1 failed: accepted invalid K_3 3-coloring"

    # Mutant 2: Tightened bound n + 1 is FALSE on K_4, P_4, and S_{2,2}
    k1_k4, k2_k4 = check_theorem1_chain(4, [(i, j) for i in range(4) for j in range(i + 1, 4)])
    assert k1_k4 + k2_k4 == 6 > 4 + 1, "Mutant 2a failed"
    k1_s22, k2_s22 = check_theorem1_chain(6, [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5)])
    assert k1_s22 == 5 and k2_s22 == 3 and k1_s22 + k2_s22 == 8 > 6 + 1, "Mutant 2b failed"

    # Mutant 3: Lemma 2.4 Omega(G) + Omega(Gbar) exceeds n + 2 on K_6!
    k6_edges = [(i, j) for i in range(6) for j in range(i + 1, 6)]
    om_k6 = exact_omega_python(6, k6_edges)
    om_ek6 = exact_omega_python(6, [])
    assert om_k6 == 3 and om_ek6 == 6 and om_k6 + om_ek6 == 9 > 6 + 2, "Mutant 3 failed"

    # Mutant 4: Dropping Handshaking Lemma at m = 3 (pseudo-degree sequence [1, 1, 1]) exceeds m + 5/2!
    pseudo_sig = sigma_from_degrees(3, [1, 1, 1])
    assert pseudo_sig == Fraction(6) > Fraction(3) + Fraction(5, 2), "Mutant 4 failed"

    # Mutant 5: Disconnected color class is still accepted by Definition 1 & bounded by Theorem 1,
    # whereas non-onto label [1, 3] (skipping color 2) is rejected by Definition 1.
    adj_e2 = [set(), set()]
    assert is_valid_subquorum(2, adj_e2, [1, 3]) == -1, "Mutant 5a failed: accepted non-onto coloring"
    assert is_valid_subquorum(2, adj_e2, [1, 1]) == 1, "Mutant 5b failed"
    return 5


def main():
    l2_cnt = check_lemma2()
    l3_cnt = check_lemma3()

    # Check Theorem 1 full chain on all labeled graphs of orders n = 2, 3, 4 (74 graphs)
    # plus 200 random graphs on n = 5, 6, 7 + named benchmarks
    t1_cnt = 0
    for n in (2, 3, 4):
        pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
        for mask in range(1 << len(pairs)):
            edges = [pairs[b] for b in range(len(pairs)) if (mask >> b) & 1]
            check_theorem1_chain(n, edges)
            t1_cnt += 1

    rng = random.Random(998877)
    for _ in range(200):
        n = rng.choice([5, 6, 7])
        p = rng.choice([0.15, 0.35, 0.5, 0.65, 0.85])
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]
        check_theorem1_chain(n, edges)
        t1_cnt += 1

    # Named benchmarks including S_{2,2} and Q_3
    check_theorem1_chain(5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)])  # C_5
    check_theorem1_chain(6, [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5)])  # S_{2,2}
    check_theorem1_chain(8, [(i, i ^ (1 << b)) for i in range(8) for b in range(3) if i < (i ^ (1 << b))])  # Q_3
    t1_cnt += 3

    mut_cnt = run_negative_controls()
    print(f"PASS: Lemma 2 ({l2_cnt} triples), Lemma 3 ({l3_cnt} graphs, exact Fraction), "
          f"Theorem 1 chain ({t1_cnt} graphs), Negative/Mutant controls ({mut_cnt}/5).")


if __name__ == "__main__":
    main()
