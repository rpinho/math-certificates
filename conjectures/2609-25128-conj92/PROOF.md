# Proof of Conjecture 9.2 of Ma, Sahbi, and Zhang (`arXiv:2609.25128v4`)

## Statement

Let $G = (V, E)$ be a finite, simple, undirected graph of order $n = |V|$, and let $\overline{G} = \bigl(V, \binom{V}{2} \setminus E\bigr)$ denote its complement. For $v \in V$, write $N_G(v) = \{u \in V : uv \in E\}$ and $N_G[v] = N_G(v) \cup \{v\}$.

**Definition 1 (Sub-quorum coloring; Definition 2.2 of `arXiv:2609.25128v4`).**
A *sub-quorum coloring* of $G$ with $k$ colors ($k \ge 0$) is an onto partial map $f : V \dashrightarrow \{1, \dots, k\}$ with domain $S = \operatorname{dom}(f) \subseteq V$ such that every $v \in S$ satisfies
$$|\{u \in N_G[v] \cap S : f(u) = f(v)\}| \ge \frac{|N_G[v] \cap S|}{2}.$$
The *sub-quorum coloring number* $\psi_{sq}(G)$ is the maximum integer $k$ for which $G$ admits a sub-quorum coloring with $k$ colors.

We prove **Conjecture 9.2 (`\label{conj:ng-upper}`)** of Haobo Ma, Rafik Sahbi, and Wenlin Zhang, *Sub-quorum colorings of graphs* (`arXiv:2609.25128v4`):

**Theorem 1.** *For every finite simple undirected graph $G$ of order $n \ge 2$ (and also for $n = 1$),*
$$\psi_{sq}(G) + \psi_{sq}(\overline{G}) \le n + 2.$$

---

## Auxiliary Lemmas

**Lemma 1 (Vertex-weight identity and induced-degree class-size bound).**
*Let $f : V \dashrightarrow \{1, \dots, k\}$ be any sub-quorum coloring of $G$ with colored support $S = \operatorname{dom}(f)$ and color classes $C_i = f^{-1}(i)$ for $1 \le i \le k$. Define $w_f : V \to [0, 1]$ by*
$$w_f(v) = \begin{cases} \dfrac{1}{|C_{f(v)}|}, & \text{if } v \in S, \\[8pt] 0, & \text{if } v \in V \setminus S. \end{cases}$$
*Then:*
1. *$0 \le w_f(v) \le 1$ for every $v \in V$, and $\sum_{v \in V} w_f(v) = k$.*
2. *For every subset $I \subseteq S$ and every vertex $v \in I$, put $d_I(v) = |N_G(v) \cap I|$. Then*
   $$|C_{f(v)}| \ge 1 + \left\lfloor \frac{d_I(v)}{2} \right\rfloor, \qquad \text{and hence} \qquad w_f(v) \le \frac{1}{1 + \lfloor d_I(v)/2 \rfloor}.$$

*Proof.*
1. When $k = 0$, $S = \emptyset$ and $w_f \equiv 0$, so $\sum_{v \in V} w_f(v) = 0 = k$. When $k \ge 1$, because $f : S \to \{1, \dots, k\}$ is onto, the color classes $C_1, \dots, C_k$ partition $S$ into $k$ nonempty pairwise disjoint sets ($|C_i| \ge 1$). Thus $0 < \frac{1}{|C_i|} \le 1$ for $v \in C_i$, $w_f(v) = 0$ for $v \in V \setminus S$, and
   $$\sum_{v \in V} w_f(v) = \sum_{i=1}^{k} \sum_{v \in C_i} \frac{1}{|C_i|} = \sum_{i=1}^{k} \frac{|C_i|}{|C_i|} = k.$$
