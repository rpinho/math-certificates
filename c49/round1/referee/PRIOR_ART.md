# Prior art for this referee

Scope: independently referee the specified candidate, not search for a new construction. Live table, PRs #260/#322, primary gluing references, and pinned baseline data will be read before writing checker code. Public searches and their limits will be recorded below. Network is restricted to the domains in the job specification; no social-media services will be contacted. No novelty claim is assumed.

## Live sources read (2026-11-14 UTC)

- [Live 49a table](https://teorth.github.io/optimizationproblems/constants/49a.html), saved as `sources/live49a.md` and `live49a.html`: best printed lower bound is Koshta's 1.5678599, exact `(64728+sqrt(3018723123))^(1/26)`.
- [PR #260](https://github.com/teorth/optimizationproblems/pull/260), fetched with the required gh executable, `pr260.json`: merged 2026-10-26, 252292-member block, positive 2x2 transfer matrix, 26 points per step.
- [PR #322](https://github.com/teorth/optimizationproblems/pull/322), `pr322.json`: open; corrects the wording to 806 lifted sets at each pendant; does not change the bound.
- Pinned baseline repository tree and data at `c4ee81737f9f6a4ae9793586a27004553a12d5c0`; only FORMAT.md, PROOF.md, and the compressed certificate downloaded. No code downloaded.
- IRSI README at `e478c81d8b57eba956fdaf621643eb6f0781f820`: exact chain count, DEGKM1997 Lemma 4.4, and previous bounds. No code downloaded.
- GitHub issue and repository searches saved as `issues49a.json`, `repos_capacity.json`, `repos_sunflower2026.json`. Additional searches for sunflower issues and named AI result repositories returned HTTP 403 API rate-limit errors (`issues_sunflower.json`, `lab_search.json`). These searches are incomplete, not evidence of absence.
- arXiv capacity search saved as `arxiv_search.html`. Community evidence is limited to the publicly readable PR discussions due to the task's network-domain restrictions.

The baseline will be reproduced before checking the candidate. No new method or global optimality claim is being considered. This is a referee of an existing candidate; numerical novelty relative to the live printed table is distinct from novelty of the checker.

## Final source check and search limits (2026-11-14, 06:43–06:45 UTC)

The final raw table (`sources/final_live49a.md`) is byte-identical to the initial fetch. It still lists Koshta's exact bound as the best printed lower bound. The refreshed repository search (`final_repos_capacity.json`, five results) and table-issue search (`final_issues49a.json`, eleven results) show no stronger numerical proposal in the returned items. The related open #357, #326, #235 and #309 concern replays, asterisks or formalization; #322 concerns the 806-member augmentation wording. Their bodies were inspected in the saved issue results.

The initial search-rate limitation cleared on retry. The final named-repository search for `sunflower` returned 312 matches, of which the first 30 paths were inspected; it is not an exhaustive content review. A more specific `sunflower-free` search returned 35 matches, with the first 30 paths pointing to plasma-ai's general sunflower/LCM material; the numerical query `1.5678` returned zero (`final_lab_search.json`, `final_lab_capacity_search.json`, `final_lab_numeric_search.json`). These search results are bounded evidence, not proof that unpublished or differently indexed improvements do not exist.

The following current public README sources were fetched and checked for relevant result listings, without downloading or running code:

- [BakeLab/Epi-results](https://github.com/BakeLab/Epi-results), `sources/EPI_README.md`.
- [google-deepmind/alphaevolve_results](https://github.com/google-deepmind/alphaevolve_results), `sources/ALPHAEVOLVE_README.md`.
- [google-deepmind/alphaevolve_repository_of_problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems), `sources/ALPHAEVOLVE_PROBLEMS_README.md` (the actual repository name corresponding to RULES.md's shorthand).
- [openai/math](https://github.com/openai/math), `sources/OPENAI_MATH_README.md`.
- [plasma-ai/erdos](https://github.com/plasma-ai/erdos), `sources/PLASMA_README.md`.
- [kisonecat/openai-math](https://github.com/kisonecat/openai-math), `sources/KISONECAT_README.md`.
- [togethercomputer/EinsteinArena-new-SOTA](https://github.com/togethercomputer/EinsteinArena-new-SOTA), `sources/EINSTEIN_README.md`, found via `einstein_search.json`. The separate arena website is outside the permitted network domains and was not visited.

None of those README listings supplies a competing C49 numerical bound. The arXiv search returned eight records; among the last twelve months, Tang–Zhang's December 2025 paper is directly relevant and the April 2026 coloring-channel paper concerns a different capacity. [Tang–Zhang](https://arxiv.org/html/2512.20055) was fetched as `sources/TZ2025.html`; it supplies the capacity context cited by the table, not a competing numerical construction. The primary operative gluing statement was read in the pinned Koshta proof and IRSI mathematical descriptions and independently proved in REFEREE.md. The original DEGKM PDF's linked host is outside the whitelist, so it was not accessed.

Conclusion for this job: the supplied candidate strictly beats the **live printed exact Koshta bound** under the same definition. This referee is a reproduction/verification, not a new construction, and makes no unrestricted priority or global-optimality claim.
