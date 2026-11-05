# C44 round 5 prior art — 2026-11-01

First job file, written before code or construction. Machine rules and the
round-four proof/report and independent review were read first.

Inherited candidate: C44 < 3.9819073803, exact rational certified and reviewed
by the separate review_c44r4 agent, but unrefereed by a human. Its method is
CHS/Wellens weighted local degree and block recurrence, Épi exact polynomial
certificates, and minimum-influence/parity caps c4=25/16,c5=71/32,c6=45/16.
No novelty, priority or optimality claim is intended.

The live rendered table was read at 20:39 UTC:
https://teorth.github.io/optimizationproblems/constants/44a.html
It lists Pinho's unrefereed 4.3576549226 as best table upper bound. The prior
job's 20:13 UTC raw-source/open-PR audit found PR294 at 4.1225323803 and PR285
citation-only. A fresh direct raw-source and all-open-PR audit follows before
mathematical search. The browser could not open GitHub's API endpoint; direct
read-only fetching will be used and its outcome recorded.

Primary structural source read:
https://arxiv.org/html/2303.10995
Alexandr Valyuzhenich (2023), Optimal functions with spectral constraints in
hypercubes, Theorem 2(2). The prior review identifies its product classification
as stronger than the inherited 2(d-1) control bound. Attribution is essential.

Other initial checks will cover public repository metadata sorted by recent
update, BakeLab/Epi-results, google-deepmind/alphaevolve_results and
alphaevolve_repository_of_problems, openai/math, EinsteinArena,
plasma-ai/erdos, kisonecat/openai-math and queelius/boolean-degree-sensitivity;
recent arXiv and indexed public community results. Coverage and unavailable
sources will be recorded. Known CHS/Shinkar–Tal lower counts 22,46,94 are lower
witnesses, not exact R4,R5,R6 values.

## Initial gate completed

Direct audit receipt 2026-11-01T20:39:33 UTC:
sources/public_initial.json.gz and sources/public_initial_summary.json.
All 43 visible open PR diffs, raw 44a, issues, eleven named repository heads
and README/indexes and recent-update repository searches were read without
fetch errors. Main remains 87b4ebbd, table best 4.3576549226*, PR294
4.1225323803*, PR285 citation-only. No stronger applicable public result was
located. Authenticated global code search and private communities unavailable.
Both inherited frozen verifiers passed on the pod before improvement search,
reproducing 157739602520732550180509661243/39614081257132168796771975168.

Recent arXiv searches locate Valyuzhenich 2609.12540 (q>=3) and the older
Potapov 2410.21937; neither supplies a sharper binary cap. Indexed X/Reddit
searches returned no applicable new result. This is bounded search coverage.

Additional prior method to investigate: binary Reed–Muller second weight
3*2^(n-k-1), due to Kasami–Tokura and Kasami–Tokura–Azumi. Primary accessible
statements: Klein–Storme (2011), Theorem 2,
https://backoffice.biblio.ugent.be/download/2140143/2939938
and Rolland (2009), introduction p.2,
https://arxiv.org/pdf/0902.0058 . The original DOI is
https://doi.org/10.1109/TIT.1970.1054545 . Boundary orders require separate
handling; the 3/2 gap is not blindly applied at k=n or k=1.

All mathematical computation will run on math-cpu-6 under
/root/os/math_c44r5_1101, nice 10, single-threaded BLAS, at most seven workers
and 40 GB. Start 20:38 UTC; five-hour deadline 01:38 UTC Nov 2, earlier than
the pod's required check cutoff 04:17 UTC. No external writes or messages.

## Final source recheck and accepted local candidate

The second complete direct audit finished at 2026-11-01T20:53:54.911162 UTC:
sources/public_final.json.gz and sources/public_final_summary.json. It again
read raw 44a, all 43 visible open-PR diffs, issues, named rival repository
heads and README/indexes, and repository searches sorted by recent update.
No fetch errors occurred. Main stays 87b4ebbd with Pinho 4.3576549226*;
PR294 remains 4.1225323803* and PR285 citation-only. No stronger applicable
public number was located in this bounded audit. The inherited local round
four candidate 3.9819073803 was reproduced before the improvement work.

The accepted round-five local candidate is C44 < 3.1674542553, unrefereed
by a human, with exact rational certificates and separate row/column checks
on frozen bytes. Its exact same-tail gain over round four is 417/512.
This is not a novelty, priority or optimality assertion.

The new dependency is the classical binary Reed–Muller second-weight theorem.
The bridge is reduction modulo two of the integer-coefficient bit polynomial
for the ternary derivative itself. Dummy coordinates place the theorem in
its interior parameter range. Valyuzhenich's full block classification is
also used explicitly: 113 finite types at degrees 4..8 are independently
checked, and the exceptional worst type is phi_2^(d-1). This classification
does not lower the worst control count; sequentially stronger lower caps
improve the minimum-case budgets.

Primary source snapshots and hashes are in sources/primary_source_receipt.json.
Valyuzhenich, Klein–Storme, Rolland, Wellens and Krotov–Valyuzhenich downloaded
successfully. The NSF CHS PDF request timed out; the corrected CHS proof was
instead read in the previously reviewed Rutgers thesis and downloaded afresh
as sources/chs_thesis2020.pdf (SHA256
e1ccfce16e2f0b9d223a632b367613077ae470c9bf207d6a4b3fafe0be3b51d0).
The original Kasami papers are credited through their DOI and the explicit
accessible published theorem statements; no claim of re-proving them is made.

Credit: CHS and Shinkar–Tal for the lower family; CHS/Wellens for weighted
local degree, extremal identity and recurrence; Wellens for the analytic
block bound; Épi for raw exact polynomial data; the earlier Fourier-energy
and block exclusions, including Koshta, Stepanovs and Towell, are retained.
Private communities and authenticated global code search were unavailable.
