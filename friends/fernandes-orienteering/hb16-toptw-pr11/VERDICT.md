HOLDS WITH CAVEATS
Referee: gpt-6.1-sol

The exact optimum is 654 for classical TOPTW long-window Cordeau pr11 with three vehicles. I found no counterexample or gap in the submitted numerical certificate.

My independently written checker closes all 46,749 states and 1,180,957 transitions, using exact integer travel and safe dominance. No claimant search/verifier code, suffix-knapsack pruning, or solver optimality status was used.
The verified bound is 1000×score ≤623716+3×11082=656962, hence score≤656. Raw prizes total657 and each is at least3, excluding655/656. Independently replayed routes attain654, omitting only customer19.

What I ran: fresh official download and byte comparison; independent primal and upper checks;40 exhaustive small fixtures with false-bound/missing-root attacks; five malformed-route attacks; fresh compilation/run of the unmodified public SISR baseline, whose new654 routes also pass my checker. My simple insertion control scored544. A separate all-customers CP test was inconclusive after120seconds and supplies no proof.

The [official format](https://www.mech.kuleuven.be/en/mim/op/instances/TOPTWformat) matches service-start windows, floored two-decimal travel and depot return. CLAIM.md links the wrong archive: the matching pr11 bytes are in [MontemanniTOPTW2](https://www.mech.kuleuven.be/en/mim/op/instances/MontemanniTOPTW2), not TOPTW1. The claimant's underlying download receipt names the correct archive.

The [2020 supplement](https://ars.els-cdn.com/content/image/1-s2.0-S0305054820301568-mmc1.pdf), Tables9/20, already reports654 unstarred for three vehicles; four-vehicle657 is starred. A fresh authenticated Ševeček2026 thesis download also confirms654. The addition here is exact certification of an existing feasible score, not a score gain. Earlier per-instance proof tables remain incompletely accessed; no priority judgment is made.

[Gama and Hugo L. Fernandes's paper](https://arxiv.org/abs/2011.03647) is genuinely coauthored by Hugo. It evaluates single-route OPTW: pr11 best-known353 and learned-model351. This three-route certificate extends the benchmark task; it does not correct those numbers or test the paper's learning/generalization comparisons.

No holdout was used or claimed: this is a deliberately reused public deterministic benchmark. Evidence and independent code are copied back in evidence/; FINAL_RECEIPT.json and RECOVERY_RECEIPT.json record verification and transport. Pod workers ended and its referee folder remains below1GB.

Strongest author objection:654 was already known as a feasible three-route score, and proving it optimal says nothing by itself about the paper's single-route model performance. That boundary is factual; the exact certificate still passes.

NEXT BAR: Add one corrected, source-linked comparison row explicitly distinguishing three-route exact654 from the paper's single-route353/351 and pointing to MontemanniTOPTW2.
