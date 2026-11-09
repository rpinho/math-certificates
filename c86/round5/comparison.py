"""Exact finite normalized mean, decimal ceiling and public comparison margins."""
from fractions import Fraction as F
from pathlib import Path
import json
c=json.loads(Path('certificate.json').read_text());x=list(map(F,c['edges']));h=list(map(F,c['node_densities']))
m=sum(F((b-a)*(u+v), 2) for a,b,u,v in zip(x,x[1:],h,h[1:]))
t=sum(F((b-a)*((2*a+b)*u+(a+2*b)*v), 6) for a,b,u,v in zip(x,x[1:],h,h[1:]))
q=F(t,m);assert q==F(c['bound'])
assert -(-q.numerator*10**10//q.denominator)==18054939963
margins={v:str(F(v)-q) for v in ['1.8054956','1.80560940','1.8084990']}
for v,floor in zip(margins,['0.0000016037','0.0001154037','0.0030050037']):assert F(margins[v])>F(floor)
public=F('780597977251274792019360777060007/432345564227458232572250425393152');assert public>q
out=dict(bound=str(q),mass=str(m),trace=str(t),roundup='1.8054939963',display_margins=margins,pr270_exact_margin=str(public-q))
Path('release_validation/comparison.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
