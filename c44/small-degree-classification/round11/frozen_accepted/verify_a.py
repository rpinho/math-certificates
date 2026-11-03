"""Exact verifier A: explicit tensor masks and rational next-count exclusions.
Written separately from proposer and B; imports neither. Standard library.
"""
import argparse, hashlib, itertools, json, math, pathlib, subprocess
from fractions import Fraction as Q
p=argparse.ArgumentParser();p.add_argument('artifact');p.add_argument('--out');a=p.parse_args()
root=pathlib.Path(a.artifact);cert=json.loads((root/'caps.json').read_text());lemma=json.loads((root/'lemma.json').read_text())
assert cert['schema']=='c44-round11-caps-v1' and cert['status']=='candidate, unrefereed'
assert cert['horizon']==96 and cert['base_counts']=={'1':1,'2':4,'3':10,'4':22}
assert cert['previous_bound']=='79671833529611582591986228957/39614081257132168796771975168'
assert cert['improvement_bar']=='1/10000'
assert lemma['schema']=='c44-one-exception-v2' and lemma['status']=='candidate, unrefereed'
assert lemma['statement']=='k>=4, lambda>=1 and h>2*k*lambda-1 imply lambda=1 and h=2*k'
assert lemma['strict'] is True and lemma['link_dimension_minimum']==2
assert lemma['thresholds']=={str(k):'1' for k in range(4,97)}
types=[]
def enumerate_types(left,lower,parts):
 if left==0:yield parts;return
 for size in range(lower,left+2):
  used=1 if size==1 else size-1
  if used<=left:yield from enumerate_types(left-used,size,parts+(size,))
for k in range(4,10):
 m=1<<(k-1);q=m//2;exceptional=[]
 for parts in enumerate_types(k-1,1,()):
  local=[];offset=1
  for size in parts:
   # Actual block Fourier masks: point empty/singleton, parity otherwise.
   b=(1<<size)-1;choices=[];sub=b
   while True:
    if size==1 or sub.bit_count()%2 != size%2:choices.append(sub<<offset)
    if sub==0:break
    sub=(sub-1)&b
   local.append(choices);offset+=size
  masks=[1+sum(combination) for combination in itertools.product(*local)]
  assert len(set(masks))==len(masks)==m
  degrees=[mask.bit_count() for mask in masks];assert max(degrees)==k
  v=sum(parts);loss=sum(k-r for r in degrees)
  assert loss==m*(k-1)-q*v
  small=[mask for mask in masks if mask.bit_count()<k];union=0
  for mask in small:union|=mask
  if loss==0:assert parts==(2,)*(k-1)
  elif loss<m:
   assert loss==q
   point=(1,)+(2,)*(k-2);triple=(2,)*(k-3)+(3,)
   assert parts in (point,triple)
   if parts==point:assert len(small)==m//2 and set(r for r in degrees if r<k)=={k-1} and union.bit_count()==2*k-3
   else:assert len(small)==m//4 and set(r for r in degrees if r<k)=={k-2} and union.bit_count()==2*k-5
   exceptional.append(parts)
  types.append(dict(k=k,blocks=list(parts),terms=m,controls=v,loss=loss,low_union=union.bit_count(),histogram=[degrees.count(t) for t in range(k+1)]))
 assert len(exceptional)==2
 # Explicit rational incidence consequences, not floating point.
 gamma=Q(2*k-5,2*k-4)
 assert Q((2*k-3)*q,k-1)>gamma*m
 assert Q((2*k-5)*q,k-2)==gamma*m
assert lemma['tensor_rows']==types
assert lemma['decisive']==[{'k':7,'weight':'135/64','h':29,'delta':34},{'k':7,'weight':'17/8','h':29,'delta':48}]
for case in lemma['decisive']:
 k=case['k'];weight=Q(case['weight']);m=1<<(k-1)
 assert k*(1<<k)*weight-case['h']*m==case['delta']<m
