# Credits

- **Haobo Ma, Rafik Sahbi, and Wenlin Zhang**: posed Conjecture 9.2 (`\label{conj:ng-upper}`) and established the foundational theory of sub-quorum colorings in *Sub-quorum colorings of graphs* (`arXiv:2609.25128v4`, 2026).
- **Rafik Sahbi and Mustapha Chellali** (2018): Nordhaus-Gaddum upper bound for total quorum colorings (`\psi_q(G) + \psi_q(\overline{G}) \le n + 2`), recovered as a special case when both supports equal `V`.

## Verification provenance

This is AI work. No human has checked it. Lean status: `verified` (standalone Lean 4.36.0 in `lean/`, zero Mathlib, standard axioms `[propext, Classical.choice, Quot.sound]`, produced by Gemini 4 Carbon High via Antigravity CLI).

- **Producer:** Gemini 4 Carbon High via Antigravity CLI (discovered the reciprocal class-size vertex-weight proof via Lemmas 1, 2, 3 and Theorem 1, ran the exhaustive `n <= 9` census across `288,265` unlabeled graphs plus `53,470` structured/SA graphs through `n = 20`, and wrote `producer/verify_proof.py`).
- **Clean-room Cross-Family Referee:** GPT-6.2 Astra via Codex (producer code withheld). Upheld Theorem 1 and all lemmas for every finite simple graph of order `n >= 2` (`VERDICT: HOLDS WITH CAVEATS`), independently verifying Definition 2.2 verbatim, `33,868` labeled graphs through order 6 (`249,299` optimal partitions, `13,047,409` subset-vertex checks), all `268,435,456` labeled graphs through order 8 for Lemma 3, all `16,348,842` graphical degree sequences for orders 8-15, and all `288,265` isomorphism classes for orders 2-9 (`referee/verification.txt`). Caught one prose precision slip in Remark 3 (`PROOF.md` line 125, repaired in `PROOF.md`) and clarified one-sided vs either-side dissociation-gap census counts (`1, 13, 133, 1236` vs `2, 26, 264, 2450` at orders 6-9).
