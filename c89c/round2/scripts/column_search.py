"""Primal rank-one column generation for the ordered-root eight-vertex SDP.
Starts with reproduced public certificates. Floating search is not a proof.
"""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','RAYON_NUM_THREADS']:os.environ[key]='1'
import sys,itertools,math,time,json
from pathlib import Path
from fractions import Fraction
import numpy as np
import cvxpy as cp
from types import SimpleNamespace
from scipy import sparse
from scipy.optimize import linprog
import pynauty
k=int(sys.argv[1]);rounds=int(sys.argv[2]) if len(sys.argv)>2 else 12
variant=sys.argv[3] if len(sys.argv)>3 else 'column';prefix='artifacts/ordered8';A=sparse.load_npz(prefix+'.npz').tocsc();nr,nc=A.shape
with open(prefix+'.meta') as f:
 n,mode=map(int,next(f).split());meta=[list(map(int,x.split())) for x in f]
obj=np.loadtxt(prefix+('.objective' if k==6 else '.objective'+str(k)));target=obj[:,0]/obj[:,1]
starts=[];off=0;tri=[];dens=[];lookup={}
for z,(t,m,typ,d,*keys) in enumerate(meta):
 starts.append(off);ii,jj=np.triu_indices(d);tri.append((ii,jj));off+=len(ii);dens.append(math.comb(n,t)*math.comb(n-t,m)*math.factorial(t));lookup[t,m,typ]=z
assert off==nc
columns=[];directions=[];norms=[]
def append(z,L):
 t,m,typ,d,*keys=meta[z];ii,jj=tri[z];Q=L.T@L
 col=np.asarray(A[:,starts[z]:starts[z]+len(ii)]@Q[ii,jj])/dens[z]
 norm=float(np.max(np.abs(col)))
 if norm<1e-30:return
 columns.append(col/norm);norms.append(norm);directions.append((z,L))
def loadcert(filename):
 v=iter(map(int,Path(filename).read_text().split()));n,k,D,B,bn,bd,mode=[next(v) for _ in range(7)];ans=[]
 for _ in range(B):
  t,m,typ,d,r=[next(v) for _ in range(5)];flags=[next(v) for _ in range(d)];L=np.array([[next(v) for _ in range(d)] for _ in range(r)],dtype=float)/D
  ans.append((t,m,typ,flags,L))
 return ans,mode
public,_=loadcert('artifacts/ppss_baseline.cert')
for t,m,typ,flags,L in public:
 z=lookup[t,m,typ];assert flags==meta[z][4:];append(z,L)
