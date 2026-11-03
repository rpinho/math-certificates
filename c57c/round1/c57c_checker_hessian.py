"""Independent checker Hessians and literal formal-series constructions.

This module imports only another standalone checker, never discovery code.
All exterior coefficients use geometric/binomial powers, and the Grunsky
polynomials are the independently reconstructed logarithm powers.
"""
from fractions import Fraction as Q
from flint import arb,acb
from verify_c57c_center6 import prepare as checked_prepare,rational,GRUNSKY,require

def h(value=0):return (acb(value),acb(0),acb(0),acb(0),acb(0),acb(0))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,c):return tuple(x*c for x in a)
def multiply(a,b):
    return (a[0]*b[0],a[1]*b[0]+a[0]*b[1],a[2]*b[0]+a[0]*b[2],
            a[3]*b[0]+2*a[1]*b[1]+a[0]*b[3],a[4]*b[0]+a[1]*b[2]+a[2]*b[1]+a[0]*b[4],
            a[5]*b[0]+2*a[2]*b[2]+a[0]*b[5])
def inverse(a):
    inv=1/a[0];factor=inv*inv
    return (inv,-a[1]*factor,-a[2]*factor,(2*a[1]*a[1]*inv-a[3])*factor,
            (2*a[1]*a[2]*inv-a[4])*factor,(2*a[2]*a[2]*inv-a[5])*factor)
def divide(a,b):return multiply(a,inverse(b))
def conjugate(a):return tuple(x.conjugate() for x in a)
def power(a,n):
    out=h(1)
    while n:
        if n&1:out=multiply(out,a)
        a=multiply(a,a);n>>=1
    return out
def linear(value=None,index=0):
    out=[h() for _ in range(5)]
    if value is not None:out[index]=value
    return out
def linear_add(a,b):return [add(x,y) for x,y in zip(a,b)]
def linear_scale(a,c):return [scale(x,c) for x in a]
def linear_scalar(a,b):return [multiply(x,b) for x in a]
def linear_product(a,b):return [multiply(a[0],b[0])]+[add(multiply(a[0],b[i]),multiply(a[i],b[0])) for i in range(1,5)]
def series_product(a,b):
    out=[linear() for _ in range(8)]
    for total in range(8):
        for left in range(total+1):out[total]=linear_add(out[total],linear_product(a[left],b[total-left]))
    return out

def prepare(witness):
    require(witness.get('kind')=='taylor4','wrong higher witness kind')
    adapted=dict(witness,kind='dual');p=checked_prepare(adapted)
    return {'norm':p['norm'][0],'polys':p['poly'],'zeta':p['zeta'][0].real}

def exterior(s,a,w,t,q,mode):
    if mode==0:tt=h(1);gamma=h();alpha=h()
    elif mode==1:tt=h(1);gamma=h();alpha=inverse(w)
    else:
        tt=h(t);gamma=scale(divide(conjugate(w),w),q)
        alpha=add(divide(tt,w),scale(multiply(gamma,w),1/t))
    f=[linear(h(1)),linear(),linear(scale(power(tt,2),-s)),linear(scale(power(tt,3),a)),
       linear(power(tt,4),1),linear(power(tt,5),2),linear(power(tt,6),3),linear(power(tt,7),4)]
    u=[row[:] for row in f];u[0]=linear();term=[linear(h(1))]+[linear() for _ in range(7)];inv=[row[:] for row in term]
    for exponent in range(1,8):
        term=series_product(term,u);inv=[linear_add(x,linear_scale(y,(-1)**exponent)) for x,y in zip(inv,term)]
    inv[1]=linear_add(inv[1],linear(scale(alpha,-1)))
    for degree in range(2,8):inv[degree]=linear_add(inv[degree],linear_scalar(f[degree-2],gamma))
    u=[row[:] for row in inv];u[0]=linear();term=[linear(h(1))]+[linear() for _ in range(7)];root=[row[:] for row in term];coefficient=Q(1)
    for exponent in range(1,8):
        coefficient*=Q(1,2)-(exponent-1);coefficient/=exponent;term=series_product(term,u)
        root=[linear_add(x,linear_scale(y,rational(coefficient))) for x,y in zip(root,term)]
    return root

def scalar_coefficients(s,a,w0,t,q,witness):
    total=linear(h(witness['norm']))
    for mode,poly in enumerate(witness['polys']):
        if not poly:continue
        hs=exterior(s,a,w0,t,q,mode);powers={}
        for axis in range(3):
            for exponent in range(8//(axis+1)+1):powers[axis,exponent]=power(hs[axis+1][0],exponent)
        for exponents,coefficient in poly.items():
            factor=h(coefficient)
            for axis in range(3):
                if exponents[axis]:factor=multiply(factor,powers[axis,exponents[axis]])
            high=[axis for axis in range(3,7) if exponents[axis]]
            require(not high or len(high)==1 and exponents[high[0]]==1,'nonaffine higher coefficient')
            term=linear_scalar(hs[high[0]+1],factor) if high else linear(factor)
            total=linear_add(total,term)
    return total

def poly_add(a,b,multiplier=1):
    out=dict(a)
    for monomial,c in b.items():out[monomial]=out.get(monomial,acb(0))+multiplier*c
    return out
def poly_times(a,b):
    out={}
    for ma,ca in a.items():
        for mb,cb in b.items():
            variables=sorted(x for x in (*ma,*mb) if x)
            require(len(variables)<=2,'polynomial exceeds quadratic degree')
            key=tuple([0]*(2-len(variables))+variables);out[key]=out.get(key,acb(0))+ca*cb
    return out
def poly_conj(a):return {m:c.conjugate() for m,c in a.items()}

def quadratic_gram(s,a,m,epsilon,E,coefficients,zeta):
    def linear_part(index):
        p={(0,0):acb(coefficients[0][index].real)}
        for j in range(4):
            p[0,1+2*j]=acb(coefficients[j+1][index].real);p[0,2+2*j]=acb(-coefficients[j+1][index].imag)
        return p
    result=linear_part(0)
    result=poly_add(result,poly_times({(0,3):acb(epsilon)},linear_part(1)))
    result=poly_add(result,poly_times({(0,4):acb(epsilon)},linear_part(2)))
    result=poly_add(result,{(3,3):acb(E),(4,4):acb(E)})
    area={(0,0):acb(1-3*s*s/4-5*m/4)}
    specs=[(7,3*s*s/8,[-rational('1/2'),0,0,0]),(9,-3*s*a/4,[0,-rational('1/2'),0,0]),
           (11,3*a*a/8+5*s**3/16,[-3*s/4,0,-rational('1/2'),0]),
           (13,-15*s*s*a/16,[3*a/4,-3*s/4,0,-rational('1/2')])]
    for weight,constant,L in specs:
        p={(0,0):acb(constant)}
        for j,c in enumerate(L):p[0,1+2*j]=acb(c);p[0,2+2*j]=acb(0,1)*c
        area=poly_add(area,poly_times(p,poly_conj(p)),-weight)
    result=poly_add(result,area,zeta)
    gram=[[arb(0) for _ in range(9)] for _ in range(9)]
    for (i,j),coefficient in result.items():
        if i==j:gram[i][j]+=coefficient.real
        else:gram[i][j]+=coefficient.real/2;gram[j][i]+=coefficient.real/2
    return gram
