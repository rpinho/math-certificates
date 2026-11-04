# Independent adversarial referee — C82

**The mathematical bound is verified; all requested controls pass.** Only the supplied PROOF.md and certificate.json are construction inputs. No producer code has been read or executed.

## Definition and normalization attack

The live [82a definition](https://github.com/teorth/optimizationproblems/blob/main/constants/82a.md) is the essential minimum of h_Z(alpha)=h(alpha)+h(1-alpha), with h logarithmic. Doche's paper uses a multiplicative height, so its formula must be logged. The supplied proof misidentifies the title: the linked Bordeaux paper is [*Zhang-Zagier heights of perturbed polynomials*](https://www.numdam.org/item/JTNB_2001__13_1_103_0/), JTNB 13 (2001), 103–110; *On the spectrum of the Zhang-Zagier height* is the separate Math. Comp. paper. The Bordeaux construction, equations (5)–(9), was checked on the actual rendered pages 108–109, including the degree maximum in (6). This bibliographic error does not change the formula.

Here is a direct derivation, including the extraction step omitted from the short supplied proof. It also establishes which hypotheses are needed. Write Q=product R_j^m_j, D=deg Q, choose a common denominator b of all q_i, and put A=product S_i^(b q_i). Then A and Q are nonzero integer polynomials, Q is monic, deg A < bD, and gcd(A,Q)=1. Define

    F_n(z)=Q(T(z))^(bn) - A(T(z))^n,  T(z)=z(1-z).

Up to an overall sign, F_n is monic of degree 2bnD. It is invariant under z -> 1-z. Its irreducible factors are monic integer polynomials; the degree-weighted average of h_Z over those factors, counting multiplicity, is therefore log M(F_n)/(bnD). The factor 2 from h(alpha)+h(1-alpha) cancels the doubling of degree from composition with T. Dividing by 2D or multiplying the stated answer by 2 would be wrong.

Apply Doche's roots-of-unity averaging lemma, on page 108, to Q(T(z))^b - y A(T(z)). Its z-degree is 2bD for every specialization of y because the degrees differ, so no specialization vanishes identically. Factoring F_n over the nth roots of unity and then using Jensen's formula in y gives

    lim log M(F_n)/(bnD)
      = (1/D) integral_0^1 max(log|Q(T(e^(2 pi i t)))|,
                              sum_i q_i log|S_i(T(e^(2 pi i t)))|) dt
      = H + J.

Finite sets cannot absorb this limit. For any root alpha of some F_n, Q(T(alpha)) is nonzero by coprimality. The rational function u(z)=A(T(z))/Q(T(z))^b is nonconstant. The multiplicity of alpha in 1-u(z)^n is the vanishing order of u(z)-u(alpha), independent of n whenever u(alpha)^n=1, since n*u(alpha)^(n-1) is nonzero. That order is at most 2bD. Hence any fixed finite set contributes only bounded total multiplicity as n grows. If only finitely many algebraic numbers had height at most B+epsilon, all but a vanishing fraction of F_n's roots would have height greater than B+epsilon, contradicting the limiting average B (heights are nonnegative). Thus there are infinitely many with h_Z <= B+epsilon for every epsilon>0, which proves C82 <= B under the live definition. This does not assert attainment of B or infinitely many values <= B exactly.

Monicity of Q and the strict degree inequality ensure monicity of F_n. Nonnegative rational q_i make A a polynomial after clearing denominators; negative exponents would require a different proof. Coprimality prevents persistent common roots. Irreducibility of individual R_j or S_i, pairwise coprimality among the R_j, and monicity of the S_i are not needed. The certificate satisfies the stronger irreducibility and denominator pairwise coprimality checks anyway. In particular its numerator n121_2_0 has leading coefficient 2; rejecting it as nonmonic would be an erroneous extra hypothesis. Its leading-coefficient logarithm must be included in numerical evaluation.

## Exact certificate attacks

Both permitted input hashes match INPUTS_SHA256SUMS. Coefficients, multiplicities and rational exponents are parsed exactly, never through JSON floating values. The fields N and numeric_unverified are ignored.

Completed FLINT audit: six monic irreducible denominators, all degree 104; 13 numerator polynomials. D=999999999856. Weighted numerator degree is 952533595715278899/1048576 and the slack is 96042404133726157/1048576 > 0. All 78 numerator/denominator gcd checks and 15 denominator pair checks pass. The certified root count is 1644, including seven numerator circle roots. All denominators have circle-root-free compositions. Controls and exact enclosures are in replay/report.md and replay/result.json.

## Numerical attacks

A high-resolution sampled sum is not a certificate here. The positive-part function has sign changes, and numerator factors vanish on the integration circle. The independent checker uses certified FLINT root enclosures and Arb validated quadrature. Neighborhoods of numerator circle roots are removed only after a one-sided interval proof that g<0 there, making their positive-part integral exactly zero. No denominator circle root is silently omitted. The first direct Arb positive-part integration exhausted 100000 evaluations and was rejected; STATUS.md records the failure before the switch to rigorously bounded Taylor integration. The full accepted calculation at 384 bits gives B in [0.2524048059550536552336383477, 0.2524048059550536552336387448]. This is inside the producer's claimed enclosure and strictly below 0.252404806. No sign-change or singularity gap was found. The coefficient and exponent corruptions and false target are all rejected; three analytic cases pass.

## Comparison and novelty

The live [PR #280](https://github.com/teorth/optimizationproblems/pull/280) says C82 < 0.2524177045* and reports an independent enclosure [0.2524177044473123, 0.2524177044473124]. These are public claims, not a local replay of #280: its certificate is outside this job's allowed inputs. See PRIOR_ART.md for the scope and timestamps.

Did this referee find something new? **No.** This is an independent replay of a supplied construction, not a new construction. The supplied candidate is now verified below the live printed #280 bound by approximately 0.000012898544946344766361. This numerical improvement belongs to the supplied construction, not to a new construction made by this referee. No predictive score is claimed; SBS is not applicable.

## Verdict and caveats

The claimed upper bound survives the algebraic, analytic and numerical attacks. The underlying essential-minimum statement is valid, and the independent interval enclosure proves the requested strict inequality. The title of the cited Doche paper should be corrected, and the brief supplied proof should include (or link to) the extraction argument given above.

The session identifies this assistant as GPT-6-based Codex without exposing an exact serving-model ID. The attestation records that limitation; it does not claim to independently establish the model difference from the producer. The clean-room input/code-access declarations are truthful. No producer code was read or run, no private material was transmitted, and no commits, pushes or posts were made.

VERDICT: HOLDS WITH CAVEATS
