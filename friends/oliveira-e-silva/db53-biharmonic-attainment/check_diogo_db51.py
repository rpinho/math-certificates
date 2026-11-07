#!/usr/bin/env python3
"""Exact algebra for the finite-p reflection-even attainment note.

Python 3.9+, standard library only. No profile search, floating point,
external imports, or sampled PDE conclusion. Symbolic identities and positive
rational coefficients verify encoded identities, not the note or its sources.
The convexity, kernel normalization, reflection, analytic continuation, tail
bounds and compactness proofs remain mathematical arguments.
"""
from fractions import Fraction as F
from math import factorial
import hashlib
from pathlib import Path

N = 7                         # x, y, z, lambda, epsilon, p, t
ZERO = (0,) * N


class Poly:
    def __init__(self, value=0):
        if isinstance(value, dict):
            self.c = {k: F(v) for k, v in value.items() if v}
        elif isinstance(value, Poly):
            self.c = dict(value.c)
        else:
            self.c = {ZERO: F(value)} if value else {}

    def __add__(self, other):
        out = dict(self.c)
        for k, v in Poly(other).c.items():
            out[k] = out.get(k, F(0)) + v
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.c.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        out = {}
        for k, v in self.c.items():
            for j, w in Poly(other).c.items():
                key = tuple(r + s for r, s in zip(k, j))
                out[key] = out.get(key, F(0)) + v * w
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        out = Poly(1)
        for _ in range(n):
            out = out * self
        return out

    def diff(self, i):
        out = {}
        for k, v in self.c.items():
            if k[i]:
                j = list(k)
                j[i] -= 1
                out[tuple(j)] = v * k[i]
        return Poly(out)

    def at(self, i, value):
        out = Poly()
        value = Poly(value)
        for k, v in self.c.items():
            j = list(k)
            j[i] = 0
            out += Poly({tuple(j): v}) * value ** k[i]
        return out


def var(i):
    k = list(ZERO)
    k[i] = 1
    return Poly({tuple(k): 1})


def equal(a, b):
    assert not (Poly(a) - b).c, (Poly(a) - b).c


x, y, z, lam, eps, p, t = (var(i) for i in range(N))


class Rat:
    """Rational functions with exact polynomial cross multiplication."""
    def __init__(self, num=0, den=1):
        if isinstance(num, Rat):
            self.num, self.den = num.num, num.den
        else:
            self.num, self.den = Poly(num), Poly(den)
        assert self.den.c

    def __add__(self, other):
        other = Rat(other)
        return Rat(self.num*other.den+other.num*self.den, self.den*other.den)

    __radd__ = __add__

    def __neg__(self):
        return Rat(-self.num, self.den)

    def __sub__(self, other):
        return self + -Rat(other)

    def __rsub__(self, other):
        return Rat(other) + -self

    def __mul__(self, other):
        other = Rat(other)
        return Rat(self.num*other.num, self.den*other.den)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Rat(other)
        return Rat(self.num*other.den, self.den*other.num)

    def __rtruediv__(self, other):
        return Rat(other) / self

    def __pow__(self, n):
        return Rat(self.num**n, self.den**n)


def same(a, b):
    a, b = Rat(a), Rat(b)
    equal(a.num*b.den, b.num*a.den)


def positive_for_p_above_two(expr):
    # Substitute p=2+x, x>0. Strictly positive coefficients certify the sign.
    expr = Rat(expr)
    for pol in (expr.num, expr.den):
        q = pol.at(5, 2+x)
        assert q.c and all(c > 0 for c in q.c.values()), q.c


# Rate elimination: t is the real parallel frequency and z is sigma.
equal(4*t**2*z**2-eps - (4*z**2*(1+z**2)-eps),
      4*z**2*(t**2-z**2-1))
