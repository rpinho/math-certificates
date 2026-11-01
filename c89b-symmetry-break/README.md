# C89b <= 2405659597/1427496763392 < 0.00168523

Unrefereed. This certifies an upper bound on the Ramsey multiplicity constant of K5, proposed as constant 89b in [PR #277](https://github.com/teorth/optimizationproblems/pull/277). No human expert has reviewed it line by line.

That's about 0.105% below Jeetu SK's 0.0016870051 in PR #277.

## The idea

Jeetu SK's step graphon optimizes the 192-vertex Cayley graph of Parczyk, Pokutta, Spiegel and Szabo. Its fractional probabilities are a perfect matching and a class of 12 neighbors per vertex, and first-order descent keeps that symmetry and stalls. A negative direction of the Hessian splits the 12 neighbors into two groups of six at every vertex. One group moves to probability 1 and the other joins the matching at 5/7. The result is a simple rational construction.

## What's here

- `PROOF.md`: the construction and the blow-up argument.
- `candidate.json.gz`: the exact step graphon.
- `independent_verify.py`, `independent_count.cpp`, `verification.log`: an exact recount of the full matrix, using no graph symmetry or search code.
- `check_counter_controls.py`, `controls.log`: exact small controls.
- `review/REVIEW.md`: an AI review, whose own exact counter agrees.

## Reproduce

Needs a C++17 compiler and Python's standard library.

    g++ -O2 -std=c++17 independent_count.cpp -o independent_count
    python3 independent_verify.py candidate.json.gz

## What this doesn't show

Two exact counters agree, and the AI review found no gap. That isn't a second party. Numerical diagnostics suggest this is a local optimum for this support pattern, which isn't proved, and nothing is claimed about optimality or priority.

## Credit

Parczyk, Pokutta, Spiegel and Szabo for the Cayley graph, and Jeetu SK for the optimized step graphon.

## AI use

Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also prepared the certificate, verifier and this text. This does not claim a line-by-line human verification.
