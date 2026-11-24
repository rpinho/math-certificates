RESULT: yes
Shipped: 13,878,989 is the second smallest missing denominator in D_9 for m ≥ 2.

A separately written exhaustive search found zero nine-term representations containing 13,878,989. All 1,412 shards completed with zero skips. The exact release check certified each of the 21,995 integers from 13,856,994 through 13,878,988. There were no gaps to settle before the answer. The reproduced first missing denominator is 13,856,993.

Is it new? **Yes against the 2026-11-23 prior-art snapshot.** The answer settles the open second-missing value identified in that snapshot. A live priority check was outside this job's download-only network scope. This is AI work. No human has checked it.

| Measure at m = 13,878,989 | Verified value |
|---|---:|
| Shards completed | 1,412 / 1,412 |
| Representations | 0 |
| Solver and work-cap skips | 0 |
| Two-term states, observed and predicted | 76,452,736 |
| Divisor probes | 487,462,597,822 |
| Largest reduced denominator | 69 bits |
| Largest selected prefix denominator | 12,321,172 |
| Sum of shard elapsed times | 2,688.396 seconds |

The 15-shard pilot projected 423.5 seconds for the remaining work. The run from exact partition to verified result took about 356 seconds. [Manifest](logs/k9-13878989/manifest.tsv), [raw shard output](logs/k9-13878989/shards.tsv), [pilot](logs/k9-13878989/pilot.tsv), [summary](logs/k9-13878989/summary.json).

## Follow-on gaps

After the answer, the search settled 59 more gaps in order. It found 52 exact representations and 7 more exhaustive zeros. The witnesses and shard summaries are in [gaps.tsv](gaps.tsv).

