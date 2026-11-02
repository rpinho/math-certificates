"""Rigorous scalar verification for SPECTRAL_LEMMA.md. No search imports."""
import json
import hashlib
from fractions import Fraction as Q
from pathlib import Path
from flint import arb,fmpq,ctx

def I(q):
    q=Q(q)
    return arb(fmpq(q.numerator,q.denominator))

def pos(x,label):
    if not x>0:raise ArithmeticError((label,str(x)))

def verify_cover(path='spectral-cover.json'):
    raw=Path(path).read_bytes();d=json.loads(raw)
    assert d['model']=='spectral_geometric_mean_v2'
    assert d['zeta']=='3/50' and d['small_a']=='1/10000' and d['max_a']=='1/4'
    assert d['ell']=='6*sqrt(3)/25'
    ell=6*arb(3).sqrt()/25;zeta=I('3/50');delta=I('1/10000')
    pos(ell/4-zeta,'a=0')
    pos(ell-delta*(1+delta),'small x0<1')
    pos(4*ell-(1+delta)**2,'small polynomial')
    pos(I('1/1024')-2*delta/ell,'small ratio monotonicity')
    pos(I('1/1024')-delta*(1+delta)/(2*ell),'small d below bins')
    small=(ell/16).log()
    bins=['1/1024','1/256','1/64','1/16','1/4','1/2','3/4']
    for a,b in zip(bins,bins[1:]):
        a,b=I(a),I(b)
        gamma=1/b-delta/(ell*b*b);pos(gamma-1,'small ratio')
        measure=2/arb.pi()*(b.sqrt().asin()-a.sqrt().asin())
        small+=measure*gamma.log()
    small_gap=small-zeta.log();pos(small_gap,'small a geometric mean')
    cells=d['cells'];assert 0<len(cells)<20000
    cursor=Q('1/10000');sine_cache={};minimum=None;argmin=None
    for j,cell in enumerate(cells):
        a,b=Q(cell['a']),Q(cell['b']);N=cell['theta_cells']
        assert a==cursor and a<b<=Q(1,4);cursor=b
        assert isinstance(N,int) and 16<=N<=100000
        if N not in sine_cache:
            sine_cache[N]=[(ell*(arb.pi()*k/(2*N)).sin()**2).lower() for k in range(N)]
        floor=I(a*a);shift=I(b);lower=arb(0)
        for v in sine_cache[N]:
            alternative=arb(v)-shift
            # max of two certified lower endpoints is still a lower bound.
            f=arb(max(floor.lower(),alternative.lower()))
            pos(f,'positive h lower');lower+=f.log()
        gap=lower/N-zeta.log();pos(gap,('parameter cell',j))
        if minimum is None or gap<minimum:minimum=gap;argmin=j
    assert cursor==Q(1,4)
    return dict(status='PASS',backend='Arb',bits=ctx.prec,
                cover_sha256=hashlib.sha256(raw).hexdigest(),parameter_cells=len(cells),
                small_a_log_gap=str(small_gap),finite_log_gap=str(minimum),finite_worst_cell=argmin)

if __name__=='__main__':
    import argparse,time
    p=argparse.ArgumentParser();p.add_argument('--cover',default='spectral-cover.json');p.add_argument('--output',default='spectral-verification.json');a=p.parse_args()
    ctx.prec=192;start=time.monotonic();out=verify_cover(a.cover);out['seconds']=time.monotonic()-start
    print(json.dumps(out,indent=2));Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
