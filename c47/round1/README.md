# C47 round 1: half-cell candidate lower bound

**Candidate, unrefereed lower bound: C47 >= 170311/100000 = 1.70311.** The fixed 59-atom single-period measure gives exact certified witness ratio

\[
q=\frac{215956002657486428307163448091951082893881}{126800499112387565339223240212480000000000}
=1.7031163455127832639\ldots .
\]

The claim is the largest 1/100000-grid value below q, rounded down. The corresponding 1/10000-grid claim is 1.7031. No novelty or record claim is made.

## Certificate and finite instance

The measure is extracted exactly from the frozen 117-atom parent: retain all atoms with `0 <= y < parent Py/2` and halve its vertical period. This selects **50 inherited atoms plus 9 hole-filling additions**, with every selected coordinate and mass preserved. There was **no further tuning** of the fixed measure. Periods are `164377561597/50000000000` and `2744174966813/1000000000000`, level 1.

| Check | Result |
| --- | --- |
| Explicit certificate | 59 positive rational atoms, 559 rational box/radius/rectangle witnesses |
| `verify_exact.py`, **separately written (same agent)** | PASS, exact q above |
| Seven semantic corruptions | All reject, exit status 1 |
| Tomar's unchanged v5 `check_exact2.py` | 33,356 rectangles; exactly the same fraction q |
| Tomar's original 50-atom baseline | Published full fraction reproduced, 5,135 rectangles |
| Finite truncation and smearing | h=2, N=2,147,177; finite ratio 1.7031100000097934850… > 1.70311 |
| Receipt and smear-margin audit | PASS; all 559 smear inequalities checked |

The 59-atom cell mass is `131978281545501/25000000000000` and its exact certified covered area is `647868007972459284921490344275853248681643/72057594037927936000000000000000000000000`.

The finite instance needs **two** boundary layers: its maximum witness radius exceeds the half-cell's vertical period. Its positive smear radius is `3075015278326308311/12117811236023199334400000000000000`. The exact finite ratio, norm and atom count are in [the finite receipt](logs/half59-finite.json); [PROOF.md](PROOF.md) gives the full periodic-to-finite argument. The receipt audit checks every radius enlargement against the strict minimum mass slack. The verifier imports no producer or search code.

The certificate [half59.json](certificates/half59.json) has SHA-256 `b4d88847ef0c41577213a34ef6fda3d0d9b52b672f6ce20e998b006a2031ba99`. The unchanged copied verifier has SHA-256 `f01475b149795e25821fc5c434ee2d535b941967897c758dbdc1391e8ae3edfe`. See [exact verification](logs/half59-exact.json), [rejection controls](logs/rejection-controls-half59.json), [Tomar replay](logs/half59-upstream.log), and [consistency audit](logs/receipt-audit.json).

## Provenance and bounded upstream experiment

The construction is **further hole-filling on Tomar's measure: the same insertion-and-refinement operation as his hf.py, applied by our own search scripts**. Our c47r1 search scripts inserted small masses into uncovered holes and refined the resulting configuration, starting from Tejasvi Singh Tomar's published 50-atom measure. The inherited parameters had already been refined in c47r1; this job freezes them. The general finite-periodic rectangle result is **Tomar's Lemma 6.2, following Lin**. Lin supplies the weighted-lattice and truncation-and-smearing foundation.

The earlier doubled-period 117-atom certificate gave 1.7031062130924713…. Its lower half, repeated at the half vertical period, gives the larger q above. The claimed increment is therefore already certified in a single period, using our scripts to apply Tomar's hole-filling operation. [CREDIT.md](CREDIT.md) records the sources and code derivation.

The provenance replay used Python 3.12.3, NumPy 2.5.4, SciPy 1.18.1, and GCC 13.3.0 (`-O3 -shared -fPIC`, no reach override). The measured process had one thread, nice 15, and an 8 GiB address-space cap; the historical environment and limits are summarized in [REPRODUCE.md](REPRODUCE.md). It executed Tomar's **unchanged v5 `hf.py`**, from his published rational 50-atom measure converted directly to floats. Settings were all CLI defaults: **20 rounds, grid 500, maxit 400, 6 tries**, seed **1103**, with **no HL_REACH override**. An observational profiler records objective returns and best parameters without changing the objective, RNG, settings or decisions. The floating replay is separate from the fixed certified measure. The frozen decision-rule gate is 1.7030; its recorded outcome is in hf-summary.json. The candidate row is prepared under option (A), not filed. No outreach has been sent.

