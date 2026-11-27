# referee_verify.py -- clean-room referee checks for PROOF.md (Selvaraja arXiv:2611.20820v1,
# conj:skew and conj:theta). Pure Python, exact integer arithmetic only.
# Rules honoured: no math import, no future import, no floats, no true-division operator.
# Run: timeout 120 python3 -I referee_verify.py
import sys
import itertools

FAIL = []
def check(cond, label):
    print(("PASS  " if cond else "FAIL  ") + label)
    if not cond:
        FAIL.append(label)

def popcount(x):
    return bin(x).count("1")

def dist(a, b):
    return popcount(a ^ b)

# ---------------------------------------------------------------------------
# Part 0: self-audit of this file for forbidden constructs
# ---------------------------------------------------------------------------
def self_audit():
    src = open(__file__).read()
    slash = chr(47)
    bad = []
    for ln, line in enumerate(src.split("\n"), 1):
        code = line.split("#")[0]
        if slash in code.replace(slash + slash, ""):
            bad.append(("single-slash", ln))
        if ("import " + "math") in code or ("__fut" + "ure__") in code or ("flo" + "at(") in code:
            bad.append(("forbidden", ln))
        # float literals like 1.5 or 1e3
        tok = code.replace("e1", "").replace("e2", "")
        for i in range(1, len(tok) - 1):
            if tok[i] == "." and tok[i - 1].isdigit() and tok[i + 1].isdigit():
                bad.append(("float-literal", ln))
    return bad

# ---------------------------------------------------------------------------
# Part 1: exact symbolic algebra A = K[e_1..e_s]/(e_j^2), K = F_p(t_hj)
# element: dict {emask: poly}; poly: dict {monomial(tuple exps): coeff mod p}
# ---------------------------------------------------------------------------
def poly_add(P, Q, p):
    R = dict(P)
    for m, c in Q.items():
        v = (R.get(m, 0) + c) % p
        if v:
            R[m] = v
        else:
            R.pop(m, None)
    return R

def poly_mul(P, Q, p):
    R = {}
    for m1, c1 in P.items():
        for m2, c2 in Q.items():
            m = tuple(a + b for a, b in zip(m1, m2))
            v = (R.get(m, 0) + c1 * c2) % p
            if v:
                R[m] = v
            else:
                R.pop(m, None)
    return R

def alg_mul(X, Y, p):
    R = {}
    for e1, P in X.items():
        for e2, Q in Y.items():
            if e1 & e2:
                continue  # e_j^2 = 0
            pr = poly_mul(P, Q, p)
            if not pr:
                continue
            S = poly_add(R.get(e1 | e2, {}), pr, p)
            if S:
                R[e1 | e2] = S
            else:
                R.pop(e1 | e2, None)
    return R

def alg_eq(X, Y):
    return X == Y

def symbolic_setup(n, s):
    nv = n * s
    def var(h, j):
        m = [0] * nv
        m[h * s + j] = 1
        return tuple(m)
    one_m = tuple([0] * nv)
    ONE = {0: {one_m: 1}}
    oneplus_u = []
    for h in range(n):
        el = {0: {one_m: 1}}
        for j in range(s):
            el[1 << j] = {var(h, j): 1}
        oneplus_u.append(el)
    return ONE, oneplus_u, nv

def P_of(x, n, ONE, opu, p):
    R = ONE
    for h in range(n):
        if (x >> h) & 1:
            R = alg_mul(R, opu[h], p)
    return R

