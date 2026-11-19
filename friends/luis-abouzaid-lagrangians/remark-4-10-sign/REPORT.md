# Independent referee result

The claim holds as a mathematical proof using the published Floer foundations
and triangle classification. The integral relative-sign prediction is actually
printed in the coauthored paper. The signed correspondence yields nonzero
ordinary trace; opposite integral signs would give identically zero trace.

See [VERDICT.md](VERDICT.md), the independent geometric and convention audit
in [AUDIT.md](independent_audit/AUDIT.md), and the exact symbolic results in
[RESULTS.json](independent_audit/RESULTS.json). No supplied verifier was imported.
The computational checks are conditional on the analytically reviewed
geometric premises; they are not a numerical certification of orientations.

Reproduce from this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 ~/dev/open-science/.venv/bin/python independent_audit/recompute.py
```

Source URLs and fresh public checks are in
[PRIOR_ART.md](independent_audit/PRIOR_ART.md) and PUBLIC_RECHECK.json.
The actual preprint, journal article and Ono paper were downloaded and opened.
No priority judgment is made. A fully explicit signed critical-corner count
would strengthen the analytic documentation of the accepted argument.
