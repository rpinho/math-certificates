"""Exact proof-trace checker; imports no search or second verifier code.
Completeness of minimum-support templates is a stated published premise.
The second verifier independently constructs every template by truth tables.
"""
import gzip,json,pathlib,sys
R=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else __file__).resolve()
if R.is_file():R=R.parent
with gzip.open(R/'quartic_certificate.json.gz','rt') as f:C=json.load(f)
assert C['schema']=='quartic-ternary-second-weight-controls-v1'
assert (C['n'],C['degree'],C['denominator'],C['squared_numerator_norm'],C['good_count'])==(11,4,16,24,7)
monomials=[s for s in range(2048) if s.bit_count()<=4];position={s:i for i,s in enumerate(monomials)}
V=[sum(1<<i for i,s in enumerate(monomials) if s&(1<<j)) for j in range(11)]
P=[];lookups=[]
for j in range(11):
 rows=[]
 for row in C['patterns0']:
  out=[]
  for s in row:
   if bool(s&1)!=bool(s&(1<<j)):s^=1|(1<<j)
   out.append(s)
  assert len(set(out))==8 and all(s&(1<<j) and s.bit_count()<=4 for s in out)
  intersection=2047
  for s in out:intersection &=s
  assert intersection==1<<j
  rows.append(sum(1<<position[s] for s in out))
 assert len(rows)==11880 and len(set(rows))==11880
 rows=sorted(rows);P.append(rows)
 lookup={}
 for i,p in enumerate(rows):
  while p:
   b=p&-p;p-=b;lookup.setdefault(b,[]).append(i)
 lookups.append(lookup)

def unpack(e):return [s for i,s in enumerate(monomials) if e>>i&1]
E0=sum(1<<position[1|(1<<a)|(1<<b)|(1<<c)] for a in (1,2) for b in (3,4) for c in (5,6))
expected=[]
for a in range(3):
 for b in range(a,3):
  for c in range(b,3):
   out=6-a-b-c
   if 0<=out<=4:expected.append(([a,b,c],out))
assert len(expected)==8 and len(C['cases'])==8
models=[];visits=0
for ci,(case,signature) in enumerate(zip(C['cases'],expected)):
 assert (case['pair_good_counts'],case['outside_good'])==signature
 good=[0]+[1+2*i+t for i,a in enumerate(signature[0]) for t in range(a)]+list(range(7,7+signature[1]))
 assert good==case['good'] and len(good)==7
 bad=[j for j in range(11) if j not in good];found=set()
 def valid(j,e,done):
  req=e&V[j];keys=[];bits=req
  while bits:
   bit=bits&-bits;bits-=bit;keys.append(bit)
  pool=min((lookups[j].get(b,[]) for b in keys),key=len) if keys else range(11880)
  processed=0
  for q in done:processed|=V[q]
  return [z for z in pool if P[j][z]&req==req and not(P[j][z]&processed&~e) and (P[j][z]|e).bit_count()<=24]
 def check(node,e,done):
  global visits
  visits+=1;kind=node[0];ss=unpack(e);rem=24-len(ss)
  loss=sum(4-s.bit_count() for s in ss)
  deficit=sum(max(0,8-sum(bool(s&(1<<j)) for s in ss)) for j in bad)
  if kind==0:assert rem<0;return
  if kind==1:assert loss>8;return
  if kind==2:assert deficit>4*rem;return
  assert rem>=0 and loss<=8
  if kind==3:
   j=node[1];assert j in good and j not in done and valid(j,e,done)==[];return
  if kind==4:
   assert len(done)==7 and rem==8
   unused=[j for j in bad if all(not(s&(1<<j)) for s in ss)]
   assert len(unused)>=2
   found.add(tuple(ss));return
  assert kind==5
  j=node[1];assert j in good and j not in done
  indices=[pair[0] for pair in node[2]]
  assert indices==valid(j,e,done),(ci,j,indices)
  for z,child in node[2]:check(child,e|P[j][z],done|{j})
 check(case['tree'],E0,{0})
 expected_models={tuple(x['terms']) for x in C['models'] if x['case']==ci}
 assert found==expected_models
 models.extend((ci,x) for x in sorted(found))
assert len(models)==9
out={'status':'PASS','checker':'quartic A: complete branch coverage in frozen trace','trace_nodes':visits,'unsigned_models':len(models),'all_rejected_by_remaining_energy_and_empty_intersection':True,'R5_second_weight_controls':10}
(R.parent/'receipts' if R.name=='frozen' else R/'receipts').mkdir(exist_ok=True)
path=(R.parent/'receipts' if R.name=='frozen' else R/'receipts')/'quartic_a.json'
path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
