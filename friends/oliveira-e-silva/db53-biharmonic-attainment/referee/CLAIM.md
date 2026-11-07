# DB51 — reflection-even axial attainment for all 3<=p<4 and epsilon>0

UNVERIFIED pending independent full functional/mechanical review and external
Opus 5.5/Fable 5.1 priority/taste. No interest or novelty judgment by Sol.

Published target and identity: Rainer Mandel and Diogo Oliveira e Silva,
*Block-radial symmetry breaking for ground states of biharmonic NLS*,
Calc. Var. 63(2024):45, DOI10.1007/s00526-023-02654-9,
https://d-nb.info/1327451220/34, printed Appendix C pp17–19,
https://arxiv.org/html/2306.03720v1 Appendix C. Their Theorem C.2/printed
Theorem4 attains the AXIAL G=O(2)x{1} level. Attainment of the reflection-even
G1=O(2)xO(1) level is left open below p=4. There is no printed numeric best
value being beaten: the proposed contribution is the following theorem.

For EVERY fixed real p in[3,4) and EVERY epsilon>0 in R3, with COMPLEX H²
inputs and the ORIGINAL quotient q_epsilon(u)/||u||p²,
 mG1(epsilon,p)<2^(1−2/p)mG(epsilon,p),
 q_epsilon=||(Delta+1)u||2²+epsilon||u||2²
 =int[|Delta u|²−2|grad u|²+(1+epsilon)|u|²].
EVERY normalized G1 minimizing sequence is relatively compact in H²; the
infimum is attained. Scaling a minimizer by mG1^(1/(p−2)) solves the FULL
weak equation Delta²v+2Delta v+(1+epsilon)v=|v|^(p−2)v.
For EACH fixed p in[3,4), the authors' existing level bounds imply ALL G1
minimizers are nonradial for sufficiently small epsilon, with a p-dependent
cutoff. No uniform numeric margin/cutoff, sharp level, assertion for2<p<3,
or strict comparison of unrestricted ground states and mG1 is claimed.
DB50's separate near4 proof supplies a common small-epsilon52/53 margin;
DB51 instead provides all positive epsilon and the whole interval, without
claiming that uniform quantitative strengthening.

Code/data on Mini:
friends_pf_diogo/DB51_p3_interaction_binding/ .
PROOF.md gives the full proof, REPORT.md scope/reproduction, PRIOR_ART.md and
final22 source receipts/archives the bounded public comparison. Source archive
receipts specify lossless storage of earlier ZIPs and unchanged DB50 sources.
MANIFEST.json here freezes the local files and executed pod_backup evidence.
All public mathematical checks ran nice10, one BLAS thread on shared phys;
Mini only edited, read public sources, transported, archived and hashed.

Mechanism, with all methods credited: real/imaginary Minkowski selects a REAL
axial minimizer. Herbst–Skibsted1306.6878v1Theorem1.1 (equivalently II
1504.07128v2Theorem1.1) gives SOME exponential L² decay because the eigenvalue0
lies BELOW Ran[(|xi|²−1)²+epsilon]=[epsilon,infinity), with real bounded
potential −mG|w|^(p−2)=o1. Local elliptic estimates give a weighted H4 strip.
For the physical convolution C(s)=(w*Lw)(0,s), its bilateral Laplace average
is the STRICTLY positive transverse form
 ||(Delta_xprime+1+lambda²)Wlambda||2²+epsilon||Wlambda||2²
for some real lambda. Holomorphy/Fourier injectivity rules out all Wlambda
being zero; O2 invariance supplies transverse evenness. Therefore C has a
positive value, and continuity/decay yields an arbitrarily small positive
cross pairing. For EVERY real p>=3, a universal two-real-number inequality
 |A+B|p>=|A|p+|B|p+p(|A|^(p−2)AB+|B|^(p−2)BA)
then gives the strict reflected trial. The proof covers all real p, not
sampled or interpolated values. Exact reflected-residual Brezis–Lieb and
mass concavity give compactness for EVERY complex minimizing sequence.
Compact group averaging gives the full Euler equation. Existing radial
lower bounds versus the authors' G1 upper bound give nonradiality.

Independent own controls, not a full functional proof checker:
verify_laplace_binding_v2.py imports no construction code; six exact cubic
sign/order cases and nonnegative corrected remainder pass. It rebuilds the
ORIGINAL shifted symbol with PLUSlambda², strict cubic gap, and the complete
weighted convolution identity for odd w=z exp(−|x|²/2). For this LINEAR
control f=Lw, the exact Laplace average is
 2pi²lambda²exp(lambda²)(1+lambda4+epsilon).
The unweighted average is ZERO; C(0)<0 and C(8)>0 at epsilon1. Thus neither
positive ordinary mean nor pointwise kernel positivity is assumed.
verify_real_power_binding_v3.py separately checks the universal derivative
and Taylor sign decomposition for ALL p>=3 and strict-binding derivative;
it explicitly rejects p5/2,A=B1 by4sqrt2−7<0. JSON and complete logs PASS.
Reproduce with python3 -u verify_laplace_binding_v2.py and python3 -u
verify_real_power_binding_v3.py, in a clean CPU directory with SymPy.
A finite symbolic PASS does NOT prove the functional decay, Fubini, Bochner
holomorphy, reflection splitting, weak equation or all-sequence quantifiers.

Failure disclosed: the FIRST draft used a FALSE cubic subtraction identity.
A separately written verifier rejected it BEFORE any claim. Failed source,
log and ABANDONED_FARFIELD_DRAFT.md are frozen as discovery history and
REJECTED. Correcting the remainder made the entire far-field/sharp-decay
argument unnecessary. The current proof uses ONLY SOME published exponential
decay, no genericity, nonzero axial far-field amplitude, complex characteristic
quadric, sharp critical rate or numerical PDE profile. Later checker v1/v2
symbolic-normalization failures and successful v3 are also retained.

Worries requiring independent audit: confirm the exact published exponential
theorem hypotheses; weighted H4 and Laplace/Fubini/integration by parts;
Banach holomorphy/Fourier injectivity; real minimizer extraction and full
Euler equation; the all-real-power sign proof; reflected complex residuals
and EVERY-sequence compactness; original radial-rate nonradial quantifiers.
The result may be implicit in classical reflection/binding arguments;
external Opus/Fable alone assesses priority and author interest. Bounded
public searches locate no same theorem but do not prove priority. No author
error, private inputs, empirical holdout, contact, publication or pod change.
