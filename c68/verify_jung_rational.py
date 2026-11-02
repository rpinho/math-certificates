"""Independently implemented integer interval proof for GEOMETRIC_LEMMA.md.
Standard library only. Machin's identity for pi; explicit series remainders
for logarithms, sine and exponential; isqrt for radicals. No other checker
or search code is imported. Every arithmetic operation rounds outward.
"""
import json,argparse,hashlib,time
from pathlib import Path
from fractions import Fraction
from math import isqrt
if not __debug__:raise SystemExit('Refusing -O/-OO: assertions are part of the proof')
Q=1<<200
def ceiling(n,d):
 assert d>0
 return -((-n)//d)
class I:
 def __init__(self,x=0,hi=None):
  if hi is not None:self.lo=int(x);self.hi=int(hi)
  elif isinstance(x,I):self.lo=x.lo;self.hi=x.hi
  else:
   v=Fraction(x);self.lo=v.numerator*Q//v.denominator;self.hi=ceiling(v.numerator*Q,v.denominator)
  assert self.lo<=self.hi
 def __add__(a,b):
  b=I(b);return I(a.lo+b.lo,a.hi+b.hi)
 __radd__=__add__
 def __neg__(a):return I(-a.hi,-a.lo)
 def __sub__(a,b):return a+-I(b)
 def __rsub__(a,b):return I(b)+-a
 def __mul__(a,b):
  b=I(b);p=[a.lo*b.lo,a.lo*b.hi,a.hi*b.lo,a.hi*b.hi];return I(min(p)//Q,ceiling(max(p),Q))
 __rmul__=__mul__
 def __truediv__(a,b):
  b=I(b);assert b.lo>0
  p=[(n*Q,d) for n in [a.lo,a.hi] for d in [b.lo,b.hi]]
  return I(min(n//d for n,d in p),max(ceiling(n,d) for n,d in p))
 def __rtruediv__(a,b):return I(b)/a
 def __pow__(a,k):
  assert isinstance(k,int) and k>=0
  r=I(1)
  while k:
   if k&1:r=r*a
   a=a*a;k//=2
  return r
 def sqrt(a):
  assert a.lo>=0
  l=isqrt(a.lo*Q);u=isqrt(a.hi*Q)
  if u*u<a.hi*Q:u+=1
  return I(l,u)
 def bounds(a):return [str(Fraction(a.lo,Q)),str(Fraction(a.hi,Q))]

def minus_log(x):
 # -log x=2*atanh((1-x)/(1+x)), 0<x<=1. Every term is positive.
 x=I(x);assert 0<x.lo<=x.hi<=Q;u=(1-x)/(1+x);assert u.hi*4<3*Q;u2=u*u;term=u;acc=I(0);N=220
 for j in range(N):acc+=term/(2*j+1);term*=u2
 # The remaining denominators are at least 2N+1; geometric summation.
 remainder=2*term/((2*N+1)*(1-u2));return 2*acc+I(0,remainder.hi)
def atan_small(x):
 # Alternating arctangent series; remainder bounded by the next term.
 x=I(x);assert 0<=x.lo<=x.hi<Q//4;xx=x*x;term=x;acc=I(0);N=100
 for j in range(N):
  piece=term/(2*j+1);acc=acc+piece if j%2==0 else acc-piece;term*=xx
 rem=term/(2*N+1);return acc+I(-rem.hi,rem.hi)
def pi_interval():return 16*atan_small(Fraction(1,5))-4*atan_small(Fraction(1,239))
def exp_positive(x):
 # Taylor at x/16, then four squarings. Positive tail has geometric bound.
 x=I(x);assert 0<=x.lo<=x.hi<16*Q;u=x/16;term=I(1);acc=I(1);N=100
 for j in range(1,N+1):term=term*u/j;acc+=term
 nxt=term*u/(N+1);remainder=nxt/(1-u/(N+2));v=acc+I(0,remainder.hi)
 for _ in range(4):v=v*v
 return v
def sin_interval(x):
 # Taylor polynomial through degree 2N-1, with Lagrange remainder.
 x=I(x);assert 0<=x.lo<=x.hi<4*Q;xx=x*x;term=x;acc=I(0);N=90
 for j in range(N):
  acc=acc+term if j%2==0 else acc-term
  term=term*xx/((2*j+2)*(2*j+3))
 return acc+I(-term.hi,term.hi)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('certificate');ap.add_argument('--out');a=ap.parse_args();start=time.monotonic();p=Path(a.certificate);d=json.loads(p.read_text());F=Fraction
 assert d['analytic_model']=='two_covering_zeros_hyperbolic_jung'
 c,R,ell=map(F,[d['c'],d['R'],d['linear_slope']]);nodes=list(map(F,d['nodes']));weights=list(map(F,d['weights']))
 assert 0<c<1 and c*c<R<1 and ell>0;assert len(nodes)==len(weights)>=2 and nodes[0]==c*c and nodes[-1]==R;assert all(nodes[j]<nodes[j+1] for j in range(len(nodes)-1)) and all(x>0 for x in weights);assert sum(weights)==R
 pi=pi_interval();assert 3*Q<pi.lo and pi.hi<4*Q;w=minus_log(c);E=exp_positive(pi*pi/(2*w));X=(E-1/E)**2/4;U=pi*minus_log(R)/(2*w);assert U.lo>0 and (U*U).hi<6*Q
 aa=(pi/(2*w))**2*(1-U*U/6)**2/X;delta=I(1-R);z=aa*delta*delta
 # Bound the numerator below and denominator above independently;
 # hence no dependency correlation is required for this enclosure.
 numerator=2*(6*aa).sqrt();denominator=(3*z*(2+z)).sqrt()+(4+6*z+3*z*z).sqrt();slope=numerator/denominator;assert slope.lo>I(ell).hi,('linear envelope',slope.bounds())
 T=list(map(I,nodes));W=list(map(I,weights));B=[I(1)]
 for node in nodes[1:]:
  angle=pi*minus_log(node)/(2*w);sin=sin_interval(angle);assert sin.lo>0
  y=sin*sin/X;hh=3*y*(2+y);root=hh.sqrt();g=2*root/(root+(hh+4).sqrt());assert 0<g.lo<=g.hi<Q;B.append(1-g)
 kA=max(1,int(R//weights[-1]));assert weights[-1]*(kA+1)>=R;kB=int(d['second_tail_k']);assert kB>=1;t0,t1=map(F,[d['second_tail_t0'],d['second_tail_t1']]);assert R<t0<t1<1
 tail=I(ell*(1-t1)*(t1-t0))*I(t0)**kB;negative=sum(v*t**kB for v,t in zip(W,T));assert tail.lo>negative.hi,('second infinite tail',(tail-negative).bounds())
 # Positive power recurrences and outward rounding for every moment.
 rp=I(R);powers=[I(1) for t in T];minsA=None;minsB=None;argA=argB=0
 for k in range(1,max(kA,kB)):
  rp*=I(R);powers=[power*t for power,t in zip(powers,T)]
  if k<kA:
   gap=(k+1)*sum(weight*power for weight,power in zip(W,powers))-rp;assert gap.lo>0,('first moment',k,gap.bounds());relative=F(gap.lo,rp.hi)
   if minsA is None or relative<minsA:minsA=relative;argA=k
  if k<kB:
   # Independently simplify the integral after multiplying by k+1.
   integral_times_k1=I(ell)*(I(F(1,k+2))-rp+rp*R*F(k+1,k+2))
   gap=integral_times_k1+rp-(k+1)*sum(v*b*power for v,b,power in zip(W,B,powers));assert gap.lo>0,('second moment',k,gap.bounds());relative=F(gap.lo,rp.hi)
   if minsB is None or relative<minsB:minsB=relative;argB=k
 out={'status':'PASS','checker':'independent standard-library integer intervals, elementary series','certificate_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'c':str(c),'atoms':len(nodes),'bits':200,'pi_interval':pi.bounds(),'linear_envelope_slope_lower':str(F(slope.lo,Q)),'first_finite_through':kA-1,'first_tail_from':kA,'second_finite_through':kB-1,'second_tail_from':kB,'first_min_relative_lower':str(minsA),'first_min_k':argA,'second_min_relative_lower':str(minsB),'second_min_k':argB,'second_tail_gap_lower':str(F(tail.lo-negative.hi,Q)),'seconds':time.monotonic()-start}
 if a.out:Path(a.out).write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2),flush=True)
if __name__=='__main__':main()
