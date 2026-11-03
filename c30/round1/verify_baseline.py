"""Separately written (same agent) Arb verifier of the frozen v3 arithmetic.

This verifies the numerical implication of Norton v3, not the imported BBEP
enumeration/concentration theorems and not a new lower bound. No float input.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from flint import arb, ctx


class Dual:
    def __init__(self, x, d=0):
        self.x = x if isinstance(x, arb) else arb(x)
        self.d = d if isinstance(d, arb) else arb(d)
    @staticmethod
    def coerce(x):
        return x if isinstance(x, Dual) else Dual(x)
    def __add__(self, other):
        o = self.coerce(other)
        return Dual(self.x+o.x,self.d+o.d)
    __radd__ = __add__
    def __neg__(self):
        return Dual(-self.x,-self.d)
    def __sub__(self, other):
        return self+-self.coerce(other)
    def __rsub__(self, other):
        return self.coerce(other)+-self
    def __mul__(self,other):
        o = self.coerce(other)
        return Dual(self.x*o.x,self.x*o.d+self.d*o.x)
    __rmul__ = __mul__
    def __truediv__(self, other):
        o=self.coerce(other)
        return Dual(self.x/o.x,(self.d*o.x-self.x*o.d)/(o.x*o.x))
    def __rtruediv__(self,other):
        return self.coerce(other)/self
    def __pow__(self, n):
        assert isinstance(n,int) and n >= 0
        if n==0:return Dual(1)
        return Dual(self.x**n,n*self.x**(n-1)*self.d)


def ball(q):
    q=Fraction(q)
    return arb(q.numerator)/q.denominator


def functions(z, q):
    s=(1-4*z).sqrt()
    q=Dual(q,1)
    D=2-q+q*s
    h0=2/D
    h2=(q**2*(3*s**5-9*s**4+10*s**3-6*s**2+3*s-1)+2*q*(9*s**4-16*s**3+6*s**2+1)+32*s**3)/(4*s**3*D**3)
    h3=(q**3*(5*s**8-20*s**7+32*s**6-28*s**5+18*s**4-12*s**3+8*s**2-4*s+1)+4*q**2*(10*s**7-29*s**6+30*s**5-15*s**4+6*s**3-3*s**2+2*s-1)+4*q*(29*s**6-48*s**5+15*s**4+3*s**2+1)+128*s**5)/(8*s**5*D**4)
    return {0:h0,2:h2,3:h3}


def verify(path):
    c=json.loads(Path(path).read_text())
    root=Path(__file__).resolve().parent
    assert hashlib.sha256((root/'BAR.json').read_bytes()).hexdigest()==c['bar_sha256'], 'changed frozen bar'
    # Source snapshots are omitted; this checks provenance linkage, not source bytes.
    bar=json.loads((root/'BAR.json').read_text())
    assert bar['source_sha256']['sources/norton-v3.html']==c['source_sha256'], 'changed source digest'
    ctx.prec=256
    z,k,alpha,beta,q0,q1,q2,lam=[Fraction(c[n]) for n in ['z','kappa','alpha','beta','q0','q1','q2','lambda']]
    assert 0 < z < Fraction(1,4)
    assert k > 0
    assert Fraction(11,20)<=alpha<Fraction(5,9)
    assert Fraction(7,40)<=beta<Fraction(5,27)
    f={0:beta,2:3-4*alpha-3*beta,3:3*alpha+2*beta-2}
    assert all(x>0 for x in f.values())
    assert c['profile']=={str(j):str(x) for j,x in f.items()}, 'wrong profile'
    assert 0 < q1 < q0 < q2
    assert lam > 0 and z*lam < 1, 'claimed bound exceeds certified reciprocal'
    Z,K,Q0,Q1,Q2=map(ball,[z,k,q0,q1,q2])
    Q=(1-(1-4*Z).sqrt())/2
    assert Q2*Q < 1, 'bracket beyond radius'
    def bracket(q):
        h=functions(Z,q)
        assert all(x.x>0 for x in h.values())
        B=-K*q.log()+sum(ball(f[j])*x.x.log() for j,x in h.items())
        slope=-K+sum(ball(f[j])*q*x.d/x.x for j,x in h.items())
        return B,slope
    _,d1=bracket(Q1)
    _,d2=bracket(Q2)
    assert d1<0 and d2>0, 'no saddle bracket'
    b,d=bracket(Q0)
    # Both endpoint distances are bounded, so no assumption about which is farther.
    radius=abs((Q1/Q0).log())+abs((Q2/Q0).log())
    lower=b-abs(d)*radius
    phi=2*(27*Z/4).log()+2*lower-K*Q.log()
    assert phi>0, 'nonpositive exponent'
    return {'status':'PASS','kind':'external baseline arithmetic only; candidate and unrefereed','verifier':'separately written (same agent)','lambda':str(lam),'Phi_lower_ball':str(phi),'B_tangent_lower_ball':str(lower),'dB_dw_ball':str(d),'bracket_slopes':[str(d1),str(d2)],'precision_bits':ctx.prec}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('certificate')
    args=p.parse_args()
    print(json.dumps(verify(args.certificate),indent=2))
