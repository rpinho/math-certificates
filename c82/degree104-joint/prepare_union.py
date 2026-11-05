"""Combine public coefficient JSON data and our own round-5 certificate."""
from pathlib import Path
import json
from numerics import certificate_weights, register, write_json

if __name__ == '__main__':
    register('prepare_union')
    public=json.loads(Path('prior_sources/pr280-v3-certificate.json').read_text())
    ours=json.loads(Path('prior_sources/round5-certificate.json').read_text())
    bank=json.loads(Path('prior_sources/factor-bank.json').read_text())
    _,mu,w=certificate_weights(public)
    state={'N':524288,'denominator':[],'numerator':[],'mu':[],'w':[]}
    for kind,weights in [('denominator','mu'),('numerator','w')]:
        known=set()
        for origin,source in [('public',public),('round5',ours),('bank',bank)]:
            if kind=='denominator' and origin=='bank':continue
            for i,r in enumerate(source[kind]):
                c=tuple(r['coeffs'])
                if c in known:continue
                known.add(c)
                state[kind].append({'name':r['name'],'coeffs':list(c)})
                state[weights].append(float((mu if kind=='denominator' else w)[i]) if origin=='public' else 0.)
    write_json('union-input.json',state)
    # Complete search bank retains older degree-44/60 starts plus all new denominators.
    for kind in ['denominator','numerator']:
        known={tuple(r['coeffs']) for r in bank[kind]}
        for source in [public,ours]:
            for r in source[kind]:
                if tuple(r['coeffs']) not in known:
                    bank[kind].append({'name':r['name'],'coeffs':r['coeffs']})
                    known.add(tuple(r['coeffs']))
    write_json('prior_sources/union-factor-bank.json',bank)
    print(json.dumps({k:len(state[k]) for k in ['denominator','numerator']}))
