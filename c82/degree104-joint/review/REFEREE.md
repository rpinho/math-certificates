# Referee report: C82 certificate, claim C82 < 0.2519694759 (round 12)

Referee: Claude Opus 5.5 (claude-opus-5-5), clean room. Inputs read: inputs/CLAIM.md, inputs/PROOF.md and inputs/certificates/certificate.json (sha256 checked against INPUTS_SHA256SUMS), plus RULES.md and this job's spec. Public sources read: teorth/optimizationproblems constants/82a.md, and the bodies and comments of PRs #87, #280 and #330. I did not read or run any producer code, packet or other file under math_wave_1030/, math-certificates/ or the rpinho and vidigoat repositories.

**Result.** The argument is sound and the certificate meets every hypothesis exactly. My independent interval replay gives

    0.2519694758380326654679408 <= B <= 0.2519694758382429035635232

This contains the producer's interval [0.2519694758381300638735, 0.2519694758381300658953]. The upper end is 6.18e-11 below 0.2519694759, so **C82 < 0.2519694759 holds**. It is 1.25e-8 below the live best printed value, #280 v6 (0.2519694883*). I found no gap.

## 1. Does the reduction prove C82 <= B? (attacks on PROOF.md)

**Definition.** Live 82a: h is the absolute logarithmic Weil height, written with the leading coefficient of the primitive minimal polynomial, h_Z(α) = h(α) + h(1-α), and C82 is the supremum of H such that {h_Z ≤ H} is finite. PROOF.md uses natural logs and h(α) = log M(P)/deg P. That is the same height, so the normalization matches. Doche writes multiplicative heights, and taking log turns his statement into this one. No factor of 2 is missing or added: deg F_n = 2bnD, and the root average of h_Z is 2 log M(F_n)/(2bnD), because F_n(1-z) = F_n(z) and T(1-z) = T(z).

**Construction.** F_n = Q(T)^{bn} - A(T)^n = ∏_{ζ^n=1}(Q(T)^b - ζA(T)), which is exact (∏(x - ζy) = x^n - y^n). The hypotheses do what the proof needs:
- Q is monic and deg A = ba < bD, so every factor Q(T)^b - ζA(T) has fixed degree 2bD and leading coefficient ±1. F_n is therefore ± a monic integer polynomial, all of its roots are algebraic integers, and the root average of h_Z equals log M(F_n)/(bnD).
- Doche's averaging step. Because the leading coefficient is fixed, ζ ↦ log M(Q(T)^b - ζA(T)) is continuous on the unit circle: log M = Σ log⁺|root|, and the roots move continuously. The roots-of-unity averages are Riemann sums, so they converge to ∫ log M(Q(T)^b - e(s)A(T)) ds. By Fubini and Jensen in y, that integral equals ∫ max(b log|Q(T)|, log|A(T)|) dt. Dividing by bD gives B = H + J. I checked this step independently; it does not depend on anything beyond Doche's lemma.
- Extraction (infinitely many α). Coprimality gives Q(T(α)) ≠ 0 at every root α of F_n. The multiplicity of α equals ord_α(A(T) - u(α)Q(T)^b) ≤ 2bD, uniformly in n. So a finite set of numbers carries at most C (independent of n) of the N_n = 2bnD roots, and the liminf/contradiction argument goes through. Heights are ≥ 0. The conclusion "for every ε, infinitely many α with h_Z ≤ B + ε" gives C82 ≤ B under the live sup-definition.

Attacks tried, none successful:
- A non-monic numerator S_i. Harmless: its leading coefficient enters only A, which has lower degree. F_n stays monic, and the leading coefficient's log appears in g as the constant c.
- Fractional q_i. b = lcm of the denominators (2^20 here) makes A an integer polynomial, and deg A = ba is the exact condition. The checker verifies a < D in exact rationals.
- A zero of Q∘T on the circle, which would make g unbounded above. None: gcd(R_j∘T, reversed(R_j∘T)) = 1 for all six j, and no isolated root has |ρ| = 1 undecided.
- Q(0) = 0 or Q(1) = 0, which would clash with P1 = X and P2 = X - 1. Excluded, because gcd(P1, R_j) = gcd(P2, R_j) = 1 was checked for all j.

**The specific point: P1 = X and P2 = X - 1 vanish on the composed circle.** P1∘T = z(1-z) vanishes at z = 1 (t = 0). P2∘T = -(z² - z + 1) vanishes at z = e^{±iπ/3} (t = 1/6, 5/6). My exact check also finds a third circle zero the attack note did not mention: P4∘T contains Φ10 (gcd(P4∘T, reversed) = x⁴ - x³ + x² - x + 1), so A∘T also vanishes at t = 1/10, 3/10, 7/10, 9/10. None of these zeros affects the theorem:
1. At such z, F_n(z) = Q(T(z))^{bn} ≠ 0. They are not roots of F_n, and the extraction never meets them.
2. Doche's averaging needs only a fixed leading coefficient in z. Zeros of A(T) do not affect the continuity of ζ ↦ log M(Q(T)^b - ζA(T)).
3. In the limit integrand max(b log|Q∘T|, log|A∘T|), a zero of A∘T makes the second argument -∞, so the max is the finite b log|Q∘T|. In J this means g → -∞ there and max(0, g) = 0 nearby. These zeros can only lower J; they cannot create a singular positive contribution. The only requirement is that A and Q share no zero, and the gcd check covers that.

