"""Full ordered-root SDP; average graph/complement inequalities before export.
The postprocessor symmetrizes PSD matrices explicitly in the original flags.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','RAYON_NUM_THREADS']:os.environ[k]='1'
import json,itertools,math,time,sys
from pathlib import Path
import numpy as np
from scipy import sparse
import pynauty
prefix=sys.argv[1] if len(sys.argv)>1 else 'artifacts/ordered8';balanced='balanced' in prefix;A=sparse.load_npz(prefix+'.npz').tocsr()
with open(prefix+'.meta') as f:n,mode=map(int,next(f).split());meta=[list(map(int,s.split())) for s in f]
# Store metadata in the same tuple layout as the unordered exporter.
meta=[(t,m,typ,d,keys) for t,m,typ,d,*keys in meta]

def ggraph(line,flip=False):
 adj={i:[] for i in range(8)};pos=0
 for j in range(1,8):
  for i in range(j):
   if bool((ord(line[1+pos//6])-63)>>(5-pos%6)&1)^flip:adj[i].append(j);adj[j].append(i)
   pos+=1
 return pynauty.Graph(8,adjacency_dict=adj)
lines=Path('sources/graph8.g6').read_text().splitlines();lookup={pynauty.certificate(ggraph(s)):i for i,s in enumerate(lines)};comp=np.array([lookup[pynauty.certificate(ggraph(s,True))] for s in lines],dtype=int);keep=np.array([i for i,j in enumerate(comp) if i<=j],dtype=int)
assert np.array_equal(comp[comp],np.arange(len(lines)))
C=(A[keep]+A[comp[keep]])*.5;del A
obj=np.loadtxt(prefix+'.objective');target=obj[:,0]/obj[:,1];target=target[keep]
# Complement an ordered-root flag, then relabel roots by one fixed type isomorphism.
def transform(code,p):
 return sum(((code>>(max(p[i],p[j])*(max(p[i],p[j])-1)//2+min(p[i],p[j])))&1)<<(j*(j-1)//2+i) for j in range(1,len(p)) for i in range(j))
bytype={(t,m,typ):b for b,(t,m,typ,d,keys) in enumerate(meta)};image=[]
for b,(t,m,typ,d,keys) in enumerate(meta):
 rootcomp=typ^((1<<(t*(t-1)//2))-1)
 targettype,p=min((transform(rootcomp,p),p) for p in itertools.permutations(range(t)))
 dest=bytype[t,m,targettype];destkeys=meta[dest][4];fl={code:i for i,code in enumerate(destkeys)};top=(1<<((t+m)*(t+m-1)//2))-1
 mapping=[]
 for key in keys:
  code=top^key;can=min(transform(code,list(p)+list(u)) for u in itertools.permutations(range(t,t+m)));mapping.append(fl[can])
 assert len(set(mapping))==d;image.append((dest,mapping))
block_scale=[]
for t,m,typ,d,keys in meta:
 adj={i:[] for i in range(t)}
 for j in range(1,t):
  for i in range(j):
   if typ>>(j*(j-1)//2+i)&1:adj[i].append(j);adj[j].append(i)
 if t:
  aut=pynauty.autgrp(pynauty.Graph(t,adjacency_dict=adj));order=round(aut[1]*10**aut[2])
 else:order=1
 block_scale.append(math.factorial(t)//order if balanced else 1)
reps=list(range(len(meta)));colblock=[];ci=[];cj=[];div=[]
for b,(t,m,typ,d,keys) in enumerate(meta):
 ii,jj=np.triu_indices(d);colblock.extend([b+1]*len(ii));ci.extend(ii+1);cj.extend(jj+1);div.extend([math.comb(8,t)*math.comb(8-t,m)*math.factorial(t)/block_scale[b]]*len(ii))
colblock=np.array(colblock);ci=np.array(ci);cj=np.array(cj);div=np.array(div);coo=C.tocoo();scale=10000.;B=len(meta)
print('EXPORT FULL ORDERED',C.shape,C.nnz,'maxdim',max(md[3] for md in meta),time.time(),flush=True)
with open(prefix+'_color.dat-s','w') as f:
 print(len(keep),file=f);print(B+2,file=f);print(*([md[3] for md in meta]+[1,-len(keep)]),file=f);print(*[format(float(v*scale),'.17g') for v in target],file=f);print(0,B+1,1,1,1,file=f)
 for row,col,val in zip(coo.row,coo.col,coo.data):print(int(row)+1,int(colblock[col]),int(ci[col]),int(cj[col]),format(float(val/div[col]/(1 if ci[col]==cj[col] else 2)),'.17g'),file=f)
 for row in range(len(keep)):print(row+1,B+1,1,1,1,file=f);print(row+1,B+2,row+1,row+1,1,file=f)
info={'reps':reps,'complement':image,'meta':meta,'scale':scale,'rows':len(keep),'kept_graphs':keep.tolist(),'full_complement_indices':comp.tolist(),'ordered_graph_average':True,'block_scale':block_scale}
Path(prefix+'_color_csdp.json').write_text(json.dumps(info));print('DONE',time.time(),flush=True)
