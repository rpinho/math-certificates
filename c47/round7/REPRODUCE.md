# Reproduce the release

Python 3 and its standard library suffice. Run from this folder without disabling assertions, one process at a time at nice 10. Use a copy to preserve the shipped timing-bearing receipts and checksums.

```sh
export PYTHONDONTWRITEBYTECODE=1
nice -n 10 python3 verify_exact.py certificates/final.json --claim 11436840446775366245825984602005252649658962678483718696299/6706834195253218266545949032739264680888893440000000000000 --out release_validation/exact.json
nice -n 10 python3 rejection_controls.py certificates/final.json 11436840446775366245825984602005252649658962678483718696299/6706834195253218266545949032739264680888893440000000000000
nice -n 10 python3 finite_instance.py certificates/final.json release_validation/exact.json release_validation/finite.json --claim 341050341/200000000
(cd referee && nice -n 10 python3 referee_check.py)
nice -n 10 python3 comparison.py
nice -n 10 python3 sources/claim_facts.py
```

The seven controls must reject: raised claim, changed heavy mass, oversized radius, expanded rectangle, atom outside cell, zero mass and duplicate atom. They generate corrupted certificate files under certificates/controls/final. The release omits these regenerable files; their SHA-256 values and the generation command are in release_validation/omitted-generated.json. Remove the generated folder with `/usr/bin/trash certificates/controls` after replay. The referee checker produces a regenerable per-witness table; its original hash is in referee/README.md and its replay hash in release_validation/omitted-generated.json. The table is omitted from the package.

The referee checker reads only the certificate and finite-instance data, not producer code. The source calculation summary is referee/exact_results.json; its fresh replay is release_validation/referee-results.json. REPLAY.json records hashes of the publication copies of the supplied historical mathematical inputs. The release PROOF.md changes citation and review-status wording; the supplied producer-proof.md is retained byte-for-byte under referee/sources/.

The finite block is specified by formula, without expanding its atoms. Floats and decimal fields are display only. The written proof supplies the passage to the planar L1 constant; no formalization or human peer review is claimed. Numerical search is unnecessary for replay and is outside this frozen-certificate release.

For the unchanged shipped bytes, run:

```sh
shasum -a 256 -c SHA256SUMS
```

## Unpublished search history

All superseded producer certificate files and archives below are omitted and unnecessary for replay; these are unpublished search history. The identical final snapshot aliases are omitted too.

