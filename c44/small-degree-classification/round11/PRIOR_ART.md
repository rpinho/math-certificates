# Round 11 prior-art audit — candidate, unrefereed

Started 2026-11-03 06:37 UTC. This is the first written job file, before code.
Rules read: ../../_codex/RULES.md. Round 10 REPORT.md and its frozen proofs,
round 9 REPORT.md, and round 8 REPORT.md read first. Frozen earlier rounds
will remain unchanged. Latest local candidate: R5<=50, R6<=107, R7<=229,
C44<2.0111998311; known lower bound 3/2. These are unrefereed candidates.
No novelty, priority, or record claim is made.

Required live audit (in progress, to finish before mathematical code):
- https://teorth.github.io/optimizationproblems/constants/44a.html
- https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/44a.md
- ALL open PR files/diffs and all open issues in teorth/optimizationproblems,
  with bodies/comments for C44 matches, using ~/dev/.bin/gh read-only.
- GitHub repository searches sorted updated descending: C44, Boolean degree,
  Nisan Szegedy, Chiarelli Hatami Saks, Wellens, and 2026.
- arXiv: NS, CHS, Wellens; last twelve months and citing papers since 2024.
- BakeLab/Epi-results; google-deepmind/alphaevolve_results and
  google-deepmind/repository_of_problems; openai/math; EinsteinArena;
  plasma-ai/erdos; kisonecat/openai-math; related repositories found.
- Public Reddit/blog/community searches. X is unavailable. Private Discord
  and Telegram and exhaustive global authenticated code search unavailable.

Best public baseline and reproduction status will be recorded after the
live retrievals. Round 10 methods credit weighted restrictions (CHS/Wellens),
minimum-support classification, Barnes–Wall gap, low-weight Reed–Muller,
Rasoolzadeh cubic catalogue, and rounds 4–9.

Limits: six hours (finish by 12:37 UTC), retrieve by 13:00 UTC. Heavy compute
only math-cpu-11:/root/os/math_c44r11_1103; <=14 workers; nice 10;
single-threaded BLAS. Pod transfers explicitly authorized by the user.
No commits, pushes, PRs, posts or messages. Do not touch other jobs.

## Initial live results (completed 06:40 UTC)

The direct HTML/raw table still gives published Wellens 4.394 and Épi's
unrefereed 4.3576549226*. The stronger public candidate is PR294's
2.0417086280* (Ricardo Pinho; retained round-eight machinery). The local
round-ten candidate 2.0111998311 is our baseline to reproduce; no stronger
applicable result was found in the bounded public check.

sources/public_final.json.gz records all 47 open PR diffs and all 53 open
issue-feed entries, repository metadata/heads/READMEs, sorted-update GitHub
searches and Épi's Wellens result. Only PR294 and PR285 modify constants/44a.md;
thread 283 concerns degree-four sensitivity and was also read. The supplement
contains comments for all three, additional updated-descending searches,
recursive trees of all twelve named result repositories, primary arXiv pages,
raw table and live HTML. Épi's exact weighted-restriction certificate remains
the best named lab result; local rounds improve that restriction framework.
Tree-name searches are bounded coverage, not exhaustive semantic code search.

Primary references checked: NS1994 DOI 10.1007/BF01263419 (the direct IAS
PDF returned HTTP403; inherited source/proof and DOI/table bibliography used),
CHS arXiv:1801.08564, Wellens arXiv:1903.08214 and 2005.00566. The latter's
journal issue has an upstream correction PR285, irrelevant to its bound.
Recent arXiv API sorted by last update was saved as sources/arxiv_recent.xml;
web searches explicitly covered the last twelve months and citing work since
2024. Potapov 2410.21937 concerns two-/three-valued discrete functions;
Valyuzhenich 2404.10418 and 2609.12540 concern q>=3 Hamming alphabets;
neither supplies an improved q=2 constant. The 2025 slice-distance paper and
2026 symmetric-group complexity work concern other domains. OpenAlex's CHS
since-2024 citation query returned five papers (sources/citing_summary.json);
NS and Wellens citation queries were rate-limited (HTTP429), including a retry.
These failures are coverage limits, not negative evidence. Prior rounds'
retained citation snapshots remain available. The 2026 Barnes–Wall spectrum
paper 2610.15288 is retained from round ten; no unproved universal decomposition
from it is assumed. Public blog/Reddit indexed searches found no applicable
improvement; Ihringer's 2021 construction writeup is consistent with CHS.
X is unavailable. No private community coverage or priority claim.

## Ranked routes before mathematical code

1. Reproduce round ten, then strengthen its near-equality deficit argument
   by classifying the case of at most one nonminimum partial. Test R8 first.
2. Complete the quartic 22-variable top-energy envelope for R5, using
   restartable shards rather than increasing root-case timeouts again.
3. Try direct low-degree control exclusions if the first argument exposes
   additional finite obstructions for R7 or R6.
4. Lower side: search jointly for signed polynomial/routing constructions
   outside the already tried disjoint-cubic, parity-map, selector-fusion and
   gate-cover banks. Exact certification only after a concrete seed.

No numerical result from an exploratory search is accepted without a full
written proof and two separately written exact frozen verifiers plus
rejection controls. All results remain candidate and unrefereed.

## Full refresh at07:55UTC

All47 open PR diffs,53 issue-feed entries, sorted-update searches and all
12 repository metadata/HEAD/README sources were read again with zero fetch
errors. Raw44a is byte-identical to the initial fetch; all12 repository
heads are unchanged. sources/public_initial.json.gz preserves the initial
snapshot, sources/public_final.json.gz the fresh one. The fresh snapshot
also includes live HTML. The end-of-job head/feed check will detect any
subsequent changes before closeout. No public novelty claim is made.

## Final source recheck — 2026-11-03 09:01:59 UTC

`jobs/final_source_heads.py` rechecked the live44a raw source and HTML,
the full open PR/issue feeds, the relevant PR diffs294/285/283, and HEADs
of all twelve result repositories against the complete07:55UTC refresh.
All were unchanged:47 open PRs,53 issue-feed entries, no changed PRs or
issues, no changed result repositories. Snapshot:
`sources/last_source_heads.json.gz`; summary:
`sources/last_source_heads_summary.json`. The official table remains
4.3576549226*, the published Wellens number is4.394, and PR294's candidate
is2.0417086280*. No stronger applicable public result appeared in this
bounded check. This does not establish novelty or priority. X remains
unavailable; the previously recorded literature-access limits still apply.
