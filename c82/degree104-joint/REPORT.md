Shipped: candidate, unrefereed C82 < 0.2519923410, certified upper endpoint 0.2519923409720083953971; frozen B < 0.2519900000 target not met.

Certified B ∈ [0.2519923409720083869767, 0.2519923409720083953971]. Exact dyadic endpoint < 251992341/1000000000: True. Exact endpoint < 25199/100000: False. RESULT.json contains the exact Fraction comparisons and margins.

Gap below our printed round-6 0.2519964890: at least 0.0000041480279916046029. Gap below Patankar #280 v4 0.2520079724: at least 0.0000156314279916046029. A positive gap means the certified endpoint is smaller. No novelty judgment is made, as requested.

This is a candidate, unrefereed Doche construction. The interval verifier was separately written (same agent), uses stdlib + python-flint only, and imports no search helper. It checks exact integer polynomial composition, positive integer denominator multiplicities, nonnegative exact rational numerator powers, strict degree inequality, all active numerator/denominator gcds, certified composed-root isolation and interval integration. The Doche reduction and arithmetic backend are not formalized here. PROOF.md gives the inherited mathematical argument; NUMERICS.md describes the enclosure formulas.

Final certificate: 8 denominator factors, 18 numerators, D=999999999856, deg A=939550863051360379/1048576; 144 gcd pairs and 2224 composed roots. Exact q_rational values are unchanged by equal-fraction encoding; CERTIFICATE_ENCODING.md lists the doubled encodings. Certificate SHA256: ee9622b5e141489ad6fbf98b0ec5c43ac3e1b657f8876b435e65c536f359fdd5.

Before the union solve, both inputs were replayed locally with our separately written verifier. Our round-6 release gives upper endpoint 0.2519964889882011727026; Patankar v4 gives B = 0.25200797232842968… . See evidence/round6-replay.json and evidence/pr280-v4-replay.json. The v4 JSON SHA256 matches c1981f1c4f5e1813f625c54ce952e9b5fa210f2cccbd5ac832d2a41f12ccc72f.

BAR.json was written before step 1. The complete joint master used the union of round-6 final factors, Patankar v4, the round-6 union bank and all coefficient dictionaries/candidate factors found in saved round-6 states. There are 104 initial denominator arrays and 913 numerator arrays. The inherited N=524288 grid, HiGHS simplex and full-grid row generation were used. rounds/union-lp.json records its numerical objective; rounds/union-replay.json certifies its exact frozen weights.

Our own c82r6/c82r5 numerics.py, joint_lp.py, cvp_search.py, add_columns.py, numerator_search.py, run_cg.py, rejection controls, verifier and numerical notes were copied and reused. The core algorithms/defaults were preserved. The initial full-matrix np.column_stack copy hit shared-memory thrashing for over 11 minutes before any LP solve (8 GB footprint); the LP file was reverted, then retried with a single column-contiguous raw-log matrix and scaled active rows, retaining the same factors/grid/LP. STATUS.md and stack samples record the resource failure. Changes: r7 labels, complete union assembly, input-shape handling for historical JSON, degree-104 direct warm-start filtering, exact fraction encoding, updated checkpoint/provenance reporting and stopping on actual LP gain. The initial historical reader failed on a list-valued metadata JSON; the added launcher was reverted before that input correction. STATUS.md records it.

The inherited weighted-CVP method uses degree 104; H=X(X−1)P4 residue restriction; 1024 stratified weighted-evaluation samples; 380-bit evaluation arithmetic; exact integer Gram LLL with delta .99; 16 retained Schnorr–Euchner points; four million nodes; up to eight IRLS steps. Two 240-second single-threaded workers use each new dual. All union degree-104 denominators are direct warm starts; degree-44/60 archive products are also starts. Complete numerator-bank pricing follows each round. Zero numerator columns are removed only from restricted masters, retaining the full bank for pricing. Search objectives and reduced costs are heuristic; only frozen, interval-verified certificates support the stated bound. No CVP optimality claim is made.

Stopping reason: three no-gain rounds. 8 rounds. The per-round gains and final master/dual paths are in rounds/finished.json; SEARCH_SUMMARY.json records the batches.

The first attempt was interrupted during round-one searches (saved elapsed values about 206 and 204 seconds of the requested 240 seconds). Resume attempt 2 consumed their checkpointed candidate, re-solved and certified it, then continued full standard batches from round 2. Completed input replays, union solving and saved searches were not repeated; the original job clock was retained. Recovered interrupted-search CPU times are lower bounds, with the missing tails covered conservatively in COMPUTE.json.

Another identical round is not recommended now: three consecutive rounds had LP gain below 1e-10. This is a plateau for these starts, duals and budgets, not an optimality result.

Factor provenance follows by full coefficient-array comparison; names are labels only. FACTOR_PROVENANCE.json retains every array, exact weight and all source matches.

