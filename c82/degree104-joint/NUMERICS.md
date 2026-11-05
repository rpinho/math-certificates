# Quantity and numerical proof

For T(z)=z(1-z), Q=product R_j^m_j, D=sum m_j deg R_j, and the formal
product A=product S_i^q_i (nonnegative rational exponents), the candidate uses

    g(t) = (sum q_i log|S_i(T(exp(2*pi*i*t)))|
            - sum m_j log|R_j(T(exp(2*pi*i*t)))|)/D
    J = integral_0^1 max(0,g(t)) dt
    H = sum m_j log M(R_j composed with T)/D
    B = H+J;  C82 <= B.

The unnormalized integral I=D*J is the integral appearing in the proof's
bracket before division by D. All logs are natural. There is no extra factor
of two in B: the integrator doubles exactly one half-circle integral because
real coefficients give g(1-t)=g(t).

The release PROOF.md gives the Doche limit-point reduction and the clean-room
referee’s bounded-multiplicity extraction argument for infinitely many distinct algebraic numbers. This
job rechecks its exact finite hypotheses (integral coefficients, positive
integer denominator multiplicities, monicity, nonnegative rational exponents,
degree A<D, and all active numerator/denominator gcds). It upgrades numerical
verification; it does not turn that mathematical reduction into a formal proof.

## Separately written implementation (same agent)

`verify_best.py` imports only standard Python and python-flint. It uses no
functions from the baseline or any submitted/search/review code. It composes
each polynomial with T exactly in Z[z], then calls FLINT's certified complex
root isolation and checks all root multiplicities against the exact degree.
Jensen gives H from log|leading coefficient|+sum log max(1,|root|).
The same root multisets express g as a signed sum of log distances plus a
leading-coefficient constant. This uses no approximate polynomial coefficients.

On an exact dyadic cell of width w and midpoint c, h=w/2 and u=exp(2*pi*i*c).
Every point of the unit-circle arc is within tau*h of u, tau=2*pi.
Triangle inequalities give whole-cell root-distance ranges [d-tau*h,d+tau*h].
Signed log bounds can prove g<0, including a numerator zero, and then the
integral is exactly zero. If any root is not separated and negativity is not
proved, the cell is split. No log singularity is passed to a Taylor formula.

For f(t)=log|exp(i*tau*t)-r|,

    f'(c) = Re(i*tau*u/(u-r))
    |f''| <= tau^2 |r| / near^2
    |f^(8)| <= tau^8 |r| A7(|r|) / near^8,
    A7(x) = 1+120x+1191x^2+2416x^3+1191x^4+120x^5+x^6.

The bounds follow by repeated application of u*d/du to log(u-r), taking
absolute values and |u|=1. Absolute rational weights give M2 and M8 for g.
The midpoint Taylor range g(c) +/- (|g'(c)|h+M2*h^2/2) can prove sign.

On proven-positive cells, four-point Gauss–Legendre quadrature has error at
most M8*w^9/1778112000; nodes and weights are evaluated as exact radical
expressions in Arb. Both signs of the remainder are retained in the result.

On crossing cells, let a=g(c), b=g'(c), and L(x)=a+b*x. The positive-part map
is 1-Lipschitz, so

    |integral max(0,g(c+x)) dx - integral max(0,L(x)) dx| <= M2*w^3/24.

For b!=0, the second integral is

    ((a+b*h)_+^2 - (a-b*h)_+^2)/(2*b).

This identity works for either sign of b. If the slope ball contains zero,
use w*max(0,a) with error |b|w^2/4 in addition to the curvature remainder.
All parameters, evaluations, errors and sums remain Arb balls. A cell is
accepted only if the entire enclosure radius is <tol*w. Failed comparisons
cause subdivision, never approximate sign decisions. Depth exhaustion aborts.
Every dyadic child is visited once, with no dropped cells. The tolerance is a
subdivision criterion; actual ball endpoints, not the tolerance, determine the
final comparison with the exact rational target.

JSON endpoints are exact dyadics, mantissa*2^exponent. Displayed balls include
their own decimal-printing uncertainty. No printed center is called an upper
bound. The trusted arithmetic backend is FLINT/Arb; this is a computational
certificate, not a machine-checked proof of the arithmetic library.
