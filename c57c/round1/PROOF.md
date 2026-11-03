# Candidate, unrefereed C57c certificate proof

All489994 leaves of the twelve-part artifact passed the separately
implemented Arb checker. This document collects every analytic reduction
and finite-cover argument. Classical area/Grunsky and complex analysis
inputs remain explicit; no independent human review or novelty judgment.

# Candidate C57c proof: a parabolic Bloch coefficient domain

**Candidate, unrefereed. Complete finite cover and separate checker passed; see verification.json.**
The proposed statement is U >= R=6123/10000=0.61230. This file proves the
reduction to the finite statement; it makes no claim that an incomplete
builder cover establishes that statement. No novelty judgment is made.

Credit: Frank Wikström, arXiv:2610.34580v1, supplies the normalization,
bounded-image transform, Grunsky framework, equation-(9) center and equation-(12) phase congruence.
The moving-phase witnesses extend that phase congruence to seven indices. The
predecessor job combined his bounded-image transform with complex 2x2
forms and proposed U>=0.61229. Here the center additionally depends on a6;
higher forms, the area theorem and a bounded Taylor remainder eliminate
a5,a6,a7,a8 from the numerical cover. Public comparison: PRIOR_ART.md.

## 1. Normalization and the complete coefficient domain

Write U=inf_f R_f/|f'(0)| over univalent maps on the unit disk, where R_f is
the inradius of the image. It suffices to consider normalized univalent
functions in B={(1-|z|^2)|f'(z)|<=1, f(0)=0, f'(0)=1}.

