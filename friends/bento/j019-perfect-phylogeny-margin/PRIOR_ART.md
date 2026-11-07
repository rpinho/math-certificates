# Prior art audit — bento_J019

Started 2026-11-03. This is an independent referee audit, not a record search.
No search, model, construction or verifier code has been written yet.

Primary baseline named by the claim: Marangola, Sheikholeslami and Bento,
“Constraints on the perfect phylogeny mixture model and their effect on reducing degeneracy”.
Sources to verify independently: https://www.jbento.info/papers/PPM_degen.pdf
and https://arxiv.org/abs/2512.24930v2 . Claimed source coefficient: 1/(36e).
Claimed extension: all same-root trees; scalar relaxation threshold 1+2/q.
General algebraic prior: Loh and Bühlmann (2014), JMLR, Theorem 7 and Lemma 27.

Audit plan: read primary definitions and authorship; inspect public paper/code listings,
recent papers and named agent result repositories; distinguish unavailable sources from
negative results. There is no numerical competition leaderboard or held-out benchmark
in this mathematical claim. Reproduce the relevant algebra and controls independently
on the authorized pod, rather than import the claimant's implementation.

Live-source findings and exact URLs will be appended below.

## Live checks before independent construction

- 2026-11-03: arXiv v2, dated 2026-10-02, confirms all three authors.
  Author homepage https://www.jbento.info/ lists this paper and links its PDF.
- Read author PDF Section V-C, equations 30–39, Assumptions 4–5, Lemmas 4–6;
  arXiv HTML https://arxiv.org/html/2512.24930v2 has corresponding equations 27–36.
  Both give 1/(36e), a one-leaf candidate neighborhood, and an explicit
  increment-only Brownian limit. The general initial-state term in the earlier
  definition is ambiguous, but is absent from the explicit limit equation.
- Read Loh–Bühlmann 2014 Theorem 7 / Lemma 27 from the primary JMLR PDF:
  strict global minimum residual score q is prior art; it applies here directly.
  The independent audit will reproduce it on the ancestry panel.
- Exact-identifier, title/2026, quadratic-variation and agent-repository searches
  located no competing source-specific theorem. No official leaderboard exists
  for this statement. GitHub search sorted by updated returned cache miss.
  Opened https://github.com/google-deepmind/alphaevolve_results and
  https://github.com/BakeLab/Epi-results . Broader repository checks pending.
- X exact-identifier and Reddit phylogeny/Bento searches returned no results;
  this is limited indexed coverage, not evidence of absence.
- Claimant's PRIOR_ART.md was read as an untrusted inventory, not source authority.
  No claimant search/verifier code was read or imported.

Best applicable baseline: the 2014 strict score minimum q; source-specific
published coefficient remains 1/(36e). No coefficient improvement is submitted.

## Broader and final source re-check

Opened the result indexes for BakeLab/Epi-results, google-deepmind/alphaevolve_results,
openai/math, kisonecat/openai-math and plasma-ai/erdos. Searched the raw OpenAI
CONTENTS.md for phylogeny and causal terminology: no match. Épi's raw README
lists its problem families, with no phylogeny match. These are index checks,
not full-text exclusions. DeepMind repository_of_problems and EinsteinArena
were inaccessible through the browser. GitHub sorted search remained inaccessible.
Public phylogenetics task/awesome-list searches returned comparative Brownian
trait software and general software lists, not this PPM degeneracy objective.
Recent-arXiv/2026 and exact-constant searches produced no additional relevant
primary result. No stronger source-specific result was located; coverage is incomplete.

Fresh primary PDFs fetched independently on the pod match the claimant's frozen
PDF hashes exactly (author 25e0100e..., arXiv a71eab12...). This is a meaningful
source-version check; claimant prose was not used to stand in for the paper.
The final raw public result-index checks and recent-paper queries occurred after
the independent enumeration, on 2026-11-03. No priority conclusion is drawn.
