# C91 >= 0.259407: canonical alignments with frontier competitors

Unrefereed. This certifies a lower bound on the average edit distance constant, the limit of E[ed(X,Y)]/n for two uniform random binary strings of length n, proposed as constant 91a in [PR #273](https://github.com/teorth/optimizationproblems/pull/273). No human expert has reviewed it line by line.

The best public lower bound I found was Leandre Jack's 0.216276, in that PR. Monte Carlo puts the constant near 0.275 (Bilardi-Schimd), and the upper bound is 0.315514 (Rosenfeld).

## The idea

Jack counts canonical optimal alignments by a first moment over five local rules. This adds three things: forbidding every noncanonical labeled word up to length 12, a dynamic program for long competing alignments with their own gaps, and counting only typical input strings through tilts on low-order spin correlations.

The certificate is a positive vector on an automaton, with 29,006,665 rows. `AV < V` is checked in exact integers, and the final exponent in Arb. Round 2, at 0.256801, is kept in `round2/`.

## What's here

- `PROOF.md`: the reduction and the certificate schema.
- `candidate.json.gz`: the certificate.
- `verify_frontier.py`, `verify_frontier.cpp`: the verifier. It imports no search code.
- `verification.log`, `rational_exponent.json`, `summary.json`: receipts.
- `review/`: AI reviews of rounds 2 and 3.

## Reproduce

Needs python-flint and a C++17 compiler. About 8 minutes.

    python -u verify_frontier.py candidate.json.gz

## What this doesn't show

Separate AI reviews found no gap. For this round, one checked all 29,006,665 rows from the proof alone and confirmed that all 4,190,209 short input pairs keep their canonical optima. For round 2, a hostile referee found no false step. None of them is a second party.

No priority or optimality is claimed.

## Credit

Leandre Jack for the five-rule first-moment method, Ganguly-Mossel-Racz and Bilardi-Schimd for canonical-script counting, and Rosenfeld for the upper bound.

## AI use

Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also prepared the certificate, verifier and this text. This does not claim a line-by-line human verification.
