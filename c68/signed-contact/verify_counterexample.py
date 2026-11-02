"""Exact rational check of the proposed three-coefficient extension."""
from fractions import Fraction as Q
from pathlib import Path
import json,hashlib
raw=Path('counterexample.json').read_bytes();d=json.loads(raw)
assert Q(d['m1'])==0 and Q(d['m2'])==1 and Q(d['kappa'])==Q(3,25)
v=list(map(Q,d['V_coefficients']));r=Q(d['radius']);assert 0<r<1
# (12/25)sin^2(theta)=(3/25)|1-exp(2i theta)|^2.
p=[Q(0)]*(len(v)+2)
for k,a in enumerate(v):p[k]+=a;p[k+2]-=a
lhs=Q(3,25)*sum(a*a for a in p);rhs=Q(7,100)*sum(a*a for a in v[:3])
assert lhs<rhs
out=dict(status='COUNTEREXAMPLE VERIFIED',lhs=str(lhs),rhs=str(rhs),gap=str(lhs-rhs),sha256=hashlib.sha256(raw).hexdigest())
print(json.dumps(out,indent=2));Path('counterexample-verification.json').write_text(json.dumps(out,indent=2)+'\n')
