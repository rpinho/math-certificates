# Prior art audit (2026-11-03)

This is an independent referee audit, not a search for a new construction.

Primary baseline to check: Safavi, Joshi, França and Bento (2018),
https://arxiv.org/abs/1801.04492 and https://www.jbento.info/papers/nesterov_sdp.pdf .
The claim reports Theorem 5 / (26), tuned beta 21/32 at kappa 25,
and squared distance factor 18/25. These are unverified at the start.

Public method to check: Taylor–Van Scoy–Lessard (2018),
https://proceedings.mlr.press/v80/taylor18a.html and
https://github.com/QCGroup/quad-lyap-first-order . The claimed extension
uses finite history interpolation, rather than a new optimization method.

Recent claimed comparator: Pokutta–Stellato,
https://arxiv.org/abs/2610.15125 . Its parameter conventions and public
certificates must be checked before comparing numbers.

Planned coverage: primary papers and code, official source references and
issues/PRs, recent arXiv, relevant lab/agent result repositories, and indexed
community discussions. No contact, login, posting, or publication.
There is no known central live leaderboard for this fixed-parameter theorem.
Reproduction will run on mscr, not the Mini. Further findings and coverage
limits will be appended here before any conclusion about prior results.

Completed audit:

- The primary PDF and the author's own publication page confirm José Bento
  (Boston College), the recurrence, and the norm-rate convention. The exact
  source baseline is reproduced independently at kappa 5,13,25,41; kappa 25
  gives beta 21/32 and squared factor 18/25. See baseline_controls_result.json.
- Read the 2018 public method paper and its current raw FixedStepMethod.m.
  The method already permits extended histories. I did not reuse its code,
  the claimant's port, search code, or checker. I reproduced the matched
  published analytical baseline instead of rerunning the numerical N1 SDP.
- Current public October 2026 paper/table: standard beta, with exact
  computer-assisted q10=0.564423277972893 and q100=0.859899778052548.
  The current table has no kappa25 entry. These are different parameters
  from this claim; I did not independently re-prove that paper's theorems.
- Gannot's primary paper https://arxiv.org/html/1912.13494 explicitly fixes
  standard beta in section 2.5. Its kappa25 polynomial gives numerical
  q=0.721857334585161 at beta2/3, not a bound at beta21/32.
- Dobson–Sanz-Serna–Zygalakis Theorem3.8,
  https://arxiv.org/html/2305.08658 , evaluated at the matched parameters,
  gives numerical q=0.7587883439825553 after its side constraints. This
  diagnostic is not an exact certificate or an exhaustive optimization
  of their full framework. See prior_comparisons_result.json.
- The live QCGroup web pages show 0 open issues and 0 open PRs. API requests
  returned403; the readable HTML snapshots and extracted counts are saved.
- Recently updated repository search for Nesterov Lyapunov returned no
  repository matches. GitHub constant/code search requires login and was
  not completed. The current Awesome-Optimizers list, AutoLyap site, and
  Epi/AlphaEvolve/problems READMEs were read; no matched reported number
  surfaced. OpenAI/math, kisonecat and Plasma tree APIs returned403;
  targeted indexed searches were incomplete. EinsteinArena homepage read.
- Indexed X/community queries produced no directly relevant verifiable
  discussion. This is incomplete coverage, not evidence of absence.
- Final table and Epi/AlphaEvolve re-reads at 2026-11-03 14:14:50 UTC agree
  with the earlier snapshots. Public URLs, hashes, and access errors are
  recorded in pod_evidence/public_audit.json and final_sources.json.

No novelty or priority determination is made. Relative to the 2018 primary
paper, the verified addition is one rational finite-kappa rate certificate
using an established interpolation method. No stronger reported matched
number was found in the readable material; coverage is not exhaustive.
