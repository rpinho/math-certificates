"""Fresh C82 floating helpers: exact-polynomial roots, root logs and Jensen.

Written for c82r5 from mathematical formulas, without third-party helper code.
Coefficient order at the file interface is descending. Search arithmetic is
heuristic; verify_interval.py supplies separately written ball verification.
"""
from functools import lru_cache
import json
import os
from pathlib import Path
import time
import numpy as np
from flint import ctx, fmpz_poly

ctx.prec = 256
ctx.threads = 1

def register(kind):
    with open('evidence/pids.jsonl', 'a') as f:
        f.write(json.dumps({'pid':os.getpid(),'kind':kind,'time':time.time(),
                            'nice':os.getpriority(os.PRIO_PROCESS,0)})+'\n')

def write_json(path, data):
    path = Path(path)
    temp = path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(data,indent=2)+'\n')
    temp.replace(path)

@lru_cache(maxsize=4096)
def root_tuple(coefficients):
    p = fmpz_poly(list(coefficients)[::-1])
    isolated = p.complex_roots()
    assert sum(m for _,m in isolated)==p.degree()
    return tuple(complex(r) for r,m in isolated for _ in range(m))

def roots(coefficients):
    return np.asarray(root_tuple(tuple(coefficients)),dtype=np.complex128)

def transformed_points(t):
    z = np.exp(2j*np.pi*np.asarray(t))
    return z*(1-z)

def root_logs(coefficients, points, rr=None):
    if rr is None:
        rr=roots(coefficients)
    values=np.full(len(points),np.log(abs(int(coefficients[0]))))
    for r in rr:
        values+=np.log(np.abs(points-r))
    return values

def mahler_T(coefficients, rr=None):
    if rr is None:
        rr=roots(coefficients)
    # Each root r of p lifts to the two roots of z(1-z)=r.
    delta=np.sqrt(1-4*rr+0j)
    lifted=np.concatenate(((1+delta)/2,(1-delta)/2))
    return float(np.log(abs(int(coefficients[0])))+np.log(np.maximum(1,np.abs(lifted))).sum())

def grid(n):
    return (np.arange(n)+.5)/(2*n)

def certificate_weights(cert):
    from fractions import Fraction
    D=sum((len(r['coeffs'])-1)*r['multiplicity'] for r in cert['denominator'])
    mu=np.array([r['multiplicity']/D for r in cert['denominator']])
    w=np.array([float(Fraction(r['q_rational'])/D) for r in cert['numerator']])
    return D,mu,w
