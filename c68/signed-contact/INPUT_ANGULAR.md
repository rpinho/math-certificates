# A Fourier majorant and a coefficient correction

Unrefereed analytic derivation, 2026-10-30. This replaces the simplex/enclosing
step of Niedbala Giraudin's PR 274 while retaining its Green/flux input.
Every integral in theta below uses normalized Lebesgue measure dtheta/(2 pi).

Let w=-log c, A=pi²/w, q=exp(-A), Psi=(1+q)²/(8q),
sigma=sin²(pi log t/(2w)), t=r², and

    Phi(u)=1/(csch²u+csch²(A-u)+2 sech²(A/2)).

Set kappa=3/25. Assume the following explicitly checked scalar hypotheses:

    sech²(A/2) <= 1/3,
    16 sinh²(A/4) <= 2(1-8 kappa) Psi,
    tanh²(A/8) >= (1+8 kappa) pi²/64,
    sech²(A/8) <= (1-4 kappa)/2.

## 1. Fourier majorant

For theta in [0,2pi], u=A theta/(2pi), put L(theta)=2 Phi(u)/Psi. Then

    L(theta) <= (1-cos theta)/2 - kappa(1-cos 2theta).       (FM)

Proof. By symmetry take 0<=u<=A/2.
From the definition Phi(u)<=sinh²u. Also, as in PR 274,

    Phi(A/2+x) <= (Psi/2) sech²x.

For completeness its denominator is >=8q cosh(2x)+8q/(1+q)²,
which is >=16q cosh²x/(1+q)²=2 cosh²x/Psi.
If u<=A/4, the right side of (FM) is
sin²(pi u/A)[1-8 kappa cos²(pi u/A)], at least
4(1-8 kappa)u²/A². Since sinh u/u increases, the second scalar
hypothesis bounds 2 sinh²u/Psi by this quantity.
For A/4<=u<=A/2 set x=A/2-u and y=pi x/A.
The right side is cos²y(1-8 kappa sin²y).
For x<=A/8 it is at least 1-(1+8 kappa)y². The third hypothesis,
with tanh x/x decreasing, gives sech²x<=1-(1+8 kappa)y².
For A/8<=x<=A/4 the right side is at least (1-4 kappa)/2,
whereas sech²x<=sech²(A/8). The last hypothesis applies.
All endpoint values follow by continuity. This proves (FM).

The elementary monotonicities used here follow directly by differentiation.
For sinh u/u, the derivative numerator u cosh u-sinh u has derivative
u sinh u>=0 and starts at zero. For tanh x/x, the negative derivative numerator
tanh x-x sech²x has derivative 2x sech²x tanh x>=0. The sine lower chord
sin y>=2y/pi on [0,pi/2] follows from concavity. Near the midpoint,
cos²y(1-8 kappa sin²y)=1-(1+8 kappa)sin²y+8 kappa sin⁴y
is at least 1-(1+8 kappa)y². On y in [pi/8,pi/4], its two nonnegative
factors are at least 1/2 and 1-4 kappa, respectively.

## 2. Minimal disk and its contact measure

Let omega map the annulus to the disk. By PR 274's Green/flux argument,
for two domain angles theta,phi on the circle,

    cosh d(omega(theta),omega(phi))-1
        <= (Psi/sigma) L(theta-phi).                      (PAIR)

Choose a smallest enclosing hyperbolic disk of the compact image of the circle.
If its radius is zero, the conclusion below is immediate. Otherwise let alpha
be its center, rho its radius, h=cosh rho, and p_i contact points. There are
at most three contacts and nonnegative lambda_i summing to one such that
the contact unit direction vectors v_i satisfy sum lambda_i v_i=0.
This follows from the first variation of distance and planar convexity:
otherwise a separating direction would strictly decrease every active distance.
Let theta_i be any domain preimage of p_i and m_j=sum lambda_i exp(ij theta_i).
The hyperbolic cosine rule gives the identities

    sum_ij lambda_i lambda_j cosh d(p_i,p_j) = h²,
    sum_i lambda_i cosh d(z,p_i) = h cosh d(z,alpha).

Define D=Psi/(2 sigma), H=sqrt(1+D). Integrating (PAIR) over the contact
measure and applying (FM) gives

    h² <= H²-D S,
    S=|m_1|²+2 kappa(1-|m_2|²).

For any image point z=omega(theta), put zeta=cosh d(z,alpha).
We have zeta<=h and h zeta<=1+2D C(theta), where
C(theta)=sum_i lambda_i L(theta-theta_i).
Since zeta<=h, we also have zeta²<=h zeta<=1+2D C. Hence

    H²-zeta² >= D max(S,T(theta)),
    T(theta)=Re(exp(i theta) conjugate(m_1))
             +2 kappa[1-Re(exp(2i theta) conjugate(m_2))].  (GAP)

