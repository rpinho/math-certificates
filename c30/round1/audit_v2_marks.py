"""Exact small-size comparison of Norton v2 (12) with actual domino statistics.

No numerical search. The recurrence and the permutation enumeration share no
enumeration routine. This is a diagnostic of a withdrawn source, not a bound.
"""
import argparse
import collections
import itertools
import json
from pathlib import Path


def add(dst, src, delta=(0, 0, 0), scale=1):
    for key, value in src.items():
        dst[tuple(x+y for x,y in zip(key, delta))] += scale*value


def mul(a, b):
    c = collections.Counter()
    for (v, t, s), x in a.items():
        for (w, u, r), y in b.items():
            c[v+w, t+u, s+r] += x*y
    return c


def recurrence(N):
    A = [collections.Counter({(0, 0, 0): 1})]
    powers = {(0, 0): A[0]}
    def power(k, n):
        if (k, n) in powers:
            return powers[k, n]
        out = collections.Counter()
        if k == 0:
            return out
        for j in range(n+1):
            if j < len(A):
                add(out, mul(A[j], power(k-1, n-j)))
        powers[k, n] = out
        return out
    for n in range(1, N+1):
        out = collections.Counter()
        add(out, A[n-1], (0, 1, 0), 2)
        add(out, A[n-1], (1, 1, 1))
        for (v, t, s), count in A[n-1].items():
            if v:
                out[v-1, t, s] += count
                out[v, t, s] += count
        for k in range(2, n+1):
            add(out, power(k, n-k), (0, 1, 1))
        A.append(out)
    return [{(t,s): c for (v,t,s),c in a.items() if v == 0} for a in A]


def avoids(p, pattern):
    for inds in itertools.combinations(range(len(p)), len(pattern)):
        q = [p[i] for i in inds]
        if tuple(sorted(range(len(q)), key=q.__getitem__)) == tuple(sorted(range(len(pattern)), key=pattern.__getitem__)):
            return False
    return True


def cell_stats(p, top):
    leaves = set()
    for i, x in enumerate(p):
        if (all(y < x for y in p[i+1:]) if top else all(y > x for y in p[:i])):
            leaves.add(x)
    indicator = [int(x not in leaves) for x in sorted(p)]
    runs = sum(x == 1 and (i == 0 or indicator[i-1] == 0) for i,x in enumerate(indicator))
    return len(leaves), runs


def enumerate_dominoes(n):
    out = collections.Counter()
    for p in itertools.permutations(range(1,n+1)):
        if not avoids(p, (1,3,2,4)):
            continue
        for cut in range(n+1):
            low = tuple(x for x in p if x <= cut)
            high = tuple(x for x in p if x > cut)
            if not avoids(low, (1,3,2)) or not avoids(high, (2,1,3)):
                continue
            l1,b1 = cell_stats(low,False)
            l2,b2 = cell_stats(high,True)
            out[l1+l2,b1+b2] += 1
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-n',type=int,default=7)
    args = ap.parse_args()
    theory = recurrence(args.max_n)
    rows = []
    for n in range(args.max_n+1):
        actual = enumerate_dominoes(n)
        diff = {str(k):[theory[n].get(k,0),actual.get(k,0)] for k in set(theory[n])|set(actual) if theory[n].get(k,0)!=actual.get(k,0)}
        row = {'n':n, 'recurrence_total':sum(theory[n].values()), 'actual_total':sum(actual.values()),'matches':not diff,'differences':diff}
        rows.append(row)
        print(json.dumps(row),flush=True)
    Path('artifacts/v2_marks.json').write_text(json.dumps(rows,indent=2)+'\n')
