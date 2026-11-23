"""Exploratory constrained maximization. All reported maxima are numerical candidates."""
import itertools
import json
import warnings

import numpy as np
from scipy.optimize import minimize

CAP = 0.4001
A = np.array([[int((i-j) % 5 in (0, 2, 3)) for j in range(5)] for i in range(5)])


def scale(a, matrix):
    """Solve t_i (A t)_i = a_i by Newton on diagonally scaled equations."""
    t = np.sqrt(a) + 1e-35
    for _ in range(50):
        at = matrix @ t
        res = t * at - a
        if np.max(np.abs(res) / np.maximum(a, 1e-30)) < 3e-15:
            break
        delta = np.linalg.solve(np.diag(at) + t[:, None] * matrix, res)
        step = min(1., 0.9 / max(1e-60, np.max(delta/t)))
        t -= step * delta
    return t


def explore(d, r):
    rng = np.random.default_rng(1182)
    best = (-np.inf, None)
    runs = 0
    for k in (5, 4, 3):
        for support in itertools.combinations(range(5), k):
            images = [tuple(sorted((s*i+j)%5 for i in support)) for s in (-1,1) for j in range(5)]
            if min(images) != support:
                continue
            m = A[np.ix_(support, support)]
            def obj(a):
                a = np.maximum(a, 1e-18)
                t = scale(a, m)
                p = a @ m @ a
                v = (d-1)*(a @ np.log(a)) - d*(a @ np.log(t)) + d/2*(t @ m @ t-1) + r*np.log(p)
                grad = (d-1)*(1+np.log(a)) - d*np.log(t) + (2*r/p)*(m@a)
                return -v, -grad
            for rep in range(40 if k == 5 else 10):
                a = rng.dirichlet(np.ones(k))
                while np.max(a) > CAP:
                    a = (a + 1/k)/2
                fit = minimize(obj, a, jac=True, method='SLSQP', bounds=[(1e-16,CAP)]*k,
                               constraints=[dict(type='eq',fun=lambda a: a.sum()-1,jac=lambda a:np.ones(k))],
                               options=dict(ftol=2e-14,maxiter=130))
                if abs(fit.x.sum()-1)>1e-11:
                    continue
                full=np.zeros(5)
                full[list(support)]=fit.x
                runs+=1
                if -fit.fun>best[0]:
                    best=(-fit.fun, full.tolist())
    return dict(d=d,r=r,cap=CAP,value=best[0],profile=best[1],feasible_runs=runs)


if __name__ == '__main__':
    warnings.filterwarnings('ignore',category=RuntimeWarning,module='scipy.optimize')
    out = []
    for case in [(11,0),(10,.03),(10,0),(10,.015)]:
        result = explore(*case)
        print(json.dumps(result),flush=True)
        out.append(result)
    with open('float.json','w') as f:
        json.dump(out,f,indent=2)
