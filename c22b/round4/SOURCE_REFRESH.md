# Public-source refresh — 8 November 2026

Refreshed at 2026-11-08T12:28:29.601626+00:00. This is a bounded source review for packaging an
existing candidate, not a new construction search or an exhaustive priority claim.

## Tao page and all open PRs

The [live page](https://teorth.github.io/optimizationproblems/constants/22b.html)
and raw constants/22b.md from the public GitHub contents API still list
Li / Claude Opus 5.5's 7.2012719* and Kim–Oh–Huh's 7.31.
The definition uses ropelength over crossing number for alternating knots
(and links), with thickness measured as a radius.

The public [open-PR list](https://api.github.com/repos/teorth/optimizationproblems/pulls?state=open&per_page=100)
returned **78 open PRs**, so a second page was not needed. Every title and
body was screened. All 78 public head refs were fetched and each full
changed-file list was computed from its merge base with its recorded base
to its head. **Only #324 and #342 touch constants/22b.md.** Their complete
C22b/README diffs and bodies were read. The list was refreshed after drafting;
all 78 head/base pairs were unchanged. The final live page and raw source
were also reread. Open 22b issue search returned zero.

- [#324](https://github.com/teorth/optimizationproblems/pull/324), Ricardo Pinho:
  7.090412*, head 9d480a39c47bed8ad17b0b715ceb1605648ee345.
- [#342](https://github.com/teorth/optimizationproblems/pull/342),
  Doldrums / SCiEL / CPIL lab MBZUAI: 7.087662112*, underlying advertised
  coefficient 7.08766211189. Head
  a1d496f0958bd06ad9e0dd25436390397146c9cd, branch 22b-sciel in
  SCiEL-RSI-CPIL/optimizationproblems. That branch was fetched directly
  and matches the upstream PR-head ref. Its PR states it is stacked on
  #324. The new diff is against this head, preserving both rows.

The correct printed-number improvement is exactly
7.087662112 - 7.087559024 = **0.000103088**.
An earlier unpublished 7.087580303 construction was the replayed starting
point; no link to it is used.

## Public code and agent inventories

An updated-sorted public repository query for ropelength, C22b and the
comparison decimals returned 52 matches; the first 30 were read as search
metadata. Most C22b matches are unrelated identifiers. Four relevant recent
README files were read: ArseniyVarlamov/ropelength-crossing-number
(a universal three-quarter-power lower bound),
andrewaschoen/ropelength-lower-bound (a universal nontrivial-knot lower bound),
Njakasoa/tight-knots-ropelength (a T(M,M) three-quarter-power upper-bound
family), and vibemathing/problem-wikipedia-f67a492dfaf70102 (general
research instructions). None of those READMEs supplied a stronger C22b
upper-bound candidate. Their full code or papers were not audited.

A topic repository search across BakeLab, google-deepmind, openai,
EinsteinArena, plasma-ai and kisonecat returned zero. README reads succeeded
for BakeLab/Epi-results, google-deepmind/alphaevolve_results, openai/math,
plasma-ai/erdos and kisonecat/openai-math; none mentioned C22b, ropelength
or superhelix. The separate google-deepmind/repository_of_problems and
EinsteinArena/EinsteinArena README endpoints returned Not Found, so those
were not successful inventory reads. This scope is not a full repository
code search. The producer's earlier inventories likewise reported no
stronger candidate, with explicit access limits.

## Papers and community

The primary abstracts of [Klotz, arXiv:2603.02416](https://arxiv.org/abs/2603.02416)
and [Klotz, arXiv:2504.00861](https://arxiv.org/abs/2504.00861) were reread.
They concern T(Q,Q) links and concentric helices/non-alternating torus knots;
no stronger alternating-constant candidate was identified from them.
The latter is older than the last twelve months and is retained as an
inherited primary reference. Indexed searches for ropelength/alternating
upper bounds in 2026 surfaced no stronger candidate. Other surfaced items
concerned ribbonlength, filtered knot spaces or the three-quarter-power
constant, rather than this C22b bound. Indexed C22b/ropelength queries on
X and Reddit returned no relevant result; no public Discord or Telegram
source was located. Search coverage is limited and this is not a claim
of absence from the literature or community.

## Reproduction and limits

The producer could not retrieve the exact #342 construction from
[Zenodo 24038188](https://zenodo.org/records/24038188): its earlier API
response reported restricted access and no files, with direct file reads
failing. That baseline is not represented as locally replayed or refuted.
The available, stronger unpublished 7.087580303 construction was replayed
before optimization, and its saved result is included. The present release
replays the selected 7.087559024 construction and the AI referee's own
checks. No claim of optimality follows.

All GitHub API reads used curl to api.github.com; repository reads used
public git fetch. Local snapshots of the two list responses, 78 changed-file
lists and commit pairs, #324/#342 bodies and diffs, page/raw reads, searches
and README responses are retained with the release preparation materials.
The publication package contains this summary rather than duplicating
all those snapshots. See [PRIOR_ART.md](PRIOR_ART.md) for method credits.
