"""Round numerical Gram matrices to explicit rational sums of squares.

This program searches for a certificate; it does not verify it.
"""
import os
for v in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']: os.environ[v]='1'
import sys,math
import numpy as np
from scipy import sparse
from fractions import Fraction
prefix,npz,out=sys.argv[1:4]
D=int(sys.argv[4]) if len(sys.argv)>4 else 10**9
k=int(sys.argv[5]) if len(sys.argv)>5 else 6
meta=[]
with open(prefix+'.meta') as f:
    header=list(map(int,next(f).split()));n=header[0];labelled=bool(header[1]) if len(header)>1 else False
    for line in f:
        t,m,typ,d,*keys=map(int,line.split());meta.append((t,m,typ,d,keys))
with open(prefix+'.coo') as f:
    nr,nc=map(int,next(f).split());data=np.loadtxt(f,dtype=np.int32).T
A=sparse.coo_matrix((data[2],(data[0],data[1])),shape=(nr,nc)).tocsr()
obj=np.loadtxt(prefix+('.objective5' if k==5 else '.objective')); target=obj[:,0]/obj[:,1]
Qs=np.load(npz); factors=[]; coeff=[]
for i,(t,m,typ,d,keys) in enumerate(meta):
    w,v=np.linalg.eigh(Qs[f'q{i}']);w=np.maximum(w,0)
    L=np.rint((np.sqrt(w)[:,None]*v.T)*D).astype(np.int64)
    factors.append(L)
    Q=(L.astype(float).T@L.astype(float))/D**2
    den=math.comb(n,t)*math.comb(n-t,m)
    if labelled: den*=math.factorial(t)
    coeff.extend(Q[a,b]/den for a in range(d) for b in range(a,d))
margin=target-A@np.array(coeff)
print('rounded exploratory min',float(min(margin)),'row',int(np.argmin(margin)),flush=True)
# Conservative fixed rational floor, with another full 1e-9 margin reserved.
b=Fraction(math.floor((float(min(margin))-1e-12)*10**15),10**15)
with open(out,'w') as f:
    print(n,k,D,len(meta),b.numerator,b.denominator,int(labelled),file=f)
    for (t,m,typ,d,keys),L in zip(meta,factors):
        print(t,m,typ,d,d,file=f)
        print(*keys,file=f)
        for row in L: print(*map(int,row),file=f)
print('candidate',str(b),float(b),out,flush=True)