| m | Verdict | Witness or shard summary |
|---:|---|---|
| 13,950,983 | found | 2 3 8 25 609 40748 13950983 56241185 9271789594135214746600 |
| 13,951,403 | found | 2 3 7 43 3200 4147 13951403 154230285300 822750236226413440 |
| 14,004,827 | found | 2 3 7 43 1807 4383484 14004827 145097004 51618856488141309393 |
| 14,177,041 | found | 2 3 9 19 344 59071 14177041 1828838160 200988477338640 |
| 14,462,659 | missing | 75,960,880 two-term states, zero skips. [Shard summary](logs/k9-14462659/summary.json) |
| 14,574,107 | found | 2 3 7 43 2160 11028 14574107 210607439310 251572920362382106547920 |
| 14,651,683 | found | 2 3 7 44 925 907720 14651683 11322481450 334298178740045068450440 |
| 14,757,749 | missing | 75,737,317 two-term states, zero skips. [Shard summary](logs/k9-14757749/summary.json) |
| 14,789,963 | missing | 75,713,859 two-term states, zero skips. [Shard summary](logs/k9-14789963/summary.json) |
| 14,883,497 | found | 2 3 7 76 94 75392 14883497 198442826624 3358441719975041952 |
| 14,890,739 | found | 2 3 8 25 609 40711 14890739 4533506196800 11385764411357292799198400 |
| 14,902,271 | found | 2 3 7 43 1816 335350 14902271 14207825171400 9756073779183170 |
| 15,125,507 | found | 2 3 7 56 169 29302 973035 15125507 3203619810969581640 |
| 15,149,639 | found | 2 3 7 43 1808 1843632 15149639 244192270 443953164999286143180 |
| 15,254,381 | found | 2 3 7 43 1808 1829177 15254381 3816584153 794191924757504112 |
| 15,495,283 | found | 2 3 7 43 1808 1824920 15495283 169264256238 11855044935909310600080 |
| 15,519,389 | missing | 75,224,865 two-term states, zero skips. [Shard summary](logs/k9-15519389/summary.json) |
| 15,634,583 | found | 2 3 7 43 1988 19752 15634583 480012967266 112194390865016712 |
| 15,649,759 | found | 2 3 7 44 1230 3715 15649759 20249261340 1299273845585969946 |
| 15,746,921 | found | 2 3 8 25 606 60950 15746921 31995093 3392416292514930200 |
| 15,795,071 | found | 2 3 7 57 160 64100 15795071 4434861060 2801957812713410400 |
| 15,800,227 | found | 2 3 7 45 652 18693 15800227 211489853695 202219952218707474940 |
| 15,802,511 | found | 2 3 7 43 1808 1821104 15802511 8899812426 1983221914001735870652 |
| 15,853,531 | found | 2 3 7 44 1308 3148 15853531 301851230240 854492234761371360 |
| 15,862,361 | found | 2 3 9 19 343 118180 15862361 457718375415 4826217657241708740 |
| 15,865,651 | missing | 75,018,095 two-term states, zero skips. [Shard summary](logs/k9-15865651/summary.json) |
| 15,946,939 | found | 2 3 7 44 1586 2214 15946939 5989682916 90373082245809213994 |
| 15,951,707 | found | 2 3 7 49 295 87224 15951707 382840968 15084208349043330 |
| 16,007,743 | found | 2 3 7 43 1814 421344 16007743 163601240 1624725822731326112160 |
| 16,061,963 | found | 2 3 7 43 1814 420368 16061963 1230166704 1474028168596667029164 |
| 16,086,041 | found | 2 3 7 43 1840 98334 16086041 145230140160 1401706793429703936 |
| 16,178,797 | found | 2 3 7 43 2236 9397 16178797 255509268 12023645753171566618 |
| 16,210,177 | missing | 74,826,283 two-term states, zero skips. [Shard summary](logs/k9-16210177/summary.json) |
| 16,215,427 | found | 2 3 7 47 395 819204 16215427 7788761680 22556840024619312496 |
| 16,228,669 | found | 2 3 7 43 1807 4398212 16228669 57337917 14991266552039335012 |
| 16,253,647 | found | 2 3 7 45 631 521325 1866300 16253647 1773975688959835788 |
| 16,264,403 | found | 2 3 7 43 1833 123558 16264403 787421986 11193113078566387485261654 |
| 16,278,671 | found | 2 3 7 43 1811 681519 16278671 32406303331920 135498929014594066700080 |
| 16,291,837 | found | 2 3 7 43 1820 239390 16291837 48444396 1407543221865427570 |
| 16,407,283 | found | 2 3 7 43 1807 5712483 14200277 16407283 269198919034806 |
| 16,418,203 | found | 2 3 7 43 1814 420024 16418203 4640623779 2052325405127755592969288 |
| 16,435,123 | found | 2 3 8 25 601 499169 1410475 16435123 131941417692414252120 |
| 16,458,947 | found | 2 3 7 43 1809 1179800 16458947 101010600 513277364898971464050 |
| 16,476,011 | found | 2 3 7 50 264 46330 16476011 24568256160 8765680582186783200 |
| 16,503,569 | found | 2 3 10 16 244 14653 16503569 133713951792 205465897252815194207165 |
| 16,503,659 | found | 2 3 7 44 928 217258 16503659 684800142 17385265209206091028832 |
| 16,513,727 | found | 2 3 7 45 669 10814 16513727 6234748025940 13793762061596764643283020 |
| 16,534,517 | found | 2 3 8 25 602 182595 16534517 56186086000 1458839872889564696454000 |
| 16,540,253 | found | 2 3 8 26 313 98236 16540253 13307295148620 886537068444750974680 |
| 16,542,839 | found | 2 4 5 21 427 25661 16542839 522334948 1424155377407766045 |
| 16,648,571 | missing | 74,600,153 two-term states, zero skips. [Shard summary](logs/k9-16648571/summary.json) |
| 16,662,991 | found | 2 3 7 43 1811 680862 16662991 1014524615874 303485261092012786358 |
| 16,665,953 | found | 2 3 7 73 99 101796 16665953 3967347209796 10797185525192170735650327 |
| 16,735,273 | found | 2 3 7 52 220 30084 16735273 53887579060 9129844508785 |
| 16,741,507 | found | 2 3 7 43 1807 4054026 16741507 40352962398 1285074889636618158 |
| 16,751,039 | found | 2 3 7 47 395 817800 16751039 218611572900 344225272448928851400 |
| 16,752,511 | found | 2 3 7 47 395 817800 16752511 101834921244 7518803725137244200 |
| 16,757,219 | found | 2 3 7 46 485 117952 16757219 256301664605 251229589558080 |
| 16,759,021 | found | 2 3 7 43 1816 334516 16759021 10425504262758 214091765387018162512856 |

