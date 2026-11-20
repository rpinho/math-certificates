Shipped: a clean-room referee verdict that the e1183b3 claim holds. For each of the 44 splits of 23, every three-block colouring has a monochromatic sublattice of size 14. Every two- or three-block colouring of the 22-cube has one of size 13. Both bounds are attained by rank words.

# Referee report: Erdős #1183, three-block colourings at n = 23 and n = 22

Refereed packet: `math_wave_1030/e1183b3` (REPORT.md, PROOF.md, data/). I did not read or run anything under `src/`, `build/` or `logs/`, and I imported no producer code. Every script I used is in `referee/`. The only producer material I used is from `data/`: the DIMACS, LRAT and family files, which I treat as certificates. Every family I used was checked from the definition.

**Is this new? No.** This is a restricted-class result. The unrestricted bounds 13 ≤ f(23) ≤ 14 stay open. REPORT.md says the same.

## 1. Definitions and reduction (PROOF.md): my own proofs

Notation: a sublattice is a family of distinct subsets closed under binary ∪ and ∩. H_c(T) is the largest colour-c sublattice in a face table T. I use N = 23 and h = 13. A face of dimension d has an exterior chain of N − d sets.

- **Exterior chain (H0 + z ≤ 13, H1 + 2 − z ≤ 13).** Let the face be [D, U]. Take a saturated chain from ∅ up to D, excluding D, and one from U up to [N], excluding U. Together they have |D| + N − |U| = N − d members. Each member is a subset of D or a superset of U, so it is comparable with every set in the face and with every other member. Adding the colour-c members to a colour-c sublattice inside the face therefore keeps it closed. In a value-13 colouring this gives H0 + z ≤ 13 and H1 + (N − d − z) ≤ 13. **Holds.**
- **Child contexts.** Fix one free coordinate absent. The parent top U is then strictly above the whole child and extends the child's upper exterior chain, so z' = z + [colour(U) = 0]. Fixing a coordinate present works the same way with the parent bottom. Directly: H_c(child) + [colour of the top is c] ≤ H_c(parent), so an admissible parent at z has an admissible child at z'. **Holds.**
- **Window gluing.** A parent table is the union of its lower and upper child windows on any axis. When the axis width is at least 2, the two windows agree on their overlap. Every admissible parent therefore appears among the glued pairs of admissible children. **Holds.**
- **Two-block slices.** Fix the count on axis j at k. The cells with count below k (other counts 0) and above k (other counts maximal) can be realised as one chain. That chain runs from the parent bottom to the slice bottom and from the slice top to the parent top, and it is comparable with the whole slice. So the slice context is z plus the zeros on that chain. **Holds.**
- **Witness rejection.** A checked closed family of k colour-c sets inside the face, with k > 13 − z (c = 0) or k > d − 10 + z (c = 1), rules out (T, z). Exterior padding in the shipped families is canonical prefixes 2^j − 1 above the face. I checked this and then dropped the padding, so only the local part was used. **Holds.**
- **48 shapes cover every face.** A 21-face of split (a, b, c) fixes two coordinates. Its free shape is a partition of 21 into at most 3 parts, empty blocks allowed, and there are exactly 48 such partitions (37 with three positive parts, 10 with two, 1 with one). Permuting blocks is a relabelling of coordinates, so tables only need to be classified up to block order. **Holds.**
- **Displaced windows (33 splits with min ≥ 2).** Fix two elements of the largest block A. The windows at offsets 0 and 1 have free shape (a − 2, b, c). On the shared cells x ∈ [1, a − 2], the ranks x + y + z run over all of 1..21, so w[k+1] = v[k] would be needed for every k = 0..20. **Holds.** I also checked by script that this argument covers all 44 splits.
- **Singleton corollary (11 splits (a, b, 1)).** Fix the singleton absent and displace a window in A (when b = 1) or in B. The shared ranks are again 1..21. The ten splits other than (11, 11, 1) need only the two-block shapes (20,1) and (12,9) to (19,2). (11, 11, 1) needs (11, 10), which the earlier two-block packet did not cover. PROOF.md says so correctly, and this run classifies (11, 10). **Holds.**
- **n = 22.** Fix one coordinate of the largest block absent. The facet has a one-set exterior chain, the full set. A global value of at most 12 forces H0 ≤ 12 and H1 ≤ 12 on the facet. That is exactly the z = 1 admissibility at ambient 23 (12 = 13 − 1 and 12 = 13 − (2 − 1)), so the facet carries one of the four words. A 12-family of that word in the colour of the full set, plus the full set, gives 13. **Holds.**
- **Finder completeness (PROOF.md, Birkhoff section).** The exclusions do not depend on it, because rejections only need lower-bound witnesses. For the upper constructions I proved the connected-prefix lemma myself and used it in my own search (§4). The lemma: if every remaining minimal element were above every prefix element, every remaining element would be comparable with every prefix element, so the incomparability graph would be disconnected. **Holds.**

