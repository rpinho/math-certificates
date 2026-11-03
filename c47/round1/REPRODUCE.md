# Reproduce the C47 round 1 checks

From the math-certificates repository root, enter `c47/round1`. Exact verification needs Python 3 and its standard library only. No network, compiled library, NumPy, SciPy or search producer is needed for the six release checks. Verify the frozen hashes before running, since reruns replace receipts and timing fields.

```sh
cd c47/round1
shasum -a 256 -c SHA256SUMS
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
PY=${PY:-python3}
nice -n 10 "$PY" verify_exact.py certificates/half59.json --claim 170311/100000 --out logs/half59-exact.json > logs/release-exact.log
nice -n 10 "$PY" rejection_controls.py certificates/half59.json 215956002657486428307163448091951082893881/126800499112387565339223240212480000000000 > logs/release-controls.log
nice -n 10 "$PY" finite_instance.py certificates/half59.json logs/half59-exact.json logs/half59-finite.json --claim 170311/100000 > logs/release-finite.log
nice -n 10 "$PY" -I sources/tomar-v5/lowerbound/check_exact2.py certificates/half59-measure.json > logs/release-half59-upstream.log
nice -n 10 "$PY" -I sources/tomar-v5/lowerbound/check_exact2.py sources/tomar-v5/lowerbound/c2lower_1p70272.json > logs/release-tomar50-upstream.log
nice -n 10 "$PY" audit_receipts.py > logs/release-receipt-audit.log
```

All six commands must exit 0. The seven intentionally invalid certificates each cause the child verifier to exit 1; their suite exits 0 only when all seven reject. Generated corruption cases remain under `certificates/controls/half59`. The two upstream runs write `.check2.json` beside their respective input measures, inside this copy.

The candidate exact ratio must be

```
215956002657486428307163448091951082893881/126800499112387565339223240212480000000000
```

Both exact calculations must agree as fractions. The candidate uses 59 atoms, 559 explicit retained witnesses; Tomar's enumeration produces 33,356 rectangles. His original 50-atom baseline must reproduce

```
482167717377842991882283179477574801392641890014291050323/283174368139841919615520431313000857449005056000000000000
```

The finite receipt must give h=2, N=2,147,177, positive smear radius, and finite ratio strictly greater than 170311/100000. `audit_receipts.py` checks all 559 enlarged-radius inequalities, exact half-cell extraction, source identity, and receipt consistency. Fresh release results are in [logs/release-checks.json](logs/release-checks.json); historical upstream geometry output is retained in `logs/half59-upstream.log` and `logs/tomar50-upstream.log`. Timing fields may differ on rerun; mathematical fractions and frozen inputs must agree.

## Source identity

Tomar's unchanged checker was freshly fetched at v5 commit `3af09fc359ce262f4a7f63d34b0d97e6d4d95d1a`:

- [check_exact2.py](https://github.com/tejasvi/square-maximal-weak-type/blob/3af09fc359ce262f4a7f63d34b0d97e6d4d95d1a/lowerbound/check_exact2.py), SHA-256 `abb311c73157e35f384ee2aca6aded4772cc13ea8f70650b8499400621a80e23`.
- [hf.py](https://github.com/tejasvi/square-maximal-weak-type/blob/3af09fc359ce262f4a7f63d34b0d97e6d4d95d1a/lowerbound/search/hf.py), SHA-256 `822f5106c7f899e93f62e3c6a2d0afc8dd54565ddbbee1e65d46f5595b5c08c9`.

The retained files match both the fresh pinned downloads and the preceding packet byte for byte. The upstream Apache-2.0 LICENSE is retained. [MANIFEST.json](MANIFEST.json) records copied-source hashes, documentation changes, and the omitted process identifier in the public hf summary.

## Optional certificate reconstruction

Work in a scratch copy of this packet because these commands replace the frozen measure and certificate. A C compiler is needed. The producer is not trusted by the exact verifier.

```sh
nice -n 10 "$PY" extract_half.py
nice -n 10 cc -O3 -shared -fPIC -o libcertificate.so certificate_scan.c -lm
nice -n 10 "$PY" make_fast_certificate.py certificates/half59-measure.json certificates/half59.json --reach 1396/125
```

The extraction preserves all selected rational atom coordinates and masses. Only the vertical period is halved; there is no further tuning. Then rerun the six checks above.

## Historical floating provenance experiment

This release does not rerun the six-hour search. [logs/hf-summary.json](logs/hf-summary.json) records the frozen result: 1.7027237336033003 after 21,572.02 CPU seconds, 14,908 objective evaluations, still in the initial 50-atom polish, below 1.7030, no accepted-round output. A controlled SIGINT ended the run with return code -2. Large raw search logs are excluded.

The historical environment was Python 3.12.3, NumPy 2.5.4, SciPy 1.18.1, GCC 13.3.0, single-threaded, with an 8 GiB process address-space cap. The unchanged hf.py defaults were 20 rounds, grid 500, maxit 400, six tries, seed 1103, no HL_REACH override. Floating trajectories and machine timing are environment dependent. To explore the same upstream method in a scratch copy with NumPy/SciPy installed:

```sh
unset HL_REACH
nice -n 10 cc -O3 -shared -fPIC -o sources/tomar-v5/lowerbound/search/libeval.so sources/tomar-v5/lowerbound/search/eval.c -lm
nice -n 10 "$PY" sources/tomar-v5/lowerbound/search/hf.py certificates/tomar50-float-start.json logs/hf-accepted.json 1103
```

`observe_hf.py` is the retained observational wrapper used historically instead of direct invocation. It executes unchanged hf.py through runpy and records objective returns without changing objective, RNG or optimization decisions. It includes initial-input evaluations and does not equate a best observed trial with an accepted configuration. It needs a separately enforced time/resource limit; the historical guard and resource logs are not included here. The commands above do not reproduce the exact historical stop time. This floating probe does not certify a bound and does not establish a distinct method.

**Verification level: L0** for the bound as a whole (definitions: https://github.com/rpinho/math-certificates/blob/59eeb7097f806da05187b5f234445be3589204d4/VERIFICATION_LEVELS.md)
Our exact verifier was separately written by the same AI agent, and Tomar's own unchanged exact checker reproduces the same fraction.

Tomar's upper-bound checkers and Lean proofs were not run here. The earlier 117-atom packet was reviewed by GPT-6 Astra (ACCEPT) and Claude Opus 5.5 via Claude Science (FLAG; it corrected an atom-pair count). Both then reviewed this release (the 59-atom certificate, proof, table diff and text), and their findings were wording corrections only, concerning the review attribution and the description of the method; those corrections are fixed in this text. Our publish gate requires both reviewers to accept the final bytes; there is no human referee. A note to Tomar is planned, not sent. No filing, publication or outreach is performed by these reproduction steps.
