#!/usr/bin/env python3
"""Closed monochromatic family in a fixed rank colouring: direct membership CNF."""
import argparse,json,pathlib
p=argparse.ArgumentParser();p.add_argument('ranks');p.add_argument('color',type=int);p.add_argument('target',type=int);p.add_argument('out');p.add_argument('--union-only',action='store_true');a=p.parse_args()
g=list(map(int,a.ranks));n=len(g)-1;sets=[s for s in range(1<<n) if g[s.bit_count()]==a.color];Y={s:i+1 for i,s in enumerate(sets)};nv=len(sets);clauses=[]
# Tautologies are omitted; equal binary conflicts from union/intersection retained.
for i,s in enumerate(sets):
 for t in sets[i+1:]:
  if s&t in [s,t]:continue
  for u in ([s|t] if a.union_only else [s|t,s&t]):
   clauses.append([-Y[s],-Y[t]]+([Y[u]] if u in Y else []))
closure_count=len(clauses)
# Backwards sequential counter: A(i,j) => at least j of first i members selected.
A={}
for i in range(1,len(sets)+1):
 for j in range(1,min(i,a.target)+1):nv+=1;A[i,j]=nv
for (i,j),v in A.items():
 b=A.get((i-1,j));c=A.get((i-1,j-1));yi=i
 clauses.append([-v]+([b] if b else [])+[yi])
 if j>1:clauses.append([-v]+([b] if b else [])+([c] if c else []))
clauses.append([A[len(sets),a.target]] if len(sets)>=a.target else [])
with open(a.out,'w') as f:
 f.write(f'p cnf {nv} {len(clauses)}\n')
 for cl in clauses:f.write(' '.join(map(str,cl))+' 0\n')
meta={'ranks':a.ranks,'n':n,'color':a.color,'target':a.target,'union_only':a.union_only,'members':sets,'variables':nv,'clauses':len(clauses),'closure_clauses':closure_count}
pathlib.Path(a.out+'.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps({k:v for k,v in meta.items() if k!='members'}))
