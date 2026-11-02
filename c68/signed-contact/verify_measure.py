"""Independent certificate verification from the written moment inequalities.
No optimizer, proposal, baseline-checker, or floating arithmetic imports.
"""
from pathlib import Path
from fractions import Fraction as Q
from flint import arb,fmpq,ctx
import json,argparse,time,hashlib
from verify_signed_cover import verify as verify_scalar
if not __debug__:raise SystemExit('Run without -O: structural assertions are required')

def I(q):
 q=Q(q);return arb(fmpq(q.numerator,q.denominator))
def positive(v,why):
 if not v>0:raise ArithmeticError((why,str(v)))
def slope(a,b,w,P):
 a,b=I(a),I(b);u=-arb.pi()*a.log()/(2*w)
 positive(u,'positive angle');positive(6-u*u,'sine remainder')
 B=arb.pi()/(2*w)*(1+(1-b)/2)*(1-u*u/6)
 positive(B,'sine slope');z=arb(2).sqrt()*B*(1-a)
 return arb((2*arb(2).sqrt()*B/(z+(z*z+P).sqrt())).lower())
def run(path,scalar=True):
 raw=Path(path).read_bytes();d=json.loads(raw)
 assert d['model']=='signed_contact_v4' and Q(d['zeta'])==Q(19,200) and Q(d['kappa'])==Q(3,25)
 c,R=Q(d['c']),Q(d['R']);nodes=list(map(Q,d['nodes']));weights=list(map(Q,d['weights']));p=list(map(Q,d['tail_partition']))
 assert 0<c<1 and c*c<R<1 and c<=R
 assert len(nodes)==len(weights)>=2 and nodes[0]==c*c and nodes[-1]==R
 assert all(x>0 for x in weights) and sum(weights)==R
 assert all(a<b for a,b in zip(nodes,nodes[1:]))
 assert 2<=len(p)<=10000 and p[0]==R and p[-1]==1 and all(a<b for a,b in zip(p,p[1:]))
 K1,K2=d['first_tail_k'],d['second_tail_k'];assert type(K1)==type(K2)==int and 2<=K1<=100000 and 2<=K2<=100000
 assert weights[-1]*(K1+1)>=R
 w=-I(c).log();A=arb.pi()**2/w;q=(-A).exp();P=(1+q)**2/(8*q);kap=I('3/25');zeta=I('19/200')
 margins=[1/arb(3)-1/(A/2).cosh()**2,2*(1-8*kap)*P-16*(A/4).sinh()**2,(A/8).tanh()**2-(1+8*kap)*arb.pi()**2/64,(1-4*kap)/2-1/(A/8).cosh()**2,P-6]
 for j,v in enumerate(margins):positive(v,('analytic hypothesis',j))
 T=list(map(I,nodes));W=list(map(I,weights));beta=[];e=[];eold=[]
 for t,node in zip(T,nodes):
  if node==c*c:g=eps=old=arb(0)
  else:
   s=(arb.pi()*t.log()/(2*w)).sin()**2;H=(1+P/(2*s)).sqrt();g=2/(1+H)
   eps=zeta*(H*H-1)/(H*(1+H)**2);old=I('7/100')*(H*H-1)/(H*(1+H)**2)
  positive(1-g-eps,'nonnegative corrected beta');beta.append(1-g);e.append(eps);eold.append(old)
 slopes=[slope(a,b,w,P) for a,b in zip(p,p[1:])]
 # Telescoping integration of the piecewise lower envelope, separately derived.
 v=list(map(I,p));coeff=[-slopes[0]]+[a-b for a,b in zip(slopes,slopes[1:])]+[slopes[-1]]
 vp=[x for x in v];tp=[arb(1) for t in T];rp=I(R)
 amin=bmin=None;ak=bk=None;oldgap=newgap=old_upper=None
 for k in range(1,max(K1,K2)):
  tp=[a*b for a,b in zip(tp,T)];rp*=I(R)
  vp=[a*b for a,b in zip(vp,v)]
  basic=rp/(k+1)
  if k<K1:
   gap=sum(a*b for a,b in zip(W,tp))-basic;positive(gap,('ordinary',k));rel=gap/basic
   if amin is None or rel<amin:amin=rel;ak=k
  if k<K2:
   integ=sum(cc*power*(1/arb(k+1)-point/(k+2)) for cc,power,point in zip(coeff,vp,v))
   atomic=sum(a*b*power for a,b,power in zip(W,beta,tp))
   gap=basic+integ-atomic
   if k==1:
    oldgap=gap+sum(a*b*power for a,b,power in zip(W,eold,tp))
    g_upper_slope=arb(2).sqrt()*arb.pi()/(w*I(R)*P.sqrt())
    J=(1-I(R)**2)/2-(1-I(R)**3)/3
    # Include even the OLD continuous epsilon contribution: epsilon_old<=.035*g.
    old_upper=basic+I('207/200')*g_upper_slope*J-atomic+sum(a*b*power for a,b,power in zip(W,eold,tp))
    positive(-old_upper,'same measure fails previous 7/100 criterion')
    gap+=sum(a*b*power for a,b,power in zip(W,e,tp));newgap=gap
   positive(gap,('weighted',k));rel=gap/basic
   if bmin is None or rel<bmin:bmin=rel;bk=k
 ta,tb=Q(d['second_tail_a']),Q(d['second_tail_b']);assert R<=ta<tb<1
 st=slope(ta,tb,w,P);tailgap=st*(1-I(tb))*I(tb-ta)*I(ta)**K2-sum(a*b**K2 for a,b in zip(W,T));positive(tailgap,'second infinite tail')
 out=dict(status='PASS',c=str(c),zeta=str(Q(d['zeta'])),certificate_sha256=hashlib.sha256(raw).hexdigest(),bits=ctx.prec,ordinary_finite_through=K1-1,weighted_finite_through=K2-1,first_infinite_from=K1,second_infinite_from=K2,ordinary_min_relative=str(amin),ordinary_min_k=ak,weighted_min_relative=str(bmin),weighted_min_k=bk,second_infinite_gap=str(tailgap),k1_new_gap=str(newgap),k1_old_007_gap_lower=str(oldgap),k1_old_007_gap_upper=str(old_upper),analytic_margins=list(map(str,margins)))
 if scalar:out['scalar']=verify_scalar(Path(path).parent/'signed-cover.json')
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('certificate');p.add_argument('--output',default='verification.json');p.add_argument('--bits',type=int,default=320);a=p.parse_args();ctx.prec=a.bits;start=time.monotonic();out=run(a.certificate);out['seconds']=time.monotonic()-start;print(json.dumps(out,indent=2));Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
