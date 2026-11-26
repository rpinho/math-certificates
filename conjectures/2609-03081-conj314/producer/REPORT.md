Shipped: Exact counterexample at n=17 disproving Conjecture 3.14 (conj:maxlayered) of Lewis & Won (arXiv:2609.03081v1): the 2-shell layered permutation w = (5,4,3,2,1,8,7,6,9,12,11,10,17,16,15,14,13) of shape (5,3,1,3,5) achieves |RP(Grid(w))| = 104,476,798,194,769 > 103,460,138,813,701 = max_m |RP(Grid(layered(m,1,...,1,m)))|, certified by witness.json and verify_counterexample.py.

RESULT: yes

- **Did we find something new?** **Yes.** We settle open **Conjecture 3.14 (`\label{conj:maxlayered}`)** of Joel Brewster Lewis and Robert Won, *Non-attacking rook placements on crossword grids* (`arXiv:2609.03081v1`, Sep 2026), in the negative by exhibiting an explicit permutation $w \in S_{17}$ (and families for $n = 18, 19, 20$) whose crossword grid admits strictly more complete non-attacking rook placements than any layered permutation of shape $(m, 1, 1, \dots, 1, m)$. In addition, we establish five new exact values of $r(n) = \max_{u \in S_n} |\operatorname{RP}(\operatorname{Grid}(u))|$ ($n = 10..14$) via exact branch-and-bound over all $n!$ permutations. For **Conjecture 3.9 (`\label{conj:skewmerged}`)**, our search found **no** counterexample (confirming Conjecture 3.9 exhaustively for all $n \le 14$ and across $5.5 \times 10^6$ near-skew-merged perturbations up to $n = 20$).

---

## 1. Main Result: Counterexample to Conjecture 3.14 (`conj:maxlayered`)

Conjecture 3.14 of Lewis & Won (`arXiv:2609.03081v1`, line 759 of `Nonattacking_rook_placements_arxivsubmission.tex`) states:

> *For each $n$, the $n \times n$ permutation grid admitting the most rook placements is given by $\operatorname{Grid}(w)$ where $w \in S_n$ is a layered permutation of shape $(m, 1, 1, \dots, 1, m)$ for some $m$.*

By Proposition 3.15 (`prop:countlayered`) and Proposition 3.16 (`prop:layeredmax`) of Lewis & Won, the maximum number of rook placements over all layered permutations of shape $(m_1, 1, 1, \dots, 1, m_2)$ in $S_n$ is achieved when $m_1 = m_2 = m$ and equals
$$L(n) = \max_{1 \le m \le \lfloor n/2 \rfloor} \sum_{k=1}^m \left[ S(m, k) \cdot k^{n - 2m} \cdot k! \right]^2.$$

### Explicit Witness at $n = 17$ ([witness.json](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_rook/witness.json))
Let $w \in S_{17}$ be the **2-shell nested layered permutation** of composition shape $(5, 3, 1, 3, 5)$:
$$w = (5, 4, 3, 2, 1, \; 8, 7, 6, \; 9, \; 12, 11, 10, \; 17, 16, 15, 14, 13).$$
- **Witness count:** $|\operatorname{RP}(\operatorname{Grid}(w))| = \mathbf{104,476,798,194,769}$.
- **Best $(m, 1, \dots, 1, m)$ count at $n = 17$:** $L(17) = \mathbf{103,460,138,813,701}$ (achieved at $m = 5$, shape $(5, 1^7, 5)$).
- **Strict excess:** $|\operatorname{RP}(\operatorname{Grid}(w))| - L(17) = \mathbf{+1,016,659,381,068}$ ($+0.9827\%$).

Complete comparison against every $(m, 1^{17-2m}, m)$ shape at $n = 17$ (and all $136$ asymmetric $(m_1, 1^{17-m_1-m_2}, m_2)$ shapes, whose maximum is also $103,460,138,813,701$):

