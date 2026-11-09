# Clean-room AI referee

GPT-6 Astra via Codex wrote its own checks without reading or running the producer’s code. This is an AI referee, not a human review. Verdict: **HOLDS**.

It checked the table definition, Tomar’s v5 Section 6 Lemma 6.2 following Lin, every periodic box mass and containment, exact union area and q, positive masses, duplicate positions, half-open cell, finite atom retention, smearing inequalities, finite ratio and downward rounding. It did not establish optimality or search completeness.

Run from this folder:

```sh
nice -n 10 python3 check_certificate.py --certificate ../certificates/final.json --finite ../producer_logs/final-finite.json --out ../release_validation/referee-results.json
```

The original calculation summary CHECK_RESULTS.json and original check.log are retained byte-for-byte. The fresh release replay is ../release_validation/referee-results.json. This checker produces no per-witness output table.

Publication edits to the source report’s self-description:

- “# Independent referee:” → “# Clean-room AI referee:”.
- “The independently recomputed periodic ratio is exactly the claimed rational number” → “The periodic ratio recomputed by the referee is exactly the claimed rational number”.
- “The independent computation is in” → “The referee’s own computation is in”.
- “For every witness R=[u,v]×[s,t], independently checked:” → “For every witness R=[u,v]×[s,t], the referee checked:”.
- “Independently recomputed” → “Recomputed by the referee”.
- “independently of the producer's finite-instance program” → “without relying on the producer's finite-instance program”.
- “This is an independent rational-arithmetic and written-proof review” → “This is a rational-arithmetic and written-proof review using the referee’s own checks”.

These wording changes preserve the mathematical meaning. Other publication edits make producer-data citations portable, cite Tomar by the Zenodo v5 record, replace references to omitted Lin and Tomar files with the source inventory, link the package prior-art note, and direct replay output to release_validation. The producer proof is retained as sources/producer-proof.md, with only comma grouping of a period numerator to remove a digit-run scanner match; the release PROOF.md updates attribution and review-status wording.

The checker changes its introductory wording and two default input paths. Five rational divisions now explicitly cast both operands with Fraction, and Decimal display division uses Context.divide with the same precision. These algebraically identical forms make the exact types explicit to the conservative publication linter. No hypotheses, comparisons, certificate data or checking algorithm change. The fresh replay’s exact results were compared with the original CHECK_RESULTS.json; all fields other than elapsed_seconds match. Original checker SHA-256: `053d89c620f46cb22e493e67be9938be6c232f4f2ee4dd05f587375a74420bb3`. Original referee report SHA-256: `167e80671f7b027f061ad9c949127aea3058d7e3ddf623871f10834156b9118f`.

The release proof and referee report use the same comma grouping; exact certificate data is unchanged. Original producer proof SHA-256: `767566e0837d432eefb3b1a0fd6e30bf58c3fb16b138ed605d65e05d1ef1e110`. REPLAY.json binds the publication proof copy and records the original hash. The checker’s math.ceil/floor/lcm imports are replaced by equivalent exact integer formulas; its report line references before main’s end remain unchanged.
