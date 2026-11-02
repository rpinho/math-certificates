# Fresh adversarial review of C89b

**PASS for the claimed upper bound.** Independent exact arithmetic gives

\[
 C_{89b}\leq \frac{2405659597}{1427496763392}
 =0.001685229458092571557325284071\ldots <0.00168523.
\]

My probability that this mathematical inequality is correct is **99.9%** (a subjective assessment, not a statistical confidence interval). I found no false step or essential proof gap. Priority is less certain: no stronger applicable public bound or contradictory lower bound was found in the bounded audit documented in [PRIOR_ART.md](PRIOR_ART.md). This is independent computational review, not a formal proof-assistant verification or journal referee acceptance.

The full certificate was recounted with reviewer-written code before reading the author's verifier or search code. I had read the stated proof, including its coefficient table, and the certificate schema first; this was not a blind review of the written proof. No author code was imported or executed. The first counter's pre-inspection hashes and timestamp are in `receipts/independent_code_before_author_verifier.sha256` and `receipts/independence_timestamp.txt`. After obtaining and pulling its successful receipts, I read the author verifier and wrote a second, direct ordered-tuple counter as an additional check.

## Verdicts with exact target lines

Line numbers below refer to the unchanged target `../sweep2/REPORT.md` and `../sweep2/frozen/PROOF.md`; copies are retained as `inputs/target_REPORT.md` and `inputs/target_PROOF.md`.

| Step | Target lines | Verdict | Reason and independent evidence |
| --- | --- | --- | --- |
| Definition and normalization | PROOF 9–15; REPORT 5–8 | **PASS** | PR #277 defines both colors' homogeneous five-element sets divided by binomial(n,5); extracted constant page `sources/pr277_constant.md`, lines 5–11. The ordered graphon sum divided by 192^5 has exactly this limit. No extra factor 2 or 5! is required. |
| Admissible step graphon | PROOF 7 | **PASS** | Frozen matrix is symmetric, 192 by 192, all weights equal and positive, all entries 0,5,7, denominator 7; all diagonal entries zero. SHA256 matches the manifest. `receipts/candidate.json`, lines 2–12; all ten manifest entries checked in `receipts/author_manifest_check.json`. |
| Repeated blocks and counting formula | PROOF 11–21; REPORT 18 | **PASS** | Independent multiset enumeration retains repetitions, restores ordered multiplicities, and checks each of ten pair factors. Small literal ordered-tuple controls agree exactly. A second full ordered enumeration agrees without any multinomial correction. |
| Coefficient table and polynomial | PROOF 23–37 | **PASS** | Both red and blue histograms match every listed coefficient; all other exponents vanish. `receipts/candidate.json`, lines 25–50. |
| Exact fraction, rounding, improvement | PROOF 39–43,53; REPORT 5–8 | **PASS** | Exact sum matches 2405659597/1427496763392. PR #277's full fraction is independently reproduced from its byte-identical live artifact. Relative improvement is 0.1052561299684265792... percent. `receipts/candidate.json`, lines 13–23,52–61; `receipts/baseline.json`. |
| Blow-up limit and upper-bound direction | PROOF 15 | **PASS** | Detailed finite calculation below supplies the argument, including existence of the minimum-density limit and why some deterministic coloring attains at most the random expectation. Fractional entries are allowed. |
| Optional fine certificate | PROOF 45–49; REPORT 10 | **PASS** | Independently recounted exact fraction agrees; support is identical to the simple certificate. `receipts/fine_candidate.json`; `receipts/structure.json`. |
| Structural 6+6 split and folded cubes | PROOF 57; REPORT 14–16 | **PASS** | Every row splits the old 12-neighbor probability class into six retained and six saturated entries. Explicit maps verify every adjacency and nonadjacency against Q7 modulo antipodes in three components of size 64. `inspect_structure.py`; `receipts/structure.json`. This is more than retuning a common scalar probability. |
| Claimed numerical search diagnostics | REPORT 16,20; PROOF 57–59 | **GAP: not independently replayed** | I did not reproduce the Hessian eigensolver, gradient, clone-splitting or signed-lift runs. These are explicitly described as numerical diagnostics, not proof inputs or optimality certificates. This gap does not affect the bound. |
| Comparison and prior art | REPORT 8,55 | **PASS for the bounded comparison; GAP for exhaustive priority** | The live #277 baseline is reproduced and beaten. Current tables, all open item titles, relevant PR diffs, specified rival indexes and primary papers yielded no stronger applicable value. Unauthenticated GitHub code search requires sign-in, and community indexing is incomplete. An exhaustive record/priority claim would require more evidence; the target expressly avoids one. |

There are **no FALSE verdicts**. Both GAP entries concern claims beyond the construction-to-upper-bound proof.

## Exact independent recount

For the preferred 5/7 certificate:

| Quantity | Exact density | Decimal |
| --- | --- | --- |
| Red K5 | 1943005 / 2427715584 | 0.0008003429284737828663... |
| Independent five-set, equivalently blue K5 | 1263172657 / 1427496763392 | 0.0008848865296187886910... |
| Sum | 2405659597 / 1427496763392 | 0.0016852294580925715573... |

