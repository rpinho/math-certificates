#!/usr/bin/env python3
"""Clean-room referee code for Erdos #1183, n=12 (stdlib only).
Bit i of a mask = element i+1 of [12].

Subcommands:
  colour  JSON              check colouring data, rank structure, a 7-member witness, chain lower bound
  dfs     JSON              exact search over (offset, weighted poset) for rank colourings
  cnf     JSON c k OUT [b t]  CNF: >=k members, closed under union/intersection, inside colour c;
                             optional b t: members lie in [B,T], B={1..b}, T={1..t}, B and T forced in
  model   JSON c MAP SOL    decode a SAT model and verify the family directly
"""
import sys, json, itertools

N = 12
FULL = (1 << N) - 1
pc = lambda m: bin(m).count("1")


def load(path):
    d = json.load(open(path))
    col = d["color_by_mask"]
    assert len(col) == 1 << N and set(col) <= {0, 1}
    return col


def is_lattice(fam):
    s = set(fam)
    return all((a | b) in s and (a & b) in s for a in s for b in s)


def cmd_colour(path):
    col = load(path)
    rank = {}
    for m in range(1 << N):
        rank.setdefault(pc(m), set()).add(col[m])
    assert all(len(v) == 1 for v in rank.values()), "colour is not a function of rank"
    word = "".join(str(rank[r].pop()) for r in range(N + 1))
    print("colouring depends only on |S|; rank word r=0..12:", word)
    for c in (0, 1):
        R = [r for r in range(N + 1) if word[r] == str(c)]
        print(f"colour {c}: ranks {R}, {sum(col[m]==c for m in range(1<<N))} sets")
    # explicit 7-member chain in colour 1
    w = [(1 << r) - 1 for r in range(N + 1) if word[r] == "1"]
    assert len(w) == 7 and is_lattice(w) and all(col[m] == 1 for m in w)
    print("7-member colour-1 sublattice (masks):", w)
    print("  as sets:", [sorted(i + 1 for i in range(N) if m >> i & 1) for m in w])
    # chain lower bound: every 2-colouring of a 13-chain has a colour class >= 7
    worst = min(max(pc(x), 13 - pc(x)) for x in range(1 << 13))
    print("min over all 8192 colourings of a 13-member chain of the larger class:", worst)
    return word


def cmd_dfs(path, word=None, n=N, quiet=False):
    """Every sublattice L of 2^[n] equals {B u D : D a down-set of a preorder on T\\B},
    so |X| = |B| + sum of block weights over an ideal of a weighted poset P.
    Build P one maximal element at a time; ideals (and their sums) only get added,
    so the monochromatic condition is monotone and pruning is exact."""
    if word is None:
        col = load(path)
        word = "".join(str(col[(1 << r) - 1]) for r in range(n + 1))
    best = {0: 0, 1: 0}
    found = {0: None, 1: None}
    for c in (0, 1):
        ok = [word[r] == str(c) for r in range(n + 1)]
        for b in range(n + 1):
            if not ok[b]:
                continue
            # state: ideals = list of (frozenset of element indices, weight sum); total weight
            stack = [([(frozenset(), 0)], 0, 0)]
            while stack:
                ideals, tot, k = stack.pop()
                if len(ideals) > best[c]:
                    best[c] = len(ideals)
                    found[c] = (b, ideals)
                if len(ideals) >= 8:
                    continue  # counterexample recorded; no need to grow
                for D, dsum in ideals:  # strict down-set of the new element
                    for w in range(1, n - b - tot + 1):
                        new = [(I | {k}, s + w) for I, s in ideals if D <= I]
                        if all(ok[b + s] for _, s in new):
                            stack.append((ideals + new, tot + w, k + 1))
        if not quiet:
            bb, ideals = found[c]
            print(f"colour {c}: largest monochromatic sublattice size {best[c]}; "
                  f"example offset {bb}, member sizes {sorted(bb + s for _, s in ideals)}")
    return best


def cmd_cnf(path, c, k, out, b=None, t=None):
    col = load(path)
    if b is None:
        mem = [m for m in range(1 << N) if col[m] == c]
        units = []
    else:
        B, T = (1 << b) - 1, (1 << t) - 1
        assert col[B] == c and col[T] == c
        mem = [m for m in range(1 << N) if col[m] == c and m & B == B and m | T == T]
    var = {m: i + 1 for i, m in enumerate(mem)}
    nv = len(mem)
    cls = []
    if b is not None:
        cls += [[var[B]], [var[T]]]
    for x, y in itertools.combinations(mem, 2):
        if x & y in (x, y):
            continue  # comparable: closure automatic
        for z in (x | y, x & y):
            cls.append([-var[x], -var[y]] + ([var[z]] if z in var else []))
    # totalizer, outputs truncated at k; o_j => (count >= j)
    def tot(lo, hi):
        nonlocal nv
        if hi - lo == 1:
            return [lo + 1]
        mid = (lo + hi) // 2
        a, bq = tot(lo, mid), tot(mid, hi)
        m = min(k, len(a) + len(bq))
        o = list(range(nv + 1, nv + m + 1))
        nv += m
        for i in range(len(a) + 1):
            for j in range(len(bq) + 1):
                if i + j + 1 > m:
                    continue
                cl = [-o[i + j]]
                if i < len(a):
                    cl.append(a[i])
                if j < len(bq):
                    cl.append(bq[j])
                cls.append(cl)
        return o
    outs = tot(0, len(mem))
    if len(outs) < k:
        cls.append([])  # fewer than k candidates: trivially UNSAT
    else:
        cls.append([outs[k - 1]])
    with open(out, "w") as f:
        f.write(f"p cnf {nv} {len(cls)}\n")
        for cl in cls:
            f.write(" ".join(map(str, cl)) + " 0\n")
    json.dump(mem, open(out + ".map", "w"))
    print(f"{out}: colour {c} k {k} interval {b,t}: {len(mem)} member vars, {nv} vars, {len(cls)} clauses")


def cmd_model(path, c, mapf, solf):
    col = load(path)
    mem = json.load(open(mapf))
    true = set()
    for line in open(solf):
        if line.startswith("v"):
            true |= {int(x) for x in line.split()[1:] if int(x) > 0}
    fam = [m for i, m in enumerate(mem) if i + 1 in true]
    assert all(col[m] == c for m in fam) and is_lattice(fam)
    print(f"model family: {len(fam)} distinct sets, all colour {c}, closed under union and intersection")
    print("  masks:", sorted(fam))
    print("  sets:", [sorted(i + 1 for i in range(N) if m >> i & 1) for m in sorted(fam)])


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "colour":
        cmd_colour(a[1])
    elif a[0] == "dfs":
        cmd_dfs(a[1])
    elif a[0] == "cnf":
        cmd_cnf(a[1], int(a[2]), int(a[3]), a[4], *(int(x) for x in a[5:7]) if len(a) > 5 else ())
    elif a[0] == "model":
        cmd_model(a[1], int(a[2]), a[3], a[4])
