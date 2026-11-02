"""Exact arithmetic checker for the two cases proved in PROOF.md.
No search imports. The universal analytic argument is a written dependency.
"""
import json, math, sys
from fractions import Fraction as Q
def verify(c):
    assert c['schema']=='c44-minimum-influence-caps-v1'
    assert c['proof']=='PROOF.md'
    assert c['external_weight_equivalence']=='CHS2020 Corollary 2.2: max D at degree<=d = R_d/2^d'
    lower={4:Q(5,4),5:Q(31,16),6:Q(5,2)};out=[]
    assert [a['degree'] for a in c['certificates']]==[4,5,6]
    for a in c['certificates']:
        d=a['degree'];M=2**(d-1);assert a['M']==M and Q(a['lower_cap'])==lower[d]
        no=d*M*M//(M+2)
        good=Q(2*d-2,2**d)+Q(1,2*M)+(1-Q(1,M))*lower[d]
        nr=math.floor(2**d*good);r=max(no,nr)
        assert a['no_minimum_R']==no and Q(a['minimum_potential'])==good and a['minimum_R']==nr
        assert a['R']==r and Q(a['cap'])==Q(r,2**d)
        assert (r+1)*(M+2)>d*M*M and Q(r+1,2**d)>good
        out.append({'degree':d,'R':r,'cap':a['cap'],'no_minimum_integer_gap':(r+1)*(M+2)-d*M*M,'minimum_potential_gap':str(Q(r+1,2**d)-good)})
    return {'status':'PASS exact cap arithmetic; universal lemmas in PROOF.md','caps':out}
if __name__=='__main__':
    print(json.dumps(verify(json.load(open(sys.argv[1] if len(sys.argv)>1 else 'cap_certificate.json'))),indent=2))
