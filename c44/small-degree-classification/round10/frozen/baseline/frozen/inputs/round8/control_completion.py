"""Independent finite control using direct character sums and exact fractions."""
from fractions import Fraction as Q
from itertools import product
import json,pathlib,sys
root=pathlib.Path(sys.argv[1]).resolve();caps={1:Q(1,2),2:Q(1),3:Q(5,4),4:Q(11,8)}
counts={'Boolean_tables':0,'Boolean_eligible':0,'retained_cases':0,'ternary_tables':0,'active_edges':0}
def spectral_degree(vals,n):
 coeff={}
 for s in range(1<<n):
  v=sum((-y if (s&x).bit_count()%2 else y) for x,y in enumerate(vals))
  if v:coeff[s]=v
 return max([0]+[s.bit_count() for s in coeff]),coeff
for n in range(4):
 N=1<<n
 for vals in product((-1,1),repeat=N):
  counts['Boolean_tables']+=1;d,coeff=spectral_degree(vals,n)
  if d<3:continue
  local={j:max([0]+[s.bit_count() for s in coeff if s>>j&1]) for j in range(n)}
  rel={j for j in range(n) if local[j]}
  if any(local[j]!=d for j in rel):continue
  counts['Boolean_eligible']+=1;m=1<<(d-1);c=caps[d-1]
  b=max([Q(1,2)]+[Q(1,4)+Q(1,1<<(t+1))+caps[t]/2 for t in range(1,d-1)])
  for i in rel:
   A=[(vals[x&~(1<<i)]-vals[x|(1<<i)])//2 for x in range(N)]
   p=Q(sum(bool(v) for v in A),N);lam=m*p
   H=set()
   for s in coeff:
    if s>>i&1:H.update(j for j in range(n) if j!=i and s>>j&1)
   assert len(rel)<=(1<<d)*c+len(H)+1-2*c*lam
   for j in H:
    e=Q(sum((A[x]-A[x^(1<<j)])**2 for x in range(N)),4*N)
    if lam<=1 or e!=Q(1,1<<d):continue
    counts['retained_cases']+=1
    assert any(A[x] and A[x^(1<<j)] for x in range(N))
    assert all(abs(A[x]-A[x^(1<<j)])<=1 for x in range(N))
    K=H-{j}
    assert all(any(s>>v&1 for v in K) for s in coeff if s.bit_count()==d)
    bound=(1<<d)*c+len(H)-2*c*lam+4*(b-(c+Q(1,2))/2)
    assert len(rel)<=bound
for n in range(4):
 N=1<<n
 for vals in product((-1,0,1),repeat=N):
  counts['ternary_tables']+=1
  # Integer bit interpolation independently determines the real degree.
  a=list(vals)
  for j in range(n):
   for x in range(N):
    if x>>j&1:a[x]-=a[x^(1<<j)]
  k=max([0]+[x.bit_count() for x,v in enumerate(a) if v])
  if k<1:continue
  p=Q(sum(bool(v) for v in vals),N)
  if p<=Q(1,1<<k):continue
  for j in range(n):
   e=Q(sum((vals[x]-vals[x^(1<<j)])**2 for x in range(N)),4*N)
   if e!=Q(1,1<<(k+1)):continue
   assert any(vals[x] and vals[x^(1<<j)] for x in range(N))
   counts['active_edges']+=1
assert counts['retained_cases']>0 and counts['active_edges']==2432
receipts=root.parent/'receipts';receipts.mkdir(exist_ok=True)
(receipts/'completion_controls_python.json').write_text(json.dumps({'status':'PASS','scope':'finite corroboration only',**counts},indent=2)+'\n')
print(json.dumps(counts),flush=True)
