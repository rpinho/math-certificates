"""Exact lower controls A: ordered XOR products, full squares at every step."""
import collections,json,math,pathlib,sys
from fractions import Fraction as Q
root=pathlib.Path(sys.argv[1]);P=json.loads((root/'artifact.json').read_text())
assert P['schema']=='c44-round11-lower-controls-v1' and P['status']=='candidate, unrefereed'
assert P['universal_lower']=='3/2' and P['improved'] is False
def times(a,b):
 out=collections.defaultdict(int)
 for s,c in a.items():
  for t,d in b.items():out[s^t]+=c*d
 return {s:c for s,c in out.items() if c}
def decode(row):
 p={int(s):c for s,c in row['terms']};D=row['denominator'];n=row['count'];d=row['degree']
 assert len(p)==len(row['terms']) and all(c and 0<=s<1<<n for s,c in p.items()) and D>0
 assert max(s.bit_count() for s in p)==d
 used=0
 for s in p:used|=s
 assert used==(1<<n)-1 and times(p,p)=={0:D*D}
 assert Q(row['lift'])==Q(n+2,1<<d)
 return n,p,D,d
for name,row in P['seeds'].items():decode(row)
assert set(P['seeds'])=={'xi5','xi6','cofactor_split5'}
assert [(P['seeds'][name]['count'],P['seeds'][name]['degree']) for name in ('xi5','xi6','cofactor_split5')]==[(46,5),(94,6),(46,5)]
chain=P['chain'];n,p,D,d=decode(chain['initial']);assert (n,d)==(23,5) and len(chain['steps'])==23
for step in chain['steps']:
 b=step['coordinate'];image=step['image'];flips=step['flips']
 assert step['before_count']==n and step['after_count']==n+1 and sorted(image)==list(range(n))
 assert image[b]==b and 0<=flips<1<<n and not(flips>>b&1)
 U={s^(1<<b):c for s,c in p.items() if s>>b&1};V={s:c for s,c in p.items() if not s>>b&1};companion={}
 for s,c in U.items():
  mapped=0
  for j in range(n):
   if s>>j&1:mapped|=1<<image[j]
  companion[mapped]=-c if (s&flips).bit_count()%2 else c
 assert companion!=U and companion!={s:-c for s,c in U.items()}
 assert times(companion,companion)==times(U,U)
 new=collections.defaultdict(int)
 for s,c in V.items():new[s]+=2*c
 for s,c in U.items():new[s|(1<<b)]+=c;new[s|(1<<n)]+=c
 for s,c in companion.items():new[s|(1<<b)]+=c;new[s|(1<<n)]-=c
 new={s:c for s,c in new.items() if c};D*=2;g=math.gcd(D,math.gcd(*new.values()));D//=g;p={s:c//g for s,c in new.items()};n+=1
 assert max(s.bit_count() for s in p)==d and times(p,p)=={0:D*D}
 used=0
 for s in p:used|=s
 assert used==(1<<n)-1
final=P['seeds'][chain['final']];assert (n,p,D,d)==decode(final) and n==46
result=dict(status='PASS',verifier='A ordered products and full Boolean squares',seeds=3,verified_splittings=23,counts=[46,94,46],lower='3/2',improved=False)
if len(sys.argv)>2:pathlib.Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
