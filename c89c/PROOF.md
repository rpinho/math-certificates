# A rational lower bound for the K6 Ramsey multiplicity constant

**Candidate, unrefereed.** The result is

    C89c = c6 >= 21083/1000000000 = 0.000021083
             = 0.345423872 * 2^-14.

This is a computer-assisted conditional-square (flag-algebra) proof. The method is standard, following Razborov and its use for clique multiplicities by Parczyk–Pokutta–Spiegel–Szabó. No novelty, optimality or priority claim is made for the method. The integer certificate and its implementations were produced in this job. PRIOR_ART.md records the source audit and qualifications. The proof uses no numerical Ramsey-number bound.

## 1. Definition and normalization

For a red/blue colouring G of K_N, let M6(G) count the unordered six-element vertex sets whose fifteen edges have one colour. Put c6(N)=min_G M6(G)/binomial(N,6). If N>=q>=6, sampling a uniform q-subset gives expected monochromatic six-set density exactly M6(G)/binomial(N,6), because every six-set has the same containment probability. This expectation is at least c6(q), so c6(N)>=c6(q). The nondecreasing sequence is bounded by 1; hence its limit c6 exists.

This is precisely the normalization of C89c in PR #279. The factor 2^-14 is the random-colouring density, not a factor in the definition. The independently checked certificate establishes the unscaled value 0.000021083 above.

## 2. Flag classes and the rational certificate

A graph on ordered vertices 0,...,s-1 is encoded by its red-edge bits, with bit 0 first, in the order

    (0,1), (0,2), (1,2), (0,3), (1,3), (2,3), ... .

A flag of parameters (t,m) is an induced graph on t+m vertices with its first t vertices distinguished as an **unordered root set**. Two flags have the same class if an isomorphism sends the root set to itself. Root permutations and non-root permutations are allowed independently; a root cannot be exchanged with a non-root. Both edges and nonedges are respected. The root type is the isomorphism class induced by the roots.

For each root type sigma, list all flag classes F_1,...,F_d with the chosen parameters. The primary certificate uses:

| t | m | root types | denominator for an eight-vertex coefficient |
|---|---|---|---|
| 2 | 3 | the two graphs on two vertices | binomial(8,2) binomial(6,3) = 560 |
| 4 | 2 | the eleven graphs on four vertices | binomial(8,4) binomial(4,2) = 420 |

Thus there are 13 blocks, and t+2m=8 in each case. For any fixed root set of the right type in a larger graph, probabilities of these flag classes form a vector x with nonnegative entries summing to 1.

The first line of `c6_8.cert` is

    8 6 1000000000 13 21083 1000000000 0

Its fields are `n k D block_count b_num b_den root_mode`. Thus n=8, k=6, D=10^9 and b=b_num/b_den=21083/10^9. Mode 0 denotes unordered roots. For each block the next line gives `t m type_code d h`, followed by d flag codes and then h rows of d signed integers forming a matrix L. The field h is the number of factor rows; no independence of those rows is asserted. The rational matrix associated to the block is

    Q = L^T L / D^2.

For every real vector z,

    z^T Q z = sum_r (sum_i L[r,i] z_i / D)^2 >= 0.             (1)

This explicitly proves positive semidefiniteness over the rationals. There is no eigenvalue tolerance or numerical positivity assumption. Exactly zero rows and the wholly zero empty-root family were removed without changing any Gram product. There are 793 stored factor rows in the primary file.

## 3. Exact finite coefficient inequalities

Fix any red/blue graph H on eight vertices. For a block Q with parameters (t,m) and root type sigma, choose a t-subset R of V(H) uniformly, followed by an m-subset A of V(H)\R uniformly. Put B=V(H)\(R union A); then |B|=m. If H[R] has type sigma, let i and j be the flag classes of H[R union A] and H[R union B]. If its type differs, this block contributes zero. Define

    a_Q(H) = sum_{R,A} 1_{type(H[R])=sigma} Q[i,j]
             / [binomial(8,t) binomial(8-t,m)].              (2)

Both orders (A,B) and (B,A) occur in the sum. Consequently each off-diagonal matrix entry is counted for each of its ordered occurrences; no factor of two is omitted. Set a(H)=sum_Q a_Q(H) over the 13 blocks, and p(H)=M6(H)/28, since binomial(8,6)=28.

The finite assertion checked by the independent verifier is

    p(H) - a(H) - b >= 0                                    (3)

for every graph H on eight vertices.

Both p(H) and a(H) are invariant under relabelling H. A vertex bijection sends six-subsets to six-subsets and root/partition choices (R,A,B) to root/partition choices of the same sizes, preserving the root type and both flag classes. It therefore preserves every summand in (2) as well as the denominators. Thus one verified representative of every isomorphism class suffices for (3) for all labelled graphs.

The self-contained C++ program `verify_exact.cpp` reads only the certificate and `sources/graph8.g6`. It checks (1) by forming the integer column dot products of L, recognizes flag classes by expanding permutation orbits, directly recounts monochromatic six-sets from adjacency matrices, and directly enumerates all root/partition choices in (2). It does not read the search coefficient tables, search metadata, numerical matrices or numerical solver results. The search generator instead uses canonical representatives and a sparse coefficient matrix.

