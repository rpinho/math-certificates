Shipped: a clean-room referee report. Every two-block colouring of 2^[23], for all eleven splits a + b = 23 with a, b ≥ 1 (and the rank case b = 0), has a monochromatic sublattice of size 14. The rank word 001001110010110001101101 attains exactly 14 in both colours. All of this was reproduced with my own checkers. Verdict: HOLDS.

# Referee report: Erdős #1183, two-block colourings of the 23-cube (job e1183b2)

**Clean room.** I read REPORT.md, PROOF.md, PRIOR_ART.md and the files in data/ only. I did not read or run anything under src/ or logs/, and I imported no producer code. All checker code is in this directory and was written for this review. The producer's data files were treated as claims and certificates. Each witness family I use was re-checked from the definition before it was allowed to reject anything.

**Did the producer find something new? No, and REPORT.md says so.** The result settles a restricted class: colourings that depend only on (|S∩A|, |S∩B|). The unrestricted bounds 13 ≤ f(23) ≤ 14 are unchanged.

## 1. Definitions and lemmas (PROOF.md §1–§5)

I checked each lemma by hand. None fails. Notes on each:

- **§1 A–B (Birkhoff labelling and vector weights).** Correct and standard. j_x is the meet of all members containing x. It is join-irreducible, and the labels are surjective onto the nonbottom join-irreducibles. Members correspond bijectively to ideals. Cells are β + Σ_{p∈D} w(p). The converse embedding works with disjoint coordinate blocks.
- **§2 C (halving).** Correct. The ideals containing a maximal element p form the interval [↓p, P]. The ideals avoiding p form J(P−p). Both are sublattices, so a family of at least 28 members contains one of at least 14. D, E, F, G and H are immediate.
- **§3 (ordinal-sum DP and connected-prefix generator).** Correct. Elements in different components of the incomparability graph are comparable, with one uniform direction between any two components (shown by walking along edges), so P is the ordinal sum of its components. J(C1⊕C2) glues the top of J(C1) to the bottom of J(C2), giving |J1|+|J2|−1 members. Connected-prefix lemma: if every minimal element of the remainder R lay above all of the prefix Q, then all of R would lie above Q and the graph would be disconnected. A minimal element of R is never below an element of Q, because Q is a down-set. So some minimal element is incomparable to an element of Q. The exclusion proof itself does not depend on §3: it uses only checked witness families. I used the same two facts in my own exact solver (§4 below) and proved them independently.
- **§4 (direct (21,2) certificate and table-selector lemma).** Correct, and confirmed computationally (§2b below).
- **§5 exterior-chain lemma.** Correct. A face F = [bot, top] of dimension d has t = 23 − d exterior sets: the chain from ∅ up to bot (|bot| sets) and the chain from just above top up to [23] (23 − |top| sets). Each exterior set is comparable with every face member and with every other exterior set. So the union of a closed face family with any subset of the chain is closed. In a colouring whose maximum is 13, every face and every exterior chain with z zeros therefore satisfy H_0 + z ≤ 13 and H_1 + t − z ≤ 13.
- **§5 canonical witness.** Correct. The local part of a closed canonical witness is closed, since unions and intersections of local sets are local. Its exterior members all have the family's colour c. They map injectively onto colour-c sets of the real chain, which has the same counts (z, t − z). The order along the chain is irrelevant because any subset of a chain is a chain.
- **§5 induction lemma.** Correct. For the lower child (one free coordinate fixed absent), the parent top sits directly above the child top. The child's exterior chain is therefore the parent's chain plus the parent top, giving context z + [C(top) = 0]. The upper child is symmetric, with the parent bottom. Survivors form a superset of the admissible tables, so extra survivors could only weaken the conclusion.
- **§5 covering.** Correct. With a ≥ b, shortening by two gives shape (a−2, b) for b ≤ 2 and (a, b−2) for 3 ≤ b ≤ 11. Every resulting shape is one of (12,9), …, (21,0), and the shortened axis keeps at least one free coordinate. The windows at offsets 0 and 1 are faces of that shape. If both carry rank tables w and w′, then on the overlap w_{k+1} = w′_k for every k = 0..20. That would make a length-21 suffix of w equal a length-21 prefix of w′.

