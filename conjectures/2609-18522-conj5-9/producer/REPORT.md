Shipped: exact counterexamples to the period formula in Conjecture 5 and the preperiod formula in Conjecture 9 of van Berkel & Bosma, arXiv:2609.18522v1.

RESULT: yes

| Claim in v1 | Seed | Formula | Certified minimal lengths and modulus | Five-block cutoff |
|---|---|---:|---|---:|
| Conjecture 5, period | $S_{4,11}$, $d=7$ | $p=9$ | $k=11, p=10, m=33$ | 495 |
| Conjecture 9, preperiod | $S_{5,10}$, $d=5$ | $k=7$ | $k=6, p=6, m=24$ | 240 |

**Did the search settle a stated conjecture? Yes.** Both sequences are ultimately periodic. The counterexamples settle the two printed length equalities in the negative. The paper's tables already contain both correct lengths, and its diagonal theorem gives the second length. The contribution here is the demonstrated contradiction between the formulas and the sequences, with replayable certificates. The broader periodicity conjecture remains open. The arXiv history listed v1 when checked on 26 November 2026 UTC. Priority for observing these discrepancies is unverified. [Paper and version history](https://arxiv.org/abs/2609.18522) · [Prior art](PRIOR_ART.md)

## Two certificates

**Period.** In Definition 3, $f=4$ gives both half-size parameters 2. The first block has index 1, and $d=7=4+2+1+0$ selects clause (4) with $j=0$. Line 300 gives $1(4+1+2)+2+1=10$. Lines 301–302 require subtraction of 1 because $f\le4$ and $d=2\cdot1\cdot4-1$. The small-$f$ exceptions on lines 336–341 leave the prediction at 9. The actual repeating gap word is $(1,6,1,1,7,1,7,1,7,1)$. Its unique 6 forces period 10. Its last gap is 1 and the immediately preceding transient gap is $37-29=8$, which fixes the onset after 11 gaps.

**Preperiod.** In Definition 8, $f=d=r=5$ and $h=0$. Clause (d), line 526, gives $5f-3=22$. Clause (k₀), line 565, subtracts $2f+r=15$, giving 7. The sequence begins $5,10,11,12,13,14,20$. Starting at 20 the gaps repeat $(8,1,6,1,1,7)$. The unique 8 forces period 6, and the preceding gap $20-14=6$ differs from the cyclic predecessor 7. There are exactly six transient gaps. [Verbatim definitions](definitions.tex) · [Certificate with both words and source lines](witness.json)

