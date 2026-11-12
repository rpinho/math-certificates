Shipped: candidate, unrefereed C82 < 0.2519758217; the certified upper endpoint is below the frozen 0.2519889613 bar.

Certified B lies in [0.2519758216376568634394, 0.2519758216376568674750]. The exact dyadic upper endpoint is strictly below 2519758217/10000000000: True. RESULT.json records the exact endpoint fractions and rational comparisons. Gap below our round-7 printed 0.2519923410: at least 0.0000165193623431325250. Gap below PR #280 v5's printed 0.2519889614: at least 0.0000131397623431325250. Positive gaps mean the endpoint is smaller. No novelty judgment is made.

This is a candidate, unrefereed Doche construction. The interval verifier is separately written (same agent), uses stdlib + python-flint only, and imports no search helper. It checks integer polynomial coefficients, monic denominators, strictly positive integer multiplicities, nonnegative rational numerator exponents, the strict degree inequality, all active numerator/denominator gcds, exact composition, certified composed-root isolation and interval integration. The Doche reduction and numerical arithmetic backend are not formally verified here. PROOF.md and NUMERICS.md are our inherited mathematical argument and enclosure formulas.

Final certificate: 5 denominators and 37 numerators; D=999999999960, deg A=235397918730308607/262144; 185 gcd pairs and 4132 composed roots. Certificate SHA256: c86be5e438d56764e3e0d7578eb8478600b0f6a7d5d66e4f1b26aae5b8bebaff. CERTIFICATE_ENCODING.md records equal fractions with doubled numerators/denominators for the requested 15–16 digit encodings; exact Fraction checks are unchanged.

Before optimization, the specified public v5 JSON was fetched at 191064e7ccd88718853fe239dfd3890a8dc0fa37 and its SHA256 matched 8a5f363c29f02fca71e99dcedfdae0bd8969cd02bbed560484d1da726175a909. Replaying it with our round-7 verifier gives B in [0.2519889613870203560855, 0.2519889613870203621210], below its printed bound. See evidence/pr280-v5-replay.json. It used 37,961,728 bytes peak RSS and 43.85 wall seconds.

BAR.json was written before step 1. The initial full coefficient union contains 109 denominators and 928 numerators, including round-7 final factors, v5, round-6/7 banks and saved candidate arrays, and the supplied v3/v4 JSON data. Its N=524288 joint LP gave numerical 0.2519889613263126; its separately verified exact frozen weights gave about 0.25198896138702378, essentially v5. The union alone did not meet the bar.

Our own c82r7/c82r6/c82r5 numerics, joint LP, CVP, factor merger, archive numerator pricing, verifier, rejection controls and proof/numerical notes were copied and reused. The first new archive reader failed on integer metadata counts; it was reverted before each of two fixes, then succeeded after requiring list-valued coefficient and candidate groups. The inherited dense LP then hit the 3 GB guard during matrix filling at 2,827,091,968 bytes worker RSS; it was reverted before changing storage. The full grid, complete factor master, HiGHS simplex and row generation remain unchanged. Row coefficients are now evaluated on demand and full-grid sums streamed by column; reduced costs use the full nonzero dual support. This solved in 20.02 seconds with 662,290,432 bytes peak worker RSS. STATUS.md records the failures and changes.

The new numerator implementation is ordinary iterated dual-weighted evaluation-lattice LLL: stratified samples from the new LP dual, IRLS evaluation weights proportional to 1/|P|, a coefficient ridge, exact integer Gram LLL with delta .99, short rows and pairwise combinations, exact irreducible factor extraction, and full-dual reduced-cost pricing including the degree dual. It uses 256 samples, 320-bit evaluation arithmetic, degree at most 80 and up to eight IRLS steps. Direct successful-factor and product starts are varied by saved seeds. This differs from round 7's fixed-archive pricing. All candidates remain heuristic until frozen and verified. After the first unrestricted 269-column merge approached the memory limit, later initial merges use the existing archive pricer's 32-best-column convention, retaining every deferred factor for repeated complete-bank pricing. Newly generated numerator factors remain in the pricing bank even when inactive in restricted masters.

Denominator generation uses our inherited degree-104 monic CVP search: H=X(X-1)P4 residue restriction, 1024 stratified complementary-dual samples, 380-bit evaluation arithmetic, exact Gram LLL, 16 Schnorr–Euchner points, four million nodes and up to eight IRLS steps. Direct degree-104 warm starts and degree-44/60 archive products are retained. After round 4 found a new denominator at the end of the archive, active factors were prioritized and rotated by the saved RNG seed (the existing round-7 warm-rotation idea), so short subsequent batches directly use accepted new factors. Each round first searches new numerators, re-solves and verifies, then searches denominators on the moved dual, re-solves and verifies; all archive numerators are re-priced after a changed solve. The first round measures one 240-second worker of each type; later rounds use two, alternating types. No pricing/CVP optimality claim is made.

Stopping reason: wall time budget (last round completed; no further round started after 9.5 hours). Completed 21 alternating rounds. Their LP gains, states and dual paths are in rounds/finished.json; SEARCH_SUMMARY.json records searches. Another warm round is worth trying: recent complete rounds still improved the LP; this job stopped for its time budget. Resume from the saved final state and dual. This is not an optimality result.

Factor provenance follows by full coefficient comparison. Names are labels only; FACTOR_PROVENANCE.json includes every coefficient array, exact weight and all matching source labels.

| Denominator | Source matches | Degree | Multiplicity |
| --- | --- | ---: | ---: |
| Pin330c_C82r6_083ca9b3950a | ours from round 7; ours from round 6; #280 v5; initial coefficient union (including v5) | 104 | 1711171698 |
| C82r8_8d2a852b3a74 | new here | 104 | 863039728 |
| C82r8_b4ce16615ae6 | new here | 104 | 2826029194 |
| C82r8_fcd3a4b2d94d | new here | 104 | 2428497927 |
| C82r8_1f8710f82b1d | new here | 104 | 1786646068 |

