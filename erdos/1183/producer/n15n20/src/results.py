import json,pathlib
from run import Runner
out=[]
with Runner() as r:
 for n,w in [(11,'100010011101'),(12,'1100101100011'),(13,'11001011000110'),(14,'110010110001101')]:
  T={11:7,12:7,13:8,14:8}[n]
  maxima=[]
  for c in (0,1):
   t=T
   while not r.decide(w,c,t)['found']:t-=1
   assert not r.decide(w,c,t+1)['found'];maxima.append(t)
  assert max(maxima)==T
  print('BASELINE',n,maxima,'overall',T,flush=True)
 ext={x['n']:x for x in json.load(open('logs/extensions.json'))}
 for n,lb in zip(range(15,21),[9,9,10,10,11,12]):
  if ext[n]['words']:w=ext[n]['words'][0]['word'];T=lb
  else:
   screen=json.load(open(f'logs/n{n}_T{lb}.json'));w=screen['survivors'][0];T=lb
  colours=[]
  for c in (0,1):
   t=T
   while not r.decide(w,c,t)['found']:t-=1
   pos=r.decide(w,c,t);neg=r.decide(w,c,t+1);assert not neg['found']
   colours.append(dict(colour=c,maximum=t,witness=pos['family'],proof=neg['proof'],nodes=neg['nodes']))
  row=dict(n=n,word=w,upper=max(x['maximum'] for x in colours),lower=lb,colours=colours,rank_minimum=T)
  assert row['upper']==lb;out.append(row);print('RESULT',json.dumps(row),flush=True)
pathlib.Path('certificates/results.json').write_text(json.dumps(out,indent=2)+'\n')
