RESULT: yes
Shipped: a second separately written exhaustive search and exact certificate check establishing v(9) = 13,856,993.

**Verdict: HOLDS.** No sum of nine distinct unit fractions equal to 1 contains $1/13{,}856{,}993$, and every $m$ from 2 through 13,856,992 has a checked nine-term representation containing $1/m$. New result under the job's definition? **No.** This reproduces the published value for Erdős #293 and OEIS A400352. This is AI work. No human has checked it.

## Exhaustive absence search

| Measure | Observed |
|---|---:|
| Completed shards | 1,412 / 1,412 |
| Representations containing 13,856,993 | 0 |
| Skipped branches | 0 |
| DFS states in the shards | 76,531,788 |
| Two-term states | 76,472,707 |
| Divisor probes | 487,525,854,050 |
| DFS states plus divisor probes | 487,602,385,838 |
| Largest selected DFS denominator | 12,338,559 |
| Largest reduced denominator $q$ | 69 bits |

The exact fraction partition replay predicted 76,472,707 two-term states and agreed with every shard's count. The DFS tally includes shard roots. A divisor probe counts a completed exponent assignment in the admissible interval passed to the congruence test. Raw per-shard records are in [logs/shards](logs/shards), with an aggregate table in [main-shards.tsv](logs/main-shards.tsv). Both [OWN.sha256](OWN.sha256) and [MAIN_INPUTS.sha256](MAIN_INPUTS.sha256) verified.

The 15-shard pilot, 1% rounded up, projected 333 seconds with eight workers. The interval from the input seal to the results seal was 309 seconds. The measured main pilot worker peaked at 57,507,840 bytes RSS, about 460 MB for eight workers at that measured size. The tracked workers and job-name process count were zero at cleanup. [Pilot log](logs/pilot.log), [RSS measurement](logs/rss-pilot-worker-0.stderr), [cleanup log](logs/cleanup.log).

The published total was 406,906,925,247 nodes in 2,000 shards. This comparison was made after writing and verifying `OWN.sha256`. Our prime-power bound and shard partition determine which residual states are visited, and we count residual states and eligible divisor probes separately. The captured published record gives no common definition for every counted operation, so the totals describe the two runs under their respective implementations. [Prior art and published total](PRIOR_ART.md).

## Controls

| $k$ | $m$ | Expected | Observed |
|---:|---:|---:|---:|
| 6 | 79 | 2 | 2 |
| 6 | 102 | 11 | 11 |
| 6 | 103 | 0 | 0 |
| 7 | 732 | 116 | 116 |
| 7 | 733 | 0 | 0 |
| 8 | 27,538 | 474 | 474 |
| 8 | 27,539 | 0 | 0 |
| 8 | 27,551 | 4 | 4 |
| 8 | 32,411 | 0 | 0 |
| 8 | 53,294 | 0 | 0 |

The separately written full enumerator gave A006585 counts of 1, 6, 72, 2,320 and 245,765 for $k=3,\ldots,7$. Every enumerated row passed a separate exact Python fraction check. At $k=6$, the fixed-denominator solver matched all 3,263,441 integers from 2 through the full enumerator's largest denominator, 3,263,442. Completeness of the full enumeration gives zero above this maximum. At $k=7$, 288 direct per-$m$ comparisons matched, comprising 256 positive labels and 32 gaps. The full incidence sums were 13,920 at $k=6$ and 1,720,355 at $k=7$, equal to $k\,A006585(k)$.

The 90-shard and unsharded canonical solution files for $k=8,m=27{,}538$ both had 474 rows and SHA-256 `3e28fd5f96130fee05e60ee65674a639d5e256e421fe474d2797142e23862683`. Both supplied nine-term certificates reappeared in their requested deep prefixes, with one completion in the $m=13{,}813{,}799$ shard and two in the $m=13{,}336{,}331$ shard. The nine-term Sylvester control recovered its 174-bit last denominator. A one-term replay recovered $(2,3,7,42)$ from the prefix $(2,3)$ with fixed $m=42$. [Control log](logs/controls.log).

| Mutant | Detecting control | Ordinary → mutated |
|---|---|---:|
| M1 requires $a\ge u+2$ | $k=4,m=42$ | 1 → 0 |
| M2 omits the fixed-$m$ tail exclusion | $k=4,m=5$ | 1 → 2 |
| M5 drops $b\ge 2^{64}$ | Sylvester deep-prefix fixture | 88,573 → 0 |
| M6 requires another multiple of $m$ | $k=4,m=42$ | 1 → 0 |
| Missing shard | $k=8,m=27{,}538$, first solution-bearing shard omitted | 474 → 107 |
| Starts at $\lfloor q/p\rfloor+2$ | $k=6,m=79$ | 2 → 0 |