2. Fix $I \subseteq S$ and $v \in I$, and write $C = C_{f(v)} \subseteq S$. Because $N_G[v] \cap C \subseteq C$ and $I \subseteq S$, Definition 1 at $v \in S$ gives
   $$|C| \ge |N_G[v] \cap C| \ge \frac{|N_G[v] \cap S|}{2} \ge \frac{|N_G[v] \cap I|}{2}.$$
   Since $v \in I$ and $G$ has no loops ($v \notin N_G(v)$), $|N_G[v] \cap I| = 1 + |N_G(v) \cap I| = 1 + d_I(v)$, so
   $$2|C| \ge 1 + d_I(v).$$
   Write $d_I(v) = 2q + \varepsilon$ with $q = \lfloor d_I(v)/2 \rfloor \ge 0$ and $\varepsilon \in \{0, 1\}$. If $\varepsilon = 0$, then $2|C| \ge 2q + 1$; since $2|C|$ is an even integer, this forces $2|C| \ge 2q + 2$. If $\varepsilon = 1$, then $2|C| \ge 2q + 2$ directly. In both cases $|C| \ge q + 1 = 1 + \lfloor d_I(v)/2 \rfloor \ge 1$. Taking reciprocals yields $w_f(v) = \frac{1}{|C|} \le \frac{1}{1 + \lfloor d_I(v)/2 \rfloor}$. $\blacksquare$

---

**Lemma 2 (Elementary integer reciprocal inequality).**
*Let $a, b \ge 1$ and $s \ge 2$ be integers satisfying $a + b \ge s$. Then*
$$\frac{1}{a} + \frac{1}{b} \le 1 + \frac{1}{s - 1}.$$

*Proof.*
Set $s' = a + b \ge s \ge 2$. Since $a - 1 \ge 0$ and $b - 1 \ge 0$, we have $(a - 1)(b - 1) \ge 0$, which rearranges to
$$ab \ge a + b - 1 = s' - 1 \ge s - 1 \ge 1 > 0.$$
Dividing the positive quantity $s'$ by $ab \ge s' - 1 > 0$ gives
$$\frac{1}{a} + \frac{1}{b} = \frac{s'}{ab} \le \frac{s'}{s' - 1} = 1 + \frac{1}{s' - 1} \le 1 + \frac{1}{s - 1}. \quad \blacksquare$$

---

**Lemma 3 (Complementary induced-graph degree-sum bound).**
*Let $H = (I, E_H)$ be any finite simple undirected graph of order $m = |I| \ge 0$, with vertex degrees $d_I(v) = |N_H(v)|$ for $v \in I$. Define*
$$\Sigma(H) := \sum_{v \in I} \left( \frac{1}{1 + \lfloor d_I(v)/2 \rfloor} + \frac{1}{1 + \lfloor (m - 1 - d_I(v))/2 \rfloor} \right)$$
*(where $\Sigma(H) = 0$ when $m = 0$). Then:*
- **Case A ($m = 0$):** *$\Sigma(H) = 0$.*
- **Case B ($m = 1$):** *$\Sigma(H) = 2 = m + 1$.*
- **Case C ($m = 2r$ even, $r \ge 1$):** *$\Sigma(H) \le m + 2$.*
- **Case D ($m = 2r + 1$ odd, $r \ge 1$):** *$\Sigma(H) \le m + 2 + \dfrac{1}{r + 1} \le m + \dfrac{5}{2}$.*

*Consequently, $\Sigma(H) \le m + \dfrac{5}{2}$ for every finite simple graph $H$ of order $m \ge 0$.*

*Proof.*
- **Case A ($m = 0$):** The index set $I$ is empty, so $\Sigma(H) = 0 \le 0 + \frac{5}{2}$.
- **Case B ($m = 1$):** For the sole vertex $v \in I$, $d_I(v) = 0$ and $m - 1 - d_I(v) = 0$, giving $\Sigma(H) = \frac{1}{1} + \frac{1}{1} = 2 = m + 1 \le m + \frac{5}{2}$.

