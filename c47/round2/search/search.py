"""Fresh multichain C47 local search; no third-party research code imported.
Scipy optimizers are general-purpose library routines. Floating values unverified.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
import argparse,json,time,resource,math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.ndimage import label,distance_transform_edt,maximum_filter
from objective import load,evaluate,holes
from checkpoint import checkpoint
ap=argparse.ArgumentParser();ap.add_argument('--chain',type=int,required=True);ap.add_argument('--seconds',type=float,default=18000);ap.add_argument('--start',default='certificates/start66-measure.json');ap.add_argument('--seed',type=int);ap.add_argument('--reach',type=float,default=6);a=ap.parse_args()
rng=np.random.default_rng(a.seed or 110870+a.chain);start=time.time();deadline=start+a.seconds
px,py,p=load(a.start);bestq=-1;evals=0;rounds=0;counts={};successes={};bestfile=Path(f'chains/chain{a.chain}-best.json');bestfile.parent.mkdir(exist_ok=True)
trace=open(f'logs/chain{a.chain}.jsonl','a',buffering=1)
def log(event,**kw):
 trace.write(json.dumps(dict(event=event,seconds=time.time()-start,cpu_seconds=time.process_time(),evaluations=evals,**kw))+'\n')
def obj(x,y,z):
 global evals,bestq
 if time.time()>deadline:raise TimeoutError
 evals+=1
 if not(2.7<x<3.9 and 2.2<y<3.3 and 2<=len(z)<=90 and np.min(z[:,2])>1e-9 and np.max(z[:,2])<6):return -100.
 q,area,nr=evaluate(x,y,z,reach=a.reach)
 if q>bestq+1e-13:
  bestq=float(q)
  d=dict(status='UNVERIFIED floating search candidate',Px=x,Py=y,lam=1,pts=z.tolist(),ratio=bestq,area=area,rectangles=nr,chain=a.chain,reach=a.reach,seed=a.seed or 110870+a.chain,evaluations=evals,seconds=time.time()-start,cpu_seconds=time.process_time())
  temp=bestfile.with_suffix('.tmp');temp.write_text(json.dumps(d,indent=1)+'\n');temp.replace(bestfile)
  if q>1.7033694708:Path(f'chains/chain{a.chain}-hit.json').write_text(json.dumps(d,indent=1)+'\n')
 return float(q)
q=obj(px,py,p)
def polish_block(ids,kind='atoms',scale=1.,maxfev=500):
 global p,px,py,q
 base=p.copy();ox,oy=px,py
 if kind=='period':
  def decode(v):
   x=ox*math.exp(v[0]*.001);y=oy*math.exp(v[1]*.001);z=base.copy();z[:,:2]*=[x/ox,y/oy];z[:,2]*=math.exp(v[2]*.002);return x,y,z
  d=3
 elif kind=='masses':
  d=len(ids)
  def decode(v):
   z=base.copy();z[ids,2]*=np.exp(np.clip(v*.03*scale,-5,5));return ox,oy,z
 elif kind=='group':
  # One shared displacement for a coordinate-aligned group, plus its masses.
  d=3
  def decode(v):
   z=base.copy();z[ids,0]=(z[ids,0]+v[0]*.002*scale)%ox;z[ids,1]=(z[ids,1]+v[1]*.002*scale)%oy;z[ids,2]*=math.exp(np.clip(v[2]*.03*scale,-5,5));return ox,oy,z
 else:
  d=3*len(ids)
  def decode(v):
   z=base.copy();t=v.reshape(-1,3);z[ids,:2]=(z[ids,:2]+t[:,:2]*.002*scale)%[ox,oy];z[ids,2]*=np.exp(np.clip(t[:,2]*.05*scale,-5,5));return ox,oy,z
 localbest=[q,(px,py,p.copy())]
 def f(v):
  try:x,y,z=decode(v);v=obj(x,y,z)
  except (OverflowError,ValueError):return 100.
  if v>localbest[0]:localbest[:]=[v,(x,y,z)]
  return -v
 minimize(f,np.zeros(d),method='Powell',options={'maxfev':maxfev,'xtol':2e-4,'ftol':2e-10})
 q=localbest[0];px,py,p=localbest[1]
 checkpoint(bestfile)
def propose_insertion():
 global p,q
 # Find components of the own box-evaluator complement. Some proposals are
 # drawn from the exact start-certificate complement as well.
 if rng.random()<.4:
  from fractions import Fraction as F
  h=json.loads(Path('logs/start-exact-holes.json').read_text())['slabs']
  h=np.array([[float(F(t)) for t in r] for r in h]);w=(h[:,1]-h[:,0])*(h[:,3]-h[:,2]);i=rng.choice(len(h),p=w/w.sum());r=h[i];x=(r[0]+r[1])/2;y=(r[2]+r[3])/2
  ox,oy,_=load('certificates/start66-measure.json');x*=px/ox;y*=py/oy
  rad=min(r[1]-r[0],r[3]-r[2])/2
 else:
  k=850;cover=holes(px,py,p,k);dist=distance_transform_edt(1-cover);maxima=(dist==maximum_filter(dist,size=15))&(dist>0)
  ij=np.argwhere(maxima)
  if not len(ij):return False
  w=dist[maxima]**2;i,j=ij[rng.choice(len(ij),p=w/w.sum())];x=(i+.5)*px/k;y=(j+.5)*py/k;rad=dist[i,j]*min(px,py)/k
 old=p.copy();oldq=q
 mass=max(1e-7,min(.003,4*rad*rad*.5))
 p=np.vstack([p,[x,y,mass]]);q=obj(px,py,p)
 polish_block(np.array([len(p)-1]),scale=3.,maxfev=400)
 if q<=oldq+1e-12:p=old;q=oldq;return False
 return True
def propose_removal():
 global p,q
 candidates=np.flatnonzero(p[:,2]<.02)
 if not len(candidates):return False
 ids=rng.choice(candidates,size=min(3,len(candidates)),replace=False);best=(q,None)
 for i in ids:
  z=np.delete(p,i,axis=0);v=obj(px,py,z)
  if v>best[0]:best=(v,z)
 if best[1] is not None:q,p=best;return True
 # Give removal+near-neighbour mass rebalancing a chance across a small valley.
 if a.chain%2==1:
  i=int(ids[np.argmin(p[ids,2])]);old=p.copy();oldq=q;xy=p[i,:2].copy();m=p[i,2];p=np.delete(p,i,axis=0)
  ds=np.abs(p[:,:2]-xy);ds=np.minimum(ds,[px,py]-ds);near=np.argsort(np.max(ds,axis=1))[:3];p[near,2]+=m/3;q=obj(px,py,p);polish_block(near,'masses',maxfev=250)
  if q>oldq:return True
  p=old;q=oldq
 return False
try:
 log('start',ratio=q,atoms=len(p))
 while time.time()<deadline:
  rounds+=1;before=q
  t=rng.random()
  if rounds%19==0:kind='period';polish_block([],kind,maxfev=400)
  elif rounds%13==0:kind='insertion';propose_insertion()
  elif rounds%17==0:kind='removal';propose_removal()
  elif t<.24:
   kind='masses';ids=rng.choice(np.arange(1,len(p)),size=min(6,len(p)-1),replace=False);polish_block(ids,kind,maxfev=450)
  elif t<.40:
   kind='group';i=int(rng.integers(2,len(p)));axis=int(rng.integers(2));ids=np.flatnonzero(abs(p[:,axis]-p[i,axis])<1e-10);polish_block(ids,kind,maxfev=300)
  else:
   n=2 if (rounds+a.chain)%3 else 3;kind='pair' if n==2 else 'triple'
   # Alternate local and far-apart atom couplings.
   i=int(rng.integers(1,len(p)));ds=np.abs(p[:,:2]-p[i,:2]);ds=np.minimum(ds,[px,py]-ds);near=np.argsort(np.max(ds,axis=1));pool=near[1:9] if rounds%2 else np.delete(np.arange(1,len(p)),max(0,i-1))
   ids=np.r_[i,rng.choice(pool,size=n-1,replace=False)].astype(int)
   polish_block(ids,maxfev=700,scale=[.4,1.,3.][a.chain%3])
  counts[kind]=counts.get(kind,0)+1
  if q>before+1e-12:successes[kind]=successes.get(kind,0)+1
  log('round',round=rounds,kind=kind,ratio=q,best=bestq,gain=q-before,atoms=len(p))
  if rounds%10==0:print(a.chain,rounds,evals,q,bestq,len(p),'seconds',time.time()-start,flush=True)
except TimeoutError:pass
log('done',ratio=q,best=bestq,atoms=len(p),counts=counts,successes=successes)
print('DONE',a.chain,bestq,evals,time.time()-start,'CPU',time.process_time(),flush=True)
