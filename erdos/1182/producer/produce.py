"""Produce profile-cover certificates using pairing entropy and occupancy bounds."""

import argparse
import gzip
import itertools
import json
import math
import resource
import time
from pathlib import Path

from flint import arb, ctx
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.special import xlogy

from reference_table import ALLOWED, naive

GRID = 10000 * 2**20
CAP = 4001 * 2**20
GAP = GRID * 3 // 20
TILT = 10**12
CLAIM = TILT // 1000
CORNERS = list(itertools.product((0, 1), repeat=4))
VERTEX_SELECTORS = [
    (i, [j for j in range(5) if i != j], np.array(CORNERS).T)
    for i in range(5)
]
ctx.prec = 160


def narrow(lo, hi, order):
    """Tighten box coordinates by halfspaces and the unit mass equation."""
    lo, hi = list(lo), list(hi)
    relations = []
    if order == "a":
        relations = [(0,1,0), (1,2,0), (1,3,0), (1,4,0)]
    if order in ("b","c"):
        relations = [(j,k,0) for j in (0,2) for k in (1,3,4)] + [(3,4,0)]
    if order == "c":
        relations += [(0,3,GAP), (2,3,GAP)]
    for _ in range(3):
        for j, k, gap in relations:
            lo[j] = max(lo[j], lo[k]+gap)
            hi[k] = min(hi[k], hi[j]-gap)
        for j in range(5):
            lo[j] = max(lo[j], GRID-sum(hi[k] for k in range(5) if j != k))
            hi[j] = min(hi[j], GRID-sum(lo[k] for k in range(5) if j != k))
        if any(a>b for a,b in zip(lo,hi)) or sum(lo)>GRID or sum(hi)<GRID:
            return None
    if order == "b" and min(lo[0],lo[2])-hi[3] > GAP:
        return None
    return lo, hi


def vertices(lo, hi):
    lo, hi = np.array(lo), np.array(hi)
    out = []
    for free, fixed, patterns in VERTEX_SELECTORS:
        block = np.empty((5, 16), dtype=np.int64)
        block[fixed] = np.where(patterns, hi[fixed,None], lo[fixed,None])
        block[free] = GRID-block[fixed].sum(axis=0)
        out.append(block[:, (lo[free] <= block[free]) & (block[free] <= hi[free])].T)
    return np.unique(np.concatenate(out), axis=0)


def pick_tilt(lo, hi):
    lo, hi = np.array(lo), np.array(hi)
    v = lo + (hi-lo)*(GRID-lo.sum())/max(1,(hi-lo).sum())
    a = np.maximum(v/GRID, 1e-12)
    a /= a.sum()
    _, q = naive(a)
    return [max(1, round(float(t)*TILT)) for t in np.sqrt(q.diagonal())]


def try_naive(lo, hi, t_int):
    t = np.array(t_int)/TILT
    w = ALLOWED * t[:,None] * t
    z = w.sum()
    v = vertices(lo,hi)/GRID
    rate = (9*xlogy(v,v)-10*v*np.log(t)).sum(axis=1).max()+5*math.log(z)
    return math.ceil((rate+2e-11)*TILT), w/z


def binary_kl(x, b):
    return float(xlogy(x,x/b)+xlogy(1-x,(1-x)/(1-b)))


def upper_limit(b, budget):
    if binary_kl(1.,b) <= budget:
        return 1.
    return brentq(lambda x: binary_kl(x,b)-budget, b, 1., xtol=1e-14)


def refine(case, lo, hi, raw, b):
    upper = raw/TILT
    budget = (upper + CLAIM/TILT)/5 + 2e-10
    a0 = lo[0]/GRID
    if case == "case1":
        high = min(hi[0], hi[3], math.ceil(GRID*upper_limit(2*b[0,3],budget)/2))
        if high <= 0 or a0 <= 0:
            return None
        x = min(1., high/(GRID*a0))
        penalty = a0*math.log1p(-(1-x)**10)
        return [high] if upper+penalty < -CLAIM/TILT-2e-9 else None

    h02 = min(hi[0], hi[2], math.ceil(GRID*upper_limit(2*b[0,2],budget)/2))
    h24 = min(hi[2], hi[4], math.ceil(GRID*upper_limit(2*b[2,4],budget)/2))
    if lo[2] <= h24 or not a0:
        return None
    p = min(1., h02/(lo[2]-h24))
    m = 9*h24/GRID

    def bound(u):
        f = 1-(1-u)**10
        beta = 10*(1-u)**9/f
        return a0*(math.log(f)-beta*u)+10*m*math.log1p(p*math.expm1(beta/10))

    fit = minimize_scalar(bound, bounds=(.08,.87), method="bounded")
    u = round(fit.x*TILT)
    return [h02,h24,u] if upper+bound(u/TILT) < -CLAIM/TILT-2e-9 else None


