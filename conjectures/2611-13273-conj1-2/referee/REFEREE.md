Shipped: Clean-room adversarial referee audit (VERDICT: HOLDS) verifying that inputs/PROOF.md settles Conjectures 1 and 2 of Crew et al. (arXiv:2611.13273v1) with zero hypothesis mismatches or proof gaps, certified by line-by-line hand verification and exact-integer polynomial checks across 4,478 digraphs (18,241 (D,v) pairs).
VERDICT: HOLDS
CONTROLS: No  --  positive controls (n=0, n=1, directed cycles C_3 and C_4, bidirected cliques bi-K_1..6, transitive tournaments TT_1..6, plus Crew et al. Corollary 4, Proposition 1, and Theorem 7 baselines across 4,476 n>=2 digraphs) and 8 deliberate mutation runs across 4 mutants (MUTANT_1_SIGN_FLIP_ID3, MUTANT_2_DROP_FALLING_FACTORIAL_ID3, MUTANT_3_WRONG_WEIGHT_COEFF_ID2, MUTANT_4_LOWER_THRESHOLD_N_MINUS_2) were run via `nice -n 10 python3 referee_verify.py` (referee_verify.py lines 975-1042); every positive control matched exact closed forms and all 8 mutant runs failed with AssertionError as required (including H_{bi-K_3}(1) = -1 < 0 and H_{bi-K_4}(2) = -4 < 0 proving the x >= n-1 threshold is sharp).
CONTRADICTING: No  --  zero digraphs, vertex choices, or boundary cases were dropped or filtered: all 4 + 64 + 4,096 = 4,164 labeled loopless digraphs on n=2,3,4 (16,584 (D,v) pairs, matching exact OEIS A003024 DAG counts 3, 25, 543) plus 312 structured and deterministic LCG-sampled digraphs on n=5,6 (1,656 (D,v) pairs) and base orders n=0,1 passed in referee_verify.py (lines 1058-1145), and boundary cases n=1 (0/0 removable singularity in article.tex lines 681, 688 vs PROOF.md line 53), n=2 at x=1 ((x-1)H_V(x) vanishing in PROOF.md lines 40, 47), DAG constant F_D(x) == 1 (article.tex line 692 vs PROOF.md line 7), and self-loops (PROOF.md line 53) were audited with zero counterexamples.
LABELS: No  --  no definition, conjecture statement, or algebraic claim in inputs/PROOF.md (lines 1-55) was trusted from prose labels alone: verbatim LaTeX definitions and Conjectures 1 & 2 were audited directly from inputs/2611.13273v1.tex.json.gz (article.tex lines 151-157, 163, 171-175, 196-202, 232, 279, 680-695, 747-755; recorded in PRIOR_ART.md), acyclicity on all 2^n subsets was cross-checked between Kahn sink-stripping and 3-state DFS (referee_verify.py lines 142-203), and P_D(x) was independently computed and matched via allowed-partition falling factorials, standalone k^n brute-force coloring DFS + exact Newton interpolation (all 4,164 n=2..4 digraphs and 16 named n=5 families, lines 242-316), and minimal-cyclic-set inclusion-exclusion (lines 319-365).

---

# Clean-Room Adversarial Referee Report: `arXiv:2611.13273v1` Conjectures 1 & 2

## 1. Executive Summary & Novelty Check

- **Referee Verdict**: **`VERDICT: HOLDS`**. The candidate proof in `PROOF.md` is **complete, self-contained, and mathematically sound**. It resolves both **Conjecture 1** (`conj:shameful_conj`, Dichromatic Shameful Conjecture) and **Conjecture 2** (`conj:monotonicity_conj`, Dichromatic Monotonicity Conjecture) of Crew, Keller, Kuehr, Lin, Monroy Rodríguez, and Williams (`arXiv:2611.13273v1`, audited from `2611.13273v1.tex.json.gz`) with zero hidden hypothesis mismatches and zero gaps.
- **Why No Statistical Holdout Applies**: This task audits a deductive mathematical proof over all finite digraphs; exact verification is performed via symbolic polynomial identities in $\mathbb{Z}[x]$ in an independently written clean-room verifier (`referee_verify.py`) rather than statistical train/test splits or ML baseline predictors.
- **Novelty Check (Rule 3  --  Did this referee job find a new mathematical result of its own? No)**: As a clean-room referee job, our output is an independent verification verdict rather than a new claim of our own. With respect to the target paper `arXiv:2611.13273v1`, `PROOF.md` **does** settle two explicitly stated open conjectures (Section 8.1, Conjectures 1 and 2), improving Crew et al.'s Theorem 7 baseline $P_D(n)/P_D(n-1) \ge 685/252 \approx 2.71825$ to the sharp $(n/(n-1))^n$ Shameful bound and proving uniform real-variable monotonicity of $P_D(x)/x^n$ on $[n-1, \infty)$ (plus exact characterization of strictness). As a secondary empirical observation from our verifier (`referee_verify.py` line 1141), for all $3,839$ cyclic digraphs tested across $n = 2, \dots, 6$, the shifted derivative polynomial $H_D((n-1)+y) \in \mathbb{Z}[y]$ had exclusively nonnegative Taylor coefficients around $x = n-1$.

