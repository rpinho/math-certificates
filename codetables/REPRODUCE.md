# Reproducing the nine exact checks

The checkers for the first seven codes (referees 2–4) were built from source inside this package and rerun successfully on 2026-11-06T20:35:26.562449+00:00. All ranks and exact minimum distances match the saved referee outputs. No candidate disagreement or incomplete search occurred. The original referee outputs remain in each check/result.json and check/run.log; the package reruns use rerun_result.json and rerun.log; for [106,12,72] they are check/result.txt and check/rerun_result.txt; for [85,15,54] the originals are check/distance_result.json and the other unprefixed files, and the reruns are check/rerun_*.

The run used Python 3.12.13 and Apple clang 21.0.0 on ARM64. Referee 2 has a scalar fallback; referees 3 and 4 require ARM64 NEON. All Python support files use only the standard library. Set PYTHONDONTWRITEBYTECODE=1 (or use python3 -B) to avoid creating bytecode caches. The commands below use python3 for portability; the executed Python was the shared research environment.

At most four enumeration workers ran concurrently: each referee 2 candidate used four threads sequentially; all four single-threaded referee 3 candidates ran simultaneously; the referee 4 candidate then used four threads. Every computational command used nice -n 10. The invoking launcher already had nice value 10, so the effective worker nice value was 20; these runtimes reflect that lower scheduling priority.

| code | exact rank | exact d | referee d | checker time (s) | elapsed wall time (s) |
|---|---:|---:|---:|---:|---:|
| [74,12,43] GF(5) | 12 | 43 | 43 | 0.272180 | 0.284518 |
| [128,14,79] GF(5) | 14 | 79 | 79 | 8.401730 | 8.418859 |
| [129,14,80] GF(5) | 14 | 80 | 80 | 7.559980 | 7.582909 |
| [130,14,81] GF(5) | 14 | 81 | 81 | 7.860010 | 7.878884 |
| [130,16,77] GF(5) | 16 | 77 | 77 | 65.796800 | 65.818849 |
| [99,12,67] GF(9) | 12 | 67 | 67 | 89.229100 | 89.249746 |
| [92,13,61] GF(9) | 13 | 61 | 61 | 34.741800 | 34.758886 |
| [106,12,72] GF(9) | 12 | 72 | 72 | 27.9225 | 28.237 |
| [85,15,54] GF(9) | 15 | 54 | 54 | 4.024 (candidate enumeration only) | not measured |

Checker time is the program’s own elapsed measurement; wall time additionally includes process launch/exit. The four concurrent referee 3 wall times overlap and should not be summed as total wall time.

The full projective weight enumerators match for both referee 2 codes. Referee 3 returns complete=true with the same enumeration counts and a stopping lower bound reaching the witnessed distance for all four codes. Referee 4 repeats 22,475,321,323 normalized evaluations and proves an unseen lower bound of 63 against the weight-61 witness. The unchanged referee scalar checks of witnesses, control codes, information sets and stopping inequalities all completed successfully. The preparation output confirms that column 129 (zero based) of [130,14,81] punctures to [129,14,80].

The following are the executed build, preparation, candidate and postprocessing commands, expressed relative to codetables/. Output paths and numeric limits are unchanged. All returned exit code 0. The four referee 3 candidate commands were launched together; wait for them all before the result copies and scalar checks. Each command is individually reproducible.

**build ref2** — 2.037333 s.

```sh
(cd checkers/ref2 && nice -n 10 clang++ -O3 -std=c++17 -pthread checker.cpp -o checker) > checkers/ref2/build.log 2> checkers/ref2/build.stderr.log
```

**build ref3** — 1.292920 s.

```sh
(cd checkers/ref3 && nice -n 10 clang++ -O3 -std=c++17 -mcpu=native checker.cpp -o checker) > checkers/ref3/build.log 2> checkers/ref3/build.stderr.log
```

**build ref4** — 1.331114 s.

```sh
(cd checkers/ref4 && nice -n 10 clang++ -O3 -std=c++17 -pthread exact_distance.cpp -o exact_distance) > checkers/ref4/build.log 2> checkers/ref4/build.stderr.log
```

**prepare ref3** — 0.514663 s.

```sh
(cd checkers/ref3 && nice -n 10 python3 prepare.py) > checkers/ref3/preparation.log 2> checkers/ref3/preparation.stderr.log
```

**prepare ref4** — 0.090062 s.

```sh
(cd checkers/ref4 && nice -n 10 python3 prepare.py) > checkers/ref4/preparation.log 2> checkers/ref4/preparation.stderr.log
```

**ref2 RS control** — 0.265605 s.

```sh
(cd checkers/ref2 && nice -n 10 ./checker control_rs5_k3.txt 1) > checkers/ref2/results/control_rs5_k3.json 2> checkers/ref2/results/control_rs5_k3.log
```

**ref3 GF(5) RS control** — 0.154799 s.

```sh
(cd checkers/ref3 && nice -n 10 ./checker results/control_q5.dat results/control_q5.json 3) > checkers/ref3/results/control_q5.log
```

**ref3 GF(9) RS control** — 0.009028 s.

```sh
(cd checkers/ref3 && nice -n 10 ./checker results/control_q9.dat results/control_q9.json 3) > checkers/ref3/results/control_q9.log
```

**ref4 RS control** — 0.174452 s.

```sh
(cd checkers/ref4 && nice -n 10 ./exact_distance rs_control.dat 1 rs_result.json) > checkers/ref4/rs_run.log
```

**q5_n74_k12_d43** — 0.284518 s.