**Finite proof.** Theorem 15, TeX lines 958–966, uses the first $5M$ characteristic bits, indexed from 1. Blocks two through five must be identical and nonempty. Its proof propagates their repetition indefinitely. The independent verifier generates the bits by adding only sums with previously accepted, distinct terms. For $M=99$ it finds 30 ones in each repeated block. For $M=48$ it finds 12. Each proposed infinite word agrees with the raw prefix and already repeats with shift $M$ on those blocks. The legacy field `M_thm13` in the harvest denotes $M$ for this same theorem. [Authors' criterion](https://arxiv.org/html/2609.18522v1#S4)

**Independent generating-function proof.** For finite head polynomial $P$ and first tail-block polynomial $B$, set $N=(1-z^m)P+B$, so $A=N/(1-z^m)$. Twice the number of unordered representations by distinct members has generating series $A(z)^2-A(z^2)$. Over denominator $(1-z^{2m})^2$, its numerator is

$$
H=N(z)^2(1+z^m)^2-N(z^2)(1-z^{2m}).
$$

Beyond the degree of $H$, the coefficients on each residue modulo $2m$ are affine. The verifier checks every initial coefficient, exact parity, and the affine slope on every residue. For each $n>g$ it proves zero representations for members and positive counts forever for nonmembers. Positivity of the terms makes every representing pair smaller than its sum, so this condition with the given seeds determines the greedy sequence. The affine checks begin at degrees 205 and 125, with strides 66 and 48 respectively. This proof uses no periodicity theorem. [Zero-dependency Python verifier](verify_counterexample.py)

## Grid and neighborhoods

All **4,800** requested seeds were certified, including each $1\le f\le6, 1\le d\le200$ and $7\le f\le30, 1\le d\le150$. The C++ search proposes a period from the differences and verifies the repeated characteristic blocks. An independent Python replay receives just the seed and block size for its recovery algorithm. It regenerates the set, checks all four blocks, computes the primitive cyclic gap word by its prefix function, and extends the period backward gap by gap. It recovered every reported $(k,p,m)$. On the primary grid, the largest required $5M$ was **192,990** at $(3,197)$. The C++ engine actually generated through integer 193,118 there.

| Quantity | Unique formula agrees | Unique formula disagrees | Overlapping clauses |
|---|---:|---:|---:|
| Minimal period $p$ | 4,799 | 1 | 0 |
| Minimal preperiod $k$ | 3,152 | 1,645 | 3 |

There are **1,646 distinct seeds** with an unambiguous contradiction. For Definition 3 the block size $2f$ on lines 294–295 selects the block before applying the formulas and the corrections at named indices. For Definition 8 the representative is $1\le r\le2f$. Both applicable values at $(f,d)=(2,2),(2,6),(2,10)$ were retained. The individual clauses give $2,5,7$, the overlapping $5h+11$ clause gives $11,16,21$, and the certified values are $2,5,7$. The three overlap cases are excluded from the 1,645.

The period failure is isolated within the search. All eight immediate neighbors of $(4,7)$ and the other 24 members of $d=8b-1, 1\le b\le25$ at $f=4$ agree on $p$. For all 1,646 discrepant seeds together, the union of their closed radius-one neighborhoods in the positive grid comprises 3,276 pairs, including 120 outside the requested rectangles. We certified a full 231-pair outer border containing those 120. On that border there were zero additional period discrepancies and 85 preperiod discrepancies. The independent replay covered 5,138 distinct pairs including the border and supplemental printed examples. [Grid records](replay_grid.jsonl) · [Border records](halo.txt)

**Two infinite preperiod failures.**

- For every $f=d\ge5$, clauses (d) and (k₀) give $5f-3-(2f+f)=2f-3$. The authors' Theorem 14 proves $k=f+1$, a difference of $f-4>0$. Its tail runs from $4f$ through $8f-3$ in each copy, translated by $5f-1$. Its wrap gap is $f+2$, while the gap into the first copy is $4f-(3f-1)=f+1$. This establishes the family for arbitrarily large $f$, independently of finite-grid extrapolation. [Theorem 14](https://arxiv.org/html/2609.18522v1#S4)
- At fixed $f=8, r=11, d=11+16h$, clause (h₂) has $q=4, s=-1$. For every odd $h\ge3$, lines 539–541 give $43h^2/2+39h+12$, a half-integer. None of the small-$h$ corrections applies. A preperiod length is an integer. At $h=3, d=59$, the conjecture gives $645/2$ and the certified $k$ is 265. This is a fixed residue class $d\equiv27\pmod{32}$ with infinitely many impossible predictions. Over the whole primary grid the formula returned 113 half-integers and 505 negative values.

## Printed controls

The 1,845 displayed period and preperiod array entries all equal the certified sequence values. Some seeds appear in multiple displays. The final column counts displayed values that disagree with every applicable formula clause.

| TeX display | Entries | Match raw sequence | Disagree with formula |
|---|---:|---:|---:|
| $20\times20$ preperiod matrix, lines 178–197 | 400 | 400 | 115 |
| $20\times20$ period matrix, lines 207–226 | 400 | 400 | 1 |
| Six 25-entry period rows, lines 412–417 | 150 | 150 | 1 |
| Six 25-entry preperiod rows, lines 718–735 | 150 | 150 | 27 |
| $f=19$ period arrays | 170 | 170 | 0 |
| $f=12$ period arrays | 107 | 107 | 0 |
| $f=9$ preperiod array | 234 | 234 | 87 |
| Same $f=9$ values printed by residue | 234 | 234 | 87 |

The worked $f=19,12$ ranges reproduce all 153 positions after the expressly stated corrections. All 18 slope annotations for $f=9$ agree with the last six observed first or second differences, including the alternating pair. The six numerical sequence prefixes, three gap lists, and modular example at line 117 also reproduce. The $S_{3,7}$ characteristic prefix at line 100 has seven incorrect bits among 64, first at integer 46 (printed 0, actual 1). Its separate barred characteristic word at line 105 gives the correct first 25 bits. [Regenerated arrays and positional discrepancies](printed_arrays.txt)

Example 18 prints $k=17{,}341$ for $S_{3,248}$. Both the greedy sequence and Definition 8 give **17,340**, with $p=2$. It also assigns $(k,p)=(71{,}709,2)$ to $S_{3,497}$, whose certified pair is **(505,251)**. The printed numbers are obtained with $d=497$, giving $S_{3,500}$. Both $f=332$ examples have the printed period 666. At $S_{12,30}$ the printed $(36,19)$ is correct, while Definition 8 gives $k=-23$. The paper's aggregate frequencies across its larger 62,500- and 250,000-seed grids lie outside the requested sweep. [Supplemental certificates](examples.txt)

## Reproduction

From the job directory, the following commands verify the witnesses, print all formula discrepancies, and replay the supplied certificates using only Python's standard library.

```sh
nice -n 10 python3 -B verify_counterexample.py
nice -n 10 python3 -B check_tables.py --mismatches
nice -n 10 python3 -B check_tables.py --arrays
nice -n 10 python3 -B replay_certificates.py --extra halo.txt --extra examples.txt
python3 -B formulas.py
```

To repeat the C++ discovery and all printed comparisons with fresh output paths, use the following commands at the same root.

```sh
pgrep -f csweep_sumfree2 | wc -l
run_dir=$(mktemp -d ./reproduce.XXXXXX)
c++ -std=c++17 -O3 -pthread csweep_engine.cpp -o "$run_dir/sweep"
c++ -std=c++17 -O3 -pthread example_cases.cpp -o "$run_dir/examples"
nice -n 10 "$run_dir/sweep" --threads 3 --strict-grid --out "$run_dir/grid.jsonl"
nice -n 10 "$run_dir/examples" > "$run_dir/examples.txt"
nice -n 10 "$run_dir/examples" --halo > "$run_dir/halo.txt"
nice -n 10 python3 -B check_tables.py --grid "$run_dir/grid.jsonl" --examples "$run_dir/examples.txt" --halo "$run_dir/halo.txt"
nice -n 10 python3 -B replay_certificates.py "$run_dir/grid.jsonl" --extra "$run_dir/halo.txt" --extra "$run_dir/examples.txt"
```

The original suffix heuristic prematurely proposed period 1 inside a run of equal gaps at $f=1,d=37$ and its run was canceled. The revised search used a longer suffix to propose candidates. The proof uses the five-block cutoff and primitive gap test. All 4,800 fresh result rows agreed field for field with the original completed harvest. The primary replay used three nice-10 workers on an Apple M5 Pro and 7,045,120 bytes reported peak RSS. The independent replay used one worker, 52.70 seconds and 30,375,936 bytes peak RSS. The original attempt's peak RSS was not recorded in the inherited files. [Original checkpoint](STATUS.md) · [Frozen comparison](EXPERIMENT_SPEC.json)

## Verdict

- **CONTROLS:** No assumption overrode the controls. `python3 -B verify_counterexample.py` proved both seed expansions in two ways and rejected seven mutations per witness, including a wrong tail under each proof, a doubled period and a delayed onset.
- **CONTRADICTING:** No contrary table values were dropped. `python3 -B check_tables.py --arrays` retained all 1,845 displayed entries, all three overlapping seeds, and the seven contrary characteristic bits at TeX line 100. The period formula agrees at 4,799 of 4,800 primary seeds.
- **LABELS:** No result relied solely on a label. `replay_certificates.py` regenerated the greedy sets and recovered 5,138 triples from seeds and block sizes. The two distinct inputs named by $g=497$ and $d=497$ were both evaluated. The witness verifier checked its formula quotations against the supplied TeX.

These are deterministic certificates for fixed mathematical statements. There is no fitted score, sampling uncertainty or statistical holdout. The finite search establishes isolation of the period discrepancy only within its stated coverage. A follow-up could test a corrected Definition 8 supplied by the authors against the full archived comparison. The present result concerns the literal v1 formulas.
