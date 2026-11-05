"""Merge negative-price factors, re-solve the joint LP, freeze exact weights."""
import argparse
import hashlib
import json
from pathlib import Path
import time
from flint import fmpz_poly
from joint_lp import JointLP,freeze
from numerics import register,write_json

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--state',required=True);ap.add_argument('--prefix',required=True)
    ap.add_argument('search',nargs='+');a=ap.parse_args();register('merge_and_solve')
    state=json.loads(Path(a.state).read_text());known={tuple(r['coeffs']) for r in state['denominator']};added=[]
    for path in a.search:
        search=json.loads(Path(path).read_text())
        for r in search['negative_candidates']:
            # Factorization is exact. Price the complete monic polynomial as found.
            c=tuple(r['coeffs'])
            if c in known:continue
            name='C82r7_'+hashlib.sha256(str(c).encode()).hexdigest()[:12]
            assert c[0]==1
            p=fmpz_poly(list(c)[::-1]);assert p.degree()==104
            assert all(p.gcd(fmpz_poly(q['coeffs'][::-1])).degree()==0 for q in state['numerator'])
            state['denominator'].append({'name':name,'coeffs':list(c)})
            state['mu'].append(0.);known.add(c)
            added.append({'name':name,'source':path,'parent_rc':r['rc']})
    solved,audit=JointLP(state).solve(a.prefix)
    sha=freeze(solved,a.prefix+'-certificate.json')
    write_json(a.prefix+'-added.json',{'added':added,'certificate_sha256':sha,'old_lp':state['lp'],
                                     'new_lp':solved['lp'],'heuristic_gain':state['lp']-solved['lp']})
    print(json.dumps({'new_lp':solved['lp'],'sha256':sha,'added':len(added)}),flush=True)
