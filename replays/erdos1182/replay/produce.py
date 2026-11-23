"""Floating certificate producer. The separate checker uses only integers and Arb."""
import argparse
import gzip
import itertools
import json
import math
from pathlib import Path

import numpy as np
from float_search import A, scale

GRID = 10000 * 2**30
CAP = 4001 * 2**30
WEIGHT = 2**40
TICKS = 10**10
BITS = np.array(list(itertools.product((0, 1), repeat=4)))
OTHER = [[i for i in range(5) if i != j] for j in range(5)]
CASES = {'11':(11,0), '503':(10,.03), '0':(10,0), '015':(10,.015)}
# Feasible already at cap .4. Neighbours of each other are indices 1 and 2.
CONTROL_POINT = np.array([.4,.0127,.18716,.4,.00014])


def vertices(lo, hi):
    points = []
    for j, axes in enumerate(OTHER):
        fixed = lo[axes] + BITS * (hi-lo)[axes]
        residual = GRID - fixed.sum(axis=1)
        valid = (lo[j] <= residual) & (residual <= hi[j])
        block = np.zeros((valid.sum(),5),dtype=np.int64)
        block[:,axes] = fixed[valid]
        block[:,j] = residual[valid]
        points.append(block)
    return np.unique(np.vstack(points),axis=0)/GRID


def trial(v, d, r):
    center = np.maximum(v.mean(axis=0),1e-14)
    t = scale(center, A)
    w = np.maximum(1,np.rint(t*WEIGHT)).astype(np.int64)
    t = w/WEIGHT
    entropy = (v*np.log(np.maximum(v,1e-300))).sum(axis=1)
    rates = ((d-1)*entropy - d*(v@np.log(t)) + d/2*np.log(t@A@t)
             + r*np.log(np.sum((v@A)*v,axis=1)))
    tick = math.ceil(np.max(rates)*TICKS)+2
    return tick, w.tolist()


def search(case):
    d,r = CASES[case]
    control = case in ('0','015')
    # Rotate by a reflection as needed to use the same representative sector.
    point = CONTROL_POINT[[0,4,3,2,1]] if CONTROL_POINT[1]<CONTROL_POINT[4] else CONTROL_POINT
    stack=[('',np.zeros(5,dtype=np.int64),np.full(5,CAP,dtype=np.int64))]
    records=[]
    counts={'bounds':0,'empty':0,'symmetry':0,'splits':0}
    worst=None
    while stack:
        path,lo,hi=stack.pop()
        if lo.sum()>GRID or hi.sum()<GRID:
            counts['empty']+=1
            records.append(['E'])
            continue
        if hi[0]<max(lo) or hi[1]<lo[4]:
            counts['symmetry']+=1
            records.append(['R'])
            continue
        v=vertices(lo,hi)
        tick,weights=trial(v,d,r)
        if tick<0:
            counts['bounds']+=1
            worst=max(tick,worst) if worst is not None else tick
            records.append(['L',tick,*weights])
            continue
        if control and len(path)>=24 and np.all(lo/GRID<=point) and np.all(point<=hi/GRID):
            info = dict(status='FAIL_TO_CLOSE',case=case,path=path,lower=lo.tolist(),upper=hi.tolist(),
                        denominator=GRID,trial_upper=tick/TICKS,positive_point=point.tolist(),
                        visited=sum(counts.values())+1,open_siblings=len(stack))
            Path('control-'+case+'.json').write_text(json.dumps(info,indent=2)+'\n')
            print(json.dumps(info),flush=True)
            return
        j=int(np.argmax(hi-lo))
        mid=(int(lo[j])+int(hi[j]))//2
        if mid in (lo[j],hi[j]):
            raise ArithmeticError('grid exhausted')
        left,right=hi.copy(),lo.copy()
        left[j]=right[j]=mid
        children=[(path+'0',lo,left),(path+'1',right,hi)]
        if control and point[j]*GRID>mid:
            children.reverse()
        stack.extend(reversed(children))
        records.append(['S',j])
        counts['splits']+=1
    if control:
        raise AssertionError('negative control unexpectedly closed')
    with gzip.open('cert-'+case+'.json.gz','wt') as f:
        json.dump({'case':case,'tree':records},f,separators=(',',':'))
    print(json.dumps(dict(case=case,counts=counts,worst_ticks=worst,scale=TICKS)),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('case',choices=CASES)
    search(parser.parse_args().case)
