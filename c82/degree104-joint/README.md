# C82 degree-104 joint certificate

This packet gives **C82 < 0.2519744488*** (rigorous interval bound, verify_best.py), a candidate, unrefereed upper bound for the essential minimum of the logarithmic Zhang-Zagier height in Tao's 82a definition. The asterisk stays. Verification level L0 applies to the bound as a whole. The producer verifier was written separately from the search code by the same AI agent lineage. The separate AI referee and its provenance limits are described below.

Under the same definition, the exact certified upper endpoint is below V. Patankar's public [#280 v5](https://github.com/vidigoat/optimization-records/blob/191064e7ccd88718853fe239dfd3890a8dc0fa37/tao/certificates/c82/v5/README.md) printed bound 0.2519889614* by at least 0.0000145126591041497817, and below [our published round-7 #330 certificate](https://github.com/rpinho/math-certificates/blob/a12c3622120c39af776902dbe49b6eff97a4d189/c82/degree104-joint/README.md), 0.2519923410*, by at least 0.0000178922591041497817. The gaps below [#280 v4](https://github.com/vidigoat/optimization-records/blob/79ce0dfb211a67ff7e387b58b0d19ff1d6accfba/tao/certificates/c82/v4/README.md)'s 0.2520079724* and [#280 v3](https://github.com/vidigoat/optimization-records/blob/197962c9610f583e9bc56efe37bfb994c1eeb834/tao/certificates/c82/v3/README.md)'s 0.2520591386* are at least 0.0000335236591041497817 and 0.0000846898591041497817, respectively. The exact comparison gaps are computed by certificate_facts.py in receipts/certificate-facts.json: each is the exact printed comparator minus the exact certified upper endpoint, rounded downward. These are deterministic mathematical comparisons, with no predictive score.

Earlier versions of our PR printed [0.2519964890*](https://github.com/rpinho/math-certificates/blob/3be6b2f133db43374ea30767b58c62ce2d39686a/c82/degree104-joint/README.md), [0.2520179248*](https://github.com/rpinho/math-certificates/blob/98208a40e043e578d35183b418452f316112a658/c82/degree104-joint/README.md) and [0.252404806*](https://github.com/rpinho/math-certificates/blob/5461d490552a518667c3fd3fceff33ebdb4d347c/c82/degree104-cvp/README.md). The cited [live-page value pinned to the supplied commit](https://github.com/teorth/optimizationproblems/blob/87b4ebbd426ff8db597a2004cc45da17903bdcf2/constants/82a.md) is 0.2534449*. Producer source captures are in prior_sources/; earlier publication captures and pinned tree evidence are in sources/. This packaging job finds no new construction or method: it ships the producer's completed result and makes no priority or optimality claim.

Credit: C. Doche supplies the perturbed-polynomial construction (J. Théor. Nombres Bordeaux 13 (2001), 103–110). V. Patankar (@vidigoat, #280) supplies the weighted-evaluation LLL / closest-vector method, public v3/v4/v5 certificates and coefficient bank. Ricardo Pinho (#301/#330) supplies the joint LP, reduced-cost pricing and residue-class restriction. Grinsztajn and Épi supply earlier factor libraries. Credit snapshots include sources/pr280.json, sources/pr301.json and prior_sources/pr280-final.json.

## Exact factor credit

FACTOR_PROVENANCE.json records full coefficient arrays and every source match. Local matches say where a factor was reused; they are not exclusive authorship claims. “New here” means generated in the round-9 continuation and absent from the comparison inputs, without a novelty claim. Every #280 match below credits V. Patankar (@vidigoat), including matching factors he previously reused from our certificate. Doche's P1, P2, P3, P4 and P6 retain Doche's mathematical credit.

| Denominator | Origin and full coefficient matches |
|---|---|
| Pin330c_C82r6_083ca9b3950a | ours from round 7 as C82r6_083ca9b3950a; ours from round 6 as C82r6_083ca9b3950a; #280 v5 as Pin330c_C82r6_083ca9b3950a; initial coefficient union (including v5) as Pin330c_C82r6_083ca9b3950a; ours from round 8 as Pin330c_C82r6_083ca9b3950a; full round-8 union bank as Pin330c_C82r6_083ca9b3950a; round-8 final LP master as Pin330c_C82r6_083ca9b3950a |
| C82r8_b4ce16615ae6 | ours from round 8 as C82r8_b4ce16615ae6; round-8 final LP master as C82r8_b4ce16615ae6 |
| C82r8_fcd3a4b2d94d | ours from round 8 as C82r8_fcd3a4b2d94d; round-8 final LP master as C82r8_fcd3a4b2d94d |
| C82r8_1f8710f82b1d | ours from round 8 as C82r8_1f8710f82b1d; round-8 final LP master as C82r8_1f8710f82b1d |
| C82r9_923bd2177a3d | new here (round 9) |

| Numerator | Origin and full coefficient matches |
|---|---|
| P1 | ours from round 7 as P1; ours from round 6 as P1; ours from round 5 or earlier as P1; #280 v5 as P1; #280 v4 as P1; #280 v3 as P1; earlier bank as P1; initial coefficient union (including v5) as P1; ours from round 8 as P1; full round-8 union bank as P1; round-8 final LP master as P1 |
| P2 | ours from round 7 as P2; ours from round 6 as P2; ours from round 5 or earlier as P2; #280 v5 as P2; #280 v4 as P2; #280 v3 as P2; earlier bank as P2; initial coefficient union (including v5) as P2; ours from round 8 as P2; full round-8 union bank as P2; round-8 final LP master as P2 |
| P3 | ours from round 7 as P3; ours from round 6 as P3; ours from round 5 or earlier as P3; #280 v5 as P3; #280 v4 as P3; #280 v3 as P3; earlier bank as P3; initial coefficient union (including v5) as P3; ours from round 8 as P3; full round-8 union bank as P3; round-8 final LP master as P3 |
| P4 | ours from round 7 as P4; ours from round 6 as P4; ours from round 5 or earlier as P4; #280 v5 as P4; #280 v4 as P4; #280 v3 as P4; earlier bank as P4; initial coefficient union (including v5) as P4; ours from round 8 as P4; full round-8 union bank as P4; round-8 final LP master as P4 |
| P6 | ours from round 7 as P6; ours from round 6 as P6; ours from round 5 or earlier as P6; #280 v5 as P6; #280 v4 as P6; #280 v3 as P6; earlier bank as P6; initial coefficient union (including v5) as P6; ours from round 8 as P6; full round-8 union bank as P6; round-8 final LP master as P6 |
| N82r8_85867779a275 | ours from round 8 as N82r8_85867779a275; full round-8 union bank as N82r8_85867779a275; round-8 final LP master as N82r8_85867779a275 |
| N82r9_2c00bf0e341e | new here (round 9) |
| N82r9_a49c3746e570 | new here (round 9) |
| N82r9_e0da03871ae5 | new here (round 9) |
| N82r9_8baddd1649e6 | new here (round 9) |
| N82r9_1aa3601f1b5c | new here (round 9) |
| n51_13_1 | #280 v5 as n51_13_1; initial coefficient union (including v5) as n51_13_1; ours from round 8 as n51_13_1; full round-8 union bank as n51_13_1; round-8 final LP master as n51_13_1 |
| N82r9_fe071196d7dd | new here (round 9) |
| cg2_4_0_c2 | ours from round 7 as cg2_4_0_c2; ours from round 5 or earlier as cg2_4_0_c2; #280 v3 as cg2_4_0_c2; earlier bank as cg2_4_0_c2; initial coefficient union (including v5) as cg2_4_0_c2; ours from round 8 as cg2_4_0_c2; full round-8 union bank as cg2_4_0_c2; round-8 final LP master as cg2_4_0_c2 |
| N82r9_6698cb93cd1c | new here (round 9) |
| N82r9_0737d1d42b6d | new here (round 9) |
| N82r8_3cc45c82e976 | ours from round 8 as N82r8_3cc45c82e976; full round-8 union bank as N82r8_3cc45c82e976; round-8 final LP master as N82r8_3cc45c82e976 |
| N82r9_85ec5b3f21c1 | new here (round 9) |
| N82r9_ba647f7a4380 | new here (round 9) |
| N82r9_a3dfda9dd5f0 | new here (round 9) |
| N82r9_85763e6df88f | new here (round 9) |
| N82r9_23ee45262ec6 | new here (round 9) |
| N82r8_37e4ca116338 | ours from round 8 as N82r8_37e4ca116338; full round-8 union bank as N82r8_37e4ca116338; round-8 final LP master as N82r8_37e4ca116338 |
| N82r9_c597af50c459 | new here (round 9) |
| N82r9_ada2a3a91f42 | new here (round 9) |
| N82r9_258c33a01a61 | new here (round 9) |
| N82r9_85d0b14b7d1d | new here (round 9) |
| N82r9_3eb80a5662af | new here (round 9) |
| N82r9_e2abadd25522 | new here (round 9) |
| N82r9_640e5f44db82 | new here (round 9) |
| N82r9_146f079dbce9 | new here (round 9) |
| N82r9_7f35ecdc039c | new here (round 9) |
| N82r9_514c188deccd | new here (round 9) |
| N82r9_fefd10f7c8e3 | new here (round 9) |
| N82r9_91a55a3e7602 | new here (round 9) |
| N82r9_4336f6c43520 | new here (round 9) |
| N82r9_1bb3ceb743ce | new here (round 9) |
| N82r9_6eca741db878 | new here (round 9) |
| N82r9_29576912e082 | new here (round 9) |
| N82r9_5ea607b75cb3 | new here (round 9) |
| N82r9_37e84d89d686 | new here (round 9) |
| N82r9_f238e50b138e | new here (round 9) |
| N82r8_e01dea931ba8 | ours from round-8 bank; full round-8 union bank as N82r8_e01dea931ba8 |
| N82r9_5ede55618598 | new here (round 9) |
| n11_6_21 | ours from round 7 as n11_6_21; ours from round 6 as n11_6_21; #280 v5 as n11_6_21; #280 v4 as n11_6_21; #280 v3 as n11_6_21; initial coefficient union (including v5) as n11_6_21; ours from round 8 as n11_6_21; full round-8 union bank as n11_6_21; round-8 final LP master as n11_6_21 |
| N82r9_2a6a4ee12708 | new here (round 9) |
| N82r9_63b99020f1c6 | new here (round 9) |
| N82r9_0b5e81317eb6 | new here (round 9) |

Exact full-coefficient overlaps, recomputed by certificate_facts.py:

- V. Patankar's #280 v3: 0 denominator factors; 7 numerator factors (P1, P2, P3, P4, P6, cg2_4_0_c2, n11_6_21).
- V. Patankar's #280 v4: 0 denominator factors; 6 numerator factors (P1, P2, P3, P4, P6, n11_6_21).
- V. Patankar's #280 v5: 1 denominator factors (Pin330c_C82r6_083ca9b3950a); 7 numerator factors (P1, P2, P3, P4, P6, n51_13_1, n11_6_21).

V5 itself reused four denominators from our round-7 certificate in this PR: C82r6_8c76cd0c4e53, C82r6_935548ec48fe, C82r6_083ca9b3950a and C82r7_dd0a7c419abf, with the public prefix Pin330c_. The current packet retains only the third of these. The v5-only numerator used here is n51_13_1; n11_6_21 also appears in v3/v4/v5; cg2_4_0_c2 appears in v3 and the earlier bank. Every such public-data use is credited to V. Patankar; coefficient reuse does not transfer the original factor credit.

## Frozen certificate and verification

The certificate has five monic degree-104 denominators with positive integer multiplicities and 48 numerators with positive rational exponents. D = 1000000000064, a = 233913093063931949/262144 and slack D-a = 28230906952845267/262144. There are 21 non-monic numerators: N82r8_85867779a275 (leading coefficient 2), N82r9_2c00bf0e341e (leading coefficient 2), N82r9_8baddd1649e6 (leading coefficient 2), N82r9_1aa3601f1b5c (leading coefficient 2), N82r9_fe071196d7dd (leading coefficient 4), N82r9_0737d1d42b6d (leading coefficient 3), N82r9_85ec5b3f21c1 (leading coefficient 2), N82r9_23ee45262ec6 (leading coefficient 2), N82r8_37e4ca116338 (leading coefficient 6), N82r9_258c33a01a61 (leading coefficient 6), N82r9_85d0b14b7d1d (leading coefficient 2), N82r9_3eb80a5662af (leading coefficient 2), N82r9_e2abadd25522 (leading coefficient 4), N82r9_640e5f44db82 (leading coefficient 6), N82r9_514c188deccd (leading coefficient 5), N82r9_91a55a3e7602 (leading coefficient 5), N82r9_4336f6c43520 (leading coefficient 3), N82r9_1bb3ceb743ce (leading coefficient 12), N82r9_5ea607b75cb3 (leading coefficient 2), N82r9_2a6a4ee12708 (leading coefficient 2), N82r9_63b99020f1c6 (leading coefficient 13). Their leading-coefficient logarithms are included. verify_best.py checks all 240 active gcd pairs and all 5370 composed roots, and encloses B = H + J with FLINT/Arb at 256 bits:

    0.2519744487408958476234 <= B <= 0.2519744487408958502183

The exact upper endpoint is strictly below 0.2519744488. receipts/frozen-release-verifier.json preserves the producer's final replay; receipts/release-verifier.json records the packet rerun, with exact command and environment in receipts/release-verifier.log. receipts/certificate-facts.json records the recomputed rational facts, comparison gaps and v3/v4/v5 overlaps. The verifier imports only Python's standard library and python-flint.

Round 9 continued round 8 warm; its final certificate-producing solve is archive-num-51-1. rounds/ contains that solve's files, its final restricted master and dual, and finished.json. The duplicate round certificate is omitted in favor of certificate.json. The producer stopped on its wall-time budget while the latest completed rounds still improved; this is not an optimality result. Round 8's own certificate, 0.2519758217* (refereed HOLDS WITH CAVEATS), is superseded and its standalone certificate is not shipped. NOTE.md explains the retained archival paths.

REPORT.md, STATUS.md, PRIOR_ART.md, NUMERICS.md, RESULT.json, BAR.json, SEARCH_SUMMARY.json, COMPUTE.json, own scripts, evidence/ and prior_sources/ describe the completed producer. REPRODUCE.md adds packet commands before its producer section. Producer evidence and rejection controls are historical records; only final-bound producer and referee replays are run by this packaging job. Read PROOF.md for the theorem and extraction argument, and METHOD.md for the heuristic search. This packet reproduces the final bound, not the full search.

No Python from vidigoat/optimization-records is included, imported or executed. seal.py recomputes PYTHON_BLOBS.json against every blob in complete metadata-only trees at 197962c, 3a7a84f, 79ce0df and 191064e and checks imports of core or wlp. Any match is a blocker. Public coefficient arrays are data; see THIRD_PARTY_NOTICE.md and the MIT license. Retained third-party data files are copied byte-for-byte, never reserialized. Raw historical snapshots preserve original URLs and prose; authored citations are pinned to commits. Whole-file omissions are listed in NOTE.md.

## Certificate encoding

certificate.json (SHA256 1e5af10142c7223df4cd56a4279727a7610137dab8e5f2d95dcb19b3030ac67e), verify_best.py and FACTOR_PROVENANCE.json are unchanged round-9 bytes. The producer used equal-fraction representations for some rational weights to avoid spurious publishing-filter patterns. Those exact representations are preserved; CERTIFICATE_ENCODING.md lists the released representations only. No rational data or verifier hash pin has been changed. Historical verifier copies retain their original pins.

## Referee

The clean-room round-9 referee was supplied only the three files in review/inputs/, attacked the reduction and exact hypotheses, and wrote its own interval checker without reading or running producer code. Verdict: **HOLDS WITH CAVEATS**. Its outward enclosure is B in [0.25197444874089584903007645293157, 0.25197444874089584903007646836791], inside the producer interval. Its two caveats are plain: the session cannot authenticate its exact model ID or prove that it differs from the producer; and the referee job's resource estimate described 37 numerators and 4,132 roots, while the hashed input actually has 48 numerators and 5,370 roots. The latter is stale documentation, not a different certificate or failed mathematical hypothesis. See review/REFEREE.md, review/replay/report.md and REPLAY.json. The original receipt is review/replay/REPLAY.original.json; root REPLAY.json adapts paths and recomputes inputs_hash. AI review does not remove the asterisk.

Arhan Canli's independent replays, disclosing AI assistance (Claude, Anthropic), cover earlier versions of this PR only: 0.252404806* and 0.2520179248* ([pinned replay code](https://github.com/arhancanli/quantavane-replays/tree/7696576f41b418a5eacaed423b7b2078a521e26e/c82)); 0.2519964890* ([pinned replay code](https://github.com/arhancanli/quantavane-replays/tree/2b7475fb6e9186973de44c1f2b0db4cb1d0ae6bf/c82)); and 0.2519923410* ([pinned replay code](https://github.com/arhancanli/quantavane-replays/tree/407182897083b3b3c2b642e2f8ac02ff92522f09/c82)). He has not replayed round 9. Their tree evidence and PUBLISH.json linked_trees entries are retained.

AI use: AI agents prepared the search, certificate, verifiers and packet text under Ricardo Pinho's direction. This packet does not attest to line-by-line human verification.