Now assume $m \ge 2$. For every $v \in I$, we have $0 \le d_I(v) \le m - 1$, so both $d_I(v) \ge 0$ and $m - 1 - d_I(v) \ge 0$. Hence
$$a(v) := 1 + \left\lfloor \frac{d_I(v)}{2} \right\rfloor \ge 1 \qquad \text{and} \qquad b(v) := 1 + \left\lfloor \frac{m - 1 - d_I(v)}{2} \right\rfloor \ge 1$$
are positive integers. Write
$$d_I(v) = 2q_1 + \varepsilon_1, \qquad m - 1 - d_I(v) = 2q_2 + \varepsilon_2,$$
with integers $q_1, q_2 \ge 0$ and remainders $\varepsilon_1, \varepsilon_2 \in \{0, 1\}$. Adding the two equations gives
$$m - 1 = 2(q_1 + q_2) + (\varepsilon_1 + \varepsilon_2) \qquad \text{and} \qquad a(v) + b(v) = 2 + q_1 + q_2.$$

- **Case C ($m = 2r$ even, $r \ge 1$):**
  Here $m - 1 = 2r - 1$ is odd. Since $\varepsilon_1 + \varepsilon_2 \in \{0, 1, 2\}$, parity forces $\varepsilon_1 + \varepsilon_2 = 1$, and therefore $q_1 + q_2 = r - 1$. Thus $a(v) + b(v) = r + 1 \ge 2$ for every $v \in I$. By Lemma 2 with $s = r + 1$,
  $$\frac{1}{a(v)} + \frac{1}{b(v)} \le 1 + \frac{1}{r} \qquad (\forall v \in I).$$
  Summing over all $m = 2r$ vertices of $I$ gives
  $$\Sigma(H) \le 2r\left(1 + \frac{1}{r}\right) = 2r + 2 = m + 2 \le m + \frac{5}{2}.$$

- **Case D ($m = 2r + 1$ odd, $r \ge 1$):**
  Here $m - 1 = 2r$ is even, so $\varepsilon_1 + \varepsilon_2 \in \{0, 2\}$, i.e., $\varepsilon_1 = \varepsilon_2 \in \{0, 1\}$:
  - If $d_I(v)$ is odd ($\varepsilon_1 = \varepsilon_2 = 1$), then $q_1 + q_2 = r - 1$ and $a(v) + b(v) = r + 1 \ge 2$. Lemma 2 with $s = r + 1$ yields
    $$\frac{1}{a(v)} + \frac{1}{b(v)} \le 1 + \frac{1}{r}.$$
  - If $d_I(v)$ is even ($\varepsilon_1 = \varepsilon_2 = 0$), then $q_1 + q_2 = r$ and $a(v) + b(v) = r + 2 \ge 3$. Lemma 2 with $s = r + 2$ yields
    $$\frac{1}{a(v)} + \frac{1}{b(v)} \le 1 + \frac{1}{r + 1}.$$
  By the handshaking lemma in $H$, $\sum_{v \in I} d_I(v) = 2|E_H|$ is even, so the number $t_{\mathrm{odd}}$ of odd-degree vertices in $H$ is even. Because $|I| = 2r + 1$ is odd, we must have $0 \le t_{\mathrm{odd}} \le 2r$, and $H$ contains $2r + 1 - t_{\mathrm{odd}} \ge 1$ vertices of even degree. Since $1 + \frac{1}{r + 1} < 1 + \frac{1}{r}$, replacing $(2r - t_{\mathrm{odd}}) \ge 0$ terms of size $1 + \frac{1}{r + 1}$ by $1 + \frac{1}{r}$ gives
  $$\Sigma(H) \le t_{\mathrm{odd}}\left(1 + \frac{1}{r}\right) + (2r + 1 - t_{\mathrm{odd}})\left(1 + \frac{1}{r + 1}\right) \le 2r\left(1 + \frac{1}{r}\right) + \left(1 + \frac{1}{r + 1}\right).$$
  Simplifying the right-hand side yields
  $$\Sigma(H) \le (2r + 2) + 1 + \frac{1}{r + 1} = (2r + 1) + 2 + \frac{1}{r + 1} = m + 2 + \frac{1}{r + 1}.$$
  Because $r \ge 1$, we have $\frac{1}{r + 1} \le \frac{1}{2}$, so $\Sigma(H) \le m + \frac{5}{2}$. $\blacksquare$

