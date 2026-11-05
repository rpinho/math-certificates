# C82 degree-104 joint certificate

This packet gives C82 < 0.2519923410 (rigorous interval bound, verify_best.py), a candidate, unrefereed upper bound for the essential minimum of the logarithmic Zhang-Zagier height in Tao's 82a definition. The asterisk stays. Verification level L0 applies to the bound as a whole. The verifier was written separately from the search code by the same AI agent lineage; this is not a second human party or a formal proof.

Under the same definition, the certified upper endpoint is below V. Patankar's public [#280 v4](https://github.com/teorth/optimizationproblems/pull/280) bound 0.2520079724* by at least 0.0000156314279916046029, and below [the previous version of our PR (#330)](https://github.com/teorth/optimizationproblems/pull/330), 0.2519964890*, by at least 0.0000041480279916046029 (packet commit [3be6b2f133db43374ea30767b58c62ce2d39686a](https://github.com/rpinho/math-certificates/commit/3be6b2f133db43374ea30767b58c62ce2d39686a)). The gap below #280 v3's 0.2520591386* is at least 0.0000667976279916046029. The exact comparison gaps are computed by certificate_facts.py in receipts/certificate-facts.json: each is the exact printed comparator minus the exact certified upper endpoint, rounded downward.

Our interval replay of the public v4 certificate gives B in [0.25200797232842968 +/- 9.19e-18] (evidence/pr280-v4-replay.json, rigorous, evidence/verify_public_v4.py). Earlier versions of our PR printed 0.2520179248* and 0.252404806*; the latter packet is [../degree104-cvp](../degree104-cvp). The cited [live-page value](https://github.com/teorth/optimizationproblems/blob/87b4ebbd426ff8db597a2004cc45da17903bdcf2/constants/82a.md) 0.2534449* remains a historical comparison. Source snapshots are in sources/ and prior_sources/. This packet makes no novelty, priority or optimality claim.

Credit: Doche supplies the construction (C. Doche, “Zhang-Zagier heights of perturbed polynomials”, J. Théor. Nombres Bordeaux 13 (2001), 103–110). V. Patankar (@vidigoat, #280) supplies the weighted-evaluation closest-vector method, the v3/v4 certificates, and the public numerator bank. Ricardo Pinho (#301) supplies the joint LP / reduced-cost pricing and residue-class restriction. Grinsztajn and Épi supply earlier factor libraries. Credit snapshots are sources/pr280.json and sources/pr301.json.

## Exact factor credit

FACTOR_PROVENANCE.json records full coefficient arrays and every source match. “Ours from round 6” and “ours from round 5 or earlier” record local input matches, not exclusive authorship. “New here” means absent from those comparison libraries; it is not a novelty claim.

| Denominator | Origin and full coefficient matches |
|---|---|
| D11_5_0 | ours from round 6; #280 v4; #280 v3 |
| C82r6_8c76cd0c4e53 | ours from round 6 |
| C82r6_935548ec48fe | ours from round 6 |
| C82r6_083ca9b3950a | ours from round 6 |
| D11_12_0 | #280 v4 |
| D31_5_0 | #280 v4 |
| C82r7_dd0a7c419abf | new here |
| C82r7_7883918fa4f2 | new here |

D11_5_0 is V. Patankar's #280 v3 factor, also in v4. D11_12_0 and D31_5_0 are from #280 v4. The three C82r6 factors are from our round-6 search; C82r7_dd0a7c419abf and C82r7_7883918fa4f2 are marked “new here.”

Every numerator is credited by name below. P1, P2, P3, P4 and P6 are Doche P-factors; MS360 is Ricardo Pinho's #301 factor. The other listed public factors come from V. Patankar (@vidigoat, #280). Coefficient reuse does not transfer mathematical authorship of Doche's or #301's factors.

| Numerator | Full coefficient matches |
|---|---|
| P1 | ours from round 6; #280 v4; #280 v3; ours from round 5 or earlier; #280 bank |
| P2 | ours from round 6; #280 v4; #280 v3; ours from round 5 or earlier; #280 bank |
| P3 | ours from round 6; #280 v4; #280 v3; ours from round 5 or earlier; #280 bank |
| P4 | ours from round 6; #280 v4; #280 v3; ours from round 5 or earlier; #280 bank |
| P6 | ours from round 6; #280 v4; #280 v3; ours from round 5 or earlier; #280 bank |
| MS360 | ours from round 6; #280 v4; #280 v3; ours from round 5 or earlier; #280 bank |
| n11_4_53 | ours from round 6; #280 v3 |
| n11_6_21 | ours from round 6; #280 v4; #280 v3 |
| n101_0_17 | ours from round 6; #280 v3; #280 bank |
| n121_3_30 | ours from round 6; #280 bank |
| n11_6_49 | ours from round 6; #280 v4; #280 v3 |
| n101_7_34 | ours from round 6; ours from round 5 or earlier; #280 bank |
| n11_7_17 | #280 v4 |
| n11_10_5 | #280 v4 |
| n11_10_6 | #280 v4 |
| n31_6_7 | #280 v4 |
| n101_0_28 | #280 bank |
| cg2_4_0_c2 | #280 v3; ours from round 5 or earlier; #280 bank |

The exact overlap with #280 v4, by full coefficient comparison, is **3 denominators** (D11_5_0, D11_12_0, D31_5_0) and **12 numerators** (P1, P2, P3, P4, P6, MS360, n11_6_21, n11_6_49, n11_7_17, n11_10_5, n11_10_6, n31_6_7). Names agree in both files. The comparison input prior_sources/pr280-v4-certificate.json is the public v4 certificate (SHA256 c1981f1c4f5e1813f625c54ce952e9b5fa210f2cccbd5ac832d2a41f12ccc72f). certificate_facts.py recomputes this overlap.

## Frozen certificate and verification

The certificate has eight monic degree-104 denominators with positive integer multiplicities and 18 numerators with positive rational exponents. D = 999999999856, a = 939550863051360379/1048576 and slack D-a = 109025136797644677/1048576. The two non-monic numerators are n121_3_30 (leading coefficient 9) and n31_6_7 (leading coefficient 2). verify_best.py checks the exact hypotheses, all 144 active gcd pairs and all 2224 composed roots, and encloses B = H + J with FLINT/Arb at 256 bits:

    0.2519923409720083869767 <= B <= 0.2519923409720083953971

The exact upper endpoint is strictly below the target 0.2519923410. receipts/frozen-release-verifier.json preserves the producer's final stated-bound PASS; receipts/release-verifier.json records the rerun inside this packet, with the exact command and environment in receipts/release-verifier.log. receipts/certificate-facts.json records recomputed exact rational facts, comparison gaps and factor overlap. The verifier imports only Python's standard library and python-flint.

REPORT.md, STATUS.md, PRIOR_ART.md, NUMERICS.md, RESULT.json, BAR.json, SEARCH_SUMMARY.json, COMPUTE.json, scripts, evidence/ and prior_sources/ describe the finished producer. REPRODUCE.md adds packet commands before the producer section. Its stricter search target was not met; the certified publication bound is 0.2519923410. The final certificate came from rounds/den-5. The search ended after three no-gain rounds (6–8), a scoped plateau rather than an optimality result. rounds/finished.json names the final restricted-9 master and den-5 dual. Only the den-5 files, their master, finished.json and restricted-9.json are retained, without the duplicate certificate. Other historical search paths in producer records refer to files not retained here. The producer's historical rejection controls are archival evidence, not fresh controls of this packaging job.

Read PROOF.md for the theorem and extraction argument, NUMERICS.md for interval integration, METHOD.md for the heuristic search, PRIOR_ART.md for source context and REPRODUCE.md for commands. The packet replays the final bound and preserves its final round, not the full search.

No Python from vidigoat/optimization-records is included, imported or executed here. PYTHON_BLOBS.json compares the git blob hash of every included Python file against every blob in the complete source trees at 197962c, 3a7a84f and 79ce0df and checks imports of core or wlp. Any match is a blocker. Public coefficient arrays are data; see THIRD_PARTY_NOTICE.md and the included MIT license. Third-party data files are copied byte-for-byte, without reserializing JSON. Three historical PR-body metadata snapshots are omitted as whole files because they contain obsolete unfinished-status text; the relevant #280/#330 producer snapshots and all coefficient data remain.

## Certificate encoding

certificate.json (SHA256 ee9622b5e141489ad6fbf98b0ec5c43ac3e1b657f8876b435e65c536f359fdd5), verify_best.py and FACTOR_PROVENANCE.json are copied byte-for-byte from c82r7_release. The producer already expressed some exponents as equal fractions with doubled numerator and denominator, because the publishing filter flags certain lowest-terms numerators as card-number patterns. We preserve those exact representations and never print the restricted numerators. CERTIFICATE_ENCODING.md lists only the released representations. No rational data or verifier hash pin has been changed. The final den-5 duplicate certificate is omitted; use the root certificate. Historical verifier copies retain their original pins.

## Referee

A separate AI referee, given only a claim note, the earlier packet's released PROOF.md and this certificate, attacked the reduction and the exact hypotheses and wrote its own interval checker without reading or running producer code. Verdict: **HOLDS WITH CAVEATS**. Its interval, B in [0.251992340972008391240902200131, 0.251992340972008391240904220544], lies inside the one above. The caveat is that the session does not expose its exact model ID; the launcher record says GPT-6 Astra, a different model from the producer's GPT-6.1 Sol, but the receipt cannot establish that. See review/README.md, review/REFEREE.md and REPLAY.json. AI review does not remove the asterisk.

AI use: AI agents prepared the search, certificate, verifiers and packet text under Ricardo Pinho's direction. This packet does not attest to line-by-line human verification.
