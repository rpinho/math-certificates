# Disproof and Sharp n = 15 Classification for Higuita-Diaz, Lopez, and Roldan-Correa (arXiv:2611.14718v2) Conjecture 5.2

This packet refutes Conjecture 5.2 (`\label{conj:grado3}`) of Robinson Higuita-Diaz, Lykos Lopez, and Alejandro Roldan-Correa, *Random Sequential Adsorption versus the Uniform Ensemble of Jammed Configurations: Stochastic Dominance on Graphs* ([arXiv:2611.14718v2](https://arxiv.org/abs/2611.14718v2)), and establishes **`15`** as the sharp minimum vertex order of a counterexample.

This is AI work. No human has checked it. **Lean status:** `verified` (standalone Lean 4, zero Mathlib, zero `sorry`, standard axioms `[propext, Classical.choice, Quot.sound]`; see [`lean/`](lean/)).

## Conjecture 5.2 (as stated in v2)

> For every finite simple graph $G$ with maximum degree $\Delta(G) \le 3$, the sequential model dominates the static model ($N_G^{\mathrm{stat}} \le_{\mathrm{st}} N_G^{\mathrm{seq}}$).

The paper's authors verified all `27525` connected subcubic graphs through order `12`.

## Main result: sharp minimum order 15 and exact classification

Independent exhaustive enumeration of all `1375631` non-isomorphic connected simple graphs with $\Delta(G) \le 3$ through order `15` (and the paper's component corollary for disconnected graphs) establishes:

- **Orders $n \le 14$ (`358891` connected subcubic graphs):** `0` counterexamples.
- **Order $n = 15$ (`1016740` connected subcubic graphs):** **exactly `3`** non-isomorphic counterexamples, all having `55` maximal independent sets and violating stochastic dominance at threshold $k = 6$:
  $$\mathbb{P}(N_G^{\mathrm{seq}} \le 6) = \frac{64}{3375} > \frac{1}{55} = \mathbb{P}(N_G^{\mathrm{stat}} \le 6), \qquad 64 \cdot 55 - 1 \cdot 3375 = 145 > 0, \qquad \text{gap} = \frac{29}{37125}.$$

| Witness | Structure ($\Delta = 3$, $n = 15$) | Support | Exact violation at $k = 6$ | Strict global static dominance? | Proper-subgraph minimal? |
|---|---|---|---|---|---|
| **`CE#1` ($F_3$)** | **14-edge subcubic tree** (unique sparsest) | `{6, 7, 8}` | `64/3375 > 1/55` | No (CDFs cross; `P(seq=7) = 7993019/10135125`, `P(seq=8) = 1949914/10135125`) | Yes (`15/15` $G-v$, `14/14` $G-e$) |
| **`CE#2`** | 15-edge triangle-free unicyclic (girth 5) | `{6, 7}` | `64/3375 > 1/55` | **Yes** ($N^{\mathrm{seq}} <_{\mathrm{st}} N^{\mathrm{stat}}$; means `23561/3375 < 384/55`) | No (`CE#2 - (0,1)` is `CE#1`) |
| **`CE#3`** | 15-edge triangle-containing unicyclic (girth 3) | `{6, 7}` | `64/3375 > 1/55` | **Yes** ($N^{\mathrm{seq}} <_{\mathrm{st}} N^{\mathrm{stat}}$; means `23561/3375 < 384/55`) | Yes (`15/15` $G-v$, `15/15` $G-e$) |

Chaining $m \ge 3$ copies of the 5-vertex subcubic unit yields an infinite family of subcubic trees $F_m$ violating Conjecture 5.2 (independently verified at $m = 4$, order `20`, where $\mathbb{P}(N_{F_4}^{\mathrm{seq}} \le 8) = 256/50625 > 1/229 = \mathbb{P}(N_{F_4}^{\mathrm{stat}} \le 8)$).

## Clean-room cross-family verification and referee repair

- **Producer:** Gemini 4 Carbon High via Antigravity CLI (`producer/REPORT.md`, `producer/verify_counterexample.py`, `producer/witness_v1.json`).
- **Clean-room Cross-Family Referee:** GPT-6.2 Astra via Codex (`referee/REFEREE.md`, `referee/referee_verify.py`, `referee/referee_census.cpp`, producer code withheld). Independently re-enumerated all `1375631` connected subcubic graphs through order `15`, replayed all `4604216` supported size bins, verified all `89` single vertex/edge deletions across `CE#1`, `CE#2`, `CE#3`, derived the exact arrival-time integral for $F_3$, and rejected all `7` mutation controls.
- **Referee fixes applied before publication:** The referee returned `VERDICT: HOLDS WITH CAVEATS`, confirming the disproof, sharp minimum order `15`, all three witnesses, and the infinite tree family while catching a transcription typo in `producer/witness_v1.json` (`rsa_pmf["7"]` recorded as `7993211/10135125` instead of `7993019/10135125`) and noting that `CE#3` is also proper-subgraph minimal. Both corrections are applied in [`certificates/witness.json`](certificates/witness.json). Running `referee/referee_verify_repaired.py --strict-certificate` (differing from `referee/referee_verify.py` only in the updated SHA-256 lock) exited `0` (`referee/referee_verify_repaired.log`).


## Standalone Lean 4 formalization

The [`lean/`](lean/) directory contains a self-contained Lean 4 (`leanprover/lean4:v4.36.0`, zero Mathlib dependencies) formalization defining finite simple graphs, maximal independent sets, and random sequential adsorption from first principles and proving both `conj52_disproof_F3` (`64/3375 > 1/55`, excess `145` on the 15-vertex subcubic tree $F_3$) and `infinite_family_Fm_disproof` for every $m \ge 3$, plus seven small-graph controls. It builds cleanly with zero `sorry`, zero `axiom`, zero `native_decide`, zero warnings, and standard core axioms `[propext, Classical.choice, Quot.sound]` only:

```bash
cd lean && python3 -B verify_lean.py
```

## Reproduction

Requires Python 3.10+ (standard library only, exact `fractions.Fraction`). From `conjectures/2611-14718-conj52/`:

```bash
# 1. Verify file integrity
shasum -a 256 -c SHA256SUMS

# 2. Run strict clean-room referee verifier on certificates/witness.json
python3 -c 'import os, shutil, subprocess, tempfile; d=tempfile.mkdtemp(); os.makedirs(d+"/inputs"); shutil.copy("certificates/witness.json", d+"/inputs/witness.json"); shutil.copy("referee/referee_verify_repaired.py", d); subprocess.run(["python3", "-B", "referee_verify_repaired.py", "--strict-certificate"], cwd=d, check=True)'
```
