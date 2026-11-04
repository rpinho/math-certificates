# Candidate C68 >= 447/1000

Unrefereed computer-assisted analytic proof, 4 November 2026. The programs
verify rational and Arb quantitative hypotheses, not arbitrary prose or
complex analysis. Acceptance verification is separately written (same agent).
No human expert verification, formalization, or novelty judgment is claimed.

Credit: V. Patankar (vidigoat), PR #274, for the retained Green/flux and
enclosing construction; Chunjie Wang for the coefficient approach; Frank
Wikström for moment integration; Ricardo Pinho for the covering-strip,
contact-harmonic and signed outer-factor constructions. A. Schuster's annular
pseudodistance approach is an antecedent cited in the retained paper.

The exact artifacts are certificates/certificate-0447.json and
certificates/row-cover.json. Their hashes and full quantitative receipts are
in logs/verification-final.json. No optimizer is part of acceptance.

## 1. Green, Fourier and balancing input

Put c=447/1000, w=-log c, A=pi²/w, q=exp(-A), Psi=(1+q)²/(8q),
kappa=3/25. For t in (c²,1), put

 sigma=sin²(pi*log(t)/(2w)), D=Psi/(2*sigma), H=sqrt(1+D),
 g=2/(1+H), beta=1-g, Q=D/[H*(1+H)²].

The verifier checks Psi>6 and the following four inequalities at this c:

 sech²(A/2)<1/3,
 16*sinh²(A/4)<2*(1-8*kappa)*Psi,
 tanh²(A/8)>(1+8*kappa)*pi²/64,
 sech²(A/8)<(1-4*kappa)/2.

INPUT_GREEN_FLUX.md proves the retained Green comparison, integral-period
flux bound, compact exhaustion, and conversion to a same-radius distance
bound. INPUT_ANGULAR.md sections 1 and 2 prove from precisely these checked
hypotheses that, for every holomorphic omega:{c<|z|<1}->D,

 cosh d(omega(r e^(i theta)),omega(r e^(i phi)))-1
       <=2D*L(theta-phi),
 L(eta)<= (1-cos eta)/2-kappa*(1-cos(2eta)), t=r².       (1)

Distances have curvature -1. Distinct strip lifts are essential and are
explicit in the retained input; no half-actual-diameter assertion is used.
All integrals below have normalized measure dtheta/(2pi).

For nonconstant omega, its compact circle image has a minimal enclosing
hyperbolic disk with center alpha and radius rho>0. Properness gives
existence: centers escaping every compact set have distances to a fixed
image point tending to infinity, so a minimizing sequence stays compact.
At its contacts the active unit directions balance zero. Otherwise a
separating direction and the first variation of distance strictly decrease
all active distances; compactness then gives a smaller enclosing disk.
Planar convexity reduces a balancing measure to at most three contacts.
Let their weights be lambda_i, their domain angles theta_i, and put

 m_j=sum_i lambda_i exp(i*j*theta_i), h=cosh rho.

Weights are nonnegative and sum to one. Domain angles are not identified
with image directions. The hyperbolic cosine rule and balance give, for
every image point z,

 sum_ij lambda_i lambda_j cosh d(p_i,p_j)=h²,
 sum_i lambda_i cosh d(z,p_i)=h*cosh d(z,alpha).        (2)

The cosine rule follows from the Lorentz scalar product of
(cosh R,sinh R*v); averaging cancels the direction terms.

## 2. The contact-row improvement

Define S=|m1|²+2*kappa*(1-|m2|²) and

 T(theta)=Re(exp(i theta)*conj(m1))
             +2*kappa*(1-Re(exp(2i theta)*conj(m2))).

Averaging (1) twice gives h²<=H²-D*S. But at EVERY contact p_i, (2) gives
the sharper individual necessary inequalities

 h²<=H²-D*T(theta_i).                                (3)

The derivation of the additional moment floor is expanded in
CONTACT_ROW_LEMMA.md. Explicitly, let a=|m1|. At a>0 put
X_i=cos(theta_i-arg(m1)), M=max_i X_i,
q0=sum lambda_i X_i²=(1+Re(m2*conj(m1)²/a²))/2.
Then sum lambda_i X_i=a, and (X_i+1)(M-X_i)>=0 implies
q0<=(M-1)a+M. Hence M>=(q0+a)/(1+a).
The second term of T is nonnegative since |m2|<=1. Thus

 max_i T(theta_i)>=a*M>=J:=a*(q0+a)/(1+a).

At a=0 define J=0. This is continuous because 0<=q0<=1 gives 0<=J<=a.
Combining (3) with the averaged bound gives h²<=H²-D*max(S,J).
For z=omega(r e^(i theta)), let zeta=cosh d(z,alpha)<=h.
Equation (2), followed by (1), gives h*zeta<=H²-D*T(theta).
Since zeta²<=h*zeta and zeta²<=h², it follows that

 H²-zeta²>=D*W(theta), W=max(S,J,T(theta)).            (4)

