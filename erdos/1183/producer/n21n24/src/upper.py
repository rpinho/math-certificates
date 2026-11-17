"""First try extensions of the preceding round's best words; emit exact maxima."""
import sys, json, pathlib, itertools, time
from run import Runner, canonical

n=int(sys.argv[1]);published_lb={20:12,21:12,22:13,23:13,24:14}[n]
lb=int(sys.argv[2]) if len(sys.argv)>2 else published_lb
prior=json.load(open('../e1183n15/certificates/results.json'))
prior += [json.load(open(p)) for p in sorted(pathlib.Path('certificates').glob('upper_n*.json'))]
previous=pathlib.Path(f'certificates/n{n-1}_T{lb}/checkpoint.json')
if previous.exists():
 state=json.loads(previous.read_text())
 if not state['stack']:
  # Every good length-n prefix is one of these four symmetry forms.
  # Reusing the completed preceding G-list is the ordinary extension search.
  for w in state['survivors']:
   inv=''.join('1' if b=='0' else '0' for b in w)
   prior += [dict(word=v) for v in (w,w[::-1],inv,inv[::-1])]
seeds=list(dict.fromkeys(x['word'] for x in prior if len(x['word'])<=n+1))
seeds.sort(key=len,reverse=True)
start=time.time();tested=set();best=None
with Runner() as r:
 for seed in seeds:
  for tail in itertools.product('01',repeat=n+1-len(seed)):
   w=seed+''.join(tail)
   if canonical(w) in tested:continue
   tested.add(canonical(w));rows=[]
   for c in (int(w[-1]),1-int(w[-1])):
    row=r.decide(w,c,lb+1);rows.append(row)
    if row['found']:break
   if len(rows)!=2 or any(x['found'] for x in rows):continue
   colours=[]
   for c in (0,1):
    m=lb
    while not r.decide(w,c,m)['found']:m-=1
    yes=r.decide(w,c,m);no=r.decide(w,c,m+1)
    assert not no['found']
    colours.append(dict(colour=c,maximum=m,witness=yes['family'],proof=no['proof'],nodes=no['nodes']))
   best=dict(n=n,word=w,upper=max(x['maximum'] for x in colours),lower=published_lb,colours=colours,
             extensions_tested=len(tested),seconds=time.time()-start)
   pathlib.Path(f'certificates/upper_n{n}.json').write_text(json.dumps(best,indent=2)+'\n')
   print('UPPER',json.dumps(best),flush=True)
   break
  if best:break
pathlib.Path(f'logs/extensions_n{n}.json').write_text(json.dumps(dict(n=n,tested=len(tested),found=bool(best),seconds=time.time()-start))+'\n')
if not best:print('NO LOWER-BOUND EXTENSION',n,len(tested),flush=True)
