"""Numerical sanity checks, independent of the interval proof of the bound."""
import argparse
import ast
import itertools
import json
import os
from pathlib import Path
import time

import numpy as np
from flint import ctx
from core import Lib
from cvp_fixed import enumerate_cvp


def check_enumerator():
    functions=[]
    for path in ['cvp_fixed.py']:
        tree=ast.parse(Path(path).read_text())
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='enumerate_cvp')
        functions.append(ast.dump(node,include_attributes=False))
    assert len(set(functions))==1
    rng=np.random.default_rng(80282)
    coords=np.array(list(itertools.product(range(-8,9),repeat=3)))
    receipts=[]
    for i in range(16):
        R=np.triu(rng.uniform(-.8,.8,(3,3)))
        np.fill_diagonal(R,rng.uniform(.8,1.7,3)*rng.choice([-1,1],3))
        y=rng.uniform(-1.5,1.5,3)
        pool,cost,nodes,complete=enumerate_cvp(R,y,16,1000000)
        truth=np.sort(np.sum((coords@R.T-y)**2,axis=1))[:16]
        assert complete
        if not np.allclose(np.sort(cost),truth,atol=1e-11,rtol=1e-11):
            failure=dict(case=i,R=R.tolist(),y=y.tolist(),costs=sorted(cost.tolist()),
                         truth=truth.tolist(),pool=pool.tolist(),complete=bool(complete))
            Path('evidence/enumeration_fixed_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
            raise AssertionError(failure)
        receipts.append(dict(case=i,nodes=int(nodes),closest_squared_distance=float(min(cost))))
    return dict(status='PASS',checked_source='cvp_fixed.py',
                brute_force_box='[-8,8]^3',number_of_closest_points=16,cases=receipts)


def check_lp(prefix):
    ctx.threads=1
    state=json.loads(Path(prefix+'.json').read_text())
    dual=np.load(prefix+'-dual.npz')
    t,nu=dual['t'],dual['nu']
    lib=Lib(state['denominator'],state['numerator'],t)
    mu,w=np.array(state['mu']),np.array(state['w'])
    lam,price=float(dual['lam']),float(dual['price'])
    g=lib.g(mu,w)
    value=float(lib.LM@mu+np.maximum(g,0).mean())
    rd=lib.LM-lib.LR@nu-lam*lib.dR
    rn=lib.LS@nu+price*lib.dS
    result=dict(prefix=prefix,grid=len(t),full_grid_value=value,saved_lp_value=state['lp'],
                full_grid_minus_saved=value-state['lp'],dual_objective=lam-price*(1-1e-7),
                primal_dual_gap=value-(lam-price*(1-1e-7)),
                normalization_residual=float(lib.dR@mu-1),degree_ratio=float(lib.dS@w),
                min_denominator_rc=float(min(rd)),min_numerator_rc=float(min(rn)),
                max_active_denominator_abs_rc=float(max(abs(rd[mu>1e-12]))),
                max_active_numerator_abs_rc=float(max(abs(rn[w>1e-12]))),
                min_dual_atom=float(min(nu)),max_dual_atom=float(max(nu)),uniform_atom=1/len(t))
    assert abs(value-state['lp'])<1e-10,result
    assert abs(result['primal_dual_gap'])<1e-9,result
    assert abs(result['normalization_residual'])<1e-10,result
    assert min(rd)>-1e-8 and min(rn)>-1e-8,result
    assert min(nu)>-1e-12 and max(nu)<1/len(t)+1e-12,result
    result['status']='PASS'
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prefix',action='append',default=[])
    ap.add_argument('--out',default='evidence/numerical_checks.json')
    a=ap.parse_args()
    start=time.monotonic()
    result=dict(pid=os.getpid(),enumeration=check_enumerator(),
                lp=[check_lp(p) for p in a.prefix],seconds=time.monotonic()-start)
    Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
