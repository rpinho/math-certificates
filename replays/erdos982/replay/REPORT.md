RESULT: yes
Shipped: An independent exact replay of Erdős #982 for n = 8 through 13.

| n | Verdict | Verification |
| ---: | --- | --- |
| 8 | **HOLDS** | At K = 3, both proof checkers accepted UNSAT on 22,345 clauses. |
| 9 | **HOLDS** | Delete a vertex and apply n = 8. |
| 10 | **HOLDS** | At K = 4, both proof checkers accepted UNSAT on 96,649 clauses with FAN. |
| 11 | **HOLDS** | Delete a vertex and apply n = 10. |
| 12 | **HOLDS** | At K = 5, both proof checkers accepted UNSAT on 317,384 clauses with FAN. |
| 13 | **HOLDS** | Delete a vertex and apply n = 12. |

The regular polygon attains floor(n/2), so each bound is sharp. The small-order sanity runs also give the bound at n = 5, 6 and 7. At n = 3 the bound is immediate. At n = 4, one distance class per vertex would force every edge to have the same length by sharing edges between rows, which contradicts the crossing-diagonal inequality.

**New result? No.** This reproduces the small-order bounds reported in the supplied prior-art snapshot. **This is AI work. No human has checked it.** Two independent programs checked each certificate. The mathematical argument that each CNF covers every geometric counterexample is written out and remains to be checked by a reader. [Prior art](PRIOR_ART.md) · [Proofs](PROOFS.md)

## Inputs and generators

The distance order is on unordered edges, so both endpoints see the same length. The primary and reference encoders are separate implementations by the same agent. Their canonical DIMACS SHA-256 digests match in every recorded case. The proofs concern exhaustive configurations and require no statistical holdout. [Primary encoder](encoder.py) · [Reference encoder](encoder_reference.py) · [CNF digests and case ledger](runs/cases.tsv)

- G1 used 10,000 randomly perturbed integer parabolic polygons with all edge lengths distinct. Exact oriented-area and integer squared-distance checks establish these properties.
- G2 tested 12,723,834 rotation classes of n-subsets of regular m-gons, for n = 3 through 13 and n ≤ m ≤ 2n + 4. An independent Burnside count agreed at all 143 (n, m) pairs. Chord step gives the exact rank.
- G3 used 5,000 constructions in five groups of 1,000. They include center-vertex circle fans, embedded equilateral triangles, alternating concentric regular polygons, thin parabolas and reflection-symmetric parabolas. A separate 5,000-sample targeted G3 panel required at least one exact tie in every sample and exercised the full FAN premise in 818 samples, including at n = 8, 10 and 12. No violations were observed. [Construction counts](runs/generators.tsv) · [Targeted coverage](runs/fan_families_targeted.tsv)

The original G1 and G3 lifts were evaluated against every emitted non-BOUND clause. The BOUND block is satisfied at the polygon's own maximum by counting its first representatives. G2 uses a factored evaluation: for each carrier the validator checks every local geometric clause instance, including FAN on quintuples, and each necklace inherits those instances. It computes the distinct-distance counts from exact ranks on each row. ASYM and TRANS hold on the same rank order, FIRST uses the first occurrence of each rank, and minimum-side rotation gives SYM. The targeted panel uses the same direct clause checker as G1 and G3. [Validator](validate.cpp) · [Generator implementation](generate.py) · [Raw generator counts](runs/necklaces.tsv)

Each cell below gives samples where **any premise literal / the full premise** held. Each family has the sample counts given above, and all violation counts are zero. UNTESTED marks a zero full-premise count. The order-level tables also flag untested cells. For BOUND, a full premise is a row with K marked representatives available to form a K+1 clause at the control's own maximum. For SYM, the premise is the minimum-side relabeling.

