# C89c round 3: C89c >= 0.000033123924116

**Candidate and unrefereed. No human referee.** Written and checked by AI agents
under Ricardo Pinho's direction. Two AI reviews: Claude Opus 5.5 via Claude Science,
and GPT-6 Astra. Our exact checkers were separately written in one AI session.

The exact bound is `8280981029/250000000000000 = 0.000033123924116`, about 27.46%
above #308's previously printed 0.000025987. The certificate uses ambient order
eight, ordered roots and type families (t,m)=(0,4),(2,3),(4,2),(6,1), with 340
integer-square PSD blocks. The gain comes from enlarged root families, including
six-root types. No genuine nine-vertex product or Ramsey-number input is claimed.
Credit: Razborov, PPSS, KPS, and Jeetu SK's proposed pages in #277/#279; the #279
upper construction is distinct from this lower-bound method. Historical baseline
credit to Conlon, de Caen and Mackey is preserved.

- `PROOF.md`: relevant complete sections of the frozen proof.
- `CERTIFICATES.json`, `certificates/`: selected certificate and unchanged hashes.
- `scripts/`: two separately written exact checkers and selected rejection controls.
- `receipts/`: frozen accepted receipts plus explicitly named `release_*` replays.
- `review/README.md`, `PRIOR_ART.md`, `PROVENANCE.json`: review findings and sources.
- `REPRODUCE.md`, `MANIFEST.json`, `SHA256SUMS`: portable reproduction and integrity.

The full release replay in `receipts/release_c6_exact.stdout` checks every one of
the 12,346 classes, exhaustive coverage of all 2^28 labelled graphs, integer-square
PSD and random-colouring normalization. The worst graph is 905; the slack is
`112016854832021/56000000000000000000000000`. The second checker and rejection
controls have frozen receipts and were also rerun in the Astra review. This
packaging job reruns the cheaper complete coefficient checker. No numerical solver
is needed. No priority or optimality is claimed. The K5 lower lift is excluded.

The historical page snapshots in `sources/` carry only the requested “out of
reach” removal and the 18,528-variable/1,248-changed-entry clarification.
