# Reproduction

Candidate and unrefereed. Frozen integer certificates are the replay targets. Run scientific commands only on an authorized compute host, relative to this artifact directory. Requirements: a C++17 compiler, GMP development headers/library, Python 3 and pynauty 2.8.8.1. Numerical solvers are unnecessary for verification.

## Exact replay

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1
mkdir -p replay
g++ -O3 -std=c++17 scripts/verify_frozen.cpp -lgmp -o replay/verify
g++ -O3 -std=c++17 scripts/verify_legacy_gmp.cpp -lgmp -o replay/verify_legacy
g++ -O3 -std=c++17 scripts/verify_lift9.cpp -lgmp -o replay/verify_lift9

gzip -dc certificates/c6_8.cert.gz > replay/c6_8.cert
gzip -dc certificates/c5_8.cert.gz > replay/c5_8.cert

nice -n 10 replay/verify replay/c6_8.cert sources/graph8.g6
nice -n 10 replay/verify_legacy replay/c6_8.cert sources/graph8.g6
nice -n 10 python3 scripts/check_graph9.py
nice -n 10 replay/verify certificates/c6_9.cert sources/graph9.g6
nice -n 10 replay/verify_lift9 certificates/c6_9.cert sources/graph8.g6 sources/graph9.g6
nice -n 10 replay/verify replay/c5_8.cert sources/graph8.g6
nice -n 10 replay/verify_legacy replay/c5_8.cert sources/graph8.g6
```

The first two certificate checks independently establish exhaustive labelled eight-vertex coverage. The Python augmentation check then proves completeness of the nine-vertex list. Both that check and the nine-vertex coefficient replays are required. The direct and vertex-deletion proof paths agree exactly on the minimum slack.

CERTIFICATES.json gives the exact bounds, compressed/uncompressed hashes and block parameters. ARTIFACT_MANIFEST.json fixes the selected proof files and logs. The bundle manifest can be checked with `scripts/check_manifest.py`.

On the original pod, GMP headers were downloaded from Ubuntu package `libgmp-dev_6.3.0+dfsg-2ubuntu6_amd64.deb` and extracted only into the own-job `sources/gmpdev` directory. The compile commands there added `-Isources/gmpdev/usr/include -Isources/gmpdev/usr/include/x86_64-linux-gnu` and linked `-Wl,-l:libgmp.so.10`. No system package installation or other-job modification is necessary.

## Public baselines

The preceding public C6 certificate is included as `certificates/public_c6_8.cert`, hash 39bd22dac99c7cd509ffc6b32762302f79b2775c3e16fed89078080c4f0296f5. Replay it with the same eight-vertex checker.

The PPSS C5 baseline is `certificates/c_5.json` inside the public archive at https://zenodo.org/records/6602512. The archive and JSON input hashes are in receipts/public_input_hashes.json. Reproduce its exact translation without rounding by generating the ordered-root metadata below and running scripts/import_ppss.py. Its independently replayed bound is

    20421620024978222587630220763104861267
    / 13398618197511951998870375167625873326080.

It is not enough to compare against the rounded printed 0.001524. After generating the ordered metadata as below, the baseline import can be replayed with:

```sh
curl -LfsS https://zenodo.org/api/records/6602512/files/certificates.zip/content -o sources/published_certificates.zip
unzip -p sources/published_certificates.zip certificates/c_5.json > sources/published_c5.json
nice -n 10 python3 scripts/import_ppss.py
nice -n 10 replay/verify artifacts/ppss_baseline.cert sources/graph8.g6
```


## Search recipe

The original numerical environment is in receipts/environment.json. Scientific launches used scripts/run_compute.sh: nice 10, single-threaded BLAS, a per-process address-space cap and recorded PIDs. Its original authorized-pod directory is hardcoded; update that path when replaying on another authorized host. Python bytecode writes to dependency environments are disabled.

First recreate the working inputs:

```sh
mkdir -p artifacts
cp certificates/public_c6_8.cert artifacts/baseline.cert
cp certificates/c6_seed8.cert artifacts/frozen_rows8.cert
g++ -O3 -std=c++17 scripts/flag_search.cpp -o flag_search
g++ -O3 -std=c++17 scripts/generate.cpp -o generate
./flag_search 8 sources/graph8.g6 artifacts/base8 0 4 2 3 4 2
LABELLED_ROOTS=1 ./generate 8 sources/graph8.g6 artifacts/ordered8 0 4 2 3 4 2 6 1
./generate 9 sources/graph9.g6 artifacts/odd9 1 4 3 3
```

The original generator fixes the flag ordering used for the unordered baseline. The new generator uses 64-bit graph masks and supports unused vertices. The exact verifiers do not read either generator's tables.

For the native unordered C6 search, use the same data under prefix `artifacts/original8` (metadata header `8 0`; coefficient/objective files identical to base8). Then:

```sh
python3 scripts/export_csdp.py artifacts/original8 CLARABEL
python3 scripts/warm_csdp.py
```

Copy `sources/param_csdp_unordered.txt` to the own working `param.csdp`. With CSDP 6.2.0, run

```sh
csdp artifacts/original8_color.dat-s artifacts/original8_color.sol artifacts/original8_color.warm
python3 scripts/read_csdp.py artifacts/original8
python3 scripts/export_squares_high.py artifacts/original8 artifacts/original8_CSDP_Q.npz candidate8.cert 1000000000000 6
```

CSDP uses a target scale of 10000; the reader expands the colour symmetry and restores the original normalization. The numerical solver returned reduced accuracy, so its optimization status and floating objective are not a proof. The exported integer factors were accepted only after both exact replays.

For the nine-vertex lift, create `artifacts/sub8_indices.npy` with scripts/lift_squares9.py and run

```sh
python3 scripts/lift_rows9_cut.py candidate8.cert csdp_lift9
```

This averages eight-vertex coefficients over the nine induced eight-vertex subgraphs. Its numerical LP did not produce a new feasible solution before its limit; the accepted artifact uses the valid baseline factors and their all-nine-vertex residual margin. The independently written lift verifier builds its own labelled orbit index and never reads these search indices.

For the final C5 refinement, download/extract the public PPSS C5 JSON, run scripts/import_ppss.py, then the block and square-direction searches in scripts/reweight_ppss.py and scripts/column_search.py. The latter starts from the reproduced public factors and prices additional PSD directions with an LP dual. The accepted C5 artifact came from its third refinement round. All resulting factors are rounded to integers and rechecked exactly.

Temporary coefficient tables and unsuccessful numerical states are intentionally not retained. They are large and reproducible. Time-limited searches, parallel floating arithmetic and shared-host performance can change intermediate factors; the frozen integer artifacts and their hashes define the authoritative deterministic verification targets.
