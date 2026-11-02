"""Numerical reweighting search starting from the published PPSS certificate.
Uses the full ordered-root coefficient model. Exact verification is separate.
"""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','RAYON_NUM_THREADS']:os.environ[key]='1'
import math,sys,time,json
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
mode_search=sys.argv[1] if len(sys.argv)>1 else 'blocks';prefix='artifacts/ordered8'
v=iter(map(int,Path('artifacts/ppss_baseline.cert').read_text().split()));n,k,oldD,B,bn,bd,mode=[next(v) for _ in range(7)];D=10**12
blocks=[]
for _ in range(B):
 t,m,typ,d,r=[next(v) for _ in range(5)];flags=[next(v) for _ in range(d)];L=np.array([[next(v) for _ in range(d)] for _ in range(r)],dtype=float)/oldD
 blocks.append((t,m,typ,d,r,flags,L))
cache=prefix+'.npz'
if Path(cache).exists():A=sparse.load_npz(cache)
else:
 with open(prefix+'.coo') as f:nr,nc=map(int,next(f).split());a=np.loadtxt(f,dtype=np.int32).T
 A=sparse.coo_matrix((a[2],(a[0],a[1])),shape=(nr,nc)).tocsr();del a
 sparse.save_npz(cache,A,compressed=False)
obj=np.loadtxt(prefix+'.objective5');target=obj[:,0]/obj[:,1];offset=0;vectors=[]
for t,m,typ,d,r,flags,L in blocks:
 ii,jj=np.triu_indices(d);den=math.comb(n,t)*math.comb(n-t,m)*math.factorial(t)
 if mode_search=='rows':products=L[:,ii]*L[:,jj]
 else:products=(L.T@L)[ii,jj][None,:]
 vectors.append(np.asarray(A[:,offset:offset+len(ii)]@products.T)/den);offset+=len(ii)
M=np.column_stack(vectors);del vectors,A
print('LP',mode_search,M.shape,'public_exact',bn/bd,'time',time.time(),flush=True)
column_scale=np.maximum(np.max(np.abs(M),axis=0),1e-100);M=M/column_scale
scale=1000000
res=linprog(np.r_[np.zeros(M.shape[1]),-1],A_ub=np.column_stack((M*scale,np.ones(len(target)))),b_ub=target*scale,bounds=[(0,None)]*M.shape[1]+[(0,2000)],method='highs',options={'threads':1,'time_limit':1800,'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
print('LP RESULT',res.message,'objective',res.fun,flush=True); print('ACTUAL_LP_MIN',float(np.min(target-M@res.x[:-1])), 'baseline min',float(np.min(target-M@column_scale)),flush=True)
assert res.x is not None
weights=np.maximum(res.x[:-1],0)/column_scale;np.save('artifacts/ppss_'+mode_search+'_weights.npy',weights);off=0;new=[];actual=[]
for z,(t,m,typ,d,r,flags,L) in enumerate(blocks):
 if mode_search=='rows':w=weights[off:off+r];off+=r
 else:w=np.repeat(weights[z],r)
 LL=np.rint(np.sqrt(w[:,None])*L*D).astype(np.int64);new.append(LL)
 # Recompute actual row/block coefficients after rounding, preserving all constraints.
 ii,jj=np.triu_indices(d);lf=LL.astype(float)/D
 if mode_search=='rows':
  # The unrounded M is accurate enough to choose a provisional bound, with ample reserve.
  pass
np.savez_compressed('artifacts/ppss_'+mode_search+'_factors.npz',**{f'l{i}':L for i,L in enumerate(new)})
# A fresh matrix-vector product after export supplies the rounded minimum.
A=sparse.load_npz(cache);coef=[]
for (t,m,typ,d,r,flags,L),LL in zip(blocks,new):
 Q=LL.astype(float).T@LL.astype(float)/D**2;coef.extend(Q[np.triu_indices(d)]/(math.comb(n,t)*math.comb(n-t,m)*math.factorial(t)))
slack=target-A@np.array(coef);b=Fraction(math.floor((float(slack.min())-1e-12)*1e15),10**15)
out=Path('artifacts/ppss_'+mode_search+'.cert')
with out.open('w') as f:
 print(n,k,D,B,b.numerator,b.denominator,mode,file=f)
 for (t,m,typ,d,r,flags,L),LL in zip(blocks,new):
  LL=LL[np.any(LL!=0,axis=1)]
  if len(LL)==0:LL=np.zeros((1,d),dtype=np.int64)
  print(t,m,typ,d,len(LL),file=f);print(*flags,file=f)
  for row in LL:print(*map(int,row),file=f)
info={'candidate':str(b),'value':float(b),'public_exact':str(Fraction(bn,bd)),'improvement':float(b)-bn/bd,'LP_status':res.message}
Path(str(out)+'.json').write_text(json.dumps(info,indent=2));print('CANDIDATE',info,flush=True)
