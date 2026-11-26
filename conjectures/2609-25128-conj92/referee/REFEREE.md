VERDICT: HOLDS WITH CAVEATS

The submitted argument proves Conjecture 9.2 for every finite simple graph of order \(n\ge2\). Every inequality in Lemmas 1–3 and Theorem 1 is valid. One sentence after the proof overstates what the weights retain. There is also a separate mislabeled column in the producer's report.

## Exact corrections

1. **Proof, line 125, final sentence.** Replace “preserves the full quorum majority constraint” with “retains the necessary lower bound on class size imposed by the colored closed-neighborhood majority at each vertex.” On the path \(1-2-3-4\), the full-support maps \(1122\) and \(1212\) both give weight \(1/2\) everywhere. Both satisfy the class-size bound for every vertex and every subset of the support. In the first map each internal vertex sees two of its own color among three. In the second each sees one among three, so Definition 2.2 rejects it. Lemma 1 uses only the forward implication. The converse can even change an optimum. On two disjoint \(P_3\) components, give the two centers a common color and the four leaves private colors. All class-size bounds pass, but each center sees only itself out of three. The exact optimum is 4, while the proposed relaxation admits 5. Each component contributes at most two colors by the path formula, and four private colors on the leaves attain four.
2. **Producer report, lines 30 and 37–40.** The printed header means that the graph in the first position has the strict dissociation gap. The entries actually count a gap in either member of the complement pair. Replace the header with “Equality with a strict gap in at least one of \(G,\overline G\)”. Alternatively, keep the header and replace the four entries by **1, 13, 133, 1,236**. The independent reconstruction below distinguishes both predicates on each individual graph.

## Primary-source decision

The numbered environments share the theorem counter, reset by section (TeX lines 9–17). Section 2 starts with the total-coloring definition, then the partial-coloring definition. Section 9 starts with the logarithmic lower bound, then the upper-bound conjecture. The verbatim appendix below uses line numbers in the decoded TeX string, starting at 1.

In Definition 2.2, **every colored vertex** is tested. On both sides the neighborhood is **closed** and intersected with \(S=\operatorname{dom}(f)\). The symbol is \(\ge\). A colored vertex contributes its own vote on both sides, ties pass, and a vertex outside \(S\) casts no vote and faces no test. If \(a\) and \(b\) count same- and other-colored open neighbors, the test reads \(2(a+1)\ge 1+a+b\), or \(b\le a+1\). Either using a strict closed majority or using a weak open majority would instead require \(b\le a\). A vertex isolated in \(G[S]\) passes with \(1\) out of \(1\), however many uncolored neighbors it has in \(G\). The color map is onto, so every counted class is nonempty. The source's equation immediately after the definition independently confirms the induced-subgraph interpretation. The proof's explicit permission for the empty map gives zero colors and cannot change any nonempty graph's optimum.

## Audit of the submitted derivation

Line numbers in this section refer to the supplied proof.

