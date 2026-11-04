# Clean-room referee archive

The replay inputs are kept byte-for-byte as given to the referee in review/inputs/PROOF.md and review/inputs/certificates/certificate.json. The original proof had the wrong Doche title; the release PROOF.md corrects it and writes out the extraction argument supplied by the clean-room referee in REFEREE.md. The archived proof is historical replay input, not the corrected release proof.

The original receipt is replay/REPLAY.original.json (also preserved as replay/REPLAY.json). The packet-root REPLAY.json changes only path keys, their canonical inputs_hash, checker/report paths, and adds a note. It preserves all original digest values and the exact model string. The referee session did not expose an exact serving-model identifier; hashes do not establish model identity or historical isolation.

The immutable report gives its original job-relative command. To rerun from the packet root with python-flint installed:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 python3 review/replay/check.py --certificate review/inputs/certificates/certificate.json --precision 384 --tol 1e-20 --controls --output referee-reproduced.json
```

The archived verdict is HOLDS WITH CAVEATS. This AI review does not remove the candidate/unrefereed asterisk.
