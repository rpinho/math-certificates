# Exact maximum monochromatic sublattice for a rank colouring (colour of S = word[|S|]) by
# ordinal-sum DP over connected weighted posets (connected-prefix linear extensions), + explicit witness.
import sys, time
def comps(word, c, cap):
    n = len(word) - 1; best = {}   # (r, r2) -> (gain, structure)
    def dfs(r, elems, ideals, top):
        # elems: list of (downmask, weight); ideals: list of (mask, rank)
        g = len(ideals) - 1
        key = (r, top)
        if g > best.get(key, (0,))[0]: best[key] = (g, list(elems))
        if len(ideals) >= cap: return
        full = (1 << len(elems)) - 1
        for D, rD in ideals:
            if D == full: continue                     # connected prefix: p incomparable with some element
            ups = [(I, rI) for I, rI in ideals if I & D == D]
            mx = max(rI for _, rI in ups)
            for w in range(1, n - mx + 1):
                if all(word[rI + w] == c for _, rI in ups):
                    p = 1 << len(elems)
                    dfs(r, elems + [(D, w)], ideals + [(I | p, rI + w) for I, rI in ups], max(top, mx + w))
    for r in range(n + 1):
        if word[r] != c: continue
        for w in range(1, n - r + 1):
            if word[r + w] == c:
                dfs(r, [(0, w)], [(0, r), (1, r + w)], r + w)
    return best
def exact(word, c, cap=40):
    n = len(word) - 1
    best = comps(word, c, cap)
    f = {}  # longest path from r
    for r in range(n, -1, -1):
        if word[r] != c: continue
        f[r] = (1, [])
        for (a, b), (g, st) in best.items():
            if a == r and b in f and f[b][0] + g > f[r][0]: f[r] = (f[b][0] + g, [(a, b, st)] + f[b][1])
    r0 = max(f, key=lambda r: f[r][0])
    return f[r0][0], r0, f[r0][1]
def family(word, r0, path):
    # physical sets: base = first r0 coords; each element gets a fresh bundle of w coords
    nxt = r0; base = (1 << r0) - 1; fam = {base}
    for a, b, st in path:
        bund = []
        for D, w in st: bund.append(((1 << (nxt + w)) - 1) ^ ((1 << nxt) - 1)); nxt += w
        k = len(st); ids = [I for I in range(1 << k) if all((not (I >> i) & 1) or (st[i][0] & I) == st[i][0] for i in range(k))]
        for I in ids:
            s = base
            for i in range(k):
                if (I >> i) & 1: s |= bund[i]
            fam.add(s)
        base = fam and max(fam, key=lambda s: bin(s).count('1'))
    return sorted(fam)
def verify(word, c, fam):
    n = len(word) - 1; S = set(fam)
    return (all(m < (1 << n) and word[bin(m).count('1')] == c for m in fam) and
            all((x | y) in S and (x & y) in S for x in fam for y in fam)), len(S)
if __name__ == '__main__':
    for word in sys.argv[1:]:
        for c in '01':
            t = time.time(); h, r0, path = exact(word, c)
            fam = family(word, r0, path); ok, sz = verify(word, c, fam)
            print(word, 'n=%d' % (len(word) - 1), 'colour', c, 'max', h, 'witness valid', ok, 'size', sz, '%.1fs' % (time.time() - t), flush=True)
