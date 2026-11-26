# Credits

- **Joel Brewster Lewis and Robert Won**: posed Conjecture 3.14 (`\label{conj:maxlayered}`, TeX line 754) and proved Proposition 3.15 (`\label{prop:countlayered}`, TeX line 759) in *Non-attacking rook placements on crossword grids* (`arXiv:2609.03081v1`, 2026).
- **Alex Chengyu Li** (`10.5281/zenodo.22679647`, 2026): prior counterexample (`155` placements at `n = 8`) to Conjecture 3.10 (`\label{conj:rookcounts}`), reproduced only as a baseline control and excluded from our claims.

## Verification provenance

This is AI work. No human has checked it. Lean status: `verified` (standalone Lean 4.36.0 in `lean/RookConj314.lean`, zero Mathlib, standard axioms `[propext, Classical.choice, Quot.sound]`, produced by GPT-6.2 Sol via Codex).

- **Producer:** Gemini 4 Carbon High via Antigravity CLI (discovered the 2-shell nested layered counterexample at `n = 17` of shape `(5, 3, 1, 3, 5)` and higher-order witnesses `n = 18..20`, proved global maxima `r(10..14)` via branch-and-bound, and wrote `producer/verify_counterexample.py`).
- **Clean-room Cross-Family Referee:** GPT-6.2 Astra via Codex (producer code withheld). Confirmed the `n = 17` and `n = 18` disproofs via matching recurrence, Ryser inclusion-exclusion, and a closed-form 7-square derivation; independently re-proved all five global maxima `r(10..14)` through `S_14` (`87,178,291,200` permutations); verified all `136` ordered endpoint pairs at `n = 17` and all `46,233` permutations for `n <= 8`; rejected `5/5` mutations (`VERDICT: HOLDS WITH CAVEATS`). Flagged four prose/metadata clarifications in `producer/REPORT.md` and `witness.json`'s `minimality_note` (TeX line `754` vs `759`, `4` moved diagonal squares vs `6`, `136` ordered vs `128` strictly asymmetric pairs, and clarifying that unconditional minimality at `n = 15, 16` remains open beyond the restricted-family checks), all explicitly clarified in `README.md`.
