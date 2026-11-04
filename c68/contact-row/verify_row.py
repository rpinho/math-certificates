"""Separately written (same agent) Arb verifier for contact-row partitions.

No search/proposal, numpy, scipy or previous acceptance-checker imports.
Each failure has a stable, exact rejection code for corruption controls.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json,time,argparse
from flint import arb,fmpq,ctx

class Rejection(ValueError):pass
def require(condition,code):
 if not condition:raise Rejection(code)
def A(q):
 q=Q(q);return arb(fmpq(q.numerator,q.denominator))
def lower(x):return arb(x.lower())
def upper(x):return arb(x.upper())
def min_lower(*args):return arb(min(x.lower() for x in args))
def min_upper(*args):return arb(min(x.upper() for x in args))
def max_lower(*args):return arb(max(x.lower() for x in args))
def max_upper(*args):return arb(max(x.upper() for x in args))
def product(al,ah,bl,bh):
 v=[al*bl,al*bh,ah*bl,ah*bh];return min_lower(*v),max_upper(*v)
def small_parameters(z):
 # For b<=.999, p=.24(1-b)-delta>0 and q=.48b. The even
 # outer factor has constant-square (p+q/2+sqrt(p(p+q)))/2 >=.12-delta/2.
 delta=A('1/1000000');ell=A('12/25')*A('999/1000')
 require(A('6/25')/1000-delta>0,'SMALL_LOW_B_POSITIVE')
 require(A('3/25')-delta/2>z,'SMALL_LOW_B_MARGIN')
 require(4*ell>(1+delta)**2,'SMALL_POLYNOMIAL')
 require(ell>delta*(1+delta),'SMALL_X0')
 coarse=[Q(1,2**k) for k in range(17,0,-1)]+[Q(16383,16384)]
 require(A(coarse[0])>2*delta/ell,'SMALL_GAMMA_MONOTONE')
 require(A(coarse[0])>delta*(1+delta)/(2*ell),'SMALL_ROOT_BELOW_BINS')
 total=(ell/16).log();bins=0
 for a,b in zip(coarse,coarse[1:]):
  for j in range(512):
   u=a+(b-a)*Q(j,512);v=a+(b-a)*Q(j+1,512)
   gamma=1/A(v)-delta/(ell*A(v)**2)
   require(gamma>1,'SMALL_GAMMA')
   mass=2/arb.pi()*(A(v).sqrt().asin()-A(u).sqrt().asin())
   total+=mass*gamma.log();bins+=1
 require(total>z.log(),'SMALL_LOG_MARGIN')
 require(ell/4>z,'SMALL_ZERO_ENDPOINT')
 return {'bins':bins,'log_margin':str(total-z.log()),'geometric_mean_lower':str(total.exp()),'zero_endpoint_margin':str(ell/4-z)}

def verify(path):
 raw=Path(path).read_bytes();data=json.loads(raw)
 require(data.get('model')=='contact_row_v1','COVER_MODEL')
 require(Q(data.get('zeta','0'))==Q(23,200),'COVER_ZETA')
 require(Q(data.get('kappa','0'))==Q(3,25),'COVER_KAPPA')
 require(Q(data.get('delta','0'))==Q(1,1000000),'COVER_DELTA')
 root=list(map(Q,data.get('root',[])))
 require(root==list(map(Q,['0','17/50','0','17/50','7/10','1'])),'COVER_ROOT')
 z=A('23/200');kap=A('6/25');delta=Q(1,1000000)
 require(A('17/50')**2>z,'LARGE_FIRST_MOMENT')
 require(kap*(1-A('7/10')**2)>z,'SMALL_SECOND_MOMENT')
 # This ensures the determinant's maximum is at b=bl and x=xl,y=yl.
 require(root[4]>root[1]**2,'PSD_MONOTONICITY')
 small=small_parameters(z);cache={};counts={};worst=None;worst_box=None;grid_cells=0;maxdepth=0
 def walk(node,box,depth=0):
  nonlocal worst,worst_box,grid_cells,maxdepth
  require(depth<=110,'COVER_DEPTH');maxdepth=max(maxdepth,depth)
  require(type(node)==dict,'COVER_NODE')
  if 'axis' in node:
   require(set(node)=={'axis','mid','left','right'},'COVER_NODE')
   axis=node['axis'];require(type(axis)==int and axis in (0,1,2),'COVER_AXIS')
   mid=Q(node['mid']);require(box[2*axis]<mid<box[2*axis+1],'COVER_SPLIT')
   left=list(box);right=list(box);left[2*axis+1]=mid;right[2*axis]=mid
   walk(node['left'],left,depth+1);walk(node['right'],right,depth+1);return
  kind=node.get('kind');require(kind in ('psd','constant','small','grid'),'COVER_LEAF_KIND')
  require(set(node)==({'kind','n'} if kind=='grid' else {'kind'}),'COVER_LEAF_FIELDS')
  counts[kind]=counts.get(kind,0)+1;require(sum(counts.values())<=200000,'COVER_LEAF_COUNT')
  xl,xh,yl,yh,bl,bh=box
  if kind=='psd':
   determinant=1-bl*bl-2*(1-bl)*xl*xl-2*(1+bl)*yl*yl
   require(determinant<0,'PSD_NOT_EXCLUDED');return
  if kind=='small':require(xh*xh+yh*yh<=delta*delta,'SMALL_REGION');return
  al=lower(A(xl*xl+yl*yl).sqrt());ah=upper(A(xh*xh+yh*yh).sqrt())
  sl=lower(A(xl*xl+yl*yl)+kap*(1-A(bh*bh)))
  sh=upper(A(xh*xh+yh*yh)+kap*(1-A(bl*bl)))
  if xh*xh+yh*yh>0:
   numerator_low=A((1+bl)*xl*xl+(1-bh)*yl*yl)
   jl=lower((al*al+numerator_low/(2*ah))/(1+ah))
   if xl*xl+yl*yl==0:jh=ah
   else:
    numerator_high=A((1+bh)*xh*xh+(1-bl)*yh*yh)
    jh=min_upper(ah,(ah*ah+numerator_high/(2*al))/(1+al))
  else:jl=jh=arb(0)
  floor_low=max_lower(sl,jl);floor_high=max_upper(sh,jh)
  if kind=='constant':require(floor_low>z,'CONSTANT_FLOOR');return
  n=node.get('n');require(type(n)==int and n in (4096,8192,16384,32768,65536,131072,262144),'GRID_SIZE')
  if n not in cache:
   h=arb.pi()/n;rows=[]
   for j in range(n):
    theta=arb.pi()*(2*j+1)/n;c=theta.cos();s=theta.sin();d=(2*theta).cos();ds=(2*theta).sin()
    # Taylor's theorem, using second derivative absolute bounds 1,1,4.
    def interval(v,e):return arb(max(-1,(v-e).lower())),arb(min(1,(v+e).upper()))
    rows.append((c,s,*interval(c,abs(s)*h+h*h/2),*interval(s,abs(c)*h+h*h/2),*interval(d,2*abs(ds)*h+2*h*h)))
   cache[n]=(h,rows)
  h,rows=cache[n];logmean=arb(0);rc=arb(0);rs=arb(0);error=arb(0)
  for c,s,cl,ch,sl0,sh0,dl,dh in rows:
   lx,hx=product(A(xl),A(xh),cl,ch);ly,hy=product(A(yl),A(yh),sl0,sh0);lb,hb=product(A(bl),A(bh),dl,dh)
   wl=max_lower(floor_low,lx+ly+kap*(1-hb))
   wh=max_upper(floor_high,hx+hy+kap*(1-lb))
   require(wl>0,'GRID_NONPOSITIVE')
   lo=lower(wl.log());hi=upper(wh.log());center=(lo+hi)/2;radius=(hi-lo)/2
   logmean+=lo;rc+=center*c;rs+=center*s;error+=radius+abs(center)*h
  logmean/=n;rc/=n;rs/=n;error/=n
  harmonic=upper((rc*rc+rs*rs).sqrt()+error)
  gap=logmean.exp()-z*(1+harmonic*harmonic)
  require(gap>0,'GRID_SCALAR_MARGIN');grid_cells+=n
  if worst is None or gap<worst:worst=gap;worst_box=list(map(str,box))
 walk(data.get('tree'),root)
 return dict(status='PASS',verifier='separately written (same agent)',model=data['model'],zeta=data['zeta'],sha256=hashlib.sha256(raw).hexdigest(),bits=ctx.prec,counts=counts,max_depth=maxdepth,grid_cells=grid_cells,min_scalar_gap=str(worst),worst_box=worst_box,small_parameters=small)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('cover');p.add_argument('--bits',type=int,default=256);p.add_argument('--output',default='logs/row-verification.json');a=p.parse_args();ctx.prec=a.bits;start=time.monotonic()
 try:out=verify(a.cover);out['seconds']=time.monotonic()-start
 except Rejection as e:out={'status':'REJECT','code':str(e)}
 Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
 if out['status']!='PASS':raise SystemExit(1)
