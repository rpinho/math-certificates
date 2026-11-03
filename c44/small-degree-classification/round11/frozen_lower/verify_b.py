"""Exact lower controls B: unordered autocorrelations and cofactor identities."""
import itertools,json,math,pathlib,sys
from fractions import Fraction
directory=pathlib.Path(sys.argv[1]);data=json.loads((directory/'artifact.json').read_text())
assert data['schema']=='c44-round11-lower-controls-v1' and data['status']=='candidate, unrefereed'
assert data['universal_lower']=='3/2' and not data['improved']
def add(a,b,scale=1):
 result=dict(a)
 for mask,c in b.items():result[mask]=result.get(mask,0)+scale*c
 return {s:c for s,c in result.items() if c}
def autocorrelation(polynomial):
 terms=sorted(polynomial.items());result={0:sum(c*c for s,c in terms)}
 for (left,a),(right,b) in itertools.combinations(terms,2):
  key=left^right;result[key]=result.get(key,0)+2*a*b
 return {s:c for s,c in result.items() if c}
def product(a,b):
 # Polarization in a separately written (same agent) checker; no A imports.
 both=autocorrelation(add(a,b));square_a=autocorrelation(a);square_b=autocorrelation(b)
 result=add(add(both,square_a,-1),square_b,-1)
 assert all(c%2==0 for c in result.values())
 return {s:c//2 for s,c in result.items()}
def read(row):
 terms=[(int(s),int(c)) for s,c in row['terms']]
 assert len({s for s,c in terms})==len(terms) and all(c!=0 for s,c in terms)
 p=dict(terms);relevant=set()
 for s,c in terms:
  assert s>=0
  relevant.update(i for i in range(s.bit_length()) if s>>i&1)
 assert relevant==set(range(row['count'])) and max(s.bit_count() for s,c in terms)==row['degree']
 assert autocorrelation(p)=={0:row['denominator']**2}
 assert Fraction(row['lift'])==Fraction(row['count']+2,2**row['degree'])
 return p,row['denominator'],row['count'],row['degree']
assert set(data['seeds'])=={'xi5','xi6','cofactor_split5'}
for name,row in data['seeds'].items():
 read(row);assert Fraction(row['lift'])==Fraction(3,2)
p,D,n,d=read(data['chain']['initial']);assert n==23 and d==5
assert len(data['chain']['steps'])==23
for record in data['chain']['steps']:
 assert record['before_count']==n and record['after_count']==n+1
 labels=record['image'];phase=record['flips'];chosen=record['coordinate']
 assert len(labels)==n and len(set(labels))==n and set(labels)==set(range(n)) and labels[chosen]==chosen
 assert 0<=phase<2**n and not(phase&2**chosen)
 q={s-2**chosen:c for s,c in p.items() if s&2**chosen};r={s:c for s,c in p.items() if not s&2**chosen}
 q2=autocorrelation(q);r2=autocorrelation(r)
 assert add(q2,r2)=={0:D*D} and product(q,r)=={}
 transformed={}
 for mask,value in q.items():
  positions=[j for j in range(n) if mask&2**j]
  newmask=sum(2**labels[j] for j in positions)
  transformed[newmask]=value*(-1 if sum(bool(phase&2**j) for j in positions)%2 else 1)
 assert transformed not in (q,{s:-c for s,c in q.items()}) and autocorrelation(transformed)==q2
 even=add(q,transformed);odd=add(q,transformed,-1)
 assembled={s:2*c for s,c in r.items()}
 assembled=add(assembled,{s+2**chosen:c for s,c in even.items()})
 assembled=add(assembled,{s+2**n:c for s,c in odd.items()})
 D*=2;divisor=math.gcd(D,*assembled.values());p={s:c//divisor for s,c in assembled.items()};D//=divisor;n+=1
 assert autocorrelation(p)=={0:D*D} and max(s.bit_count() for s in p)==5
assert (p,D,n,d)==read(data['seeds'][data['chain']['final']]) and n==46
assert [(data['seeds'][x]['count'],data['seeds'][x]['degree']) for x in ('xi5','xi6','cofactor_split5')]==[(46,5),(94,6),(46,5)]
result=dict(status='PASS',verifier='B unordered correlations and cofactor identities',seeds=3,verified_splittings=23,lower='3/2',improved=False)
if len(sys.argv)>2:pathlib.Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
