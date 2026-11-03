# Release corrections and verification

This is a packaging revision of the frozen 0.612300 candidate. It changes
no certificate selector, part, range plan, historical arithmetic receipt,
or arithmetic checker module. `CHANGES.diff` records the top-level source
and documentation corrections; the inventory includes the added review
reports and release evidence.

- Included the parent job's unchanged PRIOR_ART.md.
- Corrected the gain to +0.000058 over Wikström's arXiv 0.612242 and
  +0.000006 over our earlier, never-filed 0.612294 candidate.
- Distinguished Wikström's preprint values from the live table values.
- Described the checker as separately written by the same agent.
- Credited Wikström's equation (12) for the extended phase congruence.
- Made the u=0, x2=0 representative convention explicit; the scaled-Bloch
  inequality is not asserted on redundant u=0, x2>0 representatives.
- Set the false-exclusion and unsupported-phase fixtures' area weight to
  1; also corrected the same ineffective fixture in the fast suite.
  The false witness now passes prepare() before arithmetic rejects it at
  the refinement cap, and the unsupported phase rejects as invalid phase.
  Astra's separate simple-form control rejects at the midpoint; stale
  checker hashes, false precision and false radius also reject as intended.
- Reran all three supplied suites, Astra's corrected controls, historical
  aggregation, and three candidate ranges at actual nice 10. The mixed
  aggregate uses three fresh and 159 historical receipts. No full fresh
  arithmetic replay is claimed.

The review copies retain both FLAG verdicts. Their local filesystem paths,
and local paths in historical/control output logs, were replaced for
publication. The code/data and historical arithmetic receipts are unchanged.
An initial nice-20 launch was stopped; the final results were rerun at
actual nice 10 and supersede its output.

Reproduce the bounded release checks with Python 3 and python-flint 0.9.0.
Run from this packet directory at actual nice 10 (the usual `nice -n 10`
command is appropriate only when starting from nice 0), and set
OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1 and
PYTHONDONTWRITEBYTECODE=1:

```sh
python -B check_c57_forest_controls.py C57_FOREST_V2.json
python -B test_c57_fast_rejections.py
python -B test_c57_forest_verifier.py
python -B release_validation/astra_corrected_controls.py
python -B verify_c57c_forest.py C57_FOREST_V2.json --aggregate cert_receipts/*.json
python -B verify_c57c_forest.py --part cert_parts/prefix.jsonl.gz --leaf-start 0 --leaf-stop 589
python -B verify_c57c_forest.py --part cert_parts/pi_critical_b.jsonl.gz --leaf-start 1000 --leaf-stop 2000
python -B verify_c57c_forest.py --part cert_parts/theta_tail.jsonl.gz --leaf-start 6750 --leaf-stop 7000
shasum -a 256 -c SHA256SUMS
```

The first three suites must report all controls passing; the corrected
referee controls must end CORRECTED_CONTROLS_PASS. Aggregation must report
VERIFIED_CANDIDATE_UNREFEREED and 489,994 leaves. Individual ranges report
VERIFIED_ARITHMETIC_RANGE_NOT_FULL_PROOF; no single range proves a constant
bound. Reproduction changes generated results, so inventories should be
checked before running commands that overwrite their output files.
