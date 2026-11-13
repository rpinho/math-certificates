# C82 round-10: adversarial referee and clean-room replay

The supplied certificate proves **C82 < 0.2519696460** under the live 82a definition. No mathematical gap was found in the reduction or in the exact certificate hypotheses. My independent 384-bit Arb computation encloses

    0.2519696459872490990419691935079545
      <= B <=
    0.2519696459872490990419691935079546.

These deliberately rounded-out endpoints lie inside the producer's claimed interval [0.2519696459872490977703, 0.2519696459872491000812]. Exact rational endpoints and a substantially narrower ball are in replay/result.json. The margin below the requested target is approximately 1.27509009580308e-11. The false target 0.2519696459 is strictly below the replay's lower endpoint and is rejected.

The verdict has a provenance caveat: this session identifies itself as GPT-6 / Codex but does not expose its exact serving-model ID. I cannot independently attest the requested different-model relation to the producer. This does not change the computed enclosure. The checker is newly written here, with neither producer code nor earlier referee code read or executed.

## Attempts to break the mathematical claim

1. **Wrong height or factor of two.** The live [82a definition](https://github.com/teorth/optimizationproblems/blob/main/constants/82a.md) is logarithmic h(alpha)+h(1-alpha), with the essential minimum defined by finite closed sublevel sets. Let b clear the rational exponents. The family F_n=Q(T)^(bn)-A(T)^n has degree 2bnD and leading coefficient a sign because deg(A)<bD. After multiplication by that sign it is monic integral. T(1-z)=T(z) permutes the entire multiset of roots. Therefore its average Zhang–Zagier height is 2 log M(F_n)/(2bnD)=log M(F_n)/(bnD). Individual irreducible factors need not have this symmetry. The supplied normalization is correct.

2. **Misapplication of Doche's averaging lemma.** I read the actual page images, especially pp. 108–109 and equations (5)–(9), in [Doche (2001)](https://www.numdam.org/item/JTNB_2001__13_1_103_0/). The lemma requires positive degree in z and nonzero specializations at roots of unity. For P(y,z)=Q(T(z))^b-y A(T(z)), every specialization has the same degree 2bD, so these requirements hold. Factorization over nth roots of unity and the logarithmic form of the lemma give the torus average. Jensen in y gives max(b log|Q(T)|, log|A(T)|). Division by bD produces exactly H+J. Interchanging the two terms or multiplying the polynomial by a sign does not change this conclusion. Doche's multiplicative height must be logged; it must not be used directly as the 82a value.

3. **Nonmonic numerators and wrong exponent signs.** Numerators need only be nonzero integral polynomials. Their leading coefficients contribute log absolute value, and the independent checker includes those terms both in polynomial evaluation and in the root primitive. All active exponents are nonnegative rationals; their clearing denominators create nonnegative integer powers in A. Denominator multiplicities are positive integers and their signs in g are negative. No numerator leading coefficient was silently normalized away.

4. **Hidden cancellation, common roots, or degree loss.** All 240 active numerator/denominator gcds are constant in exact integer polynomial algebra. Thus A and Q are coprime, and composition preserves their lack of common roots. The strict degree gap prevents cancellation of the highest term in F_n. Pairwise coprimality among denominators, irreducibility of individual factors, and squarefreeness of F_n are not required.

5. **A limit of averages is not automatically an essential-minimum bound.** This is the important extraction step. Put u=A(T)/Q(T)^b. It is nonconstant, and Q(T(alpha)) is nonzero at every root of F_n. Such a root satisfies u(alpha)^n=1. The outer function 1-v^n has a simple zero at that value, so the multiplicity of alpha is the vanishing order of u-u(alpha), bounded by 2bD independently of n. Any fixed finite set therefore contributes only bounded total multiplicity. If only finitely many algebraic numbers had height <=B+epsilon, the root-height averages would have liminf at least B+epsilon, contradicting their limit B. This establishes infinitely many numbers below each B+epsilon and hence C82<=B. It does **not** establish attainment at B or an infinite sublevel set exactly at B; the proof correctly avoids claiming either.

6. **Dropped logarithmic singularities or unchecked sign changes.** Seven composed numerator roots are exactly on the circle. They are certified through cyclotomic factors of orders 1, 6 and 10, not by treating near-unit moduli as exact. The independent integrator uses rigorous panel ranges and either proves a panel nonpositive, proves it positive, or encloses its unresolved positive contribution. No neighborhood is omitted without a sign or integral bound. No denominator root is on the circle. The implementation conservatively refuses an ambiguous denominator modulus; that restriction is sufficient for this certificate and is not asserted as a theorem hypothesis.

7. **Numerical hints mistaken for evidence.** Search-time decimal fields in certificate.json are ignored and parsed as strings. The input hash was verified against INPUTS_SHA256SUMS. Only exact coefficients, exact integer multiplicities and exact rational exponents drive the result. The replay uses certified root isolation, not floating-point root guesses as proof.

## Exact certificate findings

| Item | Independent result |
|---|---:|
| Denominators | 6, all monic, degree 104 |
| Active numerators | 40 |
| D | 999999999960 |
| a=sum q_i deg S_i | 469303044808512511/524288 |
| D-a | 54984955170515969/524288 > 0 |
| Common exponent denominator b | 1048576 |
| Active gcd pairs | 240, all coprime |
| Composed roots, with multiplicities | 4198 |
| Unit-circle roots | 7, all in numerator factors |

The large multiplicities and exponent denominator are harmless: the proof uses the enormous family symbolically, while the checker operates on the small listed factors.

## Independent numerical replay

The self-contained replay/check.py uses only the standard library and python-flint 0.9.0. At 384 bits it gives

    H = 0.2519695552678072499354164706113521929338533...
    J = 0.00000009071944184910655272289660232626439...

Its independent integration method is an adaptive dyadic sign partition followed by Arb dilogarithm primitives on the proven-positive intervals. The second-derivative and singularity bounds are derived in replay/report.md. It examined 14369 panels, proved 4161 panels nonpositive, retained 96 tiny sign-uncertain panels, and merged the positive panels into 48 intervals. Every retained uncertainty is included in B. The numerical enclosure is much tighter than the margin to the target.

Controls reject a coefficient change that breaks monicity, a negative exponent, a common factor, and a degree violation. Analytic controls check B=log(5) with unit-circle numerator singularities, a constant-positive integral log(2), the full-circle Jensen identity, the inside-root primitive, and an everywhere-positive nonconstant case B=log(100). The false numerical target is also rejected by the actual lower endpoint. The AST audit finds no math import, float call, or binary floating-point literal in check.py.

Runtime and peak memory, reproduction command and exact endpoints are recorded in replay/report.md and replay/result.json. All computation stayed on this machine, with nice 10, one numerical worker and one FLINT thread. No commit, push, post, PR update or external write was made.

## Live comparisons and novelty

The permitted live sources were read on 13 November 2026 UTC (12 November local time). Their bodies and comments were read with the required gh executable; no linked packets or code were followed.

| Live source | Printed upper threshold | Reduction to new printed threshold 0.2519696460 |
|---|---:|---:|
| [#280 v5](https://github.com/teorth/optimizationproblems/pull/280) | 0.2519889614* | 0.0000193154 |
| [#330](https://github.com/teorth/optimizationproblems/pull/330) | 0.2519744488* | 0.0000048028 |
| [#301](https://github.com/teorth/optimizationproblems/pull/301) | 0.253091834* | Superseded by both above |

The live merged 82a page still lists the asterisked 0.2534449* bound. The smaller values above are open-PR claims, not merged table entries. The same essential-minimum definition is being compared. I did not independently replay those older certificates because this job's clean-room input restriction excludes them. PRIOR_ART.md records this scope.

**Did this referee find something new? No.** This job independently verifies a supplied construction. The supplied candidate does beat the two requested live printed bounds; credit for that improvement belongs to its producer and the credited Doche/Patankar/Pinho construction lineage. This is a new numerical certificate relative to those values, not a new mathematical method or a claim of globally exhaustive priority.

## Limits and disposition

The mathematical claim and numerical replay survive the attacks above. Trust remains in the cited averaging theorem, the stated extraction argument, Python integer arithmetic and FLINT/Arb's exact and interval routines. This is an AI referee report, not a human expert review or a proof-assistant formalization. The only unresolved task-specific caveat is the unavailable exact model identity, which prevents certifying that this session used a different model from the producer. No public update has been made; this local report and replay are ready for the producer's decision about updating #330.

VERDICT: HOLDS WITH CAVEATS
