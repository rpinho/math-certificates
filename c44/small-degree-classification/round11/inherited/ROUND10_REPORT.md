# C44 round ten — candidate, unrefereed

**Mathematical verification: PASS. Retrieval and process audits: PASS.**
All own compute workers have ended. Results are local, well before the
13:00 UTC retrieval deadline. The pod was left running.

The candidate result is

    R7 <= 229,  R5 <= 50 and R6 <= 107 unchanged,

    3/2 <= C44 <=
    79671833529611582591986228957 / 39614081257132168796771975168
    < 2.0111998311.

The exact gain over round nine is

    193410356957031710481684315 / 19807040628566084398385987584
    = approximately 0.009764727633167556 > 1/10000.

This meets the requested upper-bound bar through the direct R7 route.
No asymptotic lower bound above 1.5 was found. These are unrefereed
computer-assisted candidates with explicit published premises. The two
implementations were written separately by the same agent; this is not
independent human refereeing or proof-assistant formalization. No novelty,
priority, optimality or public-record claim is made. Round nine's frozen
files were not modified.

| Quantity | Round nine | Round ten final |
|---|---:|---:|
| R5 upper | 50 | 50 |
| R6 upper | 107 | 107 |
| R7 upper | 230 | 229 |
| R12 upper | 8201 | 8161 |
| Strict C44 upper | 2.0209645587 | 2.0111998311 |
| Asymptotic lower | 1.5 | 1.5 |

The preserved first-stage packet separately gives C44<2.0114439717,
already meeting the requested bar. The final sign completion improves
that value by approximately 0.000244140625.

## Proof and accepted artifacts

The new deficit argument applies to ternary degree-k polynomials near
the maximal control count. The integer partial-energy gap forces every
partial to be minimum and homogeneous when the deficit is below half a
minimum partial. At the decisive k=6, normalized weight 31/16, 23-control
point, the remaining constant coefficient would have integer numerator
whose square equals 4/3. This excludes that point and gives R7<=229 through
the inherited restriction budgets.

For the stronger propagation, the Fourier-mask complex splits into
cross-polytope boundaries. Minimum partials force character signs on each
vertex face; second discrete derivatives then force a global character.
Every component factors into pair gates. Independent components have
range width twice their number, so ternary range forces one component,
zero constant and normalized weight one. This strengthens the control
ceiling at other recurrence points, including integral normalized weights.
The exact recurrence is propagated through degree 96 and its unchanged
infinite tail is added.

Every step is in [the first-stage proof](frozen/PROOF.md) and
[the final extension](frozen_final/PROOF.md). The inherited R4 catalogue,
low-weight spectrum, minimum-support and lattice/group results remain
explicit premises. Finite replay verifies the supplied representatives,
completion calculations and arithmetic; it does not prove those published
universal completeness theorems. An optional elementary minimum-structure
review note is in experiments/ELEMENTARY_MINIMUM_STRUCTURE.md; it is not
needed to accept the frozen numerical packet.

| Packet | Role | Verification |
|---|---|---|
| frozen/ | First-stage bound 2.0114439717, unchanged nested round-nine input | Full inherited replay, two new scalar checks, thirty rejections |
| frozen_final/ | Final bound 2.0111998311 | Two exact scalar checks, sign/range controls, forty rejections |
| frozen_lower/ | Four saved known 46/94-variable seeds | Eight exact checks, sixteen rejections; lift 3/2 |
| frozen_controls/ | Cubic statistics and 36-variable graph control | Two seed checks, two catalogue checks, four graph controls, eight rejections |
| frozen_extension/ | Preserved intermediate sign-extension replay | Same final bound; superseded replay wrapper with historical receipt-byte binding |

The final manifest SHA256 is

    7b91a9bf911c1892d5615cad93bb1e987d174606a87925c91998833ebc19a627

The final receipt is receipts/final/FINAL_RECEIPT.json (PASS,
04:59:17 UTC). Both exact implementations agree on all 92 recurrence rows
and the tail; B additionally scans every allowed energy-grid point through
degree sixteen. The final sign controls check all 256 sign tables of the
three-dimensional transversal cube, with exactly sixteen admissible
character signings, and independent-component range controls.

