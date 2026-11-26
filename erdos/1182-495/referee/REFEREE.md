VERDICT: HOLDS

I verified \(F(n)\le\lfloor99n/20\rfloor-1<4.95n\) for every integer \(n\ge450000\). My largest certified rate upper bound is strictly below \(-0.00150154465578\). At the threshold, my upper bound on the probability of either obstruction is below \(0.357093479729\). Together these give a connected counterexample to triangle-goodness at each order in the claim.

## The graph and the edge budget

I checked the universal quantifier directly. The official \(F(n)\) is the largest budget \(q\) for which every connected simple graph of order \(n\) and size at most \(q\) is triangle-good. Brandt calls this universal function \(f(n;3)\). BEFRS80 page 193 phrases its definition using exactly \(q\) edges. The two conventions agree over feasible sizes because adding edges to a bad graph on the same vertex set preserves connectivity and failure to embed in the same blue graph. Thus a connected bad graph of size \(e\) gives \(F(n)\le e-1\). Round 1's stated \(5n-1\) uses the same conversion. [Official statement](https://www.erdosproblems.com/1182) · [BEFRS80](https://www.renyi.hu/~p_erdos/1980-04.pdf) · [Brandt](https://ftp.math.fu-berlin.de/pub/math/publ/pre/1996/pr-a-96-24.ps)

I wrote \(n=20q+r\) and obtained \(n_9=2q+2\mathbf1_{r>0}\). Both degree counts are positive throughout the claimed range. The number of stubs is \(D=10n-n_9\), an even integer, and \(D/2=5n-\lceil n/20\rceil=\lfloor99n/20\rfloor\). The excess \(10n_9-n\) is zero for \(r=0\) and \(20-r\) otherwise. Dividing by \(10n\) gives the exact inclusion \(1/10\le\alpha_9\le1/10+19/(10n_0)\). I checked all 40 residue classes at the first eligible representative. Each increment by 40 adds \((4,36,396)\) to \((n_9,n_{10},D)\) and 198 to the edge budget. This proves the continuation on each class, including odd orders.

The red host on \(2n-1\) vertices is triangle-free. Its blue part relation allows identical labels and labels at cyclic distance two. I checked both directions of the map-to-embedding equivalence in §1 of the proof. A loop always satisfies the same-label test. Parallel edges repeat a single test. A feasible part assignment lifts by choosing an injection within each blue clique, and every embedding induces such an assignment. Thus simplification preserves the *set* of valid maps, preserves components and weakly decreases the edge count. My small multigraph control gave the same 30 part maps from exhaustive assignments and exhaustive injections. I use the probability of disconnection as a separate summand below. The argument requires no estimate of the probability that a pairing is simple.

## Lemma 2. Minimality and the recoloring

I minimize \(\sum v_i^2\) over valid maps. Moving one unit from \(i\) to \(j\) changes the potential by \(2(v_j-v_i+1)<0\) when \(v_i\ge v_j+2\). In that case \(v_j+1\le v_i-1\le h\), so the move fits even the smaller host parts. The capacities may be relabelled along with the parts. Every embedding has \(a_i\le2/5+3/(5n)<4001/10000\). Any two largest parts are adjacent or at distance two on the pentagon. In the second orientation the reflection fixing their unordered pair allows \(a_3\ge a_4\). Ties can be assigned either admissible orientation.

In Region C the gap \(v_0-v_3\), and also \(v_2-v_3\), is at least \(3n/20\). The same lower bound holds for \(v_2-v_4\). A vertex in 0 missing 2 can move to 3. A vertex in 2 missing 0 can move to 4. The incident non-loop edges stay blue and loops stay within a part. Minimality therefore requires both sets of hits.

Case I means **at most 19** vertices in 0 miss 3. If there are at least 20 and a pivot \(u\) in 0 sees only vertices of 2 missing 4, let \(r\) count its distinct neighbors in 2. Then \(1\le r\le d(u)\le10\). At least \(20-1-(d(u)-r)\ge r-1\) donors missing 3 are distinct from, and nonadjacent to, \(u\). Move the pivot to 3, all \(r\) neighbors to 0, and \(r-1\) donors to 2. The net move is \(2\to3\). At the pivot the new neighbor labels are 0 and 3. At a moved neighbor they are among 0, 2 and 3. At a donor they are among 0 and 2. These sets permit every incident pair, including loops and pairs between moved vertices. I also checked all 21 permitted unordered endpoint-role pairs in the code. The contradiction proves Case II and includes \(r=1\) with zero donors. Only the upper degree bound enters this swap.

