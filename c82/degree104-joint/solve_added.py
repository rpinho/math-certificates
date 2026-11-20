"""Extend the previous basis columns and re-solve using the full original grid."""
import json,sys
from pathlib import Path
from flint import fmpz_poly
from joint_lp import JointLP,freeze
from numerics import register,write_json
def main():
    statefile,prefix,kind,*files=sys.argv[1:];register('merge')
    state=json.loads(Path(statefile).read_text());other='denominator' if kind=='numerator' else 'numerator'
    known={tuple(r['coeffs']) for r in state[kind]}
    candidates=sorted((r for file in files for r in json.loads(Path(file).read_text())['negative_candidates']),key=lambda r:r['rc']/(len(r['coeffs'])-1))
    opposite=[fmpz_poly(r['coeffs'][::-1]) for r in state[other]]
    added=[]
    for r in candidates:
        c=tuple(r['coeffs'])
        if c in known:continue
        if not c[-1] or not sum(c):continue
        p=fmpz_poly(list(reversed(c)))
        if any(p.gcd(q).degree() for q in opposite):continue
        known.add(c);state[kind].append(dict(name=r['name'],coeffs=c))
        state['w' if kind=='numerator' else 'mu'].append(0.);added.append(r['name'])
        if len(added)>=32:break
    write_json(prefix+'-added.json',added)
    if added:
        solved,_=JointLP(state).solve(prefix);freeze(solved,prefix+'-certificate.json')
if __name__=='__main__':main()
