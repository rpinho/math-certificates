# Release verification from the packet root

Requires Python 3 and python-flint 0.9.0. Set C82_PYTHON to an installed interpreter; the original search additionally used numpy, scipy, highspy and fpylll.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
C82_PYTHON=python3
nice -n 10 "$C82_PYTHON" verify_best.py --certificate certificate.json --target 0.2519744488 --precision 256 --tol 1e-13 --out ../final-verifier.json
nice -n 10 "$C82_PYTHON" review/replay/check.py review/inputs/certificates/certificate.json --prec 256 --tol 1e-22 --order 16 --target 0.2519744488 --output ../final-referee.json
shasum -a 256 -c SHA256SUMS
```

To regenerate the packet receipt instead, use --out receipts/release-verifier.json, then run certificate_facts.py and seal.py at nice 10, followed by `egress-gate scan .`. receipts/release-verifier.log records the original packet replay command and environment. Any change to an included file requires resealing. Final replay outputs above are outside the sealed packet.

The root certificate SHA256 is 1e5af10142c7223df4cd56a4279727a7610137dab8e5f2d95dcb19b3030ac67e. Certificate, verify_best.py and FACTOR_PROVENANCE.json retain the producer bytes unchanged. receipts/frozen-release-verifier.json is the producer's final replay. certificate_facts.py recomputes exact certificate facts, every README gap, and full coefficient overlaps with #280 v3/v4/v5.

seal.py retains the template conventions and recomputes PYTHON_BLOBS.json, MANIFEST.json and SHA256SUMS, including review/ and root REPLAY.json. Its metadata-only blob comparison includes vidigoat's 191064e tree. The round-9 referee receipt is adapted only for release paths and canonical inputs_hash; the original remains review/replay/REPLAY.original.json.

The producer section below is archival. Round 9 continued round 8 warm and met its frozen search bar. Only final archive-num-51-1 files, its restricted master/dual and finished.json are retained in rounds/. Earlier paths in the producer records are archival references; restoring a full historical search requires the producer directories, including the superseded round-8 certificate, in a separate workspace. The standalone round-8 certificate and historical encoding note are omitted. The producer's multiworker commands describe its completed run; they are not commands used in this one-core packaging job. run_local.sh accepts C82_PYTHON and uses relative paths and single-threaded numerical settings.

---

Run from this job directory using the shared venv via run_local.sh (nice 10, all numerical thread counts one). Own round-8 scripts and full state/dual were copied by bootstrap.py; do not rerun bootstrap over a completed result.

Warm baseline replay:

```sh
./run_local.sh evidence/round8-verifier.py --certificate prior_sources/round8-certificate.json --target 0.2519758217 --precision 256 --tol 1e-13 --out evidence/reproduced-warm.json
```

The baseline command uses round 8's copied, unchanged pinned verifier; verify_best.py is pinned to this continuation's best packet.

Search command used:

```sh
./run_local.sh run_cg.py --state rounds/warm.json --dual rounds/warm-dual.npz --first 22 --measure-first --workers 4 --den-workers 2 --seconds 240 > logs/cg.log 2>&1
```

Full-bank numerator pricing uses four single-threaded processes from round 23; its original serial code is retained in evidence/numerator_search_serial.py. The complete-bank reduced-cost formulas and order are unchanged.

Each accepted solve is frozen and passed through a separately written (same agent) interval verifier. The exact replay command for the final packet is in REPORT.md. Timed stochastic search is not claimed to be bit-identical; all seeds and settings are saved. Resume from rounds/finished.json's state/dual with --first equal to its last round plus one. The full mutable bank is prior_sources/union-factor-bank.json.

```sh
./run_local.sh rejection_controls.py --certificate certificate.json --verifier verify_best.py
./run_local.sh source_inventory.py
```

Older history can be stored as JSON/log gzip files. Restore with `gzip -dc PATH.json.gz > PATH.json`. Retired duals are regenerable with `./run_local.sh joint_lp.py --input rounds/STATE.json --prefix rounds/recomputed-STATE`; an LP dual on a degenerate face may differ. Current final state and dual remain uncompressed. Complete standalone best certificates and exact replays are retained in certificates/.

To keep the packet below 50 MB, old compressed floating LP master caches were moved to macOS Trash. The initial rounds/warm.json.gz and the current final master/dual are retained; certificate/replay records and every certificates/best_*.json remain. Old floating states/duals can be reconstructed approximately with joint_lp.py from the corresponding exact certificate; degenerate LP duals and timed searches need not be bit-identical. Restore warm.json from its gzip file before the warm search command if required.
