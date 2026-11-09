# Clean-room AI referee

GPT-6 Astra via Codex, in a separate commissioned session, wrote its own checks without reading or running the producer’s code. It read the five permitted producer inputs: proof, certificate, report, comparison-bar JSON and auxiliary provenance. This is an AI referee, not a human review. Its verdict is **HOLDS**; see REFEREE.md.

Its own exact/Arb checks cover structure, every auxiliary, normalization, every log integral, the whole closed support and the decimal comparison. The original recorded cover has 131,912 closed leaves over 6,308 support cells. The archived receipts are under receipts/. Fresh release outputs are under ../release_validation/.

The cover checker’s executable code is unchanged; its opening docstring now says “its own” enclosures. The structure checker replaces only the primitive-content calculation using math.gcd with FLINT fmpz.gcd, the same exact integer gcd operation, because the installed static linter misclassifies every math import as floating arithmetic. Its opening docstring also uses the public clean-room description. The original checker hash is retained in the source hashes; the release-adapted checker is freshly replayed. The corruption runner changes its opening description and its certificate path to `../certificate.json`. The referee’s original producer proof input is published as sources/producer-proof.md with portable citations and updated status wording. Original source hashes and all omitted-cover hashes are recorded in ../sources/input-hashes.json and ../sources/omitted-artifacts.json. No new historical isolation claim is created by these hashes.

Publication edits to the report (no mathematical argument, number or verdict changed):

- The implementation sentence now says “The referee’s own implementation is …”.
- Section (e) is titled “Referee corruption controls”.
- The node-selection sentence says “The density node was selected by this referee as …”.
- The concluding assessment says “This is a clean-room AI verification of the supplied candidate …”.
- The resultant explanation says it “also explains the criterion”.
- Producer-file citations now use the public proof copy or describe the producer report in words; certificate references and reproduction commands use portable paths.
- Three long integer displays use narrow spaces for digit grouping; the rational values are unchanged and certificate bytes are untouched.
- Third-party HTML and regenerable-cover retention statements now point to the source catalog and retained summaries. Historical no-submission wording was removed.

The original referee report and proof hashes are in ../sources/input-hashes.json. The proof copy changes publication citations, status wording and adds explicit checker citations to the already stated finite checks only; it preserves the argument and line numbering. The receipt manifest describes these transformations explicitly.
