"""Finite exploratory classification of h=11, lambda=3/2 quartic ternary A.
Unsigned support relaxation only; no exclusion claimed until independently checked.
"""
import itertools as it,json,pathlib,time,sys,os,gzip
R=pathlib.Path(__file__).resolve().parent
n=11
terms=[s for s in range(1<<n) if s.bit_count()<=4]
idx={s:i for i,s in enumerate(terms)}
vm=[sum(1<<i for i,s in enumerate(terms) if s>>j&1) for j in range(n)]
def matchings(a):
 if not a:yield ();return
 x=a[0]
 for j in range(1,len(a)):
  for rem in matchings(a[1:j]+a[j+1:]):yield ((x,a[j]),)+rem

def subsets(a):
 a=list(a)
 return [sum(1<<a[j] for j in range(len(a)) if s>>j&1) for s in range(1<<len(a))]

def supports(j):
 others=[x for x in range(n) if x!=j];out=set()
 def emit(factors):
  ss=[0]
  for f in factors:ss=[a|b for a in ss for b in f]
  p=sum(1<<idx[s|(1<<j)] for s in ss)
  assert p.bit_count()==8
  out.add(p)
 for a in it.combinations(others,3):emit([[0,1<<x] for x in a])
 for fixed in it.combinations(others,2):
  for pair in it.combinations([x for x in others if x not in fixed],2):
   emit([[0,1<<x] for x in fixed]+[[1<<x for x in pair]])
 for u in others:
  rest=[x for x in others if x!=u]
  for tri in it.combinations(rest,3):emit([[0,1<<u],[s for s in subsets(tri) if s.bit_count()%2==0]])
  for four in it.combinations(rest,4):
   for pairs in matchings(list(four)):emit([[0,1<<u]]+[[1<<x for x in p] for p in pairs])
 for four in it.combinations(others,4):emit([[s for s in subsets(four) if s.bit_count()%2]])
 for pair in it.combinations(others,2):
  for tri in it.combinations([x for x in others if x not in pair],3):emit([[1<<x for x in pair],[s for s in subsets(tri) if s.bit_count()%2==0]])
 for six in it.combinations(others,6):
  for pairs in matchings(list(six)):emit([[1<<x for x in p] for p in pairs])
 return sorted(out)
print('PID',os.getpid(),flush=True)
start=time.monotonic()
patterns=[supports(j) for j in range(n)]
indexes=[]
for j,ps in enumerate(patterns):
 d={}
 for z,p in enumerate(ps):
  while p:
   b=p&-p;p-=b;d[b]=d.get(b,0)|(1<<z)
 indexes.append(d)
print('patterns',[len(a) for a in patterns],time.monotonic()-start,flush=True)
E0=sum(1<<idx[1|(1<<a)|(1<<b)|(1<<c)] for a in (1,2) for b in (3,4) for c in (5,6))
casearg=int(sys.argv[1]) if len(sys.argv)>1 else -1
cases=[]
for cs in it.combinations_with_replacement(range(3),3):
 b=6-sum(cs)
 if 0<=b<=4:
  good=[0]+[1+2*i+j for i,a in enumerate(cs) for j in range(a)]+list(range(7,7+b))
  assert len(good)==7
  cases.append((cs,b,good))
def masks(p):
 out=[]
 while p:
  b=p&-p;p-=b;out.append(terms[b.bit_length()-1])
 return out
traces=[];all_models=[];statistics=[]
for ci,(cs,b,good) in enumerate(cases):
 bad=[j for j in range(n) if j not in good]
 count=[0];models=set()
 def build(E,done):
  count[0]+=1
  em=masks(E);remaining=24-len(em)
  if remaining<0:return [0]
  loss=sum(4-s.bit_count() for s in em)
  if loss>8:return [1]
  needed=sum(max(0,8-sum(bool(s>>j&1) for s in em)) for j in bad)
  if needed>4*remaining:return [2]
  if len(done)==7:
   unused=[j for j in bad if all(not(s>>j&1) for s in em)]
   assert remaining==8 and len(unused)>=2,(ci,em,remaining,unused)
   models.add(tuple(em))
   return [4]
  processed=0
  for j in done:processed|=vm[j]
  chosen=None;poss=None
  for j in good:
   if j in done:continue
   ds=(1<<len(patterns[j]))-1;req=E&vm[j]
   while req:
    bit=req&-req;req-=bit;ds &= indexes[j].get(bit,0)
   valid=[]
   while ds:
    zbit=ds&-ds;ds-=zbit;z=zbit.bit_length()-1;p=patterns[j][z]
    if p&processed&~E:continue
    if (E|p).bit_count()>24:continue
    valid.append(z)
   if not valid:return [3,j]
   if poss is None or len(valid)<len(poss):chosen=j;poss=valid
  return [5,chosen,[[z,build(E|patterns[chosen][z],done|{chosen})] for z in poss]]
 tree=build(E0,{0})
 traces.append({'pair_good_counts':cs,'outside_good':b,'good':good,'tree':tree})
 for em in sorted(models):all_models.append({'case':ci,'terms':em,'remaining_energy':8,'unused':[j for j in bad if all(not(s>>j&1) for s in em)]})
 statistics.append({'case':ci,'nodes':count[0],'models':len(models)})
 print(statistics[-1],flush=True)
packet={'schema':'quartic-ternary-second-weight-controls-v1','status':'candidate, unrefereed',
 'n':11,'degree':4,'denominator':16,'squared_numerator_norm':24,'good_count':7,
 'pattern_count':11880,'patterns0':[masks(p) for p in patterns[0]],'cases':traces,
 'models':all_models,'statistics':statistics,
 'conclusion':'No 11-control quartic ternary polynomial with p=3/32; hence second-weight control ceiling is 10.'}
with gzip.open(R/'quartic_certificate.json.gz','wt') as f:json.dump(packet,f,separators=(',',':'))
print('certificate bytes',(R/'quartic_certificate.json.gz').stat().st_size,flush=True)
