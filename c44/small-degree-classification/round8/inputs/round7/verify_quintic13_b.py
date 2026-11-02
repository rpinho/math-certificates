"""Fresh tensor template construction and fixed-order exhaustive completions.
No imports from any search, trace generator, or other verifier.
"""
import gzip,struct,pathlib,sys,itertools as it,json,math,time
R=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else __file__).resolve()
if R.is_file():R=R.parent
t0=time.monotonic()
# Walsh supports of elementary factors are derived by truth tables.
local={}
for m in range(1,6):
 a=[0]*(1<<m);a[0]=1
 if m>=2:a[-1]=(-1 if m%2==0 else 1)
 for width in [1<<i for i in range(m)]:
  for start in range(0,len(a),2*width):
   for j in range(start,start+width):a[j],a[j+width]=a[j]+a[j+width],a[j]-a[j+width]
 local[m]=[j for j,c in enumerate(a) if c]

types=[]
for r in range(5):
 for pairs in range(5):
  for triples in range(3):
   for fours in range(2):
    for fives in range(2):
     if r+pairs+2*triples+3*fours+4*fives==4:types.append((r,pairs,triples,fours,fives))
assert len(types)==12
base=set()
for tp in types:
 sizes=[s for s,c in zip(range(1,6),tp) for _ in range(c)]
 def embed(at,left,blocks):
  if at==len(sizes):
   terms=[1]
   for block in blocks:
    masks=[sum(1<<block[t] for t in range(len(block)) if s>>t&1) for s in local[len(block)]]
    terms=[a|b for a in terms for b in masks]
   assert len(terms)==16
   base.add(tuple(sorted(terms)));return
  m=sizes[at]
  for block in it.combinations(left,m):
   if at and sizes[at-1]==m and block<blocks[-1]:continue
   embed(at+1,[v for v in left if v not in block],blocks+[block])
 embed(0,list(range(1,13)),[])
assert len(base)==359502
with gzip.open(R/'quintic_minimum_templates.bin.gz','rb') as f:artifact=set(struct.iter_unpack('<16H',f.read()))
assert base==artifact
P=sorted(base);index={};nonhom=[]
for z,row in enumerate(P):
 nonhom.append(any(s.bit_count()<5 for s in row))
 for term in row:index.setdefault(term,[]).append(z)
print('templates independently rebuilt',len(P),'seconds',time.monotonic()-t0,flush=True)

def switch(s,j):return s^(1|(1<<j)) if (s&1!=0)!=(s&(1<<j)!=0) else s

def choices(j,e,done,only_nonhomogeneous):
 needed=[s for s in e if s>>j&1]
 pool=min((index.get(switch(s,j),[]) for s in needed),key=len) if needed else range(len(P))
 donebits=sum(1<<x for x in done)
 for z in pool:
  if only_nonhomogeneous and not nonhom[z]:continue
  row=frozenset(switch(s,j) for s in P[z])
  if not set(needed)<=row or any(s&donebits and s not in e for s in row):continue
  yield row

def possible_residue(e,bad):
 rem=48-len(e);loss=sum(5-s.bit_count() for s in e);eb=sum(bool(s>>bad&1) for s in e)
 for a in range(math.isqrt(rem)+1):
  rest=rem-a*a;b=math.isqrt(rest)
  if b*b!=rest:continue
  if eb+rest!=16 and eb+rest<24:continue
  if loss+5*a*a+4*rest>32:continue
  if eb+rest==16:
   if b>=2:continue
   terms=[s for s in e if s>>bad&1]+([1<<bad] if b else [])
   row=tuple(sorted(switch(s,bad) for s in terms))
   if row not in base or all(s.bit_count()==5 for s in row):continue
  return True
 return False

counts_n=[]
for tp in types:
 if tp==(0,4,0,0,0):continue
 sizes=[s for s,c in zip(range(1,6),tp) for _ in range(c)]
 blocks=[];at=1;orbits=[]
 for m in sizes:
  if not blocks or len(blocks[-1])!=m:orbits.append(at)
  blocks.append(tuple(range(at,at+m)));at+=m
 orbits.append(at)
 seed=[1]
 for block in blocks:
  masks=[sum(1<<block[t] for t in range(len(block)) if s>>t&1) for s in local[len(block)]]
  seed=[a|b for a in seed for b in masks]
 for bad in orbits:
  good=[v for v in range(13) if v!=bad];nodes=[0]
  def complete(e,at):
   nodes[0]+=1;rem=48-len(e)
   if rem<0 or sum(5-s.bit_count() for s in e)>32:return
   if sum(bool(s>>bad&1) for s in e)+rem<16:return
   missing=sum(all(not(s>>v&1) for s in e) for v in good)
   if (missing>=2 and rem<24) or (missing and rem<16):return
   if any(sum(bool(s>>v&1) for s in e)>16 for v in good):return
   if at==12:assert not possible_residue(e,bad),(tp,bad,e);return
   j=good[at]
   for row in choices(j,e,good[:at],True):complete(e|row,at+1)
  complete(frozenset(seed),1);counts_n.append({'type':tp,'bad':bad,'nodes':nodes[0]})
print('nonhomogeneous cases',len(counts_n),'seconds',time.monotonic()-t0,flush=True)
# Homogeneous seed: fixed order of all nine selected good coordinates.
seed=frozenset(1|sum(1<<v for v in x) for x in it.product((1,2),(3,4),(5,6),(7,8)))
counts_h=[];all_models=[]
for cs in it.combinations_with_replacement(range(3),4):
 b=8-sum(cs)
 if not 0<=b<=4:continue
 good=[0]+[1+2*i+t for i,a in enumerate(cs) for t in range(a)]+list(range(9,9+b));bad=set(range(13))-set(good);nodes=[0];models=set()
 def complete_h(e,at):
  nodes[0]+=1;rem=48-len(e)
  if rem<0 or sum(5-s.bit_count() for s in e)>32:return
  if sum(max(0,16-sum(bool(s>>j&1) for s in e)) for j in bad)>4*rem:return
  missing=sum(all(not(s>>v&1) for s in e) for v in good)
  if (missing>=2 and rem<24) or (missing and rem<16):return
  if any(sum(bool(s>>v&1) for s in e)>16 for v in good):return
  if at==9:
   assert rem==16 and sum(all(not(s>>v&1) for s in e) for v in bad)>=2
   models.add(tuple(sorted(e)));return
  j=good[at]
  for row in choices(j,e,good[:at],False):complete_h(e|row,at+1)
 complete_h(seed,1);counts_h.append({'pairs':cs,'outside':b,'nodes':nodes[0],'models':len(models)});all_models.append(models)
 print('homogeneous case',counts_h[-1],flush=True)
# Compare terminal artifacts only after the independent completions.
with gzip.open(R/'quintic13_homogeneous_certificate.json.gz','rt') as f:H=json.load(f)
for ci,models in enumerate(all_models):assert models=={tuple(m['terms']) for m in H['models'] if m['case']==ci}
assert len(counts_n)==31 and len(counts_h)==9
out={'status':'PASS','implementation':'quintic13 B: FWHT factor construction, fixed-order fresh exhaustive completions','templates':len(P),'nonhomogeneous':counts_n,'homogeneous':counts_h,'second_weight_controls_upper':12,'seconds':time.monotonic()-t0}
outdir=R.parent/'receipts' if R.name=='frozen' else R/'receipts';outdir.mkdir(exist_ok=True)
(outdir/'quintic13_b.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS quintic13 B',out['seconds'],flush=True)
