"""Alternate replay, separately written (same agent).

Scalar: mpmath.iv with direct trigonometric ranges, rather than Arb/Taylor.
Measure: integer ordinary moments and a 5000-cell interval tail minorant,
rather than the acceptance checker's global cubic. No other checker imports.
"""
import argparse,json,time,hashlib,math
from fractions import Fraction as Q
from pathlib import Path
from mpmath import iv
iv.dps=90

def I(q):
 q=Q(q);return iv.mpf(q.numerator)/q.denominator
def lo(v):return iv.mpf(v.a)
def hi(v):return iv.mpf(v.b)
def lowmax(*v):return max([lo(x) for x in v],key=lambda x:x.a)
def highmax(*v):return max([hi(x) for x in v],key=lambda x:x.a)
def highmin(*v):return min([hi(x) for x in v],key=lambda x:x.a)
def hull(a,b):return iv.mpf([a.a,b.b])
def need(test,why):
 if not test:raise ValueError(why)
def small(z):
 delta=I('1/1000000');ell=I('12/25')*I('999/1000')
 need(I('6/25')/1000-delta>0,'small positive');need(I('3/25')-delta/2>z,'small low b')
 need(4*ell>(1+delta)**2 and ell>delta*(1+delta),'small polynomial')
 coarse=[Q(1,2**k) for k in range(17,0,-1)]+[Q(16383,16384)];total=iv.ln(ell/16)
 need(I(coarse[0])>2*delta/ell and I(coarse[0])>delta*(1+delta)/(2*ell),'small bin start')
 def asin(x):return iv.atan2(x,iv.sqrt(1-x*x))
 for a,b in zip(coarse,coarse[1:]):
  for j in range(512):
   u=I(a+(b-a)*Q(j,512));v=I(a+(b-a)*Q(j+1,512));gam=1/v-delta/(ell*v*v);need(gam>1,'small gamma')
   total+=2/iv.pi*(asin(iv.sqrt(v))-asin(iv.sqrt(u)))*iv.ln(gam)
 need(total>iv.ln(z),'small log');need(ell/4>z,'small endpoint')
 return str(total-iv.ln(z))

