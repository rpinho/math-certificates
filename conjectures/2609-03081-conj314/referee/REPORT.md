Shipped: Lewis and Won's Conjecture 3.14 is false. At order 17 the supplied permutation beats every proposed shape by exactly 1,016,659,381,068 complete rook placements.

VERDICT: HOLDS WITH CAVEATS

RESULT: yes

| Order | Witness shape | Witness placements | Proposed family maximum | Excess |
|---:|---|---:|---:|---:|
| 17 | (5, 3, 1, 3, 5) | 104,476,798,194,769 | 103,460,138,813,701 | **1,016,659,381,068** |
| 18 | (5, 3, 1, 1, 3, 5) | 2,949,333,362,474,113 | 2,445,624,351,454,501 | **503,709,011,019,612** |

The order-17 permutation is **(5, 4, 3, 2, 1, 8, 7, 6, 9, 12, 11, 10, 17, 16, 15, 14, 13)**. Its grid has 32 across words and 32 down words. A matching recurrence and Ryser inclusion–exclusion gave the same exact permanent. Separately, the referee note derives the witness count as a sum of seven integer squares. All 136 ordered positive endpoint pairs at 17 agree with Proposition 3.15 when counted from their grids. The sole best pair is (5, 5). The source statement only asks for one maximizing grid of the proposed shape, and the strict inequality rules that out. [Referee note and source excerpts](REFEREE.md) · [Raw results](verification.txt)

**Why the caveats apply.** Thirteen certificate fields match their primary-source or arithmetic checks. The fourteenth, `minimality_note`, mixes mathematical comparisons with claims about the producer's search history. Its “>300,000” language needs a unit and a per-order or pooled interpretation. The report lists 264k SA at 15 and 290k SA at 16. The report also places the conjecture at TeX line 759 instead of 754, describes four moved diagonal black squares as six, and calls all 136 pairs asymmetric although eight have equal endpoints. [Submitted certificate](inputs/witness.json) · [Submitted report, sections 1 and 5](inputs/REPORT.md)

**Did this referee find something new? No.** The producer supplied the counterexample. This replay establishes that it settles the universal statement printed in v1. External priority is unassessed under the three-input clean-room restriction. There is no statistical holdout or predictive baseline in an exact finite counting certificate. The small-grid census and the formula serve as arithmetic controls. [Prior art and reproduction](PRIOR_ART.md)

## Reproduce the certificate

From this job directory, run the following with Python 3 on macOS. All verification code was written from the supplied definitions and uses standard-library integer arithmetic. It creates no subprocesses.

```sh
nice -n 10 python3 -B -u referee_verify.py
```

The default command runs the positive controls first, compares the endpoint families, checks the witnesses and their metadata, and exercises the five mutations. The input evidence is the supplied [Lewis–Won v1 source](inputs/2609.03081v1.tex.json.gz), [producer report](inputs/REPORT.md) and [witness](inputs/witness.json). [Verifier](referee_verify.py)

## Census scope and limitations

The independent census recovered the producer's five claimed global maxima at orders 10 through 14. In increasing order they are **255,569**, **3,316,625**, **46,301,969**, **680,707,985** and **10,353,226,769**. The order-14 proof covers 87,178,291,200 permutations by bounding classes of row orders. At orders 15 and 16 the exhaustive layered and bounded-middle searches give **202,352,501,701** and **4,493,953,750,501** respectively. Those two results cover restricted families. Whether 17 is the smallest counterexample order remains open in this audit. The producer's randomized trajectories, code, timings and Conjecture 3.9 census were outside the replay. [Order-14 transcript](census/order14.txt) · [Restricted-family counts and proofs](REFEREE.md#scope-of-the-minimality-note)

The remaining numerical ambiguity in the producer's note can be resolved by identifying the units and per-order counts of the randomized search. The report's “Best Non-… Found” column also needs a symmetry convention. At order 10 a column reflection gives a non-layered grid with the full maximum 255,569, exceeding the displayed alternative 226,409. [Reflected permutation](verification.txt)

The supplemental census commands are independent and can be run sequentially.

```sh
nice -n 10 python3 -B -u referee_verify.py --census 9 10 11
nice -n 10 python3 -B -u referee_verify.py --halves 8 10 12
nice -n 10 python3 -B -u referee_verify.py --bounded 8 10 12 13 14
nice -n 10 python3 -B -u referee_verify.py --layered 15 16
nice -n 10 python3 -B -u referee_verify.py --middle 15 16
nice -n 10 python3 -B -u referee_verify.py --empty-end 15 16
```

The job used at most four nice-10 counting workers on an Apple M5 Pro. The largest recorded process high-water RSS was 73,089,024 bytes. Two attempts to set a Darwin memory limit failed before enumeration. The completed runs used bounded state spaces and recorded kernel high-water marks. [Run checkpoints](STATUS.md) · [Peak-RSS transcript](census/explicit-halves.txt)

## Referee checks

CONTROLS: No assumption overrode a control. Enumeration of all 46,233 small permutations reproduced the eight published maxima, and the separate grid gave 155. The losing swap gave 3,697,126,675,213. All five mutations were rejected. [Verification output](verification.txt)

CONTRADICTING: No contrary result was dropped. All 136 ordered pairs enter the comparison. The discrepancy between the JSON's “>300,000” and the table's 264k and 290k, and the order-10 reflected maximizer, are recorded above. [Submitted note](inputs/witness.json) · [Submitted table](inputs/REPORT.md) · [Independent counts](verification.txt)

LABELS: No unchecked annotation was used to decide the result. The verifier counted TeX environments to obtain 3.14 and 3.15, reconstructed the shape from the raw permutation, and counted the grid by matching and inclusion–exclusion. A third calculation scanned the black columns directly. [Verifier](referee_verify.py) · [Verbatim source audit](REFEREE.md#appendix-primary-source-definitions-and-statements)

This is AI work. No human has checked it.