| Shape in $S_{17}$ | Exact $|\operatorname{RP}(\operatorname{Grid}(\cdot))|$ | Comparison vs $L(17)$ |
|:---|---:|---:|
| $(1, 1^{15}, 1)$ (identity) | $1$ | $0.0000\times$ |
| $(2, 1^{13}, 2)$ | $268,435,457$ | $0.0000\times$ |
| $(3, 1^{11}, 3)$ | $1,129,869,140,869$ | $0.0109\times$ |
| $(4, 1^{9}, 4)$ | $40,084,566,933,905$ | $0.3874\times$ |
| **$(5, 1^{7}, 5)$ [Best $(m,1^*,m)$]** | **$103,460,138,813,701$** | **$1.0000\times$** |
| $(6, 1^{5}, 6)$ | $65,555,327,816,657$ | $0.6336\times$ |
| $(7, 1^{3}, 7)$ | $18,356,098,793,509$ | $0.1774\times$ |
| $(8, 1^{1}, 8)$ | $2,824,217,777,825$ | $0.0273\times$ |
| **$(5, 3, 1, 3, 5)$ [Witness $w$]** | **$104,476,798,194,769$** | **$1.0098\times$ (BEATS $L(17)$)** |

### Quadruple Independent Exact Verification Status
1. **Pure-Python Across-Word Memoized Backtracking ([verify_counterexample.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_rook/verify_counterexample.py)):** Extracts the $32$ across words and $32$ down words directly from white-square runs of $\operatorname{Grid}(w)$ and computes $\operatorname{perm}(B_{\operatorname{Grid}(w)}) = 104,476,798,194,769$ using exact integer arithmetic (zero `math` imports, zero floating-point operations).
2. **Pure-Python Down-Word Memoized Backtracking ([verify_counterexample.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_rook/verify_counterexample.py)):** Independently computes $\operatorname{perm}(B_{\operatorname{Grid}(w)}^T) = 104,476,798,194,769$.
3. **C++ Row-Sweep Transfer-Matrix DP ([rook_engine.hpp](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_rook/src/rook_engine.hpp)):** Exact `unsigned __int128` row-by-row ASM/rook DP yields $104,476,798,194,769$.
4. **C++ Exact Gray-Code Ryser Permanent ([verify_ryser17.cpp](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_rook/src/verify_ryser17.cpp)):** Eliminating the $8$ degree-$1$ forced rooks reduces $B_{\operatorname{Grid}(w)}$ from $32 \times 32$ to $24 \times 24$, on which unapproximated $2^{24}$ Gray-code Ryser yields $104,476,798,194,769$ in $< 0.1\text{ s}$.

### Minimality of $n = 17$ and Behavior for $n = 10..20$
Why does $(m, 1, \dots, 1, m)$ fail starting at $n = 17$? Once the central identity region $(1, \dots, 1)$ reaches length $7$ ($n - 2m = 7$ at $n = 17, m = 5$), replacing the outer ends of that identity core by a **second nested anti-diagonal shell** of size $3$ — forming $(5, 3, 1, 3, 5)$ — creates two additional yellow corner triangles of multi-rook flexibility whose Stirling-number amplification outweighs the loss of $6$ diagonal black squares. For $n \ge 17$, the 2-shell advantage grows rapidly:

| $n$ | Best $(m,1^{n-2m},m)$ $L(n)$ ($m$) | Best Non-$(m,1^*,m)$ Found | Ratio vs $L(n)$ | Status |
|---:|---:|---:|---:|:---|
| 10 | $255,569$ ($m=4$) | $226,409$ `layered(4,2,4)` | $0.8859$ | **Exhaustive $S_{10}$ proved** ($r(10)=L(10)$) |
| 11 | $3,316,625$ ($m=4$) | $2,862,077$ `layered(4,1,2,4)` | $0.8629$ | **Exhaustive $S_{11}$ BnB proved** ($r(11)=L(11)$) |
| 12 | $46,301,969$ ($m=4$) | $39,411,149$ `layered(4,1,1,2,4)` | $0.8512$ | **Exhaustive $S_{12}$ BnB proved** ($r(12)=L(12)$) |
| 13 | $680,707,985$ ($m=4$) | $578,707,177$ `layered(4,2,1,2,4)` | $0.8502$ | **Exhaustive $S_{13}$ BnB proved** ($r(13)=L(13)$) |
| 14 | $10,353,226,769$ ($m=4$) | $9,686,510,081$ $J_4 \oplus (4,5,6,1,2,3) \oplus J_4$ | $0.9356$ | **Exhaustive $S_{14}$ BnB proved** ($r(14)=L(14)$) |
| 15 | $202,352,501,701$ ($m=5$) | $187,453,346,761$ `layered(4,3,1,1,1,5)` | $0.9264$ | No CEx in all $2^{14}$ layered, $J_{m_1}\oplus\sigma\oplus J_{m_2}$, 264k SA |
| 16 | $4,493,953,750,501$ ($m=5$) | $4,250,088,142,445$ `layered(5,2,1,1,2,5)` | $0.9457$ | No CEx in all $2^{15}$ layered, $J_{m_1}\oplus\sigma\oplus J_{m_2}$, 290k SA |
| **17** | **$103,460,138,813,701$ ($m=5$)** | **$104,476,798,194,769$ `layered(5,3,1,3,5)`** | **$1.0098$** | **COUNTEREXAMPLE CERTIFIED** |
| **18** | **$2,445,624,351,454,501$ ($m=5$)** | **$2,949,333,362,474,113$ `layered(5,3,1,1,3,5)`** | **$1.2060$** | **Counterexample** |
| **19** | **$61,054,032,594,828,497$ ($m=6$)** | **$88,247,151,321,075,649$ `layered(5,3,1,1,1,3,5)`** | **$1.4454$** | **Counterexample** |
| **20** | **$1,967,312,926,737,499,985$ ($m=6$)** | **$2,955,493,257,611,103,149$ `layered(5,4,1,1,4,5)`** | **$1.5023$** | **Counterexample** |

---

## 2. Conjecture 3.9 (`conj:skewmerged`) Search & Structural Findings

Conjecture 3.9 states that $w \in S_n$ is skew-merged (avoids `2143` and `3412`) iff $|\operatorname{RP}(\operatorname{Grid}(w))| \in \{1, 2\}$. Using an $O(n^2)$ exact bitmask residual-SCC classifier ([search_conj39.cpp](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_rook/src/search_conj39.cpp), [search_conj39.log](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_rook/search_conj39.log)):
1. **Unconditional Exhaustive $S_{10}$ ($3,628,800$) & $S_{11}$ ($39,916,800$):** `0` counterexamples; exact matches `#RP=1: 48,620 / 184,756` and `#RP=2: 31,312 / 126,272`.
2. **Exact Remark-3.4 Tree for $n = 10..14$ ($86,457,172$ extensions tested):** Because deleting value $n$ never increases $|\operatorname{RP}|$ (Proposition 3.3 / Remark 3.4), every $w \in S_n$ with $|\operatorname{RP}| \le 2$ extends some $w' \in S_{n-1}$ with $|\operatorname{RP}| \le 2$. Exhaustive expansion up to $n = 14$ proved `#(|RP| <= 2) == |SkewMerged(n)|` for all $n \le 14$ ($79,932$; $311,028$; $1,209,916$; $4,707,964$; $18,330,728$) — **zero counterexamples for $n \le 14$**.
3. **Near-Skew-Merged Perturbations ($n = 10..20$):** Tested $5,500,132$ non-skew-merged candidates ($>500,000$ per $n$). **Zero counterexamples**, and the minimum rook count over non-skew-merged permutations is **`5`** for every $n = 4..20$ (never `2`, `3`, or `4`).
4. **Why Conjecture 3.9 holds structurally:** Applying Remark 3.4 across all four grid boundaries (`del row 1`, `del row n`, `del val 1`, `del val n`) forces any minimal non-skew-merged obstruction in $S_n$ (up to $D_4$ symmetry) into the 2-parameter family $w_{0,b,d}$ ($b + d = n - 4$, `2143` at rows $(1, b+2, b+d+3, n)$ and values $(2, 1, n, d+3)$, decreasing NE block of size $b$, increasing center of size $d$), which always has $|\operatorname{RP}(\operatorname{Grid}(w_{0,b,d}))| \ge 5$ (achieved at $d = 0$, e.g. $(2,1,4,3) \mapsto 5$ and $(2,4,1,5,3) \mapsto 5$).

