"""Expand orbit rejection witnesses to EVERY balanced word, check direct closure."""
import json,gzip,itertools,math,time,pathlib
from check import witness,read_open
summary=[];start=time.time()
for n in (15,17,19):
 t=(n+3)//2;pool={}
 with read_open(f'certificates/n{n}_T{t-1}_screen.jsonl.gz') as inp:
  next(inp)
  for line in inp:
   w,c,f=json.loads(line)
   if w.count('1')==(n+1)//2:pool[w]=(c,f)
 count=0
 with gzip.open(f'certificates/n{n}_balanced.jsonl.gz','wt') as out:
  out.write(json.dumps(dict(n=n,threshold=t,kind='all balanced words'))+'\n')
  for ones in itertools.combinations(range(n+1),(n+1)//2):
   bits=['0']*(n+1)
   for i in ones:bits[i]='1'
   w=''.join(bits);inv=''.join('1' if b=='0' else '0' for b in w)
   forms=[(w,False,False),(inv,True,False),(w[::-1],False,True),(inv[::-1],True,True)]
   v,swap,rev=min(forms,key=lambda x:x[0]);c,f=pool[v];c^=swap
   if rev:f=sorted(((1<<n)-1)^S for S in f)
   witness(n,w,c,t,f);count+=1
   out.write(json.dumps([w,c,f],separators=(',',':'))+'\n')
 assert count==math.comb(n+1,(n+1)//2)
 summary.append(dict(n=n,words=count,threshold=t,rejected=count))
 print(summary[-1],round(time.time()-start,2),flush=True)
pathlib.Path('logs/balanced.json').write_text(json.dumps(summary,indent=2)+'\n')
