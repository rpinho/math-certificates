# Clean-room referee archive

A separate AI referee was given only review/inputs/: CLAIM.md, the released PROOF.md of the earlier degree-104 certificate (../degree104-cvp) and this packet's certificate.json, which is byte-identical to the root certificate.json. CLAIM.md told it that the proof's certificate-specific statements refer to the earlier certificate. It was asked to attack the reduction, check every exact hypothesis for this certificate and write its own interval checker. It did not read or run producer code. The release PROOF.md at the packet root replaces those certificate-specific statements with this certificate's values; its mathematical argument is unchanged.

Verdict: HOLDS WITH CAVEATS. The referee's interval, at 384 bits, is B in [0.251992340972008391240902200131, 0.251992340972008391240904220544], inside the producer's interval. The caveat is provenance: the session did not expose an exact serving-model identifier, so it cannot authenticate the model difference from the producer. According to the launcher record it ran on GPT-6 Astra; the receipt does not establish that. This is an AI review, not a human referee report or a formal proof, and it does not remove the candidate/unrefereed asterisk.

The original receipt is replay/REPLAY.original.json (also preserved as replay/REPLAY.json). The packet-root REPLAY.json changes only path keys, their canonical inputs_hash and the checker/report paths, and adds a note.

To rerun from the packet root with python-flint installed:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 python3 review/replay/check.py review/inputs/certificates/certificate.json --controls --output referee-reproduced.json
```
