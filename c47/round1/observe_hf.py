"""Observe objective returns while executing unchanged upstream hf.py.
No objective, parameters, settings or decisions are changed. Checkpoint best seen.
"""
import atexit,json,os,runpy,sys,time
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parent
search=root/'sources/tomar-v5/lowerbound/search'
sys.path.insert(0,str(search))
import search as search_module
code=search_module.objective.__code__
best=-1.; best_state=None; last_write=0.; calls=0
start=time.monotonic()
def save():
 global last_write
 if best_state is not None:
  px,py,pts=search_module.decode(best_state['params'],best_state['k'])
  d=dict(best_state,Px=px,Py=py,pts=pts,elapsed_wall_seconds=time.monotonic()-start,
         cpu_seconds=os.times().user+os.times().system,objective_calls=calls,
         status='UNVERIFIED floating provenance probe; not the fixed half-cell certificate')
  tmp=root/'logs/hf-best.tmp'; tmp.write_text(json.dumps(d,indent=1)+'\n');tmp.replace(root/'logs/hf-best.json')
  print('OBSERVER best %.15g k=%d calls=%d CPU=%.1f' % (best,best_state['k'],calls,d['cpu_seconds']),flush=True)
  last_write=time.monotonic()
def observer(frame,event,arg):
 global best,best_state,calls
 if event=='return' and frame.f_code is code:
  calls+=1
  if isinstance(arg,(float,np.floating)) and arg>best:
   best=float(arg);best_state=dict(ratio=best,k=int(frame.f_locals['k']),params=list(map(float,frame.f_locals['p'])))
  if time.monotonic()-last_write>60:save()
sys.setprofile(observer)
atexit.register(save)
sys.argv=[str(search/'hf.py'),'certificates/tomar50-float-start.json','logs/hf-accepted.json','1103']
try:runpy.run_path(str(search/'hf.py'),run_name='__main__')
finally:sys.setprofile(None);save()
