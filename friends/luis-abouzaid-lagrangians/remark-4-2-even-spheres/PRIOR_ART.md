# Independent referee prior-art gate — 2026-11-02

Opened before scientific code. This is a verification task, not a record search.

Primary baseline: Abouzaid–Diogo, https://arxiv.org/html/2011.13478v2,
Proposition 4.1 and Remark 4.2. The public paper distinguishes split-generation
in the monotone category from generation in the exact category. It has no
numerical cone benchmark. The author list includes Luís Diogo. The journal
record is https://doi.org/10.1016/j.aim.2023.109114.

Independent initial searches: exact paper title with generation, and Novikov
graded projective generation sphere. No directly applicable newer solution
identified; this is not evidence of priority. Search coverage will be expanded
to public code, open trackers, AI-result catalogs, recent papers and community
before constructing tests. There is no identified problem-specific scoreboard
or software repository; the paper is the relevant published baseline.

Classical inputs under review: Farber–Schütz, https://arxiv.org/pdf/0807.3240,
Lemma 1; Endo, https://www.jstage.jst.go.jp/article/jmath1948/15/3/15_3_339/_pdf,
p.339 (credits Seshadri's one-variable theorem). These are prior algebra,
not contributions of this packet. Tests will reproduce literal polynomial
and parity algebra independently; they cannot reproduce geometric Floer counts.

The submitted proof and common L063 proof have been read as arguments only.
No submitted search, producer or verifier code will be imported or executed.

## Completed coverage and limits

Public GitHub repository searches on the pod used `sort=updated&order=desc`:
`"Monotone Lagrangians"` returned zero; `Novikov generation` returned one
unrelated GPIO repository; `cotangent Fukaya 2026` and `awesome symplectic`
returned zero. No target repository or target issue/PR queue was identified.
GitHub repository metadata calls hit the shared IP's unauthenticated rate limit.

Independently opened these public catalogs through the web reader:

- https://github.com/BakeLab/Epi-results
- https://github.com/google-deepmind/alphaevolve_results
- https://github.com/google-deepmind/alphaevolve_repository_of_problems
- https://github.com/openai/math (also its overview.tex)
- https://github.com/vinid/einstein-arena
- https://github.com/plasma-ai/erdos
- https://github.com/kisonecat/openai-math

No applicable solution was identified in these bounded catalog inspections.
This was not an exhaustive full-text audit. AlphaEvolve result issues and PRs
were opened; Epi issue/PR pages failed in the web reader. Public catalog roots
were rechecked near completion. No mathematical priority claim is made.

The pod's arXiv API query specified 2025-11-02 through 2026-11-02, cotangent
AND generation, newest first, capped at 30 entries. It was broad and returned
mostly unrelated work, so it does not cover the whole year's literature.
Additional targeted web queries for cotangent/monotone/generation in 2025–26,
the paper's exact title, ordinary generation, Novikov graded projectives and
Seshadri found no applicable resolution. Exact-title X/Reddit/blog queries
added no relevant result. No account was created or person contacted.

The primary journal PDF independently confirms the relevant p.21 statement.
Original Seshadri scans pp.456–458 were read, including the theorem on p.457
and its proof; they expressly cover a principal ideal domain, not just a field.
Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC335443/ . Local scans retained.
The initial pod source collector accidentally used a different PMC identifier;
that receipt is excluded. sources.py now has the corrected identifier, but the
corrected collector was not rerun. A follow-up collector failed to launch
because the pod ran out of disk space; its intended reads are not claimed.

The strongest relevant published baseline remains the paper's split-generation
statement. The additional step submitted here is its replacement by ordinary
generation for even spheres over K_Z, using classical PID/projective-freeness
and a parity argument. The original geometric Floer counts were not recomputed.
