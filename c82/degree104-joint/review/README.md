# Clean-room round-12 referee archive

The referee (Claude Opus 5.5, claude-opus-5-5) received only review/inputs/CLAIM.md, review/inputs/PROOF.md and review/inputs/certificates/certificate.json. The input certificate is byte-identical to the packet root certificate. It attacked the reduction and exact hypotheses and wrote its own interval checker without reading or running producer code. INPUTS_SHA256SUMS verifies from review/inputs/.

Verdict: HOLDS. B is enclosed in [0.2519694758380326654679408, 0.2519694758382429035635232], which contains the producer enclosure and whose upper end is below 0.2519694759. Caveats, in the referee's words and ours: trust base (FLINT, Arb, python-flint, the integrand logic; AI review, not a human or a proof assistant); P1, P2 and P4 vanish on the circle and are harmless; the enclosure is wider than the producer's because of the integrator tolerance. AI review does not remove the candidate/unrefereed asterisk. REFEREE.md and PRIOR_ART.md are byte-for-byte originals, including their live links.

replay/REPLAY.original.json and replay/REPLAY.json preserve the original receipt. Root REPLAY.json changes input path keys, canonical inputs_hash and checker/report paths, and adds a note. Hashes of input bytes, checker and replay report are unchanged. The preserved outputs include the coarse-tolerance run (tolerance 2^-50, too coarse to decide the claim), the controls and the completed main run; only the final checker is used for reproduction.

From the packet root, with an installed Python and python-flint (about 30 minutes on one core):

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 nice -n 10 python3 -I review/replay/check.py review/inputs/certificates/certificate.json
```

The default target is 0.2519694759; `--target 0.2519694758` must fail. Earlier Arhan Canli replays concern earlier versions, as credited in the root README.md. He has not replayed this certificate.
