# A rational seven-vertex lower bound for the K6 Ramsey multiplicity constant

**Candidate, unrefereed.** This is a computer-assisted proof with an explicit rational sum-of-squares certificate. No optimality or priority claim is made. The method is the standard flag-algebra/conditional-square method of Razborov, as used for clique multiplicities by Parczyk–Pokutta–Spiegel–Szabó. The implementation and certificate here were produced in this job. See PRIOR_ART.md for the bounded source audit and comparison qualifications.

## 1. Normalization and statement

For a red/blue colouring G of K_N, write M_6(G) for the number of unordered six-element vertex sets whose fifteen edges have one colour. Put c_6(N)=min_G M_6(G)/binomial(N,6). Averaging over induced subsets proves c_6(N) is nondecreasing: if N>=m>=6, the expected monochromatic six-set density in a uniformly chosen m-set is exactly M_6(G)/binomial(N,6), and is at least c_6(m). Since the values lie in [0,1], their limit c_6 exists.

This is exactly C89c in PR #279. The factor 2^-14 is the random-colouring value and is not a factor in the definition of C89c.

The seven-vertex certificate establishes

    c_6 >= 2431/125000000 = 0.000019448.

The statement uses no numerical bound on any Ramsey number. The certificate's finite inequalities and the elementary limit argument below are its only ingredients.

## 2. Encoding rooted graphs

Interpret a red edge as 1 and a blue edge as 0. A graph on s ordered vertices 0,...,s-1 is encoded by the integer whose bits, beginning with bit 0, record edges

    (0,1), (0,2), (1,2), (0,3), (1,3), (2,3), ... .

The primary certificate uses **ordered roots**. A flag of parameters (t,m) is a graph on t+m vertices with vertices 0,...,t-1 distinguished individually. Two flags are identified if an isomorphism fixes each root; only the non-root vertices may be permuted. A root type is a fixed labelled graph on those t roots. One representative of each root isomorphism class is used, and its labelled realization is selected by the type indicator below.

The auxiliary, weaker certificate `c6_7.cert` instead uses unordered roots: an isomorphism may permute the roots among themselves. Both conventions have the same conditional-square proof, with the corresponding sampling denominator.

For a fixed root type sigma, list all flag classes F_1,...,F_d of that type and these parameters. Each has the same t and m. All classes are induced classes, so both edges and nonedges are respected. The seven-vertex certificate uses (t,m)=(1,3),(3,2),(5,1), and all root types for each pair. In every case t+2m=7.

For either convention, for any fixed root object R in any graph, the probabilities of these classes form a vector x_R with nonnegative coordinates summing to 1. Any positive semidefinite matrix Q therefore satisfies x_R^T Q x_R>=0. No identification between distinct labelled root statistics is assumed.

## 3. Certificate format and rational positivity

The first line of the primary `c6_7full_single.cert` is

    n k D B b_num b_den root_mode

where n=7, k=6, D=10^9, B=39, b=b_num/b_den=2431/125000000, and root_mode=1 means ordered roots. root_mode=0 means unordered roots; omission of that final field in the auxiliary file also means 0. For each block, the next line is

    t m type_code d rank

followed by d flag codes, followed by `rank` rows of d signed integers comprising a matrix L. The root type code uses the same edge-bit convention on its t vertices. It need only represent that root isomorphism class. The corresponding rational matrix is

    Q = L^T L / D^2.

For every real vector z,

    z^T Q z = sum_r (sum_i L[r,i] z_i / D)^2 >= 0.

Thus positive semidefiniteness is explicit over the rationals, and does not require a numerical eigenvalue test.

## 4. The finite coefficient check

Let H be any red/blue graph on seven vertices. For a block of parameters (t,m), choose uniformly an ordered t-tuple R of distinct vertices of V(H), then choose uniformly an m-subset A outside its underlying vertex set. Let B'=V(H)\(R union A); it has size m. If H[R], in its specified root order, equals the block's labelled root type, let i and j be the flag classes induced on R union A and R union B'. Otherwise this block contributes 0. Define its coefficient

    a_Q(H) = [sum over R,A of 1_{type(R)=sigma} Q[i,j]]
             / [(7)_t binomial(7-t,m)],

where (7)_t=7!/(7-t)!=binomial(7,t)t!. For root_mode=0, sample an unordered root set and omit t! from this denominator.

The use of B' here is unrelated to B=39 in the file header. Both orders of a partition are counted; equivalently, an off-diagonal matrix entry is counted for each of its ordered occurrences. Define a(H) as the sum of these coefficients over all 39 blocks, and p(H)=M_6(H)/7.

The separately written program `verify_exact.cpp` checks, for every graph H on seven vertices up to isomorphism,

    p(H) - a(H) - b >= 0.                                      (1)

It recognizes flags by expanding the permutation orbits of the supplied representatives, instead of using the search program's canonicalization routine. It constructs every Q entry directly as an integer dot product of columns of L. It recomputes the root/partition sums and counts monochromatic six-sets directly from adjacency matrices; it never reads the search `.coo`, `.meta`, numerical SDP matrices, or numerical solver results.

