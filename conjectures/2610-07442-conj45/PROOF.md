# Unconditional Proof of Conjecture 4.5 of `arXiv:2610.07442v1`

## Main Theorem (Resolution of Conjecture 4.5)

Let $S^{312}_{r,k,d}$ denote the number of alternating sign rectangles (ASRs) of size $r \times k$ with $d$ nonempty rows that extendably avoid the pattern $312$, with the boundary convention $S^{312}_{r,k,0} = 1$ for all integers $r, k \ge 0$, as defined in Section 4 of Höngesberg, Konvalinka, and Linusson (`arXiv:2610.07442v1`). Let $C_n = \frac{1}{n+1}\binom{2n}{n}$ denote the $n$th Catalan number, and for any integers $n, m \in \mathbb{Z}$, define the standard polynomial binomial coefficient by
$$\binom{n}{m} := \begin{cases} \dfrac{n(n-1)\cdots(n-m+1)}{m!} & \text{if } m > 0, \\[6pt] 1 & \text{if } m = 0, \\[4pt] 0 & \text{if } m < 0. \end{cases}$$
Then for all integers $r, k, d$ satisfying $0 \le d \le r, k$,
$$S^{312}_{r,k,d} = F(r, k, d),$$
where
$$F(r, k, d) := \sum_{i=1}^{d} 2^{i-1} \binom{k}{i} \left( \binom{r-2}{d-i} - 2\binom{r-2}{d-i-2} \right) + \binom{r}{d} + \sum_{i \ge 0} C_{2i} \binom{r-1+2i}{d-1-2i} + 2 \sum_{i=1}^{d} (-1)^i \binom{r}{d-i}.$$

---

## Section 1. Conventions, Boundary Values, and Architecture of the Proof

### 1.1 Well-Definedness and Boundary Evaluation of $F(r, k, d)$

First I verify that the sum in $F(r, k, d)$ is finite for every $d \in \mathbb{Z}$ and inspect all boundary indices on the cone $0 \le d \le r, k$:
1. In $\sum_{i \ge 0} C_{2i} \binom{r-1+2i}{d-1-2i}$, the lower index $d - 1 - 2i$ is negative whenever $2i > d - 1$, so $\binom{r-1+2i}{d-1-2i} = 0$ for all $i > \lfloor (d - 1)/2 \rfloor$. Hence the sum is finite.
2. When $d = 0$ and $r, k \ge 0$: the sums $\sum_{i=1}^0$ are empty (hence $0$), $\binom{r}{0} = 1$, and $d - 1 - 2i = -1 - 2i < 0$ for all $i \ge 0$, so every term in the Catalan sum vanishes. Thus
   $$F(r, k, 0) = 1 \qquad \text{for all integers } r, k \ge 0.$$
3. When $r = 1$ and $d = 1$ (with any integer $k \ge 0$):
   - First sum ($i = 1$): $2^0 \binom{k}{1} \bigl(\binom{-1}{0} - 2\binom{-1}{-2}\bigr) = k(1 - 0) = k$.
   - Remaining terms: $\binom{1}{1} + C_0 \binom{0}{0} + 2(-1)^1 \binom{1}{0} = 1 + 1 - 2 = 0$.
   Thus
   $$F(1, k, 1) = k \qquad \text{for all integers } k \ge 0$$
   (in particular $F(1, 0, 1) = 0$ and $F(1, 1, 1) = 1$). Notice also that across the entire cone $0 \le d \le r, k$, no binomial coefficient in $F(r, k, d)$ ever has simultaneously a negative upper index and a positive lower index: when $r \ge 2$ all upper indices ($k$, $r - 2$, $r$, and $r - 1 + 2i$) are non-negative; when $r = 0$ it follows that $d = 0$; and when $r = 1$ it follows that $d \in \{0, 1\}$, producing only $\binom{-1}{0} = 1$ and $\binom{-1}{-2} = 0$.

### 1.2 Proven Recurrences for $S^{312}_{r,k,d}$ from `arXiv:2610.07442v1`

Let $\operatorname{Sch}_m$ ($m \ge 0$) denote the $m$th large Schröder number, with generating function
$$S(x) := \sum_{m \ge 0} \operatorname{Sch}_m x^m = \frac{1 - x - \sqrt{1 - 6x + x^2}}{2x} \in \mathbb{Q}[[x]].$$
In Section 4 of `arXiv:2610.07442v1`, Höngesberg, Konvalinka, and Linusson prove that $S^{312}_{r,k,d}$ satisfies:
- **Base cases** (lines 407, 412, and `[JL07]`):
  $$S^{312}_{r, k, 0} = 1 \quad (r, k \ge 0), \qquad S^{312}_{r, k, d} = 0 \quad (d > \min(r, k)), \qquad S^{312}_{r, r, r} = \operatorname{Sch}_{r-1} \quad (r \ge 1).$$
- **Row-complete recurrence (Proposition 4.2, `\label{lem:r=d}`)**: For $1 \le r \le k$,
  $$S^{312}_{r, k, r} = S^{312}_{r, k-1, r} + S^{312}_{r-1, k-1, r-1} + \sum_{i=2}^{r} \operatorname{Sch}_{i-2} \, S^{312}_{r+1-i, k+1-i, r+1-i}. \tag{R1}$$
- **Balanced recurrence (Proposition 4.3, `\label{lem:k=d}`)**: For $1 \le k < r$,
  $$S^{312}_{r, k, k} = \sum_{j=0}^{k} S^{312}_{j, k, j} \binom{r - j - 1}{k - j}. \tag{R2}$$
- **General recurrence (Theorem 4.4, `\label{lem:general}`)**: For $1 \le d < r, k$,
  $$S^{312}_{r, k, d} = S^{312}_{r, k-1, d} + S^{312}_{r-1, k-1, d-1} + \sum_{i=2}^{d} \operatorname{Sch}_{i-2} \left( S^{312}_{r+1-i, k+1-i, d+1-i} - \binom{r - i}{d + 1 - i} \right). \tag{R3}$$
  *(Remark on $d = 0$ in Theorem 4.4: Theorem 4.4 in the paper states $d < r, k$ while assuming $d \ge 1$, since at $d = 0$ the right-hand side would reference $d - 1 = -1$, whereas line 407 fixes the $d = 0$ stratum directly as $S^{312}_{r, k, 0} = 1$ for all $r, k \ge 0$.)*

