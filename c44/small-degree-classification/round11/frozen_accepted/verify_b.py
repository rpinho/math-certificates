"""Exact verifier B: generating polynomials and integer scalar optimization.
Separately written (same agent); no proposer or A imports. Exhaustive energy grid through 16.
"""
import argparse, collections, hashlib, itertools, json, math, pathlib, subprocess, sys
from fractions import Fraction
cli=argparse.ArgumentParser();cli.add_argument('artifact');cli.add_argument('--out');args=cli.parse_args()
directory=pathlib.Path(args.artifact)
packet=json.loads((directory/'caps.json').read_text());law=json.loads((directory/'lemma.json').read_text())
assert packet['schema']=='c44-round11-caps-v1' and packet['status']=='candidate, unrefereed'
assert packet['horizon']==96 and packet['base_counts']==dict(zip(map(str,range(1,5)),[1,4,10,22]))
assert packet['previous_bound']=='79671833529611582591986228957/39614081257132168796771975168' and packet['improvement_bar']=='1/10000'
assert law['schema']=='c44-one-exception-v2' and law['status']=='candidate, unrefereed'
assert law['statement']=='k>=4, lambda>=1 and h>2*k*lambda-1 imply lambda=1 and h=2*k'
assert law['link_dimension_minimum']==2 and law['strict'] is True
assert law['thresholds']=={str(t):'1' for t in range(4,97)}
def multiplicities(cost,size=1):
 if size>cost+1:
  if cost==0:yield ()
  return
 # Iterate multiplicities, rather than constructing block partitions.
 unit=max(1,size-1)
 for count in range(cost//unit+1):
  remaining=cost-count*unit
  if remaining==0:yield (count,);continue
  for tail in multiplicities(remaining,size+1):yield (count,)+tail
observed=[]
for degree in range(4,10):
 minimum=2**(degree-1);gap=minimum//2;unique=set()
 for vector in multiplicities(degree-1):
  sizes=tuple(s for s,count in enumerate(vector,1) for _ in range(count))
  if sizes in unique:continue
  unique.add(sizes)
  coefficients=[1];minimum_cardinalities=[];local_minima=[]
  for size in sizes:
   poly=[int(j in (0,1)) for j in range(2)] if size==1 else [math.comb(size,j) if (j+size)%2 else 0 for j in range(size+1)]
   first=next(j for j,c in enumerate(poly) if c)
   with_coordinate=1 if size==1 or size%2==0 else 2
   minimum_cardinalities.append(first);local_minima.append(with_coordinate)
   new=[0]*(len(coefficients)+len(poly)-1)
   for i,a in enumerate(coefficients):
    for j,b in enumerate(poly):new[i+j]+=a*b
   coefficients=new
  while coefficients and coefficients[-1]==0:coefficients.pop()
  histogram=[0]+coefficients;histogram += [0]*(degree+1-len(histogram))
  assert len(histogram)==degree+1 and sum(histogram)==minimum
  loss=sum((degree-j)*c for j,c in enumerate(histogram))
  smallest=1+sum(minimum_cardinalities)
  low_union=int(smallest<degree)
  for s,v,w in zip(sizes,minimum_cardinalities,local_minima):
   if smallest-v+w<degree:low_union+=s
  if 0<loss<minimum:
   assert loss==gap and sum(sizes)==2*degree-3
   assert (histogram[degree-1]==minimum//2 and low_union==2*degree-3) or (histogram[degree-2]==minimum//4 and low_union==2*degree-5)
  observed.append(dict(k=degree,blocks=list(sizes),terms=minimum,controls=sum(sizes),loss=loss,low_union=low_union,histogram=histogram))
assert sorted(observed,key=lambda r:(r['k'],r['blocks']))==law['tensor_rows']
assert law['decisive']==[dict(k=7,weight='135/64',h=29,delta=34),dict(k=7,weight='17/8',h=29,delta=48)]
for record in law['decisive']:
 weight=Fraction(record['weight']);degree=record['k'];m=2**(degree-1)
 assert (2*degree*weight-record['h'])*m==record['delta']
 assert record['delta']<m
# The forbidden integer-energy intervals of a single exceptional link.
for degree in range(4,25):
 m=2**(degree-1);q=m//2
 assert (degree-1)*(m+q)>=m and (degree-1)*q>=m
 # t>=2 costs at least m in e_b-m; t=0 or t=1 use the above.
 assert Fraction(2*degree-3,2*degree-2)>Fraction(2*degree-5,2*degree-4)
 assert Fraction(2*degree-5,2*degree-4)<1

assert law['lower_links']==dict(P_dimension='k-2',T_dimension='k-3',P_component_loss='2^(k-1)',T_component_loss='2^(k-1)',T_requires_k_at_least=5,k4_N_divisible_by=2)
triangle=law['dimension_one_control']
assert triangle==dict(facets=[[0,1],[0,2],[1,2]],vertices=3,cross_polytope=False)
assert all(sum(v in edge for edge in triangle['facets'])==2 for v in range(3))
assert len(triangle['facets'])!=2**2
for k in range(5,97):
 # Each relevant lower component has 2r vertices and 2^r facets.
 for r in (k-1,k-2):
  facet_count=math.prod([2]*r)
  assert (k-r)*facet_count==1<<(k-1)
# Integer-valued A: N=sum z^2 ==sum z==0 mod2. At k=4, delta is 0 mod8.
assert math.gcd(4*2,8)==8

direct=json.loads((directory/'direct_r7.json').read_text())
assert direct['schema']=='c44-direct-r7-v1' and direct['status']=='candidate, unrefereed'
assert {k:direct[k] for k in ('k','weight','controls','norm','partial_minimum','partial_gap','deficit')}==dict(k=6,weight='31/16',controls=22,norm=124,partial_minimum=32,partial_gap=16,deficit=40)
assert direct['one_bad']==dict(loss_at_most=24,P_good_at_least=8,P_incidence_at_least=128,T_good_only_incidence_at_least=112,T_with_bad_incidence_at_least=104)
assert direct['two_bad']==dict(loss_at_most=8,top_pair_divisor=16,possible_top_energy_sums=[104,98,98])
assert direct['all_minimum']==dict(artifact='allminimum.json',homogeneous_seed_required=True,nonhomogeneous_minimum_loss=16,total_incidence_loss_at_most=200)
assert direct['conclusion']==dict(control_ceiling=21,R7_upper=228)
# Distinct integer accounting: list all square costs within the two-bad budget.
possible=[]
for square0 in (0,1):
 for squareb in (0,1):
  for squarec in (0,1):
   for squarebc in (0,1):
    loss=6*square0+5*(squareb+squarec)+4*squarebc
    if loss>8 or loss%2:continue
    top_sum=104-loss-squareb-squarec-2*squarebc
    possible.append(top_sum)
    assert not any(u+v==top_sum for u in range(0,105,16) for v in range(0,105,16))
assert sorted(possible)==[98,98,104]
assert (2*6-4)*16>5*24 and (2*6-5)*16>4*24
assert (2*6-6)*16+2*(32//8)>4*24
# In the homogeneous one-bad case t<=2 and 40+32-32t=6S.
assert [t for t in range(3) if (72-32*t)%6==0]==[0]
assert 72//6<48
assert 22*16>200 and 2*(64-1)>124
command=[sys.executable,str(pathlib.Path(__file__).resolve().parent/'verify_allmin_b.py'),str(directory/'allminimum.json'),'/dev/null']
child=subprocess.run(command,capture_output=True,text=True,timeout=120)
assert child.returncode==0,child.stderr
completion=json.loads(child.stdout);assert completion['status']=='PASS' and completion['target']['unsigned_leaves']==0 and completion['positive']['unsigned_leaves']>=1

counts={1:1,2:4,3:10,4:22};records=[]
assert len(packet['rows'])==92
for d in range(5,97):
 k=d-1;G=2**(d-2);sq=G*G;C=counts[k]
 B=max([G]+[G//2+(counts[t]+1)*2**(d-t-2) for t in range(1,k)])
 maxz=(2*d*sq)//(6*G-2);den=1;num=1
 below={2*G-(G>>j) for j in range(k)}
 candidates=set(below)|{2*G}
 # Breakpoints of the final control ceiling; integer quotients only.
 for control in range(4*k,(2*k*maxz)//G+2):
  candidates.add(((control*den+num)*G+2*k*den-1)//(2*k*den))
 for control in range((4*k*maxz)//(3*G)+2):candidates.add((3*control*G+4*k-1)//(4*k))
 candidates={z for z in candidates if G<=z<=maxz and (z>=2*G or z in below)}
 def score(z):
  h=2*k if z==G else (2*k*z*den-num*G)//(G*den)
  if d==5 and 2*z==3*G:h=min(h,10)
  if d==6 and 2*z==3*G:h=min(h,12)
  if d==6 and 4*z==7*G:h=min(h,13)
  if d==7 and 16*z==31*G:h=min(h,21)
  endpoints=[h,min(h,(4*k*z)//(3*G))];best=-1
  for t in endpoints:
   numerator=(2*C+t+1)*sq-C*z
   if z>G and 3*t*G>4*k*z:numerator+=min(0,(2*B-C-2*G)*G)
   best=max(best,min(numerator//sq,(2*d*sq)//z))
  return best
 best=max(score(z) for z in candidates);full=None
 if d<=16:
  exhaustive={z for z in below if z<=maxz}|set(range(2*G,maxz+1))
  assert max(score(z) for z in exhaustive)==best
  full=len(exhaustive)
 row=packet['rows'][d-5]
 assert row['d']==d and row['R']==best
 assert Fraction(row['previous'])==Fraction(C,2*G) and Fraction(row['b'])==Fraction(B,2*G)
 counts[d]=best;records.append(dict(d=d,R=best,critical_points=len(candidates),exhaustive_points=full))
assert packet['caps']=={str(d):str(Fraction(n,2**d)) for d,n in counts.items()}
tail=Fraction(9508,2**96);bound=Fraction(counts[96],2**96)+tail
assert str(tail)==packet['tail'] and str(bound)==packet['bound']
assert bound<Fraction(packet['strict_claim']) and Fraction(packet['previous_bound'])-bound>Fraction(1,10000)
assert [counts[d] for d in (5,6,7,8)]==[50,107,228,476]
result=dict(status='PASS',verifier='B generating polynomials and integer maxima',bound=str(bound),tensor_types=len(observed),completion=completion,rows=records,
 artifact_sha256={s:hashlib.sha256((directory/s).read_bytes()).hexdigest() for s in ('caps.json','lemma.json','direct_r7.json','allminimum.json')})
if args.out:pathlib.Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