The verifier also expands all permutations of all 12,346 graph representatives. Their orbits must be disjoint and cover every one of the **268,435,456 = 2^28 labelled graphs**. Thus the graph6 list's exhaustiveness is checked, rather than trusted from its source or advertised cardinality. Rooted-flag orbit tables must also be complete and have no duplicate classes or wrong root types.

All coefficient decisions are integer cross-multiplications. The C++ integer wrapper checks every addition, subtraction and multiplication for signed 128-bit overflow; overflow causes failure. A successful pass is exact arithmetic. Its smallest slack is

    56963049278016000000000
    / 47040000000000000000000000000000 > 0,                  (4)

at graph index 198 in the supplied file's zero-based order. That index has no further mathematical significance. The same enumeration verifies that uniform random colouring has density exactly 1/16384, checking the normalization.

An additional Python implementation, `verify_python.py`, uses arbitrary-precision integers for all Gram and coefficient arithmetic. It recognizes flags through nauty rather than either C++ algorithm. It reconstructs all graph classes independently by adjoining a vertex with every possible neighbourhood, at every order from 1 through 8, and checks equality with the supplied graph list. This augmentation is exhaustive by induction: deleting a vertex from any graph gives one of the previous classes, and every possible new neighbourhood is tried. Its final class counts and coefficient inequalities are independently checked. The verification logs record its exact slack for comparison. The C++ proof path needs no nauty or SDP library.

## 4. Nonnegative asymptotic expectations, with the error explicit

Let G be any graph on N>=8 vertices and fix a block Q. Choose a root t-set R uniformly. If its type differs from sigma, define this block's contribution as zero. Otherwise let x_R(i) be the probability that a uniform m-subset A outside R gives flag class i. If A and C are chosen **independently** from the m-subsets outside R, then

    E[Q[class(R,A),class(R,C)] | R] = x_R^T Q x_R >= 0.       (5)

Let M_Q=max_{i,j}|Q[i,j]|, a fixed finite rational number. Every term in the expectation is bounded in absolute value by M_Q. Conditional on A, each of its m vertices belongs to C with probability m/(N-t). The union bound gives

    epsilon = Pr(A intersects C | R) <= m^2/(N-t).           (6)

The disjointness event has positive probability because N-t>=2m. For any random variable Y with |Y|<=M_Q and event E of probability 1-epsilon>0,

    E[Y] = (1-epsilon) E[Y|E] + epsilon E[Y|not E],
    |E[Y|E]-E[Y]| = epsilon |E[Y|E]-E[Y|not E]|
                  <= 2 M_Q epsilon.                        (7)

The epsilon=0 case is immediate. Applying (7) to disjointness, and then (5)–(6), gives

    E[Q[class(R,A),class(R,C)] | R, A disjoint C]
        >= -2 M_Q m^2/(N-t).                               (8)

For a root set of the wrong type, the zero contribution also satisfies this lower bound.

Choose now a uniform eight-set S in V(G), and perform the experiment of (2) inside G[S]. The joint distribution of (R,A,B) is exactly a uniform root t-set in G followed by a uniform ordered pair of disjoint m-subsets outside it. Indeed, every such triple has the unique union S=R union A union B of size eight, and every triple has the same probability under both procedures. Therefore averaging (8) over R gives

    E_S a_Q(G[S]) >= -2 M_Q m^2/(N-t).

Sum over the 13 fixed blocks:

    E_S a(G[S]) >= -sum_Q 2 M_Q m_Q^2/(N-t_Q).              (9)

Also E_S p(G[S])=M6(G)/binomial(N,6), by the same equal-containment counting used in section 1. Average the verified inequality (3), then use (9):

    M6(G)/binomial(N,6)
        >= b - sum_Q 2 M_Q m_Q^2/(N-t_Q).                  (10)

This is an explicit finite bound, valid for every G and N>=8. All matrices and block parameters are fixed finite data, so the sum on the right tends to zero as N tends to infinity. Minimize over G and take the limit to obtain c6>=b. No step assumes that disjoint finite samples are independent; their difference from independent sampling was bounded in (6)–(8).

## 5. Verification and qualifications

From the artifact directory:

    g++ -O3 -std=c++17 verify_exact.cpp -o verify_exact
    ./verify_exact c6_8.cert sources/graph8.g6

For the additional replay, in an isolated Python environment with pynauty:

    python verify_python.py c6_8.cert sources/graph8.g6

The earlier, smaller seven-vertex certificates also pass their exact checks. `c6_7full_single.cert` gives 2431/125000000=0.000019448 using ordered roots; its full proof and format are in PROOF_7.md. It was regenerated with explicitly single-threaded solver settings. The eight-vertex artifact is the stronger primary result.

The numerical SDP and subsequent nonnegative block-weight LP only found the integer factors. Neither solver's status, floating-point objective, eigenvalues, rounding estimates nor claimed optimality is part of the proof. C++ rejection controls independently refuse a false bound, duplicated flag classes, incomplete graph coverage and overflowing integers. REPORT.md gives commands, provenance, audit limits and remaining work. This is a candidate, unrefereed computer-assisted result, not an independent human referee report or a priority assertion.
