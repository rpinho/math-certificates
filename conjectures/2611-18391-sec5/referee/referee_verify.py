"""Clean-room exact-integer adversarial referee verification for PROOF.md.

Constraints enforced:
- Pure Python exact integers only (integer floor division // only).
"""

import sys
import time


def popcount(x):
    c = 0
    while x:
        x &= x - 1
        c += 1
    return c


def ctz(x):
    if x == 0:
        return -1
    lsb = x & -x
    return lsb.bit_length() - 1


def iter_bits(mask):
    while mask:
        lsb = mask & -mask
        yield lsb.bit_length() - 1
        mask ^= lsb


def make_graph(n, edges):
    adj = [0] * n
    for u, v in edges:
        if u != v and 0 <= u < n and 0 <= v < n:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
    return n, tuple(adj)


def connected_components_mask(n, adj, subset_mask):
    rem = subset_mask
    comps = []
    while rem:
        seed = rem & -rem
        comp = seed
        frontier = seed
        while frontier:
            nxt = 0
            m = frontier
            while m:
                lsb = m & -m
                u = lsb.bit_length() - 1
                nxt |= adj[u]
                m ^= lsb
            nxt &= rem & ~comp
            comp |= nxt
            frontier = nxt
        comps.append(comp)
        rem ^= comp
    return comps


def is_connected_graph(n, adj):
    if n == 0:
        return False
    full = (1 << n) - 1
    comps = connected_components_mask(n, adj, full)
    return len(comps) == 1


# ============================================================================
# Independent Outerplanarity Oracle 1: Direct {K_4, K_{2,3}} Branch-Set Minors
# ============================================================================

def precompute_connected_masks(n, adj):
    limit = 1 << n
    conn = []
    nbr = {}
    for mask in range(1, limit):
        seed = mask & -mask
        comp = seed
        frontier = seed
        while frontier:
            nxt = 0
            m = frontier
            while m:
                lsb = m & -m
                u = lsb.bit_length() - 1
                nxt |= adj[u]
                m ^= lsb
            nxt &= mask & ~comp
            comp |= nxt
            frontier = nxt
        if comp == mask:
            conn.append(mask)
            nm = 0
            m = mask
            while m:
                lsb = m & -m
                u = lsb.bit_length() - 1
                nm |= adj[u]
                m ^= lsb
            nbr[mask] = nm & ~mask
    return conn, nbr


def has_k4_minor(n, adj, conn=None, nbr=None):
    if n < 4:
        return False
    if conn is None or nbr is None:
        conn, nbr = precompute_connected_masks(n, adj)
    cand = [m for m in conn if popcount(nbr[m]) >= 3]
    cand.sort(key=lambda m: (m & -m, popcount(m)))
    k = len(cand)
    for i0 in range(k):
        b0 = cand[i0]
        l0 = b0 & -b0
        nb0 = nbr[b0]
        c1_list = [
            cand[i1] for i1 in range(i0 + 1, k)
            if (cand[i1] & -cand[i1]) > l0
            and (cand[i1] & b0) == 0
            and (cand[i1] & nb0) != 0
        ]
        for idx1, b1 in enumerate(c1_list):
            l1 = b1 & -b1
            u01 = b0 | b1
            nb1 = nbr[b1]
            c2_list = [
                c1_list[idx2] for idx2 in range(idx1 + 1, len(c1_list))
                if (c1_list[idx2] & -c1_list[idx2]) > l1
                and (c1_list[idx2] & u01) == 0
                and (c1_list[idx2] & nb1) != 0
            ]
            for idx2, b2 in enumerate(c2_list):
                l2 = b2 & -b2
                u012 = u01 | b2
                nb2 = nbr[b2]
                for idx3 in range(idx2 + 1, len(c2_list)):
                    b3 = c2_list[idx3]
                    if (b3 & -b3) > l2 and (b3 & u012) == 0 and (b3 & nb2) != 0:
                        return True
    return False


def has_k23_minor(n, adj, conn=None, nbr=None):
    if n < 5:
        return False
    if conn is None or nbr is None:
        conn, nbr = precompute_connected_masks(n, adj)
    cand_a = [m for m in conn if popcount(nbr[m]) >= 3]
    cand_a.sort(key=lambda m: (m & -m, popcount(m)))
    ka = len(cand_a)
    for i0 in range(ka):
        a0 = cand_a[i0]
        la0 = a0 & -a0
        na0 = nbr[a0]
        for i1 in range(i0 + 1, ka):
            a1 = cand_a[i1]
            if (a1 & -a1) <= la0 or (a1 & a0) != 0:
                continue
            used = a0 | a1
            na0_out = na0 & ~used
            na1_out = nbr[a1] & ~used
            if popcount(na0_out) < 3 or popcount(na1_out) < 3:
                continue
            raw_c = [
                m for m in conn
                if (m & used) == 0 and (m & na0_out) != 0 and (m & na1_out) != 0
            ]
            if len(raw_c) < 3:
                continue
            raw_c.sort(key=popcount)
            minimal_c = []
            for m in raw_c:
                if not any((prev & ~m) == 0 for prev in minimal_c):
                    minimal_c.append(m)
            mc = len(minimal_c)
            if mc < 3:
                continue
            for j0 in range(mc):
                c0 = minimal_c[j0]
                for j1 in range(j0 + 1, mc):
                    c1 = minimal_c[j1]
                    if c0 & c1:
                        continue
                    u01 = c0 | c1
                    for j2 in range(j1 + 1, mc):
                        if (minimal_c[j2] & u01) == 0:
                            return True
    return False


def is_outerplanar_minor_free(n, adj):
    if n <= 3:
        return True
    conn, nbr = precompute_connected_masks(n, adj)
    if has_k4_minor(n, adj, conn, nbr):
        return False
    if has_k23_minor(n, adj, conn, nbr):
        return False
    return True


