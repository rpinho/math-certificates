# Clean-room referee of the supplied C82 candidate

**The bound holds:** the clean-room replay proves C82 <= B < 0.2519923410. The only caveat is model provenance: the exact serving-model ID is not exposed, so the requested different-model identity cannot be independently attested.

## Scope and independence

I used only the three supplied mathematical inputs, the allowed live 82a definition and PR text, and Doche's paper. No producer code, earlier local job, linked certificate packet, or linked replay code was read or run. The replay was written here from the mathematical definitions, using exact integer polynomial algebra and Arb balls. See [replay/report.md](replay/report.md) for the numerical argument and reproduction details.

The exact serving-model ID is unavailable in this session. I can truthfully attest clean-room code independence, but cannot independently establish that this run used a different model ID from the producer. That provenance qualification will remain even if the mathematical claim passes.

## Attacks on the reduction

**Definition and normalization.** The [live 82a page](https://github.com/teorth/optimizationproblems/blob/main/constants/82a.md) defines logarithmic h_Z(alpha)=h(alpha)+h(1-alpha), and takes the supremum of thresholds with finite non-strict sublevel sets. For F_n=Q(T)^(bn)-A(T)^n, the strict degree inequality gives deg(F_n)=2bnD and leading coefficient ±1. Multiplication by its sign makes it monic. Counting roots with multiplicity, sum h(alpha)=log M(F_n). Since T(1-z)=T(z), reflection permutes the entire multiset, giving the height average log M(F_n)/(bnD). This is exactly the supplied normalization. Individual irreducible factors need not be reflection-invariant. No missing factor of two was found.

**Citation and composition.** I inspected the printed pages 105, 108 and 109 of [Doche, JTNB 13 (2001), 103–110](https://www.numdam.org/item/JTNB_2001__13_1_103_0.pdf). His variable is X=z(1-z). The page-108 lemma concerns roots-of-unity specialization averages; the hypothesis requires that no specialization be identically zero. Equations (5)–(9) use multiplicative heights. Taking logarithms and using the strict degree inequality gives the supplied H+J formula. The certificate's use of X-1 instead of 1-X does not affect absolute values.

**Specialization and exponent signs.** Let b be the lcm of the reduced exponent denominators. Then A=product S_i^(b q_i) is an integer polynomial, with deg A=ba<bD. Apply the averaging lemma to Q(T(z))^b-y A(T(z)); its z-degree is 2bD at every y, including roots of unity. Jensen's formula in y gives max(b log|Q(T)|,log|A(T)|). After division by bD, the positive-part integrand is (sum q_i log|S_i(T)|-sum m_j log|R_j(T)|)/D. The denominator minus sign and all numerator plus signs are correct.

**Monicity and nonmonic numerators.** Monicity is essential for the algebraic-integer height average and holds for every denominator. It is not needed for the numerators. This certificate has numerator leading coefficients 9 and 2, and the checker retains their logarithms. Dividing those factors by their leading coefficients would change the claimed bound and is not done.

**Coprimality and extraction.** Exact gcd checks ensure A and Q have no common root. Hence a root alpha of F_n has Q(T(alpha)) nonzero and u(alpha)^n=1 for u=A(T)/Q(T)^b. Degree and coprimality make u nonconstant. At such a root, 1-u^n has the same vanishing order as u-u(alpha), since the outer function has a simple zero at a nonzero root of unity. Clearing the nonvanishing denominator bounds this order by 2bD, independently of n. A fixed finite set of alpha therefore contributes only bounded multiplicity. If only finitely many alpha had h_Z<=B+epsilon, nonnegativity of heights would force the average's liminf to be at least B+epsilon, contradicting its limit B. Thus infinitely many distinct alpha have h_Z<=B+epsilon for each epsilon>0, and the live essential minimum is at most B. The argument does not assert infinitely many points at B itself.

**Unnecessary hypotheses.** Neither pairwise coprimality of denominators nor irreducibility of the displayed factors is needed. Positive multiplicities and nonnegative exponents are sufficient together with the exact degree and active-pair gcd checks. No additional hypothesis needed by this argument was found missing.

## Application to this certificate

The proof file describes an older certificate. Its old a, slack, 78 gcd pairs, 1644 roots, factor names and numerical endpoint are not evidence for this one. The independently checked replacements are:

| Quantity | New certificate |
|---|---:|
| Denominators | 8, each monic of degree 104 |
| Active numerators | 18 |
| D | 999999999856 |
| a | 939550863051360379/1048576 |
| D-a | 109025136797644677/1048576 > 0 |
| b | 1048576 |
| Active coprimality pairs | 144, all pass |
| Composed roots, with multiplicity | 2224 |

All integer, monicity, multiplicity, exponent-sign, gcd and degree hypotheses hold exactly. The old D happens to equal the new D; that coincidence was not assumed.

## Numerical attack

The independent checker derives Mahler measures from certified roots and encloses J on a complete dyadic partition using Taylor series with a proved Cauchy remainder. It integrates the positive part only after certifying positivity; uncertain sign-change panels receive explicit range bounds. Panels meeting numerator log singularities can be discarded only after a full-panel negative upper bound for g. No sample-grid estimate, search-time floating value, unaccounted quadrature tolerance, or unproved omission of singular neighborhoods contributes to B.

Exact reciprocal-polynomial gcds also show that no denominator has a unit-circle root. The numerator unit-circle factors are exactly z-1 (P1), Phi_6(z) (P2), and Phi_10(z) (P4). On the half-circle the singular locations are t=0, 1/10, 1/6, 3/10. Their treatment is part of the interval calculation, not an assumption that their neighborhoods have negligible area.

The initial checker had an interval-index error, found during review and corrected after stopping and reverting that run. A subsequent run failed on decimal target parsing after integration. Both versions were withdrawn before correction and furnished no accepted result. The final calculation checks its domain coverage exactly and compares Arb enclosures directly. This implementation history is disclosed in replay/report.md.

## Comparison and novelty

The allowed public sources were read on 2026-11-05. [PR #280 v4](https://github.com/teorth/optimizationproblems/pull/280) prints 0.2520079724*, and [PR #330](https://github.com/teorth/optimizationproblems/pull/330) prints 0.2519964890*. Their underlying packets were excluded by the clean-room rule, so this job compares their printed bounds rather than claiming to replay them. [PR #301](https://github.com/teorth/optimizationproblems/pull/301) is earlier at 0.253091834*. See [PRIOR_ART.md](PRIOR_ART.md).

Did this referee find something new? **No.** This is a replay of the supplied candidate, not discovery of a new construction. The completed replay confirms that the supplied candidate improves both cited printed bounds under the same definition. No global priority or optimality claim is made.


## Completed replay and verdict

At 384 bits, the independently written checker returned PASS and the rigorous enclosure

    0.251992340972008391240902200131 <= B
      <= 0.251992340972008391240904220544.

This lies inside the producer's claimed interval. The margin below 0.2519923410 is at least 2.7991608759095779456E-11. All requested coefficient/exponent mutation, false-target, and analytic controls pass; additional degree and gcd rejection controls pass. The exact circle partition, Cauchy truncation errors, sign-crossing panels, singular-neighborhood bounds, root enclosures and outward decimal rounding are included in the enclosure. See [replay/result.json](replay/result.json) and [replay/report.md](replay/report.md).

| Compared printed bound | Improvement of the new printed target 0.2519923410 |
|---|---:|
| #280 v4: 0.2520079724* | 0.0000156314 |
| #330 live: 0.2519964890* | 0.0000041480 |

Both PR bodies/comments were reread before completion and were unchanged. The calculation is an AI referee/replay with clean-room code independence, not a human review or proof-assistant formalization. The model field truthfully records “GPT-6-based Codex (exact serving-model ID not exposed)”; no exact ID or different-model claim is invented. This provenance caveat does not weaken the proved numerical inequality.

VERDICT: HOLDS WITH CAVEATS
