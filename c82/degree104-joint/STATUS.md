You asked: find a certified C82 upper bound below the best public one, so the open C82 PR can carry a new bound. I will: replay #280 v3, optimize the union with round-5 factors, and run degree-104 column generation; ship a candidate unrefereed certificate below 0.2520500000 or the best certified value and why it stopped.

Started 2026-11-05. Rules read. Work stays in this directory; public data only from vidigoat, no third-party Python. Up to 3 cores, nice 10, single-threaded BLAS; wall limit 8 hours. No novelty judgment will be made, as specifically requested in the job spec.

Initial public data downloaded and hash matched. Our own ../c82r5/verify_best.py copied as verify_public.py; only EXPECTED changed from a2729a82ac3314893d9e046899cef06dc4645b9dd3bed06865ab90b51e14e6f8 to public v3 hash 00125f6984ad2646a79d8782ee38f5161bd24c17d4899e4af74ff3e529ba1dbe. Own round-5 numerics, LP, CVP, column merger, numerator pricing and rejection-control scripts copied for reuse. No third-party Python downloaded. Load ~7 initially; using one numerical worker to start.

Step 1 complete: public v3 replay PASS at 256 bits, tol 1e-13, using our round-5 verifier with only hash pin changed. Full exact dyadic enclosure in evidence/public-v3-replay.json. BAR.json frozen before step 2. Prepared exact coefficient union: 7 denominators and 895 numerators (all certificate and bank factors). The complete union is passed to the standard joint LP on the inherited N=524288 grid. Machine RAM 16 GiB; one master worker only.

For subsequent standard restricted-master column-generation iterations, zero-weight numerator columns are removed from the working master and the complete union public bank remains available to numerator pricing against each dual. All union denominator starts remain available. The initial full 895-numerator union solve is unchanged. Copied scripts changed only provenance/name prefix r5 -> r6 and numerator bank path to the complete union bank. run_cg.py orchestrates own round-5 search/LP/verifier subprocesses and saves certified checkpoints; it adds no acceptance layers beyond the requested certificate verification.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520591385259580091897, certified by a separately written (same agent lineage) interval verifier; frozen target not yet met. Source: rounds/union-certificate.json

2026-11-05 06:22:59 CVP round 0, master rounds/restricted-0.json; 2 workers, standard defaults, 240 seconds each.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520591385259548085535, certified by a separately written (same agent lineage) interval verifier; frozen target not yet met. Source: prior_sources/pr280-v3-certificate.json

Full-union LP completed in 267.97 elapsed seconds, grid objective 0.25205913844096395. Its frozen interval upper endpoint 0.2520591385259580091897 is ~3.3e-15 above the original public replay, due to exact-weight freezing differences. Reverted the incumbent checkpoint to the slightly better public certificate; the union master and its dual remain the search starting point. No scientific improvement from union reweighting alone. First standard CVP batches are producing negative complete-dual prices; awaiting the joint solve and interval certification.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520351609219488014857, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/den-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520345501400312483048, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/num-0-0-certificate.json

{"round": 0, "old_lp": 0.25205913844096395, "new_lp": 0.2520345490453377, "negative_candidates": 12, "gain": 2.458939562627327e-05, "empty_rounds": 0, "state": "rounds/num-0-0.json", "dual": "rounds/num-0-0-dual.npz"}

2026-11-05 06:28:52 CVP round 1, master rounds/restricted-1.json; 2 workers, standard defaults, 240 seconds each.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520333834288339518135, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/den-1-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520331437094862386852, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/num-1-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520331202550186422649, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/num-1-1-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520331100396671984295, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/num-1-2-certificate.json

{"round": 1, "old_lp": 0.2520345490453377, "new_lp": 0.25203310938409107, "negative_candidates": 5, "gain": 1.4396612466049952e-06, "empty_rounds": 0, "state": "rounds/num-1-2.json", "dual": "rounds/num-1-2-dual.npz"}

2026-11-05 06:37:38 CVP round 2, master rounds/restricted-2.json; 2 workers, standard defaults, 240 seconds each.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520268537560148147120, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/den-2-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520265765798675559521, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/num-2-0-certificate.json

{"round": 2, "old_lp": 0.25203310938409107, "new_lp": 0.2520265758167236, "negative_candidates": 1, "gain": 6.533567367461579e-06, "empty_rounds": 0, "state": "rounds/num-2-0.json", "dual": "rounds/num-2-0-dual.npz"}

2026-11-05 06:44:18 CVP round 3, master rounds/restricted-3.json; 2 workers, standard defaults, 240 seconds each.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520260808221596557065, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/den-3-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520260547756919434416, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/num-3-0-certificate.json

