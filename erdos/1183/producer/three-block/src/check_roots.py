"""Derive each root DIMACS directly from verified terminal tables and physical sets."""
from collections import Counter
from itertools import product
from math import prod
from pathlib import Path
from check import DATA,key,read,positions,index,pack,string,family_image,cnf_bytes,replay

def root(s,cache,directory=DATA):
    n=sum(s)
    dst=directory/f'split{n}'/key(s)
    shortened=list(s)
    if n==23 and s[-1]==1:
        shortened[-1]=0
        along=0 if s[1]==1 else 1
        shortened[along]-=1
    else:
        along=0
        shortened[0]-=n-21
    face=tuple(sorted(shortened,reverse=True))
    catalog=cache[face]
    assert set(catalog.values())=={2}
    ranks=[]
    for table in catalog:
        byrank={}
        for pt in positions(face):
            bit=(table>>index(pt,face))&1
            assert byrank.setdefault(sum(pt),bit)==bit
        ranks.append(tuple(byrank[i] for i in range(22)))
    ranks.sort()
    assert len(ranks)==4
    size=prod(x+1 for x in s)
    rows=[]
    shape=tuple(shortened)
    for offset in range(n-21):
        choice=list(range(size+1,size+5))
        size+=4
        rows.append(choice)
        # Scan the actual cube cells and restrict to the translated window.
        for sel,word in zip(choice,ranks):
            for pt in positions(s):
                local=list(pt);local[along]-=offset
                if all(0<=k<=bound for k,bound in zip(local,shape)):
                    lit=index(pt,s)+1
                    rows.append([-sel,lit if word[sum(local)] else -lit])
    if n==23:
        differences=Counter(sum(x!=y for x,y in zip(u[1:],v[:-1])) for u in ranks for v in ranks)
        assert differences=={10:8,11:8}
        assert shortened[along]>=1
    else:
        families=read(dst.with_suffix('.families.gz'))
        assert len(families)==8
        for j,f in enumerate(families):
            footprint,_=family_image(f,s,0,ambient=22,target=13)
            # Each also certifies a 12-family of the indicated rank colour in the bottom facet.
            full=(1<<22)-1
            freebit=1<<(s[0]-1)
            assert full in f and len(f)==13
            assert all(not x&freebit and ranks[j//2][x.bit_count()]==j%2 for x in f if x!=full)
            cellids=[i+1 for i in range(prod(x+1 for x in s)) if footprint>>i&1]
            rows.append(cellids)
            rows.append([-v for v in cellids])
    assert dst.with_suffix('.cnf').read_bytes()==cnf_bytes(size,rows),'split DIMACS regeneration'
    return face

if __name__=='__main__':
    cache=replay()
    for n in (23,22):
        count=0
        for a in range(n,-1,-1):
            for b in range(min(a,n-a),-1,-1):
                c=n-a-b
                if b>=c>=(1 if n==23 else 0):
                    root((a,b,c),cache);count+=1
        assert count==(44 if n==23 else 52)
        print('all root DIMACS agree',n,count)
