import json
import os
import sys


# ============================================================================
# Clean-Room Pure-Integer Polynomial Arithmetic (Z[q], ascending degree order)
# Zero math module, zero future imports, zero non-integer types, // only.
# ============================================================================

def poly_trim(p):
    res = list(p)
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res if res else [0]


def poly_add(a, b):
    n = len(a) if len(a) >= len(b) else len(b)
    res = [0] * n
    for i, c in enumerate(a):
        res[i] += c
    for i, c in enumerate(b):
        res[i] += c
    return poly_trim(res)


def poly_sub(a, b):
    n = len(a) if len(a) >= len(b) else len(b)
    res = [0] * n
    for i, c in enumerate(a):
        res[i] += c
    for i, c in enumerate(b):
        res[i] -= c
    return poly_trim(res)


def poly_mul(a, b):
    if (len(a) == 1 and a[0] == 0) or (len(b) == 1 and b[0] == 0):
        return [0]
    res = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x != 0:
            for j, y in enumerate(b):
                res[i + j] += x * y
    return poly_trim(res)


def poly_pow(a, exp):
    assert isinstance(exp, int) and exp >= 0
    res = [1]
    for _ in range(exp):
        res = poly_mul(res, a)
    return res


def poly_deriv(p):
    if len(p) <= 1:
        return [0]
    return poly_trim([i * p[i] for i in range(1, len(p))])


def poly_eval_int(p, q):
    assert isinstance(q, int)
    total = 0
    q_pow = 1
    for c in p:
        total += c * q_pow
        q_pow *= q
    return total


def int_gcd(a, b):
    x = a if a >= 0 else -a
    y = b if b >= 0 else -b
    while y != 0:
        x, y = y, x % y
    return x


def poly_eval_rational(p, num_q, den_q):
    """Evaluate P(num_q : den_q) exactly as reduced integer pair (num, den)."""
    assert isinstance(num_q, int) and isinstance(den_q, int) and den_q > 0
    deg = len(p) - 1
    acc = 0
    for i, c in enumerate(p):
        acc += c * (num_q ** i) * (den_q ** (deg - i))
    den = den_q ** deg
    g = int_gcd(acc, den)
    assert acc % g == 0 and den % g == 0
    return acc // g, den // g


def poly_divmod_monic(dividend, divisor):
    """Exact polynomial division in Z[q] by a monic integer divisor."""
    assert divisor[-1] == 1
    rem = poly_trim(dividend)
    deg_d = len(divisor) - 1
    if len(rem) - 1 < deg_d:
        return [0], rem
    quot = [0] * (len(rem) - deg_d)
    while len(rem) - 1 >= deg_d and not (len(rem) == 1 and rem[0] == 0):
        shift = (len(rem) - 1) - deg_d
        lead = rem[-1]
        quot[shift] = lead
        for i, c in enumerate(divisor):
            rem[i + shift] -= lead * c
        rem = poly_trim(rem)
    return poly_trim(quot), rem


# ============================================================================
# Exact Positive-Multiplier Integer Sturm Root-Counting Engine
# ============================================================================

def poly_pseudo_rem_positive(a, b):
    """
    Compute R with alpha * A = Q * B + R, deg(R) < deg(B), and alpha > 0,
    preserving exact signs at every real evaluation point.
    """
    rem = poly_trim(a)
    div = poly_trim(b)
    assert not (len(div) == 1 and div[0] == 0)
    deg_b = len(div) - 1
    lead_b = div[-1]
    mult = lead_b if lead_b > 0 else -lead_b
    sign_b = 1 if lead_b > 0 else -1
    while len(rem) - 1 >= deg_b and not (len(rem) == 1 and rem[0] == 0):
        shift = (len(rem) - 1) - deg_b
        lead_a = rem[-1]
        coeff = lead_a * sign_b
        for i in range(len(rem)):
            rem[i] *= mult
        for i, b_val in enumerate(div):
            rem[i + shift] -= coeff * b_val
        rem = poly_trim(rem)
    g = 0
    for c in rem:
        g = int_gcd(g, c)
    if g > 1:
        for i in range(len(rem)):
            assert rem[i] % g == 0
            rem[i] //= g
    return rem


def build_sturm_chain(p):
    p0 = poly_trim(p)
    p1 = poly_deriv(p0)
    chain = [p0, p1]
    while len(chain[-1]) > 1:
        r = poly_pseudo_rem_positive(chain[-2], chain[-1])
        neg_r = [-c for c in r]
        if len(neg_r) == 1 and neg_r[0] == 0:
            break
        chain.append(neg_r)
    return chain


def count_sign_variations(signs):
    nz = [s for s in signs if s != 0]
    variations = 0
    for i in range(len(nz) - 1):
        if nz[i] * nz[i + 1] < 0:
            variations += 1
    return variations


def sturm_variations_at_rational(chain, num_q, den_q):
    signs = []
    for poly in chain:
        num_val, _ = poly_eval_rational(poly, num_q, den_q)
        if num_val > 0:
            signs.append(1)
        elif num_val < 0:
            signs.append(-1)
        else:
            signs.append(0)
    return count_sign_variations(signs), signs


