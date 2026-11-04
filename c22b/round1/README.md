# C22b round 1 release — candidate upper bound 7.090412

The candidate and unrefereed result is

\[
C_{22b}\le\frac{1772603}{250000}=7.090412<\frac{36}{5}.
\]

Historical source-packet replay and all 108 exact expected corruption
rejections passed on macOS and Linux. The verifiers are separately written (same agent);
the release incorporates the two documented prose corrections.

The explicit knot family is `T(2,1104n+3)`, up to mirror, for every
integer `n ≥ 1`. Its specified spatial realizations satisfy

\[
L_n\le\frac{3545553}{500000}(1104n+3)+150,\qquad
\frac{500000}{499951}\le\tau_n<\frac{1000099}{1000000}.
\]

Thickness \(\tau_n\) is a radius. With \(\rho=499951/500000\), the explicit
uniformly scaled family \(\widetilde\Gamma_n=\rho\Gamma_n\) has thickness
at least 1 and

\[
\operatorname{Len}(\widetilde\Gamma_n)
\le\frac{1772602767903}{250000000000}(1104n+3)
+\frac{1499853}{10000}.
\]

This meets the frozen bar directly. Minimum ropelength of a knot type
is at most the length of its unit-thickness realization. Taking the
family limit gives

\[
\frac{1772602767903}{250000000000}
=7.090411071612<7.090412.
\]

The full proof, exact construction, interval certificates, and separately
written (same agent) verifiers are in
[the release packet](README.md).
The release applies the two [prose corrections](ERRATA.md): the missing
Q in Appendix C and the truncated decimal in the frozen README.
The exact construction and verified certificate inputs are unchanged.
This is a proposed proof using stated classical theorems, requiring
mathematical review. It is not a formal proof-assistant result.
No novelty judgment is made.

The finite witness `n=1` is `T(2,1107)`, with

\[
L_1<\frac{248861907}{31250},\qquad
\frac{\operatorname{Rop}_{\min}(T(2,1107))}{1107}
<\frac{13824306585173}{1921875000000}<\frac{36}{5}.
\]

The all-n proof establishes the limiting conclusion; it does not
extrapolate from this finite example.

## Construction and proof coverage

The body combines the four-strand superhelix idea of Huh–Kim–Oh with
the unequal double-helix parameters and method of Youhua Li and Claude.
Its exact parameters are

\[
N=\frac{276}{5},\quad R=\frac{293279789}{100000000},\quad
 a=\frac{193279689}{100000000},\quad i=\frac{3846709}{50000000},\quad
 b=\frac{16209211}{50000000},\quad\lambda=\frac{10001}{10000}.
\]

Two noncoaxial helical axes carry satellites of signed radii `a` and `−i`.
The reference rise is `h=(N−1)b`. One block contains five complete axis
turns and 276 complete minor screw periods. Both phases therefore return
exactly at the block ends. The checker parses `276/5` as an exact fraction
and binds its denominator to the integer closing period; it does not
round a floating twist number to claim closure. Connector radii are
`15/2` and `63/2`; upper clearance is `21/10`. Explicit nested lower
semicircles and swapped upper parallel semicircles close the body.
Every piece, domain, and tangent join is specified in
[PROOF.md](PROOF.md).

An exact speed identity and Cauchy–Schwarz bound the physical body
coefficient by
`[7.0911059675486719886727558957752231 +/- 5.05e-37]`.
Length is integrated over an integer number of complete minor periods:
276 per block. No numerical quadrature is used. Cap length is certified
below 135 for every n.

The checker reconstructs 22 complete rational interval partitions with
146198 leaves. The proof exhausts all 210 unordered piece-pair types,
including self pairs. Curvature, short-arc exclusions, periodic reductions,
vertical tails, explicit cap clearances, and all 16 connector/body
interfaces establish embeddedness and unit thickness using the stated
Cantarella–Kusner–Sullivan criterion. All 22 covers are recomputed after
the exact shrink `499951/500000`, proving the stated global margin.
A selected tangent-point circle bounds this particular family's thickness
from above. It makes no knot-type or C22b optimality claim.