# ============================================================================
# Independent Outerplanarity Oracle 2: Block Decomposition + Polygon Embedding
# ============================================================================

def get_biconnected_blocks(n, adj):
    """Partition edges into blocks (maximal biconnected subgraphs)."""
    edges = []
    for u in range(n):
        for v in iter_bits(adj[u]):
            if u < v:
                edges.append((u, v))
    m = len(edges)
    if m == 0:
        return []
    # Two edges lie in the same block iff neither endpoint removal separates them;
    # build standard Tarjan DFS edge-stack blocks.
    tin = [-1] * n
    low = [-1] * n
    timer = [0]
    edge_stack = []
    blocks = []

    def dfs(u, parent):
        tin[u] = timer[0]
        low[u] = timer[0]
        timer[0] += 1
        for v in iter_bits(adj[u]):
            if v == parent:
                continue
            if tin[v] == -1:
                edge_stack.append((u, v) if u < v else (v, u))
                dfs(v, u)
                if low[v] < low[u]:
                    low[u] = low[v]
                if low[v] >= tin[u]:
                    blk = []
                    target = (u, v) if u < v else (v, u)
                    while True:
                        e = edge_stack.pop()
                        blk.append(e)
                        if e == target:
                            break
                    blocks.append(blk)
            elif tin[v] < tin[u]:
                edge_stack.append((u, v) if u < v else (v, u))
                if tin[v] < low[u]:
                    low[u] = tin[v]

    for start in range(n):
        if tin[start] == -1:
            dfs(start, -1)
    return blocks


def is_biconnected_block_outerplanar(verts, block_edges):
    k = len(verts)
    if k <= 3:
        return True
    if len(block_edges) > 2 * k - 3:
        return False
    idx_of = {v: i for i, v in enumerate(verts)}
    badj = [0] * k
    local_edges = []
    for u, v in block_edges:
        iu = idx_of[u]
        iv = idx_of[v]
        badj[iu] |= 1 << iv
        badj[iv] |= 1 << iu
        if iu < iv:
            local_edges.append((iu, iv))
        else:
            local_edges.append((iv, iu))

    for iu in range(k):
        if popcount(badj[iu]) < 2:
            return False

    # Search Hamiltonian cycle starting at local vertex 0
    path = [0]

    def search(curr, used_mask):
        if len(path) == k:
            if not ((badj[curr] >> 0) & 1):
                return False
            if path[1] > path[-1]:
                return False
            pos = [0] * k
            for p_i, v_i in enumerate(path):
                pos[v_i] = p_i
            chords = []
            for a, b in local_edges:
                pa = pos[a]
                pb = pos[b]
                if pa > pb:
                    pa, pb = pb, pa
                diff = pb - pa
                if diff != 1 and diff != k - 1:
                    chords.append((pa, pb))
            nc = len(chords)
            for i in range(nc):
                a, b = chords[i]
                for j in range(i + 1, nc):
                    c, d = chords[j]
                    if (a < c < b < d) or (c < a < d < b):
                        return False
            return True

        avail = badj[curr] & ~used_mask
        while avail:
            lsb = avail & -avail
            nxt = lsb.bit_length() - 1
            avail ^= lsb
            path.append(nxt)
            if search(nxt, used_mask | lsb):
                return True
            path.pop()
        return False

    return search(0, 1)


def is_outerplanar_embedding(n, adj):
    if n <= 3:
        return True
    blocks = get_biconnected_blocks(n, adj)
    for blk in blocks:
        vset = set()
        for u, v in blk:
            vset.add(u)
            vset.add(v)
        verts = sorted(vset)
        if not is_biconnected_block_outerplanar(verts, blk):
            return False
    return True


# ============================================================================
# Canonical Isomorphism Certificate & 1-WL Color Refinement
# ============================================================================

def color_refinement(n, adj, init_colors=None):
    if n == 0:
        return ()
    if init_colors is None:
        cols = [0] * n
    else:
        cols = list(init_colors)
    while True:
        sigs = []
        for u in range(n):
            nbr_cols = sorted(cols[v] for v in iter_bits(adj[u]))
            sigs.append((cols[u], tuple(nbr_cols)))
        unique_sigs = sorted(set(sigs))
        rank = {s: i for i, s in enumerate(unique_sigs)}
        new_cols = [rank[s] for s in sigs]
        if len(unique_sigs) == len(set(cols)):
            return tuple(new_cols)
        cols = new_cols


def canonical_cert(n, adj):
    if n <= 1:
        return (n, 0)
    base_cols = color_refinement(n, adj)

    best_code = [-1]

    def refine_and_branch(cols):
        # Group vertices by color
        cells = {}
        for u, c in enumerate(cols):
            cells.setdefault(c, []).append(u)
        ordered_colors = sorted(cells.keys())
        if len(ordered_colors) == n:
            order = [cells[c][0] for c in ordered_colors]
            code = 0
            bit = 0
            for i in range(n):
                ui = order[i]
                ai = adj[ui]
                for j in range(i + 1, n):
                    if (ai >> order[j]) & 1:
                        code |= 1 << bit
                    bit += 1
            if code > best_code[0]:
                best_code[0] = code
            return

        # Choose first non-singleton cell of smallest size
        target_c = None
        target_len = n + 1
        for c in ordered_colors:
            clen = len(cells[c])
            if 1 < clen < target_len:
                target_len = clen
                target_c = c
        max_c = ordered_colors[-1] + 1
        for chosen_u in cells[target_c]:
            next_cols = list(cols)
            next_cols[chosen_u] = max_c
            refined = color_refinement(n, adj, next_cols)
            refine_and_branch(refined)

    refine_and_branch(base_cols)
    return (n, best_code[0])


# ============================================================================
# Graph Enumeration (All Connected n <= 7; All Connected Outerplanar n <= 9)
# ============================================================================

