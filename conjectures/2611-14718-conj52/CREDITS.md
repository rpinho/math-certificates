# Credits

- **Robinson Higuita-Diaz, Lykos Lopez, and Alejandro Roldan-Correa**: posed Conjecture 5.2 (`\label{conj:grado3}`), verified all connected subcubic graphs up to order 12 (`27,525` graphs), proved the component corollary (`\label{cor:conexidad}`), and constructed the sharp degree-4 counterexample on 6 vertices in *Random Sequential Adsorption versus the Uniform Ensemble of Jammed Configurations: Stochastic Dominance on Graphs* (`arXiv:2611.14718v2`, 2026).

## Verification provenance

This is AI work. No human has checked it. Lean status: `none`.

- **Producer:** Gemini 4 Carbon High via Antigravity CLI (discovered the sharp `n=15` subcubic tree counterexample `F_3`, the two 15-edge unicyclic counterexamples `CE#2` and `CE#3`, the infinite subcubic tree family `F_m` for `m >= 3`, and the exhaustive `n <= 15` census).
- **Clean-room Cross-Family Referee:** GPT-6.2 Astra via Codex (producer code withheld). Independently re-enumerated all `1,375,631` non-isomorphic connected subcubic graphs through order 15 (`358,891` for `n <= 14`, `1,016,740` for `n = 15`), replayed all `4,604,216` supported size bins, verified all three `n=15` counterexamples in pure `fractions.Fraction` plus exact arrival-time integration, verified all 89 single vertex/edge deletions, checked the infinite tree family at `m=4` (`n=20`), rejected all 7 mutation controls, and caught a transcription typo in `producer/witness_v1.json` (`rsa_pmf["7"]` written as `7993211/10135125` instead of `7993019/10135125`) plus the fact that `CE#3` is also proper-subgraph minimal. After repairing `certificates/witness.json`, `referee/referee_verify_repaired.py --strict-certificate` exited `0` (`referee/referee_verify_repaired.log`).
