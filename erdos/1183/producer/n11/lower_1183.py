#!/usr/bin/env python3
"""Own certificate construction from published lattice data (not research code)."""
import itertools,json,pathlib
n=11;raw=[]
for line in pathlib.Path('sources/1183_certs11.txt').read_text().splitlines():
 if line.startswith('#') or not line.strip():continue
 vals=list(map(int,line.split()));assert vals[0]==-1;fam=vals[1:];S=set(fam)
 assert len(S)==len(fam) and all(0<=s<2**n for s in S)
 assert all(s|t in S and s&t in S for s in S for t in S)
 raw.append(fam)
shapes=[]
for fam in raw:
 bottom=fam[0];top=fam[0]
 for s in fam:bottom&=s;top|=s
 coords=[i for i in range(n) if ((top^bottom)>>i)&1];d=len(coords)
 norm=[sum(((s>>i)&1)<<j for j,i in enumerate(coords)) for s in fam]
 for reflect in [False,True]:
  base=[s^((1<<d)-1) for s in norm] if reflect else norm
  for shift in range(n-d+1):shapes.append([(s<<shift)|((1<<shift)-1) for s in base])
certs=[]
# A seven-member chain rules out every rank word with at least seven of one colour.
for ranks in itertools.combinations(range(n+1),7):certs.append([(1<<r)-1 for r in ranks])
# Treat balanced words with rank zero fixed to 1, up to swapping the colours.
for ones in itertools.combinations(range(n+1),6):
 if 0 not in ones:continue
 g=[int(i in ones) for i in range(n+1)];found=False
 for fam in shapes:
  c=g[fam[0].bit_count()]
  if any(g[s.bit_count()]!=c for s in fam):continue
  b=fam[0];t=fam[0]
  for s in fam:b&=s;t|=s
  # Add a chain below the meet and above the join, at matching-colour ranks.
  below=0;extra=[]
  for i in [i for i in range(n) if (b>>i)&1]:
   if g[below.bit_count()]==c:extra.append(below)
   below|=1<<i
  above=t
  for i in [i for i in range(n) if not (t>>i)&1]:
   above|=1<<i
   if g[above.bit_count()]==c:extra.append(above)
  witness=sorted(set(fam+extra))
  if len(witness)>=7:
   certs.append(witness);found=True;break
 assert found,g
pathlib.Path('certificates/1183_lower7_families.json').write_text(json.dumps({'n':n,'target':7,'credit':'Normalized, reflected and translated from creelie/Erdos-1183 checks/window20/certs_11.txt; original source credited in REPORT.md.','families':certs},indent=2)+'\n')
clauses=[[1]]
for fam in certs:
 ranks=sorted({s.bit_count()+1 for s in fam});clauses.extend([ranks,[-x for x in ranks]])
with open('data/1183_lower7_rank.cnf','w') as f:
 f.write(f'p cnf {n+1} {len(clauses)}\n')
 for cl in clauses:f.write(' '.join(map(str,cl))+' 0\n')
print(json.dumps({'families':len(certs),'variables':n+1,'clauses':len(clauses)}))
