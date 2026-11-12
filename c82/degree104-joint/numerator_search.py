"""Cheap complete-dual pricing of the public JSON numerator archive."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
from pathlib import Path
import time
import numpy as np
from flint import fmpz_poly
from numerics import register,write_json,root_logs,roots,transformed_points
from joint_lp import JointLP,freeze

def pricing_init(points,nu,eta,den):
    global _points,_nu,_eta,_den
    register('full_bank_pricing_worker')
    _points,_nu,_eta=points,nu,eta
    _den=[fmpz_poly(r['coeffs'][::-1]) for r in den]

def price_factor(r):
    c=tuple(r['coeffs']);p=fmpz_poly(list(c)[::-1])
    if any(p.gcd(q).degree()>0 for q in _den):return r,None
    return r,float(_nu@root_logs(c,_points)+_eta*p.degree())

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--state',required=True);ap.add_argument('--dual',required=True)
    ap.add_argument('--prefix',required=True);ap.add_argument('--limit',type=int,default=32)
    ap.add_argument('--workers',type=int,default=4)
    a=ap.parse_args();register('numerator_pricing');start=time.monotonic();cpu=time.process_time()
    s=json.loads(Path(a.state).read_text());bank=json.loads(Path('prior_sources/union-factor-bank.json').read_text())
    dual=np.load(a.dual);support=dual['nu']>1e-18;nu=dual['nu'][support]
    points=transformed_points(dual['t'][support]);eta=float(dual['eta'])
    known={tuple(r['coeffs']) for r in s['numerator']};den=[fmpz_poly(r['coeffs'][::-1]) for r in s['denominator']]
    negative=[];priced=0
    candidates=[r for r in bank['numerator'] if tuple(r['coeffs']) not in known]
    with ProcessPoolExecutor(max_workers=a.workers,initializer=pricing_init,initargs=(points,nu,eta,s['denominator'])) as pool:
        for r,rc in pool.map(price_factor,candidates,chunksize=32):
            if rc is None:continue
            c=tuple(r['coeffs']);priced+=1
            if rc< -1e-9:negative.append({'name':r['name'],'coeffs':list(c),'rc':rc,'rc_per_degree':rc/(len(c)-1)})
            if priced%50==0:
                write_json(a.prefix+'-screen.json',{'priced':priced,'negative':negative,'seconds':time.monotonic()-start})
                print(json.dumps({'priced':priced,'negative':len(negative),'seconds':time.monotonic()-start}),flush=True)
    negative.sort(key=lambda r:r['rc_per_degree'])
    added=[]
    for r in negative[:a.limit]:
        s['numerator'].append({'name':r['name'],'coeffs':r['coeffs']});s['w'].append(0.)
        added.append({k:v for k,v in r.items() if k!='coeffs'})
    write_json(a.prefix+'-screen.json',{'priced':priced,'negative':negative,'added':added,
                                      'seconds':time.monotonic()-start,'cpu_seconds':time.process_time()-cpu})
    if added:
        solved,audit=JointLP(s).solve(a.prefix);sha=freeze(solved,a.prefix+'-certificate.json')
        print(json.dumps({'objective':solved['lp'],'sha256':sha}),flush=True)
