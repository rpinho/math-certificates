"""Exact density-cone inclusion audit; no numerical/search/FLINT imports.
Reconstruct initial feasible density via rational slope events on the knot union.
"""
import argparse,json,hashlib
from pathlib import Path
from fractions import Fraction as F
from bisect import bisect_right
p=argparse.ArgumentParser();p.add_argument('cone');p.add_argument('--cert',default='baseline.json');p.add_argument('--output',required=True);a=p.parse_args()
raw=Path(a.cone).read_bytes();C=json.loads(raw);rawc=Path(a.cert).read_bytes();c=json.loads(rawc);e=list(map(F,c['edges']));h=list(map(F,c['node_densities']));tri=[tuple(map(F,t)) for t in C['base']];jumps={}
assert len(tri)==len(set(tri))
if 'old_masses_exact' in C:mass=list(map(F,C['old_masses_exact']))
else:
 assert all(t[1] in e for t in tri)
 mass=[h[e.index(t[1])]*(t[2]-t[0])/2 for t in tri]
assert len(mass)==len(tri) and all(v>=0 for v in mass)
for (l,m,r),w in zip(tri,mass):
 assert 0<l<m<r
 peak=2*w/(r-l)
 for x,j in [(l,peak/(m-l)),(m,-peak/(m-l)-peak/(r-m)),(r,peak/(r-m))]:jumps[x]=jumps.get(x,F(0))+j
points=sorted(set(e)|set(jumps));height=F(0);slope=F(0);last=points[0]
for x in points:
 height+=slope*(x-last);last=x
 if x>=e[-1]:target=h[-1] if x==e[-1] else F(0)
 elif x<e[0]:target=F(0)
 else:
  k=bisect_right(e,x)-1;target=h[k]+(h[k+1]-h[k])*(x-e[k])/(e[k+1]-e[k])
 assert height==target,(x,height,target)
 slope+=jumps.get(x,F(0))
assert slope==0 and height==0
out=dict(status='PASS',cone_sha256=hashlib.sha256(raw).hexdigest(),certificate_sha256=hashlib.sha256(rawc).hexdigest(),variables=len(tri),added=len(C['added']),audited_knots=len(points),exact_initial_mass=str(sum(mass,F(0))),baseline_density_identical=True)
Path(a.output).write_text(json.dumps(out,indent=2));print(json.dumps(out))
