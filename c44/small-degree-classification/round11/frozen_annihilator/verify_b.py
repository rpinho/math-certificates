"""Separately written (same agent) exact annihilator B: explicit signed parameter substitutions."""
import collections,gzip,itertools,json,pathlib,sys
folder=pathlib.Path(sys.argv[1])
with gzip.open(folder/'certificates.json.gz','rt') as source:packet=json.load(source)
with gzip.open(folder/'source_seeds.json.gz','rt') as source:seeds=json.load(source)['seeds']
assert packet['schema']=='c44-annihilator-traces-v1' and packet['status']=='candidate, unrefereed'
assert len(packet['cases'])==14 and sorted(c['degree'] for c in packet['cases'])==[5]*6+[6]*8

def boolean_check(p,D):
 pairs=sorted(p.items());correlation={0:sum(c*c for s,c in pairs)}
 for (s,a),(t,b) in itertools.combinations(pairs,2):correlation[s^t]=correlation.get(s^t,0)+2*a*b
 assert correlation[0]==D*D and all(v==0 for k,v in correlation.items() if k)
seen=set();results=[]
for item in packet['cases']:
 name=item['seed'];source=seeds[name];p={int(s):int(c) for s,c in source['terms']};d=source['degree'];n=source['count'];D=source['denominator'];chosen=item['coordinate']
 assert item['degree']==d and item['count']==n and item['denominator']==D and item['expected_dimension']==1
 assert (d,n) in ((5,46),(6,94)) and 0<=chosen<n
 if name not in seen:boolean_check(p,D);seen.add(name)
 u={s-2**chosen:c for s,c in p.items() if s&2**chosen};v={s:c for s,c in p.items() if not s&2**chosen}
 masks=list(map(int,item['bank']));assert len(set(masks))==len(masks) and all(s>=0 and s<2**n and not(s&2**chosen) and s.bit_count()<d for s in masks)
 assert set(u)<=set(masks) and u
 product=collections.Counter()
 for left,a in u.items():
  for right,b in v.items():product[left^right]+=a*b
 assert all(value==0 for value in product.values())
 assert len(item['trace'])+1==len(masks)
 expression=list(range(1,len(masks)+1))
 for instruction in item['trace']:
  mask=int(instruction['row']);assert 0<=mask<2**n
  equation=collections.Counter()
  for term,symbol in zip(masks,expression):
   if symbol:
    coefficient=v.get(mask^term,0)
    if coefficient:equation[abs(symbol)]+=coefficient*(1 if symbol>0 else -1)
  equation={k:c for k,c in equation.items() if c};assert equation
  i=instruction['i'];assert 0<=i<len(masks);left=expression[i];assert left
  if instruction['kind']=='zero':
   assert set(equation)=={abs(left)}
   expression=[0 if abs(symbol)==abs(left) else symbol for symbol in expression]
  else:
   assert instruction['kind']=='pair';j=instruction['j'];sign=instruction['sign'];assert 0<=j<len(masks) and sign in (-1,1)
   right=expression[j];assert right and abs(left)!=abs(right)
   identity={abs(left):(1 if left>0 else -1),abs(right):-sign*(1 if right>0 else -1)}
   assert set(identity)==set(equation)
   first,second=identity
   assert equation[first]*identity[second]==equation[second]*identity[first]
   replacement=sign*(1 if left>0 else -1)*(1 if right>0 else -1)
   expression=[(1 if symbol>0 else -1)*replacement*abs(right) if abs(symbol)==abs(left) else symbol for symbol in expression]
 assert len({abs(symbol) for symbol in expression if symbol})==1
 parameter=None
 for mask,symbol in zip(masks,expression):
  value=u.get(mask,0)
  if not symbol:assert value==0
  else:
   current=value*(1 if symbol>0 else -1)
   if parameter is None:parameter=current
   else:assert parameter==current
 assert parameter not in (None,0)
 results.append(dict(seed=name,coordinate=chosen,degree=d,columns=len(masks),inferences=len(item['trace']),dimension=1))
result=dict(status='PASS',verifier='B explicit signed substitutions',cases=len(results),rows=results,scope='Only the fourteen explicitly supplied Fourier mask banks; no universal lower-bound obstruction')
if len(sys.argv)>2:pathlib.Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
