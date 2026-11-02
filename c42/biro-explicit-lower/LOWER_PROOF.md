# An explicit instance of Biró's strict lower bound

Candidate, unrefereed. This note quantifies the method of András Biró,
“An improved estimate in a power sum problem of Turán”, Indagationes
Mathematicae 11 (2000), 343–358, DOI 10.1016/S0019-3577(00)80003-8.
It does not claim a new method or a stronger qualitative theorem than
Biró's published result. The first-escape geometry, summing the Newton
identities, and the attractive fixed point below are his ideas. The
explicit estimates and constant in this note are derived here.

Author-hosted source read: https://users.renyi.hu/~biroand/pdfs/Turan1.pdf .
See PRIOR_ART.md for the live table and current upper-bound submissions.

## Statement and certificate parameters

Put

    δ = 2^(-4096),       q = 1/2 + δ,
    η = 2^(-512),        λ = 2^(-2048),
    Z = 2^(-252),        ε = 2^(-240),       σ = 2^(-48).

**Candidate theorem.** For every integer n>=1 and every complex tuple
z_1=1,z_2,...,z_n, at least one of its first n power sums has modulus
strictly larger than q. Consequently R_n>q in the compact normalization
max|z_j|=1, and

    C42 = limsup R_n >= 1/2 + 2^(-4096) > 1/2.

The limsup conclusion is >=q, not necessarily >q. No assertion about
lim R_n, extremal profiles, or optimality is made.

The frozen numerical artifact is inputs/lower_certificate.json. The
separate exact checker verifies all numerical comparisons used below,
using rational arithmetic. It does not formalize the analytic proof.

## 1. Two exact coefficient identities

Suppose, towards a contradiction, that

    S_l = sum_(i=1)^n z_i^l,     |S_l|<=q   (1<=l<=n).

The case n=1 is impossible since S_1=1>q, so n>=2. Define

    B(x)=product_(i=2)^n(1-z_i x)=sum_(j=0)^(n-1) b_j x^j,
    b_0=1,    b_n=0,
    C_t=sum_(j=0)^t b_j,        A_t=sum_(j=0)^t |b_j|.

In particular C_0=A_0=1. Formal differentiation gives

    x B'(x) = B(x) sum_(l>=1) (1-S_l)x^l.

Indeed x B'/B=-sum_(i=2)^n sum_(l>=1)z_i^l x^l, and z_1=1.
Comparing degree t, for 1<=t<=n, yields

    C_(t-1)-t b_t = sum_(j=0)^(t-1) b_j S_(t-j).             (1)

Thus

    |C_(t-1)-t b_t| <= q A_(t-1).                           (2)

The series C(x)=B(x)/(1-x) has coefficients C_t. Since

    x C'(x) = C(x) sum_(l>=1) (2-S_l)x^l,

comparing degree t gives, for 1<=t<=n-1,

    2 U_t-t C_t = sum_(j=0)^(t-1) C_j S_(t-j),
    U_t=sum_(j=0)^(t-1) C_j.                                (3)

Write V_t=sum_(j=0)^(t-1)|C_j|. In particular V_t>=1, and

    |2 U_t-t C_t| <= q V_t.                                 (4)

These are finite polynomial identities; no limit or regularity premise
is used.

## 2. First escape of the b increments

Let r=1/sqrt(2). We use the exact numerical bounds

    7/10 < r < 3/4,     q<9/16<r,     r-q>1/8.              (5)

If C_(t-1) is nonzero, b_t is nonzero, and the absolute angle θ_t
between them is <=pi/4, projection onto C_(t-1) gives

    |C_t|>=|C_(t-1)|+r|b_t|.

Consequently, while these angles are <=pi/4,

    |C_t|>=1+r(A_t-1)>=r A_t.

A zero b_t at such a stage is impossible by (2), since
|C_(t-1)|>=r A_(t-1)>q A_(t-1). The same lower bound keeps C_t
nonzero. If all angles through n-1 were <=pi/4, the case t=n of
(2), with b_n=0, would give r A_(n-1)<=q A_(n-1), also impossible.
There is therefore a first k, 1<=k<=n-1, with θ_k>pi/4.

At this k the angle is <pi/2: otherwise the distance
|C_(k-1)-k b_k| would be at least |C_(k-1)|>q A_(k-1).
The distance from C_(k-1) to any point on the ray of b_k is at least
|C_(k-1)| sin θ_k. Therefore, on writing A=A_(k-1),

    r A <= |C_(k-1)| <= (q/r) A = (r+e) A,
    e=δ/r <=2δ.                                            (6)

