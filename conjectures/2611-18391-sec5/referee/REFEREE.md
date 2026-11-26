Shipped: VERDICT: HOLDS  --  clean-room adversarial referee audit and exact-integer verification confirming that the proof in inputs/PROOF.md of Coste-Csikós-Viennot's (arXiv:2611.18391v1, §5) unrooted outerplanar equitable coloring conjecture is mathematically complete and gap-free.

VERDICT: HOLDS
CONTROLS: No  --  no assumption overrode any control: in `referee_verify.py` (`python3 referee_verify.py`), two independent outerplanarity oracles (direct `{K_4, K_{2,3}}` branch-set minor search vs. Tarjan block decomposition + Hamiltonian polygon noncrossing chords) agreed on 996/996 connected graphs (`n=1..7`); positive controls passed on 1,030/1,030 exhaustive `(G, c)` pairs (`n=1..7`), 9,120/9,120 CR pairs (`n=8..9`), and 27/27 triangle-free `delta>=2` outerplanar graphs (`n=1..9`); negative controls `NC1`-`NC3` rejected `K_4`, `K_{2,3}`, `planar_ctrex` `G_1`, antipodal `Q_3 -> K_4`, diamond, triforce, and `P_3`; and proof-mutation controls `M1`-`M4` failed exactly as predicted when dropping local surjectivity, merging whole fibers (`10`-vertex spider -> `K_{2,3}`), contracting partial matchings (`C_4 -> K_1` loop), or retaining within-color edges (`K_3`).
CONTRADICTING: No  --  zero contradicting cases were dropped or ignored across all 4,800 non-isomorphic connected outerplanar graphs for `n=1..9` (`[1, 1, 2, 5, 13, 46, 172, 777, 3783]`), all 1,030 equitable partitions for `n=1..7` (including 39 unrooted partitions with no singleton class, 282 with within-color loops `K_{ii}>0`, 758 with unequal weights `K_{ij}!=K_{ji}`, 28 with disconnected `F`, and 4,933 edge contractions including 243 multi-component `S` contractions), and all 3 counterexample figures in `inputs/2611.18391v1.tex.json.gz` (`figs/square_kites.tex`, `figs/cactus_ctrex_hor.tex`, `figs/planar_ctrex.tex`).
LABELS: No  --  no paper label, macro, or figure caption was trusted without checking raw LaTeX/TikZ/Rocq definitions in `inputs/2611.18391v1.tex.json.gz`: we verified `\newcommand{\Kt}{\widetilde{K}}` (`main_hal.tex:103`), nonempty color classes (`body/2_preliminaries.tex:15-19` and `partition` in `figs/rocq-check.tex:61`), `K` and `\widetilde{K}` (`body/2_preliminaries.tex:46-60`), outerplanarity (`body/2_preliminaries.tex:80-86` and `figs/rocq-check.tex:34-40`), `cor:K-outerplanar` and the §5 conjecture (`body/5_details.tex:43-48`), and reconstructed the vertex/edge lists directly from raw TikZ `\draw` commands in `figs/square_kites.tex:31-33`, `figs/cactus_ctrex_hor.tex:29-73`, and `figs/planar_ctrex.tex:34-68`.

---

# Clean-Room Adversarial Referee Report: `arXiv:2611.18391v1` §5 Conjecture

## 1. Executive Summary & Novelty Assessment

- **Audited Artifact:** `PROOF.md` (*The unrooted equitable quotient is outerplanar*).
- **Target Problem:** Conjecture in §5 (`body/5_details.tex`, lines 47-48) of Coste, Csikós, and Viennot, *Color Refinement Distinguishes Connected Rooted Outerplanar Graphs* (`arXiv:2611.18391v1`, `2611.18391v1.tex.json.gz`):
  > *Given a connected outerplanar graph $G$ and any equitable coloring $c$ of $G$ (not necessarily with a singleton color class), the underlying simple graph $\widetilde{K}$ of its color graph $K$ is outerplanar.*
