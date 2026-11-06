Referee 2 checker for [74,12,43] over GF(5), [128,14,79] over GF(5). The checker and its Python support sources are copies of the clean-room referee sources, with only the introductory comments edited to remove independence claims; executable code is unchanged. Inputs are copies of the corresponding generator.txt files. Python 3 uses only the standard library. All commands below start from the codetables/ root.

The exact GF(5) rank is computed by elimination. Every nonzero message is scaled so its last nonzero coordinate is 1, giving exactly (5^k−1)/4 projective representatives; all are enumerated. A full weight enumerator and an original-row minimum-weight witness are returned. Four worker threads cover disjoint partitions. ARM64 uses NEON; other architectures use the scalar fallback.

```sh
(cd checkers/ref2 && nice -n 10 clang++ -O3 -std=c++17 -pthread checker.cpp -o checker)
(cd checkers/ref2/inputs && shasum -a 256 -c SHA256SUMS)
(cd checkers/ref2 && nice -n 10 ./checker control_rs5_k3.txt 1 > results/control_rs5_k3.json 2> results/control_rs5_k3.log)
nice -n 10 checkers/ref2/checker q5_n74_k12_d43/generator.txt 4 > q5_n74_k12_d43/check/rerun_result.json 2> q5_n74_k12_d43/check/rerun.log
nice -n 10 checkers/ref2/checker q5_n128_k14_d79/generator.txt 4 > q5_n128_k14_d79/check/rerun_result.json 2> q5_n128_k14_d79/check/rerun.log
cp q5_n74_k12_d43/check/rerun_result.json checkers/ref2/results/q5_n74_k12.json
cp q5_n128_k14_d79/check/rerun_result.json checkers/ref2/results/q5_n128_k14.json
(cd checkers/ref2 && nice -n 10 python3 -B check_controls.py > scalar_checks.log 2> scalar_checks.stderr.log)
```

The last script runs the original repeated-identity and scalar subcode controls and checks the candidate witnesses. Candidate result copies in results/ are needed by that unchanged script. Run each four-thread candidate sequentially.

The package includes prepared data, original per-code outputs, and the successful package rerun outputs. Rebuilding creates a local executable; no prebuilt executable is distributed.
