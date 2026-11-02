"""Expand the floating CSDP primal matrices; no result here is a bound."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import sys,json
import numpy as np
pfx=sys.argv[1];meta=json.load(open(pfx+'_color_csdp.json'));reps=meta['reps'];blocks={b:np.zeros((meta['meta'][b][3],)*2) for b in reps};btilde=None
with open(pfx+'_color.sol') as f:
 next(f)
 for line in f:
  mat,bl,i,j,val=line.split();mat,bl,i,j=map(int,[mat,bl,i,j]);val=float(val)
  if mat!=2:continue
  if bl<=len(reps):q=blocks[reps[bl-1]];q[i-1,j-1]=q[j-1,i-1]=val/meta['scale']*meta.get('block_scale',[1]*len(meta['reps']))[bl-1]
  elif bl==len(reps)+1:btilde=val/meta['scale']
if meta.get('ordered_graph_average'):
 expanded=[q*.5 for q in blocks.values()]
 for b,(dest,p) in enumerate(meta['complement']):
  p=np.array(p,dtype=int);expanded[dest][np.ix_(p,p)]+=blocks[b]*.5
else:
 expanded=[]
 for b,(c,p) in enumerate(meta['complement']):
  p=np.array(p,dtype=int);q=blocks[min(b,c)]
  if c==b:q=(q+q[np.ix_(p,p)])/2
  elif b!=min(b,c):q=q[np.ix_(p,p)]
  expanded.append(q)
np.savez_compressed(pfx+'_CSDP_Q.npz',**{f'q{i}':q for i,q in enumerate(expanded)})
print('CSDP_FLOAT_OBJECTIVE',btilde,'minimum eigenvalue',min(float(np.linalg.eigvalsh(q)[0]) for q in expanded),flush=True)
