# Proposed reflection-even axial attainment for every 3<=p<4 and epsilon>0

UNVERIFIED pending independent original-metric analytic/mechanical review
and external Opus/Fable priority/taste. The first draft's cubic identity
was rejected by the separate verifier before any claim. The replacement
below uses the corrected inequality and a weighted Laplace average; it
requires neither a sharp decay rate nor a nonzero far-field amplitude.
The rejected source, log and draft are retained in CONTROL_REPAIR.md.

## Statement

In R3 put G=O(2)x{1}, G1=O(2)xO(1), and retain the ORIGINAL complex H²
quadratic form and metric
 q_epsilon(u)=int[|Delta u|²−2|grad u|²+(1+epsilon)|u|²]
             =||(Delta+1)u||2²+epsilon||u||2²,
 mG=inf_(0!=u inH²_G)q_epsilon(u)/||u||p²,
 m1=inf_(0!=u inH²_G1)q_epsilon(u)/||u||p², 3<=p<4.
The ambient Fourier transform is unitary.

Proposed: for EVERY fixed pair 3<=p<4 and epsilon>0,
                             m1<2^(1−2/p)mG.              (1)
Every Lp-normalized minimizing sequence for m1 is relatively compact in H²,
and m1 is attained. Multiplication of a minimizer by m1^(1/(p−2)) solves the FULL
weak equation
 Delta²v+2Delta v+(1+epsilon)v=|v|^(p−2)v.
For EACH fixed p in[3,4), every such constrained minimizer is nonradial
for all sufficiently small epsilon>0; that cutoff may depend on p. There is no uniform quantitative gap in epsilon, no sharp level,
no numerical small-epsilon cutoff, and no classification or comparison of
unrestricted ground states with m1. This covers the full real exponent interval[3,4), including non-evenp3.
Nothing is asserted here for2<p<3 or at the already-known evenendpointp4.

## 1. Published axial existence and exponential decay

Mandel–Oliveira e Silva2306.03720v1, AppendixC/TheoremC.2 (published CalcVar
63(2024):45, Theorem4) gives attainment of mG for every epsilon>0. At fixed
epsilon the symbol (|xi|²−1)²+epsilon is positive and comparable to1+|xi|4,
so mG,m1>0 and q is a Hilbert norm equivalent to H².

A REAL axial minimizer can be chosen. If u=v+iw, then q(u)=q(v)+q(w) and
 ||u||p²=||v²+w²||_(p/2)<=||v||p²+||w||p².
At least one nonzero real part has quotient at most that of u, hence equals
the infimum. Normalize a real minimizer w by ||w||p=1 and write m=mG.
Averaging arbitrary complex test functions over compact O2 gives the FULL
weak equation
                  L_epsilon w=m|w|^(p−2)w,
 L_epsilon=(Delta+1)²+epsilon.                           (2)

We need only SOME exponential decay. Since H²(R3) embeds in C0 and L-infinity,
V=-m|w|^(p−2) is bounded, real and tends to zero. Also Lw=m|w|^(p−2)w is L², so global
elliptic regularity gives w inH⁴. Apply Herbst–Skibsted1306.6878v1Theorem1.1
(or1504.07128v2Theorem1.1) to the self-adjoint operator
 H=Q(-i grad)+V, Q(xi)=(|xi|²−1)²+epsilon, eigenvalue0.
Here0 is OUTSIDE RanQ=[epsilon,infinity), and V=o(1); these are precisely
the published sufficient hypotheses. Therefore e^(b0|x|)w is L² for some
b0>0. No potential derivative or sharp-critical-rate theorem is invoked.

Local H⁴ estimates for Lw=-Vw have constants uniform in the ball center,
because V is globally bounded. Summing these estimates over unit balls
with exponential weights gives, after reducing b0 if needed,
                   e^(b|x|)D^alpha w inL², |alpha|<=4,   (3)
for some b>0. Explicitly, on each unit ball the H⁴ norm is bounded by a
constant times the L² norm on a fixed larger ball, using ||V||infinity;
weights at points of either ball differ by a fixed factor. A bounded-overlap
cover proves(3). Local Sobolev embedding also gives pointwise exponential
decay. This is a credited standard elliptic consequence, not a new estimate.

## 2. A positive weighted average of reflected cross pairings

For real lambda with |lambda|<b define the bilateral Laplace transforms in
z, with values in the transverse Sobolev spaces,
 W_lambda(x')=int_R e^(lambda z)w(x',z)dz,
 B_lambda(x')=int_R e^(lambda z)Lw(x',z)dz.
