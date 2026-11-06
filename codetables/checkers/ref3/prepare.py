"""Fresh exact finite-field arithmetic and disjoint-information-set preparation."""
import json, itertools, pathlib, hashlib, random
ROOT=pathlib.Path(__file__).parent
class Field:
 def __init__(self,q):
  self.q=q
  self.add=lambda x,y: (x+y)%5 if q==5 else (x%3+y%3)%3+3*((x//3+y//3)%3)
  self.mul=lambda x,y: (x*y)%5 if q==5 else (x%3*(y%3)-x//3*(y//3))%3+3*((x%3*(y//3)+x//3*(y%3))%3)
  self.neg=[next(y for y in range(q) if self.add(x,y)==0) for x in range(q)]
  self.inv=[0]+[next(y for y in range(1,q) if self.mul(x,y)==1) for x in range(1,q)]
 def rref(self,G,order=None):
  A=[r[:] for r in G]; k=len(A); n=len(A[0]); piv=[]
  for c in (range(n) if order is None else order):
   r=len(piv); s=next((s for s in range(r,k) if A[s][c]),None)
   if s is None: continue
   A[r],A[s]=A[s],A[r]; v=self.inv[A[r][c]]; A[r]=[self.mul(v,x) for x in A[r]]
   for s in range(k):
    if s!=r and A[s][c]:
     v=self.neg[A[s][c]]; A[s]=[self.add(x,self.mul(v,y)) for x,y in zip(A[s],A[r])]
   piv.append(c)
   if len(piv)==k: break
  return A,piv
 def encode(self,G,m):
  return [self.sum(self.mul(a,b) for a,b in zip(m,c)) for c in zip(*G)]
 def sum(self,x):
  v=0
  for a in x:v=self.add(v,a)
  return v

def prep(G,q,name):
 f=Field(q); A,p=f.rref(G); rank=len(p); G=A[:rank]; k=rank; n=len(G[0]); unused=list(range(n)); blocks=[]
 while unused:
  B,p=f.rref(G,unused); r=len(p)
  if not r: break
  B,pfull=f.rref(G,p+[c for c in range(n) if c not in p]); assert len(pfull)==k
  assert all(B[i][c]==int(i==j) for j,c in enumerate(pfull) for i in range(k))
  blocks.append({'rank':r,'pivots':pfull,'new_pivots':p,'G':B})
  unused=[c for c in unused if c not in p]
 out={'q':q,'n':n,'k':k,'rank':rank,'blocks':blocks,'zero_columns':[j for j in range(n) if not any(row[j] for row in G)]}
 (ROOT/'results'/f'{name}.prep.json').write_text(json.dumps(out))
 with (ROOT/'results'/f'{name}.dat').open('w') as h:
  h.write(f'{q} {n} {k} {len(blocks)}\n')
  for b in blocks:
   h.write(str(b['rank'])+'\n')
   for row in b['G']: h.write(' '.join(map(str,row))+'\n')
 return out

def controls():
 report={}
 for q in (5,9):
  f=Field(q)
  for a,b,c in itertools.product(range(q),repeat=3):
   assert f.add(a,b)==f.add(b,a) and f.mul(a,b)==f.mul(b,a)
   assert f.add(f.add(a,b),c)==f.add(a,f.add(b,c))
   assert f.mul(f.mul(a,b),c)==f.mul(a,f.mul(b,c))
   assert f.mul(a,f.add(b,c))==f.add(f.mul(a,b),f.mul(a,c))
  for a in range(q):
   assert f.add(a,0)==a and f.mul(a,1)==a and f.add(a,f.neg[a])==0
   if a: assert f.mul(a,f.inv[a])==1
  if q==9: assert f.mul(3,3)==2
  G=[[1]*q,list(range(q)),[f.mul(x,x) for x in range(q)]]
  dist={}
  for m in itertools.product(range(q),repeat=3):
   if not any(m):continue
   w=sum(x!=0 for x in f.encode(G,m)); dist[w]=dist.get(w,0)+1
  assert min(dist)==q-2
  prep(G,q,f'control_q{q}')
  report[str(q)]={'field_axioms':'all triples checked','add_table':[[f.add(a,b) for b in range(q)] for a in range(q)],'mul_table':[[f.mul(a,b) for b in range(q)] for a in range(q)],'RS_parameters':[q,3,q-2],'weight_distribution':dist}
 (ROOT/'results'/'controls_python.json').write_text(json.dumps(report,indent=2))

if __name__=='__main__':
 controls(); mats={}; summary={}
 for path in sorted((ROOT/'inputs').glob('q*.txt')):
  G=[list(map(int,line.split())) for line in path.read_text().splitlines()]; q=int(path.name[1]); n=int(path.name.split('_n')[1].split('_')[0]); k=int(path.name.split('_k')[1].split('_')[0])
  assert len(G)==k and all(len(r)==n and all(0<=x<q for x in r) for r in G)
  expected=dict((b,a) for a,b in (l.split() for l in (ROOT/'inputs'/'SHA256SUMS').read_text().splitlines()))[path.name]
  assert hashlib.sha256(path.read_bytes()).hexdigest()==expected
  out=prep(G,q,path.stem); mats[path.stem]=G
  summary[path.stem]={'rank':out['rank'],'block_ranks':[b['rank'] for b in out['blocks']],'zero_columns':out['zero_columns'],'sha256':expected}
 A=mats['q5_n129_k14_d80']; B=mats['q5_n130_k14_d81']; f=Field(5); RA=f.rref(A)[0]
 relation=[]
 for c in range(130):
  P=[r[:c]+r[c+1:] for r in B]
  if f.rref(P)[0]==RA:relation.append(c)
 summary['puncturing_130_14_to_129_14_zero_based_columns']=relation
 (ROOT/'results'/'preparation.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
