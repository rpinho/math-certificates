"""Primary integer-row calculation, after replay of the inherited raw certificates."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib,sys
R=Path(__file__).resolve().parent
cert=json.loads((R/'certificate.json').read_text())
baseline=json.loads((R/'baseline/c44r5/verification_independent_H96.json').read_text())
assert baseline['status']=='PASS'
B=baseline['B'];H=96;unit=1<<H
def bound(caps):
    c={int(k):Q(v) for k,v in caps.items()}
    previous=[0]*(H+1)
    for b in range(1,max(B)+1):
        current=[0]*(H+1);lower=0
        for d in range(1,H+1):
            lower=max(lower,previous[d])
            current[d]=previous[d] if b>B[d] else min(int(c.get(d,Q(d,2))*unit),d*2**(H-d)+lower)
        previous=current
    return Q(max(previous),unit)+Q(H**3+6*H**2+18*H+26,unit),previous
value,columns=bound(cert['caps'])
oldspec=json.loads((R/'baseline/c44r5/candidate.json').read_text())
old,_=bound(oldspec['caps'])
assert old==Q(125475790246857326765951236155,39614081257132168796771975168)
out={'schema':'quartic22-bound-v1','horizon':H,'caps':cert['caps'],
     'claim':'3.1498761303','bound':str(value),'baseline':str(old),'gain':str(old-value),
     'B':B,'finite_degrees':{str(d):str(Q(columns[d],unit)) for d in range(1,H+1)},
     'sources':{name:hashlib.sha256((R/name).read_bytes()).hexdigest() for name in
                ['certificate.json','sources/F10T6.txt','witness22.json',
                 'baseline/c44r5/epi_certificate.json','baseline/c44r5/spectral_certificate_round3.json']}}
print(json.dumps({k:out[k] for k in ['bound','baseline','gain']},indent=2))
assert value<Q(out['claim'])
if '--check' in sys.argv:assert json.loads((R/'candidate.json').read_text())==out
else:(R/'candidate.json').write_text(json.dumps(out,indent=2)+'\n')
