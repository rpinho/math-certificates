# Erdős problem #1110 (7,2) replay

I audited Jean-Roch Bécart’s positive lower density claim for the integers representable by an antichain of powers of 7 and 2. Bécart developed the claim with Claude Opus 5.5. I used the written argument and potential table from the pinned revision `f26cb9a2`. This was AI work by GPT-6.2 Sol via Codex. I did not read or run the claimant’s code. No human has checked this replay. I claim no new result. [Erdős Problems #1110](https://www.erdosproblems.com/1110), [pinned argument](https://github.com/Jrbecart-uo/erdos-1110-72/blob/f26cb9a2506fef170b110b6226fe294d1b9d04e8/README.md), [prior art](replay/PRIOR_ART.md).

## Verdicts

- **Theorem A · HOLDS in AI review.** I audited the reduction from the finite drift inequality to positive lower density. The least power of two in any nonempty chain forces the empty chain in residue zero. Applying the inequality at a global minimum of the potential supplies the implicit nonnegative drift allowance used in the exponential moment argument. [Lemma audit](replay/LEMMAS.md).
- **Theorem B · HOLDS.** I reproduced the exact maximum drift numerator of **8,385,274,094**, uniquely attained at **(1835, 623)**. The C sweep evaluated all **4,194,304 states**, each with **2,048 look-aheads**. The run took **23.21 seconds on 6 threads**. [Sweep](replay/logs/full_cb_away.json), [timing](replay/logs/full_cb_away.time), [comparison to the claim](replay/logs/claim.json).
- **Lean · unverified.** I left [E1110.lean](https://github.com/Jrbecart-uo/erdos-1110-72/blob/f26cb9a2506fef170b110b6226fe294d1b9d04e8/lean/E1110.lean) and the correspondence of its `Cert` with the replayed inequality outside scope.

I wrote the C and Python implementations separately as one agent. This gives an implementation cross-check without an independent review. The C verifier exhausts the fixed finite inequality using integer arithmetic after rounding the input. The Python reference evaluates transitions directly with arbitrary-precision integers. A statistical holdout does not apply to a universal finite inequality. [C verifier](replay/e1110_verify.c), [Python reference](replay/reference.py).

## Certificate checks

I obtained the same **70,701 chains** by depth-first enumeration in C and by pairing equal-size subsets in Python. The canonical lists agree byte for byte and cover every residue. C and Python agree on **32,256 synthetic state comparisons** and **675 real state comparisons**, including the recorded sweep winners. The synthetic comparison is exhaustive for every tested layout and rounding rule. [Reference comparisons](replay/logs/reference.json).

The source table has **6,659 exact half-integer ties** after scaling, all positive. With the claimed storage layout `c*P+b`, half-even rounding changes 3,963 entries and still passes at 8,385,274,062. Rounding by flooring the scaled value plus one half gives the same table as half-away. The transposed `b*P+c` layout fails for every tested rounding rule. [Rounding and table digests](replay/logs/reference.json).

| Rounding | Claimed layout maximum | Transposed layout maximum |
| --- | ---: | ---: |
| Half-away from zero | [8,385,274,094](replay/logs/full_cb_away.json) | [22,313,851,226](replay/logs/full_bc_away.json) |
| Half-even | [8,385,274,062](replay/logs/full_cb_even.json) | [22,313,851,088](replay/logs/full_bc_even.json) |
| Floor after adding one half | [8,385,274,094](replay/logs/full_cb_up.json) | [22,313,851,226](replay/logs/full_bc_up.json) |

The two integer comparisons put the canonical drift strictly below the threshold for Theorem A. [Exact comparisons](replay/logs/controls.json).

```text
73 * 8,385,274,094 = 612,125,008,862 < 614,180,323,328 = 286 * 2^31
7^26 = 9,387,480,337,647,754,305,649 < 9,444,732,965,739,290,427,392 = 2^73
```

## Controls and encoder

I checked five structural refusals. Each returned exit 1. The mutation and height rows give full sweep maxima. The table edits give pointwise witnesses at the canonical maximizer. [Full control matrix](replay/logs/controls.json).

| Control | Outcome |
| --- | --- |
| Drop the empty chain | Refused for uncovered residue zero |
| File a chain under the wrong residue | Refused for chain residue mismatch |
| Add a chain of height 11 | Refused for height above the cap |
| Insert a non-chain | Refused for failure of pair ordering |
| Repeat an alpha coordinate | Refused for duplicate alpha |
| Edit potential by −1,000 | Predicted and observed drift increase 2,048,000. Witness 8,387,322,094 passes. |
| Edit potential by −13,748 | Predicted and observed drift increase 28,155,904. Witness 8,413,429,998 fails. |
| Edit potential by −20,000 | Predicted and observed drift increase 40,960,000. Witness 8,426,234,094 fails. |
| Reduce transition chain value modulo P | 19,796,008,763 at (1574, 1819). Fails. |
| Use the last gamma in the transition multiplier | 10,525,832,334 at (1453, 284). Fails. |
| Use positive gamma in the chain value | 21,167,844,332 at (1087, 710). Fails. |
| Use minimal height +2 | 12,511,354,588 at (74, 601). Fails. |
| Use minimal height +4 | 8,385,245,846 at (821, 1699). Passes for this altered family. |
| Test the false comparison `7^26 < 2^72` | Rejected by exact integer powers. |

At `s=3`, I enumerated all 4,096 inputs for each of four policies and checked strict antichains, reconstruction, the strict size condition, conditional uniformity, and injectivity on the admissible inputs. The policies admitted 531, 33, 125 and 142 inputs respectively, including zero. The log retains 15,553 inadmissible policy/input pairs. At `s=11`, each of `N=10` and `N=20` admitted all 256 seeded random inputs and the explicit zero, and all 257 outputs per run passed the exact encoder checks. These counts describe the sampled cases. The density implication comes from Theorem A. [Encoder results](replay/logs/encoder.json).

## Replay

The replay runs on macOS with clang, xz and Python 3.10 or newer. The download commands use curl. The commands below run in a new sibling directory, keeping the captured packet logs intact. The pinned public README and compressed table are the external inputs. The four digests cover those two files and the two derived tables. [Input manifest](replay/INPUTS.sha256), [file provenance](PACKAGING.md).

```sh
set -eu
packet_dir="$(pwd)"
run_dir="$(mktemp -d "$(dirname "$packet_dir")/e1110-run.XXXXXXXX")"
cp "$packet_dir"/replay/*.py "$packet_dir"/replay/e1110_verify.c \
   "$packet_dir"/replay/INPUTS.sha256 "$run_dir"/
cd "$run_dir"
mkdir -p inputs logs
origin='https://raw.githubusercontent.com/Jrbecart-uo/erdos-1110-72/f26cb9a2506fef170b110b6226fe294d1b9d04e8'
curl -fsSL "$origin/README.md" -o inputs/README.md
curl -fsSL "$origin/certificate/V_s11_it8.bin.xz" -o inputs/V_s11_it8.bin.xz
nice -n 10 xz -dc inputs/V_s11_it8.bin.xz > replay_table.f32
sed -e '/^#/d' -e '/  V_hat\.i64le$/d' INPUTS.sha256 | shasum -a 256 -c
nice -n 10 cc -std=c11 -O3 -Wall -Wextra -Werror -pthread \
  -o e1110_verify e1110_verify.c -lm
job_deadline=$(( $(date +%s) + 7800 ))
for layout in cb bc; do
  for rounding in away even up; do
    tag="${layout}_${rounding}"
    nice -n 10 /usr/bin/time -l ./e1110_verify full 11 10 3 standard \
      replay_table.f32 "$layout" "$rounding" 6 "$job_deadline" \
      > "logs/full_$tag.json" 2> "logs/full_$tag.time"
  done
done
for rule in low-value last-gamma positive-gamma; do
  nice -n 10 /usr/bin/time -l ./e1110_verify full 11 10 3 "$rule" \
    replay_table.f32 cb away 6 "$job_deadline" \
    > "logs/full_$rule.json" 2> "logs/full_$rule.time"
done
for window in 2 4; do
  nice -n 10 /usr/bin/time -l ./e1110_verify full 11 10 "$window" standard \
    replay_table.f32 cb away 6 "$job_deadline" \
    > "logs/full_window$window.json" 2> "logs/full_window$window.time"
done
nice -n 10 python3 -B compare_claim.py
nice -n 10 /usr/bin/time -l python3 -B replay_checks.py --deadline "$job_deadline" 2> logs/reference.time
nice -n 10 /usr/bin/time -l python3 -B encoder.py --deadline "$job_deadline" 2> logs/encoder.time
shasum -a 256 -c INPUTS.sha256
```

I credit J.-R. Bécart with Claude Opus 5.5 for the proof, two-block construction and potential table, P. Erdős and M. Lewin for the problem, W.-X. Yu and Y.-G. Chen for the zero-density results, and Ding, Li, Liu and Zhang for the earlier single-block certificate for (5,2). [Credits and sources](CREDITS.md).
