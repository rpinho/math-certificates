"""Translate PPSS's exact flagmatic SOS factors to this certificate format.
Original method/data: https://doi.org/10.5281/zenodo.6602512.
This is baseline reproduction, not a new bound.
"""
import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','RAYON_NUM_THREADS']:os.environ[k]='1'
import itertools,json,math,re
from fractions import Fraction
from pathlib import Path
X=json.load(open('sources/published_c5.json'));bound=Fraction(X['bound']);D=2**60
print('PUBLISHED_EXACT',str(bound),float(bound),flush=True)
meta={}
with open('artifacts/ordered8.meta') as f:
 next(f)
 for line in f:
  t,m,typ,d,*keys=map(int,line.split());meta[t,typ]=(m,d,keys)
def parse(s):
 match=re.match(r'(\d+):(\d*)',s);n=int(match[1]);h=0
 for i,j in zip(match[2][::2],match[2][1::2]):
  a,b=int(i)-1,int(j)-1
  if a>b:a,b=b,a
  h|=1<<(b*(b-1)//2+a)
 return n,h
def permute(h,p):
 return sum(((h>>(max(p[i],p[j])*(max(p[i],p[j])-1)//2+min(p[i],p[j])))&1)<<(j*(j-1)//2+i) for j in range(1,len(p)) for i in range(j))
blocks=[]
for z,typestr in enumerate(X['types']):
 t,tc=parse(typestr)
 best,p=min((permute(tc,list(p)),p) for p in itertools.permutations(range(t)))
 m,d,keys=meta[t,best];root=list(p);fl=X['flags'][z];assert len(fl)==d
 reorder=[];lookup={key:i for i,key in enumerate(keys)}
 for flag in fl:
  s,g=parse(flag);assert s==t+m
  can=min(permute(g,root+list(u)) for u in itertools.permutations(range(t,t+m)))
  reorder.append(lookup[can])
 assert len(set(reorder))==d
 qd=X['qdash_matrices'][z];R=X['r_matrices'][z]
 assert qd is not None and R is not None
 h=len(qd)
 assert all(Fraction(v)==int(j==0) for row in qd for j,v in enumerate(row)),('nonidentity Qdash',z)
 assert len(R)==d and all(len(r)==h for r in R)
 L=[[0]*d for _ in range(h)]
 for i,row in enumerate(R):
  for r,v in enumerate(row):
   v=Fraction(v)*D;assert v.denominator==1
   L[r][reorder[i]]=v.numerator
 L=[row for row in L if any(row)]
 if not L:L=[[0]*d]
 blocks.append((t,m,best,d,len(L),keys,L))
 print('block',z,t,best,d,len(L),flush=True)
blocks.sort(key=lambda b:(b[0],b[2]))
out=Path('artifacts/ppss_baseline.cert')
with out.open('w') as f:
 print(8,5,D,len(blocks),bound.numerator,bound.denominator,1,file=f)
 for t,m,typ,d,h,flags,L in blocks:
  print(t,m,typ,d,h,file=f);print(*flags,file=f)
  for row in L:print(*row,file=f)
print('IMPORTED',out,flush=True)
