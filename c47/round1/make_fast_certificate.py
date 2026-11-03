"""Fast certificate producer: Tomar's C box scan chooses candidates in floats;
every retained radius and rectangle is then reconstructed with exact integers.
Completeness of candidate selection is not needed for a lower certificate.
The separately written verifier remains verify_exact.py and imports none of this.
"""
import argparse,bisect,ctypes,hashlib,json,math,time
from fractions import Fraction as F
from pathlib import Path

def select_cover(rectangles):
 # Exact greedy cover on each x slab, with a prefix-maximum tree over active
 # interval starts. Candidate pruning only; verify_exact.py checks the result.
 import heapq
 if not rectangles:return []
 ys=sorted({r[2] for r in rectangles});yi={y:i for i,y in enumerate(ys)}
 size=1
 while size<len(ys):size*=2
 tree=[(-1,-1)]*(2*size);heaps=[[] for _ in ys];counts=[0]*len(ys);present=[False]*len(ys)
 live=[False]*len(rectangles);active_y=[];used=set();events={}
 for i,(x0,x1,y0,y1) in enumerate(rectangles):events.setdefault(x0,[]).append((1,i));events.setdefault(x1,[]).append((-1,i))
 def update(j,value):
  j+=size;tree[j]=value;j//=2
  while j:tree[j]=max(tree[2*j],tree[2*j+1]);j//=2
 def prefix(pos):
  l=size;r=size+bisect.bisect_right(ys,pos);answer=(-1,-1)
  while l<r:
   if l&1:answer=max(answer,tree[l]);l+=1
   if r&1:r-=1;answer=max(answer,tree[r])
   l//=2;r//=2
  return answer
 for x,changes in sorted(events.items()):
  touched=set()
  for sign,i in changes:
   j=yi[rectangles[i][2]];touched.add(j)
   if sign==1:live[i]=True;counts[j]+=1;heapq.heappush(heaps[j],(-rectangles[i][3],i))
   else:live[i]=False;counts[j]-=1
  for j in touched:
   h=heaps[j]
   while h and not live[h[0][1]]:heapq.heappop(h)
   has=counts[j]>0
   if has and not present[j]:bisect.insort(active_y,j)
   elif present[j] and not has:active_y.pop(bisect.bisect_left(active_y,j))
   present[j]=has;update(j,(-h[0][0],h[0][1]) if h else (-1,-1))
  if not active_y:continue
  pos=ys[active_y[0]]
  while True:
   end,i=prefix(pos)
   if end>pos:used.add(i);pos=end
   else:
    j=bisect.bisect_left(active_y,bisect.bisect_right(ys,pos))
    if j==len(active_y):break
    pos=ys[active_y[j]]
 return sorted(used)