---

## 3. Reproduction Commands

All commands run cleanly from `/Users/ricardo/dev/open-science/math_wave_1030/csweep_rook` within $\le 4$ threads at `nice -n 10`:

```bash
# 1. Zero-dependency pure-Python exact verification of witness.json + sanity controls (~3 s)
nice -n 10 python3 verify_counterexample.py witness.json

# 2. Independent exact 24x24 Gray-code Ryser verification of the n=17 witness (~0.1 s)
clang++ -O3 -std=c++20 src/verify_ryser17.cpp -I. -o bin/verify_ryser17
nice -n 10 ./bin/verify_ryser17

# 3. Baseline n=1..9 exhaustive reproduction & solver cross-validation (~43 s)
clang++ -O3 -std=c++20 -pthread src/reproduce_and_validate.cpp -o bin/reproduce_and_validate
nice -n 10 ./bin/reproduce_and_validate

# 4. Conjecture 3.9 search (exhaustive n=10..11, Remark 3.4 exact n=10..14, near-SM n=10..20; ~222 s)
clang++ -O3 -std=c++20 -pthread src/search_conj39.cpp -o bin/search_conj39
nice -n 10 ./bin/search_conj39

# 5. Conjecture 3.14 search & exact n=10..14 branch-and-bound minimization (~189 s + ~391 s)
clang++ -O3 -std=c++20 -pthread src/search_conj314.cpp -o bin/search_conj314
clang++ -O3 -std=c++20 -pthread src/minimize_conj314.cpp -o bin/minimize_conj314
nice -n 10 ./bin/search_conj314
nice -n 10 ./bin/minimize_conj314
```

---

## 4. Self-Review Verdict (`CONTROLS`, `CONTRADICTING`, `LABELS`)

