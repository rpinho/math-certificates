"""Exact check of every rational number in the note. Python standard library, one process, no inputs.

Sparse polynomials use integer coefficients and one common denominator.
The certificate is rebuilt from P and Q alone.
"""
from fractions import Fraction as F
from math import gcd, lcm, comb, factorial
from functools import reduce
from time import perf_counter


class Poly:
    def __init__(self, terms, den=1):
        terms = {k: v for k, v in terms.items() if v}
        g = reduce(gcd, terms.values(), den)
        self.c = {k: v // g for k, v in terms.items()}
        self.d = den // g

    def __add__(self, other):
        d = lcm(self.d, other.d)
        c = {k: v * (d // self.d) for k, v in self.c.items()}
        for k, v in other.c.items():
            c[k] = c.get(k, 0) + v * (d // other.d)
        return Poly(c, d)

    def scale(self, q):
        q = F(q)
        return Poly({k: v*q.numerator for k, v in self.c.items()}, self.d*q.denominator)

    def mul(self, other, cap=None):
        c = {}
        for a, v in self.c.items():
            for b, w in other.c.items():
                k = tuple(x+y for x, y in zip(a, b))
                if cap is None or k[-1] <= cap:
                    c[k] = c.get(k, 0) + v*w
        return Poly(c, self.d*other.d)

    def power(self, n, cap=None):
        dim = len(next(iter(self.c)))
        result = Poly({(0,)*dim: 1})
        for _ in range(n):
            result = result.mul(self, cap)
        return result

    def items(self):
        return ((k, F(v, self.d)) for k, v in self.c.items())


def fractions_poly(items):
    c = {}
    for k, v in items:
        c[k] = c.get(k, F(0)) + v
    d = lcm(*(v.denominator for v in c.values()))
    return Poly({k: v.numerator*(d//v.denominator) for k, v in c.items()}, d)


def binomial(a, n):
    v = F(1)
    for j in range(n):
        v *= F(a-j, j+1)
    return v


def taylor(p, a, n, cap=None):
    dim = len(next(iter(p.c)))
    one = Poly({(0,)*dim: 1})
    result, power = one, one
    for j in range(1, n+1):
        power = power.mul(p, cap)
        result = result + power.scale(binomial(a, j))
    return result


def moment(j, scale):
    v = F(1)
    for k in range(j):
        v *= (F(5, 2)+k)*scale
    return v


def expect(p, scale=F(3, 5)):
    return fractions_poly((k[1:], v*moment(k[0], scale)) for k, v in p.items())


def avg(p):
    return fractions_poly((k[1:], v*F(comb(k[0], k[0]//2), 2**k[0]))
                          for k, v in p.items() if k[0] % 2 == 0)


def envelope(p):
    return fractions_poly(((k[-1],), abs(v)) for k, v in p.items())


def evaluate(p, x):
    return sum(v*x**k[0] for k, v in p.items())


Pcoeff = [F(35,4), -7, 1]
Qcoeff = [F(3465,16), F(-693,2), F(297,2), -22, 1]


def raw_x(beta=None):
    # Variables: s,y,epsilon (fixed beta) or s,y,beta,epsilon.
    dim = 4 if beta is None else 3
    one = Poly({(0,)*dim: 1})
    p = fractions_poly(((i,)+(0,)*(dim-2)+(1,), F(v)) for i, v in enumerate(Pcoeff))
    q = fractions_poly(((i, 0, 1, 2) if beta is None else (i, 0, 2),
                        F(v)*(1 if beta is None else beta)) for i, v in enumerate(Qcoeff))
    y = Poly({(0,1)+(0,)*(dim-2): 1})
    return (p.mul(p) + q.mul(q) + q.scale(-2)
            + p.mul(one+q).mul(y).scale(2) + q.mul(y.mul(y)).scale(4))


def certificate(beta, upper=False):
    start = perf_counter()
    x = raw_x(beta)
    h = expect(taylor(x, F(5,3), 5))
    if upper:
        h = h + expect(x.power(6)).scale(F(14,729))
    h1 = h + Poly({(0,0): -1})
    r = envelope(h1)
    eta = F(1,1000)
    rho = evaluate(r, eta)
    assert rho < F(1,100)
    # (1-rho)^(-22/5)<2 is checked without irrational arithmetic.
    assert (1-rho)**22 > F(1,32)
    n = fractions_poly([((0,), F(1)), ((2,),F(35,2)), ((4,),F(10395,2)*beta**2)])
    bound = avg(taylor(h1,F(3,5),4)) + n.scale(-1)
    bound = bound + r.power(5).scale((1 if upper else -1)*2*abs(binomial(F(3,5),5)))
    tail = sum(abs(v)*eta**(k[0]-4) for k,v in bound.items() if k[0]>4)
    low = {k[0]:str(v) for k,v in bound.items() if k[0]<=4}
    print('UPPER' if upper else 'LOWER', 'beta=',beta, flush=True)
    print('rho=',float(rho), 'degree=',max(k[0] for k in bound.c), 'low=',low, flush=True)
    print('tail=',float(tail), 'N(eta)=',float(evaluate(n,eta)), flush=True)
    assert set(low)=={4}
    lead = F(bound.c[(4,)],bound.d)
    if upper:
        assert lead == F(-736344,15625)
        assert tail < F(7,50)
        assert lead+F(7,50) < -46*evaluate(n,eta)
    else:
        assert lead == F(984312,85375)
        assert tail < F(3,25)
        assert evaluate(n,eta)<F(1001,1000)
        assert lead-F(3,25)>11*evaluate(n,eta)
        print('margin against actual 11N(eta)=',float(lead-F(3,25)-11*evaluate(n,eta)),flush=True)
    print('seconds=',round(perf_counter()-start,3),flush=True)


def quartic():
    x = raw_x()
    h = expect(taylor(x,F(5,3),4,cap=4))
    h1 = h + Poly({(0,0,0):-1})
    b = avg(taylor(h1,F(3,5),4,cap=4))
    n = fractions_poly([((0,0),F(1)),((0,2),F(35,2)),((2,4),F(10395,2))])
    c = b+n.scale(-1)
    print('Symbolic B-N through order 4 (beta-degree,epsilon-degree):',
          {k:str(v) for k,v in c.items()},flush=True)
    assert dict(c.items())=={(0,4):F(-736344,15625),(1,4):F(6453216,15625),(2,4):F(-11359656,15625)}
    a,b,c0 = (dict(c.items())[(j,4)] for j in [2,1,0])
    beta = -b/(2*a)
    maxval = c0-b*b/(4*a)
    print('vertex beta=',beta,'C(beta)=',maxval,flush=True)
    assert beta==F(194,683) and maxval==F(984312,85375)


def input_and_positivity():
    p=fractions_poly([((i,),F(v)) for i,v in enumerate(Pcoeff)])
    q=fractions_poly([((i,),F(v)) for i,v in enumerate(Qcoeff)])
    moments=[sum(v*moment(k[0],F(1)) for k,v in a.items())
             for a in [p,q,p.mul(q),p.mul(p),q.mul(q)]]
    print('input E[P],E[Q],E[PQ],E[P²],E[Q²]=',list(map(str,moments)),flush=True)
    assert moments==[0,0,0,F(35,2),F(10395,2)]
    s=Poly({(1,):1})
    const=lambda a:fractions_poly([((0,),F(a))])
    derivative=lambda p:fractions_poly([((k[0]-1,),v*k[0]) for k,v in p.items() if k[0]])
    for r,eigenvalue,degree in [(p,4,2),(q,8,4)]:
        dr=derivative(r)
        kr=s.mul(derivative(dr)).scale(-2)+(s.scale(2)+const(-5)).mul(dr)
        assert not (kr+r.scale(-eigenvalue)).c
        laguerre=fractions_poly([((j,),(-1)**j*binomial(F(degree)+F(3,2),degree-j)
                                 *F(1,factorial(j))) for j in range(degree+1)])
        assert not (r+laguerre.scale(-factorial(degree))).c
    assert not (p+((s+const(F(-7,2))).power(2)+const(F(-7,2))).scale(-1)).c
    rhs=(s+const(F(-33,2))).power(2).mul(s.power(2)+s.scale(11)+const(F(363,4)))
    rhs=rhs+(s+const(F(-7,6))).power(2).scale(F(297,2))+const(F(-98769,4))
    assert not (rhs+q.scale(-1)).c
    lower=1-F(7,2)*F(1,1000)-F(98769,4)*F(194,683)*F(1,1000)**2
    print('positivity lower=',lower,flush=True)
    assert lower==F(1351638407,1366000000)>F(49,50)
    assert -sum(binomial(F(5,3),j)*(-1)**j for j in range(6))==F(14,729)


if __name__=='__main__':
    input_and_positivity()
    quartic()
    certificate(F(194,683))
    certificate(F(0),upper=True)
    print('ALL EXACT ASSERTIONS PASSED',flush=True)
