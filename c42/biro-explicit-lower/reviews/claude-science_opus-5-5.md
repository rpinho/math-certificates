# Referee report: LOWER_PROOF.md (sha256 3acab5f8…ba1a), claimed bound C42 ≥ 1/2 + 2^−4096

I found no false step. I re-derived every step of Sections 1–8 by hand, and checked the constants against `inputs/lower_certificate.json`. The note proves everything itself and never cites a Biró lemma as a black box.

## (1) First false or unjustified step: none found

Lemma by lemma. Throughout, the standing assumption is: for all 1≤l≤n, |S_l| ≤ q, with z_1 = 1.

- **(1)/(2) PASS.** x B′/B = Σ(1−S_l)xˡ is correct, since z_1=1 gives −Σ_{i≥2}z_iˡ = 1−S_l. Comparing coefficients of x^t gives C_{t−1} − t b_t = Σ_{j<t} b_j S_{t−j}. It is valid for 1≤t≤n and uses only S_1..S_n.
- **(3)/(4) PASS.** x C′/C = x B′/B + x/(1−x) = Σ(2−S_l)xˡ, which gives 2U_t − tC_t = Σ C_j S_{t−j}. This is used only at t≤k≤n−1. The checker also verifies (1) and (3) exactly on Gaussian-rational tuples with n=2..13.
- **Section 2, first escape, PASS.**
  - While every θ_j ≤ π/4, |C_t| ≥ |C_{t−1}| + r|b_t|, so |C_t| ≥ rA_t > qA_t. Then b_t ≠ 0 by (2), and t=n is impossible because b_n=0. So there is a first k ≤ n−1 with θ_k > π/4.
  - θ_k < π/2: otherwise |C−kb| ≥ |C|.
  - q/r = r + √2·δ, so e = √2·δ ≤ 2δ.
  - (7) follows by subtracting the increments, which have projection ≥ r|b_t|.
  - (8) uses the exact projections, and (9) gives A ≥ (1−r)/e > 1/(8δ) = 2^4093.
  - (10) holds for t≤k: the upper bound is (1+q)/t ≤ 2/t, the lower bound (r−q)/t > 1/(8t).
  - (11) holds: ∏(j+2)/j = (t+1)(t+2)/2.
- **Section 3, PASS.**
  - The distance identity is correct. The radicand q² − r²(1−(r+η)²) = δ+δ²+rη+η²/2 is correct.
  - In (13), |X cos θ − A_{j−1}/2| ≤ rη·A_{j−1} + eA, because X ∈ [rA_{j−1}, rA_{j−1}+eA], cos θ ∈ [r, r+η) and r+η < 1.
  - Bad indices contribute ≤ (5/2)A_{j−1} ≤ 20 j|b_j|, which gives the 20/η term.
  - (15): W_t + M_t = tA_t (verified by counting each |b_i|), and M_t ≤ 2W_t.
  - The numerator in (16) decomposes exactly as t|C_t| − (3/2)V_t = r(M_t − W_t/2) + t(|C_t| − rA_t) − (3/2)(V_t − rW_t).
  - The coefficients are 3 + 15/(2r) + 60/η < 20 + 60/η, and 15/2 + 12/r < 24.65 < 25.
  - Presentation only: the note should say that the b-term is divided by V_t ≥ rW_t and the other terms by V_t ≥ r·tA_t/3.
- **Section 4, PASS.**
  - A_{t₀} ≥ λA > 2^2045, so t₀ ≥ 2. Then 4t₀² ≥ (t₀+2)² ≥ A_{t₀} gives t₀ > 2^1021.
  - A_{t₀} ≤ 2A_{t₀−1} < 3λA.
  - The ratio product equals k(k+1)/((t₀+1)(t₀+2)) ≤ 2(k/t₀)², so k/t₀ > 2^1022.
  - (19)–(20): b ≤ 2^−254, 20+60/η ≤ 2^518, and the total is < 2^−252.
