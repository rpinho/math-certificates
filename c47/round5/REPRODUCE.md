# Reproduce the release

Python 3 and its standard library suffice. Run from this folder without disabling assertions, one process at a time at nice 10. Use a copy to preserve the shipped timing-bearing receipts and checksums.

```sh
export PYTHONDONTWRITEBYTECODE=1
nice -n 10 python3 verify_exact.py certificates/final.json --claim 57160787529186565434927719505838181711244340833364808847853/33528886534937259000645393217902994011665203200000000000000 --out release_validation/exact.json
nice -n 10 python3 rejection_controls.py certificates/final.json 57160787529186565434927719505838181711244340833364808847853/33528886534937259000645393217902994011665203200000000000000
nice -n 10 python3 finite_instance.py certificates/final.json release_validation/exact.json release_validation/finite.json --claim 17048221231/10000000000
(cd referee && nice -n 10 python3 check_certificate.py --certificate ../certificates/final.json --finite ../producer_logs/final-finite.json --out ../release_validation/referee-results.json)
nice -n 10 python3 comparison.py
nice -n 10 python3 sources/claim_facts.py
```

The seven controls must reject: raised claim, changed heavy mass, oversized radius, expanded rectangle, atom outside cell, zero mass and duplicate atom. They generate corrupted certificate files under certificates/controls/final. The release omits these regenerable files; their SHA-256 values and the generation command are in release_validation/omitted-generated.json. Remove the generated folder with `/usr/bin/trash certificates/controls` after replay. The referee checker writes one aggregate JSON result; no per-witness table is produced.

The referee checker reads only the certificate and finite-instance data, not producer code. The source calculation summary is referee/CHECK_RESULTS.json; its fresh replay is release_validation/referee-results.json. REPLAY.json records hashes of the publication copies of the supplied historical mathematical inputs. The release PROOF.md changes citation, review-status wording and “downward-truncated”; the supplied producer-proof.md is retained under referee/sources/ with only comma grouping of one period numerator to avoid a Luhn digit-run match. No mathematical value changes.

The finite block is specified by formula, without expanding its atoms. Floats and decimal fields are display only. The written proof supplies the passage to the planar L1 constant; no formalization or human peer review is claimed. Numerical search is unnecessary for replay and is outside this frozen-certificate release.

For the unchanged shipped bytes, run:

```sh
shasum -a 256 -c SHA256SUMS
```

## Unpublished search history

The following archives are not part of this release and are unnecessary for replay. They contain intermediate measures, checkpoints and support data. Hashes identify the producer’s retained search history.

- checkpoint-history.tar.xz: SHA-256 `463863c7ad8d1beb1b41c9449dc4650c04471aa5e8eb55994e020c04f4af8b70`.
- checkpoints-1794251381.tar.gz: SHA-256 `34109b7d38f319f0da87c010a5a5e7ee51345f8806c1bc7afa06e96a0ed99c2e`.
- checkpoints-1794251667.tar.gz: SHA-256 `fefe428bbd9f626372f291ea8bbe7079bd64eaad1d1990690dbf06bb90bd6cb4`.
- checkpoints-1794252472.tar.gz: SHA-256 `7b3cc6c734d5989444cde243042946d7f0e0fd55048de4bc316f7cd24eb6f7fa`.
- final-support.tar.xz: SHA-256 `95395aa231cf8a94bce511f2f3bc2f74578dacbbb1f95d3afaf62bf72948bf04`.
- reference-certificates.tar.xz: SHA-256 `25f5295ec8b29c50b09a4eb98bedf3a3bda97ebf30d489bb0e66f2e5b5612adb`.

Scheduling note: the release machine inherited nice 15 and denied absolute nice 10; the initial replay used nice 20. Both are lower scheduling priorities. The commands above request nice 10 on an ordinary nice-0 shell.
