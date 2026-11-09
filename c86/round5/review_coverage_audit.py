#!/usr/bin/env python3
"""Exact endpoint audit, corrupted-partition controls, optional stronger floor.
The input partition comes from independent_verify.py's completed run.
"""
import argparse,copy,hashlib,json,time
from fractions import Fraction as F
from pathlib import Path
from flint import arb
import independent_verify as V

def audit(certificate,cover):
    c=json.loads(Path(certificate).read_text())
    e=list(map(F,c['edges']));h=list(map(F,c['node_densities']))
    expected={i for i in range(len(e)-1) if h[i]>0 or h[i+1]>0}
    grouped={}
    for i,l,r,lower in cover:
        assert type(i) is int and i in expected, 'wrong parent cell'
        l,r=F(l),F(r)
        assert e[i]<=l<r<=e[i+1], 'leaf outside parent or reversed'
        assert arb(lower)>0, 'nonpositive saved lower bound'
        grouped.setdefault(i,[]).append((l,r))
    assert set(grouped)==expected, 'missing support cell'
    for i,leaves in grouped.items():
        leaves.sort()
        assert leaves[0][0]==e[i], 'wrong left endpoint'
        assert leaves[-1][1]==e[i+1], 'wrong right endpoint'
        assert all(x[1]==y[0] for x,y in zip(leaves,leaves[1:])), 'gap or overlap'
    return dict(cells=len(expected),pieces=len(cover),left=str(e[min(expected)]),right=str(e[max(expected)+1]))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--strengthen',action='store_true');a=p.parse_args()
    start=time.time();cert='target-certificate.json';coverpath='independent-receipt.json.cover.json'
    cover=json.loads(Path(coverpath).read_text());receipt=json.loads(Path('independent-receipt.json').read_text())
    assert receipt['status']=='PASS'
    assert hashlib.sha256(Path(cert).read_bytes()).hexdigest()==receipt['sha256']
    assert hashlib.sha256(Path(coverpath).read_bytes()).hexdigest()==receipt['coverage_sha256']
    results={'original':audit(cert,cover),'controls':[]}
    corruptions={
        'deleted-leaf':lambda c:c.pop(len(c)//2),
        'endpoint-moved-by-1e-30':lambda c:c[0].__setitem__(1,str(F(c[0][1])+F(1,10**30))),
        'wrong-parent':lambda c:c[0].__setitem__(0,c[0][0]+1),
        'nonpositive-bound':lambda c:c[0].__setitem__(3,'-1e-30')}
    for name,mut in corruptions.items():
        bad=copy.deepcopy(cover);mut(bad)
        try:audit(cert,bad)
        except AssertionError as ex:results['controls'].append({'name':name,'status':'REJECTED','reason':str(ex)})
        else:raise AssertionError('partition control accepted: '+name)
    print('COVERAGE AUDIT',results,flush=True)
    if a.strengthen:
        data=V.load_certificate(cert);floor=V.B(F(1,10**6));new=[];tests=0
        for i,l,r,lower in cover:
            if arb(lower)>floor:
                new.append([i,l,r,lower]);continue
            todo=[(F(l),F(r),0)]
            while todo:
                lo,hi,depth=todo.pop();tests+=1
                q=V.interval_gap(data,lo,hi)
                if q>floor:
                    new.append([i,str(lo),str(hi),str(q.lower())])
                else:
                    assert depth<25,'stronger floor unresolved'
                    mid=(lo+hi)/2;todo.extend([(lo,mid,depth+1),(mid,hi,depth+1)])
            if len(new)%500==0:print('STRENGTHEN',len(new),tests,flush=True)
        results['strengthened']=audit(cert,new)
        results['strengthened'].update(floor='1/1000000',new_interval_tests=tests,
            minimum_proven_lower=str(min(arb(row[3]).lower() for row in new)))
        Path('strengthened-cover.json').write_text(json.dumps(new,separators=(',',':')))
        results['strengthened']['coverage_sha256']=hashlib.sha256(Path('strengthened-cover.json').read_bytes()).hexdigest()
    results['seconds']=time.time()-start
    Path('coverage-audit.json').write_text(json.dumps(results,indent=2))
    print('AUDIT PASS',json.dumps(results),flush=True)