## 2. Independent checker

`referee/induct.py` (about 4.7 s, 68 MB peak RSS) recomputes, from dimension 0 upward, a superset of the admissible (table, z) pairs for all 286 shapes. It covers the 132 two-block shapes and the 154 three-block shapes on the shortening tree. It uses my own gluing, my own context bit-masks and my own slice test against my own two-block catalogue. Rejections come from the shipped families in `data/{p,t}-*.gz`. Each family is checked for distinct members, closure of both the local and padded families under ∪ and ∩, canonical exterior padding, and its cell image under my block layout.

| Quantity | Mine | Producer (REPORT) |
|---|---:|---:|
| Surviving table/context pairs, all levels | **211,490** | 211,490 |
| Candidate pairs | 409,412 | 409,454 |
| Families checked, invalid | 108,524, **0** | 108,566 |
| Dimension-21 shapes | 48 | 48 |
| Survivors in every dimension-21 shape | **exactly the four rank words, z = 1 only** | same |

The 42-unit gaps in candidates and families are a counting convention: I drop context-free dimension-0 entries and exterior-only families, which my z-range rule covers. Surviving pairs agree exactly. The superset argument makes my lists sound whatever happens to the producer's lists.

**Sixteen shifts** (`final_check.py`): w[k+1] vs v[k] over k = 0..20 differ in 11, 11, 10, 10, 11, 11, 10, 10, 10, 10, 11, 11, 10, 10, 11, 11 positions. That is eight pairs at 10 and eight at 11, and none is 0. All 44 splits are excluded.

**DIMACS regeneration** (`roots.py`, `roots_singleton.py`, `face_check.py`). I compared clause multisets with the same variable numbering, not byte order.
- split23: **44/44** equal. 33 use the largest-block displacement; 11 singleton splits use singleton-absent windows (on A for (21,1,1), on B for the rest).
- split22: **52/52** equal, including the 8 family clauses per split.
- face: **48/48** structurally equal up to renaming. Each has 3 context variables, and its lower and upper choice pools per context have the same sizes as my dimension-20 child lists. All |pool|² pairs are forbidden, for example 16² + 24² + 16² = 1088 for (7,7,7). My direct join confirms that every such pair is either inconsistent or glues to one of the four words at z = 1. The face CNFs are therefore valid and add nothing beyond the join.

