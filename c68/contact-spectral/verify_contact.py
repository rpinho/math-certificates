"""Arb verification of CONTACT_SPECTRAL_LEMMA.md. No search imports."""
import json,hashlib
from fractions import Fraction as Q
from pathlib import Path
from flint import arb,ctx
from verify_spectral import I,pos

def verify_cover(path='contact-cover.json'):
    raw=Path(path).read_bytes();d=json.loads(raw)
    assert d['model']=='contact_spectral_v3' and Q(d['zeta'])==Q(7,100)
    zeta=I('7/100');ell=I('252/625');delta=I('1/10000');target=zeta.log()
    pos(I('27/100')**2-zeta,'large a')
    pos(I('6/25')*(1-I('21/25')**2)-zeta,'small b')
    pos(ell/4-zeta,'zero a');pos(ell-delta*(1+delta),'small x0')
    pos(4*ell-(1+delta)**2,'small polynomial')
    pos(I('1/1024')-2*delta/ell,'small derivative')
    pos(I('1/1024')-delta*(1+delta)/(2*ell),'small d')
    coarse=[Q(1,2**k) for k in range(10,0,-1)]+[Q(3,4)]
    bins=sorted(set([a+(b-a)*Q(j,4) for a,b in zip(coarse,coarse[1:]) for j in range(5)]))
    small=(ell/16).log()
    for a,b in zip(bins,bins[1:]):
        aa,bb=I(a),I(b);gamma=1/bb-delta/(ell*bb**2)
        pos(gamma-1,'small gamma')
        small+=2/arb.pi()*(bb.sqrt().asin()-aa.sqrt().asin())*gamma.log()
    pos(small-target,'small a integral')
    cache={};leaves=0;worst=None
    def walk(node,al,ah,bl,bh,depth=0):
        nonlocal leaves,worst
        assert depth<40
        if 'split' in node:
            axis=node['split'];m=Q(node['mid'])
            if axis=='a':
                assert al<m<ah
                walk(node['left'],al,m,bl,bh,depth+1);walk(node['right'],m,ah,bl,bh,depth+1)
            else:
                assert axis=='b' and bl<m<bh
                walk(node['left'],al,ah,bl,m,depth+1);walk(node['right'],al,ah,m,bh,depth+1)
            return
        n=node['theta_cells'];assert isinstance(n,int) and 16<=n<=100000
        leaves+=1;assert leaves<20000
        if n not in cache:cache[n]=[(arb.pi()*j/(2*n)).sin()**2 for j in range(n)]
        floor=(I(al*al)+I('6/25')*(1-I(bh*bh))).lower()
        aa=I(ah);b0=I(bl);b1=I(bh);mean=arb(0)
        p0=I('6/25')*(1-b0)-aa;p1=I('6/25')*(1-b1)-aa
        r0=I('12/25')*b0;r1=I('12/25')*b1
        for x in cache[n]:
            t0=(p0+r0*x).lower()
            t1=(p1+r1*x).lower()
            lower=arb(max(floor,min(t0,t1)));pos(lower,'positive h')
            mean+=lower.log()
        gap=mean/n-target;pos(gap,('leaf',leaves))
        if worst is None or gap<worst:worst=gap
    walk(d['tree'],Q(1,10000),Q(27,100),Q(21,25),Q(1))
    return dict(status='PASS',backend='Arb',bits=ctx.prec,cover_sha256=hashlib.sha256(raw).hexdigest(),parameter_cells=leaves,finite_log_gap=str(worst),small_a_log_gap=str(small-target))

if __name__=='__main__':
    import time,argparse
    p=argparse.ArgumentParser();p.add_argument('--cover',default='contact-cover.json');p.add_argument('--output',default='contact-verification.json');a=p.parse_args()
    ctx.prec=192;start=time.monotonic();out=verify_cover(a.cover);out['seconds']=time.monotonic()-start
    print(json.dumps(out,indent=2));Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
