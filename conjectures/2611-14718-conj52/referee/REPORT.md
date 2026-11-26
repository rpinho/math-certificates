Shipped: Independent confirmation that Conjecture 5.2 first fails at 15 vertices, with exactly three counterexamples up to isomorphism, and a correction to the tree certificate.
VERDICT: HOLDS WITH CAVEATS
RESULT: yes

All three graphs have maximum degree three and violate the required CDF order at 6. The sequential probability is 64/3375 and the uniform maximal-independent-set probability is 1/55, a difference of 29/37125. The independent census found zero violations among 358,891 connected subcubic graphs through order 14 and exactly three among 1,016,740 at order 15. The paper's component corollary excludes disconnected counterexamples at these orders. A second exact calculation matched the full distributions in all 4,604,216 supported size bins. [Full referee verdict](REFEREE.md) · [Census](census.txt) · [Class-by-class replay](census_replay.txt)

| Witness | Verified conclusion |
|---|---|
| CE#1, 14-edge tree | The CDFs cross at thresholds 6 and 7. All 15 vertex deletions and all 14 edge deletions restore the conjectured order. |
| CE#2, girth-five unicyclic graph | Static strictly dominates sequential globally. Deleting edge (0,1) gives CE#1. |
| CE#3, triangle-containing unicyclic graph | Static strictly dominates sequential globally. All 15 vertex deletions and all 15 edge deletions restore the conjectured order. |

Both unicyclic graphs have support {6,7} and static mean 384/55 versus sequential mean 23561/3375. The infinite tree family also works for every m ≥ 3. At m = 4 the direct 20-vertex calculation gives 256/50625 > 1/229. [Full laws, deletions and family checks](verification.json)

**Corrections.** The submitted tree PMF sums to 3378439/3378375. Its mass at 7 should be **7993019/10135125**. A direct integration over arrival times gives the same correction as the two finite-graph evaluations. The tree is the unique sparsest order-15 witness, but CE#3 also satisfies vertex- and edge-deletion minimality. The exact tree recurrence gives a probability-ratio growth factor of about 1.10740. The referee note also corrects the ring growth estimate, qualifies the statement about pendant-path multiplicities, and identifies an induced claw in a 2-by-3 ladder. [Derivations and other findings](REFEREE.md)

**Did you find something new? No.** The three constructions and the disproof are the producer's. This audit independently reproduced the sharp classification, corrected an exact probability and identified the second deletion-minimal graph. Priority beyond the supplied paper and report was outside the source restrictions. No statistical holdout applies to exact inequalities on a specified finite class. The producer's larger simulated-annealing trajectories and its order-22 cubic near-miss graph were unavailable. [Prior art](PRIOR_ART.md) · [Verbatim primary source](PRIMARY_SOURCE.md)

## Reproduction

Run in the job directory. The witness verifier uses Python 3.10 or later and its standard library. The full parallel replay uses POSIX fork. The first command reproduces the witness audit using the included census. The remaining commands regenerate the census from the singleton and repeat the audit against its output.

```sh
nice -n 10 python3 -B referee_verify.py --census census.txt
nice -n 10 c++ -O3 -std=c++20 -Wall -Wextra referee_census.cpp -o referee_census
nice -n 10 ./referee_census --controls
nice -n 10 ./referee_census 15 3 > census.txt
nice -n 10 python3 -B referee_verify.py --census census.txt > verification.json
```

Strict checking of the submitted tree probabilities can be reproduced with `nice -n 10 python3 -B referee_verify.py --strict-certificate`. Its expected result on the supplied hash is exit 1 at the RSA PMF comparison. Normal audit mode reports both the submitted and corrected values.

An initial Python pass recomputing every graph from scratch was stopped when its observed throughput would exceed the wall-clock cap. The completed class-by-class comparison used a temporary row stream. The C++ program identifies the connected components left by each possible first choice. Python enumerates the static sets afresh and combines the smaller component laws in exact fractions. Every component used in an equation has lower order, so verifying all rows establishes all the equations from the empty graph upward. This comparison shares the census generator and its exact graph keys. The individual witness verifier takes only raw edges for its probability calculations. The completed comparison used a 287 MB temporary stream and four workers for about ten minutes. [Replay output](census_replay.txt)

```sh
rows=$(mktemp "$PWD/.referee_rows.XXXXXX")
nice -n 10 ./referee_census --stream 15 > "$rows"
nice -n 10 python3 -B referee_replay.py "$rows" --workers 4 --seconds 1500
rm "$rows"
```

**CONTROLS:** No assumption overrode the controls. All 5,796 permutations on the five named graphs agreed with the Python laws. The paper's degree-four graph gives 5/24 > 1/5 and fails the subcubic guard. [Control output](verification.json)

**CONTRADICTING:** No contradictory result in the permitted evidence was discarded. The tree crosses back at 7, strict certificate validation fails, and 1 of 89 single deletions retains a violation. The census has 3 positive graphs out of 1,375,631. [Full results](verification.json) · [Census](census.txt)

**LABELS:** No witness claim was accepted on its label. The verifier used the raw edges to recompute topology and both laws and constructed edge-preserving bijections for all three census hits. It rejected the incorrect mass in the supplied file and all seven deliberate mutations. [Verifier](referee_verify.py) · [Computed evidence](verification.json)

The next editorial step is to correct the stored PMF and minimality wording in a new producer revision. The regular-cubic and minimum-degree-two variants remain open here. All work stayed local.

This is AI work. No human has checked it.