- best.json: SHA-256 `7604a8ed69ba333bb4fd8158a4f202401c79eb4e565a71345e345646dc9b8fb4`.
- best_1.7052517050249764.json: SHA-256 `0cd5cc0954f8cc01ac1184b7cf095ce22bb3cdaa9a602fe25c20d8c1bd2bfe04`.
- checkpoints-1794277331.tar.xz: SHA-256 `2c1e74e60f80519d6d8579baacb24678f54b680c3b830ca00601f73c9e601b19`.
- checkpoints-1794278321.tar.xz: SHA-256 `b3f68b78c3c5eab4cb107ad426acfda608dc7a9190f2b8b3ef5fb26e9a739443`.
- checkpoints-1794279339.tar.xz: SHA-256 `c5354335b510858ba9bef53e4235e7d98a3f26161b37df2ec6d854846787a9b3`.
- checkpoints-1794280245.tar.xz: SHA-256 `fce87a77d9348bc7519b49376b66e42ff1e291bc949b244a5f46a457ed95c69b`.
- checkpoints-1794281370.tar.xz: SHA-256 `7232ad1456f8d42723b43c8a16e2ab1d98a202829d5e6dbf0c9a2621428520d1`.
- checkpoints-1794282277.tar.xz: SHA-256 `c2bd3f33704aae485df55684dcbe0210fb17f01db21129b3b037d7380854831f`.
- checkpoints-1794283442.tar.xz: SHA-256 `adfc7677a931fee9b261cb82327d747e0768c6ea192c56ed81f50f5405146dad`.
- checkpoints-1794284457.tar.xz: SHA-256 `b997a406dcb5ea127caf6949d225f6e35db88377b235812ecb9a47b8639d5a12`.
- checkpoints-1794285362.tar.xz: SHA-256 `0e89c8c0d2d7e5e6ea007f56981e291fa6c053c97106165795a62678625622b9`.
- checkpoints-1794286267.tar.xz: SHA-256 `de240cf4741e7d434803574f56ba167c5761a86e39bdb6da587263467abe9512`.
- checkpoints-1794287283.tar.xz: SHA-256 `2c14879d59b339ece84def79b566dfeab11d69a5e993151ce24064ae259a7c75`.
- checkpoints-1794288289.tar.xz: SHA-256 `60fb55896eae3bc5764b8fa6809169d86988bcab692d56ec38e39b1c608d4e20`.
- checkpoints-1794289213.tar.xz: SHA-256 `93fa402392992d7702ea6ced4e3c9f3033417f99178612237b13ddcdf24b4219`.
- checkpoints-1794291481.tar.xz: SHA-256 `827b72e1b3dde73d408761673feb4877ecbd6def16a160e681738511c90fe256`.
- checkpoints-1794292152.tar.xz: SHA-256 `60f52f35bc8a79207668215ab9496dfaa4e593e52a0b0820d3de3e7741f07480`.
- checkpoints-1794293056.tar.xz: SHA-256 `f7f5008375260fc9b17af53a9a12d31f1145120805df75281543879c132b6c9d`.
- checkpoints-final-1794296083.tar.xz: SHA-256 `d9fbfb4be3a6c89cf0399fa79f691031cde381e6fb01bc4b74d5b0666abacb89`.
- final-controls.tar.xz: SHA-256 `391c2619c24bb12bcc723241a69f4911d26ed19ebf0e449e15d279f6e90d5341`.
- full-family-comparisons.tar.xz: SHA-256 `f0f0365ff72a18f1cd03b98d3f19fc67c3748c75ca11fb89f802bb4f3ce9d215`.
- retained-producer-comparison.tar.xz: SHA-256 `0e2c1197bd20dcd587d73ed7b760b981bf99aa404e9e5c4fb341d9f9f6757617`.
- start392.json: SHA-256 `c37382e18f55d07f442fe65b259d4e04d195f696d7ef06aed698143cfbe00ae3`.
- start474.json: SHA-256 `5a9baac31ca5e4875e9495a81469402018bf2cccb8889f9d85f396d4d38f32c4`.

Other unpublished producer archives (outside the certificate folder):

- chains/final-working-snapshots-1794296111.tar.xz: SHA-256 `755ddb2d20be6121bb24315cfe0d10c8ec9716e278765ca0b88dfa04eea35260`.
- chains/working-history-1794288292.tar.xz: SHA-256 `b7ca8b46ab1d3aafaaf1882fb2ba575e5b63c17bf1281d531d27e593e4dca6d2`.
- chains/working-history-1794289216.tar.xz: SHA-256 `2df329867c6c5a24abae811b0d3419679be3685c650863793528bd0a34ac7bdd`.
- chains/working-history-1794291486.tar.xz: SHA-256 `f4127442f9b6c0bb36a59e2f8ae21418d8986b27a0c80f495a4c54cfe353af44`.
- chains/working-history-1794292155.tar.xz: SHA-256 `77af24853b0db98a5bac4842e6e876c2f40344f25bc40e3ef78d98c9734c8e8c`.
- chains/working-history-1794293060.tar.xz: SHA-256 `33634b0102334657887ac2c7b931c7756a8a55ddf6562cd678758d4f6e0ec047`.
- sources/final-source-bytes-1794296111.tar.xz: SHA-256 `6765c34d1de61368d097b322217112b4f224739ea658d467fef07a8d82fa8dfa`.
- sources/initial-source-bytes-1794288294.tar.xz: SHA-256 `fd8bc5bcde456bf458f33a981c41fab4ec3489b50abdda1ee9c1e11018dfce96`.

Scheduling note: the source shell inherited nice 15 and denied absolute nice 10. The initial additive launch was stopped and reverted; completed replays inherited nice 15, a lower CPU priority than requested. Run at absolute nice 10 where permitted.
