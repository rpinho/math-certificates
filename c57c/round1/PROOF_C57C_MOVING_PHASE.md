# Moving-phase Grunsky witnesses for the proposed C57c cover

Credit: Wikström, arXiv:2610.34580v1, equation (12), already uses a
phase congruence for the complex Grunsky matrix. The seven-index moving
phases here extend his mechanism.

Candidate, unrefereed; the complete 0.61230 forest passed separate exhaustive replay. No
novelty judgment. The normalization, omitted-value transforms, center,
area theorem and quadratic contradiction are those explicitly proved in
PROOF_C57C_PARABOLIC.md, with the scaled-radius endpoint convention in
PROOF_C57C_SCALED_BLOCH.md when those constraints are present.

The classical Grunsky inequality applies to EVERY complex test vector at
each fixed function and omitted value. Hence its vector may be selected
as a function of the disk direction theta. For a frozen integer vector
z_j=(u_j+i*v_j)*sqrt(j), replace it by

    Z_j(theta)=exp(i*j*theta/2)*z_j,  1<=j<=7.

Its squared norm remains sum j*(u_j^2+v_j^2), since every phase has modulus
one. The resulting weighted real Grunsky form is still nonnegative for
every actual omitted value. This introduces no assumption on f, no
probabilistic choice and no sign tolerance. Static and moving forms may
appear in the same cover, with their respective frozen semantics.

To retain exact cancellations before Arb substitution, put

    V=exp(-i*theta)*w,
    V0=R+(C0+epsilon*mu*s*a)*exp(-i*theta),
    w=w0+epsilon*c, w0=C0+epsilon*mu*s*a+R*exp(i*theta).

Thus V=V0+epsilon*c*exp(-i*theta). As |c|<=B6 on a core box, the whole
Taylor segment is contained in the rectangle about V0 whose two component
radii are epsilon*B6. The global L<R bound of the parabolic proof keeps
this rectangle away from zero: its center displacement from R is at most
25/108+mu*(2/9)*kappa and its perturbation norm is at most sqrt(2)*kappa.
For mu=17/4 this sum is less than 25/108+3*kappa=L. The same argument
keeps the unrotated values in the transform's allowed radial range.

Here is the exact homogeneity identity used by the discovery evaluator.
Give the formal variables s,a,b,c,d,e,alpha,gamma weights

    2,3,4,5,6,7,1,2.

In the inverse/square-root series defining the exterior transform, the
coefficient h[k] has weight k: the input P's coefficient of x^k has
weight k, and inverse, multiplication and binomial square root preserve
that grading coefficient by coefficient. In the Grunsky logarithm, a
monomial contributing to entry (i,j) has total weight N=(i+j)/2, since
each h[k] term contributes total bidegree 2k. Odd i+j entries vanish.
Products preserve the sum of these degrees, proving the assertion for
every logarithm power and every relevant entry.

A formal monomial therefore has

    2u+3v+4bexp+5cexp+6dexp+7eexp+p+2q=N,

where p,q are the alpha,gamma exponents. After the bounded transform
substitution its Laurent factors are

    w^m*conj(w)^n, m=-p+h-q, n=h+q,

for a binomial term h. Thus m-n=-p-2q. The moving vector multiplies
entry (i,j) by exp(i*N*theta); substituting w=exp(i*theta)*V gives

    exp(i*N*theta)*w^m*conj(w)^n
      = exp(i*(N+m-n)*theta)*V^m*conj(V)^n.

By homogeneity, N+m-n equals 2u+3v plus the weight of the one high
coefficient in that column (zero for the constant column, otherwise
4,5,6,7). This is the exponent compiled by the discovery code. The
separately written (same agent) checker instead attaches N=(i+j)/2 to each original entry,
then uses N+m-n after its own Laurent substitution. Both are exact finite
polynomial identities. The original/direct modes are the same identities
with their absent alpha/gamma factors; the norm has phase exponent zero.

Write a compiled term as s^u*a^v*V^m*conj(V)^n*exp(i*k*theta).
During the Taylor expansion theta is FIXED. Wirtinger differentiation
with respect to the original w gives

    d/dw:    m*V^(m-1)*conj(V)^n*exp(i*(k-1)*theta),
    d/dbarw: n*V^m*conj(V)^(n-1)*exp(i*(k+1)*theta),

with the unchanged low-coefficient factors. Indeed dV/dw=exp(-i*theta)
and d(conj V)/dbarw=exp(i*theta). Iterating gives the exact second
Wirtinger derivatives. Real derivatives satisfy du=dw+dbarw and
dv=i*dw-i*dbarw, so the first-order Taylor polynomial and its quadratic
Gram use the SAME unrotated real unknowns Re(c),Im(c) as before.
No rotation of the area inequality or unknown coefficient vector is needed.

The triangle bound |Sww|+2|Swbarw|+|Sbarwbarw|, summed with the proved
coefficient caps, still bounds every real directional second derivative.
Therefore the scalar remainder E and the global quadratic contradiction
of the parabolic proof remain valid, now evaluated on the V-rectangle.
When differentiating in the four core coordinates for a mean-value
matrix enclosure, the exp(i*k*theta) factors and V0 are differentiated
explicitly, while the rigorous box remainder E remains fixed.

Every proposed form's integer coordinates and positive rational weights
are checked. The separately written (same agent) checker reconstructs its own binomial,
geometric and logarithm templates; discovery uses inverse/root recurrences
and the homogeneity grading above. Both use strict Arb arithmetic for all
acceptance. Numerical SDP coordinates are proposals only. The complete
mixed .55 control and separately derived (same agent) identities are implementation controls;
only a complete 0.61230 cover and its exhaustive separate arithmetic replay
could establish the requested candidate bound.
