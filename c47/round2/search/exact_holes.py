"""Complement of the exact certified rectangle union, for insertion proposals."""
import json
from fractions import Fraction as F
from pathlib import Path
def complement(path,out):
 c=json.loads(Path(path).read_text());px,py=map(F,(c['measure']['Px'],c['measure']['Py']))
 rs=[tuple(map(F,w['rectangle'])) for w in c['witnesses']]
 xs=sorted({F(0),px}|{x for r in rs for x in r[:2]});holes=[]
 for a,b in zip(xs,xs[1:]):
  v=sorted((s,t) for l,r,s,t in rs if l<=a and r>=b);end=F(0)
  for s,t in v:
   if s>end:holes.append((a,b,end,s))
   end=max(end,t)
  if end<py:holes.append((a,b,end,py))
 holes.sort(key=lambda r:(r[1]-r[0])*(r[3]-r[2]),reverse=True)
 d={'source':str(path),'meaning':'Uncovered by this exact certified witness union; not a maximal-function upper certificate','uncovered_area':str(px*py-sum(F(0) for _ in [])),
    'slabs':[[str(t) for t in r] for r in holes]}
 d['uncovered_area']=str(sum((b-a)*(t-s) for a,b,s,t in holes))
 Path(out).write_text(json.dumps(d,indent=1)+'\n');return d
if __name__=='__main__':
 import sys
 d=complement(sys.argv[1],sys.argv[2]);print('Uncovered area',d['uncovered_area'],'pieces',len(d['slabs']))
