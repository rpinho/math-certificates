import sys


# ============================================================================
# Exact Polynomial Arithmetic in Z[x]
# Canonical representation: tuple of ints (c_0, c_1, ..., c_d) with c_d != 0,
# and empty tuple () for the zero polynomial.
# ============================================================================

ZERO_POLY = ()
ONE_POLY = (1,)
X_POLY = (0, 1)


def poly_trim(coeffs):
     end = len(coeffs)
     while end > 0 and coeffs[end - 1] == 0:
         end -= 1
     return tuple(coeffs[:end])


def poly_const(c):
    if c == 0:
        return ZERO_POLY
    return (int(c),)


def poly_add(p, q):
    lp = len(p)
    lq = len(q)
    m = lp if lp >= lq else lq
    out = [0] * m
    for i in range(lp):
        out[i] += p[i]
    for i in range(lq):
        out[i] += q[i]
    return poly_trim(out)


def poly_sub(p, q):
    lp = len(p)
    lq = len(q)
    m = lp if lp >= lq else lq
    out = [0] * m
    for i in range(lp):
        out[i] += p[i]
    for i in range(lq):
        out[i] -= q[i]
    return poly_trim(out)


def poly_scale(p, s):
    if s == 0 or not p:
        return ZERO_POLY
    return poly_trim([c * s for c in p])


def poly_mul(p, q):
    if not p or not q:
        return ZERO_POLY
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a != 0:
            for j, b in enumerate(q):
                out[i + j] += a * b
    return poly_trim(out)


def poly_pow(p, e):
    res = ONE_POLY
    base = p
    exp = e
    while exp > 0:
        if exp & 1:
            res = poly_mul(res, base)
        base = poly_mul(base, base)
        exp >>= 1
    return res


def poly_deriv(p):
    if len(p) <= 1:
        return ZERO_POLY
    return poly_trim([i * p[i] for i in range(1, len(p))])


def poly_eval(p, x_val):
    acc = 0
    for i in range(len(p) - 1, -1, -1):
        acc = acc * x_val + p[i]
    return acc


def poly_eval_homogeneous(p, deg_n, num, den):
    # Evaluates den**deg_n * P(num over den) using exact integers only.
    total = 0
    for i, c in enumerate(p):
        if c != 0:
            total += c * (num ** i) * (den ** (deg_n - i))
    return total


def poly_shift(p, shift_c):
    # Computes p(x + shift_c) in Z[x] via Horner's rule.
    shifted_var = poly_trim([shift_c, 1])
    acc = ZERO_POLY
    for i in range(len(p) - 1, -1, -1):
        acc = poly_add(poly_mul(acc, shifted_var), poly_const(p[i]))
    return acc


def falling_factorial_poly(k):
    res = ONE_POLY
    for i in range(k):
        res = poly_mul(res, poly_trim([-i, 1]))
    return res


def poly_H(p, order_m):
    # H_U(x) = x * P'_U(x) - |U| * P_U(x)
    xp_prime = poly_mul(X_POLY, poly_deriv(p))
    return poly_sub(xp_prime, poly_scale(p, order_m))


# ============================================================================
# Digraph Helpers & Two Independent Acyclicity Oracles
# ============================================================================

def popcount(mask):
    cnt = 0
    m = mask
    while m:
        m &= m - 1
        cnt += 1
    return cnt


def vertices_in_mask(mask, n):
    return [u for u in range(n) if (mask >> u) & 1]


def check_loopless(adj):
    for u, mask in enumerate(adj):
        if (mask >> u) & 1:
            raise AssertionError(f"Self-loop detected at vertex {u}")


def is_subset_acyclic_kahn(adj, mask):
    # Iterative sink-stripping on induced subdigraph D[mask].
    rem = mask
    while rem:
        removed_any = False
        m = rem
        while m:
            lsb = m & -m
            u = lsb.bit_length() - 1
            if (adj[u] & rem) == 0:
                rem ^= lsb
                removed_any = True
            m ^= lsb
        if not removed_any:
            return False
    return True


def is_subset_acyclic_dfs(adj, mask, n):
    # Independent 3-state DFS cycle detector on D[mask].
    state = [0] * n
    for start in range(n):
        if not ((mask >> start) & 1) or state[start] != 0:
            continue
        stack = [(start, adj[start] & mask)]
        state[start] = 1
        while stack:
            u, nbrs = stack[-1]
            if nbrs == 0:
                state[u] = 2
                stack.pop()
            else:
                lsb = nbrs & -nbrs
                w = lsb.bit_length() - 1
                stack[-1] = (u, nbrs ^ lsb)
                if state[w] == 1:
                    return False
                if state[w] == 0:
                    state[w] = 1
                    stack.append((w, adj[w] & mask))
    return True


def precompute_acyclic_table(adj, n, cross_check_dfs=True):
    check_loopless(adj)
    total_masks = 1 << n
    table = [False] * total_masks
    for mask in range(total_masks):
        ans = is_subset_acyclic_kahn(adj, mask)
        if cross_check_dfs:
            ans_dfs = is_subset_acyclic_dfs(adj, mask, n)
            if ans != ans_dfs:
                raise AssertionError("Acyclicity oracle mismatch")
        table[mask] = ans
    return table


# ============================================================================
# Three Independent Clean-Room Computations of P_D(x)
# ============================================================================