This uses every contact row, not a new choice of balancing weights.

## 3. Uniform linear-coefficient lemma and its finite certificate

The lemma is: for every contact probability moment pair and analytic
U(z)=sum U_k z^k on D, and 0<r<1,

 mean W(theta)|U(r e^(i theta))|²
       >=z*r²*|U1|², z=23/200.                       (5)

Only coefficient one is asserted. Rotate to make m2=b>=0; reflection and
a pi shift put m1=x+i*y with x,y>=0. Reflection conjugates U's coefficients
and preserves analyticity and |U1|. Covariance positivity for cos(theta),
sin(theta), whose second moments are (1+b)/2,(1-b)/2 and mixed moment zero,
implies the necessary PSD inequality

 1-b²-2*(1-b)*x²-2*(1+b)*y²>=0.                     (6)

It follows either by taking the determinant of their covariance matrix or
by minimizing E|v0+v1 cos(theta)+v2 sin(theta)|² over v0,v1,v2.
At b=1 it forces y=0. We use only necessity; no realization theorem is needed.
For a=sqrt(x²+y²)>0, the explicit floor is

 J=[a²+((1+b)x²+(1-b)y²)/(2a)]/(1+a).               (7)

If a>=17/50, S>=289/2500>z. If b<=7/10, S>=306/2500>z.
Thus it suffices to cover 0<=x,y<=17/50, 7/10<=b<=1, subject to (6).

Where S>0, W is positive continuous. Its outer factor is

 C(v)=exp{(1/2)*mean[(exp(i theta)+v)/(exp(i theta)-v)*log W(theta)]}.

Kernel expansion gives C0>0, C0²=exp(mean log W),
d=C1/C0=mean(log W*exp(-i theta)). Apply Parseval to C(v)U(rv) on
|v|=s and keep coefficients zero and one. Let s increase to one:

 mean W|U(r e^(i theta))|²
   >=C0²[|U0|²+|rU1+dU0|²]
   >=C0²/(1+|d|²)*r²|U1|².                         (8)

The first limit uses uniform Poisson convergence of continuous log W and
uniform convergence of U(rs e^(i theta)); a short-arc/complement split of
the Poisson kernel proves the former. No boundary continuity of a harmonic
conjugate is assumed. The second inequality follows by expanding

 |v|²+|u+dv|²=(1+|d|²)|v+conj(d)u/(1+|d|²)|²+|u|²/(1+|d|²).

Thus the finite certificate proves exp(mean log W)>z*(1+|d|²).

The rational binary tree covers the root rectangle exactly. Every split is
strictly interior and both children are reconstructed from the parent. Its
four possible leaf conditions are:

* PSD: the maximum of the left side of (6) is strictly negative. The maximum
  is at x=xl,y=yl,b=bl: the x,y derivatives are nonpositive, and its b
  derivative is -2b+2x²-2y²<0 throughout the root rectangle, since .7>.34².
* Constant: a rigorously computed lower bound for max(S,J) exceeds z.
* Small: xh²+yh²<=delta², delta=1/1000000; the analytic proof below applies.
* Grid: the entire parameter box satisfies (8)'s scalar criterion by Arb.

For a box put al=sqrt(xl²+yl²), ah=sqrt(xh²+yh²). The bounds are

 Slo=xl²+yl²+(6/25)(1-bh²), Shi=xh²+yh²+(6/25)(1-bl²),
 Jlo=[al²+((1+bl)xl²+(1-bh)yl²)/(2ah)]/(1+ah),
 Jhi=min(ah,[ah²+((1+bh)xh²+(1-bl)yh²)/(2al)]/(1+al)).

At al=0 use Jhi=ah; at ah=0 both J bounds are zero. Nonnegative numerators
and ordered denominators justify every bound, and J<=a justifies the min.
All endpoints are rounded outward.

Divide the circle into n cells centered at theta_j=(2j+1)pi/n with half-width
h0=pi/n. Taylor's theorem bounds cosine by its midpoint value plus/minus
|sin(theta_j)|h0+h0²/2, sine by plus/minus |cos(theta_j)|h0+h0²/2,
and cos(2theta) by plus/minus 2|sin(2theta_j)|h0+2h0². Intersect with [-1,1].
Interval multiplication, (7), and maxima give 0<wlo<=W<=whi on each entire
cell and parameter box. Put lj=lower(log wlo), uj=upper(log whi),
Mj=(lj+uj)/2, Ej=(uj-lj)/2. Then

 mean log W>=mean lj,
 |mean(log W exp(-i theta))|
   <=|mean Mj exp(-i theta_j)|+mean(Ej+|Mj|h0).

