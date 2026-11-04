"""Exact geometric contact controls, separately written (same agent).
Only Fraction and Arb; no search or other acceptance imports.
"""
from fractions import Fraction as Q
from flint import arb,fmpq,ctx
from pathlib import Path
import hashlib,json
ctx.prec=320
def A(q):
 q=Q(q);return arb(fmpq(q.numerator,q.denominator))
def need(test,code):
 if not test:raise ValueError(code)
def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a):return (a[0],-a[1])
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def mean(z,weights):return tuple(sum(w*p[j] for w,p in zip(weights,z)) for j in (0,1))

def verify():
 raw=Path('certificates/contact-configurations.json').read_bytes();d=json.loads(raw);need(d['model']=='exact_contact_configurations_v1' and Q(d['kappa'])==Q(3,25),'CONFIG_SCHEMA');D=Q(d['D']);need(D>0,'CONFIG_D');out=[]
 for case in d['cases']:
  weights=list(map(Q,case['weights']));domain=[tuple(map(Q,z)) for z in case['domain']];image=[tuple(map(Q,z)) for z in case['image_directions']];n=len(weights)
  need(n in (2,3) and len(domain)==len(image)==n and all(w>0 for w in weights) and sum(weights)==1,'CONFIG_WEIGHTS')
  need(all(dot(z,z)==1 for z in domain+image),'CONFIG_UNIT_VECTORS');need(mean(image,weights)==(0,0),'CONFIG_BALANCE')
  m1=mean(domain,weights);m2=mean([mul(z,z) for z in domain],weights);a2=dot(m1,m1);b2=dot(m2,m2);S=a2+Q(6,25)*(1-b2)
  if a2:
   q0=(1+mul(m2,mul(conj(m1),conj(m1)))[0]/a2)/2;a=A(a2).sqrt();J=a*(A(q0)+a)/(1+a);need(q0>=a2 and q0<=1,'CONFIG_PROJECTED_MOMENT')
  else:q0=Q(0);J=A(0)
  T=[dot(z,m1)+Q(6,25)*(1-dot(mul(z,z),m2)) for z in domain];need(A(max(T))>=J,'CONFIG_ROW_FLOOR')
  u=None;F={}
  for i in range(n):
   for j in range(i):
    z=mul(domain[i],conj(domain[j]));F[i,j]=(1-z[0])/2-Q(3,25)*(1-mul(z,z)[0]);den=1-dot(image[i],image[j]);need(den>0 and F[i,j]>0,'CONFIG_PAIR_DISTINCT');r=2*F[i,j]/den;u=r if u is None else min(u,r)
  need(u is not None and u>0,'CONFIG_RADIUS');h2=1+D*u
  pair_gaps=[]
  for i in range(n):
   row=Q(0)
   for j in range(n):
    cosh_distance=1+D*u*(1-dot(image[i],image[j]));row+=weights[j]*cosh_distance
    if j<i:
     gap=2*D*F[i,j]-(cosh_distance-1);need(gap>=0,'CONFIG_PAIR_BOUND');pair_gaps.append(gap)
   need(row==h2,'CONFIG_CONTACT_ROW_IDENTITY')
  need(1-S-u>=0,'CONFIG_OLD_AVERAGE_FLOOR')
  improved=J>A(S)
  need(improved==case['expect_row_improvement'],'CONFIG_IMPROVEMENT_EXPECTATION')
  rowgap=1-A(u)-J if improved else A(1-u-S);need(rowgap>=0,'CONFIG_IMPROVED_RADIUS')
  out.append(dict(name=case['name'],weights=list(map(str,weights)),m1=list(map(str,m1)),m2=list(map(str,m2)),a_squared=str(a2),q0=str(q0),S=str(S),J=str(J),row_improvement=improved,allowed_normalized_radius=str(u),h_squared=str(h2),min_exact_pair_gap=str(min(pair_gaps)),improved_normalized_radius_gap=str(rowgap)))
 return dict(status='PASS',verification='separately written (same agent)',sha256=hashlib.sha256(raw).hexdigest(),cases=out,scope='Exact balanced geometric contact configurations satisfying the Fourier pair relaxation; no holomorphic annular interpolation claim.')
if __name__=='__main__':
 out=verify();Path('logs/contact-configurations.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