def enumerate_all_connected_graphs(max_n):
    by_n = {1: [(1, (0,))]}
    for n in range(2, max_n + 1):
        seen = {}
        for prev_n, prev_adj in by_n[n - 1]:
            limit = 1 << prev_n
            for nbr_mask in range(1, limit):
                new_adj = list(prev_adj) + [nbr_mask]
                for u in iter_bits(nbr_mask):
                    new_adj[u] |= 1 << prev_n
                t_adj = tuple(new_adj)
                cert = canonical_cert(n, t_adj)
                if cert not in seen:
                    seen[cert] = (n, t_adj)
        by_n[n] = list(seen.values())
    return by_n


def enumerate_connected_outerplanar_graphs(max_n):
    """Every connected outerplanar graph on n >= 2 vertices has a non-cut
    vertex of degree 1 or 2, so 1- and 2-neighbor extensions are exhaustive."""
    by_n = {1: [(1, (0,))]}
    for n in range(2, max_n + 1):
        seen = {}
        for prev_n, prev_adj in by_n[n - 1]:
            cand_masks = []
            for u in range(prev_n):
                cand_masks.append(1 << u)
                for v in range(u + 1, prev_n):
                    cand_masks.append((1 << u) | (1 << v))
            for nbr_mask in cand_masks:
                new_adj = list(prev_adj) + [nbr_mask]
                for u in iter_bits(nbr_mask):
                    new_adj[u] |= 1 << prev_n
                t_adj = tuple(new_adj)
                if not is_outerplanar_minor_free(n, t_adj):
                    continue
                cert = canonical_cert(n, t_adj)
                if cert not in seen:
                    seen[cert] = (n, t_adj)
        by_n[n] = list(seen.values())
    return by_n


# ============================================================================
# Equitable Partitions, Color Graph K, Emulator Construction & Minor Ops
# ============================================================================

def is_equitable_coloring(n, adj, c_map, num_colors):
    fibers = [[] for _ in range(num_colors)]
    for u in range(n):
        fibers[c_map[u]].append(u)
    for f in fibers:
        if not f:
            return False
    for i in range(num_colors):
        rep = fibers[i][0]
        for j in range(num_colors):
            j_mask = 0
            for v in fibers[j]:
                j_mask |= 1 << v
            expected = popcount(adj[rep] & j_mask)
            for u in fibers[i][1:]:
                if popcount(adj[u] & j_mask) != expected:
                    return False
    return True


def brute_all_set_partitions(n):
    """Generate all Bell(n) canonical set partitions as (c_map, k) pairs."""
    results = []
    cur = [0] * n

    def rec(pos, num_used):
        if pos == n:
            results.append((tuple(cur), num_used))
            return
        for c in range(num_used):
            cur[pos] = c
            rec(pos + 1, num_used)
        cur[pos] = num_used
        rec(pos + 1, num_used + 1)

    rec(0, 0)
    return results


def all_equitable_partitions(n, adj):
    """Enumerate every equitable partition of (n, adj) up to color relabeling.
    Every equitable partition refines uniform 1-WL color refinement."""
    cr = color_refinement(n, adj)
    num_cr = max(cr) + 1
    cells = [[] for _ in range(num_cr)]
    for u, c in enumerate(cr):
        cells[c].append(u)

    # Generate sub-partitions of each CR cell, then filter by equitability.
    cell_subparts = []
    for cell in cells:
        m = len(cell)
        subs = brute_all_set_partitions(m)
        cell_subparts.append((cell, subs))

    equitable_list = []

    def combine(cell_idx, offset, assign):
        if cell_idx == num_cr:
            # Canonicalize color numbering by first appearance in 0..n-1
            remap = {}
            canon = []
            nxt = 0
            for u in range(n):
                old = assign[u]
                if old not in remap:
                    remap[old] = nxt
                    nxt += 1
                canon.append(remap[old])
            t_canon = tuple(canon)
            if is_equitable_coloring(n, adj, t_canon, nxt):
                equitable_list.append((t_canon, nxt))
            return

        cell, subs = cell_subparts[cell_idx]
        for local_map, local_k in subs:
            for idx_in_cell, u in enumerate(cell):
                assign[u] = offset + local_map[idx_in_cell]
            combine(cell_idx + 1, offset + local_k, assign)

    combine(0, 0, [0] * n)
    return equitable_list


def build_color_graph_and_step0(n, adj, c_map, k):
    """Build K, weights w, underlying simple H = tilde(K), and F = G minus
    within-color edges per Step 0 of PROOF.md."""
    fibers = [[] for _ in range(k)]
    fiber_masks = [0] * k
    for u in range(n):
        ci = c_map[u]
        fibers[ci].append(u)
        fiber_masks[ci] |= 1 << u
    weights = tuple(len(f) for f in fibers)

    k_mat = [[0] * k for _ in range(k)]
    for i in range(k):
        rep = fibers[i][0]
        for j in range(k):
            k_mat[i][j] = popcount(adj[rep] & fiber_masks[j])

    # Underlying simple graph H = tilde(K): forget weights, directions, loops
    h_adj = [0] * k
    for i in range(k):
        for j in range(k):
            if i != j and (k_mat[i][j] > 0 or k_mat[j][i] > 0):
                h_adj[i] |= 1 << j
                h_adj[j] |= 1 << i

    # F = G without within-color edges
    f_adj = [0] * n
    for u in range(n):
        cu = c_map[u]
        f_adj[u] = adj[u] & ~fiber_masks[cu]

    return weights, k_mat, (k, tuple(h_adj)), (n, tuple(f_adj))


