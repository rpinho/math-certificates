"""Extract the lower half-cell exactly. No tuning or numerical computation."""
import hashlib, json
from fractions import Fraction as F
from pathlib import Path
p=Path('certificates/parent-117-measure.json'); raw=p.read_bytes(); d=json.loads(raw)
py=F(d['Py'])/2
indices=[i for i,p in enumerate(d['pts']) if F(p[1])<py]
assert len(indices)==59 and len([i for i in indices if i<100])==50
out={k:d[k] for k in ('lam','Px','reach')}
out.update(Py=str(py),pts=[d['pts'][i] for i in indices],status='candidate, unrefereed',
 credit="Further hole-filling on Tomar's measure: the same insertion-and-refinement operation as his hf.py, applied by our own search scripts; Tomar Lemma 6.2 following Lin.")
Path('certificates/half59-measure.json').write_text(json.dumps(out,indent=1)+'\n')
Path('logs/half-extraction.json').write_text(json.dumps(dict(parent_sha256=hashlib.sha256(raw).hexdigest(),selection='0 <= y < parent Py/2',selected_indices_zero_based=indices,inherited_atoms=50,added_atoms=9,no_retuning=True),indent=2)+'\n')
# hf.py expects numeric JSON; conversion of the published rational data only.
p=Path('sources/tomar-v5/lowerbound/c2lower_1p70272.json'); raw=p.read_bytes(); t=json.loads(raw)
s=dict(Px=float(F(t['Px'])),Py=float(F(t['Py'])),pts=[[float(F(v)) for v in pt] for pt in t['pts']])
assert len(s['pts'])==50
Path('certificates/tomar50-float-start.json').write_text(json.dumps(s,indent=1)+'\n')
Path('logs/tomar-start-conversion.json').write_text(json.dumps(dict(source=str(p),source_sha256=hashlib.sha256(raw).hexdigest(),conversion='float(Fraction(value)), no optimization',atoms=50),indent=2)+'\n')
print('Fixed half-cell:',len(out['pts']),'atoms, Py',out['Py'])
