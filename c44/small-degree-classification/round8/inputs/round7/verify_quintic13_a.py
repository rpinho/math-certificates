"""Exact trace verification on all minimum-partial templates, no search imports."""
import gzip,json,pathlib,sys,struct,math
R=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else __file__).resolve()
if R.is_file():R=R.parent
with gzip.open(R/'quintic_minimum_templates.bin.gz','rb') as f:raw=f.read()
assert len(raw)%32==0
P=list(struct.iter_unpack('<16H',raw));assert len(P)==359502 and P==sorted(set(P))
index={};nonhom=[]
for z,p in enumerate(P):
 assert all(s&1 and s.bit_count()<=5 for s in p)
 intersection=(1<<13)-1;counts=[0]*13
 for s in p:
  intersection &=s
  for j in range(13):counts[j]+=bool(s>>j&1)
 assert intersection==1 and counts[0]==16 and all(c in (0,8) for c in counts[1:])
 nh=any(s.bit_count()!=5 for s in p);nonhom.append(nh)
 if nh:assert sum(5-s.bit_count() for s in p)>=8
 for s in p:index.setdefault(s,[]).append(z)
patterns_set=set(P)
def swap(s,j):return s^(1|(1<<j)) if bool(s&1)!=bool(s&(1<<j)) else s

def options(j,e,done,nh,lossfilter=False):
 req=[s for s in e if s>>j&1];pool=min((index.get(swap(t,j),[]) for t in req),key=len) if req else range(len(P))
 donebits=sum(1<<v for v in done);currentloss=sum(5-s.bit_count() for s in e);out={}
 for z in pool:
  if nh and not nonhom[z]:continue
  row=tuple(sorted(swap(t,j) for t in P[z]));ss=set(row)
  if any(t not in ss for t in req) or any(t&donebits and t not in e for t in row):continue
  u=e|ss
  if len(u)>48:continue
  if lossfilter and sum(5-s.bit_count() for s in u)>32:continue
  out[z]=row
 return out

def residual(e,bad):
 rem=48-len(e);loss=sum(5-s.bit_count() for s in e);energy=sum(bool(s>>bad&1) for s in e)
 for a in range(math.isqrt(max(0,rem))+1):
  b2=rem-a*a;b=math.isqrt(b2)
  if b*b!=b2:continue
  be=energy+b2
  if be!=16 and be<24:continue
  if loss+5*a*a+4*b2>32:continue
  if be==16:
   if b>1:continue
   masks=[s for s in e if s>>bad&1]+([1<<bad] if b else [])
   canon=tuple(sorted(swap(t,bad) for t in masks))
   if canon not in patterns_set or not any(t.bit_count()!=5 for t in canon):continue
  return True
 return False

visits=[0,0];models=[]
# Case with a homogeneous good partial, nine selected good coordinates.
with gzip.open(R/'quintic13_homogeneous_certificate.json.gz','rt') as f:H=json.load(f)
assert H['n']==13 and H['good_count']==9 and len(H['traces'])==9
pairs=((1,2),(3,4),(5,6),(7,8))
from itertools import product,combinations_with_replacement
E0=set(1|sum(1<<v for v in choice) for choice in product(*pairs))
sigs=[(cs,8-sum(cs)) for cs in combinations_with_replacement(range(3),4) if 0<=8-sum(cs)<=4]
for ci,(entry,(cs,b)) in enumerate(zip(H['traces'],sigs)):
 good=[0]+[1+2*i+t for i,a in enumerate(cs) for t in range(a)]+list(range(9,9+b));bad=set(range(13))-set(good);found=set()
 assert entry['case']['good']==good and entry['case']['pair_good_counts']==list(cs) and entry['case']['outside_good']==b
 def check_h(node,e,done):
  visits[0]+=1;kind=node[0];rem=48-len(e);loss=sum(5-s.bit_count() for s in e)
  deficit=sum(max(0,16-sum(bool(s>>j&1) for s in e)) for j in bad)
  unseen=[j for j in good if j not in done and all(not(s>>j&1) for s in e)]
  if kind==0:assert rem<0;return
  if kind==1:assert loss>32;return
  if kind==2:assert deficit>4*rem;return
  if kind==3:assert len(unseen)>=2 and rem<24;return
  if kind==4:assert unseen and rem<16;return
  if kind==5:assert node[1] in good and node[1] not in done and not options(node[1],e,done,False);return
  if kind==6:
   assert len(done)==9 and rem==16
   assert sum(all(not(s>>j&1) for s in e) for j in bad)>=2
   found.add(tuple(sorted(e)));return
  assert kind==7
  j=node[1];assert j in good and j not in done
  opts=set(options(j,e,done,False).values());given=[tuple(x[0]) for x in node[2]]
  assert len(given)==len(set(given)) and set(given)==opts,(ci,j)
  for row,child in node[2]:check_h(child,e|set(row),done|{j})
 check_h(entry['tree'],E0,{0})
 assert found=={tuple(m['terms']) for m in H['models'] if m['case']==ci}
 models.extend(found)