- **Referee Verdict:** **`VERDICT: HOLDS`**. The proof in `PROOF.md` is mathematically sound, complete, self-contained modulo elementary preliminaries already stated in §2 of `arXiv:2611.18391v1`, and free of hidden hypothesis mismatches or unhandled edge cases.
- **Did `PROOF.md` settle a stated open problem? Yes:** `inputs/PROOF.md` settles the stated open conjecture in `body/5_details.tex:47-48` of `arXiv:2611.18391v1` (and in fact proves a strictly stronger characterization: *every finite simple graph admitting a finite outerplanar emulator is outerplanar*, which does not even require $G$ to be connected). As an adversarial referee job, **this report itself claims no new theorem**; it ships an independent verification verdict and clean-room exact-integer verifier `referee_verify.py`.
- **Why no statistical holdout / SBS baseline applies:** This task audits a deductive mathematical proof of a universal graph-theoretic theorem. There is no random sample, train/test split, or scalar predictive metric (AUROC/RMSE/etc.). Instead, clean-room verification combines line-by-line logical auditing with an independently written exact-integer verifier (`referee_verify.py`, written without access to any producer code) covering exhaustive small-$n$ instances, paper boundary examples, negative controls, and deliberate proof-step mutations.

---

## 2. Hypothesis & Definition Audit Summary

Full verbatim excerpts and citations are recorded in `PRIOR_ART.md`. Key findings:

1. **Exact Hypothesis Match:**
   - `body/2_preliminaries.tex:5-6` fixes all graphs as *finite, simple, and undirected* unless stated otherwise; `body/5_details.tex:47-48` conjectures that for any equitable coloring $c$ of a connected outerplanar graph $G$, the underlying simple graph $\widetilde{K}$ (`body/2_preliminaries.tex:58-59`: obtained from $K$ by forgetting weights, directions, and loops) is outerplanar.
   - `PROOF.md` proves verbatim: *"Let $G$ be a finite connected simple outerplanar graph with an equitable coloring $c$. The underlying simple graph $H=\widetilde K$ of its color graph is outerplanar."*
2. **Nonempty Color Classes:**
   - By `body/2_preliminaries.tex:16-19`, $c : V(G) \to [|c|]$ uses colors $1, \dots, |c|$ whose color classes $c^{-1}(1), \dots, c^{-1}(|c|)$ are **nonempty** ($w_i = |c^{-1}(i)| \ge 1$).
3. **Minor Expositional Convention Note (Non-blocking):**
   - In `PROOF.md`, *"A finite graph $F$ is an **emulator** of a simple graph $H$..."* relies on the paper's standing convention (`body/2_preliminaries.tex:5-6`) that "graph" means *simple undirected graph* (since a 2-vertex multigraph with 3 parallel edges would violate Lemma 2(i)). `PROOF.md` enforces simplicity explicitly throughout: $F$ in line 7 is a subgraph of simple $G$, and contracted emulators in line 14 explicitly *"discard loops and duplicate edges"*. Making the word *"simple"* explicit before *"graph $F$"* in line 5 is an optional one-word polish, not a logical gap.

---

## 3. Adversarial Line-by-Line Proof Audit

### Step 0: Equitable Coloring $\implies$ Finite Outerplanar Emulator (`PROOF.md`)

- **Construction:** Given finite simple outerplanar $G$ and equitable $c : V(G) \to [|c|]$, define $F = (V(G), \{uv \in E(G) : c(u) \ne c(v)\})$ and $H = \widetilde{K}$.
- **Outerplanarity of $F$:** $F$ is a spanning subgraph of outerplanar $G$ ($E(F) \subseteq E(G)$); outerplanarity is hereditary under edge deletion, even when $F$ becomes disconnected (e.g., $G = K_2$ with $|c|=1 \implies F = \overline{K_2}$).
- **Surjective Homomorphism $c : F \to H$:**
  - *Vertex surjectivity:* Every color class $c^{-1}(i)$ ($i \in [|c|]$) is nonempty (`body/2_preliminaries.tex:17-18`), and $V(F) = V(G)$, so $c(V(F)) = V(H)$.
  - *Homomorphism:* If $uv \in E(F)$, then $uv \in E(G)$ and $i = c(u) \ne c(v) = j$. Thus $v \in N_G(u) \cap c^{-1}(j)$, so $K_{ij} \ge 1 > 0$, hence $(i,j)$ is an arc of $K$ with $i \ne j$, giving $ij \in E(\widetilde{K}) = E(H)$.
