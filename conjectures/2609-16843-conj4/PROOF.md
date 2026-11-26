# Disproof and Complete Resolution of van Berkel & Bosma Conjecture 4

## 1. Definitions, Conventions, and Target Statement

Following Daan van Berkel and Wieb Bosma, *On $t$-sumfree sequences* (`arXiv:2609.16843v2`, Section 1 and Section 3):

1. **Greedy, strict $3$-sumfree sequence $S_{f,g,h}$:** Given positive integers $1 \le f < g < h$, define $S_{f,g,h} = (s_1, s_2, s_3, \dots)$ by $s_1 = f$, $s_2 = g$, $s_3 = h$, and for every $n > 3$, let $s_n$ be the smallest integer $z > s_{n-1}$ that cannot be written as $s_i + s_j + s_\ell$ with $1 \le i < j < \ell < n$. Since all entries of $S_{f,g,h}$ are positive integers, any representation $z = a + b + c$ with $a < b < c$ in $S_{f,g,h}$ automatically satisfies $c = z - a - b \le z - 3 < z$. Consequently, a set $A \subseteq \mathbb{Z}_{\ge 1}$ equals the set of entries of $S_{f,g,h}$ if and only if:
   - $A \cap [1, h] = \{f, g, h\}$,
   - **(Exclusion / strict $3$-sumfreeness)** no integer $x \in A$ with $x > h$ is a sum $a + b + c$ of three distinct elements $a < b < c$ of $A$, and
   - **(Inclusion / greediness)** every integer $n > h$ with $n \notin A$ can be written as $a + b + c$ for some $a < b < c$ in $A$ (necessarily with $c < n$).
2. **Characteristic sequence $C_{f,g,h}$, difference sequence $D_{f,g,h}$, and minimal parameters $(k, p, m)$:**
   - $C_{f,g,h} = (C_z)_{z \ge 1} \in \{0,1\}^{\mathbb{Z}_{\ge 1}}$ has $C_z = 1$ if $z \in S_{f,g,h}$ and $C_z = 0$ otherwise.
   - $D_{f,g,h} = (d_i)_{i \ge 1}$ is defined by $d_i = s_{i+1} - s_i$.
   - $S_{f,g,h}$ is **ultimately periodic** if $C_{f,g,h}$ is ultimately periodic: equivalently, there exist integers $k \ge 0$, $p \ge 1$, $m \ge 2$, finite preperiod entries $a_1 < \dots < a_k$, and initial periodic-block entries $b_1 < \dots < b_p$ with $a_k < b_1$ and $b_p < b_1 + m$ (taking $a_0 := 0$ if $k = 0$) such that
     $$S_{f,g,h} = \{a_1, \dots, a_k\} \sqcup \bigsqcup_{j \ge 0} \{b_1 + j m, \dots, b_p + j m\}.$$
   - Under van Berkel and Bosma's convention (the arXiv v2 TeX source, lines 104-116), the **modulus** $m$ is the minimal period length of $C_{f,g,h}$, the **minimal period length** $p$ is the minimal period length of $D_{f,g,h}$ (equal to the number of $1$s per minimal period of $C_{f,g,h}$), and the **minimal preperiod length** $k$ is the minimal preperiod length of $D_{f,g,h}$ (equal to the number of $1$s in the minimal preperiod $C_{f,g,h}[1..K]$).
3. **Authors' Finite-Computation Criterion (Lemma 7 (Section 3, `\label{lemma}`), specialized to $t = 3$):**
   If $C_{f,g,h}$ contains $Q$ consecutive, identical, non-zero blocks of length $M \ge 1$ starting at position $K + 1$ such that
   $$(Q - 6) M \ge 2 K,$$
   then $C_{f,g,h}$ repeats that block of length $M$ indefinitely from position $K + 1$ onward; hence its minimal period $m$ divides $M$, and its minimal preperiod length in $C_{f,g,h}$ is at most $K$.
4. **Conjecture 4 (`\label{conj:except}` of `arXiv:2609.16843v2`):**
   > For every $d \ge 3$ the 3-sumfree sequence $S_{1, d-1, 2d-1}$ is ultimately periodic, and, with the exception of $d=3$ or $d=5$, the preperiod length is $d+3$ and the period length is $d$ modulo $8d-1$.

---

## 2. Main Results (Summary of Disproof and Full Resolution)

**Conjecture 4 is false as stated**, for two independent reasons:
1. **$d = 4$ ($S_{1,3,7}$) is an unstated exception whose period length and modulus both disagree with Conjecture 4:** $S_{1,3,7}$ has minimal preperiod length $k = 7 = d + 3$, **minimal period length $p = 3 \ne 4 = d$**, and **modulus $m = 27 \ne 31 = 8d - 1$** (tail $\{29, 35, 36\} + 27\mathbb{Z}_{\ge 0}$, repeating gap block $(6, 1, 20)$). Because $p = 3 \ne 4$, $d = 4$ refutes Conjecture 4 even if the phrase "modulo $8d-1$" were omitted or reinterpreted.
2. **For every $d \ge 6$, the exact modulus is $8d - 3$, NOT $8d - 1$:** For $d = 6$ ($S_{1,5,11}$), the minimal preperiod length is $k = 9 = d + 3$, the minimal period length is $p = 6 = d$, and the **exact modulus is $m = 45 = 8d - 3 \ne 47 = 8d - 1$**. In general, Conjecture 4's formula $8d - 1$ is off by $2$ for every $d \ge 6$.

**Theorem 1 (Complete Resolution of $S_{1, d-1, 2d-1}$ for all $d \ge 3$).**
*For every integer $d \ge 3$, the greedy strict $3$-sumfree sequence $S_{1, d-1, 2d-1}$ is ultimately periodic, with exact minimal preperiod length $k$, minimal period length $p$, modulus $m$, preperiod tuple $(a_1, \dots, a_k)$, and initial period block $(b_1, \dots, b_p)$ given by:*

| $d$ | Sequence | $k$ | $p$ | $m$ | Preperiod $(a_1, \dots, a_k)$ | First periodic block $(b_1, \dots, b_p)$ | Repeating $D$-period |
|---:|---|---:|---:|---:|---|---|---|
| $3$ | $S_{1,2,5}$ | $5$ | $1$ | $5$ | $(1, 2, 5, 6, 7)$ | $(11)$ | $(5)$ |
| $4$ | $S_{1,3,7}$ | $7$ | $3$ | $27$ | $(1, 3, 7, 8, 9, 10, 15)$ | $(29, 35, 36)$ | $(6, 1, 20)$ |
| $5$ | $S_{1,4,9}$ | $13$ | $10$ | $104$ | $(1, 4, 9, 10, 11, 12, 13, 19, 37, 45, 46, 72, 79)$ | $(80, 81, 114, 115, 116, 123, 149, 150, 158, 176)$ | $(1, 33, 1, 1, 7, 26, 1, 8, 18, 8)$ |
| $d \ge 6$ | $S_{1,d-1,2d-1}$ | $d+3$ | $d$ | $8d-3$ | $(1, d-1, 2d-1, 2d, \dots, 3d-2, 4d-1)$ | $(10d-5, 10d-4, \dots, 11d-6)$ | $(1^{d-1}, 7d-2)$ |

---

## 3. Exact Generating-Function Criterion and Minimality Criterion

Before proving the individual cases, we record two general lemmas used in the small-case proofs and in exact integer arithmetic by `referee/referee_verify_repaired.py`.

### Lemma A (Minimality Criterion for $(k, p, m)$)
Suppose $S = \{a_1 < \dots < a_k\} \sqcup \bigsqcup_{j \ge 0} \{b_1 + j m, \dots, b_p + j m\}$ with $m \ge 2$, $p \ge 1$, $a_k < b_1$ (ignoring this inequality if $k = 0$), and $b_p < b_1 + m$. Define the cyclic gap tuple
$$G = (g_1, \dots, g_p) := (b_2 - b_1, \, b_3 - b_2, \, \dots, \, b_p - b_{p-1}, \, b_1 + m - b_p).$$
1. If $G$ is **primitive** (i.e., there is no proper divisor $r \mid p$ with $1 \le r < p$ such that $G = (g_1, \dots, g_r)^{p/r}$), then $p$ is the **unique minimal period** of $D = (s_{i+1} - s_i)_{i \ge 1}$ and $m = \sum_{i=1}^p g_i$ is the **unique minimal period** of $C$.
2. If in addition $k \ge 1$ and $b_1 - a_k \ne g_p$ (equivalently, $a_k \ne b_p - m$), then $k$ is the **unique minimal preperiod length** of $D$ (even among non-minimal period multiples $r p$), $K := \max(a_k, b_p - m)$ is the **unique minimal preperiod length** of $C$ (even among non-minimal period multiples $r m$), and the number of $1$s in $C[1..K]$ equals $k$.

