"""Exact witness construction from our own floating box selector.
No third-party code. Soundness is decided by the separate verify_exact.py.
"""
import argparse,bisect,hashlib,json,math,time
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from objective import evaluate
from select_cover import select_cover

def generate(src,out,Q=10**14,D=2**48):
 start=time.time();d=json.loads(Path(src).read_text());d=d.get('measure',d)
 def rat(v):return F(v) if isinstance(v,str) else F(round(v*Q),Q)
 reach=float(d.get('reach',6));px,py=map(rat,(d['Px'],d['Py']));pts=[tuple(map(rat,p)) for p in d['pts']]
 measure={'Px':str(px),'Py':str(py),'lam':'1','reach':str(reach),'pts':[[str(v) for v in p] for p in pts]}
 Path(out.replace('.json','-measure.json')).write_text(json.dumps(measure,indent=1)+'\n')
 p=np.array([[float(t) for t in z] for z in pts]);boxfile=Path(out+'.boxes.tsv')
 q,ar,nr=evaluate(float(px),float(py),p,reach=reach,export=boxfile)
 print('float',q,'boxes',nr,flush=True)
 dx=math.lcm(px.denominator,py.denominator,*[v.denominator for p in pts for v in p[:2]])
 dm=math.lcm(*[m.denominator for x,y,m in pts]);L=math.lcm(dx,D);sx=L//dx;sr=L//D
 pxI,pyI=int(px*dx),int(py*dx)
 # This finite window contains all exported boundaries (R<4 in search region).
 P=[(int(x*dx)+i*pxI,int(y*dx)+j*pyI,int(m*dm)) for i in range(-4,5) for j in range(-4,5) for x,y,m in pts]
 X=sorted({x for x,y,m in P});Y=sorted({y for x,y,m in P});xf=[x/dx for x in X];yf=[y/dx for y in Y];xi={x:i for i,x in enumerate(X)};yi={y:i for i,y in enumerate(Y)}
 G=[[0]*(len(Y)+1) for _ in range(len(X)+1)]
 for x,y,m in P:G[xi[x]+1][yi[y]+1]+=m
 for i in range(1,len(X)+1):
  acc=0
  for j in range(1,len(Y)+1):acc+=G[i][j];G[i][j]=G[i-1][j]+acc
 def nearest(v,grid):
  j=bisect.bisect_left(grid,v);k=min((i for i in (j-1,j) if 0<=i<len(grid)),key=lambda i:abs(v-grid[i]));assert abs(v-grid[k])<1e-10;return k
 boxes={tuple(nearest(v,g) for v,g in zip(map(float,line.split()),[xf,xf,yf,yf])) for line in boxfile.read_text().splitlines()}
 rects={}
 for a,b,c,d in boxes:
  m=G[b+1][d+1]-G[a][d+1]-G[b+1][c]+G[a][c];k=math.isqrt(m*D*D//(4*dm))-1
  if k<=0:continue
  rho=k*sr;r=(max(0,X[b]*sx-rho),min(pxI*sx,X[a]*sx+rho),max(0,Y[d]*sx-rho),min(pyI*sx,Y[c]*sx+rho))
  if r[0]<r[1] and r[2]<r[3]:rects[r]=[a,b,c,d,k]
 rectangles=list(rects);selected=select_cover(rectangles);w=[]
 for i in selected:
  a,b,c,d,k=rects[rectangles[i]];w.append({'box':[str(F(v,dx)) for v in (X[a],X[b],Y[c],Y[d])],'radius':str(F(k,D)),'rectangle':[str(F(v,L)) for v in rectangles[i]]})
 cert={'format':'c47-witness-rectangles-v1','measure':measure,'D':D,'witnesses':w,'status':'candidate, unverified by a third party','credit':"Fresh search from our #321; Doldrums/SCiEL #341 supplies the bar and moves/insertions/removals idea; Tomar Lemma 6.2 following Lin. Separately written (same agent) verifier.",'producer_seconds':time.time()-start,'search_source':str(src)}
 Path(out).write_text(json.dumps(cert,indent=1)+'\n');print('retained',len(w),'seconds',time.time()-start,flush=True)
 return cert
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('output');a=ap.parse_args();generate(a.input,a.output)
