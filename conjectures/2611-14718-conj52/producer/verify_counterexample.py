#!/usr/bin/env python3
"""
Standalone, zero-dependency pure-Python exact rational verifier for counterexamples
to Conjecture 5.2 of Higuita-Diaz, Lopez & Roldan-Correa (arXiv:2611.14718v2).

Strictly uses Python's built-in `fractions.Fraction` and exact integers only
(NO floating-point arithmetic anywhere in distribution or dominance checks).
"""

from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path
import sys


def validate_simple_graph(n, edges):
    """Validate simple undirected graph structure and compute adjacency masks & connectivity."""
    if not isinstance(n, int) or n < 1:
        raise ValueError(f"Invalid vertex count n={n}")
    adj = [0] * n
    seen_edges = set()
    for e in edges:
        if not isinstance(e, (list, tuple)) or len(e) != 2:
            raise ValueError(f"Malformed edge {e}")
        u, v = e
        if not (isinstance(u, int) and isinstance(v, int)):
            raise ValueError(f"Non-integer endpoints in edge {e}")
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError(f"Out-of-range vertex in edge {e} for n={n}")
        if u == v:
            raise ValueError(f"Self-loop detected at vertex {u}")
        pair = (u, v) if u < v else (v, u)
        if pair in seen_edges:
            raise ValueError(f"Duplicate/parallel edge detected: {pair}")
        seen_edges.add(pair)
        adj[u] |= (1 << v)
        adj[v] |= (1 << u)

    degrees = [adj[i].bit_count() for i in range(n)]
    max_deg = max(degrees) if n > 0 else 0

    # BFS connectivity check
    visited = 1
    frontier = 1
    all_mask = (1 << n) - 1
    while frontier:
        nxt = 0
        tmp = frontier
        while tmp:
            lsb = tmp & -tmp
            v = lsb.bit_length() - 1
            nxt |= adj[v]
            tmp ^= lsb
        frontier = (nxt & all_mask) & ~visited
        visited |= frontier
    connected = (visited == all_mask)

    return {
        "n": n,
        "num_edges": len(seen_edges),
        "adj": tuple(adj),
        "degrees": degrees,
        "max_deg": max_deg,
        "connected": connected,
    }


def enumerate_exact_mis_sets(n, adj):
    """
    Enumerate every maximal independent set (MIS) of G explicitly as a bitmask,
    and directly verify against raw adjacency masks that each set is:
      1. Independent: no edge inside I, and
      2. Maximal: I U N(I) == V(G).
    Returns dict {k: count_of_MIS_of_size_k} and total |M(G)|.
    """
    all_mask = (1 << n) - 1
    closed_adj = tuple(adj[i] | (1 << i) for i in range(n))
    mis_masks = set()

    # Standard backtracking over independent sets that dominate V(G):
    # Pick lowest-index undominated vertex u; any MIS must contain either u or some neighbor w in N(u).
    def dfs(indep_mask, dominated_mask):
        undom = all_mask & ~dominated_mask
        if undom == 0:
            mis_masks.add(indep_mask)
            return
        lsb = undom & -undom
        u = lsb.bit_length() - 1
        candidates = closed_adj[u]
        while candidates:
            c_bit = candidates & -candidates
            w = c_bit.bit_length() - 1
            candidates ^= c_bit
            # w can be added to indep_mask iff w has no neighbor already in indep_mask
            if (adj[w] & indep_mask) == 0:
                dfs(indep_mask | c_bit, dominated_mask | closed_adj[w])

    dfs(0, 0)

    # Direct raw-definition audit of every discovered MIS (LABELS / CONTROLS check)
    counts_by_k = {}
    for mask in mis_masks:
        dom = mask
        tmp = mask
        while tmp:
            v_bit = tmp & -tmp
            v = v_bit.bit_length() - 1
            tmp ^= v_bit
            if (adj[v] & mask) != 0:
                raise AssertionError(f"Set {mask} is NOT independent!")
            dom |= adj[v]
        if dom != all_mask:
            raise AssertionError(f"Set {mask} is NOT maximal!")
        k = mask.bit_count()
        counts_by_k[k] = counts_by_k.get(k, 0) + 1

    total_mis = len(mis_masks)
    assert sum(counts_by_k.values()) == total_mis and total_mis >= 1
    return dict(sorted(counts_by_k.items())), total_mis


