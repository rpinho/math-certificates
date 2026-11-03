"""Exact annihilator certificate A: weighted disjoint-set elimination."""
import collections,gzip,json,pathlib,sys
R=pathlib.Path(sys.argv[1])
with gzip.open(R/'certificates.json.gz','rt') as f:P=json.load(f)
with gzip.open(R/'source_seeds.json.gz','rt') as f:S=json.load(f)
assert P['schema']=='c44-annihilator-traces-v1' and P['status']=='candidate, unrefereed'
assert len(P['cases'])==14 and collections.Counter(c['degree'] for c in P['cases'])=={5:6,6:8}
class State:
 def __init__(self,n):self.p=list(range(n));self.s=[1]*n;self.w=[1]*n;self.zero=[False]*n
 def find(self,i):
  if self.p[i]!=i:
   r,s=self.find(self.p[i]);self.s[i]*=s;self.p[i]=r
  return self.p[i],self.s[i]
 def join(self,i,j,rel):
  a,x=self.find(i);b,y=self.find(j);assert a!=b and not self.zero[a] and not self.zero[b]
  rel*=x*y
  if self.w[a]>self.w[b]:a,b=b,a
  self.p[a]=b;self.s[a]=rel;self.w[b]+=self.w[a]

def multiply(a,b):
 out=collections.defaultdict(int)
 for s,c in a.items():
  for t,z in b.items():out[s^t]+=c*z
 return {s:c for s,c in out.items() if c}
checked=set();audit=[]
for case in P['cases']:
 seed=S['seeds'][case['seed']];poly={int(s):c for s,c in seed['terms']};n=seed['count'];d=seed['degree'];D=seed['denominator'];b=case['coordinate']
 assert 0<=b<n and (case['count'],case['degree'],case['denominator'])==(n,d,D) and case['expected_dimension']==1
 assert d in (5,6) and n==(46 if d==5 else 94)
 if case['seed'] not in checked:
  assert multiply(poly,poly)=={0:D*D};checked.add(case['seed'])
 U={s^(1<<b):c for s,c in poly.items() if s>>b&1};V={s:c for s,c in poly.items() if not s>>b&1}
 bank=[int(s) for s in case['bank']];assert bank==sorted(set(bank)) and set(U)<=set(bank)
 assert all(0<=s<1<<n and not(s>>b&1) and s.bit_count()<=d-1 for s in bank)
 assert U and multiply(U,V)=={}
 assert len(case['trace'])==len(bank)-1
 state=State(len(bank))
 for step in case['trace']:
  key=int(step['row']);assert 0<=key<1<<n
  row=collections.defaultdict(int)
  for i,mask in enumerate(bank):
   value=V.get(mask^key,0)
   if value:
    root,phase=state.find(i)
    if not state.zero[root]:row[root]+=value*phase
  row={r:c for r,c in row.items() if c};assert row
  i=step['i'];assert 0<=i<len(bank);ri,si=state.find(i);assert not state.zero[ri]
  if step['kind']=='zero':
   assert set(row)=={ri};state.zero[ri]=True
  else:
   assert step['kind']=='pair';j=step['j'];rel=step['sign'];assert rel in (-1,1) and 0<=j<len(bank)
   rj,sj=state.find(j);assert ri!=rj and not state.zero[rj] and set(row)=={ri,rj}
   assert row[ri]*(-rel*sj)==row[rj]*si
   state.join(i,j,rel)
 live={state.find(i)[0] for i in range(len(bank)) if not state.zero[state.find(i)[0]]};assert len(live)==1
 alpha=set()
 for i,mask in enumerate(bank):
  r,phase=state.find(i);coefficient=U.get(mask,0)
  if state.zero[r]:assert coefficient==0
  else:alpha.add(coefficient*phase)
 assert len(alpha)==1 and next(iter(alpha))!=0
 audit.append(dict(seed=case['seed'],coordinate=b,degree=d,columns=len(bank),inferences=len(case['trace']),dimension=1))
result=dict(status='PASS',verifier='A weighted union elimination',cases=len(audit),rows=audit,scope='Only the fourteen explicitly supplied Fourier mask banks; no universal lower-bound obstruction')
if len(sys.argv)>2:pathlib.Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
