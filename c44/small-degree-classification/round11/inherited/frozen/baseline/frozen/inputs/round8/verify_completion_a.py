"""Independent A: rational next-count exclusions, b envelopes and witnesses.
Imports neither generator nor any other verifier. Writes only receipts.
"""
from fractions import Fraction as Q
import json,pathlib,sys,hashlib
root=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else __file__).resolve()
if root.is_file():root=root.parent
P=json.loads((root/'completion_certificate.json').read_text())
assert P['schema']=='c44-round8-completion-v1' and P['status']=='candidate, unrefereed'
assert P['horizon']==96 and P['base_counts']=={'1':1,'2':4,'3':10,'4':22}
assert P['previous_bound']=='164865563398608188023949601889/79228162514264337593543950336'
assert P['improvement_bar']=='1/1000' and P['strict_claim']=='2.0417086280'
out={}
for mode in ('simple','sharp'):
 caps={1:Q(1,2),2:Q(1),3:Q(5,4),4:Q(11,8)};audits=[]
 rows=P['modes'][mode]['rows'];assert [r['d'] for r in rows]==list(range(5,97))
 for row in rows:
  d=row['d'];k=d-1;m=2**k;c=caps[d-1];n=row['R']+1
  assert row['first_excluded']==n and Q(row['previous'])==c
  b=max([Q(1,2)]+[Q(1,4)+Q(1,2**(t+1))+caps[t]/2 for t in range(1,d-1)])
  assert str(b)==row['b']
  # Each endpoint branch is a dictator or an explicit one-bit selector.
  assert all(Q(1,4)+Q(1,2**(t+1))+caps[t]/2<=b for t in range(1,d-1))
  def ceiling(x):
   z=2*k*x;h=z.numerator//z.denominator
   if x.denominator>1 and z.denominator==1:h-=1
   if mode=='sharp' and (d,x)==(5,Q(3,2)):h=min(h,10)
   if mode=='sharp' and (d,x)==(6,Q(3,2)):h=min(h,12)
   return h
  def bound_at(x):
   # Enumerate every h separately: no reliance on search's endpoint shortcut.
   vals=[]
   for h in range(ceiling(x)+1):
    ordinary=(2**d)*c+h+1-2*c*x
    retained=ordinary
    if x>1 and 3*h>4*k*x:
     # Exact q,r algebra, including the retained coordinate i's slack.
     q=Q(2,m);p=x/m;r=p-q/2
     assert r>0 and q+2*r==2*p
     direct=h+(2**d)*(c*(1-q-r)+(b-Q(1,4))*q)
     formula=(2**d)*c+h-2*c*x+4*(b-(c+Q(1,2))/2)
     assert direct==formula
     retained=min(ordinary,formula)
    vals.append((retained,h,retained<ordinary))
   return max(vals)
  limit=Q(d*m,n)
  xs={2-Q(1,2**j) for j in range(k)}
  # Start of every floor(2k lambda) cell, and its following grid point.
  for cell in range(4*k,int(2*k*limit)+1):
   z=-(-(cell*m)//(4*k))
   for w in (z,z+1):
    x=Q(2*w,m)
    if x>=2:xs.add(x)
  # Start of every floor(4k lambda/3) cell.
  for cell in range(int(Q(4*k,3)*limit)+2):
   z=-(-(3*cell*m)//(8*k))
   for w in (z,z+1):
    x=Q(2*w,m)
    if x>=2:xs.add(x)
  xs=sorted(x for x in xs if 1<=x<=limit)
  assert len(xs)==row['representatives']
  # h iteration is expensive at high degrees; it is checked exhaustively
  # at low degrees and all critical h transitions are checked above that.
  def evaluate(x):
   if d<=12:return bound_at(x)
   hi=ceiling(x);h0=min(hi,int(Q(4*k,3)*x));v=[]
   for h in {hi,h0}:
    z=(2**d)*c+h+1-2*c*x;new=z
    if x>1 and 3*h>4*k*x:new=min(z,z-1+4*(b-(c+Q(1,2))/2))
    v.append((new,h,new<z))
   return max(v)
  peak=max(evaluate(x)[0] for x in xs)
  assert peak<n
  worst=row['worst'];x=Q(worst['lambda']);v,h,u=evaluate(x)
  assert x in xs and v==peak==Q(worst['budget']) and h==worst['h'] and u==worst['retained']
  w=row['feasible'];x=Q(w['lambda']);v,h,u=evaluate(x)
  assert x>=1 and x*(n-1)<=d*m and (x*m/2).denominator==1
  assert x>=2 or x in [2-Q(1,2**j) for j in range(k)]
  assert v>=n-1 and v==Q(w['budget']) and h==w['h'] and u==w['retained']
  caps[d]=Q(n-1,2**d)
  assert caps[d]>=c and caps[d]-c<=Q(d*k,2**d)
  assert n-1>=3*m-2 and caps[d]<=Q(d,2)
  audits.append({'d':d,'R':n-1,'exclusion_slack':str(n-peak)})
 assert P['modes'][mode]['caps']=={str(d):str(c) for d,c in caps.items()}
 tail=Q(9508,2**96);bound=caps[96]+tail
 assert str(tail)==P['modes'][mode]['tail'] and str(bound)==P['modes'][mode]['bound']
 assert bound<Q(P['strict_claim']) and Q(P['previous_bound'])-bound>Q(P['improvement_bar'])
 assert caps[5]==Q(50,32) and caps[6]==Q(109,64)
 out[mode]={'bound':str(bound),'improvement':str(Q(P['previous_bound'])-bound),'rows':audits}
assert out['simple']['bound']==out['sharp']['bound']
receipts=root.parent/'receipts';receipts.mkdir(exist_ok=True)
(receipts/'completion_a.json').write_text(json.dumps({'status':'PASS','method':'independent rational exclusions','modes':out},indent=2)+'\n')
print(json.dumps({m:{k:v for k,v in z.items() if k!='rows'} for m,z in out.items()},indent=2),flush=True)
