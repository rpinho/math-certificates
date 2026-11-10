# Prior art and release comparison scope

Did this packaging job find something new? **No.** It packages the supplied 474-atom construction and its supplied clean-room AI referee verdict HOLDS. The construction improves the named printed C47 lower bounds under the same definition. No new construction, optimality or exhaustive priority claim is made here.

The [live source](https://api.github.com/repos/teorth/optimizationproblems/contents/constants/47a.md?ref=main) and [served page](https://teorth.github.io/optimizationproblems/constants/47a.html) were refreshed on 10 November 2026 UTC (9 November local time). Source bytes match fresh main `87b4ebbd426ff8db597a2004cc45da17903bdcf2`, table blob `3023e21af6852f5bf1b7a20ab5c3da98b0706b8a`. The merged table still displays Lin’s 1.6855099933 lower and 3.879 upper bounds.

The [open-PR inventory](https://api.github.com/repos/teorth/optimizationproblems/pulls?state=open&per_page=100&page=1) returned all 85 open PRs. Every head was fetched; complete changed-file lists against the merge base with live main found only [#321](https://github.com/teorth/optimizationproblems/pull/321), [#341](https://github.com/teorth/optimizationproblems/pull/341), and [this PR (#350)](https://github.com/teorth/optimizationproblems/pull/350) touching constants/47a.md. The complete C47 diffs and their bodies were read. Their heads remain `9e02ef230d600bf792918eb36b9bc4fd94136f4f`, `b2925204970588f719a01e3520d9ff112f07b53b`, and `67cb9a7d909138343d4bceee4bbef36e72e63859`. No other open PR contains this PR’s head. Earlier rows and references are preserved.

The largest applicable public printed lower claim located remains our first filing’s 1.7040280575 (98 atoms). Doldrums / SCiEL’s #341 proposes 1.7032090736; our round-1 #321 prints 1.70311. Our supplied round-5 392-atom packet gives 1.7048221231 and remains local; the supplied commit identifier is absent from the read-only object store. These are cited comparisons; the competing SCiEL certificate was not reproduced in this packaging job. The supplied stronger certificate and the referee’s own checker were replayed on the release copy. Numerical search is outside this job.

The standard method is periodic positive atomic measures, exact rectangle coverage, finite truncation and smearing: [T. S. Tomar, Zenodo v5, Section 6, Lemma 6.2](https://doi.org/10.5281/zenodo.23716077), following Yongxi Lin. The refreshed Zenodo record confirms version 5. The [author’s paper page](https://www.mefyi.com/papers/weak-type-squares/) prints the 50-atom 1.7027237335 result. The supplied referee read the lemma and Lin’s account; consulted sources are omitted and identified by URL, version and SHA-256 in [the source inventory](referee/sources/SOURCES.md).

Recently updated public repository searches covered “centered maximal”, “square maximal 2026” and “awesome mathematics”. The second returned zero repositories. The named lab and agent repositories were refreshed through public API metadata, latest commits and root READMEs:

- [BakeLab/Epi-results](https://github.com/BakeLab/Epi-results): head `97fa6a420f417458e11723c8bceb70f1529e447a`, unchanged since the previous release’s full path-tree and root-README screen. Fresh root README has no C47/47a/Hardy/maximal keyword hit.
- [google-deepmind/alphaevolve_results](https://github.com/google-deepmind/alphaevolve_results): head `4226acbf237ff9ad10ba7673a2af127a2d8a5971`, unchanged since the previous release’s full path-tree and root-README screen. Fresh root README has no C47/47a/Hardy/maximal keyword hit.
- [google-deepmind/repository_of_problems](https://github.com/google-deepmind/repository_of_problems): public endpoint returned 404; no absence claim.
- [openai/math](https://github.com/openai/math): public endpoint returned 200; no absence claim.
- [plasma-ai/erdos](https://github.com/plasma-ai/erdos): public endpoint returned 200; no absence claim.
- [kisonecat/openai-math](https://github.com/kisonecat/openai-math): public endpoint returned 200; no absence claim.

The final API refresh rate-limited three lab repositories (HTTP 403). Ordinary filtered public Git fetches then confirmed the unchanged heads of openai/math, plasma-ai/erdos and kisonecat/openai-math; the earlier successful root-README reads are recorded in the initial request metadata. The two other accessible lab heads refreshed through the API.

These are bounded metadata and root-page refreshes, not a full reread of every repository proof. The previous full-tree screen found no stronger applicable construction; broad path matches included unrelated disk and weak-L1-majorant material. [EinsteinArena’s public landing page](https://einsteinarena.com/) was also refreshed, without a stronger C47 claim located there.

Indexed discovery used the candidate decimal, centered squares weak-type lower bounds in 2026, arXiv over the last twelve months, and X/Reddit queries. Primary results included Tomar’s paper and Lin’s account, [Spector–Stockdale’s Euclidean-ball dimension-growth upper bound](https://arxiv.org/abs/2609.05377), and [Madrid’s real-line strong-type norm](https://arxiv.org/abs/2609.12440). The latter two concern different constants. No stronger applicable lower claim surfaced in returned results. Private or unindexed channels were not accessed. Public C47 PR bodies supply additional community context. Coverage is scoped, not exhaustive.

Predictive-model baselines and SBS do not apply to an exact mathematical lower-bound certificate; BASELINES.json records this scope.
