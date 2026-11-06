# Final recheck of v5 Section 4

The required R6 repair and all three optional R1/R3/R5 clarifications are made and correct. The full diff changes nothing else. The exact supplied PDF renders all four changes correctly.

**Exact inputs.** SHA-256 verification against `delta3/HASHES.txt` passed:

- `paper_v5.tex`: `48a3efaba0ac1d07b05f138e85625c02b50cbe5e8ee7f8750180215297b55e80`
- `paper_v5.pdf`: `533df9e669a8718b27e4312c098191daf3797d129764b21ac26280abde51f7e8`

`delta3/paper_v4.tex` is byte-for-byte identical to `delta2/paper_v4.tex`, the source assessed in the previous report. Source line numbers below refer to `delta3/paper_v5.tex`; page numbers are the printed PDF pages.

**R6 — REQUIRED CHANGE MADE; CORRECT (lines 426–428; p. 6).** The new text is:

> We reduce $A_i$ itself. Using only the real-degree bound $\deg(A_i^2)\le2k$ would give membership in $\operatorname{RM}(\min\{2k,n\},n)$; reducing $A_i$ directly gives the required order-$k$ bound.

This implements the previous report's replacement. The multilinear degree on an $n$-variable cube is at most $n$, so the degree information alone gives at most $\min\{2k,n\}$. The integer bit coefficients of the indicator can be reduced modulo two without increasing this degree. Thus the displayed Reed–Muller order is always within the usual range, including when $2k>n$. “Using only the real-degree bound” now correctly qualifies the inference: it does not claim that reduction of $A_i^2$ cannot yield a lower order. Direct reduction of $A_i$, whose bit degree is at most $k$, proves the needed order-$k$ membership as before. Both defects identified in R6 are resolved.

**R1 — OPTIONAL CHANGE MADE; CORRECT (lines 332–334; p. 5).** The new sentence is:

> Section 5 checks the values in (8) below $2$ and the necessary grid representatives (9) at and above $2$.

This explicitly includes both regimes. It agrees with Section 5: below two, test members of (8) within the relevant interval; at and above two, use the first grid value in each eligible floor cell from (9). The budget is nonincreasing within a cell, so those representatives suffice. The sentence no longer suggests that Section 5 checks only the below-two list.

**R3 — OPTIONAL CHANGE MADE; CORRECT (lines 446–449; p. 7).** The new sentence is:

> A nonzero word of algebraic degree at most $k-1$ lies in $\operatorname{RM}(k-1,n)$, so its weight is at least $2^{n-k+1}$, twice the minimum distance of $\operatorname{RM}(k,n)$.

Nonzeroness is now explicit, and the code whose minimum distance is being doubled is named. The minimum distance of $\operatorname{RM}(k-1,n)$ is $2^{n-(k-1)}=2^{n-k+1}$, exactly twice $2^{n-k}$. Consequently such a nonzero lower-degree word cannot have weight strictly below twice the minimum distance of $\operatorname{RM}(k,n)$. The contextual argument is preserved and its ambiguity removed.

**R5 — OPTIONAL CHANGE MADE; CORRECT (lines 471–475; footnote 1, p. 7).** The revised opening is:

> The attribution to third and higher below-two weights is open.

The rest of the footnote remains:

> An AI referee's ablation finds that, given the grid (6), excluding normalized weights in $(1,3/2)$ alone already gives the same rational, while the ablation numbers in Section 5 disagree. The bound does not depend on that attribution. See Correction 2, printed at the end of Section 5.

The new opening matches the unchanged correction at the end of Section 5 exactly. The footnote retains the grid hypothesis, the attribution of the ablation to the referee, the disagreement, and the independence of the bound from that attribution. It does not claim that the discrepancy is resolved. This is a correct clarification of the printed correction; this recheck does not independently recompute the ablation.

**Full diff.** A fresh normal `diff delta3/paper_v4.tex delta3/paper_v5.tex` is byte-for-byte identical to `delta3/v4_to_v5.diff`. There are exactly four hunks: R1, R6, R3 and R5, quoted above. There are no other source changes, including no additional whitespace-only changes outside those hunks. Steps 1–6, equations (6)–(9), and Section 5 through EOF are unchanged. The proof, bound, low-weight necessary set, high-grid calculation, and existing correction statements have not been strengthened or otherwise altered.

**PDF rendering.** The supplied, hash-verified PDF has 13 pages. Text extraction and visual inspection of rendered pages 5–7 confirm R1 on p. 5, R6 on p. 6, and R3 plus the complete R5 footnote on p. 7. The formula $\operatorname{RM}(\min\{2k,n\},n)$, lower-degree minimum-distance formula, references (8)/(9), and footnote text all render legibly. No clipping, overlapping text, missing symbols or unresolved references were observed in these passages. The theorem paragraph continues normally across the pp. 6–7 break.

No further change is required for these four sentences. Inputs were not edited. New result: no; this is the requested final textual and mathematical recheck, not a new bound or a rerun of the numerical certificate.

VERDICT: ACCEPT
