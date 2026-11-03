# C57c release source audit, 3 November 2026

This packages an existing frozen candidate. No search for a new construction
or numerical optimization was performed. `PRIOR_ART.md` is the unchanged
parent-job prior-art record, included to resolve the proof citation. Its
multi-target repository and PR entries are historical provenance.

The live [57c page](https://teorth.github.io/optimizationproblems/constants/57c.html)
and [upstream source](https://github.com/teorth/optimizationproblems/blob/87b4ebbd426ff8db597a2004cc45da17903bdcf2/constants/57c.md)
still list lower 0.5708858 and upper 0.6563937 (0.65628589*).
The current [Wikström preprint](https://arxiv.org/abs/2610.34580) exposes
only v1, submitted 25 October 2026. Theorem 1.2 gives lower 0.612242;
Theorems 1.3 and 7.3 give upper 0.6562681 for the same univalent constant.
The phase congruence extended here is his equation (12); the starting
center is his equation (9). His [supplement](https://doi.org/10.5281/zenodo.23650159)
is the public code/data baseline. His short verifier was not rerun in this
packaging job; the predecessor recorded reproduction. This job reruns the
frozen candidate's controls, aggregation and selected ranges, not a new
baseline search. No journal publication or human refereeing was established.

All 53 open upstream items (47 PRs and six issues) were enumerated with
pagination. Every PR file list and patch, every open-item body and issue
comment, and every PR review summary and review comment were read.
[PR #223](https://github.com/teorth/optimizationproblems/pull/223) updates
57a/57b only, using different Wikström papers. PR #272 mentions that family
numbering but changes 31b and README. No open item changes 57c or gives a
stronger 57c bound in the material inspected.

The 13 inherited repository HEADs and READMEs were refreshed, including
BakeLab/Epi-results, both google-deepmind AlphaEvolve repositories,
openai/math, plasma-ai/erdos, kisonecat/openai-math and the awesome-ai-for-math
list. No HEAD changed from the inherited audit and no additional applicable
result was found in those READMEs. GitHub public repository searches for
"univalent Bloch", "Bloch Landau", "2610.34580" and EinsteinArena were
sorted by recent update. Web/arXiv queries included those names, the exact
0.612242/0.61230/0.6562681 values, and results since 25 October. They found
no stronger applicable bound. The paper's Section 6.3 explicitly says a
higher-order compression certificate is in preparation; it states no
additional numerical lower bound. This creates a concrete priority
limitation: no novelty claim is made for our extensions.

The web searches also returned van Staden's 20 October preprint
(0.65628589, weaker than Wikström's upper result), the older
Carroll–Ortega-Cerdà work, and work on the ordinary Bloch constant, which
is a different quantity. Public community queries for Reddit, X and Tao's
blog produced no additional relevant 57c result; X was not directly
accessible. Search coverage is limited and does not prove global priority.

Full public-source receipts and a final refresh are retained in the local
release job's `sources/` directory and summarized in its `REPORT.md`.

Final release refresh: 2026-11-03T12:12:34.841605+00:00; upstream main 87b4ebbd426ff8db597a2004cc45da17903bdcf2; 47 open PRs / 53 total open items; no changed audited repository HEADs.

The Zenodo supplement was re-read online: version 1.0.0, modified 25 October 2026, with the same two bounds. The direct arXiv search endpoint failed to fetch; the current abstract/version page and indexed arXiv/web searches were available.
