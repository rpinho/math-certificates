# Clean-room AI referee

GPT-6 Astra via Codex wrote its own checks without reading or running producer code. Verdict: **HOLDS**. This is an AI referee, not a human review.

It checked the table definition and Tomar’s v5 Section 6 Lemma 6.2 following Lin, all 454 atoms and 6920 witness masses, strict radii, containments, exact union area and q, the half-open cell, boundaries, duplicates, finite retention, smearing, finite ratio and downward truncation. It did not establish optimality or search completeness.

Run from this folder:

```sh
nice -n 10 python3 referee_check.py
```

Fresh aggregate results go to ../release_validation/referee-results.json. The supplied exact_results.json and referee_run.log are retained byte-for-byte. The regenerable witness table is omitted. Original per-witness table SHA-256: `5c8c4445f002de04a4236ba3b2ad8f787cc77078c78bf47db501327923212632`. The command above regenerates the per-witness table; its output location appears in the checker and REPRODUCE.md. Remove it with /usr/bin/trash after replay. Original producer proof is retained byte-for-byte in sources/producer-proof.md.

Publication wording replacements (each applies wherever present):

- “The independent computation” → “The referee’s own computation”.
- “The independent check” → “The referee’s own check”.
- “Independent witness checks” → “Referee’s own witness checks” in the section heading.
- “independently counted mass” → “mass counted by the referee”.
- “Independent result” → “Referee’s own result” in the table heading.
- “the independent calculation” → “the referee’s own calculation”.
- “it independently verifies the supplied construction” → “it verifies the supplied construction with its own checks”.

Other publication edits, exhaustively:

- Rename the checker to referee_check.py and the run log to referee_run.log; update every reference in the report and reproduction paragraph.
- Replace the producer-directory prefix on certificate, finite-receipt and proof citations by ../certificates/, ../producer_logs/ and sources/ respectively; preserve the original proof line numbers.
- Replace the statement that table HTML and raw Markdown are retained by an omitted-source inventory reference. Replace the raw-table source citation by consulted lines 5–27 and that inventory.
- Replace Tomar’s source-file hyperlink by the Zenodo v5 DOI, explicitly naming Section 6. Replace the local TeX citation by consulted v5 lines 302–323 and the source inventory.
- Expand Lin’s abbreviated proof-note commit pin to the full commit; replace the local proof-note citation by consulted lines 119–150 and the source inventory. The historical table commit mentioned in the report is unchanged.
- Replace the per-witness file citation by a description of the omitted regenerable table, its original hash and regeneration command here. Preserve the statement of what each row contains.
- Link the prior-art citation to the package prior-art note.
- Replace the reproduction paragraph by the portable command, fresh aggregate-result destination, retained original aggregate/log names and the omitted-table description. Preserve the original 2.41-second timing and one-process statement.
- Relocate the checker’s two input paths and two output paths. Replace math.lcm with the equivalent integer Euclidean-algorithm implementation, make the ratio’s two Fraction operands explicit, and use Decimal Context.divide for display. The normal portable checker passed before these spelling changes; no hypotheses, comparisons or checking algorithm changed.

The full checker diff is retained at the release-job root as referee-checker-publication.diff. The original mathematical statements are unchanged. Original checker and report SHA-256 values:

- Checker: `fb301fa80e658096b19eed37b765070bc2d0973bbf13cf1fce993cdb09ea5964`.
- Report: `d417ecfaba361cadc423cb100a7898ebbb326f49bc6091223af5aa5d92d57c88`.
