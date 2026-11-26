Shipped: Exact disproof and complete resolution of van Berkel and Bosma (arXiv:2609.16843v2) Conjecture 4 for every d >= 3, proving that d = 4 has minimal period p = 3 != 4 and modulus m = 27 != 31, d = 3 has (k, p, m) = (5, 1, 5), d = 5 has (k, p, m) = (13, 10, 104), and every d >= 6 has minimal preperiod k = d + 3, minimal period p = d, and exact modulus m = 8d - 3 != 8d - 1, backed by PROOF.md, witnesses.json, and two independent exact verifiers in verify.py.

RESULT: yes

This is AI work. No human has checked it.

## 1. Plain-English Summary and Novelty Verdict

**Did we find something new? Yes.** In *On t-sumfree sequences* (`arXiv:2609.16843v2`, September 2026), Daan van Berkel and Wieb Bosma stated Conjecture 4 (`\label{conj:except}`): for every integer $d \ge 3$, the greedy strict $3$-sumfree sequence $S_{1, d-1, 2d-1}$ is ultimately periodic, and with the exception of $d = 3$ or $d = 5$, its minimal preperiod length is $d + 3$ and its minimal period length is $d$ modulo $8d - 1$.

We disproved Conjecture 4 as stated and proved the complete, exact characterization of $S_{1, d-1, 2d-1}$ for every integer $d \ge 3$:

1. **Unstated exception at $d = 4$ ($S_{1,3,7}$):** Conjecture 4 does not exempt $d = 4$, so it predicts $(k, p, m) = (7, 4, 31)$. In fact, $S_{1,3,7}$ has finite preperiod $(1, 3, 7, 8, 9, 10, 15)$ ($k = 7$) and periodic tail $\{29, 35, 36\} + 27\mathbb{Z}_{\ge 0}$ with repeating difference block $(6, 1, 20)$, giving **minimal period length $p = 3 \ne 4$** and **modulus $m = 27 \ne 31$**. Because $p = 3 \ne 4$, $d = 4$ refutes Conjecture 4 under any reading of "modulo".
2. **Modulus error for every $d \ge 6$:** At $d = 6$ ($S_{1,5,11}$), the minimal preperiod is $(1, 5, 11, 12, 13, 14, 15, 16, 23)$ ($k = 9 = d + 3$) and the minimal period length is $p = 6 = d$, but the periodic tail is $\{55, 56, 57, 58, 59, 60\} + 45\mathbb{Z}_{\ge 0}$, so the **exact modulus is $m = 45 = 8d - 3 \ne 47 = 8d - 1$**. In general, for every integer $d \ge 6$,
   $$S_{1, d-1, 2d-1} = \{1, d-1\} \cup [2d-1, 3d-2] \cup \{4d-1\} \cup \bigcup_{j \ge 0} \bigl([10d-5, 11d-6] + j(8d-3)\bigr),$$
   with minimal preperiod length $k = d + 3$, minimal period length $p = d$, and exact modulus $m = 8d - 3$ (off by $2$ from Conjecture 4's $8d - 1$).
3. **Exact resolution of the two small exceptions $d = 3$ and $d = 5$:**
   - **$d = 3$ ($S_{1,2,5}$):** preperiod $(1, 2, 5, 6, 7)$ ($k = 5$) and tail $\{11\} + 5\mathbb{Z}_{\ge 0}$ ($p = 1, m = 5$).
   - **$d = 5$ ($S_{1,4,9}$):** preperiod $(1, 4, 9, 10, 11, 12, 13, 19, 37, 45, 46, 72, 79)$ ($k = 13$) and tail $\{80, 81, 114, 115, 116, 123, 149, 150, 158, 176\} + 104\mathbb{Z}_{\ge 0}$ ($p = 10, m = 104$).
4. **Why $d = 3, 4, 5$ diverge while $d \ge 6$ stabilizes:** Up to $4d - 1$, every $S_{1, d-1, 2d-1}$ ($d \ge 3$) agrees with $S_0 = \{1, d-1\} \cup [2d-1, 3d-2] \cup \{4d-1\}$. Covering the gap $[4d, 10d-6]$ by strict $3$-sums from $S_0$ requires two boundary overlaps: $d \ge 4$ to prevent a hole at $16$ when $d = 3$, and $9d - 9 \ge 8d - 3$ (which holds if and only if $d \ge 6$) so that triple sums from $[2d-1, 3d-2]$ bridge across $8d - 3$ to meet $[8d-2, 10d-6]$. At $d = 4$ and $d = 5$, the integer $8d - 3$ ($29$ and $37$, respectively) goes uncovered and enters the sequence early.

## 2. Deliverables and Artifacts

- [PROOF.md](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree/PROOF.md): Self-contained mathematical disproof and proof of Theorem 1 ($d = 3, 4, 5$) and Theorem 2 (every $d \ge 6$, covering Part A Exclusion, Part B Inclusion and $d = 3, 4, 5$ breakdown, and Part C Minimality).
- [witnesses.json](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree/witnesses.json): Structured machine-checkable certificates for $d = 3..40$ (both Lemma 3 cutoffs and generating-function degrees), residue-class certificates for $d = 3, 4, 5$, affine symbolic proof data for $d \ge 6$, and negative controls.
  - **SHA-256 of `witnesses.json`:** `e40f8d4cd1523372c403614f0f25d653fb9e631bf363cda61176783fe6c07918`
- [verify.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree/verify.py): Standalone pure-Python exact verifier (no external libraries, no producer imports).
- [PRIOR_ART.md](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree/PRIOR_ART.md) and [STATUS.md](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree/STATUS.md): Prior-art survey, baseline reproduction, frozen protocol, and checkpoint log.

## 3. Verification Status, Controls, and Why No Statistical Holdout Applies

**Why no statistical holdout or SBS baseline applies:** This task settles an exact universal mathematical statement over $\mathbb{Z}_{\ge 1}$ rather than fitting a statistical or predictive model on noisy data. There is no train/test split or trivial/linear score metric; instead, soundness relies on producer/verifier separation, two mathematically independent exact proof engines, symbolic verification over $\mathbb{Z}[d]$, and explicit negative controls.

All checks in [verify.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree/verify.py) passed in `4.74s` with exit code `0`:
1. **Dual Finite-Cutoff Certificates ($d = 3..40$, plus $d = 50, 100$):** Every $d \in \{3, \dots, 40\}$ (and $d \in \{50, 100\}$) passed both:
   - *Engine 1 (`verify_via_lemma3_greedy`):* Direct bitset greedy strict $3$-sumfree simulation up to the rigorous cutoff $K + Q m$ of van Berkel and Bosma Lemma 3 (`(Q - 6)m >= 2K`), cross-checked against a separate naive $O(|S|^3)$ loop for $d = 3..12$, plus Lemma A minimality checks.
   - *Engine 2 (`verify_via_generating_function`):* Exact integer polynomial arithmetic on $6 r_3(n) = [x^n](A(x)^3 - 3A(x)A(x^2) + 2A(x^3)) = [x^n] T(x)/(1 - x^{6m})^3$, checking every integer in $[2d, \max(\deg T, b_p)]$ and all $6m$ quadratic Newton-difference progressions $(\alpha, \beta, \gamma)$.
2. **Small-Case Residue Certificates ($d = 3, 4, 5$):** Verified residue-class exclusion modulo $m_d \in \{5, 27, 104\}$ and explicit linear gap coverings across all non-member residues.
3. **Symbolic & Concrete Proof Checks ($d \ge 6$):** Exact affine-form verifier (`Affine(c1, c0)` over $\mathbb{Z}[d]$) proved all $20$ distinct-valid block-triple combinations (out of $35$ unordered $3$-multisets of the $5$ blocks), all $8$ unified residue-multiset types, all $11$ gap-covering intervals ($G_{\text{pre},1}$, $B_1..B_5$, $C_{1,j}..C_{5,j}$), the exact $d = 3, 4, 5$ first holes ($16, 29, 37$), and Part C minimality inequalities for all $d \ge 6$; additionally checked $221,653$ concrete residue triples across $d \in \{6, 7, 8, 9, 10, 50, 100\}$.
4. **Negative Controls Rejected (5/5 rejected by both Engine 1 and Engine 2):**
   - `NC_a_d4_conjectured_p4_m31`: Conjecture 4's $d = 4$ parameters ($k = 7, p = 4, m = 31$ using actual greedy terms `(29, 35, 36, 56)`).
   - `NC_b_d6_conjectured_m47`: Conjecture 4's $d = 6$ modulus ($k = 9, p = 6, m = 47$).
   - `NC_c_corrupted_preperiod_element`: Corrupted preperiod at $d = 6$ (`23 -> 24`).
   - `NC_d_nonminimal_period_multiple_2p`: Set-equivalent $2p = 12, 2m = 90$ representation at $d = 6$.
   - `NC_e_nonminimal_preperiod_shifted`: Set-equivalent $k + p = 15$ representation at $d = 6$.

**Failed check logged during development:** On the first run of `verify.py`, `verify_small_residue_certificates` failed at line 409 on $d = 3$ because it bounded $3$-element sums from $1 + 5\mathbb{Z}_{\ge 0}$ by $1 + 1 + 1 = 3 \le 7 = \max(F_3)$, ignoring that strictness forces distinct summands ($1 + 6 + 11 = 18 > 7$). We replaced that bound in [verify.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree/verify.py#L417-L423) with an exact check over all strictly increasing triples in $A_d \cap [1, \max(F_d) - 1]$.

## 4. Referee Self-Audit Verdict

- `CONTROLS:` **No** assumption overrode what the controls show. Checked in [verify.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree/verify.py#L698-L742) via `nice -n 10 python3 verify.py`, which executed all `5` negative controls (`NC_a` through `NC_e`) against both Engine 1 and Engine 2 and verified `10/10` rejections (`"negative_controls_rejected": 5`), while cross-checking bitset greedy simulation against naive $O(|S|^3)$ simulation across `10` sequences ($d = 3..12$, exact match on every term).
- `CONTRADICTING:` **No** contradicting data was dropped or ignored. Checked across all `38` parameter values $d = 3..40$ plus $d = 50, 100$ (`40` sequences total) in [witnesses.json](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree/witnesses.json) and [verify.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree/verify.py#L755-L796): all three deviations from the $d \ge 6$ formula ($d = 3, 4, 5$) are explicitly retained, proved, and explained in [PROOF.md](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree/PROOF.md#L118-L246) and Section 5 Part B(3).
- `LABELS:` **No** label or paper annotation was trusted without checking raw definitions and source text. Checked directly against [2609.16843v2.tex.json.gz](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree/inputs/2609.16843v2.tex.json.gz) (`main.tex` lines 51-119 for $S_{f,g,h}, C_{f,g,h}, D_{f,g,h}, k, p, m$; lines 164-169 for Conjecture 4; lines 278-330 for Lemma 3; lines 1226-1335 confirming $(1, d-1, 2d-1)$ was omitted from Table 1), which is precisely how the paper's unverified `8d - 1` label and missed `d = 4` exception were caught.

## 5. Exact Reproduction Commands

From `/Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree`:

```bash
# 1. Verify SHA-256 digest of witnesses.json
shasum -a 256 witnesses.json
# Expected: e40f8d4cd1523372c403614f0f25d653fb9e631bf363cda61176783fe6c07918  witnesses.json

# 2. Run both independent exact verifiers, symbolic proof checks, and negative controls
nice -n 10 python3 verify.py

# 3. Reproduce baseline check from workspace input script (d=4 and d=6)
nice -n 10 python3 inputs/csweep1_verify_witnesses.py
```

## 6. Sources, Limitations, and Next Steps

- **Sources:**
  - Daan van Berkel and Wieb Bosma, *On $t$-sumfree sequences*, `arXiv:2609.16843v2 [math.NT]` (local archive [2609.16843v2.tex.json.gz](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree/inputs/2609.16843v2.tex.json.gz)).
  - Neil J. Calkin and Steven R. Finch, *Conditions on Periodicity for SumFree Sets*, Experimental Mathematics 5:2 (1996), 131-137.
  - Prior workspace baseline script [csweep1_verify_witnesses.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree/inputs/csweep1_verify_witnesses.py) (credited for the rational generating-function identity over $L = 6m$).
- **Limitations:**
  - Per the job specification (`Lean status: none`), the general $d \ge 6$ proof in [PROOF.md](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree/PROOF.md) is checked by a custom symbolic affine verifier in pure Python ([verify.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree/verify.py)) rather than a foundational proof assistant kernel.
  - Our results resolve the boundary family $S_{1, d-1, 2d-1}$ ($f = 1, g = d - 1, h = 2d - 1$) completely, but do not address deeper uncovered families $S_{f, g, g+d}$ with $f + g \le d - 1$ (such as the five open triples in Remark 10 of `arXiv:2609.16843v2`).
- **Next Steps:**
  - Investigate the next sub-boundary family $S_{1, d-2, 2d-2}$ ($f + g = d - 1$) across $d \ge 4$ (in Table 1 of `arXiv:2609.16843v2`, $(1, 3, 8), (1, 4, 10), (1, 5, 12), (1, 6, 14), (1, 7, 16), (1, 8, 18)$ show growing period lengths $6, 6, 32, 51, 74, 101$, suggesting a quadratic period family in $d$).
  - If authorized by a human reviewer, prepare a concise erratum/corrigendum note for the authors of `arXiv:2609.16843v2` (no external contact has been made).
