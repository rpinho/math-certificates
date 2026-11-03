"""Small exact control of the physical pairing and its unequal boundaries."""
from collections import defaultdict, Counter
from itertools import permutations, combinations, product
import json

def avoids(p,pat):
    return all(tuple(1+sum(y<x for y in a) for x in a)!=pat
               for a in combinations(p,len(pat)))

def stats(cell,top):
    cell=tuple(1+sum(y<x for y in cell) for x in cell)
    leaves={x for i,x in enumerate(cell)
            if (all(y<x for y in cell[i+1:]) if top
                else all(y>x for y in cell[:i]))}
    separators=[0]+sorted(set(cell)-leaves)+[len(cell)+1]
    counts=Counter(b-a-1 for a,b in zip(separators,separators[1:]))
    return len(leaves),counts[0],counts[2],dict(counts)

checked=0
witness=None
for n in range(1,6):
    groups=defaultdict(list)
    for p in permutations(range(1,n+1)):
        if not avoids(p,(1,3,2,4)):continue
        for cut in range(n+1):
            lo=tuple(x for x in p if x<=cut)
            hi=tuple(x for x in p if x>cut)
            if not avoids(lo,(1,3,2)) or not avoids(hi,(2,1,3)):continue
            a,b=stats(hi,True),stats(lo,False)
            groups[(cut,a[:3],b[:3])].append(p)
    for (cut,a,b),members in groups.items():
        for p,q in product(members,repeat=2):
            t=n-cut
            rot=tuple(n+1-x for x in reversed(q))
            out=tuple(n+x if x>cut else x+t for x in p)+tuple(
                n+x-t if x>t else x for x in rot)
            assert sorted(out)==list(range(1,2*n+1))
            top=tuple(x for x in out if x>n)
            bottom=tuple(x for x in out if x<=n)
            assert len(top)==len(bottom)==n
            assert avoids(out,(1,3,2,4))
            assert avoids(top,(2,1,3)) and avoids(bottom,(1,3,2))
            x,y=stats(top,True),stats(bottom,False)
            for st in (x,y):
                assert st[0]==a[0]+b[0]
                assert st[1]>=a[1]+b[1]-1
                assert st[2]<=a[2]+b[2]+2
            checked+=1
            if witness is None and x[1]!=y[1]:
                witness={'n':n,'cut':cut,'sigma':p,'tau':q,'output':out,
                         'input_top_statistics':a,'input_bottom_statistics':b,
                         'output_top_statistics':x,'output_bottom_statistics':y}
print(json.dumps({'status':'PASS','pairs_checked':checked,'max_input_size':5,
                  'unequal_output_empty_strip_witness':witness},indent=2))
