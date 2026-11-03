# Round 10 prior-art audit — candidate, unrefereed

Started 2026-11-03 04:03 UTC; this is the first job file, before code.
Baseline: round 9's unrefereed R6<=107, R5<=50, giving C44<2.0209645587;
lower bound 3/2. Its REPORT.md and frozen/PROOF.md have been read. Its
frozen files will not be modified. Round 8's REPORT.md has also been read;
its proof, verifiers and rounds 4–7 remain inputs to inspect.

Deadline: eight hours from start, 12:02 UTC on 3 November; retrieve before
13:00 UTC. Pod math-cpu-11, only /root/os/math_c44r10_1103, at most fourteen
workers, nice 10, single-threaded BLAS. Other jobs and pod lifetime are
untouched. The user explicitly authorizes pod transfers despite the generic
local-only rule. No commits, pushes, PRs, public posts or messages.

Live sources to refresh before mathematical code:
- Official https://teorth.github.io/optimizationproblems/constants/44a.html
- Raw https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/44a.md
- All open PRs/issues in https://github.com/teorth/optimizationproblems;
  particularly https://github.com/teorth/optimizationproblems/pull/294 .
- GitHub repository search sorted by updated, for relevant variables, C44,
  Boolean degree 2026 and Wellens, including awesome lists.
- Required AI repositories: BakeLab/Epi-results, google-deepmind/alphaevolve_results,
  google-deepmind/alphaevolve_repository_of_problems, openai/math,
  EinsteinArena, plasma-ai/erdos, kisonecat/openai-math, and related results.
- Nisan–Szegedy, CHS arXiv:1801.08564, Wellens arXiv:1903.08214 and
  2005.00566; arXiv last twelve months and citations since 2024.
- Public indexed Reddit/blog/community summaries. X is unavailable.

Best inherited method: CHS/Wellens weighted restrictions plus integer
partial-energy gaps, low-weight ternary support classifications and round
9's signed affine-flat completion. Current public-table status and stronger
public alternatives are UNCHECKED pending this job's refresh. Round 9's
bounded audit found the official 4.3576549226* and PR294 2.0417086280* at
03:42 UTC today; that is an input, not this job's live check.

No novelty or priority claim. Any new bound requires an explicit proof,
two separately written exact verifiers on frozen data and rejection controls.
Published catalogue/lattice/classification premises remain explicit.

## Initial live audit, 04:03–04:06 UTC, 3 November 2026

Both live official HTML and raw Markdown list 4.3576549226* (Pinho), with
published Wellens 4.394. All 47 open PR diffs and the complete 53-entry
issue feed were refreshed. Only #285 and #294 change constants/44a.md;
#294 still supplies 2.0417086280*, while #283 concerns sensitivity.
Bodies and comments of the C44 threads were read. Recent-update GitHub
searches and twelve requested/related result repositories were refreshed,
including OpenAI's contents index and Epi's Wellens result JSON. No stronger
applicable public result was identified in these bounded checks. The
local round-9 2.0209645587 candidate is therefore the controlling baseline.
Receipts: sources/public_final.json.gz and public_final_summary.json.
Zero errors in that refresh; global code search/private communities remain
outside coverage. No novelty or public-record claim.

Primary arXiv pages NS/CHS/Wellens and citing-paper searches were consulted.
The since-2024 literature includes Krotov–Valyuzhenich's perfect colorings,
Potapov's degree comparisons, and Valyuzhenich arXiv:2609.12540 (q>=3,
not a better binary constant). Current indexed searches for the last twelve
months and public Reddit/blog summaries found no stronger binary bound.
Citation feed and arXiv query receipts are retained where available;
an initial curl bracket-expansion error was corrected with curl -g.
X is unavailable. This is bounded coverage, not an exhaustive literature
or citation classification. Methods and external dependencies are credited
in the inherited proof and will be explicit in the new proof.

Baseline replay will run on a job-owned hash-matched copy of round 9's
frozen packet, in baseline/frozen, before acceptance of a new claim.

