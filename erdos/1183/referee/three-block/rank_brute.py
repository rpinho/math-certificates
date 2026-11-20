# brute-force control for rank_exact on all words, n<=4 (every subfamily of 2^[n])
import itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rank_exact import exact
bad = tot = 0
for n in range(0, 5):
    sets = list(range(1 << n))
    closed = []
    for F in range(1, 1 << (1 << n)):
        S = [s for s in sets if (F >> s) & 1]; T = set(S)
        if all((a | b) in T and (a & b) in T for a in S for b in S): closed.append(S)
    for wbits in itertools.product('01', repeat=n + 1):
        word = ''.join(wbits)
        for c in '01':
            bf = max([len(S) for S in closed if all(word[bin(s).count('1')] == c for s in S)] or [0])
            ex = exact(word, c)[0] if c in word else 0
            tot += 1; bad += bf != ex
print('rank_exact vs brute force, all words n<=4, both colours:', tot, 'cases,', bad, 'mismatches')
