# First moment for Erdős #1182

I use the problem page's F, the largest integer edge budget for which every connected n-vertex graph is triangle-good. Its f is the maximum edge count of an individual connected good graph. The older [BEFRS80] uses a different letter convention. All logarithms are natural.

## What is counted

Colour the edges of the balanced blow-up of the 5-cycle red and the other edges of the complete graph blue. There are N=2n−1 vertices. Write N=5h+s, 0≤s<5. Exactly s red-independent parts have size h+1 and the others size h. There is no red triangle. Let A_ij be 1 when j−i mod 5 is 0, 2 or 3, and 0 otherwise. A blue embedding of a simple graph G induces a map of its vertices to part indices with counts v_i≤k_i and with A_ij=1 on every edge. Conversely such a map can be injected part by part. The existence events are identical.

For a fixed map of type v there are exactly ∏(k_i)_{v_i} injections extending it, with falling factorials. Thus the literal expected number of labelled embeddings is the sum over v of the expected number of valid maps of that type times this factor. The decaying first moment is for **part assignments**, with each injection family counted once. Taking the unnormalised injection count instead would introduce an n log n term.

## Pairing count and exponent

Give each vertex d labelled stubs, except that for odd n and d=11 give one distinguished vertex 10 stubs. Pair all D stubs uniformly. For d=10 superimpose m=⌊rn⌋ independent uniform unordered pairs of *distinct* vertices, with replacement across draws, independent of the pairing; repeats and existing edges are allowed. Use r=3/100 for the target, 0 and 3/200 for controls. Delete loops and identify parallel edges to obtain the witness. A loop always has an allowed colour pair and duplicate edges repeat the same constraint, so this operation preserves the set of valid maps.

Write a_i=v_i/n, S_i for the number of stubs of colour i, and b_i=S_i/D. For one allowed integer type, with k_ii internal pairs and k_ij unordered off-diagonal pairs, dividing the ways of assigning stubs to partners by internal pair symmetries gives the exact probability
[
\frac{\prod_i S_i!}{\prod_i 2^{k_{ii}}k_{ii}!\prod_{i<j} k_{ij}!}\,
\frac{2^{D/2}(D/2)!}{D!}.
]
The constraints are 2k_ii+Σ_{j≠i}k_ij=S_i. Form a symmetric probability matrix Q with Q_ii=2k_ii/D, Q_ij=Q_ji=k_ij/D, supported by A, with row sums b. Inserting log(k!)=k log k−k+O(log(D+2)), including k=0 with 0 log 0=0, the log of this probability equals
[
 D\sum_i b_i\log b_i-\tfrac D2\sum_{ij}Q_{ij}\log Q_{ij}+O(\log(n+2)).
]
Indeed the log D and linear terms cancel by the row and total constraints, and the diagonal factors of 2 cancel those from using two orientations. The error has a uniform absolute bound C log(n+2) since the number of factorials is fixed and d≤11. We use its upper side. There are at most (D+1)^10 pair types and (n+1)^5 profiles. The multinomial map count is at most exp(n H(a)) by the multinomial theorem, where H(a)=−Σ a_i log a_i.

Define P(a)=aᵀAa=1−2Σ a_i a_{i+1}. One extra edge succeeds with probability (nP(a)−1)/(n−1)≤P(a). All m draws succeed with probability at most P(a)^m ≤ 5 exp(n r log P(a)), since P≥Σ a_i²≥1/5. Only these extra draws are independent. For regular pairing b=a and D=dn. Enlarging integer types to every real symmetric Q≥0 with row sums a supported by A gives the upper rate
[
 L_{d,r}(a)=(d-1)\sum a_i\log a_i+
 \tfrac d2\max_Q[-\sum Q_{ij}\log Q_{ij}]+r\log P(a).
]
This is an entropy maximisation over edge distributions, not an independent-edge estimate. Summing the exponential bounds gives E X ≤ poly(n) exp(n max L). For odd n and d=11, D=11n−1 and r=0. Each |a_i−b_i|≤1/D. The change in nH from a to b is O(log(n+2)), by integrating |1+log x| on intervals of length ≤1/D (largest singular contribution at zero). Replacing D by 11n costs O(1) since entropies on at most 25 cells are bounded. The same upper rate applies at b, summing over at most five possible colours of the distinguished vertex.

The exact part caps imply a_i≤(2n+3)/(5n). The stub fractions are ≤(2n+3)11/[5(11n−1)] in the defective case. Consequently every required profile is covered by Σa=1, 0≤a_i≤4001/10000 for n≥7000. This explicit threshold covers rounding; exponential decay against a polynomial gives existence for sufficiently large n.

## Dual

Given any five positive numbers t_i set Z=Σ A_ij t_i t_j. The distribution B_ij=A_ij t_i t_j/Z has log density log t_i+log t_j−log Z on its support. Nonnegativity of the relative entropy of Q against B gives H(Q)≤log Z−2Σ a_i log t_i. This is the row-constraint Lagrange dual with the mass multiplier minimised analytically. Equality holds when B has rows a. The per-profile primal-dual gap equals (d/2) times that relative entropy. Only positivity of t is needed for certification.

## Floating search, frozen before certificate production

At uniform cap 0.4001, deterministic multistart SLSQP over supports of size 3, 4, 5, with Newton row scaling for the inner problem, gave the following candidate maxima. These are numerical lower-side estimates of the supremum, not upper certificates. The raw profiles and final digits are in float.json. Reproduce with `./run float_search.py`.

|d|r|candidate maximum|
|---:|---:|---:|
|11|0|−0.10524721637577039|
|10|0.03|−0.0013683343796161967|
|10|0|+0.004031321470516769|
|10|0.015|+0.001331091081370361|
