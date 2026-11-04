"""Reproduce only the public baseline's exact renewal arithmetic, not its checker."""
import json
import pathlib
import sys
from fractions import Fraction as Q
sys.set_int_max_str_digits(500000)
ROOT=pathlib.Path(__file__).resolve().parent
d=json.loads((ROOT.parent/'c38/sources/numaro/bridge_table_record_L17.json').read_text())
N=d['N'];L=d['L'];B=[[int(d['b_nl'][n][h]) for n in range(N+1)] for h in range(L+1)]
A=[[0]*(N+1) for _ in range(L+1)]
for h in range(1,L+1):
    for n in range(1,N+1):
        A[h][n]=B[h][n]-sum(A[j][m]*B[h-j][n-m] for j in range(1,h) for m in range(1,n))
        assert A[h][n]>=0
coeff=[sum(A[h][n] for h in range(1,L+1)) for n in range(N+1)]
p=1<<128;q=129513673858566230428673965530967449326
# Homogeneous Horner evaluation, denominator p^N; exact integers only.
value=0
for n in range(N,-1,-1):value=value*q+coeff[n]*p**(N-n)
denom=p**N
assert value>=denom
out={'status':'BASELINE_RENEWAL_ARITHMETIC_PASS','L':L,'N':N,
     'mu':str(Q(p,q)),'excess':str(Q(value-denom,denom)),
     'excess_diagnostic':float(Q(value-denom,denom)),
     'scope':'Original large enumeration is an attributed premise; no public checker was executed.'}
(ROOT/'results'/'BASELINE_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'],out['excess_diagnostic'])
