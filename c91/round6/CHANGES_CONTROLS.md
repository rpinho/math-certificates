> Historical producer control-repair record, with private directory prefixes redacted.
> Source paths and original host receipts below refer to the producer archive.
> In this flat release layout, run `./reproduce.sh controls`; see
> `logs/release_frozen_controls.json` and `RELEASE_NOTES.md` for this copy.

# C91 round-6 control-reporting repair

Job `math_c91r6fix_1103`, 2026-11-03. Read `_codex/RULES.md`, round 5's
`REPORT_CONTROLS.md` (including its addendum), `CHANGES_CONTROLS.md`, and
both Astra reviews before editing. The existing `PRIOR_ART.md` precedes
this maintenance; its added entry records the inherited baseline. No
mathematical search, new bound or novelty claim was made.

The repaired classifier and process launcher are ported from round 5's
second repair (`f1c3e0af8f4689aae2e968a2231ccde92b24dcdb85f4ce234ea466ce2e2cdd65`).
Round 6 uses an integer power recipe, so its five corruptions are schema,
exponent, canonical word, zero initial potential, and constant positive
potential (`steps=0`). The obsolete binary32 mutations are removed.
`power_controls.py`, the previously documented round-6 launcher, now
forwards to the repaired harness, preserving its three positional arguments
and accepting the new timeout option.

Every control requires its exact exit status, sole exact diagnostic and
exact declared checkpoint sequence before that diagnostic. Missing,
reordered, duplicate or unexpected checkpoint lines, any extra REJECT
line, wrong status/reason, exceptions, launch failures, signals and deadlines
classify ERROR. The positive control uses the unchanged artifact and the
same wrapper/launcher; it is deliberately terminated only after schema,
exponent, integer-recipe, C++ START and canonical-word PASS checkpoints.
This bounded positive replay does not certify every potential row.

The wrapper replaces three assertions with equivalent predicates and
specific diagnostic/status pairs. The combined precision/initial assertion
is split without changing its conjunction. C++ receives only two flushed
checkpoint prints. `logs/controls_integrity_validation.json` confirms
AST identity of the replaced predicates and all other Python assertions;
removing the two prints recovers the original C++ byte for byte. The
artifact, both includes, arithmetic, transitions, reconstruction and bound
`265988/1000000` remain unchanged.

RLIMIT_AS is applied in the single-threaded wrapper, logged APPLIED or
SKIPPED on OS refusal, and restored afterwards. Compiler errors remain
execution errors; C++ rejection statuses propagate without a traceback;
checker signals explicitly report VERIFY_EXECUTION_ERROR and map to 70.
Apple Clang receives the installed Homebrew libomp flags; Linux retains
GNU `-fopenmp`. These are launcher portability changes. The harness sets
single-threaded library limits and `OMP_THREAD_LIMIT=1`, which also caps
the existing explicit `num_threads(12)` clause without editing it. It
serializes cases, enforces nice at least 10 and at most four sampled child
processes, owns each process group, and cleans up on every exit path.

Thirteen regression methods port Astra's probes and extend execution
coverage. Round-6 captures, diagnostics moved before START and original
round-5 Astra2 probes are retained under `fixtures/rejection_order/`.
Mutation expectations derive from captured checkpoints independently of the
classifier declaration. Tests cover permutations, missing/duplicate markers,
diagnostics before every checkpoint, duplicate/extra REJECT lines at every
line boundary, wrong codes/reasons, signals, missing launchers/verifiers,
Python exceptions, timeouts/group cleanup and portable resource limits.

## Before/after SHA-256

Before images and the initial hash record are in `work/controls_fix_before/`
on the Mini; the pod retains before images of its affected sources and
artifact in the same relative directory. All 309 entries in the original
root manifest matched before changes (`logs/controls_original_manifest_audit.json`).

| File | Before | After |
|---|---|---|
| `code/frozen_candidate_controls.py` | `6766d6dc65f7fa9ec8a32525cde969b918d1e5e7d13043436c7c9319536d3208` | `894de9dce02349e7cc6a3ca9effd569b40fd8173fe9af8e8a6b876ea87029ebf` |
| `code/power_controls.py` | `a8505b0ea8787fe32d935ab6d639771ba09bd68621d7b054845886ae0142a142` | `15b1eae8719f1cb7c31d2d1f34eec870b309b36715edd3184e846d35a32ce3e0` |
| `code/test_frozen_candidate_controls.py` | `ABSENT (new file)` | `a072280403918cf6eecde51d154655ab908e4a41208a1914d9bd39eb7e599628` |
| `frozen/verify_orbit8.py` | `2434e8d0f962f0dbbd40a5294a421a25dbe347df92d78ad6da70a305519aa4f8` | `57b82bd06efece68246cbe819abf046eccbaa1e09bcc8a7a53dbc74fb4deab2f` |
| `frozen/verify_orbit8.cpp` | `d6fbbab3337acecd9834a9493fdfd0fb13523cc05e442173521e6201df9fa6cd` | `950688975c8c1ac40c231d629b318578df115059acd8c35a5e72732981b9ed27` |
| `PRIOR_ART.md` | `5a7d986d6884c69850bc7d9a52e3e141db7becb0f6ddcd70e1a05b21e1bf9261` | `dea189e756cc5436a451bdfad793bfed9fd976cde4c654afadae86138f749b51` |
| `frozen/SHA256SUMS` | `ABSENT` | `99ae01a42e5ea8908947238601b08f63d41e67a64917f259758855890fe26fec` |

Unchanged before and after:

| File | SHA-256 |
|---|---|
| `frozen/candidate_c91r6.json.gz` | `e6bcacb08bb36ee21e93f90a05160b6240260692390630c03049ac0ccd39f767` |
| `frozen/orbit_tracker8.inc` | `6c5d02aa074bd4b13b0d0f206a20c9ee68dbf985952babb20b8d00b3a76f697d` |
| `frozen/base_complement.inc` | `eba5b0f949045286603c5050876b522d8045f3140ff773a15cf8827e05268c30` |

`frozen/SHA256SUMS` was absent initially and is created for the eight frozen
artifact/checker/harness files; its paths are relative to the job root.
The existing root `SHA256SUMS` is refreshed while retaining all its original
paths and adding the new report, changes, manifest, tests, fixtures and
final receipts. Manifest/report self hashes are excluded to avoid cycles.
Original root-manifest hash before this repair:
`a23886bc8b3f469279ee2257c434a8618b61a986873fefda46fd6ec41e872938`.

Both hosts passed the six required outcomes and all thirteen tests at
exactly nice 10. One verifier ran at a time, with peak sampled child process
count three. The Mini logged RLIMIT_AS SKIPPED and Linux logged APPLIED.
Source hashes match across hosts. All 19 tracked Mini PIDs and 15 tracked
pod PIDs exited; final ps audits found no job workers. No unrelated shared
pod processes were touched.

One development test named its temporary signal probe `signal.py`, which
shadowed Python's standard-library module and failed an exit-code assertion.
It was renamed `terminate_probe.py`; both final thirteen-test runs passed.
That failed test output is retained in `work/controls_selftest_development/`.
No failure was counted as a successful rejection control.

The existing `REPORT.md`, full-replay receipts and original control logs
remain historical. Use `REPORT_CONTROLS.md` for the repaired harness results.
No commits, pushes, PRs, posts or messages were performed. Only this job
and the explicitly assigned pod directory were modified; transfers used
only that authorized pod.
