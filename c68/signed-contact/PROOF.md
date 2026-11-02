# Candidate C68 >= 8937/20000 = 0.44685

Unrefereed computer-assisted proof, 1 November 2026. No mathematical human
review or proof-assistant formalization is claimed. Arithmetic certificate:
`certificate-44685.json`, model signed_contact_v4, checked from scratch by
`verify_measure.py` and `verify_signed_cover.py`. See PRIOR_ART.md for live
sources and priority limitations.

The analytic input from the filed 0.44667 proof is retained, with explicit
supporting derivations in INPUT_GREEN_FLUX.md and INPUT_ANGULAR.md (copied
unchanged, including their historical weaker conclusions). Only sections 1–2
and the coefficient identity in section 4 of INPUT_ANGULAR.md are needed here.
Historical filenames inside the copied inputs refer to their INPUT_* copies
in this directory.
SIGNED_CONTACT_LEMMA.md supplies the new step; its outer-factor proof does not
use that input's old low-coefficient lemmas. We credit Niedbala Giraudin's
Green/flux bound, Pinho's covering-strip coefficient approach, Wang's
coefficient method, and Wikström's moment integration.

## Analytic coefficient inequality

Write w=-log c, A=pi^2/w, q=exp(-A), Psi=(1+q)^2/(8q),

    sigma(t)=sin^2(pi log t/(2w)), D=Psi/(2sigma), H=sqrt(1+D),
    g(t)=2/(1+H), beta(t)=1-g(t),
    epsilon(t)=(19/200)D/[H(1+H)^2]
              =(19/400)g(t)(1-1/H).

At t=c^2 and t=1, g=epsilon=0 by continuity. The frozen certificate checks
all four Green/Fourier scalar hypotheses of INPUT_ANGULAR.md with kappa=3/25,
and Psi>6. Thus H>2, g<2/3 and 0<=beta-epsilon<=beta<=1.

Let f=sum a_k z^k and u=sum b_k z^k belong to A^2(D) and obey |f|<=|u|
on c<|z|<1. If u is identically zero then f is identically zero. Otherwise
f/u extends across every zero of u in the annulus: domination forces the
vanishing order of f to be at least that of u. For a nonconstant quotient
omega=f/u, the maximum-modulus principle gives a disk-valued annular map.
Fix c<r<1 and t=r^2. Its circle image has a smallest hyperbolic enclosing
disk, center alpha and radius rho. Existence follows from compactness of
the image and properness of the hyperbolic plane. First variation plus
separation shows that its active unit contact directions balance zero;
planar convexity reduces the balancing measure to at most three contacts.
The radius-zero case would make omega constant by the identity theorem.

Let lambda_i be the balancing weights and theta_i any domain preimages of
the contacts. Put m_j=sum lambda_i e^(ij theta_i), so |m_j|<=1, and
S,T,W as in SIGNED_CONTACT_LEMMA.md. The hyperbolic cosine rule and balancing
give exactly

    sum_ij lambda_i lambda_j cosh d(p_i,p_j)=cosh^2(rho),
    sum_i lambda_i cosh d(z,p_i)=cosh(rho)cosh d(z,alpha).

The Green/flux pairwise bound, its proved Fourier majorant, and these two
identities yield, with h=cosh(rho) and zeta_theta=cosh d(omega(theta),alpha),

    h^2<=H^2-D S,
    zeta_theta<=h,
    zeta_theta^2<=h zeta_theta<=1+2D sum_i lambda_i L(theta-theta_i),
    H^2-zeta_theta^2>=D max(S,T(theta))=D W(theta).

These calculations are explicitly expanded in INPUT_ANGULAR.md section 2.
The image disk automorphism has weight v(theta)=1-|T_alpha omega|^2
=2/(1+zeta_theta). Since zeta_theta<=H,

    v-g=2(H-zeta_theta)/[(1+zeta_theta)(1+H)]
       >=D W/[H(1+H)^2].

Here H-zeta_theta=(H^2-zeta_theta^2)/(H+zeta_theta) and both denominators
are bounded above using zeta_theta<=H; all quantities are nonnegative.

Set F=f-alpha u and U=u-conjugate(alpha)f, analytic on the entire disk.
Then |F|^2=(1-v)|U|^2 on the circle. For every coefficient,

    |U_k|^2-|F_k|^2=(1-|alpha|^2)(|b_k|^2-|a_k|^2).

