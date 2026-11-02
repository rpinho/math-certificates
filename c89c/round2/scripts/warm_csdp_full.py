"""Numerical CSDP start from verified squares and the random-colouring dual."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,math,itertools,time
from pathlib import Path
import numpy as np
import pynauty
import sys
pfx=sys.argv[1] if len(sys.argv)>1 else 'artifacts/original8';info=json.load(open(pfx+'_color_csdp.json'));meta=info['meta'];reps=info['reps'];scale=info['scale'];nr=info['rows'];B=len(reps)
v=iter(map(int,Path('artifacts/frozen_rows8.cert').read_text().split()));n,k,D,nb,bn,bd,mode=[next(v) for _ in range(7)];old={}
for _ in range(nb):
 t,m,typ,d,h=[next(v) for _ in range(5)];flags=[next(v) for _ in range(d)];L=np.array([[next(v) for _ in range(d)] for _ in range(h)],dtype=float)/D;old[t,m,typ]=(flags,L.T@L)
original=[]
for t,m,typ,d,flags in meta:
 if (t,m,typ) not in old:q=np.zeros((d,d))
 else:
  fl,q=old[t,m,typ]
  if fl!=flags:
   def key(code):
    adj={i:[] for i in range(t+m)}
    for j in range(1,t+m):
     for i in range(j):
      if code>>(j*(j-1)//2+i)&1:adj[i].append(j);adj[j].append(i)
    return pynauty.certificate(pynauty.Graph(t+m,adjacency_dict=adj,vertex_coloring=[set(range(t)),set(range(t,t+m))]))
   orbit={key(code):i for i,code in enumerate(fl)};mapping=[orbit[key(code)] for code in flags]
   def maproot(p):return sum(((typ>>(max(p[i],p[j])*(max(p[i],p[j])-1)//2+min(p[i],p[j])))&1)<<(j*(j-1)//2+i) for j in range(1,t) for i in range(j))
   aut=sum(maproot(p)==typ for p in itertools.permutations(range(t)));q=q[np.ix_(mapping,mapping)]*(math.factorial(t)//aut)
 original.append(q)
X=[]
for b in reps:
 if info.get('ordered_graph_average'):q=original[b]
 else:
  c,p=info['complement'][b];p=np.array(p,dtype=int);q=(original[b]+original[c][np.ix_(p,p)])/2
 X.append(q*scale+np.eye(len(q))*1e-4)
bstart=(bn/bd-1e-6)*scale

def graph(line,flip=False):
 a={i:[] for i in range(8)};pos=0
 for j in range(1,8):
  for i in range(j):
   edge=((ord(line[1+pos//6])-63)>>(5-pos%6))&1
   if bool(edge)^flip:a[i].append(j);a[j].append(i)
   pos+=1
 return pynauty.Graph(8,adjacency_dict=a)
lines=Path('sources/graph8.g6').read_text().splitlines();lookup={};orbits=[]
for i,line in enumerate(lines):
 g=graph(line);lookup[pynauty.certificate(g)]=i;aut=pynauty.autgrp(g);order=round(aut[1]*10**aut[2]);assert math.factorial(8)%order==0;orbits.append(math.factorial(8)//order)
assert sum(orbits)==2**28
y=[]
for i in info['kept_graphs']:
 j=lookup[pynauty.certificate(graph(lines[i],True))];y.append((orbits[i]+(orbits[j] if i!=j else 0))/2**28)
y=np.array(y);assert abs(y.sum()-1)<1e-12
# Directly use the exported model, avoiding a second reduction implementation.
with open(pfx+'_color.dat-s') as f:
 next(f);next(f);next(f);rhs=np.fromstring(next(f),sep=' ')
 data=np.loadtxt(f)
rows=data[:,0].astype(int)-1;blocks=data[:,1].astype(int)-1;ii=data[:,2].astype(int)-1;jj=data[:,3].astype(int)-1;values=data[:,4]
contrib=np.zeros(nr);Z=[]
for b in range(B):
 use=(rows>=0)&(blocks==b);r=rows[use];i=ii[use];j=jj[use];val=values[use]
 contrib+=np.bincount(r,weights=val*X[b][i,j]*np.where(i==j,1.,2.),minlength=nr)
 z=np.zeros_like(X[b]);np.add.at(z,(i,j),val*y[r]);z=z+z.T-np.diag(z.diagonal());z+=np.eye(len(z))*1e-8;Z.append(z)
slacks=rhs-contrib-bstart;assert slacks.min()>0
print('WARM primal',bstart/scale,'min slack',float(slacks.min()),'dual',float(y@rhs)/scale,'minZ',min(float(np.linalg.eigvalsh(z)[0]) for z in Z),flush=True)
with open(pfx+'_color.warm','w') as f:
 print(*[format(v,'.18e') for v in y],file=f)
 for matrixnum,matrices in [(1,Z),(2,X)]:
  for b,q in enumerate(matrices):
   for i in range(len(q)):
    for j in range(i,len(q)):
     if q[i,j]:print(matrixnum,b+1,i+1,j+1,format(float(q[i,j]),'.18e'),file=f)
  print(matrixnum,B+1,1,1,format(1e-8 if matrixnum==1 else bstart,'.18e'),file=f)
  for i,val in enumerate(y if matrixnum==1 else slacks):print(matrixnum,B+2,i+1,i+1,format(float(val),'.18e'),file=f)
print('SAVED',pfx+'_color.warm',flush=True)
