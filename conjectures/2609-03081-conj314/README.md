# Partial supplement to Lewis and Won, Conjecture 3.14 (arXiv:2609.03081v1)

> Partly not first. Xiaojian Zeng proved the order-nine case by exhaustively computing the global maximum $r(9)=28{,}549$ over all $9!$ permutations. The [dated manuscript](https://raw.githubusercontent.com/ArtificialZeng/AI-Has-Taste/f3ae144b74f238f22c2b84b5283cb14ce912fd33/reproducible_source_code/BigWIN2/BW2-B41-P04/source/manuscript/main.tex) was committed on 2026-09-16 at 20:22:55 UTC.
>
> The priority audit found no earlier exact refutation at $n=17$ or $n=18$ and no earlier global maxima at $n=10$ through $n=14$. Those cases are the supplement.

The counterexamples below refute Conjecture 3.14 (`\label{conj:maxlayered}`, TeX line `754`) of Joel Brewster Lewis and Robert Won, *Non-attacking rook placements on crossword grids* ([arXiv:2609.03081v1](https://arxiv.org/abs/2609.03081v1)).

This is AI work. No human has checked it. **Lean status:** `verified` (standalone Lean 4, zero Mathlib, zero `sorry`, standard axioms `[propext, Classical.choice, Quot.sound]`; see [`lean/`](lean/)).

## Conjecture 3.14 (as stated in v1)

> For each $n$, the $n \times n$ permutation grid admitting the most rook placements is given by $\operatorname{Grid}(w)$ where $w \in S_n$ is a layered permutation of shape $(m, 1, 1, \dots, 1, m)$ for some $m$.

## Exact counterexample at n = 17 (and n = 18)

At $n = 17$, the 2-shell nested layered permutation of shape `(5, 3, 1, 3, 5)` (formed from `(5, 1, 1, 1, 1, 1, 1, 1, 5)` by moving `4` black squares off the diagonal),

$$w = (5, 4, 3, 2, 1,\; 8, 7, 6,\; 9,\; 12, 11, 10,\; 17, 16, 15, 14, 13) \in S_{17},$$

has `32` across words and `32` down words and admits strictly more complete non-attacking rook placements than every single-shell layered shape `(m, 1, ..., 1, m)` (and every one of the `136` ordered positive endpoint pairs `(m_1, 1*, m_2)`, consisting of `8` symmetric and `128` strictly unequal pairs, all independently verified both from their raw grids and from Proposition 3.15):

| Order $n$ | 2-shell witness shape | Witness rook placements | Single-shell `(m, 1*, m)` max | Exact strict excess |
|---:|---|---:|---:|---:|
| `17` | `(5, 3, 1, 3, 5)` | **`104476798194769`** | `103460138813701` (`m = 5`) | **`+1016659381068`** |
| `18` | `(5, 3, 1, 1, 3, 5)` | **`2949333362474113`** | `2445624351454501` | **`+503709011019612`** |

## Global maxima through n = 14 and minimality scope

Both producer and clean-room referee independently proved that the conjecture holds unconditionally over all $n!$ permutations through $n = 14$ (covering all `87178291200` permutations of $S_{14}$ by exact branch-and-bound), including the following five global maxima:

- $r(10) = 255569$, $r(11) = 3316625$, $r(12) = 46301969$, $r(13) = 680707985$, $r(14) = 10353226769$.

At $n = 15$ and $n = 16$, exhaustive restricted-family layered and bounded-middle checks attain `202352501701` and `4493953750501` respectively (matching the single-shell maxima), but unconditional minimality of $n = 17$ over all $15!$ and $16!$ permutations remains open. (Note: the prose field `minimality_note` in `certificates/witness.json` summarizes the producer's un-replayed randomized SA runs; the audited scope is stated here and in `referee/REFEREE.md`.)

## Clean-room cross-family verification

- **Producer:** Gemini 4 Carbon High via Antigravity CLI (`producer/REPORT.md`, `producer/verify_counterexample.py`, `certificates/witness.json`).
- **Clean-room Cross-Family Referee:** GPT-6.2 Astra via Codex (`referee/REFEREE.md`, `referee/REPORT.md`, `referee/referee_verify.py`, `referee/verification.txt`, producer code withheld). Independently verified the `n = 17` and `n = 18` counterexamples by matching recurrence, Ryser inclusion-exclusion, and a closed-form 7-square derivation; checked all `46233` permutations for $n \le 8$, all `136` endpoint pairs at $n = 17$, all five global maxima through $n = 14$, and rejected `5` adversarial mutations (`VERDICT: HOLDS WITH CAVEATS` solely for prose/unit clarifications in `producer/REPORT.md` and `minimality_note`, all resolved above).


## Standalone Lean 4 formalization

The [`lean/`](lean/) directory contains a self-contained Lean 4 (`leanprover/lean4:v4.36.0`, zero Mathlib dependencies) formalization defining permutation grids and rook placements from first principles and proving both the `n = 17` counterexample (`104476798194769` vs single-shell maximum `103460138813701`, excess `1016659381068`) and the `n = 18` counterexample (`2949333362474113` vs `2445624351454501`, excess `503709011019612`), plus small-order controls across `31` layered compositions and `153` permutations for `n <= 5`. Direct Lean verification passes with zero `sorry`, zero `axiom`, zero `native_decide`, zero warnings, and standard core axioms `[propext, Classical.choice, Quot.sound]` only:

```bash
cd lean && python3 -B verify_lean.py
```

## Reproduction

Requires Python 3.10+ (standard library integer arithmetic only). From `conjectures/2609-03081-conj314/`:

```bash
# 1. Verify file integrity
shasum -a 256 -c SHA256SUMS

# 2. Run producer standalone exact verifier
python3 -c 'import shutil, subprocess, tempfile; d=tempfile.mkdtemp(); shutil.copy("certificates/witness.json", d); shutil.copy("producer/verify_counterexample.py", d); subprocess.run(["python3", "-B", "verify_counterexample.py"], cwd=d, check=True)'
```
