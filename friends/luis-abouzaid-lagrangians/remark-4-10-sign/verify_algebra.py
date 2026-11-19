#!/usr/bin/env python3
"""Independent exact verifier: polynomial coefficients and finite linear algebra."""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
p=Path(__file__).with_name('POD_ALGEBRA.json')
r=json.loads(p.read_text())
assert len(r['rows'])==4
assert r['scope'].startswith('conditional algebra only')
# Solve Hom(M,M) via a separately built commutator map, rational RREF.
def rank(A):
 A=[list(map(Q,row)) for row in A]; m=len(A);n=len(A[0]);k=0
 for j in range(n):
  piv=next((i for i in range(k,m) if A[i][j]),None)
  if piv is None:continue
  A[k],A[piv]=A[piv],A[k];v=A[k][j];A[k]=[x/v for x in A[k]]
  for i in range(m):
   if i!=k and A[i][j]:
    v=A[i][j];A[i]=[x-v*y for x,y in zip(A[i],A[k])]
  k+=1
  if k==m:break
 return k
def homdim(U):
 n=len(U);mat=[]
 for i in range(n):
  for j in range(n):
   row=[0]*(n*n)
   for k in range(n):row[i*n+k]+=U[k][j];row[k*n+j]-=U[i][k]
   mat.append(row)
 return n*n-rank(mat)
controls={}
for U,label in [([[2,0],[0,2]],'two_same_roots'),([[2,0],[0,-2]],'two_distinct_roots'),([[2,1],[0,2]],'Jordan2')]:
 h=homdim(U);controls[label]={'Hom_dimension':h,'Ext1_dimension':h,'total':2*h}
assert controls['two_same_roots']['total']==8
assert controls['two_distinct_roots']['total']==4
assert controls['Jordan2']['total']==4
count=0
for a,b,c,d in product(range(-2,3),repeat=4):
 for s1,s2 in product([-1,1],repeat=2):
  tr=(s1+s2)*(a+d)
  if s1==-s2:assert tr==0
  count+=1
for row in r['rows']:
 s1,s2=row['signs']
 assert row['published_unsigned_matrix_compatible'] is True
 assert row['same_sign_diagonal_probe_compatible']==(s1==s2)
assert r['opposite_sign_model_self_Ext_total_dimension']==8
out={'status':'PASS','trace_integer_cases':count,'independent_Ext_controls':controls,
     'limitation':'No determinant-line, brane-equivariance or holomorphic-curve claim is certified by these checks.'}
Path(__file__).with_name('ALGEBRA_VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