assert len(models)==10
# Case with no homogeneous minimum partial; the energy calculation forces
# at least twelve good coordinates, so only one unselected coordinate.
C=json.loads((R/'quintic13_nonhomogeneous_certificate.json').read_text())
assert C['schema']=='quintic13-nonhomogeneous-v1' and C['template_count']==len(P) and len(C['cases'])==31
expected=[]
for r in range(5):
 for b2 in range(5):
  for b3 in range(3):
   for b4 in range(2):
    for b5 in range(2):
     if r+b2+2*b3+3*b4+4*b5!=4 or b2==4:continue
     sizes=[s for s,c in [(1,r),(2,b2),(3,b3),(4,b4),(5,b5)] for _ in range(c)]
     blocks=[];at=1;orbits=[]
     for size in sizes:
      if not blocks or len(blocks[-1])!=size:orbits.append(at)
      blocks.append(tuple(range(at,at+size)));at+=size
     orbits.append(at)
     seed=[1]
     for block in blocks:
      if len(block)==1:factors=[0,1<<block[0]]
      else:factors=[s for s in range(8192) if not(s&~sum(1<<v for v in block)) and s.bit_count()%2==(len(block)%2==0)]
      seed=[a|b for a in seed for b in factors]
     for bad in orbits:expected.append(([r,b2,b3,b4,b5],bad,set(seed)))
assert len(expected)==31
for entry,(type_,bad,seed) in zip(C['cases'],expected):
 assert entry['type']==type_ and entry['bad']==bad and entry['models']==0
 good=set(range(13))-{bad}
 def check_n(node,e,done):
  visits[1]+=1;kind=node[0];rem=48-len(e);loss=sum(5-s.bit_count() for s in e)
  eb=sum(bool(s>>bad&1) for s in e);unseen=sum(all(not(s>>j&1) for s in e) for j in good)
  if kind==0:assert rem<0;return
  if kind==1:assert loss>32;return
  if kind==2:assert eb+rem<16;return
  if kind==3:assert (unseen>=2 and rem<24) or (unseen and rem<16);return
  if kind==7:assert len(done)==12 and not residual(e,bad);return
  if kind==8:assert node[1] in good and sum(bool(s>>node[1]&1) for s in e)>16;return
  assert rem>=0 and loss<=32
  if kind==4:
   j=node[1];assert j in good and j not in done and not options(j,e,done,True,True);return
  assert kind==5
  j=node[1];assert j in good and j not in done
  opts=options(j,e,done,True,True);given=[z for z,ch in node[2]]
  assert len(given)==len(set(given)) and set(given)==set(opts),(type_,bad,j)
  for z,child in node[2]:check_n(child,e|set(opts[z]),done|{j})
 check_n(entry['tree'],seed,{0})
out={'status':'PASS','implementation':'quintic13 A: full-template trace verification','templates':len(P),'homogeneous_seed_nodes':visits[0],'nonhomogeneous_nodes':visits[1],'unsigned_terminal_models_rejected':10,'cases':[9,31],'second_weight_controls_upper':12}
outdir=R.parent/'receipts' if R.name=='frozen' else R/'receipts';outdir.mkdir(exist_ok=True)
(outdir/'quintic13_a.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