def poly_sign_near_int_root(poly, a, direction):
    """
    Exact sign of poly(a + direction * eps) for infinitesimally small eps > 0,
    where direction is +1 (right limit) or -1 (left limit), via Taylor derivatives.
    """
    assert direction in (1, -1)
    cur = poly_trim(poly)
    k = 0
    while True:
        val = poly_eval_int(cur, a)
        if val != 0:
            s = 1 if val > 0 else -1
            if direction == -1 and (k % 2 == 1):
                s = -s
            return s
        if len(cur) <= 1:
            return 0
        cur = poly_deriv(cur)
        k += 1


def sturm_variations_limit_at_int(chain, a, direction):
    signs = [poly_sign_near_int_root(poly, a, direction) for poly in chain]
    return count_sign_variations(signs), signs


# ============================================================================
# Graph Verification: Simplicity, Exact Connectivity, Bipartiteness & Cycles
# ============================================================================

def verify_and_canonicalize_simple_graph(n, raw_edges):
    if not isinstance(n, int) or n < 1:
        return False, [], "invalid vertex count"
    canon = []
    seen = set()
    for e in raw_edges:
        if not isinstance(e, (list, tuple)) or len(e) != 2:
            return False, [], "malformed edge entry"
        u, v = e[0], e[1]
        if not (isinstance(u, int) and isinstance(v, int)):
            return False, [], "non-integer vertex label"
        if not (0 <= u < n and 0 <= v < n):
            return False, [], "vertex out of range"
        if u == v:
            return False, [], f"self-loop at {u}"
        pair = (u, v) if u < v else (v, u)
        if pair in seen:
            return False, [], f"duplicate edge {pair}"
        seen.add(pair)
        canon.append(pair)
    canon.sort()
    return True, canon, "ok"


def connected_components_after_removal(n, edges, removed_set):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if u not in removed_set and v not in removed_set:
            adj[u].append(v)
            adj[v].append(u)
    visited = set()
    comps = []
    for start in range(n):
        if start in removed_set or start in visited:
            continue
        comp = []
        queue = [start]
        visited.add(start)
        head = 0
        while head < len(queue):
            cur = queue[head]
            head += 1
            comp.append(cur)
            for nb in adj[cur]:
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
        comp.sort()
        comps.append(comp)
    return comps


def exact_connectivity_audit(n, edges):
    """
    Exact audit of vertex connectivity up to kappa = 3:
    - Exhaustively checks 0-cuts, all n 1-cuts, all C(n,2) 2-cuts, and 3-cuts.
    - Returns (kappa_capped_at_4, witness_cut, comps_at_cut, pairs_tested).
    """
    c0 = connected_components_after_removal(n, edges, set())
    if len(c0) != 1:
        return 0, (), c0, 0
    if n == 1:
        return 0, (), c0, 0

    for u in range(n):
        c1 = connected_components_after_removal(n, edges, {u})
        if len(c1) != 1:
            return 1, (u,), c1, 0
    if n == 2:
        return 1, (0,), [[1]], 0

    pairs_tested = 0
    first_2cut = None
    first_2comps = None
    for u in range(n):
        for v in range(u + 1, n):
            pairs_tested += 1
            c2 = connected_components_after_removal(n, edges, {u, v})
            if len(c2) != 1 and first_2cut is None:
                first_2cut = (u, v)
                first_2comps = c2
    expected_pairs = (n * (n - 1)) // 2
    assert pairs_tested == expected_pairs
    if first_2cut is not None:
        return 2, first_2cut, first_2comps, pairs_tested
    if n == 3:
        return 2, (0, 1), [[2]], pairs_tested

    for u in range(n):
        for v in range(u + 1, n):
            for w in range(v + 1, n):
                c3 = connected_components_after_removal(n, edges, {u, v, w})
                if len(c3) != 1:
                    return 3, (u, v, w), c3, pairs_tested
    if n == 4:
        return 3, (0, 1, 2), [[3]], pairs_tested

    return 4, None, None, pairs_tested


def audit_bipartite_or_odd_cycle(n, edges):
    """
    2-coloring BFS. If bipartite, verifies proper 2-coloring and returns (True, color, None).
    If non-bipartite, extracts an explicit simple odd cycle and verifies all edges in E(G).
    """
    adj = [[] for _ in range(n)]
    edge_set = set()
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        edge_set.add((u, v) if u < v else (v, u))

    color = [-1] * n
    parent = [-1] * n
    depth = [0] * n

    for start in range(n):
        if color[start] != -1:
            continue
        color[start] = 0
        queue = [start]
        head = 0
        while head < len(queue):
            u = queue[head]
            head += 1
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    parent[v] = u
                    depth[v] = depth[u] + 1
                    queue.append(v)
                elif color[v] == color[u]:
                    # Reconstruct simple odd cycle via BFS tree ancestors to LCA
                    anc_u = []
                    anc_v = []
                    cu, cv = u, v
                    while depth[cu] > depth[cv]:
                        anc_u.append(cu)
                        cu = parent[cu]
                    while depth[cv] > depth[cu]:
                        anc_v.append(cv)
                        cv = parent[cv]
                    while cu != cv:
                        anc_u.append(cu)
                        anc_v.append(cv)
                        cu = parent[cu]
                        cv = parent[cv]
                    lca = cu
                    cycle = anc_u + [lca] + list(reversed(anc_v))
                    verify_odd_cycle(cycle, edge_set)
                    return False, None, cycle

    for u, v in edges:
        assert color[u] != color[v]
    return True, color, None