- **Section 5, PASS.**
  - The π/8 induction holds because 2c·sin(π/8) = sin(π/4) = r > q; the case C_t = 0 is excluded since 2c > q.
  - The squared form of (4) gives cos β ≥ (4h²+R²−q²)/(4hR), and this equals F(h) at R=3/2, q=1/2.
  - The secant coefficients 10/21, 5/18 and 1/30.24 come from the correct endpoints (smallest h and R).
  - The recurrence is valid, and a = 6(Z+δ) is its exact fixed point. The positive part is now written in (23).
  - w_t ≥ 1/t because R_t ≥ 7/5 > t/(t−1) for t ≥ 4.
  - 27t⁴ − (3t−1)³(t+1) = 18t² − 8t + 1 > 0, so the product is < (t₀/k)^(1/3) < 2^−340.
- **Sections 6–7, PASS.**
  - Σw_j ū v_j = h exactly, Σw_j|ū v_j − 1|² = 2(1−h), and Cauchy–Schwarz gives the conversion bound.
  - The d² expansion is correct.
  - (29): Bernoulli gives (1+1/(8j))⁸ ≥ 1+1/j, which telescopes to k/m.
  - (30): |b_j| ≤ 2A_j/j ≤ 2|C_j|/(rj), V ≤ kA, and k/j ≤ 2/σ.
  - (31): 1/32 + 30/4096 ≈ 0.0386 < 1/16.
  - (32) is exact: C_{k−1}/2 − k b_k = Σ b_j(S_{k−j} − 1/2).
  - The contradiction r(r−1/2) ≈ 0.146 > 1/16 holds.
- **Section 8, normalization, PASS.** The table defines R_n as the minimum over max_i|z_i| = 1 [LIT: table_42a.html]. Dividing by a unit-modulus component maps such a tuple into the z_1=1 class without changing any power-sum modulus. The minimum is attained by compactness, so R_n > q for every n, and limsup R_n ≥ q. The conclusion is ≥, not >, and the note says so.

**Numerical tests** [MEASURED, `c42_lower_referee_tests.py`]:
- I took 3 near-optimal tuples (n=44, 52, 60; q* = 0.70539, 0.70321, 0.70154 < 1/√2) and 300 small perturbations of them. In each case I set q = q* and checked every general-q statement: (1)–(16), the π/8 lemma, (21), the first half of (22), the projection recursion, the (26)/(32) identities, the conversion bound, d², (29) and (30). There were zero failures; k was between 11 and 15.
- Random sampling of the (22) perturbation bound used at most 22% of its stated slack; the (25) bound used at most 43%.
- **Weak spot of these tests:** the certified parameter regime needs k > 2^2043, so Sections 4–7 with the actual constants can only be checked by hand. The (16) test is also loose at small t, where the 25/t term dominates.

**Checker** [MEASURED, `python verify_lower_exact.py`, run on a copy, 0.13 s]:
- Status PASS_EXACT_NUMERICAL_HYPOTHESES, 59 checks, hashes match the manifest, and 6/6 negative controls are rejected.
- It does test the numerical hypotheses the proof uses, including c > 9/10 via cos²(π/8) = (1+r)/2, and it checks the two telescoping polynomial identities.
- Trivial constants such as 2(1+r) ≤ 4 and (5/2)·8 = 20 are not encoded. It is the same agent's second implementation, not an independent review.

**Reviewer pass.** I gave four narrower questions to a separate model. It returned four FAIL claims, at (16), (22), (30) and (17), and all four are its own errors:
- (16): it divided the b-term by the wrong lower bound on V_t.
- (22): it called the endpoint wrong, but h=9/10, R=7/5 is the correct one.
- (30): it said A_j ≤ |C_j|/r runs the wrong way; it does not.
- (17): it missed that A > 2^4093 makes λA > 2^2045 an absolute floor.

## (2) Uses of Biró's paper [LIT: biro2000.txt]

Each Biró item below is matched to its counterpart in the note; no Biró statement is invoked as a black box, so there are no imported hypotheses to verify.

