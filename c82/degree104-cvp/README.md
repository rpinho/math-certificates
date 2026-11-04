# C82 degree-104 closest-vector candidate

This packet gives C82 < 0.252404806 (rigorous interval bound, verify_interval.py), a candidate, unrefereed upper bound for the essential minimum of the logarithmic Zhang-Zagier height in Tao's 82a definition. The asterisk stays. Verification level L0 applies to the bound as a whole; AI review does not establish a second human party or a formal proof.

The certificate and search build on the public warm start and weighted-lattice closest-vector method of @vidigoat (#280), and the reduced-cost formula, residue-class restriction and LP infrastructure of Ricardo Pinho (#301). Doche supplies the limit-point construction; Grinsztajn and Épi supply earlier factors and methods, including Épi's unequal multiplicities. The corrected citation is C. Doche, “Zhang-Zagier heights of perturbed polynomials”, J. Théor. Nombres Bordeaux 13 (2001), 103–110, equations (5)–(9). The extraction argument is credited to the clean-room referee and written out in PROOF.md.

The certificate has six degree-104 denominators and thirteen active numerators. Its exact finite hypotheses and interval enclosure are checked by verify_interval.py, separately written from the search code by the same AI agent. The fresh release receipt is receipts/release-verifier.json. The certificate's numeric_unverified field is search metadata and is ignored by both interval checkers.

A clean-room referee supplied its own checker and reproduced the bound from only the proof and certificate; verdict HOLDS WITH CAVEATS. See review/README.md and review/REFEREE.md. The replay input proof is retained byte-for-byte despite its wrong Doche title. The release proof corrects the citation and includes the missing extraction step. The original model attestation does not expose an exact serving-model ID; a model difference is reported by coordination, not independently authenticated by the receipt.

Read PROOF.md for the cited theorem and extraction, NUMERICS.md for the validated integration, METHOD.md for the heuristic search, PRIOR_ART.md for the scoped public comparison, and REPRODUCE.md for commands and measured runtime. MANIFEST.json inventories every payload file; SHA256SUMS also binds that manifest. No search rerun is needed to verify the frozen certificate.

Did this release find something new? No. It packages an existing candidate. That supplied candidate is numerically below the printed public #280 bound under the same definition, as documented in PRIOR_ART.md; no global priority or optimality claim is made. There is no predictive score, so SBS does not apply.

AI use and author review: Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also prepared the certificate, verifiers and submission text. This does not claim a line-by-line human verification.
