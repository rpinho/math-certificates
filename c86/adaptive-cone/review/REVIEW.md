# C86 round4 adversarial review — math_review_c86r4_1102

**Overall mathematical verdict: PASS for C86 <= 1.80560940. Subjective probability that the bound is correct: 99%.** No FALSE proof step found. There are scoped GAPs in inaccessible auxiliary literature, historical optimizer/pricing runs and retrospective resource histories; none is a missing hypothesis for the frozen bound.

The independently reconstructed bound is

    C86 <= 288897505229428473/160000001279369600
         = 1.8056093932461669... < 1.80560940.

Its exact improvement over the previously reviewed round 3 certificate is

    15977168934617659866004718423/80000000639675999999929634672000
      = 0.0001997146100858127... .

Frozen input: `input/certificate.json`, byte-identical to target `frozen/adaptive_checked-10d68ec249f47c05.json`, SHA256 `10d68ec249f47c0504182d419fd8ddd1ca1c917e42a4bba59d944b9d1de0dad5`. The bound is an upper bound for the smallest limiting normalized trace, as the target says, not an inequality about every individual totally positive algebraic integer.

## Independence and exact checks

I read the target proof and Smith's actual primary theorem statements, then wrote my own derivation and complete certificate checker before opening either submitted verifier. The own full check was bound at **2026-11-02 12:14:42 UTC** in `receipts/pre-verifier-binding.json`. The original derivation draft is preserved in `input/OWN_DERIVATION.pre-verifier.md`; `OWN_DERIVATION.md` corrects an approximate manually entered timestamp. I read the prior review report for comparison, but opened no earlier-review implementation. The checker imports no search, earlier-review or submitted-verifier code.

| Reconstructed quantity | Exact result |
| --- | --- |
| Mass m | `50000000399803/50000000000000` |
| First moment T | `288897505229428473/160000000000000000` |
| Weighted auxiliary degree beta | `89509133300897/100000000000000` |
| m-beta | `10490867498709/100000000000000 > 0` |
| Positive-density cells / rational nodes | 3791 / 5375 |
| Actual support hull | `[17/320,5237/1000]` |
| Selected auxiliaries | 28, all monic; 10 with nonreal roots; largest degree 21 |

All 28 arrays independently pass integer coefficients, primitive content, irreducibility, distinctness, positive weights and certified complete root counts. Direct 256-bit Arb integration on each linear density segment gives a strictly positive logarithmic integral for each polynomial. The minimum is index 17, `8.94715228390199433334239652057456...e-8`; the full interval has radius below 5.5e-68. Leading coefficients are explicitly included in the formulas, so there is no hidden monicity assumption in the general argument.

`AUXILIARIES.md` gives **every auxiliary a PASS verdict**, with its exact array, weight, degree, nonreal-root count, direct integral and exact primary TeX line. Only indices 24, 25, 27 are newly active versus round 3; they are classical Flammang first-list entries 58, 64, 83, degrees 15, 16, 21. The old degree 13 entry 41 drops out. The 139-polynomial working pool is byte-identical to round 3, SHA256 `4319a326fc651dc2d3988266953da5c394357302beb9363e7193da101a376bea`.

## Full support and Smith's criterion

My fresh continuous checker proves positivity on **all 3791 closed support cells**, using 15,345 closed rational leaves, 26,899 tests and maximum depth 7. Its conservative saved minimum lower bound is greater than `1.78e-9`. This is an enclosure floor, not an estimate of the actual minimum. A separate standard-library rational auditor checks every parent, both endpoints, every adjacency, absence of overlap and safe serialization; all seven corrupted-cover controls reject. Receipts: `own-integrals.json`, `own-cover-0.json` through `own-cover-7.json`, `own-cover-audit.json`.

The own implementation reconstructs exact slope jumps and uses H(u)=u²(log|u|/2-3/4). It sums normalized Taylor coefficients before taking a quadratic minimum. Far-knot and root-log tails are geometrically bounded. For near knots it rescales H(rv), bounding the remaining normalized expression by 30r²|jump|; this includes a knot or endpoint without differentiating across log0. It uses a maximum-distance lower bound near auxiliary roots. Direct-cell antiderivatives, rather than the same slope-jump formula, check auxiliary integrals. The derivation is in `OWN_DERIVATION.md`; every acceptance uses rational or Arb inequalities.

