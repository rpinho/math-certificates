# Release verification from the packet root

Requires Python 3 and python-flint 0.9.0. Choose an installed interpreter as C82_PYTHON; search additionally needs numpy, scipy, highspy and fpylll.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
C82_PYTHON=python3
nice -n 10 "$C82_PYTHON" verify_best.py --certificate certificate.json --target 0.2519923410 --precision 256 --tol 1e-13 --out receipts/release-verifier.json
nice -n 10 "$C82_PYTHON" certificate_facts.py
nice -n 10 "$C82_PYTHON" seal.py
egress-gate scan .
```

The certificate, verifier and FACTOR_PROVENANCE.json are unchanged release bytes. Certificate SHA256 is ee9622b5e141489ad6fbf98b0ec5c43ac3e1b657f8876b435e65c536f359fdd5. CERTIFICATE_ENCODING.md lists the released equal fractions without restricted numerators. receipts/frozen-release-verifier.json is the producer's final stated-bound replay. receipts/release-verifier.log gives the actual packet replay command and environment. certificate_facts.py computes exact facts, all README comparison gaps, and full coefficient overlap with #280 v4.

seal.py recomputes PYTHON_BLOBS.json, MANIFEST.json and SHA256SUMS, including any subsequently added review/ and REPLAY.json. The round-7 referee archive is review/, with its receipt REPLAY.json. A verifier rerun that overwrites an included receipt must likewise be followed by resealing; for a final check use --out ../final-verifier.json and capture stdout outside the packet.

The finished producer section follows. Its 0.2519900000 target is the historical frozen search bar and was not met. To replay the delivered bound, use 0.2519923410 as above. Only den-5 round files, their master and the final restricted-9 master are retained; earlier search paths below are archival references. A full fresh search requires omitted round-6 historical inputs in a separate working copy. The two-worker commands describe the producer run; use --workers 1 for a one-core search. run_local.sh uses C82_PYTHON (default python3), with relative paths and single-threaded settings.

---

# Reproduction

All commands run from this job directory; run_local.sh sets single-threaded BLAS and invokes our shared Python at nice 10. Code is reused from our own c82r6/c82r5; third-party inputs are coefficient JSON and GitHub tree metadata only.

Replay the input certificates and solve the complete initial union:

```sh
./run_local.sh bootstrap.py
```

Run the inherited degree-104 weighted-CVP column generation, with two 240-second search workers per dual, complete numerator-bank pricing, exact weight freezing and separately written interval replay after each solve:

```sh
./run_local.sh run_cg.py --state rounds/union.json --dual rounds/union-dual.npz --first 1 --rounds 100 --seconds 240 --workers 2
```

The initial union certificate has already been replayed by bootstrap, so --first 1 skips a duplicate replay. The memory-efficient full-union implementation retains the same grid, constraints and solver, with a single column-contiguous evaluation matrix.

The loop stops after three consecutive rounds whose LP gain is below 1e-10, or at 7.5 hours from evidence/start.json. It leaves the best interval-certified certificate in certificate.json and its hash-pinned verifier in verify_best.py. The 8-hour job ceiling allows final reporting. The 1e-10 no-gain criterion is the inherited numerical tolerance, applied to actual LP gain.

Replay the final certificate against the frozen bar (returns failure if the bar is unmet):

```sh
./run_local.sh verify_best.py --certificate certificate.json --target 0.2519900000 --precision 256 --tol 1e-13 --out evidence/reproduced-best.json
```

To verify a certificate that misses the bar, use the explicitly reported rational in RESULT.json instead. The exact dyadic endpoint/rational comparison is recorded there.

Run the specified rejection controls and Python blob/import inventory:

```sh
./run_local.sh rejection_controls.py --certificate certificate.json --verifier verify_best.py
./run_local.sh source_inventory.py
```

The interrupted first round was resumed with `./run_local.sh resume_cg.py`:
its saved search checkpoints were merged without rerunning them, then rounds
2 onward used the inherited loop. That resume script consumes a specific saved
checkpoint; use the main loop command above for a new run. The finished job's
state and dual are named in rounds/finished.json. To continue that state on a
future explicitly authorized job, start at the next unused round number and
account for the existing consecutive no-gain count; this job stopped at three.

PROOF.md gives the inherited Doche construction and extraction argument.
evidence/final-stated-bound-replay.json is the final replay at the stated
rational; RESULT.json gives the exact upper-endpoint comparison. The
provenance report uses actual round-6 source files, rather than attributing
everything in the mixed r7 union to round 6.

NUMERICS.md describes the inherited verifier enclosure formulas. The verifier imports only stdlib and python-flint and shares no search helper. It was separately written by the same agent lineage, and is not an independent checker.