---

## Section 2. Uniqueness of the Solution to the Recurrence System

### Lemma 0 (Uniqueness on $0 \le d \le r, k$)
Let $T(r, k, d)$ be any function defined on integer triples $\{(r, k, d) \in \mathbb{Z}^3 : 0 \le d \le r, k\}$ satisfying:
1. $T(r, k, 0) = 1$ for all $r, k \ge 0$;
2. $T(r, r, r) = \operatorname{Sch}_{r-1}$ for all $r \ge 1$;
3. For $1 \le r < k$, $T(r, k, r) = T(r, k-1, r) + T(r-1, k-1, r-1) + \sum_{i=2}^r \operatorname{Sch}_{i-2} T(r+1-i, k+1-i, r+1-i)$;
4. For $1 \le k < r$, $T(r, k, k) = \sum_{j=0}^k T(j, k, j) \binom{r - j - 1}{k - j}$;
5. For $1 \le d < r, k$, $T(r, k, d) = T(r, k-1, d) + T(r-1, k-1, d-1) + \sum_{i=2}^d \operatorname{Sch}_{i-2}\bigl(T(r+1-i, k+1-i, d+1-i) - \binom{r-i}{d+1-i}\bigr)$.

Then $T(r, k, d) = S^{312}_{r,k,d}$ for all integers $0 \le d \le r, k$.

#### Proof of Lemma 0
First note that $S^{312}_{r,k,d}$ itself satisfies conditions (1) through (5). Let $\Delta(r, k, d) := T(r, k, d) - S^{312}_{r,k,d}$. I prove $\Delta(r, k, d) = 0$ for all $0 \le d \le r, k$ in three stages:

1. **Stratum $d = 0$ ($r, k \ge 0$)**: By condition (1), $\Delta(r, k, 0) = 1 - 1 = 0$.
2. **Row-complete stratum $1 \le d = r \le k$**: I induct on $r + k \ge 2$.
   - When $k = r \ge 1$, condition (2) gives $\Delta(r, r, r) = \operatorname{Sch}_{r-1} - \operatorname{Sch}_{r-1} = 0$.
   - When $1 \le r < k$, condition (3) expresses $\Delta(r, k, r)$ as a linear combination of:
     - $\Delta(r, k-1, r)$, which satisfies $1 \le r \le k - 1$ and $r + (k - 1) = r + k - 1 < r + k$;
     - $\Delta(r-1, k-1, r-1)$, which lies in stratum $d = 0$ if $r = 1$, or satisfies $1 \le r - 1 < k - 1$ with $(r - 1) + (k - 1) = r + k - 2 < r + k$ if $r \ge 2$;
     - $\Delta(r+1-i, k+1-i, r+1-i)$ for $2 \le i \le r$, each satisfying $1 \le r + 1 - i < k + 1 - i$ and $(r + 1 - i) + (k + 1 - i) = r + k + 2 - 2i \le r + k - 2 < r + k$.
     By the induction hypothesis (and stage 1), every term vanishes, so $\Delta(r, k, r) = 0$ for all $1 \le r \le k$.
3. **Balanced stratum $1 \le d = k < r$**: For each $0 \le j \le k$, the triple $(j, k, j)$ satisfies either $j = 0$ (stage 1) or $1 \le j \le k$ (stage 2), so $\Delta(j, k, j) = 0$. Condition (4) immediately yields $\Delta(r, k, k) = \sum_{j=0}^k \Delta(j, k, j) \binom{r - j - 1}{k - j} = 0$.
4. **General stratum $1 \le d < r, k$**: I induct on $r + k + d \ge 5$. The inhomogeneous term $-\binom{r-i}{d+1-i}$ cancels in $\Delta = T - S^{312}$, so condition (5) expresses $\Delta(r, k, d)$ as a linear combination of:
   - $\Delta(r, k-1, d)$: since $d < k$, one has $d \le k - 1$ and $d < r$. Either $k - 1 = d < r$ (already zero by stage 3), or $1 \le d < r, k - 1$ with smaller sum $r + (k - 1) + d = r + k + d - 1$;
   - $\Delta(r-1, k-1, d-1)$: since $1 \le d < r, k$, one has $0 \le d - 1 < r - 1, k - 1$. Either $d - 1 = 0$ (already zero by stage 1), or $1 \le d - 1 < r - 1, k - 1$ with smaller sum $r + k + d - 3$;
   - $\Delta(r+1-i, k+1-i, d+1-i)$ for $2 \le i \le d$: each has $1 \le d + 1 - i < r + 1 - i, k + 1 - i$ and smaller sum $r + k + d + 3 - 3i \le r + k + d - 3$.
   By strong induction, $\Delta(r, k, d) = 0$ for all $1 \le d < r, k$. $\blacksquare$

---

## Section 3. Closed-Form Generating Function in $z$ for $F(r, k, d)$

Throughout the rest of the proof, I work in the commutative ring $\mathbb{Q}[[z]]$ of formal power series with rational coefficients. For any power series $P(z) = 1 + \sum_{n \ge 1} p_n z^n \in 1 + z\mathbb{Q}[[z]]$ with constant term $1$:
- $P(z)$ is invertible in $\mathbb{Q}[[z]]$, so $P(z)^m \in 1 + z\mathbb{Q}[[z]]$ is defined for all $m \in \mathbb{Z}$; in particular, $(1 + \alpha z)^m = \sum_{n \ge 0} \binom{m}{n} \alpha^n z^n$ for all $m \in \mathbb{Z}$ and $\alpha \in \mathbb{Q}$.
- $\sqrt{P(z)} := \sum_{n \ge 0} \binom{1/2}{n} (P(z) - 1)^n \in 1 + z\mathbb{Q}[[z]]$ is the unique formal power series $Q(z) \in \mathbb{Q}[[z]]$ satisfying $Q(0) = 1$ and $Q(z)^2 = P(z)$ (uniqueness follows because if $Q_1^2 = Q_2^2$ with $Q_1(0) = Q_2(0) = 1$, then $Q_1 + Q_2$ has constant term $2 \ne 0$, hence is invertible in $\mathbb{Q}[[z]]$, forcing $Q_1 - Q_2 = 0$).

