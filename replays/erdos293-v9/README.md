# Erdős #293 replay of v(9) = 13,856,993

**Verdict. HOLDS.** With the exact solver `replay/solver.c`, I found no sum of nine distinct unit fractions equal to 1 that contains 1/13,856,993. With the exact checker `replay/check_certificates.c`, I verified a sum of that form containing $1/m$ for every integer $m$ from 2 through 13,856,992. Thus v(9), the least missing denominator greater than 1, is 13,856,993. This is a second separately written exhaustive search for the published value. [Erdős #293](https://www.erdosproblems.com/293), [EconLearn's result](https://github.com/teorth/erdosproblems/issues/403#issuecomment-5802603641).

**AI work (GPT-6.2 Sol). Nobody else's code was read for the replay. No human has checked it. No new result is claimed.**

## Absence search

I remove the fixed term $1/m$ and search for the remaining sum as eight unit fractions with increasing denominators distinct from $m$. My C solver uses exact rational bounds on each denominator. A prime power dividing the reduced residual denominator must divide at least one remaining denominator, which tightens the upper bound. For a reduced residual $p/q$ with two terms left, the solver enumerates eligible divisors of $q^2=(pa-q)(pb-q)$ and computes the last denominator with GMP. A separate Python rational traversal checks the shard partition and two-term visit counts. The proof gives the bounds for the sieve and the integer arithmetic. [Solver](replay/solver.c), [partition check](replay/run_main.py), [soundness](replay/SOUNDNESS.md).

| Shard measure | Recorded total |
|---|---:|
| Completed shards | 1,412 / 1,412 |
| Solutions | 0 |
| Skipped branches | 0 |
| DFS states | 76,531,788 |
| Two-term states | 76,472,707 |
| Divisor probes | 487,525,854,050 |

The partition check predicted 76,472,707 two-term states, with an exact match in every shard. The manifest, per-shard records and aggregate table preserve the task and result for each shard. [Manifest](replay/manifest-13856993.tsv), [partition log](replay/logs/manifest-check.log), [per-shard records](replay/logs/shards), [aggregate table](replay/logs/main-shards.tsv).

## Controls

I checked ten fixed-denominator counts for $k$ from 6 through 8. A separately written full enumerator reproduced A006585 for $k$ from 3 through 7, with exact rational checks of its rows and direct comparisons against the fixed-denominator solver. The sharded and unsharded $k=8$, $m=27,538$ positive control gave identical sets of 474 solutions. I also recovered two supplied deep-prefix solutions, a Sylvester solution with a 174-bit last denominator, and a one-term completion. [Controls](replay/logs/controls.log), [enumerator](replay/enumerator.c), [full replay report](replay/REPORT.md).

| Mutant | Ordinary count → mutant count |
|---|---:|
| M1 requires a gap after the previous denominator | 1 → 0 |
| M2 omits the fixed-denominator exclusion in the tail | 1 → 2 |
| M5 drops last denominators with at least 65 bits | 88,573 → 0 |
| M6 requires another multiple of the fixed denominator | 1 → 0 |
| Missing shard omits the first solution-bearing shard | 474 → 107 |
| Floor-plus-two lower limit skips the first candidate | 2 → 0 |

The first M1 fixture, $k=6$ and $m=79$, returned two solutions in both runs. I retained the traceback locally because it contains a machine-local path. I used a fixture containing consecutive denominators for the reported M1 control. [Source replay report](replay/REPORT.md), [detecting controls](replay/logs/controls.log).

## Certificate coverage

I streamed EconLearn's three compressed release files through the separately written exact checker `replay/check_certificates.c`, which verified 19,999,375 rows, including all 13,856,991 required labels and 6,142,384 rows above the required interval. Using GMP, the checker tests the nine raw denominators for distinctness, the labeled denominator and an exact reciprocal sum of 1. It found zero missing labels, zero bad lines, zero duplicate labels in the required interval and zero rows containing 13,856,993. Four corruption controls exercise the sum, distinctness, label membership and missing-label checks. This is an exact existence and absence claim over fixed integers, so a statistical holdout does not apply. [Checker](replay/check_certificates.c), [checker output](replay/logs/certificate-check.log), [corruption controls](replay/logs/corruption.log).

The compressed assets are available from the release. The packet carries their names, sizes, URLs and SHA-256 digests in the asset manifest. [Certificate release](https://github.com/EconLearn/erdos293-check/releases/tag/v9-certificates), [release asset digests](replay/data/release-assets.tsv).

## Replay

Verify the packet and the parts of the original run seal that travel with it. The original input seal also records the digest of the original solver executable. The packet contains the solver source and archives the manifest outside the build directory.

```bash
# From the packet root.
set -euo pipefail
shasum -a 256 -c SHA256SUMS
(
    cd replay
    shasum -a 256 -c OWN.sha256
    awk '$2 != "build/solver" {sub(/^build\/manifest-/, "manifest-", $2); print $1 "  " $2}' \
        MAIN_INPUTS.sha256 | shasum -a 256 -c -
)
```

To rerun the search, use macOS with Bash, Clang, Make, Python 3, GMP and pkg-config. Start in the packet root and create a fresh writable work directory so the rerun generates its own logs, executable, input seal and result seal.

```bash
set -euo pipefail
archive="$PWD/replay"
work="$(mktemp -d)"
cp "$archive"/{Makefile,solver.c,enumerator.c,check_certificates.c,controls.py,geometry.py,run_main.py,test_certificates.py,fetch_certificates.sh,verify_data.sh} "$work/"
cd "$work"
mkdir -p data logs
printf '%s\n' "$(( $(date +%s) + 14400 ))" > deadline.epoch
nice -n 10 make all
for k in 3 4 5 6 7; do
    nice -n 10 build/enumerator "$k" > "build/enumerator-$k.solutions" 2>> logs/enumerator.log
done
nice -n 10 python3 -B controls.py 4 > logs/controls.log 2>&1
nice -n 10 python3 -B geometry.py 13856993 9 --depth 4 --ceiling 200000 > logs/geometry.log
cmp build/manifest-13856993.tsv "$archive/manifest-13856993.tsv"
pgrep -f math_e293v9_1123 | wc -l || true
nice -n 10 python3 -B run_main.py math_e293v9_1123 --workers 4 > logs/main-driver.log 2>&1
shasum -a 256 -c MAIN_INPUTS.sha256
shasum -a 256 -c OWN.sha256
cut -f 1-16 logs/main-shards.tsv | cmp - <(cut -f 1-16 "$archive/logs/main-shards.tsv")
test ! -s logs/main-solutions.txt
```

To replay coverage in the same fresh directory, use jq, curl and xz. The fetcher checks the compressed file sizes and digests against the release. The comparison pins that release metadata to this packet before running the checker.

```bash
nice -n 10 /bin/bash fetch_certificates.sh > logs/download.log 2>&1
cmp data/release-assets.tsv "$archive/data/release-assets.tsv"
nice -n 10 /bin/bash verify_data.sh > logs/certificate-check.log 2> logs/certificate-check.time
cmp logs/certificate-check.log "$archive/logs/certificate-check.log"
nice -n 10 python3 -B test_certificates.py > logs/corruption.log
cmp logs/corruption.log "$archive/logs/corruption.log"
```

## Credits

I used the definition of van Doorn and Tang and the closed forms posted by jonathanwxh-cell in issue #403. EconLearn ran the first exhaustive v(9) search and published the certificates checked here, including contributions from ntysdd. OEIS A400352 records v(k), and A006585 supplies the full enumeration control counts. [Credits](CREDITS.md), [prior art](replay/PRIOR_ART.md).
