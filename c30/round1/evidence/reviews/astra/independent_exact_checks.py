"""Referee checks; standard library only. No submission modules imported.

F_0 counts dominoes whose top cell is decreasing. At n total points and
k top points, choose the k positions and a Catalan bottom permutation:
[z^n u^k]F_0 = binomial(n,k) C_(n-k).
We also enumerate actual permutations, cuts, and closed strips independently.
"""
from collections import Counter
from itertools import combinations, permutations
from math import comb
from pathlib import Path
import json
import sys

rows = [json.loads(x) for x in Path(sys.argv[1]).read_text().splitlines()]
# Retrieved from https://oeis.org/A061552/b061552.txt via web on 2026-11-03.
oeis = [1,1,2,6,23,103,513,2762,15793,94776,591950,3824112,
        25431452,173453058,1209639642]
checks = 0
for row in rows:
    n = row['n']
    assert row['avoiders'] == oeis[n]
    expected = {str(k):comb(n,k)*comb(2*(n-k),n-k)//(n-k+1)
                for k in range(n+1)}
    assert expected == row['series']['F'], (n, expected, row['series']['F'])
    checks += n+1

def contains(p, pattern):
    for selected in combinations(p, len(pattern)):
        ranks = tuple(1+sum(y<x for y in selected) for x in selected)
        if ranks == pattern:
            return True
    return False

direct = []
for n in range(8):
    count = 0
    f, marked = Counter(), Counter()
    for p in permutations(range(1,n+1)):
        if contains(p, (1,3,2,4)):
            continue
        count += 1
        for cut in range(n+1):
            bottom = tuple(x for x in p if x<=cut)
            top = tuple(x for x in p if x>cut)
            if contains(bottom,(1,3,2)) or contains(top,(2,1,3)):
                continue
            leaves = {x for i,x in enumerate(top) if x == max(top[i:])}
            if len(leaves)==len(top):
                f[len(top)]+=1
            # Count all internal nonempty strips between consecutive nonleaves.
            nonleaves = sorted(set(top)-leaves)
            for low,high in zip(nonleaves,nonleaves[1:]):
                k = high-low-1
                if k>0:
                    assert all(x in leaves for x in range(low+1,high))
                    marked[k-1]+=1
    assert count == oeis[n]
    assert {str(k):v for k,v in f.items()}==rows[n]['series']['F']
    assert {str(k):v for k,v in marked.items()}==rows[n]['series']['P']
    direct.append({'n':n,'avoiders':count,'P':dict(marked),'F':dict(f)})
print(json.dumps({'status':'PASS','F_coefficients_checked':checks,
                  'max_formula_n':rows[-1]['n'],'direct_n_max':7,
                  'direct':direct},indent=2))