| Denominator | Provenance | Degree | Multiplicity |
| --- | --- | ---: | ---: |
| D11_5_0 | #280 v3 (also #280 v4; ours from round 6) | 104 | 535392071 |
| C82r6_8c76cd0c4e53 | ours from round 6 | 104 | 2423151756 |
| C82r6_935548ec48fe | ours from round 6 | 104 | 1016015938 |
| C82r6_083ca9b3950a | ours from round 6 | 104 | 2312376210 |
| D11_12_0 | #280 v4 | 104 | 1064507467 |
| D31_5_0 | #280 v4 | 104 | 714907509 |
| C82r7_dd0a7c419abf | new here | 104 | 1259711048 |
| C82r7_7883918fa4f2 | new here | 104 | 289322615 |

Numerator provenance (full coefficient comparison):

- P1: #280 bank; #280 v3; #280 v4; ours from round 5 or earlier; ours from round 6; q=11703164896719798/65536.
- P2: #280 bank; #280 v3; #280 v4; ours from round 5 or earlier; ours from round 6; q=5632704471962942/32768.
- P3: #280 bank; #280 v3; #280 v4; ours from round 5 or earlier; ours from round 6; q=646486510239618/65536.
- P4: #280 bank; #280 v3; #280 v4; ours from round 5 or earlier; ours from round 6; q=6210906942666694/262144.
- P6: #280 bank; #280 v3; #280 v4; ours from round 5 or earlier; ours from round 6; q=10962525976345770/524288.
- MS360: #280 bank; #280 v3; #280 v4; ours from round 5 or earlier; ours from round 6; q=3972053051256186/2097152.
- n11_4_53: #280 v3; ours from round 6; q=1687279140887082/1048576.
- n11_6_21: #280 v3; #280 v4; ours from round 6; q=2165347480543406/1048576.
- n101_0_17: #280 bank; #280 v3; ours from round 6; q=814884675258786/2097152.
- n121_3_30: #280 bank; ours from round 6; q=1956034609316410/1048576.
- n11_6_49: #280 v3; #280 v4; ours from round 6; q=2068654955694178/2097152.
- n101_7_34: #280 bank; ours from round 5 or earlier; ours from round 6; q=611610685923002/2097152.
- n11_7_17: #280 v4; q=758287981590426/1048576.
- n11_10_5: #280 v4; q=346423862837566/2097152.
- n11_10_6: #280 v4; q=85070234974037/524288.
- n31_6_7: #280 v4; q=1196116623818586/2097152.
- n101_0_28: #280 bank; q=843331835018878/1048576.
- cg2_4_0_c2: #280 bank; #280 v3; ours from round 5 or earlier; q=319456524303830/2097152.

Rejection controls: changed bytes, zero multiplicity with repinned hash, and shared numerator/denominator factor with repinned hash all rejected: True. See evidence/rejection-controls.json and individual logs. The exact endpoint check against the stated rational is in RESULT.json.

No Python from vidigoat/optimization-records was downloaded, copied, imported or executed. Every .py in this job directory, including generated pinned verifier copies, was hashed with git hash-object and compared against every blob in the complete GitHub trees at 197962c9610f583e9bc56efe37bfb994c1eeb834, 3a7a84fec9c64ae426f06a5f52597c84b3453ba0 and 79ce0dfb211a67ff7e387b58b0d19ff1d6accfba. None equals any blob in those trees; AST import inspection confirms none imports their modules. PYTHON_BLOBS.json lists every file/hash/import. Only JSON data and tree metadata were read from that repository.

Method/factor credit: Doche; Grinsztajn and Epi; R. Pinho PR #301 joint LP, residue restriction and pricing; our earlier search factors; V. Patankar PR #280 weighted CVP, product starts and public coefficient JSON. THIRD_PARTY_NOTICE.md records data/method credit.

PRIOR_ART.md records the scoped source review: live official table, open PRs #280/#330 and the open-PR list; updated-first repository search; seven lab/result repositories; inherited same-day awesome-list searches; Doche publisher page and recent primary arXiv/author sources; focused community searches. Final source refreshes are saved in prior_sources/*-final.*. The live merged table and open-PR values are public comparators, not a worldwide priority judgment.

Measured/recovered bootstrap and CG CPU: at least 1.4443 core-hours; conservative total upper estimate 1.6652 core-hours including unsaved interrupted-search tails and a 0.01 core-hour setup/reporting allowance. Wrapper aggregates are excluded to avoid double counting. Wall time 1.177 hours. Single-threaded BLAS/HiGHS/FLINT, nice -n 10 (effective nice 20); two parallel CVP workers and no overlapping LP/replay. Mini load was checked. COMPUTE.json records accounting. Process cleanup is recorded in evidence/process-cleanup.json. All writes stayed in the job directory; no commits, pushes, PRs, posts, uploads or messages.

Reproduce the certificate at the stated rational:

```sh
./run_local.sh verify_best.py --certificate certificate.json --target 0.2519923410 --precision 256 --tol 1e-13 --out evidence/reproduced-best.json
```

REPRODUCE.md gives input replay, union LP, CVP and rejection-control commands. Every numerical solve is checkpointed, with the best certified certificate retained incrementally.
