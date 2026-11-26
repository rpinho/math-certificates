# Erdős #293. The second missing denominator of D₉

**Candidate. AI work.** GPT-6.2 Sol wrote my C/GMP solver and read nobody else’s code for the search. Claude Opus 5.5 separately read the soundness argument. No human has checked it. [Review record](VERDICT_for_ledger.txt).

I found no representation of 1 as nine distinct unit fractions that contains 1/13,878,989. I checked an exact representation for every integer strictly between 13,856,993 and 13,878,989. With the earlier result that 13,856,993 is the least missing denominator greater than one, this gives **13,878,989 as the second smallest integer missing from D₉ among integers greater than one**, where D₉ is the set of denominators occurring in such representations. [First omission replay](../../replays/erdos293-v9/), [Erdős #293](https://www.erdosproblems.com/293).

I continued through all release gaps below 20,000,000 in increasing order across Rounds 1 through 6. The table is now **complete below 20,000,000**: across all 623 previously omitted labels above 13,856,993 through 19,997,711, there are **63 exhaustive prime zeros** (starting with 13,878,989 and ending with 19,944,241) and **560 exact 9-term witnesses**, with **0 unsettled gaps** remaining. Together with EconLearn's first omission 13,856,993, all **64 missing denominators** of D_9 in `[2, 20,000,000]` are now classified and every one is prime. [Gap table](gaps.tsv), [round-6 completion note](ROUND6.md), [round-6 audit](VERDICT_round6.txt), [round-2 note](ROUND2.md), [public baseline](PRIOR_ART.md).

## Exhaustive search

For a fixed m, I remove 1/m and search for eight increasing denominators with reciprocal sum (m−1)/m, excluding m. I use exact rational bounds on the next denominator and tighten them using prime powers of m that still divide the reduced residual denominator. Each such power must divide at least one remaining denominator by the least-common-multiple rule. For the last two terms with residual p/q, the solver traverses divisors in (pa−q)(pb−q) = q² and uses GMP to compute the last denominator. [Solver](solver.c), [composite soundness](SOUNDNESS_COMPOSITE.md), [earlier soundness](SOUNDNESS.md).

I checked the shard partitions in a separate rational traversal and matched each completed zero shard’s predicted two-term state count against the raw output. At 13,878,989 all 1,412 shards finished, with zero representations, zero skips, 76,452,736 two-term states and 487,462,597,822 divisor probes. The manifests, raw shard rows and summaries are retained for all 63 exhaustive zeros, all 560 witnesses, and the reproduced first omission. [Partition and harvest code](run_gaps.py), [first new zero summary](logs/k9-13878989/summary.json), [source run report](REPORT.md).

## Controls

I matched ten fixed-denominator counts and compared the fixed-denominator solver with a separately written enumerator on 3,263,441 labels at k = 6 and 83,263 at k = 7. The k = 8 sharded and unsharded searches gave the same 474 solution rows at 27,538. I also reproduced the earlier k = 9 zero and recovered six nearby composite witnesses. [Control table](CONTROL_TABLE.md), [raw control log](logs/controls.log), [nearby witnesses](logs/nearby-controls.tsv), [first omission regression](logs/k9-13856993/summary.json).

| Mutant | Ordinary count → mutant count |
|---|---:|
| M1 requires a gap of at least two | 1 → 0 |
| M2 allows the fixed denominator in the tail | 1 → 2 |
| M5 drops final denominators at or above 2⁶⁴ | 88,573 → 0 |
| M6 requires another multiple of the full fixed denominator | 1 → 0 |
| Missing shard omits shard zero of the k = 8 positive control | 474 → 107 |
| Floor-plus-two starts the next denominator one too high | 2 → 0 |

## Certificate coverage

I used a separately written GMP checker to validate 9,999,376 release rows. It checks distinctness, the reciprocal sum and the label against the raw denominators. It found 623 omitted labels above 13,856,993 through 20,000,000 and checked that none occurs as an unlabelled term in another row. The first omission in that interval is 13,878,989, leaving 21,995 consecutive checked labels between the two missing denominators. This is a finite exact claim, so no statistical holdout applies. [Checker](check_certificates.c), [coverage log](logs/certificate-check.log), [whole-asset log](logs/certificate-check-full-range.log).

The release asset is external. Its SHA-256 is `81101aa7b75cfef850c8b98c4b3ac2711ea343684d19751511d58849125f5a2b`. [Pinned asset](https://github.com/EconLearn/erdos293-check/releases/download/v9-certificates/v9_certificates_10000001_to_20000000.txt.xz).

## Replay

From this packet, check `shasum -a 256 -c SHA256SUMS`. For a fresh run, use a separate writable directory and follow the commands in the source report. The replay uses macOS, Clang, Make, pkg-config, GMP, Python 3 and xz. Copy the source files, build with Make, verify the asset digest, and stream it through the checker for both intervals. Then run the separately written enumerator and controls, regenerate the target list, and run the sharded driver. The round-1 report gives the original commands and cutoff. Round 2 resumed with the same driver and binary under a fresh deadline. The number of gaps reached depends on throughput. [Round-1 commands and record replay](REPORT.md#reproduction), [round-2 run](ROUND2.md).

## Credits

I used EconLearn’s exhaustive result, certificate release and gap list, including ntysdd’s certificates. I followed the search method notes by jonathanwxh-cell in issue 403. The definition follows van Doorn and Tang. A400352 records v(k), and A006585 supplies enumeration checks. [Credits and sources](CREDITS.md), [discussion](https://github.com/teorth/erdosproblems/issues/403).
