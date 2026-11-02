# Final live publication check — 19 October 2026

Result: **no public Bergman-space lower bound at or above 0.432 was located**.
The strongest public certified lower bound located remains Frank Wikström’s
**0.4263**, arXiv:2607.17748 (20 July 2026). This is a bounded search, not a
proof of worldwide priority. The new 0.432 claim is an unrefereed preprint.

## Sources read live before publication

- [Tao C68 page](https://teorth.github.io/optimizationproblems/constants/68a.html)
  and [current source](https://github.com/teorth/optimizationproblems/blob/main/constants/68a.md):
  still list lower bound 0.3554 and upper bound 0.6778994. Repository main was
  `46dbf03669219cb2bcf33fd5bbf65209d137f994`.
- All open Tao PRs were fetched with pagination and screened for C68,
  Korenblum, 0.432 and 0.4263. [PR #223](https://github.com/teorth/optimizationproblems/pull/223)
  proposes Wikström’s 0.4263, with no stronger target bound located.
- [arXiv search, Korenblum, newest first](https://arxiv.org/search/?query=Korenblum&searchtype=all&abstracts=show&order=-announced_date_first&size=50):
  all 45 results fit on one page. The relevant current Bergman-space result
  is [Wikström, arXiv:2607.17748](https://arxiv.org/abs/2607.17748), whose
  abstract explicitly gives 0.4263 and whose page lists only v1.
- [Google Scholar query, Korenblum constant 2026](https://scholar.google.com/scholar?hl=en&q=Korenblum+constant+2026):
  direct HTTP 200 returned an actual results page (about 152 results).
  The first page was inspected; its leading result is Wikström’s moment-duality
  paper. This is not a claim to have inspected all 152 results. Follow-up
  exact-phrase/date-filter requests returned HTTP 403 and are not counted as
  successful checks. The web-tool request also failed; the saved successful
  direct response is the evidence for this required source.
- The newer [Wikström Fock-space paper, arXiv:2609.39622](https://arxiv.org/abs/2609.39622)
  determines a radius for Fock space, a different function space. It does not
  give a stronger bound for the unweighted Bergman-space C68 constant.
- Additional web searches used “Korenblum constant 2026 lower bound”,
  “Korenblum 0.432 0.4263 constant”, and exact-phrase lower-bound variants.
  No stronger relevant public result was located.
- [Wikström’s original software record](https://zenodo.org/records/21446369)
  was readable through the web search/open service and states 0.4263.
  A supplemental direct fetch returned 403; that direct attempt is not
  counted as successful evidence. The original archive and baseline replay
  were already retained in the earlier research audit.

## Reproducible source receipts

The raw HTML and request receipts are retained locally in
`publication_checks/live/` in the research workspace. Raw third-party pages
are not redistributed with the certificate. These are SHA-256 digests of the
successful responses used for the required source checks:

| Source | UTC retrieval | SHA-256 |
| --- | --- | --- |
| tao-page | 2026-10-19T16:58:12.272704+00:00 | `9f8371aa956178d0a0d27eeddd655a658a1b3a5185b4352fb7720613483fdded` |
| tao-raw | 2026-10-19T16:58:12.696697+00:00 | `75dcdeef8f2c897e317225f36c424274bc72c600591117b2a310b3f5d99c0369` |
| arxiv-search | 2026-10-19T16:58:13.668218+00:00 | `63de4f8798892bec663234174373d9ce56a8a9da6ade93ebb9b44128a42b2d74` |
| arxiv-paper | 2026-10-19T16:58:13.839965+00:00 | `e1f6adba11019b05dd1a47a1b508792465e39d48b30138bd2fe98a0126b0dcaf` |
| scholar | 2026-10-19T16:58:14.360083+00:00 | `90d2769084cd1cc7de78279b88719196b908148468ed1e1c4a8e6eedb29a3502` |
| fock-paper | 2026-10-19T16:59:00.442203+00:00 | `af6a424bc49edabd06728e152422dd32df66fcfe897175bb4beaf74c2c376447` |

The earlier broader audit is recorded in the research workspace’s
`FINAL_SOURCE_RECHECK.md`. Search engines have indexing and pagination limits;
unindexed, private, unpublished, and later results are outside this check.
The statement above compares public results located, not all possible work.