### Lemma 1 (Generating Function Representation of $F(r, k, d)$)
For every integer $k \in \mathbb{Z}$, define the formal power series
$$G_k(z) := \frac{1 - 2z^2}{2}(1 + 2z)^k + \frac{3 + 2z - \sqrt{1 - 4z - 4z^2}}{4} \in \mathbb{Q}[[z]],$$
and for all integers $r, k \in \mathbb{Z}$, define
$$\Phi_{r, k}(z) := (1 + z)^{r-2} G_k(z) \in \mathbb{Q}[[z]].$$
Then for all integers $r \ge 0$, $k \ge 0$, and $0 \le d \le r$ (and in fact for all $d \ge 0$ whenever $r \ge 2$),
$$F(r, k, d) = [z^d] \Phi_{r, k}(z).$$

#### Proof of Lemma 1
First recall the Catalan generating function $C(t) := \sum_{n \ge 0} C_n t^n \in \mathbb{Q}[[t]]$. Since $C_0 = 1$ and $C_{n+1} = \sum_{j=0}^n C_j C_{n-j}$ for $n \ge 0$ (equivalently $\frac{1}{n+2}\binom{2n+2}{n+1}$ satisfies the standard quadratic recurrence), $C(t)$ satisfies $C(t) = 1 + t C(t)^2$, so $(1 - 2t C(t))^2 = 1 - 4t$. Since $1 - 2t C(t)$ has constant term $1$, uniqueness of the principal square root in $1 + t\mathbb{Q}[[t]]$ gives $1 - 2t C(t) = \sqrt{1 - 4t}$, i.e.,
$$C(t) = \frac{1 - \sqrt{1 - 4t}}{2t}.$$
Taking the even part in $\mathbb{Q}[[u]]$ yields
$$\sum_{i \ge 0} C_{2i} u^{2i} = \frac{C(u) + C(-u)}{2} = \frac{1}{2}\left( \frac{1 - \sqrt{1 - 4u}}{2u} + \frac{1 - \sqrt{1 + 4u}}{-2u} \right) = \frac{\sqrt{1 + 4u} - \sqrt{1 - 4u}}{4u}.$$
Since $u(z) := z(1 + z) \in z\mathbb{Q}[[z]]$ has zero constant term, substitution into $\mathbb{Q}[[u]]$ is well-defined. Moreover,
$$1 + 4u(z) = 1 + 4z + 4z^2 = (1 + 2z)^2 \qquad \text{and} \qquad 1 - 4u(z) = 1 - 4z - 4z^2.$$
Because $1 + 2z$ has constant term $1$, $\sqrt{1 + 4u(z)} = 1 + 2z$. Therefore, in $\mathbb{Q}[[z]]$,
$$z \sum_{i \ge 0} C_{2i} z^{2i} (1 + z)^{2i} = z \cdot \frac{(1 + 2z) - \sqrt{1 - 4z - 4z^2}}{4 z(1 + z)} = \frac{1 + 2z - \sqrt{1 - 4z - 4z^2}}{4(1 + z)}. \tag{1.1}$$

Now consider the three regimes of $r \ge 0$:
1. **Case $r = 0$ ($d = 0$)**: By Section 1.1, $F(0, k, 0) = 1$. Meanwhile,
   $$[z^0] \Phi_{0, k}(z) = \Phi_{0, k}(0) = 1^{-2} \left( \frac{1}{2} \cdot 1^k + \frac{3 - 1}{4} \right) = \frac{1}{2} + \frac{1}{2} = 1 = F(0, k, 0).$$
2. **Case $r = 1$ ($d \in \{0, 1\}$)**: By Section 1.1, $F(1, k, 0) = 1$ and $F(1, k, 1) = k$. Expanding $\sqrt{1 - 4z - 4z^2} = 1 + \frac{1}{2}(-4z) + O(z^2) = 1 - 2z + O(z^2)$ and $(1 + 2z)^k = 1 + 2kz + O(z^2)$ in $\mathbb{Q}[[z]]$, I find
   $$G_k(z) = \frac{1}{2}(1 + 2kz) + \frac{3 + 2z - (1 - 2z)}{4} + O(z^2) = \left(\frac{1}{2} + kz\right) + \left(\frac{1}{2} + z\right) + O(z^2) = 1 + (k + 1)z + O(z^2).$$
   Multiplying by $(1 + z)^{1-2} = (1 + z)^{-1} = 1 - z + O(z^2)$ gives
   $$\Phi_{1, k}(z) = (1 - z)(1 + (k + 1)z) + O(z^2) = 1 + kz + O(z^2),$$
   so $[z^0] \Phi_{1, k}(z) = 1 = F(1, k, 0)$ and $[z^1] \Phi_{1, k}(z) = k = F(1, k, 1)$.
3. **Case $r \ge 2$ (all $d \ge 0$)**: Because $r - 2 \ge 0$, $r \ge 2$, and $r - 1 + 2i \ge 1$ are non-negative integers, $\sum_{m \ge 0} \binom{N}{m} z^m = (1 + z)^N$ holds for each of $N \in \{r - 2, r, r - 1 + 2i\}$. Summing each of the four pieces of $F(r, k, d)$ over all $d \ge 0$ in $\mathbb{Q}[[z]]$:
   - **Piece 1**: Since $k \ge 0$, $\sum_{i \ge 1} 2^{i-1} \binom{k}{i} z^i = \frac{(1 + 2z)^k - 1}{2}$. Setting $m = d - i \ge 0$ in the first binomial and $m = d - i - 2 \ge 0$ in the second gives
     $$\sum_{d \ge 0} z^d \sum_{i=1}^d 2^{i-1} \binom{k}{i} \left(\binom{r-2}{d-i} - 2\binom{r-2}{d-i-2}\right) = \frac{(1 + 2z)^k - 1}{2} (1 - 2z^2) (1 + z)^{r-2}.$$
   - **Piece 2**:
     $$\sum_{d \ge 0} \binom{r}{d} z^d = (1 + z)^r = (1 + z)^{r-2} (1 + 2z + z^2).$$
   - **Piece 3**: Setting $m = d - 1 - 2i \ge 0$ (so $d = 1 + 2i + m$) and applying `(1.1)` gives
     $$\sum_{d \ge 0} z^d \sum_{i \ge 0} C_{2i} \binom{r-1+2i}{d-1-2i} = (1 + z)^{r-1} \left( z \sum_{i \ge 0} C_{2i} z^{2i} (1 + z)^{2i} \right) = (1 + z)^{r-2} \frac{1 + 2z - \sqrt{1 - 4z - 4z^2}}{4}.$$
   - **Piece 4**: Using Cauchy multiplication of $\sum_{i \ge 1} (-z)^i = \frac{-z}{1 + z}$ and $\sum_{m \ge 0} \binom{r}{m} z^m = (1 + z)^r$ gives
     $$\sum_{d \ge 0} z^d \cdot 2 \sum_{i=1}^d (-1)^i \binom{r}{d-i} = \frac{-2z}{1 + z} (1 + z)^r = -2z (1 + z)^{r-1} = (1 + z)^{r-2} (-2z - 2z^2).$$

   Adding Pieces 1 through 4 and factoring out $(1 + z)^{r-2}$, the $k$-independent coefficient of $(1 + z)^{r-2}$ simplifies to
   $$-\frac{1 - 2z^2}{2} + (1 + 2z + z^2) + (-2z - 2z^2) + \frac{1 + 2z - \sqrt{1 - 4z - 4z^2}}{4} = \left(-\frac{1}{2} + z^2 + 1 - z^2\right) + \frac{1 + 2z - \sqrt{1 - 4z - 4z^2}}{4} = \frac{3 + 2z - \sqrt{1 - 4z - 4z^2}}{4}.$$
   Therefore $\sum_{d \ge 0} F(r, k, d) z^d = (1 + z)^{r-2} G_k(z) = \Phi_{r, k}(z)$ for all $r \ge 2$ and $k \ge 0$. $\blacksquare$

