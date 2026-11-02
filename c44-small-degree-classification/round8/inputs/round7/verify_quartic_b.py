"""Fresh exhaustive verification from tensor truth tables and set-based search.
No imports from generator, search, trace checker, or scalar verifiers.
"""
from itertools import combinations,product
import gzip,json,pathlib,sys,time
R=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else __file__).resolve()
if R.is_file():R=R.parent
# Enumerate disjoint tensor factors of degree costs 1,1,2,3. A one-point
# indicator uses one coordinate; an m-block uses degree m-1, m=2,3,4.
factors=[(1,(0,)),(1,(0,1)),(2,(0,1,2)),(3,(0,1,2,3))]
base=set()

def factor_truth(block,signs):
 vals=[signs[j] for j in block]
 if len(block)==1:return int(vals[0]==1)
 if all(x==1 for x in vals):return 1
 if all(x==-1 for x in vals):return -1 if len(block)%2==0 else 1
 return 0

def tensors(chosen,available,cost,lower):
 if cost==3:
  coords=sorted({x for block in chosen for x in block});h=len(coords)
  # Direct character sums, not the parity-mask formula in the search.
  truth=[]
  for bits in range(1<<h):
   signs={coords[i]:(-1 if bits>>i&1 else 1) for i in range(h)}
   val=1
   for block in chosen:val*=factor_truth(block,signs)
   truth.append(val)
  assert sum(bool(v) for v in truth)==1<<(h-3)
  supp=[]
  for mask in range(1<<h):
   coeff=sum(v*(-1 if (bits&mask).bit_count()%2 else 1) for bits,v in enumerate(truth))
   if coeff:
    assert abs(coeff)*8==1<<h
    actual=1
    for t,x in enumerate(coords):
     if mask>>t&1:actual|=1<<x
    supp.append(actual)
  assert len(supp)==8
  base.add(tuple(sorted(supp)));return
 for size in (1,2,3,4):
  charge=1 if size==1 else size-1
  if cost+charge>3:continue
  for block in combinations(available,size):
   # A fixed ordering of factors avoids duplicate tensor decompositions.
   key=(size,block)
   if key<lower:continue
   tensors(chosen+[block],[x for x in available if x not in block],cost+charge,key)
t0=time.monotonic()
tensors([],list(range(1,11)),0,(0,()))
assert len(base)==11880
with gzip.open(R/'quartic_certificate.json.gz','rt') as f:packet=json.load(f)
assert base=={tuple(sorted(x)) for x in packet['patterns0']}
print('independent tensor templates',len(base),time.monotonic()-t0,flush=True)

patterns=[];inc=[]
for j in range(11):
 rows=[]
 for row in base:
  out=[]
  for mask in row:
   a=bool(mask&1);b=bool(mask&(1<<j))
   if a!=b:mask^=1|(1<<j)
   out.append(mask)
  rows.append(frozenset(out))
 rows.sort(key=lambda s:tuple(sorted(s)));patterns.append(rows)
 by={}
 for z,row in enumerate(rows):
  for term in row:by.setdefault(term,[]).append(z)
 inc.append(by)
start=frozenset(1|(1<<a)|(1<<b)|(1<<c) for a in (1,2) for b in (3,4) for c in (5,6))
results=[];nodecount=0
orbits=set()
for six in combinations(range(1,11),6):
 cs=tuple(sorted(sum(j in six for j in pair) for pair in [(1,2),(3,4),(5,6)]))
 b=sum(j>=7 for j in six);orbits.add((cs,b))
expected=sorted(orbits)
assert len(expected)==8 and len(packet['cases'])==8
for ci,(cs,b) in enumerate(expected):
 case=packet['cases'][ci]
 g=[0]+[1+2*i+t for i,a in enumerate(cs) for t in range(a)]+list(range(7,7+b))
 assert case['good']==g and case['pair_good_counts']==list(cs) and case['outside_good']==b
 bad=set(range(11))-set(g);found=set();local=0
 def visit(e,at):
  global local,nodecount
  local+=1;nodecount+=1
  if len(e)>24 or sum(4-t.bit_count() for t in e)>8:return
  rem=24-len(e)
  # Different pruning from A: each absent coordinate alone needs 8 units.
  if rem<8 and any(not any(t>>j&1 for t in e) for j in bad):return
  if at==len(g):
   deficits=[max(0,8-sum(bool(t>>j&1) for t in e)) for j in bad]
   if max(deficits,default=0)>rem or sum(deficits)>4*rem:return
   absent=[j for j in bad if all(not(t>>j&1) for t in e)]
   assert rem==8 and len(absent)>=2,(ci,e,rem,absent)
   found.add(tuple(sorted(e)));return
  j=g[at];required={t for t in e if t>>j&1}
  pool=min((inc[j].get(t,[]) for t in required),key=len) if required else range(11880)
  done=sum(1<<v for v in g[:at])
  for z in pool:
   p=patterns[j][z]
   if not required<=p:continue
   if any(t&done and t not in e for t in p):continue
   visit(e|p,at+1)
 visit(start,1)
 assert found=={tuple(x['terms']) for x in packet['models'] if x['case']==ci}
 results.append({'case':ci,'nodes':local,'models':len(found)})
 print(results[-1],flush=True)
assert sum(x['models'] for x in results)==9
out={'status':'PASS','checker':'quartic B: direct tensor character sums, fixed-order exhaustive completion','templates':len(base),'nodes':nodecount,'cases':results,'seconds':time.monotonic()-t0,'controls_upper':10}
outdir=R.parent/'receipts' if R.name=='frozen' else R/'receipts';outdir.mkdir(exist_ok=True)
(outdir/'quartic_b.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out),flush=True)
