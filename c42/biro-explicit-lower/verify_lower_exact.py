"""Separate exact validation of LOWER_PROOF.md's frozen numerical certificate.

Written after the proof, without imports from any optimizer or numerical
model. Fractions only. This verifies numerical hypotheses and exercises
finite identities, not a formalization of the proof or a human referee.
"""
import copy,datetime,hashlib,json,math,sys
from fractions import Fraction as Q
from pathlib import Path

if not __debug__:
 raise SystemExit('FAIL: run without -O')

def two(e):
 return Q(2)**e

def validate(d):
 checks=[]
 def need(name,condition):
  if not condition:raise ValueError('FAIL '+name)
  checks.append(name)
 for key in ['delta_exponent','eta_exponent','lambda_exponent','uniform_error_exponent',
             'parallel_deficit_exponent','early_fraction_exponent','radial_error_exponent',
             't0_lower_exponent','scale_ratio_lower_exponent','contraction_product_upper_exponent']:
  need('positive integral '+key,type(d.get(key)) is int and 0<d[key]<100000)
 need('schema',d['schema']=='biro-explicit-lower-v1')
 delta=two(-d['delta_exponent']);q=Q(1,2)+delta
 eta=two(-d['eta_exponent']);lam=two(-d['lambda_exponent'])
 zeta=two(-d['uniform_error_exponent']);eps=two(-d['parallel_deficit_exponent'])
 sigma=two(-d['early_fraction_exponent']);beta_cap=two(-d['radial_error_exponent'])
 tmin=two(d['t0_lower_exponent']);scale=two(d['scale_ratio_lower_exponent'])
 product_cap=two(-d['contraction_product_upper_exponent'])
 final_cap=Q(d['final_error_upper'])
 rlo,rhi=Q(7,10),Q(3,4)
 need('r bracket by squares',rlo*rlo<Q(1,2)<rhi*rhi)
 need('positive explicit gain',delta>0 and q>Q(1,2))
 need('q upper',q<Q(9,16)<rlo)
 need('growth lower 1/8',rlo-q>Q(1,8))
 need('growth upper 2',1+q<2)
 need('e <= 2 delta',1/rlo<2)
 need('A > 1/(8 delta)',(1-rhi)/(2*delta)>=1/(8*delta))
 need('radial error e coefficient',3+Q(15,2)/rlo<20)
 need('radial error endpoint coefficient',Q(15,2)+12/rlo<25)
 need('small eta',eta<=Q(1,4))
 need('delta <= eta squared',delta<=eta*eta)
 # A completely rational enclosure of the radical defining b.
 radicand_upper=delta+delta**2+rhi*eta+eta**2/2
 need('radicand upper <= 2 eta',radicand_upper<=2*eta)
 root_upper=beta_cap-rhi*eta
 need('radical upper positive',root_upper>0)
 need('b <= beta cap by squaring',root_upper**2>=radicand_upper)
 B=20+60/eta
 Bcap=two(d['eta_exponent']+6)
 need('B upper',B<=Bcap)
 need('t0 at least 2',lam/(8*delta)>6)
 need('t0 lower from polynomial growth',lam/(8*delta)>4*tmin**2 and tmin>=2)
 need('scale ratio lower',1/(6*lam)>scale**2)
 need('uniform balance error',beta_cap+Bcap*(2*delta)/lam+25/tmin<zeta)
 need('R bracket',Q(3,2)-zeta>=Q(7,5) and Q(3,2)+zeta<=Q(8,5))
 need('summed-angle floor',Q(1,2)*(1+rlo)>Q(9,10)**2)
 need('Lipschitz first term',1/(Q(7,5)*Q(3,2))<Q(1,2))
 need('Lipschitz second term',1/(4*Q(9,10))<Q(1,3))
 need('Lipschitz third term',1/(16*Q(9,10)*Q(7,5)*Q(3,2))<Q(1,20))
 need('Lipschitz sum',Q(1,2)+Q(1,3)+Q(1,20)<1)
 need('q squared change',delta<=1 and 4*Q(9,10)*Q(7,5)>2)
 need('w >= 1/t',tmin>=4 and 3*Q(7,5)-4>0)
 need('contraction product cap',product_cap**3>=1/scale)
 need('parallelism deficit',6*(zeta+delta)+product_cap<eps)
 need('angle conversion error',zeta+delta<=eps/2)
 need('small epsilon',eps<=Q(1,100))
 need('ratio radial part',Q(5,2)/Q(9,10)<3)
 need('ratio phase part',Q(8,5)/Q(9,10)<2)
 # sqrt(2) < 3/2 and sqrt(eps)<=1/10 suffice for this estimate.
 need('weights conversion',Q(3,2)**2>2 and (Q(3,2)+Q(1,10))/Q(9,10)<3)
 need('weighted mean error',7+3*Q(9,16)<16)
 need('delta small for second moment',delta**2<=eps and delta**4<=eps)
 need('distance bound sqrt(18)<5',18<25)
 need('dyadic eighth root',d['early_fraction_exponent']%8==0)
 need('dyadic fourth root',d['parallel_deficit_exponent']%4==0)
 need('early cutoff exists',sigma*tmin*scale>2 and sigma<1)
 need('b to C transfer',2/rlo<3)
 early=2*two(-d['early_fraction_exponent']//8)
 late=(30/sigma)*two(-d['parallel_deficit_exponent']//4)
 need('final error cap',early+late<final_cap)
 need('escape contradiction',final_cap<rlo*(rlo-Q(1,2)))
 return checks

def pmul(a,b):
 c=[Q(0)]*(len(a)+len(b)-1)
 for j,x in enumerate(a):
  for k,y in enumerate(b):c[j+k]+=x*y
 return c

def universal_polynomials():
 # Independently expand both telescoping identities used in the note.
 a=pmul(pmul(pmul([-1,3],[-1,3]),[-1,3]),[1,1])
 rhs=[Q(0)]*5;rhs[4]=27
 diff=[x-y for x,y in zip(rhs,a)]
 if diff!=[1,-8,18,0,0]:raise ValueError('cubic product identity')
 # 18 t^2-8t+1=18t(t-1)+10t+1 is positive for integer t>=1.
 if pmul([0,18],[-1,1])!=[0,-18,18]:raise ValueError('positivity decomposition')
 p=[Q(1)]
 for _ in range(8):p=pmul(p,[1,8])
 p[8]-=8**8;p[7]-=8**8
 if not (p[7]==p[8]==0 and all(x>=0 for x in p)):
  raise ValueError('eighth power telescoping inequality')
 return ['cubic telescoping identity','cubic positivity on integers t>=1','eighth-power telescoping inequality']

# Gaussian rationals, no floating point or Python complex arithmetic.
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[0],-a[1])
def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,x):return (a[0]*x,a[1]*x)
def csum(xs):
 a=(Q(0),Q(0))
 for x in xs:a=add(a,x)
 return a

