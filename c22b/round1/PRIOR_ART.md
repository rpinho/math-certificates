# Prior art — math_c22b_1104

Started 2026-11-04 02:23 UTC. Candidate and unrefereed; no novelty judgment.
This document is being written before any search/model/construction code.

## Frozen starting scope

Read first: the machine-wide open-science RULES.md; sweep section
C22b in ../target_sweep_1103/astra/SWEEP.md and companion sweep.json;
../newtargets2_1103/REPORT.md, ATTEMPTS.md, C22B_CIRCLE_OBSTRUCTION.md;
../newtargets_1103/SURVEY.md and the local math-certificates README.
The circle obstruction applies to full circles with a common center axis,
including periodic unequal radii. Cutting/reconnecting arcs is outside it.
Lemniscate braid numerical cost 11.01218848 failed in the predecessor;
ellipse/Fourier and square weave attempts also failed. We must try both
sweep methods, rather than repeat those methods unchanged.

## Live table, first re-opening

https://teorth.github.io/optimizationproblems/constants/22b.html was opened
live on 2026-11-04. It lists Youhua Li / Claude Opus 5.5, unequal coaxial
double helices, 7.2012719*; underlying limiting cost 7.2012609899... .
The claim is explicitly unverified. Parameters a1=1.934060, a2=.075486,
b=.322721; stated finite family odd n>=59, L<=7.2012719 n+19.649.
The established displayed upper is 7.31, Kim–Oh–Huh (2024). The public
source reports that its inner curvature constraint was violated; that
critique will be checked against the source rather than adopted blindly.

Pinned source: https://github.com/YouhuaLi/tight-alternating-knot-constant/tree/debf7c92f93bae64486e6302e565a2d3b1290f9c .
Credit Youhua Li, Claude, Kim Hyoungjun, Oh Seungsang, Huh Youngsik,
Olsen Kasper W., Bohr Jakob, Klotz Alexander R., Maldonado Matthew,
Diao Yuanan, and Cantarella–Kusner–Sullivan where their results are used.

External retrieval and baseline reproduction are in progress. No new
construction search is authorized by this document until BAR.json records
the live source checks and the baseline reproduction status. Next: fetch
raw table, all open PR file lists through ~/dev/.bin/gh, public code and
lab inventories, papers and community checks; reproduce the public checker.

The requested target is <=36/5, beating the underlying helix limit as well
as the displayed bound. By eight elapsed hours require a topology-valid
numerical family below 7.199 with robust thickness margin; if absent,
stop refinement and finish the negative findings and final source checks.

## Completed first audit and baseline, 2026-11-04 02:27 UTC

All 57 open PRs were re-opened through ~/dev/.bin/gh, including their file
lists. No PR changes constants/22b.md. PRs #303 and #291 contain unchanged
22b table context; #196 contains the already-public historical announcement,
not a new claim. The initial broad substring flag is corrected explicitly in
sources/pr_scope_correction.json. Page and raw source are saved. Main HEAD
87b4ebbd426ff8db597a2004cc45da17903bdcf2, Li HEAD and pinned source both
debf7c92f93bae64486e6302e565a2d3b1290f9c.

The supplied full verifier completed on fresh downloaded source in 25.1 s:
odd n>=59, coefficient 7.20127188819914..., additive constant <=19.648867.
logs/baseline_li_full.log is this job's replay, not a copied old receipt.
The public paper's zone checks assume libm sine/cosine accuracy; only its
helix lemma is Arb-only. Thus we reproduce the public conditional check
without silently upgrading its rigor or claiming a separately written replay.

Public repository searches sorted by updated for 'tight alternating knot',
'ropelength', and 'ropelength 2026' were performed. GitHub code value search
used API indexed ordering after this gh version rejected --sort for code.
The knot query finds Li; ropelength finds Schoen (universal lower bound),
Njakasoa (nonalternating torus family), VibeMathing (research harness) and an
older coordinate atlas. Their HEADs/READMEs/trees were re-opened; applicable
primary pages are saved. No stronger applicable alternating-family upper
claim was located in this bounded screen. No novelty judgment.

Required AI/agent repositories were re-opened: BakeLab/Epi-results,
google-deepmind/alphaevolve_results and alphaevolve_repository_of_problems,
openai/math, plasma-ai/erdos, kisonecat/openai-math, quasar17/Alpha_Omega_Agents,
JamesWeatherhead/CodexProLong, vinid/einstein-arena and
togethercomputer/EinsteinArena-new-SOTA. Saved HEADs, README snapshots and
compressed trees record the scope. OpenAI tree truncation was supplemented
by the direct preprints listing; titles/paths, not every proof, were screened.
The actual awesome list seewoo5/awesome-ai-for-math was fetched after a guessed
repository returned 404. No applicable stronger claim located in those
inventory checks; absence is not proved.

