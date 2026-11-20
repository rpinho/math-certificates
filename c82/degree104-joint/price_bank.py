"""Complete-bank pricing on the merged dual, using recomputed polynomial roots."""
import json,sys
from pathlib import Path
import numpy as np
from numerics import roots,root_logs,transformed_points,register,write_json

if __name__=='__main__':
    statefile,dualfile,out,part=sys.argv[1:]
    part=int(part);register('bank_pricing')
    state=json.loads(Path(statefile).read_text());data=np.load(dualfile)
    support=data['nu']!=0;points=transformed_points(data['t'][support]);mass=data['nu'][support];eta=float(data['eta'])
    known={tuple(r['coeffs']) for r in state['numerator']}
    bank=json.loads(Path('inputs/full-bank.json').read_text())['numerator'][part::4]
    cache=Path(f'rounds/roots-{part}.npy')
    sizes=np.array([len(r['coeffs'])-1 for r in bank])
    ends=np.r_[0,sizes.cumsum()]
    if not cache.exists():
        allroots=np.concatenate([roots(r['coeffs']) for r in bank])
        np.save(cache,allroots)
    allroots=np.load(cache,mmap_mode='r');assert len(allroots)==ends[-1]
    negative=[];minimum=None
    for row,start,end in zip(bank,ends,ends[1:]):
        c=row['coeffs']
        if tuple(c) in known: continue
        rc=float(mass@root_logs(c,points,allroots[start:end])+eta*(end-start))
        minimum=rc if minimum is None else min(rc,minimum)
        if rc< -1e-10:negative.append(dict(name=row['name'],coeffs=c,rc=rc))
    write_json(out,dict(bank_rows=len(bank),minimum_omitted_rc=minimum,negative_candidates=negative))