- `CONTROLS:` **No** — no assumption overrode what the controls show. Checked in [reproduce_and_validate.cpp](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_rook/src/reproduce_and_validate.cpp#L48-L162), [search_conj314.cpp](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_rook/src/search_conj314.cpp#L265-L290), and [verify_counterexample.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_rook/verify_counterexample.py#L254-L309) (`nice -n 10 python3 verify_counterexample.py`):
  - Exact agreement between `RowSweepWorkspace` and naive Gray-code Ryser across all $46,233$ permutations of $n = 1..8$ plus $1,125$ random permutations of $n = 9..12$, and exact agreement on Proposition 3.15 across $1,330$ $(n, m_1, m_2)$ triples.
  - Pruned `PrefixBnBSolver` validated against unpruned exhaustive enumeration on $n = 8$ ($20,160$ half-space leaves vs $38$ pruned leaves, exact max $3,493$) and $n = 9$ ($181,440$ vs $108$, exact max $28,549$), and `FastLookaheadBnB` matched `PrefixBnBSolver` identically on $n = 10, 11, 12$.
  - Negative controls verified in `verify_counterexample.py`: Equation (2.1) non-permutation $3 \times 3$ grids evaluate to `0`; Zenodo witness `(2,7,4,8,1,6,3,5)` evaluates to `155`; and at $n = 16$, 2-shell `(5,2,1,1,2,5)` evaluates to `4,250,088,142,445 < L(16) = 4,493,953,750,501`.
- `CONTRADICTING:` **No** — no contradicting or negative data was dropped or ignored. Checked in [search_conj39.log](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_rook/search_conj39.log#L1-L21), [search_conj314.log](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_rook/search_conj314.log#L15-L55), and [minimize_conj314.log](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_rook/minimize_conj314.log#L1-L12):
  - All negative results — Conjecture 3.9 holding across all $86,457,172$ Remark-3.4 tree extensions ($n \le 14$) and $5,500,132$ near-skew-merged perturbations ($n = 10..20$), plus Conjecture 3.14 holding exhaustively for $n \le 14$ and across all $68,693$ ($n=15$) and $126,143$ ($n=16$) structured candidates and $>400,000$ SA evaluations — are reported in full in Sections 1 and 2 above.
  - All $8$ symmetric $(m, 1^{17-2m}, m)$ shapes and all $136$ asymmetric $(m_1, 1^{17-m_1-m_2}, m_2)$ shapes at $n = 17$ were checked in `verify_counterexample.py` lines 325–345 to verify none reaches `104,476,798,194,769`.
- `LABELS:` **No** — no paper formula, label, or annotation was trusted without checking it against raw crossword-grid data. Checked in [Nonattacking_rook_placements_arxivsubmission.tex](file:///Users/ricardo/.gemini/antigravity-cli/brain/d7edb5d6-adc8-42ad-802a-ba57bca921dc/.system_generated/steps/6/output.txt#L712-L775) and [verify_counterexample.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_rook/verify_counterexample.py#L31-L78):
  - Conjecture numbering (`3.9 = conj:skewmerged`, `3.10 = conj:rookcounts`, `3.14 = conj:maxlayered`) and shared `[conj]` counter were verified directly in the TeX source (lines 43–57, 712–762).
  - Instead of trusting Proposition 3.15's closed-form formula alone for $L(17)$, `verify_counterexample.py` (lines 327–332) explicitly constructs the $17 \times 17$ grid and extracts across/down words for every $(m, 1^{17-2m}, m)$ ($m = 1..8$), verifying `val_formula == val_grid` from raw white-square intersections before comparing against the witness $w$.

---

## 5. Sources, Limitations, and Next Steps

### Sources
1. Joel Brewster Lewis and Robert Won, *Non-attacking rook placements on crossword grids*, `arXiv:2609.03081v1 [math.CO]`, Sep 2, 2026 (`inputs/2609.03081v1.tex.json.gz`).
2. Alex Chengyu Li, *A Permutation Grid with 155 Rook Placements*, Zenodo `10.5281/zenodo.22679647` (2026) — prior counterexample to Conjecture 3.10 (`conj:rookcounts`) at $n = 8$, reproduced here as a baseline control and excluded from novelty claims.
3. Zvezdelina E. Stankova, *Forbidden subsequences*, *Discrete Math.* 132 (1994), 291–316; M. D. Atkinson, *Permutations which are the union of an increasing and a decreasing subsequence*, *J. Combin. Theory Ser. A* 83 (1998), 1–12.

### Limitations & Next Steps
1. **Unconditional minimality at $n = 15, 16$:** We proved $r(n) = L(n)$ unconditionally over all $n!$ permutations for $n \le 14$, and verified no counterexample exists at $n = 15, 16$ across all $2^{n-1}$ layered compositions, all $J_{m_1} \oplus \sigma \oplus J_{m_2}$ ($k \le 8$), and $>250,000$ SA+2-opt evaluations per $n$. Extending `FastLookaheadBnB` (~40 CPU-minutes estimated for $n = 15$) would settle unconditionally whether $r(15) = L(15)$ and $r(16) = L(16)$.
2. **Replacement conjecture for `conj:maxlayered`:** Every maximizer we found for $n = 1..20$ is a **palindromic multi-shell layered permutation** of shape $(m_1, m_2, \dots, m_s, 1, \dots, 1, m_s, \dots, m_2, m_1)$ with $m_1 \ge m_2 \ge \dots \ge m_s \ge 2$ ($s = 1$ for $n = 4..16$; $s = 2$ starting at $n = 17$, and likely $s = 3$ once the inner identity block grows large enough around $n \approx 35\text{--}40$). Testing whether $r(n)$ is always achieved by a palindromic layered permutation is a natural repair of Conjecture 3.14.
3. **Formalizing the proof of Conjecture 3.9:** Our 4-sided Remark-3.4 reduction reduces Conjecture 3.9 (and the stronger sharp bound $|\operatorname{RP}(\operatorname{Grid}(w))| \ge 5$ for all non-skew-merged $w$) to the explicit family $w_{0,b,d}$, offering a short non-casework proof path addressing Lewis & Won's remark following Conjecture 3.9.
