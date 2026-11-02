"""Numerical lifting of an eight-vertex SOS coefficient vector to nine vertices."""
import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','RAYON_NUM_THREADS']:os.environ[k]='1'
import itertools,sys,math,time
from pathlib import Path
import numpy as np
from scipy import sparse
import pynauty
prefix,cert=sys.argv[1:3]
v=iter(map(int,Path(cert).read_text().split()));n,k,D,B,bn,bd,mode=[next(v) for _ in range(7)]
blocks={}
for _ in range(B):
 t,m,typ,d,r=[next(v) for _ in range(5)];flags=[next(v) for _ in range(d)];L=np.array([[next(v) for _ in range(d)] for _ in range(r)],dtype=float)
 blocks[t,m,typ]=(flags,L.T@L/D**2)
coeff=[]
with open(prefix+'.meta') as f:
 next(f)
 for line in f:
  t,m,typ,d,*flags=map(int,line.split());q=np.zeros((d,d))
  if (t,m,typ) in blocks:
   ff,q=blocks[t,m,typ];assert ff==flags
  coeff.extend(q[np.triu_indices(d)]/(math.comb(n,t)*math.comb(n-t,m)))
with open(prefix+'.coo') as f:
 nr,nc=map(int,next(f).split());a=np.loadtxt(f,dtype=np.int32).T
A=sparse.coo_matrix((a[2],(a[0],a[1])),shape=(nr,nc)).tocsr();vals=A@np.array(coeff);del A,a

def decode(g6):
 n=ord(g6[0])-63;adj={i:[] for i in range(n)};b=0
 for j in range(1,n):
  for i in range(j):
   if (ord(g6[1+b//6])-63)>>(5-b%6)&1:adj[i].append(j);adj[j].append(i)
   b+=1
 return adj
lookup={}
for val,g6 in zip(vals,Path('sources/graph8.g6').read_text().splitlines()):
 lookup[pynauty.certificate(pynauty.Graph(8,adjacency_dict=decode(g6)))]=val
out=[]
for row,g6 in enumerate(Path('sources/graph9.g6').read_text().splitlines()):
 adj=decode(g6);total=0.
 for drop in range(9):
  vs=[i for i in range(9) if i!=drop];ren={v:i for i,v in enumerate(vs)}
  small={ren[v]:[ren[w] for w in adj[v] if w!=drop] for v in vs}
  total+=lookup[pynauty.certificate(pynauty.Graph(8,adjacency_dict=small))]
 out.append(total/9)
 if row%10000==0:print(row,time.time(),flush=True)
np.save('artifacts/baseline9.npy',np.array(out));print('DONE',len(out),flush=True)
