"""Fresh original-operator primal attack, no claimant code. Pod only.

The numerical statuses are diagnostics. The proof audit and separate exact
identities, rather than floating-point infeasibility, establish the lower.
"""
import json,time,warnings
import numpy as np
from scipy.optimize import linprog

warnings.filterwarnings('ignore',message='Unrecognized options detected')


def one(ell,K,eigen=False):
    N=ell*ell;q=(N-1)//2
    ids=np.arange(q+1)
    D=np.cos(2*np.pi*np.outer(ids,ids)/N)/ell
    D[:,1:]*=2
    eye=np.eye(q+1)
    A=np.vstack([-eye[0],D[0],-eye[K:],D[K:],-eye[q],D[q]])
    b=np.zeros(len(A));b[-2:]=-1
    kw=dict(A_eq=D+eye,b_eq=np.zeros(q+1)) if eigen else {}
    result=linprog(np.zeros(q+1),A_ub=A,b_ub=b,bounds=(None,None),
                   method='highs',options=dict(threads=1,time_limit=45,
                   primal_feasibility_tolerance=1e-8,dual_feasibility_tolerance=1e-8),**kw)
    row=dict(ell=ell,K=K,eigen=eigen,status=int(result.status),message=result.message)
    if result.success:
        f=result.x;Df=D@f
        row['max_constraint_violation']=float(max(0,np.max(A@f-b)))
        row['endpoints']=[float(f[q]),float(-Df[q])]
        u=(f-Df)/2
        row['projection_minus_residual']=float(np.max(np.abs(D@u+u)))
        assert row['max_constraint_violation']<1e-6
        assert row['projection_minus_residual']<1e-6
    return row


if __name__=='__main__':
    start=time.monotonic();out=[]
    for ell in (3,5,7,9,11,13,17,21,25,31):
        for eigen in (False,True):
            for K in (ell-1,ell):
                row=one(ell,K,eigen);out.append(row);print(json.dumps(row),flush=True)
                json.dump(dict(rows=out,seconds=time.monotonic()-start),open('lp_results.json','w'),indent=2)
    print('LP ATTACK COMPLETE',time.monotonic()-start,flush=True)
