Referee 5 checker for [106,12,72] over GF(9). `checker.cpp` is a copy of the clean-room referee source; the only change is its first-line comment, which was reworded. It needs a GCC- or Clang-compatible C++17 compiler on a POSIX system and no other packages. All checks are assert() statements; do not build with -DNDEBUG. All commands below start from the codetables/ root.

The checker first tests the GF(9) field axioms for the stated encoding over all elements, pairs and triples, and runs two Reed–Solomon controls of known distance, [9,4,6] and [81,4,54]. It then computes the rank and enumerates every nonzero message whose first nonzero coordinate is 1, (9^12−1)/8 = 35,303,692,060 in all. It splits each message into two halves of six coordinates, stores the left half-word and the negated right half-word as bit planes, and counts the coordinates where they differ, which are the nonzero coordinates of the sum. A scalar cross-check on 10,000 message pairs confirms the packed weight count. The search has no cutoff: exhaustion gives d ≥ 72, and the printed witness, multiplied by the generator with scalar field arithmetic, gives d ≤ 72. It prints the full projective weight distribution.

```sh
(cd checkers/ref5 && nice -n 10 clang++ -O3 -std=c++17 -pthread -Wall -Wextra checker.cpp -o checker)
nice -n 10 checkers/ref5/checker
nice -n 10 checkers/ref5/checker q9_n106_k12_d72/generator.txt > q9_n106_k12_d72/check/rerun_result.txt 2> q9_n106_k12_d72/check/rerun.log
```

Without an input file the checker runs only the field and control checks. It uses four worker threads. Rebuilding creates a local executable; no prebuilt executable is distributed.
