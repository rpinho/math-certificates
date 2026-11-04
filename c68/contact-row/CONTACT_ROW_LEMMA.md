# Contact-row moment correction (candidate, unrefereed)

Written derivation before the corresponding search. All angular integrals
use normalized measure. Credit: V. Patankar's flux lemma and enclosing
argument; Pinho's contact and signed-harmonic construction; Wang's coefficient
approach; Wikström's moment integration. This document asserts no certified
numerical constant yet.

Retain the notation in the preceding signed-contact proof. Let lambda_i be
the balancing weights of actual contacts p_i of a minimal hyperbolic disk,
with center alpha, radius rho and h=cosh(rho). Let theta_i be their domain
preimages. Set m_j=sum lambda_i exp(i*j*theta_i), D=Psi/(2*sigma), H²=1+D.
The retained pairwise majorant is

 cosh d(omega(theta),p_i)-1 <= 2D L(theta-theta_i),
 L(theta) <= (1-cos(theta))/2 - kappa*(1-cos(2theta)), kappa=3/25.

The balancing identity holds for every point z, including each contact:

 sum_j lambda_j cosh d(z,p_j)=h*cosh d(z,alpha).

At z=p_i the right side is h². Therefore, for EACH i of positive weight,

 h² <= 1+2D sum_j lambda_j L(theta_i-theta_j)
     <= H²-D*T(theta_i),
 T(theta)=Re(exp(i theta)*conj(m1))
              +2*kappa*(1-Re(exp(2i theta)*conj(m2))).

The second term of T is nonnegative because |m2|<=1. Write a=|m1|.
If a>0, set X_i=cos(theta_i-arg(m1)), so sum lambda_i X_i=a and

 q=sum lambda_i X_i²=(1+Re(m2*conj(m1)²/a²))/2.

Let M=max_i X_i. For each i, -1<=X_i<=M, and hence
(X_i+1)*(M-X_i)>=0. Expanding and averaging gives

 q <= (M-1)*a+M, so M >= (q+a)/(1+a).

Consequently max_i T(theta_i)>=a*M>=a*(q+a)/(1+a). Define

 J=a*(q+a)/(1+a) for a>0, and J=0 for a=0,
 S=|m1|²+2*kappa*(1-|m2|²), Srow=max(S,J).

Then h²<=H²-D*Srow. The old pointwise argument also gives
cosh² d(omega(theta),alpha)<=H²-D*T(theta). Combining them yields

 H²-cosh² d(omega(theta),alpha)
       >= D*max(S,J,T(theta)) = D*Wrow(theta).

The old positive denominator estimate is unchanged. Thus v-g >= Q*Wrow,
where v=1-|T_alpha omega|², g=2/(1+H), Q=D/[H*(1+H)²].

This is a joint first/second moment calculation: q is the quadratic moment
in the first-moment direction. Its positivity also follows from the 3-by-3
Toeplitz contact moment matrix. Rotating to m2=b>=0 and m1=x+i*y gives

 a=sqrt(x²+y²),
 a*q=((1+b)*x²+(1-b)*y²)/(2*a),
 J=(a²+((1+b)*x²+(1-b)*y²)/(2*a))/(1+a).

The probability moment matrix additionally requires

 M=[[1,conj(m1),conj(m2)],
    [m1,1,conj(m1)],
    [m2,m1,1]] >= 0.

This is the Gram matrix of 1,z,z² for the contact probability measure.
Its Schur complement, equivalently covariance positivity for cos and sin,
additionally requires

 2*x²/(1+b)+2*y²/(1-b)<=1  (b<1),
 y=0 and x²<=1 (b=1).

This follows from covariance positivity for cos(theta),sin(theta): their
second moments after this rotation are (1+b)/2 and (1-b)/2, their mixed
moment is zero, and their means are x,y. Its determinant is nonnegative.
Equivalently (1-b²)-2*(1-b)*x²-2*(1+b)*y²>=0. Necessity, not sufficiency
for realizable balanced contacts, is all the certificate may use.

If a positive scalar z satisfies the uniform outer-factor criterion

 exp(mean log Wrow) >= z*(1+|mean(log Wrow*exp(-i theta))|²),

then the signed-contact radial Parseval and square-completion proof yields
integral Wrow|U(r exp(i theta))|² >= z*r²*|U1|². No higher diagonal
coefficient claim follows. The new candidate would then replace 19/200 by z
in the coefficient/moment chain. A full parameter certificate and moment
certificate, including both tails, remain necessary.

In matrix language, the retained two outer coefficients give the positive
matrix G*[[1+|d|²,conj(d)],[d,1]] on (U0,rU1), where G=exp(mean log Wrow).
Its Schur complement in the first entry is G/(1+|d|²). This is the specific
valid small-matrix correction used here; it does not assert a third diagonal.

Counterexample distinction: at m1=1/50,m2=1, the old floor is 1/2500 while
J=1/50. The retained 0.105 example must be evaluated with this new floor;
PSD alone does not reject its moments. At m1=0,m2=1, J=S=0 and Wrow is
(12/25)*sin²(theta), so the naive third-diagonal counterexample is retained.
