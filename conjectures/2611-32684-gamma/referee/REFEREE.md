Shipped: VERDICT: HOLDS  --  clean-room referee certification (`referee_verify.py` + hand proof audit) that the 11-vertex, 20-edge 3-connected non-bipartite simple graph $G$ in `inputs/witness.json` satisfies $\gamma(G) = -1 < 0$, disproving the Discussion conjecture of Supkar & Yaddanapudi (`arXiv:2611.32684v1`).

VERDICT: HOLDS
- `CONTROLS:` No  --  all 6 positive controls ($K_3$: $\gamma=1$; $K_4$: $\kappa=3, \gamma=1$; Octahedron $K_{2,2,2}$: $\kappa=4, \gamma=2$; paper's triangular-grid hexagons $T_1, T_2, T_3$ from `main.tex` lines 364-374: $\kappa=3$ and $\gamma=1, 4, 16$), 1 negative control ($\Theta(2,2,3)$: $\gamma=-1$, rejected by $\kappa=2 < 3$ at 2-cut `(0,1)`), and 5 deliberate mutation controls (`M1a` deleting `(2,4)` and `M1b` deleting `(1,3)`: $\gamma=-2$, rejected by $\kappa=2 < 3$; `M2a` deleting both matching edges: rejected as bipartite with $\chi(2)=2, \kappa=1$; `M2b` rewiring matching edges to `(1,8),(2,9)`: $\kappa=3$ preserved, rejected solely by non-bipartiteness check with $\chi(2)=2$; `M3` flipping the sign of $\gamma$: caught because $K_4$ gives $\gamma_{\text{flipped}}=-1 \neq +1$) were executed via `nice -n 10 python3 referee_verify.py` (`referee_verify.py`) and matched every gate without assumption override.
- `CONTRADICTING:` No  --  all $\binom{11}{2} = 55$ two-vertex deletions of $G$, all $20$ edges in `witness.json`, all $9$ equality-pattern pairs $(r,s) \in \{1,2,3\}^2$ in `PROOF.md`, all $12$ coefficients of $\chi_G(q)$ across 4 independent exact calculations (`referee_verify.py`: deletion-contraction, independent-set falling-factorial DP, Whitney NBC forest enumeration, and closed-form polynomial) plus brute-force $k$-coloring counts at $k=0..4$ (`[0, 0, 0, 150, 20760]`), and all 406 lines of `main.tex` in `2611.32684v1.tex.json.gz` were audited with zero dropped or contradicting cases.
- `LABELS:` No  --  vertex labels and claims in `PROOF.md` ($x,a,b,c,d,u_1..u_3,v_1..v_3 \leftrightarrow 0..10$) were verified edge-for-edge against raw integer pairs in `witness.json` (`referee_verify.py`, `L800-L802`), odd cycles `[1, 5, 0, 8, 3]` and `[0, 5, 1, 3, 8]` were checked directly against `E(G)` (`referee_verify.py`, `L810-L813`), and verbatim definitions of $\chi_G(q)$, $\gamma(G) := \frac{1}{2}(-1)^{n-1}\chi'_G(2)$, and the unrestricted Discussion conjecture were verified directly against `main.tex` lines 62, 64, 68, 186, 281, 294, and 377-385 (`PRIOR_ART.md`).

---

## 1. Executive Summary, Novelty & Exact-Certificate Scope

- **Audited result:** The 11-vertex, 20-edge graph $G$ specified in `witness.json` and analyzed in `PROOF.md` is a finite, simple, undirected, 3-connected ($\kappa(G) = 3$), non-bipartite ($\chi(G) = 3$) graph with exact chromatic derivative $\chi'_G(2) = -2$ and invariant
  $$\gamma(G) = \frac{1}{2}(-1)^{11-1}\chi'_G(2) = -1 < 0.$$
  It cleanly and rigorously disproves the Discussion conjecture of Aatman Supkar and Upamanyu Yaddanapudi (*Schnyder woods and the chromatic polynomial*, `arXiv:2611.32684v1`, Section 5, `main.tex` line 384: *"However, it seems that $\gamma(G)$ is non-negative for $3$-connected non-bipartite graphs, and the authors have verified this conjecture computationally for $|G| \le 9$. It would be interesting to see a proof or disproof of this..."*).
- **Did we find something new? (Rule 3):** **Yes** with respect to the mathematical claim under audit  --  `inputs/witness.json` settles an explicitly stated open conjecture in `arXiv:2611.32684v1` (beating the $|G| \le 9$ computational horizon where $\gamma(G) \ge 0$ always holds). **No** new counterexample beyond the submitted 11-vertex witness was generated in this referee job, whose authorized scope is independent clean-room verification.
- **Why no statistical holdout or predictive baseline (`SBS`) applies:** This is a deterministic exact algebraic and combinatorial certificate on a single 11-vertex finite graph over $\mathbb{Z}[q]$. There is no statistical sample, stochastic training split, predictive score, or numerical approximation error; uncertainty is identically zero, and verification is established by hand proof plus an independently written pure-integer verifier (`referee_verify.py`) backed by positive, negative, and mutation controls.
- **Development checkpoints & diagnostic catches logged honestly:** During clean-room implementation of `referee_verify.py`, two diagnostic assertions fired and were resolved before final run: (i) an initial hand mental estimate for $\chi_G(3)$ omitted the $(r,s)=(2,2)$ contribution $9 \cdot 6 = 54$ ($150$ actual vs $96$ mental estimate, immediately caught because both `chrom_poly_*` and `count_proper_k_colorings_bruteforce` agreed on `150`), and (ii) running `compute_gamma_standard` on the bipartite mutant `M2a` (`G` minus both matching edges) yielded odd $\chi'_{M2a}(2) = 9$, empirically confirming `main.tex` line 68's observation that integrality of $\gamma(G)$ depends on $G$ being non-bipartite.

---

## 2. Source & Conjecture Scope Audit Summary

Full verbatim extracts and line references are documented in `PRIOR_ART.md`. Key findings:
1. **Standing convention (`main.tex`, line 62):** *"Let $G$ be a simple undirected graph on $n$ vertices."*
2. **Exact normalization (`main.tex`, line 68 & lines 379, 384):** $\gamma(G) := \frac{1}{2}(-1)^{n-1}\chi'_G(2) = f_2(G)$ where $f_k(G) := (-1)^{|G|+k+1}\chi'_G(k)/k!$.
3. **Zero hidden planarity or triangulation restrictions (`main.tex`, lines 377-385):** Whenever planarity or triangulation is required in Sections 1, 3, and 4, `main.tex` explicitly specifies *"plane graph"* or *"plane triangulation $T$"* (lines 62, 68, 170, 186, 281, 332). In Section 5 (`Discussion`), the authors already note Theorem 3.1 settles plane triangulations ($\gamma(T) \ge 1$) and explicitly pose the conjecture for general **"$3$-connected non-bipartite graphs"**, citing general-graph literature (`\cite{zbMATH06053893}`, `\cite{zbMATH07500699}`) and crediting `Nauty` (`\cite{zbMATH06264238}`, line 398) for their $|G| \le 9$ general-graph check. Thus non-planarity of $G$ (which contains $K_{3,3}$) violates zero hypotheses of the conjecture.

---

## 3. Hand-Proof & Witness Audit (`inputs/PROOF.md` & `inputs/witness.json`)

### 3.1 Exact Graph Construction ($n = 11, m = 20$)
Mapping `(x, a, b, c, d, u_1, u_2, u_3, v_1, v_2, v_3) = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)` (`PROOF.md`) against `witness.json`:
- **Left $K_{3,3}$** on $\{0, 1, 2\} \times \{5, 6, 7\}$: all $9$ edges `[0,5],[0,6],[0,7],[1,5],[1,6],[1,7],[2,5],[2,6],[2,7]` are present.
- **Right $K_{3,3}$** on $\{0, 3, 4\} \times \{8, 9, 10\}$: all $9$ edges `[0,8],[0,9],[0,10],[3,8],[3,9],[3,10],[4,8],[4,9],[4,10]` are present.
- **Matching edges** $ac = [1, 3]$ and $bd = [2, 4]$: both present.
- **Simplicity:** $9 + 9 + 2 = 20$ strictly ordered pairs $0 \le u < v \le 10$, zero self-loops, zero parallel edges. Degree sequence: $\deg(0) = 6$, $\deg(1..4) = 4$, $\deg(5..10) = 3$ ($\sum \deg = 40 = 2m$).

### 3.2 Exhaustive Hand Verification of Exact Connectivity $\kappa(G) = 3$
Let $L = \{0,1,2,5,6,7\}$ and $R = \{0,3,4,8,9,10\}$ with $L \cap R = \{0\}$. In $K_{3,3}$, removing $\le 2$ vertices never empties either shore of size $3$, so $K_{3,3} \setminus S$ is connected whenever $|S| \le 2$. Partition all $\binom{11}{2} = 55$ two-vertex subsets $W \subseteq V(G)$:
1. **$0 \notin W$ ($\binom{10}{2} = 45$ pairs):** Write $W = W_L \sqcup W_R$ with $W_L \subseteq L \setminus \{0\}, W_R \subseteq R \setminus \{0\}$ and $|W_L| + |W_R| = 2$ ($10$ pairs $(2,0)$, $10$ pairs $(0,2)$, $25$ pairs $(1,1)$). Both $G[L \setminus W_L]$ and $G[R \setminus W_R]$ are induced subgraphs of $K_{3,3}$ missing $\le 2$ vertices, hence both are connected and share vertex $0$; their union (a spanning subgraph of $G \setminus W$) is connected.
2. **$0 \in W$, so $W = \{0, z\}$ ($10$ pairs):** Deleting $0$ leaves $L' = G[L \setminus \{0\}] \cong K_{2,3}$ and $R' = G[R \setminus \{0\}] \cong K_{2,3}$ joined by disjoint edges $\{1,3\}$ and $\{2,4\}$.
   - **$z \in \{1, 2\}$ ($2$ pairs):** Deleting $1$ (symmetrically $2$) leaves $L' \setminus \{1\} \cong K_{1,3}$ (connected, centered at $2$), $R' \cong K_{2,3}$ (connected), and surviving edge $\{2, 4\}$ connecting them.
   - **$z \in \{3, 4\}$ ($2$ pairs):** Symmetric to above; deleting $3$ (or $4$) leaves $L' \cong K_{2,3}$ and $R' \setminus \{z\} \cong K_{1,3}$ joined by $\{2, 4\}$ (or $\{1, 3\}$).
   - **$z \in \{5, 6, 7\}$ ($3$ pairs):** $L' \setminus \{z\} \cong K_{2,2} \cong C_4$ (connected) and $R' \cong K_{2,3}$ (connected) remain joined by both $\{1,3\}$ and $\{2,4\}$.
   - **$z \in \{8, 9, 10\}$ ($3$ pairs):** Symmetric; $L' \cong K_{2,3}$ and $R' \setminus \{z\} \cong K_{2,2}$ remain joined by $\{1,3\}$ and $\{2,4\}$.
All $45 + 10 = 55$ two-vertex deletions leave $G \setminus W$ connected, so $\kappa(G) \ge 3$. Deleting the 3-vertex set $\{0, 1, 2\} = \{x, a, b\}$ removes $N(5) = N(6) = N(7) = \{0, 1, 2\}$, splitting $G \setminus \{0,1,2\}$ into $4$ components $\{5\}, \{6\}, \{7\}, \{3,4,8,9,10\}$; hence $\kappa(G) = 3$.

### 3.3 Non-Bipartiteness & Chromatic Number
The 5-vertex sequence $(0, 5, 1, 3, 8) = (x, u_1, a, c, v_1)$ uses edges $\{0,5\}, \{1,5\}, \{1,3\}, \{3,8\}, \{0,8\} \in E(G)$, forming an induced $C_5$. Thus $G$ is non-bipartite ($\chi_G(2) = 0$). Setting $\sigma(0)=\sigma(1)=\sigma(2)=1$, $\sigma(3)=\sigma(4)=2$, $\sigma(5..10)=3$ is a valid 3-coloring, so $\chi(G) = 3$.

### 3.4 Closed-Form $\chi_G(q)$, Derivative $\chi'_G(2) = -2$, and $\gamma(G) = -1$
In $H = G[\{x,a,b,c,d\}]$, the **only** edges are $ac$ and $bd$, while $u_1,u_2,u_3$ each have neighborhood $\{x,a,b\}$ and $v_1,v_2,v_3$ each have neighborhood $\{x,c,d\}$. For any proper $q$-coloring $\sigma$ of $H$ with $r = |\{\sigma(x),\sigma(a),\sigma(b)\}|$ and $s = |\{\sigma(x),\sigma(c),\sigma(d)\}|$, there are $(q-r)^3(q-s)^3$ proper extensions to $\{u_1,u_2,u_3,v_1,v_2,v_3\}$.
- **Verification of `PROOF.md` shortcut at $q = 2$ (`PROOF.md`):** Every equality pattern on $\{x,a,b,c,d\}$ using $t$ distinct colors contributes $(q)_t (q-r)^3 (q-s)^3$. Whenever $r = 2$ or $s = 2$, $(q-r)^3(q-s)^3$ already contains $(q-2)^3$ (order $\ge 3$ at $q=2$), so its first derivative at $q = 2$ is identically $0$. For $(r,s) = (1,1)$, $x=a=b=c=d$ violates $a \neq c$. Only $(1,3)$, $(3,1)$, and $(3,3)$ contribute to $\chi'_G(2)$:
  - $(1,3)$ and $(3,1)$: $(q)_3 (q-1)^3 (q-3)^3$ each ($2$ cases).
  - $(3,3)$: $(q)_3$ ways for distinct $(x,a,b)$; then $c \notin \{\sigma(x),\sigma(a)\}$ ($q-2$ choices) and $d \notin \{\sigma(x),\sigma(b)\}$ ($q-2$ choices), minus $c = d \notin \{\sigma(x),\sigma(a),\sigma(b)\}$ ($q-3$ choices), giving $(q)_3 ((q-2)^2 - (q-3)) (q-3)^6$.
  Since $\left.\frac{d}{dq}(q)_3\right|_{q=2} = 2$,
  $$\chi'_G(2) = 2\Big[2(1)^3(-1)^3 + (0^2 - (-1))(-1)^6\Big] = 2(-2 + 1) = -2, \qquad \gamma(G) = \frac{1}{2}(-1)^{11-1}(-2) = -1.$$
- **Complete 9-case hand expansion of $Q(q) = \chi_G(q) / (q)_3$:** Including $(1,2)$ and $(2,1)$ ($2(q)_2(q-1)^3(q-2)^3$), $(2,2)$ ($q(q-1)(7q-12)(q-2)^6$), and $(2,3),(3,2)$ ($2(q)_3(3q-7)(q-2)^3(q-3)^3$) yields
  $$Q(q) = 2(q-1)^3(q-2)^2 + 2(q-1)^3(q-3)^3 + (7q-12)(q-2)^5 + 2(3q-7)(q-2)^3(q-3)^3 + (q^2-5q+7)(q-3)^6$$
  $$= q^8 - 17q^7 + 137q^6 - 677q^5 + 2228q^4 - 4969q^3 + 7284q^2 - 6363q + 2509,$$
  and $\chi_G(q) = q^{11} - 20q^{10} + 190q^9 - 1122q^8 + 4533q^7 - 13007q^6 + 26647q^5 - 38153q^4 + 36166q^3 - 20253q^2 + 5018q$, matching `PROOF.md` line 38 identically, with $Q(1) = 133$ and $Q(2) = -1$.

### 3.5 Exact Rational Evaluations & Sturm Real-Root Count in $(1, 2)$
- **Exact rational sign change across $(19/10, 39/20)$:**
  $$Q\!\left(\frac{19}{10}\right) = +\frac{3694111}{100000000} > 0, \qquad Q\!\left(\frac{39}{20}\right) = -\frac{14608211579}{25600000000} < 0,$$
  $$\chi_G\!\left(\frac{19}{10}\right) = -\frac{631692981}{100000000000} < 0, \qquad \chi_G\!\left(\frac{39}{20}\right) = +\frac{10824684780039}{204800000000000} > 0.$$
- **Möbius / Descartes & Exact Sturm Sequences:**
  - $(1+t)^8 Q((1+2t)/(1+t)) = 133 + 600t + 1177t^2 + 1284t^3 + 828t^4 + 304t^5 + 51t^6 - t^7 - t^8$ has exactly $1$ sign variation on $t \in (0, \infty)$.
  - Positive-multiplier integer Sturm sequence on $Q(q)$ terminates at degree $0$ (length $9$, proving $Q$ is square-free) with sign-variation counts $(V_Q(1), V_Q(19/10), V_Q(39/20), V_Q(2)) = (5, 5, 4, 4)$, proving **exactly $5 - 4 = 1$ real root** (simple, multiplicity $1$) in $[1, 2]$, strictly inside $(19/10, 39/20)$.
  - Direct Sturm sequence on $\chi_G(q)$ terminates at degree $0$ (length $12$, square-free) with $(V_\chi(1^+), V_\chi(19/10), V_\chi(39/20), V_\chi(2^-), V_\chi(2)) = (6, 6, 5, 5, 4)$, independently confirming $6 - 5 = 1$ root in the open interval $(1, 2)$ (inside $(19/10, 39/20)$) and $6 - 4 = 2$ roots in $(1, 2]$ (adding the simple root at $q = 2$).

---

## 4. Clean-Room Verifier (`referee_verify.py`) & Controls Summary

`referee_verify.py` (977 lines, importing only `json`, `os`, `sys`) uses pure Python arbitrary-precision integers and floor division `//` exclusively (verified by AST, `tokenize`, and raw lexical audits: zero `import math`, zero `from __future__`, zero floating-point literals/calls, zero `/` characters). Every test graph's $\chi(q)$ is computed by both **Algorithm A** (memoized deletion-contraction) and **Algorithm B** (independent-set partition falling-factorial DP), with witness $G$ additionally verified by **Algorithm C** (Whitney's Broken-Circuit theorem) and brute-force $k$-coloring backtracking for $k = 0..4$ (`[0, 0, 0, 150, 20760]`).

