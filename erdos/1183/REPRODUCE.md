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

The clone URLs identify upstreams; each checkout is explicitly pinned before building. Kissat is unnecessary for the original n=11/n=12 proofs. The n=14 producer proofs use the following pinned build:

```sh
git clone https://github.com/arminbiere/kissat.git tools/kissat
(cd tools/kissat && git checkout 8af8e56f174b778aef3aa45af9f739b2a5f492c2 && nice -n 10 ./configure && nice -n 10 make -j4)
```

These pins also match the new referee’s tool inventory in referee/n13n14/tools/COMMITS.txt.

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

## n=13 and n=14: exact producer CNFs and checks

Run from the packet root, in a writable copy. The producer metadata and colourings are retained byte-for-byte in producer/n13n14; its checkers are separately written by the same producer, not a clean-room review. These commands use the supplied standard n=13 encoder and the supplied streaming n=14 encoder (the original list encoder exceeded the producer’s memory limit at n=14). Run one heavy process at a time.

```sh
(cd producer/n13n14 && nice -n 10 python3 -B check_coloring.py certificates/n13_coloring.json)
(cd producer/n13n14 && nice -n 10 python3 -B check_coloring.py certificates/n14_coloring.json)
(cd producer/n13n14 && nice -n 10 python3 -B check_rank_screen.py)
nice -n 10 python3 -B referee/n13n14/src/check_coloring.py certificates/n13_coloring.json 3,7,31,255,511,767,1023,8191
nice -n 10 python3 -B referee/n13n14/src/check_coloring.py certificates/n14_coloring.json 0,1,15,113,127,2047,4095,16383
mkdir -p work
for c in 0 1; do
  nice -n 10 python3 producer/n13n14/encode_family.py 11001011000110 "$c" 9 "work/n13_11001011000110_c${c}.cnf"
  nice -n 10 python3 producer/n13n14/add_lex.py "work/n13_11001011000110_c${c}.cnf" "work/n13_11001011000110_c${c}_lex.cnf"
  nice -n 10 python3 producer/n13n14/encode_family_stream.py 110010110001101 "$c" 9 "work/n14_110010110001101_c${c}.cnf"
  nice -n 10 python3 producer/n13n14/add_lex.py "work/n14_110010110001101_c${c}.cnf" "work/n14_110010110001101_c${c}_lex.cnf"
done
shasum -a 256 -c N13N14_CNF_SHA256SUMS
```

The eight CNF hashes (four base and four lex) must all match; SHA-256 of the final theorem queries also appears in ASSETS.json and VERIFY.md. Generated metadata JSON records the output/base path supplied, so its bytes can differ from the archived original metadata; the CNF bytes are path-independent. All eight CNFs were freshly regenerated in this packaging job and matched the supplied SHA-256 values. No large CNF is bundled in the packet.

To independently reconstruct every clause using the separately written streaming producer checker:

```sh
for c in 0 1; do
  nice -n 10 python3 producer/n13n14/check_statement.py "work/n13_11001011000110_c${c}_lex.cnf"
  nice -n 10 python3 producer/n13n14/check_statement.py "work/n14_110010110001101_c${c}_lex.cnf"
done
```

Require `EVERY CLAUSE REBUILT FROM STATEMENT`. The original outputs for all four queries are in producer/n13n14/logs; the packet also includes the older check_family.py and check_lex.py implementations, which can use substantially more memory. The streaming check_statement.py is the appropriate round-3 full checker.

The four new release streams are listed in ASSETS.json. Use VERIFY.md to download, hash, decompress and check each proof with the matching CNF. To generate fresh proofs, expected solver exit 20 means UNSAT; the resulting proof still needs default backward drat-trim:

```sh
nice -n 10 tools/cadical/build/cadical -q work/n13_11001011000110_c0_lex.cnf work/new13_c0.drat
nice -n 10 tools/cadical/build/cadical -q work/n13_11001011000110_c1_lex.cnf work/new13_c1.drat
nice -n 10 tools/kissat/build/kissat -q work/n14_110010110001101_c0_lex.cnf work/new14_c0.drat
nice -n 10 tools/kissat/build/kissat --plain -q work/n14_110010110001101_c1_lex.cnf work/new14_c1.drat
```

Fresh proof bytes need not match the archived proofs. The retained n=14 colour-1 proof is `_kissat_plain`; the unfinished non-plain colour-1 trace and the zero-byte colour-0 CaDiCaL proof are excluded. The resource stops that led the producer to streaming and these solver choices are recorded in its byte-preserved REPORT.md and CHECKS.md. A full regeneration/solve is more expensive than checking the supplied proof and is optional.

## n=13 and n=14: independent referee

The original report and scripts are in referee/n13n14. The scripts below write only fresh output under work and do not alter the archived output. Run the exact non-SAT searches at thresholds eight (witnesses) and nine (upper bounds), then check all balanced words for the n=13 lower bound:

```sh
for t in 8 9; do
  nice -n 10 python3 -B referee/n13n14/src/poset_search.py 13 11001011000110 "$t"
  nice -n 10 python3 -B referee/n13n14/src/poset_search.py 14 110010110001101 "$t"
done
nice -n 10 python3 -B referee/n13n14/src/balanced.py work/n13_balanced_words.txt
cmp work/n13_balanced_words.txt referee/n13n14/logs/n13_balanced_words.txt
nice -n 10 python3 -B referee/n13n14/src/validate_small.py
```

Threshold nine must return NONE for both colours of each word. Threshold eight constructs a family in n=13 colour zero and both n=14 colours; n=13 colour one returns NONE. The balanced check must print 3,432 rejected and zero not rejected; the small-dimension comparison must print zero mismatches. PROOF.md explains why these exact searches imply the unrestricted finite claims.