It also expands all permutations of the 1,044 graph representatives and checks that their orbits are disjoint and cover **every** one of the 2^21 labelled graphs. Consequently the public graph6 file is not trusted as an exhaustive list merely on the basis of its size or provenance. The flag orbit maps must be complete, have no duplicate classes, and have the stated root type.

All final operations use signed 128-bit integers with overflow checking on every addition, subtraction and multiplication. Overflow causes failure. A successful run is exact integer arithmetic, not a modular or floating-point check. Multiplying (1) by the positive common denominator turns it into the integer inequality checked by the program.

For each frozen artifact the exact minimum slack and its graph index are recorded in its verification log. The primary artifact has strictly positive slack; see `verify7fullsingle.log`. The auxiliary artifact also passes, at the weaker bound 11837/10^9.

For the primary certificate, the smallest exact slack is

    7685674099218500000000 / 4410000000000000000000000000000 > 0,

at graph index 68. The verifier also checks that the uniform random colouring, weighted by the exact sizes of the isomorphism orbits, has monochromatic six-set density exactly 1/16384. This checks the normalization on the same enumerated universe.

An additional implementation, `verify_python.py`, uses Python arbitrary-precision integers for all Gram products and coefficient inequalities. It recognizes flags using nauty rather than either C++ implementation's algorithm. It generates all graph classes independently by adjoining a vertex with every possible neighbourhood at orders 1 through 7, and checks that this enumeration equals the supplied graph6 file. Its exact minimum slack agrees with the C++ verifier. The primary proof needs only the self-contained C++ verifier; the Python/nauty implementation is corroboration.

The index refers to the zero-based order in `sources/graph7.g6`; no semantic property of this particular graph is needed.

## 5. Why these coefficients have nonnegative asymptotic expectation

Fix a block Q and a graph G on N>=7 vertices. Choose an ordered root tuple R uniformly among its (N)_t possibilities (or an unordered t-subset in root_mode=0). If its type is not sigma, the block contribution is zero. If its type is sigma, sample an m-subset A uniformly from V(G)\R. Let x_R(i) be the probability of its flag class i. If A and C are sampled **independently** from those m-subsets, then

    E[Q[class(R,A),class(R,C)] | R] = x_R^T Q x_R >= 0.          (2)

Let M_Q=max_{i,j}|Q[i,j]|. Every term in this expectation has absolute value at most M_Q. Conditional on A, each one of its m vertices belongs to C with probability m/(N-t). By the union bound,

    epsilon = Pr(A intersects C | R) <= m^2/(N-t).              (3)

There are disjoint choices because N-t>=2m. For any random variable Y with |Y|<=M_Q and event E of probability 1-epsilon>0,

    E[Y] = (1-epsilon) E[Y|E] + epsilon E[Y|not E],
    |E[Y|E]-E[Y]| = epsilon |E[Y|E]-E[Y|not E]|
                      <= 2 M_Q epsilon.                       (4)

The epsilon=0 case is immediate. Applying (4) to the event of disjointness and using (2)–(3) proves

    E[Q[class(R,A),class(R,C)] | R, A disjoint C]
        >= -2 M_Q m^2/(N-t).                                 (5)

Now select a uniform seven-subset S of V(G), and perform the root/partition experiment of section 4 inside S. Its joint distribution is exactly: a uniform ordered t-tuple R of V(G) (or an unordered t-subset in mode 0), followed by an ordered pair of uniformly chosen disjoint m-subsets A,C outside R. This follows either by counting the unique union S=R union A union C, or by noting that every disjoint ordered triple of the required sizes has the same probability. Therefore (5), also averaging over root sets of the wrong type with contribution zero, gives

    E_S a_Q(G[S]) >= -2 M_Q m^2/(N-t).

Summing over the finitely many blocks gives

    E_S a(G[S]) >= -sum_Q 2 M_Q m_Q^2/(N-t_Q).                 (6)

The sum tends to zero as N tends to infinity, because all matrices and parameters are fixed finite rational data.

Finally E_S p(G[S])=M_6(G)/binomial(N,6): each six-set is contained in the same number of seven-sets. Average (1), use (6), and obtain the explicit finite inequality

    M_6(G)/binomial(N,6)
        >= b - sum_Q 2 M_Q m_Q^2/(N-t_Q).                      (7)

Minimize over G and let N tend to infinity. This proves c_6>=b. Every limiting error has been displayed; there is no assumption that disjoint finite samples are independent.

## 6. Reproduction and scope

From this directory, compile and run

    g++ -O3 -std=c++17 verify_exact.cpp -o verify_exact
    ./verify_exact c6_7full_single.cert sources/graph7.g6
    ./verify_exact c6_7.cert sources/graph7.g6

For the additional Python replay, install pynauty in an isolated environment and run

    python verify_python.py c6_7full_single.cert sources/graph7.g6

The verifier requires only a C++17 compiler supporting checked `__int128` arithmetic. It requires no SDP solver or external mathematical library. The search is a way of finding the integer data, not part of the validity of the certificate.

This verifies a numerical lower bound through the written reduction. It does not establish uniqueness, optimality of the relaxation, mathematical priority, independent human review, or correctness of unrelated upper-bound certificates. Candidate and unrefereed throughout.