def verify_emulator(f_graph, h_graph, p_map):
    """Check exact emulator properties from PROOF.md line 5:
    1. F and H are finite simple graphs (no self-loops, symmetric adjacency).
    2. p : V(F) -> V(H) is vertex-surjective.
    3. Homomorphism: every edge xy of F maps to an edge p(x)p(y) of H.
    4. Local surjectivity: for every x in V(F) and every neighbor j of p(x)
       in H, some neighbor y of x in F satisfies p(y) == j.
    Returns (ok, reason)."""
    fn, f_adj = f_graph
    hn, h_adj = h_graph
    for u in range(fn):
        if (f_adj[u] >> u) & 1:
            return False, "F has a self-loop"
    for i in range(hn):
        if (h_adj[i] >> i) & 1:
            return False, "H has a self-loop"

    seen_colors = set()
    for x in range(fn):
        px = p_map[x]
        if px < 0 or px >= hn:
            return False, "p(x) out of range"
        seen_colors.add(px)
    if len(seen_colors) != hn:
        return False, "p is not vertex-surjective"

    # Homomorphism check
    for x in range(fn):
        px = p_map[x]
        for y in iter_bits(f_adj[x]):
            py = p_map[y]
            if px == py or not ((h_adj[px] >> py) & 1):
                return False, "non-homomorphism edge in F"

    # Local surjectivity check
    for x in range(fn):
        px = p_map[x]
        got = 0
        for y in iter_bits(f_adj[x]):
            got |= 1 << p_map[y]
        if (h_adj[px] & ~got) != 0:
            return False, "local surjectivity violated"

    return True, "ok"


def delete_emulator_vertex(f_graph, h_graph, p_map, del_color):
    fn, f_adj = f_graph
    hn, h_adj = h_graph
    keep_f = [x for x in range(fn) if p_map[x] != del_color]
    keep_h = [i for i in range(hn) if i != del_color]
    h_remap = {old: idx for idx, old in enumerate(keep_h)}
    f_remap = {old: idx for idx, old in enumerate(keep_f)}

    new_h_edges = []
    for i in keep_h:
        for j in iter_bits(h_adj[i]):
            if j != del_color and i < j:
                new_h_edges.append((h_remap[i], h_remap[j]))
    new_f_edges = []
    for x in keep_f:
        for y in iter_bits(f_adj[x]):
            if p_map[y] != del_color and x < y:
                new_f_edges.append((f_remap[x], f_remap[y]))
    new_p = tuple(h_remap[p_map[x]] for x in keep_f)
    return (
        make_graph(len(keep_f), new_f_edges),
        make_graph(len(keep_h), new_h_edges),
        new_p,
    )


def delete_emulator_edge(f_graph, h_graph, p_map, a, b):
    fn, f_adj = f_graph
    hn, h_adj = h_graph
    new_h_adj = list(h_adj)
    new_h_adj[a] &= ~(1 << b)
    new_h_adj[b] &= ~(1 << a)

    new_f_adj = list(f_adj)
    for x in range(fn):
        px = p_map[x]
        if px == a or px == b:
            other = b if px == a else a
            for y in iter_bits(f_adj[x]):
                if p_map[y] == other:
                    new_f_adj[x] &= ~(1 << y)
    return (fn, tuple(new_f_adj)), (hn, tuple(new_h_adj)), p_map


def contract_emulator_edge(f_graph, h_graph, p_map, a, b):
    """Exact implementation of Section 1 edge contraction in PROOF.md:
    - S = F[p^{-1}(a) union p^{-1}(b)].
    - Verify each connected component of S meets both fibers, and no F-edge
      connects two distinct components of S.
    - Contract each component of S to one vertex in F', discarding loops and
      duplicate edges, mapping to merged color z in H'."""
    fn, f_adj = f_graph
    hn, h_adj = h_graph
    assert a != b and ((h_adj[a] >> b) & 1)

    u_mask = 0
    a_mask = 0
    b_mask = 0
    for x in range(fn):
        if p_map[x] == a:
            u_mask |= 1 << x
            a_mask |= 1 << x
        elif p_map[x] == b:
            u_mask |= 1 << x
            b_mask |= 1 << x

    comps = connected_components_mask(fn, f_adj, u_mask)
    assert len(comps) >= 1, "empty fiber union"
    for comp in comps:
        assert (comp & a_mask) != 0 and (comp & b_mask) != 0, (
            "component of S lacks one of colors a, b"
        )
    # Check explicitly that no edge of F connects distinct components of S
    for idx1 in range(len(comps)):
        c1 = comps[idx1]
        nbr_c1 = 0
        for x in iter_bits(c1):
            nbr_c1 |= f_adj[x]
        for idx2 in range(idx1 + 1, len(comps)):
            assert (nbr_c1 & comps[idx2]) == 0, (
                "distinct components of induced S had an edge between them"
            )

    # Build H' = simple contraction of a, b into z (last index hn - 2)
    keep_h = [i for i in range(hn) if i != a and i != b]
    z_color = len(keep_h)
    h_remap = {old: idx for idx, old in enumerate(keep_h)}
    h_remap[a] = z_color
    h_remap[b] = z_color
    h_edges = []
    for i in range(hn):
        for j in iter_bits(h_adj[i]):
            if i < j:
                ni = h_remap[i]
                nj = h_remap[j]
                if ni != nj:
                    h_edges.append((ni, nj))
    new_h = make_graph(hn - 1, h_edges)

    # Build F': outside vertices keep individual identities; each component of S
    # becomes one new vertex mapped to z_color.
    outside_f = [x for x in range(fn) if not ((u_mask >> x) & 1)]
    f_remap = {}
    new_p = []
    for idx, x in enumerate(outside_f):
        f_remap[x] = idx
        new_p.append(h_remap[p_map[x]])
    base = len(outside_f)
    for c_idx, comp in enumerate(comps):
        vid = base + c_idx
        new_p.append(z_color)
        for x in iter_bits(comp):
            f_remap[x] = vid

    f_edges = []
    for x in range(fn):
        for y in iter_bits(f_adj[x]):
            if x < y:
                nx = f_remap[x]
                ny = f_remap[y]
                if nx != ny:
                    f_edges.append((nx, ny))
    new_f = make_graph(base + len(comps), f_edges)
    return new_f, new_h, tuple(new_p), len(comps)


