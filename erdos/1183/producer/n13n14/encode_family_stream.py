#!/usr/bin/env python3
"""Same round-2 direct membership encoding, streaming rather than retaining clauses.
Used only after the unchanged round-2 writer hit the n=14 memory guard.
"""
import argparse,json,pathlib,math
p=argparse.ArgumentParser();p.add_argument('ranks');p.add_argument('color',type=int);p.add_argument('target',type=int);p.add_argument('out');p.add_argument('--union-only',action='store_true');a=p.parse_args()
g=list(map(int,a.ranks));n=len(g)-1;sets=[s for s in range(1<<n) if g[s.bit_count()]==a.color];Y={s:i+1 for i,s in enumerate(sets)};N=len(sets)
rs=[r for r in range(n+1) if g[r]==a.color]
comparable=sum(math.comb(n,s)*math.comb(s,r) for r in rs for s in rs if r<s)
closure_count=(N*(N-1)//2-comparable)*(1 if a.union_only else 2)
A={};nv=N
for i in range(1,N+1):
 for j in range(1,min(i,a.target)+1):nv+=1;A[i,j]=nv
counter_count=sum(2*min(i,a.target)-1 for i in range(1,N+1))+1
count=0
with open(a.out,'w') as f:
 f.write(f'p cnf {nv} {closure_count+counter_count}\n')
 def emit(cl):
  global count
  f.write(' '.join(map(str,cl))+' 0\n');count+=1
 for i,s in enumerate(sets):
  for t in sets[i+1:]:
   if s&t in [s,t]:continue
   for u in ([s|t] if a.union_only else [s|t,s&t]):emit([-Y[s],-Y[t]]+([Y[u]] if u in Y else []))
 assert count==closure_count
 for (i,j),v in A.items():
  b=A.get((i-1,j));c=A.get((i-1,j-1));yi=i
  emit([-v]+([b] if b else [])+[yi])
  if j>1:emit([-v]+([b] if b else [])+([c] if c else []))
 emit([A[N,a.target]] if N>=a.target else [])
 assert count==closure_count+counter_count
meta={'ranks':a.ranks,'n':n,'color':a.color,'target':a.target,'union_only':a.union_only,'members':sets,'variables':nv,'clauses':count,'closure_clauses':closure_count}
pathlib.Path(a.out+'.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps({k:v for k,v in meta.items() if k!='members'}))
