# C89b round 3: C89b < 0.001653032

**Candidate and unrefereed. No human referee.** Written and checked by AI agents
under Ricardo Pinho's direction. Two AI reviews: Claude Opus 5.5 via Claude Science,
and GPT-6 Astra. Our exact checkers were separately written in one AI session.

The 256-part, four-layer graphon has exact monochromatic K5 density
`10014541091180996983/6058287395472553279488 = 0.001653031696493139…`, strictly
below the printed upper threshold. This is about 1.91% below #307's exact
`2405659597/1427496763392`. The #307 graphon is the three-layer member of the
same family. This builds on Jeetu SK (SK2026), #277/#307, PPSS and Thomason.
The K5 lower-bound lift is excluded.

- `PROOF.md`: the relevant complete sections of the frozen proof, with only
  the requested checker wording, comparison and credit fixes.
- `CERTIFICATES.json`, `certificates/`: selected witness and unchanged hashes.
- `scripts/`: full-matrix and structured exact checkers and the control suites.
- `receipts/`: frozen accepted receipts plus explicitly named `release_*` replays.
- `review/README.md`, `PRIOR_ART.md`, `PROVENANCE.json`: review findings and sources.
- `REPRODUCE.md`, `MANIFEST.json`, `SHA256SUMS`: portable reproduction and integrity.

`receipts/release_radial_selected.stdout` records the fast exact release replay.
The generator reconstructs the frozen witness byte for byte after decompression;
`receipts/release_validation.json` checks that match, both colour sums, rounding
and the exact #307 comparison. Frozen full-matrix receipts remain evidence of
the separate exhaustive count; this packaging job reruns the cheaper structured
count. No numerical optimizer is needed. No priority or optimality is claimed.

The files under `sources/` are historical comparison material, with the requested
18,528-variable/1,248-changed-entry clarification in `pr307_89b.md`.