# Squared beta formula: x=sqrt(1+eps), beta^2=(x-1)/2.
y_beta_squared = (x-1)*F(1, 2)
equal(4*y_beta_squared*(1+y_beta_squared), x**2-1)
# The polynomial in sigma is increasing on sigma>0 and ranges 0..infinity.
equal((4*z**2*(1+z**2)).diff(2), 8*z+16*z**3)
assert all(c > 0 for c in (8*z+16*z**3).c.values())
# alpha^2-beta^2=1 and (2 alpha beta)^2=eps.
y_alpha_squared = (x+1)*F(1, 2)
equal(y_alpha_squared-y_beta_squared, 1)
equal(4*y_alpha_squared*y_beta_squared, x**2-1)

# Critical source/overlap margins, in beta units, for ALL real p>2.
P = Rat(p)
B = (P+2)/(2*P)
eta = (P-2)/(2*(P+2))
sigma0 = (1+(P-1)*B)/2
margins = {
    'beta-b': 1-B,
    '(p-1)b-beta': (P-1)*B-1,
    'sigma0-beta': sigma0-1,
    '(p-1)b-sigma0': (P-1)*B-sigma0,
    'eta': eta,
    '1-eta': 1-eta,
    'pb-2beta': P*B-2,
    'pb(1-eta)-2beta': P*B*(1-eta)-2,
}
for margin in margins.values():
    positive_for_p_above_two(margin)
same(P*B*(1-eta), (P+6)/4)
same(P*B*(1-eta)-2, (P-2)/4)
# Angular quadric circle radius is nonnegative exactly beyond beta:
# after multiplying 4r^2, it is 4r^2(1+r^2)-eps, the same rate polynomial.
equal(4*z**2*(1+z**2)-eps, 4*z**4+4*z**2-eps)

# Encoded resolvent partial-fraction algebra. Exact pairs represent
# real + i*imag, with all entries rational polynomials; eps here is delta.
def cmul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def cequal(a, b):
    equal(a[0], b[0])
    equal(a[1], b[1])


minus = (x-1, -eps)
plus = (x-1, eps)
cequal(cmul(minus, plus), ((x-1)**2+eps**2, Poly(0)))
# 1/(x-1-i delta)-1/(x-1+i delta) has numerator 2i delta.
cequal((plus[0]-minus[0], plus[1]-minus[1]), (Poly(0), 2*eps))
# This does not derive the Helmholtz fundamental solution or its 4*pi factor.

# Formal differentiation of exp(g*r)r^s has normalized derivative g+s/r.
# Set g=ik and s=-1. Coefficients in (drr+2/r dr+k^2) cancel.
s = -1
equal(2*lam*s+2*lam, 0)
assert s*(s-1)+2*s == 0
# For arbitrary integer index j, the r^(-j) coefficients are j(j+1)
# and -2ik*j. Here y is a FREE symbolic j, rather than a finite grid.
equal((-y)*(-y-1), y*(y+1))
equal(2*lam*(-y), -2*lam*y)
# General radial conjugation: with exp(g*r)/r, v'' coefficient 1,
# v' coefficient 2g, v coefficient g^2+k^2=0.
equal(2*(lam*t-1)+2, 2*lam*t)
equal((lam*t-1)**2+1+2*(lam*t-1)-lam**2*t**2, 0)

# Zonal Laplacian applied to s^j, with s=t+1: compare coefficients of
# s^(j-1), s^j. This proves the lowering rule for a FREE symbolic j.
equal(2*y*(y-1)+2*y, 2*y**2)
equal(-y*(y-1)-2*y, -y*(y+1))
# Arbitrary-J product: P_J=2^J(J!)^2, established by its base and ratio;
# dividing by (2ik)^J J! gives J!/(ik)^J.
assert 1 == 2**0*factorial(0)**2
same(Rat(2*(y+1)**2, 2*lam*(y+1)), Rat(y+1, lam))
# Additional exact finite polynomial controls; g=ik is represented by 1,
# since the coefficient of g^-j is checked separately by homogeneity.
for J in range(13):
    coeff = (1+t)**J
    for j in range(J+1):
        equal(coeff.at(6, -1), factorial(J) if j == J else 0)
        coeff = ((1-t**2)*coeff.diff(6).diff(6)
                 -2*t*coeff.diff(6)+j*(j+1)*coeff)*F(1, 2*(j+1))

