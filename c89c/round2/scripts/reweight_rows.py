"""Numerical search only: individually reweight rational SOS factors."""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','RAYON_NUM_THREADS']: os.environ[key]='1'
import sys, math, json, time
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
from fractions import Fraction
from pathlib import Path
prefix,cert,out=sys.argv[1:4]
tokens=iter(map(int,Path(cert).read_text().split())); n,k,D,B,bn,bd,mode=[next(tokens) for _ in range(7)]
blocks=[]
for z in range(B):
 t,m,typ,d,r=[next(tokens) for _ in range(5)];flags=[next(tokens) for _ in range(d)]
 L=np.array([[next(tokens) for _ in range(d)] for _ in range(r)],dtype=np.int64)
 blocks.append((t,m,typ,d,r,flags,L))
meta=[]
with open(prefix+'.meta') as f:
 next(f)
 for line in f: meta.append(list(map(int,line.split())))
with open(prefix+'.coo') as f:
 nr,nc=map(int,next(f).split()); a=np.loadtxt(f,dtype=np.int32).T
A=sparse.coo_matrix((a[2],(a[0],a[1])),shape=(nr,nc)).tocsr();del a
starts={};offset=0
for t,m,typ,d,*flags in meta:
 starts[t,m,typ]=(offset,d,flags);offset+=d*(d+1)//2
vectors=[]
for t,m,typ,d,r,flags,L in blocks:
 off,dd,ff=starts[t,m,typ];assert dd==d and flags==ff
 ii,jj=np.triu_indices(d);X=L.astype(float)/D
 products=X[:,ii]*X[:,jj]
 den=math.comb(n,t)*math.comb(n-t,m)*(math.factorial(t) if mode else 1)
 vectors.append(np.asarray(A[:,off:off+len(ii)]@products.T)/den)
M=np.column_stack(vectors); target=np.loadtxt(prefix+'.objective');target=target[:,0]/target[:,1]
scale=1e5
print('LP',M.shape,'baseline',bn/bd,'start',time.time(),flush=True)
result=linprog(np.r_[np.zeros(M.shape[1]),-1.],A_ub=np.column_stack((M*scale,np.ones(nr))),b_ub=target*scale,bounds=[(0,100)]*M.shape[1]+[(0,10)],method='highs',options={'threads':1,'time_limit':900,'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
print('LP result',result.message,'objective',result.fun,flush=True)
assert result.x is not None
weights=np.maximum(result.x[:-1],0);off=0;coeff=np.zeros(nc);new=[]
for t,m,typ,d,r,flags,L in blocks:
 LL=np.rint(np.sqrt(weights[off:off+r,None])*L).astype(np.int64);off+=r
 LL=LL[np.any(LL!=0,axis=1)];new.append((t,m,typ,d,len(LL),flags,LL))
 q=LL.astype(float).T@LL.astype(float)/D**2
 start,_,_=starts[t,m,typ];ii,jj=np.triu_indices(d)
 den=math.comb(n,t)*math.comb(n-t,m)*(math.factorial(t) if mode else 1)
 coeff[start:start+len(ii)]=q[ii,jj]/den
slack=target-A@coeff;b=Fraction(math.floor((float(slack.min())-1e-11)*1e12),10**12)
with open(out,'w') as f:
 print(n,k,D,len(new),b.numerator,b.denominator,mode,file=f)
 for t,m,typ,d,r,flags,LL in new:
  print(t,m,typ,d,r,file=f);print(*flags,file=f)
  for row in LL:print(*map(int,row),file=f)
print('CANDIDATE',str(b),float(b),'worst',int(slack.argmin()),flush=True)
np.savez_compressed(out+'.weights.npz',weights=weights)
Path(out+'.search.json').write_text(json.dumps({'status':result.message,'candidate':str(b),'value':float(b),'rows':len(weights),'nonzero':int(sum(weights>0))},indent=2))
