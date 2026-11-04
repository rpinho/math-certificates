> Historical producer control-repair record, with private directory prefixes redacted.
> Source paths and original host receipts below refer to the producer archive.
> In this flat release layout, run `./reproduce.sh controls`; see
> `logs/release_frozen_controls.json` and `RELEASE_NOTES.md` for this copy.

# C91 round-6 repaired rejection controls

Job `math_c91r6fix_1103`, 2026-11-03. **PASS on the Mini and math-cpu-12:**
all five intended rejections, positive replay of unchanged bytes, and all
13 regression tests on each host. Verifier mathematics, artifact and bound
are unchanged. This report supersedes the old control-harness claims in
`REPORT.md`; the earlier full certificate replay is historical evidence.

Each negative control now requires the exact code and sole exact diagnostic
below, strictly after its declared checkpoint sequence. No other REJECT
line may occur anywhere. Missing, reordered, duplicate or unexpected
checkpoint lines, execution errors, signals and timeouts classify ERROR.

| Control | Exit | Exact diagnostic |
|---|---:|---|
| schema | 41 | `VERIFY_REJECT schema` |
| exponent | 42 | `VERIFY_REJECT exponent` |
| canonical_word | 1 | `REJECT: listed word is canonical` |
| zero_initial | 44 | `VERIFY_REJECT initial potential (requires 0 < initial <= 2^60)` |
| constant_positive_potential | 1 | `REJECT: exact row inequality failed at 0 (positive-minimum lower bound)` |

Checkpoint names below expand to the exact emitted lines:

- S: `VERIFY_CHECKPOINT schema PASS`
- E: `VERIFY_CHECKPOINT exponent PASS`
- P: `VERIFY_CHECKPOINT integer power recipe PASS`
- C: `VERIFY_CHECKPOINT cpp START`
- W: `VERIFY_CHECKPOINT canonical word PASS`

| Control | Required ordered checkpoints before diagnostic |
|---|---|
| schema | Empty |
| exponent | S |
| zero_initial | S → E |
| canonical_word | S → E → P → C |
| constant_positive_potential | S → E → P → C → W |
| positive_frozen | S → E → P → C → W, with no diagnostic |

Schema, exponent and zero-initial rejection intentionally occur in Python.
The two C++ controls must reach START. The constant-positive corruption
changes only recipe steps to zero, preserving positive initial potential;
the unchanged exact necessary root inequality rejects it.

The positive run checks the exact unchanged compressed bytes in the same
launcher, including Arb exponent validation and all 59,550 forbidden-word
canonicality checks. Both hosts reached W and were intentionally stopped
with wrapper exit 143. This is a successful bounded checkpoint replay,
not a rejection pass or another complete 121,332,798-row replay. The
unchanged 128-step recipe does not execute the early necessary-root branch;
no ROOT_NECESSARY_EXACT_PASS is claimed for that run. No arithmetic,
transition, potential or bound calculation was added or changed.

## Runs and limits

| Case | Exit | Mini seconds | Pod seconds | Outcome |
|---|---:|---:|---:|---|
| positive_frozen | 143 | 3.60 | 7.61 | PASS |
| schema | 41 | 0.22 | 0.17 | PASS |
| exponent | 42 | 0.21 | 0.17 | PASS |
| canonical_word | 1 | 3.03 | 8.07 | PASS |
| zero_initial | 44 | 0.21 | 0.17 | PASS |
| constant_positive_potential | 1 | 3.35 | 5.74 | PASS |

Mini suite: `2026-11-03T23:25:31.068220+00:00` to `2026-11-03T23:25:42.432094+00:00`.
Pod suite: `2026-11-03T23:25:43.088945+00:00` to `2026-11-03T23:26:07.112031+00:00`.
Both suites exited 0. Tests passed in 1.120 seconds on the Mini and
0.663 seconds on the pod. Tests' deliberately failing execution cases
record ERROR, as required.

All sampled child processes were at exactly nice 10, with one serialized
verifier invocation, at most three sampled child processes (ceiling four),
and single-threaded library/OpenMP limits. Peak sampled process-group RSS
was 268,648,448 bytes on the Mini and 295,542,784 bytes on the pod; sampling
excludes the harness and is not a full-replay memory estimate. Each case
had a 600-second deadline.

