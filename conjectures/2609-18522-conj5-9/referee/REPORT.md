Shipped: clean-room referee certification (`VERDICT: HOLDS`) confirming the exact disproofs of Conjectures 5 and 9 in van Berkel & Bosma (arXiv:2609.18522v1) via $S_{4,11}$ ($p=10 \ne 9$) and $S_{5,10}$ ($k=6 \ne 7$), with zero defects in `inputs/witness.json` or `inputs/REPORT.md`.

VERDICT: HOLDS
RESULT: yes

This is AI work. No human has checked it.

## Summary of Referee Result

**Did this clean-room audit find a defect in the producer's disproof or find a new counterexample beyond the producer's report? No.** This is an independent clean-room referee verification task. Using only `inputs/` and a newly written pure-Python (`int` + `fractions.Fraction` only, AST-checked for zero `float`, zero `/` operators, and zero `math` imports) verifier [referee_verify.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/referee_verify.py), we confirmed that:

1. **Conjecture 5 (`main.tex` lines 403–406) is genuinely refuted by $S_{4,11}$ ($f=4, d=7$):** Definition 3 (`main.tex` lines 285–344) unambiguously gives $\mathcal{L}_4(7) = 9$ via Clause `(4)` ($10$) minus the explicit `$f \leq 4$ or $k > 1$` subtraction at $2kf - 1 = 7$ (lines 301–302), whereas $S_{4,11}$ has certified minimal $(k, p, m) = (11, 10, 33)$ ($p = 10 \ne 9$).
2. **Conjecture 9 (`main.tex` lines 708–712) is genuinely refuted by $S_{5,10}$ ($f=5, d=5$):** Definition 8 (`main.tex` lines 510–703) unambiguously gives $\mathcal{K}_5(5,5) = 22 - 15 = 7$ via Clauses `(d)` and `(k₀)`, whereas $S_{5,10}$ has certified minimal $(k, p, m) = (6, 6, 24)$ ($k = 6 \ne 7$). We also confirmed $S_{12,30}$ ($f=12, d=18$) has certified $(k, p, m) = (36, 19, 71)$ while Definition 8 evaluates to $\mathcal{K}_{18}(18, 12) = -23$.
3. **Zero defects in [witness.json](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/inputs/witness.json), [definitions.tex](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/inputs/definitions.tex), and [REPORT.md](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/inputs/REPORT.md):** Every field of `inputs/witness.json` (including SHA-256 digest and all 18 verbatim `tex_lines` quotations), all 1,845 displayed array entries in `main.tex`, Example 18 ($S_{3,248}, S_{3,497}, S_{3,500}, S_{332,831}, S_{332,832}$), $(f,d)=(8,59)$ ($\mathcal{K} = 645/2$ vs $k = 265$), and the full 4,800-seed primary grid summary (`4,799 / 1`, `3,152 / 1,645 / 3`, `1,646` distinct discrepant seeds, `113` half-integers, `505` negative values) reproduced identically from scratch.

Full line-by-line mathematical analysis and audit tables are in [REFEREE.md](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/REFEREE.md), and clean-room literature baselines are in [PRIOR_ART.md](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/PRIOR_ART.md).

## Exact Reproduction Commands

From `/Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee`:

```sh
# Full verification (~105s on M5: AST self-audit, witness.json, dual proofs, 15 positive controls,
# 16 negative controls, S_{12,30}, all 1,845 printed table entries, and Example 18):
nice -n 10 python3 -B referee_verify.py

# Fast core witness + controls verification (<1s):
nice -n 10 python3 -B referee_verify.py --skip-tables
```

## Mandatory Referee Verdict Checks

- `CONTROLS:` **No** — no assumption overrode what the controls show. `nice -n 10 python3 -B referee_verify.py` ([referee_verify.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/referee_verify.py#L465-L905)) verified 15 positive controls via two independent sequence generators and two independent periodicity proofs (`14/14` matching both Definitions 3 & 8, plus $S_{5,11}$ matching Definition 3 and exposing $\mathcal{K}_6(6,5)=1 \ne 6$) and rejected `16/16` adversarial negative controls (`8/8` per witness: printed wrong length, doubled period `2p`, delayed onset `k+1`, premature onset `k-1`, corrupted preperiod term, corrupted tail term, corrupted modulus, and swapped periodic gaps).
- `CONTRADICTING:` **No** — no contradicting data was dropped or ignored. Checked across all 1,845 displayed entries in `main.tex` ([referee_verify.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/referee_verify.py#L918-L1060)) and all 4,800 primary grid pairs: Conjecture 5 holds on `4,799/4,800` primary pairs (failing solely at $(4,7)$), the 3 overlapping-clause pairs $(2,2), (2,6), (2,10)$ at `main.tex` line 607 were separated from the `1,645` unambiguous preperiod failures, and the 7 bit typos out of 64 at `main.tex` line 100 (first at $n=46$) were reported alongside the accurate 25-bit word at line 105.
- `LABELS:` **No** — no label or annotation was trusted without checking against raw data. Checked against `inputs/2609.18522v1.tex.json.gz` (`main.tex` lines 1–1043) and [witness.json](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/inputs/witness.json#L1-L142): all 18 `tex_lines` strings were verified byte-for-byte against `main.tex`, the displays labeled "conjectured values" (`main.tex` lines 409–417, 715–735) were tested against both raw sequences and formula definitions, and Example 18's `$S_{3,497}$` (`main.tex` line 1032) was evaluated at both $g=497$ ($(505, 251)$) and $d=497$ ($S_{3,500} \implies (71{,}709, 2)$).

## Statistical Holdout Note, Sources, Limitations & Next Steps

- **Why no statistical holdout or `BASELINES.json` applies:** Conjectures 5 and 9 are universal deterministic statements over $\mathbb{Z}_{\ge 1}^2$, settled in the negative by exact finite certificates verified over all $n \ge 1$ via both Theorem 15 and rational generating functions. There are no fitted parameters, random splits, or predictive metrics.
- **Sources:** Strictly `inputs/2609.18522v1.tex.json.gz` (van Berkel & Bosma, arXiv:2609.18522v1), `inputs/definitions.tex`, `inputs/REPORT.md`, and `inputs/witness.json`. Input SHA-256 digests were verified unchanged.
- **Limitations:** While Conjectures 5 and 9 (and Theorems 16 and 17 as literally stated in v1) are refuted as written, Conjecture 1 (that every strict greedy $2$-sumfree sequence is eventually periodic) remains open; in particular, both counterexample sequences $S_{4,11}$ and $S_{5,10}$ *are* ultimately periodic.
- **Next steps:** If van Berkel & Bosma post a v2 revision on arXiv updating Definition 3 (changing `$f \leq 4$` to `$f \leq 3$` on line 301) and Definition 8 (fixing the $h=0, 1, 2$ corrections and quadratic parity denominators), [referee_verify.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/referee_verify.py) can immediately test the revised formulas against the certified grid.