def verify_odd_cycle(cycle, edge_set):
    k = len(cycle)
    assert k >= 3 and (k % 2 == 1), f"cycle length {k} is not odd >= 3"
    assert len(set(cycle)) == k, "cycle repeats vertices"
    for i in range(k):
        a = cycle[i]
        b = cycle[(i + 1) % k]
        pair = (a, b) if a < b else (b, a)
        assert pair in edge_set, f"missing cycle edge {pair}"


# ============================================================================
# Chromatic Polynomial Engine A: Deletion-Contraction (Completely Independent)
# ============================================================================

def chrom_poly_deletion_contraction(n, edges):
    """
    Exact chromatic polynomial via deletion-contraction chi(G) = chi(G - e) - chi(G . e),
    with connected-component multiplicativity, pendant-leaf factoring (q - 1), and memoization.
    """
    memo = {}

    def split_components(nv, adj):
        vis = 0
        comps = []
        for s in range(nv):
            if not ((vis >> s) & 1):
                comp = 0
                stack = [s]
                vis |= (1 << s)
                while stack:
                    u = stack.pop()
                    comp |= (1 << u)
                    nb = adj[u] & ~vis
                    while nb:
                        lb = nb & -nb
                        w = lb.bit_length() - 1
                        vis |= lb
                        stack.append(w)
                        nb ^= lb
                comps.append(comp)
        return comps

    def delete_vertex_relabel(nv, adj, rem_v):
        out = []
        mask_lo = (1 << rem_v) - 1
        for w in range(nv):
            if w == rem_v:
                continue
            m = adj[w] & ~(1 << rem_v)
            lo = m & mask_lo
            hi = (m >> (rem_v + 1)) << rem_v
            out.append(lo | hi)
        return out

    def solve_connected(nv, adj):
        if nv == 1:
            return [0, 1]
        key = (nv, tuple(adj))
        if key in memo:
            return memo[key]

        best_u = -1
        best_deg = nv + 1
        for u in range(nv):
            d = adj[u].bit_count()
            if 0 < d < best_deg:
                best_deg = d
                best_u = u

        if best_deg == 1:
            sub_adj = delete_vertex_relabel(nv, adj, best_u)
            res = poly_mul([-1, 1], solve_general(nv - 1, sub_adj))
            memo[key] = res
            return res

        u = best_u
        v = (adj[u] & -adj[u]).bit_length() - 1

        # Deletion G - uv
        adj_del = list(adj)
        adj_del[u] ^= (1 << v)
        adj_del[v] ^= (1 << u)
        p_del = solve_general(nv, adj_del)

        # Simple contraction G . uv (merge v into u, remove self-loops and parallel edges)
        adj_con = list(adj_del)
        merged = adj_con[u] | adj_con[v]
        adj_con[u] = merged
        for w in range(nv):
            if (adj_con[w] >> v) & 1:
                adj_con[w] |= (1 << u)
        sub_adj = delete_vertex_relabel(nv, adj_con, v)
        p_con = solve_general(nv - 1, sub_adj)

        res = poly_sub(p_del, p_con)
        memo[key] = res
        return res

    def solve_general(nv, adj):
        if nv == 0:
            return [1]
        comps = split_components(nv, adj)
        if len(comps) == 1:
            return solve_connected(nv, adj)
        prod = [1]
        for comp in comps:
            verts = [u for u in range(nv) if (comp >> u) & 1]
            if len(verts) == 1:
                prod = poly_mul(prod, [0, 1])
                continue
            pos = {u: idx for idx, u in enumerate(verts)}
            sub_adj = [0] * len(verts)
            for idx, u in enumerate(verts):
                m = adj[u]
                sm = 0
                while m:
                    lb = m & -m
                    w = lb.bit_length() - 1
                    sm |= (1 << pos[w])
                    m ^= lb
                sub_adj[idx] = sm
            prod = poly_mul(prod, solve_connected(len(verts), sub_adj))
        return prod

    adj0 = [0] * n
    for u, v in edges:
        adj0[u] |= (1 << v)
        adj0[v] |= (1 << u)
    return solve_general(n, adj0)


# ============================================================================
# Chromatic Polynomial Engine B: Independent-Set Partition Falling-Factorial DP
# ============================================================================

