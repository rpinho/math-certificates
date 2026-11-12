# Essential-minimum proof for the degree-104 certificate

The claim is C82 <= B, with the strict numerical upper bound recorded in RESULT.json and REPORT.md and certified by verify_best.py. This is a candidate, unrefereed construction, conditional on the mathematical argument below and the trusted exact/ball arithmetic backend. This proof text is adapted from our earlier release proof retained in the round-6 review inputs; the construction and extraction argument are unchanged.

The cited construction is C. Doche, [*Zhang-Zagier heights of perturbed polynomials*](https://www.numdam.org/item/JTNB_2001__13_1_103_0/), J. Théor. Nombres Bordeaux 13 (2001), 103–110, equations (5)–(9), especially the roots-of-unity averaging lemma on page 108. Doche uses multiplicative heights: take natural logarithms to obtain the live 82a normalization. The extraction argument in the last part below is credited to the clean-room referee, for the earlier construction. The earlier review is method credit; it is not a review of this job's new certificate.

## Exact hypotheses and notation

Let T(z)=z(1-z). The certificate supplies nonconstant integer polynomials R_j with leading coefficient 1, positive integer multiplicities m_j, nonzero integer polynomials S_i, and nonnegative rational weights q_i. Discard zero weights. Define

    Q(X) = product_j R_j(X)^m_j,
    D = sum_j m_j deg(R_j),
    a = sum_i q_i deg(S_i).

Require a<D and gcd(S_i,R_j)=1 for every active pair. No monicity condition is imposed on S_i. Every numerator leading coefficient contributes its logarithm to the integrand. Irreducibility of the factors and pairwise coprimality of the denominators are unnecessary for this proof.

Choose a positive common denominator b of the q_i and set

    A(X) = product_i S_i(X)^(b*q_i).

Then A and Q are nonzero integer polynomials, Q is monic, deg(A)=ba<bD, and gcd(A,Q)=1. The exact values of D, a and the active gcd-pair count for this certificate are recorded in evidence/best-replay.json. Its exact finite hypotheses are checked by verify_best.py, separately written by the same agent lineage as the search.

For Mahler measure M and natural logarithms define

    H = (1/D) sum_j m_j log M(R_j composed with T),
    g(t) = (1/D) [sum_i q_i log|S_i(T(exp(2*pi*i*t)))|
                    - log|Q(T(exp(2*pi*i*t)))|],
    J = integral_0^1 max(0,g(t)) dt,
    B = H+J.

The logarithmic singularities are integrable; the numerical treatment must enclose them, not drop neighborhoods without a sign proof. Jensen's formula and additivity of log Mahler measure give equivalently

    B = (1/D) integral_0^1
         max(log|Q(T(exp(2*pi*i*t)))|,
             sum_i q_i log|S_i(T(exp(2*pi*i*t)))|) dt.

## Polynomial family and its height average

For each positive integer n let

    F_n(z) = Q(T(z))^(b*n) - A(T(z))^n.

Because deg(A)<bD, the degree is exactly N_n=2bnD and the leading coefficient is a sign. Multiply by that sign to make F_n monic; this does not change roots or Mahler measure. Also F_n(1-z)=F_n(z). Its irreducible factors are monic integer polynomials, so all roots are algebraic integers.

For an irreducible monic factor P of degree d and a root alpha, h(alpha)=log M(P)/d. Counting roots with multiplicity gives sum_alpha h(alpha)=log M(F_n), since the roots of each P have the same height. The transformation alpha -> 1-alpha permutes the complete root multiset. Consequently

    (1/N_n) sum_{F_n(alpha)=0} h_Z(alpha)
      = 2 log M(F_n)/N_n
      = log M(F_n)/(bnD).

This is a multiset average over roots (equivalently a degree-weighted factor average). Individual factors need not be invariant under alpha -> 1-alpha. The factor of two in h_Z cancels the doubled degree from T. No additional factor of two belongs in B.

## Limit of the averages: the cited theorem

The factorization over nth roots of unity gives, up to a harmless constant sign,

    F_n(z) = product_{zeta^n=1} (Q(T(z))^b - zeta*A(T(z))).

Apply Doche's page-108 averaging lemma to P(y,z)=Q(T(z))^b-y*A(T(z)). Every specialization in y has z-degree 2bD, since deg(A)<bD, and therefore is never identically zero. The lemma equates the limit of the roots-of-unity average of log Mahler measure with the two-variable torus average. Jensen's formula in y yields

    lim_{n -> infinity} log M(F_n)/(bnD)
      = (1/(bD)) integral_0^1
           max(b log|Q(T(exp(2*pi*i*t)))|,
               log|A(T(exp(2*pi*i*t)))|) dt
      = B.

This is the logarithmic version of Doche's equations (5)–(9), specialized to the certificate's exact factors and strict degree inequality. It is a cited mathematical theorem, not something established by running a numerical integrator.

## Extraction of infinitely many algebraic numbers

The following step is from the clean-room referee's extraction argument.

Set u(z)=A(T(z))/Q(T(z))^b. It is nonconstant because its numerator has smaller degree than its denominator; coprimality precludes cancellation. If F_n(alpha)=0 then Q(T(alpha)) is nonzero: otherwise coprimality would force a contradiction with A(T(alpha))=0. Thus u(alpha)^n=1.

Near such an alpha, the denominator is a unit, so the multiplicity of alpha in F_n equals its multiplicity in 1-u(z)^n. The function v -> 1-v^n has a simple zero at u(alpha), since n*u(alpha)^(n-1) is nonzero. The multiplicity is therefore the vanishing order of u(z)-u(alpha), independently of n whenever alpha occurs. Clearing its nonvanishing denominator shows that this order is at most 2bD: the resulting numerator is a nonzero polynomial of degree at most 2bD.

Hence any fixed finite set of algebraic numbers has bounded total multiplicity among the roots of F_n, uniformly in n. For epsilon>0, suppose only finitely many algebraic numbers have h_Z<=B+epsilon. At most a bounded number of F_n's N_n roots, counted with multiplicity, could belong to that set. Every other root would have h_Z>B+epsilon. Since heights are nonnegative, their total average has liminf at least B+epsilon. This contradicts the preceding limit B.

There are therefore infinitely many distinct algebraic numbers with h_Z<=B+epsilon for every epsilon>0. By the live definition as the supremum of thresholds having a finite sublevel set, C82<=B. This argument does not assert attainment at B or infinitely many numbers with h_Z<=B exactly.

## Computational conclusion and limits

verify_best.py checks the exact finite hypotheses, composes in integer arithmetic, isolates all composed roots with FLINT, and encloses H+J with Arb using the error bounds in NUMERICS.md. evidence/best-replay.json records the enclosure; RESULT.json gives its exact dyadic endpoints and comparisons with the stated rational and frozen bar. The actual verifier command and final numerical claim are in REPORT.md.

This job's interval verifier was separately written by the same agent lineage as the search; it is not an independent checker. No earlier review is claimed to certify this new packet. These computations are not proof-assistant formalization or line-by-line human verification. Trust includes the cited averaging theorem, the height/extraction argument, Python exact arithmetic and FLINT/Arb's certified roots and ball arithmetic.