---

## Section 4. Exact Evaluations of the Large Schröder Generating Function

### Lemma 2 (Schröder Functional Equation and Two Algebraic Substitutions)
Let $S(x) = \sum_{m \ge 0} \operatorname{Sch}_m x^m = \frac{1 - x - \sqrt{1 - 6x + x^2}}{2x} \in \mathbb{Q}[[x]]$. Then:
1. $S(x)$ satisfies the quadratic equation $x S(x)^2 - (1 - x) S(x) + 1 = 0$ in $\mathbb{Q}[[x]]$.
2. For $a(z) := \dfrac{z}{(1 + z)(1 + 2z)} \in z\mathbb{Q}[[z]]$,
   $$S\bigl(a(z)\bigr) = 1 + 2z. \tag{2.1}$$
3. For $b(z) := \dfrac{z}{1 + z} \in z\mathbb{Q}[[z]]$,
   $$S\bigl(b(z)\bigr) = \frac{1 - \sqrt{1 - 4z - 4z^2}}{2z}, \tag{2.2}$$
   and consequently
   $$-\frac{1 + 2z + \sqrt{1 - 4z - 4z^2}}{4} \, S\bigl(b(z)\bigr) = -\frac{3 + 2z - \sqrt{1 - 4z - 4z^2}}{4}. \tag{2.3}$$

#### Proof of Lemma 2
1. From $2x S(x) = 1 - x - \sqrt{1 - 6x + x^2}$, rearranging and squaring gives $(1 - x - 2x S(x))^2 = 1 - 6x + x^2$, i.e., $(1 - x)^2 - 4x(1 - x)S(x) + 4x^2 S(x)^2 = 1 - 6x + x^2$. Subtracting $1 - 2x + x^2$ from both sides yields $-4x(1 - x)S(x) + 4x^2 S(x)^2 = -4x$. Cancelling the nonzero non-zero-divisor $4x$ in the integral domain $\mathbb{Q}[[x]]$ gives $x S(x)^2 - (1 - x)S(x) + 1 = 0$.
2. Substitute $x = a(z) = \frac{z}{1 + 3z + 2z^2}$ into $1 - 6x + x^2$:
   $$1 - 6a(z) + a(z)^2 = \frac{(1 + 3z + 2z^2)^2 - 6z(1 + 3z + 2z^2) + z^2}{(1 + z)^2 (1 + 2z)^2}.$$
   Expanding the numerator gives
   $$(1 + 6z + 13z^2 + 12z^3 + 4z^4) - (6z + 18z^2 + 12z^3) + z^2 = 1 - 4z^2 + 4z^4 = (1 - 2z^2)^2.$$
   Since $\frac{1 - 2z^2}{(1 + z)(1 + 2z)} \in 1 + z\mathbb{Q}[[z]]$ has constant term $1$, uniqueness of the principal square root gives $\sqrt{1 - 6a(z) + a(z)^2} = \frac{1 - 2z^2}{(1 + z)(1 + 2z)}$. Substituting into $S(a(z)) = \frac{1 - a(z) - \sqrt{1 - 6a(z) + a(z)^2}}{2a(z)}$ yields
   $$S\bigl(a(z)\bigr) = \frac{(1 + 3z + 2z^2) - z - (1 - 2z^2)}{2z} = \frac{2z + 4z^2}{2z} = 1 + 2z.$$
3. Substitute $x = b(z) = \frac{z}{1 + z}$ into $1 - 6x + x^2$:
   $$1 - 6b(z) + b(z)^2 = \frac{(1 + z)^2 - 6z(1 + z) + z^2}{(1 + z)^2} = \frac{1 + 2z + z^2 - 6z - 6z^2 + z^2}{(1 + z)^2} = \frac{1 - 4z - 4z^2}{(1 + z)^2}.$$
   Since $(1 + z)^{-1} \sqrt{1 - 4z - 4z^2}$ has constant term $1$, $\sqrt{1 - 6b(z) + b(z)^2} = \frac{\sqrt{1 - 4z - 4z^2}}{1 + z}$. Hence
   $$S\bigl(b(z)\bigr) = \frac{(1 + z) - z - \sqrt{1 - 4z - 4z^2}}{2z} = \frac{1 - \sqrt{1 - 4z - 4z^2}}{2z},$$
   proving `(2.2)`. Multiplying `(2.2)` by $-\frac{1 + 2z + \sqrt{1 - 4z - 4z^2}}{4}$ and expanding the numerator product
   $$(1 + 2z + \sqrt{1 - 4z - 4z^2})(1 - \sqrt{1 - 4z - 4z^2}) = (1 + 2z) - (1 - 4z - 4z^2) - 2z\sqrt{1 - 4z - 4z^2} = 2z\bigl(3 + 2z - \sqrt{1 - 4z - 4z^2}\bigr),$$
   dividing by $-8z$ yields $-\frac{3 + 2z - \sqrt{1 - 4z - 4z^2}}{4}$, proving `(2.3)`. $\blacksquare$

