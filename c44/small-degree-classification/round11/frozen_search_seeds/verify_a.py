"""Exact stored-seed checker A: full ordered Fourier convolution."""
import collections,json,pathlib,sys
from fractions import Fraction as F
R=pathlib.Path(sys.argv[1]);P=json.loads((R/'artifact.json').read_text())
assert P['schema']=='c44-search-seeds-v1' and P['status']=='candidate, unrefereed' and P['source_errors']==[]
assert len(P['seeds'])==8
rows=[]
for name,seed in sorted(P['seeds'].items()):
 assert seed['schema']=='c44-sparse-seed-v1' and seed['status']=='UNVERIFIED proposal'
 p={int(mask):c for mask,c in seed['terms']};den=seed['denominator'];n=seed['count'];d=seed['degree']
 assert len(p)==len(seed['terms']) and all(c and 0<=s<1<<n for s,c in p.items()) and den>0
 used=0;square=collections.defaultdict(int)
 for mask,c in p.items():
  used|=mask
  for other,value in p.items():square[mask^other]+=c*value
 assert {s:c for s,c in square.items() if c}=={0:den*den}
 assert used==(1<<n)-1 and max(s.bit_count() for s in p)==d
 lift=F(n+2,1<<d);assert F(seed['asymptotic_lift'])==lift
 rows.append(dict(name=name,count=n,degree=d,lift=str(lift),homogeneous=all(s.bit_count()==d for s in p)))
assert F(P['lower_claim'])==max([F(3,2)]+[F(r['lift']) for r in rows])==F(3,2)
result=dict(status='PASS',verifier='A ordered full Fourier squares',rows=rows,lower=P['lower_claim'])
if len(sys.argv)>2:pathlib.Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
