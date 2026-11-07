# Independent referee of sampaio_YB01

The five 2025 Table 7 improvements hold as finite, synthetic-reviewer benchmark
results. This referee reconstructed every headline assignment exactly from
fresh public inputs with independent code. The remaining qualification is
historical hold-out provenance: local freeze records are consistent with the
claimed order but cannot prove absence of earlier test inspection. No leakage
was found. This report does not independently referee the secondary 2024 tables.

| Team | Original best, independently counted | Claimed and independently reconstructed | Own class-frequency control |
|---|---:|---:|---:|
| 1 | 138.10604 (DeCCaF) | 102.04408 | 171.26268 |
| 2 | 141.97164 (OvA) | 107.65252 | 162.14964 |
| 3 | 126.16748 (DeCCaF) | 84.82136 | 158.68900 |
| 4 | 141.57996 (DeCCaF) | 102.34236 | 156.80104 |
| 5 | 132.00812 (DeCCaF) | 98.75168 | 158.30044 |

These are means of total FN + .057 FP over the same 25 training-shuffle /
testing-capacity combinations per team. They use all 4,457 original month-8
alerts (stored month=7), ten original synthetic reviewers and the original
rigid reviewer/classifier quotas. They are neither percentages nor per-alert
costs. The original classifier has FP=2,878, FN=40, cost=204.046; rejecting
all alerts costs 213.522. The paper prints these as 204 and 213.5.

`referee_costs.py` reopened freshly downloaded FiFAR and author-model archives.
It checked 250 original decisions and 1,000 candidate scenario assignments,
including source case IDs, all original quotas, actual source reviewer
decisions, independently inferred classifier decisions and exact integer
cost units (1,000 FN + 57 FP). It independently refitted the even-validation
sigmoid used by the new classifier. No claimant module was imported.

`referee_policy.py` independently fitted all four conditional regularizations
on the original one-observed-reviewer annotations from months 3–5. It
recomputed all 350 odd-validation scores, including optional sigmoid and
fixed 50/50 blends, and obtained all 25 recorded winners. It fitted 2,000
logistic components across four regularizations; all 500 selected heads'
coefficients match the saved weights exactly. The largest
validation-score difference was 1.811e-10, with the same winners. A separate
15-candidate reconstruction also confirmed the fraud classifier's selected
sigmoid, with maximum score difference 3.842e-12.

The independent integer transportation constructor starts from a greedy
feasible assignment, without reading the candidate assignment as a start.
It reproduced all 125 headline assignments case for case and objective for
objective. A separate Floyd-Warshall exchange-cycle certificate proves
optimality for the registered utilities rounded to 1e-9. The constructor
and analytic frequency control passed exhaustive enumeration on 300 seeded
toy problems. A generic HiGHS attempt was stopped for performance; its
incomplete outputs are not evidence against the claim.

`verify_frequency.py` checked all 125 fresh class-frequency controls using a
separate exchange calculation. Their expected-risk sum discrepancies were
at most 7.106e-14 and no negative cycle was found. Their realized means match
the reported controls exactly. The better of the claimant's two count-only
controls costs 171.26268, 153.02588, 144.24156, 154.34440, 155.57260; their
saved decisions were separately evaluated. Reusing only the authors' expert
forecasts with corrected cost routing costs 133.87744, 144.38976, 118.97688,
137.20716, 133.58108. Counts or an objective change alone do not explain the
headline gain.

All 117 selection-file hashes and the fitting-code hashes match their freeze
records. Recorded freezes are 15:07:14, 15:41:40 and 15:59:02 UTC; the recorded
candidate inference pipeline begins at 15:59:03. Selected model mtimes precede
their freezes. Reviewed fitting inputs exclude month 7, hidden generator
parameters and unobserved reviewer labels. However, these records and mtimes
are self-authored and mutable, and initial manifests did not bind every
fitted weight. Exact independent refits and validation replay substantiate
the policy, while leaving historical absence of prior inspection unprovable.
The headline is the explicitly added third family. The originally primary
replacement family lowers every original Table 7 best cell but misses the
stronger public references on teams 1 and 4; all eight methods were retained.

