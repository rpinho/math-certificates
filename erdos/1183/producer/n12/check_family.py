#!/usr/bin/env python3
"""Separately written by the same agent; no encoder imports.
Checks SAT families by original set operations, and checks complete CNF semantics.
"""
import argparse,pathlib,itertools,collections,json
p=argparse.ArgumentParser();p.add_argument('cnf');p.add_argument('--model');a=p.parse_args()
m=json.loads(pathlib.Path(a.cnf+'.json').read_text());n=m['n'];target=m['target'];g=m['ranks'];color=m['color']
# Build subsets as actual frozensets rather than copying the encoder's operations.
universe=range(n);subsets=[frozenset(i for i in universe if (s>>i)&1) for s in range(2**n)];allowed=[s for s in subsets if int(g[len(s)])==color];v={s:i+1 for i,s in enumerate(allowed)}
assert m['members']==[sum(2**i for i in s) for s in allowed]
if a.model:
 true={int(z) for line in pathlib.Path(a.model).read_text().splitlines() if line.startswith('v ') for z in line[2:].split() if int(z)>0}
 family=[s for s,z in v.items() if z in true];f=set(family)
 assert len(family)>=target
 for s,t in itertools.product(family,repeat=2):
  assert s|t in f
  if not m['union_only']:assert s&t in f
 print(json.dumps({'result':'VALID FAMILY','size':len(family),'color':color,'sets':[sorted(s) for s in family]}));raise SystemExit
clauses=[]
with open(a.cnf) as f:
 for line in f:
  if line.startswith('p '):_,_,nv,nc=line.split();nv=int(nv);nc=int(nc)
  elif line.strip() and not line.startswith('c'):clauses.append(tuple(sorted(map(int,line.split()[:-1]))))
assert len(clauses)==nc
have=collections.Counter(clauses);expected=collections.Counter()
for s,t in itertools.combinations(allowed,2):
 if s<=t or t<=s:continue
 ops=[s|t] if m['union_only'] else [s|t,s&t]
 for result in ops:expected[tuple(sorted([-v[s],-v[t]]+([v[result]] if result in v else [])))]+=1
# Counter nodes are independently numbered by row lengths in the public spec.
N=len(allowed);number=N;node={}
for prefix in range(1,N+1):
 for count in range(1,min(prefix,target)+1):number+=1;node[prefix,count]=number
for (i,j),q in node.items():
 prev=node.get((i-1,j),0);less=node.get((i-1,j-1),0)
 expected[tuple(sorted([-q]+([prev] if prev else [])+[i]))]+=1
 if j!=1:expected[tuple(sorted([-q]+([prev] if prev else [])+([less] if less else [])))]+=1
expected[(node[N,target],) if N>=target else ()]+=1
assert have==expected,('clause mismatch',have-expected,expected-have)
assert nv==number
# Exhaustively check the local counter equivalence q => b OR (x AND c).
# Disjunction distributes into the two clauses used above; j=1 has c=True.
for b,x,c,q in itertools.product([False,True],repeat=4):
 assert ((not q) or b or (x and c))==(((not q) or b or x) and ((not q) or b or c))
print(json.dumps({'result':'CNF EXACT','ranks':g,'color':color,'target':target,'variables':nv,'clauses':nc,'symmetry_breaking':'none','argument':'closure of selected sets plus backwards sequential at-least counter'}))
