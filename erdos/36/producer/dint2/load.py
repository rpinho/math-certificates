import json
from fractions import Fraction as Fr
import os
_I=os.environ.get('E36_INPUTS','inputs').rstrip('/')   # dir holding unktok/ and wetch/ (see README)
U=_I+'/unktok/proof/data/'
W=_I+'/wetch/'
def F(x): return Fr(str(x))
def load():
    k=json.load(open(U+'selected-exact-kernel.json'),parse_float=str)
    c0=F(k['constant_exact']); y2=F(k['y2_exact'])
    H=[F(x) for x in k['fine_hat_heights_exact']]
    assert len(H)==241 and k['fine_hat_cells']==240
    cos=[(F(d['xi']),F(d['z'])) for d in k['merged_cos']]
    p=json.load(open(U+'exact-periodic-offsets.json'),parse_float=str)
    assert p['cells']==131072
    Z={}
    for i,v in p['sparse']:
        i=int(i); assert 0<=i<131072 and i not in Z; Z[i]=F(v)
    c=json.load(open(W+'central-certificate.json'),parse_float=str)
    rows=[]
    for r in c['functional_rows']:
        mu=F(r['multiplier']); n=int(r['certificate']['cells'])
        g=[F(x) for x in r['certificate']['functional_weights']]
        assert len(g)==n+1
        rows.append((mu,n,g))
    return dict(c0=c0,y2=y2,H=H,cos=cos,Z=Z,rows=rows,
                y2_raw=k['y2_exact'],mult_raw=[r['multiplier'] for r in c['functional_rows']])
