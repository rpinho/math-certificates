# Prior art — math_newtargets2_1103

Started 2026-11-03 01:38 UTC. This file precedes new search code.
The predecessor's SURVEY.md, PRIOR_ART.md, ATTEMPTS.md, PROOF_C57C.md,
NEEDS_POD.md, REPORT.md and frozen proof/checker/receipts have been read.
Its frozen packet is read-only and will remain unchanged.

## Starting sources and credited baselines

- Official live table and raw source: https://teorth.github.io/optimizationproblems/
  and https://github.com/teorth/optimizationproblems. Refresh of target pages,
  open PRs and issues is in progress using the supplied gh executable.
- C57c: Frank Wikström, https://arxiv.org/abs/2610.34580v1,
  supplementary data https://doi.org/10.5281/zenodo.23650159.
  Public lower 0.612242 and upper 0.6562681 reproduced by predecessor.
  Predecessor candidate, unrefereed lower 0.61229 uses the full complex
  2x2 Grunsky form after Wikström's bounded-image transform and his center.
  Its exact frozen artifact has SHA256
  a35e5fdb94fdfb4bc56d817a6a794b52295b2b8d1aa602f8dcc2eb4b514a9d05.
  This job's improvement threshold is at least 0.61230.
- C5b: public upper 5/9, anonymous reader submission
  https://www.erdosproblemaday.com/submission/7bkzb8 and Patrick White–Claude
  packet https://github.com/pw/erdosproblemaday-verification/tree/main/757/reader-5-9.
  Ma–Tang https://arxiv.org/abs/2602.23282 supplies the finite-to-asymptotic
  reduction and public lower 9/17. The desired improvement is a smaller
  upper ratio; n=20,h<=11 would give 11/20. The task's word "above" is
  interpreted as improving the bound, since a numerically larger upper
  ratio would be weaker.
- C31b: pending https://github.com/teorth/optimizationproblems/pull/272,
  Leandre Jack lower 0.617356 and upper 0.679701. Source
  https://github.com/leandrejack-afk/chvatal-sankoff-bound,
  upper kary at f5f250f, lower at bb3b815. Full live refresh pending.
- C22b: Youhua Li–Claude upper 7.2012719, limiting helix cost
  7.2012609899..., https://github.com/YouhuaLi/tight-alternating-knot-constant.
  Prior unsuccessful methods: aligned ellipses and square weaves, and the
  public author's Fourier/period-doubling screens. Distinct methods required.

## Audit scope

The predecessor's public code, AI/agent repository, recent arXiv and
community audit is retained as read-only prior evidence; this job will
refresh sources relevant to every attempted target and before any claim.
Required repositories: BakeLab/Epi-results; google-deepmind/alphaevolve_results;
google-deepmind/alphaevolve_repository_of_problems; openai/math;
EinsteinArena-related repositories; plasma-ai/erdos; kisonecat/openai-math.
Public searches should be ordered by update time. X is unavailable and will
not be represented as checked. No messages or publication are authorized.

All prospective results are candidate and unrefereed. No novelty judgment.
The separately implemented checker and explicit analytic proof must both be
present before a finite artifact supports a claim.

## Initial live refresh (01:41 UTC)

`sources/initial_audit.json` records fresh HEADs for all named repositories,
the actual DeepMind problem repository and the awesome list. Target source
HEADs match the predecessor; OpenAI/math HEAD is 4eaee875 (30 October).
All open PR file lists were inspected: only #272 touches the four target
pages; no page PR for C57c, C5b or C22b. Live raw pages and README saved.
Public repository searches sorted by updated are saved in sources/.

Fresh web searches locate Wikström v1 (25 October), unchanged Zenodo 1.0.0,
the reader's 5/9 construction, and an additional relevant C5b source:
https://einsteinarena.com/problems/sidon-45-set/threads/282
by SuperDuperAI-Salavatov, 20 October. It reports exhaustive exclusion of
n=16,h=9 and classifies n=14,h=8 into nine realizable AP-hypergraph types.
It explains the row-space realization criterion: choose distinct middle
vertices; no collision, unintended AP or disjoint-pair-sum relation may
belong to the span of the intended AP equations. Its n=18 case is explicitly
open. This is a public computational claim, not replayed certification.
Our second C5b method will build on that exact incidence criterion rather
than repeat a coordinate-only search. The n=20 pod search remains required.

For C31b, full public kary and lower READMEs and transition/iteration sources
were downloaded and read. Current h=6 upper table has 8,502,177 states and
27,720,529,578 accepted transitions (169 GB uncompressed records). The
headline lower witness has 1,431,743,147 classes (5.7 GB raw). Source logs
are evidence of the authors' computation, not a full local replay. The
replay/attack will distinguish exact arithmetic of the reported parameters,
small-state reproduction, and any complete headline artifact check.

The initial web searches returned no additional indexed applicable C31b or
C22b improvement. This is a search limitation and no novelty assessment.
X remains unavailable.

## Primary-paper finite bound re-read (03 Nov, 05:20 UTC)

Re-opened Ma–Tang v2, https://arxiv.org/pdf/2602.23282 (6 March 2026),
Section 5.2. Theorem 5.3 states 17*tau(H)<=5n+3m for linear F7-free
3-graphs, and Lemmas 2.4/5.2 give m<=n-2 and F7-free for (4,5) sets.
**Inference used in the new finite gluing screen:**
alpha=n-tau>=ceil((9n+6)/17). In particular an n=20,h<=11 or n=22,h<=12
candidate must saturate m=n-2. This pruning is a derivation from the cited
primary statements; the paper itself drops the additive term when stating
its asymptotic 9/17 lower bound. Its Theorem 1.5 also states the
finite-to-asymptotic infimum characterization. Our explicit separated-copy
proof is written in PROOF_C5B_FINITE_REDUCTION.md.