def part1_symbolic():
    print("== Part 1a: exact symbolic F_2[t_hj] algebra ==")
    for (r, n) in ((1, 3), (2, 4)):
        s = r + 1
        ONE, opu, nv = symbolic_setup(n, s)
        top = (1 << s) - 1
        sq_ok = all(alg_mul(opu[h], opu[h], 2) == ONE for h in range(n))
        u_sq_ok = True
        for h in range(n):
            u = {k: v for k, v in opu[h].items() if k != 0}
            if alg_mul(u, u, 2) != {}:
                u_sq_ok = False
        check(u_sq_ok, "r=%d n=%d: u_h^2 = 0 for all h (char 2)" % (r, n))
        check(sq_ok, "r=%d n=%d: (1+u_h)^2 = 1 for all h (char 2)" % (r, n))
        P = [P_of(x, n, ONE, opu, 2) for x in range(1 << n)]
        prod_ok = True
        thr_ok = True
        unique_ok = True
        cnt = 0
        for x in range(1 << n):
            for y in range(1 << n):
                cnt += 1
                PP = alg_mul(P[x], P[y], 2)
                D = x ^ y
                if PP != P[D]:
                    prod_ok = False
                Lv = PP.get(top, {})
                if (len(Lv) > 0) != (popcount(D) >= s):
                    thr_ok = False
                if popcount(D) >= s:
                    hs = [h for h in range(n) if (D >> h) & 1][:s]
                    m = [0] * nv
                    for j, h in enumerate(hs):
                        m[h * s + j] = 1
                    if Lv.get(tuple(m), 0) != 1:
                        unique_ok = False
        check(prod_ok, "r=%d n=%d: P_x P_y = prod_{h in D}(1+u_h) for all %d pairs" % (r, n, cnt))
        check(thr_ok, "r=%d n=%d: L(P_x P_y) != 0 iff |D| >= s, all %d pairs (incl. |D| > s)" % (r, n, cnt))
        check(unique_ok, "r=%d n=%d: monomial t_{h1,1}..t_{hs,s} has coefficient 1 in L(P_xP_y) whenever |D|>=s" % (r, n))
    # mutation control: characteristic 3
    ONE, opu, nv = symbolic_setup(3, 2)
    c3 = all(alg_mul(opu[h], opu[h], 3) == ONE for h in range(3))
    check(not c3, "MUTANT char 3: (1+u_h)^2 = 1 FAILS as expected")
    u = {k: v for k, v in opu[0].items() if k != 0}
    check(alg_mul(u, u, 3) != {}, "MUTANT char 3: u_h^2 != 0 as expected")

# ---------------------------------------------------------------------------
# Part 1b: specialization over GF(2^16), modulus x^16+x^5+x^3+x^2+1
# ---------------------------------------------------------------------------
MOD = (1 << 16) | (1 << 5) | (1 << 3) | (1 << 2) | 1

def pmulmod(a, b, mod, deg):
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if (a >> deg) & 1:
            a ^= mod
    return r

def pmod(a, m):
    dm = m.bit_length() - 1
    while a and a.bit_length() - 1 >= dm:
        a ^= m << (a.bit_length() - 1 - dm)
    return a

def pgcd(a, b):
    while b:
        a, b = b, pmod(a, b)
    return a

def irreducible16():
    # Rabin: x^(2^16) = x mod f and gcd(x^(2^8) - x, f) = 1 (only prime divisor of 16 is 2)
    x = 2
    t = x
    for i in range(8):
        t = pmulmod(t, t, MOD, 16)
    g = pgcd(MOD, t ^ x)
    for i in range(8):
        t = pmulmod(t, t, MOD, 16)
    return t == x and g == 1

def gmul(a, b):
    return pmulmod(a, b, MOD, 16)

def ginv(a):
    # a^(2^16 - 2)
    r = 1
    e = (1 << 16) - 2
    while e:
        if e & 1:
            r = gmul(r, a)
        a = gmul(a, a)
        e >>= 1
    return r

def num_alg_mul(X, Y, s):
    N = 1 << s
    R = [0] * N
    for e1 in range(N):
        a = X[e1]
        if not a:
            continue
        for e2 in range(N):
            if e1 & e2 or not Y[e2]:
                continue
            R[e1 | e2] ^= gmul(a, Y[e2])
    return R