**Proof.**
1. By construction, $d_{k + j p + i} = g_i$ for all $j \ge 0$ and $1 \le i \le p$, so $D$ has period $p$ from index $k + 1$ onward. Suppose $D$ also has ultimate period $p' \ge 1$ from some index $k' + 1$ onward. Choose Bézout coefficients $u, v \in \mathbb{Z}$ with $u p + v p' = g := \gcd(p, p')$. For all sufficiently large $i$ (specifically $i > \max(k, k') + |u|p + |v|p'$), shifting by $+p$ or $-p$ (when indices stay $> k$) and $+p'$ or $-p'$ (when indices stay $> k'$) preserves entries of $D$, so $d_{i + g} = d_i$. Hence $G$ is periodic with period $g \mid p$. By primitivity of $G$, $g = p$, so $p \mid p'$, whence $p' \ge p$.

   Now suppose $C$ has ultimate period $m' \ge 1$ for all $z > K'$. For $z_0 > \max(K', b_1)$, membership in $S \cap [z_0, \infty)$ is invariant under $+m'$. Let $c_1 \ge 1$ be the number of elements of $S$ in $[z_0, z_0 + m' - 1]$ (note $c_1 \ge 1$ because $S$ is infinite and invariant under $+m'$ on $[z_0, \infty)$). Then for every $s_i \ge z_0$, $[s_i, s_i + m' - 1]$ contains $c_1$ elements of $S$, so $s_{i + c_1} = s_i + m'$. Subtracting consecutive equations yields $d_{i + c_1} = s_{i + 1 + c_1} - s_{i + c_1} = (s_{i+1} + m') - (s_i + m') = d_i$ for all sufficiently large $i$. Therefore $c_1$ is an ultimate period of $D$, so $p \mid c_1$. Writing $c_1 = q p$ with $q \ge 1$, we obtain $m' = s_{i + q p} - s_i = \sum_{\ell = 0}^{q p - 1} d_{i + \ell} = q \sum_{r=1}^p g_r = q m \ge m$. Since $C$ already has period $m$ for all $z \ge \max(a_k, b_p - m) + 1$, $m$ is the unique minimal period of $C$.

2. Suppose $k \ge 1$ and $b_1 - a_k \ne g_p$ (i.e., $a_k \ne b_p - m$). For any period multiple $r p$ ($r \ge 1$) of $D$, at index $i = k$ we have $d_k = b_1 - a_k$, whereas $d_{k + r p} = g_p \ne d_k$; thus $D$ cannot be periodic with period $r p$ starting at any index $\le k$. Since $D$ is periodic with period $p$ starting at $k + 1$, $k$ is minimal.

   For $C$, let $K = \max(a_k, b_p - m) \ge a_1 \ge 1$. For every $z \ge K + 1$: if $z < b_1$, then $z > a_k$ implies $z \notin S$ ($C_z = 0$), and $z > b_p - m$ together with $z < b_1$ implies $b_p < z + m < b_1 + m$, so $z + m \notin S$ ($C_{z+m} = 0$); if $z \ge b_1$, both $z$ and $z + m$ exceed $a_k$ and hence have identical membership in $S$. Thus $C_{z + m} = C_z$ for all $z \ge K + 1$. Conversely, for any multiple $r m$ ($r \ge 1$) at $z = K$:
   - If $a_k > b_p - m$, then $K = a_k \in S$ ($C_K = 1$), whereas $b_p + (r-1)m < a_k + r m < b_1 + r m$ gives $a_k + r m \notin S$ ($C_{K + r m} = 0 \ne C_K$).
   - If $b_p - m > a_k$, then $a_k < K = b_p - m < b_1$ gives $K \notin S$ ($C_K = 0$), whereas $K + r m = b_p + (r-1)m \in S$ ($C_{K + r m} = 1 \ne C_K$).
   Finally, in both cases $a_k \le K < b_1$, so $S \cap [1, K] = \{a_1, \dots, a_k\}$, which has cardinality $k$. $\blacksquare$

### Lemma B (Exact Rational Generating-Function Criterion)
Let $A = \{a_1 < \dots < a_k\} \sqcup \bigsqcup_{j \ge 0} \{b_1 + j m, \dots, b_p + j m\} \subseteq \mathbb{Z}_{\ge 1}$ with $a_k < b_1$ and $b_p < b_1 + m$, and let $A(x) = \sum_{a \in A} x^a \in \mathbb{Z}[[x]]$. Set $L = 6m$. For $e \in \{1, 2, 3\}$, define the polynomial
$$P_e(x) = (1 - x^L) \sum_{i=1}^k x^{e a_i} + \sum_{i=1}^p \sum_{u=0}^{(6/e) - 1} x^{e b_i + u e m},$$
so that $A(x^e) = \frac{P_e(x)}{1 - x^L}$. Define the polynomial
$$T(x) = P_1(x)^3 - 3 P_1(x) P_2(x) (1 - x^L) + 2 P_3(x) (1 - x^L)^2, \qquad N_T := \deg T(x).$$
Then:
1. For every integer $n \ge 1$, the number $r_3(n)$ of strictly increasing triples $(u, v, w) \in A^3$ ($u < v < w$) with $u + v + w = n$ satisfies
   $$6 r_3(n) = [x^n] \frac{T(x)}{(1 - x^L)^3} = \sum_{\substack{0 \le i \le \min(n, N_T) \\ i \equiv n \pmod L}} ([x^i] T(x)) \binom{\frac{n - i}{L} + 2}{2}.$$
2. Let $n_{\text{start}} = 1 + \max(N_T, b_p, 3 a_k, h)$ (taking $a_0 = 0$; this coincides with $\max(N_T + 1, b_p + 1)$ in all cases below and guarantees every representing triple at $n \ge n_{\text{start}}$ has its largest member in the periodic tail, yielding $\beta \ge 0$ and $\gamma \ge 0$). For each $n_0 \in [n_{\text{start}}, n_{\text{start}} + L - 1]$, the function $f_{n_0}(j) := 6 r_3(n_0 + j L)$ ($j \in \mathbb{Z}_{\ge 0}$) is a polynomial in $j$ of degree at most $2$, uniquely determined by $f_{n_0}(j) = \alpha + \beta j + \gamma \binom{j}{2}$ where $\alpha = f_{n_0}(0)$, $\beta = f_{n_0}(1) - f_{n_0}(0)$, and $\gamma = f_{n_0}(2) - 2 f_{n_0}(1) + f_{n_0}(0)$.
3. Consequently, $A = S_{f,g,h}$ if and only if:
   - $A \cap [1, h] = \{f, g, h\}$;
   - for every $n \in [h + 1, n_{\text{start}} - 1]$, $n \in A \iff 6 r_3(n) = 0$;
   - for every $n_0 \in [n_{\text{start}}, n_{\text{start}} + L - 1]$, if $n_0 \in A$ then $(\alpha, \beta, \gamma) = (0, 0, 0)$, and if $n_0 \notin A$ then $\alpha > 0$, $\beta \ge 0$, and $\gamma \ge 0$.

**Proof.**
In $A(x)^3 = \sum_{(u,v,w) \in A^3} x^{u+v+w}$, a triple with three distinct entries appears in $3! = 6$ permutations, a triple with two equal entries $(u, u, v)$ ($u \ne v$) appears in $3$ permutations, and $(u, u, u)$ appears once. Subtracting $3 A(x) A(x^2) = 3 \sum_{(v, u) \in A^2} x^{v + 2u}$ cancels the $3$ permutations of $(u, u, v)$ ($u \ne v$) and changes the coefficient of $x^{3u}$ to $1 - 3 = -2$, which $+2 A(x^3)$ cancels to $0$. Thus $\sum_{n \ge 1} 6 r_3(n) x^n = A(x)^3 - 3 A(x) A(x^2) + 2 A(x^3) = T(x)/(1 - x^L)^3$. Expanding $(1 - x^L)^{-3} = \sum_{q \ge 0} \binom{q+2}{2} x^{q L}$ gives (1). For $n_0 > N_T$, the index set $\{0 \le i \le \min(n, N_T) : i \equiv n_0 \pmod L\}$ in (1) is independent of $j \ge 0$ when evaluating at $n = n_0 + j L$, and each $\binom{(n_0 - i)/L + j + 2}{2}$ is quadratic in $j$, proving (2). In (3), since $n_{\text{start}} > b_p > a_k$ and $m \mid L$, $n_0 + j L \in A \iff n_0 \in A$ for all $j \ge 0$; $(\alpha, \beta, \gamma) = (0,0,0)$ is equivalent to $f_{n_0}(j) = 0$ for all $j \ge 0$, while $\alpha > 0, \beta \ge 0, \gamma \ge 0$ implies $f_{n_0}(j) \ge \alpha > 0$ for all $j \ge 0$ (and conversely $f_{n_0}(j) > 0$ holds here with $\beta, \gamma \ge 0$). $\blacksquare$

---

## 4. Exact Disproof of Conjecture 4 and Resolution of Small Cases ($d = 3, 4, 5, 6$)

### 4.1 Case $d = 3$: $S_{1,2,5}$ ($k = 5, p = 1, m = 5$)
**Claim.** $S_{1,2,5} = A_3 := \{1, 2, 5, 6, 7\} \sqcup \{11 + 5j : j \ge 0\}$, with minimal preperiod length $k = 5$, minimal period length $p = 1$, and modulus $m = 5$.

**Proof 1 (Elementary Residue-Class Proof).**
Rewrite $A_3 = \{2, 5, 7\} \sqcup \{1 + 5j : j \ge 0\}$. Note $A_3 \cap [1, 5] = \{1, 2, 5\}$.
- *Exclusion:* Every element of $A_3$ has residue in $\{0, 1, 2\} \bmod 5$, with **only one** element ($5$) in $0 \bmod 5$ and **only two** elements ($2, 7$) in $2 \bmod 5$.
  - First check $6, 7 \in A_3$: the elements of $A_3$ below $7$ are $\{1, 2, 5, 6\}$, whose smallest $3$-sum is $1 + 2 + 5 = 8 > 7$, so neither $6$ nor $7$ is a $3$-sum.
  - Every remaining element $x \in A_3$ ($x \ge 11$) satisfies $x \equiv 1 \pmod 5$. Among unordered triples of residues from $\{0, 1, 2\} \bmod 5$, the sums modulo $5$ are:
    $$0+0+0 \equiv 0,\; 0+0+1 \equiv 1,\; 0+0+2 \equiv 2,\; 0+1+1 \equiv 2,\; 0+1+2 \equiv 3,\; 0+2+2 \equiv 4,$$
    $$1+1+1 \equiv 3,\; 1+1+2 \equiv 4,\; 1+2+2 \equiv 0,\; 2+2+2 \equiv 1.$$
    The only two multisets congruent to $1 \pmod 5$ are $\{0, 0, 1\}$ (impossible for distinct elements of $A_3$ since $A_3$ has only one element $\equiv 0 \pmod 5$) and $\{2, 2, 2\}$ (impossible since $A_3$ has only two elements $\equiv 2 \pmod 5$). Hence no $x \in A_3$ is a strict $3$-sum in $A_3$.
- *Inclusion:* For $n \in \{8, 9, 10\}$: $8 = 1 + 2 + 5$, $9 = 1 + 2 + 6$, $10 = 1 + 2 + 7$. For every $j \ge 0$, the four gap integers between $11 + 5j$ and $11 + 5(j+1)$ are strict $3$-sums in $A_3$:
  - $12 + 5j = 1 + 5 + (6 + 5j)$ ($1 < 5 < 6 + 5j$, all in $A_3$);
  - $13 + 5j = 2 + 5 + (6 + 5j)$ ($2 < 5 < 6 + 5j$, all in $A_3$);
  - $14 + 5j = 1 + 7 + (6 + 5j)$ (since $6 + 5j \equiv 1 \not\equiv 2 \equiv 7 \pmod 5$ and $6 + 5j \ge 6 > 1$, $\{1, 7, 6+5j\}$ are three distinct elements of $A_3$);
  - $15 + 5j = 2 + 7 + (6 + 5j)$ (likewise $6 + 5j \equiv 1 \pmod 5$ is distinct from $2$ and $7$).
- *Minimality:* By Lemma A with $(a_1,\dots,a_5) = (1,2,5,6,7)$, $(b_1) = (11)$, $m = 5$: $G = (5)$ has length $p = 1$ (trivially primitive), and $b_1 - a_5 = 11 - 7 = 4 \ne 5 = g_1$, so $k = 5$, $p = 1$, $m = 5$ are strictly minimal (with $K = \max(7, 11-5) = 7$ in $C_{1,2,5}$). $\blacksquare$

**Proof 2 (Authors' Lemma 7 (label `lemma`) + Rational Generating Function).**
Direct greedy computation of $S_{1,2,5}$ up to $52$ gives $C_{1,2,5}[1..7] = (1,1,0,0,1,1,1)$ followed by $Q = 9$ identical non-zero blocks $(0,0,0,1,0)$ of length $M = 5$ across $C_{1,2,5}[8..52]$. Since $(Q - 6)M = 3 \cdot 5 = 15 \ge 14 = 2 K$ ($K = 7$), Lemma 7 (label `lemma`) proves $C_{1,2,5}$ repeats $(0,0,0,1,0)$ forever from position $8$. Independently, in Lemma B ($L = 30$), $\deg T = 104$ ($68$ non-zero terms), and checking $n \in [6, 104]$ plus the $30$ quadratic Newton-difference triples on $[105, 134]$ confirms $S_{1,2,5} = A_3$ (`producer/verify.py`). $\blacksquare$

---

### 4.2 Case $d = 4$: $S_{1,3,7}$ ($k = 7, p = 3, m = 27$) — First Counterexample to Conjecture 4
**Claim.** $S_{1,3,7} = A_4 := \{1, 3, 7, 8, 9, 10, 15\} \sqcup \bigsqcup_{j \ge 0} \{29 + 27j, 35 + 27j, 36 + 27j\}$, with minimal preperiod length $k = 7$, **minimal period length $p = 3 \ne 4$**, and **modulus $m = 27 \ne 31$**. This directly refutes Conjecture 4 for $d = 4$.

**Proof 1 (Elementary Residue-Class Proof).**
Observe that $8 + 27 = 35$ and $9 + 27 = 36$, so we may decompose $A_4$ into five isolated finite elements and three infinite arithmetic progressions modulo $27$:
$$A_4 = F_4 \sqcup P_4, \qquad F_4 = \{1, 3, 7, 10, 15\}, \qquad P_4 = (29 + 27\mathbb{Z}_{\ge 0}) \sqcup (8 + 27\mathbb{Z}_{\ge 0}) \sqcup (9 + 27\mathbb{Z}_{\ge 0}).$$
Clearly $A_4 \cap [1, 7] = \{1, 3, 7\}$.
- *Exclusion:* Let $a < b < c$ be three distinct elements of $A_4$. Every element of $P_4$ has residue in $R_4 := \{2, 8, 9\} \bmod 27$.
  1. **All three in $P_4$:** The unordered sums of three elements from $\{2, 8, 9\} \bmod 27$ are
     $$\{2+2+2, 2+2+8, 2+2+9, 2+8+8, 2+8+9, 2+9+9, 8+8+8, 8+8+9, 8+9+9, 9+9+9\} \bmod 27$$
     $$= \{6, 12, 13, 18, 19, 20, 24, 25, 26, 0\} \bmod 27,$$
     which is disjoint from $R_4 = \{2, 8, 9\}$; moreover $a + b + c \ge 8 + 9 + 29 = 46 > 15 = \max(F_4)$, so $a + b + c \notin A_4$.
  2. **One in $F_4$ and two in $P_4$:** Two elements in $P_4$ have residue sum in $\{4, 10, 11, 16, 17, 18\} \bmod 27$. Adding $u \in F_4 = \{1, 3, 7, 10, 15\}$ gives modulo $27$:
     - $u = 1$: $\{5, 11, 12, 17, 18, 19\}$;
     - $u = 3$: $\{7, 13, 14, 19, 20, 21\}$;
     - $u = 7$: $\{11, 17, 18, 23, 24, 25\}$;
     - $u = 10$: $\{14, 20, 21, 26, 0, 1\}$;
     - $u = 15$: $\{19, 25, 26, 4, 5, 6\}$.
     None intersects $R_4 = \{2, 8, 9\}$, and the smallest such sum is $1 + 8 + 9 = 18 > 15 = \max(F_4)$, so $a + b + c \notin A_4$.
  3. **Two distinct elements in $F_4$ and one in $P_4$:** The $\binom{5}{2} = 10$ pairwise sums of distinct elements of $F_4$ are $\{4, 8, 10, 11, 13, 16, 17, 18, 22, 25\}$. Adding $w \in \{2, 8, 9\}$ modulo $27$ yields:
     - $+2$: $\{6, 10, 12, 13, 15, 18, 19, 20, 24, 0\}$ (note the only entry in $F_4$ is $15 \bmod 27$, which arises from $u+v = 13 = 3+10$ plus $w \equiv 2 \pmod{27}$, so $w \ge 29$ and $u + v + w \ge 42 > 15$);
     - $+8$: $\{12, 16, 18, 19, 21, 24, 25, 26, 3, 6\}$ (minimum sum $1 + 3 + 8 = 12 \notin F_4$; $15$ never occurs since $15 \notin \{12,16,\dots\}$; $3 \bmod 27$ gives $\ge 30 > 15$);
     - $+9$: $\{13, 17, 19, 20, 22, 25, 26, 0, 4, 7\}$ (minimum sum $1 + 3 + 9 = 13 \notin F_4$; $7 \bmod 27$ comes from $25 + 9 = 34 > 15$).
     None intersects $R_4 = \{2, 8, 9\}$ and none lands in $F_4$, so $a + b + c \notin A_4$.
  4. **All three distinct in $F_4$:** The $\binom{5}{3} = 10$ triple sums of $F_4 = \{1, 3, 7, 10, 15\}$ are
     $$\{11, 14, 18, 19, 20, 23, 25, 26, 28, 32\},$$
     which is disjoint from $A_4 \cap [1, 32] = \{1, 3, 7, 8, 9, 10, 15, 29\}$.
  Thus $A_4$ is strictly $3$-sumfree.
- *Inclusion:*
  1. **Finite gaps in $[8, 60] \setminus A_4$:**
     - $[11, 14] = \{1 + 3 + 7, 1 + 3 + 8, 1 + 3 + 9, 1 + 3 + 10\}$;
     - $[16, 28]$: $16 = 1+7+8$, $17 = 1+7+9$, $18 = 1+7+10$, $19 = 1+8+10$, $20 = 3+7+10$, $21 = 3+8+10$, $22 = 3+9+10$, $23 = 1+7+15$, $24 = 7+8+9$, $25 = 7+8+10$, $26 = 7+9+10$, $27 = 8+9+10$, $28 = 3+10+15$;
     - $[30, 34]$: $30 = 7+8+15$, $31 = 7+9+15$, $32 = 7+10+15$, $33 = 1+3+29$, $34 = 9+10+15$;
     - $[37, 55]$: $37 = 1+7+29$, $38 = 1+8+29$, $39 = 1+9+29$, $40 = 1+10+29$, $41 = 3+9+29$, $42 = 3+10+29$, $43 = 1+7+35$, $44 = 1+7+36$, $45 = 1+15+29$, $46 = 8+9+29$, $47 = 3+15+29$, $48 = 3+9+36$, $49 = 3+10+36$, $50 = 7+8+35$, $51 = 7+15+29$, $52 = 1+15+36$, $53 = 3+15+35$, $54 = 3+15+36$, $55 = 9+10+36$;
     - $[57, 60]$ (note $56 = 29 + 27 \in A_4$): $57 = 7+15+35$, $58 = 7+15+36$, $59 = 8+15+36$, $60 = 9+15+36$.
  2. **All gaps $n \ge 61$ ($n \notin A_4$, i.e., $n \bmod 27 \notin \{2, 8, 9\}$):** Each of the $24$ non-member residue classes modulo $27$ is covered for all $j \ge 0$ (starting at threshold $\le 61$) by $a + b + (c_0 + 27j)$ with $a < b \le 15 < 29 \le c_0 \in \{29, 35, 36\}$ (or $c_0 \in \{8, 9\}$ with $b < c_0$):
     - $0 \bmod 27$ ($\ge 54$): $3 + 15 + (36 + 27j)$; $1 \bmod 27$ ($\ge 55$): $9 + 10 + (36 + 27j)$; $3 \bmod 27$ ($\ge 57$): $7 + 15 + (35 + 27j)$; $4 \bmod 27$ ($\ge 58$): $7 + 15 + (36 + 27j)$;
     - $5 \bmod 27$ ($\ge 59$): $8 + 15 + (36 + 27j)$; $6 \bmod 27$ ($\ge 33$): $1 + 3 + (29 + 27j)$; $7 \bmod 27$ ($\ge 61$): $10 + 15 + (36 + 27j)$; $10 \bmod 27$ ($\ge 37$): $1 + 7 + (29 + 27j)$;
     - $11 \bmod 27$ ($\ge 38$): $1 + 8 + (29 + 27j)$; $12 \bmod 27$ ($\ge 39$): $1 + 3 + (35 + 27j)$; $13 \bmod 27$ ($\ge 40$): $1 + 3 + (36 + 27j)$; $14 \bmod 27$ ($\ge 41$): $3 + 9 + (29 + 27j)$;
     - $15 \bmod 27$ ($\ge 42$): $3 + 10 + (29 + 27j)$; $16 \bmod 27$ ($\ge 43$): $1 + 7 + (35 + 27j)$; $17 \bmod 27$ ($\ge 44$): $1 + 7 + (36 + 27j)$; $18 \bmod 27$ ($\ge 45$): $1 + 8 + (36 + 27j)$;
     - $19 \bmod 27$ ($\ge 46$): $3 + 7 + (36 + 27j)$; $20 \bmod 27$ ($\ge 47$): $3 + 8 + (36 + 27j)$; $21 \bmod 27$ ($\ge 48$): $3 + 9 + (36 + 27j)$; $22 \bmod 27$ ($\ge 49$): $3 + 10 + (36 + 27j)$;
     - $23 \bmod 27$ ($\ge 50$): $7 + 8 + (35 + 27j)$; $24 \bmod 27$ ($\ge 51$): $7 + 8 + (36 + 27j)$; $25 \bmod 27$ ($\ge 52$): $1 + 15 + (36 + 27j)$; $26 \bmod 27$ ($\ge 53$): $3 + 15 + (35 + 27j)$.
- *Minimality:* By Lemma A with $(a_1,\dots,a_7) = (1,3,7,8,9,10,15)$, $(b_1,b_2,b_3) = (29,35,36)$, $m = 27$: the cyclic gap tuple $G = (6, 1, 20)$ has prime length $p = 3$ and unequal entries (hence is primitive), and $b_1 - a_7 = 29 - 15 = 14 \ne 20 = g_3$. Thus $k = 7$, $p = 3$, and $m = 27$ are strictly minimal. $\blacksquare$

**Proof 2 (Authors' Lemma 7 (label `lemma`) + Rational Generating Function).**
Direct greedy simulation of $S_{1,3,7}$ up to $231$ shows that from $K + 1 = 16$ onward ($K = 15$), $C_{1,3,7}[16..231]$ consists of $Q = 8$ identical blocks of length $M = 27$ (each equal to $0^{13} 1 0^5 1^2 0^6$). Since $(8 - 6) \cdot 27 = 54 \ge 30 = 2 \cdot 15$, Lemma 7 (label `lemma`) proves periodicity from position $16$ onward. Independently, Lemma B ($L = 162$, $\deg T = 518$, $420$ non-zero terms) verifies $S_{1,3,7} = A_4$ on $[8, 518]$ and across all $162$ quadratic progressions on $[519, 680]$ (`producer/verify.py`). $\blacksquare$

---

### 4.3 Case $d = 5$: $S_{1,4,9}$ ($k = 13, p = 10, m = 104$)
**Claim.** $S_{1,4,9} = A_5 := \{1, 4, 9, 10, 11, 12, 13, 19, 37, 45, 46, 72, 79\} \sqcup \bigsqcup_{j \ge 0} (\{80, 81, 114, 115, 116, 123, 149, 150, 158, 176\} + 104 j)$, with minimal preperiod length $k = 13$, minimal period length $p = 10$, and modulus $m = 104$.

**Proof 1 (Authors' Lemma 7 (label `lemma`)).**
Direct greedy strict $3$-sumfree simulation of $S_{1,4,9}$ up to $911$ yields $S_{1,4,9} \cap [1, 79] = \{1, 4, 9, 10, 11, 12, 13, 19, 37, 45, 46, 72, 79\}$ ($k = 13$ entries, so $K = 79$), followed on $C_{1,4,9}[80..911]$ by $Q = 8$ identical non-zero blocks of length $M = 104$ whose $1$-positions in the first block $[80, 183]$ are $\{80, 81, 114, 115, 116, 123, 149, 150, 158, 176\}$. Since
$$(Q - 6) M = (8 - 6) \cdot 104 = 208 \ge 158 = 2 \cdot 79 = 2 K,$$
Lemma 7 (label `lemma`) guarantees that $C_{1,4,9}$ repeats this block of length $104$ indefinitely from position $80$ onward. Applying Lemma A: the cyclic gap tuple $G = (1, 33, 1, 1, 7, 26, 1, 8, 18, 8)$ has unique entry $33$ (appearing once), so $G$ is primitive, proving $p = 10$ and $m = 104$ are minimal; moreover $b_1 - a_{13} = 80 - 79 = 1 \ne 8 = g_{10}$, proving $k = 13$ is minimal. $\blacksquare$

**Proof 2 (Exact Generating-Function and Residue-Class Decomposition).**
1. *Generating function:* In Lemma B with $m = 104$ and $L = 624$, the numerator polynomial $T(x)$ has degree $N_T = 2059$ ($1706$ non-zero terms). Exact evaluation confirms $6 r_3(n) = 0 \iff n \in A_5$ for all $n \in [10, 2059]$, and on $[2060, 2683]$ all $60$ member progressions satisfy $(\alpha, \beta, \gamma) = (0, 0, 0)$ while all $564$ gap progressions satisfy $\alpha > 0, \beta \ge 0, \gamma \ge 0$ (`producer/verify.py`).
2. *Residue-class decomposition:* Noting that $\{10, 11, 12, 19, 45, 46, 72\} + 104 = \{114, 115, 116, 123, 149, 150, 176\}$, $A_5$ decomposes cleanly as
   $$A_5 = F_5 \sqcup \bigsqcup_{r \in R_5} (c_r + 104\mathbb{Z}_{\ge 0}),$$
   with **only six** isolated finite elements $F_5 = \{1, 4, 9, 13, 37, 79\}$ and ten arithmetic progressions $R_5 = \{10, 11, 12, 19, 45, 46, 54, 72, 80, 81\} \bmod 104$ (starting at $c_r = r$ for $r \ne 54$ and $c_{54} = 158$). Direct finite inspection (verified in exact integer arithmetic by `referee/referee_verify_repaired.py`) confirms: (a) none of the $\binom{10+2}{3} = 220$ unordered triples from $R_5$, none of the $6 \cdot \binom{10+1}{2} = 330$ combinations of one element of $F_5$ and two from $R_5$, and none of the $\binom{6}{2} \cdot 10 = 150$ combinations of two distinct elements of $F_5$ and one from $R_5$ has sum congruent modulo $104$ to any element of $R_5$ (nor equal to any element of $F_5$ when evaluated on actual distinct lifts in $A_5$); (b) the $\binom{6}{3} = 20$ triple sums of $F_5$ are $\{14, 18, 23, 26, 42, 47, 50, 51, 54, 59, 84, 89, 92, 93, 96, 101, 117, 120, 125, 129\}$, disjoint from $A_5$ (note $54 \notin A_5$ since $c_{54} = 158$); and (c) every one of the $94$ non-member residues modulo $104$ is represented for all $n \ge 221$ as $a + b + (c_0 + 104 j)$ with $a < b < c_0$ in $A_5$ for a cover-specific shifted base $c_0 = c_r + 104 h$ ($h \ge 0$; e.g. $221 = 19 + 79 + 123$ with $123 = 19 + 104$), while every gap in $[10, 220] \setminus A_5$ has an explicit strict $3$-sum in $A_5$. $\blacksquare$

---

### 4.4 Case $d = 6$: $S_{1,5,11}$ ($k = 9, p = 6, m = 45$) — Second Counterexample to Conjecture 4
Specializing Theorem 2 below to $d = 6$ (and independently certified by Lemma 7 (label `lemma`) with $K = 23, M = 45, Q = 8$, cutoff $383$, and by Lemma B with $L = 270, \deg T = 859$ in exact integer arithmetic by `referee/referee_verify_repaired.py`), $S_{1,5,11}$ equals
$$A_6 = \{1, 5, 11, 12, 13, 14, 15, 16, 23\} \sqcup \bigsqcup_{j \ge 0} \{55 + 45j, 56 + 45j, 57 + 45j, 58 + 45j, 59 + 45j, 60 + 45j\},$$
with minimal preperiod length $k = 9 = d + 3$, minimal period length $p = 6 = d$, and **exact modulus $m = 45 = 8d - 3 \ne 47 = 8d - 1$**, refuting Conjecture 4's modulus claim.

---

## 5. General Algebraic Proof for Every $d \ge 6$

### Elementary Interval-Sum Lemma
Let $[\alpha, \beta]$ be an integer interval with $\beta - \alpha + 1 = L_{\text{int}}$.
1. If $L_{\text{int}} \ge 2$, the set of sums $u + v$ of **two distinct** integers $\alpha \le u < v \le \beta$ equals the contiguous integer interval $[2\alpha + 1, \, 2\beta - 1]$.
2. If $L_{\text{int}} \ge 3$, the set of sums $u + v + w$ of **three distinct** integers $\alpha \le u < v < w \le \beta$ equals the contiguous integer interval $[3\alpha + 3, \, 3\beta - 3]$.

**Proof.**
1. Clearly $2\alpha + 1 = \alpha + (\alpha + 1) \le u + v \le (\beta - 1) + \beta = 2\beta - 1$. Conversely, for any integer $s \in [2\alpha + 1, 2\beta - 1]$, set $u = \max(\alpha, s - \beta)$ and $v = s - u = \min(s - \alpha, \beta)$. If $s \le \alpha + \beta$, then $u = \alpha$ and $v = s - \alpha \in [\alpha + 1, \beta]$, so $\alpha = u < v \le \beta$; if $s > \alpha + \beta$, then $u = s - \beta \in [\alpha + 1, \beta - 1]$ and $v = \beta$, so $\alpha < u < v = \beta$.
2. Clearly $3\alpha + 3 = \alpha + (\alpha + 1) + (\alpha + 2) \le u + v + w \le (\beta - 2) + (\beta - 1) + \beta = 3\beta - 3$. Conversely, given $s \in [3\alpha + 3, 3\beta - 3]$: if $s \le \alpha + 2\beta - 1$, then $s - \alpha \in [2\alpha + 3, 2\beta - 1]$, which by (1) applied to $[\alpha + 1, \beta]$ (length $L_{\text{int}} - 1 \ge 2$) equals $v + w$ with $\alpha < v < w \le \beta$, giving $s = \alpha + v + w$; if $s > \alpha + 2\beta - 1$, then $s - \beta \in [\alpha + \beta, 2\beta - 3] \subseteq [2\alpha + 1, 2(\beta - 1) - 1]$, which by (1) applied to $[\alpha, \beta - 1]$ equals $u + v$ with $\alpha \le u < v \le \beta - 1 < \beta$, giving $s = u + v + \beta$. $\blacksquare$

---

### Theorem 2 (Explicit Characterization of $S_{1, d-1, 2d-1}$ for all $d \ge 6$)
*For every integer $d \ge 6$, set $m = 8d - 3$, $I_* = [2d - 1, 3d - 2]$, and $T_j = [10d - 5 + j m, \, 11d - 6 + j m]$ for $j \in \mathbb{Z}_{\ge 0}$. Define*
$$A_d := \{1, d - 1\} \sqcup I_* \sqcup \{4d - 1\} \sqcup \bigsqcup_{j \ge 0} T_j.$$
*Then $S_{1, d-1, 2d-1} = A_d$, with minimal preperiod length $k = d + 3$, minimal period length $p = d$, and exact modulus $m = 8d - 3$.*

**Proof.**
First verify disjointness and initial seed agreement for $d \ge 6$:
$$1 < d - 1 < 2d - 1 < 3d - 2 < 4d - 1 < 10d - 5 < 11d - 6 < 18d - 8 = (10d - 5) + m,$$
because $d \ge 6$ gives $1 < 5 < 11 < 16 < 23 < 55 < 60 < 100$, and for every $d \ge 6$: $(d-1)-1 = d-2 \ge 4$, $(2d-1)-(d-1) = d \ge 6$, $(3d-2)-(2d-1) = d-1 \ge 5$, $(4d-1)-(3d-2) = d+1 \ge 7$, $(10d-5)-(4d-1) = 6d-4 \ge 32$, $(11d-6)-(10d-5) = d-1 \ge 5$, and $(18d-8)-(11d-6) = 7d-2 \ge 40$. In particular, $A_d \cap [1, 2d - 1] = \{1, d - 1, 2d - 1\} = S_{1, d-1, 2d-1} \cap [1, 2d - 1]$.

By Section 1, to prove $S_{1, d-1, 2d-1} = A_d$ and establish minimality of $(k, p, m) = (d+3, d, 8d-3)$, it suffices to prove **Part A (Exclusion)**, **Part B (Inclusion)**, and **Part C (Minimality)**.

---

#### Part A: Exclusion ($A_d$ is strictly $3$-sumfree for every $d \ge 6$)

We prove that **no** element $S \in A_d$ (and in particular no $S \in A_d$ with $S > 2d - 1$) can be written as $S = x_1 + x_2 + x_3$ for three pairwise distinct elements $x_1, x_2, x_3 \in A_d$.

**Quotient-residue representation of $A_d$ modulo $m = 8d - 3$.**
Since $10d - 5 = (2d - 2) + m$ and $11d - 6 = (3d - 3) + m$, and since for $d \ge 6$ we have
$$0 < 1 < d - 1 < 2d - 2 < 2d - 1 < 3d - 3 < 3d - 2 < 4d - 1 < 8d - 3 = m,$$
every integer $x \in A_d$ has a unique representation $x = r + q m$ with $q \in \mathbb{Z}_{\ge 0}$ and $r \in [1, 4d - 1] \subset [0, m - 1]$. Specifically, $x = r + q m \in A_d$ if and only if $r \in \{1, d-1\} \sqcup [2d-2, 3d-2] \sqcup \{4d-1\}$ and:
- **(C1)** if $r \in \{1, d - 1, 3d - 2, 4d - 1\}$, then $q = 0$ (so $x = r$ is a unique integer in $A_d$);
- **(C2)** if $r = 2d - 2$, then $q \ge 1$ (since $2d - 2 \notin A_d$, whereas $2d - 2 + q m \in T_{q-1}$ for all $q \ge 1$);
- **(C3)** if $r \in [2d - 1, 3d - 3]$, then $q \ge 0$ is arbitrary ($q = 0$ lies in $I_*$ and $q \ge 1$ lies in $T_{q-1}$).

Now let $\{x_1, x_2, x_3\} \subset A_d$ be **any three pairwise distinct** elements, write $x_i = r_i + q_i m$ ($i = 1, 2, 3$), and set
$$\Sigma := r_1 + r_2 + r_3, \qquad Q := q_1 + q_2 + q_3 \ge 0, \qquad S := x_1 + x_2 + x_3 = \Sigma + Q m.$$
Because $1 \le r_i \le 4d - 1$, we have
$$3 \le \Sigma \le 3(4d - 1) = 12d - 3 < 16d - 6 = 2m \qquad (\text{since } 4d - 3 \ge 21 > 0 \text{ for } d \ge 6).$$
Hence $\Sigma = r_* + \varepsilon m$ with carry $\varepsilon \in \{0, 1\}$ and canonical residue $r_* = \Sigma - \varepsilon m \in [0, m - 1]$, so $S = r_* + q_* m$ with $q_* := Q + \varepsilon \ge 0$. By (C1)-(C3), $S \in A_d$ can hold only if:
- **(Target-0)** $q_* = 0$ (meaning $Q = 0$ and $\varepsilon = 0$) and $\Sigma = r_* \in \{1, d-1\} \cup [2d-1, 3d-2] \cup \{4d-1\}$; OR
- **(Target-1)** $q_* \ge 1$ and $r_* \in [2d - 2, 3d - 3]$, which requires either ($\varepsilon = 0, Q \ge 1$ and $\Sigma \in [2d - 2, 3d - 3]$) or ($\varepsilon = 1$ and $\Sigma \in [2d - 2 + m, 3d - 3 + m] = [10d - 5, 11d - 6]$).

Partition the allowed residues $r_i$ into the four disjoint sets
$$P_1 = \{1\}, \qquad P_2 = \{d - 1\}, \qquad J = [2d - 2, 3d - 2], \qquad P_3 = \{4d - 1\}.$$
By (C1) and distinctness of $x_1, x_2, x_3$, each singleton $P_1, P_2, P_3$ can be used **at most once**, and the value $3d - 2 \in J$ can also be used **at most once** (since $r_i = 3d - 2$ forces $x_i = 3d - 2$). Therefore there are exactly **eight** unordered multiset types for $(r_1, r_2, r_3)$, and we check all eight for $d \ge 6$:

1. **Type $(P_1, P_2, P_3)$:** $\Sigma = 1 + (d - 1) + (4d - 1) = 5d - 1$. Since $4d - 1 < 5d - 1 < 8d - 3 = m$ (as $d > 0$ and $3d > 2$), $\varepsilon = 0$ and $r_* = 5d - 1 \notin \{1, d-1\} \cup [2d-2, 3d-2] \cup \{4d-1\}$. Neither Target-0 nor Target-1 holds.
2. **Type $(P_1, P_2, J)$:** $\Sigma = 1 + (d - 1) + r_3 = d + r_3 \in [3d - 2, 4d - 2] \subset [1, m - 1]$, so $\varepsilon = 0$ and $r_* = d + r_3$.
   - Subcase $r_3 = 2d - 2$: Here $r_* = 3d - 2$, and by (C2) we have $q_3 \ge 1$, so $q_* = Q = q_3 \ge 1$. Target-0 fails because $q_* \ge 1$, and Target-1 fails because $r_* = 3d - 2 \notin [2d - 2, 3d - 3]$.
   - Subcase $r_3 \in [2d - 1, 3d - 2]$: Here $r_* \in [3d - 1, 4d - 2]$, which lies strictly between $3d - 2$ and $4d - 1$. Neither Target-0 nor Target-1 holds.
3. **Type $(P_1, P_3, J)$:** $\Sigma = 1 + (4d - 1) + r_3 = 4d + r_3 \in [6d - 2, 7d - 2]$. For $d \ge 6$, $4d - 1 < 6d - 2 \le 7d - 2 < 8d - 3$ ($2d > 1$ and $d > 1$), so $\varepsilon = 0$ and $r_* \in [6d - 2, 7d - 2]$, missing both Target-0 and Target-1.
4. **Type $(P_2, P_3, J)$:** $\Sigma = (d - 1) + (4d - 1) + r_3 = 5d - 2 + r_3 \in [7d - 4, 8d - 4]$. For $d \ge 6$, $4d - 1 < 7d - 4 \le 8d - 4 = m - 1$ ($3d > 3$), so $\varepsilon = 0$ and $r_* \in [7d - 4, 8d - 4]$, missing both Target-0 and Target-1.
5. **Type $(P_1, J, J)$:** Here $r_1 = 1$, and $r_2, r_3 \in [2d - 2, 3d - 2]$ with at most one equal to $3d - 2$, so $4d - 4 \le r_2 + r_3 \le (3d - 3) + (3d - 2) = 6d - 5$, giving $\Sigma \in [4d - 3, 6d - 4]$. For $d \ge 6$, $3d - 3 < 4d - 3$ and $6d - 4 < 8d - 3$ ($2d > 1$), so $\varepsilon = 0$ and $r_* = \Sigma \in [4d - 3, 6d - 4]$.
   - Target-1 fails because $r_* \ge 4d - 3 > 3d - 3$.
   - Target-0 requires $Q = 0$, i.e., $q_2 = q_3 = 0$; by (C2) and distinctness, $x_2 = r_2$ and $x_3 = r_3$ are **distinct** elements of $[2d - 1, 3d - 2]$, so $r_2 + r_3 \ge (2d - 1) + 2d = 4d - 1$, whence $\Sigma = 1 + r_2 + r_3 \ge 4d > 4d - 1$. Thus Target-0 also fails.
6. **Type $(P_2, J, J)$:** Here $r_1 = d - 1$ and $4d - 4 \le r_2 + r_3 \le 6d - 5$, so $\Sigma \in [5d - 5, 7d - 6]$. For $d \ge 6$, $4d - 1 < 5d - 5$ (since $d > 4$) and $7d - 6 < 8d - 3$ (since $d > -3$), so $\varepsilon = 0$ and $r_* \in [5d - 5, 7d - 6]$, missing both Target-0 and Target-1.
7. **Type $(P_3, J, J)$:** Here $r_1 = 4d - 1$ and $4d - 4 \le r_2 + r_3 \le 6d - 5$ (again because $3d - 2$ occurs at most once), so $\Sigma \in [8d - 5, 10d - 6]$.
   - If $\Sigma \in \{8d - 5, 8d - 4\}$, then $\varepsilon = 0$ and $r_* = \Sigma > 4d - 1$ (since $4d > 4$), missing both Target-0 and Target-1.
   - If $\Sigma \in [8d - 3, 10d - 6]$, then $\varepsilon = 1$, $q_* = Q + 1 \ge 1$, and $r_* = \Sigma - (8d - 3) \in [0, 2d - 3]$. Since $2d - 3 < 2d - 2$, Target-1 fails (and $q_* \ge 1$ rules out Target-0).
8. **Type $(J, J, J)$:** Here $r_1, r_2, r_3 \in [2d - 2, 3d - 2]$ with at most one equal to $3d - 2$, so
   $$6d - 6 = 3(2d - 2) \le \Sigma \le (3d - 3) + (3d - 3) + (3d - 2) = 9d - 8.$$
   - If $\Sigma \le 8d - 4$, then $\varepsilon = 0$ and $r_* = \Sigma \in [6d - 6, 8d - 4]$. Since $6d - 6 > 4d - 1$ (as $2d > 5$), both Target-0 and Target-1 fail.
   - If $\Sigma \ge 8d - 3$, then $\varepsilon = 1$, $q_* = Q + 1 \ge 1$, and $r_* = \Sigma - (8d - 3) \in [0, d - 5]$. Since $d - 5 < 2d - 2$ (as $d > -3$), Target-1 fails (and $q_* \ge 1$ rules out Target-0).

All eight cases yield $S \notin A_d$. Hence $A_d$ is strictly $3$-sumfree for every $d \ge 6$. (Remark: tracking $Q = 0$ in Case 6 shows $A_d$ is in fact strictly $3$-sumfree for all $d \ge 3$; it is **Inclusion** below that fails at $d = 3, 4, 5$.) $\blacksquare$

---

#### Part B: Inclusion (Every Gap $n > 2d - 1$ with $n \notin A_d$ is a Strict $3$-Sum in $A_d$, and Why $d = 3, 4, 5$ Fail)

Let $d \ge 6$, and let $S_0 := \{1, d - 1\} \sqcup I_* \sqcup \{4d - 1\} = A_d \cap [1, 4d - 1]$. Since $I_* = [2d - 1, 3d - 2]$ has length $d \ge 6 \ge 3$, the Elementary Interval-Sum Lemma gives:
- $\mathcal{P}(I_*) := \{u + v : u, v \in I_*, \, u < v\} = [2(2d - 1) + 1, \, 2(3d - 2) - 1] = [4d - 1, \, 6d - 5]$;
- $\mathcal{T}(I_*) := \{u + v + w : u, v, w \in I_*, \, u < v < w\} = [3(2d - 1) + 3, \, 3(3d - 2) - 3] = [6d, \, 9d - 9]$.

The set of all integers $n > 2d - 1$ with $n \notin A_d$ is the disjoint union of:
$$G_{\text{pre}, 1} = [3d - 1, \, 4d - 2], \qquad G_{\text{pre}, 2} = [4d, \, 10d - 6], \qquad \text{and} \qquad G_j = [11d - 5 + j m, \, 18d - 9 + j m] \;\; (j \ge 0).$$
We exhibit explicit strict $3$-sum decompositions $n = a + b + c$ ($a < b < c$ in $A_d$, hence $c \le n - 3 < n$) covering every integer in each of these intervals:

1. **Covering $G_{\text{pre}, 1} = [3d - 1, \, 4d - 2]$:**
   For every $n \in [3d - 1, 4d - 2]$, set $a = 1$, $b = d - 1$, and $c = n - d \in [2d - 1, 3d - 2] = I_* \subset A_d$. Since $d \ge 6$, $1 < d - 1 < 2d - 1 \le c$, so $a < b < c$ are in $A_d$ and $a + b + c = n$.

2. **Covering $G_{\text{pre}, 2} = [4d, \, 10d - 6]$:**
   Define five subsets of strict $3$-sums from $S_0 \subset A_d$:
   - $B_1 := \{1\} + \mathcal{P}(I_*) = [4d, \, 6d - 4]$ (valid since $1 < 2d - 1 = \min I_*$);
   - $B_2 := \{d - 1\} + \mathcal{P}(I_*) = [5d - 2, \, 7d - 6]$ (valid since $d - 1 < 2d - 1 = \min I_*$);
   - $B_3 := \{1\} + I_* + \{4d - 1\} = [6d - 1, \, 7d - 2]$ (valid since $1 < 2d - 1$ and $\max I_* = 3d - 2 < 4d - 1$);
   - $B_4 := \mathcal{T}(I_*) = [6d, \, 9d - 9]$ (valid since $|I_*| = d \ge 6 \ge 3$);
   - $B_5 := \mathcal{P}(I_*) + \{4d - 1\} = [8d - 2, \, 10d - 6]$ (valid since $\max I_* = 3d - 2 < 4d - 1$).

   Check the four boundary-overlap inequalities for $d \ge 6$:
   - $\min(B_1) = 4d$ and $\max(B_5) = 10d - 6$;
   - $\min(B_2) = 5d - 2 \le 6d - 3 = \max(B_1) + 1 \iff d \ge 1$ (holds for $d \ge 6$);
   - $\min(B_3) = 6d - 1 \le 7d - 5 = \max(B_2) + 1 \iff d \ge 4$ (holds for $d \ge 6$);
   - $\min(B_4) = 6d \le 7d - 1 = \max(B_3) + 1 \iff d \ge 1$ (holds for $d \ge 6$);
   - $\min(B_5) = 8d - 2 \le 9d - 8 = \max(B_4) + 1 \iff \mathbf{d \ge 6}$ (holds with equality at $d = 6$, where $\max(B_4) = 45$ and $\min(B_5) = 46$!).
   Therefore $\bigcup_{r=1}^5 B_r = [4d, 10d - 6] = G_{\text{pre}, 2}$ for every $d \ge 6$.

   *(Note that $\{d - 1\} + I_* + \{4d - 1\} = [7d - 3, 8d - 4]$ and $1 + (d-1) + (4d-1) = 5d - 1$ are also strict $3$-sums in $S_0$, but even with $\{d-1\} + I_* + \{4d-1\}$ included, its upper endpoint is $8d - 4 < 8d - 3$, so it still cannot reach $8d - 3 = \min(B_5) - 1$ without $B_4$!)*

3. **Exact diagnostic of WHY $d = 3, 4, 5$ fail in $G_{\text{pre}, 2}$:**
   In all cases $d \ge 3$, $S_{1, d-1, 2d-1} \cap [1, 4d - 1] = S_0 = \{1, d-1\} \cup [2d-1, 3d-2] \cup \{4d-1\}$ holds identically. All strict $3$-sums formed from $S_0$ that exceed $4d - 1$ are exhausted by $B_1, B_2, \{5d-1\}, B_3, B_3' := \{d-1\} + I_* + \{4d-1\} = [7d - 3, 8d - 4], B_4, B_5$:
   - **At $d = 3$ ($S_0 = \{1, 2, 5, 6, 7, 11\}$):** The inequality $\min(B_3) \le \max(B_2) + 1$ ($d \ge 4$) fails: $B_1 \cup B_2 \cup \{5d-1\} = [12, 15]$, while $B_3 \cup B_3' \cup B_4 \cup B_5 = [17, 20] \cup [22, 24]$, leaving both **$16$** and **$21$** outside $\Sigma_3(S_0)$. Thus $16$ is the first deviation ($16 \in S_{1,2,5}$, and $21 \in S_{1,2,5}$ as well) and locking $S_{1,2,5}$ into period $1$ modulo $5$.
   - **At $d = 4$ ($S_0 = \{1, 3, 7, 8, 9, 10, 15\}$):** The inequality $\min(B_5) \le \max(B_4) + 1$ ($d \ge 6$) fails: $\max(B_4) = 9(4) - 9 = 27$ and $\max(B_3') = 8(4) - 4 = 28$, while $\min(B_5) = 8(4) - 2 = 30$. Thus **$8d - 3 = 29 \notin \Sigma_3(S_0)$**, forcing $29 \in S_{1,3,7}$ before $10d - 5 = 35$, which produces the tail $\{29, 35, 36\} + 27\mathbb{Z}_{\ge 0}$ ($p = 3, m = 27$).
   - **At $d = 5$ ($S_0 = \{1, 4, 9, 10, 11, 12, 13, 19\}$):** Again $\min(B_5) \le \max(B_4) + 1$ ($d \ge 6$) fails by $1$: $\max(B_4) = 9(5) - 9 = 36 = \max(B_3')$, while $\min(B_5) = 8(5) - 2 = 38$. Thus **$8d - 3 = 37 \notin \Sigma_3(S_0)$** is the unique uncovered integer in $[20, 44]$, forcing $37 \in S_{1,4,9}$ and triggering a cascade to $(k, p, m) = (13, 10, 104)$.

4. **Covering every periodic gap $G_j = [11d - 5 + j m, \, 18d - 9 + j m]$ ($j \ge 0$) for $d \ge 6$:**
   Notice that for any integer interval $[u_0, u_1]$ of pairwise sums $a + b$ ($a < b$ in $S_0$), adding $c \in T_j = [10d - 5 + j m, \, 11d - 6 + j m]$ automatically satisfies $a < b \le 4d - 1 < 10d - 5 \le c$ and produces the contiguous sumset interval $[u_0 + 10d - 5 + j m, \, u_1 + 11d - 6 + j m]$. Define five such intervals for each $j \ge 0$:
   - $C_{1,j} := \{1 + (d - 1)\} + T_j = \{d\} + T_j = [11d - 5 + j m, \, 12d - 6 + j m]$;
   - $C_{2,j} := (\{1\} + I_*) + T_j = [2d, 3d - 1] + T_j = [12d - 5 + j m, \, 14d - 7 + j m]$;
   - $C_{3,j} := (\{d - 1\} + I_*) + T_j = [3d - 2, 4d - 3] + T_j = [13d - 7 + j m, \, 15d - 9 + j m]$;
   - $C_{4,j} := \mathcal{P}(I_*) + T_j = [4d - 1, 6d - 5] + T_j = [14d - 6 + j m, \, 17d - 11 + j m]$;
   - $C_{5,j} := (I_* + \{4d - 1\}) + T_j = [6d - 2, 7d - 3] + T_j = [16d - 7 + j m, \, 18d - 9 + j m]$.

   Check distinctness in $S_0$ and all boundary-overlap inequalities for $d \ge 6$:
   - In $C_{1,j},\dots,C_{5,j}$: $1 < d - 1 < 2d - 1 \le 3d - 2 < 4d - 1 < 10d - 5 + j m$, so every summand triple $(a, b, c)$ satisfies $a < b < c$ in $A_d$.
   - $\min(C_{1,j}) = 11d - 5 + j m = \min(G_j)$ and $\max(C_{5,j}) = 18d - 9 + j m = \max(G_j)$.
   - $\min(C_{2,j}) - (\max(C_{1,j}) + 1) = (12d - 5) - (12d - 5) = 0 \le 0$ (exact adjacency).
   - $\min(C_{3,j}) - (\max(C_{2,j}) + 1) = (13d - 7) - (14d - 6) = 1 - d \le -5 \le 0$.
   - $\min(C_{4,j}) - (\max(C_{3,j}) + 1) = (14d - 6) - (15d - 8) = 2 - d \le -4 \le 0$.
   - $\min(C_{5,j}) - (\max(C_{4,j}) + 1) = (16d - 7) - (17d - 10) = 3 - d \le -3 \le 0$.
   Therefore $\bigcup_{r=1}^5 C_{r,j} = [11d - 5 + j m, \, 18d - 9 + j m] = G_j$ for every $j \ge 0$ and every $d \ge 6$.

Combining Part A and Part B proves $S_{1, d-1, 2d-1} = A_d$ for every integer $d \ge 6$. $\blacksquare$

---

#### Part C: Minimality of Preperiod $k = d + 3$, Period $p = d$, and Modulus $m = 8d - 3$

Let $d \ge 6$. Listing $A_d$ in increasing order:
- The finite preperiod tuple $(a_1, \dots, a_k) = (1, \, d - 1, \, 2d - 1, \, 2d, \, \dots, \, 3d - 2, \, 4d - 1)$ has length
  $$k = 1 + 1 + ((3d - 2) - (2d - 1) + 1) + 1 = d + 3.$$
- The initial periodic block $T_0 = (b_1, \dots, b_p) = (10d - 5, \, 10d - 4, \, \dots, \, 11d - 6)$ has length
  $$p = (11d - 6) - (10d - 5) + 1 = d,$$
  with $a_{d+3} = 4d - 1 < 10d - 5 = b_1$ and $b_d = 11d - 6 < (10d - 5) + (8d - 3) = 18d - 8 = b_1 + m$.
- The first-difference sequence is
  $$D_{1, d-1, 2d-1} = \bigl(d - 2, \, d, \, 1^{d-1}, \, d + 1, \, 6d - 4, \, \overline{1^{d-1}, \, 7d - 2}\bigr),$$
  whose cyclic periodic gap tuple is $G = (1, 1, \dots, 1, 7d - 2)$ of length $p = d$ and sum $(d - 1) \cdot 1 + (7d - 2) = 8d - 3 = m$.

Apply **Lemma A**:
1. **Primitivity of $G$ (minimality of $p = d$ and $m = 8d - 3$):** Since $d \ge 6$, $7d - 2 \ge 40 > 1$. Thus the entry $7d - 2$ occurs **exactly once** in $G = (1^{d-1}, 7d - 2)$. If $G = (G')^{d/r}$ for some divisor $r \mid d$, then the multiplicity of $7d - 2$ in $G$ is divisible by $d/r$, forcing $d/r = 1$, i.e., $r = d$. Hence $G$ is primitive, so by Lemma A(1), $p = d$ is the unique minimal period of $D_{1, d-1, 2d-1}$ and $m = 8d - 3$ is the unique minimal period (modulus) of $C_{1, d-1, 2d-1}$.
2. **Minimality of preperiod $k = d + 3$ (and $K = 4d - 1$ in $C$):** Compare $b_1 - a_{d+3}$ with $g_d$:
   $$b_1 - a_{d+3} = (10d - 5) - (4d - 1) = 6d - 4 \ne 7d - 2 = g_d \qquad (\text{since } (7d - 2) - (6d - 4) = d + 2 \ge 8 \ne 0).$$
   Equivalently, $b_d - m = (11d - 6) - (8d - 3) = 3d - 3 < 4d - 1 = a_{d+3}$. By Lemma A(2), $k = d + 3$ is the unique minimal preperiod length of $D_{1, d-1, 2d-1}$ (even if non-minimal period multiples $r d$ are allowed), $K = \max(4d - 1, 3d - 3) = 4d - 1$ is the unique minimal preperiod length of $C_{1, d-1, 2d-1}$ (even if non-minimal modulus multiples $r(8d-3)$ are allowed), and $C_{1, d-1, 2d-1}[1..4d-1]$ contains exactly $k = d + 3$ ones.

This completes the proof of Theorem 2 and Theorem 1. $\blacksquare$