For completeness, the global deduction is independently checked. The bounded compact density gives a continuous finite logarithmic potential V on C. The difference f=V-sum b_j log|Q_j| is harmonic off the actual support and auxiliary roots, tends to positive infinity at those roots, and behaves as `(m-beta)log|z|-sum b_j log|lc Q_j|+o(1)` uniformly at infinity. The minimum principle extends the verified support inequality throughout C, including all open support gaps and nonreal points.

For every other primitive irreducible integer P, leading coefficient c, the resultant identity gives

    integral log|P| dmu
      >= (m-beta)log|c| + sum_j b_j log|Res(P,Q_j)| >=0.

The resultants are nonzero integers. Selected polynomials require their separate direct checks; integer contents and factorization handle all remaining nonzero integer polynomials, with no degree restriction. Divide **both** measure and weights by m. Smith's Proposition 5.15 applies with the correct sign convention. On the positive interval Sigma = `[1/1000,13]`, capacity = `12999/4000>1`, Theorem 1.5 gives infinitely many distinct irreducible monic integer polynomials with all roots positive and conjugate distributions approaching mu/m. The continuous function x carries their normalized traces to T/m. This is the required upper bound. Primary statement: [Smith, Theorem 1.5 and Proposition 5.15](https://arxiv.org/html/2111.12660v2).

## Every changed step, with exact target lines

# Round4 changes requiring a verdict

References below are exact lines in ../c86r4/REPORT.md and ../c86r4/PROOF.md. Certificate arrays are one physical line: frozen/adaptive_checked-10d68ec249f47c05.json:1, with exact A[j]/b[j] locators in AUXILIARIES.md. Earlier-round comparison uses ../c86r3/REPORT.md and ../review_c86r3/REPORT.md. The basic Smith/resultant theorem and all four submitted proof/coverage files are inherited unchanged; new data require all hypotheses to be checked again.

