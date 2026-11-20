# Release verification from the packet root

Requires Python 3 and python-flint 0.9.0. Set C82_PYTHON to an installed interpreter; the original search additionally used numpy, scipy, highspy, fpylll and mpmath.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
C82_PYTHON=python3
nice -n 10 "$C82_PYTHON" verify.py --certificate certificate.json --sha dc129b7586da99042ff04e6cbf435d0b2e7e761ccfb87fc218da079b3f26aa33 --precision 256 --tol 1e-13 --target 0.2519694759 --out ../final-verifier.json
nice -n 10 "$C82_PYTHON" -I review/replay/check.py review/inputs/certificates/certificate.json
shasum -a 256 -c SHA256SUMS
```

The first command takes about a minute on one core. The referee's checker takes about 30 minutes on one core at its default tolerance (2^-60) and prints PASS against 0.2519694759; with `--target 0.2519694758` it must fail, and review/replay/report.md lists its controls. To regenerate the packet receipt instead, use --out receipts/release-verifier.json, then run certificate_facts.py and seal.py at nice 10, followed by `egress-gate scan .`. receipts/release-verifier.log records the original packet replay command and environment. Any change to an included file requires resealing. Final replay outputs above are outside the sealed packet.

The root certificate SHA256 is dc129b7586da99042ff04e6cbf435d0b2e7e761ccfb87fc218da079b3f26aa33. Certificate, verify.py and FACTOR_PROVENANCE.json retain the producer bytes unchanged. receipts/frozen-release-verifier.json is the producer's final replay (evidence/final-replay.json). certificate_facts.py recomputes exact certificate facts, every README gap, the replay intervals of #280 v6 and of my round 11, and full coefficient overlaps with #280 v3/v4/v5/v6.

seal.py retains the template conventions and recomputes PYTHON_BLOBS.json, MANIFEST.json and SHA256SUMS, including review/ and root REPLAY.json. Its metadata-only blob comparison includes vidigoat's 191064e and e3bae2e trees. The round-12 referee receipt is adapted only for release paths and canonical inputs_hash; the original remains review/replay/REPLAY.original.json.

The producer section below is archival. It describes the completed round-12 search, whose inputs are in inputs/ (the coefficient banks gzip-compressed; restore with `gzip -dc inputs/bank.json.gz > inputs/bank.json` and likewise full-bank) and whose final alternation files are in rounds/. Restoring the whole search also needs the external producer archive, including the round-11 directory, for files named in the producer section and omitted here (NOTE.md). The producer's multiworker commands describe its completed run; they are not commands used in this one-core packaging job. run_local.sh accepts C82_PYTHON and uses relative paths and single-threaded numerical settings; the producer's own wrapper pointed at a machine-specific interpreter.

---

# Reproduce the C82 packet

Use the final command in REPORT.md to replay the shipped certificate. The verifier reads just the pinned JSON, the Python standard library and python-flint. Use the digest printed in the report.

For a search replay, use a fresh local copy of the scripts, inputs, and a STATUS.md containing the job's first line. Copy BAR.json into that directory and create logs/, rounds/, certificates/ and evidence/. The worker wrapper sets single-threaded numerical libraries and runs at nice 10.

~~~sh
./run_local.sh worker.py
./run_local.sh -c "from result import save; save('inputs/v6.json','evidence/v6.json','#280 v6 exact incumbent')"
./run_local.sh prepare.py
./run_local.sh joint_lp.py --input inputs/union-master.json --prefix rounds/union-master
./run_local.sh search.py
./run_local.sh alternate.py
./run_local.sh controls.py
~~~

The warm state and dual were copied byte-for-byte from round 11. The polynomial bank was extracted from member prior_sources/union-factor-bank.json of round 11's prior_sources/factor-banks.tar.xz. The incumbent hash and MIT source are in inputs/SOURCE.md. The regenerable root caches come from isolating the raw polynomials again. Prepare the frozen target of 0.2519694883 before any replay search.

Alternations use wall-budgeted LLL and CVP workers. The random seeds are deterministic, but the number of completed iterations depends on CPU speed and load. Replaying a saved certificate is deterministic at the specified precision.