# ============================================================================
# Section 2 Outerplane Ear Lemmas Verification Helpers
# ============================================================================

def is_triangle_free(n, adj):
    for u in range(n):
        au = adj[u]
        for v in iter_bits(au):
            if v > u and (au & adj[v]) != 0:
                return False
    return True


def min_degree(n, adj):
    if n == 0:
        return 0
    return min(popcount(adj[u]) for u in range(n))


def has_deg_at_most_2(n, adj):
    return any(popcount(adj[u]) <= 2 for u in range(n))


def has_adjacent_deg2_pair(n, adj):
    deg = [popcount(adj[u]) for u in range(n)]
    for u in range(n):
        if deg[u] == 2:
            for v in iter_bits(adj[u]):
                if v > u and deg[v] == 2:
                    return True
    return False


# ============================================================================
# Paper Baseline Reproductions (Coste-Csikos-Viennot TikZ Figures)
# ============================================================================

def build_paper_square_kites():
    """Reproduce G and H from square_kites TikZ figure (Figure 1, n=10)."""
    # Vertex order: 0:t, 1:b, 2:a1, 3:a2, 4:b1, 5:b2, 6:l1, 7:l2, 8:r1, 9:r2
    outer = [
        (0, 2), (2, 6), (6, 7), (7, 4), (4, 1),
        (1, 5), (5, 9), (9, 8), (8, 3), (3, 0),
    ]
    g_graph = make_graph(10, outer + [(2, 4), (3, 5)])
    h_graph = make_graph(10, outer + [(2, 3), (4, 5)])
    # Colors: f=0 ({t,b}), e=1 ({a1,a2,b1,b2}), g=2 ({l1,l2,r1,r2})
    c_map = (0, 0, 1, 1, 1, 1, 2, 2, 2, 2)
    return g_graph, h_graph, c_map, 3


def build_paper_cactus_ctrex():
    """Reproduce the two 12-vertex outerplanar graphs from cactus_ctrex_hor TikZ."""
    # Left graph: octagon 0..7 + triangles (0,8,9) and (4,10,11)
    e1 = [(i, (i + 1) % 8) for i in range(8)]
    e1 += [(0, 8), (0, 9), (8, 9), (4, 10), (4, 11), (10, 11)]
    c1 = (3, 1, 0, 1, 3, 1, 0, 1, 2, 2, 2, 2)  # a=0, b=1, c=2, d=3

    # Right graph: hexagon 0..5 + diamonds at 0 (6,7,8) and at 3 (9,10,11)
    e2 = [(i, (i + 1) % 6) for i in range(6)]
    e2 += [(0, 6), (0, 7), (6, 8), (7, 8), (3, 9), (3, 10), (9, 11), (10, 11)]
    c2 = (3, 2, 2, 3, 2, 2, 1, 1, 0, 1, 1, 0)
    return make_graph(12, e1), c1, make_graph(12, e2), c2, 4


def build_paper_planar_ctrex():
    """Reproduce G_0 (outerplanar) and G_1 (non-outerplanar treewidth-2)
    from planar_ctrex TikZ figure (Figure 2, n=7)."""
    # 0:r, 1:b1, 2:b2, 3:g1, 4:g2, 5:g3, 6:g4
    tree_edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
    g0 = make_graph(7, tree_edges + [(3, 4), (5, 6)])
    g1 = make_graph(7, tree_edges + [(4, 5), (3, 6)])
    c_map = (0, 1, 1, 2, 2, 2, 2)
    return g0, g1, c_map, 3


# ============================================================================
# Main Verification Suite
# ============================================================================