For every j<k, the later increments through k-1 have projections at
least r times their moduli. Subtracting those lower increments from
the upper bound in (6) proves

    r A_j <= |C_j| <= r A_j+e A       (0<=j<k).              (7)

Summing the actual projections, rather than just their lower bounds,
also gives

    sum_(j=1)^(k-1) |b_j|(cos θ_j-r) <= e A.                (8)

The omitted initial contribution is 1-r>0, so (6) implies

    (1-r)<=e A,     A>1/(8δ)=2^4093.                       (9)

Here we used 1-r>1/4 and e<=2δ. In particular e is positive.

By the triangle and reverse triangle inequalities in (2), (7), and
|C_(t-1)|<=A_(t-1), for 1<=t<=k we have

    A_(t-1)/(8t) <= |b_t| <= 2 A_(t-1)/t.                  (10)

It follows that

    A_t<=product_(j=1)^t(1+2/j)=(t+1)(t+2)/2.              (11)

All A_t are positive and strictly increasing on this range.

## 3. Quantitative radial balance

Call an index j<k bad if cos θ_j-r>=η. Equation (8) implies

    sum_(bad j) |b_j| <= e A/η.                             (12)

For a good index j, put X=|C_(j-1)| and y=j|b_j|. The elementary
distance identity is

    |C_(j-1)-j b_j|^2
      =X^2 sin^2 θ_j+(y-X cos θ_j)^2.

Since X>=r A_(j-1) and r<=cos θ_j<r+η, (2) gives

    |y-X cos θ_j|
      <=sqrt(δ+δ^2+rη+η^2/2) A_(j-1).

To check the expression under the square root, subtract
r^2[1-(r+η)^2] from q^2, and use r^2=1/2 and
q^2=1/4+δ+δ^2. By (7),

    |j|b_j|-(1/2)A_(j-1)| <= b A_(j-1)+e A,
    b=rη+sqrt(δ+δ^2+rη+η^2/2).                            (13)

For a bad index, (10) gives the simpler bound

    |j|b_j|-(1/2)A_(j-1)|<=(5/2)A_(j-1).

Moreover A_(j-1)<=8j|b_j| by (10). Set

    W_t=sum_(j=0)^(t-1) A_j,      M_t=sum_(j=1)^t j|b_j|.

For t<k, summing (13) over good indices and using (12) for bad
indices gives

    |M_t-(1/2)W_t|<=b W_t+t e A(1+20/η).

For t=k, the last summand is bounded by (5/2)A_(k-1), so the bound
valid for all 1<=t<=k is

    |M_t-(1/2)W_t|
      <=b W_t+t e A(1+20/η)+(5/2)A_(t-1) 1_(t=k).          (14)

Counting each |b_j| in W_t explicitly proves

    t A_t=W_t+M_t,     W_t>=t A_t/3.                       (15)

For the second inequality use M_t<=2 W_t, from (10).

By (7), r W_t<=V_t and |V_t-r W_t|<=t e A. For t<k,
||C_t|-r A_t|<=e A. For t=k, the triangle inequality and (10) give

    ||C_k|-r A_k|<=e A+(1+r)|b_k|<=e A+4 A_k/k.

Define R_t=t|C_t|/V_t. It follows from (14)–(15) that

    |R_t-3/2| <= b+(20+60/η)e A/A_t+25/t  (1<=t<=k).       (16)

Here is the complete constant calculation. In the numerator
t|C_t|-(3/2)V_t, subtract r[t A_t-(3/2)W_t] and use (14).
Its absolute value is at most

    r b W_t +t e A(r+5/2+20r/η)
       +((5/2)r+4) A_t 1_(t=k).

Divide by V_t>=r W_t>=r t A_t/3. The e coefficient is
3+15/(2r)+60/η<20+60/η, and the final coefficient is
15/2+12/r<25, using r>7/10. This proves (16) without
an implicit error term.

## 4. A long interval where the balance error is small

Let t_0 be the least t in {0,...,k-1} with A_t>=λ A. It exists.
By (9), A_(t_0)>2^2045. Thus t_0>=2, and (11) implies

    A_(t_0)<=(t_0+2)^2<=4t_0^2,
    t_0>2^1021.                                          (17)

Minimality and (10) give A_(t_0)<3λ A. The upper product bound
in (10), now only between t_0 and k-1, gives

    A/A_(t_0) <= k(k+1)/[(t_0+1)(t_0+2)]
                <=2(k/t_0)^2.

Consequently (k/t_0)^2>1/(6λ)>2^2045, and hence

    k/t_0>2^1022.                                        (18)