The first counter enumerates nondecreasing block words with zero-product pruning. Each word contributes 120 divided by the factorials of its repeated-label multiplicities. Integer histograms record counts of fractional edge factors; Python `Fraction` evaluates the resulting rational sums. It uses no transitivity or other graph symmetry. There are only 192^5 ordered words in total, so the unsigned 64-bit histogram coefficients cannot overflow. The 156 small color controls include 144 comparisons against literal ordered 5-tuples with exact products, fractional diagonal entries, and 12 constant-graphon identities. They include the normalization check W=1/2, whose two-color density is 1/512.

The second counter, `ordered_recount.cpp`, directly enumerates every nonzero **ordered** block word and multiplies the ten integer matrix entries. It has no histogram evaluation, occupancy composition, or permutation correction. Its raw numerators are

- red: **58987862017781760**;
- blue: **65218998823523328**;
- common denominator: **192^5 times 7^10**.

These reproduce both separate fractions above (`receipts/ordered.json`). Arithmetic uses unsigned 128-bit integers; with the enforced n<=256, D<=10, the entire sum is at most n^5 D^10 < 2^74, safely below 2^128. The actual candidate has 259338240 nonzero red ordered words and 366670272 nonzero blue ordered words. The run took approximately 46 seconds on one pod core.

The unreduced common denominator is 73703233850355744768. The positive gap from the printed upper bound is exactly 302176211/557615923200000000 (`receipts/final_arithmetic.json`), so decimal conversion cannot reverse the inequality.

The repeated-block contribution to blue density is **847199407/1427496763392**, while the red repeated-block contribution is zero. Thus omitting repeated blocks would cause a substantial undercount; our two counters explicitly retain them. Diagonal matrix entries describe edges between different vertices within a block, not graph self-loops.

The optional p=714945/1000000 artifact gives exactly

    14656959395069207318275707929513494927 /
    8697308774400000000000000000000000000000
    = 0.001685229278993874158006081878...

The exact comparison baseline is

    107218716425177032911811117405568916263805081691166740697 /
    63555655070790142733837367909977622463036348875198349443072
    = 0.001687005134409419565485586022...

