"""Independent decimal interval kernel. No submission code or numeric libraries.

Basic operations use Decimal contexts with FLOOR and CEILING rounding.
Decimal sqrt/ln/exp are correctly rounded (half-even); one adjacent decimal
on each side encloses their exact values. Trig uses Taylor with an explicit
Lagrange remainder. Pi uses Machin's formula and alternating atan series.
"""
from decimal import Decimal as D, Context, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN
from fractions import Fraction
from math import factorial
PREC=65
DN=Context(prec=PREC,rounding=ROUND_FLOOR)
UP=Context(prec=PREC,rounding=ROUND_CEILING)
RN=Context(prec=PREC,rounding=ROUND_HALF_EVEN)
class I:
    __slots__=('lo','hi')
    def __init__(self,x=0,hi=None):
        if isinstance(x,I): self.lo,self.hi=x.lo,x.hi; return
        if isinstance(x,Fraction) or isinstance(x,str) and '/' in x:
            q=Fraction(x); self.lo=DN.divide(D(q.numerator),D(q.denominator)); self.hi=UP.divide(D(q.numerator),D(q.denominator)); return
        self.lo=D(x); self.hi=D(x if hi is None else hi)
        assert self.lo<=self.hi
    def __add__(a,b):
        b=I(b); return I(DN.add(a.lo,b.lo),UP.add(a.hi,b.hi))
    __radd__=__add__
    def __neg__(a): return I(a.hi.copy_negate(),a.lo.copy_negate())
    def __sub__(a,b): return a+-I(b)
    def __rsub__(a,b): return I(b)+-a
    def __mul__(a,b):
        b=I(b)
        return I(min(DN.multiply(x,y) for x in (a.lo,a.hi) for y in (b.lo,b.hi)),max(UP.multiply(x,y) for x in (a.lo,a.hi) for y in (b.lo,b.hi)))
    __rmul__=__mul__
    def __truediv__(a,b):
        b=I(b); assert not b.lo<=0<=b.hi
        return a*I(DN.divide(D(1),b.hi),UP.divide(D(1),b.lo))
    def __rtruediv__(a,b): return I(b)/a
    def __pow__(a,n):
        assert isinstance(n,int) and n>=0
        def positive_power(x,ctx):
            # Only directed multiplies; no Decimal.power transcendental route.
            v=D(1);base=x;k=n
            while k:
                if k&1:v=ctx.multiply(v,base)
                k//=2
                if k:base=ctx.multiply(base,base)
            return v
        def endpoint(x,lower):
            if x>=0:return positive_power(x,DN if lower else UP)
            if n%2==0:return positive_power(x.copy_abs(),DN if lower else UP)
            return positive_power(x.copy_abs(),UP if lower else DN).copy_negate()
        if n==0:return I(1)
        if n%2==0:
            upper=max(endpoint(a.lo,False),endpoint(a.hi,False))
            lower=D(0) if a.lo<=0<=a.hi else min(endpoint(a.lo,True),endpoint(a.hi,True))
            return I(lower,upper)
        return I(endpoint(a.lo,True),endpoint(a.hi,False))
    def abs(a):
        return I(0 if a.lo<=0<=a.hi else min(a.lo.copy_abs(),a.hi.copy_abs()),max(a.lo.copy_abs(),a.hi.copy_abs()))
    def sqrt(a):
        assert a.lo>=0
        return I(max(D(0),DN.next_minus(RN.sqrt(a.lo))),UP.next_plus(RN.sqrt(a.hi)))
    def log(a):
        assert a.lo>0
        return I(DN.next_minus(RN.ln(a.lo)),UP.next_plus(RN.ln(a.hi)))
    def exp(a): return I(DN.next_minus(RN.exp(a.lo)),UP.next_plus(RN.exp(a.hi)))
    def pair(a): return [str(a.lo),str(a.hi)]
    def __repr__(a): return '['+str(a.lo)+', '+str(a.hi)+']'

def imax(*args):
    aa=list(map(I,args));return I(max(a.lo for a in aa),max(a.hi for a in aa))
def imin(*args):
    aa=list(map(I,args));return I(min(a.lo for a in aa),min(a.hi for a in aa))
def hull(a,b):return I(min(a.lo,b.lo),max(a.hi,b.hi))
def atan_small(x):
    # Alternating series, x exact in (0,1); interval terms, explicit tail.
    x=I(x); assert 0<x.lo<=x.hi<1
    t=x;s=I(0)
    for j in range(110):
        s=s+((-1)**j)*t/(2*j+1);t=t*x*x
    e=t/(221);return s+I(e.hi.copy_negate(),e.hi)
PI=16*atan_small(Fraction(1,5))-4*atan_small(Fraction(1,239))

def sincos(x):
    x=I(x)
    # Only narrow inputs are used. Reduction subtracts a rigorous multiple of pi.
    m=RN.divide(RN.add(x.lo,x.hi),D(2))
    turns=int(RN.divide(m, RN.multiply(D(2),RN.divide(RN.add(PI.lo,PI.hi),D(2)))).to_integral_value(rounding=ROUND_HALF_EVEN))
    x=x-2*turns*PI
    assert x.abs().hi<4
    xx=x*x;st=x;ct=I(1);ss=st;cc=ct
    for j in range(1,55):
        st=-st*xx/((2*j)*(2*j+1));ct=-ct*xx/((2*j-1)*(2*j))
        ss+=st;cc+=ct
    # Degrees 109 and 108. Lagrange next-order errors use |derivative|<=1.
    es=(x.abs()**110)/factorial(110);ec=(x.abs()**109)/factorial(109)
    return ss+I(es.hi.copy_negate(),es.hi),cc+I(ec.hi.copy_negate(),ec.hi)

def sinh(x):return (I(x).exp()-(-I(x)).exp())/2
def cosh(x):return (I(x).exp()+(-I(x)).exp())/2
def tanh(x):return sinh(x)/cosh(x)
