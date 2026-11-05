# Independent clean-room referee: C82 candidate

The mathematical and numerical claim holds:

    C82 <= B,
    B in [0.2520179247552093517426, 0.2520179247552093517434],
    hence C82 < 0.2520179248.

The replay interval lies wholly inside the candidate's supplied interval. The verdict carries a provenance caveat: this session does not expose its exact serving-model ID, so I cannot authenticate the requested difference from the producer's model. No mathematical defect or failed numerical hypothesis was found.

## Attacks on the reduction

1. **Wrong definition or normalization.** I fetched the live [82a definition](https://github.com/teorth/optimizationproblems/blob/main/constants/82a.md). It uses logarithmic height h(alpha)=log M(P)/deg(P) and h_Z(alpha)=h(alpha)+h(1-alpha), with C82 defined by finite sublevel sets. I read the printed definitions on pages 103–104 of [Doche, *Zhang-Zagier heights of perturbed polynomials*](https://www.numdam.org/item/JTNB_2001__13_1_103_0/). His height is multiplicative, so taking logarithms matches 82a. T(z)=z(1-z) is the same composition. No missing factor of two was found: symmetry doubles the mean h, while T doubles the degree.

2. **Wrong theorem or an inadmissible specialization.** Doche's printed page-108 lemma and equations (5)–(9) were inspected directly. Apply the lemma to P(y,z)=Q(T(z))^b-y A(T(z)). The strict degree inequality makes every specialization in y have degree 2bD and nonzero leading coefficient. Root-of-unity factorization produces Q(T)^(bn)-A(T)^n. Jensen's formula in y gives the maximum of the two logarithms, and division by bD gives exactly H+J with the exponent signs in PROOF.md. General denominator multiplicities and arbitrary nonzero integer numerators fit this polynomial specialization; Doche's specific factor list is not a hypothesis of the averaging lemma.

3. **Nonintegral roots or a bad factor average.** Q is monic; the lower-degree term cannot cancel its leading term after composition. Up to a sign, F_n is monic integral. All its irreducible factors are therefore monic integral. Summing h over roots with multiplicity gives log M(F_n); invariance under alpha -> 1-alpha gives the mean h_Z as log M(F_n)/(bnD). An individual irreducible factor need not itself have that symmetry. The proof correctly uses the complete root multiset.

4. **A polynomial average that fails to bound the essential minimum.** This is the substantive extraction issue. Pairwise active gcd checks imply gcd(A,Q)=1, so no root of F_n is a pole of u=A(T)/Q(T)^b. The rational map u is nonconstant by the strict degree inequality. At u(alpha)^n=1 the outer map 1-v^n has a simple zero; the multiplicity is the vanishing order of u-u(alpha), at most 2bD independently of n. Thus any fixed finite set occupies only bounded multiplicity in F_n, whose degree grows linearly in n. If the sublevel set h_Z<=B+epsilon were finite, nonnegative heights would force the limiting multiset average to be at least B+epsilon, contradicting its limit B. This proves C82<=B under the actual 82a definition. It does not claim attainment at B or infinitely many points at height <=B exactly.

5. **Old certificate assertions substituted for new checks.** CLAIM.md explicitly warns that the supplied PROOF.md describes an earlier certificate. I did not reuse its D, slack, pair count, root count, names, or old numerical result. The new certificate has D=999999999960, a=940866927165429405/1048576, and positive slack 107709072792627555/1048576. Ten monic denominators and eighteen active numerators pass all 180 exact gcd checks. The current nonmonic numerator is n121_1_12, leading coefficient 2; its contribution is included. Denominator irreducibility and pairwise coprimality are not needed.

6. **Numerical cancellation, missed signs, or discarded logarithmic singularities.** The independent checker uses exact polynomial composition, all 2666 certified roots, and 256-bit Arb balls. It encloses signs over complete intervals, retains a bounded contribution for every unresolved sign interval, and uses rigorously evaluated dilogarithm primitives on positive intervals with explicit branch-cut checks. All denominator roots are certified off the circle. Numerator singular neighborhoods are handled by finite upper bounds, including intervals with negative-infinite lower log bounds. The proof and exact dyadic results are in [replay/report.md](replay/report.md) and [replay/result.json](replay/result.json). The tolerance is not confused with a rounding radius.

## Controls and numerical verdict

The complete replay passed in 77.04 seconds. Invalid coefficient, negative exponent, degree, and gcd perturbations are rejected. Valid P1=X -> 2X and q(P1) -> 0 perturbations satisfy the hypotheses but provably change B. The false target 0.2520179247 is below the certified lower endpoint and is rejected. Analytic cases B=log(3) and the positive log-sine integral are reproduced. See the self-contained [checker](replay/check.py) and [replay report](replay/report.md).

## Live comparisons

The permitted sources were read and rechecked on 2026-11-05; the final 82a, #280, and #330 snapshots are unchanged from the initial reads.

| Source | Printed upper bound | Printed bound minus this replay's upper endpoint |
| --- | --- | --- |
| [#280 v3, V. Patankar](https://github.com/teorth/optimizationproblems/pull/280) | 0.2520591386* | > 0.00004121384479064825 |
| [#330](https://github.com/teorth/optimizationproblems/pull/330) | 0.252404806* | > 0.00038688124479064825 |

The #280 comment gives a tighter independent interval [0.2520591385259547,0.2520591385259548] and the author acknowledges that the earlier printed ball radius alone excluded quadrature error. The present bound is also below that interval. The #301 text reports 0.253091834*. These are textual comparisons, not local replays of forbidden packets. Credit remains with Doche's construction, the factor and search methods credited in the candidate, and the candidate's producer. See [PRIOR_ART.md](PRIOR_ART.md); no exhaustive global priority claim is made.

**Did I find something new? No.** This referee job reproduces the supplied candidate. The verified candidate improves the two requested printed bounds under the same definition; this job did not discover its construction.

## Caveats and disposition

The clean-room code independence is attested: no producer source was read or run. Exact serving-model identity and the claimed model difference are not observable within this session; the receipt says so rather than inventing an ID. This is an AI referee opinion with a rigorous numerical replay, not a human referee report or formalized proof. The trusted numerical backend is Python plus FLINT/Arb. None of these caveats changes the certified numerical inequality.

The result is suitable to accompany the candidate's proposed PR update with the provenance caveat retained and with the new certificate's counts and value replacing the earlier certificate-specific statements. No commit, PR update, push, post, upload, or contact was made.

VERDICT: HOLDS WITH CAVEATS
