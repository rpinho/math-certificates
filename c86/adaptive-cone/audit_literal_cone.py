"""Independent exact audit of literal old-column inclusion and a new kink."""
import argparse,json,hashlib
from pathlib import Path
from fractions import Fraction as F
p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('cone');p.add_argument('--output',required=True);a=p.parse_args();oldraw=Path(a.source).read_bytes();raw=Path(a.cone).read_bytes();old=json.loads(oldraw)['triangles'];c=json.loads(raw);assert c['base']==old
oldknots={F(x) for t in old for x in t};witness=None
for t in c['added']:
 l,m,r=map(F,t);assert 0<l<m<r
 if m not in oldknots:witness=dict(triangle=t,new_knot=str(m),slope_jump=str(-2/((r-l)*(m-l))-2/((r-l)*(r-m))))
assert witness is not None,'No proper-inclusion witness found'
out=dict(status='PASS',source_sha256=hashlib.sha256(oldraw).hexdigest(),cone_sha256=hashlib.sha256(raw).hexdigest(),literal_old_columns=len(old),additional_columns=len(c['added']),proper_inclusion=True,witness=witness)
Path(a.output).write_text(json.dumps(out,indent=2));print(json.dumps(out))