The second estimate is the triangle inequality and
|exp(-i theta)-exp(-i theta_j)|<=h0, cell by cell. Arb verifies a strictly
positive difference between exp(mean lj) and z times one plus the square
of that upper harmonic bound. No quadrature estimate is accepted as exact.

For the small region, the old even minorant remains valid because W>=max(S,T).
If b<=999/1000, W>=p+q1 sin²theta, where p=(6/25)(1-b)-a>0 and q1=(12/25)b.
Its even outer factor is A0-B0 v² with A0=(sqrt(p)+sqrt(p+q1))/2.
Then A0²=(p+q1/2+sqrt(p(p+q1)))/2>=3/25-delta/2>z, so Parseval proves (5).
If b>=999/1000, put ell=(12/25)(999/1000)=2997/6250 and
h_a=max(a²,ell sin²theta-a). At a=0 the factor sqrt(ell)(1-v²)/2 gives
constant-square ell/4>z. For 0<a<=delta, put X=sin²theta,
X0=a(1+a)/ell, d0=X0/2. The checked inequalities X0<1 and
4ell>(1+a)² imply h_a>=ell(X-d0)². On [0,X0] use |X-d0|<=X0/2;
on [X0,1] the difference ell X-a-ell(X-d0)² is concave with nonnegative
endpoint values; at one it is a²[1-(1+a)²/(4ell)].
The polynomial v^4-2(1-2d0)v²+1 has four unit-circle roots and squared
modulus 16(X-d0)² on the unit circle. The integrable logarithm of distance
to any unit-circle root has mean zero, by the interior mean-value identity
and its logarithmic limit. Hence mean log(X-d0)²=-log16.

Subdivide each successive interval with endpoints 2^-17,...,2^-1,16383/16384
into 512 equal rational bins [u,v]. They are disjoint. Checks give u>d0,
u>2delta/ell and gamma_v=1/v-delta/(ell v²)>1. On each bin (X-d0)²<=X²
and 1/X-delta/(ell X²) decreases, so h_a/[ell(X-d0)²]>=gamma_v.
The bin's angular mass is (2/pi)(asin sqrt(v)-asin sqrt(u)). Outside the bins
the ratio is at least one. Therefore

 mean log h_a>=log(ell/16)+sum_bins mass*log gamma_v>log z.

Arb verifies this last strict inequality with all rational side conditions.
The positive continuous pi-periodic h_a has an even outer factor, so C1=0;
Parseval proves (5). All logarithmic zeros in the polynomial comparison are
integrable. This covers the singular endpoint and its full neighborhood.
The frozen tree has 265 grid, 17 PSD, four constant and one small leaf.

## 4. Coefficients on the whole disk

Let f=sum a_k z^k and u=sum b_k z^k be in A²(D), with |f|<=|u| on the
annulus. If u is zero then f is zero. Otherwise domination cancels all
annular poles of omega=f/u. A nonconstant quotient maps into D by the
maximum-modulus principle. The constant case is addressed below.
For each r choose the contact center alpha above. The disk automorphism
weight v(theta)=1-|T_alpha omega|²=2/(1+zeta), and (4) imply

 v-g=2(H-zeta)/[(1+zeta)(1+H)]
    >=D*W/[H*(1+H)²]=Q*W.                          (9)

Indeed H-zeta=(H²-zeta²)/(H+zeta), H+zeta<=2H and 1+zeta<=1+H.
Set F=f-alpha*u and U=u-conj(alpha)*f, both analytic on the WHOLE disk.
Pointwise |F|²=(1-v)|U|², and expansion at every coefficient gives

 |U_k|²-|F_k|²=(1-|alpha|²)(|b_k|²-|a_k|²).

Let x_k=(|a_k|²-|b_k|²)_+, y_k=(|b_k|²-|a_k|²)_+ and X=sum x_k t^k,
Y=sum y_k t^k, including index zero. Then |U_k|²>=(1-|alpha|²)y_k.
Using (5), (9) and Parseval gives

 (1-|alpha|²)(Y-X)=mean v|U|²
   >=g mean |U|²+z*Q*t|U1|²
   >=(1-|alpha|²)(gY+epsilon*y1*t), epsilon=z*Q.

Cancel the positive factor to obtain

 X(t)<=beta(t)Y(t)-epsilon(t)y1*t.                  (10)

Algebra gives Q=(g/2)(1-1/H). Since Psi>6, H>2, g<2/3 and
epsilon<(z/2)g. Thus beta-epsilon>1/3-z/3>0 everywhere.
A constant quotient with modulus at most one has X=0, so (10) follows from
these nonnegative weights, including unimodular constants. At t=c² define
g=epsilon=0; radial continuity extends (10). No value at t=1 is needed.

## 5. Every moment and both tails

