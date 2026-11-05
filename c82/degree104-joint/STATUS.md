You asked: find a certified C82 upper bound below the best public one, so the open C82 PR can carry a new bound. I will: run the joint union LP and closest-vector column generation, and ship a candidate, unrefereed certificate below 0.2519900000 or report the best certified value and why it stopped.

Started 2026-11-05. Maximum wall time eight hours; at most three cores, nice 10, single-threaded BLAS. All writes remain in this job directory. Public sources are read only. No publishing or messages.

Failure in ['prepare_union.py'], exit 1, log logs/prepare.log. Retained previous certified certificate and previous master state; stopping for investigation.

Initial bootstrap command exited 1. Reverted the newly added bootstrap launcher by moving it to evidence/failed-bootstrap.py before investigating; no incumbent certificate was changed. Inspecting logs next.
Failure located: prepare_union.py:13 called .get on a list-valued historical round JSON (AttributeError). The standard solver/search has not run or failed. Restore bootstrap with one input-shape correction: skip round JSONs that are not dictionaries; preserve all factor dictionaries. This is fix 1 for this failure.

Reusing our own round-6 numerics.py, joint_lp.py, cvp_search.py, add_columns.py, numerator_search.py, run_cg.py, rejection_controls.py and separately written verifier. Changes before the first solve: r7 factor labels; q_rational equal-fraction encoding; include all historical coefficient dictionaries; no-gain stopping counts actual LP gain rather than mere negative proposals; frozen comparator/provenance checkpoint text updated. Core algorithm and defaults unchanged. Two 240-second single-threaded CVP workers per dual, all union factors as warm starts; at most three cores.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519964889882011727026; frozen target not yet met. Source prior_sources/round6-certificate.json

Union assembled: 104 distinct denominator coefficient arrays and 913 numerators, including historical round-6 candidate/state factors and the v4 data. The degree-104 CVP warm list filters direct starts to degree 104; degree-44 and degree-60 archive factors remain available through the inherited product-start mode. This preserves the inherited degree restriction with the larger bank.

2026-11-05 09:16 EST: standard full-union attempt failed to reach the first LP solve after >11 minutes (PID 87843, joint_lp.py:28 np.column_stack; 104+913 columns, N=524288, 8.0 GB physical footprint). Two stack samples minutes apart remained entirely in NumPy strided array concatenation (logs/union-sample.txt and union-sample-2.txt), with heavy system compression/swapping. No numerical claim or incumbent changed. Reverted joint_lp.py to our original round-6 copy before stopping/investigating this resource failure; pre-change copy retained at evidence/pre-memory-joint_lp.py.

Change for retry: retain one Fortran-contiguous raw log matrix, filled column by column; construct scaled rows only for active constraints, and compute g from raw logs and weights. This keeps the identical full grid, factor union, LP constraints, defaults and exact-weight freezing, but avoids the all-columns list/strided-copy and permanent scaled duplicate. Resource-failure fix 1. No algorithmic search deviation.

Failure in ['joint_lp.py', '--input', 'union-input.json', '--prefix', 'rounds/union'], exit -15, log logs/union.log. Retained previous certified certificate and previous master state; stopping for investigation.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519933832441540561187; frozen target not yet met. Source rounds/union-certificate.json

2026-11-05 09:20:03 CVP round 1, master rounds/restricted-1.json; 2 workers, standard defaults, 240 seconds each.

2026-11-05 resume attempt 2: no numerical workers from attempt 1 remain. Union replay and both round-one CVP outputs are complete; resume at their merge, without repeating finished searches. The original eight-hour clock in evidence/start.json is retained.

Resume correction: round-one JSON files are usable iteration checkpoints, not completed batches: logs have no finished event and elapsed values are about 206/204 seconds of the requested 240. The interruption ended both searches. Their saved candidate is being merged; no search output is discarded. Subsequent rounds retain full standard 240-second batches. Recovered process_time values are lower bounds (less than one unsaved trial tail may be missing).

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519933783462382706207; frozen target not yet met. Source rounds/den-1-certificate.json

{"round": 1, "old_lp": 0.2519933831279051, "new_lp": 0.25199337827284685, "negative_candidates": 1, "gain": 4.855058244324084e-09, "empty_rounds": 0, "state": "rounds/den-1.json", "dual": "rounds/den-1-dual.npz"}