The RLIMIT_AS hook runs in the single-threaded parent, with no preexec_fn,
and restores the original soft limit. The Mini logged
`RESOURCE_LIMIT RLIMIT_AS SKIPPED ValueError current limit exceeds maximum limit`;
the pod logged `RESOURCE_LIMIT RLIMIT_AS APPLIED 100000000000`.
Both intended C++ diagnostics followed START despite the macOS refusal.
Apple Clang uses the installed libomp; GNU g++ retains its OpenMP flags.

## Regression and integrity evidence

All 13 test methods pass on both hosts. They include Astra's reordered-log
and diagnostic-before-START probes; diagnostics moved before every required
checkpoint; extra or duplicate REJECT lines inserted at every line boundary;
missing, permuted and duplicate checkpoints; execution failures, wrong codes,
missing executables, Python exceptions, actual signals, deadlines/child
cleanup and resource-hook acceptance/refusal. Checkpoint mutation expectations
come from actual captures independently of the classifier declarations.
Both original Astra2 probes, adapted only by adding the round-6 recipe
checkpoint and mapping the root-control name, now classify ERROR.

Evidence:

- `logs/{mini,pod}_controls_frozen_controls.json`: outcomes, commands,
  source hashes, PIDs, priorities, timing, resource notices and per-case log hashes.
- `logs/{mini,pod}_controls_control_*.log` and `*_controls_suite.log`:
  actual verifier output and suite receipts.
- `logs/{mini,pod}_controls_selftest.log`: thirteen-test results.
- `fixtures/rejection_order/`: round-6 captures/probes and original Astra2 probes.
- `logs/controls_integrity_validation.json`: checkpoint/diagnostic positions,
  byte-identical mathematical C++ after removing two prints, equivalent Python
  predicates, unchanged includes/artifact, and both before-START ERRORs.
- `logs/controls_pod_source_sha256.txt`: matching source/artifact hashes across hosts.
- `logs/controls_{mini,pod}_cleanup.json` and `*_final_ps.txt`: all 19 tracked
  Mini and 15 tracked pod PIDs exited; no job workers remain.
- `CHANGES_CONTROLS.md`: detailed changes and before/after hashes.

Artifact SHA-256 remains
`e6bcacb08bb36ee21e93f90a05160b6240260692390630c03049ac0ccd39f767`.
Bound remains **265988/1000000 = 0.265988**. The C++ change consists only
of two flushed checkpoint prints; all other C++ bytes and both includes
are unchanged. Python mathematical predicates are identical. Initial root
manifest: 309/309 entries matched before editing. `frozen/SHA256SUMS` now
covers the frozen artifact, checker and operational harness sources; the
root manifest is refreshed for the complete retained packet.

## Reproduction

Run from the job root. These commands assume a shell at nice 0; if the shell
is already at nice 10, omit the extra `nice -n 10` to avoid nice 20.
The harness itself raises priority numerically to at least nice 10 when needed.

```sh
shasum -a 256 -c frozen/SHA256SUMS
nice -n 10 ~/dev/open-science/.venv/bin/python -B -u code/frozen_candidate_controls.py \
  frozen/candidate_c91r6.json.gz frozen/verify_orbit8.py mini_replay \
  --timeout 600 > logs/mini_replay_suite.log 2>&1
nice -n 10 ~/dev/open-science/.venv/bin/python -B code/test_frozen_candidate_controls.py -v
```

On the authorized pod, from `ROUND6_ROOT`:

```sh
sha256sum -c frozen/SHA256SUMS
nice -n 10 venv/bin/python -B -u code/frozen_candidate_controls.py \
  frozen/candidate_c91r6.json.gz frozen/verify_orbit8.py pod_replay \
  --timeout 600 > logs/pod_replay_suite.log 2>&1
nice -n 10 venv/bin/python -B code/test_frozen_candidate_controls.py -v
```

`code/power_controls.py` forwards to the same repaired harness and accepts
these arguments. Suites exit 0 only if every required outcome passes;
otherwise the receipt says ERROR and exit is 2. No search output or
generated graph is needed for this bounded control suite.

The existing `PRIOR_ART.md` and round-5 reviews supply inherited source
coverage. This maintenance makes no new bound, priority or novelty claim;
no fresh literature audit or full all-row replay was performed. The
historical round-5 fixture/root diagnostics were not ported into the
higher-order integer-recipe format. No required reporting/control work
remains. No commits, pushes, PRs, posts or messages were performed.
