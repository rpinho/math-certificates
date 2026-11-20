"""Classify a face, growing through overlapping windows from its two-block base."""
import sys
from collections import defaultdict
from functools import lru_cache
from math import prod
from pathlib import Path
from planes import WORDS, Oracle, read, save, rejection, rankmap

def dims(n,zeros=False):
    return [(n-b-c,b,c) for c in range(0 if zeros else 1,n//3+1)
            for b in range(c,(n-c)//2+1)]

def axis(s):
    a,b,c=s
    if c>=2: return 2
    if b>=2: return 1
    if a>=2: return 0
    return 2

def coords(s):
    a,b,c=s
    return [(x,y,k) for k in range(c+1) for y in range(b+1) for x in range(a+1)]

def packkey(s):
    return '-'.join(map(str,s))

def routes(s,t):
    pts=coords(s)
    return [[i for i,p in enumerate(pts) if p[t]==j] for j in range(s[t]+1)]

def candidates(s,lower,z,ax):
    child=list(s); child[ax]-=1
    blocks=routes(child,ax)
    def permute(w):
        return ''.join(w[i] for row in blocks for i in row)
    child_by_end={}
    stride=len(blocks[0])
    for dz in (0,1):
        child_by_end[dz]=[permute(w) for w in sorted(lower[z+dz])]
    inv=[i for row in routes(s,ax) for i in row]
    reorder=sorted(range(len(inv)),key=inv.__getitem__)
    for first in '01':
        for last in '01':
            rights=defaultdict(list)
            for v in child_by_end[first=='0']:
                if v[-1]==last: rights[v[:-stride]].append(v[-stride:])
            for u in child_by_end[last=='0']:
                if u[0]!=first: continue
                for tail in rights.get(u[stride:],()):
                    word=u+tail
                    yield ''.join(word[i] for i in reorder)

def slice_tests(s):
    result=[]
    pts=coords(s)
    for ax in range(3):
        # Other coordinates keep their memory order and descending sizes.
        kept=tuple(v for i,v in enumerate(s) if i!=ax)
        for offset,plane in enumerate(routes(s,ax)):
            chain=[i for i,p in enumerate(pts)
                   if (p[ax]<offset and all(p[j]==0 for j in range(3) if j!=ax))
                   or (p[ax]>offset and all(p[j]==s[j] for j in range(3) if j!=ax))]
            result.append((kept,plane,chain))
    return result

def classify(targets):
    catalog=read('data/planes-cache.gz')
    planes={tuple(map(int,k.split('-'))):[set(row) for row in v] for k,v in catalog.items()}
    oracle=Oracle()
    @lru_cache(maxsize=None)
    def work(s):
        if s[2]==0:return planes[s[:2]]
        key=packkey(s)
        ax=axis(s)
        child=list(s); child[ax]-=1
        lower=work(tuple(child))
        if sum(s)==21:
            from sat import face_probe
            face_probe(s,ax,lower,WORDS,oracle)
        filters=slice_tests(s)
        bycontext=[]; records=[]
        joined=pruned=0
        for z in range(24-sum(s)):
            live=[]; families=[]
            for w in candidates(s,lower,z,ax):
                joined+=1
                for shape,indices,outside in filters:
                    budget=z+sum(w[i]=='0' for i in outside)
                    if ''.join(w[i] for i in indices) not in planes[shape][budget]:
                        pruned+=1
                        break
                else:
                    f=rejection(oracle,s,w,z)
                    if f is not None: families.append(f)
                    else: live.append(w)
            bycontext.append(sorted(live))
            records.append(families)
        save(Path(f'data/t-{key}.gz'),records)
        print(key,'joins',joined,'plane rejects',pruned,'witnesses',sum(map(len,records)),
              'surviving contexts',sum(map(len,bycontext)),flush=True)
        if sum(s)==21:
            expected=sorted(''.join(w[r] for r in rankmap(s)) for w in WORDS)
            print('TERMINAL',s,'exact four?',bycontext==[[],expected,[]],flush=True)
            save(Path(f'data/live-{key}.gz'),bycontext)
        return bycontext
    try:
        for s in targets:work(s)
    finally:oracle.close()

if __name__=='__main__':
    targets=sorted(dims(21),key=lambda s:(prod(v+1 for v in s),s))
    if len(sys.argv)>1:targets=[tuple(map(int,x.split('-'))) for x in sys.argv[1:]]
    classify(targets)
