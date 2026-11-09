"""Parallel scheduling and exact coverage audit for the unchanged review checker.
All mathematical enclosures/point checks/integrals come from independent_verify.py,
written independently of search and the first checker. This wrapper adds no
floating acceptance test.
"""
import argparse,hashlib,json,multiprocessing,os,time
from pathlib import Path
from flint import arb
import independent_verify as V

_DATA=None
_ORDER=None
_MAXDEPTH=None

def one_cell(cell):
    d=_DATA;e=d['edges'];stack=[(e[cell],e[cell+1],0)];cover=[];tests=0;deepest=0
    while stack:
        lo,hi,depth=stack.pop();tests+=1
        if hi-lo>=V.F(1,5):
            mid=(lo+hi)/2;stack.extend([(mid,hi,depth+1),(lo,mid,depth+1)]);continue
        enc=V.interval_gap(d,lo,hi,_ORDER)
        if enc>0:
            cover.append([cell,str(lo),str(hi),str(enc.lower())]);deepest=max(deepest,depth)
        else:
            mid=(lo+hi)/2;point=V.point_gap(d,mid)
            assert not point<0,f'negative potential at {mid}: {point}'
            assert depth<_MAXDEPTH,f'unresolved support cell {cell}: {lo},{hi}'
            stack.extend([(mid,hi,depth+1),(lo,mid,depth+1)])
    cover.sort(key=lambda row:V.F(row[1]))
    assert V.F(cover[0][1])==e[cell] and V.F(cover[-1][2])==e[cell+1]
    assert all(V.F(u[2])==V.F(v[1]) for u,v in zip(cover,cover[1:]))
    return cell,cover,tests,deepest,os.getpid()

def main():
    global _DATA,_ORDER,_MAXDEPTH
    ap=argparse.ArgumentParser();ap.add_argument('certificate');ap.add_argument('--output',required=True);ap.add_argument('--workers',type=int,default=4);ap.add_argument('--order',type=int,default=8);ap.add_argument('--maxdepth',type=int,default=32);a=ap.parse_args()
    assert 1<=a.workers<=4 and __debug__
    started=time.time();_DATA=V.load_certificate(a.certificate);_ORDER=a.order;_MAXDEPTH=a.maxdepth;d=_DATA
    receipt={k:str(d[k]) for k in ['mass','trace','bound','degree','sha256']};receipt.update(nodes=len(d['edges']),support_cells=len(d['cells']),integrals=V.check_integrals(d),core_sha256=hashlib.sha256(Path(V.__file__).read_bytes()).hexdigest())
    allcover=[];seen=set();tests=0;maxdepth=0;workerids=set()
    with multiprocessing.get_context('fork').Pool(a.workers) as pool:
        Path(a.output+'.workers.json').write_text(json.dumps(dict(parent=os.getpid(),workers=[p.pid for p in pool._pool])))
        for cell,cover,n,depth,pid in pool.imap_unordered(one_cell,d['cells'],chunksize=1):
            assert cell not in seen;seen.add(cell);allcover.extend(cover);tests+=n;maxdepth=max(maxdepth,depth);workerids.add(pid)
            if len(seen)%100==0:
                progress=dict(completed_cells=len(seen),total_cells=len(d['cells']),pieces=len(allcover),seconds=time.time()-started)
                Path(a.output+'.progress').write_text(json.dumps(progress));print('COVER',json.dumps(progress),flush=True)
    # A second assembly audit checks exact coverage of every original support cell.
    assert seen==set(d['cells'])
    bycell={i:[] for i in d['cells']}
    for row in allcover:bycell[row[0]].append(row)
    sortedcover=[];minimum=None
    for cell in d['cells']:
        rows=sorted(bycell[cell],key=lambda row:V.F(row[1]));assert rows
        assert V.F(rows[0][1])==d['edges'][cell] and V.F(rows[-1][2])==d['edges'][cell+1]
        for k,row in enumerate(rows):
            assert V.F(row[1])<V.F(row[2])
            if k:assert V.F(rows[k-1][2])==V.F(row[1])
            lb=arb(row[3]);assert lb>0
            if minimum is None or lb<minimum:minimum=lb
        sortedcover.extend(rows)
    out=Path(a.output+'.cover.json');out.write_text(json.dumps(sortedcover,separators=(',',':')))
    receipt.update(status='PASS',pieces=len(sortedcover),tests=tests,max_depth=maxdepth,minimum_proven_lower=str(minimum),seconds=time.time()-started,support_left=str(d['edges'][d['cells'][0]]),support_right=str(d['edges'][d['cells'][-1]+1]),precision_bits=V.ctx.prec,order=a.order,workers=a.workers,worker_pids=sorted(workerids),coverage_sha256=hashlib.sha256(out.read_bytes()).hexdigest())
    assert hashlib.sha256(Path(a.certificate).read_bytes()).hexdigest()==d['sha256']
    Path(a.output).write_text(json.dumps(receipt,indent=2));print('PASS',json.dumps({k:v for k,v in receipt.items() if k!='integrals'}),flush=True)

if __name__=='__main__':main()