My checker handles these points rigorously rather than by excision. Its non-analytic branch uses one-sided bounds: for a positive-weight root touching the ball, it uses log of the upper bound of |w - σ| and sets the lower side to -∞. The analytic branch returns a non-finite value whenever a log touches its branch cut, which forces Arb to subdivide down to the direct enclosures around those points.

**Finite hypotheses on the certificate (exact, in check.py).** All 6 + 38 coefficient lists consist of Python ints. The 6 denominators have degree 104, are monic and irreducible. Multiplicities are positive integers. The 38 q_i are strict `p/q` strings with q_i > 0 and common denominator 2^20. D = 740384615402384615382720. a/D ≈ 0.89754 < 1, checked exactly. All 228 active (S_i, R_j) pairs have constant gcd. The six rejection controls (non-monic denominator, a numerator sharing a factor with a denominator, a ≥ D, a decimal exponent, zero multiplicity, a non-integer coefficient) are all rejected.

## 2. Clean-room replay

The checker is replay/check.py: about 420 lines, standard library plus python-flint, with no `math` import, no `float(...)` and no float literals. Method and full outputs are in replay/report.md. In summary:
- H: rigorous FLINT isolation of all 6 x 208 roots of R_j∘T, with log M evaluated in Arb (each |root| decided against 1). H in [0.2519693873279416368328252, 0.2519693873279416368328253].
- J: Arb's rigorous integrator, acb_calc_integrate at 192 bits with tolerances 2^-60 absolute and 2^-50 relative. The integrand is max(0, g) in root form over 1863 isolated w-plane roots. The analytic flag is honoured: it returns the analytic continuation of g only where Re g > 0 on the whole ball, returns 0 where Re g < 0, and otherwise returns a non-finite ball. Non-analytic calls use one-sided bounds at log singularities. Sign changes and the -inf points from P1, P2 and P4 are therefore resolved by Arb's bisection and direct enclosures, with no excision. J in [8.85100910286e-8, 8.85103012667e-8].
- B in [0.2519694758380326654679408, 0.2519694758382429035635232]: **PASS** against 0.2519694759. Run time 1758 s on one core; peak RSS 35.6 MB, within the 1 GB cap.
- Controls:
  - Three analytic cases with known B: log 3; log 7 with g > 0 everywhere; and a two-crossing case checked against an independent 1-D Arb integral. All agree to below 1e-15.
  - The false target 0.2519694758 is rejected.
  - Perturbed denominator coefficient: B = 0.2568327082, a disjoint enclosure.
  - Doubled exponent of N82r12_59d304ca3db3: B = 0.2519949546, a disjoint enclosure.
  - Six malformed certificates are all rejected.
- Disclosure: a run at tolerance 2^-50 gave an enclosure 1.1e-10 wide whose upper end is above the bar. That is too coarse to decide, not a counterexample, and the claimed value lies inside it. A 2^-70 run was stopped unfinished after about 40 minutes.

## 3. Comparison with the live values

| value | source | relation to this enclosure (upper end 0.25196947583824) |
|---|---|---|
| 0.2519694883* | #280 v6 (vidigoat, 14 Nov), live best | this bound is 1.246e-8 lower |
| 0.2519696460* | #330 (our PR, 13 Nov) | this bound is 1.702e-7 lower |
| 0.2534449* | merged 82a page, best upper entry | this bound is 1.48e-3 lower |

Live re-check on 2026-11-20: no newer C82 value appears in the bodies or comments of #280, #330, #87, #242 or #301. Under the same definition and the same type of evidence, an interval-verified Doche certificate, the new bound is below every printed value. That makes it a new candidate record, subject to the usual review on the upstream PR.

## 4. Caveats

These are notes on the trust base, not defects in the claim.
- **Trust base.** FLINT root isolation, Arb ball arithmetic and acb_calc_integrate, the python-flint bindings, and the correctness of my integrand's analytic-flag logic, which the analytic controls exercise. This is an AI referee (Claude Opus 5.5), not a human or a proof assistant. I do not know the producer's model; the spec says it differs from mine.
- **Unverified references.** PROOF.md cites RESULT.json, verify.py, NUMERICS.md and an earlier round's referee extraction argument. None of them was supplied, and none was needed. Its numbers (D, a and the 228 pairs) are not stated in PROOF.md itself; I recomputed them.
- **P4 zeros on the circle.** P4∘T also vanishes on the circle (the factor Φ10), which neither PROOF.md nor the attack note mentions. As with P1 and P2, this only adds -inf points to g and is harmless.
- **Doche's averaging step.** I re-derived it instead of taking it on citation: the leading coefficient is fixed, so log M(Q(T)^b - ζA(T)) is continuous in ζ and the Riemann sums converge. The rest follows from Jensen and Fubini.

VERDICT: HOLDS
