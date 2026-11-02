# Signed contact harmonic and a one-coefficient outer-factor bound

Unrefereed, 1 November 2026. This extends the contact calculation of the filed
0.44667 argument. The Green/flux input is Niedbala Giraudin's; the covering-strip
coefficient method is Pinho's and moment integration is Wikström's. The present
change keeps the first contact harmonic with its sign, and eliminates the
outer factor's constant/linear coupling by completing a square. No relation
between contact angles in the domain and in the image is assumed.

All angular integrals use normalized measure dtheta/(2pi). Fix kappa=3/25 and
z=19/200. For any two complex numbers m1,m2 with |m1|,|m2|<=1, put

    S=|m1|^2+(6/25)(1-|m2|^2),
    T(theta)=Re(e^(i theta) conjugate(m1))
                +(6/25)[1-Re(e^(2i theta) conjugate(m2))],
    W(theta)=max(S,T(theta)).

For every analytic U on the unit disk and 0<r<1 the lemma is

    integral W(theta)|U(r e^(i theta))|^2 >= z |U_1|^2 r^2.   (1)

Only the linear coefficient is asserted. The hypotheses are weaker than being
moments of a probability measure: the certificate covers all |m1|,|m2|<=1.

## Reduction to a uniform scalar inequality

If |m1|>=31/100, then S>z. If |m2|<=77/100, then S>=
(6/25)(1-(77/100)^2)>z. In either case Parseval proves (1).
Otherwise rotate theta so m2=b is nonnegative real. The changes theta->-theta,
theta->theta+pi preserve the second harmonic and allow both Cartesian
components of m1 to be nonnegative. Writing them x,y gives

    W=max(x^2+y^2+(6/25)(1-b^2),
          x cos(theta)+y sin(theta)+(6/25)(1-b cos(2theta))). (2)

It suffices to cover the rectangular box

    0<=x,y<=31/100, 77/100<=b<=1.

A rotation/reflection preserves |U_1| and analyticity (reflection uses
conjugation of coefficients). The rectangle also contains irrelevant points
with |m1|>31/100; these only enlarge the verified domain.

Whenever S>0, L=log W is continuous. Define its outer factor by

    C(v)=exp[ (1/(4pi)) integral_0^(2pi)
                  (e^(i theta)+v)/(e^(i theta)-v) L(theta) dtheta ].

Then C0>0, C0^2=exp(mean L), and C1/C0=mean(L e^(-i theta))=:d.
Indeed expand the kernel as 1+2 sum_{j>=1}v^j e^(-ijtheta), uniformly
on compact subdisks. The real part is half the Poisson integral of L.
For 0<s<1 apply Parseval to C(v)U(rv) at |v|=s and keep its first two terms:

    integral |C(s e^(i theta))U(rs e^(i theta))|^2
        >= C0^2[|U0|^2+s^2|r U1+d U0|^2].

As s increases to one, the Poisson integral of continuous L converges
uniformly, and U(rs e^(i theta)) converges uniformly. Thus the left side
converges to integral W|U(r e^(i theta))|^2.

For clarity, the Poisson convergence follows by splitting the kernel integral
into a short arc, where uniform continuity bounds the oscillation of L,
and its complement, where the Poisson kernel tends uniformly to zero.
Uniform convergence of U follows from analyticity on a neighborhood of the
closed disk of radius r. Only the modulus of C is used, so no boundary
continuity of its harmonic conjugate is assumed. The square-completion identity

    |v|^2+|u+d v|^2
      =(1+|d|^2)|v+conjugate(d)u/(1+|d|^2)|^2
          +|u|^2/(1+|d|^2)

proves (1) if

    exp(mean log W) >= z[1+|mean(log W e^(-i theta))|^2].    (3)

This uses the constant coefficient to control the linear coefficient rather
than demanding a simultaneous correction for both. Equality between the
contact phases has not been imposed.

## Small parameter region, including S=0

Let a=sqrt(x^2+y^2)<=delta=1/10000. The first harmonic is at least -a.
For b<=99/100, (2) is at least the positive, even function

    p+q sin^2(theta), p=(6/25)(1/100)-delta=23/10000,
    q=(12/25)(77/100)=231/625.

Its explicit even outer factor is A-Bv^2, where
A=(sqrt(p)+sqrt(p+q))/2 and B=(sqrt(p+q)-sqrt(p))/2.
Its constant coefficient squared A^2 exceeds z (checked with Arb), and its
linear coefficient is zero, so Parseval proves (1) directly.

