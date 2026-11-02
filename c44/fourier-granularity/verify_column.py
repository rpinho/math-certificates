"""Second standalone exact checker. No imports of search or other verifiers.
Uses a Krawtchouk recurrence, Lagrange residues, Fraction columns and H=72.
"""
import hashlib,json,math,os,pathlib,sys
from fractions import Fraction as F
HERE=pathlib.Path(__file__).resolve().parent
EPI='ce66f1097a7284e9845113fa1dc39267932cc934fd23d9019ff13d3dcb39cf49'
def verify(spec):
 assert spec['schema']=='c44-fourier-granularity-bound-v1'
 assert spec['external_R3']==10 and spec['external_bs_theorem']=='3b(b-1)<=2(d^4-d^2)'
 assert spec['caps']=={'3':'5/4','4':'31/16','7':'447/128'}
 assert spec['horizon']==96
 bs=[0];H=72
 for d in range(1,H+1):
  b=0
  while 3*b*(b+1)<=2*(d**4-d*d):b+=1
  bs.append(b)
 raw=(HERE/spec['epi_source']).read_bytes();assert hashlib.sha256(raw).hexdigest()==EPI
 ep=json.loads(raw)
 for d in range(1,49):
  z=ep['certificates'][str(d)];x=z['nodes'];w=[F(a) for a in z['weights']]
  assert len(x)==d+1 and len(w)==len(x) and x[0]==1
  assert x==sorted(set(x)) and all(type(k)==int and k>0 for k in x)
  residues=[w[i]*x[i]*math.prod(x[i]-x[j] for j in range(len(x)) if j!=i) for i in range(len(x))]
  assert residues[0] and all(t==residues[0] for t in residues)
  assert w[0]>0 and w[0]>sum(-t for t in w[1:] if t<0)
  bs[d]=min(bs[d],x[-1]-1)
 raw=(HERE/spec['spectral_source']).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==spec['spectral_sha256']
 sp=json.loads(raw);assert sp['schema']=='c44-spectral-bounds-v1'
 seen=set();duals=[]
 for cert in sp['certificates']:
  assert cert['schema'] in ('c44-spectral-l1-dual-v1','c44-spectral-level-dual-v2','c44-spectral-lattice-dual-v3')
  d=cert['degree'];n=cert['variables']
  assert type(d)==int and 1<=d<=48 and d not in seen and type(n)==int and n>=d
  seen.add(d);a={int(k):F(v) for k,v in cert['alpha'].items()}
  lattice=cert['schema']=='c44-spectral-lattice-dual-v3'
  free=cert.get('free_levels') if cert['schema']=='c44-spectral-level-dual-v2' else [0]
  if not lattice:
   assert isinstance(free,list) and free==sorted(set(free)) and free[0]==0
   assert all(type(j)==int and 0<=j<d for j in free)
  assert len(a)==len(cert['alpha']) and all(0<=k<=n for k in a)
  coeff=[F(0)]*(d+1)
  for x,t in a.items():
   vals=[1,n-2*x]
   for j in range(1,d):
    num=(n-2*x)*vals[-1]-(n-j+1)*vals[-2]
    assert num%(j+1)==0
    vals.append(num//(j+1))
   for j in range(d+1):coeff[j]+=t*F(vals[j],math.comb(n,j))
  if not lattice:assert all(abs(z)<=1 for j,z in enumerate(coeff) if j not in free)
  lower=sum(t*(1 if x==0 else -1) if x in (0,1) else -abs(t) for x,t in a.items())
  M=F(2**(d-1))
  if lattice:
   excess=[]
   for j,t in enumerate(coeff):
    k=t.numerator//(2*t.denominator)
    excess.append(F(math.comb(n,j))*max(t*k-k*k,t*(k+1)-(k+1)*(k+1)))
   upper=M+sum(excess)/M
  else:upper=M+sum(F(math.comb(n,j))*coeff[j]**2/(4*M) for j in free)
  assert lower>upper
  assert cert['block_bound']==n-1
  bs[d]=min(bs[d],n-1);duals.append({'degree':d,'B':n-1,'gap':str(lower-upper)})
 # Columns are filled in increasing degree and then increasing block budget.
 # env[b] is max over already-computed degrees at block budget b.
 cap={3:F(5,4),4:F(31,16),7:F(447,128)}
 env=[F(0)]*(max(bs)+1);columns=[]
 for d in range(1,H+1):
  charge=F(d,2**d);ceiling=cap.get(d,F(d,2));col=[F(0)]
  for b in range(1,bs[d]+1):col.append(min(ceiling,charge+max(env[b-1],col[-1])))
  for b in range(len(env)):env[b]=max(env[b],col[min(b,bs[d])])
  columns.append(col[-1])
 assert max(columns)==columns[-1] and env[-1]==columns[-1]
 m=H+1
 tail=F(2*m**3+6*m*m+18*m+26,2**m)
 bound=columns[-1]+tail
 assert bound<F(spec['claim'])<F('4.3264049226')
 return {'status':'PASS standalone exact spectral duals, Lagrange residues, columns and cubic tail',
         'horizon':H,'finite':str(columns[-1]),'tail':str(tail),'certified_bound':str(bound),
         'claim':spec['claim'],'margin':str(F(spec['claim'])-bound),'B':bs,'duals':duals}
def main():
 print('PID',os.getpid(),flush=True)
 p=HERE/(sys.argv[1] if len(sys.argv)>1 else 'candidate.json')
 out=verify(json.loads(p.read_text()));(HERE/'verification_bound_column.json').write_text(json.dumps(out,indent=2)+'\n')
 print({k:out[k] for k in ('status','certified_bound','claim')},flush=True)
if __name__=='__main__':main()
