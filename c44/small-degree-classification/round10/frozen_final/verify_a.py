"""Round 10 exact verifier A. Rational exclusions; explicit tensor products.
No generator, search, or verifier B imports. Depends on inherited replay.
"""
from fractions import Fraction as F
from itertools import product
import hashlib,json,pathlib,sys
R=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parent
P=json.loads((R/'certificates/caps.json').read_text())
T=json.loads((R/'certificates/near_equality.json').read_text())
assert F(P['tail'])==F(9508,1<<96)
assert F(P['bound'])==F(P['rows'][-1]['R'],1<<96)+F(P['tail'])
assert F(P['bound'])<F(P['strict_claim'])
assert P['schema']=='c44-round10-signcaps-v1' and P['status']=='candidate, unrefereed'
assert P['base_counts']==dict(zip(('1','2','3','4'),(1,4,10,22))) and P['horizon']==96
assert P['near_equality_artifact']=='near_equality.json'
assert T['schema']=='c44-near-equality-v1' and T['status']=='candidate, unrefereed'
assert T['statement']=='k>=3, lambda>=1 and h>2*k*lambda-1/2 imply lambda=1 and h=2*k'
# Separately written (same agent) enumeration of the actual Fourier support of each cost-five tensor.
parts=[]
def partition(cost,start,chosen):
 if cost==0:parts.append(chosen);return
 for size in range(start,7):
  c=max(1,size-1)
  if c<=cost:partition(cost-c,size,chosen+[size])
partition(5,1,[])
rows=[]
for sizes in parts:
 masks=[1];at=1
 for size in sizes:
  b=((1<<size)-1)<<at
  local=[s<<at for s in range(1<<size) if size==1 or s.bit_count()%2 != size%2]
  masks=[s|u for s in masks for u in local];at+=size
 assert len(masks)==32 and len(set(masks))==32
 loss=sum(6-s.bit_count() for s in masks)
 assert max(map(int.bit_count,masks))==6
 if sizes==[2]*5:assert loss==0
 else:assert loss>=16 and at-1<=9
 rows.append({'blocks':sizes,'controls':at-1,'terms':len(masks),'deficit':loss})
assert T['degree6_tensor_rows']==rows
assert T['direct_case']=={'k':6,'lambda':'31/16','norm':124,'h':23,'partial_minimum':32,'partial_gap':16,'deficit':8,'constant_square':'4/3'}
assert F(6*124-23*32,6)==F(4,3)
# Negative controls for strictness and the divisibility exception.
for k,x,h,want in [(6,F(31,16),23,True),(6,F(1),12,False),(6,F(47,24),23,False),(2,F(31,16),7,False)]:
 reject=k>=3 and x>1 and F(2*k)*x-h<F(1,2)
 assert reject==want

expected_ranks=[]
for dimension in range(3,9):
 pivots={}
 for i in range(dimension):
  for j in range(i+1,dimension):
   for corner in range(1<<dimension):
    if corner&(1<<i|1<<j):continue
    relation=sum(1<<v for v in (corner,corner^(1<<i),corner^(1<<j),corner^(1<<i)^(1<<j)))
    while relation:
     leading=relation.bit_length()-1
     if leading in pivots:relation^=pivots[leading]
     else:pivots[leading]=relation;break
 assert len(pivots)==(1<<dimension)-dimension-1
 expected_ranks.append(dict(k=dimension,signs=1<<dimension,rank=len(pivots),nullity=dimension+1))
assert T['sign_completion']=={'range':'s components attain values c-s and c+s, so s<=1 and c=0','cube_face_ranks':expected_ranks,'dimension_two_exception':True}
# Each disjoint product attains +/-1. Two components have range width four.
assert max(a+b for a in (-1,1) for b in (-1,1))-min(a+b for a in (-1,1) for b in (-1,1))==4

