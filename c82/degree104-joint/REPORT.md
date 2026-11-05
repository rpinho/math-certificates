Shipped: candidate, unrefereed C82 < 0.2519964889882011727026, with a separately written (same agent) interval-verified certificate; frozen B < 0.2520500000 target met.

Certified enclosure: B ∈ [0.2519964889882011564383, 0.2519964889882011727026]. The certified gain over 0.2520591386 is at least 0.0000626496117988272974. Exact dyadic upper endpoint < 5041/20000: True. RESULT.json saves the exact Fraction comparison; evidence/best-replay.json saves H, J, B, outward endpoints and integration details.

The final public-source refresh found [the previous version of our PR (#330)](https://github.com/teorth/optimizationproblems/pull/330) now prints 0.2520179248. The final bound is below that live printed comparator by at least 0.0000214358117988272974. A concise candidate claim is C82 < 0.2519964890; RESULT.json checks its exact rational margin. The final replay against 0.2520500000 passed in evidence/final-bar-replay.json.

This is a candidate arithmetic construction under the inherited Doche reduction, unrefereed. The verifier was separately written (same agent). It imports stdlib and python-flint only, composes polynomials exactly, isolates all composed roots, checks positive integer denominator multiplicities, nonnegative rational numerator powers, strict degree inequality, every active numerator/denominator gcd, and bounds the integral with interval arithmetic. It shares no helper with the search. The reduction and arithmetic backend were not formalized in this job.

Before searching, our verifier replayed V. Patankar (@vidigoat) #280 v3: B ∈ [0.2520591385259547806692, 0.2520591385259548085535], H = 0.2520394006582629915263. This public-data reproduction is credited to Patankar; evidence/public-v3-replay.json records it. The requested JSON hash matched 00125f6984ad2646a79d8782ee38f5161bd24c17d4899e4af74ff3e529ba1dbe. Only the expected hash pin was changed in our copied round-5 verifier.

BAR.json was frozen before the union solve. The standard full union master used 7 degree-104 denominators and all 895 distinct certificate/public-bank numerators on N=524288 points. Grid B = 0.25205913844096395; its frozen certified upper endpoint was 0.2520591385259580091897, slightly worse than the original public replay due to weight freezing. The incumbent was restored to the public certificate before column generation. No meaningful gain came from union reweighting alone.

Column generation reused our own ../c82r5 numerics.py, joint_lp.py, cvp_search.py, add_columns.py and numerator_search.py. Changes were the r6 label/provenance and complete union bank path. Our own verifier, rejection controls and numerical documentation were also reused. New orchestration saved exact-weight certificates after each improved solve. Standard restricted masters removed zero numerator columns but all 895 public numerators remained available to complete-dual pricing. All union denominators remained warm starts.

The inherited CVP settings were degree 104, H=X(X−1)P4 residue restriction, 1024 stratified weighted-evaluation samples, 380-bit evaluation arithmetic, exact integer Gram LLL (delta .99), 16 retained Schnorr–Euchner points, four million nodes and up to eight IRLS steps. Two single-threaded 240-second batches ran against each dual. Floating grid objectives and negative prices are heuristic; the interval-replayed frozen certificate alone supports the headline bound. No closest-vector optimality claim is made. After the original-order search stopped with three no-gain rounds (4–6), the continuation prioritized and rotated positive-weight warm starts between workers, keeping all union denominators available and retaining the same algorithms and numerical defaults. Original loop summaries are in rounds/original-finished.json and rounds/original-progress.json.

SEARCH_SUMMARY.json and the per-round states retain the search settings, prices, actual LP gains and CPU use.

Full coefficient comparison determines every factor attribution; names are labels only.

All requested rejection controls passed by rejecting changed bytes, zero multiplicity with a repinned hash, and a shared numerator/denominator factor with a repinned hash. See evidence/rejection-controls.json and individual logs. The final bound also has an exact upper-endpoint comparison with the stated rational in RESULT.json.

Final certificate: 8 monic degree-104 denominator factors, 15 numerator factors, D=1000000000064, deg A=58700834920208207/65536. FACTOR_PROVENANCE.json records every coefficient array, exact weight, and all full-coefficient matches against #280 v3, our round 5, and the earlier public bank.

| Denominator | Coefficient provenance | Integer multiplicity |
| --- | --- | ---: |
| D11_5_0 | #280 v3 (V. Patankar) | 1217811133 |
| C82r6_7075b26a1a91 | new here | 749492747 |
| C82r6_99cd845e34d4 | new here | 240853345 |
| C82r6_8c76cd0c4e53 | new here | 2006904845 |
| C82r6_f770a2649784 | new here | 455435212 |
| C82r6_935548ec48fe | new here | 1513821032 |
| C82r6_d24f4c93ef26 | new here | 784010602 |
| C82r6_083ca9b3950a | new here | 2647055700 |

Numerator provenance, by full coefficient comparison:

- P1: #280 v3 (V. Patankar); #280's earlier public numerator bank; ours from round 5 or earlier; q=5497760358343139/32768.
- P2: #280 v3 (V. Patankar); #280's earlier public numerator bank; ours from round 5 or earlier; q=5575689194593389/32768.
- P3: #280 v3 (V. Patankar); #280's earlier public numerator bank; ours from round 5 or earlier; q=10908223350879106/1048576.
- P4: #280 v3 (V. Patankar); #280's earlier public numerator bank; ours from round 5 or earlier; q=6011285934956725/262144.
- P6: #280 v3 (V. Patankar); #280's earlier public numerator bank; ours from round 5 or earlier; q=5728433163623077/262144.
- MS360: #280 v3 (V. Patankar); #280's earlier public numerator bank; ours from round 5 or earlier; q=595314937835435/262144.
- n22_7_5: #280 v3 (V. Patankar); #280's earlier public numerator bank; q=914727581779015/1048576.
- n11_4_53: #280 v3 (V. Patankar); q=755101634873771/524288.
- n11_6_21: #280 v3 (V. Patankar); q=132195930773941/65536.
- n101_0_17: #280 v3 (V. Patankar); #280's earlier public numerator bank; q=58121956035395/32768.
- n121_3_30: #280's earlier public numerator bank; q=928976310347585/524288.
- n11_6_49: #280 v3 (V. Patankar); q=1278491793356325/1048576.
- n101_6_2: #280 v3 (V. Patankar); #280's earlier public numerator bank; q=573349973948119/1048576.
- n101_7_34: #280's earlier public numerator bank; ours from round 5 or earlier; q=65366428065105/524288.
- n101_2_37: #280's earlier public numerator bank; q=49069199874759/1048576.

Method/factor credit: Doche (perturbed-polynomial construction); Grinsztajn and Épi (earlier factors); R. Pinho PR #301 (joint LP, residue restriction and prices), our own round-5 factors; V. Patankar PR #280 (public JSON factors and weighted-CVP/product-start method). No Python from vidigoat/optimization-records was downloaded, copied, imported or executed. All third-party retrievals from that repository were JSON data or GitHub tree metadata. No novelty judgment is made, as requested.

PRIOR_ART.md records the scoped source survey: official raw 82a table, relevant open PR bodies (#242, #280, #301, #330), updated-first repository searches, BakeLab/Épi, both DeepMind repositories, OpenAI math, kisonecat, plasma-ai/erdos, EinsteinArena, primary Doche paper, arXiv:2601.18978v2 and 2609.39505, and focused recent-paper/community queries. The final refreshed official table and open-PR reads remain in prior_sources/*-final.*. This is a scoped public comparison, not a worldwide priority judgment.

Compute: measured orchestration child CPU 3.2045 core-hours; estimated total 3.2856 core-hours using single-threaded bootstrap elapsed time, plus at most about 0.01 core-hours of short setup/control/accounting work. Wall time 2.076 hours. At most three numerical workers, BLAS/FLINT/HiGHS single-threaded, nice -n 10 (effective nice 20 inherited). Mini load was checked. COMPUTE.json and evidence/pids.jsonl retain the accounting. Final process inspection is in evidence/process-cleanup.json. Artifacts stay below 50 MB. All writes stayed in this job directory; no commits, pushes, PRs, posts, uploads or messages were made.

Reproduce final certification:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1
nice -n 10 python3 verify_best.py --certificate certificate.json --target 0.2520500000 --precision 256 --tol 1e-13 --out evidence/reproduced-best.json
```

REPRODUCE.md gives public replay, full-union solve, CVP loop and rejection-control commands. NUMERICS.md gives the inherited verifier enclosure formulas.

Every local .py git blob was computed with git hash-object and compared with every blob in the complete GitHub trees at vidigoat/optimization-records@197962c9610f583e9bc56efe37bfb994c1eeb834 and @3a7a84fec9c64ae426f06a5f52597c84b3453ba0. None matches any blob in either tree. AST import inspection confirms none imports their modules. PYTHON_BLOBS.json contains all filenames, hashes, and imports.

The complete per-file git-blob inventory is in PYTHON_BLOBS.json.

Stopping reason: three no-gain rounds. The final dual/state and per-round gains are in rounds/finished.json.

Another identical round: no, not recommended now. The final three rotated warm-start rounds found no useful columns. This is a scoped search plateau, not an optimality result. A later round with broader denominator starts or a changed proposal distribution may be useful; that follow-up was not tested here.