The numerical parameters give

    b<=2^(-254),
    20+60/η<=2^518,
    b+2^518 (2δ)/λ+25/2^1021 < Z=2^(-252).                (19)

For the first inequality, δ<=η^2 and η<=1/4 imply
δ+δ^2+rη+η^2/2<=2η. Its square root is <=2^(-255),
and rη<=η<=2^(-255); their sum is <=2^(-254).
The second and third inequalities are rational comparisons. Equations
(16)–(19) prove

    |R_t-3/2|<=Z        (t_0<=t<=k).                       (20)

In particular 7/5<=R_t<=8/5. No enumeration of the possibly enormous
integer k or t_0 is required.

## 5. The summed coefficients become almost parallel

We first justify that U_t,C_t are nonzero and that their absolute
angle β_t is <=pi/8 for 1<=t<=k. Put c=cos(pi/8)>9/10.
Inductively suppose the earlier angles satisfy this bound. Projection
of U_(j+1)=U_j+C_j then gives

    |U_t|>=1+c sum_(j=1)^(t-1)|C_j|>=c V_t.

This holds initially at t=1. If C_t=0 then (4) would imply 2c<=q,
which is false. If the first offending angle were >pi/8, then the
distance |2U_t-t C_t| would be >=2|U_t|sin(pi/8), including the
case of an angle >=pi/2. Equation (4) would imply
q>=2c sin(pi/8)=r, again false. This proves the induction and
also nonvanishing. In particular

    h_t=|U_t|/V_t satisfies 9/10<=h_t<=1.                  (21)

The squared version of (4) gives, for t_0<=t<=k,

    cos β_t >= [4h_t^2+R_t^2-q^2]/(4h_t R_t)
             >= F(h_t)-2(Z+δ),
    F(h)=(2h^2+1)/(3h).                                  (22)

For completeness the numerical perturbation bound in (22) is as
follows. Write the fraction as h/R+R/(4h)-q^2/(4hR).
At R=3/2,q=1/2 it is F(h). Changing R by at most Z changes its
three terms in absolute value by at most Z/2,Z/3,Z/20,
respectively, for 9/10<=h<=1,7/5<=R<=8/5. The respective
coefficient bounds are 10/21<1/2, 5/18<1/3 and
1/[16(9/10)(7/5)(3/2)]<1/20. Changing q^2 by
δ+δ^2 changes the fraction by at most δ, since δ<=1 and
4(9/10)(7/5)>2. Their total is <=Z+δ, which is even
smaller than the stated bound.

The projection inequality for U_t+C_t, with

    w_t=|C_t|/(V_t+|C_t|)=R_t/(t+R_t),

gives h_(t+1)>=h_t+w_t(cos β_t-h_t). Since

    F(h)-h=(1-h^2)/(3h)>=(1-h)/3,

and w_t>=1/t for t>=4 and R_t>=7/5, the deficit g_t=1-h_t
satisfies

    g_(t+1)<=(1-w_t/3)g_t+2w_t(Z+δ).

Set a=6(Z+δ). Since a(1-w_t/3)+2w_t(Z+δ)=a, the recurrence reads

    g_(t+1)-a<=(1-w_t/3)(g_t-a),

and because 1-w_t/3>0 the same holds for positive parts:
(g_(t+1)-a)^+<=(1-w_t/3)(g_t-a)^+. Iterating, using 0<w_t<1,
(g_(t_0)-a)^+<=g_(t_0)<=1 and w_t>=1/t, proves

    g_k<=a+(g_k-a)^+<=a+product_(t=t_0)^(k-1)(1-1/(3t)).   (23)

The product has a completely algebraic estimate: for every t>=1,

    (1-1/(3t))^3 <= t/(t+1),

because 27t^4-(3t-1)^3(t+1)=18t^2-8t+1>0. Cubing
the product and telescoping therefore bounds it by t_0/k.
By (18), the product is <2^(-340). Finally

    6(Z+δ)+2^(-340) < ε=2^(-240).

We have proved

    h_k>=1-ε.                                            (24)

This quantitative contraction replaces the unspecified small functions
in the corresponding part of Biró's argument.

## 6. The actual power sums become close to 1/2 in a weighted mean

In this section put U=U_k, V=V_k, h=h_k and

    w_j=|C_j|/V       (0<=j<k).

These weights are nonnegative and sum to one. Since F(h)>=h,
(22), (24), and Z+δ<=ε/2 give cos β_k>=1-2ε. Thus the
unit directions of C_k and U differ in modulus by at most 2 sqrt ε.
Using |R_k-3/2|<=Z<=ε, h>=9/10, R_k<=8/5, and
ε<=1/100, we get

    |k C_k/U-3/2|
      <= |R_k/h-3/2|+(R_k/h) 2 sqrt ε
      <=3ε+4 sqrt ε <=7 sqrt ε.                          (25)