2026-11-05 09:31:04 CVP round 2, master rounds/restricted-2.json; 2 workers, standard defaults, 240 seconds each.

2026-11-05 09:35:27 shared load observation: 9:35  up 4 days, 20:09, 3 users, load averages: 37.48 20.42 14.13. Two CVP workers only, single-threaded, effective nice 20; each current batch remains capped near 240 seconds. No compute-limit increase or algorithm change.

{"round": 2, "old_lp": 0.25199337827284685, "new_lp": 0.25199337827284685, "negative_candidates": 0, "gain": 0.0, "empty_rounds": 1, "state": "rounds/restricted-2.json", "dual": "rounds/den-1-dual.npz"}

2026-11-05 09:35:29 CVP round 3, master rounds/restricted-3.json; 2 workers, standard defaults, 240 seconds each.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519932812161828876439; frozen target not yet met. Source rounds/den-3-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519932805012129085575; frozen target not yet met. Source rounds/num-3-0-certificate.json

{"round": 3, "old_lp": 0.25199337827284685, "new_lp": 0.25199328040154245, "negative_candidates": 1, "gain": 9.787130439420366e-08, "empty_rounds": 0, "state": "rounds/num-3-0.json", "dual": "rounds/num-3-0-dual.npz"}

2026-11-05 09:44:23 CVP round 4, master rounds/restricted-4.json; 2 workers, standard defaults, 240 seconds each.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519924802801214891560; frozen target not yet met. Source rounds/den-4-certificate.json

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519924502851640209556; frozen target not yet met. Source rounds/num-4-0-certificate.json

{"round": 4, "old_lp": 0.25199328040154245, "new_lp": 0.2519924501984266, "negative_candidates": 1, "gain": 8.302031158646805e-07, "empty_rounds": 0, "state": "rounds/num-4-1.json", "dual": "rounds/num-4-1-dual.npz"}

2026-11-05 09:52:37 CVP round 5, master rounds/restricted-5.json; 2 workers, standard defaults, 240 seconds each.

Certified checkpoint: Shipped: candidate, unrefereed C82 < 0.2519923409720083953971; frozen target not yet met. Source rounds/den-5-certificate.json

{"round": 5, "old_lp": 0.2519924501984266, "new_lp": 0.25199234090902256, "negative_candidates": 1, "gain": 1.0928940402665788e-07, "empty_rounds": 0, "state": "rounds/den-5.json", "dual": "rounds/den-5-dual.npz"}

2026-11-05 09:58:03 CVP round 6, master rounds/restricted-6.json; 2 workers, standard defaults, 240 seconds each.

{"round": 6, "old_lp": 0.25199234090902256, "new_lp": 0.25199234090902256, "negative_candidates": 0, "gain": 0.0, "empty_rounds": 1, "state": "rounds/restricted-6.json", "dual": "rounds/den-5-dual.npz"}

2026-11-05 10:02:16 CVP round 7, master rounds/restricted-7.json; 2 workers, standard defaults, 240 seconds each.

{"round": 7, "old_lp": 0.25199234090902256, "new_lp": 0.25199234090902256, "negative_candidates": 0, "gain": 0.0, "empty_rounds": 2, "state": "rounds/restricted-7.json", "dual": "rounds/den-5-dual.npz"}

2026-11-05 10:06:30 CVP round 8, master rounds/restricted-8.json; 2 workers, standard defaults, 240 seconds each.

{"round": 8, "old_lp": 0.25199234090902256, "new_lp": 0.25199234090902256, "negative_candidates": 0, "gain": 0.0, "empty_rounds": 3, "state": "rounds/restricted-8.json", "dual": "rounds/den-5-dual.npz"}

2026-11-05 10:14:35 Shipped: candidate, unrefereed C82 < 0.2519923410, certified upper endpoint 0.2519923409720083953971; frozen B < 0.2519900000 target not met.
Final stop: three no-gain rounds (6–8); eight rounds total. Final replay at 0.2519923410 passed. The frozen 0.2519900000 target was not met. Required rejection controls and Python blob/import comparison completed; all tracked numerical workers have exited. See REPORT.md, RESULT.json, FACTOR_PROVENANCE.json and COMPUTE.json. No publishing, commits, PRs, posts or messages.