## Pairing law and Lemma 3. Entropy and the dual

For fixed degree-part counts \(v_{di}\), I get exactly \(\prod_{d=9,10}n_d!/\prod_i v_{di}!\) maps, with the quotient taken separately for each degree. For one map put \(S_i=\sum_d d v_{di}\). A blue type \(K\) is symmetric, has row sums \(S_i\) and even diagonal. There are \(\prod_i S_i!/\prod_{ij}K_{ij}!\) assignments of labelled stubs to destination pools. I multiply by \(\prod_i(K_{ii}-1)!!\) for internal matchings and by \(\prod_{i<j}K_{ij}!\) for inter-part bijections. Dividing by the total \((D-1)!!\) gives
\[
 p_K=\frac{2^{D/2}(D/2)!\prod_i S_i!}
 {D!\prod_i 2^{K_{ii}/2}(K_{ii}/2)!\prod_{i<j}K_{ij}!}.
\]
Empty pools contribute one. Multiplying by the exact map count and summing over eligible profiles and blue matrices gives the unrestricted first moment. For a restricted count I multiply each summand by its conditional occupancy probability. The completion count depends only on \(K\), so the row assignments are conditionally independent and uniform, with independent uniform inter-pool bijections given those assignments. I reproduced all 16 observed type probabilities among the 105 labelled matchings of eight stubs.

I bounded each vertex multinomial by its entropy via the multinomial theorem. For \(m\ge1\), integrating \(\log x\) between 1 and \(m\) bounds \(\log(m!)\) below by \(m\log m-m\). The trapezoid sum lies below the integral by concavity, giving the upper bound \(m\log m-m+1+\tfrac12\log m\). The looser square root \(\sqrt{m+1}\) includes \(m=0\). Thus the six numerator factorials cost at most \(3^6(D+1)^3\). With \(a_{di}=v_{di}/n\), \(\alpha_d=n_d/n\), \(s_i=S_i/D\), \(Q=K/D\) and \(\bar d=D/n\), my remaining exponent per vertex is
\[
 L=\sum_d\alpha_d\log\alpha_d-\sum_{di}a_{di}\log a_{di}
   +\bar d\sum_i s_i\log s_i-\tfrac{\bar d}{2}\sum_{ij}Q_{ij}\log Q_{ij}.
\]
The two entries of an off-diagonal pair account for its full factorial contribution. I use \(0\log0=0\).

I expanded the relative entropy against \(B_{ij}=A_{ij}t_it_j S_{ij}/Z\), where here \(S_{ij}\) denotes the edge tilt of Lemma 3. It leaves the two penalties \(-\bar d Q_{ij}\log S_{ij}\) and \(-\bar d\,D_{\rm KL}(Q\Vert B)/2\). Adding \(\eta(\sum_i a_{9i}-\alpha_9)=0\) leaves separate one-variable maxima. For \(a=a_i>0,\ x=a_{9i}\), I maximize
\[
 (10a-x)\log((10a-x)/(\bar d t_i))-x\log x-(a-x)\log(a-x)+\eta x.
\]
Its second derivative is \(1/(10a-x)-1/x-1/(a-x)<0\). With \(\xi=x/a,\ \kappa=\bar d t_i e^{\eta-1}/a\), stationarity gives \(\xi(10-\xi)=\kappa(1-\xi)\). Writing \(y=1-\xi\) gives \(y^2+(8+\kappa)y=9\). Substitution of the interior root yields \(a[9\log a+10\log((9+y)/(\bar d t_i))-\log y+\xi]\). My implementation uses the rationalized positive roots for both \(y\) and \(\xi\), with value zero at \(a=0\). At fixed \(\xi\) the coefficient of \(a\log a\) is \(9-\xi>0\) and the rest is linear in \(a\). Taking the supremum preserves convexity, including at zero. This justifies vertex maximization for each allowed degree fraction.

## Lemma 4. Case I occupancy and the sign

