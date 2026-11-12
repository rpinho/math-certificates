# Prior art and clean-room scope — 2026-11-12

This is a referee replay, not a search for a new construction. The job-specific clean-room restrictions take precedence over the generic broad repository survey in RULES.md. Only the supplied CLAIM.md, PROOF.md and certificate are construction inputs. No linked code or certificate packets are accessed.

The live teorth/optimizationproblems constants/82a.md defines the logarithmic essential minimum of h(alpha)+h(1-alpha). Its merged upper entries are 0.2536331090204145 (Grinsztajn) and asterisked 0.2534449 (Pinho), following Doche and Épi. The strongest inspected open upper bound is Patankar's #280 v5, 0.2519889614*, updated November 9; #330 is 0.2519923410*. #301 is 0.253091834*. Bodies and comments were read using the specified gh binary and saved in sources/. Their linked code/packets were not read. The permitted sources credit Doche's limit-point construction, weighted lattice numerator searches, CVP denominator searches and joint optimization.

Sources:
- https://github.com/teorth/optimizationproblems/blob/main/constants/82a.md
- https://github.com/teorth/optimizationproblems/pull/280
- https://github.com/teorth/optimizationproblems/pull/330
- https://github.com/teorth/optimizationproblems/pull/301
- Doche (2001), https://www.numdam.org/item/JTNB_2001__13_1_103_0/

Public literature search for Zhang–Zagier essential minimum and 2026 upper bounds found no stronger upper bound than #280 v5. It also returned 2026 lower-bound work and Burgos Gil–Menares–Qu–Sombra's convergence theorem; these do not replace the upper-bound comparison. This is not an exhaustive priority survey. The generic request to clone/reproduce other public methods is incompatible with this job's clean-room scope: old certificates cannot be replayed here. Their printed bounds are comparisons, not independently certified by this run. No predictive model is being evaluated, so predictive baseline/SBS requirements do not apply.

Novelty: the replay itself is not a new mathematical method. If it succeeds, the supplied candidate beats the inspected printed numbers under the same definition; credit for that construction remains with its producer.

Final live re-check at 2026-11-12T15:14:09Z: raw constants/82a.md and the complete #280/#330 body/comment snapshots are byte-for-byte unchanged from the initial reads. #280's latest activity is the independent v5 replay comment of November 10; #330's latest activity is November 8. The compared printed values remain 0.2519889614* and 0.2519923410*. Final snapshots are sources/82a-final.md, sources/pr280-final.json and sources/pr330-final.json. No linked code or packet was opened in the re-check.