def generate(path,out,D,reach,Q=0):
 start=time.time();raw=Path(path).read_bytes();d=json.loads(raw);px,py,lam=map(F,[d['Px'],d['Py'],d['lam']]);pts=[tuple(map(F,p)) for p in d['pts']]
 assert lam==1 and px>0 and py>0 and pts
 dx=math.lcm(*[q.denominator for q in [px,py,reach]+[v for p in pts for v in p[:2]]]);dm=math.lcm(*[p[2].denominator for p in pts]);L=math.lcm(dx,D);sx=L//dx;sr=L//D
 pxI,pyI,rI=map(lambda v:int(v*dx),(px,py,reach));mc=sum(m for x,y,m in pts)
 nb=(int(reach/px)+2)*(int(reach/py)+2);q=nb*mc*D*D/4;rb=F(math.isqrt(q.numerator//q.denominator)+1,D);rbI=math.ceil(rb*dx)+1;ext=rI+rbI
 P=[(int(x*dx),int(y*dx),int(m*dm)) for x,y,m in pts];nx=ext//pxI+2;ny=ext//pyI+2
 W=[(x+i*pxI,y+j*pyI,m) for i in range(-nx,nx+1) for j in range(-ny,ny+1) for x,y,m in P if -ext<=x+i*pxI<=pxI+ext and -ext<=y+j*pyI<=pyI+ext]
 X=sorted({x for x,y,m in W});Y=sorted({y for x,y,m in W});xi={x:i for i,x in enumerate(X)};yi={y:i for i,y in enumerate(Y)}
 G=[[0]*(len(Y)+1) for _ in range(len(X)+1)]
 for x,y,m in W:G[xi[x]+1][yi[y]+1]+=m
 for i in range(1,len(X)+1):
  acc=0
  for j in range(1,len(Y)+1):acc+=G[i][j];G[i][j]=G[i-1][j]+acc
 c=ctypes;dp=c.POINTER(c.c_double);library=c.CDLL('./libcertificate.so');f=library.export_boxes;f.restype=c.c_double;f.argtypes=[c.c_int,dp,dp,dp]+[c.c_double]*7+[c.POINTER(c.c_int),c.c_char_p]
 A=(c.c_double*len(W))(*[x/dx for x,y,m in W]);B=(c.c_double*len(W))(*[y/dx for x,y,m in W]);M=(c.c_double*len(W))(*[m/dm for x,y,m in W]);count=c.c_int()
 boxfile=Path(out+'.selected-boxes.tsv');area=f(len(W),A,B,M,1.,0.,float(px),0.,float(py),float(reach),float(rb)+1e-7,c.byref(count),str(boxfile).encode())
 print('float selection',count.value,'area',area,'seconds',time.time()-start,flush=True)
 xf=[v/dx for v in X];yf=[v/dx for v in Y]
 def nearest(v,grid):
  j=bisect.bisect_left(grid,v);options=[k for k in (j-1,j) if 0<=k<len(grid)];return min(options,key=lambda k:abs(grid[k]-v))
 boxes=set()
 for line in boxfile.read_text().splitlines():
  a,b,e,f=map(float,line.split());boxes.add((nearest(a,xf),nearest(b,xf),nearest(e,yf),nearest(f,yf)))
 rects={}
 for ia,ib,ja,jb in boxes:
  ms=G[ib+1][jb+1]-G[ia][jb+1]-G[ib+1][ja]+G[ia][ja]
  if ms<=0:continue
  k=math.isqrt(ms*D*D//(4*dm))-1
  if k<=0:continue
  xa,xb,ya,yb=X[ia],X[ib],Y[ja],Y[jb];rho=k*sr
  R=(max(xb*sx-rho,0),min(xa*sx+rho,pxI*sx),max(yb*sx-rho,0),min(ya*sx+rho,pyI*sx))
  if Q:
   R=((-(-R[0]*Q//L)),R[1]*Q//L,(-(-R[2]*Q//L)),R[3]*Q//L)
  if R[0]<R[1] and R[2]<R[3]:rects[R]=[xa,xb,ya,yb,k]
 rectangles=list(rects);selected=select_cover(rectangles)
 print('exact rectangles',len(rectangles),'retained',len(selected),'seconds',time.time()-start,flush=True)
 witnesses=[]
 for i in selected:
  r=rectangles[i];xa,xb,ya,yb,k=rects[r];witnesses.append({'box':[str(F(v,dx)) for v in (xa,xb,ya,yb)],'radius':str(F(k,D)),'rectangle':[str(F(v,Q or L)) for v in r]})
 result={'format':'c47-witness-rectangles-v1','measure_sha256':hashlib.sha256(raw).hexdigest(),'measure':d,'D':D,'rectangle_grid_denominator':Q,'witnesses':witnesses,'credit':"Further hole-filling on Tomar's measure: the same insertion-and-refinement operation as his hf.py, applied by our own search scripts; Tomar Lemma 6.2 following Lin; Tomar v5 C box scan only for candidate selection; exact rational reconstruction",'status':'candidate, unrefereed','producer_seconds':time.time()-start}
 Path(out).write_text(json.dumps(result,indent=1)+'\n');print('DONE',out,flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('measure');ap.add_argument('output');ap.add_argument('--D',type=int,default=2**40);ap.add_argument('--reach',type=F,default=F(6));ap.add_argument('--grid',type=int,default=0);a=ap.parse_args();generate(a.measure,a.output,a.D,a.reach,a.grid)
