# C89c >= 0.000025987181439: a sharper flag certificate

Unrefereed. Lower bound on the Ramsey multiplicity constant of K6, proposed as 89c in [PR #279](https://github.com/teorth/optimizationproblems/pull/279). No human expert has reviewed it line by line.

It's 23% above the 0.000021083 in [`../`](../), with the same flag-algebra method on better-chosen flags. `REPRODUCE.md` gives the exact replay. A tiny C89b gain, 6.4e-10 over the published certificate, is also here and isn't claimed as an advance.

## What's here

- `certificates/`: the integer certificates.
- `scripts/`: the exact verifiers, built from source.
- `PROOF.md`, `CERTIFICATE_README.md`, `REPRODUCE.md`, `receipts/`.
- `../review/REVIEW-round2.md`: a separate AI review that rebuilt the exact checks and reran K3 and K4 as controls.

## What this doesn't show

The review passed both bounds. It's AI, so it isn't a second party. No priority or optimality is claimed.

## AI use

Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also prepared the certificates, verifiers and this text. This does not claim a line-by-line human verification.
