# Gate — math_c30r1_1103

**Candidate and unrefereed: C30 >= 521/50 = 10.42.** A written proof and exact generating-function certificate are supplied. No novelty judgment. No heavy search or scaled pod phase was launched.

BAR.json was frozen at 2026-11-03 13:19:58 UTC before mathematical tests. It records Norton v3's unrefereed 10.412263 claim, the withdrawn versions, and the minimum 521/50.

## (a) Referee and withdrawals — source-audit corrections addressed

REFEREE.md audits v3 lemma by lemma, including its published BBEP dependencies. The baseline arithmetic passes the separately written (same agent) Arb verifier and seven corrupted-certificate controls.

V1's documented failure is its unjustified inference of concavity after an entropy correction. The exact ordering certificate also exhibits different shared-neighbour counts, 1196 and 1205, for identical unordered strip profiles; an ordering average cannot certify each actual pair. No such transfer or independent-neighbour pairing is used here.

Norton's [v3 arXiv Comments](https://arxiv.org/abs/2608.20292v3) explicitly identify v2's withdrawal causes: its pairing does not force the two cells of a member to agree, and its Appendix F argument count tests only arc endpoints. The original packet missed this explanation, although it was already in `sources/norton_abs_v3.txt`. Both AI reviewers found that our candidate uses neither failed point. Our physical balancing needs only common per-cell inequalities with bounded, potentially unequal boundary corrections; it never asserts identical output profiles. Our corrected, uniform Rouché majorant controls the whole contour and does not use Appendix F's endpoint-only winding test. The required historical account is now supplied; this is not a validation of v2's withdrawn 10.466425.

V2_DIAGNOSIS.md separately gives an exact rational failure of the normalization inequality printed in Lemma 5.11. V2's appendix code already corrects that factor. This repairable defect is distinct from the two documented withdrawal causes.

The final candidate does not assume v2's removed tilted-profile or concentration assertions. FIRST_MOMENT_PROOF.md derives the marginal equations, certifies their local real first moment with the corrected normalization, and supplies a separate first-moment family argument. It does not claim to verify the full withdrawn v2 route.

## (b) Proposed marginal encoding — PASS THROUGH n=14

The method-2 encoder records the value cut, standardized cell permutations, exact binary position shuffle and ordered strip information. A direct Python enumeration agrees through n=7. A separate C++ maximum-insertion traversal covers all 1324-avoiders through n=14, matching freshly retrieved A061552 at every order.

At n=14 it visits **1,209,639,642 avoiders**, checks **1,390,594,458 valid gridded domino roundtrips**, and agrees coefficient by coefficient with all five formal marginal series, including every two-or-more-leaf strip coefficient. Results and memory snapshots are on the Mini. The first generator implementation's n=5 count failure was corrected before accepting results; that failed implementation-control run is retained.

This is an exhaustive check of the proposed marginal encoding on the stated range, not a claim that finite counts prove the infinite-family theorem. The all-size decomposition and staircase argument are written in FIRST_MOMENT_PROOF.md. The coefficientwise majorization envelope also passes 1,068,643 finite integer controls, including parity cases.

## (c) Reduced growth — PASS WITH THE FIRST-MOMENT FAMILY

The initial established-profile model scored 10.4122642333 and had an exact negative target-exponent obstruction for every kappa. Those pilot results are retained; they did not justify scale-up.

The subsequent first-moment calculation certifies the actual two-leaf constant below 1/10. A positive derivative-GF argument extracts a full-growth family with bounded two-leaf counts; published BBEP concentration is used only for leaves and empty strips. BBEP's physical arch concatenation balances the family, and a proved coefficientwise envelope gives limiting coordinates

    (37037/200000, 3289/80000, 7/50, 31259/400000).

At z=50/521 the frozen rational certificate gives **Phi > 0.00018309709357909 > 0**, with root isolation, Rouché selection, saddle bracketing and tangent error all checked in Arb. Thus the candidate reaches 10.42. The verifier is **separately written (same agent)**. Thirteen corrupted candidate/first-moment certificates are rejected.

A positive target calculation and proof were obtained with bounded gate tests and light local algebra; no heavy phase was needed or launched. No finite-palette matrix candidate is claimed.

## Stop and resource accounting

No mathematical encoder counterexample was found. The invalid profile-only joint shortcut was rejected and not adopted. The 12-hour timeout was not reached and is not reported as triggered. The historical v2-diagnosis account in (a) is corrected. The bound remains conditional on BBEP and unrefereed Norton v3; the two AI reviews are not human refereeing.

The math_c30fix_1103 revision used only small local checks at nice 10. Lemma 2.1 is now proved in FIRST_MOMENT_PROOF.md and its direct exhaustive upper-cell check passes through n=9. No pod compute was used in this revision; the resource paragraph below describes the original job only.

Pod work was confined to [historical-compute-directory] on [historical-compute-host]: one worker, nice 10, BLAS thread variables one, 1,000,000 KiB virtual-memory cap. Free-memory snapshots preceded each phase. The n<=13 run took about 96 seconds; n<=14 took 710.377 seconds, with 616.636 seconds for n=14 itself. Observed worker RSS was about 4 MB; no peak-RSS claim is made. Every worker exited and all results were pulled on 3 November, before the 4 November 11:30 UTC harvest deadline. No other job or pod lifecycle was changed.