The first M1 fixture, $k=6,m=79$, returned two solutions with and without the mutant. Both solutions have a tail gap greater than one. The repaired fixture uses the consecutive denominators 2 and 3 in $(2,3,7,42)$. The raw failed trial is retained locally because the traceback contains a machine-local path.

## Certificate coverage

The standalone GMP rational checker streamed all three EconLearn release files. It verified 19,999,375 data rows, including all 13,856,991 labels in the required interval. It recorded **0 missing labels, 0 bad lines, 0 duplicate labels in the required interval, and 0 verified rows containing 13,856,993**. It checked all 6,142,384 supplied rows beyond the required interval as well. The three compressed files matched the release sizes and SHA-256 digests. They were moved to the macOS Trash after verification. Redownloading the same bytes is sufficient for a replay. [Checker log](logs/certificate-check.log), [asset names and digests](data/release-assets.tsv), [download checks](logs/download.log), [certificate release](https://github.com/EconLearn/erdos293-check/releases/tag/v9-certificates).

The standalone checker rejected a shifted denominator by exact sum, a duplicate term by integer comparison, and removal of $m$ by checking label membership. Deleting the line reported the required $m$ missing. [Corruption log](logs/corruption.log).

## Soundness and verdict checks

The search removes $1/m$ and traverses increasing denominators with exact lower and upper bounds. The prime-power bound follows because a reduced residual denominator divides the lcm of its remaining denominators. The two-term closure traverses the possible smaller factors of $q^2=(pa-q)(pb-q)$. It computes the last denominator with GMP. The independent geometric bound puts every main DFS choice with three or more terms left within 12,806,327. The sieve covers this range, and every factorization is checked by multiplication. A statistical holdout does not apply to this exact existence and absence claim. [Soundness proof](SOUNDNESS.md), [solver](solver.c), [full enumerator](enumerator.c), [certificate checker](check_certificates.c).

- CONTROLS: No. The ten rows in `logs/controls.log` matched the frozen values, both positive deep prefixes were recovered, and all six mutants changed their detecting controls. The first M1 fixture was insensitive, returning two solutions in both runs.
- CONTRADICTING: No. The partition replay and `logs/main-shards.tsv` account for all 76,472,707 two-term states, with zero skips and zero solutions. The certificate checker processed 19,999,375 data rows, including all rows outside the required range, and queried the parsed denominators themselves for the target. The initial M1 outcome is reported above.
- LABELS: No. `check_certificates.c` parsed and compared each label with the nine raw denominator integers and verified the exact sum before counting coverage. `logs/corruption.log` shows that a row with its labeled denominator removed failed this membership check. The shard replay also checked each result against its exact manifest task and expected leaf count.

## Reproduction

Run in a clean authorized job folder with these source files, Clang, Python 3, GMP, `pkg-config`, `xz`, and `jq`. The deadline file below represents a fresh four-hour allocation.

```bash
set -euo pipefail
mkdir -p build data logs
printf '%s\n' "$(( $(date +%s) + 14400 ))" > deadline.epoch
nice -n 10 make all
for k in 3 4 5 6 7; do
    nice -n 10 build/enumerator "$k" > "build/enumerator-$k.solutions" 2>> logs/enumerator.log
done
nice -n 10 python3 -B controls.py 4 > logs/controls.log 2>&1
nice -n 10 python3 -B geometry.py 13856993 9 --depth 4 --ceiling 200000 > logs/geometry.log
pgrep -f math_e293v9_1123 | wc -l || true
nice -n 10 python3 -B run_main.py math_e293v9_1123 --workers 8 > logs/main-driver.log 2>&1
shasum -a 256 -c OWN.sha256
shasum -a 256 -c MAIN_INPUTS.sha256
nice -n 10 /bin/bash fetch_certificates.sh > logs/download.log 2>&1
nice -n 10 /bin/bash verify_data.sh > logs/certificate-check.log 2> logs/certificate-check.time
nice -n 10 python3 -B test_certificates.py > logs/corruption.log
```

The driver resumes from completed shard files using the same manifest, inputs and authorized deadline. For an interrupted run, count job processes with the command above before restarting.

## Sources, limitations and next step

The supplied 2026-11-23 prior-art capture records the published result, the smaller-$k$ baselines, and ntysdd's earlier bounded search. It credits the public residual and two-term identities and the van Doorn–Tang definition. EconLearn's executable and other search or checker source were outside the permitted sources. The job's download-only network access also prevented a live literature or scoreboard refresh. The workspace exposed neither the launcher model nor its effort setting for verification. [Prior art](PRIOR_ART.md), [Erdős #293](https://www.erdosproblems.com/293), [public computation discussion](https://github.com/teorth/erdosproblems/issues/403), [van Doorn–Tang](https://arxiv.org/abs/2512.22083), [A400352](https://oeis.org/A400352), [A006585](https://oeis.org/A006585).

The next verification step is human inspection of the proof and a local replay of the sealed run.
