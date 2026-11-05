# Exact K5 upper candidate

Candidate and unrefereed. Two separately written (same agent) exact counting implementations agree. They were prepared in one Codex session; both share the same agent authorship, and there is no human referee. No priority or optimality claim is made. See PRIOR_ART.md for the public methods and comparisons.

The selected certificate establishes

    c5 <= 15058298592194934908767847 / 9131939205947984819238469632
       < 0.001648970526.

This improves round 3's exact upper candidate. This release contains upper-bound material only.

## Construction

Partition the unit interval into 256 equal parts indexed by x in F_2^8, encoded as integers 0,...,255. For two sampled parts x,y let z=x XOR y. The red probability is q(z); blue is its complement. Define two 256-bit masks, with bit z counted from the least significant bit:

    H = 173e5ee876e8e880167c7ae06ec8a801173e5ee876e8e880e88181178117177e
    F = 0040200008000001010204081020408000402000080000010000000000000000

If bit z of H is one, set q(z)=1. If bit z of F is one, set q(z)=2648/4041. Otherwise set q(z)=0. The two masks are disjoint. There are 120 hard-red entries, 16 fractional entries and 120 zero entries. In particular q(0)=0. The fractional indices are

    64,91,109,118,135,142,149,156,
    163,170,177,184,192,219,237,246.

The complete integer matrix at denominator 4041 is frozen in certificates/c5_cayley256_fine.json.gz. Its generation-time UNVERIFIED label is historical; the later acceptance receipt fixes the same frozen hash and both successful exact replays. The companion kernel and two-mask files are readable definitions; the exact checkers replay the same full matrix. Matrix diagonal entries describe edges between distinct vertices sampled in the same part, so repeated part assignments must be counted.

For every N>=5, sample each vertex's part independently and uniformly and colour edges independently with these probabilities. The expected fraction of monochromatic K5 is exactly

    t(K5,W)+t(K5,1-W).

Consequently some colouring has no larger density. Passing to the asymptotic minimum gives the claimed upper bound once the displayed rational density has been counted exactly.

## Exact probability formula

Keeping the two masks fixed and replacing 2648/4041 by a variable p gives

    f(p) = (8734 - 5530p + 4320p^2 - 410p^3
                  + 395p^4 - 60p^5 + 10p^6) / 4194304.

For every fractional connection z, the parity of the set bits of 73 AND z is one. Fractional edges therefore cross the binary cut x -> parity(73 AND x). Among five sampled vertex positions there are at most six crossing pairs, even with repeated part assignments. Each red or blue clique product consequently has degree at most six in p. Seven exact evaluations at p=0,1/6,...,1 determine the displayed polynomial. Both counting implementations agree separately on red and blue at all seven points; the interpolation and receipt are in scripts/cayley_probability_polynomial_r4.py and receipts/cayley_probability_polynomial.json. Substitution of 2648/4041 reproduces the selected exact fraction, and 19/29 reproduces the simpler alternative.

This one-parameter family is strictly convex on [0,1]: the numerator of f'' is 8640 - 2460p + 4740p^2 - 1200p^3 + 300p^4, which is at least 4980 there. Its derivative changes sign from negative to positive, so its unique minimizing probability is approximately 0.6552833343924607. This is a statement about the fixed-mask probability family, with no global optimality claim for graphons.

## First exact count: a generic full matrix

check_wide.cpp uses no Cayley or transitivity assumption. It enumerates every distinct support of a five-tuple and every positive occupancy vector summing to five. For support vertices a_i with occupancies c_i, its edge numerator is

    product_i R[a_i,a_i]^(c_i(c_i-1)/2)
      * product_{i<j} R[a_i,a_j]^(c_i c_j),

and its ordered multiplicity is 5!/product_i(c_i!). It repeats this with D-R for blue. All masses are equal, and the denominator is D^10 * 256^5. Zero-probability support edges permit exact pruning.

The checked input range D<=4096 ensures that every ten-edge product is at most 2^120. Multiplying by the ordered multiplicity (at most 120) stays below 2^127, so unsigned 128-bit multiplication is exact. A two-word import transfers each product to GMP; arbitrary-precision GMP integers accumulate and reduce the result. The range checks are proof inputs, not numerical heuristics.

## Second exact count: root-fixed kernel enumeration

check_cayley_matrix_r4.py, separately written (same agent), checks that the frozen matrix has unit masses, n a power of two, entries in range and R[x,y]=R[0,x XOR y] for every pair. Translations of F_2^8 therefore act transitively and preserve every edge probability. Fix the first sampled part to zero.

check_cayley_exact_r4.cpp reads the extracted kernel, without any search histogram. It enumerates all weakly ordered remaining four part indices, including repetitions, and uses multiplicity 4!/product_j(m_j!). It multiplies the four probabilities from zero and the six pair probabilities among the remaining parts. All arithmetic, including intermediate products, is arbitrary-precision GMP. Its denominator is D^10 * 256^4.

The two methods agree separately on red and blue: each generic full-matrix numerator is exactly 256 times the corresponding root-fixed numerator. They also agree on the reduced density and the hash of the frozen full matrix.

## Controls and status

The retained controls compare both counters with literal ordered five-tuples on 24 small random Cayley matrices, and the generic counter with 12 arbitrary symmetric matrices that include arbitrary within-part probabilities. Denominators include 1,7,36,1000 and 4096. Ten malformed inputs are rejected. Both final matrix replay paths also reject a threshold strictly below the selected density. The exact acceptance receipt fixes compressed and uncompressed hashes, raw red/blue totals, the reduced fraction and comparison with the exact release threshold.

Discovery used negative Hessian directions in a folded-Hamming layer family, followed by unrestricted binary Cayley polishing. Standard constructions and methods are credited to Thomason, Parczyk–Pokutta–Spiegel–Szabó ([PPSS](https://arxiv.org/abs/2206.04036)), Razborov, Kiem–Pokutta–Spiegel ([KPS](https://arxiv.org/abs/2312.08049)), Jeetu SK ([SK2026], [#277](https://github.com/teorth/optimizationproblems/pull/277)), and this PR (#307)'s earlier Ricardo Pinho symmetry-breaking candidate ([Pin2026], [#307](https://github.com/teorth/optimizationproblems/pull/307)) and round 3 ([Pin2026r3]). Neither a floating objective nor a solver status enters the proof.

The simpler probability 19/29 on the same sixteen entries also has a separately replayed exact upper certificate, certificates/c5_cayley256_simple.json.gz, giving 4113966854539/2494869834563584. Its earlier acceptance receipt is retained; the selected fraction is smaller. This optional alternative is not the headline certificate. The selected probability 2648/4041 improves this by about 1.29e-11; the proof and the two primary replay algorithms are otherwise the same.

## Prior announcement and AI review

Noam Feinstein announced c5 < 0.001652 at the [Technion seminar on
21 January 2026](https://math.technion.ac.il/events/noam-feinstein/).
The [RSA 2025 abstract](https://dmg.tuwien.ac.at/rsa2025/) identifies the
research as joint work with Chaim Even-Zohar. This is an announcement with
no public certificate we could check. Its displayed upper threshold is
stronger than our round-3 0.001653032 and weaker than this round.

Written and checked by AI agents under Ricardo Pinho's direction. See
review/README.md for the two AI review statuses and the release corrections.
There is no human referee. Candidate and unrefereed.