def main():
    t0 = time.time_ns()
    print("=== Clean-Room Referee Verification: arXiv:2611.18391v1 Sec 5 ===")

    # 1. Exhaustive all-connected-graphs check (1 <= n <= 7) & dual oracle check
    all_conn = enumerate_all_connected_graphs(7)
    conn_counts = [len(all_conn[n]) for n in range(1, 8)]
    expected_conn_counts = [1, 1, 2, 6, 21, 112, 853]
    assert conn_counts == expected_conn_counts, (
        f"Connected graph count mismatch: {conn_counts}"
    )
    total_conn_checked = 0
    outer_from_all = {}
    for n in range(1, 8):
        olist = []
        for g in all_conn[n]:
            total_conn_checked += 1
            r_minor = is_outerplanar_minor_free(*g)
            r_embed = is_outerplanar_embedding(*g)
            assert r_minor == r_embed, (
                f"Oracle disagreement at n={n}: minor={r_minor}, embed={r_embed}"
            )
            if r_minor:
                olist.append(g)
        outer_from_all[n] = olist
    print(
        f"[PASS] Dual outerplanarity oracles agreed on all {total_conn_checked} "
        f"connected simple graphs for n=1..7 (counts {conn_counts})."
    )

    # 2. Connected outerplanar enumeration up to n=9 & cross-check on n=1..7
    outer_by_n = enumerate_connected_outerplanar_graphs(9)
    outer_counts = [len(outer_by_n[n]) for n in range(1, 10)]
    for n in range(1, 8):
        certs_a = {canonical_cert(*g) for g in outer_from_all[n]}
        certs_b = {canonical_cert(*g) for g in outer_by_n[n]}
        assert certs_a == certs_b, f"Outerplanar generator mismatch at n={n}"
    for n in range(8, 10):
        for g in outer_by_n[n]:
            assert is_outerplanar_embedding(*g), (
                f"Embedding oracle rejected n={n} outerplanar graph"
            )
    print(
        f"[PASS] Connected outerplanar graphs enumerated for n=1..9: "
        f"{outer_counts} (sum={sum(outer_counts)})."
    )

    # 3. Cross-check equitable partition generator against raw Bell(n) on n=1..5
    bell_checked = 0
    for n in range(1, 6):
        raw_parts = brute_all_set_partitions(n)
        for _, adj in outer_by_n[n]:
            raw_eq = {
                c_map for c_map, k in raw_parts
                if is_equitable_coloring(n, adj, c_map, k)
            }
            fast_eq = {c_map for c_map, _ in all_equitable_partitions(n, adj)}
            assert raw_eq == fast_eq, "Equitable partition generator missed a case"
            bell_checked += 1
    print(
        f"[PASS] Equitable partition enumerator matched raw Bell(n) search "
        f"across all {bell_checked} connected outerplanar graphs for n=1..5."
    )

    # 4. Exhaustive Step 0 + Step 1 + Theorem check across ALL connected
    #    outerplanar graphs for n=1..7 and ALL equitable partitions!
    total_eq_pairs = 0
    unrooted_eq_pairs = 0
    non_orbit_or_unequal_pairs = 0
    with_loops_pairs = 0
    disconnected_f_pairs = 0
    contractions_checked = 0
    multi_comp_contractions = 0
    deletions_checked = 0

    for n in range(1, 8):
        for _, adj in outer_by_n[n]:
            eq_parts = all_equitable_partitions(n, adj)
            for c_map, k in eq_parts:
                total_eq_pairs += 1
                weights, k_mat, h_graph, f_graph = build_color_graph_and_step0(
                    n, adj, c_map, k
                )
                hn, h_adj = h_graph
                fn, f_adj = f_graph

                if 1 not in weights:
                    unrooted_eq_pairs += 1

                # Double-counting & symmetric support check
                has_loop = False
                has_asym = False
                for i in range(k):
                    assert weights[i] >= 1
                    if k_mat[i][i] > 0:
                        has_loop = True
                    for j in range(i + 1, k):
                        assert weights[i] * k_mat[i][j] == weights[j] * k_mat[j][i]
                        assert (k_mat[i][j] > 0) == (k_mat[j][i] > 0)
                        if k_mat[i][j] != k_mat[j][i]:
                            has_asym = True
                if has_loop:
                    with_loops_pairs += 1
                if has_asym:
                    non_orbit_or_unequal_pairs += 1
                if not is_connected_graph(fn, f_adj):
                    disconnected_f_pairs += 1

                # Step 0 checks: F is outerplanar, c: F -> H is an emulator
                assert is_outerplanar_minor_free(fn, f_adj)
                assert is_outerplanar_embedding(fn, f_adj)
                ok, reason = verify_emulator(f_graph, h_graph, c_map)
                assert ok, f"Step 0 emulator failed: {reason}"

                # Main Theorem check: H = tilde(K) is outerplanar (both oracles!)
                assert is_outerplanar_minor_free(hn, h_adj), (
                    f"COUNTEREXAMPLE FOUND: H non-outerplanar at n={n}!"
                )
                assert is_outerplanar_embedding(hn, h_adj), (
                    f"COUNTEREXAMPLE FOUND (embedding): H non-outerplanar at n={n}!"
                )

                # Step 1 checks: every edge contraction, edge deletion, and
                # vertex deletion on (F, H, c_map) preserves outerplanar emulator!
                for a in range(hn):
                    if hn >= 2 and a == 0:
                        df, dh, dp = delete_emulator_vertex(f_graph, h_graph, c_map, a)
                        ok_v, msg_v = verify_emulator(df, dh, dp)
                        assert ok_v, f"Vertex deletion broke emulator: {msg_v}"
                        assert is_outerplanar_minor_free(*df)
                        assert is_outerplanar_minor_free(*dh)
                        deletions_checked += 1
                    for b in iter_bits(h_adj[a]):
                        if a < b:
                            ef, eh, ep = delete_emulator_edge(
                                f_graph, h_graph, c_map, a, b
                            )
                            ok_e, msg_e = verify_emulator(ef, eh, ep)
                            assert ok_e, f"Edge deletion broke emulator: {msg_e}"
                            assert is_outerplanar_minor_free(*ef)
                            deletions_checked += 1

                            cf, ch, cp, n_comps = contract_emulator_edge(
                                f_graph, h_graph, c_map, a, b
                            )
                            ok_c, msg_c = verify_emulator(cf, ch, cp)
                            assert ok_c, f"Edge contraction broke emulator: {msg_c}"
                            assert is_outerplanar_minor_free(*cf)
                            assert is_outerplanar_embedding(*cf)
                            assert is_outerplanar_minor_free(*ch)
                            contractions_checked += 1
                            if n_comps >= 2:
                                multi_comp_contractions += 1

    print(
        f"[PASS] Exhaustive n=1..7 Theorem + Step 0 + Step 1 verified across "
        f"{total_eq_pairs} (G, c) pairs\n"
        f"       (unrooted={unrooted_eq_pairs}, loops={with_loops_pairs}, "
        f"asymmetric_K={non_orbit_or_unequal_pairs}, "
        f"disconnected_F={disconnected_f_pairs},\n"
        f"        contractions={contractions_checked} "
        f"[multi_comp_S={multi_comp_contractions}], "
        f"deletions={deletions_checked})."
    )

    # 5. Structured & CR checks on n=8..9 outerplanar graphs (uniform + 1-rooted)
    n89_pairs = 0
    n89_unrooted = 0
    for n in (8, 9):
        for _, adj in outer_by_n[n]:
            # Uniform CR (often unrooted!) + one vertex-rooted CR
            c_unif = color_refinement(n, adj)
            k_unif = max(c_unif) + 1
            for c_map, k in (
                (c_unif, k_unif),
                (
                    color_refinement(n, adj, [1] + [0] * (n - 1)),
                    max(color_refinement(n, adj, [1] + [0] * (n - 1))) + 1,
                ),
            ):
                # Remap colors canonically to 0..k-1
                remap = {}
                canon = []
                nxt = 0
                for u in range(n):
                    old = c_map[u]
                    if old not in remap:
                        remap[old] = nxt
                        nxt += 1
                    canon.append(remap[old])
                t_canon = tuple(canon)
                weights, _, h_graph, f_graph = build_color_graph_and_step0(
                    n, adj, t_canon, nxt
                )
                if 1 not in weights:
                    n89_unrooted += 1
                ok, reason = verify_emulator(f_graph, h_graph, t_canon)
                assert ok, reason
                assert is_outerplanar_minor_free(*h_graph)
                assert is_outerplanar_embedding(*h_graph)
                n89_pairs += 1
    print(
        f"[PASS] Verified {n89_pairs} CR equitable partitions across ALL "
        f"n=8..9 connected outerplanar graphs (unrooted={n89_unrooted})."
    )

    # 6. Step 2 Ear Lemmas direct check across ALL connected outerplanar n=1..9
    lemma_i_count = 0
    lemma_ii_count = 0
    lemma_ii_cutvertex_count = 0
    for n in range(1, 10):
        for _, adj in outer_by_n[n]:
            assert has_deg_at_most_2(n, adj), f"Lemma 2(i) failed at n={n}"
            lemma_i_count += 1
            if is_triangle_free(n, adj) and min_degree(n, adj) >= 2:
                assert has_adjacent_deg2_pair(n, adj), (
                    f"Lemma 2(ii) failed at n={n}!"
                )
                lemma_ii_count += 1
                if len(get_biconnected_blocks(n, adj)) >= 2:
                    lemma_ii_cutvertex_count += 1
    print(
        f"[PASS] Section 2 Ear Lemmas verified on all {lemma_i_count} connected "
        f"outerplanar graphs (n=1..9);\n"
        f"       Lemma 2(ii) held on all {lemma_ii_count} triangle-free delta>=2 "
        f"outerplanar graphs (including {lemma_ii_cutvertex_count} with cut-vertices)."
    )

    # 7. Reproduction of Coste-Csikos-Viennot TikZ examples
    sk_g, sk_h, sk_c, sk_k = build_paper_square_kites()
    assert canonical_cert(*sk_g) != canonical_cert(*sk_h)
    assert is_outerplanar_minor_free(*sk_g) and is_outerplanar_embedding(*sk_g)
    assert is_outerplanar_minor_free(*sk_h) and is_outerplanar_embedding(*sk_h)
    assert is_triangle_free(*sk_g) and not is_triangle_free(*sk_h)
    assert is_equitable_coloring(10, sk_g[1], sk_c, sk_k)
    assert is_equitable_coloring(10, sk_h[1], sk_c, sk_k)
    w_g, km_g, h_sk_g, f_sk_g = build_color_graph_and_step0(10, sk_g[1], sk_c, sk_k)
    w_h, km_h, h_sk_h, f_sk_h = build_color_graph_and_step0(10, sk_h[1], sk_c, sk_k)
    assert w_g == w_h == (2, 4, 4) and km_g == km_h
    assert km_g[0][1] == 2 and km_g[1][0] == 1 and km_g[1][1] == 1 and km_g[2][2] == 1
    assert verify_emulator(f_sk_g, h_sk_g, sk_c)[0]
    assert verify_emulator(f_sk_h, h_sk_h, sk_c)[0]
    assert is_outerplanar_minor_free(*h_sk_g) and is_outerplanar_embedding(*h_sk_g)

    cac1, cc1, cac2, cc2, c_k = build_paper_cactus_ctrex()
    assert canonical_cert(*cac1) != canonical_cert(*cac2)
    assert is_outerplanar_minor_free(*cac1) and is_outerplanar_minor_free(*cac2)
    assert is_equitable_coloring(12, cac1[1], cc1, c_k)
    assert is_equitable_coloring(12, cac2[1], cc2, c_k)
    wc1, kmc1, h_cac1, _ = build_color_graph_and_step0(12, cac1[1], cc1, c_k)
    wc2, kmc2, h_cac2, _ = build_color_graph_and_step0(12, cac2[1], cc2, c_k)
    assert wc1 == wc2 == (2, 4, 4, 2) and kmc1 == kmc2
    assert is_outerplanar_minor_free(*h_cac1) and is_outerplanar_embedding(*h_cac1)

    pc_g0, pc_g1, pc_c, pc_k = build_paper_planar_ctrex()
    assert is_outerplanar_minor_free(*pc_g0) and is_outerplanar_embedding(*pc_g0)
    assert not is_outerplanar_minor_free(*pc_g1)
    assert not is_outerplanar_embedding(*pc_g1)
    assert not has_k4_minor(*pc_g1) and has_k23_minor(*pc_g1)
    assert is_equitable_coloring(7, pc_g0[1], pc_c, pc_k)
    assert is_equitable_coloring(7, pc_g1[1], pc_c, pc_k)
    print(
        "[PASS] Reproduced paper TikZ examples: square_kites (n=10), "
        "cactus_ctrex_hor (n=12), and planar_ctrex (n=7)."
    )

    # 8. Negative Controls & Deliberate Proof-Mutation Controls
    # NC1: K_4 and K_{2,3} rejected by both outerplanarity oracles
    k4 = make_graph(4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
    k23 = make_graph(5, [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)])
    assert has_k4_minor(*k4) and not has_k23_minor(*k4)
    assert not is_outerplanar_minor_free(*k4) and not is_outerplanar_embedding(*k4)
    assert has_k23_minor(*k23) and not has_k4_minor(*k23)
    assert not is_outerplanar_minor_free(*k23) and not is_outerplanar_embedding(*k23)

    # NC2: Planar (non-outerplanar) equitable coloring CAN produce K_4 quotient!
    # 3-cube Q_3 (planar, bipartite, 3-regular) colored by antipodal pairs -> K_4
    q3_edges = [
        (u, u ^ (1 << bit)) for u in range(8) for bit in range(3) if u < (u ^ (1 << bit))
    ]
    q3 = make_graph(8, q3_edges)
    q3_antipodal = tuple(min(u, 7 ^ u) for u in range(8))
    assert is_equitable_coloring(8, q3[1], q3_antipodal, 4)
    _, _, h_q3, f_q3 = build_color_graph_and_step0(8, q3[1], q3_antipodal, 4)
    assert verify_emulator(f_q3, h_q3, q3_antipodal)[0]
    assert not is_outerplanar_minor_free(*h_q3)  # H = K_4 is NOT outerplanar!

    # NC3: Dropping triangle-free or delta>=2 breaks Lemma 2(ii)
    diamond = make_graph(4, [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)])
    triforce = make_graph(
        6,
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 2), (2, 4), (4, 0)],
    )
    path3 = make_graph(3, [(0, 1), (1, 2)])
    assert is_outerplanar_minor_free(*diamond) and min_degree(*diamond) == 2
    assert not is_triangle_free(*diamond) and not has_adjacent_deg2_pair(*diamond)
    assert is_outerplanar_minor_free(*triforce) and min_degree(*triforce) == 2
    assert not is_triangle_free(*triforce) and not has_adjacent_deg2_pair(*triforce)
    assert is_outerplanar_minor_free(*path3) and is_triangle_free(*path3)
    assert min_degree(*path3) == 1 and not has_adjacent_deg2_pair(*path3)

    # Mutation M1: Dropping local surjectivity allows outerplanar F -> K_4
    # Walk in K_4 covering all 6 edges via a 7-vertex star-like tree:
    # center 0 adjacent to 1,2,3; 1 adj to 4(col 2),5(col 3); 2 adj to 6(col 3)
    f_mut1 = make_graph(7, [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6)])
    p_mut1 = (0, 1, 2, 3, 2, 3, 3)
    assert is_outerplanar_minor_free(*f_mut1)
    # Check vertex- and edge-surjective homomorphism holds, ONLY local surjectivity fails!
    seen_e = set()
    for x in range(7):
        for y in iter_bits(f_mut1[1][x]):
            if x < y:
                a_c, b_c = p_mut1[x], p_mut1[y]
                assert a_c != b_c
                seen_e.add((min(a_c, b_c), max(a_c, b_c)))
    assert len(seen_e) == 6  # All 6 edges of K_4 covered!
    ok_m1, msg_m1 = verify_emulator(f_mut1, k4, p_mut1)
    assert not ok_m1 and msg_m1 == "local surjectivity violated"

    # Mutation M2: Merging entire fiber union p^{-1}(a) U p^{-1}(b) into ONE vertex
    # instead of contracting connected components of S independently destroys outerplanarity!
    # 10-vertex spider tree F equitably colored over P_4 = (0-1-2-3), contract edge (2,3):
    spider_edges = [
        (0, 1), (0, 2), (0, 3),
        (1, 4), (2, 5), (3, 6),
        (4, 7), (5, 8), (6, 9),
    ]
    f_spider = make_graph(10, spider_edges)
    p_spider = (0, 1, 1, 1, 2, 2, 2, 3, 3, 3)
    assert is_outerplanar_minor_free(*f_spider)
    assert is_equitable_coloring(10, f_spider[1], p_spider, 4)
    _, _, h_p4, _ = build_color_graph_and_step0(10, f_spider[1], p_spider, 4)
    # Valid PROOF.md component-wise contraction keeps F' outerplanar (3 components):
    cf_good, ch_good, cp_good, n_sp_comps = contract_emulator_edge(
        f_spider, h_p4, p_spider, 2, 3
    )
    assert n_sp_comps == 3
    assert is_outerplanar_minor_free(*cf_good) and verify_emulator(cf_good, ch_good, cp_good)[0]
    # Mutated whole-fiber merge creates K_{2,3} between vertex 0 and merged vertex 4!
    bad_remap = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4}
    bad_edges = [
        (bad_remap[u], bad_remap[v]) for u, v in spider_edges if bad_remap[u] != bad_remap[v]
    ]
    cf_bad = make_graph(5, bad_edges)
    assert has_k23_minor(*cf_bad) and not is_outerplanar_minor_free(*cf_bad)

    # Mutation M3: Contracting only a partial matching instead of full connected
    # components of S creates an illegal monochromatic edge mapping to loop zz!
    c4_graph = make_graph(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
    p_c4 = (0, 1, 0, 1)
    h_k2 = make_graph(2, [(0, 1)])
    assert verify_emulator(c4_graph, h_k2, p_c4)[0]
    # Mutated contraction: contract only edges (0,1)->0 and (2,3)->1, leaving edge 0-1 over z=0!
    f_bad_match = make_graph(2, [(0, 1)])
    h_k1 = make_graph(1, [])
    ok_m3, msg_m3 = verify_emulator(f_bad_match, h_k1, (0, 0))
    assert not ok_m3 and msg_m3 == "non-homomorphism edge in F"

    # Mutation M4: Keeping within-color edges in Step 0 breaks homomorphism!
    k3_graph = make_graph(3, [(0, 1), (1, 2), (2, 0)])
    p_k3 = (0, 0, 1)
    assert is_equitable_coloring(3, k3_graph[1], p_k3, 2)
    ok_m4, msg_m4 = verify_emulator(k3_graph, h_k2, p_k3)
    assert not ok_m4 and msg_m4 == "non-homomorphism edge in F"

    print(
        "[PASS] All negative controls (NC1-NC3) and proof-mutation controls "
        "(M1-M4) behaved as predicted."
    )

    elapsed_ms = (time.time_ns() - t0) // 1000000
    print(f"[PASS] Completed in {elapsed_ms} ms.")
    print("ALL REFEREE CHECKS PASSED.")


if __name__ == "__main__":
    main()