| Family | G1 | G2 | G3 |
| --- | ---: | ---: | ---: |
| ASYM | 10,000 / 10,000 | 12,723,831 / 12,723,831 | 4,906 / 4,906 |
| TRANS | 10,000 / 10,000 | 12,723,834 / 12,723,834 | 5,000 / 5,000 |
| FIRST | 10,000 / 10,000 | 12,723,834 / 12,723,834 | 5,000 / 5,000 |
| BOUND | 0 / 0 UNTESTED | 10,634,586 / 10,634,586 | 763 / 763 |
| BISECTOR | 9,013 / 9,013 | 12,723,765 / 12,723,765 | 4,419 / 4,419 |
| CROSS | 8,888 / 8,888 | 12,723,752 / 12,723,752 | 4,355 / 4,355 |
| CAP | 9,090 / 0 UNTESTED | 12,723,792 / 0 UNTESTED | 4,545 / 909 |
| SYM | 10,000 / 10,000 | 12,723,834 / 12,723,834 | 5,000 / 5,000 |
| FAN | 8,181 / 0 UNTESTED | 12,723,663 / 0 UNTESTED | 4,090 / 1 |

[Exact G1 and G3 coverage by n](runs/fan_families_other.tsv) · [Exact G2 coverage by n](runs/fan_families_regular.tsv)

### Mutant kill matrix

Each entry counts sampled polygons that falsified the variant. The first ten variants were killed before the original solve. The FAN variant was also killed before its first solve. [Raw kill matrix](runs/mutants.tsv)

| False variant | G1 | G2 | G3 |
| --- | ---: | ---: | ---: |
| ASYM allows a tie in the strict premise | 0 | 12,723,808 | 3,965 |
| FIRST counts a repeated class | 0 | 12,723,755 | 3,494 |
| BISECTOR drops the premise | 9,013 | 12,723,765 | 4,416 |
| BISECTOR reverses the conclusion | 9,013 | 12,723,765 | 4,419 |
| CROSS requires the first diagonal alone to win | 8,888 | 12,723,752 | 4,355 |
| CROSS substitutes an adjacent side | 6,576 | 12,627,213 | 3,659 |
| CAP drops equal endpoint radii | 7,027 | 12,723,417 | 3,891 |
| CAP reverses its radial comparison | 0 | 12,723,266 | 1,297 |
| CAP shifts its center forward one vertex | 0 | 0 | 909 |
| The longest diagonal beats every side | 8,639 | 12,723,744 | 4,264 |
| FAN drops the last sector from its premise | 9 | 0 | 1,386 |

## Controls, coverage and survivors

Full positive-control CNFs at K = floor(n/2) are SAT for n = 5 through 13. The models were checked clause by clause. At n = 13, an explicit regular-polygon assignment passed all 538,875 clauses and replaced the unfinished unconstrained SAT probe. The n = 5, 6 and 7 negative sanity cases are UNSAT with DRAT cores of 7, 57 and 47 clauses respectively. The SYM brute-force check enumerated all boundary total preorders through n = 8, including 545,835 at n = 8. Each has a dihedral image satisfying the actual SYM clauses. The main instances were monolithic. [Case ledger](runs/cases.tsv) · [Enumeration log](runs/fan_verify_inputs.log) · [Pieces](PIECES.md)

| n | CaDiCaL LRAT checked by cake_lpr | CaDiCaL DRAT checked by drat-trim | Removed empty inference ID | Altered original core clause ID |
| ---: | --- | --- | ---: | ---: |
| 8 | VERIFIED UNSAT | VERIFIED | 23246 | 5227 |
| 10 | VERIFIED UNSAT | VERIFIED | 108947 | 4023 |
| 12 | VERIFIED UNSAT | VERIFIED | 698950 | 12411 |

For each row, cake_lpr rejected the proof with its empty inference removed and the original proof against the input with that one core clause replaced by a tautology. Raw hashes, original literals and checker output are under the case directories. The retained primary LRAT and DRAT archives were also replayed directly. [n=8 receipt](runs/n8/result.json) · [n=10 receipt](runs/n10-fan/result.json) · [n=12 receipt](runs/n12-fan/result.json)

