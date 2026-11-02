# Green function, integral period, and pairwise bound

This is a self-contained restatement and independent read of the mathematical
input in Niedbala Giraudin's PROOF.md, PR 274, immutable commit recorded in
PRIOR_ART.md. Credit for the flux improvement belongs to that work; the
covering-strip coefficient approach is Pinho's and the final moment argument
is Wikström's. This document supplies the analytic input for ANGULAR_LEMMA.md.

All hyperbolic distances use curvature -1, d=2 artanh(delta), where
 delta(a,b)=|a-b|/|1-conjugate(b)a|.

Let 0<c<1, w=-log c, A=pi²/w, and let Omega={c<|z|<1}. The logarithmic strip
S={-w<Re zeta<0} covers Omega under exp. Define phi(z)=(log|z|+w)/w.
Its biholomorphism to the upper half-plane is E(zeta)=exp(i pi(zeta+w)/w).
The positive Dirichlet Green function of S is

 G_S(zeta,beta)=-log |(E(zeta)-E(beta))/(E(zeta)-conjugate(E(beta)))|.

It is zero on the two finite edges, tends to zero at the two strip ends, and
has singularity -log|zeta-beta|. The annular Green function G has the same
normalization. Its lift has one singularity at every lift of its pole.
For any finite collection of distinct lifts beta_j of b,

 G(exp zeta,b) >= sum_j G_S(zeta,beta_j).                  (G1)

To prove this, subtract the right side from the lifted Green function. The
result is superharmonic, with nonnegative singularities at all unremoved
lifts, and its boundary liminf is nonnegative, including both infinite ends.
It is bounded below (the subtracted finite Green functions tend to zero at
infinity and their pole singularities have canceled). The minimum principle,
or first its bounded-strip exhaustion, proves (G1).

For Z,B in the upper half-plane,

 1-|(Z-B)/(Z-conjugate(B))|² =4 Im(Z)Im(B)/|Z-conjugate(B)|²,
 -log x >= (1-x²)/2  (0<x<=1).

Bounding |Z-conjugate(B)| by |Z|+|B| gives, if zeta=x+iy and beta=x_b+iy_b,

 G_S(zeta,beta) >= (1/2)sin(pi phi_z)sin(pi phi_b)
                         sech²(pi(y-y_b)/(2w)).

The two adjacent lifts on either side of y give arguments u and A-u, 0<=u<=A.
Assume sech²(A/2)<=1/3. Then

 sech²u+sech²(A-u) >=2 sech²(A/2).

Indeed sech² has nonnegative second derivative from
u_*=artanh(1/sqrt(3)) onwards. If both arguments exceed u_*, use convexity
and their mean A/2. If one is smaller, its term alone is >=2/3, which bounds
the claimed right side. Consequently, for every a,b in Omega,

 G(a,b)>=sin(pi phi_a)sin(pi phi_b) sech²(A/2).             (G2)

If |a|=|b|=r and their angle difference is theta in [0,2pi], set
sigma=sin²(pi phi(r)), v=A theta/pi, and
p(v)²=sinh²(v/2)/(sinh²(v/2)+sigma). Direct substitution into G_S, using
the adjacent lifts, gives

 G(a,b)>=-log p(v)-log p(2A-v).                          (G3)

## Integral period of a disk-valued annular function

Suppose omega:Omega->D is holomorphic and not identically zero, and omega(a)=0,
|a|=|z|=r. Then

 -log|omega(z)|>=G(z,a)+sigma sech²(A/2).                 (FLUX)

Work first on a smaller closed annulus whose two boundary circles contain no
zero of omega. There are finitely many zeros b there, counted with multiplicity.
The positive superharmonic function u=-log|omega| has the exact decomposition

 u=sum_b G(.,b)+h,

where h is harmonic and has the nonnegative boundary values of u. Thus h>=0.
Here all constants and Green functions temporarily belong to the smaller
annulus. The smaller annuli increase to Omega and their Green functions increase
to G. Their widths, normalized radial coordinates and scalar bounds converge.
The stated strict numerical hypothesis permits the smaller-annulus hypothesis
for all sufficiently close approximations. It is enough to prove the inequality
there and take a limit.

For a circle not meeting a zero, let Fl be the derivative of its normalized
circle mean with respect to log radius. By Cauchy-Riemann (the argument principle
on a zero-free circle), Fl(log|omega|) is an integer winding number.
The radial mean of G(.,b) is piecewise linear, zero on both boundary circles,
and its slope drops by one when passing |b|. Its flux is therefore either
1-phi_b or -phi_b. For h, the mean is linear with slope
F_h=(m_outer-m_inner)/w, where the m's are its two boundary means.
Choose the test circle just outside r. The selected zero a contributes -phi(r),
so the flux of the other zeros plus F_h is congruent to phi(r) modulo one.

Set K=sin(pi phi(r)) sech²(A/2). Equation (G2) bounds each other zero's
Green contribution at z below by K |sin(pi Fl(G_b))|.
The inward boundary normal derivative of G(z,.) in logarithmic strip coordinates
is >=K pi/w: divide (G2) by the pole's distance from either edge and let it tend
to zero. The Poisson formula, whose normalization here is 1/(2pi), gives

 h(z)>=(K pi/w)(m_outer+m_inner)>=K pi |F_h|>=K |sin(pi F_h)|.

The boundary measure in strip coordinates is dy on each edge, of period 2pi;
this accounts for the normalization of the two boundary means.
Finally |sin(pi x)| is periodic modulo integers and subadditive, because
sin(x+y)=sin x cos y+cos x sin y. Summing all contributions except the selected
zero a and using the flux congruence proves (FLUX). If z is itself a zero,
the inequality is automatic. Multiplicities are included by repeated Green terms.

## Pairwise estimate

For any disk-valued omega and two points a,z on |z|=r, postcompose omega with
the disk automorphism taking omega(a) to zero. Apply (FLUX) and (G3):

 delta(omega(a),omega(z)) <= p(v)p(2A-v) exp(-sigma sech²(A/2)).

Let u=v/2. Taking inverse squares and using exp(x)>=1+x yields

 delta^(-2)-1 >= sigma[csch²u+csch²(A-u)+2 sech²(A/2)].

Since cosh d-1=2/(delta^(-2)-1), we obtain

 cosh d(omega(a),omega(z))-1 <= (2/sigma) Phi(u),
 Phi(u)=1/(csch²u+csch²(A-u)+2 sech²(A/2)).

The coincident-point case follows by continuity. This is precisely (PAIR)
in ANGULAR_LEMMA.md, with L(theta)=2Phi(A theta/(2pi))/Psi.

## Whole-disk analyticity and the final norm comparison

If f,g are analytic on the disk with |f|<=|g| on Omega, each annular zero of g
is a zero of f of at least equal order, so f/g extends holomorphically there.
Except for the trivial constant boundary case it maps to D by the maximum
principle. Although this quotient can have poles in |z|<=c, the linear
combinations f-alpha g and g-conjugate(alpha)f are analytic on the entire disk;
therefore all Parseval coefficient identities used in ANGULAR_LEMMA.md apply.
For Bergman A², Parseval followed by radial integration gives
 ||sum a_k z^k||²=sum |a_k|²/(k+1). The modified moment criterion in that file
therefore proves the desired Bergman norm comparison.