def compute_exact_rsa_pmf(n, adj):
    """
    Compute the exact sequential (RSA) occupancy distribution P(N_G^seq = k)
    via pure-Fraction memoization over residual available vertex masks (NO floats).
    """
    closed_adj = tuple(adj[i] | (1 << i) for i in range(n))

    @lru_cache(maxsize=None)
    def solve(avail_mask):
        if avail_mask == 0:
            return ((0, Fraction(1, 1)),)
        m = avail_mask.bit_count()
        inv_m = Fraction(1, m)
        dist = {}
        tmp = avail_mask
        while tmp:
            v_bit = tmp & -tmp
            v = v_bit.bit_length() - 1
            tmp ^= v_bit
            nxt = avail_mask & ~closed_adj[v]
            for k_sub, prob_sub in solve(nxt):
                k_new = k_sub + 1
                dist[k_new] = dist.get(k_new, Fraction(0, 1)) + prob_sub * inv_m
        return tuple(sorted(dist.items()))

    full_mask = (1 << n) - 1
    pmf = dict(solve(full_mask))
    total_prob = sum(pmf.values(), Fraction(0, 1))
    if total_prob != Fraction(1, 1):
        raise AssertionError(f"RSA probabilities sum to {total_prob} != 1")
    return pmf


def evaluate_graph_exact(n, edges):
    """Full exact rational evaluation of G for Conjecture 5.2."""
    info = validate_simple_graph(n, edges)
    mis_counts, total_mis = enumerate_exact_mis_sets(n, info["adj"])
    stat_pmf = {k: Fraction(cnt, total_mis) for k, cnt in mis_counts.items()}
    seq_pmf = compute_exact_rsa_pmf(n, info["adj"])

    if set(stat_pmf.keys()) != set(seq_pmf.keys()):
        # Note: every MIS is reachable with positive sequential probability, so supports MUST match!
        raise AssertionError(f"Support mismatch: stat={set(stat_pmf)} vs seq={set(seq_pmf)}")

    max_k = max(stat_pmf.keys())
    cum_stat = Fraction(0, 1)
    cum_seq = Fraction(0, 1)
    cdf_rows = []
    violating_rows = []
    max_diff = Fraction(0, 1)
    best_k = 0

    for k in range(0, max_k + 1):
        cum_stat += stat_pmf.get(k, Fraction(0, 1))
        cum_seq += seq_pmf.get(k, Fraction(0, 1))
        diff = cum_seq - cum_stat
        p1, q1 = cum_seq.numerator, cum_seq.denominator
        p2, q2 = cum_stat.numerator, cum_stat.denominator
        cross = p1 * q2 - p2 * q1
        assert (cross > 0) == (diff > 0) and (cross == 0) == (diff == 0)
        if k in stat_pmf:
            cdf_rows.append((k, cum_seq, cum_stat, diff, cross))
        if cross > 0:
            violating_rows.append((k, cum_seq, cum_stat, diff, cross))
        if diff > max_diff:
            max_diff = diff
            best_k = k

    d1_holds = (len(violating_rows) == 0)
    is_subcubic_counterexample = (info["max_deg"] <= 3) and (not d1_holds)

    return {
        "info": info,
        "total_mis": total_mis,
        "mis_counts": mis_counts,
        "stat_pmf": stat_pmf,
        "seq_pmf": seq_pmf,
        "cdf_rows": cdf_rows,
        "violating_rows": violating_rows,
        "d1_holds": d1_holds,
        "is_subcubic_counterexample": is_subcubic_counterexample,
        "max_diff": max_diff,
        "best_k": best_k,
    }


