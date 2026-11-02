"""Additional exact replay using Python integers and nauty canonical forms.

Independent graph completeness route: vertex augmentation through orders 1..n.
The C++ verifier remains self-contained and does not depend on nauty.
No search-generated coefficient tables are read.
"""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','RAYON_NUM_THREADS']:os.environ[key]='1'
import itertools,math,sys
from fractions import Fraction
from pathlib import Path
import pynauty

def adjacency(s,mask):
    a=[[0]*s for _ in range(s)]
    for j in range(1,s):
        for i in range(j):a[i][j]=a[j][i]=(mask>>(j*(j-1)//2+i))&1
    return a

def canonical(s,mask,t=0,ordered=False):
    a=adjacency(s,mask)
    coloring=([{i} for i in range(t)] if ordered else [set(range(t))] if t else [])
    if t<s:coloring.append(set(range(t,s)))
    coloring=[x for x in coloring if x]
    g=pynauty.Graph(s,adjacency_dict={i:[j for j in range(s) if a[i][j]] for i in range(s)},vertex_coloring=coloring)
    return pynauty.certificate(g)

def induced(a,vertices):
    value=0
    for j in range(1,len(vertices)):
        for i in range(j):value|=a[vertices[i]][vertices[j]]<<(j*(j-1)//2+i)
    return value

lines=Path(sys.argv[1]).read_text().splitlines();header=list(map(int,lines[0].split()))
n,k,D,B,bn,bd=header[:6];mode=header[6] if len(header)>6 else 0
assert mode in (0,1) and D>0 and bd>0
tokens=iter(map(int,' '.join(lines[1:]).split()));blocks=[];families={};common=1
for b in range(B):
    t,m,typ,d,rank=[next(tokens) for _ in range(5)]
    assert t+2*m==n
    flags=[next(tokens) for _ in range(d)]
    rows=[[next(tokens) for _ in range(d)] for _ in range(rank)]
    columns=list(zip(*rows))
    gram=[[sum(x*y for x,y in zip(u,v)) for v in columns] for u in columns]
    den=math.comb(n,t)*math.comb(n-t,m)*(math.factorial(t) if mode else 1)
    common=math.lcm(common,den)
    fam=families.setdefault((t,m),dict(orbits={},types=set()))
    fam['types'].add(typ)
    for i,code in enumerate(flags):
        assert (code&((1<<(t*(t-1)//2))-1))==typ
        key=canonical(t+m,code,t,bool(mode))
        assert key not in fam['orbits'];fam['orbits'][key]=(b,i)
    blocks.append((gram,den))
assert next(tokens,None) is None
for (t,m),fam in families.items():
    size=1<<((t+m)*(t+m-1)//2)
    lookup=[None]*size;rootmask=(1<<(t*(t-1)//2))-1
    for mask in range(size):
        if mode and mask&rootmask not in fam['types']:continue
        key=canonical(t+m,mask,t,bool(mode))
        assert key in fam['orbits']
        lookup[mask]=fam['orbits'][key]
    fam['lookup']=lookup
print('PASS: exact integer Gram matrices and nauty flag orbit tables.',flush=True)

# Generate every graph class from scratch, by adjoining a vertex in all ways.
classes={canonical(1,0):0}
for size in range(2,n+1):
    new={};base=(size-1)*(size-2)//2
    for mask in classes.values():
        for neighbors in range(1<<(size-1)):
            h=mask|(neighbors<<base);new.setdefault(canonical(size,h),h)
    classes=new
    print('augmentation',size,len(classes),flush=True)

graphs=[];keys=set()
for line in Path(sys.argv[2]).read_text().splitlines():
    assert ord(line[0])-63==n
    mask=0
    for pos in range(n*(n-1)//2):mask|=(((ord(line[1+pos//6])-63)>>(5-pos%6))&1)<<pos
    key=canonical(n,mask);assert key not in keys;keys.add(key);graphs.append(mask)
assert keys==set(classes)
print('PASS: graph file equals complete vertex-augmentation enumeration.',flush=True)

best=None;worst=None;targetsets=list(itertools.combinations(range(n),k))
allvertices=set(range(n));scale=common*D*D*math.comb(n,k)*bd
for idx,mask in enumerate(graphs):
    a=adjacency(n,mask)
    monochromatic=sum(induced(a,vs) in (0,(1<<(k*(k-1)//2))-1) for vs in targetsets)
    lhs=monochromatic*common*D*D*bd-bn*common*D*D*math.comb(n,k)
    for (t,m),fam in families.items():
        roots=(itertools.permutations(range(n),t) if mode else itertools.combinations(range(n),t))
        for root in roots:
            if mode and induced(a,root) not in fam['types']:continue
            other=tuple(sorted(allvertices-set(root)))
            for extension in itertools.combinations(other,m):
                remaining=tuple(v for v in other if v not in extension)
                b1,i=fam['lookup'][induced(a,root+extension)]
                b2,j=fam['lookup'][induced(a,root+remaining)]
                assert b1==b2
                gram,den=blocks[b1]
                lhs-=gram[i][j]*(common//den)*math.comb(n,k)*bd
    assert lhs>=0,(idx,lhs)
    if best is None or lhs<best:best=lhs;worst=idx
print('PASS: all coefficient inequalities by Python arbitrary-precision integers.',flush=True)
print('bound',f'{bn}/{bd}','minimum slack',f'{best}/{scale}','graph index',worst,flush=True)