{"round": 3, "old_lp": 0.2520265758167236, "new_lp": 0.252026054313329, "negative_candidates": 3, "gain": 5.215033946348591e-07, "empty_rounds": 0, "state": "rounds/num-3-0.json", "dual": "rounds/num-3-0-dual.npz"}

2026-11-05 06:50:46 CVP round 4, master rounds/restricted-4.json; 2 workers, standard defaults, 240 seconds each.

{"round": 4, "old_lp": 0.252026054313329, "new_lp": 0.252026054313329, "negative_candidates": 0, "gain": 0.0, "empty_rounds": 1, "state": "rounds/restricted-4.json", "dual": "rounds/num-3-0-dual.npz"}

2026-11-05 06:55:02 CVP round 5, master rounds/restricted-5.json; 2 workers, standard defaults, 240 seconds each.

Standard search first no-gain round: round 4, rounds/search-4-0.json and search-4-1.json, 15 starts each, 0 negative columns, best unknown-column reduced costs +0.002749716375912925 and +0.005598727827862859; rounds/num-4-0-screen.json also adds no numerator. Grid remains 0.252026054313329, certified upper 0.2520260547756919434416. Continue the existing retry loop. If its three no-gain rounds finish, use round-5's ordinary positive-weight warm-start step: prioritize current positive-weight denominator factors and rotate starts between workers; preserve all union factors as available starts. Mathematical CVP/LP algorithms and numerical defaults stay unchanged.

{"round": 5, "old_lp": 0.252026054313329, "new_lp": 0.252026054313329, "negative_candidates": 0, "gain": 0.0, "empty_rounds": 2, "state": "rounds/restricted-5.json", "dual": "rounds/num-3-0-dual.npz"}

2026-11-05 06:59:18 CVP round 6, master rounds/restricted-6.json; 2 workers, standard defaults, 240 seconds each.

{"round": 6, "old_lp": 0.252026054313329, "new_lp": 0.252026054313329, "negative_candidates": 0, "gain": 0.0, "empty_rounds": 3, "state": "rounds/restricted-6.json", "dual": "rounds/num-3-0-dual.npz"}

Standard-order loop stopped after three no-gain rounds (4–6); rounds/original-finished.json records grid 0.252026054313329. Round 6 best unknown-column prices +0.0038275380851366947 and +0.00042944890977025807, 0 negatives; numerator bank also adds none. Starting normal positive-weight warm-start continuation, rotating positive factors between workers and retaining all inactive union denominators. No CVP, LP, or verifier numerical settings change.

2026-11-05 07:04:06 CVP round 7, master rounds/restricted-7.json; 2 workers, standard defaults, 240 seconds each.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520217896753045675490, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/den-7-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520217672252863027960, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/num-7-0-certificate.json

{"round": 7, "old_lp": 0.252026054313329, "new_lp": 0.25202176656492253, "negative_candidates": 2, "gain": 4.28774840643964e-06, "empty_rounds": 0, "state": "rounds/num-7-0.json", "dual": "rounds/num-7-0-dual.npz"}

2026-11-05 07:10:48 CVP round 8, master rounds/restricted-8.json; 2 workers, standard defaults, 240 seconds each.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520181372968908865948, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/den-8-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520179247552093577392, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/num-8-0-certificate.json

{"round": 8, "old_lp": 0.25202176656492253, "new_lp": 0.25201792465559375, "negative_candidates": 4, "gain": 3.841909328783366e-06, "empty_rounds": 0, "state": "rounds/num-8-0.json", "dual": "rounds/num-8-0-dual.npz"}

2026-11-05 07:17:16 CVP round 9, master rounds/restricted-9.json; 2 workers, standard defaults, 240 seconds each.

{"round": 9, "old_lp": 0.25201792465559375, "new_lp": 0.25201792465559375, "negative_candidates": 0, "gain": 0.0, "empty_rounds": 1, "state": "rounds/restricted-9.json", "dual": "rounds/num-8-0-dual.npz"}

2026-11-05 07:21:26 CVP round 10, master rounds/restricted-10.json; 2 workers, standard defaults, 240 seconds each.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520176699390351550701, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/den-10-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520176529516384528393, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/num-10-0-certificate.json

{"round": 10, "old_lp": 0.25201792465559375, "new_lp": 0.252017652696335, "negative_candidates": 1, "gain": 2.719592587241415e-07, "empty_rounds": 0, "state": "rounds/num-10-0.json", "dual": "rounds/num-10-0-dual.npz"}

2026-11-05 07:27:52 CVP round 11, master rounds/restricted-11.json; 2 workers, standard defaults, 240 seconds each.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520164098613484201687, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/den-11-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520163707121292354329, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/num-11-0-certificate.json

