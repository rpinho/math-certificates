# Candidate rational Ramsey multiplicity bounds

**Candidate and unrefereed.** The frozen certificates prove the following inequalities, subject to the supplied computer-assisted proof and its exact replays:

| Constant | Bound | Frozen artifact |
|---|---:|---|
| C89c = c6 | **25987181439/10^15 = 0.000025987181439** | `certificates/c6_9.cert` |
| c6, eight-vertex support | 3248397557/125000000000000 = 0.000025987180456 | `certificates/c6_8.cert.gz` |
| C89b = c5 | **762079654433/500000000000000 = 0.001524159308866** | `certificates/c5_8.cert.gz` |

This is standard conditional-square/flag-algebra reasoning, following Razborov and Parczyk–Pokutta–Spiegel–Szabo (PPSS), and building on the preceding public c6 certificate in PR #308. No novelty of method, optimality, exhaustive priority, or independent human review is claimed. PRIOR_ART.md gives the source audit. No Ramsey-number assumption is used.

## 1. Definition and normalization

For a red/blue colouring G of K_N, let M_k(G) count the unordered k-element vertex sets with every edge the same colour. Define p_k(G)=M_k(G)/binomial(N,k). Both colours count once, without a k! or random-density scaling factor.

If N>=q>=k, a uniform q-subset U satisfies E p_k(G[U])=p_k(G), because every k-subset has the same containment probability. Hence min_G p_k(G) is nondecreasing in N and bounded above by one. Its limit c_k exists. This is precisely the normalization in PRs #277 and #279. Random colouring has density 2^(1-binomial(k,2)), namely 1/512 for k=5 and 1/16384 for k=6.

## 2. Flags, types and exact squares

Encode red edges on ordered vertices by the bits for (0,1),(0,2),(1,2),(0,3),(1,3),(2,3),... . A (t,m)-flag is an induced graph with a distinguished root set of size t and m further vertices. Its type is the graph induced by its roots.

In root mode zero, flag isomorphisms may independently permute roots and nonroots. In root mode one, roots have distinct labels and only nonroots may be permuted. At each fixed actual root choice, these flag classes still have well-defined probabilities. Wrong root types contribute zero. A certificate contains complete flag lists for its included type blocks; orbit coverage and duplication checks are part of verification.

The header gives n,k,D,B,b_num,b_den,root_mode. Each of B blocks gives t,m,type,d,h, then d flag codes and h rows of d signed integers forming L. Its rational matrix is

    Q = L^T L / D^2.

For every real z,

    z^T Q z = sum_r (sum_i L_ri z_i / D)^2 >= 0.             (1)

This is exact positive semidefiniteness; no numerical eigenvalue tolerance enters the proof. Zero or dependent factor rows are harmless.

Both c6 artifacts have D=10^12, root mode zero, 14 blocks and 1303 stored factor rows. Their families are (t,m)=(0,4),(2,3),(4,2), with respectively 1,2,11 types. Their products use eight vertices. The primary artifact has ambient order nine, so one vertex is unused; it does not claim that genuinely nine-vertex flag products produced the gain.

The c5 artifact has n=8, D=10^12, root mode one, 170 blocks and 13227 factor rows. It uses (0,4),(2,3),(4,2),(6,1), with respectively 1,2,11,156 root types. Its matrices were obtained from the exactly replayed PPSS certificate by nonnegative reweighting and additional square directions, then refactored and rounded to the stored integers. Floating solver output is not a proof input.

## 3. Finite coefficient inequalities

For a graph H on n vertices and a block Q, choose a uniform root t-set R, a uniform m-subset A outside R, then a uniform m-subset B outside R union A. Other vertices are unused. If the root type is correct, let i,j be the classes of the flags on R union A and R union B; otherwise put the term equal to zero. Define

    a_Q(H) = sum_(R,A,B) Q_ij / d_Q,
    d_Q = binomial(n,t) binomial(n-t,m) binomial(n-t-m,m).

In mode one also average over all t! root orderings, multiplying d_Q by t!. Both ordered occurrences of off-diagonal entries are counted. Let a(H)=sum_Q a_Q(H) and b=b_num/b_den. The exact finite assertion is

    p_k(H) - a(H) >= b                                     (2)

for every graph H on n vertices.

For c6 the denominators are 70,560,420 at order eight and 630,5040,3780 at order nine. For the ordered c5 families they are 70,1120,10080,40320. The target denominators are binomial(8,6)=28, binomial(9,6)=84 and binomial(8,5)=56 respectively.

A vertex bijection preserves monochromatic k-sets and gives a bijection of all root/extension choices, preserving flag classes. Thus (2) is invariant under isomorphism and checking one representative of every graph class suffices.

## 4. Exact verification and exhaustive graph lists

The frozen graph lists have hashes

    graph8.g6: 546a249902101c97d3aa590f93e53366854bd0a6f405aa59bdb32d25c57f845a
    graph9.g6: 839f67ecc73b1f539128694badebe27adf4f0fb1ee6d0663b7ad9868100d5123

At order eight, two exact programs independently expand permutation orbits and require disjoint coverage of all 268435456 labelled graphs. They verify 12346 isomorphism classes and the random-colouring normalization. No advertised graph-list cardinality is accepted as a completeness proof.