The paper itself lists Marco O. P. Sampaio in the Feedzai author group.
See PRIMARY_SOURCE_NOTES.md and PRIOR_ART.md for the primary article, table,
identity metadata and source limitations. The difference from the paper is
class-conditional logistic correctness prediction, a fixed blend with the
published forecasts, and expected-cost routing. Prior public work already
provides solver-only improvements (Nguyet Vo) and explicitly suggests the
conditional decomposition (Fatigue-aware-human-AI-triage). No novelty,
priority, world-record or real-reviewer conclusion is drawn here.

The stronger public released/retrained reported cells found are 133.3, 133.6,
116.0, 134.4, 131.7. Retrained weights are unavailable, so those retrained
models were not rebuilt. For released models, this referee also constructed
250 independent forecast-optimal assignments. Seventeen realized costs
differ from the claimant's prior-LP replay because forecast objectives are
nearly tied: the largest recorded gain from correcting its saved assignment
at 1e-12 utility precision is only 7.571e-8 in summed predicted correctness.
For example, the independent DeCCaF Team-4 mean is 133.78820 versus saved
134.35216. Direct source evaluation reproduces every saved comparator mean.
This tie sensitivity affects the older comparator, while all 125 headline
conditional assignments reproduce exactly.

The compact evidence bundle retains public canonical feature data, the 25
masked annotation tables, all 250 original decision/assignment witnesses,
original selected author models, candidate weights/assignments, freeze
records, source snapshots, code and results. `verify_retained.py` rechecked
all 1,250 original/candidate costs using only that compact witness, without
opening either bulk download. Bundle integrity is checked by a per-file
manifest and a separately verified transport SHA-256 receipt. Numerical
work used the pod's installed libraries, not a separately provisioned runtime;
their versions are recorded in REFEREE_RESULT.json.

To reproduce on an authorized compute host, place the code and retained
claim_inputs in a fresh output directory. Set SAMPAIO_REF_ROOT to that
directory and SAMPAIO_CLAIM_INPUTS to its claim_inputs subdirectory. Obtain
`sources/fifar.zip` from https://ndownloader.figshare.com/files/52147616 and
`sources/benchmark.zip` from
https://media.githubusercontent.com/media/feedzai/openl2d/main/l2d_benchmarking.zip .
Their SHA-256 values are in COST_RESULT.json. Use a fresh output directory
for actual refitting: existing completed policy checkpoints are reused.

```sh
nice -n 10 python3 integer_transport.py
nice -n 10 python3 referee_costs.py
nice -n 10 python3 referee_policy.py
nice -n 10 python3 summarize_referee.py
nice -n 10 python3 verify_h_selection.py
nice -n 10 python3 verify_frequency.py
nice -n 10 python3 referee_prior_lp.py
nice -n 10 python3 audit_prior_ties.py
nice -n 10 python3 verify_retained.py
```

The verified local evidence archive is 17,960,658 bytes, SHA-256
`295c40e1ed32cee68d48ab7548db1e0adf36b071ce1cef968b199656fb5a9eaf`.
All 337 manifest entries passed transport integrity verification. The pod
closeout receipt records no live owned workers and 32,187,265 retained bytes
in the assigned workspace after removal of both temporary bulk downloads.
The official table and both public comparator tables were unchanged in the
final source refresh. No shared dependency was installed or changed by this
referee, and no other job's files or processes were modified.

The strongest author response to the provenance caveat is that exact refits,
validation winners and complete assignment replay already support the
frozen-policy claim; missing external timestamps do not establish leakage.
The next useful test is an externally committed full code/weight manifest
followed by one evaluation on a new, nonoverlapping hold-out with the same
capacity rules and count control. Do not tune again on these test cases.
