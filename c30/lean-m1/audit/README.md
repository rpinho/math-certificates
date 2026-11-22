# Statement audit of C30Lean (Lean-checked)

A separate-model audit (Claude Opus 5.5, 2026-11-21/22; AI, unrefereed) of whether the theorems in `../C30Lean` state the two informal lemmas they claim (`../../round1/FIRST_MOMENT_PROOF.md`).

- `Spec.lean` imports only Mathlib. It states the lemmas as written: Lemma E (strip envelope), Lemma M (weighted Markov bound) and Lemma S (selection step). It was written from the informal text before reading the Lean library.
- `Bridge.lean` proves the spec from the library's theorems.
  - `strip_envelope` gives Lemma E only under its two extra hypotheses on U (`bridge_E_conditional`). An `example` at y = [0,0], B = 2, U = 1 shows the lemma's hypotheses hold there while those two fail.
  - Lemma E in full (`specE_full`) follows from the library's auxiliary theorems.
  - Lemma M follows from `finite_weighted_markov` for real N2 >= 0 and from `finite_family_selection` for counts.
  - Lemma S has no library theorem. `specS_of_specM` proves it from Lemma M; that proof is the audit's, not the library's.
- `Mutants.lean` disproves twelve one-change variants of the spec in Lean (a swapped quantifier, a dropped hypothesis, a weakened conclusion), so the bridges are not passing because the spec is vacuous. It also shows each lemma's hypotheses hold at the C30 parameters.
- `Axioms.lean` prints the axioms of every audit theorem: only propext, Classical.choice and Quot.sound.

Build, from `c30/lean-m1` after `lake exe cache get && lake build`: `sh audit/build.sh`. The audit was also replayed through `leanchecker` and the nanoda kernel (13,719 declarations, no errors).