---

## Section 5. Master Formal Power Series Recurrence (`lem:general` and `lem:r=d`)

### Lemma 3 (Master Formal Power Series Recurrence)
For all integers $r, k \in \mathbb{Z}$, the following identity holds in $\mathbb{Q}[[z]]$:
$$\Phi_{r, k}(z) - \Phi_{r, k-1}(z) = z \Phi_{r-1, k-1}(z) + \sum_{m \ge 0} \operatorname{Sch}_m z^{m+1} \Bigl( \Phi_{r-1-m, k-1-m}(z) - (1 + z)^{r-2-m} \Bigr). \tag{3.1}$$
Consequently:
1. For all integers $1 \le d < r, k$, $F(r, k, d)$ satisfies Theorem 4.4 (`lem:general`, `(R3)`).
2. For all integers $1 \le r \le k$, $F(r, k, r)$ satisfies
   $$F(r, k, r) - F(r, k-1, r) = F(r-1, k-1, r-1) + \sum_{i=2}^{r} \operatorname{Sch}_{i-2} \, F(r+1-i, k+1-i, r+1-i); \tag{3.2}$$
   in particular, for $1 \le r < k$, $F(r, k, r)$ satisfies Proposition 4.2 (`lem:r=d`, `(R1)`).

#### Proof of Lemma 3
First observe that for every $m \ge 0$, $\Phi_{r-1-m, k-1-m}(z) - (1 + z)^{r-2-m} \in \mathbb{Q}[[z]]$, so multiplying by $z^{m+1}$ gives a series of $z$-adic valuation at least $m + 1$. Thus the infinite sum on the right-hand side of `(3.1)` converges in the $z$-adic topology on $\mathbb{Q}[[z]]$.

Set $H_2(z) := \frac{3 + 2z - \sqrt{1 - 4z - 4z^2}}{4}$, so $G_n(z) = \frac{1 - 2z^2}{2}(1 + 2z)^n + H_2(z)$ for all $n \in \mathbb{Z}$.
On the left-hand side of `(3.1)`, $H_2(z)$ cancels in $G_k(z) - G_{k-1}(z)$, leaving
$$\Phi_{r, k}(z) - \Phi_{r, k-1}(z) = (1 + z)^{r-2} \frac{1 - 2z^2}{2} \bigl((1 + 2z)^k - (1 + 2z)^{k-1}\bigr) = z(1 - 2z^2)(1 + z)^{r-2}(1 + 2z)^{k-1}. \tag{3.3}$$
On the right-hand side of `(3.1)`, rewrite the factor inside the sum for each $m \ge 0$:
$$\Phi_{r-1-m, k-1-m}(z) - (1 + z)^{r-2-m} = (1 + z)^{r-3-m} \Bigl( G_{k-1-m}(z) - (1 + z) \Bigr).$$
Since
$$H_2(z) - (1 + z) = \frac{3 + 2z - 4 - 4z - \sqrt{1 - 4z - 4z^2}}{4} = -\frac{1 + 2z + \sqrt{1 - 4z - 4z^2}}{4},$$
I decompose $G_{k-1-m}(z) - (1 + z)$ into its $(1 + 2z)$-dependent and $(1 + 2z)$-independent parts:
$$\Phi_{r-1-m, k-1-m}(z) - (1 + z)^{r-2-m} = \frac{1 - 2z^2}{2}(1 + z)^{r-3-m}(1 + 2z)^{k-1-m} - (1 + z)^{r-3-m} \frac{1 + 2z + \sqrt{1 - 4z - 4z^2}}{4}.$$
Multiplying by $\operatorname{Sch}_m z^{m+1}$ and summing over $m \ge 0$ gives two Schröder series evaluations at $a(z) = \frac{z}{(1+z)(1+2z)}$ and $b(z) = \frac{z}{1+z}$:
$$\sum_{m \ge 0} \operatorname{Sch}_m z^{m+1} \Bigl(\Phi_{r-1-m, k-1-m}(z) - (1 + z)^{r-2-m}\Bigr) = z(1 + z)^{r-3} \left[ \frac{1 - 2z^2}{2}(1 + 2z)^{k-1} S\bigl(a(z)\bigr) - \frac{1 + 2z + \sqrt{1 - 4z - 4z^2}}{4} S\bigl(b(z)\bigr) \right].$$
By Lemma 2 (`(2.1)` and `(2.3)`), $S(a(z)) = 1 + 2z$ and $-\frac{1 + 2z + \sqrt{1 - 4z - 4z^2}}{4} S(b(z)) = -H_2(z)$. Adding the leading term $z\Phi_{r-1, k-1}(z) = z(1 + z)^{r-3} \bigl(\frac{1 - 2z^2}{2}(1 + 2z)^{k-1} + H_2(z)\bigr)$, the $+H_2(z)$ and $-H_2(z)$ terms cancel identically, leaving
$$\text{RHS of (3.1)} = z(1 + z)^{r-3} \frac{1 - 2z^2}{2}(1 + 2z)^{k-1} \bigl(1 + (1 + 2z)\bigr) = z(1 + z)^{r-3} \frac{1 - 2z^2}{2}(1 + 2z)^{k-1} \cdot 2(1 + z) = z(1 - 2z^2)(1 + z)^{r-2}(1 + 2z)^{k-1},$$
which matches `(3.3)`, establishing `(3.1)`.

