Referee 3 checker for [129,14,80] over GF(5), [130,14,81] over GF(5), [130,16,77] over GF(5), [99,12,67] over GF(9). The checker and its Python support sources are copies of the clean-room referee sources, with only the introductory comments edited to remove independence claims; executable code is unchanged. Inputs are copies of the corresponding generator.txt files. Python 3 uses only the standard library. All commands below start from the codetables/ root.

This checker requires ARM64 NEON. prepare.py performs exact field arithmetic and elimination, checks the input hashes, builds disjoint pivot blocks, and confirms the last-coordinate puncturing relation. The C++ search enumerates all projective coefficient messages at each support size. For a block of rank r in dimension k, after support depth s an unseen codeword contributes at least max(0,s+1−(k−r)) on that block. Summing over disjoint blocks yields a complete stopping lower bound. The checker reports `complete=true` when the stopping lower bound reaches the witnessed distance. It can also stop at the support limit with `complete=false`; that result does not certify the exact distance. All four results here have `complete=true`. check_results.py checks the scalar witnesses, block row spaces, enumeration counts, and stopping inequalities.

```sh
(cd checkers/ref3 && nice -n 10 clang++ -O3 -std=c++17 -mcpu=native checker.cpp -o checker)
(cd checkers/ref3 && nice -n 10 python3 -B prepare.py > preparation.log)
(cd checkers/ref3 && nice -n 10 ./checker results/control_q5.dat results/control_q5.json 3 > results/control_q5.log)
(cd checkers/ref3 && nice -n 10 ./checker results/control_q9.dat results/control_q9.json 3 > results/control_q9.log)
nice -n 10 checkers/ref3/checker checkers/ref3/results/q5_n129_k14_d80.dat q5_n129_k14_d80/check/rerun_result.json 8 > q5_n129_k14_d80/check/rerun.log 2>&1
nice -n 10 checkers/ref3/checker checkers/ref3/results/q5_n130_k14_d81.dat q5_n130_k14_d81/check/rerun_result.json 8 > q5_n130_k14_d81/check/rerun.log 2>&1
nice -n 10 checkers/ref3/checker checkers/ref3/results/q5_n130_k16_d77.dat q5_n130_k16_d77/check/rerun_result.json 9 > q5_n130_k16_d77/check/rerun.log 2>&1
nice -n 10 checkers/ref3/checker checkers/ref3/results/q9_n99_k12_d67.dat q9_n99_k12_d67/check/rerun_result.json 8 > q9_n99_k12_d67/check/rerun.log 2>&1
cp q5_n129_k14_d80/check/rerun_result.json checkers/ref3/results/q5_n129_k14_d80.json
cp q5_n130_k14_d81/check/rerun_result.json checkers/ref3/results/q5_n130_k14_d81.json
cp q5_n130_k16_d77/check/rerun_result.json checkers/ref3/results/q5_n130_k16_d77.json
cp q9_n99_k12_d67/check/rerun_result.json checkers/ref3/results/q9_n99_k12_d67.json
(cd checkers/ref3 && nice -n 10 python3 -B check_results.py > result_checks.log)
```

The four candidate commands each use one CPU core. They may run simultaneously (four processes total); wait for all four to finish before copying results and running check_results.py. The recorded package rerun did this. The support limits 8,8,9,8 are the original referee limits, not timeouts.

The package includes prepared data, original per-code outputs, and the successful package rerun outputs. Rebuilding creates a local executable; no prebuilt executable is distributed.
