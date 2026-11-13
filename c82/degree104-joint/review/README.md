# Clean-room round-10 referee archive

The referee received only review/inputs/CLAIM.md, review/inputs/PROOF.md and review/inputs/certificates/certificate.json. The input certificate is byte-identical to the packet root certificate. It attacked the reduction and exact hypotheses and wrote its own interval checker without reading or running producer code. INPUTS_SHA256SUMS verifies from review/inputs/.

Verdict: HOLDS WITH CAVEATS. B is enclosed in [0.2519696459872490990419691935079545, 0.2519696459872490990419691935079546], inside the producer enclosure. The exact serving-model ID is unavailable, so model separation cannot be authenticated. AI review does not remove the candidate/unrefereed asterisk. REFEREE.md and PRIOR_ART.md are byte-for-byte originals, including historical live links and initial-status prose.

replay/REPLAY.original.json and replay/REPLAY.json preserve the original receipt. Root REPLAY.json changes input path keys, canonical inputs_hash and checker/report paths, and adds a note. Hashes of input bytes, checker and replay report are unchanged. The preserved logs include development attempts and the completed replays; only the final checker is used for reproduction.

From the packet root, with an installed Python and python-flint:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 python3 review/replay/check.py --certificate review/inputs/certificates/certificate.json --prec 384 --eps 1e-22 --target 0.2519696460 --output ../final-referee.json
```

Earlier Arhan Canli replays concern earlier versions, as credited in the root README.md. He has not replayed this certificate.