Now let $r \ge 1$, $k \ge 1$, and $1 \le d \le \min(r, k)$, and extract $[z^d]$ on both sides of `(3.1)`:
- **Left-hand side**: Since $r \ge 1$, $k \ge 1$, $k - 1 \ge 0$, and $0 \le d \le r$, Lemma 1 applies to both $(r, k, d)$ and $(r, k-1, d)$, giving $[z^d]\Phi_{r,k}(z) - [z^d]\Phi_{r,k-1}(z) = F(r, k, d) - F(r, k-1, d)$.
- **First term on RHS**: Since $r - 1 \ge 0$, $k - 1 \ge 0$, and $0 \le d - 1 \le r - 1$, Lemma 1 gives $[z^d]\bigl(z\Phi_{r-1,k-1}(z)\bigr) = [z^{d-1}]\Phi_{r-1,k-1}(z) = F(r-1, k-1, d-1)$.
- **Summation on RHS**: For each $m \ge 0$, $[z^d]\bigl(z^{m+1}(\cdots)\bigr) = [z^{d-1-m}]\bigl(\Phi_{r-1-m, k-1-m}(z) - (1 + z)^{r-2-m}\bigr)$:
  - If $m \ge d$, then $d - 1 - m < 0$, so $[z^{d-1-m}]$ of a formal power series in $\mathbb{Q}[[z]]$ is $0$.
  - If $m = d - 1$, then $d - 1 - m = 0$. For every $a, b \in \mathbb{Z}$, $\Phi_{a, b}(0) = 1^{a-2}(\frac{1}{2} + \frac{3-1}{4}) = 1$ and $(1 + 0)^{a-1} = 1$, so $[z^0]\bigl(\Phi_{r-d, k-d}(z) - (1 + z)^{r-d-1}\bigr) = 1 - 1 = 0$.
  - If $0 \le m \le d - 2$, write $i = m + 2$, so $2 \le i \le d$. Then $d' := d + 1 - i \ge 1$, $r' := r + 1 - i \ge d' \ge 1$, and $k' := k + 1 - i \ge d' \ge 1$. Hence Lemma 1 gives $[z^{d+1-i}]\Phi_{r+1-i, k+1-i}(z) = F(r + 1 - i, k + 1 - i, d + 1 - i)$. Moreover, $r - i = r' - 1 \ge 0$, so $[z^{d+1-i}](1 + z)^{r-i} = \binom{r - i}{d + 1 - i}$.

Therefore, for all $r, k \ge 1$ and $1 \le d \le \min(r, k)$,
$$F(r, k, d) - F(r, k-1, d) = F(r-1, k-1, d-1) + \sum_{i=2}^{d} \operatorname{Sch}_{i-2} \left( F(r+1-i, k+1-i, d+1-i) - \binom{r - i}{d + 1 - i} \right).$$
When $1 \le d < r, k$, this is Theorem 4.4 (`(R3)`). When $1 \le d = r \le k$, for every $2 \le i \le r$ one has $0 \le r - i < r + 1 - i$, so $\binom{r - i}{r + 1 - i} = 0$, giving `(3.2)` and (for $k > r$) Proposition 4.2 (`(R1)`). $\blacksquare$

---

## Section 6. Self-Contained Proof of Diagonal Base Cases $F(r, r, r) = \operatorname{Sch}_{r-1}$

*(Note: Höngesberg, Konvalinka, and Linusson already prove $F(r, r, r) = \operatorname{Sch}_{r-1}$ on lines 579-608 of the arXiv source file Extended_avoidance (tex) via Barry `[Bar21]` and Gauss contiguous relations `[AAR99]`. To keep this proof 100% self-contained with zero external dependencies, I prove $F(r, r-1, r) = 0$ and $F(r, r, r) = \operatorname{Sch}_{r-1}$ directly from Lemma 1 via formal Laurent residues.)*

### Lemma 4 (Formal Residue Invariance and Diagonal Evaluation)
1. **Formal residue change of variables**: Let $\mathbb{Q}((z))$ be the field of formal Laurent series $f(z) = \sum_{n \ge n_0} f_n z^n$, with formal residue $\operatorname{Res}_{z=0} f(z)\,dz := f_{-1} = [z^{-1}] f(z)$ and formal derivative $f'(z) := \sum_{n \ge n_0} n f_n z^{n-1}$. Let $z(u) = \sum_{m \ge 1} c_m u^m \in u\mathbb{Q}[[u]]$ have $c_1 \ne 0$. Then for every $f(z) \in \mathbb{Q}((z))$,
   $$\operatorname{Res}_{z=0} f(z)\,dz = \operatorname{Res}_{u=0} f\bigl(z(u)\bigr) z'(u)\,du. \tag{4.1}$$
2. For every integer $r \ge 1$,
   $$F(r, r-1, r) = 0 \qquad \text{and} \qquad F(r, r, r) = \operatorname{Sch}_{r-1}. \tag{4.2}$$

#### Proof of Lemma 4
1. Write $z(u) = u g(u)$, where $g(u) \in \mathbb{Q}[[u]]$ has $g(0) = c_1 \ne 0$, so $g(u)$ is a unit in $\mathbb{Q}[[u]]$. For any integer $m \in \mathbb{Z}$, $z(u)^m z'(u) = u^m g(u)^m z'(u)$ has $u$-adic valuation at least $m$, so the map $f(z) \mapsto f(z(u)) z'(u)$ is well-defined and $\mathbb{Q}$-linear on $\mathbb{Q}((z))$. Moreover, since $z(u)^m z'(u) \in \mathbb{Q}[[u]]$ contains no negative powers of $u$ whenever $m \ge 0$, only the finitely many terms $n_0 \le m \le -1$ of $f(z) = \sum_{m \ge n_0} f_m z^m$ can contribute to $[u^{-1}]\bigl(f(z(u)) z'(u)\bigr)$. By $\mathbb{Q}$-linearity, it suffices to verify `(4.1)` on each single Laurent monomial $f(z) = z^m$ ($m \in \mathbb{Z}$):
   - If $m \ne -1$, then $z(u)^m z'(u) = \frac{1}{m + 1} \frac{d}{du}\bigl(z(u)^{m+1}\bigr)$. For any Laurent series $h(u) = \sum_n h_n u^n$, $h'(u) = \sum_n n h_n u^{n-1}$ has $[u^{-1}] h'(u) = 0 \cdot h_0 = 0 = [z^{-1}] z^m$.
   - If $m = -1$, then by the product rule $z'(u) = g(u) + u g'(u)$, so
     $$z(u)^{-1} z'(u) = \frac{g(u) + u g'(u)}{u g(u)} = u^{-1} + g'(u) g(u)^{-1}.$$
     Since $g'(u) g(u)^{-1} \in \mathbb{Q}[[u]]$ has zero $[u^{-1}]$ coefficient, $[u^{-1}]\bigl(z(u)^{-1} z'(u)\bigr) = 1 = [z^{-1}] z^{-1}$.
   This proves `(4.1)`.

