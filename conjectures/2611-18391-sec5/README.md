# Coste, Csikos, and Viennot (arXiv:2611.18391v1), Section 5 Outerplanar Equitable Coloring Conjecture: Unconditional Proof

Unconditional proof settling the Section 5 conjecture (following Corollary `cor:K-outerplanar`) of Louann Coste, Monika Csikos, and Laurent Viennot, *Color Refinement Distinguishes Connected Rooted Outerplanar Graphs* (`arXiv:2611.18391v1`), audited in clean-room isolation (`VERDICT: HOLDS`) with an exact-integer verifier (`referee/referee_verify.py`).

## Main Theorem

Let $G$ be a finite simple connected outerplanar graph and let $c$ be any equitable coloring of $G$ (without requiring any singleton color class). Then the underlying simple undirected graph $H = \widetilde{K}$ of its color graph $K$ is outerplanar.

More generally, every finite simple graph $H$ admitting a finite outerplanar emulator (a finite outerplanar graph $F$ with a surjective, locally surjective graph homomorphism $p : F \to H$) is outerplanar.

## Proof Outline

1. **Reduction to outerplanar emulators:** Delete all within-color edges of $G$ to obtain an outerplanar subgraph $F$. Double-counting edges between distinct color classes gives $|c^{-1}(i)| K_{ij} = |c^{-1}(j)| K_{ji}$, so $K_{ij} > 0 \iff K_{ji} > 0$ and $c : F \to \widetilde{K}$ is surjective and locally surjective.
2. **Minor closure:** Deleting vertices or edges of $H$ deletes preimages in $F$. Contracting an edge $ab \in E(H)$ contracts each connected component of the induced subgraph $S = F[p^{-1}(a) \cup p^{-1}(b)]$ independently to a single vertex (discarding loops and parallel edges). Local surjectivity ensures every component of $S$ contains both an $a$-vertex and a $b$-vertex, and because $S$ is induced no edge joins distinct components of $S$, producing a finite outerplanar minor $F^{\prime}$ emulating $H / ab$.
3. **Excluding the two forbidden minors $K_4$ and $K_{2,3}$:**
   - $H = K_4$ forces minimum degree at least 3 in $F$, contradicting the fact that every nonempty finite outerplanar graph has a vertex of degree at most 2.
   - $H = K_{2,3}$ forces $F$ to be bipartite (hence triangle-free) with minimum degree at least 2, and every vertex of degree 2 maps to the 3-vertex independent side so no two degree-2 vertices are adjacent. This contradicts the leaf-block outerplanar ear lemma: every nonempty finite triangle-free outerplanar graph of minimum degree at least 2 (including graphs with cut-vertices) has two adjacent vertices of degree 2.

By the Chartrand-Harary forbidden-minor characterization, $H$ is outerplanar.

## Verification and Disclosure

- **Exact-integer audit:** `referee/referee_verify.py` (pure Python integer arithmetic, zero `math`, `float`, or `/` division) cross-checks two independent outerplanarity oracles across all 996 connected simple graphs on $n \le 7$, verifies all 4800 non-isomorphic connected outerplanar graphs on $n \le 9$, all 1030 exhaustive equitable partitions on $n \le 7$ (including 39 with no singleton class), 9120 color-refinement pairs on $n = 8, 9$, 4933 emulator edge contractions (243 with multi-component $S$), all 27 triangle-free outerplanar graphs with minimum degree at least 2 on $n \le 9$, and 4 proof-mutation controls (`M1` through `M4`).
- **Prior art:** Checked on arXiv (`v1`), GitHub, X, and the graph-emulator literature as of 2026-11-26 with no prior proof of this conjecture found.
- **Lean status:** None (elementary minor-theory and block-cut proof audited in clean room and verified in Python).
- **AI disclosure:** Proof constructed by GPT-6.2 Astra (Codex) and audited in strict clean-room isolation (producer code withheld) by Gemini 4 Carbon High (Antigravity CLI), returning `VERDICT: HOLDS`. No human mathematician has reviewed this packet.

## Reproduction

```bash
python3 referee/referee_verify.py
```
