Shipped: candidate, unrefereed C82 < 0.2520179247552093577392, certified by a separately written (same agent lineage) interval verifier; frozen target met.

Certified B lies in [0.2520179247552093455135, 0.2520179247552093577392]. The gain over 0.2520591386 is at least 0.0000412138447906422608. Exact Fraction comparison of the dyadic upper endpoint with 5041/20000: True. RESULT.json retains the exact fractions.

The public #280 v3 certificate of V. Patankar was first replayed locally: B lies in [0.2520591385259548 +/- 1.94e-17]. This is a public-data reproduction, credited to Patankar. The optimized result uses the Doche construction, Patankar weighted-CVP method and Pinho joint LP/residue pricing; Grinsztajn and Épi contributed earlier factor libraries. No novelty judgment is made.

Current certificate: 10 degree-104 denominators, 18 numerator factors, D=999999999960. Each factor's full coefficients, exact weight, and full coefficient provenance comparisons are in FACTOR_PROVENANCE.json. Search/grid objectives are heuristic; only the frozen interval replay supports the bound above.

Our own ../c82r5 scripts were copied and reused. The verifier imports only stdlib and python-flint and shares no search helper. No Python from vidigoat/optimization-records was downloaded, copied, imported or executed. Its only initial change was the certificate hash pin. This verifies the finite arithmetic construction under the inherited Doche reduction; it is not a formal proof of the reduction or arithmetic backend.

Reproduce in this job directory:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1
nice -n 10 ~/dev/open-science/.venv/bin/python verify_best.py --certificate certificate.json --target 0.2520500000 --precision 256 --tol 1e-13 --out evidence/reproduced-best.json
```

PRIOR_ART.md records the scoped public source checks. STATUS.md records the ongoing search and stopping reason; the final compute accounting, corruption controls and Python blob comparison will be appended when search ends.