Indeed, given a univalent F and 0<r<1, g(z)=F(rz) is holomorphic beyond
the closed unit disk. The continuous function (1-|z|^2)|g'(z)| vanishes
on its boundary and attains a positive maximum M at an interior point p.
With phi(z)=(p+z)/(1+conj(p)z), the normalized function

    f(z)=[g(phi(z))-g(p)]/[(1-|p|^2)g'(p)]

belongs to B, using (1-|z|^2)|phi'(z)|=1-|phi(z)|^2. Its image is a
similarity of g(D), and R_g=M R_f<=R_F. Also M>=r|F'(0)|. A lower R for
all f in B therefore gives R_F>=r|F'(0)|R; take r increasing to one.

Expansion of the Bloch inequality at zero first gives a2=0, by its linear
term in every direction, and then |a3|<=1/3, by its quadratic term. A
rotation makes a3=-s, 0<=s<=1/3. Put

    f(z)=z-s z^3+a z^4+b z^5+c z^6+d z^7+e z^8+... .

Integrating the derivative bound radially gives |f(z)|<=atanh|z|.

For any normalized univalent F, H(z)=F(z)/z is nonzero on D and has a
holomorphic logarithm with value zero at zero. The exterior map

    h(zeta)=zeta exp[-log H(zeta^-2)/2]

is holomorphic, odd, nonzero and asymptotic to zeta. Equal h-values imply
equal F(zeta^-2)-values, hence equal or opposite zeta; opposite points
have opposite nonzero h-values. Thus h is exterior univalent.

The classical strong Grunsky inequality is an explicit external theorem:
if -log((h(zeta)-h(eta))/(zeta-eta))=sum B_ij zeta^-i eta^-j,
then every finite matrix M_ij=sqrt(i*j) B_ij is a contraction. Therefore

    ||z||^2+Re(z^T M z)>=0                         (G)

for every complex vector z. The classical exterior area theorem is another
explicit external theorem: h=zeta+sum h_n zeta^-n implies

    sum n |h_n|^2 <= 1.                            (A)

Applied at indices {1,3} to f, the Grunsky matrix is
[[0,sqrt(3)s/2],[sqrt(3)s/2,-3a/2]]. A unitary diagonal congruence makes
its off-diagonal and lower diagonal entries nonnegative without changing
singular values. Its largest eigenvalue is <=1 only if
3|a|/2<=1-3s^2/4. Consequently |a|<=2/3-s^2/2.

Conjugation and f(z)->-f(-z) respectively conjugate a,c and negate a,c,
while preserving s. They preserve the proposed center below in the same
way. Thus a may be put in the closed first quadrant, with c unrestricted.

## 2. Area inequality and explicit caps

Expand (f(z)/z)^(-1/2) through degree seven. The exterior coefficients are

    h1=0, h3=s/2, h5=-a/2,
    h7=-b/2+3s^2/8,
    h9=-c/2-3sa/4,
    h11=-d/2-3sb/4+3a^2/8+5s^3/16,
    h13=-e/2-3sc/4+3ab/4-15s^2a/16.

These follow by inserting U=-s z^2+a z^3+b z^4+c z^5+d z^6+e z^7 in
1-U/2+3U^2/8-5U^3/16; higher powers have degree at least eight.
Dropping the remaining nonnegative terms of (A) gives

    A(Y)=1-3s^2/4-5|a|^2/4
         -7|h7|^2-9|h9|^2-11|h11|^2-13|h13|^2 >= 0,              (1)

where Y=(Re b,Im b,Re c,Im c,Re d,Im d,Re e,Im e).

The following uniform caps hold for every actual f:

    |b|<=1, |c|<=1, |d|<=2, |e|<=3.                (2)

For b, |b|<=3s^2/4+2/sqrt(7)<=1/12+2/sqrt(7)<1. For c,
|c|<=3s|a|/2+2/3<=1. Solving the h11 identity gives
|d|<=2/sqrt(11)+1/2+1/3+5/216<2. Solving h13 similarly gives
|e|<=2/sqrt(13)+1/2+1+5/36<3. The finite checker rechecks these scalar
comparisons in Arb. The caps are used only to bound Taylor remainders;
the final quadratic inequality is checked over all real Y.

## 3. Center and transforms

Use the old center

    C0=s[(2/5-|a|^2/3-s^2/5) Re a
         -i(25/24-3|a|^2/2-s^2/4) Im a].

Both weights are nonnegative on the parameter domain and at most 25/24,
so |C0|<=25/108. Define the exact constants and new center

    kappa=3/1000, mu=17/4, t=124993/125000,
    epsilon=kappa exp[-2500(1/3-s)^2-100|a|^2],
    C=C0+epsilon*(c+mu*s*a),
    w0=C0+epsilon*mu*s*a+R exp(i theta),   w=w0+epsilon*c.

The area theorem also gives |xi|<=2/3 for xi=c+3*s*a/2, directly from
9|h9|^2<=1. Since s|a|<=2/9, the actual perturbation obeys
|c+mu*s*a|<=2/3+(11/4)*(2/9)=23/18. Thus |C|<=25/108+(23/18)kappa<R.
Every actual circle point is nonzero and has modulus <atanh(t).

For the interval rectangles and fictitious squares used below a single
stronger bound L=25/108+3*kappa suffices. The full Taylor rectangle around
w0 has perturbation norm at most (17/18+sqrt(2))*kappa<3*kappa.
For the simple forms, xi is enclosed in the square with each component
in [-2/3,2/3]; then |xi+(mu-3/2)s*a| is at most
2*sqrt(2)/3+11/18<3. The checker verifies R>L and R+L<atanh(t), so all
these rectangles avoid zero and lie within the stated radial domain.
It may validate the broader range 0<=mu<=6, for which the same 3*kappa
bound follows from mu*(2/9)+sqrt(2)<=4/3+sqrt(2)<3 and
|mu-3/2|*(2/9)+2*sqrt(2)/3<=1+2*sqrt(2)/3<3. The frozen parameter
is the exact rational 17/4; it is not optimized by the checker.

For an omitted w, use three normalized univalent functions:

- F0=f.
- F1=f/(1-f/w). Its denominator never vanishes, and a Möbius map preserves
  injectivity and the normalization.
- Let g(z)=f(tz)/t, q=(t/atanh(t))^2, gamma=q*conj(w)/w and
  alpha=t/w+gamma*w/t. Put F2=g/(1-alpha*g+gamma*g^2).

For the last transform, |g|<atanh(t)/t=1/sqrt(q). Its denominator roots
are w/t and t/(gamma*w). The first is omitted by g, and the second has
modulus greater than 1/sqrt(q), because |w|<atanh(t). If two F2-values
agree, cross multiplication gives (g1-g2)(1-gamma*g1*g2)=0. The second
factor is nonzero by |gamma*g1*g2|<1, so g and then F2 are injective.
Their series begin z+..., proving the normalization.

Apply (G) to each transform, at all indices 1,...,7. For mode m choose
integer pairs (u_j,v_j) and set z_j=sqrt(j)(u_j+i v_j). A positive rational
weight times each resulting inequality remains nonnegative. For any finite
list of such forms define

    T(w,Y)=sum weight*(||z||^2+Re(z^T M_m(w,Y) z)) >= 0.           (3)

All weights, integer vectors, modes and the nonnegative area weight zeta
are data in the frozen artifact; no eigensolver decision is trusted.

## 4. Exact series semantics and affine dependence

For mode m set t_m=1,gamma_m=0 for modes 0,1, and t_m=t,gamma_m=gamma
for mode 2. Let alpha_m=0 for mode 0 and
alpha_m=t_m/w+gamma_m*w/t_m otherwise. Define the polynomial series

    P(x)=1-s t_m^2 x^2+a t_m^3 x^3+b t_m^4 x^4
           +c t_m^5 x^5+d t_m^6 x^6+e t_m^7 x^7.

The corresponding exterior square-root coefficients h[k] are the
coefficients through degree seven of

    sqrt(P(x)^(-1)-alpha_m*x+gamma_m*x^2*P(x)).                  (4)

The ratio (h(zeta)-h(eta))/(zeta-eta) equals 1-Q(u,v), where
u=zeta^-1,v=eta^-1 and

    Q(u,v)=sum_{i,j>=1, i+j even} h[(i+j)/2] u^i v^j.

Thus B_ij is the coefficient of u^i v^j in sum_{l=1}^7 Q^l/l,
for 1<=i,j<=7. Higher l cannot contribute. These formulas explicitly
specify all matrix entries used in (3), without higher unknown coefficients.

Every entry is affine in b,c,d,e when w is held fixed. Their first possible
series degrees in P are 4,5,6,7. A product of two has degree at least eight,
beyond (4); likewise a product of two high h[k], k>=4, has total i+j>=16,
beyond the required i+j<=14. Hence write, exactly,

    T(w,Y)=Re S0(w)+Re[Sb(w)b+Sc(w)c+Sd(w)d+Se(w)e],             (5)

where S0 includes the real norm constants from (3). Dependence on s,a,t is
suppressed. The checker reconstructs (4) using literal binomial series and
the Q-power logarithm, separately from the builder's recurrences.

### Exact Laurent substitution before interval evaluation

The rational coefficient templates in (4) can be combined before interval
substitution. Write S=s*t_m^2, A=a*t_m^3, B=b*t_m^4, C=c*t_m^5,
D=d*t_m^6 and E=e*t_m^7 inside a formal template. For a monomial with
powers s^u*a^v*b^j*c^k*d^l*e^n*alpha^p*gamma^r, put
K=2u+3v+4j+5k+6l+7n. In the bounded mode, substitution gives the finite sum

    sum_{h=0}^p binom(p,h) t^(K+p-2h) q^(h+r)
         *s^u*a^v*b^j*c^k*d^l*e^n
         *w^(-p+h-r)*conj(w)^(h+r).

This is the binomial expansion of alpha=t/w+(q/t)*conj(w) and
gamma=q*conj(w)/w. In the direct mode t=1,q=0; in the original mode
alpha=gamma=0. Combining identical monomials is an exact identity, not a
new inequality. The checker separately reconstructs (same agent) all formal
coefficients using geometric inverse powers, binomial square-root powers
and logarithm powers. Its alpha/gamma Laurent powers are expanded by
literal polynomial multiplication. The builder uses inverse/root
recurrences and the explicit binomial substitution above. All 140 nonzero
rational monomial terms across the indexed entries agree in the diagnostic
comparison, but the checker does not import or trust the builder templates.

For integer m,n, Wirtinger derivatives of w^m*conj(w)^n follow by lowering
the appropriate exponent and multiplying by that exponent. The functions
are smooth on the proved nonzero rectangles. Directly combining these
formal derivatives preserves exact cancellations before Arb evaluation.
The separately assembled (same agent) real sparse-polynomial Gram is unchanged.

## 5. A uniform Taylor remainder in the sixth coefficient

Treat w=u+i v as two real variables. For each derivative ij in {uu,uv,vv},
on the full rectangle

    w0+[-epsilon,epsilon]+i[-epsilon,epsilon],

compute an Arb upper bound

    L_ij >= |(S0)_ij|+|(Sb)_ij|+|(Sc)_ij|
                         +2|(Sd)_ij|+3|(Se)_ij|.

The checker can sharpen (2) within a core box. Let s_-<=s<=s_+,
A_-<=|a|<=A_+, and B_+=1-3*s_-^2/4-5*A_-^2/4. For the frozen rectangular map, use the nonnegative real and imaginary
endpoints in Section7 to obtain A_-<=|a|<=A_+. The following calculation
uses only those inequalities and the remaining area budget.
Every displayed area summand is at most the remaining budget B_+. Thus

    B5=3*s_+^2/4+2*sqrt(B_+/7),
    B6=3*s_+*A_+/2+2*sqrt(B_+/9),
    B7=3*s_+*B5/2+3*A_+^2/4+5*s_+^3/8+2*sqrt(B_+/11),
    B8=3*s_+*B6/2+3*A_+*B5/2+15*s_+^2*A_+/8+2*sqrt(B_+/13)

bound |b|,|c|,|d|,|e| by solving each explicit h7,h9,h11,h13 identity
and applying the triangle inequality, in that order. Replacing any Bj
by its minimum with the already proved global cap preserves validity.
The checker uses these nonnegative upper bounds in place of (1,1,2,3)
in the derivative sum. It can shrink the w rectangle to component radii
epsilon*B6, since |c|<=B6. The same Taylor integral argument then applies.
Every endpoint, square root and cap is enclosed by Arb; the checker uses
an separately written (same agent) scalar endpoint calculation. The box remainder
upper bound is still held fixed in all subsequent core derivatives.

By (2), or these sharper bounds, this bounds |T_ij| for every actual Y on the straight segment
from w0 to w0+epsilon*c. The real symmetric Hessian's operator norm is
at most max(L_uu,L_vv)+L_uv: each absolute row sum has this bound.
The integral form of the second-order Taylor remainder therefore gives

    T(w0+epsilon*c,Y)
      <= T(w0,Y)+epsilon*(Re c*T_u(w0,Y)+Im c*T_v(w0,Y))
                    +E*((Re c)^2+(Im c)^2),                     (6)

One valid choice is E>=epsilon^2*(max(L_uu,L_vv)+L_uv)/2.
A second valid directional bound uses Wirtinger derivatives. For each
complex scalar S_j define S_zz=(S_uu-2i S_uv-S_vv)/4,
S_zbar=(S_uu+S_vv)/4 and S_barbar=(S_uu+2i S_uv-S_vv)/4.
For any complex direction delta of modulus one its second real directional
derivative is S_zz delta^2+2 S_zbar delta*conj(delta)
+S_barbar conj(delta)^2. Its absolute value is at most
|S_zz|+2|S_zbar|+|S_barbar|. Sum this bound over j with weights
(1,1,1,2,3), to obtain L_complex. Thus E>=epsilon^2*L_complex/2
is also valid. Taking the smaller of the TWO rigorously computed upper
bounds preserves validity. All derivatives and bounds are evaluated in
Arb on the full parameter box and full w-rectangle, not by finite differences.

## 6. A global quadratic contradiction

For a fixed nonnegative zeta define P(Y) to be the right side of (6) plus
zeta*A(Y), with the optional nonnegative Bloch terms of Section 6b. By (1) and (3), an actual omitted value on the proposed circle
would satisfy 0<=T(w0+epsilon*c,Y)+zeta*A(Y)<=P(Y).

By (5), P is a real quadratic polynomial in eight real variables. Let
V=(1,Y) and form its symmetric Gram matrix G so that P(Y)=V^T G V.
If -G is positive definite, P(Y)<0 for every real Y, since V is nonzero.
This contradicts the preceding inequality. It excludes every possible
higher coefficient choice at once, with only s,a,theta left to cover.

The separate checker reconstructs G by sparse polynomial multiplication
of the affine forms, using separately constructed (same agent) binomial and logarithm
series. The builder instead uses inverse and square-root recurrences and
inserts Gram coefficients directly. For positivity the checker proposes a
floating Cholesky inverse, converts its entries to exact dyadic rationals,
and checks triangularity and nonzero diagonal. The proposal is therefore
an exactly invertible matrix R. Strict Arb Gershgorin diagonal dominance
with positive diagonal of R^T(-G)R proves positive definiteness. Floating
Cholesky success itself is never acceptance evidence; failed proposals
cause refinement or rejection. The builder uses interval LDL pivots.

For broad boxes the checker may enclose the matrix by a mean-value formula
AFTER the fixed exact congruence. First compute a rigorous box upper bound
E_box for the remainder. Hold E=E_box FIXED when differentiating G in the
four core coordinates. At box midpoint x*, set B(x)=R^T(-G(x;E_box))R.
Its interval Jacobian over the box gives the entrywise enclosure

    B(x) in B(x*) + sum_j (partial_j B)(box) * (x_j-x*_j).

The integral mean-value identity proves this entrywise inclusion. Apply
the same strict Gershgorin test to that enclosure. Fixing E_box is valid:
it majorizes the pointwise remainder everywhere; differentiating a
pointwise upper-bound algorithm instead would require extra derivatives
and is not done. The checker-only core chain rule was separately written (same agent)
and does not use the builder jets. The exact dyadic preconditioner may put the constant
coordinate last; the coordinate permutation is invertible. Numerical SDP
matrices are never proof inputs: the packet contains only positive rank
forms with rational weights and integer complex vectors, plus rational zeta.

A simpler permitted leaf uses one or more {1,3} forms. These entries are
independent of b,c,d,e except through w. The checker encloses
xi=c+3*s*a/2 in the full square [-2/3,2/3]+i[-2/3,2/3]. The area theorem
proves that square contains every actual xi. It evaluates the form at
w=C0+R*exp(i theta)+epsilon*((mu-3/2)*s*a+xi), uniformly over the square.
Thus a negative form gives the same omitted-value contradiction. It may use a direct interval or an explicit mean-value enclosure
in the four covered real coordinates.

For these simple forms the checker can clear denominators. Set
rho=w*conj(w)>0 and H=t_m+q_m*rho/t_m, with q_m=0 in the direct mode
and q_m=q in the bounded mode. Then alpha_m=H/w and gamma_m=q_m*conj(w)/w.
The three entries before index weighting are
B11=-alpha_m/2, B13=(gamma_m+t_m^2*s)/2-alpha_m^2/8,
B33=-t_m^3*a/2-alpha_m^3/24. Multiplication by 8*rho^3 gives

    B11_scaled = -4 H conj(w) rho^2,
    B13_scaled = 4 q_m conj(w)^2 rho^2 +4 t_m^2 s rho^3
                   -H^2 conj(w)^2 rho,
    B33_scaled = -4 t_m^3 a rho^3 -H^3 conj(w)^3/3.

The norm term is multiplied by the same 8*rho^3. These identities follow
from rho/w=conj(w) and can be checked by direct multiplication; no inequality
is introduced. Since the multiplying factor is strictly positive for every
actual circle point, a strictly negative cleared form gives exactly the
same contradiction. In the original mode take H=q_m=0,t_m=1. Using the
polynomial form can reduce interval dependency from reciprocal w values.

## 6a. Finite-radius Bloch coefficient exclusion

A third leaf kind can discard a coefficient box that contains no actual
normalized function in B. This condition is independent of the proposed
circle center and of Grunsky test vectors. It follows directly from the
Bloch derivative bound, the coefficient caps in (2), and Cauchy's formula.

On |z|=4/5, the bound |f'(z)|<=1/(1-|z|^2) is at most 25/9.
Cauchy's coefficient formula applied to f' therefore gives

    n*|a_n| <= (25/9)*(5/4)^(n-1).

For every chosen rational 0<r<=1/4, the derivative tail from n>=9 has
absolute value at most

    Tail(r) = (25/9)*(5*r/4)^8/(1-5*r/4).

This is the sum of a convergent geometric series, since 5r/4<=5/16<1.
Evaluate the derivative at z=i*r. With v=Im(a)>=0 on the covered quadrant,
its displayed coefficients and (2) imply

    Re f'(i*r) >= 1+3*s*r^2+4*v*r^3
                     -5*r^4-6*r^5-14*r^6-24*r^7-Tail(r).

Each subtraction is a lower bound for the real part of that coefficient's
term. For example 4a*(ir)^3 has real part 4*v*r^3. The Bloch inequality
also gives Re f'(i*r)<=|f'(i*r)|<=1/(1-r^2). Consequently the last
lower bound cannot be STRICTLY greater than 1/(1-r^2).

A Bloch-cap leaf records r. The separately written (same agent) checker uses that original
lower-derivative comparison in Arb over the ENTIRE closed box. The builder
uses the algebraically equivalent inequality after division by r^2:

    4*v*r <= (1-3*s)+r^2/(1-r^2)+5*r^2+6*r^3
               +14*r^4+24*r^5+(25/9)*(5/4)^8*r^6/(1-5*r/4).

Strict violation proves the box cannot represent any f in B, for any
higher coefficients or circle angle. It makes no omitted-value claim on
fictitious coefficient tuples. At s=1/3, taking r down to zero in the
necessary inequality gives v=0 (and conjugation gives the analogous
statement for negative v). Arithmetic leaves always use an explicit
positive rational r, not that limiting argument.

## 6b. Quadratic Bloch derivative disks

A higher-form witness may also contain a finite list of `bloch_disks`.
For each, the artifact specifies a positive rational radius r<=1/4,
a complex rational point z with EXACT |z|^2=r^2, and a positive rational
weight lambda. These conditions are checked before any arithmetic leaf.
Use the same Cauchy tail Tail(r) proved in Section 6a. The truncated
derivative is

    H(z,Y)=1-3*s*z^2+4*a*z^3+5*b*z^4+6*c*z^5+7*d*z^6+8*e*z^7.

The omitted derivative terms have absolute sum at most Tail(r). Therefore
for every actual normalized f in B,

    |H(z,Y)| <= |f'(z)|+Tail(r) <= 1/(1-r^2)+Tail(r) = U_r.

Consequently the REAL QUADRATIC polynomial

    Q_z(Y) = [U_r^2-|H(z,Y)|^2]/r^4

is nonnegative. Division by r^4 is positive and only changes its scale.
The constant U_r and every coefficient of H are specified explicitly;
H is affine in b,c,d,e and so Q_z is quadratic in the same eight real
variables Y. Add sum_z lambda_z*Q_z(Y) to P(Y) in Section 6.
The resulting P still majorizes a nonnegative sum for every actual tuple.
Strict negative definiteness of its augmented Gram therefore gives the
same contradiction and the same disk conclusion.

The builder assembles these quadratic matrices by outer products. The
checker separately writes (same agent) H as a sparse polynomial in eight real
variables, multiplies it by its coefficientwise conjugate, subtracts
that product from U_r^2, and inserts each quadratic monomial into the
symmetric Gram. It differentiates the resulting polynomial in the four
core parameters for the same fixed-congruence mean-value enclosure.
No finite difference or floating Bloch-disk matrix is accepted as evidence.
Old witnesses with no such terms are the special case of the empty sum.

## 7. Complete finite cover and the disk conclusion

The v3 artifact uses a different cube map, proved here to contain every
actual normalized function after the same quadrant symmetries.
Set delta=1-3*s>=0 and v=Im(a)>=0. Section 6a gives, for every 0<r<=1/4,

    4*v*r <= delta+r^2*[1/(1-r^2)+5+6*r+14*r^2+24*r^3
                       +(25/9)*(5/4)^8*r^4/(1-5*r/4)].

If delta>=16/81, the already proved bound v<=|a|<=2/3 gives
v<=3*sqrt(delta)/2. If 0<delta<16/81, choose r=(2/5)*sqrt(delta).
Then r<8/45<1/5. Every positive term in the bracket increases with r,
so the bracket is at most its value J at r=1/5. Exact rational arithmetic
(or its separately written (same agent) Arb check) verifies

    1+(4/25)*J < 12/5.

Since r^2=(4/25)*delta, the necessary inequality becomes
(8/5)*v*sqrt(delta) < (12/5)*delta, hence v<3*sqrt(delta)/2.
For delta=0, the same necessary inequality divided by r and followed
as r decreases to zero gives 4*v<=0, so v=0. Thus, in all cases,

    |Im(a)| <= (3/2)*sqrt(1-3*s).                              (P)

The new covered cube and its polynomial coefficient map are

    x in [0,1]^4, u=x0, s=(1-u^2)/3, b0=2/3-s^2/2,
    a=b0*x1 + i*(3/2)*u*x2, theta=2*pi*x3.

Every actual s and first-quadrant a are represented: choose
u=sqrt(1-3*s), x1=Re(a)/b0, and x2=Im(a)/((3/2)*u) when u>0.
Their ranges follow from |a|<=b0 and (P). If u=0 then Im(a)=0,
and set x2=0. This proves surjectivity onto every actual coefficient tuple.
For scaled-Bloch leaves this choice is mandatory at u=0: the canceled
inequality is valid for the selected representative (u=0,x2=0), by the
fixed-function radius limit detailed below. It is not asserted for redundant
representatives (u=0,x2>0), and can fail there. Every actual function has
the selected representative in the complete closed cover, where all
necessary constraints used for its exclusion hold.
The map also represents fictitious tuples with |a|>b0. They need not
correspond to a function, and are safely excluded by an optional a4cap
leaf whenever the ENTIRE closed box violates |a|<=b0.

For that leaf the checker uses the necessary inequality

    x1^2+[(3/2)*u*x2/b0]^2<=1.

All three coordinates are nonnegative, b0 increases as u increases,
and is bounded above by b0(u_upper). Consequently
x1_lower^2+[(3/2)*u_lower*x2_lower/b0(u_upper)]^2>1 excludes every
point in the box. Strict comparison is mandatory. As with Bloch-cap
leaves, this excludes a coefficient tuple and makes no omitted-value
claim about fictitious tuples. The parabolic map is used by formats c57c-bloch-parabolic-v3,
c57c-scaled-bloch-v4 and the frozen c57c-moving-phase-v7.

All earlier Grunsky and Taylor arguments apply to every ACTUAL tuple in
this map. Their global nonzero-circle bound uses the already proved
|a|<=b0. A fictitious tuple outside that disk need not obey the global
center bound. Actual Taylor segments do obey it; interval divisions and
positivity are still evaluated over the whole accepted arithmetic box,
so any such arithmetic acceptance remains a valid uniform enclosure of
its actual subset. No converse claim about fictitious functions is used.

The local remainder caps use |a| lower and upper bounds from the new
rectangular map. For u in [u_-,u_+], s_-=(1-u_+^2)/3 and
s_+=(1-u_-^2)/3. Re(a) is bounded between
(2/3-s_+^2/2)*x1_- and (2/3-s_-^2/2)*x1_+;
Im(a) is between (3/2)*u_-*x2_- and (3/2)*u_+*x2_+.
Sum the squares of those nonnegative endpoints for |a|^2 bounds,
and apply exactly the area identities and triangle inequalities of
Section 5. A negative remaining-budget upper bound means there is no
actual tuple in the box; otherwise its nonnegative upper bound applies.
The checker may take the maximum with zero without excluding any actual
function. Core derivatives are the explicit chain rule for this polynomial
map, separately implemented by the same agent in the checker.

Every leaf is a path of exact coordinate bisections from that cube. Digit
2j selects the lower child in coordinate j and digit 2j+1 its upper child.
The checker requires both children of every internal node, correct ordering,
no duplicate or missing leaf, and complete consumption of the artifact.
All boxes are closed; overlapping faces are checked on both sides.

Each accepted leaf gives either the quadratic contradiction of Section 6,
the simpler uniform form there, a necessary Bloch-coefficient violation
from Section 6a, or the proved fourth-coefficient domain exclusion above. A coefficient tuple of an actual normalized f cannot lie
in the last kind of box. Therefore every actual tuple and angle is covered
by an omitted-value contradiction. If the COMPLETE artifact passes, every
point of the circle |w-C|=R lies in f(D).

The image f(D) is simply connected. If a point p inside that circle were
omitted, the circle would have winding number one around p. Its contraction
to a point inside f(D) would preserve that winding number because p is
omitted, but a constant loop has winding number zero. This contradiction
proves that the entire closed disk is in f(D). Thus R_f>=R. Section 1
transfers the conclusion to arbitrary univalent maps and yields U>=R.

The area and Grunsky theorems, ordinary holomorphic and winding-number
facts, and the normalization argument are mathematical inputs to this
written proof. Arithmetic acceptance does not formalize those theorems or
constitute independent human review. Search and separate checker were
written by the same agent in different implementations.

## Verification status

Complete global coverage, every arithmetic range, nine rejection controls
and a fresh public-source audit passed. See verification.json, results/
and source_comparison.json. Point tests or floating SDP output alone
never supplied acceptance.

## Bounded-duration arithmetic replay

For a large artifact the separately written (same agent) checker can check its exact complete
cover structure and replay arithmetic in disjoint leaf-index ranges. The
index is the exact depth-first leaf count in the same structurally checked
artifact. Each range receipt states the frozen artifact SHA256, every
checker-source hash, the exact interval [lo,hi), and the number of arithmetic
leaves actually checked. To conclude the whole finite statement, the
ranges must cover [0,N) exactly, with no gap or overlap, N equal to the
separately checked (same agent) complete cover's leaf count, and identical artifact
and checker hashes. Every leaf then has the contradiction proved above;
the finite union gives the whole cube. Additional internal checker splits
must include both closed children and do not alter the covered leaf.

verify_c57c_forest.py checks this bookkeeping and rechecks cover
structure. Receipts are records of actual runs, not trusted mathematical
certificate inputs for a fresh reviewer. The standalone full command
replays all arithmetic directly; alternatively every range must be rerun
before aggregating. Range mode is used here solely to obey the Mini's
thirty-minute per-run limit. Its complete .55 control passes, while missing,
overlapping and stale-hash range records are rejected. No selected-leaf
sample, structure-only run, or partial range supports the claimed bound.

## Independent interval Cholesky fallback

After an exact invertible congruence, strict Gershgorin dominance is
sufficient but may be conservative. The checker may instead recursively
construct a lower triangular Cholesky enclosure. At column j define
p_j=B_jj-sum_{k<j} L_jk^2. Require its ENTIRE Arb interval to be strictly
positive, set L_jj=sqrt(p_j), and for i>j set
L_ij=(B_ij-sum_{k<j} L_ik*L_jk)/L_jj. All divisions therefore have a
strictly positive denominator. Induction on j proves that for every actual
real symmetric B in the input enclosure, its exact recursive Cholesky
entries lie in the computed balls. Strictly positive pivots yield
B=L*L^T with an invertible lower triangular L, and hence B is positive
definite. The proof uses symmetry of the exact Gram construction; each
computed lower-triangular entry encloses its exact counterpart. This
checker implementation is separately written and imports no discovery
module. Builder interval LDL acceptance is still never trusted as input.
Known positive, singular and indefinite controls exercise the fallback.

## Optional interpolation of positive duals

A blend leaf stores two static Taylor witnesses, an axis j, and one exact
dyadic coordinate window [l,h]. For x_j in that window define
alpha=(x_j-l)/(h-l). The checker verifies the actual leaf coordinate box
is contained in that window by exact rational endpoint comparisons.
Thus 0<=alpha<=1, and (1-alpha)*T_left+alpha*T_right is a nonnegative
combination of the two necessary Grunsky inequalities at every actual x.
The area and optional Bloch-disk terms are combined with the same weights,
which remain nonnegative. No SDP status is used to justify interpolation.

Let E_left and E_right separately bound the two Taylor remainders on the
entire box. Set E=max(E_left,E_right). Each static witness remains a valid
quadratic majorant after replacing its remainder by E. Their convex
combination therefore remains a quadratic majorant in the eight real
unknown coefficients, with Gram

    G(x;E)=(1-alpha(x))*G_left(x;E)+alpha(x)*G_right(x;E).

This exact identity includes the common E term, because the weights sum
to one. The four core derivatives include derivatives of alpha; E stays
fixed at its box upper bound. The same exact dyadic congruence and mean-
value/Cholesky argument applies to this Gram. Inner witnesses must be
static Taylor witnesses, so no recursive or arbitrary signed combination
is admitted. Out-of-window and malformed blends are rejected. The
checker implements the convex polynomial combination separately from
the builder. Pointwise scenario optimization is proposal work only.


---

# Scaled-radius Bloch constraints for the frozen certificate

Candidate and unrefereed. This is an additional necessary-inequality family
for PROOF_C57C_PARABOLIC.md, credited there to Wikström's normalization,
center and Grunsky framework. The complete finite R=0.61230 verification receipt accompanies this packet.
No novelty judgment is made.

Use all the notation and independently proved coefficient caps in that
proof. In particular u=sqrt(1-3s), a=a4=b(s)*x1+i*(3/2)*u*x2,
0<=u,x1,x2<=1, b(s)=2/3-s^2/2. When u=0 select x2=0 as the
representative of the actual tuple: Im(a)=0 by the parabolic lemma and
x2 is then redundant. Every actual normalized function has such a tuple.
For u>0 the representation is unchanged.

Fix rational c in (0,64], rational eta with |eta|<=8 and sigma in {-1,1}.
Put

    B=1/c+4u, r=u/B, tau=eta*r,
    xi=(2tau+i*sigma*(1-tau^2))/(1+tau^2), z=r*xi.

For u>0, 0<r<1/4, |xi|=1, and the ordinary Bloch derivative bound holds
at z. By Cauchy's coefficient formula on |z|=4/5 and |f'|<=25/9,
coefficients of the derivative after its seventh power have tail bounded by

    tail=K*r^8/(1-5r/4), K=(25/9)*(5/4)^8.

The degree-seven derivative polynomial is

    P=1-3s*z^2+4a*z^3+sum_{n=5}^8 n*a_n*z^(n-1).

The triangle inequality gives |P|<=1/(1-r^2)+tail. Therefore

    H(Y)=[(1/(1-r^2)+tail)^2-|P|^2]/r^4 >=0.             (S)

This is a real quadratic polynomial in the same eight unknowns Y as the
area and Grunsky forms. A positive rational multiple may be added to the
quadratic contradiction, since it is nonnegative for every actual omitted
value and every actual normalized function. It does not change the disk
center or eliminate any actual function.

The following formulas remove every division by u before interval
substitution. Write a=A+i*v, v=(3/2)*u*x2, h=r^2*p,
p=-3s*xi^2+4a*r*xi^3, and

    Q(Y)=sum_{n=5}^8 n*r^(n-5)*xi^(n-1)*a_n.

Then P=1+h+r^4*Q and

    H(Y)=H00-2 Re[(1+h)*conj(Q)]-r^4*|Q|^2.             (S2)

For an independently factored expression, put

    J=sigma*(1-eta^2*r^2)/(1+eta^2*r^2),
    E=2eta/(1+eta^2*r^2), so xi=r*E+i*J.

Use 1-3s=u^2, 1+Re(xi^2)=2r^2*E^2,
Re(xi^3)/r=r^2*E^3-3E*J^2 and
Im(xi^3)=3r^2*E^2*J-J^3. Direct expansion of (S) gives

    H00 = 2B^2 +12s*E^2 -8A*(r^2*E^3-3E*J^2)
          +12x2*B*(3r^2*E^2*J-J^3)
          +(3-2r^2)/(1-r^2)^2
          +2K*r^4/[(1-5r/4)*(1-r^2)]
          +K^2*r^12/(1-5r/4)^2 - |p|^2.               (S3)

For clarity, the first term comes from
[2/(1-r^2)-2 Re(-3s*xi^2)]/r^2:
its non-angular part is 2(1-3s)/r^2=2B^2. The remaining
identity [1/(1-r^2)^2-1-2r^2]/r^4=(3-2r^2)/(1-r^2)^2
accounts for the scalar rational term. The two tail terms follow by
squaring 1/(1-r^2)+tail. All denominators in (S2)-(S3) are strictly
positive even at u=0, and every unknown coefficient has a nonnegative
power of r. Thus the expressions and their core-coordinate derivatives
are continuous on the closed parameter cube.

Endpoint justification must be stated separately. For an actual function
with u=0 choose x2=0. Its coefficients s=1/3 and Im(a)=0 are fixed.
Apply the ordinary Bloch bound at radii rho>0, with the same angle rule
tau=eta*rho, then let rho decrease to zero in the normalized expression.
The terms 2(1-3s)/rho^2 and Im(a)/rho vanish exactly. Formula (S3) at
u=0,x2=0 equals that nonnegative limit plus 2/c^2>=0; (S2)'s other terms
have their ordinary continuous limits. Consequently (S) in its canceled
form remains a valid necessary inequality for the selected representative.
For redundant tuples with u=0,x2>0 validity is not asserted or needed:
every actual function is represented by u=0,x2=0 and the complete cover
must include that subset. This distinction is part of the analytic proof.

Discovery code c57c_scaled_bloch.py uses an expanded tau-polynomial H00
and an outer-product Gram. The separate c57c_checker_scaled_bloch.py uses
(S3), the factorization xi=rE+iJ and sparse polynomial multiplication of
Q. It imports no discovery code. All weights and descriptor parameters are
checked exactly; Arb evaluates the whole closed box. The complete cover
checker must check all previous and new leaf forms and every coverage edge.
Value/gradient controls and finite-radius identities are useful diagnostics
but do not replace that exhaustive check or referee review of this proof.


---

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


---

# Composite finite certificate and exhaustive part verification

Candidate, unrefereed; no novelty judgment. A full 0.61230 statement requires
complete global coverage AND every arithmetic leaf of every immutable part.
This supplements PROOF_C57C_PARABOLIC.md, PROOF_C57C_SCALED_BLOCH.md and
PROOF_C57C_MOVING_PHASE.md. It changes only the finite artifact packaging.

The artifact is a manifest and a finite list of gzip JSONL part files.
Every part has the same exact radius, transform parameter, center, bump,
mu and coefficient caps. Supported format tags distinguish optional witness
evaluations but do not change those mathematical parameters. Each part has
its own ordered witness-definition list. A leaf consists of its GLOBAL
binary-bisection path and an index into that part's definition list.
Unused definitions may be removed and referenced indices renumbered before
verification; a separately checked compact artifact is then immutable.
Diagnostic search points are not mathematical inputs.

For a path, start from [0,1]^4. Digit 2j replaces coordinate j's interval
by its closed lower half; digit 2j+1 uses its closed upper half. If that
coordinate is [n/2^d,(n+1)/2^d], the children have pairs (2n,d+1) and
(2n+1,d+1). Thus every endpoint is an exact dyadic rational, independent
of floating arithmetic. Overlapping boundary faces belong to both boxes.

To check global coverage, collect every path from every manifest part,
sort them, and recursively consume the complete list. At prefix p, either
the next path equals p (one leaf), or its next digit must be an even digit
2j. Recursively consume p+(2j), then p+(2j+1). A wrong prefix, odd first
child, missing record or leftover record is rejection. Induction on this
recursion shows that every accepted internal node has both complete
children for the SAME axis. Their boxes cover their parent. The root is
the whole unit cube, so successful consumption proves coverage. Duplicate
leaves, ancestor/descendant overlaps and gaps cannot pass this recursion.
No search stack or approximate volume statistic is trusted.

The separate arithmetic checker reconstructs each leaf box from its global
path and checks precisely the necessary inequality specified by that
part's referenced witness. Every definition is validated, including all
positive weights, vector dimensions, transform modes, coefficient caps,
scaled-radius descriptors and permitted phase rule. The analytic proofs
above apply to that exact box and witness, whether another part supplies
its neighboring boxes or a different Grunsky vector.

The part-only mode makes NO global-coverage claim. A range mode additionally
checks only an exact interval [lo,hi) in the part's leaf order and states
that limited scope. Its record includes the part byte SHA256, every local
checker-source hash, exact mathematical parameters, precision, total leaf
count and number of leaves actually checked. The checker requires the
artifact and its own sources to remain unchanged throughout the pass.
Every internally subdivided leaf requires both closed children.

For a complete verification, arithmetic ranges for each frozen part must
cover [0,N_part) exactly, without gaps or overlaps, and must have identical
part bytes, checker sources, parameters and precision. Their verified-leaf
counts must equal the interval lengths. Every manifest part must appear;
no receipt for an extra part is allowed. Independently recheck the global
coverage recursion described above. It then follows by finite union that
every actual parameter tuple and direction has an accepted inequality.
The omitted-value contradiction and simply connected winding-number
argument of the analytic proof yield U>=R.

verify_c57c_forest.py supplies both a complete fresh verification command
and bounded range commands. Its receipt-assembly mode is bookkeeping of
ACTUAL exhaustive arithmetic runs, not a way to trust arbitrary supplied
receipts as mathematical certificate inputs. A fresh reviewer must rerun
all ranges or use the complete fresh command. Structure-only, selected
leaf checks and unfinished queues never establish a constant bound.

The fast checker changes no mathematical criterion. Its four-component
chain rule omits derivative operations only for exactly zero derivatives;
active derivatives use the same product, inverse and trigonometric chain
rules. Its fixed exact congruence may be multiplied with Arb matrices
instead of Python scalar loops; both evaluate the same R^T(-G)R with
rigorous ball enclosures. Strict positive diagonal/Gershgorin or interval
Cholesky tests are still required. Its phase factor is evaluated directly
as cos(k*theta)+i*sin(k*theta), the identical exponential in the moving-
phase proof. No floating Cholesky proposal itself is acceptance evidence.
The separately written formal-series, Gram and chain-rule implementations
remain distinct from the discovery recurrences and numerical SDP search.
