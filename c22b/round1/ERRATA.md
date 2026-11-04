# Errata for the frozen rational packet

Candidate and unrefereed. These two prose corrections apply to
the original frozen packet `frozen/c22b_7090412_rational`, whose
manifest SHA256 remains
`8e9a8979855ecf4b5eb75dce191d5e24d4df4bd7151024ed9fce7f4ebe5106a9`.
No frozen member, construction coordinate, certificate, verifier, or
replay receipt has been changed.

1. In PROOF.md Appendix C, the single occurrence
   `H_n=lambda*2pi*n*h` must read `H_n=lambda*2pi*Q*n*h`, with `Q=5`.
   Section 1 and Appendices A and I already give the correct height.
   Explicitly, the upper body endpoint has parameter `t=2pi*Q*n` and
   satellite sine `sin(-2pi*P*n)=0`. Its physical height is therefore
   `lambda*h*(2pi*Q*n)`. Under the margin transform only lambda changes
   in this expression, to `rho*lambda`; Q, n, and h remain fixed.
   Hence the upper cap translation scales by rho, exactly as required
   by Appendix C. The missing factor in that prose line does not enter
   any certificate or checker computation.
2. The README first paragraph displays
   `1772603/250000=7.09041`. The exact equality is
   `1772603/250000=7.090412`. Its title and rational value are correct;
   PROOF.md already states the correct full decimal, and ROP_BOUND.json
   binds the correct exact fraction.

The claimed upper bound is **1772603/250000 = 7.090412**. The separately
written (same agent) verifiers and all 108 exact expected rejection
controls passed on both machines before these prose corrections were
recorded. No new mathematical acceptance is inferred from this erratum.
