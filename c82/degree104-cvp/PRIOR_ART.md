# C82 release source audit — 4 November 2026

This is a packaging/replay job, not a search. The supplied construction already has a separate exact/interval verification and a clean-room replay. Did this release find something new? No. The supplied candidate is below the checked printed #280 value under the same live definition, but no global priority claim is made.

## Live scoreboard and open work

At main 87b4ebbd426ff8db597a2004cc45da17903bdcf2, the [live 82a page](https://teorth.github.io/optimizationproblems/constants/82a.html) still prints the asterisked upper value 0.2534449. All 62 open PRs and their changed-file lists were retrieved. Exactly #242, #280 and #301 change 82a. Their current bodies, author evidence, comments and diffs are archived in sources/. #242 changes replay/asterisk status of older rows. @vidigoat (#280) prints the degree-104 upper claim 0.2524177045, and Ricardo Pinho (#301) prints the degree-44 upper claim 0.253091834. The former is the best public upper claim in this checked inventory. None is merged. These are cited public values, not new local measurements.

Sources: [#280](https://github.com/teorth/optimizationproblems/pull/280), [#301](https://github.com/teorth/optimizationproblems/pull/301), [#242](https://github.com/teorth/optimizationproblems/pull/242). The #280 author snapshot has login vidigoat and an empty profile name, but #280's own page diff credits V. Patankar (table row and bibliography) and its commits are authored by Vidit Patankar, so release credit is V. Patankar (@vidigoat, #280).

The producer first independently replayed #280's pinned public certificate. Its historical receipt is evidence/replay.json; the public certificate is prior_sources/certificate.json and verify_public.py is the separate pinned checker. This release reruns only the final candidate checker. See evidence/verifier_provenance.json and REPRODUCE.md. No predictive claim is involved; SBS is inapplicable.

## Public code and agent/lab repositories

An updated-first GitHub repository search for Zhang Zagier and public default-branch heads were refreshed; snapshots are sources/repository-search.json and sources/repository-heads.json. The tracked sources include BakeLab/Epi-results, both google-deepmind alphaevolve result/problem repositories, openai/math, plasma-ai/erdos, kisonecat/openai-math, togethercomputer/EinsteinArena-new-SOTA, Grinsztajn's repository, vidigoat/optimization-records and Pinho's certificate repository. The producer's content/path checks and READMEs are retained in prior_sources/ and its full audit is sources/PRODUCER_PRIOR_ART.md. The release head refresh supplements rather than repeats every historical content check. The first guessed Neehan endpoint returned 404; the updated-first search supplied the correct endpoint Neehan/zhang-zagier-82a, whose head and README were then refreshed (sources/neehan-refresh.json). The current README matches the producer archive byte-for-byte.

The public warm start is vidigoat/optimization-records commit 3a7a84fec9c64ae426f06a5f52597c84b3453ba0. Its closest-vector method and product-start description are the direct method baseline; Pinho's #301 supplies the reduced cost and residue restriction. The final candidate is independently verified from exact frozen coefficients. Search prices and LP values are heuristic.

## Papers and community

The correct primary construction reference is C. Doche, [Zhang-Zagier heights of perturbed polynomials](https://www.numdam.org/item/JTNB_2001__13_1_103_0/), J. Théor. Nombres Bordeaux 13 (2001), 103–110, equations (5)–(9). Its page-108 averaging lemma and page-109 degree normalization were checked by the referee; the release refreshed the primary article and PDF. PROOF.md corrects the old title while retaining the original referee input.

Recent context: [Burgos Gil–Menares–Qu–Sombra, arXiv:2601.18978v2](https://arxiv.org/abs/2601.18978) concerns LP convergence and duality, not a competing printed numerical upper claim in its abstract. The producer's last-year query also found Qu–Yang 2609.39505 and no competing numerical claim. The release refreshed public web searches for Zhang-Zagier upper bounds in 2026 and arXiv, plus public X/Reddit results; results were sparse/noisy and showed older table/replay pages rather than a smaller claim. No account access or private community was used. Community coverage is not exhaustive.

The older replay report [Carlos Toledo's public report](https://carlostoledo.co/reports/optconst-queue.html) concerns older merged C82 candidates and is consistent with #242's scope. It is not a new construction here. The clean-room referee's separate source audit is review/PRIOR_ART.md.

## Interpretation

This supplied candidate beats the checked public printed #280 value under the same C82 definition. It remains candidate/unrefereed, with the prose reduction and arithmetic backend requiring review. A finite checked source set does not establish worldwide priority. The release itself makes no new construction, settles no new open problem and tests no prediction on new data.
