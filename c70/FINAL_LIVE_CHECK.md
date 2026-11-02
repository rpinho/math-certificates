# Final live check — C70

Live refresh: 2026-10-23T17:58:25.590333+00:00 to 2026-10-23T17:58:33.359708+00:00 (UTC), before publication.

**Outcome: no lower bound stronger than exp(1/(2e)) > 1.20194336847
was located in the checked public sources.** This is a bounded audit;
exhaustive priority is not asserted.

| Source | Live result |
| --- | --- |
| [Tao's C70 entry](https://teorth.github.io/optimizationproblems/constants/70a.html) and [pinned source](https://github.com/teorth/optimizationproblems/blob/46dbf03669219cb2bcf33fd5bbf65209d137f994/constants/70a.md) | Still lists the trivial lower bound 1. Repository head `46dbf03669219cb2bcf33fd5bbf65209d137f994`. |
| [Tao's open PRs](https://github.com/teorth/optimizationproblems/pulls) | All 37 open PRs fetched with pagination; titles, bodies, filenames and every returned file patch screened. No missing patches. PR #226 is the only substantive C70 proposal found: Patankar's 1.201927. Other screening matches in #223, #236 and #239 concern unchanged table context, unrelated constants, author credit or commit strings. |
| [Patankar/vidigoat's source](https://github.com/vidigoat/optimization-records/tree/c7c811aa06430527cccd5f992e41cd38dd9548ca) | Head `c7c811aa06430527cccd5f992e41cd38dd9548ca`, unchanged from the preceding audit. The untruncated recursive tree, all README files, proof file, C70 submission page and both RBM scripts were inspected. The current strongest advertised C70 value remains 1.201927. The current cube script is byte-for-byte identical to the approved archive's baseline script. |
| [Carlos Toledo's replay](https://carlostoledo.co/reports/optconst-queue.html) | Still reports the preceding witness near 1.20192714257250284496, replay dated 16 October 2026. |
| [arXiv exact phrase query](https://export.arxiv.org/api/query?search_query=all:%22reverse%20Brunn%20Minkowski%22&sortBy=submittedDate&sortOrder=descending&max_results=100) | All 9 returned records screened. No stronger C70 bound located. |
| [arXiv broader reverse query](https://export.arxiv.org/api/query?search_query=all:%22Brunn%20Minkowski%22%20AND%20all:reverse&sortBy=submittedDate&sortOrder=descending&max_results=100) | All 26 returned records screened. Recent papers 2610.13596 and 2609.07463 concern Gaussian inequalities and information functionals, respectively; they do not announce a larger lower bound for this dimension-free relative-position constant. |
| [arXiv Milman/cube query](https://export.arxiv.org/api/query?search_query=all:%22Brunn%20Minkowski%22%20AND%20%28all:%22Milman%22%20OR%20all:%22cube%22%29&sortBy=submittedDate&sortOrder=descending&max_results=100) | All 29 returned records screened, including the 2026 Gaussian, centro-sectional, weighted centro-affine and affine-quermassintegral papers. No stronger C70 bound located. |
| [arXiv numeric query](https://export.arxiv.org/api/query?search_query=all:%221.201943%22%20OR%20all:%221.201927%22&sortBy=submittedDate&sortOrder=descending&max_results=100) | Zero records returned. |

Supplemental indexed searches included `"reverse Brunn" "1.201943"`,
`site:arxiv.org "reverse Brunn-Minkowski" 2026`, `"vidigoat" "70a"`,
`"reverse Brunn-Minkowski constant" "2026"`, `"1.20194336847"`,
`"exp(1/(2e))" "Brunn"`, and `"Patankar" "Brunn"`.
No stronger applicable bound was located. Search indexing and terminology
can omit work; neither these searches nor the repository/API checks
establish exhaustive priority. The arXiv queries returned all reported
records within their 100-record limits; their result sets overlap.

All 59 direct source requests succeeded. URL/time/hash receipts are in
[verification/live_source_receipts.json](verification/live_source_receipts.json).
Full response snapshots, PR patches and screening records were retained in
the publication workspace; unrelated content is not redistributed.

## Clean-copy arithmetic gate

A fresh extraction of the approved `source.zip` was used. Archive SHA-256:
`20ab7ad8a1cb4311d4850aaef38267fa7988b20be6940649639312e0faba93f8`.
Both checkers, the certificate and the original rejection harness were unchanged.
Every execution used:

```sh
uv run -q --python 3.12 --with python-flint==0.9.0 --with mpmath==1.3.0 python -B <script>
```

- `verify_c70_arb.py certificates/c70_candidate.json`: PASS, exit 0.
  Finite witness near 1.2019433684431505669948027797355; limiting value
  near 1.2019433684703144671942411393813.
- `independent/verify_c70_rational.py certificates/c70_candidate.json`:
  PASS, exit 0; positive exact rational comparisons for both claims.
- Original `rejection_controls.py`: PASS, exit 0. All 32 original
  checker/mutation combinations rejected, including all 18 C70 combinations.
  No extracted or edited replacement harness was executed.
- Unchanged `sources/patankar-rbm_cube.py --n 300000 --t 0.013`: exit 0,
  preceding bound reproduced near 1.20192714257. Its displayed zero
  interval width is a formatting artifact, not a singleton claim.
- `verify_c70_arb.py --baseline`: PASS, exit 0; separate rigorous Arb
  enclosure near 1.201927142572502844960989032655, below 1.201927142573.

Both checkers were written by the same AI agent. They verify arithmetic,
without independent human review or formal verification of the geometric
reduction or limiting proof. No optimality over convex-body pairs is claimed.

## Paper changes

Every paper change is listed in [PAPER_CHANGES.md](PAPER_CHANGES.md).
Only release-status and AI/author-review disclosure wording changed.
The mathematical body and bibliography were compared byte-for-byte with
the approved archive and are unchanged. The PDF was rebuilt.
