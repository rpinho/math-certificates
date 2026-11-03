# C44 round 9 prior-art audit — candidate, unrefereed

Started 2026-11-03 00:51 UTC. This is the first written job file, before code.
The job has at most eleven hours (finish by 11:51 UTC); the pod must be
vacated and results retrieved by 13:04 UTC, 45 minutes before its expiry.
The user's explicit pod allowance is at most fourteen workers, nice 10,
single-threaded BLAS, in /root/os/math_c44r9_1103 on math-cpu-11.
No commits, pushes, PRs, posts, messages, or pod termination are authorized.

## Baseline and sources to inspect

Local baseline: ../c44r8/REPORT.md, PROOF.md, exact verifiers and frozen
packet. Candidate and unrefereed: R4=22, 46<=R5<=50, 94<=R6<=109,
C44 < 2.0417086280; lower bound 3/2. The next R5 obstruction is the
minimum-support quartic derivative at scalar budget 201/4, including four
pairs. The next R6 obstruction is lambda=7/4.

Official live table: https://teorth.github.io/optimizationproblems/constants/44a.html
Raw table: https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/44a.md
All open PRs and issues will be fetched from teorth/optimizationproblems,
with all PR diffs searched for C44, 44a, relevant variables and degree-junta
terms. PR294: https://github.com/teorth/optimizationproblems/pull/294 .
GitHub repository searches will be sorted by recent update.

Primary methods to credit and reproduce: Nisan–Szegedy relevant-variable
bound; Chiarelli–Hatami–Saks and Wellens weighted restriction framework;
Shinkar–Tal/CHS 3/2 construction; Rasoolzadeh cubic catalogue; low-weight
Reed–Muller and low-support eigenspace classifications; Barnes–Wall energy
gap, with exact hypotheses inherited from round 8 to be checked.

Required public result repositories: BakeLab/Epi-results,
google-deepmind/alphaevolve_results, google-deepmind/repository_of_problems,
openai/math, EinsteinArena, plasma-ai/erdos, kisonecat/openai-math and
related repositories identified in the audit. Recent arXiv coverage includes
Nisan–Szegedy, Chiarelli–Hatami–Saks, Wellens and citing work since 2024.
X is not available to this job. Private communities are unavailable.
Public indexed Reddit, blogs and community summaries will be checked.

This audit is bounded coverage, not a claim of novelty or priority. Live
sources and result repositories must be checked again before any such claim.

## Initial live refresh, 00:58 UTC, 3 November 2026

