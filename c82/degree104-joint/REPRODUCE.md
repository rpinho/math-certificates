# Release verification from the packet root

Requires Python 3 and python-flint 0.9.0. Set C82_PYTHON to an installed interpreter; the original search additionally used numpy, scipy, highspy and fpylll.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
C82_PYTHON=python3
nice -n 10 "$C82_PYTHON" verify_best.py --certificate certificate.json --target 0.2519696460 --precision 256 --tol 1e-13 --out ../final-verifier.json
nice -n 10 "$C82_PYTHON" review/replay/check.py --certificate review/inputs/certificates/certificate.json --prec 384 --eps 1e-22 --target 0.2519696460 --output ../final-referee.json
shasum -a 256 -c SHA256SUMS
```

To regenerate the packet receipt instead, use --out receipts/release-verifier.json, then run certificate_facts.py and seal.py at nice 10, followed by `egress-gate scan .`. receipts/release-verifier.log records the original packet replay command and environment. Any change to an included file requires resealing. Final replay outputs above are outside the sealed packet.

The root certificate SHA256 is 0c4df95ec7a422943176ab560b961531a41f5f7f83adeb8daae24878de643077. Certificate, verify_best.py and FACTOR_PROVENANCE.json retain the producer bytes unchanged. receipts/frozen-release-verifier.json is the producer's final replay. certificate_facts.py recomputes exact certificate facts, every README gap, and full coefficient overlaps with #280 v3/v4/v5.

seal.py retains the template conventions and recomputes PYTHON_BLOBS.json, MANIFEST.json and SHA256SUMS, including review/ and root REPLAY.json. Its metadata-only blob comparison includes vidigoat's 191064e tree. The round-10 referee receipt is adapted only for release paths and canonical inputs_hash; the original remains review/replay/REPLAY.original.json.

The producer section below is archival. Rounds 9 and 10 continued round 8 warm and met their frozen search bars. Only final archive-num-77-0 files, its restricted master/dual and finished.json are retained in rounds/. Earlier paths in producer records are archival references; restoring a full historical search requires the producer directories, including the superseded round-8 and round-9 certificates, in a separate workspace. The producer's multiworker commands describe its completed run; they are not commands used in this one-core packaging job. run_local.sh accepts C82_PYTHON and uses relative paths and single-threaded numerical settings. The retained coefficient banks are gzip-compressed; restore as described in the producer section before any search reconstruction.

---

Our own round-9 scripts and warm data are copied and reused. Do not rerun bootstrap over results. run_local.sh selects the shared venv, nice -n 10, and single-thread BLAS/FLINT/HiGHS.

Baseline replay:

```sh
./run_local.sh evidence/round9-verifier.py --certificate prior_sources/round9-certificate.json --target 0.2519744488 --precision 256 --tol 1e-13 --out evidence/reproduced-warm.json
```

Warm search (restore compressed warm/provenance data first if needed):

```sh
for f in rounds/warm.json prior_sources/round8-bank.json prior_sources/round9-bank.json prior_sources/union-factor-bank.json; do
  if [ ! -f "$f" ]; then gzip -dc "$f.gz" > "$f"; fi
done
./run_local.sh run_cg.py --state rounds/warm.json --dual rounds/warm-dual.npz --first 52 --measure-first --workers 4 --den-workers 2 --seconds 240 > logs/cg.log 2>&1
```

Timed search is stochastic; all seeds/settings are saved, but runtime differences need not reproduce identical factors. Exact certificates replay deterministically. The full union bank is prior_sources/union-factor-bank.json. Resume using rounds/finished.json's state/dual and the next round index. Only active numerator columns are compacted; all denominator columns and all bank numerator factors remain available.

```sh
./run_local.sh rejection_controls.py --certificate certificate.json --verifier verify_best.py
./run_local.sh source_inventory.py
```

Completed historical JSON/log files may be gzip-compressed. Restore with `gzip -dc FILE.json.gz > FILE.json`. The final LP state/dual remain uncompressed. Every new best and exact replay remain in certificates/.

Redundant old floating LP state archives were moved to reversible macOS Trash at closure. The initial warm state and final state/dual remain. Older floating solutions can be approximately reconstructed from their exact certificate and the full coefficient bank using joint_lp.py; degenerate LP duals and timed stochastic searches need not be identical. Every certified best and exact replay remains in certificates/.
