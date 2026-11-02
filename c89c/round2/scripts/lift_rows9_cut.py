"""Nine-vertex LP using lifted, already certified eight-vertex square blocks."""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','RAYON_NUM_THREADS']:os.environ[key]='1'
import sys,math,json,time
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
import pynauty
which='rows';use_cut=True
inputcert=sys.argv[1] if len(sys.argv)>1 else 'artifacts/frozen_rows8.cert';tag=sys.argv[2] if len(sys.argv)>2 else 'lift9_rows_cut'
pfx='artifacts/base8';v=iter(map(int,Path(inputcert).read_text().split()));n,k,D,B,bn,bd,mode=[next(v) for _ in range(7)];newD=10**12
assert n==8 and mode==0, 'requires eight-vertex unordered-root squares'
blocks=[]
for _ in range(B):
 t,m,typ,d,r=[next(v) for _ in range(5)];flags=[next(v) for _ in range(d)];L=np.array([[next(v) for _ in range(d)] for _ in range(r)],dtype=float)/D;blocks.append((t,m,typ,d,r,flags,L))
with open(pfx+'.meta') as f:
 next(f);meta=[list(map(int,s.split())) for s in f]
starts={};offset=0
for t,m,typ,d,*keys in meta:starts[t,m,typ]=(offset,d,keys);offset+=d*(d+1)//2
with open(pfx+'.coo') as f:nr,nc=map(int,next(f).split());a=np.loadtxt(f,dtype=np.int32).T
A=sparse.coo_matrix((a[2],(a[0],a[1])),shape=(nr,nc)).tocsr();del a
vectors=[]
for t,m,typ,d,r,flags,L in blocks:
 off,dd,ff=starts[t,m,typ];assert dd==d and ff==flags;ii,jj=np.triu_indices(d)
 products=L[:,ii]*L[:,jj] if which=='rows' else (L.T@L)[ii,jj][None,:]
 vectors.append(np.asarray(A[:,off:off+len(ii)]@products.T)/(math.comb(n,t)*math.comb(n-t,m)))
M8=np.column_stack(vectors);del vectors,A
indexfile=Path('artifacts/sub8_indices.npy')
def decode(g6):
 n=ord(g6[0])-63;a={i:[] for i in range(n)};b=0
 for j in range(1,n):
  for i in range(j):
   if (ord(g6[1+b//6])-63)>>(5-b%6)&1:a[i].append(j);a[j].append(i)
   b+=1
 return a
if indexfile.exists():indices=np.load(indexfile)
else:
 lookup={pynauty.certificate(pynauty.Graph(8,adjacency_dict=decode(s))):i for i,s in enumerate(Path('sources/graph8.g6').read_text().splitlines())};indices=[]
 for row,s in enumerate(Path('sources/graph9.g6').read_text().splitlines()):
  adj=decode(s);ix=[]
  for drop in range(9):
   vs=[i for i in range(9) if i!=drop];ren={v:i for i,v in enumerate(vs)};small={ren[v]:[ren[w] for w in adj[v] if w!=drop] for v in vs}
   ix.append(lookup[pynauty.certificate(pynauty.Graph(8,adjacency_dict=small))])
  indices.append(ix)
  if row%10000==0:print('lifting indices',row,time.time(),flush=True)
 indices=np.asarray(indices,dtype=np.int32);np.save(indexfile,indices)
M=np.empty((len(indices),M8.shape[1]))
for start in range(0,len(indices),5000):M[start:start+5000]=M8[indices[start:start+5000]].mean(axis=1)
obj=np.loadtxt('artifacts/odd9.objective');target=obj[:,0]/obj[:,1];norms=np.maximum(np.max(np.abs(M),axis=0),1e-100);M/=norms
print('LP9',which,M.shape,'baseline',bn/bd,'time',time.time(),flush=True);scale=1e5
from types import SimpleNamespace
initial=norms.copy();best=initial.copy();bestvalue=float(np.min(target-M@best));active=set(np.argsort(target-M@best)[:12000].tolist());active.update(np.random.default_rng(42).choice(len(target),3000,replace=False).tolist());lastmessage='baseline'
for cycle in range(6):
 use=np.array(sorted(active),dtype=int)
 print('CUT ROUND',cycle,len(use),time.time(),flush=True)
 trial=linprog(np.r_[np.zeros(M.shape[1]),-1.],A_ub=np.column_stack((M[use]*scale,np.ones(len(use)))),b_ub=target[use]*scale,bounds=[(0,None)]*M.shape[1]+[(0,10)],method='highs',options={'threads':1,'time_limit':600,'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10,'small_matrix_value':1e-12})
 if trial.x is None:print('NO LP',trial.message,flush=True);break
 margin=target-M@np.maximum(trial.x[:-1],0);minimum=float(margin.min());lastmessage=trial.message
 print('CUT RESULT',cycle,'global',minimum,'subset',-trial.fun/scale,flush=True)
 if minimum>bestvalue:bestvalue=minimum;best=np.maximum(trial.x[:-1],0)
 before=len(active);active.update(np.argsort(margin)[:5000].tolist())
 if before==len(active):break
res=SimpleNamespace(x=np.r_[best,bestvalue*scale],fun=-bestvalue*scale,message='cutting planes; '+lastmessage)
print('LP9 RESULT',res.message,res.fun,flush=True);assert res.x is not None
weights=np.maximum(res.x[:-1],0)/norms;np.save('artifacts/'+tag+'_weights.npy',weights);print('ACTUAL',float(np.min(target-M@(weights*norms))),flush=True)
# Evaluate the rounded factors first at order eight, then lift via the frozen index map.
coef=np.zeros(nc);new=[];offw=0
for z,(t,m,typ,d,r,flags,L) in enumerate(blocks):
 if which=='rows':w=weights[offw:offw+r];offw+=r
 else:w=np.repeat(weights[z],r)
 LL=np.rint(np.sqrt(w[:,None])*L*newD).astype(np.int64);new.append(LL);Q=LL.astype(float).T@LL.astype(float)/newD**2;ii,jj=np.triu_indices(d);off,_,_=starts[t,m,typ];coef[off:off+len(ii)]=Q[ii,jj]/(math.comb(n,t)*math.comb(n-t,m))
with open(pfx+'.coo') as f:nr,nc=map(int,next(f).split());a=np.loadtxt(f,dtype=np.int32).T
A=sparse.coo_matrix((a[2],(a[0],a[1])),shape=(nr,nc)).tocsr();vals=A@coef
residual=target-vals[indices].mean(axis=1);b=Fraction(math.floor((float(residual.min())-1e-12)*1e15),10**15)
out=Path('artifacts/'+tag+'.cert')
with out.open('w') as f:
 print(9,6,newD,B,b.numerator,b.denominator,0,file=f)
 for (t,m,typ,d,r,flags,L),LL in zip(blocks,new):
  LL=LL[np.any(LL!=0,axis=1)]
  if len(LL)==0:LL=np.zeros((1,d),dtype=np.int64)
  print(t,m,typ,d,len(LL),file=f);print(*flags,file=f)
  for row in LL:print(*map(int,row),file=f)
summary={'value':float(b),'candidate':str(b),'baseline':bn/bd,'LP_status':res.message,'mode':which,'worst':int(residual.argmin())};Path(str(out)+'.json').write_text(json.dumps(summary,indent=2));print('CANDIDATE9',summary,flush=True)