def run_controls():
    print("=== RUNNING POSITIVE & NEGATIVE CONTROLS ===")

    # Control 1: Paper's Section 5.2 6-vertex Delta=4 graph
    # Fails D_1 (5/24 > 1/5 at k=2), AND must be REJECTED by Delta <= 3 gate!
    g_deg4 = [(0, 1), (0, 2), (0, 3), (0, 4), (4, 5), (1, 2)]
    c1 = evaluate_graph_exact(6, g_deg4)
    assert c1["info"]["max_deg"] == 4
    assert c1["d1_holds"] is False
    assert c1["is_subcubic_counterexample"] is False  # rejected because max_deg == 4 > 3
    assert c1["max_diff"] == Fraction(1, 120)
    print("[PASS] Control 1 (Paper Sec 5.2 n=6, Delta=4): D_1 fails (5/24 > 1/5, diff=1/120), "
          "Delta<=3 check REJECTS Delta=4.")

    # Control 2: Path P_4 (Delta=2 <= 3, D_1 holds)
    c2 = evaluate_graph_exact(4, [(0, 1), (1, 2), (2, 3)])
    assert c2["info"]["max_deg"] == 2
    assert c2["d1_holds"] is True
    assert c2["is_subcubic_counterexample"] is False
    print("[PASS] Control 2 (P_4, Delta=2): D_1 PASSES (P(seq<=2)=1 <= 1=P(stat<=2)); not a counterexample.")

    # Control 3: Triangle K_3 (Delta=2 <= 3, D_1 holds)
    c3 = evaluate_graph_exact(3, [(0, 1), (1, 2), (0, 2)])
    assert c3["info"]["max_deg"] == 2
    assert c3["d1_holds"] is True
    assert c3["is_subcubic_counterexample"] is False
    print("[PASS] Control 3 (K_3, Delta=2): D_1 PASSES (P(seq<=1)=1 <= 1=P(stat<=1)); not a counterexample.")

    # Control 4: Path P_3 (Delta=2 <= 3, strict dominance D_1 holds: 1/3 < 1/2)
    c4 = evaluate_graph_exact(3, [(0, 1), (1, 2)])
    assert c4["info"]["max_deg"] == 2
    assert c4["d1_holds"] is True
    assert c4["is_subcubic_counterexample"] is False
    assert c4["cdf_rows"][0][1] == Fraction(1, 3) and c4["cdf_rows"][0][2] == Fraction(1, 2)
    print("[PASS] Control 4 (P_3, Delta=2): D_1 PASSES strictly (P(seq<=1)=1/3 < 1/2=P(stat<=1)).")

    # Control 5: Top n=14 subcubic near-miss (4/225 < 1/55, cross = -5 < 0, D_1 holds!)
    g_n14 = [[0,1],[0,2],[0,3],[1,2],[3,4],[4,5],[5,6],[5,7],[6,8],[7,12],[8,9],[9,10],[9,11],[10,13]]
    c5 = evaluate_graph_exact(14, g_n14)
    assert c5["info"]["max_deg"] == 3
    assert c5["d1_holds"] is True
    assert c5["is_subcubic_counterexample"] is False
    print("[PASS] Control 5 (Top n=14 subcubic near-miss): D_1 PASSES (4/225 < 1/55, p1*q2-p2*q1 = -5 < 0).\n")


def verify_minimality(n, edges):
    """Verify every (n-1)-vertex induced subgraph G-v and every edge-deleted subgraph G-e satisfies D_1."""
    # 1. All n vertex-deleted induced subgraphs G - v
    for rem in range(n):
        remap = {v: (v if v < rem else v - 1) for v in range(n) if v != rem}
        sub_edges = [(remap[u], remap[v]) for u, v in edges if u != rem and v != rem]
        r = evaluate_graph_exact(n - 1, sub_edges)
        if not r["d1_holds"]:
            return False, f"G - vertex({rem}) still violates D_1!"

    # 2. All |E| edge-deleted subgraphs G - e
    for idx in range(len(edges)):
        sub_edges = [edges[j] for j in range(len(edges)) if j != idx]
        r = evaluate_graph_exact(n, sub_edges)
        if not r["d1_holds"]:
            return False, f"G - edge({edges[idx]}) still violates D_1!"

    return True, f"All {n} subgraphs G-v and all {len(edges)} subgraphs G-e satisfy Conjecture 5.2."