The original n = 10 formula returned a checked SAT model. Its raw shortest-class literals force two equilateral sectors at vertex 1, which contradict the distance order of the middle sector. The exact refutation led to the FAN family. The final n = 10 and n = 12 cases have no surviving SAT models. The witness and its exact refutation are retained. [Survivors](SURVIVORS.md)

## Cores and ablation

The main DRAT cores contain 478, 3,803 and 29,256 clauses for n = 8, 10 and 12. Totals are unique clauses. A clause can carry both BISECTOR and CROSS labels because those two proofs imply identical clauses. Every family used in every core is proved in PROOFS.md. Each UNSAT case has the core DIMACS, clause IDs, family provenance and its checker logs, either in that case directory or in the identical input's shared proof directory. [All core counts and hashes](runs/cases.tsv)

Ablation removes one family's contributions before canonicalization. UNSAT cells show DRAT core sizes. SAT cells have complete assignments checked against every remaining clause.

| Omitted family | n = 8 | n = 10 | n = 12 |
| --- | --- | --- | --- |
| ASYM | SAT | SAT | SAT |
| TRANS | SAT | SAT | SAT |
| FIRST | SAT | SAT | SAT |
| BOUND | SAT | SAT | SAT |
| BISECTOR | UNSAT, 478 | UNSAT, 3,803 | UNSAT, 29,256 |
| CROSS | UNSAT, 478 | UNSAT, 3,803 | UNSAT, 29,256 |
| CAP | UNSAT, 422 | UNSAT, 4,443 | UNSAT, 29,096 |
| SYM | UNSAT, 712 | UNSAT, 4,355 | UNSAT, 31,512 |
| FAN | Absent in full n = 8 run | SAT | SAT |

Dropping BISECTOR and CROSS together at n = 8 gives SAT. The unrestricted n = 12 no-ASYM run hit its 90-second cap. Adjacent distance-class merges also failed. A restricted SAT search then produced a full assignment passing all 315,239 clauses of the unrestricted ablation. After that check, the longer unrestricted probe was stopped. [Failed construction](runs/n12-fan-no-ASYM/constructed_model.log) · [Clause-checked SAT witness](runs/n12-fan-no-ASYM/restricted_model.txt)

## Reproduce in this directory