The first unsettled candidate is **16,762,189**. The search stopped there with 563 unsettled in-scope candidates. It completed 15 of 1,403 shards. The pilot estimated 391.5 seconds of work with 365.6 seconds remaining. [Unsettled shard summary](logs/k9-16762189/summary.json).

## Release coverage

The SHA-256-pinned EconLearn asset contained 9,999,376 valid rows, three header comments, zero bad rows and zero duplicate labels. Of 6,143,007 integers strictly above 13,856,993 through 20,000,000, 6,142,384 have a checked certificate. The other 623 do not appear even as a nonlabel term on any valid row. The 624 full-release omissions include 13,856,993 itself, which explains the difference from the job's expected count. The first in-scope gap is 13,878,989. [Requested interval](logs/certificate-check.log), [full release interval](logs/certificate-check-full-range.log), [checksum log](logs/download-check.log).

## Controls

| Control | Observed |
|---|---|
| Ten fixed k=6, 7, 8 point counts | All ten matched, with 0 skips |
| k=6 all-m comparison | 3,263,441 labels matched, including all 1,115 reached composites. Incidence sum 13,920 |
| k=7 full-positive comparison plus frozen gap sample | 83,263 labels matched, including all 82,771 reached composites. Incidence sum 1,720,355 |
| k=7 frozen 288-label comparison with witness output | All 288 matched and all emitted witnesses passed exact verification |
| k=8 at 27,538 | Identical canonical solution files with 474 rows for both 90 shards and one unsharded search |
| Other inherited fixtures | Both deep prefixes, the 174-bit Sylvester last term and the one-term fixture matched |
| k=9 regression at 13,856,993 | 1,412/1,412 shards, 0 solutions, 0 skips, 76,472,707 two-term states |
| Six nearby k=9 composite controls | 6/6 found and verified exactly, with 0 skips |

| Mutant | Ordinary count | Mutated count |
|---|---:|---:|
| M1 | 1 | 0 |
| M2 | 1 | 2 |
| M5 | 88,573 | 0 |
| M6 | 1 | 0 |
| Missing shard | 474 | 107 |
| floor(q/p)+2 | 2 | 0 |

The full point table, mutant fixtures and six exact composite witnesses are in [CONTROL_TABLE.md](CONTROL_TABLE.md). The third nearby composite initially produced an exact witness and then hit a worker group cancellation error. The retry with direct subprocess cancellation passed before the gap search. The first planned interruption added explicit work-cap accounting during the regression, and the resumed run verified the existing completed shards. The binary and regression manifest were unchanged. [Restart snapshot](logs/regression-restart-snapshot.json), [interrupted run records](logs/initial-k9-13878988/), [resumed driver](logs/gap-driver.log).

## Soundness

Removing the fixed term leaves $(m-1)/m$. Every prime power exactly dividing $m$ must divide at least one remaining denominator because their least common multiple is a common denominator for that reduced fraction. The terms witnessing different powers can differ. At a prefix the same argument applies to the reduced denominator $q$. Its prime factors come from $m$ and the prefix choices. The DFS applies the strongest of the applicable prime-power bounds, and the separate partition replay checks each applicable bound with exact Python fractions. The two-term closer traverses divisors of $q^2=(pa-q)(pb-q)$ and uses GMP to recover the last denominator. The geometric caps keep the campaign within checked native arithmetic. An absence requires every shard, its exact predicted two-term count, and zero skips. Any positive needs one exact witness. There is no statistical holdout for these finite exact claims. [SOUNDNESS_COMPOSITE.md](SOUNDNESS_COMPOSITE.md).

## Reproduction

Run in a clean authorized copy of this job directory with Clang, GMP, pkg-config, xz and Python 3. Run the search from a shell at nice 10 where permitted. This workspace inherited nice 15 and macOS refused raising its priority to nice 10. The initial commands using relative nice +10 reached effective nice 20. The final continuation used the inherited nice 15. Concurrency stayed at eight workers or fewer. Measured k=9 peak worker RSS was 57,507,840 bytes.

~~~bash
set -euo pipefail
mkdir -p build data logs
printf '%s\n' "$(( $(date +%s) + 14400 ))" > deadline.epoch
make all
asset=v9_certificates_10000001_to_20000000.txt.xz
curl -q --fail --location --max-time 1800 \
    --output "data/$asset" \
    "https://github.com/EconLearn/erdos293-check/releases/download/v9-certificates/$asset" \
    > logs/download.log 2>&1
