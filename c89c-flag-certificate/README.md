# C89c >= 0.000021083: an exact flag-algebra certificate

Unrefereed. This certifies a lower bound on the Ramsey multiplicity constant of K6, proposed as constant 89c in [PR #279](https://github.com/teorth/optimizationproblems/pull/279). No human expert has reviewed it line by line.

That's 0.3454 * 2^-14. The upper bound in the PR is 0.7423 * 2^-14. The best explicit lower value I found was about 1.08e-9, from de Caen's bound with Mackey's R(6,6) <= 165, so this is a large jump, and it uses no Ramsey-number input.

## The idea

An eight-vertex sum-of-squares certificate in the flag algebra of 2-coloured graphs, with 13 rational Gram blocks, written as integer squares with denominator 10^9. `PROOF.md` gives the complete proof, with the finite-sampling error and the limit.

## What's here

- `PROOF.md`, `CERTIFICATE_README.md`, `ELEMENTARY.md`: the proof, the format, and the elementary baselines.
- `c6_8.cert`: the certificate.
- `verify_exact.cpp`, `checked_integer.hpp`, `verify_python.py`: two separately written exact verifiers, and their logs.
- `review/REVIEW.md`: a separate AI review.

## Reproduce

    g++ -O3 -std=c++17 verify_exact.cpp -o verify_exact
    ./verify_exact c6_8.cert sources/graph8.g6
    python3 verify_python.py c6_8.cert sources/graph8.g6

## What this doesn't show

The AI review found no gap and wrote a third exact checker. The same method on K3 and K4 gave 0.249290642 and 0.027777765, below the known values, and a separate Goodman control recovered exactly 1/4. That's AI, so it isn't a second party. This isn't near the upper bound, and no priority or optimality is claimed.

## Credit

Razborov's flag algebras, Conlon, de Caen and Mackey for the baselines, and Jeetu SK for the constant's page in PR #279.

## AI use

Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also prepared the certificate, verifiers and this text. This does not claim a line-by-line human verification.
