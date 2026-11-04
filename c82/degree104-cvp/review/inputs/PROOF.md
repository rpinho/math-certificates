# C82 upper-bound candidate: statement to referee

Candidate, unrefereed. Constant 82a on https://teorth.github.io/optimizationproblems/ (raw: constants/82a.md in teorth/optimizationproblems): read the live page for the exact definition and normalization (it concerns the Zhang-Zagier height spectrum); checking that the statement below matches it is part of the referee's job.

## The reduction (Doche 2001)

C. Doche, "On the spectrum of Zhang-Zagier heights", J. Théor. Nombres Bordeaux 13 (2001), https://www.numdam.org/item/JTNB_2001__13_1_103_0/. Put T(z) = z(1-z). Let R_1..R_r be monic integer polynomials (denominators) with positive integer multiplicities m_j, and S_1..S_s integer polynomials (numerators) with nonnegative rational exponents q_i. Put Q = prod R_j^{m_j}, D = sum_j m_j deg R_j, and require deg(prod S_i^{q_i}) = sum q_i deg S_i < D, and each S_i coprime to each R_j. Define, with natural logarithms and t in [0,1),

  g(t) = [ sum_i q_i log|S_i(T(e^{2 pi i t}))| - sum_j m_j log|R_j(T(e^{2 pi i t}))| ] / D,
  J    = integral_0^1 max(0, g(t)) dt,
  H    = sum_j m_j log M(R_j o T) / D,   where M is the Mahler measure,
  B    = H + J.

Doche's limit-point argument gives C82 <= B. (The referee should check this against the paper and the live page, including whether the hypotheses above are exactly those needed.)

## The certificate

certificates/certificate.json:
- "denominator": list of {name, coeffs, multiplicity}; coeffs is a JSON list of integers, highest-degree coefficient first; multiplicity is a positive JSON integer.
- "numerator": list of {name, coeffs, q_rational}; coeffs as above; q_rational is a nonnegative rational "p/q" as a JSON string. A zero exponent means the factor is unused.
- "N", "numeric_unverified": search-time floating values. They are NOT evidence.

## Claim

B < 0.252404806 for this certificate; the producer's interval enclosure is B in [0.2524048059550536501, 0.2524048059550536604]. Compare with PR #280 (vidigoat), C82 < 0.2524177045*.