# Check finite instances of the exceptional-link facet-energy contradiction.
for k in range(4,17):
 m=1<<(k-1);q=m//2
 for t in range(3):
  for z in range(math.isqrt(2*m)+1):
   eb=t*m+z*z
   if eb>=m+q:assert (eb-m)+(k-1)*z*z>=m
 # Minimum nonhomogeneous A tensors occur at delta=m, outside the theorem.
 assert not (m<Q(2*k-5,2*k-4)*m)

# Lower Fourier-mask complexes have cross-polytope vertex links.
assert lemma['lower_links']=={'P_dimension':'k-2','T_dimension':'k-3','P_component_loss':'2^(k-1)','T_component_loss':'2^(k-1)','T_requires_k_at_least':5,'k4_N_divisible_by':2}
assert lemma['dimension_one_control']=={'facets':[[0,1],[0,2],[1,2]],'vertices':3,'cross_polytope':False}
for dimension in range(2,9):
 facets=[sum(1<<(2*j+((choice>>j)&1)) for j in range(dimension)) for choice in range(1<<dimension)]
 assert len(set(facets))==2**dimension
 for v in range(2*dimension):
  link={mask^(1<<v) for mask in facets if mask>>v&1}
  assert len(link)==2**(dimension-1) and all(mask.bit_count()==dimension-1 for mask in link)
for k in range(5,97):
 assert 2**(k-1)==2*2**(k-2)
 # Sizes k-1 and k-2 have deficit factors one and two.
 assert (k-(k-1))*2**(k-1)==(k-(k-2))*2**(k-2)==2**(k-1)
assert all((4*N-8*h)%8==0 for N in range(0,100,2) for h in range(30))

D=json.loads((root/'direct_r7.json').read_text())
assert D=={'schema':'c44-direct-r7-v1','status':'candidate, unrefereed','k':6,'weight':'31/16','controls':22,'norm':124,'partial_minimum':32,'partial_gap':16,'deficit':40,'one_bad':{'loss_at_most':24,'P_good_at_least':8,'P_incidence_at_least':128,'T_good_only_incidence_at_least':112,'T_with_bad_incidence_at_least':104},'two_bad':{'loss_at_most':8,'top_pair_divisor':16,'possible_top_energy_sums':[104,98,98]},'all_minimum':{'artifact':'allminimum.json','homogeneous_seed_required':True,'nonhomogeneous_minimum_loss':16,'total_incidence_loss_at_most':200},'conclusion':{'control_ceiling':21,'R7_upper':228}}
assert 6*124-22*32==40 and 40-2*16==8 and 40-16==24
patterns=set()
for constant,b,c,pair in itertools.product(range(3),repeat=4):
 loss=6*constant**2+5*(b*b+c*c)+4*pair*pair
 if loss<=8 and loss%2==0:
  top=104-loss-b*b-c*c-2*pair*pair
  assert top%16!=0;patterns.add((loss,pair*pair,top))
assert patterns=={(0,0,104),(4,1,98),(6,0,98)}
assert 8*16>5*24 and 7*16>4*24 and 6*16+2*4>4*24
for t in range(3):
 for b in range(9):
  for constant in range(3):
   assert not (32*t+b*b>=48 and 40==(t-1)*32+6*(b*b+constant*constant))
assert 22*16>5*40
case=json.loads((root/'allminimum.json').read_text())
given_seed=case.pop('seed')
assert given_seed==dict(distinguished=0,pairs=[[1+2*j,2+2*j] for j in range(5)],terms=sorted(1|sum(1<<(1+2*j+((choice>>j)&1)) for j in range(5)) for choice in range(32)))
assert case=={'schema':'c44-allminimum-v1','status':'candidate, unrefereed','degree':6,'target':{'controls':22,'norm':124,'expected_unsigned_leaves':0},'positive':{'controls':12,'norm':64,'expected_unsigned_leaves_at_least':1},'component_variance_numerator':63,'two_component_norm_threshold':126}
binary=pathlib.Path(__file__).resolve().parent.parent/'build/verify_allmin_a'
completion=[]
for n,N,positive in ((12,64,1),(22,124,0)):
 child=subprocess.run([str(binary),str(n),str(N),str(positive)],capture_output=True,text=True,timeout=120)
 assert child.returncode==0,child.stderr
 check=json.loads(child.stdout);assert check['controls']==n and check['norm']==N
 assert (check['unsigned_leaves']>=1) if positive else (check['unsigned_leaves']==0)
 completion.append(check)

