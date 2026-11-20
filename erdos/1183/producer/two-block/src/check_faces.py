"""Standalone induction using integer grids and masks of possible budgets.

Only input certificates: explicit packed 23-set families, root CNF and LRAT.
No search/producer import. The generic RUP reader is shared between replays.
"""
import gzip
import itertools
import json
from collections import defaultdict,Counter
from pathlib import Path
import numpy as np
from replay import check_lrat,require

def local_case(a,b,f,z):
    n=a+b
    fam=set(f)
    require(14<=len(f)<=27 and len(fam)==len(f),"face family size")
    require(all(type(s) is int and 0<=s<2**23 for s in fam),"face mask range")
    for s,t in itertools.combinations(fam,2):
        require(s&t in fam and s|t in fam,"face family closure")
    cols=set()
    fixed=set()
    for s in fam:
        if s>>n:
            k=s.bit_length()
            require(s==(1<<k)-1,"member outside canonical extension chain")
            fixed.add(int(k>n+z))
        else:
            cols.add((s&((1<<a)-1)).bit_count()+(a+1)*(s>>a).bit_count())
    require(len(fixed)<=1,"two exterior colours")
    return cols,fixed or {0,1}

def all_joins(a,b,child):
    remaining=23-a-b
    domain=(1<<(remaining+1))-1
    if a+b==0:return {0:domain,1:domain}
    stride=a+1 if b else 1
    count=(a+1)*(b+1)
    shared=(1<<(count-2*stride))-1
    by_overlap=defaultdict(list)
    for right in child:
        by_overlap[right&shared].append(right)
    result={}
    for left,possible in child.items():
        for right in by_overlap[left>>stride]:
            whole=left | (right<<stride)
            top_zero=not (whole>>(count-1)&1)
            bottom_zero=not whole&1
            options=domain & (possible>>top_zero) & (child[right]>>bottom_zero)
            if options:result[whole]=options
    return result

def replay_faces(file,summary=False):
    source=gzip.open(file,"rt")
    proven={}
    count=Counter()
    schedule=[(a,0) for a in range(22)]
    schedule += [(a,b) for a in range(12,21) for b in range(1,22-a)]
    for a,b in schedule:
        t=23-a-b
        child=proven.get((a,b-1) if b else (a-1,0))
        candidates=all_joins(a,b,child)
        live=defaultdict(int)
        for z in range(t+1):
            ra,rb,rz,examples=json.loads(next(source))
            require((ra,rb,rz)==(a,b,z),"missing face budget")
            candidates_z=[w for w,h in candidates.items() if h>>z&1]
            count["joined"]+=len(candidates_z)
            cells=(a+1)*(b+1)
            # Pack the bits down each column. A single AND now filters every
            # candidate word matching one side of a physical witness.
            colmask=[]
            for j in range(cells):
                bits=np.fromiter((w>>j&1 for w in candidates_z),dtype=np.uint8,count=len(candidates_z))
                colmask.append(int.from_bytes(np.packbits(bits,bitorder="little").tobytes(),"little"))
            domain=(1<<len(candidates_z))-1
            kept=domain
            for f in examples:
                columns,colours=local_case(a,b,f,z)
                for c in colours:
                    hit=domain
                    for j in columns:hit &= colmask[j] if c else ~colmask[j]
                    kept &= ~hit
                count["families"]+=1
            for i,w in enumerate(candidates_z):
                if kept>>i&1:live[w] |= 1<<z
            count["surviving_contexts"]+=kept.bit_count()
            count["budget_cases"]+=1
        proven[a,b]=dict(live)
        count["shapes"]+=1
        if summary and a+b==21:
            print("face",a,b,"tables",len(live),"budget masks",sorted(set(live.values())),flush=True)
    require(source.readline()=="","extra certificate record")
    source.close()
    return {s:v for s,v in proven.items() if sum(s)==21},dict(count)

def check_root(terminal,file):
    next_id=13
    out=[" ".join(str(i) for i in range(1,13))+" 0\n"]
    path_count=0
    rankwords=set()
    for branch in range(1,13):
        b=branch-1
        a=23-b
        origin=next_id
        next_id+=(a+1)*(b+1)
        dx,dy=(1,0) if b<3 else (0,1)
        u,v=a-2*dx,b-2*dy
        words=sorted(format(x,f"0{(u+1)*(v+1)}b")[::-1] for x in terminal[u,v])
        # Directly check if TWO candidate windows agree on their shared cells.
        step=1 if dx else u+1
        for w in words:
            fullrank={}
            for j in range(v+1):
                for i in range(u+1):
                    h=w[j*(u+1)+i]
                    require(fullrank.setdefault(i+j,h)==h,"terminal face not rank")
            rankwords.add("".join(fullrank[k] for k in range(22)))
            for other in words:
                agree=all(w[j*(u+1)+i]==other[j*(u+1)+i-step]
                          for j in range(dy,v+1) for i in range(dx,u+1))
                path_count+=agree
        for off in (0,1):
            ids=list(range(next_id,next_id+len(words)))
            next_id+=len(ids)
            out.append(" ".join(map(str,[-branch]+ids))+" 0\n")
            for s,w in zip(ids,words):
                for k,symbol in enumerate(w):
                    y,x=divmod(k,u+1)
                    ix=origin+(y+off*dy)*(a+1)+x+off*dx
                    out.append(f"{-s} {ix if symbol=='1' else -ix} 0\n")
    require(path_count==0,"compatible top-level windows")
    raw=f"p cnf {next_id-1} {len(out)}\n"+"".join(out)
    require(file.read_bytes()==raw.encode(),"all-splits DIMACS bytes")
    return sorted(rankwords),len(out)

if __name__=="__main__":
    d=Path("data")
    terminal,stats=replay_faces(d/"faces.jsonl.gz",summary=True)
    rankwords,stats["clauses"]=check_root(terminal,d/"all-splits.cnf")
    stats["lrat_steps"]=check_lrat(d/"all-splits.cnf",d/"all-splits.lrat")
    print("21-dimensional rank words",rankwords)
    print(json.dumps(stats,sort_keys=True))
