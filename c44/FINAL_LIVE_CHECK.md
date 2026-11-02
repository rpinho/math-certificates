# Final live check — C44

Live refresh: 2026-10-23T17:46:09.146503+00:00 to
2026-10-23T17:46:19.896112+00:00 (UTC), before publication.

**Outcome: no bound below 4.3576549226 was located in the sources checked.**
This is a bounded public-source audit. Exhaustive priority is not asserted.

| Source | Live result |
| --- | --- |
| [Tao's C44 entry](https://teorth.github.io/optimizationproblems/constants/44a.html) and [pinned source](https://github.com/teorth/optimizationproblems/blob/46dbf03669219cb2bcf33fd5bbf65209d137f994/constants/44a.md) | Still lists Wellens's 4.394. Repository head `46dbf03669219cb2bcf33fd5bbf65209d137f994`. |
| [Tao's open PRs](https://github.com/teorth/optimizationproblems/pulls) | All 36 open PRs fetched with pagination; titles, bodies, filenames and every returned file patch screened. No missing patches. No competing C44 bound found. The C44 line appearing in PRs 184 and 251 is unchanged README context; other matches concern unrelated constants or Boolean program flags. |
| [BakeLab/Epi-results](https://github.com/BakeLab/Epi-results/tree/97fa6a420f417458e11723c8bceb70f1529e447a/mathematics/wellens) | Head `97fa6a420f417458e11723c8bceb70f1529e447a`. README and result JSON still state 4.3654674227. The current certificate is byte-for-byte identical to the retained 108347-byte artifact, SHA-256 `ce66f1097a7284e9845113fa1dc39267932cc934fd23d9019ff13d3dcb39cf49`. The recursive tree lists only the expected Wellens README, certificate and result artifacts. |
| [Épi arXiv report, Appendix A.1](https://arxiv.org/html/2610.24944v1#A1.SS1) and [BakeLab article](https://bakelab.ai/research/articles/epi/) | Still report 4.3654674227 for Wellens's quantity. |
| [arXiv relevant-variable query](https://export.arxiv.org/api/query?search_query=all:%22relevant%20variables%22%20AND%20all:%22Boolean%22&sortBy=submittedDate&sortOrder=descending&max_results=100) | All 16 returned titles and abstracts screened. No competing improvement found. The recent [Hamming-graph paper 2609.12540](https://arxiv.org/html/2609.12540v1) treats q ≥ 3 and retains Wellens's 4.394 as the binary comparison. Its smaller q-ary coefficients do not bound binary C44. |
| [arXiv broader query](https://export.arxiv.org/api/query?search_query=au:Wellens%20OR%20%28all:%22Boolean%22%20AND%20all:%22block%20sensitivity%22%29&sortBy=submittedDate&sortOrder=descending&max_results=100) | Latest 100 of 111 records returned, sorted by submission date, covering the last twelve months and older records. Titles and abstracts screened; recent block-sensitivity papers concern other complexity comparisons or restricted classes, without a smaller universal C44 bound. This query is capped at 100 and includes unrelated authors named Wellens. |

Supplemental indexed searches included `"4.3576549226"`,
`"Wellens" "Boolean" "2026"`, `"Épi" "4.365" "Wellens"`,
`site:arxiv.org "relevant variables" "2026" Boolean`,
`site:arxiv.org "4.357" Boolean`, `site:arxiv.org "4.3654674227"`,
`site:arxiv.org "Boolean functions" "relevant variables" "4.3"`, and
`"degree-three" "potential" "5/4" Boolean`.
No additional stronger relevant bound was located. Search indexing can be
incomplete; repository APIs and the arXiv API were read directly as well.

All 51 direct source requests succeeded. URL/time/hash receipts are in
[verification/live_source_receipts.json](verification/live_source_receipts.json).
Full responses and PR screening records were retained in the publication
workspace; unrelated material is not part of the public artifacts.

## Clean-copy arithmetic gate

A fresh extraction of the approved source archive was used, without changing
either checker, its certificate inputs, or the original rejection harness.
Each command used:

```sh
uv run -q --python 3.12 --with python-flint==0.9.0 --with mpmath==1.3.0 python -B <script>
```

- `verify_c44_exact.py certificates/c44_candidate.json`: PASS, exit 0.
  Exact bound `172624496193406565421448533795/39614081257132168796771975168`.
- `independent/verify_c44_fraction.py certificates/c44_candidate.json`: PASS,
  exit 0. Exact bound `10289221775138769568521/2361183241434822606848`.
- Original `rejection_controls.py`: PASS, exit 0. All 14 C44 checker/mutation
  combinations rejected; no edited or extracted replacement harness was used.

Both bounds display approximately 4.357654922574458, with strictly positive
exact margins below `21788274613/5000000000 = 4.3576549226`.
They are distinct rational bounds because the horizons differ (96 and 72).
The unchanged preceding recurrence gives approximately 4.365467422574458;
its exact horizon-96 improvement is 1/128.

These programs were written by the same AI agent. They are algorithmic
cross-checks, without independent human review or proof-assistant formalization.
The published R₃ ≤ 10 theorem and the universal analytic proof are cited,
not formally verified by these computations. No optimality is claimed.

## Paper changes for public release

Only the following disclosure and status changes were made; mathematical
content, bibliographic credits, checkers and certificate inputs are unchanged:

- Added: “Analysis and proof drafting by AI agents under my direction;
  I reviewed the results at summary level,” with the explanation that this
  does not claim line-by-line human verification.
- Replaced preparation-only wording in the source comment, date, abstract
  and final review-status sentence with public unrefereed-preprint wording.
- Retained “not peer reviewed,” “not verified in a proof assistant” and
  “exhaustive priority is not asserted”; explicitly stated no optimality claim.

The same-AI-agent disclosure, lack of independent human review, and credits
to Wellens, BakeLab/Épi and the ten-variable theorem authors were already
present and retained. The PDF was rebuilt after these changes (five pages).