## Live sources 1–3 refreshed (03 Nov, 06:15 UTC)

Read the live HTML table and raw target pages again; read all open PR file
lists with pagination, PR #272 and its complete C31b page. Only #272 touches
these targets. The live main HEAD and all 13 audited public repository HEADs
are unchanged from the initial audit. Repository READMEs were fetched again;
no additional target result was found. Saved in `sources/refresh_0615/` with
empty audit error list. Target issue searches also saved. X unavailable.

C31b comparison uses Jack's underlying exact lower r=59928872/134217728,
which yields gamma=0.617356904524725130..., rather than merely the page's
six-decimal 0.617356. The public upper source gives 0.679700467578359;
our prospective replay upper 0.6797005 would reproduce the displayed page
but would not improve that more precise public source. Our lower producer
has proposed r=479430980/1073741824; complete independent checking and
procedural replay are pending. No improvement claim is made at this stage.

## C31b exact comparison after the complete check (06:53 UTC)

The separately written literal-operator checker passed all 1,431,743,147
classes of the frozen h=9 potential (receipt in frozen/c31_lower_h9/).
Its conservative r=479430980/2^30 is above the public exact
r0=59928872/2^27=479430976/2^30 by 4/2^30. Since
2r/(1+r)-2r0/(1+r0)=2(r-r0)/[(1+r)(1+r0)]>0, this is a candidate,
unrefereed lower bound gamma>=239715490/388293201>.617356908085.
No novelty judgment. PR #272 was re-read at 06:49 and remains open with
updated_at 26 October; the 06:15 full live-table/repository audit applies.
A complete procedural decode/hash replay is running before the final
small-packet report. A fail-closed checker revision will also be replayed
in full, without altering the first frozen packet or its historical receipt.

## Resume live-source refresh (07:32 UTC)

Re-read the live table HTML, raw C57c/C5b/C22b pages, all open PR file lists,
and PR #272's complete C31b page, using the supplied gh executable. All 13
audited repository HEADs are unchanged; only #272 touches these four target
pages. Complete fresh receipts: sources/refresh_0731/, no audit errors.
The exact C31b source comparison above remains the comparison used here.
X is unavailable. No novelty judgment, and incomplete C57c covers support
no improvement claim.

## C31b complete upper baseline and decoded lower artifact (08:10 UTC)

The exact upper replay completed every one of 8,502,177 states and
27,720,529,578 accepted transitions. Certified upper .6797005 is retained
as a baseline replay, not an improvement over the public source's underlying
.679700467578359. A diagnostic using the exact maximum row ratio would give
about .67970047139, still weaker than that source; no upper gain is claimed.

The lower procedural decoder completed and matched all prescribed hashes.
The original full direct-sum check reported minimum drift numerator
7,670,895,684 over 17,179,869,184. The tightened packet uses this exact r,
giving gamma>=3835447842/6212691217, prospective gain
570425344/150771609578801525>0 over the public exact source. The hardened
checker is performing a full replay before the final qualification is set.
No novelty judgment; this is a fixed-point refinement of Jack's operator.

## Hardened C31b receipt and fresh comparison (08:39 UTC)

The complete hardened exact checker passed all 1,431,743,147 classes for
r=1917723921/4294967296, minimum numerator 7,670,895,684 over 2^34.
The full h=5..9 procedural decode and every hash also passed. Therefore
candidate, unrefereed gamma_4>=3835447842/6212691217>.617356908308.
The exact gain over the public source is
570425344/150771609578801525>0, approximately 3.78e-9. This is a
fixed-point refinement of Jack/Lueker, with no novelty judgment.

Before this comparison, the live table HTML, raw target pages, all open PR
file lists, PR #272's complete proposed page, and all 13 audited repository
HEADs/READMEs were re-read. `sources/refresh_0837/` records no changed HEADs
and no audit errors; only #272 touches these targets. X remains unavailable.
The underlying exact public value remains the comparison, not its printed
six-decimal page ceiling/floor. Verification and value controls are in
frozen/c31_lower_h9_tight/; final complete output hashes match that packet.

## Read-only refresh, 2026-11-03 09:55 UTC

Live table, target pages, every open PR file list, issue searches and the 13 audited repository HEADs re-read in sources/refresh_0955/. No audit errors and no changes to the compared repository HEADs. Only open PR #272 touches these targets. Its four-letter lower display remains .617356; the underlying exact public value used in the comparison is 14982218/24268325. C31b candidate/unrefereed packet is sealed with the full check and decoder receipts. No novelty judgment. X unavailable.

## Pre-claim live-source refresh, 2026-11-03 11:00 UTC

sources/refresh_1100/ re-reads the live table, raw target pages, all open PR
file lists, PR#272's complete C31b page, issue searches and all13 audited
repository HEADs/READMEs. Empty audit error list; no HEAD changes relative
to09:55. Only#272 touches the four targets. Wikstrom's C57c comparison
remains .612242 and the reader C5b upper5/9; C31b comparison still uses
Jack's exact underlying14982218/24268325, and C22b upper7.2012719.
C57c arithmetic is not yet complete at this refresh; no .61230 claim made.
X unavailable, no novelty judgment. A final end-of-job refresh remains due.

## End-of-job source refresh, 2026-11-03T11:32:50.836954+00:00

sources/refresh_1132/ re-read the live HTML table, raw target pages, every open PR file list, PR#272, target issue searches and all13 audited repository HEADs/READMEs. No errors or changed HEADs since11:00. Only#272 touches these targets. The exact underlying C31b comparison and C57c/C5b/C22b values remain unchanged. Candidate and unrefereed; no novelty judgment. X unavailable.
