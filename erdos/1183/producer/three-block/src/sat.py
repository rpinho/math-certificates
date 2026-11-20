from pathlib import Path
from itertools import product
import subprocess

SOLVER='build/cadical/build/cadical'

def dimacs(n,clauses):
    return f'p cnf {n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)

def solve(path,contents,proof=True):
    path.with_suffix('.cnf').write_text(contents)
    args=[SOLVER,'--plain','--no-binary']
    if proof: args.append('--lrat')
    args.append(str(path.with_suffix('.cnf')))
    if proof: args.append(str(path.with_suffix('.lrat')))
    result=subprocess.run(args,stdout=subprocess.PIPE,text=True)
    if result.returncode==20:return None
    assert result.returncode==10,result.stdout[-300:]
    return {x for line in result.stdout.splitlines() if line.startswith('v ')
            for x in map(int,line[2:].split()) if x>0}

def face_probe(s,ax,lower,words,oracle):
    """Choose the two child windows of a putative exception by SAT."""
    from three import coords,packkey
    from planes import rejection,save
    sh=list(s); sh[ax]-=1
    child=coords(sh); pts=coords(s)
    pos={p:i for i,p in enumerate(pts)}
    left=[pos[p] for p in child]
    right=[pos[tuple(v+(i==ax) for i,v in enumerate(p))] for p in child]
    cuts=[]; options=[]
    n=3
    clauses=[[1,2,3]]
    good={''.join(w[sum(p)] for p in pts) for w in words}
    for z in range(3):
        candidates=sorted(set(lower[z])|set(lower[z+1]))
        lids=list(range(n+1,n+1+len(candidates)));n+=len(lids)
        rids=list(range(n+1,n+1+len(candidates)));n+=len(rids)
        clauses.extend([[-(z+1)]+lids,[-(z+1)]+rids])
        for i,u in zip(lids,candidates):
            for j,v in zip(rids,candidates):
                bad=(u not in lower[z+(v[-1]=='0')] or v not in lower[z+(u[0]=='0')])
                if not bad:
                    buf=['?']*len(pts)
                    for k,b in zip(left,u):buf[k]=b
                    for k,b in zip(right,v):
                        if buf[k] not in ('?',b):
                            bad=True;break
                        buf[k]=b
                    w=''.join(buf)
                    if not bad and z==1 and w in good:bad=True
                if bad:clauses.append([-i,-j])
                else:options.append((z,i,j,w))
    path=Path('data/face')/packkey(s)
    while True:
        model=solve(path,dimacs(n,clauses))
        if model is None:break
        z,i,j,w=next(row for row in options if row[0]+1 in model and row[1] in model and row[2] in model)
        f=rejection(oracle,s,w,z)
        if f is None:
            save(path.with_suffix('.survivor.gz'),[z,w])
            raise RuntimeError(f'confirmed exceptional survivor on {s}, context {z}')
        cuts.append([z,w,f])
        clauses.append([-i,-j])
    save(path.with_suffix('.cuts.gz'),cuts)
    print('SAT face',s,'exceptional models checked',len(cuts),'UNSAT',flush=True)