At 04:09 UTC, live OpenAlex feeds returned 23 NS, five CHS and one Wellens
citing works since 2024. Their complete metadata and titles are retained
in sources/*_citing_since2024.json and citing_summary.json; no stronger
applicable binary result was identified. Index false positives and dates
are not taken as theorem statements. The primary Masuda–Panov Lemma 4.7,
https://arxiv.org/html/math/0607094v2, was read directly: connected dimension
at least two and cross-complex vertex links imply a cross-complex. Its
hypotheses match the new near-equality argument. Valyuzhenich's primary
https://arxiv.org/html/2303.10995 was also consulted directly.

Open-diff coverage correction: the broad C44 matches in other PRs are
unchanged README/table context (not only hexadecimal coincidences). All
47 diffs were retained and those matched lines were examined directly;
only #285/#294 change the C44 constant/citation, and #283 cites adjacent
Wellens sensitivity work. No open C44 issue thread was found besides the
PRs in the complete open-issue feed. This clarifies the initial audit's
coverage rather than treating a path-only check as exhaustive.

## Resume literature cross-check, 05:24 UTC

Read the primary arXiv HTML of Potapov, *On the number of relevant variables
for discrete functions*, https://arxiv.org/html/2410.21937v1 . Its introduction
still uses Wellens 4.394 for the binary case; its new bounds concern
additional degree parameters and multivalued domains. It supplies no
stronger binary constant applicable here.

Read the authors' published PDF of Maitra–Mukherjee–Stănică–Tang,
*Interplay between resiliency and polynomial degree*, Discrete Applied
Mathematics 365 (2025), 138–159:
https://faculty.nps.edu/pstanica/research/2025DAM_InterplayResiliencyDegree.pdf .
The work studies sensitivity, resiliency and Maiorana–McFarland selector
constructions (especially section 5), rather than a new asymptotic C44
constant. No construction beating 1.5 was identified there. The distinction
between full sensitivity and total relevant-variable count matters here.
This is a primary-source check, not a classification of all consequences.

## Barnes–Wall followup, 05:59 UTC

Located and read the primary https://arxiv.org/html/2610.15288v1,
Cao–Hu–Huang–Yang, *The Norm Spectrum of Barnes–Wall Lattices Below Twice
the Minimum* (11 October 2026). It classifies norms in that interval and
constructs examples as sums of two minimum vectors. It does not state
that every short vector is such a sum, or that the summands preserve real
polynomial degree. Its spectrum alone does not improve the ternary
below-two list already used here. No new C44 cap is inferred from it.
The possible two-minimum decomposition route is therefore unproved and
is excluded from the accepted recurrence. This adds a recent relevant
lattice reference missed by the earlier problem-name-only search.

## Final full public audit, started 06:17 UTC, 3 November 2026

Refreshed the official HTML/raw source, all 47 open PR diffs and all 53
open issue-feed entries. Added searches in open-thread comments for C44,
44a, Wellens, CHS/NS names and the current decimal candidates; fetched
all pages of comments in the matched threads. Only #294/#285 alter the
44a source; #283 concerns adjacent sensitivity work. No other open C44
issue was identified. Official raw source remains 4.3576549226*, while
PR294 remains 2.0417086280*. The twelve AI-lab/related result repositories,
recent-update searches (including 2.0209645587 and 2.0111998311), OpenAI's
contents index and Epi's Wellens result were refreshed without fetch errors.
No stronger applicable public result was identified in this bounded audit.

The rpinho/math-certificates head changed since the initial audit. The
complete public compare shows one C89 commit, 71 files and no C44 path
changes; the C44 README still states 2.0417086280. The compare receipt is
sources/math_certificates_head_delta.json.gz. Full final feeds, diffs,
comments, repository metadata/readmes and queries are in
sources/public_final.json.gz and its summary. This job made no commits
or external posts. X remains unavailable. Final targeted head/table/PR
checks are recorded separately if run at closeout.
