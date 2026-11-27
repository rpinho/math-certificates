RESULT: yes
Shipped: a referee verdict on WITNESSES.tsv: all 50 Def. 3.4 witness pairs check out, so every one of the 49 refuted p.27 tuples in Liang arXiv:2608.13273v2 is refuted. 0 of 177 rows were rejected; 24 template rows are unclear because they rely on the caption's "starting from size 1".

This is AI work (claude-opus-5-5, clean-room referee). No human has checked it.

## Did we find something new?
No, not on our part. This job checks someone else's refutations. Our solver confirms them independently.

## Definitions used
See DEFINITIONS.md for the verbatim quotes and the reading each row type needs. In brief:
- standard octal move rules (§3.2);
- misère convention: terminal positions are N (Def. 2.2);
- grouped-digit shorthand ˙d = d,d+1; ¨d = d,d+2; ¯d = d..d+3 (§3.5.2), which expands the 25 table entries to 55 codes;
- Def. 3.4: for sorted u with a1 ≥ p1+t1, o−(u) equals o−(a1−t1, a2, …) when a2 < p2+t2, and equals o−(a1−t2, a2−t2, a3, …) otherwise.

The tuples were taken from the p.27 table (inputs/sources/page27.png). They agree with the text extraction.

## Solver
`referee_solver.py`:
- exact outcomes by memoised DFS over sorted multisets of nonzero heaps, under misère or normal play;
- handles impartial or partizan codes (labelled reduction of §3.2).

`naive_solver.py` is a second, deliberately naive recursion over unsorted options. In `check_witnesses.py` it is asserted to agree on every witness position: 177 rows, 0 disagreements. On 5,103 three-heap positions across 7 codes it also agreed with the main solver (0 mismatches).

## Controls (`python3 controls.py` → ALL CONTROLS PASS)
| control | source | result |
|---|---|---|
| 0.26: H13+H17+H31 is a misère P-position | Plambeck–Siegel 0609825, footnote 5 | PASS (P) |
| 0.3122: o(2,2,h,h)=P and o(2,2,h+1,h)=N for h ≤ 60 | 2611.29198 Thm 3.7 | PASS, 0 violations |
| 0.3123: o(3,3,h,h)=P and o(3,3,h+1,h)=N for h ≤ 60 | 2611.29198 Thm 3.8 | PASS, 0 violations |
| 0.04:0.03 class outcomes (L;)P, (L;2)P, (L;4)N, (R;)P, (R;2)N | 2608v2 §3.5.1 | PASS |
| 16 printed 0.04:0.03 equivalences, each tested against 165 suffixes | 2608v2 §3.5.1 | PASS, 0 violations |
| printed p.28 rows for 0.2˙6¯0 (8 codes) and 4.¨0˙6 (4 codes) | 2608v2 p.28 | exact over all 35 entries if read from size 0 (`controls_crossmatch.py`) |
| printed rows under the labels 0.337, 0.73˙2 and 0.73˙4 | 2608v2 p.28 | exactly equal the true rows of 0.72¯4, 0.32˙6 and 0.73˙2 respectively |
| 0.73˙4 printed row | 2608v2 p.28 | 1/35 mismatch, at size 4. There the paper's own Pout formula agrees with us (4 is P) |

**Caveat on the p.28 table.** Read as the caption says (misère, from size 1), most printed rows disagree with the true rows (`controls_rows.py`). I tried 6 bit-meaning permutations × misère/normal × start 0/1 (`controls_convention_probe.py`). No alternative convention explains the rows; the standard reading scores best. Several printed rows equal another code's true row exactly. My conclusion is that the p.28 table is mislabelled or garbled in the paper, and that my reading is not at fault. This caveat affects only the template rows. The p.27 tuple checks do not depend on p.28.

## Per-game table (generated from witness_results.json)
| game | Def 3.4 / 4.2 rows (tuple claim) | template / formula / conjecture rows | rows confirmed | rejected | unclear (offset) | not a refutation |
|---|---|---|---|---|---|---|
| 0.157 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.175 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.260 | 1 (refuted) | 2 | 1 | 0 | 2 | 0 |
| 0.261 | 1 (refuted) | 2 | 1 | 0 | 2 | 0 |
| 0.262 | 1 (refuted) | 2 | 1 | 0 | 2 | 0 |
| 0.263 | 1 (refuted) | 2 | 1 | 0 | 2 | 0 |
| 0.270 | 1 (refuted) | 2 | 1 | 0 | 2 | 0 |
| 0.271 | 1 (refuted) | 2 | 1 | 0 | 2 | 0 |
| 0.272 | 1 (refuted) | 2 | 1 | 0 | 2 | 0 |
| 0.273 | 1 (refuted) | 2 | 1 | 0 | 2 | 0 |
| 0.326 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.327 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.337 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.355 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.357 | 2 (refuted) | 2 | 4 | 0 | 0 | 0 |
| 0.512 | 0 (-) | 2 | 2 | 0 | 0 | 0 |
| 0.513 | 0 (-) | 2 | 2 | 0 | 0 | 0 |
| 0.516 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.517 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.534 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.535 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.552 | 0 (-) | 2 | 2 | 0 | 0 | 0 |
| 0.553 | 0 (-) | 2 | 2 | 0 | 0 | 0 |
| 0.556 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.557 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.570 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.571 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.574 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.575 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.716 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.717 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.724 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.725 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.726 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.727 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.732 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.733 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.734 | 0 (-) | 3 | 3 | 0 | 0 | 0 |
| 0.735 | 0 (-) | 3 | 3 | 0 | 0 | 0 |
| 0.736 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.737 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.754 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.755 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.756 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.757 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 4.06 | 1 (refuted) | 2 | 1 | 0 | 2 | 0 |
| 4.07 | 1 (refuted) | 2 | 1 | 0 | 2 | 0 |
| 4.26 | 1 (refuted) | 2 | 1 | 0 | 2 | 0 |
| 4.27 | 1 (refuted) | 2 | 1 | 0 | 2 | 0 |
| 4.16 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 4.17 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 4.52 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 4.53 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 4.70 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 4.71 | 1 (refuted) | 2 | 3 | 0 | 0 | 0 |
| 0.3102 | 2 (refuted) | 1 | 2 | 0 | 0 | 1 |
| 0.3122 | 0 (-) | 10 | 9 | 0 | 0 | 1 |
| 0.3123 | 0 (-) | 1 | 0 | 0 | 0 | 1 |
| 0.3312 | 0 (-) | 1 | 0 | 0 | 0 | 1 |
| **total** | 52 | | 149 | 0 | 24 | 4 |