## 2. My own exact checker

Commands (from this directory; `P=~/dev/open-science/.venv/bin/python`):

```sh
nice -n 10 python3 regen_all.py out/all-splits.regen.cnf && cmp out/all-splits.regen.cnf ../data/all-splits.cnf
nice -n 10 python3 lrat_check.py ../data/all-splits.cnf ../data/all-splits.lrat
nice -n 10 python3 lrat_check.py ../data/exclusion.cnf  ../data/exclusion.lrat
nice -n 10 python3 faces_check.py ../data/faces.jsonl.gz          # out/faces_check.log
nice -n 10 $P excl_check.py ../data out/exclusion.regen.cnf && cmp out/exclusion.regen.cnf ../data/exclusion.cnf
nice -n 10 python3 upper_check.py ../data                         # out/upper_check.log
nice -n 10 python3 rows_exact.py ../data                          # out/rows_exact.log
nice -n 10 python3 brute6.py                                      # out/brute6.log
nice -n 10 sh corrupt.sh                                          # out/corrupt.log
```

### 2a. All-splits certificate (faces.jsonl.gz, all-splits.cnf/.lrat, faces21.json)

- **DIMACS regenerated from the definition: byte-identical** (SHA-256 0f09c798…dd69ddf). regen_all.py builds 12 split selectors and, per split, grid variables at base + j(a+1) + i. It adds 4 + 4 window selectors, each forcing the rank embedding of one of the four words on its window.
- **LRAT: my checker (lrat_check.py, RUP with hints; RAT is rejected) prints VERIFIED UNSAT.** This instance is logically just the overlap test, so the substance lies in the face induction.
- **Witness families: 86,466 read, 0 rejected.** For every family, faces_check.py checks the following: the members are distinct; there are at least 14; it is pairwise closed under ∪ and ∩; every member is a local set of the d = u+v local bits (A first) or an exterior prefix [k] with k > d, coloured 0 iff k − d ≤ z; and the exterior members all share one colour.
- **Face induction (my own enumeration), using only those checked families to reject:**
  - 747,796 joined table/context pairs. REPORT gives 747,844; the difference of 48 is the 2 colours × 24 contexts of the one-cell base, which I do not count as joins.
  - **20,948 survivors over all levels, identical to REPORT.**
  - **On each of the ten terminal shapes (12,9) … (21,0), contexts z = 0 and z = 2 are empty. z = 1 holds exactly the rank embeddings of the four words:** 0010011100101100011011, 0011001011100010110011, 1100110100011101001100, 1101100011010011100100.
- **16 suffix/prefix comparisons:** 8 differ in 10 positions and 8 in 11; the minimum is 10. REPORT's "at least ten" is correct.
- My exact solver gives maxima of 12/12 for each of the four words on the 21-cube, so they do satisfy (1) at z = 1. "Precisely" in PROOF §5 is therefore right: there are not merely at most four.
- Peak RSS 50 MB, 42 s of CPU.

### 2b. Direct (21,2) certificate (sets.jsonl.gz, window-families.jsonl, rows.json, V.json, triples.json, exclusion.cnf/.lrat)

- sets.jsonl.gz: **146,641 families, 0 rejected** (distinct, ≥ 14 members, closed). window-families.jsonl: **42,432, 0 rejected.**
- **The rows and windows re-derived from the definition match.** I filtered all 2^22 row words by the footprints of checked families lying inside one row: **1,198 survive in each of rows 0, 1 and 2, equal to rows.json.** I then filtered all 1,198² ordered pairs by the footprints lying inside rows (0,1), and separately rows (1,2): **28 survive in each window, equal to V.json.** So the selector clauses are valid lemmas.
- **Length-2 paths through V: exactly 4, equal to the paths in triples.json.** Each triple's 14-family is closed and monochromatic on its 3-row grid (two in colour 0, two in colour 1).
- **DIMACS regenerated: byte-identical** (SHA-256 842bb9fd…1625bf4). **LRAT: VERIFIED UNSAT** with my checker. This certificate independently excludes (21,2) even without SAT: valid grid → both windows in V → one of the 4 paths → monochromatic 14-family.
- Peak RSS 187 MB, 109 s.

### 2c. Secondary counts in REPORT (rows_exact.py, my exact solver)