def scalar(path):
 raw=Path(path).read_bytes();d=json.loads(raw);need(d['model']=='contact_row_v1' and Q(d['zeta'])==Q(23,200),'scalar schema')
 root=list(map(Q,d['root']));need(root==list(map(Q,['0','17/50','0','17/50','7/10','1'])),'root')
 need(Q(d['kappa'])==Q(3,25) and Q(d['delta'])==Q(1,1000000),'constants');z=I('23/200');counts={};cache={};worst=None;gap_small=small(z);beg=time.monotonic()
 need(I('17/50')**2>z and I('6/25')*(1-I('7/10')**2)>z,'outside root')
 def walk(node,box,depth=0):
  nonlocal worst
  need(depth<=110,'depth')
  if 'axis' in node:
   need(set(node)=={'axis','mid','left','right'},'branch schema');axis=node['axis'];mid=Q(node['mid']);need(type(axis)==int and axis in (0,1,2),'axis');need(box[2*axis]<mid<box[2*axis+1],'split')
   a=list(box);b=list(box);a[2*axis+1]=mid;b[2*axis]=mid;walk(node['left'],a,depth+1);walk(node['right'],b,depth+1);return
  kind=node['kind'];counts[kind]=counts.get(kind,0)+1;xl,xh,yl,yh,bl,bh=box
  if kind=='psd':need(1-bl*bl-2*(1-bl)*xl*xl-2*(1+bl)*yl*yl<0,'psd');return
  if kind=='small':need(xh*xh+yh*yh<=Q(1,1000000)**2,'small');return
  al=lo(iv.sqrt(I(xl*xl+yl*yl)));ah=hi(iv.sqrt(I(xh*xh+yh*yh)))
  sl=lo(I(xl*xl+yl*yl)+I('6/25')*(1-I(bh*bh)));sh=hi(I(xh*xh+yh*yh)+I('6/25')*(1-I(bl*bl)))
  if ah>0:
   jl=lo(al*al/(1+al)+I((1+bl)*xl*xl+(1-bh)*yl*yl)/(2*ah*(1+ah)))
   jh=ah if xl*xl+yl*yl==0 else highmin(ah,ah*ah/(1+ah)+I((1+bh)*xh*xh+(1-bl)*yh*yh)/(2*al*(1+al)))
  else:jl=jh=I(0)
  fl=lowmax(sl,jl);fh=highmax(sh,jh)
  if kind=='constant':need(fl>z,'constant');return
  need(kind=='grid','leaf');n=node['n'];need(type(n)==int and n in [4096,8192,16384,32768,65536,131072,262144],'grid n')
  if n not in cache:
   rows=[];h=iv.pi/n
   for j in range(n):
    # A full cell angle is bounded directly, with no derivative estimate.
    theta=iv.pi*iv.mpf([2*j,2*j+2])/n;center=iv.pi*(2*j+1)/n
    rows.append((iv.cos(center),iv.sin(center),iv.cos(theta),iv.sin(theta),iv.cos(2*theta)))
   cache[n]=(h,rows)
  h,rows=cache[n];L=I(0);re=I(0);im=I(0);err=I(0)
  xx=hull(I(xl),I(xh));yy=hull(I(yl),I(yh));bb=hull(I(bl),I(bh))
  for cs,sn,c,s,c2 in rows:
   tr=xx*c+yy*s+I('6/25')*(1-bb*c2);wl=lowmax(fl,tr);wh=highmax(fh,tr);need(wl>0,'positive')
   l=lo(iv.ln(wl));u=hi(iv.ln(wh));m=(l+u)/2;rad=(u-l)/2
   L+=l;re+=m*cs;im+=m*sn;err+=rad+abs(m)*h
  upper_h=hi(iv.sqrt((re/n)**2+(im/n)**2)+err/n);gap=iv.exp(L/n)-z*(1+upper_h**2);need(gap>0,'scalar margin')
  if worst is None or gap.a<worst.a:worst=gap
  if counts['grid']%20==0:print('scalar grids',counts['grid'],'seconds',time.monotonic()-beg,flush=True)
 walk(d['tree'],root)
 return dict(status='PASS',verification='separately written (same agent)',backend='mpmath.iv direct trigonometric cells',sha256=hashlib.sha256(raw).hexdigest(),counts=counts,min_scalar_gap=str(worst),small_log_gap=gap_small)