For b>=99/100 put ell=(12/25)(99/100)=297/625. Then

    W >= h_a(theta)=max(a^2,ell sin^2(theta)-a).

At a=0 use sqrt(ell)(1-v^2)/2, whose constant coefficient squared ell/4>z.
For 0<a<=delta, put X=sin^2(theta), X0=a(a+1)/ell, d0=X0/2.
The checker verifies X0<1 and 4ell>(1+a)^2. For 0<=X<=X0,
|X-d0|<=X0/2 gives ell(X-d0)^2<=a^2. For X0<=X<=1,
ell X-a-ell(X-d0)^2 is concave, nonnegative at X0, and its value
at 1 is a^2[1-(1+a)^2/(4ell)]>=0. Consequently

    h_a >= ell(X-d0)^2.

The mean of log(X-d0)^2 is -log(16): the polynomial
v^4-2(1-2d0)v^2+1 has all four roots on the unit circle and on that circle
has squared modulus 16(X-d0)^2. The mean of log|e^(i theta)-eta| is zero
for |eta|=1, obtained from the mean-value identity inside the circle and
its integrable logarithmic limit. Integrability at the finitely many zeros
also justifies integrating the logarithmic inequalities below.

For every bin [u,v] listed by the certificate algorithm, u>=1/2048,
v<=1023/1024. It verifies u>2delta/ell, u>d0, and

    gamma_v=1/v-delta/(ell v^2)>1.

On this bin, (X-d0)^2<=X^2 and ell X-a>0. The function
1/X-delta/(ell X^2) is decreasing for X>2delta/ell. Therefore
h_a/[ell(X-d0)^2]>=gamma_v. A bin has angular measure
(2/pi)(asin(sqrt(v))-asin(sqrt(u))). It follows that

    mean log h_a >= log(ell/16)
       +sum_bins (2/pi)(asin sqrt(v)-asin sqrt(u)) log gamma_v.

The bins are formed by subdividing each consecutive coarse interval with
endpoints 2^-11,2^-10,...,2^-1,1023/1024 into 128 equal rational pieces.
All bins are disjoint. Outside them the ratio is at least one. Arb proves
the displayed bound exceeds log(z). Since h_a is positive, continuous and
pi-periodic, its outer factor is even and has C1=0; the same radial Parseval
limit proves (1). Thus the exceptional endpoint S=0 and a neighborhood of
it require no singular quadrature or limiting assumption about parameters.

## Finite rational box certificate for the remaining region

`signed-cover.json` is a binary partition tree of the stated x,y,b rectangle.
Every internal split is a rational, strictly interior split in one coordinate.
The verifier reconstructs child boxes recursively, which proves exact coverage
without an area calculation. A leaf is one of:

* `S`: its exact minimum S is strictly above z;
* `small`: its exact maximum x^2+y^2 is at most delta^2;
* `grid`: it proves (3) for the entire box by the following bounds.

For a grid leaf use n equal angular cells, theta_j=(2j+1)pi/n and h=pi/n.
On cell j, sin and cos differ from their center values by at most h, and
cos(2theta) differs by at most 2h. Intersect these ranges with [-1,1].
Exact rational parameter intervals and interval multiplication bound both
expressions in (2). The maximum of their lower bounds is a positive bound
w_j^- for W; the maximum of their upper bounds is w_j^+.
Set l_j=log(w_j^-), u_j=log(w_j^+), M_j=(l_j+u_j)/2,
D_j=(u_j-l_j)/2, using directed interval endpoints. Then

    mean L >= (1/n)sum l_j =: L_-,
    |mean(L e^(-i theta))-(1/n)sum M_j e^(-i theta_j)|
       <= (1/n)sum [D_j+|M_j|h] =: E.

The second inequality follows from |e^(-i theta)-e^(-i theta_j)|<=h
and the triangle inequality, cell by cell. Therefore (3) follows from

    exp(L_-) > z[1+( |(1/n)sum M_j e^(-i theta_j)|+E )^2].

All elementary functions and all sums in `verify_signed_cover.py` use outward
Arb balls; inputs and split points are exact rationals. The floating proposal
code is never imported. The frozen tree has 210 grid leaves (4096 cells each),
two S leaves and one small leaf. Its arithmetic verification is a quantitative
certificate for this written proof, not formal verification of the prose.
