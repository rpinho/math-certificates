import sys; sys.path.insert(0, '.')
import numpy as np
from rates_numeric import *
from scipy.optimize import minimize
cap = 0.4001; dl = 0.15
def toa(y):
    a = np.array(y[:4].tolist() + [0.0]); a[4] = 1 - a[:4].sum()
    return a
def inC(a):
    return (a.min() >= 0 and a.max() <= cap and a[0] >= a[3] + dl and a[2] >= a[3] + dl and a[3] >= a[4]
            and a[0] >= a[1] and a[2] >= a[1])
def neg(y):
    a = toa(np.asarray(y))
    if not inC(a): return 1.0
    return -case1_exact(a)[0]
rng = np.random.default_rng(int(sys.argv[1]))
res = []
for k in range(int(sys.argv[2])):
    while True:
        a = rng.dirichlet([1, 0.3, 1, 1, 0.3])
        a = np.array([rng.uniform(0.15, cap), rng.uniform(0, 0.1), rng.uniform(0.15, cap), rng.uniform(0, 0.25), 0]); a[4] = 1 - a[:4].sum()
        if inC(a): break
    r = minimize(neg, a[:4], method='Nelder-Mead', options={'xatol': 1e-8, 'fatol': 1e-12, 'maxiter': 700})
    res.append((-r.fun, toa(r.x).tolist()))
    print(k, -r.fun, np.round(toa(r.x), 6).tolist(), flush=True)
res.sort(reverse=True)
print('BEST', res[0])