---

## Proof of Theorem 1

*Proof of Theorem 1.*
Let $G = (V, E)$ be any finite simple undirected graph of order $n = |V| \ge 1$. Let $f_1 : V \dashrightarrow \{1, \dots, k_1\}$ be an optimal sub-quorum coloring of $G$, with $k_1 = \psi_{sq}(G)$ and support $S_1 = \operatorname{dom}(f_1)$, and let $f_2 : V \dashrightarrow \{1, \dots, k_2\}$ be an optimal sub-quorum coloring of $\overline{G}$, with $k_2 = \psi_{sq}(\overline{G})$ and support $S_2 = \operatorname{dom}(f_2)$.

Put $I = S_1 \cap S_2$ and $m = |I|$, so $|V \setminus I| = n - m$. By Lemma 1(1) applied to $(G, f_1)$ and $(\overline{G}, f_2)$,
$$k_1 + k_2 = \sum_{v \in V} \bigl(w_{f_1}(v) + w_{f_2}(v)\bigr) = \sum_{v \in V \setminus I} \bigl(w_{f_1}(v) + w_{f_2}(v)\bigr) + \sum_{v \in I} \bigl(w_{f_1}(v) + w_{f_2}(v)\bigr).$$

First, consider any vertex $v \in V \setminus I$. Since $I = S_1 \cap S_2$, either $v \notin S_1$ (so $w_{f_1}(v) = 0$ and $w_{f_2}(v) \le 1$ by Lemma 1(1)) or $v \notin S_2$ (so $w_{f_2}(v) = 0$ and $w_{f_1}(v) \le 1$ by Lemma 1(1)). In either case $w_{f_1}(v) + w_{f_2}(v) \le 1$, and summing over the $n - m$ vertices of $V \setminus I$ gives
$$\sum_{v \in V \setminus I} \bigl(w_{f_1}(v) + w_{f_2}(v)\bigr) \le n - m.$$

Second, put $H = G[I]$. If $m = 0$, then $I = \emptyset$ and $\sum_{v \in I} \bigl(w_{f_1}(v) + w_{f_2}(v)\bigr) = 0 = \Sigma(H)$. If $m \ge 1$, then for every vertex $v \in I$, its degree in $H = G[I]$ is $d_I(v) = |N_G(v) \cap I|$, and because $G$ is simple, every vertex of $I \setminus \{v\}$ is adjacent to $v$ in exactly one of $G$ or $\overline{G}$, so its degree in $\overline{G}[I]$ is
$$|N_{\overline{G}}(v) \cap I| = (m - 1) - d_I(v).$$
Since $I \subseteq S_1$ and $I \subseteq S_2$, applying Lemma 1(2) to $(G, f_1)$ and to $(\overline{G}, f_2)$ gives, for every $v \in I$,
$$w_{f_1}(v) + w_{f_2}(v) \le \frac{1}{1 + \lfloor d_I(v)/2 \rfloor} + \frac{1}{1 + \lfloor (m - 1 - d_I(v))/2 \rfloor}.$$
Summing over $v \in I$ and applying Lemma 3 to $H = G[I]$ yields (for all $m \ge 0$)
$$\sum_{v \in I} \bigl(w_{f_1}(v) + w_{f_2}(v)\bigr) \le \Sigma(H) \le m + \frac{5}{2}.$$

