"""Explore 14-control quintic second-weight derivatives using Nebe's gap.
No mathematical bound accepted until a separate verifier and written proof.
"""
import itertools as it,json,pathlib,time,os,functools,gzip
R=pathlib.Path(__file__).resolve().parent
n=13;k=5;q=4
terms=[s for s in range(1<<n) if s.bit_count()<=k];ix={s:i for i,s in enumerate(terms)}
vm=[sum(1<<i for i,s in enumerate(terms) if s>>j&1) for j in range(n)]
def pack(ss):return sum(1<<ix[s] for s in ss)
def unpack(e):
 ss=[]
 while e:
  b=e&-e;e-=b;ss.append(terms[b.bit_length()-1])
 return ss

def tensor(factors,j):
 ss=[1<<j]
 for fac in factors:ss=[a|b for a in ss for b in fac]
 assert len(set(ss))==16
 return pack(ss)
def pairf(pair):return [1<<x for x in pair]
@functools.lru_cache(None)
def all_patterns(j,available):
 out=set()
 def rec(chosen,left,cost,lower):
  if cost==4:
   factors=[]
   for block in chosen:
    if len(block)==1:factors.append([0,1<<block[0]])
    else:
     subs=[sum(1<<block[t] for t in range(len(block)) if z>>t&1) for z in range(1<<len(block))]
     parity=1 if len(block)%2==0 else 0
     factors.append([s for s in subs if s.bit_count()%2==parity])
   out.add(tensor(factors,j));return
  for size in (1,2,3,4,5):
   cost0=1 if size==1 else size-1
   if cost+cost0>4:continue
   for block in it.combinations(left,size):
    key=(size,block)
    if key<lower:continue
    rec(chosen+[block],[v for v in left if v not in block],cost+cost0,key)
 rec([],list(available),0,(0,()))
 return tuple(sorted(out))

pairs0=((1,2),(3,4),(5,6),(7,8))
start=tensor([pairf(p) for p in pairs0],0)
cases=[]
for cs in it.combinations_with_replacement(range(3),4):
 b=8-sum(cs)
 if 0<=b<=4:
  g=[0]+[1+2*i+t for i,a in enumerate(cs) for t in range(a)]+list(range(9,9+b))
  cases.append((cs,b,g))
print('PID',os.getpid(),'cases',[(cs,b) for cs,b,g in cases],flush=True)
summary=[];totalmodels=[];traces=[];t0=time.monotonic()
for ci,(cs,b,good) in enumerate(cases):
 bad=set(range(n))-set(good);nodes=[0];models=set();fallback=[0]
 anchors0={0:None}
 for a,p in enumerate(pairs0):
  for j in p:
   if j in good:anchors0[j]=(0,tuple(pair for z,pair in enumerate(pairs0) if z!=a))
 def candidates(j,e,done,anchors):
  req=e&vm[j];donebits=0
  for v in done:donebits|=vm[v]
  if j in anchors and anchors[j] is not None:
   v,pairs=anchors[j]
   half=pack((1<<j)|(1<<v)|sum(1<<x for x in choice) for choice in it.product(*pairs))
   assert half&req==half
   occupied={j,v}|{x for p in pairs for x in p}
   rows=[]
   for w in range(n):
    if w not in occupied:rows.append((tensor([pairf((v,w))]+[pairf(p) for p in pairs],j),(w,(j,pairs))))
   rows.append((tensor([[0,1<<v]]+[pairf(p) for p in pairs],j),None))
   for pi,p in enumerate(pairs):
    block=(v,)+p
    even=[0]+[(1<<a)|(1<<b) for a,b in it.combinations(block,2)]
    rows.append((tensor([even]+[pairf(p1) for z,p1 in enumerate(pairs) if z!=pi],j),None))
  else:
   fallback[0]+=1
   appeared=0
   for s in unpack(req):appeared|=s
   available=tuple(v for v in range(n) if v!=j and (v not in done or appeared>>v&1))
   assert len(available)<=8,(ci,j,len(available))
   rows=[(p,None) for p in all_patterns(j,available)]
  out=[]
  for p,an in rows:
   if p&req!=req or p&donebits&~e or (p|e).bit_count()>48:continue
   out.append((p,an))
  # Multiple formal decompositions are irrelevant; same unsigned pattern
  # may use any valid recorded anchor for later generation.
  d={}
  for p,an in out:d.setdefault(p,an)
  return sorted(d.items())
 def search(e,done,anchors):
  nodes[0]+=1;ss=unpack(e);rem=48-len(ss)
  if rem<0:return [0]
  loss=sum(5-s.bit_count() for s in ss)
  if loss>32:return [1]
  deficit=sum(max(0,16-sum(bool(s>>j&1) for s in ss)) for j in bad)
  if deficit>4*rem:return [2]
  unseen=[j for j in good if j not in done and e&vm[j]==0]
  if len(unseen)>=2 and rem<24:return [3]
  if unseen and rem<16:return [4]
  if len(done)==9:
   models.add(tuple(ss));return [6]
  chosen=None;choices=None
  # Keep anchored vertices ahead of untouched components.
  remaining=[j for j in good if j not in done]
  anchored=[j for j in remaining if j in anchors]
  for j in anchored or remaining[:1]:
   opts=candidates(j,e,done,anchors)
   if not opts:return [5,j]
   if choices is None or len(opts)<len(choices):chosen=j;choices=opts
  branches=[]
  for p,an in choices:
   aa=dict(anchors)
   if an is not None:
    w,newanchor=an
    if w in good and w not in aa:aa[w]=newanchor
   branches.append([unpack(p),search(e|p,done|{chosen},aa)])
  return [7,chosen,branches]
 trace=search(start,{0},anchors0)
 row={'case':ci,'pair_good_counts':cs,'outside_good':b,'good':good,'nodes':nodes[0],'models':len(models),'fallbacks':fallback[0],'seconds':time.monotonic()-t0}
 summary.append(row);traces.append({'case':row,'tree':trace})
 for model in sorted(models):totalmodels.append({'case':ci,'terms':model})
 print(row,flush=True)
packet={'schema':'quintic13-homogeneous-seed-v1','status':'EXPLORATORY','n':13,'degree':5,'norm':48,'good_count':9,'summary':summary,'models':totalmodels,'traces':traces}
with gzip.open(R/'quintic13_homogeneous_certificate.json.gz','wt') as f:json.dump(packet,f,separators=(',',':'))
print('DONE',len(totalmodels),'bytes',(R/'quintic13_homogeneous_certificate.json.gz').stat().st_size,flush=True)
