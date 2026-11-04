# Reproduce C22b round 1

Use Python 3 with python-flint 0.9.0 (FLINT/Arb). NumPy/SciPy and discovery
code are unnecessary. From this packet directory:

```sh
shasum -a 256 -c SHA256SUMS
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
PY=${PY:-python3}
nice -n 10 "$PY" verify_all.py . > ../replay.json
nice -n 10 "$PY" run_controls.py . > ../controls.json
```

Both commands must exit zero. Expected verdicts:
`ALL_FROZEN_C22B_CHECKS_PASS_CANDIDATE_UNREFEREED` and
`ALL_EXACT_EXPECTED_CORRUPTION_REJECTIONS_PASS`, with `total_controls=108`.
Each control's actual rejection must equal its exact expected code.
The full replay uses exact fractions/integers and 220-bit Arb, recomputing
all 22 geometry covers (146198 leaves), all 22 covers again after the exact
margin shrink, all 33800 projection leaves and 24849 inverse brackets.
It derives body action [[1,0],[1104,1]] and the claimed bound 1772603/250000.

Keep generated receipts outside round1: the unchanged verifier enforces
an exact file set. Disable bytecode writes; any __pycache__ invalidates it.
The release itself runs one mathematical worker at a time on the Mini,
single-threaded. Its launcher inherits nice 10 and uses `nice -n 0` to
preserve effective nice 10; on a normal nice-0 shell use `nice -n 10` above.
The fresh environment/exit codes/timing and full outputs are retained in
[../release_validation](../release_validation/). No pod is used unless the
release receipt explicitly says so. Historical two-machine replays are
separately labeled and do not substitute for the release replay.

The integrity checker validates all listed members and rejects extra files;
SHA256SUMS covers the members and MANIFEST.json is externally anchored in the
release report and validation summary. Consult README.md for L0 and prose
limitations, and CHECKER_MAP.md for claim-by-claim coverage.
