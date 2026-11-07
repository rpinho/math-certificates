"""Independent DB51 controls, written from q(u) in the published paper.

Run only on stats. No claimant module, search output or verifier is used.
Exact polynomial Gaussian integration uses elementary Gaussian moments.
Finite controls supplement the functional proof audit in REPORT.md.
"""
import json
import math
import pathlib
import random
import time

import sympy as S
import mpmath as mp

started = time.time()
x, y, z, t, s, lam = S.symbols('x y z t s lam', real=True)
eps = S.symbols('eps', positive=True)
pi = S.pi
results = {}


def exact_zero(a):
    v = S.simplify(S.expand(a))
    assert v == 0, str(v)


def normal_mean(poly, variables, variance):
    """Expectation under independent zero-mean normal variables."""
    out = 0
    for powers, coeff in S.Poly(S.expand(poly), *variables).terms():
        term = coeff
        for k in powers:
            if k % 2:
                term = 0
                break
            term *= (S.factorial2(k-1) if k else 1) * variance**(k//2)
        out += term
    return S.expand(out)


def laplace_gaussian(poly, variables):
    """e^(|X|²/2) Delta[poly e^(-|X|²/2)]."""
    return S.expand(sum(S.diff(poly, v, 2)-2*v*S.diff(poly, v)
                        +(v*v-1)*poly for v in variables))


def original_operator(poly):
    d = laplace_gaussian(poly, (x, y, z))
    return S.expand(laplace_gaussian(d, (x, y, z))+2*d+(1+eps)*poly)


# Rebuild the Fourier symbol from Delta^2+2Delta+1+epsilon.
k2 = S.symbols('k2', nonnegative=True)
exact_zero(k2**2-2*k2+1+eps-((k2-1)**2+eps))
results['original_symbol'] = '(k2-1)^2+epsilon'

# Whole real-power inequality: an independent mixed-derivative proof.
a, b, p = S.symbols('a b p', positive=True)
same = (a+b)**p-a**p-b**p-p*(a**(p-1)*b+b**(p-1)*a)
mixed = p*(p-1)*((a+b)**(p-2)-a**(p-2)-b**(p-2))
exact_zero(S.diff(same, a, b)-mixed)
rr = S.symbols('rr', nonnegative=True)
exact_zero(same.subs(p, 3+rr).subs(b, 0))
exact_zero(same.subs(p, 3+rr).subs(a, 0))
# For p>=3 the power r=p-2 is >=1: (a+b)^r>=a^r+b^r.
# For opposite signs a>=b, the tangent bound at a leaves b^(p-1)(p*a-b)>=0.
opposite = (a-b)**p-a**p-b**p+p*(a**(p-1)*b+b**(p-1)*a)
exact_zero(opposite-((a-b)**p-a**p+p*a**(p-1)*b)-b**(p-1)*(p*a-b))
# Cubic controls cover all sign/order cases after swapping the larger magnitude.
for sa in [-1, 1]:
    for sb in [-1, 1]:
        A, B = sa*(a+b), sb*b
        lhs = (a+2*b)**3 if sa == sb else a**3
        rhs = (a+b)**3+b**3+3*((a+b)*A*B+b*B*A)
        rem = S.factor(lhs-rhs)
        assert all(c >= 0 for _, c in S.Poly(rem, a, b).terms())
results['power_inequality'] = 'exact mixed derivative and all cubic signs PASS; analytic sign argument in REPORT.md'
negative_control = 2**S.Rational(5, 2)-2-5
assert negative_control < 0
results['below_three_negative_control'] = str(negative_control)

xx = S.symbols('xx', positive=True)
h = 2*S.log(1+p*xx)-p*S.log(1+xx)
exact_zero(S.diff(h, xx)-p*(1+(2-p)*xx)/((1+p*xx)*(1+xx)))
results['binding_derivative'] = str(S.factor(S.diff(h, xx)))

# Exact controls with both odd and even zero axial mean, plus transverse coupling.
controls = [
    ('odd', z),
    ('even_zero_mean', z*z-1),
    ('odd_transverse', z*(1+(x*x+y*y)/3)),
    ('mixed', 1+z/2+(x*x+y*y-2)/3+(z**3-3*z)/5),
]
gaussians = []
for name, poly in controls:
    fpoly = original_operator(poly)
    # Physical convolution at (0,0,s), complete square in the integration variable.
    conv_integrand = poly.subs(z, t+s/2)*fpoly.subs(
        {x:-x, y:-y, z:s/2-t}, simultaneous=True)
    cpoly = normal_mean(conv_integrand, (x, y, t), S.Rational(1, 2))
    # C(s)=pi^(3/2) exp(-s²/4) cpoly(s).
    # Its bilateral Laplace integral shifts s to 2*lambda+N(0,2).
    avg_poly = normal_mean(cpoly.subs(s, t+2*lam), (t,), S.Integer(2))
    weighted = S.expand(2*pi*pi*avg_poly)  # suppress common exp(lambda²)
    # Independently transform w, then compute the transverse shifted form.
    # W_lambda=sqrt(2pi) exp(lambda²/2) exp(-r²/2) wp.
    wp = normal_mean(poly.subs(z, t+lam), (t,), S.Integer(1))
    wp_op = laplace_gaussian(wp, (x, y))+(1+lam*lam)*wp
    positive_form = S.expand(2*pi*pi*normal_mean(wp_op**2+eps*wp**2,
                                               (x, y), S.Rational(1, 2)))
    exact_zero(weighted-positive_form)
    # Also check Lw's transform, including the PLUS lambda² sign.
    bp = normal_mean(fpoly.subs(z, t+lam), (t,), S.Integer(1))
    transformed_operator = laplace_gaussian(wp_op, (x, y))+(1+lam*lam)*wp_op+eps*wp
    exact_zero(bp-transformed_operator)
    if name in ['odd', 'even_zero_mean']:
        exact_zero(wp.subs(lam, 0))
        exact_zero(weighted.subs(lam, 0))
        assert weighted.subs({lam:1, eps:1}) > 0
    # C may change sign. This is a linear identity, NOT an eigenfunction test.
    values = {str(j): str(S.simplify(cpoly.subs({s:j,eps:1}))) for j in [0,2,4,8]}
    gaussians.append(dict(name=name,w_polynomial=str(poly),
                          C_polynomial=str(S.factor(cpoly)),
                          weighted_average_without_exp=str(S.factor(weighted)),
                          C_sign_polynomial_at_epsilon1=values))
    print('GAUSSIAN', name, 'PASS', flush=True)
results['gaussian_controls'] = gaussians

# A complex reflected pair is even without conjugation; conjugating is incorrect.
R = S.symbols('R', real=True)
u = (z+S.I*(z*z-1))*S.exp(-z*z/2)
pair = u.subs(z,z-R)+u.subs(z,-z-R)
exact_zero(pair-pair.subs(z,-z))
wrong = u.subs(z,z-R)+S.conjugate(u.subs(z,-z-R))
assert S.simplify((wrong-wrong.subs(z,-z)).subs({z:2,R:1})) != 0
results['complex_reflection'] = 'exact evenness PASS; conjugated reflection rejected'

# Stress tests are only falsification controls, never proof of all real exponents.
mp.mp.dps = 65
rng = random.Random(5132026)
minimum = mp.inf
count = 0
for pp in ['3', '3.000001', '3.1', '3.5', '3.999999', '4', '5', '10']:
    power = mp.mpf(pp)
    for _ in range(400):
        tv = mp.power(10, -12*rng.random())
        for sign in [-1,1]:
            bv = sign*tv
            rem = abs(1+bv)**power-1-abs(bv)**power-power*(bv+abs(bv)**(power-2)*bv)
            assert rem >= -mp.mpf('1e-60'), (pp,str(tv),sign,str(rem))
            minimum = min(minimum, rem)
            count += 1
results['stress_only'] = dict(count=count,minimum=str(minimum),precision=mp.mp.dps)

# Splitting with mass a at two escaping centers gives the sharp factor 2^(1-2/p).
# Taking any positive strict binding gap makes this incompatible with minimality.
for pp in [mp.mpf(3),mp.mpf('3.5'),mp.mpf('3.999999')]:
    alpha = 2/pp
    for j in range(1,1001):
        mass = mp.mpf(j)/2000
        strict_ratio = mp.mpf('0.999')
        lhs = 2*mass**alpha/(strict_ratio*2**(1-alpha))+(1-2*mass)**alpha
        assert lhs > 1
results['mass_splitting_control'] = '3000 escaping-mass controls PASS (analytic concavity in REPORT.md)'
results['elapsed_seconds'] = time.time()-started
pathlib.Path('referee_results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2),flush=True)
print('REFEREE_CHECKS_PASS',flush=True)
