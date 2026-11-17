Shipped: candidate exact values f(13)=8, f(14)=8 for Erdős #1183, with total colourings and checked DRAT proofs; candidate and unrefereed.

Cases tried: **2 dimensions**, n=13 and n=14. Verified theorem DRAT certificates produced: **4**. Exact values settled: **2 candidates**. Total-colouring files: **2**. Each certified case also has a checked SAT closure-deletion control and a rejected corrupted-proof control.

**Did we find something new? Yes, candidate exact-value results:** f(13)=8, f(14)=8. The bounded public-source search found no earlier exact value for these dimensions; see [PRIOR_ART.md](PRIOR_ART.md). The lower bound f(13)≥8 is already public. This extends the existing closure-SAT method; no new general method is claimed.

**Correction to the ask.** The requested f(13)=7 is impossible. The omega note and current Bhattacharjee–Mandal–Bhattacharya paper already give f(13)≥8. We settled the mathematically possible next exact value, 8. No structured non-rank search for upper bound seven was run, because the published lower bound rules out every colouring.

**Definition.** The [problem page](https://www.erdosproblems.com/1183) asks for a “monochromatic family of at least $f(n)$ sets which is closed under taking unions and intersections.” Equivalently, f(n)=minχ max{|L|: L is a nonempty monochromatic union-and-intersection-closed subfamily of 2^[n]}. The [cited paper](https://raw.githubusercontent.com/anaxia-research/Erdos-1183/2842ef3a58604a8f4b35271d5753c2bf9bdecd0b/paper/Erdos.tex), Introduction, calls a family “a sublattice if it is closed under both union and intersection.” Neither ∅ nor [n] is required to be in L.

All bit-mask files use bit i for element i+1. The query is **at least nine members**, covering families of every larger size too. The full encoding, counter argument and soundness of the standard transposition lex-leaders are explained in [CHECKS.md](CHECKS.md). Every theorem check used default **backward** drat-trim, without `-f`, on the exact listed CNF.

## n=13: candidate f(13)=8

Rank word, from rank 0 through rank 13: **`11001011000110`**. Colour 0 ranks: `[2, 3, 5, 8, 9, 10, 13]`; colour 1 ranks: `[0, 1, 4, 6, 7, 11, 12]`. Full colouring: [certificates/n13_coloring.json](certificates/n13_coloring.json) (8,192 subsets).

Explicit monochromatic chain masks: `0,1,15,63,127,2047,4095`. Explicit optimal eight-member lattice masks: `3,227,1795,2019,4067,6115,8163,8191`. [logs/n13_coloring_check.log](logs/n13_coloring_check.log) prints `FULL COLOURING AND OPTIMAL WITNESS VALID`.

The chain alone gives f(13)≥7. The [omega note](https://raw.githubusercontent.com/the-omega-institute/trureturing/HEAD/Problems/bhattacharjee-mandal-bhattacharya-2026-sublattice-chain-bound-refutation.md) gives f(n)≥(n+3)/2 for odd n≥11. BMB Proposition `prop:flower` gives ceil((n+1+floor((n+1)/12))/2), hence **f(13)≥8**. We separately check this finite case: if every monochromatic lattice had size ≤7, every maximal chain would have exactly seven sets of each colour; adjacent-chain exchanges then force colour to depend only on rank. [check_rank_screen.py](check_rank_screen.py) checks actual closed-family witnesses for all 8,192 colour-swap representatives, including all 1,716 balanced representatives (all 3,432 balanced rank words). Its output [logs/n13_rank_screen_check.log](logs/n13_rank_screen_check.log) is `ALL RANK WORDS REJECTED FOR UPPER SEVEN`. This reproduces the known lower bound.

For the corrected target, the cheap screen rejects 7,958 of 8,192 colour-swap representatives (3,473 by chains, 4,485 by checked lattices plus comparable prefixes); 234 survive. The first full-SAT colouring tried was the successful n=12 word with a final 0. Both queries below are UNSAT, so its maximum monochromatic lattice has size eight and **f(13)≤8**.

| Colour | Variables | Clauses | Solver | Solver wall s | Solver peak RSS bytes | Backward check wall s | Check peak RSS bytes |
|---|---:|---:|---|---:|---:|---:|---:|
| 0 | 113,152 | 14,751,865 | CaDiCaL UNSAT | 2.84 | 1,704,443,904 | 26.63 | 1,420,034,048 |
| 1 | 128,440 | 17,916,013 | CaDiCaL UNSAT | 22.69 | 4,340,875,264 | 100.83 | 1,953,284,096 |

Colour 0:

- Exact CNF: [data/n13_11001011000110_c0_lex.cnf](data/n13_11001011000110_c0_lex.cnf), 232,767,831 bytes; SHA-256 `6dfa65c62cdc04fef32a4d08209f5c87fc594e710bb066ba124f88d370846e86`.
- Base CNF: [data/n13_11001011000110_c0.cnf](data/n13_11001011000110_c0.cnf); SHA-256 `5081db668592748036daf5522791772972022bca35324dd41a304e418af05908`.
- Verified uncompressed DRAT: 97,861,273 bytes; SHA-256 `5c2aa6b9a1373055ca8bf6feb2b974d0da6944646eba2f140ab1b7bd1691d08f`.
- Retained `xz -T1` proof: [certificates/n13_11001011000110_c0_lex.drat.xz](certificates/n13_11001011000110_c0_lex.drat.xz), 12,887,576 bytes; SHA-256 `547d375af2065d39572307554b5463d871fab2c582ed150264800793d6505dac`.
- Solver [logs/n13_extension_c0.solve](logs/n13_extension_c0.solve): `s UNSATISFIABLE`, exit 20. Backward checker [logs/n13_extension_c0.drat_check](logs/n13_extension_c0.drat_check): **`s VERIFIED`**, exit 0.
- [logs/n13_extension_c0.statement_check](logs/n13_extension_c0.statement_check): **`EVERY CLAUSE REBUILT FROM STATEMENT`**, including all 78 coordinate transpositions. The check is separately written by the same agent, **not independent**.

Colour 1:

- Exact CNF: [data/n13_11001011000110_c1_lex.cnf](data/n13_11001011000110_c1_lex.cnf), 266,296,176 bytes; SHA-256 `dcd199ef02063665c693662669db382875cb34d09fd783e8459fcce22c4782f0`.
- Base CNF: [data/n13_11001011000110_c1.cnf](data/n13_11001011000110_c1.cnf); SHA-256 `9331d9995a42be5e281e267e4912159736e66934a8c2dae734a75975aade159d`.
- Verified uncompressed DRAT: 201,701,771 bytes; SHA-256 `e576ec4902f00921344f445fac63e9c89484f47f6ce04022e080bfea77a64a14`.
- Retained `xz -T1` proof: [certificates/n13_11001011000110_c1_lex.drat.xz](certificates/n13_11001011000110_c1_lex.drat.xz), 22,163,952 bytes; SHA-256 `20790502a710a4105dd6cc0b0bd58a1c2fcea2e75d09bd79ca58f53776004719`.
- Solver [logs/n13_extension_c1.solve](logs/n13_extension_c1.solve): `s UNSATISFIABLE`, exit 20. Backward checker [logs/n13_extension_c1.drat_check](logs/n13_extension_c1.drat_check): **`s VERIFIED`**, exit 0.
- [logs/n13_extension_c1.statement_check](logs/n13_extension_c1.statement_check): **`EVERY CLAUSE REBUILT FROM STATEMENT`**, including all 78 coordinate transpositions. The check is separately written by the same agent, **not independent**.

Rejection controls:

- Delete exactly original closure clause 13,974,481, `-3220 -3312 0`, from colour 0; all counter and lex clauses remain. [data/n13_deleted.cnf](data/n13_deleted.cnf) is SAT, exit 10, in 2.51 s. The model [logs/n13_deleted.solve](logs/n13_deleted.solve) is checked against **every remaining clause** by [logs/n13_deleted.model_check](logs/n13_deleted.model_check). The separately constructed nine-set witness is [data/n13_deletion_witness.json](data/n13_deletion_witness.json); its direct full-clause check is [logs/n13_deletion_witness_check](logs/n13_deletion_witness_check).
- Corrupt the proof by deleting every justification and retaining only the final empty clause in textual DRAT: [certificates/n13_corrupt.drat](certificates/n13_corrupt.drat). Default backward drat-trim rejects it with **`s NOT VERIFIED`**, exit 1: [logs/n13_corrupt.check](logs/n13_corrupt.check). Expected rejection is not a theorem proof.

Control CNF SHA-256: `79d51383bc262a827185002ec550324c16d64e078a638d21304177f0cf7432e4`. Corrupted proof SHA-256: `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa`. Both controls are regenerated by the commands below; the corrupted proof is the two-byte text `0\n`.

## n=14: candidate f(14)=8

Rank word, from rank 0 through rank 14: **`110010110001101`**. Colour 0 ranks: `[2, 3, 5, 8, 9, 10, 13]`; colour 1 ranks: `[0, 1, 4, 6, 7, 11, 12, 14]`. Full colouring: [certificates/n14_coloring.json](certificates/n14_coloring.json) (16,384 subsets).

Explicit monochromatic chain masks: `0,1,15,63,127,2047,4095,16383`. Explicit optimal eight-member lattice masks: `0,1,15,63,127,2047,4095,16383`. [logs/n14_coloring_check.log](logs/n14_coloring_check.log) prints `FULL COLOURING AND OPTIMAL WITNESS VALID`.

A maximal chain has fifteen subsets. Its larger colour class is a subchain of at least eight sets and is closed under union and intersection. Thus **f(14)≥8** for every colouring.

The cheap screen rejects 16,368 of 16,384 colour-swap representatives (9,949 by chains, 6,419 by checked lattices plus comparable prefixes), leaving 16. The first full-SAT colouring tried appends 1 to the successful n=13 word. The two checked UNSAT queries below prove **f(14)≤8**. Search data: [data/screen_n14_t9.json](data/screen_n14_t9.json) and [data/screen_n14_t9_witnesses.jsonl](data/screen_n14_t9_witnesses.jsonl).

The unchanged round-2 Python-list encoder hit the guard before writing any CNF: 14.213 s, sampled aggregate RSS 7,515,635,712 bytes, output size zero. The colour-0 query requires 68,851,692 closure clauses. After recording the failure in STATUS.md, `encode_family_stream.py` changed only storage, preserving every variable, clause and clause order; the separately written checker rebuilt the full result. Default CaDiCaL then hit the guard on the full colour-0 lex CNF after 6.332 s, sampled aggregate RSS 7,861,108,736 bytes, zero proof bytes, result UNKNOWN. The supplied default kissat build fit. [logs/n14_extension_c0.encode.json](logs/n14_extension_c0.encode.json), [logs/n14_extension_c0.solve.json](logs/n14_extension_c0.solve.json). These are resource stops, not UNSAT results. Default kissat on colour 1 was also stopped after 57.823 s at sampled aggregate RSS 7,512,571,904 bytes; its unfinished proof is retained as `certificates/n14_110010110001101_c1_lex_kissat.UNVERIFIED.drat`. The alternative for colour 1 is the standard `--plain` configuration on the exact same CNF, after this observed default-setting failure.

| Colour | Variables | Clauses | Solver | Solver wall s | Solver peak RSS bytes | Backward check wall s | Check peak RSS bytes |
|---|---:|---:|---|---:|---:|---:|---:|
| 0 | 274,105 | 69,563,843 | kissat UNSAT | 9.49 | 3,676,733,440 | 273.05 | 6,309,232,640 |
| 1 | 262,399 | 61,463,499 | kissat --plain UNSAT | 121.37 | 1,973,796,864 | 133.66 | 6,363,217,920 |

Colour 0:

- Exact CNF: [data/n14_110010110001101_c0_lex.cnf](data/n14_110010110001101_c0_lex.cnf), 1,110,354,998 bytes; SHA-256 `e17cc779134fc56128b956a223695b28b8f20e1d43befa927c59dfc0bb8c4813`.
- Base CNF: [data/n14_110010110001101_c0.cnf](data/n14_110010110001101_c0.cnf); SHA-256 `8c9a5442a44a6b0a40e7cf0f0a2f2d921b8d63a514028e987ad8888128b3f553`.
- Verified uncompressed DRAT: 530,031,562 bytes; SHA-256 `cc3794efafe7eebb09aba3f705c2c3d88182ff4988eeaeb9eefabdf284c55286`.
- Retained `xz -T1` proof: [certificates/n14_110010110001101_c0_lex_kissat.drat.xz](certificates/n14_110010110001101_c0_lex_kissat.drat.xz), 68,698,972 bytes; SHA-256 `cf83c2ae9cc27d9e1f35c8fcda06942316845f571b02f0b01cee511f6a421e64`.
- Solver [logs/n14_extension_c0.kissat_solve](logs/n14_extension_c0.kissat_solve): `s UNSATISFIABLE`, exit 20. Backward checker [logs/n14_extension_c0.kissat_drat_check](logs/n14_extension_c0.kissat_drat_check): **`s VERIFIED`**, exit 0.
- [logs/n14_extension_c0.statement_check](logs/n14_extension_c0.statement_check): **`EVERY CLAUSE REBUILT FROM STATEMENT`**, including all 91 coordinate transpositions. The check is separately written by the same agent, **not independent**.

Colour 1:

- Exact CNF: [data/n14_110010110001101_c1_lex.cnf](data/n14_110010110001101_c1_lex.cnf), 937,785,191 bytes; SHA-256 `4ef13fb01b49058199649ddc58887421f382c0108019078d6c3e3ce9c793cd99`.
- Base CNF: [data/n14_110010110001101_c1.cnf](data/n14_110010110001101_c1.cnf); SHA-256 `27ee9711805a5ffd5e8425875a823259418426253af036cfa8d07829078c0231`.
- Verified uncompressed DRAT: 1,406,556,327 bytes; SHA-256 `356842ddd0573ea909a280f54e24e2f33e72ab9a2e957e94d0e1a83fae47a8f8`.
- Retained `xz -T1` proof: [certificates/n14_110010110001101_c1_lex_kissat_plain.drat.xz](certificates/n14_110010110001101_c1_lex_kissat_plain.drat.xz), 36,520,456 bytes; SHA-256 `9abcb772cf46e854888fbd2db7531170ea40285fda144183bd6d4bba8f907a84`.
- Solver [logs/n14_extension_c1.kissat_plain_solve](logs/n14_extension_c1.kissat_plain_solve): `s UNSATISFIABLE`, exit 20. Backward checker [logs/n14_extension_c1.kissat_plain_drat_check](logs/n14_extension_c1.kissat_plain_drat_check): **`s VERIFIED`**, exit 0.
- [logs/n14_extension_c1.statement_check](logs/n14_extension_c1.statement_check): **`EVERY CLAUSE REBUILT FROM STATEMENT`**, including all 91 coordinate transpositions. The check is separately written by the same agent, **not independent**.

Rejection controls:

- Delete exactly original closure clause 29,676,065, `-2238 -4253 0`, from colour 1; all counter and lex clauses remain. [data/n14_deleted.cnf](data/n14_deleted.cnf) is SAT, exit 10, in 10.10 s. The model [logs/n14_deleted.solve](logs/n14_deleted.solve) is checked against **every remaining clause** by [logs/n14_deleted.model_check](logs/n14_deleted.model_check). The separately constructed nine-set witness is [data/n14_deletion_witness.json](data/n14_deletion_witness.json); its direct full-clause check is [logs/n14_deletion_witness_check](logs/n14_deletion_witness_check).
- Corrupt the proof by deleting every justification and retaining only the final empty clause in textual DRAT: [certificates/n14_corrupt.drat](certificates/n14_corrupt.drat). Default backward drat-trim rejects it with **`s NOT VERIFIED`**, exit 1: [logs/n14_corrupt.check](logs/n14_corrupt.check). Expected rejection is not a theorem proof.

Control CNF SHA-256: `47c772242c69401b0142fb79c75d9ddf99674d3a33961e16d82fc021dd1d2949`. Corrupted proof SHA-256: `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa`. Both controls are regenerated by the commands below; the corrupted proof is the two-byte text `0\n`.

## Exact regeneration and replay

Run from this job directory, one solver or drat-trim process at a time. The shared Python is `../../.venv/bin/python`; `run_limited.py` applies nice 10, `/usr/bin/time -l`, the RSS guard and proof/directory caps. The tool executables were copied from `../erdos_sat2/tools/`, without rebuilding. [tools/COMMITS.json](tools/COMMITS.json) pins source commits; [tools/COPIED_THIS_JOB.json](tools/COPIED_THIS_JOB.json) records matching executable hashes. No n=11 or n=12 solve was rerun.

```sh
PY=../../.venv/bin/python
for c in 0 1; do
  nice -n 10 "$PY" encode_family.py 11001011000110 "$c" 9 "data/n13_11001011000110_c${c}.cnf"
  nice -n 10 "$PY" add_lex.py "data/n13_11001011000110_c${c}.cnf" "data/n13_11001011000110_c${c}_lex.cnf"
  nice -n 10 "$PY" encode_family_stream.py 110010110001101 "$c" 9 "data/n14_110010110001101_c${c}.cnf"
  nice -n 10 "$PY" add_lex.py "data/n14_110010110001101_c${c}.cnf" "data/n14_110010110001101_c${c}_lex.cnf"
done
```

For each regenerated CNF, compare its SHA-256 with the per-colour values above (also [HASHES.json](HASHES.json)). Exact solver and check invocations, including elapsed wall time, return code and peak sampled aggregate RSS, are in the corresponding `logs/*.json`. Examples:

```sh
"$PY" run_limited.py --seconds 900 --log logs/replay_n13.solve --proof data/replay.drat -- tools/cadical/build/cadical -q data/n13_11001011000110_c0_lex.cnf data/replay.drat
"$PY" run_limited.py --seconds 1200 --log logs/replay_n14.solve --proof data/replay14.drat -- tools/kissat/build/kissat -q data/n14_110010110001101_c0_lex.cnf data/replay14.drat
xz -dc certificates/n13_11001011000110_c0_lex.drat.xz > data/replay_checked.drat
"$PY" run_limited.py --seconds 2400 --log logs/replay_drat.check -- tools/drat-trim/drat-trim data/n13_11001011000110_c0_lex.cnf data/replay_checked.drat
nice -n 10 "$PY" check_statement.py data/n13_11001011000110_c0_lex.cnf
nice -n 10 "$PY" check_statement.py data/n14_110010110001101_c0_lex.cnf
nice -n 10 "$PY" check_rank_screen.py
nice -n 10 "$PY" check_coloring.py certificates/n13_coloring.json
nice -n 10 "$PY" check_coloring.py certificates/n14_coloring.json
nice -n 10 "$PY" make_deletion.py data/n13_11001011000110_c0_lex.cnf data/n13_deletion_witness.json data/replay_deleted13.cnf
nice -n 10 "$PY" make_deletion.py data/n14_110010110001101_c1_lex.cnf data/n14_deletion_witness.json data/replay_deleted14.cnf
printf '0\n' > certificates/n13_corrupt.drat
printf '0\n' > certificates/n14_corrupt.drat
nice -n 10 "$PY" check_control.py data/n13_11001011000110_c0_lex.cnf data/n13_deleted.cnf --model logs/n13_deleted.solve
nice -n 10 "$PY" check_control.py data/n14_110010110001101_c1_lex.cnf data/n14_deleted.cnf --model logs/n14_deleted.solve
```

For the n=13 second query replace colour 0 by 1. For n=14 colour 1, use `tools/kissat/build/kissat --plain -q`, because the default configuration hit the memory cap. The retained proof is `_c1_lex_kissat_plain.drat.xz`; colour 0 uses `_c0_lex_kissat.drat.xz`. Search reproduction: `nice -n 10 "$PY" screen_ranks.py 13 8`, then `screen_ranks.py 13 9`, then `screen_ranks.py 14 9`. These screens use only our supplied, locally checked seed data. `find_deletion_witness.py WORD 9` reproduces each almost-closed witness. Uncompressed verified proofs were hashed before compression, `xz -T1 -k` compressed, and moved to macOS Trash; the retained compressed streams are also checked against the verified uncompressed hashes.

## Resources, sources and credit

Maximum sampled allocated job disk: **8,503,443,456 bytes**; current allocated disk: **7,093,133,312 bytes**. Conservative all-time disk bound (current allocated files plus removed uncompressed proofs rounded up to MiB, plus a 64-MiB margin): **9,398,951,936 bytes**, below 30 GB. No single proof approaches 15 GB. The largest measured aggregate RSS sample was 7,861,108,736 bytes, when the default n=14 CaDiCaL run was stopped. Successful runs were below the 8-GB cap. All workers ran at nice 10; at most four CPU-heavy workers overlapped, with one solver or drat-trim at a time. Solver/check per-process RSS above is from `/usr/bin/time -l`; aggregate measurements in JSON include overlapping lightweight checks and this session.

Initial public reads were on November 16 local time (November 17, 04:50 UTC). [PRIOR_ART.md](PRIOR_ART.md) records problem page, all eleven forum comments, anaxia issue #20 and paper, omega note, arXiv, recently updated GitHub searches, and named AI-result repositories, with failures and coverage limits. Final recheck: [sources/FETCH_FINAL.json](sources/FETCH_FINAL.json). No submissions, commits, pushes, PRs, posts, uploads or messages were made.

Credit: **Erdős and Ulam** for the problem; **Deep Bhattacharjee, Priyabrata Mandal and Ushashi Bhattacharya** for closure-SAT, counterexample-guided searches and prior bounds; **the omega institute note** for the stronger odd-dimensional lower bound; **ipezygj** for the SAT-plus-DRAT workflow on #609; **CaDiCaL and kissat (A. Biere et al.)**; **drat-trim (M. Heule et al.)**. The anaxia and ipezygj repositories were read only as text; none of their research scripts were copied, imported or run. All theorem encoders/checkers here are our supplied/reused code or separately written same-agent code. No predictive metric was used, so trivial/simple/SBS comparisons do not apply.

## Open items

Both exact values are candidate and unrefereed. Human mathematical review remains open; no next dimension was searched. The public-source search is bounded and does not prove priority. The arguments and encoder checks are not a formal proof in a proof assistant; the requested DRAT proofs pass the standard backward checker.

Completed 2026-11-17T05:25:31.363885+00:00. Session elapsed 36:19 (well under eight hours). Final process snapshot [logs/final_processes.txt](logs/final_processes.txt) confirms no worker processes remain.