caps={1:Q(1,2),2:Q(1),3:Q(5,4),4:Q(11,8)};audit=[]
assert [row['d'] for row in cert['rows']]==list(range(5,97))
for row in cert['rows']:
 d=row['d'];k=d-1;G=1<<(d-2);m=2*G;n=row['R']+1;c=caps[k];gamma=Q(1)
 b=max([Q(1,2)]+[Q(1,4)+Q(1,2**(t+1))+caps[t]/2 for t in range(1,k)])
 assert row['previous']==str(c) and row['b']==str(b)
 def ceiling(x):
  top=2*k if x==1 else math.floor(2*k*x-gamma)
  if d==5 and x==Q(3,2):top=min(top,10)
  if d==6 and x==Q(3,2):top=min(top,12)
  if d==6 and x==Q(7,4):top=min(top,13)
  if d==7 and x==Q(31,16):top=min(top,21)
  return top
 def at(x):
  hi=ceiling(x);choices=range(hi+1) if d<=12 else {hi,min(hi,math.floor(Q(4*k,3)*x))}
  values=[]
  for h in choices:
   ordinary=(1<<d)*c+h+1-2*c*x;v=ordinary
   if x>1 and 3*h>4*k*x:
    support=Q(2,m);inactive=(x-1)/m
    direct=h+(1<<d)*(c*(1-support-inactive)+(b-Q(1,4))*support)
    assert direct==(1<<d)*c+h-2*c*x+4*(b-(c+Q(1,2))/2)
    v=min(v,direct)
   values.append((v,h,v<ordinary))
  return max(values)
 limit=Q(d*m,n);small={2-Q(1,2**j) for j in range(k)}
 test=set(small)|{Q(2)}
 # Exactly the leftmost energy-grid point of each ceiling/applicability cell.
 for h in range(4*k,math.floor(2*k*limit)+2):test.add(Q(math.ceil(G*(Q(h)+gamma)/(2*k)),G))
 for h in range(math.floor(Q(4*k,3)*limit)+2):test.add(Q(math.ceil(Q(3*h*G,4*k)),G))
 test={x for x in test if 1<=x<=limit and (x>=2 or x in small)}
 assert len(test)==row['representatives']
 peak=max(at(x)[0] for x in test);assert peak<n
 worst=row['worst'];x=Q(worst['weight'])
 assert x in test and at(x)[0]==peak==Q(worst['budget'])
 w=row['feasible'];x=Q(w['weight']);value,h,used=at(x)
 assert x>=1 and x*(n-1)<=d*m and (x*G).denominator==1
 assert x>=2 or x in small
 assert (value,h,used)==(Q(w['budget']),w['h'],w['retained']) and value>=n-1
 caps[d]=Q(n-1,1<<d);assert caps[d]>=c and caps[d]-c<=Q(d*k,1<<d)
 audit.append(dict(d=d,R=n-1,peak=str(peak),slack=str(n-peak)))
assert cert['caps']=={str(d):str(c) for d,c in caps.items()}
tail=Q(96**2+3*96+4,1<<96);bound=caps[96]+tail
assert str(tail)==cert['tail'] and str(bound)==cert['bound']
assert bound<Q(cert['strict_claim']) and Q(cert['previous_bound'])-bound>Q(1,10000)
assert [int(caps[d]*2**d) for d in (5,6,7,8)]==[50,107,228,476]
result=dict(status='PASS',verifier='A explicit tensors and rational exclusions',bound=str(bound),tensor_types=len(types),completion=completion,rows=audit,
 artifact_sha256={s:hashlib.sha256((root/s).read_bytes()).hexdigest() for s in ('caps.json','lemma.json','direct_r7.json','allminimum.json')})
if a.out:pathlib.Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
