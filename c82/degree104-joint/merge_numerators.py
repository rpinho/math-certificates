"""Append new LLL numerator columns, solve complete master and freeze packet."""
import argparse,json
from pathlib import Path
from numerics import register,write_json
from joint_lp import JointLP,freeze
from flint import fmpz_poly
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--state',required=True);ap.add_argument('--prefix',required=True);ap.add_argument('search',nargs='+');a=ap.parse_args();register('merge_lll_numerators')
    s=json.loads(Path(a.state).read_text());initial_count=len(s['numerator']);known={tuple(r['coeffs']) for r in s['numerator']};den=[fmpz_poly(r['coeffs'][::-1]) for r in s['denominator']];added=[]
    for path in a.search:
        for r in json.loads(Path(path).read_text())['negative_candidates']:
            c=tuple(r['coeffs'])
            if c in known:continue
            p=fmpz_poly(list(c)[::-1]);assert p.degree()>0 and all(p.gcd(q).degree()==0 for q in den)
            known.add(c);s['numerator'].append({'name':r['name'],'coeffs':list(c)});s['w'].append(0.)
            added.append({'name':r['name'],'source':path,'parent_rc':r['rc'],'degree':len(c)-1})
    bank=json.loads(Path('prior_sources/union-factor-bank.json').read_text())
    bank_known={tuple(r['coeffs']) for r in bank['numerator']}
    for r in s['numerator']:
        c=tuple(r['coeffs'])
        if c not in bank_known:bank['numerator'].append(r);bank_known.add(c)
    write_json('prior_sources/union-factor-bank.json',bank,compact=True)
    new=list(zip(s['numerator'][initial_count:],added))
    new.sort(key=lambda pair:pair[1]['parent_rc']/pair[1]['degree'])
    deferred=max(0,len(new)-32);new=new[:32]
    s['numerator']=s['numerator'][:initial_count]+[row for row,meta in new]
    s['w']=s['w'][:initial_count]+[0.]*len(new);added=[meta for row,meta in new]
    solved,audit=JointLP(s).solve(a.prefix);sha=freeze(solved,a.prefix+'-certificate.json')
    write_json(a.prefix+'-added.json',{'added':added,'deferred_to_full_bank_pricing':deferred,'old_lp':s['lp'],'new_lp':solved['lp'],'heuristic_gain':s['lp']-solved['lp'],'certificate_sha256':sha})
    print(json.dumps({'added':len(added),'lp':solved['lp'],'sha256':sha}),flush=True)
