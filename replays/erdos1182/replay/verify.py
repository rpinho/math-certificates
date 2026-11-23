"""Standalone proof checker. No search, float arithmetic, numpy or producer imports."""
import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import gzip
from itertools import product
import json
import sys

from flint import arb, ctx, fmpq

ctx.prec = 160
CAP = F(4001,10000)
PARAMS = {'11':(11,F(0)), '503':(10,F(3,100))}
NEIGHBOURS = [(0,1),(1,2),(2,3),(3,4),(4,0)]
ALLOWED_CROSS = [(0,2),(0,3),(1,3),(1,4),(2,4)]


def need(test, message):
    if not test:
        raise ValueError(message)


@lru_cache(maxsize=4096)
def ball(q):
    return arb(fmpq(q.numerator,q.denominator))


@lru_cache(maxsize=4096)
def xlog(q):
    if q == 0:
        return arb(0)
    x = ball(q)
    if q <= F(1,4):
        # f decreases here. The limiting upper endpoint of f at zero is 0.
        lo, hi = x.lower(), x.upper()
        low_value = hi*hi.log()
        high_value = lo*lo.log() if lo>0 else arb(0)
        return low_value.union(high_value)
    return x*x.log()


def extreme_points(bounds):
    # Traverse each undirected cube edge from its all-lower free coordinate.
    points = set()
    for flags in product((0,1),repeat=5):
        corner = tuple(interval[f] for interval,f in zip(bounds,flags))
        remaining = 1-sum(corner)
        if remaining<0:
            continue
        for i,f in enumerate(flags):
            if f==0 and corner[i]+remaining<=bounds[i][1]:
                points.add(corner[:i]+(corner[i]+remaining,)+corner[i+1:])
    need(points,'nonempty slice must have a vertex')
    return points


@lru_cache(maxsize=32768)
def profile_terms(v, d, r):
    val = (d-1)*sum(xlog(q) for q in v)
    if r:
        p = 1-2*sum(v[i]*v[j] for i,j in NEIGHBOURS)
        val += ball(r)*ball(p).log()
    return val, tuple(ball(q) for q in v)


def verify_leaf(bounds, d, r, record):
    need(len(record)==7 and all(type(k) is int for k in record[1:]),'bad numeric leaf')
    _,ticks,*weight = record
    need(ticks<0 and min(weight)>0,'nonnegative bound or inadmissible dual weight')
    # Overall rescaling cancels in the normalised dual.
    z = sum(w*w for w in weight)+2*sum(weight[i]*weight[j] for i,j in ALLOWED_CROSS)
    const = d*arb(z).log()/2
    coeff = [-d*arb(w).log() for w in weight]
    ceiling = ball(F(ticks,10**10))
    points = extreme_points(bounds)
    for v in points:
        base, coords = profile_terms(v,d,r)
        expr = base+const+sum(x*y for x,y in zip(coords,coeff))
        need(expr<ceiling, f'claimed leaf bound fails: ticks={ticks}, vertex={v}, value={expr}')
    return len(points)


def check(filename, case, coverage=False):
    with gzip.open(filename,'rt') as stream:
        data=json.load(stream)
    need(data['case']==case,'wrong case')
    d,r=PARAMS[case]
    stream=iter(data['tree'])
    counts=Counter()
    worst=None
    def visit(box):
        nonlocal worst
        rec=next(stream,None)
        need(isinstance(rec,list) and len(rec)>0,'uncovered child or invalid node')
        tag=rec[0]
        counts[tag]+=1
        lo,hi=zip(*box)
        if tag=='S':
            need(len(rec)==2 and type(rec[1]) is int and 0<=rec[1]<5,'bad split')
            i=rec[1]
            mid=(lo[i]+hi[i])/2
            for interval in ((lo[i],mid),(mid,hi[i])):
                visit(box[:i]+(interval,)+box[i+1:])
        elif tag=='E':
            need(sum(lo)>1 or sum(hi)<1,'false empty slice')
        elif tag=='R':
            need(any(a>hi[0] for a in lo) or lo[4]>hi[1],'false orbit exclusion')
        elif tag=='L':
            need(sum(lo)<=1<=sum(hi),'empty numerical leaf')
            if not coverage:
                counts['vertices']+=verify_leaf(box,d,r,rec)
                worst=max(worst,rec[1]) if worst is not None else rec[1]
        else:
            raise ValueError(f'unknown tag {tag}')
    visit(((F(0),CAP),)*5)
    need(next(stream,None) is None,'extra nodes outside root')
    need(counts['S']+1==counts['E']+counts['R']+counts['L'],'incomplete tree')
    return dict(case=case,mode='coverage' if coverage else 'arb_and_coverage',
                cap=str(CAP),counts=dict(counts),worst_ticks=worst,tick_scale=10**10)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('case',choices=PARAMS)
    parser.add_argument('--file')
    parser.add_argument('--coverage',action='store_true')
    args=parser.parse_args()
    try:
        result=check(args.file or 'cert-'+args.case+'.json.gz',args.case,args.coverage)
    except (ValueError,ArithmeticError) as err:
        sys.exit('REJECT: '+str(err))
    print('PASS',json.dumps(result))
