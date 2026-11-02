"""Fresh completion enumeration. Explicit high-control tensor types and FWHT.
Reads no search trace until after independent exclusions.
"""
import itertools as I,json,gzip,pathlib,sys
R=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else __file__).resolve()
if R.is_file():R=R.parent

def match(a):
 if not a:yield [];return
 for t in range(1,len(a)):
  for rest in match(a[1:t]+a[t+1:]):yield [(a[0],a[t])]+rest

def fourier(blocks):
 vals=[]
 for x in range(256):
  value=1
  for block in blocks:
   bits=[(x>>j)&1 for j in block]
   if len(block)==1:value*=1-bits[0]
   elif all(v==0 for v in bits):pass
   elif all(v==1 for v in bits):value*= -1 if len(block)%2==0 else 1
   else:value=0;break
  vals.append(value)
 for width in [1,2,4,8,16,32,64,128]:
  for base in range(0,256,2*width):
   for a in range(base,base+width):
    x,y=vals[a],vals[a+width];vals[a],vals[a+width]=x+y,x-y
 nonzero=frozenset(j for j,v in enumerate(vals) if v)
 assert len(nonzero)==16 and all(abs(vals[j])==16 for j in nonzero)
 return nonzero

# A compatible tensor must use the seven coordinates already present in
# its known top masks. Only these three degree-cost-four types have >=7
# controls: four pairs; one point with three pairs; two pairs with a triple.
all_high=set()
for pairs in match(list(range(8))):all_high.add(fourier(pairs))
for point in range(8):
 for six in I.combinations([j for j in range(8) if j!=point],6):
  for pairs in match(list(six)):all_high.add(fourier([(point,)]+pairs))
for triple in I.combinations(range(8),3):
 for four in I.combinations([j for j in range(8) if j not in triple],4):
  for pairs in match(list(four)):all_high.add(fourier([triple]+pairs))
req=frozenset(1|(1<<a)|(1<<b)|(1<<c) for a in (1,2) for b in (3,4) for c in (5,6))
compatible=[p for p in all_high if req<=p]
assert len(compatible)==5

initial_pairs=[(1,2),(3,4),(5,6),(7,8)]
base=frozenset(1|sum(1<<v for v in choice) for choice in I.product(*initial_pairs))
signatures=[((0,2,2,2),5),((1,1,2,2),5),((1,2,2,2),4),((2,2,2,2),3)]
results=[]
for ci,(counts,b) in enumerate(signatures):
 good=[0]+[1+2*i+t for i,c in enumerate(counts) for t in range(c)]+list(range(9,9+b))
 bad=[j for j in range(14) if j not in good];neighbors=[j for j in good if 1<=j<=8]
 nodes=[0]
 def visit(e,at):
  nodes[0]+=1;rem=48-len(e)
  if rem<0 or sum(5-s.bit_count() for s in e)>16:return
  if any(sum(bool(s>>j&1) for s in e)+rem<16 for j in bad):return
  missing=[j for j in good if all(not(s>>j&1) for s in e)]
  if len(missing)>=2 and rem<24:return
  if missing and rem<16:return
  assert at<len(neighbors),'unexcluded model requires additional classification'
  j=neighbors[at];done=[0]+neighbors[:at]
  other=[p for p in initial_pairs if j not in p];labels=[0]+[v for p in other for v in p]
  choices=set()
  for w in range(14):
   if w==j or w in labels:continue
   mapping=labels+[w]
   for p in compatible:
    row=frozenset((1<<j)|sum(1<<mapping[t] for t in range(8) if s>>t&1) for s in p)
    if not {s for s in e if s>>j&1}<=row:continue
    if any(any(s>>v&1 for v in done) and s not in e for s in row):continue
    choices.add(row)
  for row in choices:visit(e|row,at+1)
 visit(base,0)
 results.append({'case':ci,'nodes':nodes[0]})
with gzip.open(R/'quintic14_certificate.json.gz','rt') as f:C=json.load(f)
assert C['models']==[] and len(C['traces'])==4
out={'status':'PASS','implementation':'quintic B: FWHT local templates and fresh fixed-order completion','high_control_templates':len(all_high),'compatible_templates':len(compatible),'cases':results,'controls_upper':13}
outdir=R.parent/'receipts' if R.name=='frozen' else R/'receipts';outdir.mkdir(exist_ok=True)
(outdir/'quintic_b.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
