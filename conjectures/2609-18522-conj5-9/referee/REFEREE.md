VERDICT: HOLDS

# Clean-Room Cross-Family Referee Report: Disproof of van Berkel & Bosma (arXiv:2609.18522v1) Conjectures 5 & 9

This is AI work. No human has checked it.

## Executive Summary

An independent, adversarial, clean-room mathematical audit of `inputs/2609.18522v1.tex.json.gz`, `inputs/definitions.tex`, `inputs/witness.json`, and `inputs/REPORT.md` confirms **`VERDICT: HOLDS`** with **zero defects**:

1. **Conjecture 5 (`\label{conj:per}`, `main.tex` lines 403–406) is refuted by $S_{4,11}$ ($f=4, d=7$):**
   - Definition 3 (`\label{def:LL}`, lines 285–344) unambiguously evaluates to $\mathcal{L}_4(7) = 9$.
   - The strict greedy $2$-sumfree sequence $S_{4,11}$ is certified by two independent exact proofs to have minimal preperiod $k = 11$, minimal period $p = 10 \ne 9$, and modulus $m = 33$.
2. **Conjecture 9 (`\label{conj:pre}`, `main.tex` lines 708–712) is refuted by $S_{5,10}$ ($f=5, d=5$):**
   - Definition 8 (`\label{def:KK}`, lines 510–703) unambiguously evaluates to $\mathcal{K}_5(5,5) = 7$ (and more generally $\mathcal{K}_f(f,f) = 2f - 3$ for all $f \ge 5$, contradicting the paper's own Theorem 14 proving $k = f + 1$).
   - The sequence $S_{5,10}$ is certified by two independent exact proofs to have minimal preperiod $k = 6 \ne 7$, minimal period $p = 6$, and modulus $m = 24$.
3. **Every field of `inputs/witness.json` and every concrete claim in `inputs/REPORT.md` (including all 1,845 displayed array entries in `main.tex`, Example 18, and all 4,800 primary grid comparisons) reproduced identically from scratch** in pure `int` + `fractions.Fraction` Python ([referee_verify.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/referee_verify.py)).

---

## 1. Primary-Source Verbatim Formula & Clause Audit

All checks were conducted directly against `main.tex` (1,043 lines, UTF-8 length 46,164 bytes, SHA-256 `627fc91a31108750b06dc1f465a80d1768cc23448ec5f10ab239a086917d9bf3`) inside [2609.18522v1.tex.json.gz](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/inputs/2609.18522v1.tex.json.gz).

### 1.1 Sequence, Period, Preperiod, and Cutoff Definitions
- **Strict greedy $2$-sumfree sequence $S_{f,g}$ (`main.tex` lines 60–71):** Initialized by $s_0 = f \ge 1$ and $s_1 = g > f$; for $i \ge 2$, $s_i$ is the smallest integer $> s_{i-1}$ not representable as $s_a + s_b$ with $0 \le a < b < i$.
- **Difference and characteristic sequences (`main.tex` lines 77–115):** $D_{f,g} = (s_i - s_{i-1})_{i \ge 1}$ and $1$-indexed $C_{f,g} = (c_n)_{n \ge 1}$ with $c_n = \mathbf{1}_{n \in S_{f,g}}$. Minimal preperiod length $k = \mathcal{Q}(d,f)$ and minimal period length $p = \mathcal{P}(d,f)$ ($d = g - f$) are the minimal $k \ge 0, p \ge 1$ such that $d_{i+p} = d_i$ for all $i \ge k + 1$, equivalently $s_{i+p} = s_i + m$ for all $i \ge k$ where $m = \sum_{j=k+1}^{k+p} d_j$.
- **Theorem 15 (`\label{corollary}`, `main.tex` lines 958–994):** If for $M > 0$ the $1$-indexed prefix $C_{f,g}[1\dots 5M]$ consists of five blocks $M_0, M_1, M_2, M_3, M_4$ of length $M$ with $M_1 = M_2 = M_3 = M_4 \ne 0^M$, then $c_u = c_{u-M}$ for all $u \ge 2M + 1$ (hence $c_{u+M} = c_u$ for all $u \ge M + 1$).
  - *Adversarial proof check:* Line 979 invokes "$c_u = 0$ iff $u$ is a sum of two distinct elements of $S$", which holds only for $u > g$. Because $M_1$ and $M_2$ are both non-null, $|S_{f,g} \cap [1, 3M]| \ge 2$, forcing $g = s_1 \le 3M < 4M + 1 \le v - M < v$ at the minimal potential failure $v \ge 5M + 1$. Also $v \ge 5M + 1 \implies r_2 \ge 2M + 1$, and when $r_2 = r_1 + M$, $2r_1 + M \ge 5M + 1 \implies r_1 \ge 2M + 1$. Thus Theorem 15 holds without gap in $1$-based indexing.

### 1.2 Adversarial Audit of Definition 3 & Conjecture 5 at $(f, d) = (4, 7)$ ($S_{4,11}$)
- **Conjecture 5 (`main.tex` lines 403–406):**
  ```tex
  \begin{conjecture}\label{conj:per}
  For all $f, d=g-f\geq 1$ the strict, greedy 2-sum sequence
  $S_{f,g}$ is ultimately periodic with length of the period $\PP(d,f)=\LL_f(d)$.
  \end{conjecture}
  ```
- **Definition 3 (`main.tex` lines 285–344) evaluated at $(f, d) = (4, 7)$:**
  - Line 286: $q_- = \lfloor 4/2 \rfloor = 2$, $q^+ = \lceil 4/2 \rceil = 2$.
  - Line 292, Clause `(1)`: $1 \le d \le f - 1 = 3$ — does not apply.
  - Lines 294–295: blocks of length $2f = 8$ for $k \ge 1$ cover $[(2k-1)f, (2k+1)f - 1] = [8k-4, 8k+3]$; $d = 7$ lies uniquely in block $k = 1$ ($[4, 11]$). Even without pre-selecting block $k$, $(2k-1)f \ge 12 > 7$ for all $k \ge 2$.
  - Line 297, Clause `(2)`: $d = 4 + j$ for $0 \le j \le 2$ ($d \in \{4, 5, 6\}$) — does not apply.
  - Line 298, Clause `(3)`: requires odd $f$ — does not apply.
  - Line 300, Clause `(4)`:
    `$\LL_f(d)=k(f+1+q_{-})+q^{+}+1-j\cdot (k-1)$, if $d=(2k-1)f+q^{+}+1+j$ for $0\leq j\leq q_{-}+1$;`
    At $k = 1$, $d = 4 + 2 + 1 + j = 7 + j$ ($0 \le j \le 3$), so $d = 7$ uniquely selects $j = 0$, giving $1(4 + 1 + 2) + 2 + 1 - 0 \cdot 0 = 10$.
  - **Lines 301–302 correction (verbatim):**
    ```tex
    \item[] with the correction that, if $f\leq 4$ or $k>1$ then $k$ 
    is to be subtracted from $\LL_f(2kf-1)$;
    ```
    At $f = 4, k = 1$, $2kf - 1 = 2(1)(4) - 1 = 7 = d$, and $f \le 4$ holds ($4 \le 4$), subtracting $k = 1$ to give $10 - 1 = 9$.
  - Lines 303–305, Clause `(5)`: $11 \le d \le 11$ — does not apply.
  - Lines 336–342 (`for $f=4$:` modifications): modify only $d = 5$, $d = 36$, and $d \equiv 4 \bmod 8$ with $d \ge 44$ — none applies to $d = 7$.
- **Can any alternative reading rescue Conjecture 5?** **No.** Notice that in `if $f\leq 4$ or $k>1$`, the disjunct `$k > 1$` already holds for all $k \ge 2$, so `$f = 4$` in `$f \leq 4$` affects *exclusively* the single point $(f, k) = (4, 1) \implies (f, d) = (4, 7)$. The authors needed the $k = 1$ subtraction at $f = 1, 2$ ($d = 1, 3$), wrote `$f \leq 4$` instead of `$f \leq 3$` (or `$f \leq 2$`), and left $(4, 7)$ uncorrected in the small-$f$ list. Consequently, Conjecture 5 (and Theorems 16 & 17 on lines 1005–1021, which claim Conjecture 5 holds for all $f, d \le 250$ and $f, d \le 500$) is literally false at $(4, 7)$.

### 1.3 Adversarial Audit of Definition 8 & Conjecture 9 at $(f, d) = (5, 5)$ and $(12, 18)$
- **Conjecture 9 (`main.tex` lines 708–712):**
  ```tex
  \begin{conjecture}\label{conj:pre}
  For all $f, d=g-f\geq 1$ the strict, greedy 2-sum sequence
  $S_{f,g}$ is ultimately periodic with preperiod length
  	$\QQ(d,f)=\KK_{r}(d,f)$, where $r\equiv d\bmod 2f$.
  \end{conjecture}
  ```
- **At $(f, d) = (5, 5)$ ($S_{5,10}$):**
  - Lines 511–513: $d = r + h \cdot (2f)$ with $1 \le r \le 2f = 10$ fixes $r = 5, h = 0$.
  - Line 517 (`For $f\geq 5$`): uniquely selects Clause `(d)` (line 526):
    `\item[(d)] $\KK_{f}(h,f)=(4f+1)\cdot h+(5f-3)$;`
    giving $21 \cdot 0 + 22 = 22$.
  - Lines 561–573, Clause `(k)` corrections:
    - Line 565, `(k_0)`: `\item[(k$_0$)] if $h=0$, subtract $2f+r$ from $\KK_{r}$;` — applies ($h = 0$), subtracting $2(5) + 5 = 15$ to give $22 - 15 = 7$.
    - Lines 566–572, `(k_1)`–`(k_7)`: require $h = 1$, $h = 2$, or $r \in \{1, 2, 3\}$ — none applies.
  - *Can any alternative reading rescue Conjecture 9 at $(5, 5)$?* **No.** Without `(k_0)` the formula gives $22 \ne 6$; with `(k_0)` it gives $7 \ne 6$ (and if $d=5$ were substituted for $h$ literally from line 711's notation $\mathcal{K}_r(d,f)$, it would give $127$ or $112$, still $\ne 6$). Moreover, for every $f = d \ge 5$, `(d)` + `(k_0)` gives $5f - 3 - 3f = 2f - 3$, contradicting the paper's own Theorem 14 (lines 887–898) which proves $k = f + 1$.
- **At $(f, d) = (12, 18)$ ($S_{12,30}$):**
  - $2f = 24 \implies r = 18, h = 0$. Since $f = 12 \ge 6$ is even, $q = \lfloor 13/2 \rfloor = 6$, $f + q = 18 = r$, $s = 0$.
  - Clause `(h_0)` (lines 536–537) gives $\frac{3f + 2}{2} = \frac{38}{2} = 19$ at $h = 0$.
  - Clause `(k_0)` (line 565) subtracts $2f + r = 24 + 18 = 42$, yielding $\mathcal{K}_{18}(18, 12) = 19 - 42 = -23$ (a negative integer!). Even if `(k_0)` were omitted on quadratic branches, `(h_0)` gives $19 \ne 36$.

### 1.4 Internal Contradictions in the Paper's Own Tables and Examples
All reported contradictions inside `main.tex` were independently confirmed:
- `main.tex` prints the true sequence values `P(7, 4) = 10` (line 213 and `P[1..25, 4]` at line 415) and `K(5, 5) = 6` (line 182 and `Q[1..25, 5]` at line 731), contradicting its own $\mathcal{L}_4(7) = 9$ and $\mathcal{K}_5(5,5) = 7$ even where lines 409 and 715 label those rows "conjectured values".
- Across all 1,845 displayed array entries in `main.tex`, every entry matches the true greedy sequence, while disagreeing with the paper's formulas at `115/400` ($20 \times 20$ $K$), `1/400` ($20 \times 20$ $P$), `1/150` ($6 \times 25$ $P$), `27/150` ($6 \times 25$ $Q$), `0/170` ($f=19$ $P$), `0/107` ($f=12$ $P$), and `87/234` (each of the two $f=9$ $Q$ displays).
- Line 100 prints 64 bits of $C_{3,7}$ with 7 bit errors (first at $n = 46$: printed `0`, true `1`), whereas line 105 prints the correct 25-bit barred word.
- Example 18 (lines 1022–1033) prints $k = 17{,}341$ for $S_{3,248}$ ($d = 245$), whereas both $S_{3,248}$ and Definition 8 give $k = 17{,}340$ ($p = 2$); it also prints $(k, p) = (71{,}709, 2)$ for $S_{3,497}$ ($d = 494$), whose certified pair is $(505, 251)$, whereas $(71{,}709, 2)$ is the certified pair of $S_{3,500}$ ($d = 497$, confusing $g$ and $d$).

---

## 2. Independent Exact Computational Verification

[referee_verify.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/referee_verify.py) enforces pure `int` + `fractions.Fraction` arithmetic via an AST self-check (forbidding `float`, `/`, and `math`) and cross-checks two greedy sequence generators (naive $O(|S|^2)$ pair-set and chunked arbitrary-precision `int` bitmask) with two independent periodicity proof engines:

| Sequence | $(f,d)$ | Certified $(k, p, m)$ | Proof I: Theorem 15 Cutoff | Proof II: Rational GF $H(z)/(1-z^{2m})^2$ | Formula Value | Status |
|---|---|---|---:|---|---|---|
| $S_{4,11}$ | $(4,7)$ | $(11, 10, 33)$ | $M=99, 5M=495$ ($30$ ones/block) | $\deg N=69, \deg H=204$, affine $\ge 205$, stride $66$ | $\mathcal{L}_4(7)=9$ | Refutes Conj. 5 |
| $S_{5,10}$ | $(5,5)$ | $(6, 6, 24)$ | $M=48, 5M=240$ ($12$ ones/block) | $\deg N=38, \deg H=120$, affine $\ge 125$, stride $48$ | $\mathcal{K}_5(5,5)=7$ | Refutes Conj. 9 |
| $S_{12,30}$ | $(12,18)$ | $(36, 19, 71)$ | $M=142, 5M=710$ ($38$ ones/block) | $\deg N=220, \deg H=558$, affine $\ge 583$, stride $142$ | $\mathcal{K}_{18}(18,12)=-23$ | Refutes Conj. 9 |

- **Minimality proofs:**
  - For $S_{4,11}$: repeating gap word $(1,6,1,1,7,1,7,1,7,1)$ fails divisor periods $1, 2, 5$ (unique `6`), proving minimal $p = 10$; transient gap $d_{11} = 37 - 29 = 8 \ne 1 = d_{21}$ proves minimal $k = 11$.
  - For $S_{5,10}$: repeating gap word $(8,1,6,1,1,7)$ fails divisor periods $1, 2, 3$ (unique `8`), proving minimal $p = 6$; transient gap $d_6 = 20 - 14 = 6 \ne 7 = d_{12}$ proves minimal $k = 6$.
- **Positive controls (15 sequences):** 14 full positive controls ($S_{1,2}, S_{1,3}, S_{2,3}, S_{2,4}, S_{2,5}, S_{2,8}, S_{3,6}, S_{3,7}, S_{4,10}, S_{4,12}, S_{5,9}, S_{5,35}, S_{5,36}, S_{6,11}$) passed both Theorem 15 and GF proofs and matched both $\mathcal{L}_f(d)$ and $\mathcal{K}_r(d,f)$; $S_{5,11}$ ($f=5, d=6$) was also certified as $(k, p, m) = (6, 7, 29)$, matching $\mathcal{L}_5(6) = 7$ and printed $K(6,5)=6$ while exhibiting an additional Conjecture 9 failure ($\mathcal{K}_6(6,5) = 1 \ne 6$).
- **Adversarial negative controls (16 mutants, 8 per witness):** For both $S_{4,11}$ and $S_{5,10}$, [referee_verify.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/referee_verify.py) constructed and rejected all 8 mutations: printed wrong period/preperiod (`p=9` / bogus `k=7`), doubled period (`2p, 2m`), delayed onset (`k+1` — which for $S_{5,10}$ is also `k=7`), premature onset (`k-1`), corrupted last preperiod term (`+1`), corrupted last period term (`+1`), corrupted modulus (`m+1`), and swapped adjacent distinct periodic gaps (`8/8` rejected per witness).
- **Witness & Grid Audit:** Every key, array, integer, SHA-256 digest, and `tex_lines` entry in [witness.json](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/inputs/witness.json) (lines 1–142) matched with zero discrepancies. An independent replay of all 4,800 primary grid pairs reproduced `4,799` period agreements / `1` disagreement, `3,152` preperiod agreements / `1,645` disagreements / `3` overlaps (`(2,2), (2,6), (2,10)`), `1,646` distinct discrepant seeds, `113` half-integers, and `505` negative formula values.

---

## 3. Mandatory Referee Checks

- `CONTROLS:` **No** — no assumption overrode what the controls show. Checked by running `nice -n 10 python3 -B referee_verify.py` ([referee_verify.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/referee_verify.py#L465-L905)), which verified 15 positive controls via both Theorem 15 and the independent rational generating-function identity (`14/14` matching both Definitions 3 & 8, plus $S_{5,11}$ matching Definition 3 and exposing $\mathcal{K}_6(6,5)=1 \ne 6$) and rejected `16/16` adversarial negative controls (`8/8` per witness, including doubled period `2p`, delayed onset `k+1`, premature onset `k-1`, printed wrong formula length, corrupted preperiod/tail terms, corrupted modulus, and swapped periodic gaps).
- `CONTRADICTING:` **No** — no data contradicting or qualifying the conclusion was dropped or ignored. Checked across all 1,845 displayed entries in `main.tex` ([referee_verify.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/referee_verify.py#L918-L1060)) and all 4,800 primary grid seeds: Conjecture 5 agrees on `4,799/4,800` primary grid pairs (failing solely at $(f,d)=(4,7)$, with `0/8` neighbor failures and `0/24` other failures on $d = 8b-1 \le 199$ at $f=4$), the 3 overlapping-clause pairs $(2,2), (2,6), (2,10)$ from `main.tex` line 607 were retained separately from the `1,645` unambiguous preperiod failures, and the 7 bit typos in `main.tex` line 100 (out of 64 bits, first at $n=46$) were explicitly verified alongside the correct 25-bit word at line 105.
- `LABELS:` **No** — no label, table caption, or annotation was trusted without checking against the raw sequence and raw LaTeX bytes. Checked against `inputs/2609.18522v1.tex.json.gz` (`main.tex` lines 1–1043, SHA-256 `627fc91a31108750...`) and [witness.json](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_sumfree2_referee/inputs/witness.json#L1-L142): all 18 quoted `tex_lines` strings were checked character-for-character against `main.tex`, the rows labeled "conjectured values" at `main.tex` lines 409–417 and 715–735 were checked against both raw sequences and Definitions 3 & 8 (revealing they print raw sequence values rather than formula outputs), and Example 18's label `$S_{3,497}$` at line 1032 was checked at both $g=497$ ($S_{3,497} \implies (505, 251)$) and $d=497$ ($S_{3,500} \implies (71709, 2)$).