2. Let $r \ge 1$. Since $r \ge 1$, $r - 1 \ge 0$, and $0 \le r \le r$, Lemma 1 gives $F(r, r-1, r) = [z^r] \Phi_{r, r-1}(z)$ and $F(r, r, r) = [z^r] \Phi_{r, r}(z)$. Recall $\Phi_{r, k}(z) = \frac{1 - 2z^2}{2}(1 + z)^{r-2}(1 + 2z)^k + (1 + z)^{r-2} H_2(z)$ where $H_2(z) = \frac{3 + 2z - \sqrt{1 - 4z - 4z^2}}{4}$. I evaluate $[z^r]$ of the two summands separately using `(4.1)`:

   - **Second summand**: Apply `(4.1)` to $f(z) = \frac{(1 + z)^{r-2} H_2(z)}{z^{r+1}}$ with $z(w) = \frac{w}{1 - w} = w + w^2 + \cdots$ ($c_1 = 1 \ne 0$). Then $1 + z(w) = (1 - w)^{-1}$ and $z'(w) = (1 - w)^{-2}$. Substituting into `(4.1)`:
     $$[z^r]\bigl((1 + z)^{r-2} H_2(z)\bigr) = \operatorname{Res}_{w=0} \frac{(1 - w)^{-(r-2)} H_2\!\left(\frac{w}{1-w}\right)}{w^{r+1}(1 - w)^{-(r+1)}} (1 - w)^{-2}\,dw = [w^r]\left\{(1 - w) H_2\!\left(\frac{w}{1 - w}\right)\right\}.$$
     As computed in Lemma 2 (Part 3, since $\frac{w/(1-w)}{1 + w/(1-w)} = w$), $1 - 4z(w) - 4z(w)^2 = \frac{1 - 6w + w^2}{(1 - w)^2}$ and $3 + 2z(w) = \frac{3 - w}{1 - w}$, so
     $$(1 - w) H_2\!\left(\frac{w}{1 - w}\right) = \frac{3 - w - \sqrt{1 - 6w + w^2}}{4} = \frac{2 + (1 - w - \sqrt{1 - 6w + w^2})}{4} = \frac{1 + w S(w)}{2}.$$
     Since $r \ge 1$, $[w^r]\left(\frac{1 + w S(w)}{2}\right) = \frac{1}{2}[w^{r-1}] S(w) = \frac{1}{2}\operatorname{Sch}_{r-1}$.

   - **First summand (for $k \in \{r - 1, r\}$)**: Define $z(u) := \frac{S(u) - 1}{2} = \frac{1}{2}\sum_{m \ge 1} \operatorname{Sch}_m u^m \in u\mathbb{Q}[[u]]$, which has $[u^1] z(u) = \frac{1}{2}\operatorname{Sch}_1 = 1 \ne 0$. Then $1 + 2z(u) = S(u)$ and $1 + z(u) = \frac{S(u) + 1}{2}$. From Lemma 2 (Part 1), $u S(u)^2 - (1 - u)S(u) + 1 = 0$, which rearranges to $u S(u)(S(u) + 1) = S(u) - 1$, i.e.,
     $$\frac{z(u)}{(1 + z(u))(1 + 2z(u))} = \frac{(S(u) - 1)/2}{\frac{S(u) + 1}{2} S(u)} = \frac{S(u) - 1}{S(u)(S(u) + 1)} = u. \tag{4.3}$$
     Differentiating `u = z(u) (1 + 3z(u) + 2z(u)^2)^{-1}` formally with respect to $u$ by the quotient rule gives
     $$1 = \frac{(1 + 3z(u) + 2z(u)^2) - z(u)(3 + 4z(u))}{(1 + z(u))^2 (1 + 2z(u))^2} z'(u) = \frac{1 - 2z(u)^2}{(1 + z(u))^2 (1 + 2z(u))^2} z'(u),$$
     so $\bigl(1 - 2z(u)^2\bigr) z'(u) = (1 + z(u))^2 (1 + 2z(u))^2$. Applying `(4.1)` to $f(z) = \frac{1 - 2z^2}{2} \frac{(1 + z)^{r-2}(1 + 2z)^k}{z^{r+1}}$ and substituting $z(u) = u(1 + z(u))(1 + 2z(u))$ from `(4.3)` gives
     $$[z^r]\left\{\frac{1 - 2z^2}{2}(1 + z)^{r-2}(1 + 2z)^k\right\} = \operatorname{Res}_{u=0} \frac{1}{2} \frac{(1 + z(u))^{r-2}(1 + 2z(u))^k}{u^{r+1}(1 + z(u))^{r+1}(1 + 2z(u))^{r+1}} (1 + z(u))^2 (1 + 2z(u))^2\,du = [u^r]\left\{\frac{(1 + 2z(u))^{k - r + 1}}{2(1 + z(u))}\right\}.$$
     Now evaluate $\frac{1}{2(1 + z(u))}$: from $1 + z(u) = \frac{S(u) + 1}{2} = \frac{1 + u - \sqrt{1 - 6u + u^2}}{4u}$ and $(1 + u - \sqrt{1 - 6u + u^2})(1 + u + \sqrt{1 - 6u + u^2}) = (1 + u)^2 - (1 - 6u + u^2) = 8u$, I obtain
     $$\frac{1}{2(1 + z(u))} = \frac{4u}{2(1 + u - \sqrt{1 - 6u + u^2})} = \frac{4u(1 + u + \sqrt{1 - 6u + u^2})}{16u} = \frac{1 + u + (1 - u - 2u S(u))}{4} = \frac{1 - u S(u)}{2}.$$
     - At $k = r - 1$ ($k - r + 1 = 0$), since $r \ge 1$, $[u^r]\left(\frac{1 - u S(u)}{2}\right) = -\frac{1}{2}\operatorname{Sch}_{r-1}$.
     - At $k = r$ ($k - r + 1 = 1$), since $\frac{1 + 2z(u)}{2(1 + z(u))} = 1 - \frac{1}{2(1 + z(u))} = 1 - \frac{1 - u S(u)}{2} = \frac{1 + u S(u)}{2}$ and $r \ge 1$, $[u^r]\left(\frac{1 + u S(u)}{2}\right) = +\frac{1}{2}\operatorname{Sch}_{r-1}$.

   Adding the first and second summands for $r \ge 1$ yields
   $$F(r, r-1, r) = -\frac{1}{2}\operatorname{Sch}_{r-1} + \frac{1}{2}\operatorname{Sch}_{r-1} = 0 \qquad \text{and} \qquad F(r, r, r) = \frac{1}{2}\operatorname{Sch}_{r-1} + \frac{1}{2}\operatorname{Sch}_{r-1} = \operatorname{Sch}_{r-1}. \quad \blacksquare$$

