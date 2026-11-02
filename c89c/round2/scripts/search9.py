"""Nine-vertex cutting-plane SDP, retaining a certified eight-vertex direction.
All numerical outputs require independent exact verification.
"""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','RAYON_NUM_THREADS']:os.environ[key]='1'
import sys,math,time,json
from pathlib import Path
import numpy as np
from scipy import sparse
import cvxpy as cp
prefix='artifacts/odd9';seed=int(sys.argv[1]) if len(sys.argv)>1 else 2
with open(prefix+'.meta') as f:
 n,mode=map(int,next(f).split());meta=[list(map(int,line.split())) for line in f]
cache=prefix+'.npz'
if Path(cache).exists():A=sparse.load_npz(cache)
else:
 with open(prefix+'.coo') as f:nr,nc=map(int,next(f).split());a=np.loadtxt(f,dtype=np.int32).T
 A=sparse.coo_matrix((a[2],(a[0],a[1])),shape=(nr,nc)).tocsr();del a
 sparse.save_npz(cache,A,compressed=False)
nr,nc=A.shape
obj=np.loadtxt(prefix+'.objective');target=obj[:,0]/obj[:,1];base=np.load('artifacts/baseline9.npy')
qs=[];expr=[];cons=[]
for t,m,typ,d,*flags in meta:
 q=cp.Variable((d,d),symmetric=True);qs.append(q);cons.append(q>>0)
 den=math.comb(n,t)*math.comb(n-t,m)*math.comb(n-t-m,m);expr.append(q[np.triu_indices(d)]/den)
w=cp.Variable(nonneg=True);b=cp.Variable();vector=cp.hstack(expr)
rng=np.random.default_rng(seed);active=set(rng.choice(nr,2500,replace=False).tolist());active.update([0,nr-1]);active.update(np.argsort(target-base)[:5000].tolist());
for rnd in range(4):
 use=np.array(sorted(active),dtype=int);p=cp.Problem(cp.Maximize(b),cons+[A[use]@vector+w*base[use]+b<=target[use],w<=10,b<=1/16384,cp.sum(cp.hstack([cp.trace(q) for q in qs]))<=100])
 if rnd==0:
  for q in qs:q.value=np.zeros(q.shape)
  w.value=1.;b.value=0.000021892488
 print('ROUND',rnd,'constraints',len(use),'time',time.time(),flush=True)
 p.solve(solver='SCS',verbose=True,eps=1e-8,max_iters=30000,time_limit_secs=600,warm_start=True)
 if any(q.value is None for q in qs):break
 vals=[];factors=[];D=10**9
 for q,(t,m,typ,d,*flags) in zip(qs,meta):
  ev,U=np.linalg.eigh(q.value);L=np.rint(np.sqrt(np.maximum(ev,0))[:,None]*U.T*D).astype(np.int64);factors.append(L)
  Q=L.astype(float).T@L.astype(float)/D**2;den=math.comb(n,t)*math.comb(n-t,m)*math.comb(n-t-m,m);vals.extend(Q[np.triu_indices(d)]/den)
 rounded_w=max(0.,float(w.value));resid=target-A@np.array(vals)-rounded_w*base
 minimum=float(resid.min());print('CANDIDATE',rnd,minimum,'raw',float(b.value),'w',rounded_w,flush=True)
 np.savez_compressed(f'artifacts/nine_round{rnd}_Q.npz',**{f'q{i}':q.value for i,q in enumerate(qs)},weight=np.array([rounded_w]))
 Path(f'artifacts/nine_round{rnd}.json').write_text(json.dumps({'candidate':minimum,'raw':float(b.value),'weight':rounded_w,'active':len(use),'status':p.status},indent=2))
 # Add most violated rows. The final artifact must satisfy all rows after rounding.
 violations=target-A@np.concatenate([q.value[np.triu_indices(q.shape[0])]/(math.comb(n,t)*math.comb(n-t,m)*math.comb(n-t-m,m)) for q,(t,m,typ,d,*flags) in zip(qs,meta)])-rounded_w*base
 new=np.argsort(violations)[:3000];old=len(active);active.update(new.tolist())
 if len(active)==old:break
print('DONE',time.time(),flush=True)