def canon(s,code,t):
 adj={i:[] for i in range(s)}
 for j in range(1,s):
  for i in range(j):
   if code>>(j*(j-1)//2+i)&1:adj[i].append(j);adj[j].append(i)
 return pynauty.certificate(pynauty.Graph(s,adjacency_dict=adj,vertex_coloring=[set(range(t)),set(range(t,s))]))
def perm(code,p):
 return sum(((code>>(max(p[i],p[j])*(max(p[i],p[j])-1)//2+min(p[i],p[j])))&1)<<(j*(j-1)//2+i) for j in range(1,len(p)) for i in range(j))
if k==6:
 base,_=loadcert('artifacts/frozen_rows8.cert')
 for t,m,typ,flags,L in base:
  z=lookup[t,m,typ];keys=meta[z][4:];fl={canon(t+m,key,t):i for i,key in enumerate(flags)};mapping=[fl[canon(t+m,key,t)] for key in keys]
  aut=sum(perm(typ,p)==typ for p in itertools.permutations(range(t)));factor=math.factorial(t)//aut
  append(z,L[:,mapping]*math.sqrt(factor))
print('START',k,'directions',len(columns),'time',time.time(),flush=True)
for rnd in range(rounds):
 M=np.column_stack(columns);scale=1e3
 res=linprog(np.r_[np.zeros(len(columns)),-1.],A_ub=np.column_stack((M*scale,np.ones(nr))),b_ub=target*scale,bounds=[(0,None)]*len(columns)+[(0,scale)],method='highs-ipm',options={'threads':1,'time_limit':900,'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10,'small_matrix_value':1e-12})
 if res.x is None:
  ww=cp.Variable(len(columns),nonneg=True);bb=cp.Variable();ineq=M*scale@ww+bb<=target*scale
  prob=cp.Problem(cp.Maximize(bb),[ineq,bb>=0,bb<=scale]);prob.solve(solver='CLARABEL',max_threads=1,tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9,max_iter=150)
  if ww.value is None:print('NO_LP',res.message,prob.status,flush=True);break
  res=SimpleNamespace(x=np.r_[ww.value,bb.value],fun=-float(bb.value),message='Clarabel fallback '+prob.status,ineqlin=SimpleNamespace(marginals=-ineq.dual_value))
 weights=np.maximum(res.x[:-1],0);margin=target-M@weights;actual=float(margin.min())
 print('ROUND',rnd,'cols',len(columns),'status',res.message,'raw',-res.fun/scale,'actual',actual,'time',time.time(),flush=True)
 # Freeze a compact rational square factorization, then evaluate every search row.
 Q=[np.zeros((md[3],md[3])) for md in meta]
 for weight,norm,(z,L) in zip(weights,norms,directions):
  if weight:Q[z]+=(weight/norm)*(L.T@L)
 D=10**12;factors=[];coeff=[]
 for q,(ii,jj),den in zip(Q,tri,dens):
  ev,U=np.linalg.eigh((q+q.T)/2);LL=np.rint(np.sqrt(np.maximum(ev,0))[:,None]*U.T*D).astype(np.int64);factors.append(LL);q2=LL.astype(float).T@LL.astype(float)/D**2;coeff.extend(q2[ii,jj]/den)
 rtarget=target-A@np.array(coeff);b=Fraction(math.floor((float(rtarget.min())-1e-12)*1e15),10**15)
 filename=f'artifacts/{variant}_k{k}_r{rnd}.cert'
 with open(filename,'w') as f:
  print(8,k,D,len(meta),b.numerator,b.denominator,1,file=f)
  for (t,m,typ,d,*flags),LL in zip(meta,factors):
   LL=LL[np.any(LL!=0,axis=1)]
   if len(LL)==0:LL=np.zeros((1,d),dtype=np.int64)
   print(t,m,typ,d,len(LL),file=f);print(*flags,file=f)
   for row in LL:print(*map(int,row),file=f)
 summary={'k':k,'round':rnd,'columns':len(columns),'candidate':str(b),'value':float(b),'actual_LP':actual,'status':res.message}
 Path(filename+'.json').write_text(json.dumps(summary,indent=2));print('CANDIDATE',summary,flush=True)
 np.savez_compressed(f'artifacts/{variant}_k{k}_latest.npz',**{f'q{i}':q for i,q in enumerate(Q)})
 # Dual graph distribution prices every possible PSD square via eigenvalues.
 y=-res.ineqlin.marginals;cost=np.asarray(A.T@y);proposals=[]
 for z,(t,m,typ,d,*keys) in enumerate(meta):
  ii,jj=tri[z];c=cost[starts[z]:starts[z]+len(ii)]/dens[z];S=np.zeros((d,d));S[ii,jj]=c;S=(S+S.T)/2
  ev,U=np.linalg.eigh(S)
  for ell in range(min(2,d)):
   if ev[ell]>=-1e-12:continue
   u=U[:,ell];col=np.asarray(A[:,starts[z]:starts[z]+len(ii)]@(u[ii]*u[jj]))/dens[z];norm=float(np.max(np.abs(col)))
   if norm<1e-30:continue
   price=float(y@col)/norm;proposals.append((price,z,u,col,norm))
 proposals.sort(key=lambda p:p[0]);print('PRICING',len(proposals),'best',proposals[0][0] if proposals else None,flush=True)
 if not proposals:break
 for price,z,u,col,norm in proposals[:80]:columns.append(col/norm);directions.append((z,u[None,:]));norms.append(norm)
print('DONE',k,time.time(),flush=True)
