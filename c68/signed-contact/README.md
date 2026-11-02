# C68 >= 0.44685: a signed contact-harmonic lemma

Unrefereed. This certifies a lower bound on Korenblum's constant in the Bergman space, Tao table [68a](https://teorth.github.io/optimizationproblems/constants/68a.html). No human expert has reviewed it line by line.

It improves the 0.44667 in [`../contact-spectral/`](../contact-spectral/) by 0.00018. The change is a new input to the coefficient inequality, not a better LP. The old contact reduction replaced the signed first harmonic by its minimum. Retaining the sign raises the correction constant from 0.07 to 0.095.

## What's here

- `PROOF.md`, `SIGNED_CONTACT_LEMMA.md`, `INEQUALITY_AUDIT.md`, `INPUT_*.md`: the proof and its inputs.
- `certificate-44685.json`, `signed-cover.json`: exact inputs.
- `verify_measure.py`, `verify_signed_cover.py`, `verify_controls.py`: Arb and exact checks, and their receipts.
- `counterexample.json`, `verify_counterexample.py`: a certified counterexample to the naive third-coefficient extension.
- `review/REVIEW.md`: a separate AI review, with its own Arb checks.

## What this doesn't show

The programs check numerical hypotheses, not complex analysis. The review passed every step and found no counterexample to 0.095, and it shows the stronger 0.105 is false. It's AI, so it isn't a second party. No priority or optimality is claimed.

## Credit

David Niedbala Giraudin for the flux input, Wang for the coefficient approach, Wikstrom for moment integration.

## AI use

Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also prepared the certificate, verifiers and this text. This does not claim a line-by-line human verification.
