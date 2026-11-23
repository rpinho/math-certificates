# From the pairing model to a Ramsey witness

The two certificates use the same domain and differ in the degree and extra-edge parameter. Here a is the vertex profile and b is the stub profile. Write c for the worst certified upper exponent in the applicable proof tree. Every row below applies to both parities.

| Step | Verdict | Basis |
|---|---|---|
| Balanced parts, assignment equivalence and triangle-free red graph | HOLDS | A triangle must project to a triangle of the 5-cycle. Partwise injections realise precisely the assignments of a simple graph. |
| Pairing rate and row constraints | HOLDS | Labelled-stub factorial count in DERIVATION.md. Six exact counts in controls.log, plus the finite coefficient inequality below. |
| Lagrange dual, including zero profile coordinates | HOLDS | Relative entropy against positive allowed weights. Boundary coordinates have continuous entropy and Arb uses monotone endpoint enclosures near zero. |
| Vertex bounds for the **combined** objective | HOLDS | Hessian estimate below for the logarithm of the extra-edge probability. |
| Coverage of the uniform capped simplex | HOLDS | Dihedral orbit argument below, both children at every split, strict empty-box tests, exact rational geometry. See coverage-11.log and coverage-503.log. |
| Strictly negative global bound | HOLDS | check-11.log and check-503.log. Every retained leaf has its own verified negative rational upper bound. |
| Finite part sizes and odd orders | HOLDS | Exact capacities and the single deficient stub described below. Both profiles fit the cap for every n≥7000. |
| Added edges, rounding, loops and parallel edges | HOLDS | Independent uniform unordered pairs of different vertices, sampled with replacement across draws. The floor costs a factor at most five. Simplifying preserves assignments and connectivity, and only decreases the edge count. |
| First moment to absence of assignments | HOLDS | Markov gives Pr(X≥1)≤E X. The finite bound below gives E X<1/2 throughout each stated range. |
| Connectivity and simultaneous existence | HOLDS | Fixed-degree configuration connectivity and the direct cut estimate below, valid also with the single defect. The two bad-event probabilities sum to less than one. |
| Ramsey and edge-budget conclusion | HOLDS | The resulting simple connected graph has no blue embedding on 2n−1 vertices. Its edge count e gives F(n)≤e−1. |

## Why the numerical leaves suffice

For positive t define Z=tᵀAt. The bound checked on a profile u is

$$
U(u;t)=(d-1)\sum_i u_i\log u_i-d\sum_i u_i\log t_i
         +\tfrac d2\log Z+r\log(u^TAu).
$$

The dual argument in DERIVATION.md gives L≤U, unchanged by scaling all t by the same positive constant. The checker uses the saved positive integers directly. Each region is a closed axis-aligned box intersected with the sum-one hyperplane. To keep the extra-edge factor at its actual vertex value, we prove convexity of the *whole* U on this domain. Put P=uᵀAu. Along a vector h, the second derivative of log P is

$$
2 h^TAh/P-4(h^TAu)^2/P^2.
$$

A is symmetric with three ones per row, so its operator norm is at most 3. Since each (Au)_i≤1, ‖Au‖²≤5. Also P≥Σu_i²≥1/5. The displayed expression is at least −530‖h‖². The other nonlinear term contributes at least (d−1)‖h‖²/0.4001. Hence the total is positive on the relative interior, since 9/0.4001−0.03·530>0. Continuity along segments to the uniform point proves convexity on the closed capped simplex, also on lower dimensional faces. In the 11 case r=0 suffices directly. The maximum of U on any nonempty closed polytope is at a vertex. Two coordinates strictly between bounds could move in opposite directions by a small amount, so each vertex is on a box edge. The checker visits those edges with rational endpoints, solves the sum constraint exactly, and removes coincident points.

Rotations of the cycle preserve every term and the matrix constraints. Rotate any largest coordinate into position 0. Reflect about 0 if necessary to make u₁≥u₄. The uniform cap is invariant under both operations. Ties need no uniqueness. Every orbit therefore meets the closed sector u₀≥uᵢ for all i, u₁≥u₄. The checker drops a box by symmetry only if an inequality fails *strictly throughout*. On numerically accepted boxes it certifies all simplex vertices, even outside the sector. This reduction is applied only after enlarging the nonuniform finite part caps.

The independent reader starts at [0,4001/10000]⁵, reconstructs both exact midpoint children for every recorded split, and allows elimination only by a strict sum or sector inequality. Each surviving leaf carries five positive weights and a signed integer bound in units of 10⁻¹⁰. verify.py recomputes U and proves it strictly below the stored rational at each vertex in 160-bit Arb arithmetic. For x≤1/4 the function x log x is decreasing, so the upper argument endpoint gives the lower function bound and the lower endpoint gives the upper bound (zero at zero). The two records of coverage were also replayed without reading numerical bounds. No statistical holdout applies to a universal certificate.

## A uniform finite bound, including the odd degree sequence

In the 11 case, give each of n vertices 11 stubs for even n, and give one fixed vertex 10 and all others 11 for odd n. In the 10 case use 10 stubs per vertex on all orders. Thus D is always even. With exact capacities k_i the vertex fractions are at most (2n+3)/(5n). For the single defect, b_i=(11n a_i−indicator_i)/(11n−1). This gives b_i≤11(2n+3)/[5(11n−1)]≤0.4001 for n≥7000, and |a_i−b_i|≤1/D. No pendant-vertex argument is required.

Here is an explicit prefactor for the first moment. It also supplies the finite bound tested against six exact pairing counts. Let S_i=Db_i, let z be a vector of formal variables and write [z^S] for coefficient extraction. Ordering the pairs and orienting them gives the exact allowed-pairing probability