The unchanged round-nine replay excluded all 189 cases in both native
implementations, with zero unresolved leaves and node totals 42,853,514
and 43,046,684. Its forty-six rejection outcomes and all 378 classification
outputs were retrieved and checked for agreement with its frozen case
artifact. The compressed receipt archive contains 856 files, SHA256

    df4855ca9485b47d5536d20f4fd0d807d0f2c260658aba81942a9b8ddad9018b

See receipts/RETRIEVAL_MATH.json, receipts/baseline_receipts.tar.gz and the
individual final/lower/auxiliary receipts. All frozen file sets and hashes
were checked before/after their replays and again after retrieval.

## Exact reproduction

From this directory on a suitable compute machine with standard Python 3
and a C++17 compiler, run sequentially:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  nice -n 10 python3 frozen/replay.py --workers 4 --replay
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  nice -n 10 python3 frozen_final/replay.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  nice -n 10 python3 frozen_lower/replay_reference.py
```

All mutable outputs stay outside frozen packets. The final wrapper binds
the baseline's static hashes and mathematical receipt fields, allowing
fresh replay timestamps. The historical byte-bound intermediate wrapper
is preserved for audit, but the commands above use the corrected wrapper.
Generators are retained for inspection; do not run them inside frozen
folders when regenerating artifacts.

The optional auxiliary replay is `nice -n 10 python3 frozen_controls/replay.py`;
it additionally needs NumPy. Exploratory solvers need OR-Tools. Their
exact command arrays, timeouts, memory limits and seeds are in jobs/*.json
and the retained process ledgers. They are not needed for the accepted
upper-bound replay.

## Ranked routes and failures

1. **Direct R7 near-equality exclusion succeeded.** The specific integer-square
   contradiction and the safe generic divisibility lemma gave the first
   packet. Global sign completion then gave the final stronger propagation.

2. **R5 quartic top-energy completion remains incomplete.** The target remains
   the precise 22-variable quartic energy envelope in the inherited
   [R5_OBSTACLE.md](frozen/baseline/frozen/R5_OBSTACLE.md): top energy at least 5/8 would exclude R5=50 at budget
   201/4. This round added exact slice-range tests, polynomial support-degree
   rank tests, a half-support completion lemma and even-energy/incidence
   pruning. The final sweep ran the 45 cases not already closed in prior
   prototypes, with six workers and 600 seconds per case: fifteen ended
   with zero unresolved leaves and thirty timed out. Together with fifteen
   prior zero-leaf cases, prototype coverage is 30/60. This is UNVERIFIED
   exploratory coverage, not an R5 theorem or a second independent complete
   implementation. Symmetry hard cases processed hundreds of millions of
   nodes before being superseded. Both corrected arithmetic hard cases
   also timed out after 1200 seconds. The remaining case names and hashes
   are in receipts/QUARTIC_CASE_COVERAGE.json.

   The first arithmetic prototype double-counted a deficit when fewer than
   four coordinates were unfinished. It was stopped; its outcomes are
   INVALID/UNVERIFIED. Version two combines the two incidence bounds by
   their minimum and passed its controls. Neither version enters the
   accepted recurrence. The half-support proof avoids the unsupported
   shared-Y-input shortcut in the older exploratory notes; its cubic
   statistics passed two separate frozen checks and rejection controls.

3. **Nonminimum-gate exact-cover searches found no improved seed.** Four small
   banks on 8/10/12 controls ran 1200-second searches; hinted followups
   recovered the known 46/94-variable seeds, which passed both checkers.
   Four sparse 5000-gate banks on 20/24/28/32 controls exhausted their
   budgets. Proposed counts 47–55 failed exact coverage. Four 1600-gate
   overlap-cut searches and unequal-payload/local-potential searches also
   found no improvement. Direct exact overlap-graph proposers then
   exhausted the corresponding small finite banks at the target threshold.
   The random banks contain few mutually compatible nonminimum supports;
   isolated attractive gates do not make a partition.

4. **Scaled overlap graphs also found no improved seed.** Four 20,000-gate
   banks included exact fusions of a known partition, guaranteeing genuine
   nonminimum covers. All four graph runs ended without a 47-variable
   seed. These are single-implementation exploratory finite-bank outcomes,
   not universal nonexistence certificates. Branch-and-bound skips branches
   below the target: printed best_count and complete_partitions describe
   encountered leaves, not certified maxima or every partition.

5. **Coordinated selector-tree fusions found no improved seed.** All 128
   depth-three point/pair tree patterns were searched with every signed
   fusion, at thresholds 47 for degree five and 95 for degree six. All
   models returned INFEASIBLE. At depth four, 607 sampled tree patterns
   used every fusion on at most four leaves plus sampled larger fusions.
   Initially 325 models returned INFEASIBLE and 282 UNKNOWN; only those
   282 unfinished models were retried with longer budgets, and all returned
   INFEASIBLE. Two additional longer degree-five/six models also closed.
   These are recorded solver outcomes for specified finite fusion banks,
   without independently checked UNSAT certificates. They do not classify
   all Boolean functions or prove that 1.5 is optimal.

receipts/ROUTE_SUMMARY.json records each stage. Supervisor FAILED entries
include deliberate SIGTERM on superseded stages and exit-two unresolved
prototype leaves; they are never interpreted as exclusions. Timeouts and
numerical/solver bounds enter no accepted mathematical claim.

## Prior art and credits

PRIOR_ART.md was written before mathematical code and records the live
[44a page](https://teorth.github.io/optimizationproblems/constants/44a.html),
[raw source](https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/44a.md),
all open PR diffs and issue-feed entries, comments on matched threads,
recent-update GitHub searches, required
AI-lab result repositories, NS/CHS/Wellens, recent arXiv and since-2024
citations. The final full audit started at 06:17 UTC; the 06:26:31 UTC
recheck found unchanged HTML/raw table, all 47 open PRs/53 issue-feed
entries, relevant diffs and twelve repository heads. The official table
remains 4.3576549226*, while [PR294](https://github.com/teorth/optimizationproblems/pull/294)
remains 2.0417086280*. No stronger applicable public result was found in
this bounded coverage. X is unavailable; private communities and
exhaustive authenticated global code search are outside coverage.

Primary followups included Potapov arXiv:2410.21937, the 2025
Maitra–Mukherjee–Stănică–Tang sensitivity/resiliency paper, and the October
2026 Barnes–Wall norm-spectrum paper arXiv:2610.15288. The latter supplies
norms and examples, without the degree-preserving universal two-minimum
vector decomposition that would be needed for a further cap. No such
unsupported decomposition was used.

Credits: Nisan–Szegedy; CHS/Wellens weighted restrictions; Shinkar–Tal/CHS
lower constructions; Rasoolzadeh's complete cubic catalogue; Valyuzhenich;
low-weight Reed–Muller results; Masuda–Panov; Barnes–Wall, Broué–Enguehard
and Nebe; and the retained rounds four–nine. Precise premises and source
snapshots are in the frozen proofs and PRIOR_ART.md.

## Closeout and next work

All accepted results and exploratory outcomes were retrieved. The remote
working-directory/process audit at 06:26:48 UTC found no own processes;
the local ps audit also passed. The job stayed within fourteen own CPU
workers, nice 10 and single-threaded BLAS. The pod and other jobs were
not modified or terminated. This job made no commits, pushes, PRs,
posts or external messages.

The retained packet is about 42 MB, below 50 MB. It includes all frozen
certificates, full mathematical receipt evidence, one compressed large
search bank, compressed small banks, every large-bank hash/seed/generator,
and all process/search ledgers. Redundant regenerable bank exports were
moved reversibly to macOS Trash; RETENTION.json records the changes.

Referee the direct R7 exclusion and global sign completion first, then
the inherited universal premises. For R5, add restartable subcase sharding
and a separately written complete implementation before extending the
thirty remaining cases; merely raising the same root-case timeout has
not closed them. For the lower side, generate compatible nonminimum
supports jointly or leave the examined selector/payload families. A
47-variable degree-five or 95-variable degree-six seed must pass two
frozen exact verifiers and rejection controls before an improved lower
bound is claimed.
