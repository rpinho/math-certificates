"""Independent exact quintic trace verification and exhaustive local templates.
Does not import the search, quartic checkers, or other quintic checker.
"""
import itertools as it,gzip,json,pathlib,sys
R=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else __file__).resolve()
if R.is_file():R=R.parent
# Enumerate all minimum-support degree-four tensors on eight labelled inputs.
patterns=set()
def tensor_list(chosen):
 masks=[0]
 for block in chosen:
  if len(block)==1:factor=[0,1<<block[0]]
  else:factor=[s for s in range(256) if s&~sum(1<<v for v in block)==0 and s.bit_count()%2==(len(block)%2==0)]
  masks=[a|b for a in masks for b in factor]
 assert len(set(masks))==16
 return tuple(sorted(masks))
def enumerate_factors(chosen,left,cost,lower):
 if cost==4:patterns.add(tensor_list(chosen));return
 for size in range(1,6):
  charge=max(1,size-1)
  if cost+charge>4:continue
  for block in it.combinations(left,size):
   if (size,block)<lower:continue
   enumerate_factors(chosen+[block],[j for j in left if j not in block],cost+charge,(size,block))
enumerate_factors([],list(range(8)),0,(0,()))
for p in patterns:
 used=0;inter=255
 for s in p:used|=s;inter&=s
 assert inter==0
 for j in range(8):
  if used>>j&1:assert sum(bool(s>>j&1) for s in p)==8
 if not all(s.bit_count()==4 for s in p):assert sum(4-s.bit_count() for s in p)>=8
canonical={1|(1<<a)|(1<<b)|(1<<c) for a in (1,2) for b in (3,4) for c in (5,6)}
local=sorted(p for p in patterns if canonical<=set(p))
assert len(local)==5
with gzip.open(R/'quintic14_certificate.json.gz','rt') as f:C=json.load(f)
assert C['schema']=='quintic14-second-weight-v1' and C['n']==14 and C['degree']==5 and C['norm']==48 and C['good_count']==12
assert C['models']==[] and len(C['traces'])==4
pairs=((1,2),(3,4),(5,6),(7,8))
start=frozenset(1|sum(1<<v for v in vs) for vs in it.product(*pairs))
expected=[((0,2,2,2),5),((1,1,2,2),5),((1,2,2,2),4),((2,2,2,2),3)]
visits=0
for ci,(entry,(signature,b)) in enumerate(zip(C['traces'],expected)):
 g=[0]+[1+2*i+t for i,a in enumerate(signature) for t in range(a)]+list(range(9,9+b))
 case=entry['case'];assert case['pair_good_counts']==list(signature) and case['outside_good']==b and case['good']==g
 bad=set(range(14))-set(g)
 def options(j,e,done):
  assert 1<=j<=8 # All frozen branching variables have this checked anchor.
  own=next(i for i,p in enumerate(pairs) if j in p)
  other=[p for i,p in enumerate(pairs) if i!=own]
  labels=[0]+[v for p in other for v in p]
  known=set(labels)|{j};out=set()
  req={s for s in e if s>>j&1};donebits=sum(1<<v for v in done)
  for extra in range(14):
   if extra in known:continue
   mapping=labels+[extra]
   for p in local:
    row=frozenset((1<<j)|sum(1<<mapping[i] for i in range(8) if s>>i&1) for s in p)
    if not req<=row or any(s&donebits and s not in e for s in row) or len(e|row)>48:continue
    out.add(tuple(sorted(row)))
  return sorted(out)
 def check(node,e,done):
  global visits
  visits+=1;kind=node[0];rem=48-len(e)
  loss=sum(5-s.bit_count() for s in e)
  need=sum(max(0,16-sum(bool(s>>j&1) for s in e)) for j in bad)
  unseen=[j for j in g if j not in done and all(not(s>>j&1) for s in e)]
  if kind==0:assert rem<0;return
  if kind==1:assert loss>16;return
  if kind==2:assert need>2*rem;return
  if kind==3:assert len(unseen)>=2 and rem<24;return
  if kind==4:assert unseen and rem<16;return
  assert rem>=0 and loss<=16
  if kind==5:assert node[1] in g and node[1] not in done and not options(node[1],e,done);return
  assert kind==7 # There are no accepted terminal models.
  j=node[1];assert j in g and j not in done
  rows=[tuple(x[0]) for x in node[2]]
  assert len(rows)==len(set(rows)) and set(rows)==set(options(j,e,done)),(ci,j)
  for row,child in node[2]:check(child,e|frozenset(row),done|{j})
 check(entry['tree'],start,{0})
out={'status':'PASS','implementation':'quintic A: exhaustive tensor-role table and complete trace','minimum_templates_on_8':len(patterns),'compatible_local_templates':len(local),'trace_nodes':visits,'excluded_controls':14,'new_second_weight_control_ceiling':13,'additional_external_premise':'Nebe Barnes-Wall second-minimum theorem and written integer-polynomial embedding'}
outdir=R.parent/'receipts' if R.name=='frozen' else R/'receipts';outdir.mkdir(exist_ok=True)
(outdir/'quintic_a.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