Indeed zeta²<=h² and zeta²<=1+2D C, and (FM) gives
1-2C>=T. In particular h<=H; this already recovers the old enclosing bound.

## 3. A uniform low-coefficient bound

For ANY analytic U(z)=sum U_k z^k on the disk and any m_1,m_2 as above,

    integral max(S,T(theta)) |U(r exp(i theta))|²
        >= (9/320)(|U_0|²+|U_1|² r²).                    (LC)

Here is an elementary proof, including constants. Put a=|m_1|, b=|m_2|.
If a>=17/100, S>=289/10000>9/320. If b<=15/16, then
S>=2(3/25)(1-(15/16)²)=93/3200>9/320. Either case proves (LC) by Parseval.
Otherwise a<17/100, b>15/16; write theta_0=arg(m_2)/2,
x=sin²(theta-theta_0), and ell=4 kappa b>9/20.
We have max(S,T)>=max(a²,ell x-a). Set x_0=a(a+1)/ell<1 and d=x_0/2.
Because 4ell>9/5>(117/100)²>=(1+a)²,

    max(a²,ell x-a) >= ell(x-d)²    (0<=x<=1).           (POLY)

On [0,x_0], use |x-d|<=x_0/2 and 4ell>=(1+a)².
On [x_0,1], the difference ell x-a-ell(x-d)² is concave;
its endpoint values are nonnegative (the value at 1 is
 a²[1-(1+a)²/(4ell)]). This proves (POLY).
Now 16(sin²(theta-theta_0)-d)² is the squared modulus of a polynomial
P(exp(i theta)) of degree four whose constant coefficient has modulus one
and whose linear coefficient is zero. Explicitly, up to a unit scalar,

    P(z)=z^4-2(1-2d)exp(2i theta_0)z²+exp(4i theta_0).

Thus Parseval gives integral (x-d)² |U|² >=
(|U_0|²+|U_1|² r²)/16. Since ell/16>9/320, (LC) follows.

## 4. Stronger coefficient estimate

Put g(t)=2/(1+H), and

    epsilon(t)=(9/320) D/[H(1+H)²]
              = g(t)(9/640)(1-1/H).

The radius weight v(theta)=1-|T_alpha omega(r exp(i theta))|²
is 2/(1+zeta). From (GAP), zeta<=H and

    v(theta)-g(t)
      =2(H-zeta)/[(1+zeta)(1+H)]
      >= D max(S,T(theta))/[H(1+H)²].

Let f=sum a_k z^k, g0=sum b_k z^k (g0 denotes the second function,
not the scalar g(t)), with |f|<=|g0| on the annulus. Set
F=f-alpha g0 and U=g0-conjugate(alpha) f. On the circle,
|F|²=(1-v)|U|². Write x_k=(|a_k|²-|b_k|²)_+,
y_k=(|b_k|²-|a_k|²)_+, X=sum x_k t^k, Y=sum y_k t^k, including k=0.
The exact coefficient identity gives

    |U_k|²-|F_k|²=(1-|alpha|²)(|b_k|²-|a_k|²),
    |U_k|² >= (1-|alpha|²)y_k.

Apply (LC) to U, integrate |U|²-|F|²=v|U|², and use Parseval:

    Y-X >= g(t)Y+epsilon(t)(y_0+y_1 t).

Consequently

    X(t) <= beta(t)Y(t)-epsilon(t)(y_0+y_1 t), beta=1-g.  (NEW)

The case of constant omega also satisfies (NEW): at each coefficient
|a_k|=|omega||b_k|, so X=0 and the right side is nonnegative because
beta-epsilon>=0 for the numerical c under consideration, as checked.
At t=c² define g=epsilon=0 by continuity.

## 5. Modified moment criterion

A probability measure mu on [c²,1], without an atom at 1, suffices if

    integral t^k dmu >=1/(k+1)                       (k>=0),
    integral beta t^k dmu <=1/(k+1)                  (k>=2),
    integral (beta-epsilon)t dmu <=1/2.              (k=1)

The k=0 upper condition holds automatically because beta-epsilon<=1.
For our c the checker proves Psi>6. Then H>=sqrt(1+Psi/2)>2,
g<2/3, and epsilon<(9/640)g, so beta-epsilon>0. Tonelli and (NEW) therefore give the norm
comparison exactly as in Wikström's criterion. When checking k=1, the verifier
may discard the positive epsilon contribution of the continuous tail and use
only its atomic contributions. All other infinite-tail arguments are unchanged.

The scalar hypotheses and every moment require exact interval checking.
This is a new analytic input, not a claimed optimization of the old framework.
