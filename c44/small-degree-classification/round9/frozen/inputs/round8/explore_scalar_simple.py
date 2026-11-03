from fractions import Fraction as F
import json,pathlib,itertools
R=pathlib.Path(__file__).resolve().parent
base=json.loads((R/'inputs/round7/certificate.json').read_text())
H=96
caps={1:F(1,2),2:F(1),3:F(5,4),4:F(11,8)}
rows=[]
def hcap(d,x):
 z=2*(d-1)*x;h=int(z)
 if d>=4 and x.denominator>1 and z.denominator==1:h-=1
 return h
def options(d,lower):
 k=d-1;M=1<<k;top=F(d*M,lower)
 xs=[2-F(1,1<<j) for j in range(k)]
 # Complete scalar cells include both old h ceilings and the good-partial
 # threshold h>4k lambda/3. Exact additional boundaries are inserted.
 for a in range(4*k,int(2*k*top)+1):
  z=(a*M+4*k-1)//(4*k)
  for v in (z,z+1):
   x=F(2*v,M)
   if int(2*k*x)==a:xs.append(x)
 for h in range(0,int(2*k*top)+1):
  # At lambda=3h/(4k), good partial is no longer guaranteed for h.
  v=(3*h*M+8*k-1)//(8*k)
  for j in (-1,0,1):xs.append(F(2*(v+j),M))
 allowed={2-F(1,1<<j) for j in range(k)}
 return sorted(set(x for x in xs if 1<=x<=top and (x>=2 or x in allowed)))
def best(d,x):
 c=caps[d-1];b=max([F(1,2)]+[F(1,4)+F(1,1<<(t+1))+caps[t]/2 for t in range(1,d-1)])
 hi=hcap(d,x);h0=min(hi,int(F(4*(d-1),3)*x));vals=[]
 for h in {h0,hi}:
  v=(1<<d)*c+h+1-2*c*x;used=False
  if x>1 and 3*h>4*(d-1)*x:
   w=v-1+4*(b-(c+F(1,2))/2)
   if w<v:v=w;used=True
  vals.append((v,h,used))
 return max(vals)
for d in range(5,H+1):
 xs=options(d,3*(1<<(d-1))-2)
 vals=[]
 for x in xs:
  v,h,u=best(d,x);n=min(int(v),int(F(d*(1<<(d-1)),1)/x))
  vals.append((n,x,h,u,v))
 n,x,h,u,v=max(vals);caps[d]=F(n,1<<d)
 rows.append({'d':d,'R':n,'previous':str(caps[d-1]),'lambda':str(x),'h':h,'completion':u,'budget':str(v)})
 print(rows[-1],flush=True)
bound=caps[H]+F(H*H+3*H+4,1<<H)
p={'status':'EXPLORATORY','horizon':H,'rows':rows,'caps':{str(d):str(v) for d,v in caps.items()},'bound':str(bound),'bound_decimal':float(bound)}
(R/'completion_scalar_simple_explore.json').write_text(json.dumps(p,indent=2)+'\n')
print('BOUND',bound,float(bound),flush=True)