def finite_identities():
 for n in range(2,14):
  roots=[(Q(1),Q(0))]+[(Q((7*j)%11-5,7),Q((3*j)%7-3,9)) for j in range(1,n)]
  b=[(Q(1),Q(0))]
  for root in roots[1:]:
   new=[(Q(0),Q(0))]*(len(b)+1)
   for j,x in enumerate(b):
    new[j]=add(new[j],x);new[j+1]=add(new[j+1],neg(mul(x,root)))
   b=new
  powers=[(Q(1),Q(0))]*n;S=[(Q(n),Q(0))]
  for k in range(1,n+1):
   powers=[mul(a,z) for a,z in zip(powers,roots)];S.append(csum(powers))
  C=[csum(b[:j+1]) for j in range(n)];bn=b+[(Q(0),Q(0))]
  for t in range(1,n+1):
   left=add(C[t-1],neg(scale(bn[t],t)))
   right=csum(mul(b[j],S[t-j]) for j in range(t))
   if left!=right:raise ValueError(f'Newton identity n={n},t={t}')
  for t in range(1,n):
   left=add(scale(csum(C[:t]),2),neg(scale(C[t],t)))
   right=csum(mul(C[j],S[t-j]) for j in range(t))
   if left!=right:raise ValueError(f'summed identity n={n},t={t}')
 return ['Gaussian-rational Newton identities n=2..13', 'Gaussian-rational summed identities n=2..13']

def main():
 artifact=Path(sys.argv[1] if len(sys.argv)>1 else 'inputs/lower_certificate.json')
 manifest=json.loads(Path('inputs/lower_manifest.json').read_text())
 for name,digest in manifest['files'].items():
  if hashlib.sha256(Path(name).read_bytes()).hexdigest()!=digest:raise ValueError('frozen hash mismatch: '+name)
 d=json.loads(artifact.read_text());checks=validate(d)+universal_polynomials()+finite_identities()
 controls=[]
 for key,value in [('delta_exponent',1),('eta_exponent',1),('parallel_deficit_exponent',500),
                   ('scale_ratio_lower_exponent',4096),('early_fraction_exponent',8),
                   ('final_error_upper','1/2')]:
  bad=copy.deepcopy(d);bad[key]=value
  try:validate(bad)
  except ValueError as e:controls.append(dict(key=key,value=value,rejected=str(e)))
  else:raise ValueError('negative control unexpectedly accepted: '+key)
 out=dict(status='PASS_EXACT_NUMERICAL_HYPOTHESES',claim=d['claim'],
  qualification='Candidate and unrefereed. Analytic proof is not formally verified.',
  utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
  artifact_sha256=hashlib.sha256(artifact.read_bytes()).hexdigest(),
  proof_sha256=hashlib.sha256(Path(d['proof_file']).read_bytes()).hexdigest(),
  checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  checks=checks,negative_controls=controls)
 Path('results/lower_exact.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))

if __name__=='__main__':main()