Regenerate the referee's independent CNFs as follows. They differ from the producer CNFs and **cannot** be used with the producer release proofs. Their four original hashes appear in referee/n13n14/logs/n13_hashes.txt and n14_hashes.txt. The original referee proofs were discarded after checking, so only hashes and check logs are preserved. Fresh proofs are possible but were not regenerated by packaging.

```sh
nice -n 10 cc -O3 -o work/referee_enc referee/n13n14/src/enc.c
for c in 0 1; do
  nice -n 10 work/referee_enc 13 11001011000110 "$c" 9 1 0 "work/referee_n13_c${c}_k9_lex.cnf"
  nice -n 10 work/referee_enc 14 110010110001101 "$c" 9 1 0 "work/referee_n14_c${c}_k9_lex.cnf"
done
```

The referee used CaDiCaL for both n=13 colours and n=14 colour zero; default kissat for n=14 colour one after CaDiCaL exceeded its resource limit. The original command pattern is `nice -n 10 tools/cadical/build/cadical -q CNF PROOF`, or `nice -n 10 tools/kissat/build/kissat -q CNF PROOF`; then `nice -n 10 tools/drat-trim/drat-trim CNF PROOF -t 20000` must exit zero and print `s VERIFIED`. The report documents positive, deletion and corrupted-proof controls as historical referee evidence, and the no-symmetry SAT run that timed out. The weighted-poset argument does not need those SAT runs or symmetry clauses.

The supplied directory has no standalone VERDICT_for_ledger.txt. The original report ends `VERDICT: HOLDS`; no replacement ledger file is fabricated. This packaging session read producer code and is not another clean-room referee.

## n=15..20: replay from the delivered packet

Use Python 3.10+ (standard library only), and a C/C++ compiler only if rebuilding searches. Disable bytecode creation to keep the packet seal unchanged. From the packet root:

```sh
nice -n 10 python3 -B producer/n15n20/replay_packet.py
```

This replays all twelve headline trees with their expected rank words and thresholds supplied from the original results table, checks both maximum witnesses per colouring, checks the complete mask-indexed colourings, and checks every producer screen/prefix rejection witness and all balanced-word witnesses. It also checks the referee’s complete balanced-word lists using the packaged direct witness checker. It needs no release download and writes no output files except stdout.

The tree for n=15 colour one uses threshold nine because its exact maximum is eight. All other thresholds are maximum plus one, as recorded in results.json. Single-tree example (run from `producer/n15n20/`):

```sh
nice -n 10 python3 -B src/check.py certificates/search_1100101100011010_c0_t10.tree.gz 1100101100011010 0 10
```

To repeat the producer’s additional rank-minimum proof replay, run the command below from `producer/n15n20/`. All trees directly referenced by these screens are included, so this replay also needs no download. The v3 archive retains the additional search/control trees for optional inspection as described in VERIFY.md:

```sh
nice -n 10 python3 -B src/replay.py
```

That original replay additionally checks all surviving words’ proof trees and prefix/full-screen correspondence. The original complete screen and prefix files and direct trees are included. These extra rank-minimum claims are unnecessary for the six unrestricted upper bounds and were outside the clean-room referee’s exhaustive review.

To rebuild the producer’s searches (run in a writable copy of `producer/n15n20/`):

```sh
clang++ -O3 -std=c++17 src/poset.cpp -o src/poset
clang++ -O3 -std=c++17 src/brute.cpp -o src/brute
nice -n 10 src/brute
```

The original producer validation script retains a historical neighbouring-directory import for the earlier referee. To run it in this packet, use a working copy and point its `spec_from_file_location` to `../../referee/n13n14/src/poset_search.py` relative to `producer/n15n20/`. It is not needed for replay and is not imported by the checker. Other producer search scripts write new certificates/logs and should likewise run only in a working copy.

The clean-room referee’s own search can be rebuilt from the packet root:

```sh
mkdir -p work
cc -O3 -std=c11 referee/n15n20/src/wps.c -o work/wps
nice -n 10 work/wps max 15 1100101100011010
nice -n 10 work/wps max 16 00100111010011001
nice -n 10 work/wps max 17 110010110001101001
nice -n 10 work/wps max 18 0010110011101001100
nice -n 10 work/wps max 19 00110010111000101101
nice -n 10 work/wps max 20 110010110001101100110
nice -n 10 python3 -B referee/n15n20/src/check_witnesses.py producer/n15n20/certificates/results.json
nice -n 10 python3 -B referee/n15n20/src/check_balanced.py 15 referee/n15n20/out/bal_n15.tsv
nice -n 10 python3 -B referee/n15n20/src/check_balanced.py 17 referee/n15n20/out/bal_n17.tsv
nice -n 10 python3 -B referee/n15n20/src/check_balanced.py 19 referee/n15n20/out/bal_n19.tsv
```

The last three historical scripts print their results; require `all_covered=True` and `bad=0`. The packaged replay driver asserts coverage and closure itself and fails nonzero on an error. Original referee brute-force outputs through n=6 and all rank-word comparisons are retained. The conventional representation and completeness arguments in PROOF.md remain part of the proof; they are not kernel formalizations. Candidate, no human review.

The referee balanced-word stdout tables use `.tsv` in this packet. Every original space delimiter is replaced by a tab to disambiguate numeric fields for the publication scan. No value changes; `referee/n15n20/out/FORMATS.json` records original and packaged hashes. Replacing tabs with spaces reconstructs the original stdout byte-for-byte. The unchanged referee report retains the historical `.txt` filenames. Its scripts use whitespace splitting and accept these TSV tables. Other referee outputs are byte-preserved.
