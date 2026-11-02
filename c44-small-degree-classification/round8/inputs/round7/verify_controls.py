"""Exact sparse polynomial controls for claims and barriers; no search imports."""
from fractions import Fraction as Q
from collections import defaultdict
import pathlib,json,sys
R=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else __file__).resolve()
if R.is_file():R=R.parent

def mul(a,b):
 out=defaultdict(Q)
 for s,x in a.items():
  for t,y in b.items():out[s^t]+=x*y
 return {s:x for s,x in out.items() if x}
def add(a,b):
 out=defaultdict(Q,a)
 for s,x in b.items():out[s]+=x
 return {s:x for s,x in out.items() if x}
def times(a,x):return {s:c*x for s,c in a.items() if c*x}
def shift(a,k):return {s<<k:c for s,c in a.items()}
def support(a):
 mask=0
 for s in a:mask|=s
 return mask.bit_count()
def degree(a):return max(s.bit_count() for s in a)

a={1:Q(1)};count=1;witnesses=[]
for d in range(1,7):
 if d>1:
  n=count;left=a;right=shift(a,n)
  s={1<<(2*n):Q(1)};t={1<<(2*n+1):Q(1)}
  a=add(times(mul(add(s,t),left),Q(1,2)),times(mul(add(s,times(t,-1)),right),Q(1,2)))
  count=2*n+2
 assert mul(a,a)=={0:Q(1)}
 assert degree(a)==d and all(s.bit_count()==d for s in a)
 assert support(a)==count==3*(1<<(d-1))-2
 witnesses.append({'degree':d,'variables':count,'terms':len(a),'denominator':max(c.denominator for c in a.values())})
# A six-cycle ternary quadratic. Coordinates a,b,c,d,e,f are 0..5.
cycle={ (1<<u)|(1<<v):Q(sign,4) for u,v,sign in [(1,2,1),(0,3,1),(1,3,-1),(4,2,-1),(0,5,-1),(4,5,1)]}
assert mul(mul(cycle,cycle),cycle)==cycle
barriers=[]
for k in [2,3,4,5]:
 a=cycle
 for j in range(k-2):a=mul(a,{1<<(6+2*j):Q(1,2),1<<(7+2*j):Q(1,2)})
 assert mul(mul(a,a),a)==a
 p=sum(c*c for c in a.values());h=support(a)
 assert degree(a)==k and p*(1<<k)==Q(3,2) and h==2*k+2
 energies=[]
 for j in range(h):
  e=sum(c*c for s,c in a.items() if s>>j&1)
  assert e>=Q(1,1<<(k+1))
  energies.append(str(e))
 barriers.append({'degree':k,'controls':h,'support_energy':str(p),'lambda':'3/2','terms':len(a),'partial_energies':energies})
# Sharp control-count witnesses do not imply Boolean functions with the
# scalar count ceilings; they show only that reducing h alone cannot work.
out={'status':'PASS','Boolean_lower_witnesses':witnesses,'ternary_control_barriers':barriers,'known_lower_C44':'3/2','R5_lower':46,'R6_lower':94}
outdir=R.parent/'receipts' if R.name=='frozen' else R/'receipts';outdir.mkdir(exist_ok=True)
(outdir/'controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
