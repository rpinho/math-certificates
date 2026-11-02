"""Floating SDP search. Only exported integer factors and exact replay prove bounds."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','RAYON_NUM_THREADS']:os.environ[k]='1'
import sys,math,json,time
import numpy as np
from scipy import sparse
import cvxpy as cp
prefix=sys.argv[1];k=int(sys.argv[2]);solver=sys.argv[3] if len(sys.argv)>3 else 'SCS';seconds=int(sys.argv[4]) if len(sys.argv)>4 else 1200
with open(prefix+'.meta') as f:
 n,mode=map(int,next(f).split());meta=[list(map(int,x.split())) for x in f]
with open(prefix+'.coo') as f:
 nr,nc=map(int,next(f).split());d=np.loadtxt(f,dtype=np.int32).T
A=sparse.coo_matrix((d[2],(d[0],d[1])),shape=(nr,nc)).tocsr();del d
obj=np.loadtxt(prefix+('.objective' if k==6 else '.objective'+str(k)));target=obj[:,0]/obj[:,1]
qs=[];terms=[];cons=[]
for t,m,typ,d,*flags in meta:
 q=cp.Variable((d,d),symmetric=True);qs.append(q);cons.append(q>>0)
 den=math.comb(n,t)*math.comb(n-t,m)*math.comb(n-t-m,m)*(math.factorial(t) if mode else 1)
 terms.append(q[np.triu_indices(d)]/den)
b=cp.Variable();cons.append(A@cp.hstack(terms)+b<=target)
p=cp.Problem(cp.Maximize(b),cons)
print('SETUP',n,k,nr,nc,'blocks',len(qs),'maxdim',max(x.shape[0] for x in qs),'time',time.time(),flush=True)
args=dict(verbose=True)
if solver=='SCS':args.update(eps=1e-8,max_iters=100000,time_limit_secs=seconds)
if solver=='SCS_INDIRECT':args.update(eps=1e-8,max_iters=100000,time_limit_secs=seconds,use_indirect=True)
if solver=='CLARABEL':args.update(max_threads=1,max_iter=150,time_limit=seconds,tol_feas=1e-9,tol_gap_abs=1e-9,tol_gap_rel=1e-9)
try:p.solve(solver='SCS' if solver=='SCS_INDIRECT' else solver,**args)
finally:
 tag=prefix+f'_k{k}_{solver}'
 r={'status':p.status,'objective':None if b.value is None else float(b.value),'time':time.time()}
 if all(q.value is not None for q in qs):
  np.savez_compressed(tag+'_Q.npz',**{f'q{i}':q.value for i,q in enumerate(qs)})
  r['minimum_eigenvalue']=min(float(np.linalg.eigvalsh(q.value)[0]) for q in qs)
 open(tag+'.json','w').write(json.dumps(r,indent=2));print('RESULT',r,flush=True)
