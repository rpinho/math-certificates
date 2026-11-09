"""Release endpoint assembly and hash audit for the referee's regenerated cover.
The referee's cover checker produces every inequality; this checks the saved tiling.
"""
import argparse,json,hashlib
from fractions import Fraction as F
from pathlib import Path
from flint import arb
p=argparse.ArgumentParser();p.add_argument('certificate');p.add_argument('cover');p.add_argument('--output',required=True);a=p.parse_args()
c=json.loads(Path(a.certificate).read_bytes());x=list(map(F,c['edges']));y=list(map(F,c['node_densities']))
expected={i for i in range(len(x)-1) if y[i] or y[i+1]};parts={i:[] for i in expected};parents=0;leaves=0
for line in Path(a.cover).read_text().splitlines():
 r=json.loads(line);i=r['cell'];assert type(i) is int and i in expected
 left,right=F(r['left']),F(r['right']);assert x[i]<=left<right<=x[i+1]
 rows=sorted(r['leaves'],key=lambda row:F(row[0]));assert rows
 assert F(rows[0][0])==left and F(rows[-1][1])==right
 for k,(l,h,lower) in enumerate(rows):
  l,h=F(l),F(h);assert left<=l<h<=right and arb(lower)>0
  if k:assert F(rows[k-1][1])==l
 parts[i].append((left,right));parents+=1;leaves+=len(rows)
for i,rows in parts.items():
 rows.sort();assert rows and rows[0][0]==x[i] and rows[-1][1]==x[i+1]
 assert all(a[1]==b[0] for a,b in zip(rows,rows[1:])), 'gap or overlap'
summary=json.loads(Path(a.cover+'.summary.json').read_text());assert summary['complete'] is True and parents==summary['pieces'] and leaves==summary['leaves'] and arb(summary['minimum'])>0
out=dict(status='PASS',certificate_sha256=hashlib.sha256(Path(a.certificate).read_bytes()).hexdigest(),cover_sha256=hashlib.sha256(Path(a.cover).read_bytes()).hexdigest(),cells=len(expected),parents=parents,leaves=leaves,minimum=summary['minimum'],all_closed_endpoints=True)
Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
