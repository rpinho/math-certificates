# C82 degree-104 joint certificate

This packet gives **C82 < 0.2519696460*** (rigorous interval bound, verify_best.py), a candidate, unrefereed upper bound for the essential minimum of the logarithmic Zhang-Zagier height in Tao's 82a definition. The asterisk stays. Verification level L0 applies to the bound as a whole. The producer verifier was written separately from the search code by the same AI agent lineage. The separate AI referee and its provenance limits are described below.

Under the same definition, the exact certified upper endpoint is below V. Patankar's public [#280 v5](https://github.com/vidigoat/optimization-records/blob/191064e7ccd88718853fe239dfd3890a8dc0fa37/tao/certificates/c82/v5/README.md) printed bound 0.2519889614* by at least 0.0000193154127508999188, and below [our previous packet for this PR](https://github.com/rpinho/math-certificates/blob/dadec7353c435a081befca73888e3ab6cef3134a/c82/degree104-joint/README.md), 0.2519744488*, by at least 0.0000048028127508999188. That previous packet was round 9 of this search. The gap below [our earlier certificate in this PR](https://github.com/rpinho/math-certificates/blob/a12c3622120c39af776902dbe49b6eff97a4d189/c82/degree104-joint/README.md), 0.2519923410*, is at least 0.0000226950127508999188. The gaps below [#280 v4](https://github.com/vidigoat/optimization-records/blob/79ce0dfb211a67ff7e387b58b0d19ff1d6accfba/tao/certificates/c82/v4/README.md)'s 0.2520079724* and [#280 v3](https://github.com/vidigoat/optimization-records/blob/197962c9610f583e9bc56efe37bfb994c1eeb834/tao/certificates/c82/v3/README.md)'s 0.2520591386* are at least 0.0000383264127508999188 and 0.0000894926127508999188, respectively. The exact comparison gaps are computed by certificate_facts.py in receipts/certificate-facts.json: each is the exact printed comparator minus the exact certified upper endpoint, rounded downward. These are deterministic mathematical comparisons, with no predictive score.

Earlier versions of our PR printed [0.2519964890*](https://github.com/rpinho/math-certificates/blob/3be6b2f133db43374ea30767b58c62ce2d39686a/c82/degree104-joint/README.md), [0.2520179248*](https://github.com/rpinho/math-certificates/blob/98208a40e043e578d35183b418452f316112a658/c82/degree104-joint/README.md) and [0.252404806*](https://github.com/rpinho/math-certificates/blob/5461d490552a518667c3fd3fceff33ebdb4d347c/c82/degree104-cvp/README.md). The cited [live-page value pinned to the supplied commit](https://github.com/teorth/optimizationproblems/blob/87b4ebbd426ff8db597a2004cc45da17903bdcf2/constants/82a.md) is 0.2534449*. Producer source captures are in prior_sources/; earlier publication captures and pinned tree evidence are in sources/. This packaging job finds no new construction or method: it ships the producer's completed result and makes no priority or optimality claim.

Credit: C. Doche supplies the perturbed-polynomial construction (J. Théor. Nombres Bordeaux 13 (2001), 103–110). V. Patankar (@vidigoat, #280) supplies the iterated LLL numerator search as well as the weighted-evaluation LLL / closest-vector method, public v3/v4/v5 certificates and coefficient bank. Ricardo Pinho supplies the earlier dual-weighted LLL numerator work [Pin26] (PR #229, [pinned contribution](https://github.com/teorth/optimizationproblems/tree/d27a71ff70b57af6e529e6016f741b5cd7dc6f4d)), joint LP, reduced-cost pricing and residue-class restriction. Grinsztajn and Épi supply earlier factor libraries. Credit snapshots include sources/pr280.json, sources/pr301.json and prior_sources/pr280-final.json.

## Exact factor credit

FACTOR_PROVENANCE.json records full coefficient arrays and every source match. Local matches say where a factor was reused; they are not exclusive authorship claims. “New here” means generated in round 10 of this search and absent from the comparison inputs, without a novelty claim. Every #280 match below credits V. Patankar (@vidigoat). Doche's P1, P2, P3, P4 and P6 retain Doche's mathematical credit.

| Denominator | Origin and full coefficient matches |
|---|---|
| C82r8_b4ce16615ae6 | ours from round 9 as C82r8_b4ce16615ae6; round-9 final LP master as C82r8_b4ce16615ae6; ours from round 8 as C82r8_b4ce16615ae6; round-8 final LP master as C82r8_b4ce16615ae6 |
| C82r8_fcd3a4b2d94d | ours from round 9 as C82r8_fcd3a4b2d94d; round-9 final LP master as C82r8_fcd3a4b2d94d; ours from round 8 as C82r8_fcd3a4b2d94d; round-8 final LP master as C82r8_fcd3a4b2d94d |
| C82r8_1f8710f82b1d | ours from round 9 as C82r8_1f8710f82b1d; round-9 final LP master as C82r8_1f8710f82b1d; ours from round 8 as C82r8_1f8710f82b1d; round-8 final LP master as C82r8_1f8710f82b1d |
| C82r9_923bd2177a3d | ours from round 9 as C82r9_923bd2177a3d; round-9 final LP master as C82r9_923bd2177a3d |
| C82r10_a6af275a730c | new here (round 10 of this search) |
| C82r10_76a523b0f880 | new here (round 10 of this search) |

| Numerator | Origin and full coefficient matches |
|---|---|
| P1 | ours from round 7 as P1; ours from round 6 as P1; ours from round 5 or earlier as P1; #280 v5 as P1; #280 v4 as P1; #280 v3 as P1; earlier bank as P1; initial coefficient union (including v5) as P1; ours from round 9 as P1; full rounds 8–9 union bank as P1; round-9 final LP master as P1; ours from round 8 as P1; full round-8 union bank as P1; round-8 final LP master as P1 |
| P2 | ours from round 7 as P2; ours from round 6 as P2; ours from round 5 or earlier as P2; #280 v5 as P2; #280 v4 as P2; #280 v3 as P2; earlier bank as P2; initial coefficient union (including v5) as P2; ours from round 9 as P2; full rounds 8–9 union bank as P2; round-9 final LP master as P2; ours from round 8 as P2; full round-8 union bank as P2; round-8 final LP master as P2 |
| P3 | ours from round 7 as P3; ours from round 6 as P3; ours from round 5 or earlier as P3; #280 v5 as P3; #280 v4 as P3; #280 v3 as P3; earlier bank as P3; initial coefficient union (including v5) as P3; ours from round 9 as P3; full rounds 8–9 union bank as P3; round-9 final LP master as P3; ours from round 8 as P3; full round-8 union bank as P3; round-8 final LP master as P3 |
| P4 | ours from round 7 as P4; ours from round 6 as P4; ours from round 5 or earlier as P4; #280 v5 as P4; #280 v4 as P4; #280 v3 as P4; earlier bank as P4; initial coefficient union (including v5) as P4; ours from round 9 as P4; full rounds 8–9 union bank as P4; round-9 final LP master as P4; ours from round 8 as P4; full round-8 union bank as P4; round-8 final LP master as P4 |
| P6 | ours from round 7 as P6; ours from round 6 as P6; ours from round 5 or earlier as P6; #280 v5 as P6; #280 v4 as P6; #280 v3 as P6; earlier bank as P6; initial coefficient union (including v5) as P6; ours from round 9 as P6; full rounds 8–9 union bank as P6; round-9 final LP master as P6; ours from round 8 as P6; full round-8 union bank as P6; round-8 final LP master as P6 |
| N82r8_3cc45c82e976 | ours from round 9 as N82r8_3cc45c82e976; full rounds 8–9 union bank as N82r8_3cc45c82e976; round-9 final LP master as N82r8_3cc45c82e976; ours from round 8 as N82r8_3cc45c82e976; full round-8 union bank as N82r8_3cc45c82e976; round-8 final LP master as N82r8_3cc45c82e976 |
| N82r9_3f20ba401cbd | full rounds 8–9 union bank as N82r9_3f20ba401cbd |
| N82r9_4336f6c43520 | ours from round 9 as N82r9_4336f6c43520; full rounds 8–9 union bank as N82r9_4336f6c43520; round-9 final LP master as N82r9_4336f6c43520 |
| N82r10_606dbc0a25c8 | new here (round 10 of this search) |
| N82r10_b0bf5b3c7238 | new here (round 10 of this search) |
| N82r10_170f661d6c60 | new here (round 10 of this search) |
| N82r10_41ddd69ffcd5 | new here (round 10 of this search) |
| N82r10_456efce38800 | new here (round 10 of this search) |
| N82r10_7de87861282b | new here (round 10 of this search) |
| N82r9_1aa3601f1b5c | ours from round 9 as N82r9_1aa3601f1b5c; full rounds 8–9 union bank as N82r9_1aa3601f1b5c; round-9 final LP master as N82r9_1aa3601f1b5c |
| N82r10_1bbacf8ab38a | new here (round 10 of this search) |
| N82r10_27154344b965 | new here (round 10 of this search) |
| N82r10_1f26d88dc0d3 | new here (round 10 of this search) |
| N82r10_ee8bca9e620b | new here (round 10 of this search) |
| N82r10_562e07bebc11 | new here (round 10 of this search) |
| N82r10_54dfa8f276cc | new here (round 10 of this search) |
| N82r10_94a396a37f48 | new here (round 10 of this search) |
| N82r10_1d4bc4f945b2 | new here (round 10 of this search) |
| N82r8_4d6f8374e36e | full rounds 8–9 union bank as N82r8_4d6f8374e36e; ours from round 8 as N82r8_4d6f8374e36e; full round-8 union bank as N82r8_4d6f8374e36e; round-8 final LP master as N82r8_4d6f8374e36e |
| N82r10_124431dd6625 | new here (round 10 of this search) |
| N82r10_e1ea62d3db1d | new here (round 10 of this search) |
| N82r10_15818c8051b0 | new here (round 10 of this search) |
| N82r10_c1eacfe02031 | new here (round 10 of this search) |
| N82r10_33402b0b35d5 | new here (round 10 of this search) |
| N82r9_a49c3746e570 | ours from round 9 as N82r9_a49c3746e570; full rounds 8–9 union bank as N82r9_a49c3746e570; round-9 final LP master as N82r9_a49c3746e570 |
| N82r10_586046c46951 | new here (round 10 of this search) |
| N82r10_45fe7b99ca93 | new here (round 10 of this search) |
| N82r10_d6fbcfac6e8c | new here (round 10 of this search) |
| N82r10_cdce61d0a006 | new here (round 10 of this search) |
| N82r10_e867b4951b24 | new here (round 10 of this search) |
| N82r10_c1f59e8c85f8 | new here (round 10 of this search) |
| N82r10_862f4cf24c9b | new here (round 10 of this search) |
| N82r10_2596dac40d1c | new here (round 10 of this search) |
| N82r10_de57f20345c4 | new here (round 10 of this search) |
| N82r10_ab5efea58089 | new here (round 10 of this search) |

Exact full-coefficient overlaps, recomputed by certificate_facts.py:

- V. Patankar's #280 v3: 0 denominator factors; 5 numerator factors (P1, P2, P3, P4, P6).
- V. Patankar's #280 v4: 0 denominator factors; 5 numerator factors (P1, P2, P3, P4, P6).
- V. Patankar's #280 v5: 0 denominator factors; 5 numerator factors (P1, P2, P3, P4, P6).

V5 itself reused four denominators from our round-7 certificate in this PR: C82r6_8c76cd0c4e53, C82r6_935548ec48fe, C82r6_083ca9b3950a and C82r7_dd0a7c419abf, with the public prefix Pin330c_. The current certificate retains none of those four denominators. Its exact overlaps with all three #280 versions are the five numerator factors named above. Public-data reuse does not transfer original mathematical authorship.

## Frozen certificate and verification

The certificate has six monic degree-104 denominators with positive integer multiplicities and 40 numerators with positive rational exponents. D = 999999999960, a = 469303044808512511/524288 and slack D-a = 54984955170515969/524288. There are 13 non-monic numerators: N82r9_3f20ba401cbd (leading coefficient 2), N82r9_4336f6c43520 (leading coefficient 3), N82r10_170f661d6c60 (leading coefficient 3), N82r10_41ddd69ffcd5 (leading coefficient 2), N82r10_7de87861282b (leading coefficient 7), N82r9_1aa3601f1b5c (leading coefficient 2), N82r10_27154344b965 (leading coefficient 3), N82r10_54dfa8f276cc (leading coefficient 8), N82r10_1d4bc4f945b2 (leading coefficient 4), N82r10_c1eacfe02031 (leading coefficient 2), N82r10_d6fbcfac6e8c (leading coefficient 3), N82r10_cdce61d0a006 (leading coefficient 2), N82r10_c1f59e8c85f8 (leading coefficient 6). Their leading-coefficient logarithms are included. verify_best.py checks all 240 active gcd pairs and all 4198 composed roots, and encloses B = H + J with FLINT/Arb at 256 bits:

    0.2519696459872490977703 <= B <= 0.2519696459872491000812

The exact upper endpoint is strictly below 0.2519696460. receipts/frozen-release-verifier.json preserves the producer's final replay; receipts/release-verifier.json records the packet rerun, with exact command and environment in receipts/release-verifier.log. receipts/certificate-facts.json records the recomputed rational facts, comparison gaps and v3/v4/v5 overlaps. The verifier imports only Python's standard library and python-flint.

Rounds 9 and 10 of this search continued round 8 warm; round 8 had added #280 v5 data. The final certificate-producing solve is archive-num-77-0. rounds/ contains that solve's files, its final restricted master and dual, and finished.json. The duplicate round certificate is omitted in favor of certificate.json. The producer stopped on its wall-time budget while the latest completed rounds still improved; this is not an optimality result. The round-8 (0.2519758217*) and round-9 (0.2519744488*, previous packet at commit dadec7353c435a081befca73888e3ab6cef3134a) certificates are superseded and their standalone certificates are not shipped. NOTE.md explains the retained archival paths.

REPORT.md, STATUS.md, PRIOR_ART.md, NUMERICS.md, RESULT.json, BAR.json, SEARCH_SUMMARY.json, COMPUTE.json, own scripts, evidence/ and prior_sources/ describe the completed producer. REPRODUCE.md adds packet commands before its producer section. Producer evidence and rejection controls are historical records; only final-bound producer and referee replays are run by this packaging job. Read PROOF.md for the theorem and extraction argument, and METHOD.md for the heuristic search. This packet reproduces the final bound, not the full search.

No Python from vidigoat/optimization-records is included, imported or executed. seal.py recomputes PYTHON_BLOBS.json against every blob in complete metadata-only trees at 197962c, 3a7a84f, 79ce0df and 191064e and checks imports of core or wlp. Any match is a blocker. Public coefficient arrays are data; see THIRD_PARTY_NOTICE.md and the MIT license. Retained third-party data files are copied byte-for-byte, never reserialized. Raw historical snapshots preserve original URLs and prose; authored citations are pinned to commits. Whole-file omissions are listed in NOTE.md.

## Certificate encoding

certificate.json (SHA256 0c4df95ec7a422943176ab560b961531a41f5f7f83adeb8daae24878de643077), verify_best.py and FACTOR_PROVENANCE.json are unchanged round-10 bytes. The producer used equal-fraction representations for some rational weights to avoid spurious publishing-filter patterns. Those exact representations are preserved; CERTIFICATE_ENCODING.md describes the unchanged exact release encoding; the released q_rational strings are in certificate.json. No rational data or verifier hash pin has been changed. Historical verifier copies retain their original pins.

## Referee

The clean-room round-10 referee was supplied only the three files in review/inputs/, attacked the reduction and exact hypotheses, and wrote its own interval checker without reading or running producer code. Verdict: **HOLDS WITH CAVEATS**. Its outward enclosure is B in [0.2519696459872490990419691935079545, 0.2519696459872490990419691935079546], inside the producer interval. The unresolved caveat is model provenance: the session identifies itself as GPT-6 / Codex but cannot attest its exact serving-model ID or certify that it differs from the producer. The numerical computation is unaffected. The referee trusts the cited averaging theorem, the height/extraction argument, Python integer arithmetic and FLINT/Arb; this is AI review, without human expert review or proof-assistant formalization. See review/REFEREE.md, review/replay/report.md and REPLAY.json. The original receipt is review/replay/REPLAY.original.json; root REPLAY.json adapts paths and recomputes inputs_hash. AI review does not remove the asterisk. The original REFEREE.md and PRIOR_ART.md are preserved byte-for-byte, including their historical live links and their initial-status prose; the final verdict and closing source account govern their interpretation.

Arhan Canli's independent replays, disclosing AI assistance (Claude, Anthropic), cover earlier versions of this PR only: 0.252404806* and 0.2520179248* ([pinned replay code](https://github.com/arhancanli/quantavane-replays/tree/7696576f41b418a5eacaed423b7b2078a521e26e/c82)); 0.2519964890* ([pinned replay code](https://github.com/arhancanli/quantavane-replays/tree/2b7475fb6e9186973de44c1f2b0db4cb1d0ae6bf/c82)); and 0.2519923410* ([pinned replay code](https://github.com/arhancanli/quantavane-replays/tree/407182897083b3b3c2b642e2f8ac02ff92522f09/c82)). He has not replayed this round-10 certificate. Their tree evidence and PUBLISH.json linked_trees entries are retained.

AI use: AI agents prepared the search, certificate, verifiers and packet text under Ricardo Pinho's direction. This packet does not attest to line-by-line human verification.
