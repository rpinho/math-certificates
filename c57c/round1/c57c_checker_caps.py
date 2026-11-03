"""Checker-only local coefficient caps for a Taylor remainder.
The independently written enclosure uses scalar interval ranges of s, |a|
and the remaining area budget, then the explicit h7..h13 identities.
"""
from flint import arb

def local_caps(cells,parabolic=False):
 if parabolic:return parabolic_caps(cells)
 ss,sd=cells[0];rr,rd=cells[1]
 s=arb(arb(2*ss+1)/(3*2**(sd+1)),arb(1)/(3*2**(sd+1)))
 radius=arb(arb(2*rr+1)/2**(rd+1),arb(1)/2**(rd+1))
 # s and radius are nonnegative on the exact dyadic box. Work with
 # endpoints so squaring a centered interval never loses that information.
 sl=max(arb(0),s.lower());su=s.upper();rl=max(arb(0),radius.lower());ru=radius.upper()
 low_a=(arb(2)/3-su**2/2)*rl;high_a=(arb(2)/3-sl**2/2)*ru
 remaining=(1-arb(3)/4*sl**2-arb(5)/4*low_a**2).upper()
 A5=(arb(3)/4*su**2+2*(remaining/7).sqrt()).upper()
 A6=(arb(3)/2*su*high_a+arb(2)/3*remaining.sqrt()).upper()
 A7=(arb(3)/2*su*A5+arb(3)/4*high_a**2+arb(5)/8*su**3+2*(remaining/11).sqrt()).upper()
 A8=(arb(3)/2*su*A6+arb(3)/2*high_a*A5+arb(15)/8*su**2*high_a+2*(remaining/13).sqrt()).upper()
 return [arb(1),min(arb(1),A5),min(arb(1),A6),min(arb(2),A7),min(arb(3),A8)]


def parabolic_caps(cells):
 ends=[(arb(n)/2**d,arb(n+1)/2**d)for n,d in cells[:3]]
 u0,u1=ends[0];re0,re1=ends[1];im0,im1=ends[2]
 sl=(1-u1*u1)/3;su=(1-u0*u0)/3
 alo2=((arb(2)/3-su*su/2)*re0)**2+(arb(3)/2*u0*im0)**2
 ahi2=((arb(2)/3-sl*sl/2)*re1)**2+(arb(3)/2*u1*im1)**2;A=ahi2.sqrt().upper()
 R=max(arb(0),(1-arb(3)/4*sl*sl-arb(5)/4*alo2).upper())
 b=(2*(R/7).sqrt()+arb(3)/4*su*su).upper()
 c=(arb(2)/3*R.sqrt()+arb(3)/2*su*A).upper()
 d=(2*(R/11).sqrt()+arb(3)/2*su*b+arb(3)/4*ahi2+arb(5)/8*su**3).upper()
 e=(2*(R/13).sqrt()+arb(3)/2*su*c+arb(3)/2*A*b+arb(15)/8*su*su*A).upper()
 return [arb(1),min(arb(1),b),min(arb(1),c),min(arb(2),d),min(arb(3),e)]
