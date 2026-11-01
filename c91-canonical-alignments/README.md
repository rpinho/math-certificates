# C91 >= 0.256801: canonical alignments with typical-set counting

Unrefereed. This certifies a lower bound on the average edit distance constant, the limit of E[ed(X,Y)]/n for two uniform random binary strings of length n, proposed as constant 91a in [PR #273](https://github.com/teorth/optimizationproblems/pull/273). No human expert has reviewed it line by line.

The best public lower bound I found was Leandre Jack's 0.216276, in that PR. Monte Carlo puts the constant near 0.275 (Bilardi-Schimd), and the upper bound is 0.315514 (Rosenfeld).

## The idea

Jack counts canonical optimal alignments by a first moment over five local rules. This adds three things: forbidding every noncanonical labeled word up to length 12, tracking long competing alignments of unbounded length, and counting only typical input strings through tilts on low-order spin correlations.

The certificate is a positive vector on an automaton with 7,206,135 states. `AV < V` is checked in exact integers, and the final exponent in Arb. The threshold is 0.2568017632.

## What's here

- `PROOF.md`: the reduction and the certificate schema.
- `candidate.json.gz`: the certificate. SHA-256 `472cb2e9a0bc3b377f0ea0bf4a8d052c93fa4be4a3c81d81566be92655165c67`.
- `independent_verify.py`: imports no search code.
- `verification.log`, `rational_exponent.json`: receipts.
- `review/`: two AI reviews.

## Reproduce

Needs python-flint. About 5 minutes.

    python -u independent_verify.py candidate.json.gz

## What this doesn't show

Two separate AI reviews found no gap. One rebuilt and checked the whole unmerged certificate from the proof alone. The other tested the tracker exhaustively on all pairs up to length 8. Neither is a second party.

No priority or optimality is claimed.

## Credit

Leandre Jack for the five-rule first-moment method, Ganguly-Mossel-Racz and Bilardi-Schimd for canonical-script counting, and Rosenfeld for the upper bound.

## AI use

Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also prepared the certificate, verifier and this text. This does not claim a line-by-line human verification.
