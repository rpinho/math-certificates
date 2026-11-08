"""Small geometric summary of an exact certificate and its complement."""
import json,sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.ndimage import label,distance_transform_edt
from objective import load,evaluate,holes
src=sys.argv[1];px,py,p=load(src);reach=float(json.loads(Path(src).read_text()).get('reach',6));cover=holes(px,py,p,k=1100,reach=reach);lab,num=label(1-cover);dist=distance_transform_edt(1-cover)
components=[]
for i in range(1,num+1):
 ij=np.argwhere(lab==i);ds=dist[lab==i];a,b=ij[np.argmax(ds)];components.append(dict(grid_area=float(len(ij)*px*py/1100**2),center=[float((a+.5)*px/1100),float((b+.5)*py/1100)],grid_inradius=float(ds.max()*min(px,py)/1100),pixels=len(ij)))
components.sort(key=lambda d:d['grid_area'],reverse=True)
d=dict(source=src,period=[px,py],mass=float(p[:,2].sum()),floating_ratio=float(evaluate(px,py,p,reach=reach)[0]),atoms=len(p),components=components[:50],total_uncovered_grid_area=float(np.sum(1-cover)*px*py/1100**2),qualification='grid diagnostics; exact certificate alone proves the ratio')
out=Path(sys.argv[2]);out.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