- The 1,198 rows have exact maxima 12/12: 4, 12/13: 118, 13/12: 118 and 13/13: 958, as REPORT states. The four 12/12 rows are exactly the four face words.
- All 28 windows are rank restrictions of 23-letter words, each with exact maxima 13/13, as REPORT states.

## 3. Upper construction (upper_check.py)

- C(i,j) = w_{i+j} colours S by w_{|S|}, so the construction is the same rank colouring for every split.
- Both shipped 14-families are distinct, closed and monochromatic (colour 0 and colour 1) on 2^[23].
- **No 15-family: my own exact search gives a maximum of 14 in each colour**, and no component reaches 15.
  - The method is complete, not a sample. It enumerates weighted posets by connected-prefix linear extensions; a component reaching 15 ideals is caught with at most 8 elements. A DP over ranks then glues components (the §3 lemmas, re-proved above).
  - The solver matches direct brute-force sublattice enumeration on all 240 word/colour cases with n ≤ 5 and on 16 cases at n = 6, with 0 mismatches.
  - It reproduces REPORT's 4/118/118/958 distribution over 2,396 independent (row, colour) maxima.
- I did not replay the producer's .tree.gz files. My search replaces them.

## 4. Corruption controls (corrupt.sh, out/corrupt.log)

- **Flipped clause literal.**
  - Both regenerated DIMACS files differ from the corrupted ones, so regeneration rejects them.
  - LRAT on corrupted formulas: flipping a literal in all-splits clause 2 (`-1 37…` → `-1 -37…`) is rejected. A flip in exclusion clause 293306, which the proof uses, is rejected.
  - Two flips in exclusion clauses that the proof never cites (clause 1 and `-122 -62`) still give VERIFIED UNSAT. This is expected, because an unused clause cannot affect the refutation. The byte-for-byte regeneration is the control that catches those flips.
- **Altered LRAT hint:** an in-range hint was replaced by a neighbouring id in each proof, and each was rejected ("not unit"). A truncated all-splits proof (empty-clause step removed) was rejected.
- **Dropped set:**
  - Upper families: 28/28 single-member drops rejected. Flipping one coordinate of a member is rejected (not closed).
  - faces.jsonl.gz, first 20,013 drops: 19,999 rejected. sets.jsonl.gz, every 997th family, 2,102 drops: 2,054 rejected.
  - The 14 and 48 accepted remainders came from families larger than 14 where an extreme member was removed. They are themselves closed families of size ≥ 14, i.e. still valid witnesses, so accepting them is correct.
- **The induction actually depends on the witnesses.** Removing the two checked witnesses of case (20,0,1) turns the face result into NOT CONFIRMED.

## 5. Scope and wording of REPORT.md

- REPORT.md states the scope correctly. Its headline is restricted to two-block colourings. It says 13 ≤ f(23) ≤ 14 stays open and answers "Did we find something new? No". It calls the result candidate and unrefereed.
- No number I could check is wrong. 67 shapes = 22 rank + 45 rectangles; 552 cases; 20,948 survivors; 747,844 joins = my 747,796 + 48 base cells; 1,198 / 1,435,204 / 28 / 4; 122 variables / 295,748 clauses; 1,408 / 7,881; 146,641 and 86,466 families.
- Mild emphasis issues, not errors:
  1. The table's "Fresh SAT proof" column for all splits certifies only the final overlap step. All the eliminating work is the witness induction, which is not inside the LRAT. PROOF §5 says this explicitly; REPORT's table could be read as giving the SAT proof more weight than it carries.
  2. "To attain 13 unrestrictedly would require a colouring that breaks every two-block symmetry" should be read as: a value-13 colouring, if one exists, is not of two-block form for any split. That is exactly what is proved.
- The lower bound 13 is attributed to the producer's own earlier work (PRIOR_ART.md). I did not re-referee it, and the two-block exclusion does not depend on it.
- I did not run Lean or CaDiCaL. Neither is needed, since my own LRAT checker and regeneration cover the propositional part.

## Resources

Single-threaded except rows_exact.py (4 workers). Under 10 minutes of CPU in total. Peak RSS 187 MB, against the 4 GB budget. No processes left running.

VERDICT: HOLDS