printf '%s  data/%s\n' \
    81101aa7b75cfef850c8b98c4b3ac2711ea343684d19751511d58849125f5a2b "$asset" |
    shasum -a 256 -c > logs/download-check.log
xz -dc "data/$asset" |
    /usr/bin/time -l build/check_certificates 13856994 20000000 13856993 \
    > logs/certificate-check.log 2> logs/certificate-check.time
xz -dc "data/$asset" | build/check_certificates 10000001 20000000 0 \
    > logs/certificate-check-full-range.log
python3 -B prepare_gaps.py > logs/gap-preparation.log
for k in 3 4 5 6 7; do
    build/enumerator "$k" > "build/enumerator-$k.solutions" 2>> logs/enumerator.log
done
python3 -B controls.py 8 > logs/controls.log 2> logs/controls.stderr
pgrep -f math_e293gaps_1123 | wc -l || true
python3 -B run_gaps.py math_e293gaps_1123 --workers 8 > logs/gap-driver.log 2>&1
~~~

The runner records per-candidate manifests, measured pilots when the pilot did not already find a witness, raw solver rows, and harvested summaries under [logs/](logs/). Additional coverage reached in a four-hour replay will depend on throughput. Solver output mode 0 counts all representations, mode 1 emits all, and mode 2 emits the first per shard. The driver cancels remaining work for a candidate after a checked witness.

To replay the answer's coverage and shard counts from retained records, run the following from the job directory.

~~~bash
python3 -B - <<'PY'
from prepare_gaps import read_check
from run_gaps import Sweep, TARGET

m = 13_878_989
missing, _ = read_check("logs/certificate-check.log")
assert m == min(missing) and missing[m] == 0
assert m - TARGET - 1 == 21_995
s = Sweep(m, 8)
assert set(s.records) == set(s.manifest) and len(s.records) == 1_412
assert all(not cert and row[2] == row[4] == 0 for _, row, cert in s.records.values())
assert sum(row[6] for _, row, _ in s.records.values()) == sum(s.leaves.values()) == 76_452_736
assert sum(row[3] for _, row, _ in s.records.values()) == 487_462_597_822
PY
~~~

## Sources and limits

The frozen 2026-11-23 prior-art snapshot credits EconLearn's result and release, ntysdd's certificate searches, and the preceding local exhaustive replay. This job's network scope allowed downloading the pinned release asset and GMP if missing. It precluded a live literature or scoreboard refresh. The workspace exposed no model or effort setting for separate verification. [PRIOR_ART.md](PRIOR_ART.md), [Erdős #293](https://www.erdosproblems.com/293), [public computation thread](https://github.com/teorth/erdosproblems/issues/403), [EconLearn release](https://github.com/EconLearn/erdos293-check/releases/tag/v9-certificates), [A400352](https://oeis.org/A400352), [A006585](https://oeis.org/A006585).

## Verdict checks

- CONTROLS: No. The control log records all ten fixed counts, the 3,263,441 k=6 and 83,263 k=7 direct comparisons, and all six mutant changes. The k=9 control output contains six exact witnesses. The regression replay matched all 1,412 shard records and the earlier 76,472,707 two-term states. [Control log](logs/controls.log), [k=9 positive controls](logs/nearby-controls.tsv), [regression summary](logs/k9-13856993/summary.json).
- CONTRADICTING: No. The release checker validated all 9,999,376 rows and explicitly checked whether any missing label appeared among the raw denominators. The answer replay covered all 76,452,736 two-term states and all 1,412 shard records, with no witness or skip. The harvest checked 58 solver or nearby-control witness records against all reported absences. The original cancellation failure and its witness remain in [the failed attempt](logs/initial-k9-13878988/).
- LABELS: No. The release checker compared each printed label with its nine parsed integer denominators before using it for coverage. The harvest replay checked the m and k in each shard record against its task and counted leaves from exact rational bounds. Each of the 58 witness rows used in this verdict was checked by exact reciprocal sum and by membership in its parsed denominators. [Certificate checker](check_certificates.c), [exact shard replay](run_gaps.py).

The next verification step is human inspection of the proof and a replay of the first exhaustive zero.

The driver exited and its tracked workers were reaped.
