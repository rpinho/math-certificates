# C86 <= 1.80560940: classical auxiliaries on an adaptive density cone

Unrefereed. Upper bound on the Schur-Siegel-Smyth trace constant, Tao table [86a](https://teorth.github.io/optimizationproblems/constants/86a.html). No human expert has reviewed it line by line.

    C86 <= 288897505229428473 / 160000001279369600 < 1.80560940

It improves the 1.80580911 in [`../classical-half-cells/`](../classical-half-cells/) by about 0.0002, with the same proof by Smith's criterion. There are 28 auxiliaries from classical lists, 10 with nonreal roots, largest degree 21, on 5,375 rational nodes. `adaptive_checked-provenance.json` gives the source of each.

## What's here

- `certificate.json`: SHA-256 `10d68ec249f47c0504182d419fd8ddd1ca1c917e42a4bba59d944b9d1de0dad5`.
- `PROOF.md`, `METHOD.md`, `VERIFIER_NOTES.md`.
- `verify_linear.py`, `independent_verify.py`: two checkers, with their receipts and a closed-cover audit.
- `review/REVIEW.md`: a separate AI review with its own full-support proof check.

## What this doesn't show

The review passed every step and all 28 auxiliaries. It's AI, so it isn't a second party. No priority or optimality is claimed.

## Credit

The auxiliaries come from Flammang's and McKee's lists, as the provenance file records. Smith for the criterion, and Tomar for the adaptive nodes.

## AI use

Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also prepared the certificates, verifiers and this text. This does not claim a line-by-line human verification.