| New step or changed premise | Exact target lines | Verdict | Independent evidence |
| --- | --- | --- | --- |
| Lower exact ratio, improvement and upward rounding | REPORT3,5,35,37 | PASS | Direct rational trapezoid reconstruction yields the exact headline fraction; exact gain over the frozen baseline agrees. |
| New5375-node positive measure,3791 support cells and changed support hull | REPORT10,18; PROOF3,7 | PASS | Own structure and full-support audits; endpoints17/320 and5237/1000. Every positive cell is covered. |
| Actual mass and weighted degree, rather than assumed unit mass | REPORT10,18,49; PROOF8 | PASS | m=50000000399803/50000000000000; beta=89509133300897/100000000000000; m-beta=10490867498709/100000000000000>0. |
| Changed active set:28 auxiliaries,10 with nonreal roots,maxdegree 21 | REPORT11; PROOF3,9 | PASS | All 28 independently integer, primitive, irreducible, distinct, positive-weight, complete roots and directly positive integrals. AUXILIARIES.md gives each verdict/source/array. New activation only at24,25,27; classical F19 entries 58, 64, 83. |
| Positive direct integrals for the new density | REPORT12,18; PROOF9 | PASS | Fresh256-bit direct-cell integration; minimum8.94715228390199e-8 at final index 17. All nonreal roots included. |
| Potential positivity on every point of the entire closed new support | REPORT12--14,18; PROOF10,13 | PASS | Own pre-verifier15345-leaf proof, 26,899 interval tests; independent endpoint auditor covers all 3791 cells with no gap or overlap and rejects7 corruptions. |
| New support still permits global minimum principle, resultants and Smith normalization | REPORT18; PROOF13--25,35 | PASS | Own proof in OWN_DERIVATION.md. Root singularities are positive infinity; strict degree deficit controls infinity. Normalize both density and weights. Positive ambient interval[1/1000,13] has capacity12999/4000>1. No untested gap boundary, real-root restriction or degree cap remains. |
| New frozen binding and two inherited analytic paths | REPORT9,12--15,20--22 | PASS | Own check finished before source inspection; frozen SHA10d68ec... verified. Both kernels/scheduler/auditor byte-match round3. Fresh supplied replays/cover audit retained. |
| Baseline and six intermediate feasible improvements | REPORT28--34,37 | PASS | Exact fractions, hashes, counts, all active polynomial sources and fresh first-kernel complete-support replays. These establish feasible values only. |
| Adaptive3881 columns beats full1500's4604 columns by6.72702016864e-6 | REPORT35,39 | PASS | Column counts independently read from cone data and literal extension; exact bound difference. No optimizer necessity/optimality assertion is made. |
| Pure78-hat control stays inside old support and improves bound | REPORT29,41,45; METHOD21 | PASS | Fresh exact support-subset audit plus complete certificate replay;51 old closed support components. |
| Mixed hats are mostly support extensions, not a refinement ablation | REPORT30--32,45 | PASS | Independent exact counts: gap104/106 extend support, midpoint98/176, boundary204/218. The target's interpretation and limitation are correct. |
| Proper full500/full1500 cones restore all3068 old directions and broad triangle | REPORT33--34,47; PROOF37; METHOD15 | PASS | Fresh exact rational interpolation audit includes every old and selected hat, plus broad triangle; new-knot slope jumps-64000000 witness strict enlargement. |
| Adaptive300 keeps every full500 column and adds300 new directions | REPORT35,47; METHOD19 | PASS | Fresh literal-column comparison:3581 old columns +300. A new center63/500 gives a nonzero slope kink where all old columns are affine. |
| Further refine100 cone contains all4604 full1500 directions and adds100 | METHOD23 | PASS | Independent exact literal inclusion and a new-center slope kink prove proper enlargement. It produced no stronger accepted bound. |
| Primal/Devex and adaptive-IPM pilot details | METHOD23; REPORT51 | GAP | Reconstructed528 cuts and solver-budget histories were not independently replayed. The final bound uses none of these incomplete pilots; no stronger accepted certificate is claimed from them. |
| New floating exports are certified after clipping/rounding | REPORT49 | PASS | Acceptance uses the exported rational measure, not LP normalization or floating residuals. Its exact ratio and all analytic obligations pass independently. Historical arithmetic rounding implementation is unnecessary to the bound. |
| Eight lists,513 source rows,378 union and239 additions | REPORT55 | PASS | Independent primary-source parsing/manual comparison and exact factorization; fresh source bytes match. Full per-list credit in sources/primary-reading.md. |
| Additional239 inputs have positive costs at the final saved dual | REPORT57 | PASS | Own root-form replay using standard-library NPZ reader and math.fsum: minimum0.015547413236567695, maximum difference1.8e-15. This is a floating diagnostic, not a rigorous global exclusion. |
| Earlier-dual pricing, LP paths, pilots and causal history | REPORT39,49,51,57; METHOD9,23 | GAP | Did not rerun optimizers or all earlier dual/pricing histories. Saved feasible results, geometry and final pricing are verified. The target correctly disclaims LP optimality and labels uncertified pilots UNVERIFIED. |
| Credit for every new list and for the inherited mathematics | REPORT55,57,61,63 | PASS | Flammang three trace lists plus Rhin/sector lists; Liang--Wu Table1; Flammang2009 Table1; Aguirre--Peral2007 Table2. No polynomial discovery or first-complex-auxiliary claim. Smith, Orloski--Sardari and computational predecessors credited. |
| Auxiliary-source coverage beyond those lists | REPORT59 | GAP | Inaccessible Wang--Wu--Wu2021 and other-power lists; incomplete AP08/Wang--Pang--Wu2023 and unaccepted Smyth scan. Acknowledged coverage gap, not a missing condition for this certificate. |
| New negative-integral and potential controls | REPORT14; METHOD25 | PASS | Own structural controls and negative analytic witnesses; both supplied integral paths reject the rebound density corruption for E4. Wrong-bound and raised-weight controls reject for intended reasons. |
| Public status and absence of a stronger identified public upper | REPORT67--69 | PASS within stated scope | Fresh raw table, all46 open PR bodies/titles,12 unchanged repository HEADs/READMEs, canonical C86 directory, relevant conversation pages, repository/paper/community search. API comment-rate failures replaced by HTML reads. No worldwide-priority inference. |
| Original job's resource/search history | REPORT94--98 | GAP | Historical runtime/peak-memory history cannot be independently recovered as a continuous measurement. The target itself discloses its guard failure. No impact on validity of the frozen mathematical data; our own receipt-backed pod runs are separate. |

No FALSE mathematical step found. Overall verdict concerns the bound: PASS. The GAP rows delimit experimental-history replication and literature coverage; they are not omitted hypotheses in the proof.

## Fresh replays and hostile controls

After the independent pass, I inspected and replayed the submitted kernels. Both kernels, scheduler and old cover auditor are byte-identical to round3. `verifier_review.md` gives exact implementation lines and checks the Taylor coefficients, remainder signs, near-knot chord/tangent treatment, complex-root distances and closed bisections. No incorrect acceptance condition was found.

