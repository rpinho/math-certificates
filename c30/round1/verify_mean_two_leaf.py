"""Arb first-moment certificate, separately written (same agent).

u is the strip-length mark and w is the critical curve parameter. Jets retain
1,u,w,u*w exactly under truncated formal algebra. No numerical differentiation.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
from flint import arb,ctx


def a(q):
    q=F(q)
    return arb(q.numerator)/q.denominator


class Jet:
    def __init__(self,x,u=0,w=0,uw=0):
        self.c=tuple(t if isinstance(t,arb) else arb(t) for t in [x,u,w,uw])
    @staticmethod
    def j(x):return x if isinstance(x,Jet) else Jet(x)
    def __add__(self,o):
        o=self.j(o);return Jet(*(x+y for x,y in zip(self.c,o.c)))
    __radd__=__add__
    def __neg__(self):return Jet(*(-x for x in self.c))
    def __sub__(self,o):return self+-self.j(o)
    def __rsub__(self,o):return self.j(o)+-self
    def __mul__(self,o):
        o=self.j(o);x,u,w,m=self.c;y,v,z,n=o.c
        return Jet(x*y,u*y+x*v,w*y+x*z,m*y+u*z+w*v+x*n)
    __rmul__=__mul__
    def inv(self):
        x,u,w,m=self.c
        assert x>0 or x<0, 'uncertified denominator'
        return Jet(1/x,-u/x**2,-w/x**2,2*u*w/x**3-m/x**2)
    def __truediv__(self,o):return self*self.j(o).inv()
    def __rtruediv__(self,o):return self.j(o)*self.inv()
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        out=Jet(1)
        for _ in range(n):out=out*self
        return out
    def sqrt(self):
        x,u,w,m=self.c
        assert x>0, 'uncertified analytic square-root branch'
        y=x.sqrt()
        return Jet(y,u/(2*y),w/(2*y),m/(2*y)-u*w/(4*y**3))


Z=a('4/27');D0=a('27/16')
def A(v):
    v=Jet.j(v)
    p2=Z*v-Z**2*(1+v)-Z**2*v*(1+v)
    p1=-v+Z*(1+2*v+v**2)+Z**2*(1+v)*D0
    p0=v-Z*(1+v)*D0
    disc=p1**2-4*p2*p0
    assert disc.c[0]>0
    return -2*p0/(p1+disc.sqrt())
def g(x):return Z**2*x**2/(1-Z*x)
def ka(v):return 1-3*Z-Z*v-Z/v
def roots(u):
    b=1-Z*(2+u)
    d=(b**2-4*Z**2).sqrt()
    return 2*Z/(b+d),(b+d)/(2*Z)
def FF(u,v):
    r,rp=roots(u)
    return 1/(Z*(1+r)*(rp-v))
def RR(x,y):return Z**2*(x+y-Z*x*y)/((1-Z*x)*(1-Z*y))
def kernel(u,v):return ka(v)-RR(A(v),FF(u,v))


def verify(c):
    global Z,D0
    ctx.prec=384
    Z=a('4/27');D0=a('27/16')
    assert c['bar_sha256']==hashlib.sha256(Path('BAR.json').read_bytes()).hexdigest()
    assert 3*F(4,27)*F(2187,16)*F(4,9)==27
    assert F(c['markov_threshold'])==F(1,10)
    lo,hi=map(F,[c['root_lower'],c['root_upper']])
    assert F(1,3)<lo<hi<F(2,5)
    r=(a(lo)+a(hi))/2+arb(0,(a(hi)-a(lo))/2)
    assert kernel(Jet(0),Jet(a(lo))).c[0]<0
    assert kernel(Jet(0),Jet(a(hi))).c[0]>0
    kv=kernel(Jet(0,1),Jet(r,0,1))
    assert kv.c[2]>0
    ru=-kv.c[1]/kv.c[2]
    root=Jet(r,ru)
    u=Jet(0,1)
    # Corrected Rouché normalization proves selection of the formal root.
    vmax=Z*(1+16*Z)
    assert vmax<a('1/2')
    CA=A(Jet(vmax)).c[0]
    CF=FF(Jet(1),Jet(vmax)).c[0]
    assert Z*CA<1 and Z*CF<1
    CR=(CA+CF-Z*CA*CF)/((1-Z*CA)*(1-Z*CF))
    rouche=(1+16*Z)*(3+Z*(1+16*Z)+CR*Z)
    assert rouche<16
    assert abs(r-Z)<16*Z**2
    v1,_=roots(u)
    s0=v1*g(A(v1))/(Z*(1+v1))
    t0=root*g(FF(u,root))/(Z*(1+root))
    W=Jet(a('1/2'),0,1)
    aw=(1+W)**2
    f=FF(u,W)
    S=(g(aw)-Z*(1+W)*s0/W)/(ka(W)+Z-u*Z)
    R=RR(aw,f)
    T=(g(f)-Z*(1+W)*t0/W)/(ka(W)-R)
    V=S*Z**2/((1-Z*aw)**2*(1-Z*f))
    P=W*(S*R+T*V)/(Z*(1+W))
    mu1=4*P.c[2]/27
    mu2=4*P.c[3]/27
    assert mu2>0 and mu2<a(c['markov_threshold']), str(mu2)
    return {'status':'PASS','scope':'local algebraic first-moment calculation; family proof in FIRST_MOMENT_PROOF.md must also hold','verifier':'separately written (same agent)','root':str(r),'root_du':str(ru),'root_derivative_v':str(kv.c[2]),'rouche_lhs':str(rouche),'one_leaf_density_diagnostic':str(mu1),'two_leaf_density':str(mu2),'markov_threshold':c['markov_threshold'],'mixed_derivative_P':str(P.c[3])}


if __name__=='__main__':
    c=json.loads(Path('artifacts/mean_two_leaf_certificate.json').read_text())
    out=verify(c)
    Path('artifacts/mean_two_leaf_verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