**LRAT** (`run_lrat.sh`): **144/144** verified by my own checker, `lrat.py` (RUP with positive hints only, empty clause required). They are also verified by the standard `lrat-check` from drat-trim (https://github.com/marijnheule/drat-trim, commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; lrat-check.c sha256 `bf07c2ac96b9035da1ebcc578cb95e956a2b795629d613154cdb307f8a8f4a95`). It was built locally and run offline, writing only under referee/.

## 3. The four words, from the definition

`rank_exact.py` computes the exact maximum for rank colourings. It runs a longest-path DP over ordinal sums of connected weighted posets, enumerated by connected-prefix linear extensions, and it builds and checks an explicit physical family. Controls: it matches brute force on 124 cases (every word, n ≤ 4, every subfamily) and on 150 cases (closure enumeration, all words at n = 5 and 12 random words at n = 6), with 0 mismatches. Each of the four words has H0 = H1 = 12 on the 21-cube, with checked 12-families. So they are admissible exactly at z = 1: at z = 0 the bound is H1 ≤ 11, and at z = 2 it is H0 ≤ 11.

## 4. Upper constructions

- `001001110010110001101101` (n = 23): exact maximum **14 in colour 0 and 14 in colour 1**, with checked 14-families.
- `00100111010011100110100` (n = 22): **13 and 13**, with checked 13-families.

A rank colouring is a three-block colouring for every split, so these bounds are attained on all splits.

## 5. n = 22 families

All 52 splits (40 three-block, 11 two-block, the rank control) and all 416 families were checked. Each family has 13 distinct sets, is closed, contains the full 22-set, and its other 12 sets avoid one A-coordinate. For every split, the 12-sets have ranks that are monochromatic for all 4 words × 2 colours. Both the argument and the CNFs check out.

## 6. Corruption controls (`corrupt.py`, `corrupt2.py`, `corrupt3.py`, `corrupt/controls.log`)

| Damage | Result |
|---|---|
| Flip a literal in a clause the proof uses (split23 9-7-7, split23 11-11-1, split22 10-7-5, face 7-7-7) | Rejected by both checkers, 4/4 |
| Change one LRAT hint (split23, face, split22) | Rejected by both, 3/3 |
| Flip a literal in a clause the proof does not use (split23) | LRAT still verifies, as it should; regeneration reports clause multiset ≠ shipped |
| Drop the set 31 = 1 ∪ 30 from a shipped family | My checker marks it invalid (fam_bad = 1) |
| Drop a set from a split22 family | Not closed, size 12: rejected |

In the second run of `corrupt2.py`, a parsing slip (indexing with a negative literal) flipped the wrong clauses. Those lines were superseded by the third run, and all three runs are appended in controls.log. One earlier drop control removed set 2017, which left a family that was still closed and therefore valid, so it was not a corruption.

## 7. Scope and wording of REPORT.md

The first line of REPORT.md claims the exact three-block minimum at n = 23 is 14 for all 44 splits, and 13 at n = 22 for all two- and three-block splits. That is correct and properly restricted. REPORT.md states that 13 ≤ f(23) ≤ 14 remains open and answers "new? No". I found nothing overstated. Two minor points:
- "Byte-for-byte" regeneration is the producer's own claim. I confirmed clause-multiset equality, and face CNFs only up to renaming.
- The two checks REPORT calls separate (its LRAT checker and its face replay) are by the same agent, as REPORT says.

Live sources re-checked on 2026-11-20: the authors' repo issues (anaxia-research/Erdos-1183, latest #20 "f(11) = 7 and f(12) = 7") and an arXiv API query. Neither shows f(23) settled.

## Caveats on my verification, none affecting the verdict

- The rejection witnesses come from the producer. I verified them; I did not search for them.
- Rank upper bounds rest on my exact search, which is brute-force-validated only up to n = 6.

## Reproduction (from referee/)

```sh
P=~/dev/open-science/.venv/bin/python
nice -n 10 $P -I induct.py ../data out && $P -I final_check.py
$P -I roots.py && $P -I roots_singleton.py && $P -I face_check.py
nice -n 10 ./run_lrat.sh            # needs ext/lrat-check: cc -O2 -o ext/lrat-check ext/drat-trim/lrat-check.c
$P -I rank_brute.py && $P -I rank_brute2.py
$P -I rank_exact.py 0010011100101100011011 0011001011100010110011 1100110100011101001100 1101100011010011100100 00100111010011100110100 001001110010110001101101
$P -I corrupt.py && $P -I corrupt2.py && $P -I corrupt3.py
```

Resources: every step ran sequentially at nice 10, about 1 minute of CPU in total, with peak RSS under 100 MB.

VERDICT: HOLDS
