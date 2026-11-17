"""Full orbit screen, explicit rejection witnesses, and factor-pruned comparison."""
import itertools,json,gzip,time,pathlib,array,sys
from run import Runner,canonical,chain
from check import witness
class Catalogue:
 def __init__(self,n,t,r):
  self.n=n;self.t=t;self.r=r;self.top=(1<<(n+1))-1
  self.table=array.array('i',[-1])*(1<<(n+1));self.families=[];self.calls=0;self.hits=0
 def query(self,w,c):
  R=sum(1<<i for i,ch in enumerate(w) if int(ch)==c)
  idx=self.table[R]
  if idx>=0:
   self.hits+=1;return {'found':True,'family':self.families[idx]}
  if R.bit_count()>=self.t:
   f=chain(w,c)
  else:
   self.calls+=1;row=self.r.decide(w,c,self.t)
   if not row['found']:return row
   f=row['family']
  witness(self.n,w,c,self.t,f)
  support=sum(1<<i for i in {x.bit_count() for x in f})
  idx=len(self.families);self.families.append(f)
  free=self.top^support;sub=free
  while True:
   if self.table[support|sub]<0:self.table[support|sub]=idx
   if not sub:break
   sub=(sub-1)&free
  return {'found':True,'family':f}
 def reject(self,w):
  for c in sorted((0,1),key=lambda c:-w.count(str(c))):
   row=self.query(w,c)
   if row['found']:return c,row
  return None

def full(n,T,r,stop_first=False,label=None):
 label=label or f'n{n}_T{T}'
 cat=Catalogue(n,T+1,r);survivors=[];count=0;rejects=0;start=time.time()
 with gzip.open(f'certificates/{label}_screen.jsonl.gz','wt') as out:
  out.write(json.dumps(dict(n=n,T=T,symmetries=['swap','reversal'],stop_first=stop_first))+'\n')
  for i in range(1<<n): # first letter zero: colour-swap representatives
   w=format(i,f'0{n+1}b')
   if canonical(w)!=w:continue
   count+=1;bad=cat.reject(w)
   if bad:
    c,row=bad;f=row['family'];witness(n,w,c,T+1,f)
    out.write(json.dumps([w,c,f],separators=(',',':'))+'\n');rejects+=1
   else:
    ps=[r.decide(w,c,T+1) for c in (0,1)]
    out.write(json.dumps([w,'survives',[x['proof'] for x in ps]],separators=(',',':'))+'\n');survivors.append(w)
    if stop_first:break
 result=dict(n=n,T=T,orbits=count,rejected=rejects,survivors=survivors,seconds=time.time()-start,search_calls=cat.calls,catalogue_hits=cat.hits,complete=not stop_first)
 pathlib.Path(f'logs/{label}.json').write_text(json.dumps(result,indent=2)+'\n')
 print('SCREEN',n,T,'orbits',count,'rejected',rejects,'survivors',len(survivors),'search calls',cat.calls,'sec',round(result['seconds'],2),flush=True)
 return result

def prefix(n,T,r,expected):
 # No intermediate symmetry pruning. Every bad prefix has an explicit family.
 start=time.time();cats={};leaves=[];prunes=0;visited=0
 with gzip.open(f'certificates/n{n}_T{T}_prefix.jsonl.gz','wt') as out:
  out.write(json.dumps(dict(n=n,T=T,kind='prefix witnesses'))+'\n')
  def walk(w):
   nonlocal prunes,visited
   visited+=1;l=len(w)
   if l not in cats:cats[l]=Catalogue(l-1,T+1,r)
   bad=cats[l].reject(w)
   if bad:
    c,row=bad;f=row['family'];witness(l-1,w,c,T+1,f)
    out.write(json.dumps([w,c,f],separators=(',',':'))+'\n');prunes+=1;return
   if l==n+1:
    if canonical(w)==w:leaves.append(w)
    return
   walk(w+'0');walk(w+'1')
  walk('0') # other half supplied by colour swap
 assert sorted(leaves)==sorted(expected),(n,T,len(leaves),len(expected))
 result=dict(n=n,T=T,visited=visited,pruned=prunes,survivors=len(leaves),seconds=time.time()-start)
 pathlib.Path(f'logs/n{n}_T{T}_prefix.json').write_text(json.dumps(result,indent=2)+'\n');print('PREFIX',result,flush=True)
 return result

if __name__=='__main__':
 results=[]
 with Runner() as r:
  for n in range(11,21):
   lb={11:7,12:7,13:8,14:8,15:9,16:9,17:10,18:10,19:11,20:12}[n]
   # Every rank word is explicitly rejected below the published lower bound.
   low=full(n,lb-1,r);assert not low['survivors'];results.append(low)
   if n in (14,15,16):
    at=full(n,lb,r);results.append(at);prefix(n,lb,r,at['survivors'])
    if not at['survivors']:
     above=full(n,lb+1,r,True);assert above['survivors'];results.append(above)
   elif n in (18,19):
    at=full(n,lb,r);results.append(at)
    if not at['survivors']:
     above=full(n,lb+1,r,True);assert above['survivors'];results.append(above)
  print('TOTAL queries',r.yes,r.no,flush=True)
 pathlib.Path('logs/screens.json').write_text(json.dumps(results,indent=2)+'\n')
