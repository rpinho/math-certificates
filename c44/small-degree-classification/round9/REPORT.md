# C44 round nine — candidate, unrefereed

Frozen mathematical replay: PASS, 03:56 UTC on 3 November 2026.
Retrieval and process audits: PASS. Results are local; the pod was left running.

The candidate result is R6<=107, with R5<=50 unchanged, giving

    3/2 <= C44 <=
    80058654243525646012949597587 / 39614081257132168796771975168
    < 2.0209645587.

This improves the round-eight rational upper bound by approximately
0.02074406935, exceeding the requested 0.0001 bar. It is a computer-assisted
candidate, unrefereed. Two separately written exact implementations in the
same agent session are not independent human refereeing or formalization.
No novelty, priority or public-record claim is made.

The candidate finite statement is: a ternary polynomial A of real degree at most
five and energy E A^2=7/128 has at most thirteen relevant controls. Integer
partial-energy gaps reduce possible larger cases to 189 tensor/selected-
coordinate orbits. Exact completion, residual minimum-partial energy and
local affine-sign equations exclude them. In the decisive residual case,
32 Fourier masks form an affine five-flat and the local sign equations
have rank 26; all remaining signs are global characters. The resulting
ternary minimum piece leaves a nonzero integer polynomial with energy
below the degree-five minimum, a contradiction. See frozen/PROOF.md.

The inherited R4=22 and sharp second-weight classifications are used.
Published completeness and lattice-group premises are explicit in the
proof. Finite verifiers do not establish those published universal
premises. The accepted recurrence uses none of the unfinished quartic
energy search or numerical lower-side solver bounds.

## Verification

PASS. Both native classifiers excluded all 189 cases with zero unresolved
leaves. A visited 42,853,514 nodes; B visited 43,046,684. Each applied the
rank-based residual rejection 23 times. Both exact scalar verifiers
passed all 92 recurrence rows through degree 96 and the infinite tail.
All thirteen stored lower seeds passed both exact checks, with lift 3/2.
All 23 corrupted artifacts were rejected by both checkers: 46 rejections.
Ten native flat-predicate controls and both complete 64-character signed
controls passed, including rejected noncharacters and rank/shape failures.

The frozen replay also reran both inherited quartic and quintic classifiers,
the strengthened quintic second-weight classifiers, round-eight recurrence
checks and the full R4 replay on hash-matched mutable copies. All passed.
The 552 static files total 26,839,728 bytes. Every frozen hash was checked
before and after replay. Frozen MANIFEST.json SHA256:

    69deb7b19db9a718720a8c3f0fe51afb46481e1406ba7b36bc2325dcf4e7cff2

Receipts: receipts/FINAL_RECEIPT.json, frozen_replay_ledger.json and the
complete compressed receipt archive. The first attempted launch occurred
while transfer was finishing and the initial file-set hash guard stopped
it before any mathematical task. After transfer completed, the full
unchanged packet replay passed. That guard failure is retained separately.

## Reproduction

From this job directory on a suitable compute machine with standard
Python 3 and a C++17 compiler:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      nice -n 10 python3 frozen/replay.py --workers 4 --replay

The --replay switch permits reproduction after this job's historical
compute deadline. All output is written outside frozen/. This command
rebuilds native verifiers, checks every frozen hash before and after,
and writes receipts/FINAL_RECEIPT.json. The job's actual run uses the
worker count stated in its process ledger, maintaining the aggregate
fourteen-worker allowance while other own exploratory work runs.

## Routes tried and limits

1. The third-weight R6 route succeeded as described above. The preliminary
   control ceiling fourteen gave R6<=108 and C44<2.0267901075; the complete
   affine-sign argument strengthened it to thirteen and R6<=107. The final
   packet uses only the stronger result.
2. R5's budget 201/4 remains unresolved. For R5=50, four pair controls
   would force at least 208 quartic sections to maximize potential, but
   their total top energy is at most 128. A lower top-energy bound 5/8
   for every maximizing quartic would give a contradiction (130>128).
   The corresponding 22-variable, energy-numerator<=39 exclusion was
   attempted with norm/deficit, adaptive good-partial completion, Boolean
   restriction, parity and signed-character filters. It is unfinished.
   Timeouts and unsigned survivors are not exclusions. Details and final
   coverage: R5_OBSTACLE.md and QUARTIC_EXPERIMENT.md. The signed prototype
   returned zero leaves in 13 distinct case files and unresolved leaves
   in eight others; other work timed out, stopped or was not reached.
   These are unverified prototype outcomes, not certified exclusions.
   The stronger final relaxation still leaves a pattern with 42 forced
   unit coefficients, norm remainder 22, nine completed controls, six
   observed unfinished coordinates and seven absent ones. Its forced top
   numerator is 27 and deficit 26. No actual Boolean completion is known.
   Further unsigned enumeration cannot resolve that known completion gap,
   so the remaining exploratory batches were stopped with a PID receipt.
