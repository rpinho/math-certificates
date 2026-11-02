# C44 < 3.9819073803: exact local-degree caps

Unrefereed. This certifies an upper bound on C44, the constant in the relevant-variable bound r(f) <= C 2^deg(f), Tao table [44a](https://teorth.github.io/optimizationproblems/constants/44a.html). No human expert has reviewed it line by line.

    C44 <= 157739602520732550180509661243 / 39614081257132168796771975168 < 3.9819073803

It improves the 4.1225323803 in [`../fourier-granularity/`](../fourier-granularity/) by exactly 9/64, with the same recurrence, block-sensitivity bounds and tail. Only the local-weight caps change: c4 = 25/16, c5 = 71/32, c6 = 45/16, from R4 <= 25, R5 <= 71, R6 <= 180. B8 <= 32 is not proved.

## The idea

Put M = 2^(d-1). M^2 times an influence is a sum of integer squares, and evaluating the derivative at the all-plus point makes it even. So each influence is exactly 1/M or at least (M+2)/M^2. If none is minimal, total influence bounds the variable count. If one is minimal, its Fourier support is an affine cube, at most 2(d-1) control coordinates leave a dictator on a 1/M fraction of branches, and restriction finishes the case. The Chiarelli-Hatami-Saks extremal identity turns the counts into universal caps.

## What's here

- `PROOF.md`: the written proof. The arithmetic verifiers check the certificates, not these lemmas.
- `cap_certificate.json`, `candidate.json`, `spectral_certificate_round3.json`: the exact inputs.
- `verify_caps.py`, `verify_spectral.py`, `verify_bound.py`, `verify_column.py`: exact verifiers. `verify_column.py` imports neither the search nor another verifier.
- `control_structure.py`, `control_rejections.py`: finite controls and corruption tests.
- `FINAL_RECEIPT.json`, `verification_*`: receipts. `baseline/` holds the inherited proofs.
- `review/`: a separate AI review, `REVIEW.md`, with its own exact recomputation and brute-force attacks.

## Reproduce

Standard library only, from this folder.

    python3 verify_caps.py cap_certificate.json
    python3 verify_spectral.py spectral_certificate_round3.json
    python3 verify_bound.py candidate.json
    python3 verify_column.py candidate.json

## What this doesn't show

The AI review passed every proof step, recomputed the exact 9/64 gain, and found no counterexample in 17.6 million Boolean function instances and all 43,046,721 ternary tables on four coordinates. The best lower constructions it located are 22, 46 and 94, below the caps. It's AI, so it isn't a second party.

The cited theorems R3 <= 10 and Wellens's block-sensitivity inequality are used, not reproved. The minimum-support structure follows from stronger work of Valyuzhenich (2023), so this may not be new. No priority or optimality is claimed.

## Credit

Chiarelli, Hatami and Saks for the weighted framework, including the corrected duplication in Chiarelli's thesis. Wellens for the recurrence, Épi for the exact polynomial data, Koshta for public B4 <= 9, Stepanovs for B5 <= 14, Towell for earlier Fourier integer-energy exclusions, and Valyuzhenich for the structure of minimum-influence functions.

## AI use

Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also prepared the certificates, verifiers and this text. This does not claim a line-by-line human verification.
