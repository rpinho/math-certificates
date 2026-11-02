"""Checker A: exact rational dual moments, dyadic row DP, finite local-degree cases.
The general proof in paper/c44.tex cites the published theorem R_3<=10.
"""
import pathlib,json,sys,hashlib,itertools,math,os,shutil
from fractions import Fraction as F
ROOT=pathlib.Path(__file__).resolve().parent

def check_cap():
 # Every nonzero coefficient of an affine {-1,0,1}-valued polynomial has |b|>=1/2.
 # Its range has width <=2, so there are <=2 such coefficients. Check all patterns.
 patterns=0;maxcap=F(0)
 for s in range(3):
  for coeff in itertools.product([F(-1),F(-1,2),F(0),F(1,2),F(1)],repeat=s+1):
   a,*bs=coeff
   if any(b==0 for b in bs):continue
   vals=[a+sum(b*x for b,x in zip(bs,z)) for z in itertools.product([-1,1],repeat=s)]
   if any(v not in [-1,0,1] for v in vals) or all(v==0 for v in vals):continue
   active=sum(v!=0 for v in vals);p=F(active,len(vals))
   cap=F(s,4)+p*F(1,2)+(1-p)*1
   if cap>F(5,4):raise ValueError('local case cap')
   patterns+=1;maxcap=max(maxcap,cap)
 # Explicit 10-variable degree-three witness: F_{d+1}=(s+t)F_d/2+(s-t)F'_d/2.
 table=[]
 def seed(vals):
  s,t=vals[:2];return ((s+t)*vals[2]+(s-t)*vals[3])//2
 for x in itertools.product([-1,1],repeat=10):table.append(((x[0]+x[1])*seed(x[2:6])+(x[0]-x[1])*seed(x[6:10]))//2)
 if any(v not in [-1,1] for v in table):raise ValueError('Boolean seed')
 a=table[:];h=1
 while h<len(a):
  for i in range(0,len(a),2*h):
   for j in range(i,i+h):u,v=a[j],a[j+h];a[j]=u+v;a[j+h]=u-v
  h*=2
 local=[0]*10
 for mask,v in enumerate(a):
  if v:
   d=mask.bit_count()
   if d>3:raise ValueError('seed degree')
   for i in range(10):
    if mask>>i&1:local[i]=max(local[i],d)
 if local!=[3]*10:raise ValueError('cap sharpness witness')
 return {'affine_patterns':patterns,'max_local_case':str(maxcap),'sharpness_local_degrees':local}

def exact_bound(c,artifact):
 H=c['horizon'];N=c['degree_cutoff']
 if type(H)!=int or not 48<=H<=128 or N!=48:raise ValueError('cutoffs')
 B=[0]*(H+1)
 for d in range(1,H+1):
  z=math.isqrt(2*(d**4-d*d)//3)+1
  while 3*z*(z-1)>2*(d**4-d*d):z-=1
  B[d]=z
 for d in range(1,N+1):
  entry=artifact['certificates'][str(d)];xs=entry['nodes'];ws=[F(s) for s in entry['weights']]
  if len(xs)!=d+1 or len(ws)!=len(xs) or any(type(x)!=int for x in xs) or sorted(set(xs))!=xs or xs[0]!=1:raise ValueError('dual nodes')
  for k in range(1,d+1):
   if sum((w*x**k for x,w in zip(xs,ws)),F(0)):raise ValueError('dual moment')
  if ws[0]<=0 or ws[0]+sum((w for w in ws[1:] if w<0),F(0))<=0:raise ValueError('dual gap')
  B[d]=min(B[d],max(xs)-1)
 U=1<<H;row=[0]*(H+1)
 for b in range(1,max(B)+1):
  new=[0]*(H+1);prefix=0
  for d in range(1,H+1):
   prefix=max(prefix,row[d]);cap=(5*U//4 if d==3 else d*U//2)
   new[d]=row[d] if b>B[d] else min(cap,d*(1<<(H-d))+prefix)
  row=new
 tail=F((H+1)**3+2*H*H+11*H+19,2**(H+1))
 return F(row[H],U)+tail,tail

def check(path,artifact_override=None):
 p=pathlib.Path(path);c=json.loads(p.read_text())
 if c.get('schema')!='c44-low-degree-cap-v1' or c.get('lemma')!='degree-three-local-potential-v1':raise ValueError('schema/lemma')
 if F(c['degree_three_cap'])!=F(5,4) or c['external_theorem_R3']!=10:raise ValueError('unsupported analytic premise')
 data=(ROOT/c['source_certificate']).read_bytes() if artifact_override is None else artifact_override
 if hashlib.sha256(data).hexdigest()!=c['source_sha256']:raise ValueError('source hash')
 cap=check_cap();bound,tail=exact_bound(c,json.loads(data));claim=F(c['claim'])
 if not bound<claim:raise ValueError('upper bound overclaim')
 return {'status':'PASS','checker':'Q moments + dyadic row DP','bound':str(bound),'display':float(bound),'claim':str(claim),'margin':str(claim-bound),'tail':str(tail),'cap_checks':cap,'external_input':'published R_3<=10; not reclassified here'}
if __name__=='__main__':
 if shutil.disk_usage('.').free<30_000_000_000:raise SystemExit('PAUSED disk floor')
 print('PID',os.getpid(),flush=True);print(json.dumps(check(sys.argv[1]),indent=2),flush=True)