Put x_k=(|a_k|^2-|b_k|^2)_+, y_k=(|b_k|^2-|a_k|^2)_+,
X(t)=sum x_k t^k and Y(t)=sum y_k t^k, including k=0.
The identity implies |U_k|^2>=(1-|alpha|^2)y_k. Parseval and the new lemma
therefore imply

    (1-|alpha|^2)(Y-X)=integral v|U|^2
      >=g integral |U|^2 +epsilon |U_1|^2 t
      >=(1-|alpha|^2)[gY+epsilon y_1 t].

Cancel 1-|alpha|^2>0 to obtain the new inequality

    X(t)<=beta(t)Y(t)-epsilon(t)y_1 t.                 (C)

For a constant quotient, |a_k|=|omega||b_k| at every index, so X=0;
(C) holds because beta-epsilon>=0. This includes unimodular constants.
Taking the inner radial limit extends (C) to t=c^2: the power series are
continuous there and g=epsilon=0. No value at t=1 is needed.

## Rational measure and every moment

The frozen artifact specifies positive rational weights and ordered nodes

    c^2=t_1<...<t_m=R<1, sum_j w_j=R,
    dmu=sum_j w_j delta_(t_j)+1_[R,1] dt.

It is a probability measure with no atom at 1. The checker requires R>=c.
The ordinary lower moments for k>=1 are equivalent to

    A_k=sum_j w_j t_j^k-R^(k+1)/(k+1)>=0.             (A)

The required weighted upper moments for k>=1 follow from

    B_k=R^(k+1)/(k+1)+integral_R^1 g(t)t^k dt
          -sum_j w_j beta(t_j)t_j^k
          +1_(k=1)sum_j w_j epsilon(t_j)t_j >=0.     (B)

At k=1 we discard the nonnegative continuous epsilon contribution.
At k=0 both needed facts are automatic: mu has mass one and beta<=1.
There is no correction to y0 in (C), which is harmless for this step.

All finite assertions are checked using an analytic lower envelope, not
quadrature. For each exact tail cell [a,b] put

    U0=-pi log a/(2w),
    B0=(pi/(2w))(1+(1-b)/2)(1-U0^2/6),
    z0=sqrt(2)B0(1-a),
    ell_ab=2sqrt(2)B0/[z0+sqrt(z0^2+Psi)].

The checker proves 0<U0<sqrt(6), so B0>0. For t in [a,b], delta=1-t,
-log t>=delta(1+(1-b)/2), and sin x>=x(1-U0^2/6) for 0<=x<=U0.
Thus sqrt(sigma(t))>=B0 delta. Rationalizing g and increasing its denominator
after division by delta gives g(t)>=ell_ab(1-t). The formula remains valid
at t=1 by continuity. Each ell_ab is rounded down by Arb. Integrate exactly
with the antiderivative F_k(t)=t^(k+1)/(k+1)-t^(k+2)/(k+2).
The independently written moment checker telescopes the sum
sum ell_ab[F_k(b)-F_k(a)]; it imports no search or baseline checker code.
It verifies (A) for 1<=k<6000 and (B) for 1<=k<1800.

For every k>=6000, the exact condition w_m(6001)>=R proves
sum w_j t_j^k>=w_m R^k>=R^(k+1)/(k+1), closing the first infinite tail.

For the second tail the certificate chooses [a,b]=[999/1000,1249/1250].
It computes a fresh lower slope ell_ab and checks at K=1800 that

    ell_ab(1-b)(b-a)a^K > sum_j w_j t_j^K.

For all k>=K, division by a^k makes each (t_j/a)^k nonincreasing because
t_j<=R<=a. Thus the strict inequality propagates to every k>=K, and
integral_R^1 g(t)t^k dt>sum w_j t_j^k>=sum w_j beta(t_j)t_j^k.
This proves (B) for all remaining indices without extrapolation.

## Norm comparison

Integrate (C) against mu. The coefficients beta for k!=1 and beta-epsilon
for k=1 are nonnegative, so Tonelli and the upper moments give

    integral [beta Y-epsilon y_1 t] dmu <=sum y_k/(k+1)<infinity.

The lower moments and Tonelli also give sum x_k/(k+1)<=integral X dmu.
Consequently sum x_k/(k+1)<=sum y_k/(k+1). Bergman Parseval,
||sum a_k z^k||_2^2=sum |a_k|^2/(k+1), proves ||f||_2<=||u||_2.
Thus a passing certificate establishes the candidate lower bound stated in
the title, conditional only on the unrefereed analytic proof written here
and in the two explicitly retained input derivations.
