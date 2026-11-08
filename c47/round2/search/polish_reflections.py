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
ap=argparse.ArgumentParser();ap.add_argument('--chain',type=int,required=True);ap.add_argument('--seconds',type=float,default=900);ap.add_argument('--reach',type=float,default=6);ap.add_argument('--start',default='chains/best-snapshot.json');ap.add_argument('--first',type=int,default=75);a=ap.parse_args()
start=time.time();deadline=start+a.seconds;rng=np.random.default_rng(110870+a.chain)
px,py,p=load(a.start);ev=0;best=[-1,None];trace=open(f'logs/directed{a.chain}.jsonl','a',buffering=1)
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

# Long polish of the accepted reflective insertion, with its current nearest
# neighbours. Relative target locations let a later exact incumbent move rows.
targets=p[a.first:,:2]/[px,py]
try:
 ids=np.arange(a.first,len(p));p=polish(p,ids,maxfev=1300,scale=2)
 for rnd in range(100):
  from fractions import Fraction as F
  meta=json.loads(Path('certificates/best.json').read_text())
  if float(F(meta['ratio']))>best[0]+1e-11:
   xx,yy,zz=load(meta['certificate']);score(xx,yy,zz)
  px,py,p=best[1];before=best[0];ids=[]
  for target in targets:
   ds=np.abs(p[:,:2]-target*[px,py]);ds=np.minimum(ds,[px,py]-ds)
   ids.extend(np.argsort(ds.max(axis=1))[:3])
  if rnd%3==2:
   extra=np.flatnonzero(p[:,2]<.003)
   ids.extend(rng.choice(extra,size=min(3,len(extra)),replace=False))
  ids=np.unique(ids).astype(int)
  z=polish(p,ids,maxfev=2600)
  z=polish(z,np.arange(1,len(z)),kind='masses',maxfev=3500)
  log('polish',trial='accepted-reflections',round=rnd,ratio=best[0],atoms=len(best[1][2]),gain=best[0]-before)
  print('REFLECTION POLISH',rnd,best[0],len(best[1][2]),ev,time.time()-start,flush=True)
except TimeoutError:pass
checkpoint(Path(f'chains/directed{a.chain}-best.json'))
log('done',ratio=best[0],atoms=len(best[1][2]));print('DONE REFLECTION POLISH',best[0],ev,time.time()-start,'CPU',time.process_time(),flush=True)
