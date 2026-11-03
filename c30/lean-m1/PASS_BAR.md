# C30 Lean milestone 1: frozen pass bar (2026-11-03T17:43:21Z; general approved 11-03)

The milestone passes only if ALL hold, on a pinned Lean 4 toolchain + Mathlib commit recorded in lean-toolchain and lake-manifest.json:
1. `lake build` succeeds from a clean checkout (receipt: full build log + exit code + sha256 of every .lean file).
2. No `sorry`, `sorryAx`, `admit` anywhere (grep receipt plus `#print axioms` output).
3. `#print axioms` for each main theorem lists only Lean's standard axioms (propext, Classical.choice, Quot.sound) and the names declared in AXIOMS.md; every non-standard axiom there has an exact citation (paper, version, theorem number). For milestone 1 the expected non-standard axiom list is EMPTY (both statements are self-contained finite/integer facts).
4. `native_decide` (and `Lean.ofReduceBool`) absent, or each use explained in AXIOMS.md with why it is needed.
5. The Lean statements match the informal statements in c30r2/FIRST_MOMENT_PROOF.md (integer strip envelope with parity choice e2 in {U, U-1}; finite weighted Markov inequality), and a statement-correspondence note says so line by line.
