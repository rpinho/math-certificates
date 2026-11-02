"""Exploratory floating-point SDP; no output here is an exact certificate."""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','RAYON_NUM_THREADS']:
    os.environ[key]='1'
import sys, math, json, time
import numpy as np
from scipy import sparse
import cvxpy as cp
prefix=sys.argv[1]; solver=sys.argv[2] if len(sys.argv)>2 else 'CLARABEL'
k=int(sys.argv[3]) if len(sys.argv)>3 else 6
weight=float(sys.argv[4]) if len(sys.argv)>4 else 1.
with open(prefix+'.coo') as f:
    nr,nc=map(int,next(f).split())
    data=np.loadtxt(f,dtype=np.int32).T
A=sparse.coo_matrix((data[2],(data[0],data[1])),shape=(nr,nc)).tocsr()
meta=[]
with open(prefix+'.meta') as f:
    header=list(map(int,next(f).split()));n=header[0];labelled=bool(header[1]) if len(header)>1 else False
    for line in f:
        t,m,typ,d,*keys=map(int,line.split()); assert len(keys)==d
        meta.append((t,m,typ,d,keys))
obj=np.loadtxt(prefix+('.objective56' if k==56 else '.objective5' if k==5 else '.objective'))
target=obj[:,0]/obj[:,1]
if k==56: target=target+weight*obj[:,2]/obj[:,3]
print('size',n,nr,nc,'blocks',[(t,typ,d) for t,m,typ,d,keys in meta],flush=True)
Q=[]; expr=[]; psd=[]
for t,m,typ,d,keys in meta:
    q=cp.Variable((d,d),symmetric=True);Q.append(q);psd.append(q>>0)
    den=math.comb(n,t)*math.comb(n-t,m)
    if labelled: den*=math.factorial(t)
    expr.append(q[np.triu_indices(d)]/den)
bound=cp.Variable()
constraints=psd+[A@cp.hstack(expr)+bound <= target]
prob=cp.Problem(cp.Maximize(bound),constraints)
kwargs=dict(verbose=True)
if solver=='SCS': kwargs.update(eps=1e-8,max_iters=100000,time_limit_secs=1500)
if solver=='SCS_INDIRECT': kwargs.update(eps=1e-7,max_iters=30000,time_limit_secs=1200,use_indirect=True)
if solver=='CLARABEL': kwargs.update(tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9,max_iter=150,max_threads=1)
try:
    prob.solve(solver='SCS' if solver=='SCS_INDIRECT' else solver,**kwargs)
finally:
    result={'status':prob.status,'bound':float(bound.value) if bound.value is not None else None,'solver':solver,'n':n,'k':k,'weight':weight}
    tag=f'_{solver}_k{k}_w{weight:g}'
    if all(q.value is not None for q in Q):
        np.savez_compressed(prefix+tag+'_Q.npz',**{f'q{i}':q.value for i,q in enumerate(Q)})
        coeff=np.concatenate([[q.value[i,j]/(math.comb(n,t)*math.comb(n-t,m)*(math.factorial(t) if labelled else 1)) for i in range(d) for j in range(i,d)] for q,(t,m,typ,d,keys) in zip(Q,meta)])
        result['min_residual']=float(np.min(target-A@coeff))
        result['min_eigenvalue']=min(float(np.linalg.eigvalsh(q.value)[0]) for q in Q)
    with open(prefix+tag+'_result.json','w') as f: json.dump(result,f,indent=2)
    print('RESULT',result,flush=True)