Equation(3) and Cauchy–Schwarz in z show W_lambda inH⁴(R2) and B_lambda inL².
For example the leftover factor int exp(2lambda z−2b|z|)dz is finite.
They are real and O2-invariant. Integration by parts in z, justified by
exponential cutoff approximations and(3), gives
 B_lambda=P_lambda W_lambda,
 P_lambda=(Delta_x'+1+lambda²)²+epsilon.                 (4)
In particular its REAL transverse quadratic form is strictly positive:
 int W_lambda B_lambda
   =||(Delta_x'+1+lambda²)W_lambda||2²
      +epsilon||W_lambda||2²>0 ifW_lambda!=0.            (5)
The sign of lambda² in(4) is important: bilateral Laplace transformation
of partial_z² gives PLUSlambda², not minuslambda².

There exists a real lambda in(-b,b) with W_lambda!=0. Otherwise the H²-valued
holomorphic function W_lambda on the complex strip |Re lambda|<b would
vanish on a real interval. The identity theorem, applied to every continuous
linear functional, makes it zero on the whole strip. At lambda=i tau this
is the vertical Fourier transform of w, so Fourier injectivity would give
w=0, a contradiction. Holomorphy follows directly by dominated Bochner
integration on each smaller strip; polynomial factors in z are absorbed
by the available exponential margin. This handles the case W_0=0, such
as an odd axial profile, without a nonvanishing-moment assumption.

Define a real continuous function of s,
 C(s)=(w*Lw)(0,s),                                      (6)
where convolution is the ordinary physical convolution on R3. It tends to
zero at infinity, since both factors are L². Weighted Fubini and transverse
evenness give
 int_R e^(lambda s)C(s)ds
  =int_R2 W_lambda(x')B_lambda(-x')dx'
  =int_R2 W_lambda(x')B_lambda(x')dx'.                   (7)
All integrals are absolutely justified: Cauchy–Schwarz as above puts the
absolute vertical weighted integrals in transverse L² for both w and Lw,
so their product is integrable. O2 invariance includes x'→-x', which is
why the second equality in(7) holds. By(5), choose a real lambda for which
the right side is strictly positive. Consequently C(s0)>0 for some real s0.
No far-field expansion, generic phase, kernel positivity, or numerical
profile is used to obtain this positive cross pairing.

## 3. A universal real-power inequality and strict binding

For EVERY real A,B and EVERY real p>=3,
 |A+B|^p >= |A|^p+|B|^p
       +p(|A|^(p−2)A B+|B|^(p−2)B A).                 (9)
Here is a proof for the whole real exponent range, not sampled exponents.
By homogeneity and symmetry, reduce magnitudes to1,t with0<=t<=1.
For opposite signs let
 Fminus(t)=(1−t)^p−1−t^p+p(t+t^(p−1)).
Then Fminus(0)=0 and
 Fminus'(t)/p=1−(1−t)^(p−1)−t^(p−1)+(p−1)t^(p−2)>=0,
since (1−t)^r+t^r<=1 forr=p−1>=1. This proves the opposite-sign case.
For equal signs let
 Fplus(t)=(1+t)^p−1−t^p−p(t+t^(p−1)).
Its derivative divided byp is
 (1+t)^r−1−t^r−r t^(r−1), r=p−1>=2.
Taylor's formula with nonnegative third derivative gives
 (1+t)^r>=1+r t+[r(r−1)/2]t².
Therefore that derivative is at least
 r(t−t^(r−1))+t²[r(r−1)/2−t^(r−2)]>=0.
All terms have the indicated signs for0<=t<=1,r>=2. Since Fplus(0)=0,
this proves(9). Atp3 the opposite-sign remainder is exactly
 2min(|A|,|B|)²[3max(|A|,|B|)−min(|A|,|B|)]>=0;
the same-sign remainder iszero. The failed draft's negative remainder is
not used. For2<p<3 the same-sign inequality fails even atA=B=1, so no
extension below3 is being inferred.

Return to C(s) from(6). It is continuous and tends0 at infinity, and some
C(s0)>0 by(7). Thus for the fixedp,m one may choose a real s with
                      0<C(s)/m<1/(2p).                 (10)
Indeed continuity from a positive value to a value arbitrarily close to0
passes through every smaller positive value, even if the function later
changes sign. No assumed sign of an unweighted mean is needed.

Set R=-s/2 and
 a_R(x',z)=w(x',z-R), b_R(x',z)=w(x',-z-R), v_R=a_R+b_R.
The sum is EXACTLYG1. Both profiles have q-energy m and Lp-to-powerp mass1,
and both solve(2). Their real q-cross pairing is
 I=q(a_R,b_R)=int a_R Lb_R=C(-2R)=C(s)>0.
The q-Cauchy bound also gives I<=m. Write x=I/m. Integrating(9), the two
nonlinear cross integrals each equal I/m by(2), hence
 q(v_R)=2m+2I, ||v_R||p^p>=2+2pI/m=2(1+p x).
For0<x<1/(2p), the function
 h(x)=2log(1+p x)−p log(1+x)
has h(0)=0 and
 h'(x)=p[1+(2−p)x]/[(1+p x)(1+x)]>0.
Thus (1+p x)^(2/p)>1+x, and
 q(v_R)/||v_R||p²
 <=2^(1−2/p)m (1+x)/(1+p x)^(2/p)<2^(1−2/p)m.
This proves(1) for EVERY fixedp in[3,4) and epsilon>0. The proof of(9)
actually permits p>=3, but no assertion outside the stated target interval
is needed here. No uniform numerical margin or explicit separation is claimed.

## 4. Compactness for every complex minimizing sequence

Fix(epsilon,p) in the stated range. A normalized G1minimizing sequence is bounded in H². Lions
nonvanishing and local Rellich give translations with a nonzero weak profile.
Transverse centers cannot diverge: after selecting a limiting direction,
arbitrarily many fixed O2 rotations produce disjoint balls carrying the
same positive Lp mass. Absorb bounded transverse shifts and translate only
along z; the nonzero weak profile u is EXACTLYG-invariant.

If the axial centers remain bounded, the original weak limit lies inG1.
Writing a for its Lp-to-power-p mass, Brezis–Lieb and quadratic splitting give
 m1>=m1[a^(2/p)+(1−a)^(2/p)], a>0,
forcinga1 and then strong H² convergence. If the axial centers diverge,
evenness supplies u andRu at opposite centers, each massa>0. Subtract both
profiles; the residual is EXACTLYG1 even for complex profiles, without
conjugating Ru. Successive Brezis–Lieb and weak quadratic orthogonality give
0<2a<=1 and
 m1>=2mG a^(2/p)+m1(1−2a)^(2/p)
    >m1[(2a)^(2/p)+(1−2a)^(2/p)]>=m1
by(1), a contradiction including2a1 and nonzero residual mass. Applying the
argument to every subsequence proves relative compactness of EVERY normalized
minimizing sequence at each fixed(epsilon,p). Compact G1-averaging of arbitrary
complex tests gives full Euler Lu=m1|u|^(p−2)u; scaling v=m1^(1/(p−2))u
gives the full PDE (atp3 the multiplier is m1).

## 5. Nonradiality from the authors' existing level bounds

Mandel–Oliveira e Silva Theorem1.3/(1.12),(1.13), atd3,gamma2, gives,
for each fixedp in[3,4),
 m1<=C_p epsilon^(2/p),
 m_rad>=c_p epsilon^(1/2) ifp>3,
 m_rad>=c epsilon^(1/2)|logepsilon|^(-2/3) ifp3.
These LEVEL bounds are already proved without assuming attainment ofm1.
Since2/p>1/2 forp<4, their ratio tends zero. Thus for EACHfixedp in[3,4)
every G1 minimizer is nonradial for all sufficiently small epsilon; this
cutoff need not be uniform as p→4. This is an existence consequence of
credited rates, not a new Knapp construction or radial asymptotic estimate.

## Independent checks, scope and remaining audit

A separate exact verifier must rebuild thep3case of(9) in all sign/order cases, the
real-power derivative decomposition, the PLUSlambda² transverse operator, and the weighted
convolution identity on an explicit odd real axial control with W0=0.
That control is crucial: assuming positive UNWEIGHTED mean for every profile
would leave a gap. The initial failed checker and draft are retained, with
no passing claim based on them. The replacement proof has no far-field or
sharp-decay assumptions hidden as hypotheses.

The functional audit must check the published exponential-decay theorem's
hypotheses, weighted H⁴ regularity, Banach-valued Laplace holomorphy/Fourier
injectivity, all Fubini and integration-by-parts steps, real minimizer
selection, exact reflection residual and all compactness quantifiers. A
finite symbolic PASS does not mechanize those analytical statements.
Priority and author interest are for external Opus/Fable. No author error,
private data, empirical holdout, contact, publication or pod lifecycle change.