def enumerate_allowed_partitions(target_mask, acyclic_table):
    # Yields tuples of nonempty bitmasks partitioning target_mask into allowed blocks.
    if target_mask == 0:
        yield ()
        return
    lsb = target_mask & -target_mask
    rest = target_mask ^ lsb
    # Iterate over all submasks of rest to form the block containing lsb.
    sub = rest
    while True:
        block = lsb | sub
        if acyclic_table[block]:
            rem = target_mask ^ block
            for tail in enumerate_allowed_partitions(rem, acyclic_table):
                yield (block,) + tail
        if sub == 0:
            break
        sub = (sub - 1) & rest


def dichrom_poly_partitions(mask, acyclic_table, ff_cache):
    # Method 1: Exact partition expansion sum_{pi allowed} (x)_{|pi|}.
    if mask == 0:
        return ONE_POLY
    counts_by_k = {}
    for pi in enumerate_allowed_partitions(mask, acyclic_table):
        k = len(pi)
        counts_by_k[k] = counts_by_k.get(k, 0) + 1
    res = ZERO_POLY
    for k, cnt in counts_by_k.items():
        res = poly_add(res, poly_scale(ff_cache[k], cnt))
    return res


def is_proper_coloring_direct_dfs(adj, n, colors, k):
    # Completely standalone coloring check using DFS per color class (no bitmask table).
    for col in range(k):
        in_class = [colors[u] == col for u in range(n)]
        state = [0] * n
        for start in range(n):
            if not in_class[start] or state[start] != 0:
                continue
            stack = [(start, 0)]
            state[start] = 1
            while stack:
                u, nxt = stack[-1]
                if nxt >= n:
                    state[u] = 2
                    stack.pop()
                else:
                    stack[-1] = (u, nxt + 1)
                    if in_class[nxt] and ((adj[u] >> nxt) & 1):
                        if state[nxt] == 1:
                            return False
                        if state[nxt] == 0:
                            state[nxt] = 1
                            stack.append((nxt, 0))
    return True


def count_proper_colorings_bruteforce(adj, n, k):
    if n == 0:
        return 1
    if k == 0:
        return 0
    total = k ** n
    valid = 0
    for code in range(total):
        tmp = code
        colors = [0] * n
        for u in range(n):
            colors[u] = tmp % k
            tmp //= k
        if is_proper_coloring_direct_dfs(adj, n, colors, k):
            valid += 1
    return valid


def newton_interpolate_from_values(vals, ff_cache):
    # Given [P(0), P(1), ..., P(n)], reconstructs exact Z[x] polynomial via
    # Newton forward differences and exact integer floor division //.
    deg_bound = len(vals) - 1
    diffs = list(vals)
    res = ZERO_POLY
    fact = 1
    for r in range(deg_bound + 1):
        if r > 0:
            fact *= r
        top = diffs[0]
        if top % fact != 0:
            raise AssertionError(f"Non-integer Newton coefficient at r={r}: {top} vs {fact}")
        coeff = top // fact
        if coeff != 0:
            res = poly_add(res, poly_scale(ff_cache[r], coeff))
        diffs = [diffs[i + 1] - diffs[i] for i in range(len(diffs) - 1)]
    return res


def dichrom_poly_bruteforce(adj, n, ff_cache, check_extra_point=True):
    # Method 2: Brute-force coloring enumeration at k=0..n (+ out-of-sample k=n+1).
    vals = [count_proper_colorings_bruteforce(adj, n, k) for k in range(0, n + 1)]
    poly = newton_interpolate_from_values(vals, ff_cache)
    if check_extra_point:
        extra_val = count_proper_colorings_bruteforce(adj, n, n + 1)
        if poly_eval(poly, n + 1) != extra_val:
            raise AssertionError("Out-of-sample brute-force evaluation mismatch at k=n+1")
    return poly


def minimal_cyclic_sets(n, acyclic_table):
    min_sets = []
    for mask in range(1, 1 << n):
        if not acyclic_table[mask]:
            is_min = True
            for prev in min_sets:
                if (prev & mask) == prev:
                    is_min = False
                    break
            if is_min:
                min_sets.append(mask)
    return min_sets


def dichrom_poly_min_cycles(n, acyclic_table):
    # Method 3: Inclusion-exclusion over minimal cyclic sets (Crew et al. Sec 3).
    c_sets = minimal_cyclic_sets(n, acyclic_table)
    m = len(c_sets)
    coeffs = [0] * (n + 1)
    for f_mask in range(1 << m):
        # Merge intersecting cyclic sets in F to count equivalence classes kappa(F).
        parent = list(range(n))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        bits = 0
        fm = f_mask
        while fm:
            lsb = fm & -fm
            idx = lsb.bit_length() - 1
            cm = c_sets[idx]
            verts = vertices_in_mask(cm, n)
            r0 = find(verts[0])
            for w in verts[1:]:
                rw = find(w)
                if rw != r0:
                    parent[rw] = r0
            bits += 1
            fm ^= lsb
        kappa = sum(1 for u in range(n) if find(u) == u)
        if bits & 1:
            coeffs[kappa] -= 1
        else:
            coeffs[kappa] += 1
    return poly_trim(coeffs)


# ============================================================================
# Exact Sturm Positivity Certificate on (0, +infinity) in Z[y]
# (Used only as exact fallback if shifted Taylor coefficients ever had a < 0 entry)
# ============================================================================

