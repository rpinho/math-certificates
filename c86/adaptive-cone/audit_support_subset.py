"""Exact support inclusion, independent of search/basis code."""
import argparse,json,hashlib
from pathlib import Path
from fractions import Fraction as F
from bisect import bisect_right
p=argparse.ArgumentParser();p.add_argument('certificate');p.add_argument('--baseline',default='baseline.json');p.add_argument('--output',required=True);a=p.parse_args();raw=Path(a.certificate).read_bytes();c=json.loads(raw);oldraw=Path(a.baseline).read_bytes();old=json.loads(oldraw);e=list(map(F,old['edges']));h=list(map(F,old['node_densities']));ee=list(map(F,c['edges']));hh=list(map(F,c['node_densities']));cells=0
for l,r,u,v in zip(ee,ee[1:],hh,hh[1:]):
 if not(u or v):continue
 assert e[0]<=l<r<=e[-1];k=bisect_right(e,l)-1
 while k<len(e)-1 and e[k]<r:
  if max(l,e[k])<min(r,e[k+1]):assert h[k]>0 or h[k+1]>0,('new mass in old open gap',l,r,k)
  k+=1
 cells+=1
out=dict(status='PASS',certificate_sha256=hashlib.sha256(raw).hexdigest(),baseline_sha256=hashlib.sha256(oldraw).hexdigest(),positive_cells=cells,support_subset=True)
Path(a.output).write_text(json.dumps(out,indent=2));print(json.dumps(out))
