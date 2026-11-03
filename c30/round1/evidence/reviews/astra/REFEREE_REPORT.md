Referee report: candidate C30 >= 521/50 = 10.42, 3 November 2026.

The arithmetic and enumeration checks pass. I found no mathematical counterexample to the candidate's first-moment route in the checks below. I flag the packet because its source audit contains two definite errors, including an incorrect account of the documented withdrawal reasons. This is an AI referee audit, not human peer review or formal verification of the entire theorem.

The first false item is `submission/GATE.md:13`: it says the reopened sources do not state a precise reason for Norton's v2 withdrawal. The v3 arXiv abstract Comments explicitly identify two defects: the pairing does not ensure agreement between the two cells of a member, and the Appendix F zero count only checks argument increments at arc endpoints. The archived abstract already contains this explanation and matches today's online version exactly. The assertion recurs in REPORT.md:5, STATUS.md:7, V2_DIAGNOSIS.md:26 and SELF_REVIEW.md:14. [Norton v3 Comments](https://arxiv.org/abs/2608.20292v3).

There is also a sign error in REFEREE.md:36. Norton's v1 equation (43) has `J=A-2 Ent`, where A is an infimum of affine functions and therefore concave. Subtracting concave entropy does not preserve concavity. The packet instead says that concavity of `J-2 Ent` would not imply concavity of J; it would, because J would be a sum of concave functions. The corrected known concave quantity is `J+2 Ent`. This does not rescue v1, whose claim remains withdrawn. [Norton v1, equation (43) and Proposition 7.2](https://arxiv.org/html/2608.20292v1).

Neither error is an input to FIRST_MOMENT_PROOF.md. The candidate does use ideas from withdrawn v2—its marginal equations and kernel algebra—but re-derives the needed untilted statements and avoids the withdrawn equal-profile and complex zero-count assertions. The detailed theorem/hypothesis audit is in [EXTERNAL_PREMISES.md](EXTERNAL_PREMISES.md).

All work was done in `../c30r1_review/astra`. The original was copied to `submission/` and was not edited. The original's 131 manifested files and all 32 BAR source hashes pass. At completion, the copy's 131 manifested files also still match: regenerated receipts agree exactly with the frozen ones. New scripts, downloaded sources and logs are outside the copied packet.

Numerical certification results:

| Check | Result |
|---|---|
| Candidate, z=50/521, 384-bit Arb | `Phi > 0.00018309709357909 > 0`. Full ball: midpoint `0.000183097093579096121688885511033486513642923182692066886445219451347805670647887783197856623990070711757807630`, radius `3.95e-112`. |
| Root isolation | `r=0.389444730290250260681229499213459372003778166112582186280 +/- 4.77e-58`; opposite endpoint kernel signs, positive derivative throughout the isolating ball. |
| Root derivative | `partial_v(K_A-R)=0.735815915854709523418243484377832824929066263336219141 +/- 5.52e-55`. |
| Rouché selection | Correctly normalized whole-contour bound `15.2705413938275046967434443880376332302594289762028786295... < 16`; `vmax=364/729<1/2`; the isolated root lies in the selected disc. |
| First moment | `(4/27) p_wu=0.06627960057204584443150090889068205402162470119054947236 +/- 3.23e-57 < 1/10`. Jets are exact truncated algebra over Arb balls. |
| Saddle bracket | Derivative with respect to log q is about `-0.38221648128885995` at q=1 and `29.560384371185575` at q=9. Both lie inside q<1/Q(z). |
| Tangent error | At rational q0=3049509956240/10^12 the slope is `1.402802417551569164...e-13`. The verifier subtracts its absolute value times the sum of the two log endpoint distances, a conservative bound on the tangent loss. |
| Rational conditions | Reciprocal z is exactly 521/50; strict leaf/empty threshold inequalities, first-moment cap slack, four positive profile coordinates, and both profile moment identities pass. |
| Corruptions | All 13 candidate/first-moment controls reject. Nine candidate mutations: inflated bound, invalid profile, too-small two-leaf cap, invalid leaf density, negative kappa, bad saddle, bad z, wrong BAR hash, wrong mean-certificate hash. Four mean mutations: wrong root, non-isolating endpoints, wrong mean threshold, wrong BAR hash. |

These are re-executed results, not acceptance of stored PASS labels. `review_logs/replay.txt` preserves all output. The checker checks signs, branches, and denominators needed by its algebra; the written proof supplies the all-size combinatorics, absolute-convergence majorant and transfer to permutations. Thirteen rejection controls are useful regression controls, not a completeness proof for the checker.

Fresh enumeration and independent coefficient checks:

| Check | Result |
|---|---|
| Recompiled C++ maximum-insertion traversal, n=0 through 13 | PASS against OEIS A061552; all five A,F,S,T,P marginal coefficient polynomials match the formal tower. At n=13: 173,453,058 avoiders and 243,035,536 domino roundtrips. |
| Extended fresh traversal, n=0 through 14 | PASS. At n=14: 1,209,639,642 avoiders and 1,390,594,458 domino roundtrips. All five complete polynomials match. The complete run took 373.989 seconds, with 325.041 seconds at n=14. |
| Original enumeration receipts | Every integer field and coefficient of the fresh n<=14 run matches `pod_results/brute14.jsonl`; timing fields intentionally differ. |
| Python permutation/cut enumeration through n=7 | The supplied independent Python traversal and its formal tower agree in every coefficient of all five series. |
| New exact F check | `independent_exact_checks.py` imports no submission code. A decreasing top cell with k points and a Catalan bottom cell on n-k points gives `[z^n u^k] F_0=binomial(n,k) Cat_(n-k)`. All 120 coefficients through n=14 agree. |
| New exact actual-object F and P check | The same new script uses combinations of actual entries to recognize patterns, enumerates all permutations and value cuts through n=7, and counts internal nonempty strips directly between consecutive nonleaves. Every F and P coefficient agrees. |
| Leaf/block marking control | `audit_v2_marks.py --max-n 7` agrees coefficientwise with actual dominoes at every size. This supports the marking interpretation, not the withdrawn tilted theorem. |
| Envelope controls | All 1,068,643 finite integer majorization tests pass, including parity cases and rejection of a deliberately invalid envelope. |
| New physical pairing check | `independent_pairing_check.py` tests 5,313 pairs through input size 5: balance, cell avoidance, global 1324 avoidance, additive leaves and the stated empty/two-leaf boundary bounds all pass. It also finds a concrete unequal-output-profile witness, recorded in the premise audit. |

The C++ runs were invoked with `nice -n 10`; the inherited process priority was already lowered, and a process snapshot showed effective NI=20. Thus these ran at a lower priority than requested, with one enumeration worker. They remained well within the 30-minute allowance. No pod or other remote computation was used. The code caps its own supported range at 14, so I did not extend it beyond that range.

The live [OEIS b-file](https://oeis.org/A061552/b061552.txt) agrees at every n=0,...,14. Its endpoint values include `a(12)=25431452`, `a(13)=173453058`, `a(14)=1209639642`. Direct urllib retrieval received HTTP 403; the web tool successfully retrieved the b-file and the sequence page. The independent script records these live reference values explicitly.

Additional exact algebra and diagnostic checks:

- `independent_algebra_checks.py` uses SymPy exact symbolic algebra to compare H0,H1,H2,H3 with `(1/j!) d^j(z^j H)/dz^j`, including the closed expressions used by the checker; verify R and V as the corresponding divided differences of g; verify the critical discriminant `(2v-9)(2v-1)^3/729`; and verify the local coefficients `rho-z=(16/81)(w-1/2)^2+...`, `D` singular coefficient `2187/16`, and the first-moment normalization. All pass.
- Norton v3's baseline certificate passes at 256 bits with positive exponent about `1.27885367023e-7`; all seven baseline corrupted certificates reject.
- The ordered-placement diagnostic reproduces joint counts 1196 and 1205 for the same unordered profile; both corrupted totals reject. This does not contradict Harris, which is applied to actual neighbors at a fixed positive z.
- The printed v2 normalization counterexample passes exactly: R=8/81 while the asserted upper bound is at most `1376/373977`, with strict difference `35560/373977`. Its corrupted R control rejects. The appendix already uses the corrected normalization; this is separate from the documented withdrawal causes.
- The retained old-profile obstruction passes, giving exponent at most approximately `-0.00200072633016` at the target for every kappa in that reduced model; a corrupted profile rejects. This is not an upper bound on C30 and does not contradict the new four-coordinate envelope.
- I checked the proof's derivative-ratio argument: the bad-family weighted second derivative is bounded by `z M'(z)/s`; the BBEP bad leaf/empty events are `o(D_n)` and hence contribute `o(z^2 D''(z))`; the boundary term has finite first derivative. Positivity then gives radius rho for the good family without inferring concentration from a mean. The balancing injection, integer envelope, common coefficient sequence, and fixed-grid radius argument use only the resulting limsup subsequence. No additional unjustified mathematical item was found in that chain.

External sources, withdrawal audit and credit:

I downloaded the full online Norton v1, v2 and v3 HTML texts and each version's abstract/Comments, also the current unversioned abstract. The history lists those three versions, latest 4 September 2026. I inspected the relevant structural, marginal, tilted-family, entropy, kernel, concentration and appendix arguments and compared their dependencies with the candidate. The new BBEP v3 download matches the archived version. The complete premises table records the exact result and necessary hypotheses for each imported BBEP/Norton ingredient.

The candidate uses none of the withdrawn v1 transfer/vertex argument, the v2 claim of identical post-pairing profiles, the v2 Appendix F endpoint-only winding test, or v2's full tilted profile/concentration theorem. It does reuse and rebuild the v2 marginal equations, kernel cancellations and local algebra. The packet should credit this mathematical ancestry precisely, rather than describe all the analytic setup as independent of v2. BBEP retain credit for the published domino and staircase framework, exact enumeration, leaf/empty concentration, physical pairing, coefficient inequalities and coefficient-extraction lemma; Norton retains credit for the two-axis relaxation and Harris count. Reuse of a correctly re-proved part of a withdrawn paper does not validate its withdrawn headline bound.

Current public bounds and priority:

| Source checked live | Finding |
|---|---|
| [Constant 30 page](https://teorth.github.io/optimizationproblems/constants/30a.html) and raw main files | Still lists lower 10.27 and upper 13.5. Its webpage bytes match the packet's snapshot. |
| [Open PR #313](https://github.com/teorth/optimizationproblems/pull/313) | Proposes lower 10.412263 from Norton v3. Created 3 November 2026 at 14:21:59 UTC. No review or review comments were present when checked. The author credits Norton. |
| [Earlier PR #223](https://github.com/teorth/optimizationproblems/pull/223) | Closed at the time of the audit, superseded by split PRs including #313; comments explain the split. It is not another independent mathematical lower-bound claim. |
| [Norton v3](https://arxiv.org/abs/2608.20292v3) | Unwithdrawn, unrefereed lower-bound claim 10.412263. Its earlier 10.617 and 10.466425 claims are withdrawn. Search-result snippets still repeat 10.617, so current versioned primary sources matter. |
| [Franklín, 22 December 2025](https://arxiv.org/abs/2512.19462) | Conditional lower bound 10.418, under a weighted-quotient counting conjecture. Below 10.42 and not unconditional. |
| [Brignall, 1 October 2026](https://arxiv.org/abs/2610.02535) | Public preprint upper bound 13.167248, stronger than the live table's 13.5. This upper-bound proof was identified, not independently refereed here. |
| [Meng v2, 9 September 2026](https://arxiv.org/abs/2609.06717v2) | Improved regions of inversion monotonicity, including k<=2n+6 and certain growing regions. The unrestricted conjecture remains open; this is not a proof of the conditional global upper bound near 13.002. |

Using `~/dev/.bin/gh`, I fetched all 58 open repository items (52 PRs, 6 issues), every open PR's file list/patches, comments for all open items that had comments, and the reviews/review comments for the relevant #313 and historical #223. The scan covered 71 additional API collections without errors. Only #313 changes constant 30; other matches were unchanged README context or unrelated numerical text. Raw data are retained in `review_sources/github/`, with `github_audit.json` and `github_c30_changes.json` recording the scan.

The arXiv recent-first search for 1324 returned 50 items, spanning beyond 2025; I inspected all 16 results with 2025–2026 identifiers. Other relevant results concern subclasses, cyclic permutations or involutions, not a stronger growth bound for the full class. Web searches covered 1324 growth/lower/upper bounds in 2025–2026, Norton withdrawals, 10.42 and 13.167248; the query results led back to the primary sources above. I found no unwithdrawn unconditional public lower bound stronger than 10.42 in this search. There are stronger *conditional* historical numbers (for example 10.607 under Stieltjes/continued-fraction hypotheses) and the withdrawn Norton numbers, which should not be counted as unconditional competitors. This is a scoped search, not an exhaustive priority certification.

Reproduction and evidence:

The environment was Python 3.12.13, python-flint 0.9.0, SymPy 1.14.0, macOS arm64. BLAS thread limits in replay were one. The main commands were:

```sh
cd submission
~/dev/open-science/.venv/bin/python check_manifest.py
TASK_PYTHON=~/dev/open-science/.venv/bin/python bash replay.sh
nice -n 10 clang++ -O3 -std=c++17 brute_gate.cpp -o ../review_brute_gate
nice -n 10 ../review_brute_gate 13
nice -n 10 ../review_brute_gate 14
nice -n 10 ~/dev/open-science/.venv/bin/python check_tower_counts.py ../review_logs/brute13.jsonl
nice -n 10 ~/dev/open-science/.venv/bin/python check_tower_counts.py ../review_logs/brute14.jsonl
nice -n 10 ~/dev/open-science/.venv/bin/python check_profile_envelope.py
nice -n 10 ~/dev/open-science/.venv/bin/python audit_strip_encoding.py --max-n 7
nice -n 10 ~/dev/open-science/.venv/bin/python audit_v2_marks.py --max-n 7
cd ..
nice -n 10 ~/dev/open-science/.venv/bin/python independent_exact_checks.py review_logs/brute14.jsonl
nice -n 10 ~/dev/open-science/.venv/bin/python independent_algebra_checks.py
nice -n 10 python3 independent_pairing_check.py
```

`replay.sh` executes the baseline, its controls, ordering, v2 normalization, reduced obstruction, archived n14 tower comparison, mean, candidate and candidate controls. The extra tower checks above use newly enumerated data. stdout/stderr are retained under `review_logs/`. Initial operational retries: BeautifulSoup was unavailable, so downloaded HTML was read with the standard-library parser; direct OEIS urllib access returned 403 and was replaced by successful web retrieval; an initial leaf/block audit invocation from the workspace root completed its coefficient comparisons but failed to write a relative receipt, then succeeded when rerun from `submission/`. No mathematical test failed.

Key SHA-256 values:

| File | SHA-256 |
|---|---|
| Original MANIFEST.json | `f06ac15cf9a02b47ebba40525821731963f1e577e16449faaf45647ed3086e03` |
| BAR.json | `2d3511f185f4c3569332082544a2bb146a64120c879d32633f73fab2da97960e` |
| Candidate certificate | `e219af1a3d05c5c7b9bd8dc88000d94e9a1513ab3ba5e8f54cef2668ef3267e5` |
| Mean certificate | `9e723705ee52191f0e79a042dcef8c923d192b30ef151761d7c78298ea46546d` |
| Candidate verifier | `7366c972e04fb5bc541edeaf4921a094eb3db241cc5841e45696534e28554d6b` |
| Mean verifier | `0a370b570a238851a216333c6ecb749689b33889879f9ac034bf1326b7e97d59` |

`review_logs/hash_audit.json` records all 32 source-hash checks; `review_sources/retrievals.json` records primary download times and hashes. The source-audit corrections above are required before describing this packet as having passed its external-premise gate. The checked arithmetic and candidate mathematical route survive these particular corrections.

VERDICT: FLAG
