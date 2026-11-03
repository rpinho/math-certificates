"""Separately written (same agent) structured replay from the same frozen full matrix as checker 1."""
import json,gzip,pathlib,subprocess,sys,hashlib
from fractions import Fraction
file=pathlib.Path(sys.argv[1]);raw=file.read_bytes();z=json.loads(gzip.decompress(raw) if file.suffix=='.gz' else raw)
assert z['schema']=='rational-step-graphon-v1';R=z['red_probability_numerators'];weights=z['block_weights'];n=len(weights);D=z['edge_probability_denominator'];assert type(D) is int and 1<=D<=10**9 and 2<=n<=1024 and n&(n-1)==0;assert all(type(w) is int and w==1 for w in weights);assert len(R)==n and all(len(row)==n for row in R);q=R[0];assert all(type(x) is int and 0<=x<=D for row in R for x in row);assert all(R[a][b]==q[a^b] for a in range(n) for b in range(n)),'matrix is not this binary Cayley kernel'
s=f'{n} {D}\n'+' '.join(map(str,q))+'\n';result=subprocess.run([str(pathlib.Path(__file__).resolve().parent.parent/'check_cayley_exact_r4')],input=s,text=True,capture_output=True,check=True);a,b,red,blue=map(int,result.stdout.split());density=Fraction(a,b);assert density==Fraction(red+blue,D**10*n**4)
if len(sys.argv)>2:assert density<Fraction(sys.argv[2]),'claimed upper threshold fails exact comparison'
print(json.dumps(dict(PASS=True,status='candidate and unrefereed',sha256=hashlib.sha256(raw).hexdigest(),parts=n,density=str(density),root_red_integer=str(red),root_blue_integer=str(blue)),indent=2))