$$
\frac{\prod S_i!}{D!}[z^S](z^TAz)^{D/2}.
$$

Indeed each oriented ordered list of colour pairs lifts to ∏S_i! lists of labelled stubs, and all D! stub orders have equal probability. Nonnegative coefficients give the upper bound Z^{D/2}∏t_i^{-S_i} for the coefficient. Multiplication by the number D!/[2^{D/2}(D/2)!] of pairings gives the integer-count bound used in controls.py.

The multinomial coefficient D!/∏S_i! is at least exp(DH(b))/(D+1)^5. Under the multinomial law of profile b, S is a mode: for each S_i>0, S_i^k/k! is maximised at k=S_i, and a zero-probability colour has count zero. Among at most (D+1)^5 count vectors a mode has probability at least (D+1)⁻⁵. The map count per profile is at most exp(nH(a)). Including the coefficient estimate, the exponent before the extra edges is at most

$$
n H(a)-D H(b)+(D/2)K(b,t),\qquad K=\log Z-2\sum b_i\log t_i,
$$

apart from the factor (D+1)^5. Each t_i²≤Z because A includes its diagonal, so K≥0.

For D=dn this expression equals the regular dual exponent without extra edges, multiplied by n. For the odd defect, write D=dn−1. The cost of replacing D by dn in the last two terms is H(b)−K/2≤log 5. Also n|H(a)−H(b)|≤log D+2. To see this, integrate |1+log x|≤1−log x over an interval of length 1/D inside [0,1]. Its integral is greatest at zero and is (2+log D)/D. Sum over five coordinates and use 5n/D≤1. This bounds even classes with zero stubs. The five possibilities for the distinguished vertex's colour cost a further factor at most five.

In the 10 case let m=⌊rn⌋. An unordered draw of a distinct vertex pair succeeds with probability (nP−1)/(n−1)≤P, with independent draws conditional on the map. Hence its contribution is at most 5 exp(nr log P). There are at most (n+1)^5 vertex profiles. Choose for each covered profile a certified leaf multiplier, conjugating by the sector symmetry when needed. Combining the preceding factors, a common upper bound is

$$
\mathbb E X\ \le\ 125 e^2(11n+1)^6(n+1)^5 e^{cn},\qquad n\ge7000.
$$

The constant allows all three factors of five even when they cannot occur together. The power six absorbs the factor D from the entropy perturbation and the five powers from the multinomial estimate. This argument uses the exact generating polynomial and supplies a finite counterpart of the Stirling derivation.

For d=11 take c=−0.0001800948 and n₀=10⁶. For d=10, r=0.03 take c=−0.0000003225 and n₀=10⁹. At these n₀ the log upper bounds are below −6.908 and −73.328 respectively. The derivative of the log upper bound is at most 11/n+c<0 for every larger n. Thus E X<1/2 for every n≥n₀ in its case. finite.py evaluates the endpoint inequalities with Arb. These conservative explicit thresholds make no claim about the least possible n₀.

## Connectivity, simplification and the witness

The standard fixed-d≥3 connectivity result is discussed by N. C. Wormald, *Models of random regular graphs*, Surveys in Combinatorics 1999, pp. 239–298, and B. Bollobás, *Random Graphs*, 2nd ed. (2001), as cited in the supplied preprint. One can check the unconditioned version for every fixed d≥3 directly. For k vertices, x=k/n≤1/2, an even number dk of stubs is internally closed with probability binom(dn/2,dk/2)/binom(dn,dk). An odd number has probability zero. For k≤n/100, sequential pairing and the choice of the vertex set give the bound [e x^(d/2−1)]^k. The base is at most e/10 and the fixed-k terms tend to zero, so this range sums to o(1) by geometric domination. For 1/100≤x≤1/2, the entropy bounds for binomial coefficients give a union-bound term at most (dn+1) exp[−(d/2−1)n h(x)], where h is binary entropy. The lower entropy bound in the denominator follows from the same mode argument used above, with at most dn+1 outcomes. Here h(x)≥h(1/100)>0, so even the sum of n such terms vanishes. Thus a uniform regular pairing is connected with probability tending to one for all admissible orders.

For the two degrees in this replay the following stronger finite cut bound also covers the odd near-regular sequence.

If the pairing is disconnected, some k≤n/2 vertices have all their s stubs paired internally. Odd s makes this impossible. For even s, exposing internal partners successively gives probability ∏_{j=0}^{s/2−1}(s−2j−1)/(D−2j−1)≤(s/D)^{s/2}. Here 10k≤s≤11k and D≥10n. Union bounding over at most (en/k)^k vertex sets gives a contribution at most

$$
[e(11/10)^5(k/n)^4]^k.
$$

For k≤n/2 its base is at most ρ=e(11/10)^5/16<0.274, giving total probability at most ρ/(1−ρ)<0.377 for every order under consideration. It even tends to zero, since each fixed-k bound vanishes and the geometric series dominates. This verifies connectivity for the cases used without transferring a theorem for simple regular graphs to an unconditioned irregular pairing.

The event “disconnected or admits an assignment” has probability less than 0.377+1/2<1. Thus some connected multigraph with the specified extra draws admits no assignment. Adding edges preserves connectivity. Deleting loops and retaining one copy of each nonloop edge preserves connectivity and exactly the same forbidden-pair constraints. Its simple underlying graph G has n vertices and at most ⌊11n/2⌋ edges in the first case, or 5n+⌊3n/100⌋ in the second.

The complete graph on 2n−1 vertices now has a colouring with triangle-free red graph and no blue G. Thus R(K₃,G)>2n−1. Since a connected non-good graph with e edges violates the universal property at q=e, F(n)≤e−1. This proves each requested inequality for **every** n from its stated threshold.
