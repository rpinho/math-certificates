"""Search certificate generator. Acceptance requires both independent checkers."""
from fractions import Fraction as F
import hashlib,json,pathlib
R=pathlib.Path(__file__).resolve().parent
H=96

def options(d,n,mode):
 k=d-1;M=1<<k;t=F(d*M,n)
 xs=[2-F(1,1<<j) for j in range(k)]
 for h in range(4*k,int(2*k*t)+1):
  z=(h*M+4*k-1)//(4*k)
  # Strict equality exclusions can demote the first point in the cell.
  for e in (z,z+1):
   x=F(2*e,M)
   if int(2*k*x)==h:xs.append(x)
 return sorted(set(x for x in xs if 1<=x<=t))

def hcap(d,x,mode):
 v=2*(d-1)*x;h=int(v)
 if mode in ('refined','quartic','quintic','classified') and d>=4 and x.denominator>1 and v.denominator==1:h-=1
 if mode=='second_equality' and d>=4 and x==F(3,2):h-=1
 if mode in ('quartic','quintic','classified') and d==5 and x==F(3,2):h=min(h,10)
 if mode=='quintic' and d==6 and x==F(3,2):h=min(h,13)
 if mode=='classified' and d==6 and x==F(3,2):h=min(h,12)
 return h

def budget(d,c,x,mode):return (1<<d)*c+hcap(d,x,mode)-(2*c-1)*x

def make(mode):
 caps={1:F(1,2),2:F(1),3:F(5,4),4:F(11,8)};rows=[]
 for d in range(5,H+1):
  c=caps[d-1]
  def feasible(n):return any(budget(d,c,x,mode)>=n for x in options(d,n,mode))
  lower=3*(1<<(d-1))-2
  values=[(min(int(budget(d,c,x,mode)),int(F(d*(1<<(d-1)),1)/x)),x) for x in options(d,lower,mode)]
  low=max(values)[0];high=low+1
  assert feasible(low) and not feasible(high)
  cases=options(d,high,mode)
  worst=max(cases,key=lambda x:budget(d,c,x,mode))
  witness=next(x for x in options(d,low,mode) if budget(d,c,x,mode)>=low)
  rows.append({'d':d,'R':low,'previous':str(c),'first_excluded':high,'case_count':len(cases),
   'worst':{'lambda':str(worst),'h':hcap(d,worst,mode),'budget':str(budget(d,c,worst,mode))},
   'witness':{'lambda':str(witness),'h':hcap(d,witness,mode),'budget':str(budget(d,c,witness,mode))}})
  caps[d]=F(low,1<<d)
 tail=F(H*H+3*H+4,1<<H);bound=caps[H]+tail
 return {'caps':{str(d):str(c) for d,c in caps.items()},'rows':rows,'tail':str(tail),'bound':str(bound)}
packet={'schema':'c44-round7-v1','status':'candidate, unrefereed','horizon':H,
 'base_counts':{'1':1,'2':4,'3':10,'4':22},'gap1_R5_upper':53,
 'premises':{'quartic':'inputs/gap1/PROOF.md','round6':'inputs/round6/PROOF.md',
 'minimum_support':'Valyuzhenich 2303.10995 Theorem 2(2)',
 'complex':'Masuda-Panov math/0607094 Lemma 4.7'},
 'claims':{'combined':'2.1720558669','second_equality':'2.1330712908','refined':'2.1255305914','quartic':'2.0963373341','quintic':'2.0886707842','classified':'2.0808959614'},
 'modes':{m:make(m) for m in ['combined','second_equality','refined','quartic','quintic','classified']}}
(R/'certificate.json').write_text(json.dumps(packet,indent=2)+'\n')
for m,v in packet['modes'].items():print(m,v['bound'],float(F(v['bound'])),[(r['d'],r['R']) for r in v['rows'][:8]],flush=True)