| Graph / Control | $n$ | $m$ | $\kappa$ | Non-bipartite? | $\chi(2)$ | $\chi'(2)$ | $\gamma$ | Gate Result |
|---|---:|---:|---:|---|---:|---:|---:|---|
| **Witness $G$ (`witness.json`)** | 11 | 20 | **3** | **Yes** (`[0,5,1,3,8]`) | 0 | $-2$ | **$-1$** | **VALID COUNTEREXAMPLE** |
| Positive: $K_3$ | 3 | 3 | 2 | Yes (`[0,1,2]`) | 0 | $+2$ | $+1$ | Non-negative $\gamma = 1$ |
| Positive: $K_4$ | 4 | 6 | 3 | Yes | 0 | $-2$ | $+1$ | Non-negative $\gamma = 1$ |
| Positive: Octahedron $K_{2,2,2}$ | 6 | 12 | 4 | Yes | 0 | $-4$ | $+2$ | Non-negative $\gamma = 2$ |
| Positive: Paper $T_1, T_2, T_3$ | 10, 14, 18 | 19, 29, 39 | 3 | Yes | 0 | $-2, -8, -32$ | $+1, +4, +16$ | Matches $2^{2(k-1)}$ (`main.tex` Fig. 4) |
| Negative: $\Theta(2,2,3)$ | 6 | 7 | **2** | Yes (`5`-cycle) | 0 | $+2$ | $-1$ | **Rejected** ($\kappa = 2 < 3$, cut `(0,1)`) |
| Mutant `M1a` / `M1b` (del 1 match edge) | 11 | 19 | **2** | Yes | 0 | $-4$ | $-2$ | **Rejected** ($\kappa = 2 < 3$) |
| Mutant `M2a` (del both match edges) | 11 | 18 | 1 | **No** (bipartite) | 2 | $+9$ | non-int | **Rejected** (bipartite, $\chi(2)=2$) |
| Mutant `M2b` (rewire `(1,8),(2,9)`) | 11 | 20 | 3 | **No** (bipartite) | 2 |  --  |  --  | **Rejected** solely by non-bipartite gate |
| Mutant `M3` (flip sign of $\gamma$ on $K_4$) | 4 | 6 | 3 | Yes | 0 | $-2$ | $-1$ (mut) | **Caught** ($\gamma_{\text{mut}}(K_4) = -1 \neq +1$) |

