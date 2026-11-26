# Unconditional Sub-$5n$ Upper Bound for Erdos Problem #1182: $F(n) \le \lfloor \frac{99}{20}n \rfloor - 1$ for All $n \ge 450{,}000$

**Theorem 1.** *Let $F(n)$ denote the largest integer $q$ such that every connected simple graph $G$ on $n$ vertices with at most $q$ edges satisfies $R(K_3, G) = 2n - 1$. For every integer $n \ge 450{,}000$ (both even and odd $n$),*
$$F(n) \le \left\lfloor \frac{99}{20} n \right\rfloor - 1 < 4.95\,n.$$

All logarithms below are natural, with $0 \log 0 := 0$ by continuity. My proof builds on the balanced $C_5$ blow-up construction of Brandt (1996) and Nikiforov and Rousseau (2009), the configuration-model pairing framework of Kataria (2026), and the Round 1 potential-minimal Kempe-swap dichotomy (`2c87d8e`, [PRIOR_ART.md](referee/PRIOR_ART.md)), generalized here to a $(9, 10)$-bidegree configuration model with a closed-form vertex-convex saddlepoint dual and a 1D-concave product occupancy bound in Case I.

---

## 1. Reduction to $(9, 10)$-Bidegree Part Maps

Fix any integer $n \ge n_0 := 450{,}000$. Write $2n - 1 = 5h + s$ with integers $h \ge 1$ and $0 \le s \le 4$. Form the red graph $H_n$ on $2n - 1$ vertices by partitioning $V(H_n)$ into five independent sets $W_0, W_1, W_2, W_3, W_4$ (indexed by $\mathbb{Z}_5$) of sizes $k_i \in \{h, h + 1\}$ with $\sum_{i=0}^4 k_i = 2n - 1$, placing complete bipartite red edge sets between $W_i$ and $W_{i \pm 1 \pmod 5}$. Because $C_5$ is triangle-free, $H_n$ is triangle-free. Its complement $\overline{H_n}$ (the blue graph) has adjacency indicator $A_{ij} = \mathbf{1}_{(j - i) \bmod 5 \in \{0, 2, 3\}}$ between parts: each $W_i$ is a blue clique ($A_{ii} = 1$), and $W_i \cup W_j$ is complete blue whenever $j - i \equiv 2, 3 \pmod 5$.

Set
$$k := \left\lceil \frac{n}{20} \right\rceil, \qquad n_9 := 2k = 2\left\lceil \frac{n}{20} \right\rceil, \qquad n_{10} := n - n_9.$$
For every integer $n \ge 20$ (both even and odd $n$), $n_9 = 2k$ is an even positive integer, $n_{10} > 0$, and the total stub count
$$D := 9 n_9 + 10 n_{10} = 10 n - 2k$$
is an even integer. Moreover, writing $n = 20 q + r$ with $q \in \mathbb{Z}_{\ge 1}$ and $r \in \{0, 1, \dots, 19\}$:
- if $r = 0$, then $D / 2 = 5(20q) - q = 99q = \lfloor \frac{99}{20} n \rfloor$;
- if $1 \le r \le 19$, then $k = q + 1$, so $D / 2 = 5(20q + r) - (q + 1) = 99q + 5r - 1 = \lfloor 99q + 5r - \frac{r}{20} \rfloor = \lfloor \frac{99}{20} n \rfloor$.

Hence the number of multiedges is identically $m := D / 2 = \lfloor \frac{99}{20} n \rfloor$ for every integer $n$. Furthermore, since $\frac{n}{20} \le \lceil \frac{n}{20} \rceil \le \frac{n + 19}{20}$, the degree-$9$ vertex fraction $\alpha_9 := \frac{n_9}{n}$, degree-$10$ fraction $\theta := \frac{n_{10}}{n} = 1 - \alpha_9$, and average degree $\bar{d} := \frac{D}{n} = 9 \alpha_9 + 10 \theta = 10 - \alpha_9$ satisfy, for every $n \ge n_0 = 450{,}000$,
$$\alpha_9 \in \left[\frac{1}{10},\; \frac{1}{10} + \frac{19}{10 n_0}\right] = \left[\frac{1}{10},\; \frac{450{,}019}{4{,}500{,}000}\right], \qquad \bar{d} \in \left[\frac{44{,}549{,}981}{4{,}500{,}000},\; \frac{99}{10}\right].$$