| Artifact | Complete first-kernel proof pieces | Fresh runtime, seconds | Verdict |
| --- | ---: | ---: | --- |
| Round3 baseline | 7,954 | 362.9 | PASS |
| Pure support refinement | 8,173 | 383.1 | PASS |
| Gap family | 8,244 | 378.7 | PASS |
| Boundary family | 9,899 | 441.8 | PASS |
| Mixed midpoint | 9,226 | 421.1 | PASS |
| Full500 cone | 9,032 | 487.9 | PASS |
| Full1500 cone | 10,804 | 694.2 | PASS |
| Final adaptive certificate | 10,243 | 533.0 | PASS |

The inherited independent kernel separately passes the final certificate with **15,332 closed pieces**, 26,873 tests, depth 7,192-bit Arb and four workers (826.0s under concurrent load). Its minimum proven leaf lower is approximately 1.29174361953e-10. Its saved cover SHA256 `1567b41f92b21bebacdea7f84a76f451b4f69525ec298d281868c01206554b9c` exactly matches the target's original cover. Our own proof uses a different near-knot enclosure and different accepted leaves. Fresh independent rational and supplied cover/hash audits both pass; five and four altered-cover controls respectively reject.

All seven improved frozen artifacts' exact ratios, gains, hashes, node/cell counts and source matches independently agree with `comparison-accepted.json`. Their 32 unique selected polynomials all pass exact primitive irreducibility and complete root classification (`all-frozen-facts.json`). Replays verify feasible certificates; they do not reconstruct LP optimality or a causal attribution of the gain.

My own 11 structural controls reject, and two substantive analytic controls give certified failures while structure still passes:

- Multiply every auxiliary weight by 1001/1000: f(5) is enclosed around `-0.00090963059659501745491414188591764`.
- Lower last positive density node 5358 by 1%, recomputing exact mass, trace and declared ratio: the log(x) integral is enclosed around `-4.72174270792132418177918870108e-6`.

The submitted wrong-bound and raised-weight controls also reject for their intended reasons. Both submitted direct-integral paths reject the rebound density corruption for E4, with a certified negative integral rather than a malformed file or execution error. Receipts: `own-controls.json`, `review-final-negative-controls.json`, `review-final-negative-integral-control.json`, `replayed-cover-own-audit.json`, `replayed-cover-supplied-audit.json`.

## Classical sources and credit

| Source list | Rows | Change versus prior round | Transcription/integrality/irreducibility/source credit |
| --- | ---: | --- | --- |
| Flammang arXiv1907.09407v1 first trace list |97| Inherited; independently revalidated | PASS |
| Same note, second list |74| New collection in this round | PASS |
| Same note, third list |62| New collection in this round | PASS |
| Flammang arXiv2401.12951, Rhin list |45| New collection | PASS |
| Same paper, sector table |67| New collection, including repeated rows across sectors | PASS |
| Liang--Wu2011 Table1 |85| New collection | PASS |
| Flammang2009 Table1 |38| Full35 numbered plus 3 starred entries, beyond prior partial matches | PASS |
| Aguirre--Peral2007 Table2 |45| New collection | PASS |

Total 513 source rows, union 378 canonical inputs with the inherited 139 working polynomials, 239 additions. Every final auxiliary occurs literally in the first Flammang list. Fresh arXiv TeX and fresh publisher/institutional PDFs match the stored hashes. My own parser was rerun on newly extracted primary PDF text: every Liang--Wu and AP07 coefficient matches, including the printed mixed signs. Flammang2009's complete indexed primary Table1 was manually compared; direct PDF access failed, so no raw-PDF hash is claimed. `sources/primary-reading.md` and `fresh-primary-source-audit.json` distinguish these evidence paths.

The target credits each list author and makes no polynomial-discovery claim. Flammang's earlier complex-root auxiliaries and Wu's method are prior work; the starred Chebyshev rows also have earlier context. Smith's criterion, Orloski--Talebizadeh Sardari's method, and Tomar/Pinho/Koshta/Giraudin infrastructure retain their credit. The collection of known lists and reuse of their polynomials does not transfer authorship. All list-credit verdicts are PASS. Missing Wang--Wu--Wu2021 and other-power lists remain explicitly acknowledged coverage GAPs.

## Public comparison

The required prior-art file preceded review code. Initial live checks read the raw table, 46 open PR bodies/titles, open issues, updated repository search and 12 official/rival/lab repository HEADs/READMEs. API comment requests later hit the public rate limit; fresh public conversation HTML for all five relevant C86 PRs succeeded. Recent arXiv and indexed community searches found lower-bound reports and the known upper certificates, with no stronger upper identified. The scope and access limitations are recorded in `PRIOR_ART.md`.