def gcd_int(a, b):
    a = abs(a)
    b = abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def poly_primitive(p):
    if not p:
        return ZERO_POLY
    g = 0
    for c in p:
        g = gcd_int(g, c)
    if g <= 1:
        return p
    return poly_trim([c // g for c in p])


def pseudo_rem_pos(a, b):
    # Exact pseudo-remainder of a mod b in Z[y] preserving signs by multiplying by lc(b)**2
    # or |lc(b)|**(deg(a)-deg(b)+1) > 0 so Sturm sign sequence is exact without division!
    if not b:
        raise ValueError("Zero divisor in pseudo_rem_pos")
    r = list(a)
    db = len(b) - 1
    lcb = b[db]
    scale_pos = abs(lcb)
    while len(r) - 1 >= db and any(c != 0 for c in r):
        dr = len(r) - 1
        lcr = r[dr]
        shift = dr - db
        # Multiply r by |lcb| > 0; subtract (sgn(lcb) * lcr) * y**shift * b
        # Since |lcb| * lcr - (sgn(lcb) * lcr) * lcb = 0, top term cancels cleanly!
        sgn_lcb = 1 if lcb > 0 else -1
        factor = sgn_lcb * lcr
        for i in range(len(r)):
            r[i] *= scale_pos
        for j in range(db + 1):
            r[j + shift] -= factor * b[j]
        while r and r[-1] == 0:
            r.pop()
    return poly_primitive(poly_trim(r))


def sign_at_zero_plus(p):
    for c in p:
        if c > 0:
            return 1
        if c < 0:
            return -1
    return 0


def sign_at_pos_inf(p):
    if not p:
        return 0
    return 1 if p[-1] > 0 else -1


def count_sign_variations(signs):
    nz = [s for s in signs if s != 0]
    return sum(1 for i in range(len(nz) - 1) if nz[i] != nz[i + 1])


def certify_strictly_positive_on_open_halfline(q_poly):
    # Certifies Q(0) >= 0 and Q(y) > 0 for all real y > 0 for nonzero Q in Z[y].
    if not q_poly:
        return False, "zero_poly"
    if poly_eval(q_poly, 0) < 0:
        return False, "negative_at_left_endpoint"
    if q_poly[-1] <= 0:
        return False, "nonpositive_leading_coeff"
    # Fast exact Taylor certificate: all coefficients >= 0 and non-constant (or q_0 > 0)
    if all(c >= 0 for c in q_poly) and any(c > 0 for c in q_poly):
        return True, "taylor_nonnegative"
    # General exact squarefree Sturm certificate on (0, +inf)
    # First divide out gcd(Q, Q') via exact polynomial pseudo-gcd if needed;
    # for squarefree or general Q, check Sturm chain on squarefree part:
    chain = [poly_primitive(q_poly), poly_primitive(poly_deriv(q_poly))]
    while chain[-1]:
        rem = pseudo_rem_pos(chain[-2], chain[-1])
        if not rem:
            break
        chain.append(poly_scale(rem, -1))
    # Check common squarefree gcd chain[-1] signs on the open half-line:
    # Note: multiplying every element of a Sturm chain by a polynomial G(y) that has no roots
    # on (0, +inf) preserves sign variations, and if G had a root we also detect roots of gcd!
    if len(chain[-1]) > 1:
        ok_gcd, _ = certify_strictly_positive_on_open_halfline(chain[-1])
        if not ok_gcd and not certify_strictly_positive_on_open_halfline(poly_scale(chain[-1], -1))[0]:
            return False, "sturm_gcd_root"
    v_zero = count_sign_variations([sign_at_zero_plus(p) for p in chain])
    v_inf = count_sign_variations([sign_at_pos_inf(p) for p in chain])
    if v_zero - v_inf != 0:
        return False, "positive_root_found"
    return True, "sturm_certified"


# ============================================================================
# Core Proof Audit Per Digraph: Identities (1), (2), (3) + Theorem Claims
# ============================================================================

def audit_digraph(
    adj,
    n,
    ff_cache,
    run_bruteforce=False,
    run_min_cycles=False,
    run_paper_corollaries=False,
    mutant_mode=None,
):
    acyclic_table = precompute_acyclic_table(adj, n, cross_check_dfs=True)
    full_mask = (1 << n) - 1

    # Precompute P_U and H_U for all induced subdigraphs U subseteq V.
    p_table = [ZERO_POLY] * (1 << n)
    h_table = [ZERO_POLY] * (1 << n)
    p_table[0] = ONE_POLY
    h_table[0] = ZERO_POLY
    for mask in range(1, 1 << n):
        m_sz = popcount(mask)
        p_u = dichrom_poly_partitions(mask, acyclic_table, ff_cache)
        p_table[mask] = p_u
        h_table[mask] = poly_H(p_u, m_sz)

    p_v = p_table[full_mask]
    h_v = h_table[full_mask]

    if run_bruteforce:
        p_bf = dichrom_poly_bruteforce(adj, n, ff_cache, check_extra_point=(n <= 4))
        if p_bf != p_v:
            raise AssertionError(f"Brute-force polynomial mismatch: {p_bf} != {p_v}")

    if run_min_cycles:
        p_mc = dichrom_poly_min_cycles(n, acyclic_table)
        if p_mc != p_v:
            raise AssertionError(f"Min-cycle polynomial mismatch: {p_mc} != {p_v}")

    if n < 2:
        # Base case checks for n=0, 1
        if n == 0 and (p_v != ONE_POLY or h_v != ZERO_POLY):
            raise AssertionError("Base case n=0 failed")
        if n == 1 and (p_v != X_POLY or h_v != ZERO_POLY):
            raise AssertionError("Base case n=1 failed")
        return {"taylor_cert": True, "has_cycle": False}

    x_minus_1 = (-1, 1)
    x_sq = (0, 0, 1)

    # Check Identities (1), (2), (3) for EVERY marked vertex v in V.
    for v in range(n):
        v_bit = 1 << v
        rest_v = full_mask ^ v_bit

        # Collect all allowed S containing v
        allowed_S = []
        sub = rest_v
        while True:
            s_mask = v_bit | sub
            if acyclic_table[s_mask]:
                allowed_S.append(s_mask)
            if sub == 0:
                break
            sub = (sub - 1) & rest_v

        # Identity (1): P_V(x) = x * sum_{S ni v allowed} P_{V \ S}(x - 1)
        sum_p_r_shifted = ZERO_POLY
        # Intermediate H_V line 17: H_V(x) = x * sum_S [x P'_R(x-1) - (n-1) P_R(x-1)]
        sum_line17 = ZERO_POLY
        # Identity (2) terms:
        sum_h_r_shifted = ZERO_POLY
        term2_second_inner = ZERO_POLY

        for s_mask in allowed_S:
            r_mask = full_mask ^ s_mask
            s_sz = popcount(s_mask)
            p_r = p_table[r_mask]
            h_r = h_table[r_mask]

            p_r_sh = poly_shift(p_r, -1)
            p_r_deriv_sh = poly_shift(poly_deriv(p_r), -1)
            h_r_sh = poly_shift(h_r, -1)

            sum_p_r_shifted = poly_add(sum_p_r_shifted, p_r_sh)

            line17_term = poly_sub(
                poly_mul(X_POLY, p_r_deriv_sh),
                poly_scale(p_r_sh, n - 1),
            )
            sum_line17 = poly_add(sum_line17, line17_term)

            sum_h_r_shifted = poly_add(sum_h_r_shifted, h_r_sh)

            # Weight: (n - 1) - x * (|S| - 1)
            if mutant_mode == "MUTANT_3_WRONG_WEIGHT_COEFF_ID2":
                weight_poly = poly_trim([n - 1, -s_sz])
            else:
                weight_poly = poly_trim([n - 1, -(s_sz - 1)])
            term2_second_inner = poly_add(term2_second_inner, poly_mul(weight_poly, p_r_sh))

        rhs1 = poly_mul(X_POLY, sum_p_r_shifted)
        if p_v != rhs1:
            raise AssertionError(f"Identity (1) failed at v={v}: {p_v} != {rhs1}")

        rhs_line17 = poly_mul(X_POLY, sum_line17)
        if h_v != rhs_line17:
            raise AssertionError(f"Line 17 H_V identity failed at v={v}: {h_v} != {rhs_line17}")

        lhs2 = poly_mul(x_minus_1, h_v)
        term2_first = poly_mul(x_sq, sum_h_r_shifted)
        term2_second = poly_mul(X_POLY, term2_second_inner)
        rhs2 = poly_add(term2_first, term2_second)
        if lhs2 != rhs2:
            raise AssertionError(f"Identity (2) failed at v={v}: {lhs2} != {rhs2}")

        # Identity (3): sum over allowed partitions pi of V \ {v}
        term3_second = ZERO_POLY
        for pi in enumerate_allowed_partitions(rest_v, acyclic_table):
            k = len(pi)
            b_sum_poly = ZERO_POLY
            for blk in pi:
                if not acyclic_table[blk | v_bit]:
                    blk_sz = popcount(blk)
                    # x * |B| - (n - 1)
                    b_sum_poly = poly_add(b_sum_poly, poly_trim([-(n - 1), blk_sz]))
            if b_sum_poly:
                if mutant_mode == "MUTANT_2_DROP_FALLING_FACTORIAL_ID3":
                    factor_pi = ONE_POLY
                else:
                    factor_pi = ff_cache[k]
                term3_second = poly_add(term3_second, poly_mul(factor_pi, b_sum_poly))

        if mutant_mode == "MUTANT_1_SIGN_FLIP_ID3":
            rhs3 = poly_sub(term2_first, term3_second)
        else:
            if term2_second != term3_second:
                raise AssertionError(
                    f"Double-counting sub-identity failed at v={v}: {term2_second} != {term3_second}"
                )
            rhs3 = poly_add(term2_first, term3_second)

        if lhs2 != rhs3:
            raise AssertionError(f"Identity (3) failed at v={v}: {lhs2} != {rhs3}")

    # Verify Theorem conclusions (Conjecture 1, Conjecture 2, Strictness, DAGs)
    has_cycle = not acyclic_table[full_mask]
    p_at_n = poly_eval(p_v, n)
    p_at_n_minus_1 = poly_eval(p_v, n - 1)
    lhs_shameful = ((n - 1) ** n) * p_at_n
    rhs_shameful = (n ** n) * p_at_n_minus_1

    # Crew et al. Theorem 7 baseline check: 252 * P_D(n) >= 685 * P_D(n-1)
    if 252 * p_at_n < 685 * p_at_n_minus_1:
        raise AssertionError("Crew et al. Theorem 7 baseline failed")

    if mutant_mode == "MUTANT_4_LOWER_THRESHOLD_N_MINUS_2":
        if poly_eval(h_v, n - 2) < 0:
            raise AssertionError(f"Threshold n-2 failed: H_D({n-2}) < 0")

    cert_kind = "dag_zero"
    if not has_cycle:
        # DAG case: P_D(x) == x**n, H_D(x) == 0, Shameful holds with equality
        expected_dag = tuple([0] * n + [1])
        if p_v != expected_dag:
            raise AssertionError(f"DAG polynomial != x**n: {p_v}")
        if h_v != ZERO_POLY:
            raise AssertionError(f"DAG H_D != 0: {h_v}")
        if lhs_shameful != rhs_shameful:
            raise AssertionError("DAG Shameful equality failed")
    else:
        # Cyclic case: verify strictness witness from PROOF.md line 51
        min_cycs = minimal_cyclic_sets(n, acyclic_table)
        if not min_cycs:
            raise AssertionError("Cyclic digraph had no minimal cyclic set")
        c_mask = min_cycs[0]
        c_sz = popcount(c_mask)
        if c_sz < 2:
            raise AssertionError("Minimal cyclic set size < 2 in loopless digraph")
        v_wit = (c_mask & -c_mask).bit_length() - 1
        b0_mask = c_mask ^ (1 << v_wit)
        if b0_mask == 0 or not acyclic_table[b0_mask]:
            raise AssertionError("Witness block C \\ {v} not nonempty allowed")
        if acyclic_table[b0_mask | (1 << v_wit)]:
            raise AssertionError("Witness block C \\ {v} union {v} unexpectedly allowed")

        # Strict Conjecture 1 inequality
        if not (lhs_shameful > rhs_shameful):
            raise AssertionError(f"Strict Shameful inequality failed: {lhs_shameful} <= {rhs_shameful}")

        # Exact real-line positivity certificate for H_D((n-1) + y) on y > 0 and >= 0 at y = 0
        q_shifted = poly_shift(h_v, n - 1)
        ok_pos, cert_kind = certify_strictly_positive_on_open_halfline(q_shifted)
        if not ok_pos:
            raise AssertionError(f"Positivity certificate failed on [n-1, inf): {cert_kind}, Q={q_shifted}")

        # Exact rational-grid strict monotonicity check on F_D(x) = P_D(x) over x**n
        # Sample x_t = (4*(n-1) + t) over 4 for t = 0..16
        den = 4
        prev_num = 4 * (n - 1)
        prev_hom = poly_eval_homogeneous(p_v, n, prev_num, den)
        for t in range(1, 17):
            cur_num = 4 * (n - 1) + t
            cur_hom = poly_eval_homogeneous(p_v, n, cur_num, den)
            # Compare cur_hom over cur_num**n > prev_hom over prev_num**n (den**n cancels!)
            if not (cur_hom * (prev_num ** n) > prev_hom * (cur_num ** n)):
                raise AssertionError("Strict rational-grid monotonicity failed")
            prev_num = cur_num
            prev_hom = cur_hom

    if run_paper_corollaries:
        # Check Crew et al. Sec 3 Corollary 4 (c_n = 1, c_{n-1} = -q, c_{n-2} = C(q,2) - t_S - t_D)
        coeffs_full = list(p_v) + [0] * (n + 1 - len(p_v))
        if coeffs_full[n] != 1 or coeffs_full[0] != 0:
            raise AssertionError("Leading or constant coefficient check failed")
        digons = []
        for u in range(n):
            for w in range(u + 1, n):
                if ((adj[u] >> w) & 1) and ((adj[w] >> u) & 1):
                    digons.append((u, w))
        q_digons = len(digons)
        if coeffs_full[n - 1] != -q_digons:
            raise AssertionError(f"Second coefficient mismatch: {coeffs_full[n-1]} != {-q_digons}")
        if n >= 2:
            t_s = 0
            t_d = 0
            for a in range(n):
                for b in range(a + 1, n):
                    for c in range(b + 1, n):
                        ab = ((adj[a] >> b) & 1) and ((adj[b] >> a) & 1)
                        bc = ((adj[b] >> c) & 1) and ((adj[c] >> b) & 1)
                        ca = ((adj[c] >> a) & 1) and ((adj[a] >> c) & 1)
                        if ab and bc and ca:
                            t_s += 1
                        if not (ab or bc or ca):
                            cyc1 = ((adj[a] >> b) & 1) and ((adj[b] >> c) & 1) and ((adj[c] >> a) & 1)
                            cyc2 = ((adj[a] >> c) & 1) and ((adj[c] >> b) & 1) and ((adj[b] >> a) & 1)
                            if cyc1:
                                t_d += 1
                            if cyc2:
                                t_d += 1
            expected_cn2 = (q_digons * (q_digons - 1)) // 2 - t_s - t_d
            if coeffs_full[n - 2] != expected_cn2:
                raise AssertionError(
                    f"Third coefficient mismatch: {coeffs_full[n-2]} != {expected_cn2}"
                )

        # Check Crew et al. Sec 4 Proposition 1 (di-simplicial linear factor)
        for v in range(n):
            in_nbrs = [u for u in range(n) if u != v and ((adj[u] >> v) & 1)]
            out_nbrs = [w for w in range(n) if w != v and ((adj[v] >> w) & 1)]
            is_disimp = True
            for x_in in in_nbrs:
                for y_out in out_nbrs:
                    if x_in != y_out and not ((adj[x_in] >> y_out) & 1):
                        is_disimp = False
                        break
                if not is_disimp:
                    break
            if is_disimp:
                q_both = sum(1 for u in in_nbrs if ((adj[v] >> u) & 1))
                p_minus_v = p_table[full_mask ^ (1 << v)]
                expected_p = poly_mul(poly_trim([-q_both, 1]), p_minus_v)
                if p_v != expected_p:
                    raise AssertionError(f"Chordal di-simplicial identity failed at v={v}")

    return {"cert_kind": cert_kind, "has_cycle": has_cycle}


# ============================================================================
# Digraph Generators (Exhaustive n=2..4, Named Families & Diverse Sample n=5..6)
# ============================================================================

def digraph_from_arc_code(n, code):
    # Maps integer in [0, 2**(n*(n-1))) to loopless labeled digraph on n vertices.
    adj = [0] * n
    bit = 0
    for u in range(n):
        row = 0
        for w in range(n):
            if u != w:
                if (code >> bit) & 1:
                    row |= 1 << w
                bit += 1
        adj[u] = row
    return tuple(adj)


def make_empty_digraph(n):
    return tuple([0] * n)


def make_directed_path(n):
    adj = [0] * n
    for u in range(n - 1):
        adj[u] |= 1 << (u + 1)
    return tuple(adj)


def make_transitive_tournament(n):
    adj = [0] * n
    for u in range(n):
        for w in range(u + 1, n):
            adj[u] |= 1 << w
    return tuple(adj)


def make_directed_cycle(n):
    adj = [0] * n
    for u in range(n):
        adj[u] |= 1 << ((u + 1) % n)
    return tuple(adj)


def make_bidirected_clique(n):
    full = (1 << n) - 1
    return tuple([full ^ (1 << u) for u in range(n)])


def make_bidirected_cycle(n):
    adj = [0] * n
    for u in range(n):
        nxt = (u + 1) % n
        adj[u] |= 1 << nxt
        adj[nxt] |= 1 << u
    return tuple(adj)


def make_bidirected_star(n):
    adj = [0] * n
    for u in range(1, n):
        adj[0] |= 1 << u
        adj[u] |= 1 << 0
    return tuple(adj)


def disjoint_union(adj1, adj2):
    n1 = len(adj1)
    n2 = len(adj2)
    out = list(adj1)
    for m in adj2:
        out.append(m << n1)
    return tuple(out)


def build_named_digraphs_n5():
    named = []
    named.append(("empty_5", make_empty_digraph(5)))
    named.append(("dir_path_5", make_directed_path(5)))
    named.append(("trans_tourn_5", make_transitive_tournament(5)))
    named.append(("dir_cycle_5", make_directed_cycle(5)))
    named.append(("bi_clique_5", make_bidirected_clique(5)))
    named.append(("bi_cycle_5", make_bidirected_cycle(5)))
    named.append(("bi_star_5", make_bidirected_star(5)))
    # Regular tournament on 5 vertices: u -> (u+1)%5, (u+2)%5
    reg5 = [0] * 5
    for u in range(5):
        reg5[u] |= (1 << ((u + 1) % 5)) | (1 << ((u + 2) % 5))
    named.append(("regular_tourn_5", tuple(reg5)))
    # Chorded directed 5-cycle
    ch5 = list(make_directed_cycle(5))
    ch5[0] |= 1 << 2
    named.append(("chorded_cycle_5", tuple(ch5)))
    # Disconnected combinations
    c3 = make_directed_cycle(3)
    k2 = make_bidirected_clique(2)
    e2 = make_empty_digraph(2)
    k3 = make_bidirected_clique(3)
    c4 = make_directed_cycle(4)
    e1 = make_empty_digraph(1)
    named.append(("C3_disjoint_biK2", disjoint_union(c3, k2)))
    named.append(("C3_disjoint_empty2", disjoint_union(c3, e2)))
    named.append(("biK3_disjoint_biK2", disjoint_union(k3, k2)))
    named.append(("biK3_disjoint_empty2", disjoint_union(k3, e2)))
    named.append(("C4_disjoint_singleton", disjoint_union(c4, e1)))
    named.append(("biK2_biK2_singleton", disjoint_union(disjoint_union(k2, k2), e1)))
    # Crew et al. Section 5 bipartite triangle construction D_{K_{2,2}} on 5 vertices:
    # w=0, A={1,2}, B={3,4}; edges ab give w->a->b->w
    dk22 = [0] * 5
    for a in (1, 2):
        for b in (3, 4):
            dk22[0] |= 1 << a
            dk22[a] |= 1 << b
            dk22[b] |= 1 << 0
    named.append(("sec5_D_K22", tuple(dk22)))
    return named


def build_named_digraphs_n6():
    named = []
    named.append(("empty_6", make_empty_digraph(6)))
    named.append(("dir_path_6", make_directed_path(6)))
    named.append(("trans_tourn_6", make_transitive_tournament(6)))
    named.append(("dir_cycle_6", make_directed_cycle(6)))
    named.append(("bi_clique_6", make_bidirected_clique(6)))
    named.append(("bi_cycle_6", make_bidirected_cycle(6)))
    named.append(("bi_star_6", make_bidirected_star(6)))
    # Bidirected K_{3,3}
    bik33 = [0] * 6
    for a in (0, 1, 2):
        for b in (3, 4, 5):
            bik33[a] |= 1 << b
            bik33[b] |= 1 << a
    named.append(("bi_K33", tuple(bik33)))
    # Near-regular tournament on 6 vertices
    t6 = [0] * 6
    for u in range(6):
        for step in (1, 2):
            t6[u] |= 1 << ((u + step) % 6)
    for u in range(3):
        t6[u] |= 1 << (u + 3)
    named.append(("near_reg_tourn_6", tuple(t6)))
    # Disconnected combinations
    c3 = make_directed_cycle(3)
    k3 = make_bidirected_clique(3)
    k2 = make_bidirected_clique(2)
    c4 = make_directed_cycle(4)
    e3 = make_empty_digraph(3)
    named.append(("C3_disjoint_C3", disjoint_union(c3, c3)))
    named.append(("biK3_disjoint_C3", disjoint_union(k3, c3)))
    named.append(("biK3_disjoint_empty3", disjoint_union(k3, e3)))
    named.append(("three_disjoint_biK2", disjoint_union(disjoint_union(k2, k2), k2)))
    named.append(("C4_disjoint_biK2", disjoint_union(c4, k2)))
    # Directed wheel on 6 vertices (hub 0 -> rim 1..5 -> 0 alternating)
    wh6 = [0] * 6
    for u in range(1, 6):
        nxt = 1 + (u % 5)
        wh6[u] |= 1 << nxt
        if u & 1:
            wh6[0] |= 1 << u
        else:
            wh6[u] |= 1 << 0
    named.append(("dir_wheel_6", tuple(wh6)))
    # Crew et al. Section 5 D_{P_5} (bipartite path 1-3-2-4-5 plus w=0 -> n=6)
    dp5 = [0] * 6
    # A={1,2,5}, B={3,4}, edges (1,3),(2,3),(2,4),(5,4)
    for a, b in ((1, 3), (2, 3), (2, 4), (5, 4)):
        dp5[0] |= 1 << a
        dp5[a] |= 1 << b
        dp5[b] |= 1 << 0
    named.append(("sec5_D_P5", tuple(dp5)))
    return named


def generate_diverse_sample(n, count, seed_init):
    # Deterministic pure-integer LCG generating oriented (digon-free), tournament,
    # sparse, medium, dense, and disconnected digraphs without duplicates.
    state = seed_init
    seen = set()
    sample = []
    modes = ("sparse", "medium", "dense", "oriented", "tournament", "disconnected")
    idx = 0
    while len(sample) < count:
        mode = modes[idx % len(modes)]
        idx += 1
        adj = [0] * n
        if mode in ("sparse", "medium", "dense"):
            thresh = 20 if mode == "sparse" else (50 if mode == "medium" else 80)
            for u in range(n):
                for w in range(n):
                    if u != w:
                        state = (state * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
                        if ((state >> 32) % 100) < thresh:
                            adj[u] |= 1 << w
        elif mode == "oriented":
            for u in range(n):
                for w in range(u + 1, n):
                    state = (state * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
                    r = (state >> 32) % 3
                    if r == 1:
                        adj[u] |= 1 << w
                    elif r == 2:
                        adj[w] |= 1 << u
        elif mode == "tournament":
            for u in range(n):
                for w in range(u + 1, n):
                    state = (state * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
                    if (state >> 32) & 1:
                        adj[u] |= 1 << w
                    else:
                        adj[w] |= 1 << u
        else:
            # Disconnected split into [0..split-1] and [split..n-1]
            split = n // 2
            for u in range(n):
                for w in range(n):
                    if u != w and ((u < split) == (w < split)):
                        state = (state * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
                        if ((state >> 32) % 100) < 55:
                            adj[u] |= 1 << w
        tup = tuple(adj)
        if tup not in seen:
            seen.add(tup)
            sample.append(tup)
    return sample


# ============================================================================
# Positive Controls & Deliberate Mutation Controls
# ============================================================================

def run_positive_controls(ff_cache):
    # 1. Base cases n=0 and n=1
    audit_digraph((), 0, ff_cache, run_bruteforce=True)
    audit_digraph((0,), 1, ff_cache, run_bruteforce=True)

    # 2. Exact closed-form formulas for C_3, C_4, bi-K_n, DAGs
    c3 = make_directed_cycle(3)
    ac3 = precompute_acyclic_table(c3, 3)
    p_c3 = dichrom_poly_partitions(7, ac3, ff_cache)
    if p_c3 != (0, -1, 0, 1):
        raise AssertionError(f"Control P_(C_3) mismatch: {p_c3}")
    if poly_H(p_c3, 3) != (0, 2):
        raise AssertionError("Control H_(C_3) != 2x")

    c4 = make_directed_cycle(4)
    ac4 = precompute_acyclic_table(c4, 4)
    p_c4 = dichrom_poly_partitions(15, ac4, ff_cache)
    if p_c4 != (0, -1, 0, 0, 1):
        raise AssertionError(f"Control P_(C_4) mismatch: {p_c4}")
    if poly_H(p_c4, 4) != (0, 3):
        raise AssertionError("Control H_(C_4) != 3x")

    for n in range(1, 7):
        bik = make_bidirected_clique(n)
        ack = precompute_acyclic_table(bik, n)
        p_bik = dichrom_poly_partitions((1 << n) - 1, ack, ff_cache)
        if p_bik != ff_cache[n]:
            raise AssertionError(f"Control P_(biK_{n}) != (x)_{n}")

        tt = make_transitive_tournament(n)
        act = precompute_acyclic_table(tt, n)
        p_tt = dichrom_poly_partitions((1 << n) - 1, act, ff_cache)
        expected_xn = tuple([0] * n + [1])
        if p_tt != expected_xn:
            raise AssertionError(f"Control P_(TT_{n}) != x**{n}")


def run_mutant_controls(ff_cache):
    k2 = make_bidirected_clique(2)
    c3 = make_directed_cycle(3)
    k3 = make_bidirected_clique(3)
    k4 = make_bidirected_clique(4)

    mutants = [
        ("MUTANT_1_SIGN_FLIP_ID3", [(k2, 2), (c3, 3)]),
        ("MUTANT_2_DROP_FALLING_FACTORIAL_ID3", [(k2, 2), (c3, 3)]),
        ("MUTANT_3_WRONG_WEIGHT_COEFF_ID2", [(make_empty_digraph(2), 2), (k2, 2)]),
        ("MUTANT_4_LOWER_THRESHOLD_N_MINUS_2", [(k3, 3), (k4, 4)]),
    ]

    caught_summary = []
    for m_name, targets in mutants:
        for adj, n in targets:
            caught = False
            reason = ""
            try:
                audit_digraph(adj, n, ff_cache, mutant_mode=m_name)
            except AssertionError as exc:
                caught = True
                reason = str(exc)
            if not caught:
                raise RuntimeError(f"CRITICAL: Mutant {m_name} was NOT caught on n={n}!")
            caught_summary.append((m_name, n, reason))
    return caught_summary


def main():
    max_n = 6
    ff_cache = [falling_factorial_poly(k) for k in range(max_n + 2)]

    print("=== Clean-Room Exact-Integer Referee Verification (arXiv:2611.13273v1) ===")

    # Step 1: Positive controls + base cases
    run_positive_controls(ff_cache)
    print("[PASS] Positive controls: n=0, n=1, C_3, C_4, bi-K_1..6, TT_1..6 exact polynomials & H_D")

    # Step 2: Deliberate mutation controls (must fail!)
    caught = run_mutant_controls(ff_cache)
    print(f"[PASS] Deliberate mutation controls: all {len(caught)} mutant checks detected and rejected:")
    for m_name, n_val, reason in caught:
        print(f"       - {m_name} on n={n_val}: caught ({reason})")

    # Step 3: Exhaustive verification on ALL labeled loopless digraphs for n = 2, 3, 4
    cert_counts = {"dag_zero": 0, "taylor_nonnegative": 0, "sturm_certified": 0}
    for n in (2, 3, 4):
        num_arcs = n * (n - 1)
        total_digraphs = 1 << num_arcs
        cyclic_cnt = 0
        dag_cnt = 0
        for code in range(total_digraphs):
            adj = digraph_from_arc_code(n, code)
            info = audit_digraph(
                adj,
                n,
                ff_cache,
                run_bruteforce=True,
                run_min_cycles=True,
                run_paper_corollaries=True,
            )
            cert_counts[info["cert_kind"]] += 1
            if info["has_cycle"]:
                cyclic_cnt += 1
            else:
                dag_cnt += 1
        pairs = total_digraphs * n
        print(
            f"[PASS] Exhaustive n={n}: {total_digraphs} digraphs ({pairs} (D,v) pairs; "
            f"{cyclic_cnt} cyclic, {dag_cnt} DAGs) verified (Id 1-3 + brute-force + min-cycle + Sec 3&4&8)"
        )

    # Step 4: Named structured families + diverse deterministic samples on n = 5 and n = 6
    named5 = build_named_digraphs_n5()
    for label, adj in named5:
        info = audit_digraph(
            adj,
            5,
            ff_cache,
            run_bruteforce=True,
            run_min_cycles=True,
            run_paper_corollaries=True,
        )
        cert_counts[info["cert_kind"]] += 1
    print(f"[PASS] Named n=5 families: {len(named5)} digraphs ({len(named5)*5} (D,v) pairs, with brute-force) verified")

    sample5 = generate_diverse_sample(5, 200, 2611132735)
    for adj in sample5:
        info = audit_digraph(
            adj,
            5,
            ff_cache,
            run_bruteforce=False,
            run_min_cycles=False,
            run_paper_corollaries=True,
        )
        cert_counts[info["cert_kind"]] += 1
    print(f"[PASS] Diverse n=5 sample: {len(sample5)} digraphs ({len(sample5)*5} (D,v) pairs) verified")

    named6 = build_named_digraphs_n6()
    for label, adj in named6:
        info = audit_digraph(
            adj,
            6,
            ff_cache,
            run_bruteforce=False,
            run_min_cycles=False,
            run_paper_corollaries=True,
        )
        cert_counts[info["cert_kind"]] += 1
    print(f"[PASS] Named n=6 families: {len(named6)} digraphs ({len(named6)*6} (D,v) pairs) verified")

    sample6 = generate_diverse_sample(6, 80, 2611132736)
    for adj in sample6:
        info = audit_digraph(
            adj,
            6,
            ff_cache,
            run_bruteforce=False,
            run_min_cycles=False,
            run_paper_corollaries=True,
        )
        cert_counts[info["cert_kind"]] += 1
    print(f"[PASS] Diverse n=6 sample: {len(sample6)} digraphs ({len(sample6)*6} (D,v) pairs) verified")

    total_digraphs_all = 2 + 4 + 64 + 4096 + len(named5) + len(sample5) + len(named6) + len(sample6)
    total_pairs_all = (
        1
        + 4 * 2
        + 64 * 3
        + 4096 * 4
        + (len(named5) + len(sample5)) * 5
        + (len(named6) + len(sample6)) * 6
    )
    print(
        f"[SUMMARY] Total verified: {total_digraphs_all} digraphs, {total_pairs_all} (D,v) pairs; "
        f"positivity certificates={cert_counts}"
    )
    print("ALL CLEAN-ROOM EXACT-INTEGER REFEREE CHECKS PASSED.")


if __name__ == "__main__":
    main()
