# C82 degree-104 joint certificate

This packet gives C82 < 0.2519964890 (rigorous interval bound, verify_best.py), a candidate, unrefereed upper bound for the essential minimum of the logarithmic Zhang-Zagier height in Tao's 82a definition. The asterisk stays. Verification level L0 applies to the bound as a whole. The verifier was written separately from the search code by the same AI agent lineage; this is not a second human party or a formal proof.

Under the same definition it improves V. Patankar's public [#280 v3](https://github.com/teorth/optimizationproblems/pull/280) bound 0.2520591386* by at least 0.0000626496117988272974, and [the previous version of our PR (#330)](https://github.com/teorth/optimizationproblems/pull/330), 0.2520179248*, by at least 0.0000214358117988272974 (packet commit [98208a40e043e578d35183b418452f316112a658](https://github.com/rpinho/math-certificates/commit/98208a40e043e578d35183b418452f316112a658)). These are exact lower bounds on the printed comparators minus the certified upper endpoint, computed by certificate_facts.py in receipts/certificate-facts.json. After this search ended, V. Patankar posted a v4 certificate to #280 with 0.2520079724* (13:30 UTC, 5 November 2026); our verifier, run on that public certificate, gives B in [0.25200797232842968 +/- 9.19e-18] (evidence/pr280-v4-replay.json, rigorous, evidence/verify_public_v4.py, which is verify_public.py with its pinned hash changed to the v4 certificate), so the bound here is also below v4. v4 uses none of the seven denominators newly found in this search; the two certificates share D11_5_0 and nine numerators, all already present in #280 v3. Our earlier bound 0.252404806* in [../degree104-cvp](../degree104-cvp) and the cited [live-page value](https://github.com/teorth/optimizationproblems/blob/87b4ebbd426ff8db597a2004cc45da17903bdcf2/constants/82a.md) 0.2534449* remain historical comparisons. Public source snapshots are in sources/ and prior_sources/*-final.*. This packet makes no novelty, priority or optimality claim.

