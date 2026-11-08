Referee 6 checker for [85,15,54] over GF(9). These five files are copies of the clean-room referee's sources. The only change is the first-line comments of `checker.py` and `enumerate.cpp`, which were reworded from "Independent" to "Clean-room". It needs Python 3 (standard library only) and a GCC/Clang-compatible C++17 compiler: `enumerate.cpp` uses `__builtin_popcountll`, and `run_check.py` invokes it as `clang++`. It uses no SIMD intrinsics.

Full enumeration of the (9^15−1)/8 ≈ 2.6·10^13 projective messages does not fit, so the proof has two parts.
- `checker.py` asserts the GF(9) field axioms for the stated encoding, the input hash and the input shape. It records the rank, the pivots, whether each row's first 80 entries are x^i·g(x) (`shift_structure`, which implies the first 80 columns have rank 15) and a BCH (Vandermonde) bound in `initial_check.json`, without asserting them.
- `prepare.py` and `enumerate.cpp` impose zeros on the last coordinates to get a 12-dimensional subcode, and run a complete Brouwer–Zimmermann information-set enumeration on it, which covers the empty-tail and position-0-only cases. A Reed–Solomon [9,3,7] control runs through the same engine.
- `finish_distance.py` asserts rank 15, the 65 shared roots and the BCH bound of at least 51. It covers every other appended-support case with the BCH bound and assembles the result. A witness of weight 54 gives the upper bound.

The step "the first 80 columns have rank 15" rests on the recorded `shift_structure: true` in `initial_check.json`, which is not asserted. The Python checks are `assert` statements, so do not run with `python -O` or `PYTHONOPTIMIZE` set.

The scripts read `inputs/q9_n85_k15_d54.txt` and `inputs/SHA256SUMS`, and write their outputs to the current directory. So replay them in a fresh working directory; [COMMAND.md](../../q9_n85_k15_d54/check/COMMAND.md) gives the commands. The whole replay takes about 8 s on four threads.
