"""Checker-only parabolic domain lemma and coefficient-box exclusions."""
from flint import arb
from verify_c57c_center6 import require,rational

def lemma():
 # For delta<=16/81 choose r=(2/5)*sqrt(delta)<=8/45<1/5.
 # The Bloch inequality of Section 6a then gives v<3*sqrt(delta)/2.
 r=arb(1)/5;C=arb(25)/9*(arb(5)/4)**8
 bracket=1/(1-r*r)+5+6*r+14*r*r+24*r**3+C*r**4/(1-5*r/4)
 require(1+arb(4)/25*bracket<arb(12)/5,'parabolic coefficient cap lemma')
 require(arb(8)/45<r,'lemma radius bound')

def ranges(cells,point=False):
 x=[]
 for n,d in cells[:3]:
  mid=arb(2*n+1)/2**(d+1);x.append(mid if point else arb(mid,arb(1)/2**(d+1)))
 return (1-x[0]**2)/3,arb(3)/2*x[0]*x[2]

def excluded(cells,point=False):
 x=[]
 for n,d in cells[:3]:
  mid=arb(2*n+1)/2**(d+1);x.append(mid if point else arb(mid,arb(1)/2**(d+1)))
 # A necessary condition is x1^2+(3*u*x2/(2*b))^2<=1.
 # All variables are nonnegative. Use exact endpoints to avoid losing
 # monotonicity to centered interval dependency.
 if point:
  u,re,im=x;s=(1-u*u)/3;b=arb(2)/3-s*s/2;return re*re+(arb(3)/2*u*im/b)**2-1
 lo=[arb(n)/2**d for n,d in cells[:3]];u_hi=arb(cells[0][0]+1)/2**cells[0][1]
 b_upper=arb(2)/3-((1-u_hi*u_hi)/3)**2/2
 return lo[1]**2+(arb(3)/2*lo[0]*lo[2]/b_upper)**2-1
