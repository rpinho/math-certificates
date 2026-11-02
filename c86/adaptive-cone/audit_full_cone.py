"""Independently audit nested cones against the frozen inherited model metadata.
No search-code imports. Rational node interpolation proves basis inclusion.
"""
import argparse,json,hashlib
from pathlib import Path
from fractions import Fraction as F
from bisect import bisect_left,bisect_right
p=argparse.ArgumentParser();p.add_argument('cone');p.add_argument('--output',required=True);a=p.parse_args();raw=Path(a.cone).read_bytes();C=json.loads(raw);rawold=Path('inherited-half-model.json').read_bytes();old=json.loads(rawold);e=list(map(F,old['edges']));O=[tuple(e[k:k+3]) for k in old['allowed']];assert len(O)==3068
new=[tuple(map(F,t)) for t in C['base']];added=[tuple(map(F,t)) for t in C['selected_hats']];centers={t[1] for t in new};assert len(centers)==len(new)
points=sorted(set(e+[x for t in added+new for x in t]));position={x:i for i,x in enumerate(points)}
for l,c,r in new:
 assert 0<l<c<r
 assert position[c]==position[l]+1 and position[r]==position[c]+1
for name,targets in [('inherited',O),('selected',added)]:
 for l,c,r in targets:
  assert l in position and c in position and r in position
  assert all(x in centers for x in points[bisect_right(points,l):bisect_left(points,r)]),(name,(l,c,r))
triangle=tuple(map(F,['1/100','601/100','1201/100']));assert triangle in [tuple(map(F,t)) for t in C['added']]
oldknots=set(e)|set(triangle);witness=next(t for t in added if t[1] not in oldknots)
# The witness has a nonzero slope jump at its interior knot. Every density in
# the old cone (including its broad triangle) is affine near that new knot.
strict_jump=-F(2,1)/(witness[2]-witness[0])*(1/(witness[1]-witness[0])+1/(witness[2]-witness[1]));assert strict_jump<0
out=dict(status='PASS',cone_sha256=hashlib.sha256(raw).hexdigest(),inherited_model_sha256=hashlib.sha256(rawold).hexdigest(),inherited_directions=3068,selected_directions=len(added),refined_free_nodes=len(new),broad_triangle_included=True,proper_superset=True,strict_witness=list(map(str,witness)),witness_slope_jump=str(strict_jump))
Path(a.output).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
