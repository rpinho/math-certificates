# Reproduce the release certificate

Run from this packet's root with Python 3.12 and python-flint 0.9.0. Verification needs only the standard library and python-flint. Search additionally uses numpy, scipy, highspy, mpmath and numba; the historical environment is evidence/environment.json. Set PYTHON to a Python interpreter with these packages installed.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1
PYTHON=python3
nice -n 10 "$PYTHON" verify_interval.py --certificate certificate.json \
  --target 0.252404806 --precision 256 --tol 1e-13 --out reproduced.json
```

The release rerun on the Apple M4 Mini took **18.396355 seconds** of checker wall time, at 256 bits and tolerance 1e-13. It used one process and one FLINT thread, launched at nice 10 (effective nice 20 inherited from the job). See receipts/release-verifier.json and its log. Exact dyadic endpoints determine acceptance; a printed midpoint or tolerance is not an upper endpoint. This is a fresh run on the release copy, separate from the producer's historical 18.65-second replay.

verify_interval.py and verify_final.py are byte-identical copies of the producer's final pinned verifier. verify_public.py is its original public-certificate version with a different pinned hash. The fresh final receipt binds its own source hash. The original producer receipt is evidence/final-replay.json. NUMERICS.md explains all panel enclosures.

The referee archive can be rerun independently, sequentially after the first command:

```sh
nice -n 10 "$PYTHON" review/replay/check.py \
  --certificate review/inputs/certificates/certificate.json \
  --precision 384 --tol 1e-20 --controls --output referee-reproduced.json
```

Its historical accepted run took 452.66 seconds with controls. That independent calculation was not rerun during packaging; its byte-identical source, result and report are archived. The original report's job-relative reproduction command uses its original layout; the command above uses the release layout. Only Python and python-flint are needed.

## Search archive

Search is heuristic and runtime-limited, so exact completed-start counts can vary. It is not part of the certificate replay. The scripts are at the packet root, states and dual arrays in runs/, and public warm-start data in prior_sources/. No code from @vidigoat (#280) was imported or executed by the producer. Credit Ricardo Pinho (#301) for the inherited reduced-cost and residue-class infrastructure. The legacy cvp_gram.py has the documented duplicate-seed limitation; use cvp_fixed.py for a new search.

```sh
nice -n 10 "$PYTHON" cvp_fixed.py --state runs/pilot-early.json \
  --dual runs/pilot-early-dual.npz --degree 104 --points 1024 \
  --seconds 180 --iterations 8 --nodes 4000000 --seed 7104 \
  --out search-reproduced.json
nice -n 10 "$PYTHON" merge_evaluate.py runs/after-dual104.json runs/fixed104.json \
  --baseline runs/pilot-early.json --prefix runs/reproduced-final --threshold 0.00001
```

Re-optimisation yields a newly generated certificate that must pass its own pinned verifier; the release verifier deliberately rejects different certificate bytes. Floating LP/pricing results do not certify bounds. No search or LP was rerun for this release. Cap reproduction at two concurrent processes and keep each numerical library to one thread.

For integrity, run `shasum -a 256 -c SHA256SUMS`. MANIFEST.json lists payload hashes excluding itself and SHA256SUMS to avoid circular hashes; SHA256SUMS includes MANIFEST.json and excludes only itself.