At order nine, `scripts/check_graph9.py` independently adjoins a new vertex with every one of 256 neighbourhoods to every eight-vertex representative: 3160576 augmentations. Canonical certificates from nauty must form exactly the set of 274668 classes in the nine-vertex list, without duplicates. This is exhaustive by induction: deleting a vertex of an arbitrary nine-vertex graph yields an eight-vertex class, and its missing neighbourhood is among those tried. The complete eight-vertex input is separately checked by labelled orbit coverage. The supplied list's exhaustiveness is therefore checked, rather than trusted from its public source.

`scripts/verify_frozen.cpp` was independently written in this job. It reads only the certificate and graph list, forms integer Gram products with GMP, reconstructs flag orbits, directly counts monochromatic sets and every root/disjoint-extension choice, and checks (2) by integer cross-multiplication. It does not read search tables, metadata, numerical matrices, LP weights or solver output.

The second eight-vertex replay, `scripts/verify_legacy_gmp.cpp`, adapts the preceding checker only in its integer backend and integer text I/O. Its graph-orbit and coefficient bookkeeping are separately implemented. All final arithmetic uses arbitrary-precision integers.

The second nine-vertex replay uses a different finite identity. Since all its flag products use eight vertices,

    a_9(H) = (1/9) sum_v a_8(H-v),
    p_k(H) = (1/9) sum_v p_k(H-v).

Every root/extension triple has exactly one unused vertex, proving the first identity; uniform subset sampling proves the second. `scripts/verify_lift9.cpp` recomputes all eight-vertex residuals from the nine-vertex certificate, including negative individual residuals. It builds an exhaustive labelled eight-vertex orbit-to-class index, then sums the nine exact residuals for every nine-vertex graph. It does not read the search's nauty lifting indices. This proves the same inequalities by vertex deletion rather than direct nine-vertex partition enumeration. Both nine-vertex coefficient replays require the separate completeness check above.

Both exact routes agree on these positive minimum slacks:

| Artifact | Minimum slack | Graph index |
|---|---|---:|
| c6_9.cert | 7564739462625047/7560000000000000000000000000 | 30156 |
| c6_8.cert.gz | 420281426482829/420000000000000000000000000 | 11661 |
| c5_8.cert.gz | 560022510134247/560000000000000000000000000 | 9736 |

`receipts/exact_slacks.json` checks equality of the independently printed fractions. Negative controls reject a doubled bound, a wrong square denominator, duplicate flags, duplicate or missing eight-vertex graphs, and an incomplete nine-vertex list. These are implementation checks, not independent human review.

## 5. Asymptotic nonnegativity with an explicit error

Fix a large graph G on N>=n vertices and a block. Choose its actual roots R uniformly, with labels in mode one. If the type is correct, let x_R(i) be the probability that a uniform m-subset outside R gives flag class i. For independent choices A,C,

    E[Q_class(R,A),class(R,C) | R] = x_R^T Q x_R >= 0.      (3)

Let M_Q=max_ij |Q_ij|. The overlap probability epsilon is at most m^2/(N-t), by the union bound. For |Y|<=M_Q and the positive-probability disjointness event E,

    |E[Y|E]-E[Y]| <= 2 M_Q Pr(not E).

Indeed E[Y]=Pr(E)E[Y|E]+Pr(not E)E[Y|not E]. Thus the expected contribution of disjoint extensions is at least -2 M_Q m^2/(N-t), including zero contributions from wrong root types.

Choosing a uniform n-set U and then its root/extension choices gives the uniform distribution on disjoint triples in G: each triple belongs to the same number binomial(N-t-2m,n-t-2m) of n-sets. Consequently

    E_U a_Q(G[U]) >= -2 M_Q m^2/(N-t).

Averaging (2), using E_U p_k(G[U])=p_k(G), gives for every G

    p_k(G) >= b - sum_Q 2 M_Q m_Q^2/(N-t_Q).               (4)

The matrices are fixed and finite, so the error tends to zero uniformly in G. Minimize over G and let N tend to infinity to obtain c_k>=b, proving the stated candidate inequalities.

The coefficient a(H) can be negative on a small graph. The proof uses nonnegativity of the limiting large-graph expectation, not pointwise nonnegativity, and does not assert that every eight- or nine-vertex graph contains a monochromatic K6.

## 6. Frozen artifact identification

Uncompressed certificate SHA256:

    c6_9: 0137db8ed8648496eddf8f007bcda642ffae9c2e7d93f9b224c4b5c4eec96665
    c6_8: bbcc572b177c0f1a5bf5a36f3be7056441f0fe160ad8e7f59b840aaf0ff199ad
    c5_8: cc7fa1eb973d9d350b4a0cc01163eb027578497c0d2f3aa12d7deb8e7ffb385a

CERTIFICATES.json records compressed-file hashes, exact values and block metadata. The manifest fixes the proof, graph lists, verifier sources and replay receipts. REPRODUCE.md gives commands. The proof depends on these exact artifacts and checks, not on numerical optimization status or a claim that the relaxation is optimal.