The artifact supplies eight ordered positive rational atoms, t1=c²,t8=R=99/100,
and sum wj=R exactly. Define dmu=sum wj delta_tj+1_[R,1]dt. This is a
probability measure on [c²,1] with no atom at one. For k>=1 require

 A_k=sum wj tj^k-R^(k+1)/(k+1)>=0,
 B_k=R^(k+1)/(k+1)+integral_R^1 g(t)t^k dt-sum wj beta(tj)tj^k
          +1_(k=1)sum wj epsilon(tj)tj>=0.           (11)

The nonnegative continuous epsilon contribution is discarded at k=1.
At k=0 the lower moment is mass one and the upper moment follows from beta<=1.

The finite integral lower bound is global and explicit. Put p=pi/(2w),
B=sqrt(2/Psi), K=2Bp, delta_t=1-t. On [R,1],

 delta_t+delta_t²/2<=-log t<=delta_t/R,
 0<=sin(-p log t)<=p*delta_t/R,
 sin(-p log t)>=p*(delta_t+delta_t²/2)-p³*delta_t³/(6R³).

The verifier checks -p log R<pi, giving nonnegative sine. The log bounds
follow from its positive series and integrating 1/t<=1/R. The sine lower
bound follows by integrating 1-cos x<=x²/2. Let x=B*sin(-p log t)>=0.
Rationalization yields g=2x*sqrt(1+x²)-2x²>=2x-2x². Substitute the lower
sine bound in the positive linear term and the upper sine bound in the
negative square term to obtain

 g(t)>=K*delta_t+[K/2-4p²/(Psi R²)]*delta_t²
                    -[Kp²/(6R³)]*delta_t³.          (12)

No positivity of the polynomial is required for it to be a lower bound.
Every monomial is integrated exactly using

 integral_R^1 (1-t)^j*t^k dt
   =sum_(l=0)^j (-1)^l binom(j,l)*(1-R^(k+l+1))/(k+l+1).

Outward Arb evaluation verifies A_k>0 for 1<=k<6000 and B_k>0 for
1<=k<1800, including all intervening integers. Rational recurrences and the
explicit three monomial integrals are recomputed from the frozen artifact.

For k>=6000 the exact check w8*6001-R=33/200000>0 gives
sum wj tj^k>=w8 R^k>=R^(k+1)/(k+1). This closes the first infinite tail.

For the second tail use a0=999/1000,b0=1249/1250. Put

 u0=-pi log(a0)/(2w),
 B0=pi/(2w)*(1+(1-b0)/2)*(1-u0²/6), z0=sqrt(2)*B0*(1-a0),
 ell0=2sqrt(2)*B0/[z0+sqrt(z0²+Psi)].

Arb checks 0<u0<sqrt6. The logarithm series and sine lower bound give
sqrt(sigma)>=B0*(1-t) on [a0,b0]. The function
2s/[s+sqrt(s²+Psi)] increases for s>=0; substitution s=sqrt2*B0*(1-t)
and increasing the denominator proves g(t)>=ell0*(1-t).
The checker rounds ell0 down and verifies at K2=1800

 ell0*(1-b0)*(b0-a0)*a0^K2 > sum wj tj^K2.           (13)

For k>=K2 divide by a0^k: every atomic ratio (tj/a0)^k is nonincreasing
because tj<=R<=a0. Thus (13) persists for every larger integer k.
The integral on [a0,b0] alone exceeds sum wj tj^k, which exceeds
sum wj beta(tj)tj^k. Equation (11) follows for all remaining k.

## 6. Norm implication and verification boundary

The lower moments mean integral t^k dmu>=1/(k+1). The upper moments mean
integral beta*t^k dmu<=1/(k+1) for k!=1, and
integral (beta-epsilon)*t dmu<=1/2. Every coefficient weight is nonnegative.
Integrate (10). Tonelli applies before integrability is established because
the regrouped right side is a series of nonnegative terms. Its verified
upper moments bound it by sum y_k/(k+1), which is finite by u in A²(D).
Tonelli and the lower moments give

 sum x_k/(k+1)<=integral X dmu
       <=integral[beta Y-epsilon*y1*t]dmu<=sum y_k/(k+1).

Angular orthogonality followed by radial integration gives Bergman Parseval
||f||²=sum |a_k|²/(k+1), ||u||²=sum |b_k|²/(k+1). Subtracting yields
||f||²-||u||²<=0, and hence ||f||<=||u||. This proves the candidate radius
447/1000, subject to the explicitly unrefereed analytic proof above and
the fully written retained Green/Fourier derivations.

Arithmetic does not verify the Green-function maximum principle, first
variation, convexity, outer-function existence or Tonelli's theorem. These
are written analytic steps requiring mathematical review. The exact rejection
controls test the acceptance programs, not arbitrary prose. The retained
0.105 and third-diagonal examples are checked separately; neither is
discarded by an unsupported realizability assumption.
