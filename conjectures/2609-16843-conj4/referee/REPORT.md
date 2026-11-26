Shipped: An independent referee verdict confirming the disproof of Conjecture 4 and the corrected theorem for every d ≥ 3, with exact repairs to the proof and one false symbolic witness field.

VERDICT: HOLDS WITH CAVEATS

RESULT: yes

This is AI work. No human has checked it.

The sequence is ultimately periodic for every d in the conjecture. The minimal triples (preperiod in entries, period in entries, modulus in integer positions) are **(5,1,5)** at d=3, **(7,3,27)** at d=4, **(13,10,104)** at d=5, and **(d+3,d,8d−3)** for every d≥6. At d=4 the first block is 29,35,36, repeated every 27. At d=6 the block is 55–60, repeated every 45. Starting later does not recover the printed parameters. The full prefixes, tails, proof corrections and line-by-line audit are in [REFEREE.md](REFEREE.md).

**Did this referee find a new mathematical result? No.** The supplied theorem settles the question stated in v2. This review independently certifies that theorem and identifies defects in its evidence. The restricted source set does not establish publication priority.

## Verification and failed claims

The fresh verifier certified 40 cases by direct greedy generation with the paper's cutoff, an independent construction of the entire strict triple-sum set by residue, and exact generating-function counts. It checked the primitive binary and gap periods and the earliest boundaries. The symbolic exclusion check covers all 20 admissible original block types for unbounded d. The written inclusion proof covers all eleven intervals, including the d=6 join between 45 and 46. No summand collision or uncovered integer survives in the d≥6 theorem. [Verifier](referee_verify.py) · [Detailed proof audit](REFEREE.md)

The unchanged witness is 105,007 bytes and has the required SHA-256, `e40f8d4cd1523372c403614f0f25d653fb9e631bf363cda61176783fe6c07918`. The independently reconstructed 38 finite records and three small-case certificates match their serialized fields byte for byte. **Full semantic agreement fails.** At lines 105–114, `general_theorem_d_ge_6.blocks.U1` encodes the singleton d. Both endpoints must encode 1 as `[0,1]`. At d=6 the supplied block includes 6 and omits the first seed 1. [Original witness](inputs/witnesses.json)

The proof also needs corrections. At d=3, line 288 misses a second seed-only hole at 21. At d=4, lines 130 and 135 give incorrect finite-set lists. At d=5, line 171 imposes an unattainable order on the least progression base. The only strict triple for 221 is 19+79+123, with 123 already one step along the progression from 19. The witness uses valid shifted bases. The detailed verdict also repairs the rational-coefficient convention, the inclusion of a converse without its argument, an inequality annotation, and the cutoff lemma's printed number. [Producer proof](inputs/PROOF.md) · [Corrections](REFEREE.md)

## Reproduction

From the referee working directory, run the following with Python 3.10 or later.

~~~sh
nice -n 10 python3 -B referee_verify.py
~~~

The original payload produces **exit status 1** after completing all comparisons. Its final lines give `Completed 40 exact cases, 38 finite witness rows compared.` and `Total scientific witness disagreements: 1`. The intervening line identifies the two endpoints of `blocks.U1`. A zero exit would be incorrect for this input. For a standalone byte check use `shasum -a 256 inputs/witnesses.json`. The independent verifier uses only the Python standard library. On Apple M5 Pro, the final run, including literal triple enumeration, took 2.60 seconds and reached 31,014,912 bytes maximum resident memory.

## Referee checks

- CONTROLS: No assumption overrode the controls. The published controls with seeds (1,2,3) and (1,2,6) reproduced (6,5,23) and (6,6,28). All five supplied negative controls were rejected. Greedy first disagreed with the two printed-parameter candidates at n=60 and n=100. The doubled period and late boundary describe the correct set and fail minimality. All 1,169 additional mutants were rejected. [Verifier](referee_verify.py)
- CONTRADICTING: No contrary data was dropped. All 38 supplied rows and both requested spot-checks at d=50 and d=100 were retained. The digest matches while the symbolic block fails, and the false d=3,4,5 assertions are itemized with corrected values. [Detailed verdict](REFEREE.md) · [Witness](inputs/witnesses.json)
- LABELS: No annotation supplied its own verification. The shared theorem counter makes the cutoff Lemma 7 in Section 3. The affine witness field conflicts with its declared encoding. The small-case reconstruction reproduced 122 infinite-residue triples and 241 finite-gap triples from the raw sequence. [Verbatim primary source extracts](PRIOR_ART.md) · [Verifier](referee_verify.py)

## Sources, limits and next step

The four permitted inputs were the v2 TeX archive, the producer's proof and report, and the JSON witness. The audit credits van Berkel and Bosma's greedy sieve and finite-cutoff argument. It uses exact integer assertions with an independent verifier and a symbolic proof on the full parameter range. There is no fitted predictor, sampling estimate or statistical holdout. This is a local mathematical review without foundational proof-assistant verification. The next editorial step is to apply the numbered corrections in the verdict and regenerate the witness digest. [Prior art and baseline reproduction](PRIOR_ART.md) · [Producer report](inputs/REPORT.md)
