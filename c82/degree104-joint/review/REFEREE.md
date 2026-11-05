# Independent referee verdict on the supplied C82 certificate

The mathematical claim survives the attacks below. My independent 256-bit Arb replay proves

    0.251996488988201164531880087886 <= B
      <= 0.251996488988201164532207712015 < 0.2519964890.

This enclosure lies strictly inside the interval stated in `inputs/CLAIM.md`. Together with the reduction, it establishes **C82 < 0.2519964890**. The verdict has a provenance caveat: this session exposes only “GPT-6-based Codex”, not an exact serving-model ID. I cannot truthfully certify the requested different-model condition. No producer code was read or run.

## Inputs and scope

The only producer inputs were `inputs/CLAIM.md`, `inputs/PROOF.md`, and `inputs/certificates/certificate.json`. All match `INPUTS_SHA256SUMS`. The certificate SHA-256 is `b71150bb7c1a7ac34e86b447e565cdd6c6d33bb225fa910f0acced4136f74171`.

I read the permitted machine rules, the live [82a definition](https://github.com/teorth/optimizationproblems/blob/main/constants/82a.md), [Doche's 2001 paper](https://www.numdam.org/item/JTNB_2001__13_1_103_0/), and the allowed PR bodies/comments using the specified gh executable. I did not access the linked code, certificates or replay packets. Sources are saved locally in `sources/`; the comparison history and clean-room restriction on broader prior-art searches are in `PRIOR_ART.md`.

This is an independently written AI mathematical review and replay, not a human review or proof-assistant formalization. Trust includes Python integer arithmetic, python-flint/FLINT/Arb, the cited averaging lemma, and the mathematical arguments explained here.

## Attacks on the reduction

**Normalization and the substitution.** The live definition uses natural logarithmic Weil height and h_Z(alpha)=h(alpha)+h(1-alpha), then the supremum of thresholds with finite sublevel set. The supplied proof uses precisely that definition. T(z)=z(1-z) is invariant under z -> 1-z. Doche uses multiplicative heights; taking the logarithm accounts for the change of notation. I inspected the displayed formulas and lemma on pp. 108–109, not only the imperfect PDF text extraction.

**Exact hypotheses on the new certificate.** The checker reconstructs polynomials from highest-degree-first integer arrays, using exact FLINT integer polynomials. It does not use search-time numerical fields. It verifies:

| Quantity or condition | New certificate |
|---|---:|
| Nonconstant monic denominator factors | 8, all degree 104 |
| Positive integer multiplicities | all 8 |
| Active numerator factors | 15 |
| Nonnegative exact rational exponents | all 15, all positive |
| D = sum m_j deg R_j | 1000000000064 |
| a = sum q_i deg S_i | 58700834920208207/65536 |
| D-a | 6835165083986097/65536 > 0 |
| Common exponent denominator b | 1048576 |
| Exact active gcd(S_i,R_j) checks | 120, all constant |
| Roots of all composed factors, with multiplicity | 2126 |

A common denominator b makes A=product S_i^(b q_i) an integer polynomial with nonnegative integer powers and deg A=ba<bD. Q=product R_j^m_j is monic of degree D. All active cross gcds being constant gives gcd(A,Q)=1 over Q[X]. No irreducibility of the listed factors or pairwise coprimality within the denominator list is needed. Numerators need not be monic; leading coefficients are included in the integral. Composition preserves cross coprimality by a Bezout identity over Q[X].

**Degree, algebraic integers, and the factor of two.** Independently reconstructing the argument, F_n=Q(T)^(bn)-A(T)^n has degree 2bnD and leading coefficient +/-1. Its roots are algebraic integers, with multiplicity. Each irreducible factor contributes its degree times the height of a root to log M(F_n). The symmetry permutes the full root multiset, so its average h_Z is log M(F_n)/(bnD). In particular, dividing once more by 2 would be wrong; the supplied proof does not make that mistake. Individual irreducible factors need not have the symmetry.

**Averaging theorem and exponent signs.** Apply Doche's p. 108 roots-of-unity averaging lemma to P(y,z)=Q(T(z))^b-y A(T(z)). Every specialization has the same positive z-degree 2bD and nonzero leading coefficient, satisfying its nonvanishing hypothesis. Factoring F_n over nth roots of unity and taking the logarithmic form of the lemma gives the two-variable Mahler integral. Jensen in y gives max(b log|Q(T)|,log|A(T)|). Division by bD gives exactly H+J, with positive q_i in the numerator and negative denominator contributions to g. This agrees with Doche's construction in equations (5)–(9). There is no negative polynomial exponent or hidden integrality assumption.

**Averages are not automatically infinitely many small points.** The supplied extraction step is necessary and valid. At any root alpha of F_n, Q(T(alpha)) is nonzero by coprimality. The rational function u=A(T)/Q(T)^b is nonconstant, since its numerator has strictly smaller degree. The multiplicity of alpha is the order of u(z)-u(alpha), as u(alpha)^n=1 and the outer power has nonzero derivative. Clearing the denominator bounds that order by 2bD, uniformly in n. Consequently any fixed finite set accounts for only bounded multiplicity while deg F_n grows linearly in n. If only finitely many alpha satisfied h_Z<=B+epsilon, nonnegativity of height would force the averages to have liminf at least B+epsilon, contradicting their limit B. This proves C82<=B. It does not claim attainment or an infinite sublevel set at B itself.

## Attacks on the numerical claim

The new checker `replay/check.py` is self-contained: only the standard library and python-flint. It contains no math import, float conversion, or floating-point literal. JSON search-time decimals are parsed as strings and ignored. Computation uses 256-bit Arb with one FLINT thread.

Mahler measures use complete certified FLINT root enclosures of the exact composed polynomials. Every denominator root has modulus rigorously separated from 1. The seven numerator roots on the unit circle come from exact divisions by Phi_1, Phi_6 and Phi_10; all remaining roots are separated from the circle.

For J the checker covers [0,1/2] by an adaptive exact dyadic partition and doubles by conjugation symmetry. It proves each accepted positive or negative panel's sign using rigorous range bounds (also a mean-value bound when nonsingular). A numerator logarithm tending to -infinity causes no omitted neighborhood: its finite upper bound can still prove g<0. All unresolved panels contribute a conservative [0,error] interval. There are 29 joined positive arcs, and the combined upper contribution from 58 unresolved panels is less than 3.277e-22.

On positive arcs the integral is evaluated by explicit dilogarithm antiderivatives of the root logarithms; there is no sampled-grid quadrature error to overlook. `replay/report.md` supplies the formulas and their branch justification. The actual unresolved-panel bound and Arb errors are included in the displayed enclosure.

The split is

    H in [0.251992523252609459669852920685,
          0.251992523252609459669852920686]
    J in [0.000003965735591704862027167201,
          0.000003965735591704862354791329].

The certificate's search-time `numeric_unverified` field is below this certified enclosure and is not evidence for the bound. The stale numerical particulars in PROOF.md belong to the earlier certificate, as CLAIM.md explicitly warns; they must not be presented as the new certificate's D, root count, gcd count, or verified value.

## Controls

- Changing a denominator's leading coefficient from 1 to 2 is rejected as nonmonic.
- Changing a numerator exponent to -1 is rejected as negative.
- The false target 0.2519964889 is rejected: even the lower endpoint of B exceeds it.
- The analytic case Q=X-3, S=5, q=1 gives B=log(5), J=log(5/3); both are enclosed.
- The analytic case Q=X-3, S=X, q=1/2 has a numerator unit-circle singularity and g<0 everywhere else; the checker returns J=0 and encloses B=log(3).

The first two controls deliberately violate hypotheses; they establish rejection, not a quantitative sensitivity claim for valid coefficient/exponent changes.

## Comparison with permitted live values

| Comparison | Printed strict upper bound | Improvement in printed bound to 0.2519964890 |
|---|---:|---:|
| [#280 v3](https://github.com/teorth/optimizationproblems/pull/280) requested in the spec | 0.2520591386* | 0.0000626496 |
| [#330](https://github.com/teorth/optimizationproblems/pull/330), unchanged at final check | 0.2520179248* | 0.0000214358 |
| #280 v4, added during this review | 0.2520079724* | 0.0000114834 |

The final #280 body has updated_at 2026-11-05T13:30:35Z and reports B<=0.25200797232846 for v4. The v3 comparison remains relevant but is no longer its latest value. Its comments also correct an earlier confusion between quadrature upper bounds and two-sided enclosures. I did not replay any of these forbidden external packets, so these comparisons are to the public statements, not independent verification of the older certificates.

**Did this referee find something new? No.** It verifies the supplied candidate, not a newly discovered certificate or construction. The supplied candidate does beat the specified printed numbers under the same definition, including the newly observed v4. This is not an exhaustive global priority or optimality claim.

## Disposition

The mathematics and numerical replay support updating the candidate bound to 0.2519964890*, with the new certificate-specific quantities above. Preserve the AI-review qualification and do not assert demonstrated different-model provenance from this receipt. No PR, repository or external service was modified; no commit, push or post was made.

VERDICT: HOLDS WITH CAVEATS
