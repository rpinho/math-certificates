"""Direct substitution and reciprocal images in the raw polynomial variable X."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
from flint import fmpz_poly
from numerics import root_logs,transformed_points,register,write_json

def norm(p):
    if p.leading_coefficient()<0:p=-p
    return tuple(int(x) for x in p.coeffs())
def orbit(p):
    seen={norm(p)};todo=list(seen)
    while todo:
        c=todo.pop();p=fmpz_poly(list(c))
        for q in (p(fmpz_poly([1,-1])),fmpz_poly(list(c[::-1]))):
            key=norm(q)
            if key not in seen:seen.add(key);todo.append(key)
    assert len(seen)<=6
    return seen
def main():
    state,dual,out=sys.argv[1:];register('orbit_pricing')
    s=json.loads(Path(state).read_text());v6=json.loads(Path('inputs/v6.json').read_text())
    d=np.load(dual);keep=d['nu']!=0;mass=d['nu'][keep];points=transformed_points(d['t'][keep])
    known={tuple(r['coeffs']) for r in s['numerator']}
    seeds=v6['numerator'][-16:]+[r for r,w in zip(s['numerator'],s['w']) if w>0 and len(r['coeffs'])>24]
    candidates={}
    for r in seeds:
        p=fmpz_poly(r['coeffs'][::-1])
        for c in orbit(p):candidates[c[::-1]]=(r['name'],'orbit')
    # Direct coefficient neighbours around the degree-42 v6 addition.
    p=next(r for r in v6['numerator'][-16:] if len(r['coeffs'])==43)
    for j in range(1,43):
        for step in (-1,1):
            c=p['coeffs'].copy();c[j]+=step;candidates[tuple(c)]=(p['name'],'neighbour')
    negatives=[];counts={}
    for c,(seed,method) in candidates.items():
        if c in known or not c[-1] or not sum(c):continue
        rc=float(mass@root_logs(c,points)+float(d['eta'])*(len(c)-1))
        counts[method]=counts.get(method,0)+1
        if rc < -1e-10:
            name='N82r12_'+hashlib.sha256(str(c).encode()).hexdigest()[:12]
            negatives.append(dict(name=name,coeffs=c,rc=rc,seed=seed,method=method))
    write_json(out,dict(priced=counts,negative_candidates=negatives))
if __name__=='__main__':main()