---

## 2. Summary of Definition & Hypothesis Alignment (`PRIOR_ART.md`)

Full verbatim excerpts and citation checks are recorded in `PRIOR_ART.md`. Every potential convention mismatch was audited against `article.tex`:

1. **Looplessness and parallel arcs (`article.tex` lines 151, 163, 196-202, 324, 694, 738 vs. `PROOF.md` lines 3, 53)**:
   `article.tex` adopts standard Bang-Jensen & Gutin / Diestel conventions where a digraph $D = (V, A)$ is a finite vertex set $V$ paired with a *set* of ordered pairs of *distinct* vertices (no self-loops, no parallel arcs, while bidirected pairs / digons $\{(u,v), (v,u)\}$ are explicitly permitted on line 153). Looplessness is confirmed throughout `article.tex` by $c_n = 1$ (line 163), the decomposition $\mathcal{C}(D) = \{\text{digons}\} \sqcup \{C \in \mathcal{C}(D) : |C| \ge 3\}$ in Theorem 1 (lines 196-202), existence of $\mathrm{dc}(D)$ (line 324), monicity of $P_D$ of degree $n$ (line 694), and division by $P_D(n)$ in Corollary 7 (line 738). Moreover, `PROOF.md` explicitly notes that if self-loops are admitted, a loop forces $P_D \equiv 0$, so both conjectures still hold with equality wherever defined (and by continuous extension at $x=0$).
2. **Order $n = 1$ removable singularity (`article.tex` lines 681, 688 vs. `PROOF.md` lines 3, 47, 53)**:
   For the loopless singleton $D = (\{v\}, \emptyset)$, $P_D(x) = x$ and $H_D(x) = x \cdot 1 - 1 \cdot x \equiv 0$. At $n = 1$, Conjecture 1's RHS $\frac{P_D(0)}{0^1} = \frac{0}{0}$ and Conjecture 2's $F_D(x) = \frac{x}{x}$ at $x = 0$ have a removable singularity whose unique continuous/rational extension on $`0, \infty)$ is $F_D \equiv 1$ ($1 \ge 1$). [PROOF.md` states the main theorem cleanly for $n \ge 2$ (where $x \ge n-1 \ge 1 > 0$) and explicitly resolves the $n = 1$ removable singularity.
3. **Weak vs. strict monotonicity and DAGs (`article.tex` lines 678, 689, 692 vs. `PROOF.md` lines 7, 51)**:
   For any DAG $D$ of order $n$, no directed cycles exist, so $P_D(x) = x^n$ and $F_D(x) = P_D(x)/x^n \equiv 1$. In `article.tex`, "monotonically increasing" means *nondecreasing* (weakly increasing): line 678 uses the same phrase for Dong's undirected theorem (which includes $\overline{K}_n$ where $\chi_G(q)/q^n \equiv 1$), and line 692 translates Conjecture 2 into $(x-1)^n P_D(x) \ge x^n P_D(x-1)$. `PROOF.md` proves both nondecreasing behavior for all loopless digraphs and strict monotonicity ($H_D(x) > 0$ for $x > n-1$, $P_D(n)/n^n > P_D(n-1)/(n-1)^n$) whenever $D$ has a directed cycle.
4. **Disconnected digraphs and cycle lengths**:
   Neither the conjectures nor `PROOF.md` assume connectivity or restrict cycle lengths; digons ($|C|=2$) and chordless asymmetric cycles ($|C| \ge 3$) are handled uniformly.

---

