# second control: enumerate every closed family inside the allowed (colour-c) sets by closure growth; n=5 all words, n=6 sample
import itertools, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rank_exact import exact
def maxclosed(n, allowed):
    A = set(allowed); seen = set(); best = 0; stack = []
    def clos(F):
        F = set(F); ch = True
        while ch:
            ch = False
            for a in list(F):
                for b in list(F):
                    for x in (a | b, a & b):
                        if x not in F:
                            if x not in A: return None
                            F.add(x); ch = True
        return frozenset(F)
    for s in A:
        f = frozenset([s]); seen.add(f); stack.append(f)
    while stack:
        F = stack.pop(); best = max(best, len(F))
        for s in A - F:
            G = clos(F | {s})
            if G is not None and G not in seen: seen.add(G); stack.append(G)
    return best
random.seed(1); bad = tot = 0
cases = [(5, ''.join(w)) for w in itertools.product('01', repeat=6)] + [(6, ''.join(random.choice('01') for _ in range(7))) for _ in range(12)]
for n, word in cases:
    for c in '01':
        allowed = [s for s in range(1 << n) if word[bin(s).count('1')] == c]
        if not allowed: continue
        bf = maxclosed(n, allowed); ex = exact(word, c)[0]
        tot += 1; bad += bf != ex
        if bf != ex: print('MISMATCH', word, c, bf, ex)
print('rank_exact vs closure enumeration (n=5 all words, n=6 12 random words):', tot, 'cases,', bad, 'mismatches')
