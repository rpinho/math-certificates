"""All order-nine constraints, indirect SCS, plus a certified order-eight direction."""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','RAYON_NUM_THREADS']:os.environ[key]='1'
import math,time,json
from pathlib import Path
import numpy as np
from scipy import sparse
import cvxpy as cp
pfx='artifacts/odd9';A=sparse.load_npz(pfx+'.npz');obj=np.loadtxt(pfx+'.objective');target=obj[:,0]/obj[:,1];base=np.load('artifacts/baseline9.npy')
with open(pfx+'.meta') as f:n,mode=map(int,next(f).split());meta=[list(map(int,s.split())) for s in f]
qs=[];terms=[];cons=[]
for t,m,typ,d,*flags in meta:
 q=cp.Variable((d,d),symmetric=True);qs.append(q);cons.append(q>>0)
 terms.append(q[np.triu_indices(d)]/(math.comb(n,t)*math.comb(n-t,m)*math.comb(n-t-m,m)))
w=cp.Variable(nonneg=True);b=cp.Variable();cons += [A@cp.hstack(terms)+base*w+b<=target,w<=10,b<=1/16384,cp.sum(cp.hstack([cp.trace(q) for q in qs]))<=100]
prob=cp.Problem(cp.Maximize(b),cons);print('START',time.time(),A.shape,A.nnz,flush=True)
try:prob.solve(solver='SCS',use_indirect=True,verbose=True,eps=1e-8,max_iters=30000,time_limit_secs=1200)
finally:
 info={'status':prob.status,'bound':None if b.value is None else float(b.value),'time':time.time()}
 if all(q.value is not None for q in qs):
  np.savez_compressed('artifacts/nine_full_Q.npz',**{f'q{i}':q.value for i,q in enumerate(qs)},weight=np.array([max(0.,float(w.value))]))
  coeff=[]
  for q,(t,m,typ,d,*flags) in zip(qs,meta):
   ev,U=np.linalg.eigh(q.value);Q=(U*np.maximum(ev,0))@U.T;coeff.extend(Q[np.triu_indices(d)]/(math.comb(n,t)*math.comb(n-t,m)*math.comb(n-t-m,m)))
  info['projected_minimum']=float(np.min(target-A@np.array(coeff)-max(0.,float(w.value))*base));info['weight']=float(w.value)
 Path('artifacts/nine_full.json').write_text(json.dumps(info,indent=2));print('RESULT',info,flush=True)
