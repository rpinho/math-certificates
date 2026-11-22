"""Replay fixed type-K witnesses and run mutations with the same checker.
usage: E36_INPUTS=DIR python referee_check.py [CERT.json] [OUTDIR]   (defaults: ../certificates/certK_r105.json, .)
Writes OUTDIR/replay.json."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from pathlib import Path

from flint import ctx
from referee_data import GRID, read, rebuild, targets
from referee_kernel import SCALE, enclose


def endpoints(rows):
    edges = [(F(r['lo']),F(r['hi'])) for r in rows]
    gaps = [(a,b) for a,b in zip([F(0)]+[e[1] for e in edges],
                                 [e[0] for e in edges]+[F(1,160)]) if a!=b]
    assert all(lo<hi for lo,hi in edges)
    return gaps


def prefix_minimum(g):
    mins = []
    for x in g:
        mins.append(min(mins[-1],x) if mins else x)
    return mins


def check_row(row, g, pref, dup, N0, C, L):
    lo,hi,lam = [F(row[k]) for k in ('lo','hi','lam')]
    k0 = row['k0']
    slopes = list(map(F,row['slopes']))
    assert 0<=k0<=GRID and len(slopes)==GRID-k0
    # Anchor the right endpoint at zero. Work in units GRID*u.
    right = F(0)
    area = F(0)
    slack = F(pref[k0-1],SCALE)-abs(lam) if k0 else None
    bad = sum(F(g[i],SCALE)<abs(lam) for i in range(k0)) if k0 and slack<0 else 0
    crossings = 0
    for k in reversed(range(k0,GRID)):
        s = slopes[k-k0]
        delta = F(g[k],SCALE)-abs(lam-s)
        bad += delta<0
        slack = delta if slack is None else min(slack,delta)
        left = right-s
        if left*right < 0:
            crossings += 1
            area += (left**2+right**2)/(2*abs(s))
        else:
            area += (abs(left)+abs(right))/2
        right = left
    area += k0*abs(right)
    U = area/GRID**2
    margin = min(N0+C*m*m+lam*m/2 for m in (lo,hi))/dup - U/dup - L
    return dict(U=U, margin=margin, minimum_slack=slack, violations=bad,
                crossings=crossings, prefix_value=right/GRID, lo=lo, hi=hi)


def replay(rows,g,gu,dup):
    N0,C,L = targets()
    pref = prefix_minimum(g)
    def run(row):
        return check_row(row,g,pref,dup,N0,C,L)
    gaps = endpoints(rows)
    results = [run(row) for row in rows]
    def threshold_failures(increment):
        return [i for i,r in enumerate(results) if r['margin'] <= increment]
    target = [i for i,r in enumerate(results) if r['hi']>=F('0.000146') and r['lo']<=F(1,160)]
    worst = min(target,key=lambda i:results[i]['margin'])
    poorest = min(range(len(rows)),key=lambda i:results[i]['margin'])
    controls = {}
    for increment in ('1e-9','1e-6'):
        # Apply the same strict comparator, using exact bounds already computed.
        failed = threshold_failures(F(increment))
        controls['raise_'+increment] = dict(failed=failed,
            minimum=float(results[poorest]['margin']-F(increment)))
    flipped = run(dict(rows[worst],lam=str(-F(rows[worst]['lam']))))
    controls['flip'] = dict(bin=worst, violations=flipped['violations'], margin=float(flipped['margin']))
    changed = dict(rows[worst],slopes=list(rows[worst]['slopes']))
    # One spatial grid unit beyond a rigorous UPPER bound on g throughout this cell.
    old = changed['slopes'][-1]
    changed['slopes'][-1] = str(F(changed['lam'])+F(gu[-1],SCALE)+F(1,GRID))
    broken = run(changed)
    controls['slope'] = dict(bin=worst,cell=GRID-1,old=old,new=changed['slopes'][-1],
        upper=str(F(gu[-1],SCALE)),violations=broken['violations'],margin=float(broken['margin']))
    controls['drop'] = dict(bin=worst,gaps=endpoints(rows[:worst]+rows[worst+1:]))
    summary = dict(bins=len(rows),cell_checks=len(rows)*GRID,gaps=gaps,
        violations=sum(r['violations'] for r in results),nonzero_prefixes=sum(r['prefix_value']!=0 for r in results),
        nonpositive=len(threshold_failures(0)), min_slope_slack=float(min(r['minimum_slack'] for r in results)),
        crossings=sum(r['crossings'] for r in results),target_bins=len(target),target_bin=worst,
        target_margin=float(results[worst]['margin']),minimum_bin=poorest,minimum_margin=float(results[poorest]['margin']))
    return results,summary,controls


def main():
    import time
    ctx.prec = 220
    start = time.monotonic()
    c0,y2,cosines,grids,offsets,ledger = rebuild()
    print('Ledger completed', round(time.monotonic()-start,1),flush=True)
    g,gu,dlo,dup,count = enclose(c0,y2,cosines,grids,offsets)
    print('Quadrature completed',round(time.monotonic()-start,1), count,flush=True)
    here = Path(__file__).resolve().parent
    cert = Path(sys.argv[1]) if len(sys.argv) > 1 else here.parent / 'certificates' / 'certK_r105.json'
    outdir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('.')
    rows = read(cert)['bins']
    results,summary,controls = replay(rows,g,gu,dup)
    from decimal import Decimal, localcontext
    with localcontext() as c:
        c.prec=28
        dd = lambda q: str(Decimal(q.numerator)/Decimal(q.denominator))
        quad = dict(count,lower=str(dlo),upper=str(dup),display_lower=dd(dlo),display_upper=dd(dup),
                    width=dd(dup-dlo),producer_minus_upper=dd(F('2.627239663352680428')-dup))
    result = dict(ledger=ledger,quadrature=quad,summary=summary,controls=controls,
                  bins=results,elapsed_seconds=round(time.monotonic()-start,2))
    (outdir / 'replay.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
    print(quad,summary,controls,flush=True)
    assert len(rows)==94 and not any([summary[k] for k in ('gaps','violations','nonpositive','nonzero_prefixes')])
    assert all(controls['raise_'+inc]['failed'] for inc in ('1e-9','1e-6'))
    assert controls['flip']['violations'] and controls['slope']['violations'] and controls['drop']['gaps']


if __name__=='__main__':
    main()