Partition a fixed $n$-vertex set $V$ into $V^{(9)}$ of size $n_9$ (assigning $9$ labelled stubs to each $u \in V^{(9)}$) and $V^{(10)}$ of size $n_{10}$ (assigning $10$ labelled stubs to each $u \in V^{(10)}$). Sample a uniform perfect matching of all $D$ stubs to obtain a random configuration multigraph $M$ on $V$ with $m = \lfloor \frac{99}{20} n \rfloor$ multiedges, and let $G = \mathrm{simple}(M)$ be the simple graph obtained by deleting all self-loops and replacing parallel multiedges between distinct vertices by single simple edges. Then:
1. $e(G) \le m = \lfloor \frac{99}{20} n \rfloor$.
2. $G$ is connected if and only if $M$ is connected, since loops join a vertex to itself and collapsing parallel edges preserves vertex reachability.
3. Call a part map $f : V \to \mathbb{Z}_5$ *valid* for $M$ if $|f^{-1}(i)| \le k_i$ for every $i \in \mathbb{Z}_5$ and every paired stub $\{s, s'\}$ of $M$ at vertices $\{u, v\}$ satisfies $A_{f(u), f(v)} = 1$. Then $G \subseteq \overline{H_n}$ if and only if $M$ admits a valid map $f$: any injective homomorphism $\phi : V(G) \hookrightarrow V(\overline{H_n})$ induces $f(u) = i$ for $\phi(u) \in W_i$, where self-loops at $u$ automatically satisfy $A_{f(u), f(u)} = 1$ and parallel edges repeat the simple-edge condition $A_{f(u), f(v)} = 1$; conversely, any valid map $f$ lifts to an embedding $G \hookrightarrow \overline{H_n}$ by choosing arbitrary injections $f^{-1}(i) \hookrightarrow W_i$ (since each $W_i$ is a blue clique).

(By Janson's theorem, $\Pr(M \text{ is simple}) = \exp(-\lambda - \lambda^2 + o(1)) = \Theta(1)$ with $\lambda = \frac{36 + 9\theta}{9 + \theta} \in [4, 4.5]$, but working directly with $G = \mathrm{simple}(M)$ avoids conditioning on simplicity and yields an unconditional finite-$n$ bound with zero asymptotic error terms.)

If I show $\Pr(M \text{ admits a valid map}) + \Pr(M \text{ disconnected}) < 1$, then there exists a deterministic pairing $M$ that is connected and admits no valid map; its simplification $G = \mathrm{simple}(M)$ is a connected $n$-vertex simple graph with $e(G) \le \lfloor \frac{99}{20} n \rfloor$ and $G \not\subseteq \overline{H_n}$, so $R(K_3, G) > 2n - 1$ and therefore $F(n) \le e(G) - 1 \le \lfloor \frac{99}{20} n \rfloor - 1$.

---

## 2. Canonical Regions and the Bidegree Kempe-Swap Dichotomy

If $M$ admits at least one valid map, choose a valid map $f : V \to \mathbb{Z}_5$ minimizing the potential
$$\Phi(f) := \sum_{i=0}^4 v_i^2, \qquad v_i := |V_i| = |f^{-1}(i)|.$$
Write $a_i := v_i / n$, so $\sum_{i=0}^4 a_i = 1$. Since $5h + s = 2n - 1$ with $s \ge 0$, if $s = 0$ then $k_i = h = \frac{2n - 1}{5} < \frac{2}{5}n$, while if $s \ge 1$ then $k_i \le h + 1 = \frac{2n - 1 - s + 5}{5} \le \frac{2n + 3}{5}$. Thus for every $n \ge 450{,}000$,
$$\max_{0 \le i \le 4} a_i \le \frac{2}{5} + \frac{3}{5 n} \le \frac{2}{5} + \frac{3}{2{,}250{,}000} < \frac{4001}{10000}.$$

The $10$-element dihedral group $D_5$ of symmetries of $\mathbb{Z}_5$ preserves blue adjacency $A$ and permutes the capacity vector $(k_0, \dots, k_4) \in \{h, h + 1\}^5$. Fix a pair of two largest parts of $f$:
- **Region A:** If the pair is red-adjacent, apply a dihedral symmetry so that $a_0 \ge a_1 \ge \max(a_2, a_3, a_4)$.
- **Regions B and C:** If the pair is blue-adjacent, apply a rotation to place it at $\{0, 2\}$, and apply the reflection $i \mapsto (2 - i) \bmod 5 = (0\;2)(3\;4)$ if needed so that $a_3 \ge a_4$ (leaving $a_0, a_2$ unordered, with $\min(a_0, a_2) \ge \max(a_1, a_3, a_4)$). With $\delta := \frac{3}{20}$, **Region B** imposes $\min(a_0, a_2) - a_3 \le \delta$, and **Region C** imposes $\min(a_0, a_2) - a_3 \ge \delta$.

**Lemma 2 (Kempe-swap dichotomy for $(9, 10)$-bidegree multigraphs).** *Let $n \ge 254$ and let $f$ be a $\Phi$-minimal valid map whose dihedral normalization lies in Region C. For each $u \in V$ and $i \in \mathbb{Z}_5$, let $n_i(u)$ be the number of stubs at $u$ whose paired mate lies in $V_i$ (so $\sum_{i=0}^4 n_i(u) = d(u) \in \{9, 10\}$). Put $Z_0 := \{u \in V_0 : n_3(u) = 0\}$ and $G_2 := \{v \in V_2 : n_4(v) = 0\}$. Then:*
1. *Every $u \in V_0$ satisfies $n_2(u) \ge 1$, and every $v \in V_2$ satisfies $n_0(v) \ge 1$.*
2. *Either **Case I** holds: $|Z_0| \le 19$, or **Case II** holds: every $u \in V_0$ has at least one stub paired to a vertex in $V_2 \setminus G_2$.*

*Proof.* In Region C, $v_0 - v_3 \ge \frac{3}{20}n > 38 \ge 2$ and $v_2 - v_4 \ge v_2 - v_3 \ge \frac{3}{20}n > 2$ (for $n \ge 254$). Note that neither capacity feasibility nor $\Phi$-decrease depends on vertex degrees: whenever a valid recoloring changes the part-size vector $v$ by $-1$ in part $i$, $+1$ in part $j$, and $0$ in all other parts for some $i, j$ with $v_i \ge v_j + 2$, we have $v_j + 1 \le v_i - 1 \le (h + 1) - 1 = h \le k_j$ (so every part obeys its capacity $k_\ell$) and
$$\Delta \Phi = (v_i - 1)^2 + (v_j + 1)^2 - v_i^2 - v_j^2 = 2(v_j - v_i + 1) \le -2 < 0,$$
contradicting $\Phi$-minimality of $f$.

For (1), any $u \in V_0$ has all stub mates in $V_0 \cup V_2 \cup V_3$. If $n_2(u) = 0$, recoloring $u : 0 \to 3$ places all non-loop edges at $u$ on $\{3\} \times \{0, 3\}$ and any self-loops at $u$ on $(3, 3)$, all of which satisfy $A = 1$. Since $v_0 \ge v_3 + 2$, this contradicts $\Phi$-minimality. Likewise, any $v \in V_2$ has stub mates in $V_0 \cup V_2 \cup V_4$; if $n_0(v) = 0$, recoloring $v : 2 \to 4$ places all edges at $v$ on $\{4\} \times \{2, 4\}$ (blue) and decreases $\Phi$ since $v_2 \ge v_4 + 2$, contradiction.

For (2), suppose $|Z_0| \ge 20$ and suppose for contradiction that some $u \in V_0$ has all of its $V_2$-neighbors in $G_2$. Let $v_1, \dots, v_r \in G_2$ be the distinct vertices of $V_2$ paired to stubs of $u$. By (1), $r \ge 1$, and $r \le d(u) \le 10$. Because at least $r$ stubs of $u$ go to $V_2$, at most $d(u) - r \le 10 - r$ stubs of $u$ go to $V_0 \setminus \{u\}$, so $|N_M(u) \cap (Z_0 \setminus \{u\})| \le 10 - r$. Hence
$$|Z_0 \setminus (N_M(u) \cup \{u\})| \ge 20 - 1 - (10 - r) = 9 + r \ge r - 1.$$
Choose $r - 1$ distinct donor vertices $w_1, \dots, w_{r-1} \in Z_0 \setminus (N_M(u) \cup \{u\})$, and simultaneously recolor $u : 0 \to 3$, $v_1, \dots, v_r : 2 \to 0$, and $w_1, \dots, w_{r-1} : 0 \to 2$. All $2r$ moved vertices are pairwise distinct, and the net part-size changes are $\Delta v_0 = -1 + r - (r - 1) = 0$, $\Delta v_2 = -r + (r - 1) = -1$, $\Delta v_3 = +1$, and $\Delta v_1 = \Delta v_4 = 0$. Since $v_2 \ge v_3 + 2$, capacities hold and $\Delta \Phi \le -2$. Every paired stub remains blue:
- At $u$ (now in $3$): its old $V_2$-neighbors are $\{v_1, \dots, v_r\}$ (all moved to $0$, and $A_{30} = 1$); its old $V_0 \setminus \{u\}$-neighbors contain none of $\{w_1, \dots, w_{r-1}\}$ (stayed in $0$, $A_{30} = 1$); its old $V_3$-neighbors stayed in $3$ ($A_{33} = 1$); self-loops at $u$ become $(3, 3)$ ($A_{33} = 1$).
- At each $v_j \in G_2$ (now in $0$): since $n_4(v_j) = 0$, its old neighbors lay in $V_0 \cup V_2$, whose vertices all lie in $\{0, 2, 3\}$ after the recoloring, and $A_{00} = A_{02} = A_{03} = 1$.
- At each donor $w_\ell \in Z_0$ (now in $2$): since $n_3(w_\ell) = 0$ and $w_\ell \notin N_M(u) \cup \{u\}$, its old neighbors lay in $(V_0 \setminus \{u\}) \cup V_2$, whose vertices all lie in $\{0, 2\}$ after the recoloring, and $A_{20} = A_{22} = 1$.

This contradicts $\Phi$-minimality of $f$ and establishes Case II. $\square$

---

## 3. Exact Bidegree Pairing Law and Closed-Form Vertex-Convex Dual

For any map $f : V \to \mathbb{Z}_5$, write $v_{9,i} := |f^{-1}(i) \cap V^{(9)}|$ and $v_{10,i} := |f^{-1}(i) \cap V^{(10)}|$, with $v_i = v_{9,i} + v_{10,i}$, $a_{9,i} := v_{9,i} / n$, $a_{10,i} := v_{10,i} / n$, and $a_i = a_{9,i} + a_{10,i}$. Part $i$ has $S_i := 9 v_{9,i} + 10 v_{10,i} = D \tilde{s}_i$ stubs, where $\tilde{s}_i := \frac{9 a_{9,i} + 10 a_{10,i}}{\bar{d}}$ and $\sum_{i=0}^4 \tilde{s}_i = 1$.

By the multinomial theorem $1 = \bigl(\sum_{i=0}^4 (a_{9,i}/\alpha_9)\bigr)^{n_9} \ge \binom{n_9}{v_{9,0},\dots,v_{9,4}} \prod_{i=0}^4 (a_{9,i}/\alpha_9)^{v_{9,i}}$ and its degree-$10$ counterpart, the number of maps with bidegree profile $(v_9, v_{10})$ satisfies
$$\binom{n_9}{v_{9,0},\dots,v_{9,4}} \binom{n_{10}}{v_{10,0},\dots,v_{10,4}} \le \exp\!\left(n\left[\alpha_9 \log \alpha_9 + \theta \log \theta - \sum_{i=0}^4 a_{9,i}\log a_{9,i} - \sum_{i=0}^4 a_{10,i}\log a_{10,i}\right]\right).$$

Let $K = (K_{ij})_{0 \le i, j \le 4}$ be any symmetric nonnegative integer matrix supported on blue pairs ($K_{ij} = 0$ whenever $A_{ij} = 0$) with row sums $\sum_{j=0}^4 K_{ij} = S_i$ and even diagonal entries $K_{ii}$. Conditional on $f$, partitioning each part's $S_i$ labelled stubs into destination pools of sizes $(K_{i0}, \dots, K_{i4})$, matching each internal pool in $(K_{ii} - 1)!! = \frac{K_{ii}!}{2^{K_{ii}/2}(K_{ii}/2)!}$ ways, matching each inter-part pair in $K_{ij}!$ ways, and dividing by $(D - 1)!! = \frac{D!}{2^{D/2}(D/2)!}$ gives the exact probability
$$p_K := \Pr(K \mid f) = \frac{2^{D/2}(D/2)!}{D!} \frac{\prod_{i=0}^4 S_i!}{\prod_{i=0}^4 2^{K_{ii}/2}(K_{ii}/2)! \prod_{0 \le i < j \le 4} K_{ij}!}.$$
Because the number of pairing completions is identical for every destination assignment of type $K$, conditional on $(f, K)$ the five row destination assignments are **independent uniform multinomial permutations** of their respective $S_i$ stubs, and each inter-part bijection is uniform and independent of those row assignments.

For every integer $m \ge 0$ (using $0^0 = 1$), concavity of $\log x$ gives $\bigl(\frac{m}{e}\bigr)^m \le m! \le e\sqrt{m + 1}\bigl(\frac{m}{e}\bigr)^m$. Applying the upper bound to $(D/2)!$ and $S_0!, \dots, S_4!$ (each $\le D$) and the lower bound to all denominator factorials, all powers of $2$, $e$, and $D$ cancel identically, while $e^6 \sqrt{D/2 + 1} \prod_{i=0}^4 \sqrt{S_i + 1} < 3^6 (D + 1)^3$. Putting $Q_{ij} := K_{ij} / D$ yields
$$\binom{n_9}{v_{9,\cdot}} \binom{n_{10}}{v_{10,\cdot}} p_K \le 3^6 (D + 1)^3 \exp\!\big(n\, L_{\mathrm{bideg}}(a_9, a_{10}, Q)\big),$$
where
$$L_{\mathrm{bideg}}(a_9, a_{10}, Q) := \alpha_9 \log \alpha_9 + \theta \log \theta - \sum_{i=0}^4 \big(a_{9,i}\log a_{9,i} + a_{10,i}\log a_{10,i}\big) + \bar{d}\sum_{i=0}^4 \tilde{s}_i\log \tilde{s}_i - \frac{\bar{d}}{2}\sum_{i,j=0}^4 Q_{ij}\log Q_{ij}.$$

**Lemma 3 (Closed-form vertex-convex bidegree dual and binary-KL tail).** *Fix any positive tilt vector $t = (t_0, \dots, t_4) \in (0, \infty)^5$, any multiplier $\eta \in \mathbb{R}$, and edge weights $s_{03} \ge 1$, $s_{02} \ge 1$. Put $S_{03} = S_{30} = s_{03}$, $S_{02} = S_{20} = s_{02}$, and $S_{ij} = 1$ on all other blue pairs; let $Z := \sum_{i,j=0}^4 A_{ij} t_i t_j S_{ij} > 0$ and $B_{ij} := A_{ij} t_i t_j S_{ij} / Z$.*
1. *For every valid $(a_9, a_{10}, Q)$ with $a_9 + a_{10} = a$, $\sum_{i=0}^4 a_{9,i} = \alpha_9$, and $\sum_{j=0}^4 Q_{ij} = \tilde{s}_i$,*
   $$L_{\mathrm{bideg}}(a_9, a_{10}, Q) \le U_{t, \mathbf{s}, \eta}(a) - \bar{d}(\log s_{03})\, Q_{03} - \bar{d}(\log s_{02})\, Q_{02} - \frac{\bar{d}}{2} D_{\mathrm{KL}}(Q \Vert B),$$
   *where*
   $$U_{t, \mathbf{s}, \eta}(a) := \alpha_9 \log \alpha_9 + \theta \log \theta + \frac{\bar{d}}{2} \log Z - \eta \alpha_9 + \sum_{i=0}^4 F_i(a_i),$$
   *with $F_i(0) := 0$ and, for $a_i > 0$, setting $\kappa_i := \frac{\bar{d} t_i e^{\eta - 1}}{a_i} > 0$, $r_i := \sqrt{(8 + \kappa_i)^2 + 36}$, $y_i^* := \frac{18}{(8 + \kappa_i) + r_i} \in (0, 1)$, and $\xi_i^* := \frac{2 \kappa_i}{(10 + \kappa_i) + r_i} \in (0, 1)$,*
   $$F_i(a_i) := a_i \Big[9 \log a_i - 10 \log(\bar{d} t_i) + 10 \log(9 + y_i^*) - \log y_i^* + \xi_i^*\Big].$$
2. *For fixed $(t, \mathbf{s}, \eta, \alpha_9)$, each $F_i$ is convex on $[0, \infty)$, so $a \mapsto U_{t, \mathbf{s}, \eta}(a)$ (plus any linear function of $a$) attains its maximum on any compact convex polytope $P \subseteq \Delta_4$ at an extreme point of $P$.*
3. *When $s_{03} = s_{02} = 1$, for any off-diagonal blue pair $\{i, j\}$ and any cutoff $h_{ij} > B_{ij}$ with $2 h_{ij} \le 1$, every $Q$ satisfying $Q_{ij} > h_{ij}$ satisfies $D_{\mathrm{KL}}(Q \Vert B) \ge \mathcal{D}(2 h_{ij}, 2 B_{ij})$, where $\mathcal{D}(x, b) := x \log(x/b) + (1 - x)\log((1 - x)/(1 - b))$.*

*Proof.* Expanding $-\frac{\bar{d}}{2}\sum_{i,j} Q_{ij} \log B_{ij} = -\bar{d}\sum_i \tilde{s}_i \log t_i + \frac{\bar{d}}{2}\log Z - \bar{d}(\log s_{03})Q_{03} - \bar{d}(\log s_{02})Q_{02}$ and adding $\eta\bigl(\sum_{i=0}^4 a_{9,i} - \alpha_9\bigr) = 0$ yields
$$L_{\mathrm{bideg}}(a_9, a_{10}, Q) = \alpha_9\log\alpha_9 + \theta\log\theta + \frac{\bar{d}}{2}\log Z - \eta\alpha_9 + \sum_{i=0}^4 \psi_i(a_i, a_{9,i}) - \bar{d}(\log s_{03})Q_{03} - \bar{d}(\log s_{02})Q_{02} - \frac{\bar{d}}{2}D_{\mathrm{KL}}(Q \Vert B),$$
where $\psi_i(a_i, x) := (10 a_i - x)\log\frac{10 a_i - x}{\bar{d} t_i} - x\log x - (a_i - x)\log(a_i - x) + \eta x$ for $0 \le x \le a_i$. For $a_i = 0$, $x = 0$ gives $\psi_i(0, 0) = 0 = F_i(0)$. For $a_i > 0$, $\psi_i(a_i, \cdot)$ is continuous on $[0, a_i]$ and strictly concave on $(0, a_i)$ since $\frac{\partial^2 \psi_i}{\partial x^2} = \frac{1}{10 a_i - x} - \frac{1}{x} - \frac{1}{a_i - x} < 0$, with $\frac{\partial \psi_i}{\partial x} \to +\infty$ as $x \downarrow 0^+$ and $\to -\infty$ as $x \uparrow a_i^-$. Its unique maximizer $x^* = a_i \xi_i^* \in (0, a_i)$ solves
$$0 = \frac{\partial \psi_i}{\partial x}(a_i, a_i \xi_i^*) = -\log\frac{a_i(10 - \xi_i^*)}{\bar{d} t_i} - 1 - \log \xi_i^* + \log(1 - \xi_i^*) + \eta \iff \frac{\xi_i^*(10 - \xi_i^*)}{1 - \xi_i^*} = \kappa_i.$$
With $y_i^* = 1 - \xi_i^* \in (0, 1)$, this is $(1 - y_i^*)(9 + y_i^*) = \kappa_i y_i^*$, i.e., $(y_i^*)^2 + (8 + \kappa_i)y_i^* - 9 = 0$ and $(\xi_i^*)^2 - (10 + \kappa_i)\xi_i^* + \kappa_i = 0$. Since $(10 + \kappa_i)^2 - 4\kappa_i = \kappa_i^2 + 16\kappa_i + 100 = (8 + \kappa_i)^2 + 36 = r_i^2$, rationalizing numerators gives the stated subtraction-free expressions for $y_i^*$ and $\xi_i^* = 1 - y_i^*$, and $10 - \xi_i^* = 9 + y_i^*$. Multiplying the stationarity identity $-\log\frac{a_i(10-\xi_i^*)}{\bar{d}t_i} - \log \xi_i^* + \log y_i^* + \eta = 1$ by $\xi_i^*$ and substituting into $\psi_i(a_i, a_i\xi_i^*)$ gives $F_i(a_i)$ identically, proving (1).

For (2), parameterizing $x = a_i \xi$ with $\xi \in [0, 1]$ gives
$$\psi_i(a_i, a_i\xi) = (9 - \xi)\, a_i \log a_i + a_i \left[(10 - \xi)\log\frac{10 - \xi}{\bar{d} t_i} - \xi\log\xi - (1 - \xi)\log(1 - \xi) + \eta\xi\right].$$
For every fixed $\xi \in [0, 1]$, $9 - \xi \ge 8 > 0$, so $a_i \mapsto \psi_i(a_i, a_i\xi)$ is convex on $[0, \infty)$. Thus $F_i(a_i) = \sup_{\xi \in [0, 1]} \psi_i(a_i, a_i\xi)$ is convex on $[0, \infty)$.

For (3), coarse-graining the blue entries into $\{(i, j), (j, i)\}$ (mass $2 Q_{ij}$ under $Q$ and $2 B_{ij} \in (0, 1)$ under $B$) and its complement gives $D_{\mathrm{KL}}(Q \Vert B) \ge \mathcal{D}(2 Q_{ij}, 2 B_{ij})$ by the log-sum inequality, and $\frac{\partial}{\partial x}\mathcal{D}(x, b) = \log\frac{x(1 - b)}{b(1 - x)} > 0$ for all $x \in (b, 1)$. $\square$

---

## 4. Case I Bound via Conditional Row Independence and 1D Concavity

Put $f_{10}(x) := 1 - (1 - x)^{10}$ for $x \in [0, 1]$. For $x \in (0, 1)$, writing $q = 1 - x \in (0, 1)$,
$$\frac{d}{dx}\log f_{10}(x) = \frac{10 q^9}{1 - q^{10}} > 0, \qquad \frac{d^2}{dx^2}\log f_{10}(x) = -\frac{10 q^8 (9 + q^{10})}{(1 - q^{10})^2} < 0.$$
Hence $\log f_{10}$ is strictly increasing and strictly concave on $(0, 1)$ (continuous at $x = 1$ where $\log f_{10}(1) = 0$). Consequently, for any reference point $u \in (0, 1)$, setting
$$\beta(u) := \frac{10(1 - u)^9}{1 - (1 - u)^{10}} > 0, \qquad \gamma(u) := \log\big(1 - (1 - u)^{10}\big) - \beta(u) u < 0,$$
concavity yields $\log f_{10}(x) \le \gamma(u) + \beta(u) x$ for every $x \in (0, 1]$.

**Lemma 4 (Case I certificate inequality).** *Let $n \ge 254$, fix $(v_9, v_{10})$ in Region C, and fix an admissible blue matrix $K$. Let $\mathcal{E}_{\mathrm{I}}$ be the event that $n_2(u) \ge 1$ for all $u \in V_0$, $n_0(v) \ge 1$ for all $v \in V_2$, and $|Z_0| \le 19$.*
1. *Put $p_3 := K_{03} / S_0$, $p_2 := K_{02} / S_0$, and $q_2 := K_{02} / S_2$ (with $\Pr(\mathcal{E}_{\mathrm{I}} \mid K) = 0$ if $K_{03} < v_0 - 19$ or $K_{02} < \max(v_0, v_2)$). Whenever $\Pr(\mathcal{E}_{\mathrm{I}} \mid K) > 0$,*
   $$\Pr(\mathcal{E}_{\mathrm{I}} \mid K) \le 27 (D + 1)^3 n^{19} 200^{19} \exp\!\Big(n\big[a_0 \log f_{10}(p_3) + a_0 \log f_{10}(p_2) + a_2 \log f_{10}(q_2)\big]\Big).$$
2. *On any profile box $B = \prod_{i=0}^4 [\underline{a}_i, \overline{a}_i]$ with $\underline{a}_0, \underline{a}_2 > 0$ and $\alpha_9 \in [\underline{\alpha}_9, \overline{\alpha}_9]$, define for $i \in \{0, 2\}$:*
   $$\rho_i := \begin{cases} \frac{1}{9} & \text{if } \underline{a}_i \le \overline{\alpha}_9, \\ \frac{\underline{a}_i}{10 \underline{a}_i - \overline{\alpha}_9} & \text{if } \underline{a}_i > \overline{\alpha}_9. \end{cases}$$
   *Then $\frac{a_i}{S_i / n} \le \rho_i$ for every feasible $(a_9, a_{10})$ in $B$. Consequently, for any $u_1, u_2, u_3 \in (0, 1)$, setting $s_{03} := \exp(\rho_0 \beta(u_1)) > 1$ and $s_{02} := \exp(\rho_0 \beta(u_2) + \rho_2 \beta(u_3)) > 1$, every valid $(a_9, a_{10}, K)$ with $a \in B$ satisfies*
   $$L_{\mathrm{bideg}}(a_9, a_{10}, Q) + a_0 \log f_{10}(p_3) + a_0 \log f_{10}(p_2) + a_2 \log f_{10}(q_2) \le U_{t, \mathbf{s}, \eta}(a) + a_0\big(\gamma(u_1) + \gamma(u_2)\big) + a_2 \gamma(u_3).$$

*Proof.* In Region C, $v_0 \ge \frac{3}{20}n \ge 38$. The event $|Z_0| \le 19$ holds if and only if some subset $W \subseteq V_0$ of exact size $|W| = 19$ satisfies $n_3(u) \ge 1$ for all $u \in V_0 \setminus W$. Thus $\Pr(\mathcal{E}_{\mathrm{I}} \mid K) > 0$ requires $K_{03} \ge v_0 - 19 \ge v_0 / 2$ and $K_{02} \ge v_0$; since $S_0 \le 10 v_0$, this forces $p_3 \ge \frac{1}{20}$ and $p_2 \ge \frac{1}{10}$.

Conditional on $(f, K)$, Row $0$ and Row $2$ stub destination assignments are independent. In Row $0$, put $p_0 := K_{00} / S_0 = 1 - p_2 - p_3$. Under i.i.d. $\mathrm{Multinomial}(S_0;\, p_0, p_2, p_3)$ destination labels on the $S_0$ stubs of $V_0$, Stirling's bounds give
$$\Pr_{\mathrm{Mult}}(K_{00}, K_{02}, K_{03}) = \frac{S_0!}{K_{00}!\, K_{02}!\, K_{03}!} p_0^{K_{00}} p_2^{K_{02}} p_3^{K_{03}} \ge \frac{1}{e^3 \sqrt{(K_{00}+1)(K_{02}+1)(K_{03}+1)}} > \frac{1}{27 (D + 1)^2}.$$
Conditioning on $(K_{00}, K_{02}, K_{03})$ recovers the uniform row-$0$ permutation law, while under the unconditioned i.i.d. law the vertex stub blocks are independent. For a vertex $u \in V_0 \setminus W$ of degree $d \in \{9, 10\}$, since $0 \le 1 - p_3 - p_2 \le 1 - p_3 - p_2 + p_3 p_2 = (1 - p_3)(1 - p_2)$ and $1 - (1 - x)^9 \le 1 - (1 - x)^{10}$,
$$\Pr_{\mathrm{Mult}}(n_3(u) \ge 1 \text{ and } n_2(u) \ge 1) = 1 - (1 - p_3)^d - (1 - p_2)^d + (1 - p_3 - p_2)^d \le \big(1 - (1 - p_3)^d\big)\big(1 - (1 - p_2)^d\big) \le f_{10}(p_3)\, f_{10}(p_2).$$
Because $f_{10}(x) \ge x$, $p_3 \ge \frac{1}{20}$ and $p_2 \ge \frac{1}{10}$ give $\big(f_{10}(p_3) f_{10}(p_2)\big)^{-19} \le 200^{19}$. Union-bounding over $\binom{v_0}{19} \le n^{19}$ choices of $W$ yields $\Pr(\mathcal{E}_{\mathrm{I},\text{row }0} \mid K) \le 27(D + 1)^2 n^{19} 200^{19} \big(f_{10}(p_3) f_{10}(p_2)\big)^{v_0}$.

Independently in Row $2$, under i.i.d. $\mathrm{Bernoulli}(q_2)$ selection of the $S_2$ stubs ($q_2 = K_{02} / S_2$), $K_{02}$ is a mode of $\mathrm{Binomial}(S_2, q_2)$ with probability $\ge \frac{1}{S_2 + 1} \ge \frac{1}{D + 1}$, and each $v \in V_2$ of degree $d \in \{9, 10\}$ is hit with probability $1 - (1 - q_2)^d \le f_{10}(q_2)$, giving $\Pr(\forall v \in V_2,\ n_0(v) \ge 1 \mid K) \le (D + 1) f_{10}(q_2)^{v_2}$. Multiplying the Row-$0$ and Row-$2$ bounds proves (1).

For (2), since $a_{9,i} \le \min(a_i, \alpha_9) \le \min(a_i, \overline{\alpha}_9)$, we have $S_i / n = 10 a_i - a_{9,i} \ge \max(9 a_i,\, 10 a_i - \overline{\alpha}_9)$. Thus $\frac{a_i}{S_i / n} \le \frac{1}{9}$ always, and when $a_i \ge \underline{a}_i > \overline{\alpha}_9$, differentiating $\frac{d}{da_i}\bigl(\frac{a_i}{10 a_i - \overline{\alpha}_9}\bigr) = \frac{-\overline{\alpha}_9}{(10 a_i - \overline{\alpha}_9)^2} < 0$ gives $\frac{a_i}{S_i / n} \le \frac{\underline{a}_i}{10 \underline{a}_i - \overline{\alpha}_9} = \rho_i$. Applying $\log f_{10}(x) \le \gamma(u_m) + \beta(u_m) x$ to $p_3 = \frac{1}{S_0/n} \bar{d} Q_{03}$, $p_2 = \frac{1}{S_0/n} \bar{d} Q_{02}$, and $q_2 = \frac{1}{S_2/n} \bar{d} Q_{02}$, using $\frac{a_i}{S_i/n} \le \rho_i$, $\beta(u_m) > 0$, $Q_{ij} \ge 0$, and $D_{\mathrm{KL}}(Q \Vert B) \ge 0$ in Lemma 3(1), the $\bar{d} Q_{03}$ and $\bar{d} Q_{02}$ terms are nonpositive and drop out, yielding (2). $\square$

---

## 5. Case II Bound via Exact Row-2 Hot-Stub Polynomial $M_{10}$ and $8 \times 8$ KL Subdivision

For $q_0, q_4 \in [0, 1]$ and $w \ge 1$, define the polynomial
$$M_d(q_0, q_4;\, w) := \big(1 + (w - 1) q_0\big)^d - \big(1 - q_4 + (w - 1) q_0\big)^d + (1 - q_4)^d - (1 - q_0)^d.$$
Note that for all $q_0, q_4 \in [0, 1]$ and $w \ge 1$,
$$\frac{\partial M_d}{\partial q_0} = d(w - 1)\Big[\big(1 + (w - 1)q_0\big)^{d - 1} - \big(1 - q_4 + (w - 1)q_0\big)^{d - 1}\Big] + d(1 - q_0)^{d - 1} \ge 0,$$
$$\frac{\partial M_d}{\partial q_4} = d\Big[\big(1 - q_4 + (w - 1)q_0\big)^{d - 1} - (1 - q_4)^{d - 1}\Big] \ge 0,$$
so $M_d(\cdot, \cdot;\, w)$ is nondecreasing in both $q_0$ and $q_4$ on the entire square $[0, 1]^2$.

**Lemma 5 (Case II certificate inequality).** *Fix $(v_9, v_{10})$ in Region C and an admissible blue matrix $K$. Mark a destination-$0$ stub at $v \in V_2$ **hot** if $n_4(v) \ge 1$, let $R \in \{0, \dots, K_{02}\}$ be the total number of hot stubs in $V_2$, and let $\mathcal{E}_{\mathrm{II}}(K, R)$ be the event that $n_0(v) \ge 1$ for all $v \in V_2$, $R$ takes the given value, and every $u \in V_0$ receives at least one hot stub.*
1. *Put $q_0 := K_{02} / S_2$ and $q_4 := K_{24} / S_2$. For any $u \in (0, 1)$ and $\rho_0$ as in Lemma 4(2), setting $w := \exp(\beta(u) \rho_0) > 1$,*
   $$\sum_{R=0}^{K_{02}} \Pr(\mathcal{E}_{\mathrm{II}}(K, R) \mid K) \le 27 (D + 1)^3 \exp\!\Big(n\big[a_0 \gamma(u) + a_2 \log M_{10}(q_0, q_4;\, w)\big]\Big).$$
2. *On a profile box $B = \prod_{i=0}^4 [\underline{a}_i, \overline{a}_i]$ with $\underline{a}_0, \underline{a}_2 > 0$ and $U_{t, \mathbf{1}, \eta}(a) \le U$, put $s_{2,\min} := \max(9 \underline{a}_2,\, 10 \underline{a}_2 - \overline{\alpha}_9) > 0$. Fix cutoffs $h_{02}, h_{24} > 0$:*
   - *Whenever $Q_{02} > h_{02}$ or $Q_{24} > h_{24}$, that tail is empty if $h_{ij} \ge q_{ij,\mathrm{cap}} := \frac{\min(s_{i,\max}, s_{j,\max})}{\underline{d}_{\min}}$ (with $s_{k,\max} := \min(10 \overline{a}_k,\, 9 \overline{a}_k + \overline{\theta})$ and $\underline{d}_{\min} := 10 - \overline{\alpha}_9$), and otherwise satisfies $L_{\mathrm{bideg}}(a_9, a_{10}, Q) \le U - \frac{\underline{d}_{\min}}{2} \mathcal{D}(2 h_{ij}, 2 B_{ij})$ provided $h_{ij} > B_{ij}$.*
   - *Partition $[0, h_{02}] \times [0, h_{24}]$ into the $64$ subrectangles $[\frac{i}{8}h_{02}, \frac{i+1}{8}h_{02}] \times [\frac{j}{8}h_{24}, \frac{j+1}{8}h_{24}]$ ($0 \le i, j \le 7$). On subrectangle $(i, j)$, put $\bar{q}_{0,i} := \min\bigl(1, \frac{\overline{d}_{\max}(i+1)h_{02}}{8 s_{2,\min}}\bigr)$ and $\bar{q}_{4,j} := \min\bigl(1, \frac{\overline{d}_{\max}(j+1)h_{24}}{8 s_{2,\min}}\bigr)$, and let $\Delta_{02,i}$ equal $\mathcal{D}(\frac{2i}{8}h_{02}, 2B_{02})$ if $\frac{i}{8}h_{02} > B_{02}$, $\mathcal{D}(\frac{2(i+1)}{8}h_{02}, 2B_{02})$ if $\frac{i+1}{8}h_{02} < B_{02}$, and $0$ otherwise (defining $\Delta_{24,j}$ analogously vs $B_{24}$). Then every $(a_9, a_{10}, K)$ in subrectangle $(i, j)$ satisfies*
     $$L_{\mathrm{bideg}}(a_9, a_{10}, Q) + a_0 \gamma(u) + a_2 \log M_{10}(q_0, q_4;\, w) \le U - \frac{\underline{d}_{\min}}{2}\max(\Delta_{02,i},\, \Delta_{24,j}) + \underline{a}_0 \gamma(u) + \max_{a_2 \in [\underline{a}_2, \overline{a}_2]} a_2 \log M_{10}(\bar{q}_{0,i}, \bar{q}_{4,j};\, w).$$

*Proof.* Conditional on $(f, K)$ and any fixed Row-$2$ destination arrangement having $R$ hot stubs (and $n_0(v) \ge 1$ for all $v \in V_2$), the uniform $(0, 2)$ bijection and independent uniform Row-$0$ destination permutation send those $R$ hot stubs to a uniform $R$-subset of all $S_0$ stubs of $V_0$. For $R = 0$, $\Pr = 0$; for $R \ge 1$, the binomial-mode bound on $\mathrm{Binomial}(S_0, R/S_0)$ gives $\Pr(\forall u \in V_0,\, n_{\mathrm{hot}}(u) \ge 1 \mid K, \text{Row } 2) \le (D + 1) f_{10}(R / S_0)^{v_0} \le (D + 1) \exp(n a_0 \gamma(u)) w^R$.

Summing over $R = 0, \dots, K_{02}$ reduces to bounding $\mathbb{E}\bigl[w^R \mathbf{1}_{\{\forall v \in V_2,\, n_0(v) \ge 1\}} \mid K\bigr]$ over the uniform Row-$2$ multinomial permutation of $(K_{20}, K_{22}, K_{24})$ stubs ($K_{20} = K_{02}$, $S_2 = K_{20} + K_{22} + K_{24}$). Put $q_2 := K_{22} / S_2 = 1 - q_0 - q_4$. Under i.i.d. $\mathrm{Multinomial}(S_2;\, q_0, q_2, q_4)$ labels across the $S_2$ stubs of $V_2$, Stirling's inequality gives $\Pr_{\mathrm{Mult}}(K_{20}, K_{22}, K_{24}) > \frac{1}{27(D + 1)^2}$, and conditioning on $(K_{20}, K_{22}, K_{24})$ recovers the exact uniform Row-$2$ law. Under the unconditioned i.i.d. law, vertex stub blocks are independent, and for a single vertex $v \in V_2$ of degree $d \in \{9, 10\}$, splitting into $n_4(v) = 0$ vs $n_4(v) \ge 1$ yields
$$\begin{aligned}
\mathbb{E}_{\mathrm{Mult}(d; q)}\big[w^{n_0 \mathbf{1}_{\{n_4 \ge 1\}}} \mathbf{1}_{\{n_0 \ge 1\}}\big]
&= \big[(q_0 + q_2)^d - q_2^d\big] + \big[(w q_0 + q_2 + q_4)^d - (w q_0 + q_2)^d - (q_2 + q_4)^d + q_2^d\big] \\
&= M_d(q_0, q_4;\, w).
\end{aligned}$$
Coupling a degree-$9$ block with the first $9$ stubs of a degree-$10$ block, since $(n_0, n_4) \mapsto w^{n_0 \mathbf{1}_{\{n_4 \ge 1\}}} \mathbf{1}_{\{n_0 \ge 1\}}$ is nondecreasing in $(n_0, n_4)$ for $w \ge 1$, we have $M_9(q_0, q_4;\, w) \le M_{10}(q_0, q_4;\, w)$. Multiplying across all $v_2$ vertices of $V_2$ proves (1).

For (2), on subrectangle $(i, j)$ we have $q_0 = \frac{\bar{d} Q_{02}}{S_2 / n} \le \bar{q}_{0,i}$ and $q_4 = \frac{\bar{d} Q_{24}}{S_2 / n} \le \bar{q}_{4,j}$, so $M_{10}(q_0, q_4;\, w) \le M_{10}(\bar{q}_{0,i}, \bar{q}_{4,j};\, w)$ by coordinatewise nondecrease of $M_{10}$ on $[0, 1]^2$; meanwhile $D_{\mathrm{KL}}(Q \Vert B) \ge \max\bigl(\mathcal{D}(2 Q_{02}, 2 B_{02}),\, \mathcal{D}(2 Q_{24}, 2 B_{24})\bigr) \ge \max(\Delta_{02,i},\, \Delta_{24,j})$ by Lemma 3(3) and unimodality of $x \mapsto \mathcal{D}(x, b)$ around $b$, and $a_0 \gamma(u) \le \underline{a}_0 \gamma(u)$ since $\gamma(u) < 0$. $\square$

---

## 6. Certified Cover, Connectivity, and Finite Threshold $n_0 = 450{,}000$

### 6.1 Certified Rate Upper Bound $\le -3/2000$
The three archives in `certificates/` (`cert_naive_ab.json.gz`, `cert_case1.json.gz`, `cert_case2.json.gz`) partition the exact rational box $[0, 4001/10000]^5$ by strictly interior dyadic coordinate splits. On each leaf, interval propagation of $\sum_{i=0}^4 a_i = 1$ and the defining linear inequalities of Region A, Region B, or Region C yields a tightened box whose slice by $\sum_{i=0}^4 a_i = 1$ contains every feasible profile in that leaf. Because a sliced box has at most one coordinate strictly interior at any extreme point, enumerating all points on $\sum_{i=0}^4 a_i = 1$ with at least four endpoint coordinates captures all extreme points of the convex slice. The standalone verifier [verify_arb.py](producer/verify_arb.py) evaluates Lemmas 3, 4, and 5 in 180-bit outward-rounded Arb interval arithmetic over the exact ball enclosing $\alpha_9 \in [\frac{1}{10}, \frac{450{,}019}{4{,}500{,}000}]$, certifying an exponential rate upper bound of $-\frac{3}{2000} = -0.0015$ on every leaf across Regions A and B, Case I, and Case II.

### 6.2 Connectivity of the $(9, 10)$-Bidegree Multigraph
If $M$ is disconnected, some nonempty subset $U \subseteq V$ of size $1 \le k \le \lfloor n / 2 \rfloor$ has zero edges to $V \setminus U$. Let $S_U = \sum_{u \in U} d(u)$ be the total stubs of $U$. Isolation requires $S_U$ to be even; since $d(u) \in \{9, 10\}$, $9k \le S_U \le 10k$, so the number of internal pairing steps is $S_U / 2 \ge \frac{9}{2} k$. Revealing the mates of stubs in $U$ sequentially, after $j$ internal pairs ($0 \le j < S_U / 2$) the next stub pairs inside $U$ with probability $\frac{S_U - 2j - 1}{D - 2j - 1} \le \frac{S_U}{D} \le \frac{10 k}{\bar{d} n}$. Since $\bar{d} \ge \frac{44{,}549{,}981}{4{,}500{,}000} > \frac{49}{5}$, we have $\frac{10 k}{\bar{d} n} \le \frac{50}{49}\frac{k}{n} < 1$ for $k \le n / 2$. Using $\binom{n}{k} \le (e n / k)^k$ and $k / n \le 1 / 2$,
$$\Pr(M \text{ disconnected}) \le \sum_{k=1}^{\lfloor n/2 \rfloor} \left(\frac{e n}{k}\right)^k \left(\frac{50}{49}\frac{k}{n}\right)^{\frac{9}{2} k} \le \sum_{k=1}^{\infty} \rho_{\mathrm{disc}}^k = \frac{\rho_{\mathrm{disc}}}{1 - \rho_{\mathrm{disc}}}, \qquad \rho_{\mathrm{disc}} := e \left(\frac{50}{49}\right)^{9/2} 2^{-7/2}.$$
Verified in 180-bit Arb, $\rho_{\mathrm{disc}} < 0.2633$ and $\frac{\rho_{\mathrm{disc}}}{1 - \rho_{\mathrm{disc}}} < 0.3574 < \frac{1}{2}$ for every $n \ge n_0$.

### 6.3 Complete Finite-$n$ First-Moment Sum
Let $X_{\mathrm{rigid}}$ be the number of valid maps $f$ satisfying the necessary conditions of Lemma 2 in at least one dihedral orientation. Counting all $\le 10$ dihedral orientations, $3$ regional/case terms (A $\cup$ B naive, Region C Case I, Region C Case II), $\binom{n_9+4}{4}\binom{n_{10}+4}{4} \le (n_9 + 1)^4(n_{10} + 1)^4 \le (n + 1)^8$ bidegree profiles $(v_9, v_{10})$, and at most $(D + 1)^5 \le (10n + 1)^5$ symmetric blue matrices $K$ per bidegree profile (determined by the five off-diagonal blue entries in $\{0, \dots, D\}$), with pairing factor $3^6(D + 1)^3 \le 3^6(10n + 1)^3$ and uniform conditional-probability prefactor $\max\bigl(1,\, 27(D+1)^3 n^{19} 200^{19},\, 27(D+1)^3\bigr) \le 3^3(10n + 1)^3 n^{19} 200^{19}$, Lemmas 3-5 and the certified leaf bound $\le -\frac{3}{2000}$ yield
$$\mathbb{E} X_{\mathrm{rigid}} \le B(n) := 30 \cdot 3^9 (n + 1)^8 (10n + 1)^{11}\, n^{19} 200^{19}\, e^{-3n / 2000}.$$
Differentiating $\log B(n)$ for $n \ge 450{,}000$ gives
$$\frac{d}{dn}\log B(n) = \frac{8}{n + 1} + \frac{110}{10n + 1} + \frac{19}{n} - \frac{3}{2000} < \frac{38}{n} - \frac{3}{2000} \le \frac{38}{450{,}000} - \frac{3}{2000} < -0.00141 < 0,$$
so $B(n)$ is strictly decreasing for all $n \ge 450{,}000$. At $n_0 = 450{,}000$, 180-bit Arb evaluation certifies $\log B(450{,}000) < -41$, hence $B(450{,}000) < 2 \times 10^{-18}$, and
$$\Pr(X_{\mathrm{rigid}} > 0) + \Pr(M \text{ disconnected}) \le B(n) + \frac{\rho_{\mathrm{disc}}}{1 - \rho_{\mathrm{disc}}} < 0.3574 < 1 \qquad \forall\, n \ge 450{,}000.$$
All side conditions ($\frac{2}{5} + \frac{3}{5n} \le \frac{4001}{10000}$ and $\frac{3}{20}n \ge 38$) hold for every $n \ge 450{,}000$. By §1, this proves Theorem 1. $\square$
