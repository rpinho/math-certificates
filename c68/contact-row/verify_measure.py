"""Separately written (same agent) full frozen-artifact verifier.

Derived from the written norm and moment inequalities, with a global cubic
tail envelope. Imports neither search nor baseline acceptance code.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse,hashlib,json,math,time
from flint import arb,fmpq,ctx
from verify_row import Rejection,require,verify as verify_cover

def A(x):
 x=Q(x);return arb(fmpq(x.numerator,x.denominator))
def rational(x,code):
 require(type(x)==str and 0<len(x)<300,code)
 try:return Q(x)
 except (ValueError,ZeroDivisionError):raise Rejection(code)
def slope(aa,bb,w,P):
 a,b=A(aa),A(bb);u=-arb.pi()*a.log()/(2*w)
 require(u>0 and 6-u*u>0,'TAIL2_SINE_REMAINDER')
 B=arb.pi()/(2*w)*(1+(1-b)/2)*(1-u*u/6);v=arb(2).sqrt()*B*(1-a)
 return arb((2*arb(2).sqrt()*B/(v+(v*v+P).sqrt())).lower())

def verify(path):
 raw=Path(path).read_bytes();d=json.loads(raw)
 require(d.get('model')=='contact_row_v1','MEASURE_MODEL')
 c=rational(d.get('c'),'MEASURE_C');R=rational(d.get('R'),'MEASURE_R')
 require(c==Q(447,1000),'TARGET_RADIUS')
 require(rational(d.get('kappa'),'MEASURE_KAPPA')==Q(3,25),'MEASURE_KAPPA')
 require(rational(d.get('zeta'),'MEASURE_ZETA')==Q(23,200),'MEASURE_ZETA')
 require(type(d.get('nodes'))==list and type(d.get('weights'))==list,'MEASURE_LISTS')
 nodes=[rational(t,'MEASURE_NODE_RATIONAL') for t in d['nodes']];weights=[rational(t,'MEASURE_WEIGHT_RATIONAL') for t in d['weights']]
 require(2<=len(nodes)<=100 and len(nodes)==len(weights),'MEASURE_LENGTH')
 require(c*c<R<1 and R>=c,'MEASURE_R')
 require(nodes[0]==c*c and nodes[-1]==R,'MEASURE_ENDPOINTS')
 require(all(t<s for t,s in zip(nodes,nodes[1:])),'MEASURE_ORDER')
 require(all(w>0 for w in weights),'MEASURE_WEIGHT')
 require(sum(weights)==R,'MEASURE_MASS')
 require(d.get('tail_envelope')=='cubic_v1','TAIL_ENVELOPE')
 K1,K2=d.get('first_tail_k'),d.get('second_tail_k')
 require(type(K1)==int and type(K2)==int and 2<=K1<=100000 and 2<=K2<=100000,'TAIL_CUTOFF_TYPE')
 require(weights[-1]*(K1+1)>=R,'TAIL1_START')
 ta=rational(d.get('second_tail_a'),'TAIL2_INTERVAL');tb=rational(d.get('second_tail_b'),'TAIL2_INTERVAL')
 require(R<=ta<tb<1,'TAIL2_INTERVAL')
 require(d.get('cover_file')=='row-cover.json','COVER_FILENAME')
 cover=Path(path).parent/d['cover_file'];require(cover.is_file(),'COVER_MISSING')
 require(hashlib.sha256(cover.read_bytes()).hexdigest()==d.get('cover_sha256'),'COVER_HASH')
 C=A(c);RR=A(R);z=A('23/200');w=-C.log();a=arb.pi()**2/w;q=(-a).exp();P=(1+q)**2/(8*q);kap=A('3/25')
 margins=[1/arb(3)-1/(a/2).cosh()**2,2*(1-8*kap)*P-16*(a/4).sinh()**2,(a/8).tanh()**2-(1+8*kap)*arb.pi()**2/64,(1-4*kap)/2-1/(a/8).cosh()**2,P-6]
 for i,gap in enumerate(margins):require(gap>0,'ANALYTIC_HYPOTHESIS_'+str(i))
 T=list(map(A,nodes));W=list(map(A,weights));beta=[];eps=[]
 for j,t in enumerate(T):
  if j==0:g=e=arb(0)
  else:
   sigma=(arb.pi()*t.log()/(2*w)).sin()**2;h=(1+P/(2*sigma)).sqrt();g=2/(1+h);e=z*(h*h-1)/(h*(1+h)**2)
  require(1-g-e>0,'COEFFICIENT_WEIGHT');beta.append(1-g);eps.append(e)
 # Cubic lower envelope for every t in [R,1].
 p=arb.pi()/(2*w);B=(2/P).sqrt();K=2*B*p
 require(-p*RR.log()<arb.pi(),'TAIL_ANGLE_RANGE')
 linear=K;quadratic=K/2-4*p*p/(P*RR*RR);cubic=-K*p*p/(6*RR**3)
 def J(k,j):
  return sum(A((-1)**l*math.comb(j,l))*(1-RR**(k+l+1))/(k+l+1) for l in range(j+1))
 def integral(k):return linear*J(k,1)+quadratic*J(k,2)+cubic*J(k,3)
 ordinary_min=weighted_min=None;ordinary_k=weighted_k=None;k1=None;old_upper=None
 powers=[arb(1) for _ in T];rp=RR
 for k in range(1,max(K1,K2)):
  powers=[x*t for x,t in zip(powers,T)];rp*=RR;base=rp/(k+1)
  if k<K1:
   gap=sum(ww*tt for ww,tt in zip(W,powers))-base
   require(gap>0,'ORDINARY_MOMENT_'+str(k));rel=gap/base
   if ordinary_min is None or rel<ordinary_min:ordinary_min=rel;ordinary_k=k
  if k<K2:
   atomic=sum(ww*bb*tt for ww,bb,tt in zip(W,beta,powers));gap=base+integral(k)-atomic
   if k==1:
    correction=sum(ww*ee*tt for ww,ee,tt in zip(W,eps,powers));gap+=correction;k1=gap
    # An upper bound for the FULL old .095 criterion on this measure.
    upper_slope=arb(2).sqrt()*arb.pi()/(w*RR*P.sqrt());old_atomic=correction*A('19/23')
    old_upper=base-atomic+old_atomic+A('419/400')*upper_slope*J(1,1)
   require(gap>0,'WEIGHTED_MOMENT_'+str(k));rel=gap/base
   if weighted_min is None or rel<weighted_min:weighted_min=rel;weighted_k=k
 slope2=slope(ta,tb,w,P)
 tail_gap=slope2*A(1-tb)*A(tb-ta)*A(ta)**K2-sum(ww*tt**K2 for ww,tt in zip(W,T))
 require(tail_gap>0,'TAIL2_GAP')
 scalar=verify_cover(cover)
 return dict(status='PASS',verification='separately written (same agent)',candidate=True,unrefereed=True,c=str(c),zeta='23/200',bits=ctx.prec,certificate_sha256=hashlib.sha256(raw).hexdigest(),ordinary_finite_through=K1-1,weighted_finite_through=K2-1,ordinary_min_relative=str(ordinary_min),ordinary_min_k=ordinary_k,weighted_min_relative=str(weighted_min),weighted_min_k=weighted_k,k1_sufficient_gap=str(k1),old_0095_full_k1_margin_upper=str(old_upper),first_infinite_from=K1,first_tail_exact_gap=str(weights[-1]*(K1+1)-R),second_infinite_from=K2,second_infinite_gap=str(tail_gap),tail_cubic_coefficients=list(map(str,[linear,quadratic,cubic])),analytic_margins=list(map(str,margins)),scalar=scalar)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('certificate');p.add_argument('--bits',type=int,default=320);p.add_argument('--output',default='logs/verification-final.json');a=p.parse_args();ctx.prec=a.bits;t=time.monotonic()
 try:out=verify(a.certificate);out['seconds']=time.monotonic()-t
 except Rejection as e:out={'status':'REJECT','code':str(e)}
 Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
 if out['status']!='PASS':raise SystemExit(1)