## 3. Line-by-Line Mathematical Proof Audit (`inputs/PROOF.md`)

### 3.1 Setup and Allowed Vertex Sets (`PROOF.md`)
- For a loopless digraph $D = (V, A)$ with $n = |V| \ge 2$, a subset $W \subseteq V$ is *allowed* iff $D[W]$ is acyclic.
- **Singleton admissibility**: Because $D$ has no self-loops $(u, u) \notin A$, $D[\{u\}]$ has empty arc set and is acyclic; every singleton is allowed.
- **Heredity**: If $W' \subseteq W$ and $D[W']$ contained a directed cycle, that cycle would lie in $D[W]$; hence every subset of an allowed set is allowed.
- **Empty set conventions**: $P_\varnothing(t) = 1$ and $H_\varnothing(t) = t P_\varnothing'(t) - 0 \cdot P_\varnothing(t) = 0$.

### 3.2 Audit of Identity (1) (`PROOF.md`)
> $$P_V(x) = x \sum_{S \ni v \text{ allowed}} P_{V \setminus S}(x-1). \tag{1}$$

- **Combinatorial bijection at integers $x \ge n \ge 2$**:
  Fix $v \in V$ and an integer $x \ge n$ (so $x - 1 \ge 1$ is a positive integer, matching `article.tex` line 157). Let $\mathcal{P}(V, x)$ be the set of proper $x$-colorings $c: V \to [x]$.
  - Given $c \in \mathcal{P}(V, x)$, let $i = c(v) \in [x]$ and $S = c^{-1}(i)$. Clearly $v \in S$, and $D[S]$ is acyclic (allowed) because any directed cycle in $D[S]$ would be monochromatic of color $i$. The restriction $c|_R$ to $R = V \setminus S$ takes values in $[x] \setminus \{i\}$ (of size $x - 1 \ge 1$) and induces no monochromatic directed cycle in $D[R]$.
  - Conversely, given an allowed $S \ni v$, a color $i \in [x]$ ($x$ choices), and a proper coloring $\tilde{c}: R \to [x] \setminus \{i\}$ of $D[R]$ ($P_R(x-1)$ choices), extending $\tilde{c}$ by $c|_S \equiv i$ yields a proper $x$-coloring of $D$ (any monochromatic cycle of color $i$ would lie in $D[S]$, impossible; any monochromatic cycle of color $j \neq i$ would lie in $D[R]$, impossible) with $c^{-1}(c(v)) = S$.
  - **Boundary summand $S = V$ ($R = \varnothing$)**: Occurs iff $D$ is a DAG. Exactly $x$ proper $x$-colorings satisfy $c^{-1}(c(v)) = V$ (the $x$ constant maps). Since $P_\varnothing = 1$, the summand contributes $x P_\varnothing(x-1) = x \cdot 1 = x$. Exact match.
- **Polynomial promotion**: Both sides lie in $\mathbb{Z}[x]$ and agree at all integers $x \ge n$ (infinitely many points), hence are equal in $\mathbb{Z}[x]$. **Holds.**

### 3.3 Audit of Identity (2) (`PROOF.md`)
> $$(x-1)H_V(x) = x^2 \sum_S H_R(x-1) + x \sum_S \big[(n-1) - x(|S|-1)\big] P_R(x-1). \tag{2}$$

Checking every algebraic operation in $\mathbb{Z}[x]$ by hand from (1), with $R = V \setminus S$ and $m = |R| = n - |S|$:
1. Differentiate (1):
   $$P_V'(x) = \sum_S P_R(x-1) + x \sum_S P_R'(x-1).$$
