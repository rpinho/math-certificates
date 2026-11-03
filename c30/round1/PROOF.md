# Baseline proof notes and pilot scope — candidate, unrefereed

These are the initial baseline and reduced-model notes. The final candidate proof of 521/50 is in **FIRST_MOMENT_PROOF.md**, with its separate candidate certificate. The baseline certificate discussed below replays the **external Norton v3 baseline**, conditional on the combinatorial results listed in REFEREE.md. See RELEASE_NOTES.md for the source-digest provenance check used by this trimmed release.

## Baseline implication

For a cell whose ordered free-strip sizes are a_i, the one-sided weighted count is the product of H_{a_i}. Here Q(z)=(1-sqrt(1-4z))/2 and H_j=(d/dz)^j[z^j/(1-qQ(z))]/j!. BBEP's published balanced domino family has growth 27/4 and meets every strict leaf/empty-strip lower threshold alpha<5/9, beta<5/27. Imposing restrictions on surplus leaves, then applying coefficientwise log-convexity of H_j, bounds every such cell's one-sided count below by a common equitable strip profile. Its limiting entries are eta0=beta, eta2=3-4alpha-3beta, eta3=3alpha+2beta-2.

At a fixed component count c and free connecting-cell size, each component size has law proportional to Catalan(k-1)*z^k. Both neighbour-placement counts increase in each size. The product-measure association argument therefore bounds the true shared-cell count below by the product of its two marginal sums divided by Q(z)^c. This step never replaces actual adjacent cells by unrelated independent neighbours and never claims a coefficientwise inequality in z.

Set B(q)=-kappa*log(q)+sum_j eta_j*log(H_j(z,q)). Its derivative in w=log(q) is nondecreasing, because each log(H_j(z,exp(w))) is convex. A negative derivative at q1 and positive derivative at q2 place a global minimum in [q1,q2]. Any tangent at q0 in this interval gives the lower bound

    min B >= B(q0) - |dB/dw(q0)| *
                        (|log(q1/q0)|+|log(q2/q0)|).

The two-axis exponent for equal-size balanced dominoes is

    Phi = 2 log(27 z/4) + 2 min B - kappa log Q(z).

BBEP's coefficient lemma produces a single component-count sequence approaching kappa*m for the common threshold profile. For a fixed finite number of staircase cells the multiplicity of grid divisions of an n-point permutation is polynomial in n. Thus, if the ungridded avoidance GF converged at z, the corresponding gridded GF would converge there and uniformly bound each fixed-m subfamily's value. A positive Phi makes the m-root of those values exceed one for a sufficiently large fixed number of cells, a contradiction. Hence the avoidance GF's radius is at most z and its growth is at least 1/z.

The frozen arithmetic certificate takes z=9604060/10^8, kappa=516/1000, alpha=55555555/10^8, beta=18518518/10^8, q0=3046850759320/10^12, q1=1 and q2=9. All inputs are rational. The 256-bit Arb verifier evaluates the explicit H0,H2,H3 polynomials with outward rounding, establishes both derivative signs and the radius constraints, and proves a tangent-based Phi lower bound greater than 1.2788e-7. The exact product z*(10412263/10^6)<1 then implies the external baseline 10.412263.

The omitted historical `baseline_float.py` used the derivative definition and mpmath. `verify_baseline.py` was separately written (same agent), uses explicit closed forms and Arb, reads the frozen JSON artifact, and checks its BAR.json hash and the source digest recorded there. Its seven corruption controls include target inflation to 521/50; that certificate is rejected. These checks do not turn the baseline into a new result or human-refereed work.

## Exhaustive marginal encoding

Every nonempty permutation has a unique maximum and a unique parent after deleting it. When inserting the new maximum at slot s in an avoider, a new 1324 can only end at that maximum; it occurs exactly if the prefix before s already contains 132. Therefore insertion into all and only the slots at or before the first 132-ending index enumerates every 1324-avoider once. The implementation tests exact counts against the freshly retrieved OEIS sequence at every completed size, and compares its small orders with direct permutations.

For an avoider p and value threshold c, its low cell avoids 132 iff c is smaller than every maximum of a 132 in p. Its high cell avoids 213 iff c is at least every minimum of a 213 in p. These conditions give exactly an interval of valid cuts. At each such cut the encoding is (c, binary position shuffle, standardized top cell, standardized bottom cell). Decoding restores the value c+top_rank or bottom_rank at each indicated position. This is injective for **gridded dominoes**, and all valid encodings are tested. It does not assert an injective finite-palette encoding of the entire infinite ungridded staircase.

The all-size terminal-chain value-word rule, including the ordering and preservation of leaf status in every subobject, is proved in [FIRST_MOMENT_PROOF.md, Lemma 2.1](FIRST_MOMENT_PROOF.md#2-an-exact-marginal-strip-generating-function), from BBEP v3 Propositions 3.2–3.4. Its direct finite check is `check_value_word.py --max-n 9`; all 6,918 upper cells through n=9 pass. We use mu2 for the actual density 0.0662796..., s2=1/10 for the family threshold, c2=7/50 for the final cap, and eta_j for envelope coordinates.

For the top cell write zero for a right-to-left maximum and one for a non-leaf, in increasing value order. Each closed positive leaf strip is the zero-run after one maximal one-run and before a later one-run. The prototype records its run length exactly. Four additional series record all dominoes, no-one words, zeros before the first one, and zeros after the last one. The formal recurrence and the direct C++ permutation traversal are separate implementations; all five series are compared coefficient by coefficient. Finite agreement validates this marginal enumeration on the tested range. It cannot prove asymptotic concentration or establish a whole-staircase concatenation theorem.

## Reduced model

With the established limiting equitable profile (5/27,2/9,1/27), optimize the one-parameter Harris exponent. Stationarity in kappa forces q=1/sqrt(Q(z)); substituting cancels the kappa terms. The remaining scalar equation is

    log(27 z/4) + sum_j eta_j log(H_j(z,1/sqrt(Q(z)))) = 0.

The floating root is 10.4122642333..., below 10.42. This parameter replay is not an improvement candidate.

A diagnostic hypothetical profile adds delta one-leaf strips, removes 2*delta two-leaf strips, and adds delta three-leaf strips. It preserves the two moments. In this *conditional reduced model* delta greater than approximately 0.03766125 would reach the target, and delta=0.04 scores about 10.420480. At this pilot stage no uniform asymptotic delta-threshold had been proved. The final first-moment proof instead extracts a family with a two-leaf-strip upper cap and supplies a coefficientwise majorization envelope. See FIRST_MOMENT_PROOF.md; finite counts alone are not used to establish that family.
