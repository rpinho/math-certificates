"""Independent rational exclusion checker; no imports from search or checker B."""
from fractions import Fraction as Q
import json,pathlib,sys
R=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else __file__).resolve()
if R.is_file():R=R.parent
C=json.loads((R/'certificate.json').read_text())
assert C['schema']=='c44-round7-v1' and C['horizon']==96 and C['status']=='candidate, unrefereed'
assert C['base_counts']=={'1':1,'2':4,'3':10,'4':22} and C['gap1_R5_upper']==53

def control(degree,x,mode):
 a=2*(degree-1)*x;h=a.numerator//a.denominator
 if mode in ['refined','quartic','quintic','classified'] and x.denominator>1 and a.denominator==1:h-=1
 if mode=='second_equality' and x==Q(3,2):h-=1
 if mode in ['quartic','quintic','classified'] and degree==5 and x==Q(3,2):h=min(h,10)
 if mode=='quintic' and degree==6 and x==Q(3,2):h=min(h,13)
 if mode=='classified' and degree==6 and x==Q(3,2):h=min(h,12)
 return h

out={}
for mode in ['combined','second_equality','refined','quartic','quintic','classified']:
 cap={1:Q(1,2),2:Q(1),3:Q(5,4),4:Q(11,8)};checks=[]
 rows=C['modes'][mode]['rows'];assert [r['d'] for r in rows]==list(range(5,97))
 for row in rows:
  d=row['d'];m=1<<(d-1);k=d-1;c=cap[d-1];n=row['R']+1
  assert row['previous']==str(c) and row['first_excluded']==n
  assert Q(1,2)<=c<=Q(k,2) and n-1>=3*m-2
  limit=Q(d*m,n);xs=[]
  for j in range(k):
   x=2-Q(1,1<<j)
   if x<=limit:xs.append(x)
  for cell in range(4*k,int(2*k*limit)+1):
   z=-(-(cell*m)//(4*k))
   for e in [z,z+1]:
    x=Q(2*e,m)
    if 2<=x<=limit and int(2*k*x)==cell:xs.append(x)
  xs=sorted(set(xs));assert len(xs)==row['case_count']
  def val(x):return (1<<d)*c+control(d,x,mode)+(1-2*c)*x
  values=[val(x) for x in xs];assert all(v<n for v in values)
  peak=max(values);z=Q(row['worst']['lambda'])
  assert z in xs and val(z)==peak==Q(row['worst']['budget']) and row['worst']['h']==control(d,z,mode)
  # An explicit feasible point proves the end of this relaxation only.
  x=Q(row['witness']['lambda']);assert x>=1 and x*(n-1)<=d*m
  assert (x*m/2).denominator==1
  if x<2:assert x in [2-Q(1,1<<j) for j in range(k)]
  assert row['witness']['h']==control(d,x,mode)
  assert Q(row['witness']['budget'])==val(x)>=n-1
  cap[d]=Q(n-1,1<<d)
  assert cap[d]>=c and cap[d]-c<=Q(d*(d-1),1<<d)
  checks.append({'d':d,'R':n-1,'exclusion_slack':str(n-peak)})
 assert C['modes'][mode]['caps']=={str(d):str(v) for d,v in cap.items()}
 tail=Q(96*96+3*96+4,1<<96);bound=cap[96]+tail
 assert str(tail)==C['modes'][mode]['tail'] and str(bound)==C['modes'][mode]['bound']
 assert bound<Q(C['claims'][mode])
 old=Q(174098727923678791596986402933,1<<96)
 assert old-bound>Q(1,1000)
 out[mode]={'bound':str(bound),'gain':str(old-bound),'gap_to_1_5':str(bound-Q(3,2)),'checks':checks}
assert Q(C['modes']['combined']['caps']['5'])==Q(53,32)
assert Q(C['modes']['quartic']['caps']['5'])==Q(51,32)
outdir=R.parent/'receipts' if R.name=='frozen' else R/'receipts';outdir.mkdir(exist_ok=True)
(outdir/'scalar_a.json').write_text(json.dumps({'status':'PASS','implementation':'A: exclusion at first impossible count','modes':out},indent=2)+'\n')
print(json.dumps({m:{k:v for k,v in z.items() if k!='checks'} for m,z in out.items()},indent=2),flush=True)
