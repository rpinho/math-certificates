# Clean-room AI referee

GPT-6 Astra via Codex wrote its own checks without reading or running producer code. Verdict: **HOLDS**. This is an AI referee, not a human review.

It checked the table definition, Tomar’s v5 Section 6 Lemma 6.2 following Lin, all 474 atoms and 6292 witness masses, strict radii and containments, exact union area and q, the half-open cell, boundaries, duplicates, finite retention, smearing, finite ratio and downward truncation. It did not establish optimality or search completeness.

Run from this folder:

```sh
nice -n 10 python3 referee_check.py --certificate ../certificates/final.json --finite ../producer_logs/final-finite.json --output ../release_validation/referee-results.json --witness-output ../release_validation/witness_checks.csv
```

The original CHECK_RESULTS.json and check.log are retained byte-for-byte. Fresh results go to ../release_validation/referee-results.json. The regenerable witness table is omitted. Original per-witness table SHA-256: `a5b29b40e56da1b7232258f85478906a33fb5755e1ee62d160e9adb19b5145ac`. The command above regenerates it; remove the table with /usr/bin/trash after replay.

Wording edits to the referee’s self-description:

- “# Independent referee of” → “# Clean-room AI referee of”.
- “The full independent output” → “The full output of the referee’s own checks”.
- “Hypothesis | Independent check” → “Hypothesis | Referee’s own check”.
- “implemented independently in” → “implemented by the referee in”.
- “Independently recomputed” → “Recomputed by the referee”.
- “the independently recomputed certificate values” → “the certificate values recomputed by the referee”.
- “The independent check gives” → “The referee’s own check gives”.

These wording edits leave the mathematical content unchanged. Other publication edits relocate input citations and commands, cite Tomar by the Zenodo v5 DOI, point omitted source and witness-table links to their inventories, and link the package prior-art note. The quoted definition is preserved; third-party source files are omitted.

The checker changes two input defaults, makes six rational division forms explicit with Fraction, uses Decimal Context.divide for display, and replaces math.ceil/floor/lcm with equivalent exact integer formulas. These algebraically identical forms address the conservative linter’s unresolved-division and blanket math-import classifications. No hypotheses, comparisons, certificate data or checking algorithms change. The complete diff is supplied alongside this packet in the local release deliverables. The original producer proof is retained byte-for-byte in sources/producer-proof.md.

Original checker SHA-256: `ad5dc41885eed8e96678e7821d345edd7086373812f7b511906a02f45d517af8`. Original report SHA-256: `e9b0d4ee79c815d557bd6f425eaaf405c7910432fb79eb31308ab598795d4cb8`.