Divide (3) by U. It follows that

    |sum_(j<k) (C_j/U) S_(k-j)-1/2|<=7 sqrt ε.            (26)

Here is an explicit conversion to the real weights w_j. Put u=U/|U|
and v_j=C_j/|C_j|. All C_j in this range are nonzero. Then
sum_j w_j conjugate(u)v_j=h, and hence

    sum_j w_j |conjugate(u)v_j-1|^2=2(1-h)<=2ε.

Cauchy–Schwarz and (24) give

    sum_j |C_j/U-w_j|
      <=sqrt(2ε)/h+(1/h-1)<=3 sqrt ε.

Since q<9/16, (26) implies the deliberately looser estimate

    |sum_j w_j S_(k-j)-1/2|<=16 sqrt ε.                   (27)

Define d=sum_j w_j |S_(k-j)-1/2|. Again by Cauchy–Schwarz,

    d^2 <= sum_j w_j |S_(k-j)-1/2|^2
        =sum_j w_j |S_(k-j)|^2+1/4-sum_j w_j Re S_(k-j)
        <=δ+δ^2+16 sqrt ε <=18 sqrt ε.

The last inequality uses δ<=sqrt ε and δ^2<=sqrt ε. Since
18<25, we conclude

    d<=5 ε^(1/4)=5*2^(-60).                              (28)

## 7. Transfer the weighted statement back to b, and contradict escape

Let m=floor(σ k). Equations (17)–(18) give k>2^2043, so
σ k>2, and in particular m>=σ k/2 and 1<=m<k.
The lower growth bound in (10) gives

    A/A_(m-1)>=product_(j=m)^(k-1)(1+1/(8j)).

Bernoulli's binomial inequality gives
(1+1/(8j))^8>=1+1/j. Raise the last product inequality to
the eighth power and telescope, to obtain

    A_(m-1)/A <= (m/k)^(1/8) <= σ^(1/8)=2^(-6).           (29)

For m<=j<k, use (7), (10), r>7/10 and V<=k A to get

    |b_j|/A <= (2/(rj)) |C_j|/A
             <= (3k/j) w_j <= (6/σ) w_j.                  (30)

At the early indices use |S_l-1/2|<=q+1/2<2. Combining
(28)–(30) yields

    E := sum_(j=0)^(k-1) |b_j| |S_(k-j)-1/2|
       <= A[2*2^(-6)+(6/σ)*5*2^(-60)]
       = A[1/32+30*2^(-12)] < A/16.                      (31)

The j=0 term, with b_0=1, is included in the early part.
Subtract (1/2)C_(k-1) from the case t=k of (1), and apply (31):

    |C_(k-1)-k b_k| <= (1/2)|C_(k-1)|+A/16.              (32)

But the first escape angle θ_k>pi/4, θ_k<pi/2 gives

    |C_(k-1)-k b_k| >=r |C_(k-1)|.

Together with (6) and (32), this implies

    r(r-1/2) <=1/16.

This is impossible: (5) gives r(r-1/2)>(7/10)(1/5)=7/50,
and 7/50>1/16. The assumed tuple does not exist.

## 8. Normalization, minimum, and limsup

If max_i|z_i|=1, divide the tuple by a component of modulus one and
renumber it first. Every power-sum modulus is unchanged, so the
preceding proof applies. The set of such tuples is compact and the
maximum of the first n power-sum moduli is continuous. Its minimum R_n
is attained; the pointwise strict inequality therefore gives R_n>q.
Taking limsup gives C42>=q>1/2.

Conversely the alternative z_1=1 normalization has the same infimum:
divide any such tuple by a component of largest modulus M>=1; all
power-sum moduli weakly decrease by the factors M^(-l), and the
resulting tuple has maximum modulus one. This also checks consistency
with the definitions in the current upper-bound submissions.

## Verification scope

The exact checker, written separately from this note but by the same
AI agent, reads the frozen numerical artifact,
checks the proof hash, proves the radical bounds by squaring rational
numbers, verifies the parameter estimates in (5), (9), (17)–(20),
(22)–(25), (28)–(31), and checks the polynomial identities underlying
the two telescoping inequalities. A separate exact finite-polynomial
check exercises (1) and (3) on rational complex tuples. Neither check
is a formal proof assistant or an independent human referee.

This is a candidate, unrefereed numerical instantiation of Biró's
existing effective strict lower bound. The gain is extremely small and
does not locate the true constant. It changes no upper bound.
