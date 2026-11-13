Shipped: candidate, unrefereed C82 < 0.2519744488; the exact certified upper endpoint is below the frozen 0.2519758216 bar.

Certified enclosure: [0.2519744487408958476234, 0.2519744487408958502183]. Exact endpoint fraction: 58353295708258735494685767687692308273187894063503527442935389087900933107455/231584178474632390847141970017375815706539969331281128078915168015826259279872. The endpoint is strictly below the stated rational 314968061/1250000000; the comparison uses Fraction, without decimal rounding.

| Comparator | Certified improvement (at least) |
| --- | ---: |
| Round 8 printed 0.2519758217 | 0.0000013729591041497817 |
| [#330](https://github.com/teorth/optimizationproblems/pull/330) live printed 0.2519923410 | 0.0000178922591041497817 |
| [#280 v5](https://github.com/teorth/optimizationproblems/pull/280) printed 0.2519889614 | 0.0000145126591041497817 |
| Round 8 upper endpoint 0.2519758216376568674750 | 0.0000013728967610172567 |

The packet has 5 denominators and 48 numerators. D=1000000000064; deg A=233913093063931949/262144; 240 exact gcd pairs and 5370 composed roots. SHA256: 1e5af10142c7223df4cd56a4279727a7610137dab8e5f2d95dcb19b3030ac67e.

Verification uses the separately written (same agent) inherited stdlib + python-flint verifier. It checks the hash, integer coefficients, monic denominators, positive integer multiplicities, nonnegative rational powers, strict degree inequality, every active numerator/denominator gcd, exact composition, composed-root isolation and interval integration. Changed bytes, repinned zero multiplicity and repinned shared factor all fail (evidence/rejection-controls.json). The Doche reduction and arithmetic backend are not formally verified. PROOF.md and NUMERICS.md give the inherited mathematical argument and enclosure formulas. All conclusions remain candidate and unrefereed.

Our own round-8 joint LP, numerical helpers, iterated dual-weighted evaluation-lattice LLL numerator pricing, degree-104 monic CVP denominator generation, mergers, controller, checkpoint code, verifier and rejection controls were copied and reused. The search began from its final floating master and dual, without a cold restart: 115 denominators and 37 active numerators, plus its complete bank of 14,192 numerator factors and 109 archive denominators. Its certificate replay reproduced B in [0.2519758216376568634394, 0.2519758216376568674750]. BAR.json was written before search.

The standard alternation was retained: numerator search on the current dual, joint LP and certification, full-bank numerator repricing after each moved solve, then CVP denominator search on the new dual, joint LP and certification. Numerator generation and full-bank pricing receive four workers and CVP two, with sequential solving/verification, following round 8’s frequent numerator gains and occasional larger denominator gains. Initial generation batches ran solo under /usr/bin/time -l before scaling. Full-bank pricing began with the inherited serial implementation; from round 23 its independent per-factor calculations use four workers, with unchanged formulas, complete-bank coverage and ordering. The first full parallel pass completed in 104.9 wall seconds with 559 MB sampled aggregate RSS. Each worker uses one BLAS/HiGHS/FLINT thread and nice -n 10. Search settings, seeds and outcomes are in SEARCH_SUMMARY.json. No pricing or CVP optimality claim is made.

Stopping reason: wall time budget: no new round started after 9.5 hours; the last complete round finished before 10 hours. Completed 30 alternating rounds (numbered from 22). Three no-gain rounds means three complete rounds without a smaller certified endpoint; the old 1e-10 LP cutoff was larger than this job’s frozen-bar margin. The search time limit leaves time for the final packet within ten hours. No stop is interpreted as an optimality result.

Another warm round is worth trying: the latest completed rounds still improved the certified value and the time budget ended the run.
Resume from rounds/restricted-archive-num-51-1.json and rounds/archive-num-51-1-dual.npz with the complete bank.

The plot shows all certified checkpoints without fitting or extrapolation. The table lists the baseline, the first improvement in each elapsed hour and the final value; IMPROVEMENT_CURVE.csv records every certified improvement and certificate path.

![Certified improvement curve](IMPROVEMENT_CURVE.png)

The plot is also available as IMPROVEMENT_CURVE.pdf.

| Elapsed hours | Certified upper endpoint |
| ---: | ---: |
| 0.059 | 0.2519758216376568674750 |
| 1.141 | 0.2519756801294185915884 |
| 2.185 | 0.2519756069540503236489 |
| 3.057 | 0.2519755445399234998198 |
| 4.018 | 0.2519754806606503392866 |
| 5.225 | 0.2519752868352606523623 |
| 6.124 | 0.2519747169284980306825 |
| 7.170 | 0.2519745289258011211607 |
| 8.125 | 0.2519744829177648826996 |
| 9.168 | 0.2519744557953114964140 |
| 9.554 | 0.2519744487408958502183 |

Compute: 25.3227 recorded core-hours; 25.4298 estimated total with explicit controller/setup allowance. Wall time 9.707 hours. Largest sampled aggregate RSS 1,015,513,088 bytes; 3 GB cap. COMPUTE.json records accounting and measured process peaks. evidence/process-cleanup.json records the final ps check.

Factor provenance is by full coefficient comparison, including exact weights and all matches in FACTOR_PROVENANCE.json. A factor absent from the compared sources is labeled “generated in this continuation”; this is provenance only. Names are labels.

| Denominator | Degree | Multiplicity | Full coefficient matches |
| --- | ---: | ---: | --- |
| Pin330c_C82r6_083ca9b3950a | 104 | 739243927 | ours from round 7; ours from round 6; #280 v5; initial coefficient union (including v5); ours from round 8; full round-8 union bank; round-8 final LP master |
| C82r8_b4ce16615ae6 | 104 | 2606138513 | ours from round 8; round-8 final LP master |
| C82r8_fcd3a4b2d94d | 104 | 2831784578 | ours from round 8; round-8 final LP master |
| C82r8_1f8710f82b1d | 104 | 1846791246 | ours from round 8; round-8 final LP master |
| C82r9_923bd2177a3d | 104 | 1591426352 | generated in this continuation |

| Numerator | Degree | Full coefficient matches |
| --- | ---: | --- |
| P1 | 1 | ours from round 7; ours from round 6; ours from round 5 or earlier; #280 v5; #280 v4; #280 v3; earlier bank; initial coefficient union (including v5); ours from round 8; full round-8 union bank; round-8 final LP master |
| P2 | 1 | ours from round 7; ours from round 6; ours from round 5 or earlier; #280 v5; #280 v4; #280 v3; earlier bank; initial coefficient union (including v5); ours from round 8; full round-8 union bank; round-8 final LP master |
| P3 | 3 | ours from round 7; ours from round 6; ours from round 5 or earlier; #280 v5; #280 v4; #280 v3; earlier bank; initial coefficient union (including v5); ours from round 8; full round-8 union bank; round-8 final LP master |
| P4 | 4 | ours from round 7; ours from round 6; ours from round 5 or earlier; #280 v5; #280 v4; #280 v3; earlier bank; initial coefficient union (including v5); ours from round 8; full round-8 union bank; round-8 final LP master |
| P6 | 8 | ours from round 7; ours from round 6; ours from round 5 or earlier; #280 v5; #280 v4; #280 v3; earlier bank; initial coefficient union (including v5); ours from round 8; full round-8 union bank; round-8 final LP master |
| N82r8_85867779a275 | 22 | ours from round 8; full round-8 union bank; round-8 final LP master |
| N82r9_2c00bf0e341e | 36 | generated in this continuation |
| N82r9_a49c3746e570 | 28 | generated in this continuation |
| N82r9_e0da03871ae5 | 39 | generated in this continuation |
| N82r9_8baddd1649e6 | 38 | generated in this continuation |
| N82r9_1aa3601f1b5c | 36 | generated in this continuation |
| n51_13_1 | 21 | #280 v5; initial coefficient union (including v5); ours from round 8; full round-8 union bank; round-8 final LP master |
| N82r9_fe071196d7dd | 32 | generated in this continuation |
| cg2_4_0_c2 | 30 | ours from round 7; ours from round 5 or earlier; #280 v3; earlier bank; initial coefficient union (including v5); ours from round 8; full round-8 union bank; round-8 final LP master |
| N82r9_6698cb93cd1c | 67 | generated in this continuation |
| N82r9_0737d1d42b6d | 62 | generated in this continuation |
| N82r8_3cc45c82e976 | 32 | ours from round 8; full round-8 union bank; round-8 final LP master |
| N82r9_85ec5b3f21c1 | 64 | generated in this continuation |
| N82r9_ba647f7a4380 | 62 | generated in this continuation |
| N82r9_a3dfda9dd5f0 | 55 | generated in this continuation |
| N82r9_85763e6df88f | 64 | generated in this continuation |
| N82r9_23ee45262ec6 | 64 | generated in this continuation |
| N82r8_37e4ca116338 | 32 | ours from round 8; full round-8 union bank; round-8 final LP master |
| N82r9_c597af50c459 | 65 | generated in this continuation |
| N82r9_ada2a3a91f42 | 50 | generated in this continuation |
| N82r9_258c33a01a61 | 63 | generated in this continuation |
| N82r9_85d0b14b7d1d | 62 | generated in this continuation |
| N82r9_3eb80a5662af | 64 | generated in this continuation |
| N82r9_e2abadd25522 | 64 | generated in this continuation |
| N82r9_640e5f44db82 | 65 | generated in this continuation |
| N82r9_146f079dbce9 | 67 | generated in this continuation |
| N82r9_7f35ecdc039c | 64 | generated in this continuation |
| N82r9_514c188deccd | 68 | generated in this continuation |
| N82r9_fefd10f7c8e3 | 67 | generated in this continuation |
| N82r9_91a55a3e7602 | 64 | generated in this continuation |
| N82r9_4336f6c43520 | 33 | generated in this continuation |
| N82r9_1bb3ceb743ce | 62 | generated in this continuation |
| N82r9_6eca741db878 | 61 | generated in this continuation |
| N82r9_29576912e082 | 34 | generated in this continuation |
| N82r9_5ea607b75cb3 | 58 | generated in this continuation |
| N82r9_37e84d89d686 | 34 | generated in this continuation |
| N82r9_f238e50b138e | 29 | generated in this continuation |
| N82r8_e01dea931ba8 | 30 | full round-8 union bank |
| N82r9_5ede55618598 | 39 | generated in this continuation |
| n11_6_21 | 32 | ours from round 7; ours from round 6; #280 v5; #280 v4; #280 v3; initial coefficient union (including v5); ours from round 8; full round-8 union bank; round-8 final LP master |
| N82r9_2a6a4ee12708 | 63 | generated in this continuation |
| N82r9_63b99020f1c6 | 63 | generated in this continuation |
| N82r9_0b5e81317eb6 | 63 | generated in this continuation |

For every q_rational with a reduced 15- or 16-digit numerator, the equal fraction with numerator and denominator doubled is retained. CERTIFICATE_ENCODING.md and the inherited encoding note identify these entries; exact Fraction arithmetic is unchanged.

No vidigoat Python was downloaded, copied, imported or executed. PYTHON_BLOBS.json records the git blob hash of every .py in this job directory and checks against every blob in complete metadata-only trees at 197962c, 3a7a84f, 79ce0df and 191064e. No matches or imports of their modules were found. Only their already supplied certificate JSON data and tree metadata were used. Credits: Doche, Grinsztajn and Epi, Pinho PR301/#330, Patankar PR280 v3/v4/v5. THIRD_PARTY_NOTICE.md records the inherited factor/method credits.

PRIOR_ART.md records the current public table/open PRs, recent repository searches, lab/result READMEs, papers and community searches, with initial and final read snapshots. Public comparison sources: [#330](https://github.com/teorth/optimizationproblems/pull/330), [#280](https://github.com/teorth/optimizationproblems/pull/280), [official table](https://teorth.github.io/optimizationproblems/constants/82a.html). No novelty judgment is made. All network use was read-only; no commits, pushes, PRs, uploads, posts or messages were made. All retained outputs are in this job directory. Completed history was gzip-compressed; redundant old floating LP/dual caches and compressed originals were moved to macOS Trash to keep the packet below 50 MB. Every certified best and its exact replay remain retained.

Reproduce the bound:

```sh
./run_local.sh verify_best.py --certificate certificate.json --target 0.2519744488 --precision 256 --tol 1e-13 --out evidence/reproduced-best.json
```

REPRODUCE.md gives warm search, rejection-control and source-inventory commands. Every new certified best is retained in certificates/.
