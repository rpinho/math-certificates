"""All nine-vertex constraints via raw SCS, avoiding CVXPY canonicalization copies."""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','RAYON_NUM_THREADS']:os.environ[key]='1'
import math,time,json,gc
from pathlib import Path
import numpy as np
from scipy import sparse
import scs
prefix='artifacts/odd9';A=sparse.load_npz(prefix+'.npz');nr,nc=A.shape
with open(prefix+'.meta') as f:
 n,mode=map(int,next(f).split());meta=[list(map(int,line.split())) for line in f]
divisors=[];psdscale=[]
for t,m,typ,d,*flags in meta:
 ii,jj=np.triu_indices(d);den=math.comb(n,t)*math.comb(n-t,m)*math.comb(n-t-m,m);divisors.extend([den]*len(ii));psdscale.extend(np.where(ii==jj,1.,math.sqrt(2.)))
divisors=np.array(divisors);psdscale=np.array(psdscale);A.data=A.data.astype(float)/divisors[A.indices];del divisors
obj=np.loadtxt(prefix+'.objective');target=obj[:,0]/obj[:,1];base=np.load('artifacts/baseline9.npy')
# Variables: nc upper-triangle Gram entries, weight of the certified direction, bound.
print('ASSEMBLE',A.shape,A.nnz,time.time(),flush=True)
left=sparse.vstack([A,sparse.diags(-psdscale),sparse.csr_matrix((3,nc))],format='csc');del A
weight=sparse.csc_matrix(np.r_[base,np.zeros(nc),-1.,1.,0.][:,None]);bound=sparse.csc_matrix(np.r_[np.ones(nr),np.zeros(nc),0.,0.,1.][:,None])
AA=sparse.hstack([left,weight,bound],format='csc');del left,weight,bound;gc.collect()
# SCS requires all linear-cone rows first, followed by PSD cones.
order=np.r_[np.arange(nr),np.arange(nr+nc,nr+nc+3),np.arange(nr,nr+nc)]
AA=AA[order].tocsc();rhs=np.r_[target,[0.,10.,1/16384],np.zeros(nc)];c=np.r_[np.zeros(nc+1),-1.]
x0=np.r_[np.zeros(nc),1.,0.000021892488];s0=rhs-AA@x0
print('SOLVE',AA.shape,AA.nnz,'time',time.time(),flush=True)
result=scs.solve(dict(A=AA,b=rhs,c=c,x=x0,s=s0,y=np.zeros(len(rhs))),dict(l=nr+3,s=[md[3] for md in meta]),linear_solver='cpu_indirect',eps_abs=1e-8,eps_rel=1e-8,max_iters=10000,time_limit_secs=1200,verbose=True)
info=result['info'];print('RESULT',info,flush=True);Path('artifacts/nine_raw_info.json').write_text(json.dumps(info,indent=2))
x=result['x'];qs={};off=0;coeff=[]
for z,(t,m,typ,d,*flags) in enumerate(meta):
 ii,jj=np.triu_indices(d);q=np.zeros((d,d));q[ii,jj]=x[off:off+len(ii)];q[jj,ii]=x[off:off+len(ii)];off+=len(ii);qs[f'q{z}']=q
qs['weight']=np.array([max(0.,float(x[nc]))]);np.savez_compressed('artifacts/nine_raw_Q.npz',**qs)
print('SAVED',float(x[-1]),float(x[nc]),time.time(),flush=True)
