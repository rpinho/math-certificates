"""Independent Arb proof of the signed-contact scalar lemma.
Reads only a frozen rational partition. Imports no proposal/search code.
"""
import json,hashlib,time,argparse
from pathlib import Path
from fractions import Fraction as F
from flint import arb,fmpq,ctx
if not __debug__:raise SystemExit('Run without -O: structural assertions are required')

def A(q):
 q=F(q);return arb(fmpq(q.numerator,q.denominator))
def pos(v,label):
 if not v>0:raise ValueError((label,str(v)))
def down(v):return arb(v.lower())
def up(v):return arb(v.upper())
def lowmin(*vs):return arb(min(v.lower() for v in vs))
def highmax(*vs):return arb(max(v.upper() for v in vs))
def mulrange(al,ah,bl,bh):
 vals=[al*bl,al*bh,ah*bl,ah*bh];return lowmin(*vals),highmax(*vals)
def verify(path):
 raw=Path(path).read_bytes();d=json.loads(raw);assert d['model']=='signed_contact_v4' and F(d['zeta'])==F(19,200)
 root=list(map(F,d['root']));assert root==list(map(F,['0','31/100','0','31/100','77/100','1']))
 z=A('19/200');kap2=A('6/25');delta=A('1/10000')
 pos(A('31/100')**2-z,'large first moment');pos(kap2*(1-A('77/100')**2)-z,'small second moment')
 # Small a: b<=.99 gives a strictly positive even quadratic weight.
 p=kap2*(1-A('99/100'))-delta;q=A('12/25')*A('77/100')
 gm=(p.sqrt()+(p+q).sqrt())**2/4;pos(gm-z,'small a, b<=.99')
 # b>=.99: use the polynomial/log argument, with all bins explicit.
 ell=A('12/25')*A('99/100');start=F(1,2048)
 pos(4*ell-(1+delta)**2,'polynomial');pos(ell-delta*(1+delta),'x0<1')
 pos(A(start)-2*delta/ell,'monotone gamma');pos(A(start)-delta*(1+delta)/(2*ell),'d below bins')
 coarse=[F(1,2**k) for k in range(11,-1,-1)]
 coarse[-1]=F(1023,1024)
 bins=sorted(set(a+(b-a)*F(j,128) for a,b in zip(coarse,coarse[1:]) for j in range(129)))
 total=(ell/16).log()
 for u,v in zip(bins,bins[1:]):
  gamma=1/A(v)-delta/(ell*A(v)**2);pos(gamma-1,'gamma')
  mass=2/arb.pi()*(A(v).sqrt().asin()-A(u).sqrt().asin())
  total+=mass*gamma.log()
 pos(total-z.log(),'small a, b>=.99');pos(ell/4-z,'a=0')
 small_gap=total-z.log()
 cache={};counts={};worst=None;minnode=None
 def walk(node,box,depth=0):
  nonlocal worst,minnode
  assert depth<80
  if 'axis' in node:
   ax=node['axis'];assert type(ax)==int and ax in (0,1,2)
   m=F(node['mid']);assert box[2*ax]<m<box[2*ax+1]
   L=list(box);R=list(box);L[2*ax+1]=m;R[2*ax]=m
   walk(node['left'],L,depth+1);walk(node['right'],R,depth+1);return
  kind=node['kind'];counts[kind]=counts.get(kind,0)+1
  assert sum(counts.values())<=100000
  xl,xh,yl,yh,bl,bh=box
  s0=A(xl*xl+yl*yl)+kap2*(1-A(bh*bh))
  if kind=='S':pos(s0-z,'constant S');return
  if kind=='small':assert xh*xh+yh*yh<=F(1,10000)**2;return
  assert kind=='grid';n=node['n'];assert type(n)==int and 16<=n<=131072
  if n not in cache:
   h=arb.pi()/n;rows=[]
   for j in range(n):
    t=arb.pi()*(2*j+1)/n;c=t.cos();s=t.sin();c2=(2*t).cos()
    def ran(v,h):return arb(max(-1,(v-h).lower())),arb(min(1,(v+h).upper()))
    rows.append((c,s,*ran(c,h),*ran(s,h),*ran(c2,2*h)))
   cache[n]=(h,rows)
  h,rows=cache[n];s1=A(xh*xh+yh*yh)+kap2*(1-A(bl*bl));sm=arb(0);rc=arb(0);rs=arb(0);err=arb(0)
  for c,s,cl,ch,sl,sh,dl,dh in rows:
   x0,x1=mulrange(A(xl),A(xh),cl,ch);y0,y1=mulrange(A(yl),A(yh),sl,sh);b0,b1=mulrange(A(bl),A(bh),dl,dh)
   wl=arb(max(s0.lower(),(kap2*(1-b1)+x0+y0).lower()))
   wh=highmax(s1,kap2*(1-b0)+x1+y1)
   pos(wl,'positive grid lower');ll=down(wl.log());lh=up(wh.log());m=(ll+lh)/2;dd=(lh-ll)/2
   sm+=ll;rc+=m*c;rs+=m*s;err+=dd+abs(m)*h
  mean=sm/n;rnorm=((rc/n)**2+(rs/n)**2).sqrt();E=err/n
  gap=mean.exp()-z*(1+(rnorm+E)**2);pos(gap,('scalar leaf',counts['grid']))
  if worst is None or gap<worst:worst=gap;minnode=list(map(str,box))
 walk(d['tree'],root)
 return dict(status='PASS',model=d['model'],zeta=d['zeta'],bits=ctx.prec,sha256=hashlib.sha256(raw).hexdigest(),leaf_counts=counts,min_scalar_gap=str(worst),worst_box=minnode,small_a_log_gap=str(small_gap),small_a_low_b_gm=str(gm))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('cover');ap.add_argument('--output',default='signed-verification.json');ap.add_argument('--bits',type=int,default=256);a=ap.parse_args();ctx.prec=a.bits;t=time.monotonic();out=verify(a.cover);out['seconds']=time.monotonic()-t;print(json.dumps(out,indent=2));Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
