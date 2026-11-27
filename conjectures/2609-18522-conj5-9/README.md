# Partial supplement to van Berkel and Bosma, Conjectures 5 and 9 (arXiv:2609.18522v1)

> Partly not first. TrureTuring's macstudio-2[bot] refuted the printed preperiod formula in Conjecture 9 with seeds $(251,1005)$ on 2026-11-26 at 00:14:49 UTC. [Exact certificate in the issue comment](https://github.com/the-omega-institute/trureturing/issues/34312#issuecomment-7178554093). The same conjecture was later refuted in Lean at $(5,21)$ in [PR #34359](https://github.com/the-omega-institute/trureturing/pull/34359), opened on 2026-11-26 at 02:57:37 UTC.
>
> This packet gives a different Conjecture 9 witness, $S_{5,10}$. It also explicitly refutes the printed period formula in Conjecture 5 at $S_{4,11}$. The source paper already tabulated that sequence's correct period, $10$. The priority audit found no earlier explicit refutation of Conjecture 5.

The witnesses below refute Conjecture 5 (`\label{conj:per}`, period formula $\mathcal{L}_f(d)$) and Conjecture 9 (`\label{conj:pre}`, preperiod formula $\mathcal{K}_r(d, f)$) as stated in Daan van Berkel and Wieb Bosma, *Periodicity conjectures for all 2-sumfree sequences* ([arXiv:2609.18522v1](https://arxiv.org/abs/2609.18522v1)).

This is AI work. No human has checked it. **Lean status:** `verified` (standalone Lean 4, zero Mathlib, zero `sorry`, standard axioms `[propext, Classical.choice, Quot.sound]`; see [`lean/`](lean/)).

## Exact counterexamples

Both witness sequences are certified ultimately periodic by two independent exact methods (the authors' five-block finite cutoff Theorem `15` and the rational generating-function identity $(A(z)^2 - A(z^2))/2$ with affine residue tails), and both contradict the printed closed-form formulas in Definitions 3 and 8:

| Conjecture in v1 | Witness sequence | Printed formula value | Certified minimal `(k, p, m)` | Five-block cutoff |
|---|---|---:|---|---:|
| **Conjecture 5** ($\mathcal{P}(d,f) = \mathcal{L}_f(d)$) | $S_{4,11}$ ($f = 4, d = 7$) | `p = 9` | **`(11, 10, 33)`** (`p = 10` != `9`) | `495` |
| **Conjecture 9** ($\mathcal{Q}(d,f) = \mathcal{K}_r(d,f)$) | $S_{5,10}$ ($f = 5, d = 5$) | `k = 7` | **`(6, 6, 24)`** (`k = 6` != `7`) | `240` |

- For $S_{4,11}$, the repeating first-difference block is `(1, 6, 1, 1, 7, 1, 7, 1, 7, 1)` of minimal period `10` and modulus `33` (after `11` transient gaps), whereas Definition 3 Clause `(4)` with the `f <= 4` subtraction gives `9`. Across the `4800` primary grid pairs tested, Conjecture 5 agrees on `4799` pairs and fails at `(4, 7)`.
- For $S_{5,10}$, the repeating first-difference block is `(8, 1, 6, 1, 1, 7)` after `6` transient gaps (modulus `24`), whereas Definition 8 Clauses `(d)` and `(k_0)` give `7` (and across the `4800`-pair grid, Definition 8 has `1645` unambiguous mismatches, including negative value `-23` at $S_{12,30}$ whose true minimal parameters are `k = 36, p = 19, m = 71`). Note that the paper's own printed tables already list the correct values at $S_{4,11}$ and $S_{5,10}$; the contradiction is between the printed conjecture formulas and the actual sequences.

## Clean-room cross-family verification

- **Producer:** GPT-6.2 Astra via Codex (`producer/REPORT.md`, `producer/definitions.tex`, `producer/verify_counterexample.py`, `certificates/witness.json`).
- **Clean-room Cross-Family Referee:** Gemini 4 Carbon High via Antigravity CLI (`referee/REFEREE.md`, `referee/REPORT.md`, `referee/referee_verify.py`, producer code withheld). Returned **`VERDICT: HOLDS`** with zero defects in `certificates/witness.json`, `producer/definitions.tex`, or `producer/REPORT.md`. `referee/referee_verify.py` uses pure Python `int` and `fractions.Fraction` only (AST-verified zero `float`, zero `/` operators, zero `math` imports), independently reproducing both dual proofs, `15` positive controls, `16` adversarial negative controls (`8` per witness), all `1845` displayed table entries, and all `4800` primary grid comparisons.


## Standalone Lean 4 formalization

The [`lean/`](lean/) directory contains a self-contained Lean 4 (`leanprover/lean4:v4.36.0`, zero Mathlib dependencies) formalization defining strict greedy 2-sumfree sequences from first principles and proving `S4_11_minimal` (`(11, 10, 33)`), `conj5_disproof_S4_11` (`p = 9` fails), `S5_10_minimal` (`(6, 6, 24)`), `conj9_disproof_S5_10` (`k = 7` is not minimal), four positive controls, and five formal negative controls. It compiles standalone in about three seconds with zero `sorry`, zero `axiom`, zero `native_decide`, and standard core axioms `[propext, Classical.choice, Quot.sound]` only:

```bash
cd lean && python3 -B verify_lean.py
```

## Reproduction

Requires Python 3.10+ (standard library only). From `conjectures/2609-18522-conj5-9/`:

```bash
# 1. Verify file integrity
shasum -a 256 -c SHA256SUMS

# 2. Run producer standalone exact verifier
python3 -c 'import shutil, subprocess, tempfile; d=tempfile.mkdtemp(); shutil.copy("certificates/witness.json", d); shutil.copy("producer/verify_counterexample.py", d); subprocess.run(["python3", "-B", "verify_counterexample.py"], cwd=d, check=True)'
```
