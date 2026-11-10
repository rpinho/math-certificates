# Clean-room AI referee

GPT-6 Astra via Codex wrote its own checks without reading or running producer code. Verdict: **HOLDS**. This is an AI referee, not a human review.

It checked the table definition and Tomar v5, Section 6, Lemma 6.2 following Lin; all 440 atoms and 7806 witnesses; exact masses, strict radii, containments, union area and q; the half-open cell, boundaries, duplicates, finite retention, smearing, finite ratio and downward truncation. It did not establish optimality or search completeness.

From this folder, the following command regenerates the aggregate and per-witness outputs shown in the checker. The per-witness table is omitted from the package.

```sh
/usr/bin/time -l nice -n 10 python3 referee_check.py
# Outputs: ../release_validation/referee-results.json
#          ../release_validation/witness_results.json
# After replay: /usr/bin/trash ../release_validation/witness_results.json
```

Original per-witness table SHA-256: `2f1dde6cdfd39e840429c09d94de249f65ec31561a045407d2091dc3432890b5`. The release replay generated identical table bytes; see ../release_validation/omitted-generated.json. The original producer proof is retained byte-for-byte in sources/producer-proof.md.

Publication edits, exhaustively:

- In the checker docstring, replace the opening adjective asserting independence with “using the referee’s own checks”; relocate its certificate and finite-receipt input paths to ../certificates/final.json and ../producer_logs/final-finite.json. Relocate both output paths to the release-validation folder shown above.
- In the opening report sentence, describe the rational arithmetic as “The referee’s own rational arithmetic”. In the hypothesis list, describe the count as “the referee’s own count”. In the section (c) transition, replace the adverb asserting independence by “separately”. In section (b), describe the periods as “The periods read by the referee”, the per-witness mass as “mass counted by the referee”, and the table column as “Recomputed by the referee”. In the novelty sentence, replace the independence claim by “a verification using its own checks”. Each replacement retains a grammatical complete sentence.
- In every report certificate, finite-receipt and proof citation, replace the original producer-directory prefix by ../certificates/, ../producer_logs/ and sources/ respectively. Preserve original line numbers against the retained original producer proof. Replace the previous-round referee's internal directory citation by “the previous round’s AI referee report”.
- Replace the report's table-download paragraph by a paragraph stating that the consulted HTML, raw Markdown and Apache-2.0 license are omitted and identified in sources/SOURCES.md; preserve its definition quotation and source markers.
- Replace Tomar’s pinned source hyperlink by the Zenodo v5 DOI and explicitly name v5 in the link label. Replace its local TeX citations by consulted v5 lines 302–323 and line 302, with sources/SOURCES.md. Replace Lin’s local proof citation by consulted proof lines 119–150 and that inventory; retain Lin’s pinned public proof link.
- Replace the per-witness file citation by a description of the omitted regenerable table, retaining what each row records and pointing here for its hash and regeneration command.
- Link the report's prior-art and baseline-scope citations to ../PRIOR_ART.md and ../BASELINES.json.
- Replace the report's reproduction opening by the portable command and fresh output locations. Replace its final output sentence by the retained aggregate/run-log names and the omitted-table description. Preserve the supplied 14.29-second duration and inherited nice-20 statement as historical facts.
- In the supplied exact_results.json and referee_run.log, relocate only the historical certificate path to ../certificates/final.json. All numerical fields remain unchanged.
- Following the preceding release, replace math.lcm by the equivalent integer Euclidean-algorithm implementation, replace math.ceil and math.floor by their exact integer definitions on rationals, spell the operands of all rational divisions as Fraction, and use Decimal Context.divide for display. The original math import is conservatively treated as floating arithmetic by the local static inspector; the explicit rational types and integer ceiling/floor definitions resolve that ambiguity. The normal portable checker passed before these changes; no hypotheses, inequalities, fractions or checking algorithm change.

The complete checker diff is supplied at the release-job root as referee-checker-publication.diff. These are publication edits to the supplied review, not a new commissioned review. Original SHA-256 values:

- Checker: `f792ae74a398af1de188692a41eebade6178b8b9396c1b3d02793168e6e3b9df`.
- Report: `d25dd8e1fbd66201cf409c5731298556224a8b6603f6c98c77e1555cf81c2b05`.
- Aggregate result: `615c0adb5000f8c39a6bc46d73297f54f8d8521fa68a7f850466b9def4f8087c`.
- Run log: `99310fa5e9ef1d64d0817b3b29ac46752742b8581281f4180d3ccf3d0171593c`.

Checker line citations in the retained report refer to the supplied original checker, identified by its hash above; the publication diff maps those locations to the relocated checker. Producer-proof line citations refer to the retained byte-for-byte original proof.
