# Conditional-square certificates for Ramsey multiplicity

Candidate and unrefereed. These are computational proof candidates, with separate exact implementations; there has been no external human referee review. Standard flag-algebra reasoning is credited to Razborov, PPSS, KPS and the preceding public certificates. See PRIOR_ART.md.

## C6 result and scope

The frozen larger-type certificate `certificates/c6_ordered_type8.cert.xz` states

    c6 >= 8280981029 / 250000000000000 = 0.000033123924116.

It uses ordered roots, ambient order eight, and every root type in families (t,m)=(0,4),(2,3),(4,2),(6,1). Thus it genuinely enlarges the type family used by round 2, whose C6 model stopped at four roots. It does not claim that eight-vertex products become genuine nine-vertex products by introducing an unused vertex. The requested larger-type alternative is the source of this gain.

The comparison 0.000025987 in public candidate PR #308 gives an improvement of 27.4634398583907...%, exceeding the requested 5%. Comparisons use exact fractions. No priority, novelty or optimality claim is made.

## Stored data and coefficient inequality

A header specifies ambient n, clique size k, a positive integer D, the number of blocks, the rational bound b, and root mode. Each block fixes root size t, extension size m, a root graph, its list of rooted flags F_i, and integer rows L_r. In the selected format the header mode is -2 and every block additionally stores its own root mode and colour (0 or 1). A colour-1 block evaluates its flags in the complement of the ambient graph. The selected certificate has 340 blocks: one copy for each colour of 170 ordered-root blocks. Its factors already incorporate the colour-averaging scale; no additional factor of two is applied by a verifier. Flags have t+m distinct vertices. Root mode zero identifies root permutations as well as extension permutations; mode one fixes root labels and only identifies extension permutations. The matrix is exactly

    Q_ij = sum_r L_ri L_rj / D^2.

It is positive semidefinite without any numerical eigenvalue assumption.

For an ambient graph H, enumerate a root set R of size t, then ordered disjoint extension sets A,B of size m. Evaluate the rooted flags on R+A and R+B. The contribution of a block is the sum of Q_ij over the samples belonging to that block, divided by

    binom(n,t) binom(n-t,m) binom(n-t-m,m).

In ordered-root mode also enumerate all t! root orders and multiply the denominator by t!. Root types not equal to the specified type contribute zero. All sums and comparisons are rational. The checked inequality for each H is

    monochromatic_Kk_density(H) - sum_blocks contribution(H) >= b.

For the C6 certificate all 12,346 eight-vertex isomorphism classes pass. The predecessor checker independently expands every vertex permutation and proves that their union is exactly all 2^28 labelled graphs, rejecting duplicate or incomplete class lists. It also checks the uniform random-colouring normalization. The new checker rebuilds flag orbits and disjoint extension samples from the frozen certificate, aggregates integer occurrence counts, and computes its Gram matrices directly from the integer factors. It imports neither generator tables nor solver matrices. Both exact implementations agree on the minimum and worst graph.

## Why the finite inequalities imply an asymptotic lower bound

Fix a large graph G_N representing one colour; its complement represents the other. Choose a root set (or an ordered root embedding in mode one) and then two *independent* uniform m-subsets outside it. Fix the block colour and use either the graph or its complement. Conditional on the root, let p_i be the probabilities of the rooted flags. The expected block contribution with independent extensions is

    p^T Q p = sum_r (sum_i L_ri p_i)^2 / D^2 >= 0.

Restricting the two extension sets to be disjoint changes the expectation by a quantity tending uniformly to zero as N tends to infinity. Explicitly, put M_b=max_i Q_ii for a block. By Cauchy–Schwarz, |Q_ij|<=M_b. Independent extensions intersect with probability at most m^2/(N-t). The difference between independent and disjoint expectations has absolute value at most 2 M_b m^2/(N-t). Including the root-type indicator does not increase this bound.

Average the verified ambient inequality over uniform n-subsets of G_N. Double counting gives exactly the monochromatic K_k density of G_N on the objective side, and the disjoint-extension averages on the square side. Consequently, for N>=n,

    density_Kk(G_N) >= b - 2 sum_blocks M_b m_b^2/(N-t_b).

There are finitely many fixed rational blocks. The error tends to zero, proving the candidate asymptotic bound c_k>=b. No solver optimality claim is needed.

## Independence and limitations

The search generates numerical SDP matrices or graphons. Exact checkers use frozen integer factors or rational probabilities and do not call search routines. Separate implementations are not independent external authorship: all new code here was prepared in one Codex session, and remains unrefereed. Rejection controls, hashes and final receipts accompany the selected artifacts. Floating objectives, solver return codes, and numerical PSD diagnostics are not proof inputs.

