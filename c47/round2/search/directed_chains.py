"""Own directed continuation of c47r4 insertion and joint mass/position polish."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
import argparse,json,time,math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from objective import load,evaluate,holes
from checkpoint import checkpoint
from scipy.ndimage import distance_transform_edt,maximum_filter
ap=argparse.ArgumentParser();ap.add_argument('--chain',type=int,required=True);ap.add_argument('--seconds',type=float,default=900);ap.add_argument('--reach',type=float,default=6);a=ap.parse_args()
start=time.time();deadline=start+a.seconds;rng=np.random.default_rng(110870+a.chain)
px,py,p=load('certificates/start66-measure.json');ev=0;best=[-1,None];trace=open(f'logs/directed{a.chain}.jsonl','a',buffering=1)
def log(kind,**kw):trace.write(json.dumps(dict(event=kind,seconds=time.time()-start,cpu_seconds=time.process_time(),evaluations=ev,**kw))+'\n')
def score(x,y,z):
 global ev
 if time.time()>=deadline:raise TimeoutError
 ev+=1
 if not (2.7<x<3.9 and 2.2<y<3.3 and np.min(z[:,2])>1e-10 and np.max(z[:,2])<6):return -100.
 q,ar,nr=evaluate(x,y,z,reach=a.reach);q=float(q)
 if q>best[0]+1e-14:
  best[:]=[q,(x,y,z.copy())]
  d=dict(Px=x,Py=y,lam=1,pts=z.tolist(),ratio=q,area=ar,rectangles=nr,reach=a.reach,chain=a.chain,seed=110870+a.chain,status='UNVERIFIED floating candidate',evaluations=ev,seconds=time.time()-start,cpu_seconds=time.process_time())
  file=Path(f'chains/directed{a.chain}-best.json');tmp=file.with_suffix('.tmp');tmp.write_text(json.dumps(d,indent=1)+'\n');tmp.replace(file)
 return q
q=score(px,py,p)
def polish(z,ids,kind='atoms',maxfev=1500,scale=1):
 base=z.copy();local=[score(px,py,z),z.copy()]
 def f(v):
  zz=base.copy()
  if kind=='masses':zz[ids,2]*=np.exp(np.clip(v*.01,-2,2))
  elif kind=='row':
   zz[ids,:2]=(zz[ids,:2]+np.array(v[:2])*.001*scale)%[px,py];zz[ids,2]*=math.exp(float(np.clip(v[2]*.02,-2,2)))
  else:
   vv=v.reshape(-1,3);zz[ids,:2]=(zz[ids,:2]+vv[:,:2]*.002*scale)%[px,py];zz[ids,2]*=np.exp(np.clip(vv[:,2]*.05,-3,3))
  value=score(px,py,zz)
  if value>local[0]:local[:]=[value,zz]
  return -value
 d=len(ids) if kind=='masses' else 3 if kind=='row' else len(ids)*3
 if kind=='masses':minimize(f,np.zeros(d),method='L-BFGS-B',options=dict(maxfun=maxfev,maxiter=40,ftol=1e-14,gtol=1e-9,eps=1e-4,maxls=15))
 else:minimize(f,np.zeros(d),method='Powell',options=dict(maxfev=maxfev,xtol=1e-5,ftol=1e-12))
 checkpoint(Path(f'chains/directed{a.chain}-best.json'))
 return local[1]
# Each chain starts with a distinct requested insertion. A failed proposal is
# discarded and the saved incumbent restored, before the next target.
inherited_residual=[(2.1085,1.1313),(1.1491,1.1313),(1.1491,1.6103),(1.4899,1.1313),(1.489858,1.610332),(1.767806,1.131348),(2.108516,1.610332),(2.135414,1.034055)]
residual=[(1.149149,1.610332),(2.135414,1.034055),(2.123459,1.131348),(2.123459,1.612826),(1.149149,1.031560),(1.149149,1.707625),(2.135414,1.707625),(1.994946,1.717604)]
try:
 for trial in range(100):
  px,py,p=best[1];oldq=best[0];old=p.copy()
  if trial==0 and a.chain==1:
   # Missing symmetric counterpart of the inherited inside-row filler 58.
   proposals=[(*residual[0],.0002)]
  elif trial==0 and a.chain==2:proposals=[(*residual[0],.0002),(*residual[1],.0002)]
  elif trial==0 and a.chain==3:proposals=[(*residual[1],.0002),(*residual[2],.0002),(*residual[3],.0002)]
  elif trial<9:proposals=[(*residual[(trial-1+a.chain)%len(residual)],.0001)]
  elif trial<29:
   i=50+(trial-9+a.chain)%16;x,y,m=p[i];proposals=[((px-x)%px,y,m)] if trial%2 else [(x,(py-y)%py,m)]
  else:
   k=800;cover=holes(px,py,p,k,reach=a.reach);dist=distance_transform_edt(1-cover);mask=(dist==maximum_filter(dist,size=15))&(dist>0);ij=np.argwhere(mask)
   if not len(ij):break
   weights=dist[mask]**2;i,j=ij[rng.choice(len(ij),p=weights/weights.sum())];rad=dist[i,j]*min(px,py)/k
   proposals=[((i+.5)*px/k,(j+.5)*py/k,max(1e-7,min(.001,2*rad*rad)))]
  z=np.vstack([p,proposals]);insert=np.arange(len(p),len(z));score(px,py,z)
  z=polish(z,insert,maxfev=1000,scale=2)
  # Long coupled polish of inserted atoms and their nearest old neighbours.
  near=[]
  for i in insert:
   ds=np.abs(z[:len(p),:2]-z[i,:2]);ds=np.minimum(ds,[px,py]-ds);near.extend(np.argsort(ds.max(axis=1))[:2])
  ids=np.unique(np.r_[insert,near]).astype(int)
  for rnd in range(10):
   z=polish(z,ids,maxfev=2000)
   z=polish(z,np.arange(1,len(z)),kind='masses',maxfev=4000)
   if best[0]>=oldq+1e-10:z=best[1][2].copy()
   log('polish',trial=trial,round=rnd,ratio=best[0],atoms=len(best[1][2]),proposals=proposals)
   print('chain',a.chain,'trial',trial,'polish',rnd,'best',best[0],'evals',ev,'seconds',time.time()-start,flush=True)
   if best[0]<=oldq+1e-12 and rnd>=1:break
  accepted=best[0]>oldq+1e-12;log('insertion',trial=trial,accepted=accepted,gain=best[0]-oldq,proposals=proposals,ratio=best[0])
  # Coupled row coordinate and mass changes around the incumbent.
  px,py,p=best[1]
  axis=trial%2;i=int(rng.integers(2,50));ids=np.flatnonzero(abs(p[:,axis]-p[i,axis])<1e-10)
  polish(p,ids,kind='row',maxfev=600)
except TimeoutError:pass
log('done',ratio=best[0],atoms=len(best[1][2]));print('DONE',a.chain,best[0],ev,time.time()-start,'CPU',time.process_time(),flush=True)