def chrom_poly_indep_partitions(n, edges):
    """
    Completely independent combinatorial algorithm:
    Counts unordered partitions of V(G) into j non-empty independent sets (1 <= j <= n)
    by canonical minimum-uncovered-vertex DP, then expands sum_{j=1}^n N_j * (q)_j.
    """
    adj = [0] * n
    for u, v in edges:
        adj[u] |= (1 << v)
        adj[v] |= (1 << u)

    indep_by_min = [[] for _ in range(n)]

    def enum_indep(min_v, cur_v, mask, forbidden):
        if cur_v == n:
            indep_by_min[min_v].append(mask)
            return
        enum_indep(min_v, cur_v + 1, mask, forbidden)
        if not ((forbidden >> cur_v) & 1):
            enum_indep(min_v, cur_v + 1, mask | (1 << cur_v), forbidden | adj[cur_v])

    for v in range(n):
        enum_indep(v, v + 1, 1 << v, adj[v])

    full_mask = (1 << n) - 1
    dp = {0: [1] + [0] * n}
    for covered in range(full_mask):
        row = dp.get(covered)
        if row is None:
            continue
        rem = full_mask ^ covered
        low_v = (rem & -rem).bit_length() - 1
        for ind in indep_by_min[low_v]:
            if (ind & covered) == 0:
                nxt = covered | ind
                nxt_row = dp.get(nxt)
                if nxt_row is None:
                    nxt_row = [0] * (n + 1)
                    dp[nxt] = nxt_row
                for j in range(n):
                    c = row[j]
                    if c:
                        nxt_row[j + 1] += c

    counts_nj = dp[full_mask]
    total = [0] * (n + 1)
    falling = [1]
    for j in range(1, n + 1):
        falling = poly_mul(falling, [-(j - 1), 1])
        nj = counts_nj[j]
        if nj != 0:
            for deg, coeff in enumerate(falling):
                total[deg] += nj * coeff
    return poly_trim(total), counts_nj


# ============================================================================
# Chromatic Polynomial Engine C (Witness Cross-Checks): NBC & Brute-Force Colorings
# ============================================================================

def chrom_poly_broken_circuit(n, edges):
    """
    Whitney's Broken-Circuit (NBC) Theorem over ordered E(G):
    A subset F is an NBC forest iff F is acyclic and for every e_i = (u_i, v_i),
    u_i and v_i are not connected in {e_j in F : j > i}.
    Accumulates (-1)^|F| * q^(n - |F|) with zero polynomial multiplications.
    """
    m = len(edges)
    coeffs = [0] * (n + 1)

    def dfs(idx, chosen_count, comp):
        if idx < 0:
            deg = n - chosen_count
            sign = -1 if (chosen_count % 2 == 1) else 1
            coeffs[deg] += sign
            return
        u, v = edges[idx]
        cu, cv = comp[u], comp[v]
        if cu == cv:
            # {e_j in F : j > idx} already contains the broken circuit P = (P + e_idx) - e_idx
            return
        # Branch 1: exclude e_idx
        dfs(idx - 1, chosen_count, comp)
        # Branch 2: include e_idx (merge cv into cu)
        merged = tuple(cu if c == cv else c for c in comp)
        dfs(idx - 1, chosen_count + 1, merged)

    dfs(m - 1, 0, tuple(range(n)))
    return poly_trim(coeffs)


def count_proper_k_colorings_bruteforce(n, edges, k):
    """Direct backtracking count of proper k-colorings V(G) -> {0, ..., k - 1}."""
    assert isinstance(k, int) and k >= 0
    if k == 0:
        return 1 if n == 0 else 0
    lower_neighbors = [[] for _ in range(n)]
    for u, v in edges:
        if u < v:
            lower_neighbors[v].append(u)
        else:
            lower_neighbors[u].append(v)

    assign = [0] * n

    def backtrack(v):
        if v == n:
            return 1
        total = 0
        lnb = lower_neighbors[v]
        for col in range(k):
            ok = True
            for nb in lnb:
                if assign[nb] == col:
                    ok = False
                    break
            if ok:
                assign[v] = col
                total += backtrack(v + 1)
        return total

    return backtrack(0)


def chrom_poly_hand_closed_form():
    """
    Exact closed-form polynomial chi_G(q) = (q)_3 * Q(q) obtained by summing over
    all proper coloring equality patterns on {x, a, b, c, d}.
    """
    qm1 = [-1, 1]
    qm2 = [-2, 1]
    qm3 = [-3, 1]
    # Q(q) = 2(q-1)^3(q-2)^2 + 2(q-1)^3(q-3)^3 + (7q-12)(q-2)^5
    #        + 2(3q-7)(q-2)^3(q-3)^3 + (q^2-5q+7)(q-3)^6
    t1 = poly_mul([2], poly_mul(poly_pow(qm1, 3), poly_pow(qm2, 2)))
    t2 = poly_mul([2], poly_mul(poly_pow(qm1, 3), poly_pow(qm3, 3)))
    t3 = poly_mul([-12, 7], poly_pow(qm2, 5))
    t4 = poly_mul([-14, 6], poly_mul(poly_pow(qm2, 3), poly_pow(qm3, 3)))
    t5 = poly_mul([7, -5, 1], poly_pow(qm3, 6))
    q_poly = poly_add(t1, poly_add(t2, poly_add(t3, poly_add(t4, t5))))
    q_fall_3 = poly_mul([0, 1], poly_mul(qm1, qm2))
    return poly_mul(q_fall_3, q_poly), q_poly