The physical projection of the entire five-axis-turn block has 33800
leaves, 24849 inverse-phase brackets, 908 isolated events, and 1560 raw
crossings. The verifier derives the actual action `[[1,0],[1104,1]]` and
identity material permutation. Exact cap actions, a nilpotent matrix
identity, and rational-tangle classification identify every finite knot
as `T(2,1104n+3)`, up to mirror. The proof explicitly aligns body and cap
projection frames and explains the boundary half twists making the caps
rational. It uses full tangle classification rather than determinant
matching. Reduced alternating crossing minimality gives exact crossing
number `1104n+3`. The physical projection itself need not be alternating.

[CHECKER_MAP.md](CHECKER_MAP.md) maps claims to inputs and justifications.
[ADVERSARIAL_REVIEW.md](ADVERSARIAL_REVIEW.md) records the same-agent
review and earlier immutable checkpoints. The [cap illustration](figures/caps.png)
and [selected contact illustration](figures/selected_contact.png) are
floating point drawings, not metric certificates.

## Corrections

The frozen source remains untouched. This release corrects its Appendix C
height display from `H_n=lambda*2pi*n*h` to
`H_n=lambda*2pi*Q*n*h`, with `Q=5`. Section 1 and Appendices A and I already
used the correct height; certificate arithmetic is unchanged.
The frozen README's `1772603/250000=7.09041` is corrected to
`1772603/250000=7.090412` in the headline and bound above.
No construction, certificate, or checker code changes accompany these corrections.

## Verification and provenance

[REPRODUCE.md](REPRODUCE.md) gives the full replay and all 108 exact expected
rejection controls. The geometry checker is [verify.py](verify.py); the
separately implemented physical projection checker is
[verify_projection.py](verify_projection.py). Both were written by the same
AI agent as the proof; this is not independent authorship.
The remaining exact arithmetic, margin, contact, diagram and integrity
checkers are run by [verify_all.py](verify_all.py).

Fresh release receipts are in [../release_validation](../release_validation/).
The release manifest covers every file in this round1 directory except the
two index files themselves; the validation directory is deliberately outside
the strict file-set boundary so reruns cannot invalidate the checked packet.
Historical macOS/Linux receipts are in [historical_receipts](historical_receipts/).
Their environment packet paths have been replaced by a portable packet label;
mathematical outputs are unchanged. Historical Mini nice was 20 as recorded;
the fresh release records its own effective priority.

The source manifest SHA256 is
`8e9a8979855ecf4b5eb75dce191d5e24d4df4bd7151024ed9fce7f4ebe5106a9`.
[RELEASE_PROVENANCE.json](RELEASE_PROVENANCE.json) lists all unchanged, changed,
and added members against that source. MANIFEST.json and SHA256SUMS have been
regenerated for this release; they do not claim the original frozen digest.
The sole private absolute path in the frozen PRIOR_ART.md was replaced by
a portable description. The inherited prior-art and adversarial notes describe
historical work; files mentioned there outside this packet are not included.

## Credit and review scope

This combines Huh–Kim–Oh's four-strand superhelix idea with the unequal
double-helix parameters and method of Youhua Li / Claude Opus 5.5.
The live table credits its preceding row to [Claude2026], Claude Opus 5.5;
the pinned public repository is YouhuaLi/tight-alternating-knot-constant.
[CREDITS.md](CREDITS.md) retains the full classical and construction credits,
including source-access limitations. [PRIOR_ART.md](PRIOR_ART.md) is the inherited
source-job audit; the fresh release audit is [SOURCE_REFRESH.md](SOURCE_REFRESH.md).
No novelty or optimality claim is made. The same-agent adversarial review
is historical; it is not an external referee report or a release-byte review.

**Verification level: L0** for the bound as a whole (definitions: https://github.com/rpinho/math-certificates/blob/59eeb7097f806da05187b5f234445be3589204d4/VERIFICATION_LEVELS.md)
The interval verifiers were separately written by the same AI agent, and the topology/thickness argument uses stated classical theorems and needs mathematical review.

Computation checks the finite interval covers, curvature and distance scalar
inequalities, actual body projection, exact speed identity, cap matrices,
margin transform, finite diagrams and final rational arithmetic. Prose supplies
the exhaustive analytic reductions, endpoint/gluing and all-n arguments,
physical-to-rational-tangle identification, use of classical thickness and
crossing-minimality theorems, and the limiting inference to C22b. Passing
arithmetic does not independently validate these mathematical reductions.
