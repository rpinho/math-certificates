# C44 round 6 prior art — candidate, unrefereed

First job file, before code or mathematical construction. Read the machine
RULES.md and round-five PROOF.md, REPORT.md and STRUCTURE_LADDER.md.
Start: 2026-11-01 21:03 UTC. Five-hour deadline: 2026-11-02 02:03 UTC,
before the mandatory pod check cutoff 04:17 UTC. Compute only on
math-cpu-6 in /root/os/math_c44r6_1101, nice 10, single-threaded BLAS,
at most eight workers and 40 GB. No other job writes or external messages.

Inherited local best: round-five candidate C44 < 3.1674542553, exact value
125475790246857326765951236155/39614081257132168796771975168.
It uses CHS/Wellens weighted local degree and block recurrence, Épi exact
polynomial certificates, Valyuzhenich minimum-support classification and the
Kasami–Tokura / Kasami–Tokura–Azumi Reed–Muller second-weight gap.
The review_c44r5 directory has no STATUS.md or REPORT.md at 21:03 UTC.
Any reported flaw has priority over improvement work.

Round-five source audit at 20:53 UTC found the live table at
https://teorth.github.io/optimizationproblems/constants/44a.html still lists
Pinho 4.3576549226*, with open PR294 at 4.1225323803* and PR285 citation-only.
Source: ../c44r5/PRIOR_ART.md and its public audit receipts.
This round will refresh raw table/open PRs/issues, recent-update public code
search, named AI/agent result repositories, recent arXiv and indexed public
community sources before improvement search and again before any novelty claim.
No novelty, priority or record claim is intended.

Primary references to inspect: Kasami–Tokura (1970),
https://doi.org/10.1109/TIT.1970.1054545 ; Kasami–Tokura–Azumi (1976),
https://doi.org/10.1016/S0019-9958(76)90355-7 ; Valyuzhenich (2023),
https://arxiv.org/html/2303.10995 ; Rolland,
https://arxiv.org/pdf/0902.0058 ; Klein–Storme,
https://backoffice.biblio.ugent.be/download/2140143/2939938 .
Third and higher weights require precise parameter ranges and structural
statements; finite checks cannot substitute for their universal proofs.
The inherited exact verifiers will be replayed on the pod as the baseline.

## Initial audit completed

Read-only direct audit at 21:03:58 UTC: sources/public_initial.json.gz and
sources/public_initial_summary.json. Raw table and all 43 inherited open-PR
diffs, visible PR pages/issues, eleven named public repository HEADs and
README/indexes, awesome-ai-for-math, and recent-update repository searches
were fetched without errors. Main is still 87b4ebbd; table best remains
4.3576549226*. PR294 now contains the round-four 3.9819073803* packet.
No stronger applicable public value was located. Authenticated global code
search and private community access are unavailable. Baseline pod replay
passed all ten inherited stages, including both exact H=96 implementations.

Recent arXiv search located Wei et al., arXiv:2610.29807 (21 Oct 2026),
https://arxiv.org/html/2610.29807 , a weight-spectrum inclusion for RM(m-7,m),
not a stronger C44 bound. Carlet (2024), Identifying codewords in general
Reed-Muller codes and determining their weights, DOI 10.3934/math.2024518,
https://www.aimspress.com/aimspress-data/math/2024/5/PDF/math-09-05-518.pdf ,
section 2, gives the precise below-twice-minimum spectrum and describes why
the 2..2.5 range has many more cases. The primary KTA text remains a target.

## KTA table hazard found

Krotov's public 2017 discussion (read 21:10 UTC),
https://www.researchgate.net/post/What_is_the_next_admissible_weight_of_codewords_of_the_Reed-Muller_code_RMm_r_after_2d_where_d2m-r_is_the_code_distance ,
reports a missing sequence in the final 1976 KTA table: an assertion after
its equation (23) omits weights that become relevant when n-r>7. It gives
an explicit complemented quadratic example with normalized weight 2.0625.
This will be independently checked exactly; the discussion is a lead to a
source defect, not a substitute for a theorem. In particular no universal
2-to-2.125 gap will be used. The original 1976 PDF endpoint and Elsevier API
are inaccessible here (403/authorization denial); the returned files are
marked attempts, not papers. The full 1974 preprint is reported to be 225 pages.
This does not challenge the below-two spectrum or round-five second gap.

Lou–Wang, https://arxiv.org/html/2610.36687 (27 Oct 2026), gives a codimension-7
KTA specialization. Such a fixed-codimension statement cannot be silently
applied to derivatives with arbitrary ambient dimension. Its new conjecture
counterexample is outside the accepted theorem dependencies in this job.

## Related ternary-degree work and final public audit

Potapov, On the number of relevant variables for discrete functions,
Cryptography and Communications 17 (2025), 989–998, DOI
10.1007/s12095-025-00797-4, was read:
https://link.springer.com/article/10.1007/s12095-025-00797-4 .
Its section 5 also uses spectral energy and mixed edges for three-valued
functions. It encodes outputs by complex cube roots of unity; converting
our real ternary A to that encoding is quadratic in A and can double real
degree. Its theorem cannot simply be applied with the original degree k.
It is related prior art for the energy method, not an additional premise
or a sharper cap used here. No novelty is claimed for the energy argument.

The final direct table/repository/PR refresh completed successfully; see
sources/public_final.json.gz and sources/public_final_summary.json.
Main remains 87b4ebbd, live table 4.3576549226*, PR294 at 3.9819073803*.
All visible relevant PR diffs, eleven named result-repository heads and
README/indexes, awesome-list and recent-update repository searches were
read with no fetch errors. No stronger applicable public C44 bound was
located in this bounded coverage. This is not a claim to exhaustive search.