Adding the bounds on $V \setminus I$ and $I$, we obtain
$$k_1 + k_2 \le (n - m) + \left(m + \frac{5}{2}\right) = n + \frac{5}{2}.$$
Because $k_1 = \psi_{sq}(G)$ and $k_2 = \psi_{sq}(\overline{G})$ are integers, $k_1 + k_2$ is an integer satisfying $k_1 + k_2 \le n + \frac{5}{2}$, and hence
$$\psi_{sq}(G) + \psi_{sq}(\overline{G}) \le \left\lfloor n + \frac{5}{2} \right\rfloor = n + 2. \quad \blacksquare$$

---

## Remarks on Sharpness and Relation to Known Bounds

1. **Sharpness of Theorem 1 ($n \ge 2$):** For every $n \ge 2$, $\psi_{sq}(K_n) + \psi_{sq}(\overline{K_n}) = 2 + n = n + 2$. Moreover, equality is also attained by graphs with strict dissociation gap $\psi_{sq}(G) > \beta_2(G)$, starting at $n = 6$ on the double star $S_{2,2}$ ($\psi_{sq}(S_{2,2}) = 5 > \beta_2(S_{2,2}) = 4$ and $\psi_{sq}(\overline{S_{2,2}}) = 3$, giving $5 + 3 = 8 = n + 2$).
2. **Exact sharpness of the $m + \frac{5}{2}$ constant in Lemma 3:** On $G = S_{2,2}$ with adjacent centers $x, y$ and leaf pairs $\{a_1, a_2\}$ at $x$ and $\{b_1, b_2\}$ at $y$, an optimal coloring $f_1$ of $G$ has $S_1 = V$ with color classes $\{x, y\}, \{a_1\}, \{a_2\}, \{b_1\}, \{b_2\}$ ($k_1 = 5$), and an optimal coloring $f_2$ of $\overline{G}$ has $S_2 = \{x, a_1, a_2\}$ with singleton classes $\{x\}, \{a_1\}, \{a_2\}$ ($k_2 = 3$, as $\overline{G}[S_2] \cong K_2 \cup K_1$). Here $I = S_1 \cap S_2 = \{x, a_1, a_2\}$ has $m = 3$ ($r = 1$), $G[I] \cong P_3$ has degrees $(2, 1, 1)$, and
   $$\sum_{v \in I} \bigl(w_{f_1}(v) + w_{f_2}(v)\bigr) = \left(\frac{1}{2} + 1\right) + (1 + 1) + (1 + 1) = \frac{11}{2} = m + \frac{5}{2} = \Sigma(G[I]),$$
   attaining Lemma 3(Case D) with exact equality. Meanwhile $y \in V \setminus I$ shares its color class with $x \in I$, contributing $w_{f_1}(y) + w_{f_2}(y) = \frac{1}{2}$ on $V \setminus I$ so that $\frac{11}{2} + \frac{5}{2} = 8 = n + 2$.
3. **Why Lemma 2.4 ($\Omega$) of `arXiv:2609.25128v4` could not prove Conjecture 9.2:** Replacing each non-singleton class $C_i$ by a single representative edge assigns weight $\frac{1}{2}$ to two vertices of $C_i$ even when large colored degree forces $|C_i| \ge 3$; thus $\Omega(\overline{K_6}) + \Omega(K_6) = 6 + 3 = 9 = n + 3$. Keeping the exact class-size reciprocal $1/|C_{f(v)}|$ in Lemma 1 retains a necessary class-size bound forced by the quorum majority constraint (sufficient for Theorem 1, though distinct colorings can share identical vertex weights).
4. **Recovery of Sahbi & Chellali (2018):** Restricting $f_1, f_2$ to total quorum colorings ($S_1 = S_2 = V$, so $I = V$ and $m = n$) immediately yields $\psi_q(G) + \psi_q(\overline{G}) \le n + 2$ for all $n \ge 2$.