I get the necessary cutoffs \(K_{03}\ge v_0-19\) and \(K_{02}\ge\max(v_0,v_2)\). In particular \(p_3=K_{03}/S_0\ge1/20\) and \(p_2=K_{02}/S_0\ge1/10\), since \(v_0\ge38\) and \(S_0\le10v_0\). The number-of-misses cutoff and the number-of-stubs cutoff point in opposite directions.

Under independent row-0 destination draws, the chance of seeing both 2 and 3 in a block of degree \(d\) is at most \(f_d(p_2)f_d(p_3)\), where \(f_d(p)=1-(1-p)^d\). This follows from \(1-p_2-p_3\le(1-p_2)(1-p_3)\). Both factors increase with \(d\). Conditioning the three destination counts costs at most \(27(D+1)^2\) by the factorial bounds above, including a category of size zero. Choosing the 19 exempt vertices costs at most \(n^{19}\). Restoring the two factors on those vertices costs at most \(200^{19}\) because \(f_{10}(p)\ge p\). The independent row-2 binomial conditioning costs at most \(D+1\), since its integer mean is a mode. Its every-vertex hit probability is bounded by \(f_{10}(K_{02}/S_2)^{v_2}\).

For a tangent to \(\log f_{10}\) at \(u\), the slope \(\beta>0\) and intercept \(\gamma=\log f_{10}(u)-u\beta<0\). Concavity gives an upper bound everywhere on \((0,1]\). The stub density obeys \(S_i/n\ge\max(9a_i,10a_i-\alpha_{9,\max})\). The ratio \(a/(10a-\alpha_{9,\max})\) decreases above \(\alpha_{9,\max}\), giving precisely the upper bounds \(\rho_i\) in the proof. I used \(\log S_{03}=\rho_0\beta_1\) and \(\log S_{02}=\rho_0\beta_2+\rho_2\beta_3\). Each residual coefficient of \(Q_{03}\) or \(Q_{02}\) is therefore nonpositive. The sign holds for both degrees.

## Lemma 5. Case II hot stubs and KL tails

Conditioned on row 2, the \(R\) hot partners land on a uniform \(R\)-subset of all \(S_0\) stubs. This uses both the uniform \(0,2\) bijection and the independent uniform choice of row-0 destination stubs. Binomial conditioning and a tangent bound its all-vertices-hit probability by \((D+1)e^{v_0\gamma}w^R\), with \(w=e^{\beta\rho_0}\). For \(R=0\) the hit event is empty. Conditioning the row-2 trinomial costs \(27(D+1)^2\). Taking the weighted expectation sums over every \(R\) once.

With row-2 destination probabilities \(p=q_0,\ q=q_4\), I split on whether a block has a 4. The moment of \(w^{n_0\mathbf1_{n_4>0}}\mathbf1_{n_0>0}\) is
\[
 (1+(w-1)p)^d-(1-q+(w-1)p)^d+(1-q)^d-(1-p)^d.
\]
Appending one stub can only increase the integrand when \(w\ge1\), proving \(M_9\le M_{10}\) for feasible probabilities. Both partial derivatives of the displayed polynomial are nonnegative throughout the whole unit square: each power difference in the derivatives in §5 has nonnegative base and ordered terms. This extends the coordinatewise upper bound to a cell corner even if its coordinates sum to more than one. I tested the identity against exact multinomial sums in 16 degree, probability and weight combinations, including zero categories.

Coarsening \(Q,B\) to an unordered blue pair and its complement gives binary KL with masses \(2Q_{ij},2B_{ij}\). On a nonempty upper tail I checked \(B_{ij}<h_{ij}<1/2\). The binary divergence increases beyond its reference mass. The tail is empty whenever the cutoff reaches the rational stub cap, using \(S_i/n\le\min(10\bar a_i,9\bar a_i+\theta_{\max})\). On each near cell I minimize each divergence by projecting its reference onto the closed interval. I subtract \(\bar d_{\min}/2\) times the **maximum** of the two resulting penalties. I use the upper endpoints for the arguments of \(M_{10}\), the lower endpoint of \(a_0\) for its negative intercept, and the larger endpoint product for \(a_2\log M_{10}\). Both signs of that logarithm are covered.

