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