# ============================================================================
# Invariant gamma(G) and Full Candidate-Counterexample Gate
# ============================================================================

def compute_gamma_standard(n, chi_poly):
    chi_2 = poly_eval_int(chi_poly, 2)
    chi_deriv = poly_deriv(chi_poly)
    chi_prime_2 = poly_eval_int(chi_deriv, 2)
    sign = 1 if ((n - 1) % 2 == 0) else -1
    signed_num = sign * chi_prime_2
    gamma_int = (signed_num // 2) if (signed_num % 2 == 0) else None
    return chi_2, chi_prime_2, gamma_int


def compute_gamma_sign_flipped_mutant(n, chi_poly):
    chi_2, chi_prime_2, gamma_std = compute_gamma_standard(n, chi_poly)
    flipped = (-gamma_std) if (gamma_std is not None) else None
    return chi_2, chi_prime_2, flipped


def evaluate_graph_record(name, n, raw_edges, gamma_fn=compute_gamma_standard):
    is_simple, edges, msg = verify_and_canonicalize_simple_graph(n, raw_edges)
    assert is_simple, f"{name}: simplicity failed ({msg})"

    kappa, cut_witness, cut_comps, pairs_tested = exact_connectivity_audit(n, edges)
    is_3_connected = (n >= 4) and (kappa >= 3)

    is_bip, _, odd_cycle = audit_bipartite_or_odd_cycle(n, edges)
    is_non_bipartite = not is_bip

    poly_a = chrom_poly_deletion_contraction(n, edges)
    poly_b, indep_counts = chrom_poly_indep_partitions(n, edges)
    assert poly_a == poly_b, f"{name}: Algorithm A != Algorithm B"

    chi_2, chi_prime_2, gamma_val = gamma_fn(n, poly_a)
    if is_non_bipartite:
        assert chi_2 == 0, f"{name}: non-bipartite graph must have chi(2) == 0"
        assert gamma_val is not None, f"{name}: non-bipartite graph must have integer gamma"
    else:
        assert chi_2 > 0, f"{name}: connected or nonempty bipartite graph must have chi(2) > 0"

    is_counterexample = (
        is_simple
        and is_3_connected
        and is_non_bipartite
        and (chi_2 == 0)
        and (gamma_val is not None)
        and (gamma_val < 0)
    )
    return {
        "name": name,
        "n": n,
        "m": len(edges),
        "edges": edges,
        "kappa": kappa,
        "cut_witness": cut_witness,
        "cut_comps": cut_comps,
        "pairs_tested": pairs_tested,
        "is_3_connected": is_3_connected,
        "is_non_bipartite": is_non_bipartite,
        "odd_cycle": odd_cycle,
        "chi_poly": poly_a,
        "indep_counts": indep_counts,
        "chi_2": chi_2,
        "chi_prime_2": chi_prime_2,
        "gamma": gamma_val,
        "is_counterexample": is_counterexample,
    }


# ============================================================================
# Graph Constructors for Constructive Witness & Controls
# ============================================================================

def build_constructive_witness():
    # x=0; left first shore {0,1,2}, left second shore {5,6,7};
    # right first shore {0,3,4}, right second shore {8,9,10}; matching {1,3}, {2,4}.
    edges = []
    for u in (0, 1, 2):
        for v in (5, 6, 7):
            edges.append((u, v))
    for u in (0, 3, 4):
        for v in (8, 9, 10):
            edges.append((u, v))
    edges.append((1, 3))
    edges.append((2, 4))
    edges.sort()
    return 11, edges


def build_complete_graph(n):
    return n, [(u, v) for u in range(n) for v in range(u + 1, n)]


def build_octahedron():
    # K_{2,2,2} with opposite non-adjacent pairs {0,1}, {2,3}, {4,5}
    antipodal = {(0, 1), (2, 3), (4, 5)}
    edges = [
        (u, v)
        for u in range(6)
        for v in range(u + 1, 6)
        if (u, v) not in antipodal
    ]
    return 6, edges


def build_paper_tk(k):
    """
    Hexagon T_k on the triangular grid with side lengths 1, 2, k (main.tex Fig. 4):
    lattice points {(x, y) : 0 <= x <= 3, 0 <= y <= 1 + k, -k <= x - y <= 2}
    with triangular-grid unit steps (1, 0), (0, 1), (1, 1).
    """
    a, b = 1, 2
    pts = [
        (x, y)
        for x in range(a + b + 1)
        for y in range(a + k + 1)
        if -k <= x - y <= b
    ]
    pt_id = {pt: idx for idx, pt in enumerate(pts)}
    edges = []
    for x, y in pts:
        u = pt_id[(x, y)]
        for dx, dy in ((1, 0), (0, 1), (1, 1)):
            nb = (x + dx, y + dy)
            if nb in pt_id:
                v = pt_id[nb]
                edges.append((u, v) if u < v else (v, u))
    edges.sort()
    return len(pts), edges


def build_theta_2_2_3():
    # Poles 0 and 1 joined by paths 0-2-1, 0-3-1, and 0-4-5-1
    edges = [(0, 2), (1, 2), (0, 3), (1, 3), (0, 4), (4, 5), (1, 5)]
    return 6, edges


# ============================================================================
# Main Adversarial Verification Suite
# ============================================================================

def main():
    witness_path = os.path.join("inputs", "witness.json")
    with open(witness_path, "r", encoding="utf-8") as fh:
        witness_data = json.load(fh)

    assert set(witness_data.keys()) == {"n", "edges"}
    rec_g = evaluate_graph_record("Witness_G", witness_data["n"], witness_data["edges"])

    # 1. Witness structure & exact match to PROOF.md construction
    exp_n, exp_edges = build_constructive_witness()
    assert rec_g["n"] == 11 and rec_g["m"] == 20
    assert rec_g["edges"] == exp_edges, "witness.json does not match two-K3,3 + matching construction"

    # 2. Exact 3-connectivity check (all 55 2-vertex deletions + explicit 3-cut {0,1,2})
    assert rec_g["pairs_tested"] == 55
    assert rec_g["is_3_connected"] and rec_g["kappa"] == 3
    comps_012 = connected_components_after_removal(11, rec_g["edges"], {0, 1, 2})
    assert comps_012 == [[3, 4, 8, 9, 10], [5], [6], [7]]

    # 3. Non-bipartiteness (BFS odd cycle + PROOF.md explicit 5-cycle [0, 5, 1, 3, 8])
    assert rec_g["is_non_bipartite"]
    assert rec_g["odd_cycle"] is not None and len(rec_g["odd_cycle"]) == 5
    verify_odd_cycle([0, 5, 1, 3, 8], set(rec_g["edges"]))

    # 4. Chromatic polynomial cross-verification (Alg A == Alg B == Alg C == Hand == Brute-force k=0..4)
    chi_g = rec_g["chi_poly"]
    chi_nbc = chrom_poly_broken_circuit(11, rec_g["edges"])
    chi_hand, q_hand = chrom_poly_hand_closed_form()
    assert chi_g == chi_nbc, "Algorithm A != NBC Broken-Circuit Algorithm C"
    assert chi_g == chi_hand, "Algorithm A != Hand Closed-Form"

    expected_chi_desc = [
        1, -20, 190, -1122, 4533, -13007, 26647, -38153, 36166, -20253, 5018, 0
    ]
    assert list(reversed(chi_g)) == expected_chi_desc

    brute_counts = [
        count_proper_k_colorings_bruteforce(11, rec_g["edges"], k)
        for k in range(5)
    ]
    poly_counts = [poly_eval_int(chi_g, k) for k in range(5)]
    assert brute_counts == poly_counts == [0, 0, 0, 150, 20760]

    # 5. Exact evaluations at q=2, quotient Q(q), Mobius coefficients, rational signs & Sturm root count
    assert rec_g["chi_2"] == 0
    assert rec_g["chi_prime_2"] == -2
    assert rec_g["gamma"] == -1
    assert rec_g["is_counterexample"] is True

    q_quot, q_rem = poly_divmod_monic(chi_g, [0, 2, -3, 1])
    assert q_rem == [0] and q_quot == q_hand
    expected_q_desc = [1, -17, 137, -677, 2228, -4969, 7284, -6363, 2509]
    assert list(reversed(q_quot)) == expected_q_desc
    assert poly_eval_int(q_quot, 1) == 133
    assert poly_eval_int(q_quot, 2) == -1
    assert poly_eval_int(poly_deriv(chi_g), 1) == -133

    # Mobius transform (1 + t)^8 * Q((1 + 2t) : (1 + t))
    mobius = [0]
    for idx, c in enumerate(q_quot):
        term = poly_mul([c], poly_mul(poly_pow([1, 2], idx), poly_pow([1, 1], 8 - idx)))
        mobius = poly_add(mobius, term)
    expected_mobius_asc = [133, 600, 1177, 1284, 828, 304, 51, -1, -1]
    assert mobius == expected_mobius_asc
    assert count_sign_variations([1 if x > 0 else -1 for x in mobius if x != 0]) == 1

    # Rational evaluations at 19:10 and 39:20
    q_19_10 = poly_eval_rational(q_quot, 19, 10)
    q_39_20 = poly_eval_rational(q_quot, 39, 20)
    chi_19_10 = poly_eval_rational(chi_g, 19, 10)
    chi_39_20 = poly_eval_rational(chi_g, 39, 20)
    assert q_19_10 == (3694111, 100000000) and q_19_10[0] > 0
    assert q_39_20 == (-14608211579, 25600000000) and q_39_20[0] < 0
    assert chi_19_10 == (-631692981, 100000000000) and chi_19_10[0] < 0
    assert chi_39_20 == (10824684780039, 204800000000000) and chi_39_20[0] > 0

    # Exact Sturm root counts on Q(q) and directly on chi_G(q)
    sturm_q = build_sturm_chain(q_quot)
    assert len(sturm_q) == 9 and len(sturm_q[-1]) == 1 and sturm_q[-1][0] != 0
    vq_1, _ = sturm_variations_at_rational(sturm_q, 1, 1)
    vq_19_10, _ = sturm_variations_at_rational(sturm_q, 19, 10)
    vq_39_20, _ = sturm_variations_at_rational(sturm_q, 39, 20)
    vq_2, _ = sturm_variations_at_rational(sturm_q, 2, 1)
    assert (vq_1, vq_19_10, vq_39_20, vq_2) == (5, 5, 4, 4)
    assert vq_1 - vq_2 == 1
    assert vq_19_10 - vq_39_20 == 1

    sturm_chi = build_sturm_chain(chi_g)
    assert len(sturm_chi) == 12 and len(sturm_chi[-1]) == 1 and sturm_chi[-1][0] != 0
    vchi_1_plus, _ = sturm_variations_limit_at_int(sturm_chi, 1, 1)
    vchi_19_10, _ = sturm_variations_at_rational(sturm_chi, 19, 10)
    vchi_39_20, _ = sturm_variations_at_rational(sturm_chi, 39, 20)
    vchi_2_minus, _ = sturm_variations_limit_at_int(sturm_chi, 2, -1)
    vchi_2, _ = sturm_variations_at_rational(sturm_chi, 2, 1)
    assert (vchi_1_plus, vchi_19_10, vchi_39_20, vchi_2_minus, vchi_2) == (6, 6, 5, 5, 4)
    assert vchi_1_plus - vchi_2_minus == 1
    assert vchi_19_10 - vchi_39_20 == 1

    # 6. Positive Controls: K3, K4, Octahedron, and Paper's T1, T2, T3
    rec_k3 = evaluate_graph_record("K3", *build_complete_graph(3))
    assert rec_k3["gamma"] == 1 and rec_k3["chi_prime_2"] == 2 and not rec_k3["is_counterexample"]

    rec_k4 = evaluate_graph_record("K4", *build_complete_graph(4))
    assert rec_k4["is_3_connected"] and rec_k4["is_non_bipartite"]
    assert rec_k4["gamma"] == 1 and rec_k4["chi_prime_2"] == -2 and not rec_k4["is_counterexample"]

    rec_oct = evaluate_graph_record("Octahedron", *build_octahedron())
    assert rec_oct["is_3_connected"] and rec_oct["kappa"] == 4 and rec_oct["is_non_bipartite"]
    assert rec_oct["gamma"] == 2 and rec_oct["chi_prime_2"] == -4 and not rec_oct["is_counterexample"]

    rec_t1 = evaluate_graph_record("Paper_T1", *build_paper_tk(1))
    rec_t2 = evaluate_graph_record("Paper_T2", *build_paper_tk(2))
    rec_t3 = evaluate_graph_record("Paper_T3", *build_paper_tk(3))
    assert rec_t1["is_3_connected"] and rec_t1["gamma"] == 1 and not rec_t1["is_counterexample"]
    assert rec_t2["is_3_connected"] and rec_t2["gamma"] == 4 and not rec_t2["is_counterexample"]
    assert rec_t3["is_3_connected"] and rec_t3["kappa"] == 3 and rec_t3["is_non_bipartite"]
    assert rec_t3["n"] == 18 and rec_t3["m"] == 39
    assert rec_t3["gamma"] == 16 and rec_t3["chi_prime_2"] == -32 and not rec_t3["is_counterexample"]

    # 7. Negative Control: 2-connected Theta(2, 2, 3) (gamma = -1, caught because kappa = 2 < 3)
    rec_theta = evaluate_graph_record("Theta_2_2_3", *build_theta_2_2_3())
    assert rec_theta["is_non_bipartite"] and rec_theta["gamma"] == -1
    assert rec_theta["kappa"] == 2 and not rec_theta["is_3_connected"]
    assert rec_theta["cut_witness"] == (0, 1)
    assert rec_theta["is_counterexample"] is False

    # 8. Deliberate Mutation Controls
    # Mutant M1a & M1b: deleting one matching edge drops connectivity to kappa = 2 (caught!)
    edges_m1a = [e for e in rec_g["edges"] if e != (2, 4)]
    rec_m1a = evaluate_graph_record("Mutant_Delete_One_Matching_2_4", 11, edges_m1a)
    assert rec_m1a["kappa"] == 2 and not rec_m1a["is_3_connected"]
    assert rec_m1a["is_counterexample"] is False

    edges_m1b = [e for e in rec_g["edges"] if e != (1, 3)]
    rec_m1b = evaluate_graph_record("Mutant_Delete_One_Matching_1_3", 11, edges_m1b)
    assert rec_m1b["kappa"] == 2 and not rec_m1b["is_3_connected"]
    assert rec_m1b["is_counterexample"] is False

    # Mutant M2a: deleting both matching edges makes G bipartite (caught!)
    edges_m2a = [e for e in rec_g["edges"] if e not in ((1, 3), (2, 4))]
    rec_m2a = evaluate_graph_record("Mutant_Delete_Both_Matching", 11, edges_m2a)
    assert not rec_m2a["is_non_bipartite"] and rec_m2a["chi_2"] == 2 and rec_m2a["kappa"] == 1
    assert rec_m2a["is_counterexample"] is False

    # Mutant M2b: rewiring matching edges to (1, 8), (2, 9) keeps kappa = 3 yet becomes bipartite (caught!)
    edges_m2b = sorted(edges_m2a + [(1, 8), (2, 9)])
    rec_m2b = evaluate_graph_record("Mutant_Rewire_3Conn_Bipartite", 11, edges_m2b)
    assert rec_m2b["is_3_connected"] and rec_m2b["kappa"] == 3
    assert not rec_m2b["is_non_bipartite"] and rec_m2b["chi_2"] == 2
    assert rec_m2b["is_counterexample"] is False

    # Mutant M3: flipping sign of gamma fails K4 (and K3, Octahedron, T3) positive controls (caught!)
    rec_k4_flipped = evaluate_graph_record("Mutant_Flipped_Sign_on_K4", 4, rec_k4["edges"], compute_gamma_sign_flipped_mutant)
    assert rec_k4_flipped["gamma"] == -1 and rec_k4_flipped["is_counterexample"] is True
    assert rec_k4_flipped["gamma"] != 1  # Fails mandatory K4 positive control gamma(K4) == +1

    # Print concise audit summary
    print("=== CLEAN-ROOM EXACT-INTEGER REFEREE VERIFICATION PASSED ===")
    print(f"Witness G: n={rec_g['n']}, m={rec_g['m']}, kappa={rec_g['kappa']} (55 2-cuts connected; 3-cut (0,1,2) -> 4 comps)")
    print(f"Non-bipartite: odd cycle {rec_g['odd_cycle']} & explicit [0, 5, 1, 3, 8] verified")
    print(f"chi_G(q) desc (Alg A == Alg B == NBC == Hand): {expected_chi_desc}")
    print(f"Brute-force k-colorings k=0..4: {brute_counts}")
    print(f"Invariants at q=2: chi_G(2)={rec_g['chi_2']}, chi'_G(2)={rec_g['chi_prime_2']}, gamma(G)={rec_g['gamma']}")
    print(f"Quotient Q(q) desc: {expected_q_desc}, Q(1)=133, Q(2)=-1")
    print(f"Mobius coeffs asc: {mobius} (variations=1)")
    print(f"Rational evals: Q(19:10)={q_19_10}, Q(39:20)={q_39_20}")
    print(f"Rational evals: chi_G(19:10)={chi_19_10}, chi_G(39:20)={chi_39_20}")
    print(f"Sturm on Q [1, 19:10, 39:20, 2]: V={(vq_1, vq_19_10, vq_39_20, vq_2)} -> 1 root in (1,2), in (19:10, 39:20)")
    print(f"Sturm on chi [1+, 19:10, 39:20, 2-, 2]: V={(vchi_1_plus, vchi_19_10, vchi_39_20, vchi_2_minus, vchi_2)} -> 1 root in (1,2)")
    print(
        f"Positive controls: K3 gamma={rec_k3['gamma']}, K4 gamma={rec_k4['gamma']} (kappa={rec_k4['kappa']}), "
        f"Octahedron gamma={rec_oct['gamma']} (kappa={rec_oct['kappa']}), "
        f"T1 gamma={rec_t1['gamma']}, T2 gamma={rec_t2['gamma']}, T3 gamma={rec_t3['gamma']} (kappa={rec_t3['kappa']})"
    )
    print(f"Negative control Theta(2,2,3): gamma={rec_theta['gamma']}, kappa={rec_theta['kappa']} < 3 -> REJECTED")
    print(
        f"Mutation controls: M1a(del 2-4) kappa={rec_m1a['kappa']} (gamma={rec_m1a['gamma']}) -> REJECTED; "
        f"M1b(del 1-3) kappa={rec_m1b['kappa']} (gamma={rec_m1b['gamma']}) -> REJECTED; "
        f"M2a(del both) non_bip={rec_m2a['is_non_bipartite']}, chi(2)={rec_m2a['chi_2']} -> REJECTED; "
        f"M2b(rewire 3-conn bip) kappa={rec_m2b['kappa']}, non_bip={rec_m2b['is_non_bipartite']} -> REJECTED; "
        f"M3(sign flip) K4 gamma_flipped={rec_k4_flipped['gamma']} != +1 -> CAUGHT"
    )
    print("VERDICT: HOLDS")


if __name__ == "__main__":
    sys.exit(0 if main() is None else 1)
