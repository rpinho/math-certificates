"""Independent outward mpmath interval checker for the contact lemma."""
import json,hashlib
from pathlib import Path
from fractions import Fraction as Q
from mpmath import iv
from verify_spectral_interval import I,pos

def verify_cover(path='contact-cover.json'):
    raw=Path(path).read_bytes();d=json.loads(raw)
    assert d['model']=='contact_spectral_v3' and Q(d['zeta'])==Q(7,100)
    zeta=I('7/100');target=iv.ln(zeta);ell=I('252/625');delta=I('1/10000')
    pos(I('27/100')**2-zeta,'a threshold')
    pos(I('6/25')*(1-I('21/25')**2)-zeta,'b threshold')
    pos(ell/4-zeta,'a=0');pos(ell-delta*(1+delta),'x0 small')
    pos(4*ell-(1+delta)**2,'polynomial')
    pos(I('1/1024')-2*delta/ell,'small derivative')
    pos(I('1/1024')-delta*(1+delta)/(2*ell),'d bound')
    base=[Q(1,2**k) for k in range(10,0,-1)]+[Q(3,4)]
    bins=sorted(set(a+(b-a)*Q(j,4) for a,b in zip(base,base[1:]) for j in range(5)))
    small=iv.ln(ell/16)
    for a,b in zip(bins,bins[1:]):
        aa,bb=I(a),I(b);gamma=1/bb-delta/(ell*bb**2);pos(gamma-1,'gamma')
        alpha=iv.atan2(iv.sqrt(aa),iv.sqrt(1-aa));beta=iv.atan2(iv.sqrt(bb),iv.sqrt(1-bb))
        small+=2/iv.pi*(beta-alpha)*iv.ln(gamma)
    pos(small-target,'small integral')
    leaves=0;minimum=None;cache={}
    def walk(node,al,ah,bl,bh,depth=0):
        nonlocal leaves,minimum
        assert depth<40
        if 'split' in node:
            m=Q(node['mid']);axis=node['split']
            if axis=='a':
                assert al<m<ah
                walk(node['left'],al,m,bl,bh,depth+1);walk(node['right'],m,ah,bl,bh,depth+1)
            else:
                assert axis=='b' and bl<m<bh
                walk(node['left'],al,ah,bl,m,depth+1);walk(node['right'],al,ah,m,bh,depth+1)
            return
        n=node['theta_cells'];assert isinstance(n,int) and 16<=n<=100000
        leaves+=1;assert leaves<20000
        if n not in cache:cache[n]=[iv.sin(iv.pi*j/(2*n))**2 for j in range(n)]
        S=(I(al*al)+I('6/25')*(1-I(bh*bh))).a
        b0,b1=I(bl),I(bh)
        p0=I('6/25')*(1-b0)-I(ah);p1=I('6/25')*(1-b1)-I(ah)
        r0=I('12/25')*b0;r1=I('12/25')*b1
        total=iv.mpf(0)
        for x in cache[n]:
            t0=(p0+r0*x).a;t1=(p1+r1*x).a
            T=t0 if t0<=t1 else t1
            lower=S if S>=T else T
            pos(lower,'positive integrand');total+=iv.ln(iv.mpf(lower))
        gap=total/n-target;pos(gap,('leaf',leaves))
        if minimum is None or gap.a<minimum.a:minimum=gap
    walk(d['tree'],Q(1,10000),Q(27,100),Q(21,25),Q(1))
    return dict(status='PASS',backend='mpmath.iv',bits=iv.prec,cover_sha256=hashlib.sha256(raw).hexdigest(),parameter_cells=leaves,finite_log_gap=str(minimum),small_a_log_gap=str(small-target))

if __name__=='__main__':
    import time,argparse
    p=argparse.ArgumentParser();p.add_argument('--cover',default='contact-cover.json');p.add_argument('--output',default='contact-verification-interval.json');a=p.parse_args()
    iv.prec=240;start=time.monotonic();out=verify_cover(a.cover);out['seconds']=time.monotonic()-start
    print(json.dumps(out,indent=2));Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