def measure(path):
 raw=Path(path).read_bytes();d=json.loads(raw);need(d['model']=='contact_row_v1' and Q(d['c'])==Q(447,1000) and Q(d['zeta'])==Q(23,200) and Q(d['kappa'])==Q(3,25),'measure schema')
 c=Q(d['c']);R=Q(d['R']);nd=list(map(Q,d['nodes']));wt=list(map(Q,d['weights']));need(len(nd)==len(wt) and nd[0]==c*c and nd[-1]==R and sum(wt)==R and all(x>0 for x in wt) and all(x<y for x,y in zip(nd,nd[1:])),'measure structure')
 K1,K2=d['first_tail_k'],d['second_tail_k'];need(type(K1)==type(K2)==int and 2<=K1<=100000 and 2<=K2<=100000,'cutoffs');need(wt[-1]*(K1+1)>=R,'first infinite')
 den=10**18;ni=[int(x*den) for x in nd];wi=[int(x*den) for x in wt];ri=int(R*den)
 need(all(Q(x,den)==t for x,t in zip(ni,nd)) and all(Q(x,den)==t for x,t in zip(wi,wt)),'integer scaling')
 powers=[1]*len(nd);rp=ri
 for k in range(1,K1):
  powers=[p*t for p,t in zip(powers,ni)];rp*=ri;gap=(k+1)*sum(x*y for x,y in zip(wi,powers))-rp;need(gap>0,'exact ordinary '+str(k))
 print('exact integer ordinary moments PASS',K1-1,flush=True)
 w=-iv.ln(I(c));AA=iv.pi**2/w;q=iv.exp(-AA);P=(1+q)**2/(8*q);kap=I('3/25')
 def cosh(x):return (iv.exp(x)+iv.exp(-x))/2
 def sinh(x):return (iv.exp(x)-iv.exp(-x))/2
 def tanh(x):return (iv.exp(2*x)-1)/(iv.exp(2*x)+1)
 hypotheses=[I(1)/3-1/cosh(AA/2)**2,2*(1-8*kap)*P-16*sinh(AA/4)**2,tanh(AA/8)**2-(1+8*kap)*iv.pi**2/64,(1-4*kap)/2-1/cosh(AA/8)**2,P-6]
 need(all(x>0 for x in hypotheses),'analytic hypotheses')
 beta=[];epsilon=[]
 for j,t in enumerate(nd):
  if j==0:g=e=I(0)
  else:
   sig=iv.sin(iv.pi*iv.ln(I(t))/(2*w))**2;H=iv.sqrt(1+P/(2*sig));g=2/(1+H);e=I('23/200')*g/2*(1-1/H)
  need(1-g-e>0,'positive coefficient');beta.append(1-g);epsilon.append(e)
 def slope(a,b):
  a,b=I(a),I(b);u=-iv.pi*iv.ln(a)/(2*w);need(u>0 and u*u<6,'slope sine');B=iv.pi/(2*w)*(1+(1-b)/2)*(1-u*u/6);v=iv.sqrt(2)*B*(1-a)
  return lo(2*iv.sqrt(2)*B/(v+iv.sqrt(v*v+P)))
 part=[R+(1-R)*Q(j,5000) for j in range(5001)];slopes=[slope(a,b) for a,b in zip(part,part[1:])]
 coeff=[-slopes[0]]+[x-y for x,y in zip(slopes,slopes[1:])]+[slopes[-1]]
 points=[I(t) for t in part];ratios=[I(t/R) for t in part];pp=list(ratios);tr=[I(t/R) for t in nd];tp=[I(1) for t in nd];min_gap=None;min_k=None;rr=I(R);beg=time.monotonic()
 for k in range(1,K2):
  pp=[x*y for x,y in zip(pp,ratios)];tp=[x*y for x,y in zip(tp,tr)]
  integ=sum(cc*vv*(1/I(k+1)-point/(k+2)) for cc,vv,point in zip(coeff,pp,points))
  gap=1+(k+1)*integ-(k+1)/rr*sum(I(ww)*bb*power for ww,bb,power in zip(wt,beta,tp))
  if k==1:gap+=(k+1)/rr*sum(I(ww)*ee*power for ww,ee,power in zip(wt,epsilon,tp))
  need(gap>0,'weighted '+str(k))
  if min_gap is None or gap.a<min_gap.a:min_gap=gap;min_k=k
  if k%100==0:print('weighted',k,'seconds',time.monotonic()-beg,flush=True)
 a=Q(d['second_tail_a']);b=Q(d['second_tail_b']);need(R<=a<b<1,'second interval');sg=slope(a,b);gap=sg*I(1-b)*I(b-a)-sum(I(ww)*I(t/a)**K2 for ww,t in zip(wt,nd));need(gap>0,'second infinite')
 return dict(status='PASS',verification='separately written (same agent)',backend='integer ordinary moments; mpmath.iv 5000-cell tail',sha256=hashlib.sha256(raw).hexdigest(),ordinary_through=K1-1,weighted_through=K2-1,weighted_min_relative=str(min_gap),weighted_min_k=min_k,first_infinite_from=K1,second_infinite_from=K2,second_infinite_gap_divided_by_a_power=str(gap))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['scalar','measure']);p.add_argument('artifact');p.add_argument('--output',required=True);a=p.parse_args();start=time.monotonic();out=(scalar if a.mode=='scalar' else measure)(a.artifact);out['seconds']=time.monotonic()-start;Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
