# The unrooted equitable quotient is outerplanar

**Theorem.** Let $G$ be a finite connected simple outerplanar graph with an equitable coloring $c$. The underlying simple graph $H=\widetilde K$ of its color graph is outerplanar.

We prove a stronger statement. A finite graph $F$ is an **emulator** of a simple graph $H$ if it admits a surjective graph homomorphism $p:F\to H$ such that, for every $x\in V(F)$ and every neighbor $j$ of $p(x)$, some neighbor of $x$ maps to $j$. Call this last property *local surjectivity*. Every finite simple graph with a finite outerplanar emulator is outerplanar.

To apply that statement, delete from $G$ just the edges with equal-colored ends and call the result $F$. It is outerplanar. Every edge of $F$ maps to an edge of $H$. If $ij\in E(H)$, then $K_{ij}>0$, so **every** vertex of color $i$ has a neighbor of color $j$. Thus $c:F\to H$ is an emulator. The argument allows $F$ to become disconnected. In particular it allows unequal fiber sizes, more than one neighbor of a required color, and arbitrary within-color edges in the original graph.

## 1. Taking a minor of the target

If $H$ has a finite outerplanar emulator, so does every minor of $H$.

* To delete a vertex of $H$, delete its entire fiber. To delete an edge, delete all edges mapping to it. All surviving required neighbor colors are still present at every vertex.
* To contract an edge $ab$ of $H$, consider the subgraph of $F$ induced by the fibers over $a,b$. Every vertex in it has a neighbor in the opposite fiber by local surjectivity. Thus each connected component contains **both** colors. Contract each such component to one vertex in $F$, independently of the others. Give the resulting vertices the merged color $z$, and discard loops and duplicate edges.

For the contraction, each new vertex contains a representative of $a$ and of $b$. Every outside color adjacent to $z$ was adjacent to at least one of $a,b$, so the corresponding representative supplies a neighbor of that color. Conversely an outside vertex that required a neighbor of color $a$ or $b$ is still adjacent to the component containing that neighbor. All other required adjacencies persist. This gives a surjective homomorphism to the simple contracted target, locally surjective at every vertex. The new source is a minor of $F$, hence finite and outerplanar. Iteration proves the assertion.

## 2. Two facts about outerplane ears

(i) Every nonempty finite outerplanar graph has a vertex of degree at most two.

(ii) Every nonempty finite **triangle-free** outerplanar graph of minimum degree at least two has an edge whose ends both have degree two.

Here is a proof that includes cut vertices. Work in a connected component. An isolated vertex or a vertex of degree one proves (i) immediately. In the remaining case take a leaf block $B$ of the block-cut tree, or the sole block if the component is biconnected. Because the minimum degree is at least two, this block cannot be a bridge (its non-cut endpoint would have degree one). Thus $B$ is 2-connected and has at most one vertex $s$ incident to edges outside $B$.

Embed $B$ as its boundary polygon with noncrossing chords. If there is no chord, all boundary vertices except possibly $s$ have degree two in the whole graph. There are at least three boundary vertices, and at least four in the triangle-free case. In the latter case two consecutive vertices avoid $s$.

If there is a chord, the bounded faces form a tree under adjacency across chords. Each new noncrossing diagonal splits one region into two, replacing one tree vertex by two joined vertices and distributing its incident edges between them. This tree has at least two leaves. Each leaf face consists of one chord and a boundary path between its ends. Every interior vertex of that path has degree two in $B$ because an additional incident chord would subdivide the leaf face. The interiors of the boundary paths for distinct leaf faces are disjoint, since a degree-two boundary vertex belongs to only one bounded face. Choose a leaf whose path has no $s$ in its interior. Its path has at least one interior vertex. In the triangle-free case the face has length at least four, so its path has at least **two consecutive** interior vertices. These vertices have degree two in the whole graph. This proves both facts.

## 3. Neither forbidden minor has an outerplanar emulator

For $K_4$, each source vertex would require neighbors of three different colors and hence degree at least three, contradicting (i).

For $K_{2,3}$, call the side of size two $A$ and the side of size three $B$. Any emulator is bipartite, with sides the inverse images of $A,B$, since every edge must map to a target edge. Vertices over $A$ have degree at least three, and vertices over $B$ have degree at least two. Thus the emulator is triangle-free and has minimum degree at least two. By (ii) it has adjacent degree-two vertices. One endpoint must map into $A$, where the minimum is three. This is a contradiction.

If $H$ were non-outerplanar, the forbidden-minor characterization would give $K_4$ or $K_{2,3}$ as a minor of $H$. Section 1 would give that graph a finite outerplanar emulator, which Section 3 excludes. Hence $H$ is outerplanar. ∎

The only graph-structure facts used from the supplied source are the forbidden-minor characterization, the block-cut tree and the boundary polygon description of a 2-connected outerplanar graph, all in its preliminaries. The question and its singleton-color predecessor are due to Coste, Csikós and Viennot. [Paper, v1](https://arxiv.org/abs/2611.18391v1)
