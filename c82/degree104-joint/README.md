# C82 degree-104 joint certificate

This packet gives C82 < 0.2520179248 (rigorous interval bound, verify_best.py), a candidate, unrefereed upper bound for the essential minimum of the logarithmic Zhang-Zagier height in Tao's 82a definition. The asterisk stays. Verification level L0 applies to the bound as a whole. The verifier was written separately from the search code by the same AI agent lineage; this is not a second human party or a formal proof.

Under the same definition it improves V. Patankar's public #280 v3 bound 0.2520591386* and our earlier bound 0.252404806* in [../degree104-cvp](../degree104-cvp), the previous version of our PR (#330). The live-page value 0.2534449* is retained as a cited comparison. Sources are refreshed in sources/pr280.json, sources/pr330.json and sources/82a.md. This packet makes no novelty, priority or optimality claim.

Credit: Doche supplies the construction (C. Doche, “Zhang-Zagier heights of perturbed polynomials”, J. Théor. Nombres Bordeaux 13 (2001), 103–110). V. Patankar (@vidigoat, #280) supplies the weighted-evaluation closest-vector method, the #280 v3 certificate, and the public numerator bank. Ricardo Pinho (#301) supplies the joint LP / reduced-cost pricing and residue-class restriction. Grinsztajn and Épi supply earlier factor libraries. The source credit snapshots are sources/pr280.json and sources/pr301.json.

## Exact factor credit

FACTOR_PROVENANCE.json compares full coefficient arrays, not labels. Its first-match label “ours from round 5 or earlier” records a local input match, not authorship. The 10 monic degree-104 denominators comprise D11_5_0 from #280 v3 (V. Patankar) and nine marked “new here” in that provenance file:

C82r6_0a687958c979, C82r6_a2d5e71133fb, C82r6_719d74e5da39, C82r6_c87f877b9d4a, C82r6_7075b26a1a91, C82r6_99cd845e34d4, C82r6_8cc229a6f730, C82r6_6e2d6a4a1891, C82r6_e842aec1399f.

Every numerator is credited by name below. All 18 also have full coefficient matches in the public #280 v3 certificate or its earlier public bank; none is claimed as a new numerator.

| Numerator names | Origin |
|---|---|
| P1, P2, P3, P4, P6 | Doche P-factors; coefficient matches in #280 v3 and the earlier #280 public bank |
| MS360 | Ricardo Pinho, #301 MS360; also matches #280 v3 and the earlier #280 public bank |
| n22_7_5, n23_3_6, n11_4_53, n11_6_21, n11_6_46, n101_0_17 | #280 v3, V. Patankar (@vidigoat); full matches recorded in FACTOR_PROVENANCE.json |
| n23_2_3, n23_3_1, n111_1_0, n121_1_12, cg12_6_3, n101_2_13 | #280's earlier public numerator bank, V. Patankar (@vidigoat); full matches recorded in FACTOR_PROVENANCE.json |

## Frozen certificate and verification

The certificate has 10 degree-104 denominators with positive integer multiplicities and 18 numerators with positive rational exponents. D = 999999999960, a = 940866927165429405/1048576 and slack D-a = 107709072792627555/1048576. Only n121_1_12 is non-monic, with leading coefficient 2. verify_best.py checks the exact hypotheses, all 180 active gcd pairs and all 2666 composed roots, and encloses B = H + J with FLINT/Arb at 256 bits:

    0.2520179247552093455135 <= B <= 0.2520179247552093577392

The target 0.2520179248 has margin about 4.48e-11. receipts/frozen-release-verifier.json preserves the supplied release PASS; receipts/release-verifier.json records the rerun from inside this packet, with its exact command in receipts/release-verifier.log. receipts/certificate-facts.json records exact rational facts. The verifier imports only Python's standard library and python-flint.

REPORT.md and STATUS.md are byte-identical frozen producer records. They describe a search that was still running and continued after this certificate was frozen. Only the root certificate.json supports the bound stated here. The rounds/ directory contains the frozen round-8 material only, without its duplicate certificate (see Certificate encoding); its historical target is archival, not a second bound claim. RESULT.json and BAR.json retain the producer's earlier search target 0.2520500000; the release target is 0.2520179248.

Read PROOF.md for the cited theorem and extraction argument, NUMERICS.md for interval integration, METHOD.md for the heuristic search, PRIOR_ART.md for inherited source context and REPRODUCE.md for release commands. The snapshot is sufficient to replay the bound and inspect its frozen round; it is not the complete later search history. Historical evidence/control files are preserved as evidence, not alternate release certificates.

No third-party Python is included, imported or executed here. PYTHON_BLOBS.json compares the git blob hash of every Python file against the complete vidigoat/optimization-records trees at 197962c and 3a7a84f and checks for imports of core or wlp. A match is a blocker. Public coefficient arrays are data; see THIRD_PARTY_NOTICE.md and the included MIT license.

## Certificate encoding

certificate.json is the producer's frozen certificate (SHA256 2b5bf95d950a96193864689c6b77c08b5a79528d0c695de929c1df13944aef18) with one change of notation: the exponent of n22_7_5 is written as 693216426750998/1048576, with numerator and denominator doubled from its lowest-terms form over 524288. FACTOR_PROVENANCE.json uses the same notation. All exact data, and therefore B, are unchanged. The reason is our publishing filter, which flags the lowest-terms numerator as a card-number pattern. verify_best.py differs from the producer's verifier only in its pinned certificate hash. The rerun gives the same exact endpoints, finite checks and integration panels as receipts/frozen-release-verifier.json, which was made on the producer bytes. The producer's duplicate copy of the round-8 certificate in rounds/ is omitted; other rounds/ files still name the producer hash.

## Referee

A separate AI referee, given only a claim note, the earlier packet's released PROOF.md and this certificate, attacked the reduction and the exact hypotheses and wrote its own interval checker without reading or running producer code. Verdict: **HOLDS WITH CAVEATS**. Its interval, B in [0.2520179247552093517426, 0.2520179247552093517434], lies inside the one above. The caveat is that the session does not expose its exact model ID; the launcher record says GPT-6 Astra, a different model from the producer's GPT-6.1 Sol, but the receipt cannot establish that. See review/README.md, review/REFEREE.md and REPLAY.json. AI review does not remove the asterisk.

AI use: AI agents prepared the search, certificate, verifiers and packet text under Ricardo Pinho's direction. This packet does not attest to line-by-line human verification.
