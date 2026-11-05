"""Union of round-6 factors and Patankar v4 JSON data; no foreign code."""
from pathlib import Path
import json
from numerics import register,certificate_weights,write_json
register('prepare_union')
ours=json.loads(Path('prior_sources/round6-certificate.json').read_text())
public=json.loads(Path('prior_sources/pr280-v4-certificate.json').read_text())
bank=json.loads(Path('../c82r6/prior_sources/union-factor-bank.json').read_text())
sources=[('ours round6 final',ours),('#280 v4',public),('round6 union bank',bank)]
for path in sorted(Path('../c82r6/rounds').glob('*.json')):
    data=json.loads(path.read_text())
    if 'denominator' in data and 'numerator' in data:sources.append((str(path),data))
    if data.get('negative_candidates'):
        sources.append((str(path),{'denominator':data['negative_candidates'],'numerator':[]}))
_,mu,w=certificate_weights(ours)
state={'N':524288,'denominator':[],'numerator':[],'mu':[],'w':[]}
provenance={}
for kind,weights in [('denominator','mu'),('numerator','w')]:
    seen=set();provenance[kind]=[]
    for origin,source in sources:
        for i,r in enumerate(source[kind]):
            c=tuple(r['coeffs'])
            if c in seen:continue
            seen.add(c)
            state[kind].append({'name':r['name'],'coeffs':list(c)})
            state[weights].append(float((mu if kind=='denominator' else w)[i]) if origin=='ours round6 final' else 0.)
            provenance[kind].append({'name':r['name'],'origin':origin,'degree':len(c)-1})
write_json('union-input.json',state)
write_json('prior_sources/union-factor-bank.json',{k:state[k] for k in ['denominator','numerator']})
write_json('prior_sources/union-inventory.json',provenance)
print(json.dumps({k:len(state[k]) for k in ['denominator','numerator']}))
