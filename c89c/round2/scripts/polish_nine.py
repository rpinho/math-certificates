"""All-nine-vertex LP polishing of lifted blocks and projected nine-vertex blocks."""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','RAYON_NUM_THREADS']:os.environ[key]='1'
import sys,math,json,time
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
files=sys.argv[1:] or ['artifacts/nine_round0_Q.npz']
v=iter(map(int,Path('artifacts/frozen_rows8.cert').read_text().split()));n,k,D,B,bn,bd,mode=[next(v) for _ in range(7)];base=[]
for _ in range(B):
 t,m,typ,d,r=[next(v) for _ in range(5)];flags=[next(v) for _ in range(d)];L=np.array([[next(v) for _ in range(d)] for _ in range(r)],dtype=float)/D;base.append((t,m,typ,d,flags,L))
with open('artifacts/base8.meta') as f:next(f);meta8=[list(map(int,s.split())) for s in f]
starts={};off=0
for t,m,typ,d,*flags in meta8:starts[t,m,typ]=(off,d,flags);off+=d*(d+1)//2
with open('artifacts/base8.coo') as f:nr,nc=map(int,next(f).split());a=np.loadtxt(f,dtype=np.int32).T
A=sparse.coo_matrix((a[2],(a[0],a[1])),shape=(nr,nc)).tocsr();del a
indices=np.load('artifacts/sub8_indices.npy');vectors=[];dirs=[]
for z,(t,m,typ,d,flags,L) in enumerate(base):
 ii,jj=np.triu_indices(d);start,dd,ff=starts[t,m,typ];assert flags==ff
 coeff=(L.T@L)[ii,jj]/(math.comb(8,t)*math.comb(8-t,m));v8=A[:,start:start+len(ii)]@coeff;vectors.append(v8[indices].mean(axis=1));dirs.append(('base',z,L.T@L))
del A
with open('artifacts/odd9.meta') as f:next(f);meta9=[list(map(int,s.split())) for s in f]
A=sparse.load_npz('artifacts/odd9.npz');nr,nc=A.shape
for filename in files:
 data=np.load(filename);off=0
 for z,(t,m,typ,d,*flags) in enumerate(meta9):
  q=data[f'q{z}'];ev,U=np.linalg.eigh((q+q.T)/2);q=(U*np.maximum(ev,0))@U.T;ii,jj=np.triu_indices(d);width=len(ii);den=math.comb(9,t)*math.comb(9-t,m)*math.comb(9-t-m,m)
  vectors.append(np.asarray(A[:,off:off+width]@q[ii,jj])/den);dirs.append(('odd',z,q));off+=width
M=np.column_stack(vectors);del vectors,A
norm=np.maximum(np.max(np.abs(M),axis=0),1e-100);M/=norm;obj=np.loadtxt('artifacts/odd9.objective');target=obj[:,0]/obj[:,1];scale=1e5
print('LP9 POLISH',M.shape,time.time(),flush=True)
res=linprog(np.r_[np.zeros(M.shape[1]),-1.],A_ub=np.column_stack((M*scale,np.ones(nr))),b_ub=target*scale,bounds=[(0,None)]*M.shape[1]+[(0,10)],method='highs',options={'threads':1,'time_limit':900,'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10,'small_matrix_value':1e-12})
print('LP RESULT',res.message,res.fun,flush=True);assert res.x is not None
w=np.maximum(res.x[:-1],0)/norm;Qs_base=[np.zeros((x[3],x[3])) for x in base];Qs_odd=[np.zeros((x[3],x[3])) for x in meta9]
for weight,(kind,z,q) in zip(w,dirs):(Qs_base if kind=='base' else Qs_odd)[z][:]+=weight*q
D=10**12;factors=[];delta=np.zeros(nr)
# Recompute rounded search coefficients through the same two independently-sized tables.
for (t,m,typ,d,flags,L),q in zip(base,Qs_base):
 ev,U=np.linalg.eigh((q+q.T)/2);LL=np.rint(np.sqrt(np.maximum(ev,0))[:,None]*U.T*D).astype(np.int64);factors.append((t,m,typ,d,flags,LL))
for (t,m,typ,d,*flags),q in zip(meta9,Qs_odd):
 ev,U=np.linalg.eigh((q+q.T)/2);LL=np.rint(np.sqrt(np.maximum(ev,0))[:,None]*U.T*D).astype(np.int64);factors.append((t,m,typ,d,flags,LL))
# Floating reserve covers the tiny factor rounding in this provisional candidate;
# authoritative bound is accepted only after the exact verifier passes.
b=Fraction(math.floor((float(np.min(target-M@(w*norm)))-1e-9)*1e12),10**12)
out=Path('artifacts/nine_polished.cert')
with out.open('w') as f:
 print(9,6,D,len(factors),b.numerator,b.denominator,0,file=f)
 for t,m,typ,d,flags,LL in factors:
  LL=LL[np.any(LL!=0,axis=1)]
  if len(LL)==0:LL=np.zeros((1,d),dtype=np.int64)
  print(t,m,typ,d,len(LL),file=f);print(*flags,file=f)
  for row in LL:print(*map(int,row),file=f)
summary={'candidate':str(b),'value':float(b),'weights':w.tolist(),'inputs':files,'status':res.message};Path(str(out)+'.json').write_text(json.dumps(summary,indent=2));print('CANDIDATE9',summary,flush=True)
