"""Standalone certificate reader. Takes sets, edge words, DIMACS, and LRAT only."""
import argparse
import gzip
import itertools
import json
import tempfile
from collections import Counter
from functools import lru_cache
from pathlib import Path

import numpy as np


def require(test, reason):
    if not test:
        raise ValueError(reason)


def footprint(sets):
    family=frozenset(sets)
    require(len(sets)==len(family) and 14<=len(family)<=27,"family size")
    require(all(type(s) is int and 0<=s<2**23 for s in family),"coordinate outside cube")
    for x,y in itertools.combinations(family,2):
        require(x|y in family and x&y in family,"closure")
    # Ground coordinates 0..20 are A. Rows of the physical grid correspond to
    # choosing zero, one or two of the final two ground coordinates.
    return sorted({1+(s%(2**21)).bit_count()+22*(s//2**21).bit_count() for s in family})


def enum_rows(single):
    # Explicit slices of the 22-dimensional binary array represent partial
    # words: set every completion of an observed monochromatic pattern invalid.
    alive=np.ones((2,)*22,dtype=bool)
    for cells in single:
        for bit in (0,1):
            sub=[slice(None)]*22
            for x in cells:sub[x-1]=bit
            alive[tuple(sub)]=False
    return ["".join(map(str,idx)) for idx in zip(*np.where(alive))]


def enum_edges(words,pairs):
    masks=np.array([int(w,2) for w in words],dtype=np.int64)
    live=np.ones((len(words),len(words)),dtype=bool)
    @lru_cache(maxsize=None)
    def matching(pattern,bit):
        return np.flatnonzero((masks&pattern)==(pattern if bit else 0))
    for cells in pairs:
        left=sum(1<<(22-k) for k in cells if k<=22)
        right=sum(1<<(44-k) for k in cells if k>22)
        for bit in (0,1):
            live[np.ix_(matching(left,bit),matching(right,bit))]=False
    return [(words[i],words[j]) for i,j in zip(*np.where(live))]


def physical_certificate(sets_path,window_path,formula):
    windows=[tuple(line.split()) for line in window_path.read_text().splitlines()]
    counts=Counter()
    singles,pairs,triples=[],[],[]
    with tempfile.TemporaryFile(dir=formula.parent) as spool:
        def clause(literals):
            spool.write((" ".join(map(str,literals))+" 0\n").encode())
        with gzip.open(sets_path,"rt") as stream:
            for line in stream:
                width,offset,f=json.loads(line)
                require(width in range(3) and 0<=offset<=2-width,"window metadata")
                cells=footprint(f)
                require(all(offset<=(k-1)//22<=offset+width for k in cells),"misplaced family")
                clause(cells)
                clause(-k for k in cells)
                counts[width]+=1
                if offset==0:
                    (singles,pairs,triples)[width].append(cells)
        words=enum_rows(singles)
        require(enum_edges(words,pairs)==windows,"window completeness")
        paths=0
        for u,v in windows:
            for middle,w in windows:
                if middle!=v:continue
                paths+=1
                grid=u+v+w
                require(any(len({grid[k-1] for k in cells})==1 for cells in triples),
                        "uncovered triple")
        q=len(windows)
        for start in (0,1):
            begin=67+start*q
            clause(range(begin,begin+q))
            for s,(u,v) in enumerate(windows,begin):
                for k,ch in enumerate(u+v,1+22*start):
                    clause([-s,k if ch=="1" else -k])
        nclauses=2*sum(counts.values())+2*(1+44*q)
        header=f"p cnf {66+2*q} {nclauses}\n".encode()
        spool.seek(0)
        with formula.open("rb") as original:
            require(original.readline()==header,"DIMACS header")
            while chunk:=spool.read(65536):
                require(original.read(len(chunk))==chunk,"DIMACS clause bytes")
            require(original.read(1)==b"","trailing DIMACS")
    return dict(rows=len(words),windows=len(windows),compatible_triples=paths,
                explicit_families=dict(counts),clauses=nclauses)


def check_lrat(formula,certificate):
    # Cadical --plain emits addition-only LRAT using reverse unit propagation.
    # Reject every other operation rather than skipping unsupported steps.
    with formula.open() as inp:
        p,cnf,nvars,nclauses=inp.readline().split()
        require((p,cnf)==("p","cnf"),"DIMACS syntax")
        nvars,nclauses=int(nvars),int(nclauses)
        clauses=[None]
        for line in inp:
            *c,zero=map(int,line.split())
            require(zero==0 and all(1<=abs(x)<=nvars for x in c),"DIMACS literal")
            clauses.append(c)
        require(len(clauses)==1+nclauses,"DIMACS length")
    steps=0
    for line in certificate.read_text().splitlines():
        require(steps==0 or bool(clauses[-1]),"proof continues past empty clause")
        ident,*body=map(int,line.split())
        require(ident==len(clauses),"clause identifier")
        sep=body.index(0)
        c=body[:sep]
        require(body[-1]==0 and len(body)>sep+2,"expected RUP hints")
        require(all(1<=abs(x)<=nvars for x in c),"proof literal")
        forced={-x for x in c}
        require(all(-x not in forced for x in forced),"tautology")
        hints=body[sep+1:-1]
        for j,i in enumerate(hints):
            require(1<=i<ident,"hint reference")
            h=clauses[i]
            require(not any(x in forced for x in h),"satisfied hint")
            unassigned=[x for x in h if -x not in forced]
            if j+1==len(hints):require(not unassigned,"missing contradiction")
            else:
                require(len(unassigned)==1,"hint is not unit")
                forced.add(unassigned[0])
        clauses.append(c)
        steps+=1
    require(steps and clauses[-1]==[],"no empty clause")
    return steps


if __name__=="__main__":
    cli=argparse.ArgumentParser()
    cli.add_argument("--data",type=Path,default=Path("data"))
    d=cli.parse_args().data
    result=physical_certificate(d/"sets.jsonl.gz",d/"windows.txt",d/"exclusion.cnf")
    result["lrat_steps"]=check_lrat(d/"exclusion.cnf",d/"exclusion.lrat")
    print(json.dumps(result,sort_keys=True))
