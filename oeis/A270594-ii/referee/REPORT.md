RESULT: yes

Shipped: referee verdict HOLDS. 1,782,381 is the smallest natural number not of the form 4*pen(x)^2 + T(y) + hep(z) with x, y, z integers, so that clause of A270594(ii), as printed in inputs/A270594.txt, is false.

This is AI work (claude-opus-5-5). No human has checked it.

## 1. Definitions (verbatim from inputs/A270594.txt)

> (ii) Let T(x) = x(x+1)/2, pen(x) = x(3x+1)/2 and hep(x) = x(5x+3)/2. Then any natural number can be written as P(x,y,z) with x, y and z integers, where P(x,y,z) is either of the following polynomials: ... 4*pen(x)^2+T(y)+hep(z), ...

- x, y, z range over **all integers**, as the text says. So pen covers both branches k(3k±1)/2 (the generalized pentagonal numbers) and hep covers both branches k(5k±3)/2. T(y) = T(-1-y), so y ≥ 0 is enough. pen and hep are ≥ 0 on Z, so every term is nonnegative and the search space is finite.
- "Natural number": the A270594 comment does not say. Whether 0 is included makes no difference here: 0 = 4pen(0)^2 + T(0) + hep(0).

## 2. Method (referee_check.py, exact Python ints, stdlib only)

Reproduce: `python3 -I referee_check.py > run.log` (3.4 s, 27 MB peak RSS on the M5). Output is in run.log.

- **The claimed value n = 1,782,381.** x takes 42 values in [-21, 20] (21 of them negative) and z takes 1,689 values in [-844, 844] (844 negative). The script asserts that the next value outward on each side is > n. That gives 62,229 (x, z) pairs, each tested with an isqrt check of 8t+1: **0 representations**. Two independent routes agree:
  - a fixed wide box with x in [-40, 40] and z in [-1000, 1000] gives 0 hits;
  - a loop over y in [0, 1887] and all z, testing whether the remainder is 4p^2 with 24p+1 a square (p generalized pentagonal), also gives 0 hits.
- **Minimality.** A big-int bitset sieve over 0..2,000,000: (triangular indicator) shifted by each of the 43 distinct 4pen^2 values, then by each of the 1,789 distinct hep values. Unrepresented: **exactly one, [1782381]**. Below n there are **0** unrepresented values, so every m in 0..1,782,380 is represented. On 0..20000 and n±200, the sieve and direct enumeration disagree **0** times.
- Witnesses (x, y, z): 0 = (0,0,0), 1 = (0,1,0), 2 = (0,1,-1), 3 = (0,2,0), 1782380 = (0,1879,80), 1782382 = (0,1886,34).

## 3. Controls

- 25 random m < n (seed 20261127). Each has an explicit witness, re-checked by direct evaluation. For example, 1563261 = 4·pen(6)^2 + T(1760) + hep(15) = 12996 + 1549680 + 585, and 343426 = (1, 336, -339). All 25 pass. The full list is in run.log, section 3.
- The negative branches are actually used. 372 values m ≤ n are represented only with some x < 0: for example, 9 has only (-1, 1, 1) and 69 has only (-1, 4, -5). 156 values are represented only with some z < 0: for example, 2 has only (0, 1, -1). If the enumeration had missed negative x or z, these would show up as exceptions. They don't.

## 4. Other readings

- Naturals from 1: no change, since 0 is represented and n > 0.
- x, y, z ≥ 0 only: the clause becomes trivially false at m = 2. There are 3,593 exceptions ≤ n: 2, 8, 9, 11, 12, 18, 24, 38, 51, 54, …
- x ≥ 0 only: it fails first at 9 (373 exceptions ≤ n). z ≥ 0 only: it fails first at 2 (157 exceptions ≤ n).
- Sun's text says "integers", and the clause survives to 1,782,380 only with both signs. So the printed all-integers reading is the right one. Under it, the claim is neither trivial nor false.

## Referee rubric

- CONTROLS: no assumption overrode the controls. 25/25 random controls are represented with checked witnesses. The negative-branch controls (372 x-only and 156 z-only cases, run.log section 3) show the enumeration covers x, z < 0. The sieve vs direct cross-check has 0 mismatches over 20,402 values.
- CONTRADICTING: nothing was dropped. Three independent routes at n (62,229 pairs; the wide box; the y,z loop) all give 0 hits, and the sieve lists every unrepresented value up to 2·10^6 (count 1). No result contradicts the claim.
- LABELS: the claim's label "smallest, unrepresentable" was not trusted. It was recomputed from the definitions quoted from inputs/A270594.txt. I did not use the AI search's code (it was withheld).

## Limitations and next steps

- No network access. I could not check that inputs/A270594.txt matches the live OEIS entry, or whether this counterexample has already been reported (for example, in a later OEIS edit or by Sun). Recheck novelty before any public claim.
- Whether this is "new": a clause of a printed conjecture is settled (disproved) by an explicit counterexample, verified here independently. Its novelty against the literature is unverified.
- Only this one clause of part (ii) was checked.

VERDICT: HOLDS