```sh
nice -n 10 checkers/ref2/checker q5_n74_k12_d43/generator.txt 4 > q5_n74_k12_d43/check/rerun_result.json 2> q5_n74_k12_d43/check/rerun.log
```

**q5_n128_k14_d79** — 8.418859 s.

```sh
nice -n 10 checkers/ref2/checker q5_n128_k14_d79/generator.txt 4 > q5_n128_k14_d79/check/rerun_result.json 2> q5_n128_k14_d79/check/rerun.log
```

**q5_n129_k14_d80** — 7.582909 s.

```sh
nice -n 10 checkers/ref3/checker checkers/ref3/results/q5_n129_k14_d80.dat q5_n129_k14_d80/check/rerun_result.json 8 > q5_n129_k14_d80/check/rerun.log
```

**q5_n130_k14_d81** — 7.878884 s.

```sh
nice -n 10 checkers/ref3/checker checkers/ref3/results/q5_n130_k14_d81.dat q5_n130_k14_d81/check/rerun_result.json 8 > q5_n130_k14_d81/check/rerun.log
```

**q5_n130_k16_d77** — 65.818849 s.

```sh
nice -n 10 checkers/ref3/checker checkers/ref3/results/q5_n130_k16_d77.dat q5_n130_k16_d77/check/rerun_result.json 9 > q5_n130_k16_d77/check/rerun.log
```

**q9_n99_k12_d67** — 89.249746 s.

```sh
nice -n 10 checkers/ref3/checker checkers/ref3/results/q9_n99_k12_d67.dat q9_n99_k12_d67/check/rerun_result.json 8 > q9_n99_k12_d67/check/rerun.log
```

**q9_n92_k13_d61** — 34.758886 s.

```sh
nice -n 10 checkers/ref4/exact_distance checkers/ref4/candidate.dat 4 q9_n92_k13_d61/check/rerun_result.json > q9_n92_k13_d61/check/rerun.log
```

The unchanged referee support scripts expect these additional copies of the completed outputs:

```sh
cp q5_n74_k12_d43/check/rerun_result.json checkers/ref2/results/q5_n74_k12.json
cp q5_n128_k14_d79/check/rerun_result.json checkers/ref2/results/q5_n128_k14.json
cp q5_n129_k14_d80/check/rerun_result.json checkers/ref3/results/q5_n129_k14_d80.json
cp q5_n130_k14_d81/check/rerun_result.json checkers/ref3/results/q5_n130_k14_d81.json
cp q5_n130_k16_d77/check/rerun_result.json checkers/ref3/results/q5_n130_k16_d77.json
cp q9_n99_k12_d67/check/rerun_result.json checkers/ref3/results/q9_n99_k12_d67.json
cp q9_n92_k13_d61/check/rerun_result.json checkers/ref4/candidate_result.json
```

**ref2 scalar controls and witnesses** — 0.528808 s.

```sh
(cd checkers/ref2 && nice -n 10 python3 check_controls.py) > checkers/ref2/scalar_checks.log 2> checkers/ref2/scalar_checks.stderr.log
```

**ref3 stopping proofs and witnesses** — 0.211342 s.

```sh
(cd checkers/ref3 && nice -n 10 python3 check_results.py) > checkers/ref3/result_checks.log
```

**ref4 scalar witness** — 0.101592 s.

```sh
(cd checkers/ref4 && nice -n 10 python3 check_witness.py) > checkers/ref4/witness_check.log
```

The package includes the prepared information sets and data, so every intermediate is inspectable. The original prepare.py scripts regenerate them. Build executables were moved to Trash after the runs; only source and small text evidence are distributed.

Verify the saved package file hashes from this folder with:

```sh
shasum -a 256 -c SHA256SUMS
```

SHA256SUMS lists every other file and excludes itself. A fresh rerun changes timing and process IDs, and multithreaded witness selection may change; ranks, minimum distances, completeness bounds and enumerator counts are the mathematical results to compare.

## [106,12,72] over GF(9) (referee 5, added 2026-11-07)

Referee 5's checker was built from the packaged source and rerun on 2026-11-07 with Apple clang 21.0.0 on ARM64, four threads, nice 10. Rank 12 and exact minimum distance 72 match the referee output, and so does the full projective weight distribution, line for line. The printed minimum-weight witness can differ between runs because of thread scheduling.

**build ref5** — compile warnings: none (build.log and build.stderr.log are empty).

```sh
(cd checkers/ref5 && nice -n 10 clang++ -O3 -std=c++17 -pthread -Wall -Wextra checker.cpp -o checker) > checkers/ref5/build.log 2> checkers/ref5/build.stderr.log
```

**q9_n106_k12_d72** — checker 27.9225 s, wall 28.237 s. The same run also executes the field-axiom checks and both Reed–Solomon controls.

```sh
nice -n 10 checkers/ref5/checker q9_n106_k12_d72/generator.txt > q9_n106_k12_d72/check/rerun_result.txt 2> q9_n106_k12_d72/check/rerun.log
```

## [85,15,54] over GF(9) (referee 6, added 2026-11-08 UTC)

The referee's Python and C++ sources are in [checkers/ref6](checkers/ref6/README.md). They write into their working directory, so the replay runs in a fresh temporary directory; [q9_n85_k15_d54/check/COMMAND.md](q9_n85_k15_d54/check/COMMAND.md) has the commands. The package replay (Python 3.9.6; the referee used Python 3.12.13) gave rank 15 and d = 54 in 7.7 s including compilation, with the candidate enumeration taking 4.024 s, matching the referee outputs apart from timing fields and thread output order ([RERUN.md](q9_n85_k15_d54/check/RERUN.md)).
