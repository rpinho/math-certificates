# Brute-force: all sublattices of 2^[n] (closure BFS), max size per allowed-size set R, vs poset_search.
import sys, itertools, random
sys.path.insert(0, sys.argv[0].rsplit('/',1)[0])
from poset_search import search
def close(F):
    F=set(F)
    while True:
        new={x|y for x in F for y in F}|{x&y for x in F for y in F}
        if new<=F: return frozenset(F)
        F|=new
def all_sublattices(n):
    U=range(1<<n); seen=set(); frontier=[close([s]) for s in U]; seen.update(frontier)
    while frontier:
        nxt=[]
        for L in frontier:
            for s in U:
                if s not in L:
                    M=close(L|{s})
                    if M not in seen: seen.add(M); nxt.append(M)
        frontier=nxt
    return seen
for n in (3,4,5):
    subs=all_sublattices(n); pc=[bin(s).count('1') for s in range(1<<n)]
    words=list(itertools.product('01',repeat=n+1))
    bad=0
    for w in words:
        for c in '01':
            R={i for i,ch in enumerate(w) if ch==c}
            best=max([len(L) for L in subs if all(pc[s] in R for s in L)],default=0)
            # poset_search max: largest t found
            m=0
            for t in range(1,best+3):
                r,_=search(n,R,t)
                if r: m=t
                else: break
            if m!=best: bad+=1; print('MISMATCH',n,''.join(w),c,best,m)
    print(f'n={n}: {len(subs)} sublattices, {len(words)} words x 2 colours, mismatches={bad}')
