# C30 Lean milestone 1: two finite lemmas of the new step

Lean 4 + Mathlib proofs of two finite facts used in the candidate C30 >= 521/50 argument (../round1): the integer strip envelope with its parity choice (`C30Lean.strip_envelope`, `strip_envelope_application`) and the finite weighted Markov / family-selection inequality (`finite_weighted_markov`, `finite_family_selection`). All 16 theorems use only Lean's standard axioms (propext, Classical.choice, Quot.sound); there is no sorry, admit or native_decide.

This checks those two lemmas only. It does not prove the C30 bound: the marking, analytic and generating-function steps are not in Lean, and the bound stays conditional on Norton's unrefereed v3. The pass bar was frozen before the run (PASS_BAR.md). STATEMENTS.md maps each Lean statement to the informal text. Written by an AI agent (GPT-6.1 Sol via Codex) under Ricardo Pinho's direction.

Build: `lake exe cache get && lake build` with the pinned lean-toolchain and lake-manifest.json; receipts/ holds the clean-build log, exit code, pins, source hashes and `#print axioms` output.