2. Multiply by $x$ and subtract $n P_V(x) = n x \sum_S P_R(x-1)$:
   $$H_V(x) = x P_V'(x) - n P_V(x) = x^2 \sum_S P_R'(x-1) - (n-1)x \sum_S P_R(x-1) = x \sum_S \big[x P_R'(x-1) - (n-1)P_R(x-1)\big].$$
   Matches `PROOF.md` line 17 verbatim.
3. Multiply by $(x-1)$:
   $$(x-1)H_V(x) = x \sum_S \big[x(x-1)P_R'(x-1) - (n-1)(x-1)P_R(x-1)\big].$$
4. Substitute $H_R(t) = t P_R'(t) - m P_R(t)$ at $t = x - 1$, i.e., $(x-1)P_R'(x-1) = H_R(x-1) + (n - |S|)P_R(x-1)$ (note this also holds at $S = V, R = \varnothing, m = 0$ since $0 = 0 + 0 \cdot 1$):
   $$\begin{aligned}
   x(x-1)P_R'(x-1) - (n-1)(x-1)P_R(x-1)
   &= x H_R(x-1) + \big[x(n - |S|) - (n-1)(x-1)\big] P_R(x-1) \\
   &= x H_R(x-1) + \big[xn - x|S| - xn + n + x - 1\big] P_R(x-1) \\
   &= x H_R(x-1) + \big[(n-1) - x(|S|-1)\big] P_R(x-1).
   \end{aligned}$$
5. Multiplying through by the outer factor $x$ yields (2) with every sign and coefficient matching verbatim. **Holds.**

### 3.4 Audit of Identity (3) (`PROOF.md`)
> $$(x-1)H_V(x) = x^2 \sum_{S \ni v\;\mathrm{allowed}} H_{V \setminus S}(x-1) + \sum_\pi (x)_{|\pi|} \sum_{B \in \mathcal{B}(\pi)} \big(x|B| - (n-1)\big). \tag{3}$$

Fix an integer $x \ge n \ge 2$ and let $V' = V \setminus \{v\}$ ($|V'| = n - 1 \ge 1$).
1. **Weighted sum interpretation of the second sum of (2)**:
   By the bijection in Identity (1), for each allowed $S \ni v$, there are $x P_R(x-1)$ proper $x$-colorings $c \in \mathcal{P}(V, x)$ whose color class of $v$ is $S(c) := c^{-1}(c(v)) = S$. Hence:
   $$x \sum_{S \ni v \text{ allowed}} \big[(n-1) - x(|S|-1)\big] P_R(x-1) = \sum_{c \in \mathcal{P}(V, x)} \big[(n-1) - x(|S(c)| - 1)\big].$$
2. **Unique restriction-extension correspondence ($D$ vs. $D - v$)**:
   - Restricting any $c \in \mathcal{P}(V, x)$ to $V'$ yields a proper $x$-coloring $c' = c|_{V'} \in \mathcal{P}(V', x)$ because $D - v = D[V']$ is an induced subdigraph.
   - Grouping $c' \in \mathcal{P}(V', x)$ by the unordered partition $\pi$ of $V'$ into nonempty color classes: every block $B \in \pi$ is nonempty and allowed ($D[B]$ acyclic), with $1 \le k = |\pi| \le n - 1 < x$. Because blocks of $\pi$ are pairwise disjoint nonempty sets of labeled vertices, injections $\phi: \pi \hookrightarrow [x]$ are in exact bijection with proper $x$-colorings $c'$ inducing $\pi$; thus there are $(x)_k = x(x-1)\cdots(x-k+1)$ such colorings $c'$.
3. **Disjointness and exhaustiveness of valid color choices for $v$**:
   Fix $c' \in \mathcal{P}(V', x)$ inducing $\pi$ ($|\pi| = k$), with used color set $U = \mathrm{im}(c') \subseteq [x]$ ($|U| = k$). Extending $c'$ by $c_j(v) = j \in [x]$ leaves all color classes $\ell \neq j$ unchanged (hence allowed), so $c_j \in \mathcal{P}(V, x)$ iff $S(c_j) = (c')^{-1}(j) \cup \{v\}$ is allowed in $D$. Partition $[x] = ([x] \setminus U) \sqcup U$:
   - **Unused colors $j \in [x] \setminus U$ ($x - k$ colors, $x - k \ge 1$)**: $(c')^{-1}(j) = \varnothing$, so $S(c_j) = \{v\}$, which is always allowed (looplessness). Each gives $|S(c_j)| - 1 = 0$.
   - **Used block colors $j \in U$ ($k$ colors, indexed by $B_j = (c')^{-1}(j) \in \pi$)**: $S(c_j) = B_j \cup \{v\}$ is allowed iff $B_j \notin \mathcal{B}(\pi) := \{B \in \pi : B \cup \{v\} \text{ is not allowed}\}$. Letting $b = |\mathcal{B}(\pi)|$, exactly $k - b$ used colors yield valid extensions, and since $v \notin B_j$, each gives $|S(c_j)| - 1 = |B_j|$.
   - The two sets of valid colors have sizes $x - k$ and $k - b$, are disjoint subsets of $[x] \setminus U$ and $U$, and exhaust all valid choices for $c(v)$, totaling $(x - k) + (k - b) = x - b$ extensions.
4. **Unconditional verification of $\sum_{\text{ext}} (|S| - 1) = (n - 1) - h$**:
   With $h = \sum_{B \in \mathcal{B}(\pi)} |B|$:
   $$\sum_{\text{valid ext } j} \big(|S(c_j)| - 1\big) = \sum_{j \in [x] \setminus U} 0 + \sum_{B \in \pi \setminus \mathcal{B}(\pi)} |B| = \sum_{B \in \pi} |B| - \sum_{B \in \mathcal{B}(\pi)} |B| = (n - 1) - h,$$
   using $\sum_{B \in \pi} |B| = |V'| = n - 1$. This holds unconditionally at both extremes:
   - When $b = 0$ ($\mathcal{B}(\pi) = \varnothing$): $h = 0$ and $\sum_{B \in \pi} |B| = n - 1 = (n - 1) - 0$.
   - When $b = k$ ($\mathcal{B}(\pi) = \pi$): $h = n - 1$ and $\pi \setminus \mathcal{B}(\pi) = \varnothing$, giving $0 = (n - 1) - (n - 1)$.
5. **Extension weight sum and polynomial promotion to all real $x$**:
   Summing $(n-1) - x(|S|-1)$ over the $x - b$ valid extensions of $c'$ gives:
   $$(n-1)(x - b) - x\big((n-1) - h\big) = xh - (n-1)b = \sum_{B \in \mathcal{B}(\pi)} \big(x|B| - (n-1)\big),$$
   which depends only on $\pi$ (and vanishes cleanly when $\mathcal{B}(\pi) = \varnothing$). Multiplying by $(x)_{|\pi|}$ and summing over $\pi$ proves (3) for every integer $x \ge n$. Because both sides of (3) are polynomials in $\mathbb{Z}[x]$ agreeing at infinitely many integers $x \ge n$, Identity (3) holds identically for **all real $x \in \mathbb{R}$** (including $x = n - 1$ and $x = 1$). **Holds.**

### 3.5 Audit of Induction, Endpoints, Strictness, and DAG Case (`PROOF.md`)
1. **Base cases ($n = 0, 1$)**:
   $P_\varnothing(x) = 1 \implies H_\varnothing(x) = 0$; $P_{\{v\}}(x) = x \implies H_{\{v\}}(x) = x \cdot 1 - 1 \cdot x = 0$.
2. **Inductive step for $n \ge 2$ and real $x > n - 1$**:
   - *First sum of (3)*: For each allowed $S \ni v$, $|S| \ge 1 \implies m = |R| = n - |S| \in \{0, 1, \dots, n - 1\}$.
     - If $m \in \{0, 1\}$, $H_R(x-1) = 0$ unconditionally by the base cases.
     - If $2 \le m \le n - 1$, then $x > n - 1 \implies x - 1 > n - 2 \ge m - 1$, so $H_R(x-1) \ge 0$ by the induction hypothesis on order $m < n$.
     Since $x > n - 1 \ge 1 > 0$, $x^2 > 0$, so the first sum is $\ge 0$.
   - *Second sum of (3)*: Every partition $\pi$ of $V \setminus \{v\}$ into nonempty blocks satisfies $1 \le |\pi| \le n - 1$. For $x > n - 1$, every factor $x - i$ ($0 \le i \le |\pi| - 1 \le n - 2$) satisfies $x - i > (n - 1) - (n - 2) = 1 > 0$, so $(x)_{|\pi|} > 0$. Every $B \in \mathcal{B}(\pi)$ is nonempty ($|B| \ge 1$), so $x|B| - (n - 1) \ge x - (n - 1) > 0$. Hence the second sum is $\ge 0$.
   - *Dividing by $x - 1$ and endpoint continuity at $x = n - 1$*:
     For $n \ge 2$ and $x > n - 1$, we have $x - 1 > n - 2 \ge 0$, so $x - 1 > 0$ strictly. Dividing $(x - 1)H_V(x) \ge 0$ by $x - 1 > 0$ gives $H_V(x) \ge 0$ on $(n - 1, \infty)$. Since $H_V \in \mathbb{Z}[x]$ is continuous on $\mathbb{R}$, $H_V(n - 1) = \lim_{x \to (n-1)^+} H_V(x) \ge 0$. Note how crucial this is at $n = 2, x = 1$ (e.g. $D = \overset{\leftrightarrow}{K}_2$, where $H_V(x) = x$ and $(x-1)H_V(x) = x(x-1)$ vanishes at $x = 1$ while $H_V(1) = 1 > 0$).
3. **Conjectures 2 and 1**:
   For $n \ge 2$ and $x \in [n - 1, \infty) \subseteq [1, \infty)$, $x > 0$ and $(P_V(x)/x^n)' = H_V(x)/x^{n+1} \ge 0$, proving $P_V(x)/x^n$ is nondecreasing on $[n - 1, \infty)$ (Conjecture 2) and $P_V(n)/n^n \ge P_V(n-1)/(n-1)^n$ (Conjecture 1).
4. **Strictness for cyclic digraphs**:
   Suppose $D$ contains a directed cycle. Because $V$ is finite, $\{U \subseteq V : D[U] \text{ contains a directed cycle}\}$ is nonempty and admits an inclusion-minimal element $C$.
   - Since $D$ is loopless, no singleton induces a cycle, so $|C| \ge 2$.
   - Choose $v \in C$ (valid since Identity (3) holds for any choice of marked vertex $v \in V$).
   - Set $B_0 = C \setminus \{v\}$. Then $|B_0| = |C| - 1 \ge 1$ ($B_0 \neq \varnothing$), and by inclusion-minimality of $C$, $D[B_0]$ is acyclic ($B_0$ is allowed).
   - Define $\pi_0 = \{B_0\} \cup \{\{u\} : u \in V \setminus C\}$. Every block of $\pi_0$ is nonempty and allowed, and $\pi_0$ partitions $V \setminus \{v\}$ into $|\pi_0| = n - |C| + 1 \in \{1, \dots, n - 1\}$ blocks.
   - Because $B_0 \cup \{v\} = C$ induces a cycle, $B_0 \in \mathcal{B}(\pi_0)$. For every $x > n - 1$, $(x)_{|\pi_0|} > 0$ and $x|B_0| - (n - 1) \ge x - (n - 1) > 0$, making $(x - 1)H_V(x) > 0$ and hence (dividing by $x - 1 > 0$) $H_V(x) > 0$ for all $x > n - 1$.
   - *Why $F_V'(x) > 0$ on $(n - 1, n)$ implies $F_V(n) > F_V(n - 1)$*: Even without needing $H_V(n-1) > 0$ at the left endpoint, $F_V(x) = P_V(x)/x^n$ is continuous on the closed interval $[n - 1, n] \subset (0, \infty)$ and differentiable on the open interval $(n - 1, n)$. By the Mean Value Theorem, $F_V(n) - F_V(n - 1) = F_V'(\xi) = H_V(\xi)/\xi^{n+1} > 0$ for some $\xi \in (n - 1, n)$, proving strict monotonicity on $[n - 1, \infty)$ and $P_V(n)/n^n > P_V(n-1)/(n-1)^n$.
5. **DAG equality**:
   If $D$ is acyclic, all $x^n$ maps $V \to [x]$ are proper at every integer $x \ge 1$, so $P_D(x) = x^n$, $H_D(x) \equiv 0$, and $P_D(x)/x^n \equiv 1$ on $(0, \infty)$. **Holds.**

---

## 4. Clean-Room Exact-Integer Verification (`referee_verify.py`)

### Static Purity & Resource Compliance
- **File**: `referee_verify.py`
- **Purity checks verified via Python `ast` and regex**:
  - `import math`: **0 occurrences**
  - `from __future__`: **0 occurrences**
  - `float` constants or calls: **0 occurrences**
  - True division `/` (`ast.Div` or single `/` character anywhere in file): **0 occurrences** (`//` integer division only)
- **Resource footprint**: Executed under `nice -n 10`, single thread (`1 <= 4` threads), wall time **9.89 s**, peak RSS **18.87 MB** (`18,874,368` bytes $\ll 2$ GB limit).

### Coverage & Control Results

| Test Suite | Digraph Count | $(D, v)$ Pairs | Cross-Checks Executed | Result |
| :--- | ---: | ---: | :--- | :--- |
| Base cases ($n = 0, 1$) | 2 | 1 | Brute-force coloring + Newton interpolation | **PASS** |
| Positive closed-form controls ($\vec{C}_3, \vec{C}_4, \overset{\leftrightarrow}{K}_{1..6}, TT_{1..6}$) | 14 |  --  | Exact polynomial & $H_D(x)$ match | **PASS** |
| Deliberate mutation controls (4 mutants $\times$ 2 targets) | 8 runs |  --  | Must fail with `AssertionError` | **PASS (8/8 caught)** |
| Exhaustive $n = 2$ (1 cyclic, 3 DAGs) | 4 | 8 | Id (1)-(3) + brute-force + min-cycle + Sec 3/4/8 | **PASS** |
| Exhaustive $n = 3$ (39 cyclic, 25 DAGs) | 64 | 192 | Id (1)-(3) + brute-force + min-cycle + Sec 3/4/8 | **PASS** |
| Exhaustive $n = 4$ (3,553 cyclic, 543 DAGs) | 4,096 | 16,384 | Id (1)-(3) + brute-force + min-cycle + Sec 3/4/8 | **PASS** |
| Named $n = 5$ families (tournaments, cycles, $\overset{\leftrightarrow}{K}_5$, disconnected, Sec 5 $D_{K_{2,2}}$) | 16 | 80 | Id (1)-(3) + brute-force + min-cycle + Sec 3/4/8 | **PASS** |
| Diverse LCG $n = 5$ sample (sparse/medium/dense/oriented/tournament/disconnected) | 200 | 1,000 | Id (1)-(3) + exact half-line cert + Sec 3/4/8 | **PASS** |
| Named $n = 6$ families (wheel, $\overset{\leftrightarrow}{K}_{3,3}$, $\overset{\leftrightarrow}{K}_6$, disconnected, Sec 5 $D_{P_5}$) | 16 | 96 | Id (1)-(3) + exact half-line cert + Sec 3/4/8 | **PASS** |
| Diverse LCG $n = 6$ sample (sparse/medium/dense/oriented/tournament/disconnected) | 80 | 480 | Id (1)-(3) + exact half-line cert + Sec 3/4/8 | **PASS** |
| **Total** | **4,478** | **18,241** | Zero failures, zero filtered cases | **PASS** |

### Reproduction Commands
```zsh
cd /Users/ricardo/dev/open-science/math_wave_1030/csweep_dichrom_ref
nice -n 10 /usr/bin/time -l python3 referee_verify.py
```

---

## 5. Sources, Limitations, and Next Steps

- **Permitted Sources Used**:
  1. `2611.13273v1.tex.json.gz`  --  Crew, Keller, Kuehr, Lin, Monroy Rodríguez, and Williams, *"Properties of the Dichromatic Polynomial"*, `arXiv:2611.13273v1` (`article.tex` and `tournament.tex`).
  2. `PROOF.md`  --  Candidate proof of Conjectures 1 and 2.
- **Limitations**:
  - Exhaustive computational enumeration of all $2^{n(n-1)}$ labeled digraphs becomes infeasible at $n \ge 5$ ($2^{20} = 1,048,576$ at $n=5$, $2^{30} \approx 1.07 \times 10^9$ at $n=6$), so $n = 5, 6$ computational checks use structured families plus deterministic stratified sampling; however, the deductive proof audited in Section 3 is **exact and unconditional for all finite $n \ge 2$** (with $n=1$ covered by continuous extension).
  - As noted in `PRIOR_ART.md`, at $n = 1$ the literal expression $P_D(0)/0^1$ in `article.tex` Conjecture 1 requires interpreting $x/x \equiv 1$ via its removable singularity at $x = 0$; any public write-up should retain `PROOF.md`'s explicit remark on $n = 1$.
- **Next Steps**:
  1. The proof in `PROOF.md` is ready for downstream packaging or author communication (subject to separate task authorization and outreach review).
  2. *Optional mathematical follow-up*: In `referee_verify.py`, all $3,839$ cyclic digraphs tested up to $n = 6$ satisfied the stronger property that $H_D((n-1)+y)$ has **all nonnegative Taylor coefficients** in $y$ (and $H_D(n-1) > 0$ for all cyclic digraphs tested). Determining whether Taylor-nonnegativity of $H_D((n-1)+y)$ holds for all $n$ (or fails at some larger $n$) is an interesting open strengthening beyond Conjectures 1 and 2.
