"""Round 10 verifier B: integer maximization, separately written (same agent) tensor multiplicities.
Imports neither generator nor A. Exhaustive energy grid through degree 16.
"""
import itertools,json,pathlib,sys
from fractions import Fraction
root=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parent
artifact=json.loads((root/'certificates/caps.json').read_text())
lemma=json.loads((root/'certificates/near_equality.json').read_text())
assert Fraction(artifact['tail'])==Fraction(9508,1<<96)
assert Fraction(artifact['bound'])==Fraction(artifact['rows'][-1]['R'],1<<96)+Fraction(artifact['tail'])
assert Fraction(artifact['bound'])<Fraction(artifact['strict_claim'])
assert artifact['schema']=='c44-round10-signcaps-v1' and artifact['status']=='candidate, unrefereed'
assert artifact['horizon']==96 and artifact['base_counts']=={'1':1,'2':4,'3':10,'4':22}
assert artifact['near_equality_artifact']=='near_equality.json'
assert lemma['schema']=='c44-near-equality-v1' and lemma['status']=='candidate, unrefereed'
assert lemma['statement']=='k>=3, lambda>=1 and h>2*k*lambda-1/2 imply lambda=1 and h=2*k'
seen=[]
for counts in itertools.product(range(6),range(6),range(3),range(2),range(2),range(2)):
 if sum(c*max(1,m-1) for m,c in enumerate(counts,1))!=5:continue
 sizes=[m for m,c in enumerate(counts,1) for _ in range(c)]
 variables=sum(sizes);loss=32*6-32-16*variables
 assert variables<=10 and (sizes==[2]*5 or loss>=16)
 seen.append({'blocks':sizes,'controls':variables,'terms':32,'deficit':loss})
assert sorted(seen,key=lambda x:x['blocks'])==lemma['degree6_tensor_rows']
case=lemma['direct_case'];assert case==dict(k=6,**{'lambda':'31/16'},norm=124,h=23,partial_minimum=32,partial_gap=16,deficit=8,constant_square='4/3')
assert (6*124-23*32)*2<32 and (23*32)%6!=0

face_records=[]
for dimensions in range(2,9):
 equations=[]
 for fixed in range(dimensions):
  for value in (0,1):
   base=value<<fixed
   remaining=[j for j in range(dimensions) if j!=fixed]
   for subset in range(1<<len(remaining)):
    if subset.bit_count()<2:continue
    vertex=base
    relation=(1<<base) if subset.bit_count()%2==0 else 0
    for index,coordinate in enumerate(remaining):
     if subset>>index&1:
      vertex|=1<<coordinate
      relation^=1<<(base|(1<<coordinate))
    relation^=1<<vertex;equations.append(relation)
 basis=[0]*(1<<dimensions);rank=0
 for relation in equations:
  while relation:
   pivot=(relation&-relation).bit_length()-1
   if basis[pivot]:relation^=basis[pivot]
   else:basis[pivot]=relation;rank+=1;break
 if dimensions==2:
  assert rank==0 # vertex links alone do not force global affine signs here.
 else:
  assert rank==2**dimensions-dimensions-1
  face_records.append(dict(k=dimensions,signs=2**dimensions,rank=rank,nullity=dimensions+1))
assert lemma['sign_completion']==dict(range='s components attain values c-s and c+s, so s<=1 and c=0',cube_face_ranks=face_records,dimension_two_exception=True)
# If c-1 and c+1 both lie in [-1,1], the only denominator-grid c is zero.
assert [c for c in range(-64,65) if -64<=c-64<=64 and -64<=c+64<=64]==[0]

assert artifact['previous_bound']=='159363009872336981657958180965/79228162514264337593543950336'
assert artifact['improvement_bar']=='1/10000'
previous={1:1,2:4,3:10,4:22};records=[]
for d in range(5,97):
 k=d-1;G=1<<(d-2);square=G*G;C=previous[k]
 B=max([G]+[G//2+(previous[t]+1)*(1<<(d-t-2)) for t in range(1,k)])
 zmax=(2*d*square)//(6*G-2)
 low={2*G-(G>>j) for j in range(k)}
 test=set(low)|{2*G}
 # All changes in floor controls, including new half-cell starts.
 for a in range(4*k,(2*k*zmax)//G+2):
  start=(a*G+2*k-1)//(2*k);test.update((start,start+1))
  half=((2*a+1)*G+4*k-1)//(4*k);test.add(half)
 for a in range((4*k*zmax)//(3*G)+2):
  start=(3*a*G+4*k-1)//(4*k)
  if start>=2*G:test.update((start,start+1))
 for integer in range(2,zmax//G+1):test.add(integer*G)
 test={z for z in test if G<=z<=zmax and (z>=2*G or z in low)}
 def at(z):
  h=(2*k*z)//G
  if z%G and (2*k*z)%G==0:h-=1
  if d==5 and 2*z==3*G:h=min(h,10)
  if d==6 and 2*z==3*G:h=min(h,12)
  if d==6 and 4*z==7*G:h=min(h,13)
  # Integer form of the strict near-equality predicate.
  if k>=3 and z>G and 4*k*z-2*h*G<G:h-=1
  cut=min(h,(4*k*z)//(3*G));best=-1
  for t in (cut,h):
   numerator=(2*C+t+1)*square-C*z
   if z>G and 3*t*G>4*k*z:numerator+=min(0,(2*B-C-2*G)*G)
   best=max(best,min(numerator//square,(2*d*square)//z))
  return best
 maximum=max(at(z) for z in test)
 full=None
 if d<=16:
  allpoints={z for z in low if z<=zmax}|set(range(2*G,zmax+1))
  full=len(allpoints);assert maximum==max(at(z) for z in allpoints)
 row=artifact['rows'][d-5]
 assert row['d']==d and row['R']==maximum and row['first_excluded']==maximum+1
 assert Fraction(row['previous'])==Fraction(C,2*G) and Fraction(row['b'])==Fraction(B,2*G)
 previous[d]=maximum
 records.append({'d':d,'R':maximum,'representatives':len(test),'exhaustive_points':full})
assert len(artifact['rows'])==92
assert artifact['caps']=={str(d):str(Fraction(n,1<<d)) for d,n in previous.items()}
tail=Fraction(96**2+3*96+4,1<<96);bound=Fraction(previous[96],1<<96)+tail
assert str(tail)==artifact['tail'] and str(bound)==artifact['bound']
assert bound<Fraction(artifact['strict_claim']) and Fraction(artifact['previous_bound'])-bound>Fraction(1,10000)
assert (previous[5],previous[6],previous[7])==(50,107,229)
result={'status':'PASS','verifier':'B integer maxima and full low-degree grid','bound':str(bound),'tensor_types':len(seen),'rows':records}
out=root.parent/'receipts/final' if root.name=='frozen_final' else root/'receipts'
out.mkdir(exist_ok=True,parents=True)
(out/'verify_b.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
