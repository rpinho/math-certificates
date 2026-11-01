# Adversarial review of the C89c lower-bound certificate

**Overall verdict: PASS for C89c >= 0.000021083, in the unscaled PR #279 normalization, without a Ramsey-number assumption. My subjective probability that this mathematical inequality is correct is 99%.** I found no false step or mathematical gap after reviewing the proof and code, replaying both submitted verifiers, writing a third exact implementation, and running K3/K4 falsification tests. Exhaustive priority remains unestablished; that is separate from correctness.

The target is the frozen bundle accompanying `../sweep3/REPORT.md`, claiming **c6 >= 21083/10^9 = 0.000021083** without a Ramsey-number assumption. The reviewer did not author the submitted proof or either submitted verifier. The review began 2026-11-01 at 21:50 UTC (first persisted checkpoint). No commits, pushes, PRs, posts, or external messages were made.

## Definition checked first

[PR #279](https://github.com/teorth/optimizationproblems/pull/279) defines the limit of the minimum **number of monochromatic six-element vertex sets divided by binomial(N,6)**. The freshly fetched diff (`sources/pr279.diff`, lines 86–103) matches the submitted source snapshot. This agrees with `bundle/PROOF.md:12–14` and the actual verifier, `bundle/verify_exact.cpp:83–89`.

For ordered injective six-tuples the numerator and denominator both acquire 6!, so the density is unchanged. Dividing an ordered numerator by binomial(N,6), or an unordered numerator by N^6, would change the normalization; neither error occurs here. Independent graphon sampling agrees in the limit since repeated finite vertices have probability O(1/N).

The random-colouring density is **2^(1-15)=1/16384**, with both colours counted. It is a reference scale, not a factor built into c6. The candidate is 0.345423872 times that value. The proposed asterisked upper bound is approximately 4.530364145469e-5, or 2.1488232915 times this candidate. No missing factor 2, 6!, or 2^14 was found.

## Step-by-step verdicts

Line references to PROOF.md and code identify the frozen files under `bundle/`; their contents match the author's source by the manifest. References to REPORT.md in this table identify the submitted `../sweep3/REPORT.md`, also preserved verbatim as `sources/submitted_REPORT.md`. A range is given where a step spans several lines.

| Step | Exact location | Verdict | Reason/evidence |
|---|---|---|---|
| Definition and existence of limit | PROOF.md:12–14; live pr279.diff:86–92 | PASS | Uniform subset sampling proves monotonicity of the minimum densities. Both sources use the same unordered-set normalization. |
| Unordered rooted flags | PROOF.md:18–31; verify_exact.cpp:45–64 | PASS | Root and nonroot permutations remain separate; type and full orbit coverage checked. Unordered roots still define deterministic class probabilities for each actual root set. |
| Rational PSD matrices | PROOF.md:33–45; verify_exact.cpp:34–40 | PASS | Q=L^T L/10^18 is PSD over the rationals by explicit squares. Confirmed 13 blocks and 793 factor rows. No numerical eigenvalue test enters. |
| Root/extension sampling coefficients | PROOF.md:49–54; verify_exact.cpp:41,90–99 | PASS | Denominators are 560 and 420. All t-subsets and both ordered complementary m-subsets are counted. Wrong root types contribute zero. |
| Off-diagonal factor of two | PROOF.md:54; verify_exact.cpp:93–99 | PASS | A and its complement are both visited; symmetric off-diagonal q_ij terms have both ordered occurrences. |
| Target K6 density | PROOF.md:54; verify_exact.cpp:83–89 | PASS | Directly counts monochromatic six-subsets and divides by binomial(8,6)=28. Both all-red and all-blue subsets count once. |
| Graph-list completeness | PROOF.md:62–66; verify_exact.cpp:68–82,106 | PASS | C++ replay covers all 268,435,456 labelled graphs using disjoint permutation orbits of 12,346 representatives. Python augmentation independently reconstructs those classes. |
| All rational coefficient inequalities | PROOF.md:56–73; verify_exact.cpp:89–103 | PASS | Submitted C++, submitted Python, and a newly written reviewer checker reproduce all inequalities and the same exact minimum slack. |
| Integer arithmetic and overflow | PROOF.md:68; checked_integer.hpp:13–25 | PASS | Successful C++ operations are checked signed-128-bit operations. Two Python replays use arbitrary-precision integers. An oversized integer was rejected. |
| Positivity for independent extensions | PROOF.md:79–81 | PASS | Conditional on the actual root set R, independent samples produce x_R^T Q x_R >=0. The indices may merge root automorphisms without harming this fact. |
| Correction for intersecting samples | PROOF.md:83–98 | PASS | Overlap probability <=m^2/(N-t), and conditioning changes a bounded expectation by <=2 M_Q epsilon. No finite disjoint-sample independence is assumed. |
| Match with uniform eight-set sampling | PROOF.md:100–106 | PASS | Each disjoint triple (R,A,B) has a unique eight-vertex union and equal probability under both experiments. |
| Average and take the limit | PROOF.md:108–113 | PASS | Gives p6(G)>=b-sum_Q 2M_Q m_Q^2/(N-t_Q), uniformly over G. Fixed finite matrices make the error vanish. The inequality direction is correct. |
| No Ramsey-number assumption | PROOF.md:8,113; REPORT.md:56 | PASS | The proof and frozen certificate replay never use 165, 252, or another Ramsey input. Those occur in separate baseline comparisons. |
| Solver and verifier independence qualifications | REPORT.md:24,70; PROOF.md:128 | PASS | Floating solver status is explicitly excluded from the proof. The author acknowledges both original verifiers came from one authoring session. This review supplies a fresh implementation and mathematical audit. |
| Exhaustive novelty/priority | REPORT.md:58,62; PRIOR_ART.md | GAP for any stronger priority claim | The source audit is bounded and has API/indexing limits. The submitted report expressly disclaims exhaustive priority. This does not affect the inequality. |

No mathematical step received FALSE or GAP. The sole GAP above concerns an exhaustive priority assertion that the author does not make.

## Exact replay receipts

All 40 files in `bundle/ARTIFACT_MANIFEST.json` matched their byte counts and hashes on the pod. The archive SHA256 also matches the submitted report: `92e6822d0440527ea03a725c9f9dae739106f121d6804855ca5379bc84231f84`. Certificate SHA256:

```
39bd22dac99c7cd509ffc6b32762302f79b2775c3e16fed89078080c4f0296f5
```

Three exact replays agree:

- `receipts/replay_cpp.log`: submitted C++; complete labelled-graph coverage plus integer inequalities.
- `receipts/replay_python.log`: submitted Python/nauty; independent vertex augmentation for graph-list completeness.
- `receipts/reviewer_exact.log` and `reviewer_exact.json`: fresh reviewer implementation in `scripts/reviewer_verify.py`, using adjacency sets and row-major tuple keys internally, rebuilding rooted flag orbits and all root/extension partitions. No submitted verifier or search coefficient table is imported. Its graph-list completeness relies on the separately checked complete list.

All reproduce the minimum slack at zero-based graph index 198:

```
56963049278016000000000 / 47040000000000000000000000000000
= 42383221189 / 35000000000000000000 > 0.
```

The worst graph is `G?ACKK`, a red K4 plus four isolated vertices. It has **zero** monochromatic K6s, while its a(H) is `-737947383221189/35000000000000000000`. This directly checks that the proof does not treat a(H) as pointwise nonnegative or assume every eight-set contains a K6; nonnegativity is only asymptotic after averaging. The witness is retained in `receipts/worst_graph.json`.

Negative controls reject a bound above the random-colouring upper bound, doubling the claimed bound with the same factors, doubling D while keeping those factors, deleting the final graph representative, duplicating a flag, and an overflowing integer. The respective failure messages are in `receipts/reviewer_controls.json` and `receipts/fast_controls.json`. Rejection of the doubled bound is a test of this certificate; it does not itself prove the doubled bound is mathematically false.

## K3/K4 falsification and literature comparison

The requested K3 and K4 tests passed exact verification. A separate hand-derived same-method triangle certificate passes exactly at **c3>=1/4**, with zero coefficient slack on all four three-vertex graph classes; see `receipts/goodman.log` and `scripts/goodman.sh`. Its Gram matrix is (3/4)[[1,-1],[-1,1]], represented by three identical integer factor rows (1,-1)/2. For a monochromatic triangle a(H)=3/4; for a mixed triangle a(H)=-1/4. Thus p3(H)-a(H)=1/4 identically. Together with random colouring this gives the known exact c3=1/4.

The fresh eight-vertex tests use exactly the primary certificate's two unordered-root families (t,m)=(2,3),(4,2), with 13 blocks and all 12,346 graph classes. Only the target objective changes to monochromatic K3, K4, or K5 density. `scripts/make_targets.py` counts these objectives independently by vertex subsets. The submitted search/rounding scripts were copied into `scripts/` and adapted only to read these target filenames. All three runs reached their time limits with `optimal_inaccurate` status. Their matrices were projected and rounded to integer factors, and their rational bounds then passed complete exact replay; the floating objectives are not used as proofs. These are achieved certificates, not claims of optimality for the relaxation.


The fresh results are:

| Target | Raw solver objective (not a bound) | Exactly certified lower bound | Verdict |
|---|---:|---:|---|
| K3 | 0.249357941256 | 0.249290642 = 124645321/500000000 | PASS |
| K4 | 0.0278482363437 | 0.027777765 = 5555553/200000000 | PASS |
| K5 | 0.00136736855672 | 0.001190775 = 47631/40000000 | PASS |

Each replay checks all 12,346 classes covering all 268,435,456 labelled eight-vertex graphs. The random-density checks give 1/4, 1/32 and 1/512 respectively. Exact source locations: `receipts/verify_k3.log:1–5`, `verify_k4.log:1–5`, `verify_k5.log:1–5`; the certificate headers are in `target_certificates/k3.cert:1`, `k4.cert:1`, `k5.cert:1`. `receipts/targets_summary.json` records hashes and comparisons with exact published upper bounds.

The eight-vertex K3 certificate stays below the known 1/4. The K4 certificate is below both the published lower benchmark 0.0296 and published upper bound 0.030145; this restricted, time-limited run achieves a weaker bound than the published K4 methods. The K5 result also stays below the published lower benchmark 0.001524. No normalization inflation or contradiction appears. The separate exact Goodman certificate recovers 1/4 with the same conditional-square method at ambient order three. None of these tests establishes optimality or priority.

Published benchmarks checked in primary sources:

| Quantity | Certified published benchmark located | Source and comparison |
|---|---:|---|
| c3 | 1/4, exact | Goodman; also stated in [PPSS section 1.1](https://arxiv.org/html/2206.04036v3). |
| c4 | >0.0296 | [Grzesik–Lee–Lidický–Volec, final discussion](https://arxiv.org/html/2012.02057v2), a nine-vertex flag computation; current live table lists 0.0296. Published upper <0.030145 in PPSS, so the constant is about 0.03, not known exactly. |
| c5 | >0.001524 | [PPSS Theorem 1.2 and section 4.3](https://arxiv.org/html/2206.04036v3), an eight-vertex exact certificate. |

[KPS section 7](https://arxiv.org/html/2312.08049v1) gives nine-vertex floating suggestions 0.02961 and 0.001557, explicitly not converted to exact rational certificates. They are not substituted for certified published lower bounds.

At a fixed ambient order of eight, the flag-product coefficient matrix and PSD block sizes do not depend on the target clique order k. Only the objective vector changes. Thus a K6 bound need not require a larger graph enumeration than an eight-vertex K5 bound. This is a direct observation from the same matrix used in the fresh tests, not a claim that near-optimal K6 bounds are easy. The blanket feasibility remark in PR #279 (`sources/pr279.diff:113`) is not evidence that this certificate must fail.

The published lower/random ratios for K4 and K5 are approximately 0.9472 and 0.780288. The K6 candidate's 0.345423872 is less tight relative to random colouring. Its large improvement over the elementary estimate is still remarkable, but not inconsistent with these comparisons: the exact ratio to 5/98240568426 is 414241.1808250716; the ratio to the author's stronger de Caen/Mackey consequence 1/929632032 is 19599.432130656. No priority claim is made here.

A further exact calculation from the stored factors gives a coarse finite bound

```
p6(G) >= 0.000021083 - (2247872748790544739/62500000000000000)/(N-4).
```

The coefficient is 35.965963980648715824; this expression becomes positive only above about 1.7 million vertices. Thus the asymptotic result does not imply an unexpectedly small Ramsey number. Individual eight-vertex colourings can have no K6; their negative a(H) terms are consistent with the proof. Only the large-graph average becomes nonnegative. See `receipts/certificate_stats.json` and `AUDIT_NOTES.md`.

## Prior-art scope

`PRIOR_ART.md` records fresh public reads of the live table, PR #279, open PRs and issues, GitHub repositories sorted by updated, the seven required AI-result repositories, recent arXiv results, and primary papers. The #279 diff matched the author's snapshot. The main table still has only K4; K5/K6 are proposed additions. No competing applicable c6 lower certificate was found in this bounded audit. Some recursive repository queries were rate-limited; the openai/math tree is truncated and was supplemented by its overview. Community searches found no additional applicable certificate. No account creation or contact was attempted. The classical comparison arithmetic was also replayed exactly. The historical R<=165 thesis computation was not rerun and is separate from the submitted theorem.

## Reproduction and closeout

The primary replays can be reproduced on the authorized pod inside this review directory with:

```sh
cd the job directory
sh scripts/run_compute.sh g++ -O2 -std=c++17 bundle/verify_exact.cpp -o verify_exact
nohup sh scripts/run_compute.sh ./verify_exact bundle/c6_8.cert bundle/sources/graph8.g6 > receipts/replay_cpp.log 2>&1 < /dev/null &
nohup sh scripts/run_compute.sh python3 scripts/reviewer_verify.py bundle/c6_8.cert bundle/sources/graph8.g6 > receipts/reviewer_exact.log 2>&1 < /dev/null &
```

The submitted Python/nauty replay uses the read-only installed pod venv, as detailed in [REPRODUCE.md](REPRODUCE.md). For the new targets, first run `nohup sh scripts/run_compute.sh sh scripts/falsify.sh > receipts/falsify_driver.log 2>&1 < /dev/null &`; after `receipts/targets.done`, run the following for each k=3,4,5:

```sh
nohup sh scripts/run_compute.sh sh scripts/one_target.sh "$k" > "receipts/target${k}_driver.log" 2>&1 < /dev/null &
```

All substantial computation ran only on a rented pod in `the job directory`, under nohup, with single-threaded numerical libraries and at most four active compute processes. The first nested replay wrappers lowered priority to nice 19; the corrected wrapper sets nice 10. The temporary coefficient table was retained losslessly as gzip after all target exports. All certificates, completed logs, hashes and process-audit receipts were pulled back. Local scientific work was limited to tiny arithmetic and document/receipt processing.

Final process audit: `receipts/worker_cleanup.json` reports PASS with no surviving recorded worker/launcher PIDs (apart from the short audit itself, which exited). Full requested `ps -axo pid,ppid,pcpu,command` snapshots are retained for the pod and local machine. The pod remains running; no other jobs or lifecycle controls were changed. Retained workspace size is below 50 MB.

Next useful verification is an independent import of these frozen factors into an established flag-algebra checker or expert review of the short averaging argument. The public-source audit remains bounded. The 99% confidence estimate concerns the normalized inequality, not originality, SDP optimality, or the quoted upper certificate.

The current open-PR inventory contains 45 entries. In particular [#307](https://github.com/teorth/optimizationproblems/pull/307) proposes an unrefereed K5 upper bound 0.00168523 and does not change the published lower benchmark. PR #279's comments concern the upper certificate; this review checks its definition and quoted scale, and does not certify that upper construction. `receipts/baselines_replay.log` separately reproduces the supplied exact baseline arithmetic after checking Conlon's stated recurrence.

The primary eight-vertex certificate is sufficient for the reviewed theorem. The original numerical K6 search and older seven-vertex certificates were not rerun in this review; their optimality and provenance claims are not prerequisites of the primary exact proof. Search reproducibility is separate from deterministic replay of the frozen certificate.

Review finalized 2026-11-01 22:26:08 UTC.