| Lines | Inference checked |
|---|---|
| 5–15 | The complement is loopless on the same vertex set. The weak inequality at lines 8–9 reproduces the source's numerator, denominator and quantifier. The extension to \(n=1\) gives a true inequality, \(1+1\le3\). |
| 21–31 | Each of the \(\lvert C_i\rvert\) vertices in a nonempty class contributes \(1/\lvert C_i\rvert\), giving exactly one per color. Off the support the contribution is zero. When \(k=0\) both sums are empty. |
| 32–36 | Write \(d_S=\lvert N_G(v)\cap S\rvert\). The numerator is at most the size of the **whole** class. The closed colored denominator is \(1+d_S\), so \(\lvert C\rvert\ge\lceil(1+d_S)/2\rceil=1+\lfloor d_S/2\rfloor\). Since \(v\in I\subseteq S\), \(d_I\le d_S\). At \(d_I=2q\) the unrounded lower bound is \(q+1/2\). At \(2q+1\) it is \(q+1\). Both give class size at least \(q+1\). The proof keeps the class in the full support throughout. The restriction of a coloring to \(I\) can fail the quorum test without affecting this argument. All quantities inverted are positive. |
| 40–48 | With \(s'=a+b\), \((a-1)(b-1)\ge0\) implies \(ab\ge s'-1\ge s-1\ge1\). Multiplying the reciprocal inequality by positive \(s'\) gives \(1/a+1/b\le1+1/(s'-1)\le1+1/(s-1)\). Equality in the full chain occurs exactly when \(\min(a,b)=1\) and \(s'=s\). This includes \(a=b=1,s=2\). |
| 52–72 | The empty sum is 0 and the one-vertex sum is 2. For \(m\ge2\), both \(d\) and \(m-1-d\) lie in \([0,m-1]\), including isolated and universal vertices. Dividing each by two with remainder gives the stated positive integer denominators \(a,b\). |
| 74–78 | At \(m=2r\), the open degrees sum to \(2r-1\), so exactly one degree is odd. The two floors sum to \(r-1\). Hence \(a+b=r+1\) and each term is at most \(1+1/r\). Multiplication by \(2r\) gives \(m+2\). At \(r=1\) both denominators are 1. |
| 80–85 | At \(m=2r+1\), the two open degrees have the same parity. If both are odd, their floors sum to \(r-1\). If both are even, the sum is \(r\). The respective caps from Lemma 2 are \(1+1/r\) and \(1+1/(r+1)\). |
| 86–90 | A simple undirected graph has degree sum \(2\lvert E\rvert\), so its number \(t\) of odd degrees is even. On \(2r+1\) vertices this gives \(t\le2r\). The bound increases with \(t\) by \(1/r-1/(r+1)>0\) per vertex. Substituting \(2r\) gives \(m+2+1/(r+1)\), at most \(m+5/2\) for \(r\ge1\). The argument needs only the parity of the degree sum. |
| 94–103 | Finitely many partial partitions exist and the maxima are attained. They may use different supports. Outside their intersection, at least one of the two weights is zero, so their sum is at most 1. This also covers a vertex omitted by both maps. |
| 105–110 | For \(v\in I\), partition \(I\setminus\{v\}\) into its neighbors and nonneighbors in \(G\). These are exactly its two open neighborhoods in the induced complementary graphs. Their sizes sum to \(m-1\). Apply Lemma 1 separately with the same \(I\), sum the bounds, and use Lemma 3. For \(m=0\) there is no vertex at which a negative complement degree could enter a denominator. |
| 112–115 | The two disjoint parts contribute at most \(n-m\) and \(m+5/2\). Their actual sum is exactly the integer \(k_1+k_2\), so \(k_1+k_2\le\lfloor n+5/2\rfloor=n+2\). Rounding individual summands would give a different argument. |

### Boundary and sharpness checks

For \(m=2\), both labeled graphs have sum 4. For \(m=3\), the empty and complete graphs give \(9/2\). A single edge plus an isolate and its complement \(P_3\) give \(11/2\). At \(m=4\) all four possible degrees contribute \(3/2\), giving 6 on every graph. At \(m=5\) degrees \(0,4\) contribute \(4/3\), degrees \(1,3\) contribute \(3/2\), and degree 2 contributes 1. Four degree-one vertices and an isolate attain \(22/3\).

There is no hidden edge-count threshold. Adding one edge flips two degree parities, so \(t\) changes by \(-2,0\), or \(2\). The handshaking argument holds at both endpoints of every change, including the empty and complete graphs. In fact, \(r\) disjoint edges on \(2r\) vertices attain the even bound. Add one isolate for \(2r+1\) vertices: the \(2r\) endpoints attain the odd-degree term and the isolate attains the even-degree term. This verifies attainability of the sharper bounds at every order, including the exceptional half-unit at order three.

**Line 121.** In a complete graph with nonempty support \(S\), each class has size at least \(\lvert S\rvert/2\), so at most two classes occur. Two differently colored adjacent vertices attain two. In the edgeless graph all \(n\) singleton colors pass. Thus \(n+2\) is attained for every \(n\ge2\). For the second example, the independent census finds no one-sided dissociation gap through order five and precisely one isomorphism class with a gap at order six.

**Lines 122–124.** Use the order \(x,y,a_1,a_2,b_1,b_2\). In the tree the center pair contributes two same-colored votes out of four at each center, and each leaf has one vote out of two. In the complement, on \(x,a_1,a_2\), just the two leaves are adjacent. Their distinct colors tie, and \(x\) is isolated. The independent optima are 5 and 3, with dissociation numbers 4 and 3. The three intersection weights sum to \(3/2+2+2=11/2=\Sigma(P_3)\). The other three sum to \(1/2+1+1=5/2\). They total 8. A class straddling the intersection causes no double counting.

**Lines 125–126.** In the source's representative-pair definition, the edgeless graph has \(M=\varnothing\) and permits all six vertices in \(T\). In \(K_6\), if \(T\ne\varnothing\) the occupied set has size at most two, and if \(T=\varnothing\) a perfect matching attains three. Thus the sum of the two \(\Omega\) bounds is 9 while the true sum is 8. This defeats the proposed direct summation of the two \(\Omega\)'s. The wording correction above concerns only the description of the stronger weight bound. Total quorum colorings follow either by taking full supports in the argument or directly from \(\psi_q\le\psi_{sq}\) for each graph. The prior attribution of the total-coloring case comes from the supplied documents.

## Independent finite checks

The verifier builds graphs from unordered pairs. For the small coloring census it tries every support and partitions it by choosing the block of the least unused vertex. Every partial partition occurs once up to renaming colors. It tests the closed-neighborhood numerator against the closed-neighborhood denominator by integer cross-multiplication. It retains every tied optimum and tests each subset of its support. For the larger named examples it builds every allowable class on a fixed support and maximizes over exact covers by these classes. Reconstructing each winning map and reading its labels at each closed neighborhood provides a direct check on the witness.

| Graph | \(\psi_{sq}\) from the definition | Source |
|---|---:|---|
| \(K_n,\ \overline{K_n}\), \(2\le n\le8\) | \(2,\ n\) | Proposition 6.2 and line 861. At \(n=1\) both values are 1. |
| \(P_4,\ C_5\) | \(3,\ 3\) | Theorem 6.1 with ceiling for the path and floor for the cycle |
| \(S_{2,2},\ \overline{S_{2,2}}\) | \(5,\ 3\) | Proposition 4.4 prints the tree value. The complement value is from the submitted proof. |
| \(K_{1,4}\) | 4 | Proposition 6.3 with four leaves, five vertices in all |
| \(Q_3\) | 4 | Theorem 8.2 and the figure with four distinct colors on even-weight vertices |
| \(G_{3,3},\ G_{3,4}\) | \(5,\ 7\) | Theorem 7.4 gives \(\lceil5n/3\rceil\) at width three. The grids have 12 and 17 edges. |

Across orders 0–6 there are **33,868 labeled graphs**, **28,948,869** candidate partial partitions and **9,817,637** valid ones. The verifier checks **249,299** optimal partitions and **13,047,409** triples of an optimal partition, a subset \(I\), and a vertex \(v\in I\). Orders 0 and 1 are included as boundary controls. The highest complementary sum at orders 2–6 is respectively 4, 5, 6, 7 and 8.

Lemma 2 was also tested at every \(1\le a,b\le31\) and every \(2\le s\le a+b\), giving 29,791 triples and 61 equality cases. For Lemma 3, consecutive reflected Gray codes flip one edge. For each graph the verifier checks the degree sum against twice the number of set edge bits and computes each complementary degree directly. It reuses a rational sum only for graphs with identical sorted degree lists. It checks the stronger parity bound and the number of masks in each edge-count layer.

| \(m\) | Labeled graphs | Maximum \(\Sigma\) | Labeled maximizers |
|---:|---:|---:|---:|
| 0 | 1 | 0 | 1 |
| 1 | 1 | 2 | 1 |
| 2 | 2 | 4 | 2 |
| 3 | 8 | \(11/2\) | 6 |
| 4 | 64 | 6 | 64 |
| 5 | 1,024 | \(22/3\) | 80 |
| 6 | 32,768 | 8 | 224 |
| 7 | 2,097,152 | \(37/4\) | 308 |
| 8 | 268,435,456 | 10 | 1,656 |

For every order 8–30, the verifier tests matchings with isolates, their complements, complete bipartite cuts and their complements, graphs built one edge at a time in two orders, and random graphs at five densities. The six steepest-ascent starts at each order examine every one-edge neighbor before choosing an improvement. There are 471,754 evaluations, including 2,760 random graphs and 455,271 neighboring states. Revisited states are included in those counts. At each order the constructed matching examples attain the claimed parity maximum.

The impossibility of \((1,1,1)\) as the degree sequence of a three-vertex graph is essential. Feeding those three degrees to the reciprocal formula gives 6, exceeding \(11/2\). Conversely, feeding an actual three-vertex path to the mutant bound \(m+2\) gives \(11/2>5\). The real \(K_3\) rejects three singleton colors but accepts two singletons with the third vertex uncolored. The latter control simultaneously distinguishes a closed neighborhood, a weak majority, and the restriction to the support. A non-onto map with labels 1 and 3 and codomain \(\{1,2,3\}\) is rejected.

The separate pair search evaluates all feasible maps on each graph and its complement through order six, taking one representative per graph isomorphism class. For all **13,445,083** pairs it recomputes the full weight vectors, their intersection and exterior sums. Every intersection size from 0 to 6 occurs. The maximum actual intersection sum minus its order reaches \(5/2\), including in the prescribed optimal double-star witness.

As a further attack on the graph hypothesis, for each order 8–30 a dynamic program maximizes the reciprocal sum over **all** degree lists at every possible even degree sum. It starts with a zero-length list and appends every degree from 0 through \(m-1\), keeping the largest rational objective for each length and sum. Allowing nongraphical lists can only increase this maximum. All 4,462 even-sum layers stay within their order's parity cap, and some layer attains it at every order. This finite check avoids any assumed distribution of vertex degrees.

A realizability check at orders 8–15 separately visits all 104,645,277 sorted degree lists. Of the 52,326,147 with even sum, Havel–Hakimi reduction accepts 16,348,842. Its step deletes a largest entry \(d\), subtracts one from the next \(d\) largest remaining entries, and sorts again. Every accepted list was scored. The maximum in each edge-count layer agrees with its complementary layer, and the global maximum attains the parity cap at every order. At order 15, exactly the layers with 7, 13, 14, 91, 92 or 98 edges attain \(137/8\). The cap for that order is \(15+2+1/8\).

### Reconstruction of the disputed census column

For the supplementary table replay, construct the graphs of each order by adjoining a vertex with every possible neighborhood to each smaller graph. Every graph is reached by deleting and restoring a vertex. Canonicalization refines ordered cells by their neighbor counts in each cell, then individualizes tied vertices and takes the least final edge mask. Only branches related by a transposition of interchangeable vertices are merged. A final edge mask encodes every adjacency.

For a child graph, a coloring either uses the whole graph or omits at least one vertex. Enumerate all allowable color classes and solve the exact-cover maximization for full support. For proper supports take the largest partial-coloring optimum among the deletion parents. Every such parent occurs in the construction. Apply the same deletion rule to dissociation, testing maximum degree at most one on full support. Look up the complement by its actual adjacency. This reconstructs the table directly from the definitions. The exhaustive labeled checks through six also provide a separate comparison for these counts.

| Order | Isomorphism classes | Complementary sum, min–max | Equality | One-sided gap, all graphs | Equality and one-sided gap | Equality and either-side gap |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 2 | 4–4 | 2 | 0 | 0 | 0 |
| 3 | 4 | 5–5 | 4 | 0 | 0 | 0 |
| 4 | 11 | 6–6 | 11 | 0 | 0 | 0 |
| 5 | 34 | 6–7 | 32 | 0 | 0 | 0 |
| 6 | 156 | 7–8 | 122 | 1 | 1 | 2 |
| 7 | 1,044 | 7–9 | 538 | 13 | 13 | 26 |
| 8 | 12,346 | 7–10 | 3,036 | 263 | 133 | 264 |
| 9 | 274,668 | 8–11 | 21,354 | 7,160 | 1,236 | 2,450 |

The two one-sided sets overlap on 2 graphs at order eight and 22 at order nine, by inclusion–exclusion. The corrected counts cannot in general be obtained simply by halving the printed column. The producer describes 53,470 other evaluations in its report. Their raw instances are outside the permitted inputs.

## Verdict checks

CONTROLS: No assumption overrode a control. In the verifier output, the lines beginning with CONTROLS record \(11/2>5\) for the tightened degree-sum bound, \(6+3>8\) for the representative-pair substitution, and opposite validity outcomes for the two equal-weight maps on \(P_4\). The last outcome requires the correction to proof line 125.

CONTRADICTING: No contrary observation was set aside in reaching the theorem verdict. The small coloring census covers 33,868 labeled graphs, the degree-sum census visits all \(2^{21}\) and \(2^{28}\) edge masks at orders seven and eight, and the support-pair check includes every feasible map on both sides through order six up to graph isomorphism and color renaming. The false converse and the one-sided table mismatch are both retained. The verifier raises on any failed mathematical check.

LABELS: No. The formula in decoded TeX lines 69–75 and the statement in lines 861–867 were checked against the raw member. Figure labels for the cube agree with the four even-weight bit strings in TeX lines 757–772. The independent TABLE output tests both gap predicates on the actual graph and complement. At order nine it gives 1,236 for the printed heading and 2,450 for the intended either-side heading.

This is AI work. No human has checked it.

## Verbatim primary-source extracts

The following fenced ranges are copied from the sole decoded LaTeX member of the supplied gzip/JSON file. Some named examples are instances of family statements. The paper gives the general formula in those cases. In particular, its standalone double-star proposition concerns the tree itself.

**Neighborhood and dissociation conventions** (TeX 56–58)

```tex
All graphs are finite, simple and undirected. For a graph $G=(V,E)$ and $v\in V$, let $N_G(v)$ and $N_G[v]=N_G(v)\cup\{v\}$ denote the open and closed neighborhoods, and let $d_G(v)=|N_G(v)|$. For $S\subseteq V$, $G[S]$ is the subgraph induced by $S$ and $d_S(v)=|N_G(v)\cap S|$. We write $\Delta(G)$ and $\delta(G)$ for the maximum and minimum degrees. The complement is $\overline G$.

A matching is a set of pairwise vertex-disjoint edges; its maximum size is $\mu(G)$. For $k\ge1$, a set $S\subseteq V$ is \emph{$k$-independent} if $\Delta(G[S])\le k-1$. Its maximum cardinality is $\beta_k(G)$. Thus $\beta_1(G)=\alpha(G)$ is the ordinary independence number, while a $2$-independent set induces only isolated vertices and edges. We write $\omega(G)$ for the clique number.
```

**Sub-quorum coloring and the induced-subgraph identity** (TeX 69–79)

```tex
\begin{definition}
A \emph{sub-quorum coloring} is an onto partial map $f:V(G)\dashrightarrow\{1,\ldots,k\}$. If $S=\operatorname{dom}(f)$, then every $v\in S$ must satisfy
\[
 |\{u\in N_G[v]\cap S:f(u)=f(v)\}|\ge\frac{|N_G[v]\cap S|}{2}.
\]
The maximum possible number of colors is denoted $\psq(G)$. We write $G_f=G[S]$.
\end{definition}
Thus a sub-quorum coloring of $G$ is exactly a quorum coloring of some induced subgraph $G[S]$, and consequently
\begin{equation}\label{eq:induced}
\psq(G)=\max_{S\subseteq V(G)}\pq(G[S])\ge\pq(G).
\end{equation}
```

**Representative-pair bound** (TeX 88–92)

```tex
For upper bounds, let $\Omega(G)$ be the maximum of $|T|+|M|$ over matchings $M$ and vertex sets $T$ disjoint from $V(M)$ such that every $t\in T$ has at most one neighbor in $T\cup V(M)$. We call $(T,M)$ a \emph{feasible representative pair}.
\begin{lemma}\label{lem:omega} For every graph $G$, $\psq(G)\le\Omega(G)$. \end{lemma}
\begin{proof}
Take an optimal sub-quorum coloring. Let $T$ consist of its singleton color classes and choose one edge from every other class, forming a matching $M$; such an edge exists because the class is connected. Each $t\in T$ has at most one neighbor in the colored support by Lemma~\ref{lem:local}, and hence at most one in $T\cup V(M)$. Thus $(T,M)$ is feasible and its objective is exactly the number of colors.
\end{proof}
```

**Complete graph at the cubic endpoint** (TeX 184–193)

```tex
\begin{corollary}[Cubic graphs]\label{cor:cubic-bounds}
If $G$ is a cubic graph of order $n$, then
\[
\boxed{\frac n2\le\bii(G)\le\psq(G)\le\frac{3n}{5}.}
\]
The constants $1/2$ and $3/5$ cannot be improved: $K_4$ attains the lower endpoint, while the Petersen graph attains the upper endpoint.
\end{corollary}
\begin{proof}
The first inequality follows from the cited dissociation bound with $\Delta(G)=3$, the middle inequality is Theorem~\ref{thm:beta2}, and the last inequality is Theorem~\ref{thm:degree-upper}. For $K_4$, Proposition~\ref{prop:complete} gives $\psq(K_4)=2=n/2$. For the Petersen graph $P$, label the outer cycle $u_0u_1u_2u_3u_4u_0$, the inner vertices $v_0,\ldots,v_4$, with spokes $u_iv_i$ and inner edges $v_iv_{i+2}$ (indices modulo $5$). Then $\{u_0,u_1,u_3,v_2,v_3,v_4\}$ induces three disjoint edges, and is therefore a $2$-independent set of size $6$. Hence $\psq(P)\ge6$, while the upper bound gives $\psq(P)\le6$.
\end{proof}
```

**Double star** (TeX 314–322)

```tex
\begin{proposition}\label{prop:s22}
For the double star $S_{2,2}$,
\[
\bii(S_{2,2})=4,\qquad \psq(S_{2,2})=5.
\]
\end{proposition}
\begin{proof}
Let $x,y$ be the adjacent centers, each with two leaves.  The four leaves form a dissociation set, while any dissociation set containing a center has size at most four; hence $\bii(S_{2,2})=4$.  For the sub-quorum coloring, give $x$ and $y$ one common color and give the four leaves four distinct colors.  At either center there is one same-colored and two differently colored neighbors, so the local inequality holds and five colors are feasible.  Six colors would make every vertex a singleton, which fails at each center.  Thus $\psq(S_{2,2})=5$.
\end{proof}
```

**Path and cycle formula** (TeX 360–362)

```tex
\begin{theorem}\label{thm:pathcycle}
For $n\ge1$, $\psq(P_n)=\bii(P_n)=\lceil2n/3\rceil$. For $n\ge3$, $\psq(C_n)=\bii(C_n)=\lfloor2n/3\rfloor$.
\end{theorem}
```

**Complete graphs and stars** (TeX 378–390)

```tex
\begin{proposition}\label{prop:complete}
For every $n\ge2$, $\psq(K_n)=2$.
\end{proposition}
\begin{proof}
Every nonempty induced subgraph of $K_n$ is a complete graph. Hedetniemi et al.~\cite{HHLM2013} proved that the quorum coloring number of a complete graph is at most two, while an induced $K_2$ has quorum coloring number two. Equation~\eqref{eq:induced} therefore gives $\psq(K_n)=2$.
\end{proof}

\begin{proposition}\label{prop:star}
For every $n\ge2$, $\psq(K_{1,n})=n$.
\end{proposition}
\begin{proof}
The $n$ leaves form an independent set, so $\psq(K_{1,n})\ge n$. A sub-quorum coloring with $n+1$ colors would make every vertex a singleton-colored vertex; the center would then have $n$ colored neighbors of other colors and would violate Lemma~\ref{lem:local}. Hence $\psq(K_{1,n})\le n$.
\end{proof}
```

**Complete multipartite formula, including complete graphs and stars** (TeX 392–398)

```tex
\begin{theorem}\label{thm:multipartite}
Let $p\ge2$ and $1\le n_1\le\cdots\le n_p$. Then
\begin{equation}\label{eq:multipartite}
\psq(K_{n_1,\ldots,n_p})=\max\{2,n_p\}.
\end{equation}
In particular, the value is $n_p$ whenever $n_p\ge2$.
\end{theorem}
```

**Corona family, including the four-leaf star at one central vertex** (TeX 411–421)

```tex
\begin{theorem}[Corona graphs]\label{thm:corona}
For all positive integers $n$ and $m$,
\[
\psq(K_n\circ\overline{K_m})
=mn+\left\lceil\frac{m}{n}\left\lfloor\frac{n}{m}\right\rfloor\right\rceil
=\begin{cases}
mn, & 1\le n<m,\\
mn+1, & 1\le m\le n.
\end{cases}
\]
\end{theorem}
```

**Join family, including stars with one clique vertex** (TeX 470–475)

```tex
\begin{theorem}[Join graphs]\label{thm:join}
For all integers $m\ge1$ and $n\ge2$,
\[
\psq(K_m+\overline{K_n})=n.
\]
\end{theorem}
```

**Rectangular grid notation and cover identity** (TeX 484–488)

```tex
The NP-completeness result above already holds for bipartite graphs. Rectangular grids form a much more structured bipartite family, and for the first fixed widths the sub-quorum coloring number can nevertheless be determined exactly. Write $G_{m,n}=P_m\square P_n$. Dissociation sets are complements of vertex sets meeting every three-vertex path, so
\[
\beta_2(G)=|V(G)|-\tau_3(G),
\]
where $\tau_3(G)$ is the minimum $3$-path vertex-cover number. The exact grid values proved in \cite{Bresar2013,JakovacTaranenko2013} therefore give the following formula.
```

**Grid formula and dissociation bound** (TeX 491–507)

```tex
\begin{equation}\label{eq:Fmn}
F(m,n)=
\max\left\{
\left\lceil\frac m2\right\rceil\left\lceil\frac{2n}3\right\rceil+
\left\lfloor\frac m2\right\rfloor\left\lfloor\frac n3\right\rfloor,
\left\lceil\frac n2\right\rceil\left\lceil\frac{2m}3\right\rceil+
\left\lfloor\frac n2\right\rfloor\left\lfloor\frac m3\right\rfloor
\right\}.
\end{equation}

\begin{theorem}[Equivalent form of the grid $3$-path-cover formula \cite{Bresar2013,JakovacTaranenko2013}]\label{thm:gridbeta}
For all integers $m,n\ge1$,
\[
\boxed{\beta_2(G_{m,n})=F(m,n).}
\]
Consequently $\psq(G_{m,n})\ge F(m,n)$.
\end{theorem}
```

**Grid conjecture and the widths proved** (TeX 519–526)

```tex
\begin{conjecture}[Rectangular-grid conjecture]\label{conj:grid}
For all integers $m,n\ge2$,
\[
\boxed{\psq(G_{m,n})=\beta_2(G_{m,n})=F(m,n).}
\]
\end{conjecture}

The results below verify Conjecture~\ref{conj:grid} for the first infinite families of grid strips, namely whenever $2\le m\le11$ (and, by symmetry, whenever $2\le n\le11$).
```

**Exact strip theorem, including both requested grids** (TeX 549–567)

```tex
\begin{theorem}[Computer-assisted exact grid strips]\label{thm:gridstrips}
For every $n\ge1$,
\[
\begin{aligned}
\psq(G_{3,n})=\beta_2(G_{3,n})&=\left\lceil\frac{5n}{3}\right\rceil,\\
\psq(G_{4,n})=\beta_2(G_{4,n})&=\begin{cases}2n,&n\text{ even},\\2n+1,&n\text{ odd},\end{cases}\\
\psq(G_{5,n})=\beta_2(G_{5,n})&=\max\left\{3\left\lceil\frac{2n}{3}\right\rceil+2\left\lfloor\frac n3\right\rfloor,
4\left\lceil\frac n2\right\rceil+\left\lfloor\frac n2\right\rfloor\right\},\\
\psq(G_{6,n})=\beta_2(G_{6,n})&=\begin{cases}3n,&n\text{ even},\\3n+1,&n\text{ odd},\end{cases}\\
\psq(G_{7,n})=\beta_2(G_{7,n})&=\max\left\{4\left\lceil\frac{2n}{3}\right\rceil+3\left\lfloor\frac n3\right\rfloor,
5\left\lceil\frac n2\right\rceil+2\left\lfloor\frac n2\right\rfloor\right\}.
\end{aligned}
\]
For each $m\in\{8,9,10,11\}$,
\[
\boxed{\psq(G_{m,n})=\beta_2(G_{m,n})=F(m,n).}
\]
Together with Theorem~\ref{thm:ladder}, this determines $\psq(G_{m,n})$ for every fixed width $2\le m\le11$.
\end{theorem}
```

**Cube dissociation theorem** (TeX 619–625)

```tex
\begin{theorem}\label{thm:cubebeta}
For every integer $n\ge2$,
\[
\boxed{\bii(Q_n)=2^{n-1}.}
\]
Consequently, $\psq(Q_n)\ge 2^{n-1}$.
\end{theorem}
```

**Cube sub-quorum theorem** (TeX 648–653)

```tex
\begin{theorem}\label{thm:cubeall}
For every integer $n\ge2$,
\[
\boxed{\psq(Q_n)=\bii(Q_n)=2^{n-1}.}
\]
\end{theorem}
```

**Optimal parity example** (TeX 746–746)

```tex
The lower-bound construction appearing in Theorem~\ref{thm:cubebeta} is illustrated in Figures~\ref{fig:q3parity} and~\ref{fig:q4parity}.  Only the even-weight vertices are colored, and each of them receives its own color; the odd-weight vertices are left uncolored.  Since every hypercube edge joins vertices of opposite parity, the colored support is independent.  Thus these figures display optimal sub-quorum colorings with $2^{n-1}$ colors, rather than a two-coloring of the whole hypercube.
```

**Three-cube figure, including vertex labels and adjacency** (TeX 748–776)

```tex
\begin{figure}[ht]
\centering
\begin{tikzpicture}[
  scale=1.02,
  every node/.style={circle,draw,minimum size=5.7mm,inner sep=0pt,font=\scriptsize},
  sel/.style={fill=gray!45},
  un/.style={fill=white}
]
% Q3 as two offset squares. Even-weight vertices are filled.
\node[sel] (q000) at (0,0) {000};
\node[un]  (q001) at (2.2,0) {001};
\node[un]  (q010) at (0,2.2) {010};
\node[sel] (q011) at (2.2,2.2) {011};

\node[un]  (q100) at (.75,.75) {100};
\node[sel] (q101) at (2.95,.75) {101};
\node[sel] (q110) at (.75,2.95) {110};
\node[un]  (q111) at (2.95,2.95) {111};

\draw (q000)--(q001)--(q011)--(q010)--cycle;
\draw (q100)--(q101)--(q111)--(q110)--cycle;
\draw (q000)--(q100) (q001)--(q101) (q010)--(q110) (q011)--(q111);

\node[draw=none,rectangle,font=\small] at (1.48,-.72)
{$E_3=\{000,011,101,110\}$,\qquad $|E_3|=4=2^{3-1}$};
\end{tikzpicture}
\caption{An optimal sub-quorum coloring of $Q_3$. Filled vertices are the even-weight vertices and each receives a distinct color; unfilled vertices are uncolored. Hence the colored support is independent and the coloring uses four colors.}
\label{fig:q3parity}
\end{figure}
```

**Smaller cube in the four-cube figure** (TeX 828–829)

```tex
\caption{The same optimal construction on $Q_4$, drawn as two copies of $Q_3$. Dashed edges join corresponding vertices in the two copies. Exactly the eight even-weight vertices are filled, each with its own color; all odd-weight vertices are uncolored.}
\label{fig:q4parity}
```

**Lower complementary bound** (TeX 835–844)

```tex
\begin{theorem}\label{thm:ng-lower}
For every graph $G$ of order $n\ge2$,
\[
\boxed{\psq(G)+\psq(\overline G)>\log_2 n.}
\]
In particular,
\[
\psq(G)+\psq(\overline G)\ge\lfloor\log_2 n\rfloor+1.
\]
\end{theorem}
```

**Complete and empty graphs and the exact upper-bound conjecture** (TeX 861–867)

```tex
The complete and empty graphs suggest the complementary extremal question.  Since $\psq(K_n)=2$ for $n\ge2$ and $\psq(\overline{K_n})=n$, they give sum $n+2$.
\begin{conjecture}\label{conj:ng-upper}
For every graph $G$ of order $n\ge2$,
\[
\psq(G)+\psq(\overline G)\le n+2.
\]
\end{conjecture}
```

**Open status in the conclusion** (TeX 882–882)

```tex
The Nordhaus--Gaddum inequality $\psq(G)+\psq(\overline G)>\log_2 |V(G)|$ shows that complementation forces a nonconstant amount of sub-quorum structure. Determining the corresponding upper extremum, and in particular Conjecture~\ref{conj:ng-upper}, remains open. Other natural directions include characterizing trees for which $\psq(T)=\beta_2(T)$, extending the tree algorithm to bounded-treewidth classes, and developing approximation or parameterized algorithms for the general problem.
```
