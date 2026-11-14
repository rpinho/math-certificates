# Reproduce and check

Use Python 3.10 or newer (standard library only), xz, a C/C++ compiler, make and git. Run from the packet root in a writable copy. Work and tools below are generated files outside the sealed sources; their addition is not part of the packet seal. Keep one heavy solver or checker active at a time, at nice 10. The delivered large assets are separate.

## Source builds

These source commands are for the reader; source downloads are not bundled. The exact commits used by both producer jobs and both referees were:

- CaDiCaL rel-3.0.1: `c60730422e758ef1cebe7aeddf2dda31c996bf04`.
- drat-trim: `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

```sh
mkdir -p tools work
git clone https://github.com/arminbiere/cadical.git tools/cadical
(cd tools/cadical && git checkout c60730422e758ef1cebe7aeddf2dda31c996bf04 && nice -n 10 ./configure && nice -n 10 make -j4)
git clone https://github.com/marijnheule/drat-trim.git tools/drat-trim
(cd tools/drat-trim && git checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 && nice -n 10 make -j1)
```

The clone URLs identify upstreams; each checkout is explicitly pinned before building. Kissat was present in the original producer tool inventory but is unnecessary for these four proofs.

## Lightweight checks

These producer checks run inside their packet subdirectories and read only the supplied certificates and CNF metadata:

```sh
(cd producer/n11 && nice -n 10 python3 check_coloring_certificate.py)
(cd producer/n12 && nice -n 10 python3 check_n12.py)
nice -n 10 python3 -B referee/n12/ref.py colour certificates/n12_coloring.json
nice -n 10 python3 -B referee/n12/ref.py dfs certificates/n12_coloring.json
nice -n 10 python3 -B referee/n12/dfs_control.py referee/n12
nice -n 10 python3 -B referee/n12/dfs_scan.py referee/n12
```

The DFS returns maximum seven in each colour for the supplied word. Its scan is over rank colourings and is not an unrestricted lower-bound proof. To rerun the first referee's published lower-bound and poset checks without changing archived outputs:

```sh
cp -R referee/n11 work/n11-referee
(cd work/n11-referee && nice -n 10 python3 -B check_data.py)
(cd work/n11-referee && nice -n 10 python3 -B published_lower.py)
(cd work/n11-referee && nice -n 10 python3 -B rank_lattices.py)
```

## Exact producer CNFs

Generate every theorem query and the base needed for the n=12 symmetry check:

```sh
nice -n 10 python3 producer/n11/encode_family.py 100010011101 0 8 work/1183_n11_c0.cnf
nice -n 10 python3 producer/n11/encode_family.py 100010011101 1 8 work/1183_n11_c1.cnf
nice -n 10 python3 producer/n12/encode_family.py 1100101100011 0 8 work/n12_1100101100011_c0.cnf
nice -n 10 python3 producer/n12/add_lex.py work/n12_1100101100011_c0.cnf work/n12_1100101100011_c0_lex.cnf
nice -n 10 python3 producer/n12/encode_family.py 1100101100011 1 8 work/n12_1100101100011_c1.cnf
shasum -a 256 -c CNF_SHA256SUMS
```

CNF_SHA256SUMS expects exactly these work/ filenames. All five generated CNFs were regenerated during packaging and matched the originals byte-for-byte. The encoders also create metadata JSON. Metadata for the lex query includes the base path supplied on the command line; only the CNF bytes are path independent. Archived producer metadata retains its original relative base path.

To run the separately written producer semantic checkers (memory use may be higher than proof checking):

```sh
nice -n 10 python3 producer/n11/check_family.py work/1183_n11_c0.cnf
nice -n 10 python3 producer/n11/check_family.py work/1183_n11_c1.cnf
nice -n 10 python3 producer/n12/check_family.py work/n12_1100101100011_c0.cnf
nice -n 10 python3 producer/n12/check_lex.py work/n12_1100101100011_c0.cnf work/n12_1100101100011_c0_lex.cnf
nice -n 10 python3 producer/n12/check_family.py work/n12_1100101100011_c1.cnf
```

For checking the retained proofs, follow VERIFY.md: download, verify compressed hashes, decompress one at a time, verify uncompressed hashes, then run default backward drat-trim on the matching CNF. Do not pass forward-only or permissive flags. A solver's UNSAT message is not a substitute for checking its certificate.

Fresh proofs can also be generated with `nice -n 10 tools/cadical/build/cadical CNF PROOF`. For these queries the expected solver exit is 20. Then `nice -n 10 tools/drat-trim/drat-trim CNF PROOF` must exit zero with `s VERIFIED`. Fresh proof bytes can differ; the published retained proof hashes identify the exact release bytes.

## Independently encoded referee CNFs

The original reports describe their original directory layouts, not this combined packet. The following commands make writable copies for regeneration. The original referee large proofs are not release assets; their recorded hashes are in PROOFS.json and their original hash records. Regeneration of a new proof need not recreate the same DRAT bytes.

```sh
mkdir -p work/n11-referee/replay
(cd work/n11-referee && nice -n 10 python3 encode.py 0 8 replay/c0_k8.cnf)
(cd work/n11-referee && nice -n 10 python3 encode.py 1 8 replay/c1_k8.cnf)
(cd work/n11-referee && nice -n 10 python3 encode.py 0 7 replay/c0_k7.cnf)
cp -R referee/n12 work/n12-referee
mkdir -p work/n12-referee/cnf
nice -n 10 python3 work/n12-referee/ref.py cnf certificates/n12_coloring.json 0 8 work/n12-referee/cnf/c0_k8.cnf
nice -n 10 python3 work/n12-referee/ref.py cnf certificates/n12_coloring.json 1 8 work/n12-referee/cnf/c1_k8.cnf
nice -n 10 python3 work/n12-referee/ref.py cnf certificates/n12_coloring.json 0 7 work/n12-referee/cnf/c0_k7.cnf
nice -n 10 python3 work/n12-referee/ref.py cnf certificates/n12_coloring.json 1 7 work/n12-referee/cnf/c1_k7.cnf
for pair in '2 5' '2 8' '2 9' '2 10' '3 8' '3 9' '3 10' '5 8' '5 9' '5 10'
do
    set -- $pair
    nice -n 10 python3 work/n12-referee/ref.py cnf certificates/n12_coloring.json 0 8 "work/n12-referee/cnf/c0_iv_${1}_${2}.cnf" "$1" "$2"
done
nice -n 10 python3 work/n12-referee/ref.py cnf certificates/n12_coloring.json 0 7 work/n12-referee/cnf/c0_iv7_2_10.cnf 2 10
```

Use sh or bash for the loop above; zsh has different unquoted variable splitting. REFEREE_CNFS.json lists all original referee CNF SHA-256 values. At n=11 the encoder writes its count/mask metadata to a .json beside the CNF; at n=12 it writes a .cnf.map. Source is deterministic and standard-library only. For each fresh k=8 referee query use the same pinned solver and default drat-trim commands above. The n=12 interval colour-zero proofs retained in referee/n12/proofs can be checked against these regenerated interval queries; compare their hashes in PROOFS.json. A k=7 query is a positive SAT control, not an upper-bound proof.

## What was checked in packaging

The top-level verification results summarize fresh checks. Original referee reports are historical independent reviews, not reviews commissioned by this packaging job. REPLAY.json records both reports and identifies the original generic exact DFS, which was also run on both supplied rank words during packaging. This rerun does not make the packaging session a clean-room referee: the packager read the producer code. No predictive metric was used; trivial/simple/SBS does not apply.
