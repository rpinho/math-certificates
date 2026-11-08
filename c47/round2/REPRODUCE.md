# Reproduce the release

Python 3 with its standard library is sufficient for all bound checks. Run from this folder without disabling assertions. Use one process at a time, at nice 10.

```sh
export PYTHONDONTWRITEBYTECODE=1
nice -n 10 python3 verify_exact.py certificates/final.json --claim 1771220457083239070854869084751983500209800598673/1039431510074799032049552767561236480000000000000 --out release_validation/exact.json
nice -n 10 python3 rejection_controls.py certificates/final.json 1771220457083239070854869084751983500209800598673/1039431510074799032049552767561236480000000000000
nice -n 10 python3 finite_instance.py certificates/final.json release_validation/exact.json release_validation/finite.json --claim 681611223/400000000
(cd referee && nice -n 10 python3 independent_check.py)
nice -n 10 python3 comparison.py
shasum -a 256 -c SHA256SUMS
```

The seven controls must all reject: raised claim, changed heavy mass, oversized radius, expanded rectangle, atom outside cell, zero mass, duplicate atom. They write corrupted certificates under certificates/controls/final and their receipt under logs. Replays overwrite timing-bearing outputs; use a copy if preserving the shipped checksums. The referee run also regenerates referee/witness_results.tsv, which is deliberately omitted from the public packet; see referee/README.md for its original SHA-256. After inspection, remove it with `/usr/bin/trash referee/witness_results.tsv` before the checksum check so the packet again has its shipped file set.

The referee checker reads only its own saved certificate and finite receipt, not producer programs. Its saved producer proof has the original bytes; PROOF.md is the release presentation of the same mathematical argument with a Corrections note. REPLAY.json records the actual historical input files, with hash provenance explained there.

Search is unnecessary for checking the bound. Our selected search sources and final rationalized snapshot are in search/. They require NumPy and SciPy for numerical exploration and a C++17 compiler for evaluator.cpp; they are not the exact evidence. From search/, compile `c++ -O3 -std=c++17 -dynamiclib evaluator.cpp -o libsearch.dylib`. See search/README.md for scope. A fresh search is not promised to reproduce the same optimization trajectory; the frozen certificate is the claimed artifact.

The written proof supplies the periodic-to-finite L1 argument. The finite receipt specifies the enormous finite block by a formula; no enumeration of its atoms is needed. Floats in receipts and decimal expansions are display only.
