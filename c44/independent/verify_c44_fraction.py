"""Checker B: interpolation identities, column-wise Fraction recurrence, H=72.
This implementation does not import the first checker or discovery programs.
"""
from fractions import Fraction as Rat
import pathlib,json,hashlib,math,itertools,sys,os,shutil
BASE=pathlib.Path(__file__).resolve().parent.parent

def local_lemma_tests():
 # Classify by the truth values of a ternary affine form on the two-control square.
 checked=0;worst=Rat(0)
 for v in itertools.product((-1,0,1),repeat=4):
  if not any(v) or v[0]+v[3]!=v[1]+v[2]:continue
  b=Rat(v[2]+v[3]-v[0]-v[1],4);c=Rat(v[1]+v[3]-v[0]-v[2],4)
  s=int(b!=0)+int(c!=0);p=Rat(sum(x!=0 for x in v),4)
  cost=Rat(s,4)+p/2+1-p
  if cost>Rat(5,4):raise ValueError('affine budget fails')
  checked+=1;worst=max(worst,cost)
 # Independently construct the 10-variable cubic polynomial and test its entire cube.
 def quad(start):
  s,t,u,v=[1<<(start+i) for i in range(4)]
  return {s|u:Rat(1,2),t|u:Rat(1,2),s|v:Rat(1,2),t|v:Rat(-1,2)}
 P={}
 for block,sgn in [(2,1),(6,-1)]:
  for mask,a in quad(block).items():
   for control,coef in [(1,Rat(1,2)),(2,Rat(sgn,2))]:P[mask|control]=a*coef
 if len(P)!=16 or any(mask.bit_count()!=3 for mask in P):raise ValueError('cubic polynomial')
 for x in range(1024):
  y=sum((a*(-1 if (mask&x).bit_count()%2 else 1) for mask,a in P.items()),Rat(0))
  if y not in (-1,1):raise ValueError('not Boolean')
 degrees=[max(mask.bit_count() for mask in P if mask>>i&1) for i in range(10)]
 if sum((Rat(1,2**d) for d in degrees),Rat(0))!=Rat(5,4):raise ValueError('sharpness')
 return {'ternary_affine_tables':checked,'largest_budget':str(worst),'sharp_cubic_terms':len(P)}

def check(path,artifact_override=None):
 spec=json.loads(pathlib.Path(path).read_text())
 if spec.get('schema')!='c44-low-degree-cap-v1':raise ValueError('schema')
 if spec.get('lemma')!='degree-three-local-potential-v1' or Rat(spec['degree_three_cap'])!=Rat(5,4) or spec['external_theorem_R3']!=10:raise ValueError('unsupported lemma')
 if spec['degree_cutoff']!=48 or spec['horizon']!=96:raise ValueError('certificate cutoffs')
 bts=(BASE/spec['source_certificate']).read_bytes() if artifact_override is None else artifact_override
 if hashlib.sha256(bts).hexdigest()!=spec['source_sha256']:raise ValueError('artifact changed')
 art=json.loads(bts);H=72
 caps=[0]
 for d in range(1,H+1):
  # Independently get the integer bound without a square-root formula.
  b=1
  while 3*(b+1)*b<=2*(d**4-d*d):b+=1
  caps.append(b)
 for degree in range(1,49):
  cert=art['certificates'][str(degree)];x=cert['nodes'];w=[Rat(z) for z in cert['weights']]
  if len(x)!=degree+1 or len(w)!=len(x) or x[0]!=1 or sorted(set(x))!=x or any(type(y)!=int or y<1 for y in x):raise ValueError('interpolation nodes')
  residues=[w[i]*x[i]*math.prod(x[i]-y for j,y in enumerate(x) if j!=i) for i in range(len(x))]
  if not residues[0] or any(a!=residues[0] for a in residues):raise ValueError('interpolation annihilator')
  if w[0]<=0 or w[0]<=sum((-a for a in w[1:] if a<0),Rat(0)):raise ValueError('no separating gap')
  caps[degree]=min(caps[degree],x[-1]-1)
 M=max(caps);prior=[Rat(0)]*(M+1);last=None
 for d in range(1,H+1):
  column=[Rat(0)]*(caps[d]+1);budget=Rat(5,4) if d==3 else Rat(d,2);fee=Rat(d,2**d)
  for b in range(1,len(column)):column[b]=min(budget,fee+max(prior[b-1],column[b-1]))
  for b in range(M+1):prior[b]=max(prior[b],column[min(b,caps[d])])
  last=column[-1]
 # Sum the tail independently by geometric-series moments starting at m=H+2.
 m=H+2
 s0=Rat(1,2**(m-1));s1=(m+1)*s0;s2=(m*m+2*m+3)*s0
 tail=Rat((H+1)**3,2**(H+1))+2*s2-s1
 total=last+tail;claim=Rat(spec['claim'])
 if not total<claim:raise ValueError('bound overclaim')
 finite=local_lemma_tests()
 return {'status':'PASS','checker':'Lagrange residues + Fraction column DP','independent_horizon':H,'bound':str(total),'display':float(total),'claim':str(claim),'margin':str(claim-total),'tail':str(tail),'finite_lemma_checks':finite,'external_input':'published R_3<=10, cited rather than re-enumerated'}

if __name__=='__main__':
 if shutil.disk_usage('.').free<30_000_000_000:raise SystemExit('PAUSED disk floor')
 print('PID',os.getpid(),flush=True);print(json.dumps(check(sys.argv[1]),indent=2),flush=True)
