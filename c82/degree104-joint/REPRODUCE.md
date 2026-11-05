# Release verification from the packet root

Requires Python 3 and python-flint 0.9.0 (the recorded backend). The search additionally uses numpy, scipy, highspy and fpylll; these are not needed for the certificate replay. Choose an installed interpreter as C82_PYTHON. Do not run the producer's search in the sealed packet: use a working copy.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
C82_PYTHON=python3
nice -n 10 "$C82_PYTHON" verify_best.py --certificate certificate.json --target 0.2520179248 --precision 256 --tol 1e-13 --out receipts/release-verifier.json
nice -n 10 "$C82_PYTHON" seal.py
```

The original release receipt is receipts/frozen-release-verifier.json. The packaged replay is receipts/release-verifier.json. Both retain exact dyadic endpoints. Certificate SHA256: a4061273a4c69c593dac56ede91a1c5c2e9afbb70eb19c037d712bf5c20fe36e. The frozen-release receipt was made on the producer bytes (SHA256 2b5bf95d950a96193864689c6b77c08b5a79528d0c695de929c1df13944aef18), which differ only in how one exponent is written; see README "Certificate encoding". seal.py recomputes the Python blob/import comparison, MANIFEST.json and SHA256SUMS, including any added review/ and REPLAY.json. Do not reuse an earlier certificate's review receipt for this certificate.

The commands below are inherited producer documentation. Their target is the earlier search bar, and the archive omits other rounds and later continuation; they are not a promise to reproduce the stochastic search trajectory. The producer's two-worker commands describe its historical run; use --workers 1 for a one-core rerun. See METHOD.md.

---

# Reproduce the C82 union and column generation

Use our shared venv, single-threaded arithmetic, nice 10, within this job directory. All scripts reused from ../c82r5 are ours. No vidigoat Python is needed or permitted.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1
C82_PYTHON=python3
nice -n 10 "$C82_PYTHON" verify_public.py --certificate prior_sources/pr280-v3-certificate.json --target 0.2520591386 --precision 256 --tol 1e-13 --out evidence/reproduced-public.json
nice -n 10 "$C82_PYTHON" prepare_union.py
nice -n 10 "$C82_PYTHON" joint_lp.py --input union-input.json --prefix rounds/reproduced-union
nice -n 10 "$C82_PYTHON" run_cg.py --state rounds/reproduced-union.json --dual rounds/reproduced-union-dual.npz --seconds 240 --workers 2 --rounds 12
```

The union master uses all 7 union denominator coefficient arrays and all 895 union numerator coefficient arrays, N=524288, the inherited HiGHS simplex/row-generation method. Multiplicities are frozen at scale 10^12 and numerator powers at dyadic scale 2^20 by our round-5 freeze routine. Later standard restricted-master solves discard zero numerator columns while screening the entire union numerator bank against each new dual. All union denominators stay in the warm-start bank.

CVP uses inherited defaults: degree 104, residue H=X(X-1)P4, 1024 stratified evaluation samples, 380-bit evaluations, exact integer Gram LLL with delta=.99, budgeted Schnorr–Euchner enumeration with 4 million nodes and 16 retained points, up to 8 IRLS steps per start. Each proposal is priced against the complete dual. Floating results do not certify any bound. Per-batch JSON records settings, candidates and timing; replay the final certificate to reproduce the mathematical result.

```sh
nice -n 10 "$C82_PYTHON" verify_best.py --certificate certificate.json --target 0.2520500000 --precision 256 --tol 1e-13 --out evidence/reproduced-best.json
nice -n 10 "$C82_PYTHON" rejection_controls.py --certificate certificate.json --verifier verify_best.py
```

The second command deliberately rejects changed bytes, a zero denominator multiplicity (hash repinned), and a shared numerator/denominator factor (hash repinned). These are requested controls, not numerical search failures. Verification is separately written (same agent), using stdlib and python-flint only. Exact dyadic upper endpoint comparison with rational 5041/20000 is saved in RESULT.json. No novelty judgment is made; claims remain candidate and unrefereed.

NUMERICS.md was copied from round 5 and describes the verifier's integration enclosures. Factor names are labels only; FACTOR_PROVENANCE.json compares full coefficient arrays. The final blob inventory uses git hash-object on every .py and compares it with the complete GitHub trees at both prohibited-code commits, downloading tree metadata only.

After the original-order loop stalled for three rounds, the standard positive-weight warm-start continuation used `run_cg.py --state rounds/restricted-7.json --dual rounds/num-3-0-dual.npz --first 7 --rounds 12 --seconds 240 --workers 2 --rotate-warm`. Per-worker reordered coefficient/weight inputs are saved as rounds/warm-K-W.json. All union denominators are retained.