- **Symmetric Support & Local Surjectivity:**
  - Suppose $ij \in E(H)$ ($i \ne j$). By definition of $\widetilde{K}$ ("forgetting weights, directions and loops"), either $K_{ij} > 0$ or $K_{ji} > 0$. Double-counting the undirected edges of $G$ between $c^{-1}(i)$ and $c^{-1}(j)$ yields
    $$w_i K_{ij} = \bigl|E_G(c^{-1}(i), c^{-1}(j))\bigr| = w_j K_{ji}.$$
    Since $w_i = |c^{-1}(i)| \ge 1$ and $w_j = |c^{-1}(j)| \ge 1$, $K_{ij} > 0 \iff K_{ji} > 0$.
  - Therefore, for **every** $x \in c^{-1}(i)$ and **every** $j \in N_H(i)$, we have $K_{ij} \ge 1$ (even if $w_i \ne w_j$, $K_{ij} \ne K_{ji}$, or $K_{ij} > 1$). Pick any $y \in N_G(x) \cap c^{-1}(j)$; since $c(x) = i \ne j = c(y)$, the edge $xy$ was **not** deleted when forming $F$, so $y \in N_F(x)$ and $c(y) = j$.
  - *(Note: vertex surjectivity plus local surjectivity automatically implies edge surjectivity onto $E(H)$; and at any color $i$ that is isolated in $H$, e.g. $|c|=1$ or $|V(G)|=1$, $N_H(i) = \emptyset$ makes local surjectivity vacuous.)*
- **Audit Status:** **HOLDS.**

---

### Step 1: Minor Closure of Finite Outerplanar Emulators (`PROOF.md`)

Let $p : F \to H$ be a finite (simple) outerplanar emulator of a finite simple graph $H$. Every minor of $H$ is obtained (up to isomorphism, under which emulators transport by post-composing $p$ with the target isomorphism) by iterating three elementary operations:

1. **Vertex Deletion ($H' = H - v$):**
   - Delete the fiber $p^{-1}(v)$ from $F$ to obtain induced subgraph $F' = F - p^{-1}(v)$, with $p' = p|_{V(F')}$.
   - $F'$ is an induced subgraph of $F$, hence finite, simple, and outerplanar.
   - Surjectivity holds onto $V(H) \setminus \{v\}$. Any edge of $F'$ maps into $V(H) \setminus \{v\}$, hence into $E(H')$. For $x \in V(F')$ and $j \in N_{H'}(p(x))$, $j \ne v$ and $j \in N_H(p(x))$, so local surjectivity in $F$ gives $y \in N_F(x)$ with $p(y) = j \ne v$; then $y \in V(F')$ and $xy \in E(F')$.
2. **Edge Deletion ($H' = H \setminus ab$):**
   - Delete $\{xy \in E(F) : \{p(x), p(y)\} = \{a, b\}\}$ from $E(F)$, keeping $V(F') = V(F)$ and $p' = p$.
   - $F'$ is a spanning subgraph of $F$, hence finite, simple, and outerplanar.
   - Surjectivity is unchanged; edges mapping to $ab$ are gone so $p'$ is a homomorphism to $H'$; for $x \in V(F')$ and $j \in N_{H'}(p(x))$, $\{p(x), j\} \ne \{a, b\}$, so the witness $y \in N_F(x)$ with $p(y) = j$ satisfies $\{p(x), p(y)\} \ne \{a, b\}$, hence $xy \in E(F')$.
3. **Edge Contraction ($H' = H / ab$ for $ab \in E(H)$, merging $a, b$ into $z$ and simplifying):**
   - Let $U = p^{-1}(a) \cup p^{-1}(b)$ and let $S = F[U]$ be the subgraph of $F$ **induced** by $U$.
   - **Both colors in every component of $S$:** Since $p$ is surjective, $p^{-1}(a) \ne \emptyset$ and $p^{-1}(b) \ne \emptyset$, so $S$ has $k \ge 1$ connected components $C_1, \dots, C_k$. For any $x \in p^{-1}(a)$, $b \in N_H(a)$ so local surjectivity gives $y \in N_F(x)$ with $p(y) = b \in U$; since $S = F[U]$ is induced, $xy \in E(S)$, placing $y$ in the same component of $S$ as $x$. Symmetrically every $y \in p^{-1}(b)$ has a neighbor in $p^{-1}(a)$ in $S$. Thus **every** component $C_r$ ($1 \le r \le k$) contains both an $a$-representative $u_a \in V(C_r) \cap p^{-1}(a)$ and a $b$-representative $u_b \in V(C_r) \cap p^{-1}(b)$.
   - **Valid minor $F'$ of $F$:** The sets $V(C_1), \dots, V(C_k)$ and $\{w\}$ ($w \in V(F) \setminus U$) are pairwise disjoint nonempty connected vertex subsets of $F$. Contracting a spanning tree of each $C_r$ and discarding loops and parallel edges produces a simple minor $F'$ of $F$ with vertices $\{v_{C_1}, \dots, v_{C_k}\} \dot\cup (V(F) \setminus U)$. Since outerplanar graphs are minor-closed, $F'$ is finite, simple, and outerplanar. *(As Mutation Control `M2` in `referee_verify.py` demonstrates on a 10-vertex tree, merging all of $U$ into a single vertex instead of contracting components independently would NOT be a minor and can create $K_{2,3}$!)*
   - **Homomorphism $p' : F' \to H'$ (crucial zero-loop check at $z$):** Define $p'(v_{C_r}) = z$ and $p'(w) = p(w)$ for $w \in V(F) \setminus U$. Could $F'$ contain an edge $v_{C_r} v_{C_s}$ ($r \ne s$), which $p'$ would map to a loop $zz \notin E(H')$? **No:** an edge $v_{C_r} v_{C_s} \in E(F')$ requires an edge $xy \in E(F)$ with $x \in V(C_r) \subseteq U$ and $y \in V(C_s) \subseteq U$. Because $S = F[U]$ is the **induced** subgraph on $U$, any such $xy$ lies in $E(S)$, forcing $C_r = C_s$! *(Mutation Control `M3` verifies that contracting non-maximal subgraphs of $S$ fails here.)* Self-loops at $v_{C_r}$ were discarded. Every remaining edge of $F'$ either joins $w_1, w_2 \in V(F) \setminus U$ (mapping to $p(w_1)p(w_2) \in E(H')$) or joins $v_{C_r}$ to $w \in V(F) \setminus U$ via some $u \in V(C_r)$ with $uw \in E(F)$, so $p(u) \in \{a, b\}$, $p(w) \notin \{a, b\}$, and $p(u)p(w) \in E(H) \implies z p(w) \in E(H')$.
   - **Surjectivity & local surjectivity of $p'$:**
     - Since $k \ge 1$, $v_{C_1}$ maps to $z$, and outside fibers are untouched, so $p'$ is surjective.
     - At $v_{C_r}$ ($p'(v_{C_r}) = z$): if $c \in N_{H'}(z)$, then $c \notin \{a, b\}$ and either $ac \in E(H)$ or $bc \in E(H)$. Using $u_a \in V(C_r) \cap p^{-1}(a)$ (if $ac \in E(H)$) or $u_b \in V(C_r) \cap p^{-1}(b)$ (if $bc \in E(H)$), local surjectivity of $p$ supplies $w \in V(F) \setminus U$ adjacent in $F$ to $V(C_r)$ with $p(w) = c$, hence $v_{C_r} w \in E(F')$ (deduplicating parallel edges preserves adjacency) and $p'(w) = c$.
     - At $w \in V(F) \setminus U$: for $j \in N_{H'}(p(w)) \setminus \{z\}$, the witness in $p^{-1}(j) \subseteq V(F) \setminus U$ persists; for $j = z \in N_{H'}(p(w))$, either $p(w)a \in E(H)$ or $p(w)b \in E(H)$, so $w$ had a neighbor $u \in U$ in $F$, which belongs to some component $C_r$ of $S$, giving $w v_{C_r} \in E(F')$ with $p'(v_{C_r}) = z$.
- **Audit Status:** **HOLDS.**

---

### Step 2: Two Outerplane Ear Lemmas (`PROOF.md`)

- **Statements:** For every nonempty finite simple outerplanar graph $G_0$:
  - **(i)** $G_0$ has a vertex of degree $\le 2$.
  - **(ii)** If $G_0$ is **triangle-free** and $\delta(G_0) \ge 2$, then $G_0$ has an edge whose endpoints both have degree $2$.
- **Component & Block-Cut Tree Reduction:**
  - Pick a connected component $C$ of $G_0$ (degrees and triangles in $C$ match those in $G_0$). If $\delta(C) \le 1$, (i) holds immediately and the hypothesis $\delta(G_0) \ge 2$ of (ii) is not active.
  - Otherwise $\delta(C) \ge 2$ (hence $|V(C)| \ge 3$). If $C$ is 2-connected, let $B = C$ (no external attachments). If $C$ has cut-vertices, its block-cut tree $T_C$ (`body/2_preliminaries.tex:92-95`) has $\ge 2$ leaves, and every leaf of $T_C$ is a block node (every cut-vertex belongs to $\ge 2$ blocks). Let $B$ be a leaf block of $T_C$, with unique cut-vertex $s$ of $C$.
  - No vertex of $V(B) \setminus \{s\}$ is incident to edges outside $B$ (any external edge lies in another block $B' \ne B$, making its endpoint in $B$ a cut-vertex, hence $s$).
  - Could $B$ be a bridge ($K_2$)? No: its endpoint in $V(B) \setminus \{s\}$ would have degree $1$ in $C$ and $G_0$, contradicting $\delta(C) \ge 2$. Thus $B$ is a **2-connected outerplanar graph** ($|V(B)| = k \ge 3$) with at most one vertex $s$ incident to edges outside $B$.
- **Outer Polygon $O$ and Chord Cases:**
  - Embed $B$ as its unique Hamiltonian outer-face polygon $O = (v_0, \dots, v_{k-1})$ with noncrossing interior chords (`body/2_preliminaries.tex:82-85`).
  - **Case A (0 chords, $B \cong C_k$):** Every $v \in V(B) \setminus \{s\}$ has $\deg_{G_0}(v) = \deg_B(v) = 2$. Since $k \ge 3$, $k - 1 \ge 2$ vertices prove (i). If $G_0$ is triangle-free, $k \ge 4$, so $O - s$ contains a path of $k - 1 \ge 3$ vertices (or all $k \ge 4$ vertices if there is no $s$), which has at least two consecutive vertices avoiding $s$; both have degree $2$ in $G_0$, proving (ii).
  - **Case B ($c \ge 1$ chords):**
    - *Weak dual is a tree $T_c$ with $\ge 2$ leaves:* Starting from the single bounded region of $O$ ($T_0 \cong K_1$), inserting each noncrossing chord splits one bounded polygonal region along two non-adjacent boundary vertices into two joined regions and partitions the prior boundary chords between them, replacing one tree vertex by two joined vertices. By induction on $c \ge 1$, $T_c$ is a tree on $c + 1 \ge 2$ bounded faces, hence has $\ge 2$ leaf faces.
    - *Structure of a leaf face $f$:* Having degree $1$ in $T_c$, $\partial f$ consists of exactly one chord $xy \in E(B) \setminus E(O)$ and one boundary path $P_f = (x = u_0, u_1, \dots, u_m = y)$ along $O$. Because $B$ is **simple** and $xy \notin E(O)$, $m \ge 2$, so $\mathrm{int}(P_f) = \{u_1, \dots, u_{m-1}\}$ is nonempty ($m - 1 \ge 1$). In the triangle-free case, the cycle $\partial f$ has length $m + 1 \ge 4$, so $m \ge 3$ and $\mathrm{int}(P_f)$ has $m - 1 \ge 2$ **consecutive** vertices $u_1, u_2$ along $O$.
    - *Degree $2$ in $B$:* Any chord incident to $u_r \in \mathrm{int}(P_f)$ would enter the disk strictly between the two outer-face edges $u_{r-1}u_r$ and $u_r u_{r+1}$, separating them into distinct bounded faces; since both lie on $\partial f$, no chord touches $u_r$, so $\deg_B(u_r) = 2$.
    - *Disjoint interiors across distinct leaf faces (including $c = 1$):* Every outer-face edge $e \in E(O)$ borders the unbounded outer face on one side and **uniquely one** bounded face on its interior side. For $u \in \mathrm{int}(P_f)$, both incident edges of $O$ border $f$ alone, so $\mathrm{int}(P_{f_1}) \cap \mathrm{int}(P_{f_2}) = \emptyset$ whenever $f_1 \ne f_2$ (even when $c = 1$ and the two leaf faces share their single chord $xy$, in which case their paths are the two opposite arcs of $O$ between $x$ and $y$).
    - *Avoiding $s$ (including when $s \in \{x, y\}$):* Since $\mathrm{int}(P_{f_1}) \cap \mathrm{int}(P_{f_2}) = \emptyset$ for two leaves $f_1 \ne f_2$ and $s$ is at most a single vertex (note that if $s$ is a chord endpoint, $s \notin \mathrm{int}(P_f)$ already!), at least one leaf face $f$ satisfies $s \notin \mathrm{int}(P_f)$. Its interior supplies one vertex of degree $2$ in $G_0$ for (i), and two adjacent vertices $u_1 u_2 \in E(G_0)$ of degree $2$ in $G_0$ for (ii).
- **Audit Status:** **HOLDS.**

---

### Step 3: Excluding $K_4$ and $K_{2,3}$ & Forbidden-Minor Conclusion (`PROOF.md`)

- **$K_4$ has no finite outerplanar emulator:** If $p : F \to K_4$ is an emulator, surjectivity onto $|V(K_4)| = 4$ ensures $F$ is nonempty. Every $x \in V(F)$ requires neighbors in the $3$ distinct target colors $V(K_4) \setminus \{p(x)\}$; since $p$ is single-valued, those $3$ neighbors in $N_F(x)$ are pairwise distinct, forcing $\delta(F) \ge 3$, contradicting Lemma 2(i).
- **$K_{2,3}$ has no finite outerplanar emulator:** Let $(A, B)$ be the bipartition of $K_{2,3}$ with $|A| = 2, |B| = 3$. If $p : F \to K_{2,3}$ is an emulator, $F$ is nonempty ($|V(F)| \ge 5$) and every edge of $F$ maps to an edge between $A$ and $B$, so $(p^{-1}(A), p^{-1}(B))$ is a bipartition of $F$; hence $F$ is **triangle-free**. Local surjectivity forces $\deg_F(x) \ge |B| = 3$ for $x \in p^{-1}(A)$ and $\deg_F(y) \ge |A| = 2$ for $y \in p^{-1}(B)$, so $\delta(F) \ge 2$. By Lemma 2(ii), $F$ has an edge $uv \in E(F)$ with $\deg_F(u) = \deg_F(v) = 2$; by bipartiteness, one of $u, v$ lies in $p^{-1}(A)$, contradicting $\deg_F \ge 3$ on $p^{-1}(A)$.
- **Completion:** By Chartrand-Harary (`body/2_preliminaries.tex:80-82`), any non-outerplanar finite simple graph $H$ has $K_4$ or $K_{2,3}$ as a minor. By Step 1, if $H$ had a finite outerplanar emulator, that minor would also have one, contradicting the exclusions above. Hence $H = \widetilde{K}$ is outerplanar.
- **Audit Status:** **HOLDS.**

---

## 4. Clean-Room Exact-Integer Verification (`referee_verify.py`)

### 4.1 Reproduction Command & Resource Footprint
```bash
/usr/bin/time -l python3 referee_verify.py
```
- **Purity Compliance:** Pure Python exact integers only; AST, `tokenize`, and raw-string verified to contain **zero** `import math`, **zero** `from __future__`, **zero** `float`, and **zero** `/` division (`//` only).
- **Runtime & Peak RSS:** `47.37 s` wall time, `20,987,904` bytes (`~20.0 MB`) peak RSS (1.0% of the 2 GB ceiling).

### 4.2 Summary of Verification Suites & Controls

| Check / Control Suite | Scope & Exact Counts | Outcome |
| :--- | :--- | :--- |
| **Dual Outerplanarity Oracles** | Cross-checked direct `{K_4, K_{2,3}}` branch-set minor search vs. Tarjan block + Hamiltonian polygon noncrossing chords across all **996** connected simple graphs for $n=1..7$ (`[1, 1, 2, 6, 21, 112, 853]`) and all **4,800** connected outerplanar graphs for $n=1..9$ (`[1, 1, 2, 5, 13, 46, 172, 777, 3783]`, matching OEIS A007027) | **PASS** (0 disagreements) |
| **Equitable Generator Audit** | Cross-checked CR-refinement partition enumerator against raw `Bell(n)` partition enumeration on all **22** connected outerplanar graphs for $n=1..5$ | **PASS** (exact set equality) |
| **Exhaustive Positive Controls ($n=1..7$)** | **1,030** `(G, c)` pairs (all connected outerplanar $G$ and **all** equitable colorings $c$): **39** unrooted (no singleton class), **282** with loops $K_{ii}>0$, **758** with asymmetric $K_{ij} \ne K_{ji}$, **28** with disconnected $F$; **4,933** Step-1 edge contractions (**243** with $\ge 2$ components in $S$) and **5,956** vertex/edge deletions | **PASS** (100% $\widetilde{K}$ outerplanar & locally surjective) |
| **CR Positive Controls ($n=8..9$)** | **9,120** `(G, c)` CR partitions (uniform + 1-rooted across all `777 + 3,783` connected outerplanar graphs, including **62** unrooted partitions) | **PASS** (100% $\widetilde{K}$ outerplanar) |
| **Section 2 Ear Lemmas ($n=1..9$)** | Lemma 2(i) on all **4,800** connected outerplanar graphs; Lemma 2(ii) on all **27** connected triangle-free $\delta \ge 2$ outerplanar graphs (including **9** with cut-vertices) | **PASS** (27/27 have adjacent deg-2 pair) |
| **Paper TikZ Reproductions** | `square_kites` ($n=10$, 2-connected unrooted), `cactus_ctrex_hor` ($n=12$, cut-vertex unrooted), `planar_ctrex` ($n=7$, $G_0$ outerplanar vs $G_1$ treewidth-2 $K_{2,3}$-minor) | **PASS** |
| **Negative Controls (`NC1`-`NC3`)** | `NC1`: $K_4, K_{2,3}$ rejected by both oracles; `NC2`: planar $3$-cube $Q_3$ colored by antipodal pairs yields non-outerplanar $\widetilde{K} = K_4$ (planarity insufficient); `NC3`: diamond ($n=4$), triforce ($n=6$), and $P_3$ ($n=3$) lack adjacent degree-2 pairs when triangle-freeness or $\delta \ge 2$ is dropped | **PASS** (all rejected as expected) |
| **Proof Mutations (`M1`-`M4`)** | `M1`: dropping local surjectivity admits a 7-vertex tree mapping onto all 6 edges of $K_4$; `M2`: merging all of $p^{-1}(a)\cup p^{-1}(b)$ on a 10-vertex spider creates $K_{2,3}$; `M3`: contracting partial matchings on $C_4$ creates a loop edge over $K_1$; `M4`: keeping within-color edges on $K_3$ violates homomorphism | **PASS** (all mutations caught) |

---

## 5. Sources, Limitations, and Next Steps

### Sources Inspected (Strictly Local Clean-Room Inputs)
- `2611.18391v1.tex.json.gz`  --  Louann Coste, Mónika Csikós, and Laurent Viennot, *Color Refinement Distinguishes Connected Rooted Outerplanar Graphs* (`arXiv:2611.18391v1`, November 2026), specifically `main_hal.tex`, `body/1_intro.tex`, `body/2_preliminaries.tex`, `body/2b_structure.tex`, `body/5_details.tex`, `body/6_non-connected.tex`, `body/A_setting_toolkit_bis.tex`, `body/B_dichotomy_new.tex`, `body/C_Block_Structure_bis.tex`, `figs/rocq-check.tex`, `figs/square_kites.tex`, `figs/cactus_ctrex_hor.tex`, and `figs/planar_ctrex.tex`.
- `PROOF.md`  --  Candidate proof under audit.

### Limitations
1. **Finite-horizon computational checks vs. deductive proof:** Computational checks in `referee_verify.py` are exhaustive over all equitable partitions up to $n = 7$ and all connected outerplanar graphs up to $n = 9$ (plus $n = 10, 12$ paper examples); validity for general finite $n$ rests on the deductive line-by-line mathematical audit in §3, not on finite enumeration alone.
2. **Not machine-checked in a formal theorem prover:** Unlike the paper's Dichotomy Lemma (`figs/rocq-check.tex`), `PROOF.md` is a human-readable mathematical proof rather than a Rocq/Lean kernel term.

### Concrete Next Steps
1. **Optional one-word exposition polish in `PROOF.md` line 5:** Write *"A finite **simple** graph $F$ is an **emulator** of a simple graph $H$..."* so line 5 states simplicity directly rather than inheriting it from the paper's §2 standing convention.
2. **Rocq / MathComp formalization:** Because `figs/rocq-check.tex` already imports `GraphTheory.sgraph`, `minor`, and `excluded` (`K4_free /\ K23_free`), Steps 0-3 of `PROOF.md` (~35 lines of prose) are an ideal target for a short Rocq 9.1.1 formalization on top of the authors' existing `Spec.Outerplanar` setup.
