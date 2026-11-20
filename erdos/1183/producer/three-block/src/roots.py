from math import prod
from pathlib import Path
from planes import WORDS,read,save,Oracle
from three import coords,dims,packkey
from sat import dimacs,solve

def dims_key(s):return prod(x+1 for x in s),s

def solve_root(s,oracle):
    n=sum(s)
    out=Path(f'data/split{n}')/packkey(s)
    cells=coords(s)
    ids={p:i for i,p in enumerate(cells,1)}
    size=len(ids)
    free=list(s)
    if n==23 and s[2]==1:
        free[2]-=1
        ax=int(s[1]>=2)
        free[ax]-=1
    else:
        ax=0
        free[ax]-=n-21
    shape=tuple(sorted(free,reverse=True))
    if shape[2]:
        live=read(f'data/live-{packkey(shape)}.gz')
    else:
        live=read('data/planes-cache.gz')[f'{shape[0]}-{shape[1]}']
    assert live==[[],sorted(''.join(w[sum(p)] for p in coords(shape)) for w in WORDS),[]]
    rows=[]
    for offset in range(n-21):
        selectors=list(range(size+1,size+5));size+=4
        rows.append(selectors)
        for var,w in zip(selectors,WORDS):
            for p in coords(free):
                pt=list(p);pt[ax]+=offset
                cell=ids[tuple(pt)]
                rows.append([-var,cell if w[sum(p)]=='1' else -cell])
    if n==22:
        unused=s[0]-1
        low=(1<<unused)-1
        families=[]
        for w in WORDS:
            for col in (0,1):
                local=oracle.query((21,0,0),w,col,13)
                assert len(local)==12
                f=[(x&low)|((x&~low)<<1) for x in local]+[(1<<22)-1]
                families.append(f)
                image=set()
                for x in f:
                    p=[]
                    for width in s:
                        p.append((x%2**width).bit_count());x>>=width
                    image.add(ids[tuple(p)])
                literals=sorted(image)
                rows.extend([literals,[-x for x in literals]])
        save(out.with_suffix('.families.gz'),families)
    assert solve(out,dimacs(size,rows)) is None
    print('excluded',n,s,'face',shape,'clauses',len(rows),flush=True)

if __name__=='__main__':
    import sys
    n=int(sys.argv[1])
    oracle=Oracle()
    try:
        for s in sorted(dims(n,zeros=n==22),key=dims_key):
            solve_root(s,oracle)
    finally:oracle.close()
