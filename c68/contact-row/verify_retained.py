"""Separately written (same agent) retained-counterexample checks.
Exact rational polynomial products and exact-arc Arb integration; no quadrature.
"""
from pathlib import Path
from fractions import Fraction as Q
from flint import arb,fmpq,ctx
import json,hashlib
ctx.prec=320
def A(q):
 q=Q(q);return arb(fmpq(q.numerator,q.denominator))
def demand(test,code):
 if not test:raise ValueError(code)
def capped_energy(v,a,cap):
 # T=a cos(theta)+.24-.24cos(2theta). T=cap has cosine roots.
 ell=A('12/25');disc=A(a*a)-4*ell*(A(cap)-ell)
 left=(A(a)-disc.sqrt())/(2*ell);right=(A(a)+disc.sqrt())/(2*ell)
 demand(left>-1 and left<1,'RETAINED_ARC_ROOT')
 # In the two frozen cases right>=1 exactly; row case has right=1.
 demand(cap in (a*a,a),'RETAINED_CAP')
 theta=left.acos();pi=arb.pi()
 def J(k):
  k=abs(k)
  return 1-theta/pi if k==0 else -(k*theta).sin()/(pi*k)
 def moment(k):
  base=A('6/25') if k==0 else (A(a)/2 if k==1 else (-A('3/25') if k==2 else arb(0)))
  return base+(A(cap)-A('6/25'))*J(k)-A(a)/2*(J(k-1)+J(k+1))+A('3/25')*(J(k-2)+J(k+2))
 value=moment(0)*A(sum(t*t for t in v))
 for k in range(1,len(v)):value+=2*moment(k)*A(sum(v[j]*v[j+k] for j in range(len(v)-k)))
 return value

def verify():
 path=Path('baseline/nearby-candidate.json');raw=path.read_bytes();d=json.loads(raw)
 a=Q(d['m1']);demand(a==Q(1,50) and Q(d['m2'])==1,'RETAINED_MOMENTS')
 v=list(map(Q,d['coefficients']));demand(len(v)==129 and v[1]==1,'RETAINED_POLYNOMIAL')
 old=capped_energy(v,a,a*a);new=capped_energy(v,a,a)
 demand(old<A('21/200'),'EXPECTED_0105_COUNTEREXAMPLE_MISSING')
 demand(old>A('19/200'),'BASELINE_0095_CONTRADICTION')
 demand(new>A('23/200'),'ROW_COUNTEREXAMPLE')
 # Their moment matrix is PSD: the measure has masses (1+a)/2,(1-a)/2 at +/-1.
 demand((1+a)/2>0 and (1-a)/2>0,'RETAINED_PSD')
 # For the naive third diagonal, multiply V by (1-z²) exactly.
 w=[Q(1),0,Q(3,2),0,Q(9,8),0,Q(3,4),0,Q(3,8)]
 prod=[Q(0)]*(len(w)+2)
 for j,t in enumerate(w):prod[j]+=t;prod[j+2]-=t
 energy=Q(3,25)*sum(t*t for t in prod);rhs=Q(7,100)*sum(w[j]**2 for j in (0,1,2))
 demand(energy==Q(87,400) and rhs==Q(91,400) and energy-rhs==Q(-1,100),'EXPECTED_THIRD_COUNTEREXAMPLE_MISSING')
 return dict(status='PASS',verification='separately written (same agent)',bits=ctx.prec,retained_sha256=hashlib.sha256(raw).hexdigest(),old_energy=str(old),old_0105_gap=str(old-A('21/200')),old_0095_gap=str(old-A('19/200')),row_energy=str(new),row_0115_gap=str(new-A('23/200')),third_energy=str(energy),third_rhs=str(rhs),third_gap=str(energy-rhs),scope='The old relaxed .105 and naive third-diagonal claims remain rejected; the new row lemma corrects only coefficient one.')
if __name__=='__main__':
 out=verify();Path('logs/retained-verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
