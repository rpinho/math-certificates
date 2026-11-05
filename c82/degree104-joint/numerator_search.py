"""Cheap complete-dual pricing of the public JSON numerator archive."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import numpy as np
from flint import fmpz_poly
from numerics import register,write_json,root_logs,roots,transformed_points
from joint_lp import JointLP,freeze

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--state',required=True);ap.add_argument('--dual',required=True)
    ap.add_argument('--prefix',required=True);ap.add_argument('--limit',type=int,default=32)
    a=ap.parse_args();register('numerator_pricing');start=time.monotonic();cpu=time.process_time()
    s=json.loads(Path(a.state).read_text());bank=json.loads(Path('prior_sources/union-factor-bank.json').read_text())
    dual=np.load(a.dual);support=dual['nu']>1e-18;nu=dual['nu'][support]
    points=transformed_points(dual['t'][support]);eta=float(dual['eta'])
    known={tuple(r['coeffs']) for r in s['numerator']};den=[fmpz_poly(r['coeffs'][::-1]) for r in s['denominator']]
    negative=[];priced=0
    for r in bank['numerator']:
        c=tuple(r['coeffs'])
        if c in known:continue
        p=fmpz_poly(list(c)[::-1])
        if any(p.gcd(q).degree()>0 for q in den):continue
        rc=float(nu@root_logs(c,points)+eta*p.degree());priced+=1
        if rc< -1e-9:negative.append({'name':r['name'],'coeffs':list(c),'rc':rc,'rc_per_degree':rc/p.degree()})
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
