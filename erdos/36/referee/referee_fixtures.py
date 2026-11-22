"""Construct lawful rational step densities and compute both signs of every lag."""
import json, os, sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from referee_data import targets


def design(n=128):
    # Fit a symmetric example only. Every reported inequality below is recomputed
    # on a rational example, including negative shifts, without this objective.
    width = 2/n
    half = n//2
    def values(x):
        h = np.r_[x[:half], x[:half][::-1]]
        return np.correlate(1-h,h,'full')[n-1:]*width
    def jac(x):
        h = np.r_[x[:half],x[:half][::-1]]
        j = np.zeros((n,n))
        for k in range(n):
            j[k,:n-k] += 1-h[k:]
            j[k,k:] -= h[:n-k]
        return np.column_stack((-width*(j[:,:half]+j[:,half:][:,::-1]), np.ones(n)))
    x = np.linspace(.99,.01,half)
    x = np.r_[x,.6]
    result = minimize(lambda x:x[-1],x,jac=lambda x:np.r_[np.zeros(half),1],
        bounds=[(0,1)]*(half+1),constraints=[
            dict(type='eq',fun=lambda x:sum(x[:half])-n/4,jac=lambda x:np.r_[np.ones(half),0]),
            dict(type='ineq',fun=lambda x:x[-1]-values(x), jac=jac)],
        method='SLSQP', options={'ftol':1e-11,'maxiter':250})
    # Round and restore mass by largest fractional parts.
    den = 10**10
    vals = np.clip(result.x[:half],0,1)*den
    units = np.floor(vals).astype(np.int64)
    residue = den*n//4-int(units.sum())
    assert 0<=residue<=half
    units[np.argsort(units-vals)[:residue]] += 1
    v = [F(int(p),den) for p in units]
    return v+v[::-1],str(result.message)


def direct(h):
    n = len(h)
    width = F(2,n)
    assert min(h)>=0 and max(h)<=1 and width*sum(h)==1
    p = [width*sum(h[i]*(1-h[i+k]) for i in range(max(0,-k),min(n,n-k)))
         for k in range(-n,n+1)]
    # p is affine on every mesh interval, including both support edges.
    mass = width*sum(p)
    moment = width**2*sum(k*q for k,q in zip(range(-n,n+1),p,strict=True))
    density_mean = 2-width**2*sum((2*i+1)*v for i,v in enumerate(h))
    assert mass==1 and moment==density_mean
    return moment,max(p),p.index(max(p))-n


def main():
    outdir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')   # dir holding replay.json from referee_check.py
    replay = json.loads((outdir / 'replay.json').read_text())
    bins = replay['bins']
    L = targets()[2]
    base,status = design()
    n = len(base)
    fixtures = [('constant',[F(1,2)]*2),('two halves',[F(501,1000),F(499,1000)])]
    for m in [F(0),F('0.00007'),F('0.000146'),F('-0.000146'),F(1,160)]:
        h = [(1-abs(m))*x+abs(m)*int((i<n//2) if m>=0 else (i>=n//2)) for i,x in enumerate(base)]
        fixtures.append(('symmetric design tilted to '+str(m),h))
    output = []
    for name,h in fixtures:
        m,M,peak = direct(h)
        idx = [i for i,r in enumerate(bins) if F(r['lo'])<=abs(m)<=F(r['hi'])]
        assert idx
        B = max(L+F(bins[i]['margin']) for i in idx)
        output.append(dict(name=name,m=str(m),M=str(M),M_display=float(M),peak_grid_shift=peak,
                           bins=idx,B_display=float(B),slack=float(M-B),pass_exact=(M>B)))
    (outdir / 'fixtures.json').write_text(json.dumps(dict(symmetric_half=list(map(str,base[:n//2])),
        optimizer_status=status,fixtures=output),indent=2)+'\n')
    print(status)
    for r in output:
        print(r)
    assert all(r['pass_exact'] for r in output)


if __name__=='__main__':
    main()
