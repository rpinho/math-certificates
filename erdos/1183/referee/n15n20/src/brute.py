"""Referee's brute force: enumerate every nonempty sublattice (closed under binary union and intersection) of 2^[n]
by closure growth, then the exact colour maxima of every rank word. Independent of the weighted-poset reduction.
Usage: python3 brute.py N  -> prints '#count', then 'word max0 max1' for all 2^(N+1) words."""
import sys

n = int(sys.argv[1])
U = 1 << n


def close(members):
    s = set(members)
    todo = list(s)
    while todo:
        x = todo.pop()
        for y in list(s):
            for z in (x | y, x & y):
                if z not in s:
                    s.add(z)
                    todo.append(z)
    return frozenset(s)


seen = set()
frontier = [frozenset([x]) for x in range(U)]
seen.update(frontier)
while frontier:
    nxt = []
    for L in frontier:
        for x in range(U):
            if x in L:
                continue
            M = close(L | {x})
            if M not in seen:
                seen.add(M)
                nxt.append(M)
    frontier = nxt
print("#count", len(seen))
best = {}  # rank-set mask -> max size
for L in seen:
    r = 0
    for x in L:
        r |= 1 << bin(x).count("1")
    if best.get(r, 0) < len(L):
        best[r] = len(L)
for w in range(1 << (n + 1)):
    word = "".join(str((w >> i) & 1) for i in range(n + 1))
    out = []
    for c in (0, 1):
        R = sum(1 << i for i in range(n + 1) if int(word[i]) == c)
        out.append(max([v for r, v in best.items() if r & ~R == 0], default=0))
    print(word, out[0], out[1])
