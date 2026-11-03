# Prior art — C44 round seven, candidate and unrefereed

First job file, written before code, search, or construction. Start 2026-11-01
22:06 UTC. Deadline 2026-11-02 03:06 UTC (five hours), before the pod's
05:35 UTC check cutoff. Compute: math-cpu-8, /root/os/math_c44r7_1101,
nice 10, single-threaded BLAS, <=10 workers and <=40 GB. All other jobs
are read-only. No commits, pushes, PRs, posts or messages.

The round-six review REPORT.md is complete and says mathematical PASS for
C44 <2.1974348818 (98% subjective confidence). Its source-coverage GAP is
confined to an unused KTA theorem. It also independently reports that the
R4=22 input gives R5<=53, R6<=117 and R7<=250. Review monitoring continues.
The gap1 proof and review supply candidate R4=22 and R5<=53. These are local,
unrefereed inputs, not public records. Baseline: reproduce round six and
its scalar optimizer, then combine the quartic input before improvement.

Inherited live public baseline (to refresh before compute): official table
https://teorth.github.io/optimizationproblems/constants/44a.html lists
4.3576549226*, published Wellens 4.394 and lower bound 3/2. Open PR294
https://github.com/teorth/optimizationproblems/pull/294 has 3.9819073803*.
Raw table https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/44a.md .

Methods credited: CHS/Wellens weighted degree and restrictions; Shinkar–Tal
lower family 22,46,94; Valyuzhenich's minimum-support classification;
Kasami–Tokura's binary second-weight gap; Rasoolzadeh's 761-class cubic
catalogue. Primary references:
https://par.nsf.gov/servlets/purl/10201042 ,
https://arxiv.org/html/2005.00566 ,
https://arxiv.org/html/2303.10995 ,
https://arxiv.org/html/2311.05566v2 ,
https://doi.org/10.46586/tosc.v2023.i3.213-226 ,
https://gitlab.science.ru.nl/shahramr/ResilientFunctions ,
https://www.aimspress.com/aimspress-data/math/2024/5/PDF/math-09-05-518.pdf .

Read-only audit will cover raw live table and open PRs/issues; public code
sorted by recent update; BakeLab/Epi-results, DeepMind alphaevolve_results
and repository_of_problems, openai/math, EinsteinArena, plasma-ai/erdos,
kisonecat/openai-math; recent arXiv and indexed community sources. Coverage
and limitations will be recorded. No novelty or priority claim is planned.

## Initial gate completed (22:09 UTC)

Read-only audit succeeded with zero fetch errors: all 43 inherited open-PR
diffs plus visible new entries, table/issues, eleven named repository HEADs
and README/indexes, awesome-list and repository searches sorted by update.
Receipts: sources/public_initial.json.gz and public_initial_summary.json.
Round-six exact checkers A and B reproduced its frozen rational. Gap1's
unmodified replay supervisor requested 40 GiB, above our stricter 40 GB
hard cap; it stopped before mathematical checks. A job-owned wrapper is
replaying its unchanged mathematical steps at the authorized 40 GB limit.

Primary classification limitation: Rasoolzadeh 2023 p.225 reports
1,035,596,784 classes already at (n,t)=(6,1) for t+5, with larger tables
not stored. The 2024 addendum (DOI 10.46586/tosc.v2024.i3.298-301) treats
only binary ANF degree <=3 and therefore is not a full real-quartic
classification. It cannot be substituted for an unrestricted quartic
energy envelope.

Additional primary leads read: Ghorbani–Kamali–Khosrovshahi–Krotov,
On the volumes and affine types of trades,
https://arxiv.org/abs/1810.02296 ; Krotov, On the gaps of the spectrum of
volumes of trades, https://arxiv.org/abs/1811.00015 . Their volume results
are related to signed small-support polynomials. Any affine-coordinate
normal form still requires a separate argument for real degree.
Indexed X/Reddit searches located no stronger applicable result. Private
communities and authenticated global code search are outside coverage.

## Equality-case topology source checked before use

Masuda–Panov, *Semifree circle actions, Bott towers, and quasitoric
manifolds*, Sbornik Mathematics 199(8) (2008), 1201–1223,
DOI 10.1070/SM2008v199n08ABEH003959, Lemma 4.7, says a connected
simplicial complex of dimension at least two whose vertex links are
cross-polytope boundaries is itself a cross-polytope boundary. The arXiv
primary PDF https://arxiv.org/pdf/math/0607094v2 was read at pp.14–15;
the published text was checked via the indexed Math-Net full text. The
lemma's elementary proof will be expanded in PROOF.md. This is a credited
published tool, not a new topological classification claim.

## Integer-valued energy gap found before using it (22:26 UTC)

Gabriele Nebe, *The second minimum of Barnes–Wall lattices*,
https://arxiv.org/abs/2603.23133 and author's primary PDF
https://www.math.rwth-aachen.de/~Gabriele.Nebe/papers/BW.pdf ,
Definitions 2.1/2.3 and Theorem 3.3, supplies a possible stronger ingredient:
a nonminimal vector has squared norm at least 3/2 times the minimum.
The two integral models have affine-subspace generators with coefficients
2^floor(codim/2) and 2^ceil(codim/2), respectively. Embedding integer-valued
real-degree-r cube polynomials requires a written scaling proof; no bound
is inferred from a bare analogy with Reed–Muller codes.
The recent Cao–Hu–Huang–Yang preprint https://arxiv.org/html/2610.15288
claims the complete below-twice norm spectrum. It was read as context;
only Nebe's second gap is being considered as an added premise.

## Classical lattice sources and expanded gap proof

Barnes–Wall 1959, DOI 10.1017/S1446788700025064, was opened at the primary
Cambridge PDF: Theorem 3.1(ii) gives the coordinate-subspace basis,
Theorem 3.2 the minimum, and Theorem 4.3 the similarity. Broué–Enguehard
1973, https://www.numdam.org/item/10.24033/asens.1241.pdf , Theorem II.4
and its proof at printed pp.36–37 state minimum-vector transitivity.
Nebe's precise pair-stabilizer convention is stated in her Theorem 2.5.
BW_GAP_PROOF.md expands the recent norm-gap induction, congruence step,
ordered-pair similarity, and low-dimensional bases. Classical basis,
minimum and transitivity remain explicit external dependencies; the
finite exact checks do not replace them. No priority is claimed for this
credited lattice argument or its C44 consequences.

## Final live recheck (2026-11-01 22:50 UTC)

The final audit re-fetched the raw official table, all inherited 43 open-PR
diffs and visible new entries, issues, eleven result-repository HEADs and
README/indexes, awesome-list and public repository searches sorted by
update. It completed with zero fetch errors. Main remains
87b4ebbd426ff8db597a2004cc45da17903bdcf2; the public table still lists
4.3576549226*, and the applicable PR294 packet is 3.9819073803*.
No stronger applicable public C44 bound was located in this coverage.
Receipts: sources/public_final.json.gz and public_final_summary.json.
This is bounded source coverage, not an exhaustive priority search.
Neither this job nor its frozen packet claims novelty, priority, a public
record, or independent human refereeing.
