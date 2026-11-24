# Erdős #293 control results

## Fixed denominator and incidence checks

| k | m or check | Expected | Observed | Skips |
|---:|---|---:|---:|---:|
| 6 | 79 | 2 | 2 | 0 |
| 6 | 102 | 11 | 11 | 0 |
| 6 | 103 | 0 | 0 | 0 |
| 7 | 732 | 116 | 116 | 0 |
| 7 | 733 | 0 | 0 | 0 |
| 8 | 27,538 | 474 | 474 | 0 |
| 8 | 27,539 | 0 | 0 | 0 |
| 8 | 27,551 | 4 | 4 | 0 |
| 8 | 32,411 | 0 | 0 | 0 |
| 8 | 53,294 | 0 | 0 | 0 |
| 6 | Incidence sum across all 3,263,441 labels from 2 to 3,263,442, including 1,115 reached composites | 13,920 | 13,920 | 0 |
| 7 | Incidence sum across 83,231 reached labels, including 82,771 composites, plus 32 gap controls | 1,720,355 | 1,720,355 | 0 |
| 8 | Canonical representations for 27,538 across 90 shards | 474 | 474 | 0 |
| 9 | 13,813,799 deep prefix, required witness plus any other completions | ≥1 | 1 | 0 |
| 9 | 13,336,331 deep prefix, required witness plus any other completions | ≥1 | 2 | 0 |
| 9 | Sylvester fixture with an 87-bit reduced denominator | 174-bit last term | 174-bit last term | 0 |
| 4 | 42, one-term replay with prefix (2, 3) | 1 | 1 | 0 |

The separate enumerator reproduced A006585 at k = 3, 4, 5, 6 and 7 with counts 1, 6, 72, 2,320 and 245,765. Each enumerated row passed an exact sum check. The frozen k=7 sample ran with witness output and matched all 288 labels. The 90-shard and unsharded solution files at k=8 had identical SHA-256 digests, `3e28fd5f96130fee05e60ee65674a639d5e256e421fe474d2797142e23862683`. [Control log](logs/controls.log), [enumerator log](logs/enumerator.log).

## Mutants

| Mutant | Detecting control | Unmutated count | Mutated count |
|---|---|---:|---:|
| M1, requires a gap of at least 2 | k=4, m=42 | 1 | 0 |
| M2, omits the fixed-m tail exclusion | k=4, m=5 | 1 | 2 |
| M5, discards last denominators at least 2⁶⁴ | k=9 Sylvester deep prefix | 88,573 | 0 |
| M6, requires another multiple of m | k=4, m=42 | 1 | 0 |
| Missing shard | k=8, m=27,538, omit shard 0 | 474 | 107 |
| floor(q/p)+2 | k=6, m=79 | 2 | 0 |

M2 admitted the invalid row `2 5 5 10` with denominator 5 repeated. All fixture outcomes and the missing-shard hash are in [the control log](logs/controls.log).

## Required k=9 regression and nearby positives

The regression at 13,856,993 returned 0 solutions and 0 skips across all 1,412 shards. The separate partition replay and the solver agreed on 76,472,707 two-term states, and the recorded 487,525,854,050 divisor probes matched the previous run. [Regression summary](logs/k9-13856993/summary.json).

| m | Observed | Exact witness denominators |
|---:|---|---|
| 13,878,986 | found, 0 skips | 2 3 7 43 1807 4266711 13878986 1224346943820 5571819867780 |
| 13,878,987 | found, 0 skips | 2 3 7 43 1807 4266694 13878987 14792396018777 292312646689245427 |
| 13,878,988 | found, 0 skips | 2 3 7 43 1807 4266906 13878988 85341897212 324463292332512718 |
| 13,878,990 | found, 0 skips | 2 3 7 43 1807 4266696 13878990 5180229320760 10857680405927065893 |
| 13,878,991 | found, 0 skips | 2 3 7 43 1807 4266696 13878991 5046734223384 11737892721305283 |
| 13,878,992 | found, 0 skips | 2 3 7 43 1807 4266696 13878992 4915843726352 1530761438116801821 |

The six subjects were the nearest three certified composite labels on either side of the first gap. The search received only m and its generated shard tasks. All six emitted witnesses passed the separate Python rational check. The original positive attempt interrupted at 13,878,988 and its successful replay are both preserved. [Witness log](logs/nearby-controls.tsv), [interrupted run records](logs/initial-k9-13878988/).
