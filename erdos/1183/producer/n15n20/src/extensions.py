import itertools,json,time
from run import Runner
start=time.time();out=[]
with Runner() as r:
 for n,lb in zip(range(15,21),[9,9,10,10,11,12]):
  tested=0;best=[]
  for tail in itertools.product('01',repeat=n-14):
   word='110010110001101'+''.join(tail);tested+=1
   rows=[]
   for c in (0,1):
    row=r.decide(word,c,lb+1);rows.append(row)
    if row['found']:break
   if len(rows)==2 and not any(x['found'] for x in rows):best.append(dict(word=word,proofs=rows))
  out.append(dict(n=n,lower=lb,tested=tested,words=best))
  print(n,'extensions',tested,'certified_at_bound',len(best),'elapsed',round(time.time()-start,2),flush=True)
json.dump(out,open('logs/extensions.json','w'),indent=2)
