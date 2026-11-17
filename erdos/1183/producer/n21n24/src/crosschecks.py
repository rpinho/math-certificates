"""Required restriction and monotonicity comparisons with exact maxima."""
import pathlib,json
from run import Runner

rows=[json.load(p.open()) for p in sorted(pathlib.Path('certificates').glob('upper_n*.json'))]
by_n={r['n']:r for r in rows};out=[]
with Runner() as r:
 for n,row in sorted(by_n.items()):
  if n<21:continue
  assert by_n[n-1]['upper']<=row['upper']
  restrictions=[]
  for label,w in [('prefix',row['word'][:-1]),('suffix',row['word'][1:])]:
   colours=[]
   for c in (0,1):
    t=row['upper']
    while not r.decide(w,c,t)['found']:t-=1
    yes=r.decide(w,c,t);no=r.decide(w,c,t+1);assert not no['found']
    colours.append(dict(colour=c,maximum=t,witness=yes['family'],proof=no['proof']))
   value=max(x['maximum'] for x in colours)
   assert by_n[n-1]['upper']<=value<=row['upper']
   restrictions.append(dict(kind=label,word=w,value=value,colours=colours))
  out.append(dict(n=n,previous_rank_minimum=by_n[n-1]['upper'],rank_minimum=row['upper'],restrictions=restrictions))
pathlib.Path('certificates/crosschecks.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print('RESTRICTION',x['n'],x['previous_rank_minimum'],[a['value'] for a in x['restrictions']],x['rank_minimum'],flush=True)
