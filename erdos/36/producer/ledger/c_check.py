import os
import json
from fractions import Fraction as F
I = os.environ.get('E36_INPUTS', 'inputs').rstrip('/') + '/'   # dir holding unktok/ and wetch/ (see README)
w=json.load(open(I+'wetch/central-certificate.json'),parse_float=str)
k=json.load(open(I+'unktok/proof/data/selected-exact-kernel.json'),parse_float=str)
t=json.load(open(I+'unktok/proof/data/target.json'),parse_float=str)
bf=json.load(open(I+'unktok/proof/data/barrier-functional.json'),parse_float=str)
C=F(t['C_exact']); y2=F(k['y2_exact'])
print('C',float(C),'y2/2',float(y2/2),'C-y2/2',float(C-y2/2))
S=F(0)
for r in w['functional_rows']:
    c=r['certificate']; n=int(c['cells']); a=F(2,n); mu=F(r['multiplier']); eta=F(c['mean_multiplier'])
    S+=mu*(-eta/a**2)
print('sum_r mu_r(-eta_r/a_r^2) =',float(S))
b=F(2,240); a=F(2,120)
C2=-(F(bf['fine_eta'])+F(bf['fine_lambda']))/b**2-(F(bf['coarse_eta'])+F(bf['coarse_lambda']))/a**2
print('two-scale C (unit weight) =',float(C2))
print('residual C - y2/2 - rows =',float(C-y2/2-S), ' ratio to C2:',float((C-y2/2-S)/C2))
print('wetch y2',w['y2'],'kernel y2',k['y2_exact'])
