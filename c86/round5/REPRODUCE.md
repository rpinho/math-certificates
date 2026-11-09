# Reproduce the bound

Use ordinary Python with assertions enabled and python-flint installed. The release replay used CPython 3.12 and python-flint; exact versions are in release_validation/environment.json. No search or optimization is needed. Verify the distributed bytes before replay, then run in a disposable copy of this folder unless a `cd` is shown. Fresh receipts contain new timers and output hashes, so they need not match the archived receipt bytes. Each parallel stage uses at most four workers; run the stages sequentially. Set BLAS/OpenMP thread limits to one if other numerical libraries are loaded.

```sh
shasum -a 256 -c SHA256SUMS
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
mkdir -p release_validation logs controls
nice -n 10 python verify_linear.py certificate.json --beat 1.8054956 --output release_validation/first.json
nice -n 10 python parallel_verify.py certificate.json --workers 4 --output release_validation/second.json
nice -n 10 python audit_artifact.py certificate.json release_validation/second.json --output release_validation/cover-audit.json
nice -n 10 python negative_controls.py certificate.json release
nice -n 10 python negative_integral_control.py certificate.json release
nice -n 10 python comparison.py
cd referee
nice -n 10 python referee_check.py ../certificate.json --output ../release_validation/referee-structure.json
nice -n 10 python cover_check.py ../certificate.json --workers 4 --output ../release_validation/referee-cover.jsonl
nice -n 10 python corruption_controls.py
cd ..
nice -n 10 python referee/audit_saved_cover.py certificate.json release_validation/referee-cover.jsonl --output release_validation/referee-cover-audit.json
```

Both producer checkers must report PASS, the exact cover/hash audit must accept every support cell and reject all four cover mutations, and both producer implementations must reject a false declared mean, raised weights and a perturbed density with recomputed mean. The referee structure/integral checker must pass, its full closed cover must complete, and its three own corruption controls must reject. The separate saved-cover assembly checks rational endpoints, complete parent coverage, positivity and the fresh cover hash; the cover checker itself recomputes every Arb inequality.

The first checker uses 160-bit Arb with order 18; the second uses 192-bit Arb with order 8. The referee uses 192-bit Arb with order 32. The different enclosure minima are conservative proof margins, not estimates of the actual minimum. Exact rational comparisons and Arb decisions determine acceptance; display floats, timers and worker IDs do not.

The finite certificate is exactly the normalized mean T/m. Smith’s theorem turns that finite checked measure into a limiting trace statement. See PROOF.md for the all-size argument and its one energy-sign clarification relative to the adaptive-cone proof.

The cover files and corrupted witness certificates are regenerable and are not distributed. The original and fresh cover hashes are listed in sources/omitted-artifacts.json, and their commands are above. Producer cover ordering is canonical; referee parallel JSONL order and timers vary. A different referee file hash is expected on replay, with the same exact coverage and enclosed minimum. Source documents are cited in referee/sources/SOURCES.md.
