# Reproduce the release

Python 3 and its standard library suffice. Run from this folder without disabling assertions, one process at a time at nice 10. Use a copy to preserve the shipped timing-bearing receipts and checksums.

```sh
export PYTHONDONTWRITEBYTECODE=1
nice -n 10 python3 verify_exact.py certificates/final.json --claim 28587164107974856086021451670774323985081039148875463526401/16766169836386813382037844357636904350593843200000000000000 --out release_validation/exact.json
nice -n 10 python3 rejection_controls.py certificates/final.json 28587164107974856086021451670774323985081039148875463526401/16766169836386813382037844357636904350593843200000000000000
nice -n 10 python3 finite_instance.py certificates/final.json release_validation/exact.json release_validation/finite.json --claim 8525251857/5000000000
(cd referee && nice -n 10 python3 referee_check.py --certificate ../certificates/final.json --finite ../producer_logs/final-finite.json --output ../release_validation/referee-results.json --witness-output ../release_validation/witness_checks.csv)
nice -n 10 python3 comparison.py
nice -n 10 python3 sources/claim_facts.py
```

The seven controls must reject: raised claim, changed heavy mass, oversized radius, expanded rectangle, atom outside cell, zero mass and duplicate atom. They generate corrupted certificate files under certificates/controls/final. The release omits these regenerable files; their SHA-256 values and the generation command are in release_validation/omitted-generated.json. Remove the generated folder with `/usr/bin/trash certificates/controls` after replay. The referee checker produces a regenerable per-witness table; its original hash is in referee/README.md and its replay hash in release_validation/omitted-generated.json. The table is omitted from the package.

The referee checker reads only the certificate and finite-instance data, not producer code. The source calculation summary is referee/CHECK_RESULTS.json; its fresh replay is release_validation/referee-results.json. REPLAY.json records hashes of the publication copies of the supplied historical mathematical inputs. The release PROOF.md changes citation and review-status wording; the supplied producer-proof.md is retained byte-for-byte under referee/sources/.

The finite block is specified by formula, without expanding its atoms. Floats and decimal fields are display only. The written proof supplies the passage to the planar L1 constant; no formalization or human peer review is claimed. Numerical search is unnecessary for replay and is outside this frozen-certificate release.

For the unchanged shipped bytes, run:

```sh
shasum -a 256 -c SHA256SUMS
```

## Unpublished search history

These producer archives and starting measures are omitted and unnecessary for replay. They identify unpublished search history.

- checkpoint-history.tar.xz: SHA-256 `97c43c8b1bff1ff891117c915847358fc9f6180e44824cb397b52afb618a170e`.
- checkpoints-1794272020.tar.gz: SHA-256 `6d27fb16e3d0125a879cc6a1aa889bdfb8df0df1050d24923d392002eebcf9e0`.
- checkpoints-1794273131.tar.gz: SHA-256 `c41bcf39c4be669e6d462d9e81dcb3dcf78cc40bb300ac6b91e2bf0f4c2c17b0`.
- checkpoints-1794274178.tar.gz: SHA-256 `c932fc1c76877b2b0aa90ba522d15106a6bf06a562b55ae64c041989d440b53d`.
- corruption-inputs.tar.xz: SHA-256 `7c8688530e77733148d28fa915798e8e0d54df97fd522c22e64af11bb4ba3ea8`.
- removal-sources.tar.xz: SHA-256 `016b64dc4270d64f491e7cc4460971c14423199105267a7ef7be10600e552e8e`.
- start392-measure.json: SHA-256 `0721d70642239d1da54039f64fdce61a8eaa06be24c2f5b9dcad39771225cd2e`.
- start392.json: SHA-256 `c37382e18f55d07f442fe65b259d4e04d195f696d7ef06aed698143cfbe00ae3`.

Scheduling note: the source shell inherited nice 15 and denied absolute nice 10. The first replay ran at nice 20, and the final referee replay retained nice 15; both are lower CPU priorities. Run at absolute nice 10 where permitted.