Papers re-opened: Kim–Oh–Huh DOI 10.1088/1402-4896/ad54fd (publisher abstract
available, full text paywalled; the fetched PDF is the publisher landing page,
NOT the paper); Diao DOI 10.1017/S0305004124000288 and arXiv:2208.00123;
Cantarella–Kusner–Sullivan arXiv:math/0103224; Klotz–Thompson
arXiv:2504.00861; Klotz arXiv:2603.02416v2. The latter two construct
nonalternating torus links, so their attractive costs do not transfer here.
The recent arXiv API query (25 entries sorted submittedDate) and public web
queries for 2025–2026 were re-run; sources/arxiv_titles.json records titles,
dates and abstracts. Private communities were not accessed. Indexed X/Reddit
queries found no useful applicable construction; X was not directly readable.
EinsteinArena's live public page and results repository were re-opened.

BAR.json now freezes <=36/5, the smaller underlying helix comparison, both
methods, the eight-hour pilot and all proof/closure/checker obligations.
No new mathematical search preceded that freeze.

## Underlying helix numerical reproduction, 03:17 UTC

Fresh execution of the public helix_optimum.py gives
c=7.2012609899825052627, a1=1.9340602789825294117,
a2=.07548595597617848789, b=.32272145257985288442.
logs/baseline_helix_optimum.log retains this replay. This is numerical
optimization, not a proof of global optimality. It confirms the underlying
comparison already frozen in BAR.json; merely improving the displayed
7.2012719 rounding would not meet the task.

## Additional code-search hits screened, 03:21 UTC

The earlier indexed value query returned 198 hits, first 30 retained; most
are unrelated numerical data or copies of the official table. Its additional
relevant repositories were re-opened during continuation: u00dxk2/bounds-ledger
(the 22b page explicitly mirrors the same Li/Claude row at main 87b4ebb) and
carlostoledo1891/cert-machine (README plus complete 12,806-entry tree, no
C22b-specific certificate path located). The latter search is an inventory
screen, not a proof audit of all its corpus. No changed applicable comparison
was located; BAR.json remains unchanged. These additional hits were fully
screened during continuation rather than represented as pre-freeze readings.

## Classical crossing-count input re-opened, 03:27 UTC

The reduced-alternating crossing-minimality input was checked in the original
papers: Kunio Murasugi, Jones polynomials and classical conjectures in knot
theory (Topology 26, 1987, 187–194),
https://www.maths.ed.ac.uk/~v1ranick/papers/murasugijones.pdf ; and Morwen B.
Thistlethwaite, A spanning tree expansion of the Jones polynomial (Topology
26, 1987, 297–309),
https://www.maths.ed.ac.uk/~v1ranick/papers/thistlewaitejones.pdf . Their
statements cover links with connected reduced alternating diagrams, not just
prime knots. Louis H. Kauffman's parallel bracket-polynomial contribution is
credited; DOI 10.1016/0040-9383(87)90009-7 was re-opened as well. Our finite
checker only establishes the diagram hypotheses and explicitly relies on
this classical theorem. It certifies no spatial reach or C22b bound.

## Superhelix and rational-tangle continuation, 04:05 UTC

A promising unverified four-strand candidate uses the superhelix construction
of Huh–Kim–Oh and the unequal satellite radii of Li/Claude. The Huh–Kim–Oh
2018 primary institutional abstract (DOI 10.1088/1751-8121/aae969) was
reopened: its stated family is T(2,6k+1), bound 45.8237k+28.4223.
The full article was unavailable here; no claim to have read its proof.
The following full primary papers were also reopened and saved, rather
than relying on remembered topology statements:

- Louis H. Kauffman and Sofia Lambropoulou, *On the classification of
  rational tangles*, https://arxiv.org/abs/math/0311499, full PDF and text
  in sources/rational_tangles.*. Theorem 4 supplies the integral coloring
  fraction; the rational tangle classification is needed, not merely a
  determinant calculation.
- Kauffman–Lambropoulou, *On the classification of rational knots*,
  https://arxiv.org/abs/math/0212011, full sources/rational_knots.*.
- Murasugi and Thistlethwaite 1987 full original papers retained in
  sources/; the reduced alternating crossing theorem is needed for the
  final two-strand torus link diagram. Kauffman's parallel result is
  credited; its full journal PDF was not available (403).

These are additional credited ingredients, not evidence of novelty.

04:20 UTC continuation: reopened Youngsik Huh's primary author homepage,
https://sites.google.com/site/youngsikhuh/home; it lists the 2018, 2021 and
2024 papers but supplies no accessible full-paper download for them. Also
reopened Huh–Kim–Oh, *Tight conformation of 2-bridge knots using superhelices*
(2021), DOI10.1063/5.0059298, via the primary Korea University publication
page. Its abstract describes a superhelix construction for long twisted
2-bridge knots; no stronger applicable numerical constant is stated in the
available abstract. This is an additional credited related construction;
the full text was unavailable in this audit.

05:20 UTC continuation: credited Richard L. Bishop for the named relatively
parallel frame used in the bending/length derivation. Primary publisher
metadata reopened at https://doi.org/10.1080/00029890.1975.11993807
(*There is More than One Way to Frame a Curve*,1975,82(3),246–251).
The author-labelled ResearchGate PDF opened in the browser exposed only a
bibliographic reference in extracted text; direct download returned403.
The full original paper was not validated. Every frame formula used here
is explicitly derived or checked algebraically; no uninspected theorem
from that paper is assumed.