def rank_gf(M):
    M = [row[:] for row in M]
    rk = 0
    rows = len(M)
    cols = len(M[0]) if rows else 0
    for c in range(cols):
        piv = None
        for i in range(rk, rows):
            if M[i][c]:
                piv = i
                break
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]
        iv = ginv(M[rk][c])
        M[rk] = [gmul(iv, v) for v in M[rk]]
        for i in range(rows):
            if i != rk and M[i][c]:
                f = M[i][c]
                M[i] = [a ^ gmul(f, b) for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk

def subcube_system(n, r):
    # Selvaraja / PROOF sec.1: v=(x,0,0..), w=(xbar,1,0..), x in {0,1}^r; bit h = coordinate h
    vs, ws = [], []
    for x in range(1 << r):
        vs.append(x)
        ws.append(((~x) & ((1 << r) - 1)) | (1 << r))
    return vs, ws

def is_close_skew(vs, ws, r):
    k = len(vs)
    for i in range(k):
        for j in range(k):
            if dist(vs[i], vs[j]) > r:
                return False
        if dist(vs[i], ws[i]) <= r:
            return False
        for j in range(i):
            if dist(ws[i], vs[j]) > r:
                return False
    return True

def is_skew(pairs, r):
    m = len(pairs)
    for i in range(m):
        if dist(pairs[i][0], pairs[i][1]) <= r:
            return False
        for j in range(i + 1, m):
            if dist(pairs[i][0], pairs[j][1]) > r:
                return False
    return True

def reversed_doubling(vs, ws):
    return [(v, w) for v, w in zip(vs, ws)] + [(w, v) for v, w in reversed(list(zip(vs, ws)))]

def forward_doubling(vs, ws):
    return [(v, w) for v, w in zip(vs, ws)] + [(w, v) for v, w in zip(vs, ws)]

def part1_finite_field():
    print("== Part 1b: GF(2^16) specialization ==")
    check(irreducible16(), "x^16+x^5+x^3+x^2+1 is irreducible over F_2 (Rabin test)")
    seed = 12345
    for r in (1, 2, 3, 4):
        s = r + 1
        N = 1 << s
        for n in (r + 1, r + 2):
            # deterministic t_hj values in GF(2^16)\{0}
            T = []
            for h in range(n):
                row = []
                for j in range(s):
                    seed = (seed * 1103515245 + 12345) % (1 << 31)
                    row.append((seed >> 8) % 65535 + 1)
                T.append(row)
            opu = []
            for h in range(n):
                el = [0] * N
                el[0] = 1
                for j in range(s):
                    el[1 << j] = T[h][j]
                opu.append(el)
            cache = {}
            def Pn(x):
                if x not in cache:
                    R = [0] * N
                    R[0] = 1
                    for h in range(n):
                        if (x >> h) & 1:
                            R = num_alg_mul(R, opu[h], s)
                    cache[x] = R
                return cache[x]
            def Lpair(x, y):
                return num_alg_mul(Pn(x), Pn(y), s)[N - 1]
            vs, ws = subcube_system(n, r)
            k = len(vs)
            check(is_close_skew(vs, ws, r) and k == (1 << r),
                  "r=%d n=%d: subcube close-skew system valid, k=2^r=%d" % (r, n, k))
            pairs = reversed_doubling(vs, ws)
            check(is_skew(pairs, r), "r=%d n=%d: reversed doubling is skew, length %d" % (r, n, len(pairs)))
            m = len(pairs)
            M = [[Lpair(pairs[i][0], pairs[j][1]) for j in range(m)] for i in range(m)]
            tri = all(M[i][j] == 0 for i in range(m) for j in range(i + 1, m))
            diag = all(M[i][i] != 0 for i in range(m))
            rk = rank_gf(M)
            # rank of the P_{a_i} vectors in A
            rkA = rank_gf([Pn(a) for a, b in pairs])
            check(tri and diag, "r=%d n=%d: M_ij = L(P_a_i P_b_j) is triangular with nonzero diagonal" % (r, n))
            check(rk == m and m <= N and rkA <= N,
                  "r=%d n=%d: rank M = %d = m <= dim A = %d (rank of P_a in A = %d)" % (r, n, rk, N, rkA))
            # isotropic subspace
            Pv = [Pn(v) for v in vs]
            iso = all(Lpair(vi, vj) == 0 for vi in vs for vj in vs)
            dimU = rank_gf(Pv)
            # Gram matrix of B on monomial basis: B(e_S, e_T) = [T = complement of S]
            basis = [[1 if i == S else 0 for i in range(N)] for S in range(N)]
            G = [[num_alg_mul(basis[a], basis[b], s)[N - 1] for b in range(N)] for a in range(N)]
            nondeg = rank_gf(G) == N
            # U-perp = kernel of the k x N matrix (B(P_v_i, e_S))_S
            Bm = [[num_alg_mul(Pv[i], basis[S], s)[N - 1] for S in range(N)] for i in range(k)]
            dimPerp = N - rank_gf(Bm)
            check(nondeg, "r=%d n=%d: B(z,z')=L(zz') nondegenerate on A (dim %d)" % (r, n, N))
            check(iso and dimU == k and dimU + dimPerp == N and 2 * dimU <= N,
                  "r=%d n=%d: U isotropic, dim U=%d, dim U^perp=%d, 2 dim U <= %d" % (r, n, dimU, dimPerp, N))
            # mutation: drop the diameter condition: full (r+1)-subcube with antipodes
            fv = list(range(1 << s))
            fw = [((~x) & ((1 << s) - 1)) for x in fv]
            witness_ok = all(dist(fw[i], fv[i]) > r for i in range(len(fv))) and \
                all(dist(fw[i], fv[j]) <= r for i in range(len(fv)) for j in range(i))
            Pf = [Pn(v) for v in fv]
            dimF = rank_gf(Pf)
            isoF = all(Lpair(a, b) == 0 for a in fv for b in fv)
            check(witness_ok and len(fv) > (1 << r) and not is_close_skew(fv, fw, r) and dimF == len(fv) and not isoF,
                  "MUTANT r=%d n=%d: dropping diameter allows k=%d > 2^r, span not isotropic" % (r, n, len(fv)))

# ---------------------------------------------------------------------------
# Part 2: theta via the recurrence; Lew sequences
# graphs: adjacency list of bitmasks over vertex indices
# ---------------------------------------------------------------------------
def make_theta(adj, canon_isolates=False):
    memo = {}
    def T(S):
        if S in memo:
            return memo[S]
        piv = []
        x = S
        while x:
            b = x & (-x)
            v = b.bit_length() - 1
            x ^= b
            if adj[v] & S:
                piv.append(v)
        if not piv:
            memo[S] = 0
            return 0
        if canon_isolates:
            core = 0
            for v in piv:
                core |= 1 << v
            if core != S:
                val = T(core)
                memo[S] = val
                return val
        best = None
        for v in piv:
            a = T(S & ~(1 << v))
            if best is not None and a >= best:
                continue
            b = 1 + T(S & ~(adj[v] | (1 << v)))
            val = a if a > b else b
            if best is None or val < best:
                best = val
        memo[S] = best
        return best
    return T

def make_lew_rec(adj):
    # s(H) = max(0, max over nonisolated p of 1 + s(H - N[p]))  (derived, see REPORT)
    memo = {}
    def L(S):
        if S in memo:
            return memo[S]
        best = 0
        x = S
        while x:
            b = x & (-x)
            v = b.bit_length() - 1
            x ^= b
            if adj[v] & S:
                val = 1 + L(S & ~(adj[v] | (1 << v)))
                if val > best:
                    best = val
        memo[S] = best
        return best
    return L

def lew_brute(adj, nv):
    # direct DFS on the definition (Lew Prop 11 conditions i-iii), no recurrence
    best = [0]
    def dfs(ps, qs):
        if len(ps) > best[0]:
            best[0] = len(ps)
        for p in range(nv):
            if p in ps or any((adj[p] >> a) & 1 for a in ps):
                continue
            for q in range(nv):
                if not (adj[p] >> q) & 1:
                    continue
                if any((adj[a] >> q) & 1 for a in ps):
                    continue  # p_j q_i must be a nonedge for j < i
                dfs(ps + [p], qs + [q])
    dfs([], [])
    return best[0]

def hamming_graph(n, r):
    N = 1 << n
    adj = [0] * N
    for a in range(N):
        m = 0
        for b in range(N):
            if dist(a, b) > r:
                m |= 1 << b
        adj[a] = m
    return adj

def part2_theta():
    print("== Part 2: theta(VR(I_n;r)) by exact minimax recurrence ==")
    for (n, r) in ((2, 1), (3, 1), (3, 2), (4, 1), (4, 2), (4, 3)):
        adj = hamming_graph(n, r)
        T = make_theta(adj)
        full = (1 << (1 << n)) - 1
        t = T(full)
        check(t == (1 << r), "theta(VR(I_%d;%d)) = %d (expected 2^r = %d)" % (n, r, t, 1 << r))
        L = make_lew_rec(adj)
        d = L(full)
        check(d == (1 << r), "d'(VR(I_%d;%d)) = %d via Lew recurrence (conj:skew small case)" % (n, r, d))
    # independent small cases of conj:skew beyond the paper's r<=2 or n=r+1, by the Lew recurrence
    for (n, r) in ((5, 3), (5, 2)):
        adj = hamming_graph(n, r)
        L = make_lew_rec(adj)
        d = L((1 << (1 << n)) - 1)
        check(d == (1 << r), "d'(VR(I_%d;%d)) = %d via Lew recurrence" % (n, r, d))
    print("== Part 2b: subcube tightness through r=4, n=6 ==")
    for r in (1, 2, 3, 4):
        for n in range(r + 1, 7):
            adj = hamming_graph(n, r)
            Q = 0
            for x in range(1 << (r + 1)):
                Q |= 1 << x  # coordinate subcube on the first r+1 coordinates
            edges = 0
            matching = True
            x = Q
            while x:
                b = x & (-x)
                v = b.bit_length() - 1
                x ^= b
                nb = adj[v] & Q
                if popcount(nb) != 1 or nb != (1 << (v ^ ((1 << (r + 1)) - 1))):
                    matching = False
                edges += popcount(nb)
            T = make_theta(adj, canon_isolates=True)
            tQ = T(Q)
            vs, ws = subcube_system(n, r)
            check(matching and edges == 2 * (1 << r) and tQ == (1 << r) and is_close_skew(vs, ws, r),
                  "n=%d r=%d: subcube induces antipodal perfect matching (%d edges), theta = %d, close-skew length 2^r valid"
                  % (n, r, edges >> 1, tQ))

# ---------------------------------------------------------------------------
# Part 3: T(H) <= s(H) on all labeled graphs on 4 vertices + 100 sampled on 5
# ---------------------------------------------------------------------------
def graph_from_mask(nv, mask):
    adj = [0] * nv
    k = 0
    for i in range(nv):
        for j in range(i + 1, nv):
            if (mask >> k) & 1:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            k += 1
    return adj

def part3_T_le_s():
    print("== Part 3: T(H) <= s(H) ==")
    ok = True
    eq_rec = True
    mono_ok = True
    iso_ok = True
    cnt = 0
    graphs = [(4, m) for m in range(1 << 6)]
    seed = 987654321
    for i in range(100):
        seed = (seed * 6364136223846793005 + 1442695040888963407) % (1 << 64)
        graphs.append((5, (seed >> 20) % (1 << 10)))
    for nv, m in graphs:
        adj = graph_from_mask(nv, m)
        full = (1 << nv) - 1
        T = make_theta(adj)
        t = T(full)
        sb = lew_brute(adj, nv)
        sr = make_lew_rec(adj)(full)
        cnt += 1
        if t > sb:
            ok = False
        if sb != sr:
            eq_rec = False
        # monotonicity on all induced subgraphs
        for S in range(1 << nv):
            if T(S) > t:
                mono_ok = False
        # isolate invariance: add an isolated vertex
        adj2 = adj + [0]
        T2 = make_theta(adj2)
        if T2((1 << (nv + 1)) - 1) != t:
            iso_ok = False
    check(ok, "T(H) <= s(H) on all %d graphs (64 on 4 vertices + 100 sampled on 5)" % cnt)
    check(eq_rec, "brute-force Lew s(H) equals the recurrence s(H)=max_p 1+s(H-N[p]) on all %d graphs" % cnt)
    check(mono_ok, "T monotone on all induced subgraphs of the %d graphs" % cnt)
    check(iso_ok, "adding an isolated vertex leaves T unchanged on all %d graphs" % cnt)
    # matchings
    mok = True
    for m in range(0, 7):
        adj = [0] * (2 * m)
        for i in range(m):
            adj[2 * i] = 1 << (2 * i + 1)
            adj[2 * i + 1] = 1 << (2 * i)
        if make_theta(adj)((1 << (2 * m)) - 1) != m:
            mok = False
    check(mok, "T(M_m) = m for matchings m = 0..6")

# ---------------------------------------------------------------------------
# Part 4: positive and mutation controls
# ---------------------------------------------------------------------------
def find_asymmetric_example():
    # close-skew system with a one-sided witness: some w_i far from a later v_j (j > i)
    for (n, r) in ((3, 1), (4, 2), (4, 1)):
        N = 1 << n
        for k in (2, 3):
            for vs in itertools.permutations(range(N), k):
                if any(dist(a, b) > r for a in vs for b in vs):
                    continue
                cand = [[w for w in range(N) if dist(w, vs[i]) > r and all(dist(w, vs[j]) <= r for j in range(i))]
                        for i in range(k)]
                for ws in itertools.product(*cand):
                    if any(dist(ws[i], vs[j]) > r for i in range(k) for j in range(i + 1, k)):
                        return n, r, list(vs), list(ws)
    return None

def find_append_counterexample():
    # graph H, nonisolated p, neighbor q, Lew list in H - N[p] such that APPENDING (p,q) fails
    for nv in (3, 4):
        for m in range(1 << (nv * (nv - 1) >> 1)):
            adj = graph_from_mask(nv, m)
            for p in range(nv):
                if not adj[p]:
                    continue
                rest = [v for v in range(nv) if v != p and not (adj[p] >> v) & 1]
                for a in rest:
                    for b in rest:
                        if (adj[a] >> b) & 1:
                            for q in range(nv):
                                if (adj[p] >> q) & 1 and (adj[a] >> q) & 1:
                                    return nv, m, p, q, a, b
    return None

def lew_valid(adj, seq):
    ps = [a for a, b in seq]
    if len(set(ps)) != len(ps):
        return False
    for i in range(len(seq)):
        for j in range(len(seq)):
            if i != j and (adj[ps[i]] >> ps[j]) & 1:
                return False
        if not (adj[seq[i][0]] >> seq[i][1]) & 1:
            return False
        for j in range(i):
            if (adj[seq[j][0]] >> seq[i][1]) & 1:
                return False
    return True

def part4_controls():
    print("== Part 4: controls ==")
    ex = find_asymmetric_example()
    check(ex is not None, "found an asymmetric (one-sided-witness) close-skew example")
    if ex:
        n, r, vs, ws = ex
        rd = reversed_doubling(vs, ws)
        fd = forward_doubling(vs, ws)
        check(is_close_skew(vs, ws, r) and is_skew(rd, r),
              "POSITIVE n=%d r=%d v=%s w=%s: reversed doubling skew" % (n, r, vs, ws))
        check(not is_skew(fd, r), "MUTANT forward doubling on the same example is NOT skew")
    # exhaustive: reversed doubling skew for every close-skew system on small cubes
    allok = True
    tot = 0
    for (n, r) in ((2, 1), (3, 1), (3, 2)):
        N = 1 << n
        def rec(vs, ws):
            nonlocal_ok = True
            if vs:
                rd = reversed_doubling(vs, ws)
                if not is_skew(rd, r):
                    nonlocal_ok = False
            cnt = 1
            for v in range(N):
                if any(dist(v, a) > r for a in vs):
                    continue
                for w in range(N):
                    if dist(w, v) > r and all(dist(w, a) <= r for a in vs):
                        c, o = rec(vs + [v], ws + [w])
                        cnt += c
                        nonlocal_ok = nonlocal_ok and o
            return cnt, nonlocal_ok
        c, o = rec([], [])
        tot += c
        allok = allok and o
    check(allok, "reversed doubling skew for ALL %d close-skew systems on (n,r) in (2,1),(3,1),(3,2)" % tot)
    ce = find_append_counterexample()
    check(ce is not None, "found graph where APPENDING (p,q) breaks the Lew list")
    if ce:
        nv, m, p, q, a, b = ce
        adj = graph_from_mask(nv, m)
        good = lew_valid(adj, [(p, q), (a, b)])
        bad = lew_valid(adj, [(a, b), (p, q)])
        check(good and not bad,
              "MUTANT append: graph nv=%d mask=%d, prepend [(%d,%d),(%d,%d)] valid, append invalid" % (nv, m, p, q, a, b))

def main():
    bad = self_audit()
    check(not bad, "self-audit: no single-slash, float, math import or future import (%s)" % (bad[:3],))
    part1_symbolic()
    part1_finite_field()
    part2_theta()
    part3_T_le_s()
    part4_controls()
    print("SUMMARY: %d failures" % len(FAIL))
    return 1 if FAIL else 0

if __name__ == "__main__":
    sys.exit(main())