Final refresh **2026-11-02 12:31:19--12:31:24UTC** independently reread the raw table, canonical C86 README, open PR/issue pages, repository search and PR298, and obtained all 12 HEADs with git ls-remote. All pins remain unchanged. The [official table](https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/86a.md) still gives Koshta's 1.8084990*; [PR298](https://github.com/teorth/optimizationproblems/pull/298) and the [canonical C86 repository](https://github.com/rpinho/math-certificates/tree/main/c86) give Pinho's 1.80580911 as newest. Giraudin's 1.80220 and Tomar's 1.8022225 are lower claims. No worldwide novelty or exhaustive-priority claim follows. Receipts are under `sources/public/` and `sources/public-final/`.

## Exact reproduction

All numerical integration, factorization/root isolation, continuous potential proofs, geometry and floating pricing ran on **a rented pod**, own directory `the job directory`, through own detached tmux sessions. `run_remote.sh` sets nice 10, single-thread numerical-library environment variables and affinity to eight permitted CPUs. The address-space cap was tightened to about 3 GB per process; an own-cwd snapshot records aggregateRSS below 0.3 GB. No worker group used more than eight cores. Local work was editing, inspection, public-source reads and lightweight standard-library rational receipt/cover assembly checks. No heavy local computation occurred.

Python3.12.3 and python-flint0.9.0 were used. PDF re-extraction additionally uses pypdf6.21.4, pinned separately; retained fresh extracts make that package unnecessary for a certificate replay. Stage only into this own job, without deletion, then run in tmux:

```sh
rsync -az input sources receipts *.py *.sh requirements*.txt a rented pod:the job directory
ssh a rented pod
cd the job directory
test -x venv/bin/python || uv venv venv
UV_CACHE_DIR="$PWD/uv-cache" uv pip install --python venv/bin/python -r requirements-review.txt
tmux new-session -s review_c86r4_reproduce
```

Inside tmux, the mathematical replay commands are:

```sh
bash run_remote.sh own_check.py input/certificate.json --output receipts/own-integrals.json
bash launch_own_cover.sh
bash run_remote.sh cover_audit.py
bash run_remote.sh own_controls.py
bash run_remote.sh source_audit.py
bash run_remote.sh source_audit_fresh.py
bash run_remote.sh source_anchors.py
bash run_remote.sh frozen_facts.py
bash run_remote.sh geometry_audit.py
bash run_remote.sh refine100_audit.py
bash run_remote.sh own_pricing.py
bash launch_replays.sh
bash run_remote.sh audit_replayed_cover.py
bash run_remote.sh audit_artifact.py input/certificate.json receipts/replay-final-independent.json --output receipts/replayed-cover-supplied-audit.json
bash launch_controls.sh
bash run_remote.sh final_process_audit.py
```

The launcher waits for its own child processes and records exit receipts/PIDs; this reproduces the staged frozen files rather than rerunning LP searches. Pull receipts and logs back with rsync, without deletion. After this pod's expiry, reproduction requires an authorized replacement and adjustment of only the own-job cwd/allowed CPU list. Full certificate/data retention is below 50 MB; `MANIFEST.json` hashes every retained input, code and receipt.

## End state and next action

The remote own-cwd audit at **2026-11-02T12:41:29.039156+00:00**, using `ps -axo pid,ppid,pcpu,command`, found zero remaining own scientific workers. The local audit also found none. The audit session itself exited 0; the pod was left running. No other job was modified or controlled; no commits, pushes, PRs, posts or external messages were made. This review finished well before the 15:04 UTC task deadline and 18:05 UTC pod expiry. STATUS.md was initialized and updated during the review; elapsed work was under one hour.

Development errors in source-title matching and inherited-hat indexing were corrected before the successful audits; failed logs are retained. They were review implementation issues, not certificate failures. Independently written AI programs share the FLINT/Arb arithmetic dependency; this is neither independent human peer review nor a formal proof-assistant verification.

No numerical or mathematical repair is indicated. Retain the candidate/unrefereed qualification. The useful next work is to obtain the missing classical lists and, if pursuing publication, have a human check the theorem application and enclosure arguments. The historical optimizer/resource GAPs should remain distinct from the completed certificate proof.

**Overall verdict: PASS for C86 <= 1.80560940. Probability the bound is correct: 99%.**
