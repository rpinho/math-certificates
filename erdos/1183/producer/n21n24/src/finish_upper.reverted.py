"""Produce exact headline maxima for a word found by a standard orbit search."""
import sys,json,pathlib
from run import Runner
n=int(sys.argv[1]);T=int(sys.argv[2]);w=sys.argv[3]
colours=[]
with Runner() as r:
 for c in (0,1):
  m=T
  while not r.decide(w,c,m)['found']:m-=1
  yes=r.decide(w,c,m);no=r.decide(w,c,m+1)
  assert not no['found']
  colours.append(dict(colour=c,maximum=m,witness=yes['family'],proof=no['proof'],nodes=no['nodes']))
row=dict(n=n,word=w,upper=max(x['maximum'] for x in colours),lower={21:12,22:13,23:13,24:14}[n],colours=colours)
pathlib.Path(f'certificates/upper_n{n}.json').write_text(json.dumps(row,indent=2)+'\n')
print(json.dumps(row),flush=True)
