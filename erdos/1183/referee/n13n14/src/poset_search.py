"""Exact search for union/intersection-closed families when colour depends only on set size.
A closed family L in 2^[n] with min A, max B is (Birkhoff) the down-set lattice of its poset P of
join-irreducibles; |S_D| = |A| + sum_{J in D} w(J) with integer weights w(J) >= 1, |A| + sum w <= n,
and every such weighted poset is realised. Elements are added one at a time in a linear extension
(natural labelling); each prefix is a down-set of P, so its down-sets are members of the final family.
The number of down-sets strictly grows, so any family with >= t members passes through a prefix
with >= t members whose ancestors all have < t members and valid sizes: the DFS below is complete."""
import sys, itertools

def search(n, R, t, want_witness=True):
    """R: set of allowed sizes. Return witness (a, elems) with >= t down-sets, or None.
    elems: list of (pred_downset_bitmask, weight). nodes counted."""
    nodes = [0]
    def dfs(a, used, downs, elems):
        # downs: dict downset_bitmask -> weight sum
        nodes[0] += 1
        if len(downs) >= t:
            return (a, list(elems))
        k = len(elems)
        for D0 in list(downs):
            sup = [D for D in downs if D & D0 == D0]
            for w in range(1, n - a - used + 1):
                if all((a + downs[D] + w) in R for D in sup):
                    nd = dict(downs)
                    for D in sup:
                        nd[D | (1 << k)] = downs[D] + w
                    elems.append((D0, w))
                    r = dfs(a, used + w, nd, elems)
                    elems.pop()
                    if r: return r
        return None
    for a in range(n + 1):
        if a in R:
            r = dfs(a, 0, {0: 0}, [])
            if r: return r, nodes[0]
    return None, nodes[0]

def realise(n, a, elems):
    """Turn a weighted poset into actual subsets of [n] (bit i = element i+1)."""
    nxt = a; blocks = []
    for D0, w in elems:
        blocks.append(sum(1 << (nxt + i) for i in range(w))); nxt += w
    assert nxt <= n
    A = (1 << a) - 1
    k = len(elems)
    # down-sets: closed under predecessors (pred sets are down-sets, so closure is one-step)
    fam = set()
    for m in range(1 << k):
        if all((m >> i) & 1 == 0 or (elems[i][0] & m) == elems[i][0] for i in range(k)):
            S = A
            for i in range(k):
                if (m >> i) & 1: S |= blocks[i]
            fam.add(S)
    return sorted(fam)

def closed(fam):
    F = set(fam)
    return all((x | y) in F and (x & y) in F for x in F for y in F)

if __name__ == "__main__":
    n = int(sys.argv[1]); word = sys.argv[2]; t = int(sys.argv[3])
    assert len(word) == n + 1
    for c in "01":
        R = {i for i, ch in enumerate(word) if ch == c}
        r, nodes = search(n, R, t)
        if r:
            fam = realise(n, *r)
            ok = closed(fam) and all(bin(S).count("1") in R for S in fam) and len(fam) >= t
            print(f"n={n} word={word} colour={c} t={t}: FOUND {len(fam)} sets, independent closure check {'OK' if ok else 'FAIL'}; masks={fam}; sizes={[bin(S).count('1') for S in fam]}; nodes={nodes}")
        else:
            print(f"n={n} word={word} colour={c} t={t}: NONE (exhaustive, {nodes} DFS nodes)")