# Scalar inequality uses convex tangent bounds at +/-t. Coefficient
# bookkeeping with x=t^p and y=t^(p-1) is exact, for a FREE real p.
# Same signs: (1+pt)-1-x-p(t+y)=-x-py.
equal((1+p*t)-1-x-p*(t+y), -x-p*y)
# Opposite signs: (1-pt)-1-x+p(t+y)=py-x.
equal((1-p*t)-1-x+p*(t+y), p*y-x)
# On 0<=t<=1, exponent ordering supplies t^p<=t^(p-1)<=t^(p/2).
equal(p-1-p*F(1, 2), (p-2)*F(1, 2))
positive_for_p_above_two(P/2-1)
# Stronger no-error inequality fails at p=5/2, A=B=1:
# 2^(5/2)-2-2p = 4sqrt(2)-7 <0, exactly since 32<49.
assert 2+2*F(5, 2) == 7
assert 4**2*2 < 7**2

# Encoded quotient bookkeeping: cross energy is m*x, each Euler integral x;
# loss <=(p/2)x leaves 2+(3p/2)x.
equal(2+2*p*t-p*t*F(1, 2), 2*(1+3*p*t*F(1, 4)))
# Derivative at zero of (1+(3p/4)x)^(2/p)-(1+x).
same((3*P/4)*(2/P)-1, F(1, 2))
# Scaling Lu=m1 |u|^(p-2)u: the power of m1 on both sides agrees.
same(1+Rat(1, p-2), Rat(p-1, p-2))
# Two equal p-masses a: 2*m*a^(2/p) / (2a)^(2/p)
# is 2^(1-2/p)*m. Compare exponents, without sampled powers.
same(1-2/P, (P-2)/P)
positive_for_p_above_two(1-2/P)

# Gaussian linear-source negative control, g=exp(-|x|^2).
# Compute Lg/g from the original operator, not a far-field approximation.
coords = (x, y, z)

def dg(poly, i):
    return poly.diff(i)-2*coords[i]*poly


def lapg(poly):
    return sum((dg(dg(poly, i), i) for i in range(3)), Poly())


rho = x**2+y**2+z**2
lap = lapg(Poly(1))
equal(lap, 4*rho-6)
ratio = lapg(lap)+2*lap+1+eps
equal(ratio, 16*rho**2-72*rho+49+eps)
assert ratio.c[(4, 0, 0, 0, 0, 0, 0)] == 16
# Encoded d=3,k=1,gamma=2 rate substitutions, all three radial regimes.
alpha1 = 2-4/P
alpha_rad = 3-6/P
same(1-alpha1/2, 2/P)
same(1-alpha_rad/2, 3/P-F(1, 2))
same(2/P-(3/P-F(1, 2)), F(1, 2)-1/P)
positive_for_p_above_two(F(1, 2)-1/P)
same(2/P-F(1, 2), (4-P)/(2*P))  # positive precisely when 2<p<4.
assert F(1-3, 3) == -F(2, 3)
assert F(2, 3)-F(1, 2) == F(1, 6)  # power gap at p=3 beats logarithm.

print('PASS: encoded rate and partial-fraction identities; Gaussian operator algebra')
print('PASS: all p>2 rational source/overlap margins and strict binding slope 1/2')
print('PASS: arbitrary-index transport/axis identities; additional orders 0..12')
print('PASS: scalar bound bookkeeping and exact p=5/2 no-error counterexample')
print('PASS: encoded scaling and escape-threshold exponent identities')
print('PASS: encoded nonradial rate substitutions, including p=3 logarithm')
print('Scope: encoded algebra only; does not read the note or verify cited theorems,')
print('kernel normalization, reflection, analytic lemmas, or existence/compactness.')
print('SHA-256:', hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