| Biró | Note | Status |
|---|---|---|
| (3), (4) Newton–Girard with z₁ = 1 | (1), re-derived by generating function | Stated correctly |
| Lemma 2: first α_k > π/4, and α_k < π/2 | Section 2 | Same structure, proved explicitly |
| Lemma 6: R_t = 3/2 + O(·) | (16), (20) | Explicit constants replace the f-functions |
| (14), summed formulas | (3) | Identical |
| Lemma 7: β_t ≤ π/8 | Section 5, start | Identical argument |
| Lemma 8: h_k → 1, using the attractive fixed point of F(h) = (2h²+1)/(3h) | (22)–(24) | Replaced by a contraction recurrence; Biró argues by contradiction |
| Section 4: conversion and the H_c split | Sections 6–7 | Different, self-contained route via the early/late split (29)–(31) |

Biró's theorem uses the z₁ = 1 normalization and says it is trivially equivalent to the max-modulus one. The note checks that equivalence itself.

## (3) The step I trust least

The constant bookkeeping in (14)–(16). It has the most terms, the special t=k term, and three error sources combined. Its numerical test is weak, and the certified regime is never exercised on real tuples. I re-derived it term by term and it holds, but it rests on one hand check (mine) plus the author's.

## (4) Novelty and worth

- **Absent from the page.** The C42 page as fetched today lists ">1/2 Biró [Bir00b]", with the note that the computable constant was not computed [LIT: table_42a.html]. Biró writes that he does not compute a concrete value of q [LIT: biro2000.txt]. So an explicit q is absent from the page and from the source.
- **Not checked by me.** I could not check open PRs or arXiv in this session. The claim that none of the 46 open PRs has an explicit lower value comes from the author's PRIOR_ART.md, and I have not verified it.
- **Blunt assessment.** The gain is 2^−4096 ≈ 9.6 × 10^−1234. It says nothing about where C42 lies in [1/2, 0.687]. Its only value is that it turns ">1/2" into a number, which would be at most an asterisked lower-bound row. It is a quantification of Biró's method, not a new idea, and the note says so. I would file it only if the table maintainers want explicit values for qualitative rows. Otherwise it is too small to matter.
- **Asterisk.** This review is AI-to-AI, so it cannot remove the asterisk.

## (5) Probability the bound is correct: about 0.95

Basis:
- Biró's qualitative theorem is refereed.
- Every analytic step was re-derived here, and the exact checker passes all the numerical comparisons.
- The general-q inequalities hold on 303 explicit tuples.
- The remaining risk is a hand-algebra slip, in the k > 2^2043 regime, that both the author and I missed. Only one referee did the hand check.

---
**VERDICT.**
- No false or unjustified step was found. The bound C42 ≥ 1/2 + 2^−4096, with R_n > 1/2 + 2^−4096 for every n, follows. The only flags are presentation: which lower bound on V_t is used for which term in (16), and the reuse of the letter b for the radial error.
- The three defects found in the earlier version (sha 922f2a4e) — missing positive part in (23), missing manifest, missing PRIOR_ART.md — are fixed here [OURS: memory].

**PROBABILITIES.**
- The bound is correct: 0.95 (full hand re-derivation, exact checker, 303 tuple tests, Biró refereed).
- It is the first explicit q > 1/2 anywhere: about 0.7 (the page and Biró show none; PRs and arXiv were not checked by me).

**IDEAS.**
- Do one human or second-party line check of (14)–(16) and (22) before filing. Bar: an independent party re-derives the coefficients 20+60/η, 25 and 1/20.
- Ricardo approves draft row wording only after the open PRs and arXiv have been checked on the filing date.

**OUT_OF_BOUNDS.**
- Re-tuning the exponents (δ might reach roughly 2^−1000 within the same scheme; this is my inference) is mechanical polishing of the same construction with no new input, so I did not pursue it.
- No PR or comment drafting beyond this report.

Files are in the workspace:
- [c42_lower_referee_tests.py](#) — floating-point tests of the general-q inequalities; not a certificate.
- [c42_lower_referee_tuples.npz](#) — the three test tuples (n = 44, 52, 60).

VERDICT: PASS