Credit: Doche supplies the construction (C. Doche, “Zhang-Zagier heights of perturbed polynomials”, J. Théor. Nombres Bordeaux 13 (2001), 103–110). V. Patankar (@vidigoat, #280) supplies the weighted-evaluation closest-vector method, the #280 v3 certificate, and the public numerator bank. Ricardo Pinho (#301) supplies the joint LP / reduced-cost pricing and residue-class restriction. Grinsztajn and Épi supply earlier factor libraries. The source credit snapshots are sources/pr280.json and sources/pr301.json.

## Exact factor credit

FACTOR_PROVENANCE.json compares full coefficient arrays, not labels. Its first-match label “ours from round 5 or earlier” records a local input match, not authorship. The eight monic degree-104 denominators comprise D11_5_0 from #280 v3 (V. Patankar) and seven marked “new here” in that provenance file (new in this search relative to #280 and our earlier libraries; C82r6_7075b26a1a91 and C82r6_99cd845e34d4 were already in the previous version of this packet, at commit 98208a40e043e578d35183b418452f316112a658):

C82r6_7075b26a1a91, C82r6_99cd845e34d4, C82r6_8c76cd0c4e53, C82r6_f770a2649784, C82r6_935548ec48fe, C82r6_d24f4c93ef26, C82r6_083ca9b3950a.

Every numerator is credited by name below. All 15 have full coefficient matches in the public #280 v3 certificate or its earlier public bank; none is claimed as a new numerator.

| Numerator names | Origin |
|---|---|
| P1, P2, P3, P4, P6 | Doche P-factors; coefficient matches in our round 5 or earlier, #280 v3 and the earlier #280 public bank |
| MS360 | Ricardo Pinho, #301 MS360; also matches our round 5 or earlier, #280 v3 and the earlier #280 public bank |
| n22_7_5, n11_4_53, n11_6_21, n101_0_17, n11_6_49, n101_6_2 | #280 v3, V. Patankar (@vidigoat); n22_7_5, n101_0_17 and n101_6_2 also match the earlier #280 public bank |
| n121_3_30, n101_2_37 | #280's earlier public numerator bank, V. Patankar (@vidigoat) |
| n101_7_34 | #280's earlier public numerator bank, V. Patankar (@vidigoat); also matches a factor in our earlier round-5 input |

## Frozen certificate and verification

The final certificate has eight degree-104 denominators with positive integer multiplicities and 15 numerators with positive rational exponents. D = 1000000000064, a = 58700834920208207/65536 and slack D-a = 6835165083986097/65536. Only n121_3_30 is non-monic, with leading coefficient 9. verify_best.py checks the exact hypotheses, all 120 active gcd pairs and all 2126 composed roots, and encloses B = H + J with FLINT/Arb at 256 bits:

    0.2519964889882011564383 <= B <= 0.2519964889882011727026

The target 0.2519964890 has margin about 1.18e-11. receipts/frozen-release-verifier.json preserves the final producer PASS on the original encoding; receipts/release-verifier.json records the rerun from inside this packet, with its exact command in receipts/release-verifier.log. receipts/certificate-facts.json records recomputed exact rational facts and comparison gaps. The verifier imports only Python's standard library and python-flint.

REPORT.md, STATUS.md, PRIOR_ART.md, NUMERICS.md, NOTE.md, RESULT.json, BAR.json and the producer section of REPRODUCE.md now describe the finished producer. Publication paths are relative, and REPORT.md uses the P3 encoding described below. The final certificate came from rounds/num-16-1-*. The search ended after three no-gain rounds (17–19); this is a scoped plateau, not an optimality result. RESULT.json and BAR.json retain the historical frozen search target 0.2520500000; the release target is 0.2519964890. RESULT.json retains the original producer certificate hash, whose exact rational data equal the root release certificate.

Read PROOF.md for the cited theorem and extraction argument, NUMERICS.md for interval integration, METHOD.md for the heuristic search, PRIOR_ART.md for producer source context and REPRODUCE.md for release commands. The packet is sufficient to replay the bound and inspect its final round; it does not retain the full search history. rounds/ contains only final num-16-1 material and restricted-16.json, without its duplicate certificate. Historical per-round verifiers retain their original producer hash pin. Three historical corrupted-certificate copies in evidence/ are omitted because they contain the restricted P3 encoding; the corresponding control logs and outcomes remain archival evidence. Those controls are not claimed as fresh tests of the release encoding.

No Python from vidigoat/optimization-records is included, imported or executed here. PYTHON_BLOBS.json compares the git blob hash of every Python file against the complete vidigoat/optimization-records trees at 197962c and 3a7a84f and checks for imports of core or wlp. A match is a blocker. Public coefficient arrays are data; see THIRD_PARTY_NOTICE.md and the included MIT license.

## Certificate encoding

certificate.json (SHA256 b71150bb7c1a7ac34e86b447e565cdd6c6d33bb225fa910f0acced4136f74171) is the producer's final certificate (SHA256 aa90cc311fae557b4e3661aa7ea1313bdf29d25a0eafa951035f6b6897edeced) with one change of notation: the exponent of P3 is written as 10908223350879106/1048576, doubled from its lowest-terms form over 524288. FACTOR_PROVENANCE.json uses the same notation. All exact data, and therefore B, are unchanged. Our publishing filter flags the lowest-terms numerator as a card-number pattern, so it is omitted throughout this packet. verify_best.py differs from the producer's verifier only in its pinned certificate hash. The rerun gives the same exact endpoints, finite checks and integration panels as receipts/frozen-release-verifier.json, which was made on the producer bytes. The producer's duplicate copy of the final-round certificate in rounds/ and its three corrupted-certificate control copies in evidence/ are omitted; other historical round and evidence files still name the producer hash.

## Referee

A separate AI referee, given only a claim note, the earlier packet's released PROOF.md and this certificate, attacked the reduction and the exact hypotheses and wrote its own interval checker without reading or running producer code. Verdict: **HOLDS WITH CAVEATS**. Its interval, B in [0.251996488988201164531880087886, 0.251996488988201164532207712015], lies inside the one above. The caveat is that the session does not expose its exact model ID; the launcher record says GPT-6 Astra, a different model from the producer's GPT-6.1 Sol, but the receipt cannot establish that. See review/README.md, review/REFEREE.md and REPLAY.json. AI review does not remove the asterisk.

AI use: AI agents prepared the search, certificate, verifiers and packet text under Ricardo Pinho's direction. This packet does not attest to line-by-line human verification.