Distinct 2608v2 codes whose p.27 tuple is refuted by a confirmed Def. 3.4 witness: 49

Row counts (177 total):
- **Def. 3.4 (50 rows, 49 codes):** 47 branch-2 and 3 branch-1 rows; all 50 confirmed. In each, a1 ≥ p1+t1 holds, the branch is the one the row names, the reduct equals the partner position, and the outcomes are P vs N. 0.357 has one witness for each branch.
- **p.28 template (108 rows):** 84 confirmed, meaning the printed letter (read from size 1) differs from the true outcome. 24 are unclear (see below).
- **0.73˙4 explicit P formula (4 rows):** 4 confirmed. (2,2) is P but the formula says N; (3,1) is N but the formula says P.
- **2611.29198 rows:**
  - Definition 4.2 branch 2, 0.3102 with tuple (46,5,12,5): 2 confirmed.
  - Conjecture 4.1 residue key, 0.3122: 9 confirmed.
  - Fixed-heap folding: 4 rows that are not refutations.
- **Rejected:** 0.

## Rows not confirmed, with reasons
- **24 UNCLEAR-OFFSET rows** (the 2 template rows for each of 0.260–0.263, 0.270–0.273, 4.06, 4.07, 4.26, 4.27). They are wrong only if the row is read from size 1, as the caption says. Read from size 0, the whole printed row is exactly right (it begins with N, and the empty position is N in misère). This is a one-place offset in the caption, not a false outcome claim. I do not count these rows as refutations.
- **4 NOT-A-REFUTATION rows** ("fixed heap folding": 0.3102, 0.3122, 0.3123, 0.3312). 2611.29198 Conjecture 4.4 says folding *fails*, so the exhibited inequalities agree with the paper.

## Scope notes
- The 2611.29198 rows (15) are outside the job's "rules printed in 2608.13273v2". I checked them but they do not enter the verdict.
- The Conjecture 4.1 residue rows use small x, y, for example (2,2,3,0). The conjecture as printed ("depends only on …") has no size threshold, so they refute it literally. A reader who assumes an implicit preperiod could dispute this.
- The 0.73˙4 formula is mostly right. It agrees with the solver on 1,794 of 1,819 positions (≤4 heaps, each ≤12). The 25 failures follow a pattern (mostly Δ(u)=2, plus (2,2) and (1,1,2,2)), so the inner/outer boundary looks off by one.

## Rubric
- **CONTROLS:** No assumption overrode the controls. All 5 independent control groups pass (`python3 controls.py`). The p.28 rows disagree with the solver, and I did not explain that away with an assumption. I tested 24 alternative conventions (`controls_convention_probe.py`) and none fits. I found exact row matches under other labels (`controls_crossmatch.py`), which points to the paper's table rather than my reading. The p.27 tuple verdicts do not use p.28 at all.
- **CONTRADICTING:** Nothing that contradicts the conclusion was dropped. Three groups of rows cut against "every claimed refutation stands", and all are reported above:
  - 24 rows are fully correct under the size-0 reading. They are counted as unclear, not confirmed (`grep -c UNCLEAR witness_results.txt` → 24).
  - 4 folding rows agree with the paper.
  - The 0.73˙4 formula holds on 1,794/1,819 positions (`controls.py` INFO lines).
- **LABELS:** No label was trusted without a check against the raw data.
  - Every "printed X" label in WITNESSES.tsv was compared with the paper text: 216/216 agree.
  - Every tuple and branch label was recomputed from page27.png. The P/N labels were recomputed by two solvers (`check_witnesses.py`; 0 disagreements).
  - The producer's code was not seen.

## Reproduce
```
cd ~/dev/open-science/math_wave_1030/misere_ref
python3 check_witnesses.py > witness_results.txt   # ~30 s; also writes witness_results.json
python3 controls.py                                # ~5 s
python3 controls_rows.py; python3 controls_crossmatch.py; python3 controls_convention_probe.py
python3 referee_solver.py 0.157 28,7,4,4 25,4,4,4   # single check
```

## Limitations and next steps
- The verdict rests on exact search with no sampling, so no statistical holdout applies. It is still one AI-written solver plus one naive cross-check, written by the same author.
- I did not re-derive the true (preperiod, period) of each single-heap row; a run to heap 150 was too slow and I stopped it.
- I could not render p.28 of the PDF (no poppler), so the table text comes from the supplied .txt extraction only.
- Next: a human look at the p.28 PDF to settle whether the rows are mislabelled, and a check of 2608v1 for the same table.

VERDICT: HOLDS