The directly fetched official HTML and raw Markdown both list the unrefereed
4.3576549226 candidate (Pinho), versus Wellens's published 4.394.
All 47 open PRs and the complete paginated open-issue feed were fetched;
all PR diffs are retained in sources/pr_diffs. The only diffs changing
constants/44a.md are #285 (Wellens citation correction to 2022:20) and #294
(the current 2.0417086280 candidate with R4=22, R5<=50, R6<=109).
PR bodies, comments and reviews were fetched for the C44 threads. Loose
text matches in other PRs are hexadecimal coincidences or neighboring
Boolean sensitivity work (#283); no stronger C44 result was identified.

Recently-updated GitHub searches are retained as sources/github_*_updated.json.
They identify the existing rpinho packet and moffatstudio/relevant-variables-degree,
a September 2026 unrefereed nonattainment/R3 proof; its README explicitly
credits Tarannikov–Kirienko for R3=10 and does not improve the present caps.
All eleven required/related result repositories were inspected through their
live metadata, recursive trees and READMEs (sources/repos). Épi's Wellens
packet remains the 4.3654674227 degree-48 predecessor; no stronger usable
C44 method was located in these bounded checks. The actual DeepMind problem
repository is google-deepmind/alphaevolve_repository_of_problems.

Primary arXiv references checked: CHS 1801.08564, Wellens 1903.08214 and
2005.00566; recent searches since 2024 locate Krotov–Valyuzhenich's June
2024 revision 2311.05566, Potapov 2410.21937 (discrete two/three-valued degree
comparisons), and Valyuzhenich 2609.12540 (q>=3 Hamming graphs, not the binary
bound). The upcoming 5 November 2026 Toulouse seminar describes work in
progress without an available applicable theorem. The 2021 Ratio Bound
construction blog traces the CHS/Shinkar–Tal family to older perfect-coloring
work; the construction is not new. Indexed public community searches found
no stronger applicable result. X is unavailable; private Discord/Telegram
and authenticated global code search are outside coverage. Semantic Scholar
citation-feed requests for NS/CHS/Wellens were rate-limited; those failures
are retained, and indexed citing-paper searches are the available fallback.

Best public method to reproduce is the round-8 packet linked in PR294,
candidate and unrefereed, with explicit classical completeness premises.
The local frozen exact checkers will be replayed before an improved bound
is accepted. No novelty, priority or public-record claim is made.

Audit corrections: the all-open-PR feed contains 47 entries; the broad loose
C44 grep also matched hex strings, so actual changed paths were checked.
A shell-glob error on the rpinho/math-certificates tree request was corrected
with a quoted URL; its current c44/small-degree-classification/round8/PROOF.md
path is present. An attempted obsolete public REPORT path returned 404;
the local round-8 report and public PROOF are the controlling input instead.
OpenAlex CHS metadata and its since-2024 citing feed were fetched as an
additional citation-index fallback. No claim of exhaustive citation coverage.

OpenAlex's CHS citing feed since 2024 returns five works: Sparse juntas on
the biased hypercube (2024); Krotov–Valyuzhenich perfect colorings (2024);
Potapov discrete functions (2025 publication); Valyuzhenich q-ary Hamming
graph bound (2025 publication); Complexity measures on the symmetric group
and beyond (2026). None of their indexed descriptions supplies a better
binary relevant-variable constant. The separate Wellens/NS metadata
requests returned non-JSON errors; retained as failed coverage. An
experimental guessed-ID NS citing request is not trusted or used.

## Citation-index fallback completed, 01:43 UTC

Correct OpenAlex IDs were recovered by title search: NS journal W1969865855
(and conference W2023834316), Wellens arXiv W3023068186. The journal-NS feed
returns 23 indexed citing works since 2024, CHS five, and Wellens one;
complete JSON and titles are retained. Relevant additions to inspect are
Maitra et al., Interplay between resiliency and polynomial degree — Recursive
amplification, higher order sensitivity and beyond (DAM 2025,
https://doi.org/10.1016/j.dam.2025.01.003), Sparse juntas on the biased
hypercube (TheoretiCS 2024), and Sensitivity and Hamming Graphs (2026).
Other indexed items concern quantum/approximate/symmetric-function measures,
surveys, and unrelated false matches; the feed is not treated as infallible.
This fills part of the initial rate-limited citation coverage, without a
claim of exhaustiveness. The earlier guessed-ID request remains unused.

The live OpenAI recursive tree is truncated (55,173 returned entries), so
its tree alone is incomplete coverage. The current CONTENTS.md was also
fetched and searched for C44, Wellens, relevant variables and CHS, with no
applicable stronger entry found. The plasma-ai tree is not truncated.
Primary full text of Maitra et al. (2025) was checked through its author-hosted
PDF; its amplification/sensitivity and Maiorana–McFarland results do not
supply a better relevant-variable constant here. Dinur–Filmus–Harsha's
2024 publication concerns approximate low degree under biased measure;
Asensio et al. 2505.08951 concerns m-ary sensitivity. Neither is an input
for a stronger binary C44 value in this job.

## Live re-check, 02:32–02:35 UTC, 3 November 2026

The official raw table still lists 4.3576549226*; PR294's directly fetched
diff and the current rpinho/math-certificates README list 2.0417086280*.
All 47 open PR diffs and the complete paginated open-issue feed were
refetched. Only #285 and #294 change 44a.md; #283's sensitivity result is
an adjacent topic, not a C44 improvement. The initial audit's prose count
of 48 was corrected to the actual 47 in its retained feed.

Twelve result repositories were refreshed through current commit IDs and
READMEs, plus OpenAI's complete current contents index and Épi's Wellens
result JSON. Épi remains at 4.3654674227. Recently-updated GitHub searches
were repeated for relevant variables/Boolean/2026, C44, Wellens, the input
constant and awesome lists. No applicable public result stronger than the
input 2.0417086280 candidate was located in this bounded coverage. The
refresh had zero fetch errors. Receipts: sources/public_final.json.gz,
sources/public_final_summary.json and receipts/public_refresh.log.
X remains unavailable. No novelty, priority or public-record claim is made.

## Final checkpoint public refresh, 03:40–03:42 UTC

The official raw source, all 47 open PR diffs and the 53-entry complete
open-issue feed were refreshed again. Only #285 and #294 change 44a.md;
PR294 still supplies the input 2.0417086280 candidate. The twelve result
repository heads/READMEs, OpenAI contents index, Epi result JSON and recent-
update repository searches were checked again, with zero fetch errors.
No stronger applicable input was identified in this bounded coverage.
The prior 02:32 data remain in public_0232.json.gz; the latest data are
in public_final.json.gz and public_final_summary.json. X is unavailable.
There is no novelty or priority claim.