## Exact cover and independent replay

I read three preorder trees. Starting from the full five-coordinate box, each strictly interior split gives two closed children sharing the cut face. I required exact exhaustion of each tree. On the simplex slice I applied Region A, or each of the two branches of Region B, or both gap inequalities of Region C as appropriate. In B, \(\min(a_0,a_2)-a_3\le3/20\) is a **union**. In C the reversed weak inequality is an **intersection**. Both include their common boundary.

For a constraint \(a_i\ge a_j+g\), raising the lower endpoint of \(i\) to \(\ell_j+g\) and lowering the upper endpoint of \(j\) to \(h_i-g\) preserves every feasible point. The sum constraint likewise gives \(1-\sum_{j\ne i}h_j\le a_i\le1-\sum_{j\ne i}\ell_j\). I performed these operations in integer units of \(1/10485760000\) on the endpoints. Coordinates within each box are **real**. Contradictory bounds prove emptiness. Otherwise the contracted box intersected with the sum hyperplane contains the full regional piece. Any vertex of that outer slice has at most one free coordinate, since two free coordinates allow opposite small perturbations. Enumerating four endpoints and solving for the fifth therefore suffices, including lower-dimensional faces. This argument covers all of the 4D region without requiring a file of its vertices.

I evaluated the convex dual on those vertices, passing the full closed interval for \(\alpha_9\) as one outward-rounded Arb ball at 192-bit working precision. All splits, region offsets, profile vertices, support caps and KL cut comparisons use exact integers or rational numbers. I used the records only for splits, positive tilts, multipliers, rational tangent locations, and tail cutoffs. I computed the bound anew at every applicable leaf. The table gives upper endpoints rounded upward.

| Archive | Empty | Unrestricted | Occupancy | Slice vertices evaluated | Largest rate upper bound | Worst record, zero-based |
|---|---:|---:|---:|---:|---:|---:|
| A or B | 39 | 1,054 | 0 | 30,931 | −0.00156261056077 | 1,727 |
| C, Case I | 0 | 682 | 1,914 | 48,930 | −0.00150233734065 | 4,739 |
| C, Case II | 0 | 1,593 | 5,729 | 133,908 | −0.00150154465578 | 8,332 |

I checked 11,008 splits and 11,011 leaves. On the 5,729 Case II occupancy leaves I evaluated 366,656 near cells, all 5,729 tails for pair 02, and 2,335 tails for pair 24. The other 3,394 tails for pair 24 were empty by the exact cap test. The smallest clearance to the pass line exceeds \(1.54465\times10^{-6}\). The last digits of the computed bounds vary with the order of interval operations. Each displayed upper bound follows from my own enclosures.

| Compressed input | SHA-256 recomputed against the supplied manifest |
|---|---|
| cert_naive_ab.json.gz | 47f08e107625a0c6a0fdc7f4a91c170bad08145a6fccacf498576899fd3514d3 |
| cert_case1.json.gz | f463e313d6bda97a799e90dc2075471b18d4814aec7d07e4cd212b0478ac1de2 |
| cert_case2.json.gz | ce8ff7c984358add6bfc987ed125f77fbc9aba0a458f237548d81f54dcec134a |

## Finite sum, connectivity and continuation

I count at most 10 orientations and three bounds per orientation (A/B together, C-I and C-II). Every feasible map has a potential-minimal representative in at least one of these cases whenever any map exists. Each degree profile uses four freely chosen part counts per degree, at most \((n+1)^8\) choices. Each blue pairing matrix uses five off-diagonal entries, at most \((D+1)^5\) choices, since row sums determine the diagonal. I multiply by the pairing remainder \(3^6(D+1)^3\) and the uniform occupancy prefactor \(27(D+1)^3(200n)^{19}\). The resulting polynomial has degree **38**, and its factor involving \(10n+1\) has exponent **11**. For the map event I obtain
\[
 B(n)=30\,3^9(n+1)^8(10n+1)^{11}(200n)^{19}e^{-3n/2000}.
\]

