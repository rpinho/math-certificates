"""Referee's own test of the Kempe-swap step (PROOF.md lines 21-25) on random 10-regular configurations.

Each instance: a map f: V -> Z5 with Region-C-like gaps (v0, v2 >= v3 + 2, v2 >= v4 + 2) and a random
10-regular configuration (multigraph, loops allowed) all of whose stub pairs are blue for f.
To make the hypothesis of the swap occur often, every vertex gets a random subset of its blue part list
it is allowed to touch (pairing respects it both ways).
Checks, for every u in V0 with n2(u)>=1 whose V2-neighbours all have n4=0 and for which
|Z0 \\ (N(u) ∪ {u})| >= r-1:
   the swap (u:0->3, each v_j:2->0, r-1 donors 0->2) gives a valid map, net profile change (0,0,-1,+1,0),
   and Phi decreases by 2(v3 - v2 + 1).
Also checks the counting claim |Z0| >= 2d  =>  enough donors, the one-vertex moves, and three mutants.
Usage: python -I kempe_sim.py SEED N_INSTANCES OUT.json
"""
import sys, json, random

d = 10
BLUEDIFF = {0, 2, 3}


def blue(i, j):
    return (j - i) % 5 in BLUEDIFF


def make_instance(rng):
    while True:
        n = rng.randint(40, 160)
        v3 = rng.randint(1, n // 6); v4 = rng.randint(0, v3); v1 = rng.randint(0, n // 8)
        rest = n - v1 - v3 - v4
        v0 = rest // 2 + rng.randint(-3, 3); v2 = rest - v0
        if min(v0, v2) >= v3 + 2 and v2 >= v4 + 2 and v0 >= 1:
            break
    f = [0] * v0 + [1] * v1 + [2] * v2 + [3] * v3 + [4] * v4
    rng.shuffle(f)
    n = len(f)
    allowed = []
    for x in range(n):
        p = f[x]
        cand = [q for q in range(5) if blue(p, q)]
        others = [q for q in cand if q != p]
        keep = {p}
        for q in others:
            if rng.random() < 0.6:
                keep.add(q)
        allowed.append(keep)
    for attempt in range(50):
        stubs = [x for x in range(n) for _ in range(d)]
        rng.shuffle(stubs)
        mate = []
        pool = stubs[:]
        ok = True
        while pool:
            a = pool.pop()
            # candidates: stubs whose vertex part is allowed by a and which allow a's part
            idx = [k for k, b in enumerate(pool) if f[b] in allowed[a] and f[a] in allowed[b]]
            if not idx:
                ok = False; break
            k = rng.choice(idx)
            b = pool[k]; pool[k] = pool[-1]; pool.pop()
            mate.append((a, b))
        if ok:
            return f, mate
    return None


def valid(f, edges):
    return all(blue(f[a], f[b]) for a, b in edges)


def bad_edges(f, edges):
    return [(a, b) for a, b in edges if not blue(f[a], f[b])]


def analyse(f, edges, rng, stats, examples):
    n = len(f)
    nbr = [[] for _ in range(n)]
    for a, b in edges:
        nbr[a].append(b)
        if a != b:
            nbr[b].append(a)
        else:
            nbr[a].append(a)  # loop: two stub ends at a
    cnt = [[0] * 5 for _ in range(n)]
    for x in range(n):
        for y in nbr[x]:
            cnt[x][f[y]] += 1
    v = [f.count(i) for i in range(5)]
    V0 = [x for x in range(n) if f[x] == 0]
    Z0 = [x for x in V0 if cnt[x][3] == 0]
    Z0set = set(Z0)
    G2 = {x for x in range(n) if f[x] == 2 and cnt[x][4] == 0}
    phi = sum(c * c for c in v)
    # one-vertex moves
    for x in V0:
        if cnt[x][2] == 0:
            g = f[:]; g[x] = 3
            stats["move03"] += 1
            if not valid(g, edges):
                stats["move03_invalid"] += 1
    for x in range(n):
        if f[x] == 2 and cnt[x][0] == 0:
            g = f[:]; g[x] = 4
            stats["move24"] += 1
            if not valid(g, edges):
                stats["move24_invalid"] += 1
    for u in V0:
        N2 = sorted({y for y in nbr[u] if f[y] == 2})
        r = len(N2)
        if r == 0:
            continue
        Nu = set(nbr[u]) | {u}
        pool = [z for z in Z0 if z not in Nu]
        hyp = all(y in G2 for y in N2)
        if len(Z0) >= 2 * d:
            stats["Z0big_u"] += 1
            if len(pool) < r - 1:
                stats["Z0big_but_short"] += 1
        if hyp:
            stats["hyp_u"] += 1
            if len(pool) >= r - 1:
                donors = rng.sample(pool, r - 1)
                g = f[:]
                g[u] = 3
                for y in N2:
                    g[y] = 0
                for z in donors:
                    g[z] = 2
                w = [g.count(i) for i in range(5)]
                dprof = [w[i] - v[i] for i in range(5)]
                dphi = sum(c * c for c in w) - phi
                stats["swaps"] += 1
                if not valid(g, edges):
                    stats["swap_invalid"] += 1
                    if len(examples) < 3:
                        examples.append({"kind": "SWAP_INVALID", "u": u, "bad": bad_edges(g, edges)[:3]})
                if dprof != [0, 0, -1, 1, 0]:
                    stats["swap_wrong_profile"] += 1
                if dphi != 2 * (v[3] - v[2] + 1) or dphi >= 0:
                    stats["swap_phi_not_decreasing"] += 1
            # mutant A: donors may be adjacent to u
            poolA = [z for z in Z0 if z != u]
            adjZ = [z for z in poolA if z in Nu]
            if adjZ and len(poolA) >= r - 1 and r >= 2:
                donors = [rng.choice(adjZ)]
                rest = [z for z in poolA if z != donors[0]]
                if len(rest) >= r - 2:
                    donors += rng.sample(rest, r - 2)
                    g = f[:]; g[u] = 3
                    for y in N2: g[y] = 0
                    for z in donors: g[z] = 2
                    stats["mutA_swaps"] += 1
                    if not valid(g, edges):
                        stats["mutA_invalid"] += 1
                        if len([e for e in examples if e["kind"] == "MUT_A"]) < 2:
                            examples.append({"kind": "MUT_A", "u": u, "donor_adjacent": donors[0],
                                             "bad": bad_edges(g, edges)[:2], "parts": [g[x] for x in bad_edges(g, edges)[0]]})
            # mutant C: donors from V0 \ Z0 (have a V3 neighbour)
            poolC = [z for z in V0 if z not in Z0set and z not in Nu]
            if poolC and len(pool) >= r - 2 and r >= 2:
                donors = [rng.choice(poolC)] + rng.sample(pool, r - 2) if len(pool) >= r - 2 else None
                if donors:
                    g = f[:]; g[u] = 3
                    for y in N2: g[y] = 0
                    for z in donors: g[z] = 2
                    stats["mutC_swaps"] += 1
                    if not valid(g, edges):
                        stats["mutC_invalid"] += 1
        else:
            # mutant B: hypothesis fails (some V2 neighbour has n4>=1) but swap anyway
            if len(pool) >= r - 1:
                donors = rng.sample(pool, r - 1)
                g = f[:]; g[u] = 3
                for y in N2: g[y] = 0
                for z in donors: g[z] = 2
                stats["mutB_swaps"] += 1
                if not valid(g, edges):
                    stats["mutB_invalid"] += 1


def main():
    seed, N, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    rng = random.Random(seed)
    keys = ["instances", "failed_gen", "move03", "move03_invalid", "move24", "move24_invalid", "Z0big_u",
            "Z0big_but_short", "hyp_u", "swaps", "swap_invalid", "swap_wrong_profile", "swap_phi_not_decreasing",
            "mutA_swaps", "mutA_invalid", "mutB_swaps", "mutB_invalid", "mutC_swaps", "mutC_invalid", "loops"]
    stats = {k: 0 for k in keys}
    examples = []
    for _ in range(N):
        inst = make_instance(rng)
        if inst is None:
            stats["failed_gen"] += 1; continue
        f, edges = inst
        assert valid(f, edges)
        deg = [0] * len(f)
        for a, b in edges:
            deg[a] += 1; deg[b] += 1
        assert all(x == d for x in deg)
        stats["loops"] += sum(1 for a, b in edges if a == b)
        stats["instances"] += 1
        analyse(f, edges, rng, stats, examples)
    json.dump({"seed": seed, "stats": stats, "examples": examples}, open(out, "w"), indent=1)
    print(json.dumps(stats))


if __name__ == "__main__":
    main()