*(Remark: Notice that `(3.2)` at $k = r$ together with $F(r, r-1, r) = 0$ also immediately recovers the Schröder recurrence $F(r, r, r) = F(r-1, r-1, r-1) + \sum_{i=2}^r \operatorname{Sch}_{i-2} F(r+1-i, r+1-i, r+1-i)$.)*

---

## Section 7. Universal Chu-Vandermonde Proof of Proposition 4.3 (`lem:k=d`)

### Lemma 5 (Universal Linear Operator Identity and `lem:k=d`)
For every formal power series $G(z) = \sum_{n \ge 0} g_n z^n \in \mathbb{Q}[[z]]$ and all integers $1 \le k < r$,
$$[z^k]\bigl((1 + z)^{r-2} G(z)\bigr) = \sum_{j=0}^{k} [z^j]\bigl((1 + z)^{j-2} G(z)\bigr) \binom{r - j - 1}{k - j}. \tag{5.1}$$
In particular, setting $G(z) = G_k(z)$ yields Proposition 4.3 (`lem:k=d`, `(R2)`):
$$F(r, k, k) = \sum_{j=0}^{k} F(j, k, j) \binom{r - j - 1}{k - j} \qquad \text{for all } 1 \le k < r.$$

#### Proof of Lemma 5
First recall two elementary polynomial binomial identities valid for all $x, y \in \mathbb{Z}$ and integers $M \ge 0$:
- **Upper negation**: For $M \ge 0$, factoring $(-1)$ from each of the $M$ factors in the numerator gives
  $$\binom{x}{M} = \frac{x(x-1)\cdots(x-M+1)}{M!} = (-1)^M \frac{(-x)(-x+1)\cdots(-x+M-1)}{M!} = (-1)^M \binom{M - x - 1}{M}. \tag{5.2}$$
- **Chu-Vandermonde**: Since $(1 + t)^x (1 + t)^y = (1 + t)^{x+y}$ in $\mathbb{Q}[[t]]$, extracting $[t^M]$ gives
  $$\sum_{m=0}^{M} \binom{x}{m} \binom{y}{M - m} = \binom{x + y}{M}. \tag{5.3}$$

Now consider `(5.1)`. Both sides of `(5.1)` depend only on the coefficients $g_0, g_1, \dots, g_k$ of $G(z)$ and are $\mathbb{Q}$-linear in $(g_0, \dots, g_k)$. Thus it suffices to verify `(5.1)` on each basis monomial $G(z) = z^n$ for $0 \le n \le k$:
- On the left-hand side of `(5.1)`, $[z^k]\bigl(z^n (1 + z)^{r-2}\bigr) = [z^{k-n}](1 + z)^{r-2} = \binom{r - 2}{k - n}$.
- On the right-hand side of `(5.1)`, for each $0 \le j \le k$, $[z^j]\bigl(z^n (1 + z)^{j-2}\bigr) = [z^{j-n}](1 + z)^{j-2} = \binom{j - 2}{j - n}$ (which vanishes for $j < n$). Setting $m = j - n$ and $M = k - n \ge 0$, the right-hand side equals
  $$\sum_{m=0}^{M} \binom{n - 2 + m}{m} \binom{r - n - 1 - m}{M - m}.$$
  Applying upper negation `(5.2)` to both factors in each summand gives
  $$\binom{n - 2 + m}{m} = (-1)^m \binom{-n + 1}{m} \qquad \text{and} \qquad \binom{r - n - 1 - m}{M - m} = (-1)^{M - m} \binom{M - r + n}{M - m}.$$
  Since $(-1)^m (-1)^{M - m} = (-1)^M$, Chu-Vandermonde `(5.3)` with $x = -n + 1$ and $y = M - r + n$ yields
  $$\sum_{m=0}^{M} \binom{n - 2 + m}{m} \binom{r - n - 1 - m}{M - m} = (-1)^M \sum_{m=0}^{M} \binom{-n + 1}{m} \binom{M - r + n}{M - m} = (-1)^M \binom{M - r + 1}{M}.$$
  Applying upper negation `(5.2)` once more gives $(-1)^M \binom{M - r + 1}{M} = \binom{r - 2}{M} = \binom{r - 2}{k - n}$, matching the left-hand side for every $0 \le n \le k$. This proves `(5.1)`.

Finally, let $1 \le k < r$ and set $G(z) = G_k(z)$ in `(5.1)`. Since $r > k \ge 1$, Lemma 1 gives $[z^k]\bigl((1 + z)^{r-2} G_k(z)\bigr) = [z^k]\Phi_{r, k}(z) = F(r, k, k)$. Likewise, for every $j \in \{0, 1, \dots, k\}$, one has $j \ge 0$, $k \ge 1$, and $0 \le j \le j$, so Lemma 1 gives $[z^j]\bigl((1 + z)^{j-2} G_k(z)\bigr) = [z^j]\Phi_{j, k}(z) = F(j, k, j)$ (including $j = 0$ and $j = 1$). Substituting into `(5.1)` proves $F(r, k, k) = \sum_{j=0}^k F(j, k, j) \binom{r - j - 1}{k - j}$. $\blacksquare$

---

## Section 8. Proof of the Main Theorem (Conjecture 4.5)

Let $T(r, k, d) := F(r, k, d)$ on the cone $\{(r, k, d) \in \mathbb{Z}^3 : 0 \le d \le r, k\}$. I check all five hypotheses of Lemma 0:
1. $F(r, k, 0) = 1$ for all $r, k \ge 0$, proved in Section 1.1.
2. $F(r, r, r) = \operatorname{Sch}_{r-1}$ for all $r \ge 1$, proved in Lemma 4 (`(4.2)`).
3. For all $1 \le r < k$, $F(r, k, r)$ satisfies Proposition 4.2 (`(R1)`), proved in Lemma 3 (`(3.2)`).
4. For all $1 \le k < r$, $F(r, k, k)$ satisfies Proposition 4.3 (`(R2)`), proved in Lemma 5.
5. For all $1 \le d < r, k$, $F(r, k, d)$ satisfies Theorem 4.4 (`(R3)`), proved in Lemma 3.

By Lemma 0, $S^{312}_{r,k,d} = F(r, k, d)$ holds unconditionally for all integers $r, k, d$ with $0 \le d \le r, k$. This completes the proof of Conjecture 4.5. $\blacksquare$
