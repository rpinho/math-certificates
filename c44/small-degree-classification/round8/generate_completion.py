"""Build a candidate certificate from exploratory caps; no acceptance role."""
from fractions import Fraction as F
import json,pathlib,sys,functools
R=pathlib.Path(__file__).resolve().parent
E=json.loads((R/'completion_scalar_simple_explore.json').read_text());H=96
C={int(d):F(c) for d,c in E['caps'].items()}
def points(d,n):
 m=1<<(d-1);k=d-1;t=F(d*m,n)
 xs={2-F(1,1<<j) for j in range(k)}
 for a in range(4*k,int(2*k*t)+1):
  z=(a*m+4*k-1)//(4*k)
  for e in (z,z+1):
   x=F(2*e,m)
   if x>=2:xs.add(x)
 for a in range(0,int(F(4*k,3)*t)+2):
  z=(3*a*m+8*k-1)//(8*k)
  for e in (z,z+1):
   x=F(2*e,m)
   if x>=2:xs.add(x)
 return sorted(x for x in xs if 1<=x<=t)
def hlimit(d,x,mode):
 t=2*(d-1)*x;h=int(t)
 if x.denominator!=1 and t.denominator==1:h-=1
 if mode=='sharp' and d==5 and x==F(3,2):h=min(h,10)
 if mode=='sharp' and d==6 and x==F(3,2):h=min(h,12)
 return h
@functools.lru_cache(None)
def envelope(d):return max([F(1,2)]+[F(1,4)+F(1,1<<(t+1))+C[t]/2 for t in range(1,d-1)])
def value(d,x,mode):
 c=C[d-1];b=envelope(d);hi=hlimit(d,x,mode);lo=min(hi,int(F(4*(d-1),3)*x));v=[]
 for h in {lo,hi}:
  old=(1<<d)*c+h+1-2*c*x
  good=x>1 and 3*h>4*(d-1)*x
  new=old-1+4*(b-(c+F(1,2))/2) if good else old
  use=new<old
  v.append((min(old,new),h,use))
 return max(v)
packet={'schema':'c44-round8-completion-v1','status':'candidate, unrefereed','horizon':H,
 'base_counts':{'1':1,'2':4,'3':10,'4':22},'previous_bound':'164865563398608188023949601889/79228162514264337593543950336',
 'strict_claim':'2.0417086280','improvement_bar':'1/1000','modes':{}}
for mode in ('simple','sharp'):
 rows=[]
 for d in range(5,H+1):
  n=int(C[d]*(1<<d));ps=points(d,n+1)
  x=max(ps,key=lambda x:value(d,x,mode)[0]);v,h,u=value(d,x,mode)
  assert v<n+1
  ws=[(value(d,y,mode),y) for y in points(d,n) if value(d,y,mode)[0]>=n]
  assert ws
  (vb,hb,ub),y=min(ws,key=lambda a:(a[1],a[0][1]))
  row={'d':d,'R':n,'previous':str(C[d-1]),'b':str(envelope(d)),
    'first_excluded':n+1,'representatives':len(ps),
    'worst':{'lambda':str(x),'h':h,'retained':u,'budget':str(v)},
    'feasible':{'lambda':str(y),'h':hb,'retained':ub,'budget':str(vb)}}
  rows.append(row)
  if d<=8:print(mode,row,flush=True)
 tail=F(H*H+3*H+4,1<<H);bound=C[H]+tail
 packet['modes'][mode]={'caps':{str(d):str(c) for d,c in C.items()},'rows':rows,'tail':str(tail),'bound':str(bound)}
packet['strict_claim']=str(F(1,int(1))) if False else '2.0417086280'
assert F(packet['modes']['simple']['bound'])<F(packet['strict_claim'])
assert F(packet['previous_bound'])-F(packet['modes']['simple']['bound'])>F(1,1000)
(R/'completion_certificate.json').write_text(json.dumps(packet,indent=2)+'\n')
print('BOUND',bound,float(bound),flush=True)
