"""Search nonnegative weights for already rational SOS blocks.

The final scaled factors are rounded back to integers. The result still needs
the independent exact verifier; the LP itself is never a proof.
"""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','RAYON_NUM_THREADS']:os.environ[key]='1'
import sys,math,json
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
prefix,cert,out=sys.argv[1:4]
lines=Path(cert).read_text().splitlines();header=list(map(int,lines[0].split()))
n,k,D,B,bn,bd=header[:6];mode=header[6] if len(header)>6 else 0
tokens=iter(map(int,' '.join(lines[1:]).split()));blocks=[]
for b in range(B):
    t,m,typ,d,rank=[next(tokens) for _ in range(5)];flags=[next(tokens) for _ in range(d)]
    L=np.array([[next(tokens) for _ in range(d)] for _ in range(rank)],dtype=np.int64)
    blocks.append((t,m,typ,d,rank,flags,L))
with open(prefix+'.coo') as f:
    nr,nc=map(int,next(f).split());data=np.loadtxt(f,dtype=np.int32).T
A=sparse.coo_matrix((data[2],(data[0],data[1])),shape=(nr,nc)).tocsr()
obj=np.loadtxt(prefix+'.objective');target=obj[:,0]/obj[:,1]
offset=0;vectors=[]
for t,m,typ,d,rank,flags,L in blocks:
    Q=L.astype(float).T@L.astype(float)/D**2
    den=math.comb(n,t)*math.comb(n-t,m)*(math.factorial(t) if mode else 1)
    width=d*(d+1)//2
    vectors.append(A[:,offset:offset+width]@(Q[np.triu_indices(d)]/den));offset+=width
assert offset==nc
M=np.column_stack(vectors)
result=linprog(np.r_[np.zeros(B),-1.],A_ub=np.column_stack((M,np.ones(nr))),b_ub=target,bounds=[(0,10)]*B+[(0,1)],method='highs',options={'threads':1,'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
print('exploratory LP',result.message,'bound',None if not result.success else result.x[-1],flush=True)
assert result.success
weights=np.maximum(result.x[:B],0);print('weights',weights.tolist(),flush=True)
new=[];coeff=[]
for w,(t,m,typ,d,rank,flags,L) in zip(weights,blocks):
    L=np.rint(math.sqrt(float(w))*L).astype(np.int64);new.append(L)
    Q=L.astype(float).T@L.astype(float)/D**2
    den=math.comb(n,t)*math.comb(n-t,m)*(math.factorial(t) if mode else 1)
    coeff.extend(Q[np.triu_indices(d)]/den)
margin=target-A@np.array(coeff)
b=Fraction(math.floor((float(min(margin))-1e-12)*1e15),10**15)
with open(out,'w') as f:
    print(n,k,D,B,b.numerator,b.denominator,mode,file=f)
    for (t,m,typ,d,rank,flags,L),Lnew in zip(blocks,new):
        print(t,m,typ,d,rank,file=f);print(*flags,file=f)
        for row in Lnew:print(*map(int,row),file=f)
print('rounded candidate',str(b),float(b),'row',int(np.argmin(margin)),flush=True)