def main():
    witness_path = Path(sys.argv[1]) if len(sys.argv) > 1 else (Path(__file__).resolve().parent / "witness.json")
    run_controls()

    print(f"=== VERIFYING WITNESS: {witness_path} ===")
    data = json.loads(witness_path.read_text(encoding="utf-8"))
    n = data["n"]
    edges = data["edges"]

    res = evaluate_graph_exact(n, edges)
    info = res["info"]

    print(f"Graph summary: n = {info['n']}, |E| = {info['num_edges']}, "
          f"connected = {info['connected']}, max_degree Delta(G) = {info['max_deg']}")
    print(f"Degree sequence: {info['degrees']}")
    print(f"Total maximal independent sets |M(G)| = {res['total_mis']}")
    print(f"Static MIS counts by size k: {res['mis_counts']}")
    print("Exact Cumulative Distributions (reduced fractions):")
    for k, f_seq, f_stat, diff, cross in res["cdf_rows"]:
        p1, q1 = f_seq.numerator, f_seq.denominator
        p2, q2 = f_stat.numerator, f_stat.denominator
        rel = ">" if cross > 0 else ("==" if cross == 0 else "<")
        print(f"  k = {k}: P(N_G^seq <= {k}) = {p1}/{q1} {rel} {p2}/{q2} = P(N_G^stat <= {k}) "
              f"| diff = {diff} | p1*q2 - p2*q1 = {cross}")

    if not res["is_subcubic_counterexample"]:
        print("VERIFICATION FAILED: Graph is NOT a valid Delta(G) <= 3 counterexample!")
        sys.exit(1)

    k0, f_seq0, f_stat0, diff0, cross0 = res["violating_rows"][0]
    p1, q1 = f_seq0.numerator, f_seq0.denominator
    p2, q2 = f_stat0.numerator, f_stat0.denominator
    assert info["max_deg"] <= 3
    assert cross0 == p1 * q2 - p2 * q1 and cross0 > 0

    is_min, min_msg = verify_minimality(n, edges)
    assert is_min, min_msg
    print(f"Minimality check: [PASS] {min_msg}")

    print("\n=== EXACT RATIONAL CERTIFICATE (PRIMARY MINIMAL WITNESS) ===")
    print(f"Simple graph G on n = {n} vertices, |E| = {info['num_edges']} edges, Delta(G) = {info['max_deg']} <= 3")
    print(f"At k = {k0}:")
    print(f"  P(N_G^seq <= {k0}) = {p1}/{q1} > {p2}/{q2} = P(N_G^stat <= {k0})")
    print(f"  Exact integer cross-difference: p1*q2 - p2*q1 = {p1}*{q2} - {p2}*{q1} = {cross0} > 0")
    print(f"  Exact rational gap J(G) = {diff0}")

    if "all_minimal_n15_counterexamples" in data:
        print("\n=== VERIFYING ALL THREE n=15 COUNTEREXAMPLES FROM EXHAUSTIVE CENSUS ===")
        for item in data["all_minimal_n15_counterexamples"]:
            sub_res = evaluate_graph_exact(item["n"], item["edges"])
            assert sub_res["is_subcubic_counterexample"] is True
            assert sub_res["info"]["max_deg"] == 3 and sub_res["info"]["connected"] is True
            sk, sf_seq, sf_stat, sdiff, scross = sub_res["violating_rows"][0]
            assert sk == 6 and sf_seq == Fraction(64, 3375) and sf_stat == Fraction(1, 55) and scross == 145
            glob_rev = all(row[4] >= 0 for row in sub_res["cdf_rows"])
            assert glob_rev == item["global_static_dominance"]
            print(f"  [PASS] {item['id']} ({item['type']}, |E|={item['num_edges']}): "
                  f"P(seq<=6)=64/3375 > 1/55=P(stat<=6), global_static_dominates={glob_rev}")

    print("\nVERDICT: CERTIFIED COUNTEREXAMPLE TO CONJECTURE 5.2 (arXiv:2611.14718v2).")


if __name__ == "__main__":
    main()