{"round": 11, "old_lp": 0.252017652696335, "new_lp": 0.2520163706878416, "negative_candidates": 1, "gain": 1.2820084934195286e-06, "empty_rounds": 0, "state": "rounds/num-11-0.json", "dual": "rounds/num-11-0-dual.npz"}

2026-11-05 07:34:26 CVP round 12, master rounds/restricted-12.json; 2 workers, standard defaults, 240 seconds each.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520163690713724570623, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/den-12-certificate.json

{"round": 12, "old_lp": 0.2520163706878416, "new_lp": 0.2520163690134206, "negative_candidates": 1, "gain": 1.6744209907493257e-09, "empty_rounds": 0, "state": "rounds/den-12.json", "dual": "rounds/den-12-dual.npz"}

2026-11-05 07:39:35 CVP round 13, master rounds/restricted-13.json; 2 workers, standard defaults, 240 seconds each.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520051490326487050550, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/den-13-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520050015677050936317, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/num-13-0-certificate.json

{"round": 13, "old_lp": 0.2520163690134206, "new_lp": 0.2520050014766615, "negative_candidates": 4, "gain": 1.13675367591215e-05, "empty_rounds": 0, "state": "rounds/num-13-0.json", "dual": "rounds/num-13-0-dual.npz"}

2026-11-05 07:45:21 CVP round 14, master rounds/restricted-14.json; 2 workers, standard defaults, 240 seconds each.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520020314352719000547, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/den-14-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520017194238047735476, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/num-14-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2520016576526502824754, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/num-14-1-certificate.json

{"round": 14, "old_lp": 0.2520050014766615, "new_lp": 0.25200165756122467, "negative_candidates": 1, "gain": 3.343915436826439e-06, "empty_rounds": 0, "state": "rounds/num-14-1.json", "dual": "rounds/num-14-1-dual.npz"}

2026-11-05 07:51:46 CVP round 15, master rounds/restricted-15.json; 2 workers, standard defaults, 240 seconds each.

{"round": 15, "old_lp": 0.25200165756122467, "new_lp": 0.25200165756122467, "negative_candidates": 0, "gain": 0.0, "empty_rounds": 1, "state": "rounds/restricted-15.json", "dual": "rounds/num-14-1-dual.npz"}

2026-11-05 07:55:56 CVP round 16, master rounds/restricted-16.json; 2 workers, standard defaults, 240 seconds each.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519967643780124960368, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/den-16-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519964916810427295401, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/num-16-0-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519964889882011727026, certified by a separately written (same agent lineage) interval verifier; frozen target met. Source: rounds/num-16-1-certificate.json

{"round": 16, "old_lp": 0.25200165756122467, "new_lp": 0.25199648892320536, "negative_candidates": 2, "gain": 5.168638019303895e-06, "empty_rounds": 0, "state": "rounds/num-16-1.json", "dual": "rounds/num-16-1-dual.npz"}

2026-11-05 08:03:36 CVP round 17, master rounds/restricted-17.json; 2 workers, standard defaults, 240 seconds each.

{"round": 17, "old_lp": 0.25199648892320536, "new_lp": 0.25199648892320536, "negative_candidates": 0, "gain": 0.0, "empty_rounds": 1, "state": "rounds/restricted-17.json", "dual": "rounds/num-16-1-dual.npz"}

2026-11-05 08:07:53 CVP round 18, master rounds/restricted-18.json; 2 workers, standard defaults, 240 seconds each.

{"round": 18, "old_lp": 0.25199648892320536, "new_lp": 0.25199648892320536, "negative_candidates": 0, "gain": 0.0, "empty_rounds": 2, "state": "rounds/restricted-18.json", "dual": "rounds/num-16-1-dual.npz"}

Rotated warm-start batch reached its 12-round batch limit. Continuing from round 19 with existing consecutive no-gain count 2; no algorithm/settings change. Prior summaries preserved in rounds/rotated-1-*.json.

2026-11-05 08:13:05 CVP round 19, master rounds/restricted-19.json; 2 workers, standard defaults, 240 seconds each.

{"round": 19, "old_lp": 0.25199648892320536, "new_lp": 0.25199648892320536, "negative_candidates": 0, "gain": 0.0, "empty_rounds": 3, "state": "rounds/restricted-19.json", "dual": "rounds/num-16-1-dual.npz"}

Shipped: candidate, unrefereed C82 < 0.2519964889882011727026, with a separately written (same agent) interval-verified certificate; frozen B < 0.2520500000 target met.
Final stop: three no-gain rounds. See REPORT.md.

Exit: search finished; final frozen-bar replay PASS, all three requested rejection controls reject; 44 Python git blobs compared with both complete public trees, no matches or foreign imports; 138 tracked PIDs checked with ps, none alive; 33949971 artifact bytes. Final REPORT.md and NOTE.md complete.
