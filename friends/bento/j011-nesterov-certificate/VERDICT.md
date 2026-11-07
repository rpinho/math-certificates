HOLDS
Referee: gpt-6.1-sol

The exact theorem survives independent reconstruction: at kappa25 and
beta21/32, q=3599/5000=0.7198 is a universal squared-distance upper factor,
improving the matched published q18/25 by1/5000.
The paper's norm factor is sqrt(q); the metric and recurrence match.
[Primary source](https://www.jbento.info/papers/nesterov_sdp.pdf), Algorithm1,
Eqs25–26 and Theorem7. José Bento's identity matches the author block and
[his publication page](https://www.jbento.info/).

I wrote independent code from the definitions and ran it on mscr: exact
source-baseline reproduction at kappa5,13,25,41; rational reconstruction
of the submitted certificate; 35/36 positive LDL pivots; exact function
cancellation, nonnegative multipliers, and coercivity. Three corrupted
certificates were rejected. Code, logs, hashes and receipts are retained here.

No hold-out or dataset exists. The trivial quadratic control gives
q=441/625=0.7056 and cannot certify the nonquadratic class. The basic
matched off-by-one frequency test fails exactly at the proposed factor.

Relative to the paper, the addition is one finite-kappa rational certificate
using the established 2018 finite-history interpolation method. The 2026
[Pokutta–Stellato paper](https://arxiv.org/abs/2610.15125) reports exact standard-beta rates at kappa10 and100;
this uses different momentum and does not improve those matched results.
Source coverage and access limits are recorded in PRIOR_ART.md.

Strongest objection: a look-ahead potential might hide an unjustified
initial bound. Independent finite-window bounds close this gap with uniform
K about3.12e43, so no useful finite-time improvement follows from this proof.

NEXT BAR: Certify a finite-time distance bound that beats the source guarantee
at these same parameters with both prefactors included.
