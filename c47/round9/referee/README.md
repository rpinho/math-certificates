# Clean-room AI referee

GPT-6 Astra via Codex wrote its own checks without reading or running producer code. Verdict: **HOLDS**. This is an AI referee, not a human review.

It checked the table definition and Tomar v5, Section 6, Lemma 6.2 following Lin; all 452 atoms and 8443 witnesses; exact masses, strict radii, containments, union area and q; the half-open cell, boundaries, duplicates, finite retention, smearing, finite ratio and downward truncation. It did not establish optimality or search completeness.

From this folder:

```sh
/usr/bin/time -l nice -n 10 python3 referee_check.py
```

The aggregate output is ../release_validation/referee-results.json. This checker emits no per-witness table; no such table is shipped or needed. The original producer proof is retained byte-for-byte in sources/producer-proof.md. Numerical fields in the retained original aggregate and historical run logs are unchanged. Paths printed by historical logs identify original inputs; the public replay uses the defaults above.

Publication edits:

- Checker: replace the opening adjective asserting independence and the startup message by wording that says it uses its own checks. Add portable default positional input paths and relocate the aggregate output. No mathematical checking code changes.
- Checker exact-type publication spellings, after the normal portable checker passed: replace math.lcm by the same positive-denominator integer Euclidean lcm, use explicit Fraction operands for the ratio division, and use Decimal Context.divide for display. These preserve every mathematical result and checking algorithm while making exact types visible to the local static inspector.
- Report: change the heading, hypothesis-table heading and recomputation-column heading to clean-room/own-check wording. Replace the count adverb by “separately” and the calculation attribution by “the referee’s own calculation”. Relocate producer proof, certificate, finite-receipt and prior-art links to their release locations. Replace the reproduction interpreter by python3 and relocate its output. Replace the Tomar paper link by the v5 DOI. Replace the table-source/retained-license statement by the source-inventory reference. Mark the supplied time/run logs as historical. Shorten only the explanatory decimal finite-margin display to 4.76293 × 10^-22 to avoid a long Luhn-valid digit run; exact fractions and numerical receipts are unchanged. Original line citations refer to the byte-for-byte producer proof and the supplied checker; the complete publication diffs at the release-job root map the checker/report edits.

These are publication edits to the supplied review, not a new review. Original SHA-256 values:

- referee_check.py: `3f61366f47f08bf7ac6a03a829ee30b3d65f4a310ef01c6fe56d989633f220d8`.
- REFEREE.md: `57cb5ddb29d241f872a907de9827ad62a0bfb733eff2697985324aa3d584e9df`.
- referee-results.json: `401bad8aaa527865b4267639d13bb4fa4217cc0497458fabbffa3f7e343bae7a`.
- referee-run.log: `108cd5614aacda063279cbb8c4adcbdc2fc363a04a0561b7b5b8d0bde9ff19b9`.
- referee-time.log: `29b0e753bafa870ac7dc2e091089420ce6271891b3194843147a3b4a23478192`.
