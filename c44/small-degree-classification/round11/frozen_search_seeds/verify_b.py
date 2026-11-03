"""Separately written (same agent) stored-seed B: unordered coefficient autocorrelations."""
import itertools,json,pathlib,sys
from fractions import Fraction
root=pathlib.Path(sys.argv[1]);packet=json.loads((root/'artifact.json').read_text())
assert packet['schema']=='c44-search-seeds-v1' and packet['status']=='candidate, unrefereed'
assert not packet['source_errors'] and len(packet['seeds'])==8
rows=[]
for name,entry in sorted(packet['seeds'].items()):
 assert entry['schema']=='c44-sparse-seed-v1' and entry['status']=='UNVERIFIED proposal'
 terms=sorted((int(s),int(c)) for s,c in entry['terms']);D=entry['denominator']
 assert len({s for s,c in terms})==len(terms) and D>0 and all(c!=0 and s>=0 for s,c in terms)
 correlation={0:sum(c*c for s,c in terms)}
 for (s,a),(t,b) in itertools.combinations(terms,2):
  key=s^t;correlation[key]=correlation.get(key,0)+2*a*b
 assert correlation[0]==D*D and all(c==0 for s,c in correlation.items() if s)
 variables=set(j for s,c in terms for j in range(s.bit_length()) if s>>j&1)
 degree=max(s.bit_count() for s,c in terms);number=len(variables)
 assert variables==set(range(number)) and number==entry['count'] and degree==entry['degree']
 lift=Fraction(number+2,2**degree);assert lift==Fraction(entry['asymptotic_lift'])
 homogeneous=sum(c*c for s,c in terms if s.bit_count()==degree)==D*D
 rows.append(dict(name=name,count=number,degree=degree,lift=str(lift),homogeneous=homogeneous))
assert max([Fraction(3,2)]+[Fraction(r['lift']) for r in rows])==Fraction(packet['lower_claim'])==Fraction(3,2)
result=dict(status='PASS',verifier='B unordered Fourier autocorrelations',rows=rows,lower=packet['lower_claim'])
if len(sys.argv)>2:pathlib.Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
