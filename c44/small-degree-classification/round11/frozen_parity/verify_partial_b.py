"""Acceptance B, written from definitions: immutable sets and highest-pivot spans.
No imports from proposer, A, or earlier verifier implementations.
"""
import argparse,itertools,json,pathlib,time
p=argparse.ArgumentParser();p.add_argument('artifact');p.add_argument('--case',type=int);p.add_argument('--positive',action='store_true');a=p.parse_args()
D=json.loads(pathlib.Path(a.artifact).read_text())
assert D['schema']=='c44-parity-partial-v1' and D['status']=='candidate, unrefereed'
assert D['degree']==6 and D['controls']==21 and D['norms']==[120,124]
assert D['minimum_norm']==32 and D['gap']==16 and D['component_variance_numerator']==63
assert D['homogeneous_seed'] is True and D['even_masks'] is True
expected=[]
for N,omitted in [(120,3),(124,4)]:
 for counts in itertools.combinations_with_replacement(range(3),5):
  if sum(counts)>omitted:continue
  b=sum(1<<(1+2*i+j) for i,t in enumerate(counts) for j in range(t))
  b|=sum(1<<(11+j) for j in range(omitted-sum(counts)))
  expected.append(dict(norm=N,omitted=b,seed_pair_counts=list(counts)))
assert D['cases']==expected and len(expected)==15
assert D['conclusion']=={'ceiling':20,'weights':['15/8','31/16'],'R7':227}

def patterns(total,minimum=2):
 if total==0:yield ();return
 for s in range(minimum,total+2):
  for tail in patterns(total-s+1,s):yield(s,)+tail

def submasks(mask):
 t=mask
 while True:
  yield t
  if not t:return
  t=(t-1)&mask

def span_basis(vectors):
 basis={}
 for x in vectors:
  while x:
   j=x.bit_length()-1
   if j in basis:x^=basis[j]
   else:basis[j]=x;break
 space={0}
 for x in basis.values():space|={q^x for q in tuple(space)}
 return len(basis),space

class Check:
 def __init__(self,n,N,selected,positive=False):
  self.n=n;self.N=N;self.selected=selected;self.all=(1<<n)-1;self.positive=positive;self.nodes=0;self.leaves=0
 def tensors(self,chosen,known,done,used):
  # An empty selected partial is seeded by all minimum tensor types.
  # Old coordinates stay fixed; fresh pools are consumed from the high end.
  old=used&~done&~(1<<chosen);fresh=self.all&~used&~(1<<chosen)
  pools=(fresh&self.selected,fresh&~self.selected)
  def build(sizes,at,available,pools,blocks,prior):
   if at==len(sizes):
    terms={1<<chosen}
    for b in blocks:
     choices=[q for q in submasks(b) if q.bit_count()%2!=b.bit_count()%2]
     terms={u|v for u in terms for v in choices}
    assert len(terms)==32
    yield frozenset(terms);return
   s=sizes[at]
   for b in submasks(available):
    c=b.bit_count()
    if c>s:continue
    for x in range(min(s-c,pools[0].bit_count())+1):
     y=s-c-x
     if y>pools[1].bit_count():continue
     role=(s,b,x,y)
     if prior is not None and sizes[at-1]==s and role<prior:continue
     chosen_bits=[];rest=[]
     for pool,amount in zip(pools,(x,y)):
      q=0
      for j in range(amount):bit=1<<(pool.bit_length()-1);q|=bit;pool^=bit
      chosen_bits.append(q);rest.append(pool)
     block=b|chosen_bits[0]|chosen_bits[1]
     yield from build(sizes,at+1,available^b,tuple(rest),blocks+(block,),role)
  for sizes in patterns(5):
   if sum(sizes)>(self.all&~done&~(1<<chosen)).bit_count():continue
   yield from build(sizes,0,old,pools,(),None)
 def visit(self,known,done):
  if self.positive and self.leaves:return
  self.nodes+=1
  energy=[sum(bool(s>>j&1) for s in known) for j in range(self.n)]
  loss=sum(6-s.bit_count() for s in known);used=0
  if len(known)>self.N or loss>6*self.N-32*self.n:return
  for s in known:
   if not s or s.bit_count()>6 or s.bit_count()%2:return
   used|=s
  if any(energy[j]>32 for j in range(self.n) if self.selected>>j&1):return
  need=0
  for j,e in enumerate(energy):
   if done>>j&1:
    assert e==32;continue
   target=32 if self.selected>>j&1 or e<=32 else max(48,2*((e+1)//2))
   need+=target-e
  if need>6*(self.N-len(known)):return
  # A proper component whose vertices are completed cannot gain any terms.
  unseen=used
  while unseen:
   comp=unseen&-unseen
   while True:
    added=comp
    for term in known:
     if term&comp:added|=term
    if added==comp:break
    comp=added
   unseen&=~comp
   if comp&~done==0 and comp!=self.all:return
  if done&self.selected==self.selected:self.leaves+=1;return
  available=[j for j in range(self.n) if self.selected>>j&1 and not done>>j&1 and used>>j&1]
  if not available:
   chosen=max(j for j in range(self.n) if self.selected>>j&1 and not done>>j&1)
   for tensor in self.tensors(chosen,known,done,used):self.visit(known|tensor,done|(1<<chosen))
   return
  chosen=max(available,key=lambda j:(energy[j],-j));required={s for s in known if s>>chosen&1}
  assert len(required)>=16
  origin=min(required);rank,direction=span_basis(s^origin for s in required)
  if rank>5:return
  assert rank>=4
  base={origin^q for q in direction}
  def accept(flat):
   if len(flat)!=32 or any(s.bit_count()>6 or s.bit_count()%2 or (s&done and s not in known) for s in flat):return
   self.visit(known|frozenset(flat),done|(1<<chosen))
  if rank==5:accept(base);return
  active=[j for j in range(self.n) if j!=chosen and used>>j&1]
  fresh=[sorted((j for j in range(self.n) if not used>>j&1 and bool(self.selected>>j&1)==bool(t)),reverse=True) for t in (False,True)]
  seen=set()
  for count in range(min(5,len(active))+1):
   for part in itertools.combinations(active,count):
    mask=(1<<chosen)|sum(1<<j for j in part)
    for x in range(min(5-count,len(fresh[0]))+1):
     for y in range(min(5-count-x,len(fresh[1]))+1):
      extra=mask|sum(1<<j for j in fresh[0][:x]+fresh[1][:y])
      if extra.bit_count()%2 or extra in base:continue
      coset=frozenset(extra^q for q in direction)
      if coset in seen:continue
      seen.add(coset);accept(base|coset)
 def run(self):
  terms=frozenset(1|sum(1<<(1+2*j+((t>>j)&1)) for j in range(5)) for t in range(32))
  self.visit(terms,1)
  return dict(nodes=self.nodes,unsigned_leaves=self.leaves)

if a.positive:
 c=Check(12,64,(1<<12)-1,True);row=c.run();assert row['unsigned_leaves']>0;print(json.dumps(dict(status='PASS',positive=True,**row)),flush=True)
else:
 chosen=range(15) if a.case is None else [a.case]
 for index in chosen:
  row=expected[index];start=time.monotonic();c=Check(21,row['norm'],((1<<21)-1)^row['omitted']);out=c.run();print(json.dumps(dict(case=index,**out,seconds=time.monotonic()-start)),flush=True);assert out['unsigned_leaves']==0
