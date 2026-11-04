"""Exact auxiliary rejection controls, separately written (same agent)."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json
def run():
 raw=Path('auxiliary_failures.json').read_bytes();d=json.loads(raw)
 if d['model']!='contact_row_negative_controls_v1':raise ValueError('AUXILIARY_MODEL')
 a=d['naive_floor'];x=Q(a['domain_cosine']);y=Q(a['domain_sine']);D=Q(a['D']);lam=list(map(Q,a['weights']))
 if x*x+y*y!=1 or lam!=[Q(1,2),Q(1,2)] or not 0<y<1:raise ValueError('AUXILIARY_CONTACTS')
 b=x*x-y*y;S=y*y+Q(6,25)*(1-b*b);J=y*y
 # T at BOTH domain contacts is S. The pairwise majorant is L=1-S.
 L=(1+b)/2-Q(3,25)*(1-(2*b*b-1));h2=1+D*L
 if not (L==1-S and J<=S<y and h2==1+D-D*S and h2>1+D-D*y):raise ValueError('NAIVE_FLOOR_REJECTION_MISSING')
 b0=d['too_large_coefficient'];N=b0['N'];z=Q(b0['zeta']);v=[Q(0)]*(2*N+2)
 if type(N)!=int or N!=12 or Q(b0['m1'])!=0 or Q(b0['m2'])!=1 or Q(b0['radius'])!=Q(1,2):raise ValueError('AUXILIARY_POLYNOMIAL')
 for j in range(N+1):v[2*j+1]=Q(N+1-j,N+1)
 p=[Q(0)]*(len(v)+2)
 for j,c in enumerate(v):p[j]+=c;p[j+2]-=c
 energy=Q(3,25)*sum(c*c for c in p);gap=energy-z*v[1]**2
 if energy!=Q(42,325) or gap!=Q(-1,1300):raise ValueError('COEFFICIENT_REJECTION_MISSING')
 actual=['FALSE_NAIVE_FLOOR_J_EQUALS_ABS_M1','FALSE_UNIFORM_COEFFICIENT_13_100']
 if actual!=d['expected_rejections']:raise ValueError('EXPECTED_AUXILIARY_CODES_MISMATCH')
 return dict(status='PASS',verification='separately written (same agent)',sha256=hashlib.sha256(raw).hexdigest(),exact_expected_rejections=actual,naive_floor=dict(a=str(y),b=str(b),S=str(S),J=str(J),wrong_floor_gap=str(S-y)),coefficient=dict(energy=str(energy),rhs=str(z),gap=str(gap)))
if __name__=='__main__':
 out=run();Path('logs/auxiliary-rejections.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