assert P['previous_bound']=='159363009872336981657958180965/79228162514264337593543950336'
assert P['improvement_bar']=='1/10000'
caps={1:F(1,2),2:F(1),3:F(5,4),4:F(11,8)};audit=[]
assert [r['d'] for r in P['rows']]==list(range(5,97))
for row in P['rows']:
 d=row['d'];k=d-1;M=1<<k;n=row['R']+1;c=caps[k]
 assert row['first_excluded']==n and F(row['previous'])==c
 b=max([F(1,2)]+[F(1,4)+F(1,1<<(t+1))+caps[t]/2 for t in range(1,k)])
 assert F(row['b'])==b
 def hcap(x):
  total=2*k*x;h=int(total)
  if x.denominator>1 and total.denominator==1:h-=1
  if d==5 and x==F(3,2):h=min(h,10)
  if d==6 and x==F(3,2):h=min(h,12)
  if d==6 and x==F(7,4):h=min(h,13)
  if k>=3 and x>1 and total-h<F(1,2):h-=1
  return h
 def budget(x):
  top=hcap(x);hs=range(top+1) if d<=16 else {top,min(top,int(F(4*k,3)*x))}
  values=[]
  for h in hs:
   ordinary=(1<<d)*c+h+1-2*c*x;v=ordinary
   if x>1 and 3*h>4*k*x:
    q=F(2,M);r=F(x-1,M)
    direct=h+(1<<d)*(c*(1-q-r)+(b-F(1,4))*q)
    assert direct==(1<<d)*c+h-2*c*x+4*(b-(c+F(1,2))/2)
    v=min(v,direct)
   values.append((v,h,v<ordinary))
  return max(values)
 limit=F(d*M,n)
 points={2-F(1,1<<j) for j in range(k)}|{F(2)}
 for a in range(4*k,int(2*k*limit)+2):
  z=(a*M+4*k-1)//(4*k)
  points.update(F(2*w,M) for w in (z,z+1))
  z=((2*a+1)*M+8*k-1)//(8*k);points.add(F(2*z,M))
 for a in range(int(F(4*k,3)*limit)+2):
  z=(3*a*M+8*k-1)//(8*k)
  points.update(F(2*w,M) for w in (z,z+1) if w>=M)
 points.update(F(a) for a in range(2,int(limit)+1))
 small={2-F(1,1<<j) for j in range(k)}
 points=sorted(x for x in points if 1<=x<=limit and (x>=2 or x in small))
 assert len(points)==row['representatives']
 peak=max(budget(x)[0] for x in points)
 assert peak<n
 x=F(row['worst']['normalized_weight'])
 assert x in points and budget(x)[0]==peak==F(row['worst']['budget'])
 w=row['feasible'];x=F(w['normalized_weight']);v,h,used=budget(x)
 assert x>=1 and x*(n-1)<=d*M and (x*M/2).denominator==1
 assert x>=2 or x in small
 assert (v,h,used)==(F(w['budget']),w['h'],w['retained']) and v>=n-1
 caps[d]=F(n-1,1<<d)
 assert c<=caps[d]<=F(d,2) and caps[d]-c<=F(d*k,1<<d)
 audit.append({'degree':d,'count':n-1,'peak':str(peak),'slack':str(n-peak)})
assert P['caps']=={str(d):str(v) for d,v in caps.items()}
tail=F(9508,1<<96);bound=caps[96]+tail
assert str(tail)==P['tail'] and str(bound)==P['bound']
assert bound<F(P['strict_claim']) and F(P['previous_bound'])-bound>F(1,10000)
assert [int(caps[d]*(1<<d)) for d in (5,6,7)]==[50,107,229]
O=R.parent/'receipts/final' if R.name=='frozen_final' else R/'receipts';O.mkdir(exist_ok=True,parents=True)
result={'status':'PASS','verifier':'A rational exclusions and tensor supports','bound':str(bound),'rows':audit,'tensor_types':len(parts)}
(O/'verify_a.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
