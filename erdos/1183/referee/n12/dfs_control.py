# control: compare the poset DFS (capped at 8) with brute-force enumeration of all sublattices of 2^[4], all 32 rank words
import sys, itertools
sys.path.insert(0, sys.argv[1]); import ref
n = 4; U = range(1 << n)
lat = []
for bits in range(1, 1 << (1 << n)):
    fam = [m for m in U if bits >> m & 1]
    if ref.is_lattice(fam): lat.append(fam)
print("sublattices of 2^[4]:", len(lat))
bad = 0
for wi in range(1 << (n + 1)):
    word = "".join(str(wi >> r & 1) for r in range(n + 1))
    best = ref.cmd_dfs(None, word, n, quiet=True)
    for c in (0, 1):
        bf = max([len(f) for f in lat if all(word[bin(m).count('1')] == str(c) for m in f)] or [0])
        if min(bf, 8) != min(best[c], 8): bad += 1; print("MISMATCH", word, c, bf, best[c])
print("words x colours compared: 64, mismatches:", bad)