def abox(x):
    return arb(x)/GRID


def ascaled(x):
    return arb(x)/TILT


def bounded_leaf(lo,hi,t_int,raw):
    """Check the numerical choice with directed rounding before emitting it."""
    t = list(map(ascaled,t_int))
    z = sum(t[i]*t[j] for i in range(5) for j in range(5) if ALLOWED[i,j])
    constants = [-10*x.log() for x in t]
    cache = {}

    def term(i,x):
        if x == 0:
            return arb(0)
        key = i,x
        if key not in cache:
            y = abox(x)
            cache[key] = y*(9*y.log()+constants[i])
        return cache[key]

    cutoff = ascaled(raw)-5*z.log()
    return all(sum(term(i,int(x)) for i,x in enumerate(v)) < cutoff for v in vertices(lo,hi))


def build(case, max_seconds):
    start = time.monotonic()
    records = []
    totals = {"split":0,"empty":0,"naive":0,"occupancy":0}
    deadline = start+max_seconds

    def visit(lo,hi,depth):
        if time.monotonic() >= deadline:
            raise TimeoutError((case,depth,totals))
        if depth > 110:
            raise ArithmeticError((case, "depth", lo,hi,totals))
        if case == "naive_ab":
            boxes = [box for order in ("a","b") if (box:=narrow(lo,hi,order))]
        else:
            box = narrow(lo,hi,"c")
            boxes = [box] if box else []
        if not boxes:
            records.append(["X"])
            totals["empty"] += 1
            return
        boxlo = [min(b[0][i] for b in boxes) for i in range(5)]
        boxhi = [max(b[1][i] for b in boxes) for i in range(5)]
        t = pick_tilt(boxlo,boxhi)
        raw, b = try_naive(boxlo,boxhi,t)
        if raw <= -CLAIM and bounded_leaf(boxlo,boxhi,t,raw):
            records.append(["N",t,raw,-CLAIM])
            totals["naive"] += 1
            return
        if case != "naive_ab" and raw < 0.03*TILT:
            payload = refine(case,boxlo,boxhi,raw,b)
            if payload and bounded_leaf(boxlo,boxhi,t,raw):
                records.append(["C",t,raw,payload,-CLAIM])
                totals["occupancy"] += 1
                return
        j = max(range(5), key=lambda x: boxhi[x]-boxlo[x])
        cut = (boxlo[j]+boxhi[j])//2
        if not lo[j] < cut < hi[j]:
            raise ArithmeticError(("inconclusive",case,lo,hi,raw))
        records.append(["S",j,cut])
        totals["split"] += 1
        if totals["split"] % 4096 == 0:
            print(case,"checkpoint",totals,"elapsed",round(time.monotonic()-start,2),flush=True)
        upper = list(hi)
        upper[j] = cut
        visit(lo,upper,depth+1)
        lower = list(lo)
        lower[j] = cut
        visit(lower,hi,depth+1)

    visit([0]*5,[CAP]*5,0)
    stats = dict(totals,elapsed_seconds=round(time.monotonic()-start,3),
                 peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(case,stats,flush=True)
    doc = {"format":2 if case == "case1" else 1,"case":case,"root":[[0]*5,[CAP]*5],"grid":GRID,
           "tilt_scale":TILT,"claim":-CLAIM,"records":records}
    with gzip.GzipFile(f"cert_{case}.json.gz", "wb", mtime=0) as f:
        f.write((json.dumps(doc,separators=(",",":"))+"\n").encode())
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case",choices=["naive_ab","case1","case2","all"])
    parser.add_argument("--seconds",type=int,default=1200)
    args = parser.parse_args()
    start = time.monotonic()
    cases = ("naive_ab","case1","case2") if args.case == "all" else (args.case,)
    stats = {}
    for case in cases:
        stats[case] = build(case,args.seconds-(time.monotonic()-start))
    Path("producer_stats.json").write_text(json.dumps(stats,indent=2)+"\n")