**Best observed floating ratio: 1.7027237336033003, with 50 atoms**, including the initial input evaluation. The run used **21572.02 CPU seconds (5.9922 CPU-hours)** and 21575.59 observer wall seconds, over **14,908 objective evaluations**, below the six CPU-hour maximum. The run stopped during the **initial 50-atom polish** and never inserted atoms. No completed-round output file was produced.

**Frozen gate 1.7030: NOT REACHED in this run.** This is a bounded experimental outcome, not a theorem about the method. No filing or outreach is performed.

This probe ended at the bounded stop; its raw return code is `-2`. Its best value is a floating measurement, **UNVERIFIED** as a new lower-bound certificate. It did not reproduce the certified 59-atom gain within this run. A bounded failure to reach q does not establish a new method or an obstruction to continuing Tomar's search. The provenance attribution remains further hole-filling on Tomar's measure: the same insertion-and-refinement operation as his hf.py, applied by our own search scripts.

Full settings, timing, best-observed versus accepted output, and termination condition: [hf-summary.json](logs/hf-summary.json). Large raw floating-search logs and resource samples are omitted from this release. The early diagnostic cap and 5.5-hour wall cap were superseded, without restarting hf.py, to use approximately the full six CPU-hour budget in the frozen DECISION_RULE.md. The guard planned SIGINT at 21,590 CPU seconds and enforced a hard limit of 21,599 seconds. A controlled stop at 21,570 CPU seconds left a 30-second margin for the final observer checkpoint and supervision overhead; actual CPU use is given above. The guard then resumed the earlier supervisor to reap all children. The decision-rule threshold is 1.7030. Any filing or outreach steps in that file are outside this job: the user explicitly forbade them.

## Release verification and scope

The release reruns the exact verifier, all seven semantic rejection controls, the finite-instance calculation, the receipt/smear-margin audit, and Tomar's unchanged exact checker freshly fetched from the pinned v5 commit. Fresh command outputs are in `logs/release-*`; the exact, finite and control JSON receipts use their canonical names in `logs/`. Historical geometry logs are retained separately. See [REPRODUCE.md](REPRODUCE.md) for local commands, [MANIFEST.json](MANIFEST.json) for file hashes and source provenance, and [SHA256SUMS](SHA256SUMS) for the full release inventory.

**Verification level: L0** for the bound as a whole (definitions: https://github.com/rpinho/math-certificates/blob/59eeb7097f806da05187b5f234445be3589204d4/VERIFICATION_LEVELS.md)
Our exact verifier was separately written by the same AI agent, and Tomar's own unchanged exact checker reproduces the same fraction.

The earlier 117-atom packet was reviewed by GPT-6 Astra (ACCEPT) and Claude Opus 5.5 via Claude Science (FLAG; it corrected an atom-pair count). Both then reviewed this release (the 59-atom certificate, proof, table diff and text), and their findings were wording corrections only, concerning the review attribution and the description of the method; those corrections are fixed in this text. Our publish gate requires both reviewers to accept the final bytes; there is no human referee. Neither the candidate nor Tomar's upper proof was rebuilt in Lean here. Tomar's upper bound is reported with credit, not freshly verified by this release.

The source paper is Tejasvi Singh Tomar, *Bounds for the weak type (1,1) constant of the centred maximal operator over squares*, October 2026, preprint, not peer reviewed: [v5 paper](https://doi.org/10.5281/zenodo.23716077), [supplement](https://doi.org/10.5281/zenodo.23716078), [author page](https://www.mefyi.com/papers/weak-type-squares/). The construction is further hole-filling on Tomar's measure: the same insertion-and-refinement operation as his hf.py, applied by our own search scripts; the weighted lattice and truncation/smearing foundation are due to Yongxi Lin. No novelty or optimality claim is made. A note to Tomar is planned, not sent.