It is the value in [PR #277](https://github.com/teorth/optimizationproblems/pull/277), independently reproduced here. The live certificate and frozen baseline both hash to `19c433540936fcdf6d90256dcee9585729bcf36a443d7f76ef4b8bb91e6abc06`. The simple candidate hashes to `6f26198c6a98bb42e8f40778fd53ad0a705712dad375a35f495fbfb3d06e6cfc`.

## Finite blow-ups prove the upper bound

Write m=192 and W=R/7. For every positive integer t, make t distinct vertices in each block. Color every actual unordered pair independently red with probability W_ij, blue otherwise. For a five-element set with block occupancy vector a=(a_1,...,a_m), its expected monochromatic indicator is

\[
 P(a)=\prod_i W_{ii}^{\binom{a_i}{2}}
       \prod_{i<j}W_{ij}^{a_i a_j}
   +\prod_i(1-W_{ii})^{\binom{a_i}{2}}
       \prod_{i<j}(1-W_{ij})^{a_i a_j},
\]

with zero exponents interpreted as factors one. Its exact expected density is

\[
 E_t=\frac{\sum_{a_i\ge0,\ \sum a_i=5}
                 \left(\prod_i\binom{t}{a_i}\right)P(a)}
                {\binom{mt}{5}}.
\]

For fixed a, the quotient of binomial factors tends to

\[
 \frac{5!}{m^5\prod_i a_i!}.
\]

There are finitely many such a, so E_t tends exactly to the ordered block sum in PROOF line 11. A coupling gives the explicit error bound |E_t-c(W)| <= 10/(192t): sample five actual vertices with replacement, condition on their being distinct, and use the union bound for any repeated actual vertex. The two-color indicator expectation lies in [0,1]. This distinguishes a repeated actual vertex, which disappears in the limit, from repeated block labels, which remain.

Some deterministic coloring has density at most E_t, because E_t is the mean over finitely many colorings. Let q(n) be the minimum normalized monochromatic count on n vertices. For n>=s>=5, averaging induced s-vertex subgraphs gives q(n)>=q(s). Therefore q(n) is nondecreasing and bounded, its limit exists, and q(192t)<=E_t implies C89b<=lim E_t=c(W). The argument requires neither an optimality assertion nor a deterministic finite realization of every fractional block pair. It also proves the inequality for the fine certificate.

## Structural check

For every one of the 192 rows, the exact baseline-to-simple transition profile is:

| Old numerator, denominator 2^20 | New numerator, denominator 7 | Entries per row |
| --- | --- | --- |
| 0 | 0 | 92 |
| 1048576 | 7 | 87 |
| 706864 | 5 | 1 |
| 913211 | 5 | 6 |
| 913211 | 7 | 6 |

The p-edge graph has three components, each 64 vertices and degree seven. The reviewer script labels each component by seven-bit subsets of size at most three, representatives modulo complementation. It verifies for **every pair** that adjacency is equivalent to Hamming distance one or six. This is an explicit isomorphism to the folded seven-cube, not an identification inferred solely from degree or spectrum. All maps are retained in `receipts/structure.json`.

## Literature and contradiction audit

Checked 2026-11-01. Detailed URLs, HEADs, retrieval results and limitations are in [PRIOR_ART.md](PRIOR_ART.md) and `sources/`.

- The main optimization table has not yet incorporated a C89b row. The current public candidate is the unmerged [PR #277](https://github.com/teorth/optimizationproblems/pull/277), with exact value reproduced above. The 48 open items comprise 43 PRs and five issues. Relevant #270 and #276 concern K4; #279 introduces K6 and repeats the same K5 value.
- [PPSS, Theorem 1.2](https://arxiv.org/html/2206.04036v3) gives the certified lower bound 0.001524 and the older upper bound 2320651/1358954496. Its definitions agree with this normalization. No contradiction.
- [Kiem–Pokutta–Spiegel, Section 7](https://arxiv.org/html/2312.08049v1#S7) reports a floating-point lower bound 0.001557 from nine-vertex flag algebra computations and explicitly says it was not converted to exact rational values. It is below the candidate, even if accepted. The paper's title concerns four-color triangles, but its K5 remark is applicable and was checked directly (`sources/kps.txt`, lines 22438–22475).
- [Épi's Ramsey artifact](https://github.com/BakeLab/Epi-results/tree/main/mathematics/ramsey-c45) and [its paper, Appendix A.6](https://arxiv.org/html/2610.24944#A1.SS6) give 4427841832181/2^49 for **c45**, involving K4 in one color and K5 in the other. This is a different objective. Likewise the PPSS bound g55>0.002020 applies with a K5-free constraint; our red K5 density is positive, so it does not apply to this certificate.
- Fresh result indexes and tree metadata were read for BakeLab/Epi-results, both specified DeepMind repositories, openai/math, EinsteinArena-new-SOTA, plasma-ai/erdos and kisonecat/openai-math. OpenAI's truncated root tree was supplemented by its complete preprints tree and CONTENTS.md. No applicable stronger claim was found in the relevant public paths. Recent GitHub repository searches were sorted by update; code search required sign-in and was unavailable.
- Last-year searches included primary arXiv records for [ordered Ramsey multiplicity](https://arxiv.org/abs/2608.02299), [threshold multiplicity for odd cycles](https://arxiv.org/abs/2609.07285) and the Épi paper. These do not improve the symmetric asymptotic K5 value. Public X/Reddit and blog searches found no applicable stronger value; unindexed/private community content remains outside the audit.

The appropriate statement is “beats the strongest applicable public upper bound found in this audit,” with PPSS and Jeetu SK credited. The review does not establish exhaustive priority or global optimality.

## Reproduction and execution receipts

Copy this review directory's source files and `inputs/` to `the job directory` on the assigned pod. Do not run the mathematical enumeration on the local machine. On the pod:

```bash
cd the job directory
REVIEW_CPUS="$(python3 -c 'import os; print(",".join(map(str, sorted(os.sched_getaffinity(0))[:8])))')"
nohup nice -n 10 taskset -c "$REVIEW_CPUS" bash run_review.sh \
  > receipts/runner.log 2>&1 < /dev/null &
```

After that run completes, the structural and direct ordered checks can be reproduced under a tracked detached wrapper:

```bash
nohup nice -n 10 taskset -c "$REVIEW_CPUS" bash -c '
  export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
  python3 inspect_structure.py > receipts/structure.json
  g++ -O2 -std=c++17 ordered_recount.cpp -o ordered_recount
  python3 ordered_driver.py > receipts/ordered.json
  python3 final_arithmetic.py > receipts/final_arithmetic.json
' > receipts/additional.log 2>&1 < /dev/null &
```

Only the standard Python library and a C++17 compiler are needed. The actual commands and first-run input hashes are retained in `run_review.sh`, `receipts/input_hashes.sha256`, `receipts/runner_process.txt` and the per-run PID/error/timing files. The first launch stopped before compilation because the pod lacks `/usr/bin/time`; the corrected run uses Bash's builtin timing. Its failure receipt was preserved. The successful mathematical jobs used nice 10, single-threaded workers, an eight-CPU affinity ceiling, and one-thread BLAS settings. Receipts were pulled back locally. No other job was modified, and the pod was not terminated.

Final checks at approximately 21:11 UTC found no remaining review workers on the pod (`receipts/process_audit_final.json`); the local process snapshot is retained too. Final live README, open-item titles and all eight audited repository HEADs were unchanged (`sources/final/recheck.json`). Retained local artifacts total about 33 MB, below the 50 MB limit. The review completed within the three-hour allowance; STATUS.md was checkpointed during the run and at completion.

Next: retain the frozen certificate and this independent recount with the detailed finite reduction above. A human specialist can check the short normalization and blow-up argument. Replaying search diagnostics is optional; it cannot strengthen the already verified inequality without a different certificate. No commits, pushes, PRs, posts or external messages were made.
