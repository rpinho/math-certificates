# Korenblum lower bound from a retained angular coefficient term

Unrefereed computer-assisted proof, 2026-10-30. Read with
GREEN_FLUX_PROOF.md, ANGULAR_LEMMA.md, SPECTRAL_LEMMA.md, and
CONTACT_SPECTRAL_LEMMA.md.
These files contain the analytic derivation; the checkers verify its numerical
hypotheses, not the validity of arbitrary mathematical prose.

## The theorem and its inputs

Let c be the rational in a passing certificate of model
contact_spectral_v3. Then c is admissible for Korenblum's maximum
principle. No external mathematical
review or formal proof-assistant verification is claimed.

The retained Green-function/flux argument is Niedbala Giraudin's PR 274 input;
GREEN_FLUX_PROOF.md supplies its full derivation, including exhaustion by
compact subannuli, the integral winding-number constraint, and Poisson
normalization. The covering-strip coefficient approach is Pinho's. The final
moment integration is Wikström's method. Immutable sources and baseline
reproductions are recorded in PRIOR_ART.md.

For w=-log c, A=pi^2/w, q=exp(-A), Psi=(1+q)^2/(8q), put

 sigma(t)=sin^2(pi log t/(2w)), D=Psi/(2 sigma), H=sqrt(1+D),
 g(t)=2/(1+H), beta(t)=1-g(t),
 epsilon(t)=(7/100)D/[H(1+H)^2]=(7/200)g(t)(1-1/H).

At t=c^2 and t=1 use g=epsilon=0 by continuity. The four Fourier/flux scalar
conditions are listed and proved sufficient in ANGULAR_LEMMA.md. That file's
minimal-disk/contact-moment proof reduces the coefficient estimate to a
low-coefficient integral inequality. SPECTRAL_LEMMA.md proves the stronger
constant 3/50 in that inequality by an even outer factor.
CONTACT_SPECTRAL_LEMMA.md retains both contact parameters and proves the
constant 7/100 used here. Its uniform scalar geometric-mean bound is proved by
a finite rational rectangle tree plus a separate small-parameter argument;
both interval implementations check it.

Existence of the smallest enclosing hyperbolic disk used there follows from
properness of the hyperbolic plane and compactness of the image circle.
If its active unit directions did not have zero in their convex hull, strict
separation and the first variation of distance would give a common decreasing
direction; compactness then decreases the maximal radius. Planar Caratheodory
gives a balancing measure on at most three contact directions. This also
justifies the contact-measure case division in the earlier proof.

For f=sum a_k z^k, u=sum b_k z^k in A^2(D), with |f|<=|u| on c<|z|<1,
put x_k=(|a_k|^2-|b_k|^2)_+, y_k=(|b_k|^2-|a_k|^2)_+,
X(t)=sum x_k t^k and Y(t)=sum y_k t^k, including k=0 in both.
The geometric coefficient identity and Parseval, proved in ANGULAR_LEMMA.md,
give

 X(t)<=beta(t)Y(t)-epsilon(t)(y_0+y_1 t).               (C)

If the quotient is constant the norm comparison is immediate. Otherwise the
quotient maps the annulus to the disk; the linear combinations used for
Parseval are analytic on the whole disk even if the quotient has inner poles.
Taking the inner radial limit extends (C) to t=c^2. The checker verifies Psi>6,
which gives H>2, g<2/3, and 0<=beta-epsilon<=1 globally.

## Moment measure and exact quantitative hypotheses

The certificate is the positive probability measure

 mu=sum_j w_j delta_{t_j} + 1_[R,1] dt,
 c^2=t_1<...<t_m=R<1, w_j>0, sum_j w_j=R, R>=c.

For every k>=1 the ordinary moment requirement is equivalent to

 A_k=sum_j w_j t_j^k - R^(k+1)/(k+1)>=0.              (A)

Define b_j(k)=beta(t_j)-epsilon(t_j) for k=1 and beta(t_j) for k>=2.
The weighted moment requirement is equivalent to

 B_k=R^(k+1)/(k+1)+integral_R^1 g(t)t^k dt
                         -sum_j w_j b_j(k)t_j^k>=0.   (B)

For k=1 this discards the nonnegative continuous-tail epsilon contribution,
so it is a sufficient condition. The k=0 lower moment is probability mass
one; the k=0 upper moment is automatic because beta-epsilon<=1.

Here is the proved lower bound used for the continuous integral. On any
certificate interval [a,b] within [R,1], set

 U=-pi log a/(2w),
 B=(pi/(2w))(1+(1-b)/2)(1-U^2/6),
 l=2 sqrt(2) B/[sqrt(2) B(1-a)+sqrt(2 B^2(1-a)^2+Psi)].

The checker verifies 0<U<sqrt(6), so B>0. For t in [a,b], delta=1-t,
-log t>=delta(1+(1-b)/2) by its positive Taylor series. Also
sin x>=x(1-U^2/6) for 0<=x<=U: integrate cos x>=1-x^2/2, or use the
alternating sine remainder. Thus sqrt(sigma(t))>=B delta. Rationalizing
g=2 sqrt(2 sigma)/(sqrt(2 sigma)+sqrt(2 sigma+Psi)) and maximizing its
denominator after dividing by delta gives

 g(t)>=l(1-t).                                        (T)

At t=1 the bound follows by continuity. The checker rounds l downward.
For every finite B_k, integrate (T) exactly on each partition cell using
the antiderivative t^(k+1)/(k+1)-t^(k+2)/(k+2). No quadrature is trusted
for any moment assertion. The scalar outer-factor integral is a separate
lower Riemann sum whose rounding and parameter covering are both checked.

## Proofs for the two infinite tails

For k>=K_1, the checker requires w_m(K_1+1)>=R. Therefore

 sum_j w_j t_j^k>=w_m R^k>=R^(k+1)/(k+1),

which proves (A) for all such k.

For (B), choose the certificate interval [a,b] with R<=a<b<1. Compute its
slope l by (T) and check exactly at K_2 that

 l(1-b)(b-a)a^K_2 > sum_j w_j t_j^K_2.

For all t in [a,b], g(t)t^k>=l(1-b)a^k. Also t_j<=R<=a, so after dividing
by a^k every summand on the right is nonincreasing in k. The displayed
strict inequality therefore propagates to every k>=K_2, giving
integral_R^1 g(t)t^k dt>sum_j w_j t_j^k. Since 0<=b_j(k)<=1, (B) follows,
even after discarding its positive R^(k+1)/(k+1) term. This argument covers
every index beyond the finite checks and does not use numerical extrapolation.

## Final norm comparison

Integrate (C) against mu. All coefficient weights beta and beta-epsilon
are nonnegative. Tonelli and the checked upper moments imply

 integral [beta Y-epsilon(y_0+y_1 t)] dmu
       <=sum_{k>=0} y_k/(k+1)<infinity.

The ordinary lower moments and Tonelli then give

 sum_{k>=0} x_k/(k+1)<=integral X dmu<=sum_{k>=0} y_k/(k+1).

Normalized Bergman Parseval says ||sum a_k z^k||_2^2=sum |a_k|^2/(k+1).
This is precisely ||f||_2<=||u||_2, proving admissibility of c.
