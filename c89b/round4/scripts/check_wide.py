"""Frozen rational graphon verifier: no imports from numerical search."""
import pathlib,gzip,json,sys,subprocess,hashlib
from fractions import Fraction
p=pathlib.Path(sys.argv[1]);raw=p.read_bytes();z=json.loads(gzip.decompress(raw) if p.suffix=='.gz' else raw)
assert z['schema']=='rational-step-graphon-v1';D=z['edge_probability_denominator'];R=z['red_probability_numerators'];w=z['block_weights'];n=len(w)
assert type(D) is int and 0<D<=10**12 and 0<n<=1024
assert D<=4096 and all(a==1 for a in w)
assert len(R)==n and all(len(r)==n for r in R)
assert all(type(a) is int and 0<=a<=D for r in R for a in r)
assert all(type(a) is int and 0<a<=10**12 for a in w)
assert all(R[i][j]==R[j][i] for i in range(n) for j in range(n))
s=f'{n} {D}\n'+' '.join(map(str,w))+'\n'+'\n'.join(' '.join(map(str,r)) for r in R)+'\n'
bin=pathlib.Path(__file__).resolve().parent.parent/'check_wide'
r=subprocess.run([str(bin)],input=s,text=True,capture_output=True,check=True).stdout.splitlines();assert len(r)==4
a,b,red,blue=map(int,r);assert a>=0 and b>0;value=Fraction(a,b);assert value==Fraction(red+blue,D**10*sum(w)**5)
if len(sys.argv)>2:assert value<Fraction(sys.argv[2]),'claimed upper threshold fails exact comparison'
print(json.dumps(dict(PASS=True,status='candidate and unrefereed',sha256=hashlib.sha256(raw).hexdigest(),parts=n,density=str(value),red_integer=str(red),blue_integer=str(blue)),indent=2))