---

## 5. Reproduction Commands, Resource Footprint & Next Steps

### Exact Reproduction Command
```sh
/usr/bin/time -l nice -n 10 python3 referee_verify.py
```
- **Verified runtime & resource bounds:** `0.60 s` wall (`0.58 s` user, `0.01 s` sys), single-threaded (`1 <= 4` threads), Peak RSS `34,308,096` bytes ($\approx 32.7\text{ MiB} \ll 2\text{ GB}$ limit), `0` lingering background processes (`pgrep -f csweep_gamma_ref | wc -l`).

### Sources, Limitations & Next Steps
- **Permitted sources used:** `2611.32684v1.tex.json.gz`, `PROOF.md`, and `witness.json`.
- **Limitations & next steps:**
  1. **Order minimality ($|G| = 10$):** Supkar & Yaddanapudi verified $\gamma(G) \ge 0$ up to $|G| \le 9$, while this counterexample has $|G| = 11$. An exhaustive `geng -C` scan of 3-connected non-bipartite graphs at $n = 10$ would settle whether $n = 11$ is the minimum order with $\gamma(G) < 0$.
  2. **Planar 3-connected restriction:** Because $G$ contains $K_{3,3}$, $G$ is non-planar. Testing whether $\gamma(G) \ge 0$ holds when restricted to **planar** 3-connected non-bipartite graphs (extending Theorems 3.1 and 4.3 of `arXiv:2611.32684v1`) is the natural narrowed conjecture.