| Numerator | Source matches | Degree |
| --- | --- | ---: |
| P1 | ours from round 7; ours from round 6; ours from round 5 or earlier; #280 v5; #280 v4; #280 v3; earlier bank; initial coefficient union (including v5) | 1 |
| P2 | ours from round 7; ours from round 6; ours from round 5 or earlier; #280 v5; #280 v4; #280 v3; earlier bank; initial coefficient union (including v5) | 1 |
| P3 | ours from round 7; ours from round 6; ours from round 5 or earlier; #280 v5; #280 v4; #280 v3; earlier bank; initial coefficient union (including v5) | 3 |
| P4 | ours from round 7; ours from round 6; ours from round 5 or earlier; #280 v5; #280 v4; #280 v3; earlier bank; initial coefficient union (including v5) | 4 |
| P6 | ours from round 7; ours from round 6; ours from round 5 or earlier; #280 v5; #280 v4; #280 v3; earlier bank; initial coefficient union (including v5) | 8 |
| n51_13_0 | #280 v5; initial coefficient union (including v5) | 29 |
| n51_13_1 | #280 v5; initial coefficient union (including v5) | 21 |
| N82r8_8e3176749e98 | new here | 22 |
| N82r8_4d6f8374e36e | new here | 34 |
| N82r8_37e4ca116338 | new here | 32 |
| n11_6_21 | ours from round 7; ours from round 6; #280 v5; #280 v4; #280 v3; initial coefficient union (including v5) | 32 |
| n11_4_53 | ours from round 7; ours from round 6; #280 v5; #280 v3; initial coefficient union (including v5) | 27 |
| N82r8_94765bb798aa | new here | 42 |
| N82r8_3cc45c82e976 | new here | 32 |
| N82r8_7e987bb7eb61 | new here | 66 |
| N82r8_0f16aab36a5c | new here | 30 |
| N82r8_fb5d479c5cc5 | new here | 62 |
| N82r8_668b7d383857 | new here | 62 |
| N82r8_9dfa148ebc59 | new here | 58 |
| N82r8_fba31c2bf8ec | new here | 66 |
| N82r8_85867779a275 | new here | 22 |
| N82r8_da2d43e99dcf | new here | 49 |
| N82r8_7ad0717acabe | new here | 62 |
| N82r8_399c97c85245 | new here | 60 |
| cg2_4_0_c2 | ours from round 7; ours from round 5 or earlier; #280 v3; earlier bank; initial coefficient union (including v5) | 30 |
| N82r8_5401c5faee2a | new here | 41 |
| N82r8_eed007427f22 | new here | 67 |
| N82r8_db72c355cf9d | new here | 69 |
| N82r8_7acaebc812f8 | new here | 66 |
| N82r8_15a2c891a952 | new here | 66 |
| N82r8_97b8b9cc3ffc | new here | 66 |
| N82r8_afc966e68dcc | new here | 67 |
| N82r8_7e03982f5b83 | new here | 33 |
| n51_9_0 | #280 v5; initial coefficient union (including v5) | 26 |
| N82r8_507d02a40ecd | new here | 63 |
| N82r8_c87f2773ef9f | new here | 68 |
| N82r8_3e96efae6b5c | new here | 59 |

Changed bytes, repinned zero multiplicity and repinned shared numerator/denominator factor all fail the verifier. See evidence/rejection-controls.json and its individual logs. The exact final endpoint comparison is in RESULT.json and evidence/final-replay.json.

No Python from vidigoat/optimization-records was downloaded, copied, imported or executed. PYTHON_BLOBS.json lists git hash-object for every local .py, including generated verifier and failed-reader copies, compared against every blob in the complete GitHub trees at 197962c, 3a7a84f, 79ce0df and 191064e; no matches and no imports of their modules. Only the specified certificate JSON and tree metadata were fetched from that repository. Method and factor credits: Doche; Grinsztajn and Epi; Pinho PR301/#330; Patankar PR280 v3/v4/v5 weighted CVP and iterated numerator LLL. THIRD_PARTY_NOTICE.md records reuse.

PRIOR_ART.md records the scoped initial and final source reads: live official table, open PRs #280/#330, open PR list, updated-first repository searches, lab/result repositories, primary references and focused arXiv/community searches. These establish the checked public comparators, without a worldwide priority judgment. All network activity was public reading. No commits, pushes, PRs, posts, uploads or messages were made. All research outputs stayed in this job directory; completed historical round JSON/log data were gzip-compressed and their originals, plus old regenerable LP dual caches, moved to macOS Trash under the reversible-deletion policy. Current master/dual and the standalone final certificate/replay remain uncompressed; REPRODUCE.md explains restoring an older compressed state.

Recorded compute: 13.0305 core-hours; estimated total including an explicit setup/controller/reporting allowance 13.1379 core-hours. Wall time since setup 9.741 hours. Maximum sampled aggregate worker/controller RSS 2,850,127,872 bytes, including the stopped dense attempt, below 3 GB. At most two numerical workers, single-threaded BLAS/HiGHS/FLINT, nice -n 10 (effective nice 20). COMPUTE.json contains accounting. evidence/process-cleanup.json records the final check that no workers remain.

Reproduce the final bound:

```sh
./run_local.sh verify_best.py --certificate certificate.json --target 0.2519758217 --precision 256 --tol 1e-13 --out evidence/reproduced-best.json
```

REPRODUCE.md gives v5 replay, union, search and rejection-control commands. Intermediate exact certificates and improved results were checkpointed throughout.