3. Shared parity substitutions of Xi5 used a pair-column MILP, a larger
   triple-column MILP and six randomized cancellation-aware local searches.
   The pair MILP returned 46 with a nonexact, nonclosing numerical bound;
   the triple MILP timed out in presolve. The local searches returned 46.
   Two larger Xi6-to-degree-five searches tested further cancellation maps.
   The six Xi5 searches completed 1,090,507 local moves, and the Xi6
   searches 4,418 and 341 moves (the larger column family was expensive).
   All returned 46-variable degree-five seeds. No improved seed was found.
4. Overlapping cubic branches with one or two shared selectors, followed
   by weighted Xi substitutions, tested 2,339,737,440 allocations and
   returned 46. Two further searches optimized local-degree potential
   over 910,012,576 allocations, favoring shared branches and a single
   selector to test possible CHS duplication improvements. Their best
   potential was 46/32, with every local degree five. These are sampled
   searches, not nonexistence certificates.
5. Cubic/Xi compositions were exhaustively enumerated for potential
   through degree eight as an exploratory finite family. They recovered
   the Xi counts 46,94,190,382; their smaller-local-degree maxima were
   two units below each count. This is not a classification of all
   Boolean constructions. Minimum-support gate partitions have a
   conditional structural obstruction, explained with its published
   affine-partition premise in LOWER_ROUTE.md.

The universal lower bound remains 1.5. Failed searches do not prove its
optimality. Every stored seed claimed as certified is checked separately
for Booleanity, exact degree, relevant count and asymptotic lift.

## Literature and live-source coverage

PRIOR_ART.md was written first and records the baseline, source URLs,
query receipts, coverage gaps and refresh times. The official live table
and raw source, all open teorth/optimizationproblems PR diffs/issues,
recently-updated GitHub searches, the requested AI-lab result repositories,
NS/CHS/Wellens and since-2024 citing work were checked. The official table
still lists 4.3576549226*, while PR294 and the public input packet list
2.0417086280*. No stronger applicable public result was found in the
bounded checks. X is unavailable; private communities and authenticated
global code search are outside coverage. Final checkpoint refresh: 03:40–03:42 UTC, 3 November 2026.

Credits: Nisan–Szegedy; CHS and Wellens's weighted restriction framework;
Shinkar–Tal/CHS lower construction; Rasoolzadeh's cubic catalogue;
Valyuzhenich's minimum-support classification; the low-weight Reed–Muller
theorems; Barnes–Wall/Broué–Enguehard/Nebe; and rounds four through eight
of the retained candidate packet. Full dependency details are in PROOF.md
and frozen inherited sources.

## Next steps

Referee the new affine-sign minimum-piece lemma and both completion
implementations, then the explicitly listed inherited premises. For R5,
complete or disprove the precise quartic energy envelope instead of
assuming it. For the lower side, nonminimum gates and shared compositions
remain open; target a 47-variable degree-five or 95-variable degree-six
seed, and expand/check it exactly before making an asymptotic claim.

Completed and retrieved by 03:59 UTC on 3 November 2026, well before the
13:04 UTC retrieval deadline. All job-owned compute workers have ended;
the required remote and local ps audits found no remaining workers. The
local launcher and Codex controller are the current session, not workers.
The pod was left running and other jobs were not modified.

The complete receipt archive was pulled back and its SHA256 matched:

    830ead3770dd804a4dff8f1c3f367713b756662fa2507fe69ae3653dda448c7d

The local frozen manifest matches the pod's, every frozen file hash was
rechecked, and the archive's 378 classification outputs, all successful
batch ledgers, thirteen lower seeds and 46 rejection outcomes were checked
for receipt consistency. See receipts/RETRIEVAL.json and
receipts/OWN_WORKERS_STOPPED.json. The retained local files total about
38.3 MB of logical data (below 50 MB); the frozen static packet is 26.8 MB.
No commits, pushes, PRs, posts or messages were made. Network actions
were public reads and the authorized pod transfers.
