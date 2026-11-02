"""Independent mpmath interval verification of the spectral scalar covering.

No Arb and no search imports. The proof is SPECTRAL_LEMMA.md.
"""
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from mpmath import iv


def I(q):
    q=Q(q)
    return iv.mpf(q.numerator)/iv.mpf(q.denominator)


def pos(x,label):
    if not x.a>0:raise ArithmeticError((label,str(x)))


def verify_cover(path='spectral-cover.json'):
    raw=Path(path).read_bytes();d=json.loads(raw)
    assert d['model']=='spectral_geometric_mean_v2'
    assert Q(d['zeta'])==Q(3,50) and Q(d['small_a'])==Q(1,10000)
    assert Q(d['max_a'])==Q(1,4) and d['ell']=='6*sqrt(3)/25'
    ell=6*iv.sqrt(3)/25;delta=I('1/10000');target=iv.ln(I('3/50'))
    pos(ell/4-I('3/50'),'zero a')
    pos(ell-delta*(1+delta),'small x0')
    pos(4*ell-(1+delta)**2,'small polynomial')
    pos(I('1/1024')-2*delta/ell,'ratio derivative')
    pos(I('1/1024')-delta*(1+delta)/(2*ell),'small d')
    bins=list(map(Q,['1/1024','1/256','1/64','1/16','1/4','1/2','3/4']))
    small=iv.ln(ell/16)
    for a,b in zip(bins,bins[1:]):
        aa,bb=I(a),I(b)
        gamma=1/bb-delta/(ell*bb**2);pos(gamma-1,'gamma')
        # asin(sqrt x) via atan2 uses a different elementary evaluation.
        angle_a=iv.atan2(iv.sqrt(aa),iv.sqrt(1-aa))
        angle_b=iv.atan2(iv.sqrt(bb),iv.sqrt(1-bb))
        small+=2*(angle_b-angle_a)/iv.pi*iv.ln(gamma)
    pos(small-target,'small geometric mean')
    cursor=Q(1,10000);cache={};worst=None;index=None
    assert 0<len(d['cells'])<20000
    for j,cell in enumerate(d['cells']):
        a,b=Q(cell['a']),Q(cell['b']);n=cell['theta_cells']
        assert a==cursor and a<b<=Q(1,4);cursor=b
        assert isinstance(n,int) and 16<=n<=100000
        if n not in cache:
            cache[n]=[(ell*iv.sin(iv.pi*k/(2*n))**2).a for k in range(n)]
        floor=I(a*a).a;shift=I(b).b;bound=iv.mpf(0)
        for s in cache[n]:
            alternative=(s-shift).a
            lower=floor if floor>=alternative else alternative
            pos(lower,'positive lower integrand')
            bound+=iv.ln(iv.mpf(lower))
        gap=bound/n-target;pos(gap,('parameter cell',j))
        if worst is None or gap.a<worst.a:worst=gap;index=j
    assert cursor==Q(1,4)
    return dict(status='PASS',backend='mpmath.iv',bits=iv.prec,
                cover_sha256=hashlib.sha256(raw).hexdigest(),parameter_cells=len(d['cells']),
                small_a_log_gap=str(small-target),finite_log_gap=str(worst),finite_worst_cell=index)


if __name__=='__main__':
    import argparse,time
    p=argparse.ArgumentParser();p.add_argument('--cover',default='spectral-cover.json');p.add_argument('--output',default='spectral-verification-interval.json');a=p.parse_args()
    iv.prec=240;start=time.monotonic();out=verify_cover(a.cover);out['seconds']=time.monotonic()-start
    print(json.dumps(out,indent=2));Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