The builds are pinned to CaDiCaL commit 14593f819cb242082b127396218bd60889409737, drat-trim commit 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, and cake_lpr commit 033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2. Build these pinned tools separately as described in the [packet README](../README.md). The original proofs and the smaller checked n = 12 exports share the same canonical input. The two large n = 12 ablation traces, no-CAP and no-SYM, were discarded after verification. Their original SHA-256 digests, cores and checker logs are retained, and the ablation commands below regenerate the proof bytes. [CaDiCaL](https://github.com/arminbiere/cadical/tree/14593f819cb242082b127396218bd60889409737) · [drat-trim](https://github.com/marijnheule/drat-trim/tree/2e3b2dc0ecf938addbd779d42877b6ed69d9a985) · [cake_lpr](https://github.com/tanyongkiam/cake_lpr/tree/033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2)

Recheck the retained primary proofs using a fresh local directory. The unpacked DIMACS byte hash matches the solver input.

~~~sh
replay_dir=$(mktemp -d "$PWD/runs/replay.XXXXXX")
for case_name in n8 n10-fan n12-fan; do
    proof_stem=proof
    if [ "$case_name" = n12-fan ]; then proof_stem=trimmed; fi
    gzip -dc "runs/$case_name/formula.cnf.gz" > "$replay_dir/$case_name.cnf"
    xz -dc "runs/$case_name/$proof_stem.lrat.xz" > "$replay_dir/$case_name.lrat"
    xz -dc "runs/$case_name/$proof_stem.drat.xz" > "$replay_dir/$case_name.drat"
    nice -n 10 upstream/cake_lpr/cake_lpr --CML_HEAP_SIZE=1400 --CML_STACK_SIZE=256 \
        "$replay_dir/$case_name.cnf" "$replay_dir/$case_name.lrat"
    nice -n 10 upstream/drat-trim/drat-trim "$replay_dir/$case_name.cnf" "$replay_dir/$case_name.drat"
done
nice -n 10 python3 harvest.py > "$replay_dir/cases.tsv"
diff -u runs/cases.tsv "$replay_dir/cases.tsv"
~~~

Rebuild the input and original proof bytes. Select (n, K, options) as (8, 3, empty), (10, 4, --fan), or (12, 5, --fan). Add --omit CAP or --omit SYM to both encoders for the corresponding ablation. CaDiCaL returns 20 for UNSAT.

~~~sh
n=12
k=5
nice -n 10 python3 encoder.py "$n" "$k" "$replay_dir/rebuilt.cnf" --fan
nice -n 10 python3 encoder_reference.py "$n" "$k" "$replay_dir/reference.cnf" --fan
shasum -a 256 "$replay_dir/rebuilt.cnf" "$replay_dir/reference.cnf"
nice -n 10 upstream/cadical/build/cadical --lrat --no-binary "$replay_dir/rebuilt.cnf" "$replay_dir/rebuilt.lrat"
nice -n 10 upstream/cadical/build/cadical "$replay_dir/rebuilt.cnf" "$replay_dir/rebuilt.drat"
nice -n 10 upstream/cake_lpr/cake_lpr --CML_HEAP_SIZE=1400 --CML_STACK_SIZE=256 \
    "$replay_dir/rebuilt.cnf" "$replay_dir/rebuilt.lrat"
nice -n 10 upstream/drat-trim/drat-trim "$replay_dir/rebuilt.cnf" "$replay_dir/rebuilt.drat" \
    -c "$replay_dir/core.cnf"
~~~

Reproduce the generator and symmetry checks. The encoded samples and TSVs under runs/ are regenerated by these commands.

~~~sh
nice -n 10 python3 generate.py
nice -n 10 python3 generate.py --targeted
nice -n 10 clang++ -std=c++17 -O3 -Wall -Wextra -Werror validate.cpp -o runs/validate_fan
for n in $(seq 3 13); do
    nice -n 10 python3 encoder.py "$n" "$((n-1))" "runs/check_fan_$n.cnf" --fan
done
nice -n 10 runs/validate_fan other > "$replay_dir/families_other.tsv"
nice -n 10 runs/validate_fan regular > "$replay_dir/families_regular.tsv"
nice -n 10 runs/validate_fan targeted > "$replay_dir/families_targeted.tsv"
nice -n 10 python3 verify_inputs.py > "$replay_dir/verify_inputs.log"
~~~

Independent review can start with the FAN lemma and the retained n = 12 proofs. The replay used only the prior-art snapshot and the permitted upstream tools. Scope extends through n = 13. Earlier nested niceness adjustments gave the solver workers nice 20. The wrapper was corrected, and both retained proof formats for each main case passed replay at nice 10. The final harvest contains 44 canonical cases and the retained run data are below 50 MB.

CONTROLS: No. The clause-checked SAT controls for n = 5 through 13 in runs/cases.tsv are consistent with the regular witnesses. The three main corrupted-proof and three altered-core controls rejected in the case logs.

CONTRADICTING: No. The original n = 10 SAT assignment is in runs/n10/model.txt, with its raw classes reconstructed and refuted in SURVIVORS.md. The no-ASYM timeout and failed n = 12 construction remain in their run logs.

LABELS: No. harvest.py matched raw core clauses against the original DIMACS, then checked source clause IDs and family counts for every UNSAT case. verify_inputs.py independently matched all 143 raw necklace counts to the Burnside formula.