For disconnection I sum over possible isolated sets of size \(1\le k\le n/2\). An odd number \(S\) of stubs cannot pair internally. For even \(S\) each of the \(S/2\ge9k/2\) exposures has conditional internal probability \((S-2j-1)/(D-2j-1)\le S/D\le(50/49)k/n<1\). The binomial count \((en/k)^k\) leaves \((k/n)^{7k/2}\le2^{-7k/2}\). Thus the geometric series gives \(\rho/(1-\rho)\), where \(\rho=e(50/49)^{9/2}2^{-7/2}\).

| Quantity at \(n=450000\) | My outward decimal enclosure |
|---|---|
| \(\log B\) | \((-41.068697064409,-41.068697064408)\) |
| \(B\) | \((1.459121598044,1.459121598045)\times10^{-18}\) |
| \(\rho\) | \((0.263131084971,0.263131084972)\) |
| \(\rho/(1-\rho)\) | \((0.357093479728537854,0.357093479728537855)\) |
| \(B+\rho/(1-\rho)\) | \((0.357093479728537856,0.357093479728537857)\) |

For real \(n\ge450000\) the log derivative is
\(8/(n+1)+110/(10n+1)+19/n-3/2000<38/n-3/2000\le-637/450000<0\).
The disconnection bound is constant throughout this range. The union bound is strictly below one, so some pairing is both connected and free of valid maps. Its simplification witnesses the integer bound in the verdict.

## Controls, contrary evidence and scope

**CONTROLS:** No. I checked the 14 named rejections in the reproduction command below. They cover the threshold, root, coefficient, missing leaf, duplicate leaf, boundary split, weakened leaf claim, false emptiness, removed Case I occupancy, perturbed interior tangents in both cases, an invalid KL tail, a reversed Case I cutoff, and failure of the finite bound at 400000. The leaf mutations go through the analytic checks in memory after the genuine compressed bytes pass SHA-256.

I retained an unsuccessful preliminary control. My first choice for removing Case I occupancy was the most restrictive Case I archive record, 4739. Inspection showed that it already used the unrestricted bound. Changing its advisory number left the analytic check passing, as it should. I located the independent positive witness in record 873, removed occupancy there and obtained a rejected rate. The full replay also rejected a perturbed Case II tangent on the witness's record 5948.

**CONTRADICTING:** No. In the verifier's positive_witness function I checked the support, symmetry, nonnegativity and row sums of an explicit rational matrix. Its unrestricted rate exceeds \(+0.00336352695\) for degree 10. Taking \(a_{9i}=a_i/10\) gives the same normalized stub rows and rate above \(+0.01436464953\) for the target mixture. Rational masses here can be realized as integer types by scaling to clear denominators and enforce even diagonals. These witnesses explain why unrestricted negativity fails. My 366,656 near-cell evaluations and 11,458 tail decisions include the regions where that evidence matters.

**LABELS:** No. In the verifier's walk, contract, vertices and evaluate functions I reconstructed all three covers from their split coordinates, derived emptiness on 39 leaves, and recomputed every numerical bound. All 3,329 unrestricted leaves used the analytic dual even when an archive supplied a diagnostic value. Replaying the finite expression used the stated \(n_0\), rate, and independently derived polynomial.

**Did I find something new? No.** I independently verified the submitted theorem. It improves the supplied Round 1 comparison in both coefficient and threshold. My verdict covers the theorem for \(n\ge450000\). The producer's exploratory crossing estimates, optimality of the coefficient and world priority are separate claims. An exact proof covering every feasible profile has no statistical target or holdout.

I found two bibliographic errors in the supplied prior-art note. Its BEFRS80 DOI points to a different paper, and the Nikiforov–Rousseau article ends on page 262. I give the corrected references in my prior-art note. These corrections leave the mathematical verdict intact. [Original BEFRS80 article](https://www.renyi.hu/~p_erdos/1980-04.pdf) · [Nikiforov and Rousseau publication record](https://digitalcommons.memphis.edu/facpubs/5557/)

## Reproduction

From this job directory I ran the following command using python-flint 0.9.0, one FLINT thread, and a 600-second alarm. It rereads the compressed inputs, prints every archive maximum and finite bound, runs the controls, and exits zero on success. My successful run used 47,415,296 bytes peak RSS. The submitted producer and verifier were withheld. I inspected public prior work separately.

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  nice -n 10 /Users/ricardo/dev/open-science/.venv/bin/python -Bu referee_verify.py
~~~
