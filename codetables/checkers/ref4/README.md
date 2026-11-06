Referee 4 checker for [92,13,61] over GF(9). The checker and its Python support sources are byte-for-byte copies of the clean-room referee sources. Inputs are copies of the corresponding generator.txt files. Python 3 uses only the standard library. All commands below start from the codetables/ root.

This checker requires ARM64 NEON. prepare.py checks the field axioms, exact rank, input hash and Reed–Solomon control and builds seven disjoint information sets of size 13. The search enumerates all projective coefficient vectors of support weight 1 through 8 in every information set. An unseen word would have at least nine nonzero coordinates in each of the seven disjoint sets, so would have weight at least 63. A witnessed weight of 61 therefore proves d=61. check_witness.py verifies the transformed matrices and multiplies the witness by the original generator using scalar field arithmetic.

```sh
(cd checkers/ref4 && nice -n 10 clang++ -O3 -std=c++17 -pthread exact_distance.cpp -o exact_distance)
(cd checkers/ref4 && nice -n 10 python3 -B prepare.py > preparation.log)
(cd checkers/ref4 && nice -n 10 ./exact_distance rs_control.dat 1 rs_result.json > rs_run.log)
nice -n 10 checkers/ref4/exact_distance checkers/ref4/candidate.dat 4 q9_n92_k13_d61/check/rerun_result.json > q9_n92_k13_d61/check/rerun.log 2>&1
cp q9_n92_k13_d61/check/rerun_result.json checkers/ref4/candidate_result.json
(cd checkers/ref4 && nice -n 10 python3 -B check_witness.py > witness_check.log)
```

The candidate uses four worker threads. Run it separately from other candidate jobs to stay within four cores.

The package includes prepared data, original per-code outputs, and the successful package rerun outputs. Rebuilding creates a local executable; no prebuilt executable is distributed.
