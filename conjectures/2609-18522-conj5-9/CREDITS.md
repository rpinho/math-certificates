# Credits

- **Earlier work.** TrureTuring's macstudio-2[bot] refuted the printed preperiod formula in Conjecture 9 with seeds $(251,1005)$ on 2026-11-26 at 00:14:49 UTC. [Exact certificate in the issue comment](https://github.com/the-omega-institute/trureturing/issues/34312#issuecomment-7178554093). The same conjecture was later refuted in Lean at $(5,21)$ in [PR #34359](https://github.com/the-omega-institute/trureturing/pull/34359), opened on 2026-11-26 at 02:57:37 UTC.
- **Daan van Berkel and Wieb Bosma**: posed Conjectures 5 (`\label{conj:per}`) and 9 (`\label{conj:pre}`), stated Definitions 3 and 8, and proved Theorem 15 (the five-block finite-computation periodicity criterion) in *Periodicity conjectures for all 2-sumfree sequences* (`arXiv:2609.18522v1`, 2026).

## Verification provenance

This is AI work. No human has checked it. Lean status: `verified` (standalone Lean 4.36.0 in `lean/`, zero Mathlib, standard axioms `[propext, Classical.choice, Quot.sound]`, produced by Gemini 4 Carbon High via Antigravity CLI).

- **Producer:** GPT-6.2 Astra via Codex (swept 4,800 strict greedy 2-sumfree sequences, computed the counterexamples at `S_{4,11}` and `S_{5,10}` plus the negative formula value `-23` at `S_{12,30}`, and wrote `producer/verify_counterexample.py`).
- **Clean-room Cross-Family Referee:** Gemini 4 Carbon High via Antigravity CLI (producer code withheld). Returned `VERDICT: HOLDS` with zero defects in `certificates/witness.json`, `producer/definitions.tex`, or `producer/REPORT.md`, writing pure-`int`/`Fraction` `referee/referee_verify.py` (AST-audited for zero `float`, zero `/` operators, and zero `math` imports), verifying dual independent proofs (Theorem 15 five-block cutoff and rational GF identity), 15 positive controls, 16/16 adversarial negative controls, all 1,845 displayed table entries, and all 4,800 primary grid comparisons.
