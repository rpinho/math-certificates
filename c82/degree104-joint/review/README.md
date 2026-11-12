# Clean-room round-9 referee archive

The referee received only review/inputs/CLAIM.md, review/inputs/PROOF.md and review/inputs/certificates/certificate.json. The input certificate is byte-identical to the packet root certificate. It attacked the reduction and exact hypotheses and wrote its own interval checker without reading or running producer code. INPUTS_SHA256SUMS verifies from review/inputs/.

Verdict: HOLDS WITH CAVEATS. B is enclosed in [0.25197444874089584903007645293157, 0.25197444874089584903007646836791], inside the producer enclosure. The caveats are that the exact serving-model ID is unavailable, so model separation cannot be authenticated, and that a resource-estimate line in its job specification said 37 numerators/4,132 roots although the hashed certificate has 48 numerators/5,370 roots. The stale line is documentation only. AI review does not remove the candidate/unrefereed asterisk.

replay/REPLAY.original.json and replay/REPLAY.json preserve the original receipt. Root REPLAY.json changes input path keys, canonical inputs_hash and checker/report paths, and adds a note. Hashes of input bytes, checker and replay report are unchanged. The preserved logs include development attempts and both completed replays; only the final checker is used for reproduction.

From the packet root, with an installed Python and python-flint:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 python3 review/replay/check.py review/inputs/certificates/certificate.json --prec 256 --tol 1e-22 --order 16 --target 0.2519744488 --output ../final-referee.json
```

Earlier Arhan Canli replays concern earlier versions, as credited in the root README.md. He has not replayed this certificate.
