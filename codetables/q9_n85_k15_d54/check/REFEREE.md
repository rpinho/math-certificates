> Packaged copy, lightly edited. Changes from the referee's original: the title and six wordings (in five places) say "clean-room" or "separate" where the original said "independent", because the referee is part of our own pipeline, not a third party. The reproduction section replaces the referee's interpreter path (its shared environment, Python 3.12.13) with `python3`, and notes that `compare_bounds.py` is not packaged. No mathematical or factual claim was changed.

# Clean-room referee report: [85,15,54] over GF(9)

**CODE VERDICT: CONFIRMED**

The supplied matrix has **rank 15 and exact minimum Hamming distance 54** over the specified GF(9). The live codetables.de entry is **53–63**, so the verified distance improves its lower bound by **one**. It is not implied by the eight earlier codes through standard parameter propagation. No earlier public report of a [85,15,≥54] GF(9)-linear code was found in the searches below.

**Did this identify a new improvement against the public record? Yes:** 54 beats the printed 53 for the same field, length, dimension and distance definition. This is a clean-room verification of the supplied matrix, not a claim that this referee invented it. A search that finds nothing is not proof of absence or an absolute priority certificate.

## Input, field and rank

The SHA-256 of `inputs/q9_n85_k15_d54.txt` is

```text
26e048b359ec2381558530ed88cc2df5ca8220c7a1626177a9043844575e761c
```

It matches `inputs/SHA256SUMS`. The file contains exactly 15 rows of 85 entries, each in 0–8. No input was changed.

An integer a+3b represents a+b·t, with a,b in GF(3) and t²=−1=2. Addition is componentwise modulo 3; multiplication is

```text
(a+b·t)(c+d·t) = (ac−bd) + (ad+bc)·t.
```

`checker.py` exhaustively checks closure, identities, commutativity, additive inverses, nonzero multiplicative inverses, associativity and distributivity on the nine elements (729 triples), including t²=2. Exact Gaussian elimination gives pivots in columns 0–14 and rank **15**. Independently, that 15×15 submatrix is upper triangular with nonzero diagonal 4, which also proves full row rank. All column numbers in the proof are zero-based.

## Complete minimum-distance proof

The method combines a standard BCH bound with complete Brouwer–Zimmermann enumeration on a shortened subcode. It does not infer a lower bound from random sampling.

### 1. BCH bound on the first 80 coordinates

Let g(x) have the first 66 entries of row 0 as its coefficients, in increasing degree. The checker verifies that row i restricted to columns 0–79 is xⁱg(x), for i=0,…,14.

Work in GF(81)=GF(9)[u]/(u²−(1+t)). The encoded element 4=1+t is a nonsquare in GF(9), checked exhaustively, so this is a field. The element α=t+u (extension encoding 12) satisfies α⁸⁰=1, α⁴⁰≠1 and α¹⁶≠1, hence has order 80. Exact evaluations find the 65 roots of g among its powers at exponents

```text
4–8, 13–17, 22–26, 30–79.
```

In particular, every polynomial representing a first-80-coordinate codeword vanishes at 50 consecutive powers α³⁰,…,α⁷⁹. Therefore every nonzero such word has weight at least **51**.

For completeness, the BCH bound here is just a Vandermonde argument: a word supported at w distinct positions, with w no larger than the number L of consecutive roots, would satisfy w homogeneous equations with coefficient matrix diag(nonzero factors) times a Vandermonde matrix on distinct powers of α. That matrix is invertible. The word would be zero, a contradiction. Thus its weight is at least L+1. This argument also applies to each subspace below; that subspace need not itself be cyclic.

### 2. Exhaust all appended-support cases

Write a full word as (c,z), with c of length 80 and z in GF(9)⁵. For any prescribed support S of z, impose zⱼ=0 for j outside S by exact nullspace calculation in the original 15 message coordinates. Evaluate every resulting basis polynomial at all αⁱ to identify shared roots and apply the preceding bound.

The separately computed cases are:

| Actual appended support | Bound on wt(c) | Result for wt(c,z) |
|---|---:|---:|
| wt(z)≥3 | 51 | ≥54 |
| Exactly two nonzero appended coordinates: all 10 pairs | ≥52 | ≥54 |
| Exactly one, at appended position 1, 2, 3 or 4 | ≥53 | ≥54 |
| No appended nonzero, or only appended position 0 nonzero | Handled by the subcode in step 3 | ≥54 |

`distance_result.json` gives the dimensions, consecutive-root starts and bounds for all 14 small-support cases in the middle two rows. For pairs, the consecutive roots start at 29 or 30 and have length 51; for the four singletons they start at 29 and have length 52. Since the first 80 columns have rank 15, a nonzero original message cannot give c=0. The table therefore covers every nonzero word without an exception hidden in a zero base word.

### 3. Complete enumeration of the remaining subcode

Imposing zeros in original columns 81–84 has constraint rank 3, giving a **12-dimensional** subcode. Delete those four zero coordinates to obtain D of length 81. Exact basis messages and systematic generator matrices are stored in `bz_setup.json`.

Use these information sets:

```text
I0 = { 0,…,11}       I1 = {12,…,23}
I2 = {24,…,35}       I3 = {36,…,47}
I4 = {48,…,59}       I5 = {60,…,71}
I6 = {72,…,80,0,1,2}
```

Each has rank 12. The first six are disjoint. The seventh adds nine previously unused positions, so the relative ranks are (12,12,12,12,12,12,9).

For each systematic generator, enumerate **all** information vectors of weights 1 through rᵢ, with

```text
(r0,r1,r2,r3,r4,r5,r6) = (8,7,7,7,7,7,7).
```

For a support of size w, normalize its first nonzero coefficient to 1 and enumerate all 8 choices at each other support position. This represents every scalar orbit and preserves Hamming weight. There are C(12,w)·8^(w−1) visits at weight w; the complete run makes **2,727,944,644 visits** across the seven sets, with possible repeats between sets. The minimum encountered is **54**.

**Stopping/completeness argument.** A nonzero word not represented by any enumerated scalar orbit has information weight at least rᵢ+1 in every Iᵢ. It therefore has at least 9 nonzeros in I0 and at least 8 in each of I1,…,I5. In I6 at most three nonzeros can lie in its already-counted positions {0,1,2}; it has at least 8−3=5 in {72,…,80}. Consequently every unexamined word has weight at least

```text
9 + 5·8 + 5 = 54.
```

All examined words have weight at least 54 too, and a weight-54 word occurs. Hence **d(D)=54**. Together with step 2 this proves **d(C)≥54** for the entire original 15-dimensional code.

### 4. Explicit upper-bound witness

The following message in the **original supplied row basis**, using the required 0–8 field encoding, gives a word of weight 54:

```text
0 0 0 5 7 1 4 2 4 6 5 7 2 5 7
```

`finish_distance.py` recomputes its 85 coordinates directly using scalar GF(9) arithmetic and checks equality with the enumeration witness. The full word is in `distance_result.json`; its final four coordinates are zero. Thus **d(C)≤54**, completing the proof that **d(C)=54**.

## Control and runtime

The same arithmetic and enumeration engine were applied to the known Reed–Solomon code obtained by evaluating degree-at-most-2 polynomials at all nine GF(9) elements. This is [9,3,7]₉: a nonzero quadratic has at most two roots, and a polynomial with two distinct roots attains weight 7. Separate scalar enumeration of all 91 projective messages gives weights 7, 8 and 9 with counts 36, 18 and 37. The information-set enumerator also returns **7**. Packed componentwise GF(3) addition is checked against scalar addition for all 81 pairs at every one of 128 bit positions before enumeration.

The measured end-to-end replay completed at 2026-11-08 00:58:11 UTC on macOS arm64, using **four CPU threads maximum**, at nice 10:

| Stage | Wall seconds |
|---|---:|
| Compile clean-room C++ enumerator | 0.466 |
| Field, input, rank and base BCH check | 0.033 |
| Subcode/information-set preparation and scalar RS control | 0.066 |
| RS information-set control | 0.055 |
| Complete candidate information-set enumeration | **4.450** |
| Support-case BCH calculations and final assembly | 1.305 |
| **Total including compilation** | **6.386** |

`run_metadata.json` records the measured times; `bz_result.jsonl` records the enumeration counts and minima. Arithmetic for the proof is exact; floating point is used only for elapsed time.

## Live comparison and derived entries

The [live codetables.de target](https://www.codetables.de/BKLC/BKLC.php?q=9&n=85&k=15), fetched again at **2026-11-08 01:00:38.935 UTC**, reports lower bound **53** and upper bound **63**. The listed lower-bound construction is a subcode of a [85,16,53] Construction XX code; the construction date is 2001-12-17. The new verified 54 **strictly exceeds 53**. The upper bound remains 63; optimality is not claimed.

The [GF(9) table rectangle](https://www.codetables.de/BKLC/Tables.php?q=9&n0=1&n1=85&k0=1&k1=15) was fetched at 00:56:22.398755 UTC. The immediate consequences are:

| Operation | Guaranteed code parameters | Live bounds | Improvement? |
|---|---|---|---|
| Puncture once | [84,15,≥53]₉ | 53–62 | No |
| Shorten once | [84,14,≥54]₉ | 54–63 | No |

More generally, s shortenings and p punctures give [85−s−p,15−s,≥54−p]₉ for 0≤s≤14, 0≤p≤53. Choose independent information coordinates for shortening; since p<54, puncturing preserves dimension. All **810** such parameter pairs, including the target, were compared with the live table. **Only (85,15) improves.** The remaining 809 consequences do not improve their printed lower bounds. `bound_comparison.json` contains all comparisons. This assesses the usual guaranteed propagation bounds, not a claim about specially optimized puncturing/shortening patterns.

## Relation to the eight earlier codes

None implies the candidate by the standard shortening, puncturing, subcode, repetition, or coordinate-extension propagation rules:

| Earlier code | Reason |
|---|---|
| [74,12,43]₅ | Different characteristic; no field extension or restriction turns GF(5)-linearity into GF(9)-linearity. |
| [128,14,79]₅ | Same alphabet obstruction. |
| [129,14,80]₅ | Same alphabet obstruction. |
| [130,14,81]₅ | Same alphabet obstruction. |
| [130,16,77]₅ | Same alphabet obstruction, despite its larger dimension. |
| [99,12,67]₉ | Dimension 12 cannot increase to 15 under those operations; puncturing to length 85 guarantees only [85,12,≥53]₉. |
| [92,13,61]₉ | Puncturing gives [85,13,≥54]₉, but dimension 13 is insufficient. |
| [106,12,72]₉ | Dimension 12 is insufficient; puncturing to 85 guarantees [85,12,≥51]₉. |

Dualization does not provide the needed distance guarantee from these parameters, and reversing shortening or adding three independent generators is not a guaranteed high-distance operation. A genuinely new construction from several codes would require extra structure and a new argument; the listed parameters alone supply no such implication. This is a parameter-propagation conclusion, not an equivalence classification of unavailable earlier matrices.

## Prior-art findings

The detailed search record, exact queries, scope and limitations are in **[PRIOR_ART.md](PRIOR_ART.md)**. Principal findings:

- [codetables.de history](https://www.codetables.de/updates.html): no target update; the exact target remains at 53.
- [MinT exact query](http://mint.sbg.ac.at/query.php?i=c&de=1&b=9&s=85&n=15&d=&t=), fetched 00:56:59.884541 UTC: **53–63**, not an earlier 54.
- [Chen exact query](http://databases.cs.hkr.se/qtcodes/searchqc2.php?n=85&k=15&q=9&m=&p=&author=), fetched 00:57:34.880160 UTC: no match. Its broader length-85 query returns [85,10,59]₉, which has insufficient dimension.
- Recent arXiv searches, including the last twelve months of GF(9)/quasi-twisted metadata and relevant paper text, found no [85,15,≥54]₉ report. Older GF(9) references were traced through Chen and the primary publisher/Math-Net records.
- Public GitHub searches sorted by recent updates, relevant coding-result READMEs and open issue/PR descriptions, the specified AI-lab result catalogues, and indexed community searches found no earlier target claim. One recent repository does report GF(4) improvements not yet on codetables.de; those were checked and are not this target.

The exact table, update history, public repository search, and relevant result catalogues were rechecked at **01:00:38–01:00:39 UTC** before this verdict. Search coverage is finite: some checks are catalogue/abstract-level, GitHub repository search is not exhaustive file-content search, and the older paper's full text was not accessible through its advertised link. **No earlier report found is not proof of absence.**

## Reproduction and scope

In the referee's job directory, with a C++17 compiler and Python 3 (the packaged replay is in [COMMAND.md](COMMAND.md)):

```sh
(cd inputs && shasum -a 256 -c SHA256SUMS)
nice -n 10 python3 run_check.py
nice -n 10 python3 compare_bounds.py   # not packaged; bound_comparison.json is its saved output
```

The distance replay is offline and rebuilds the clean-room checker. The comparison command reads the saved live-table snapshot; its fetch time is recorded above. `checker.py`, `prepare.py`, `enumerate.cpp`, and `finish_distance.py` contain the complete clean-room arithmetic and proof computation. No producer/referee directory or math-certificates directory was read, and no third-party repository code was downloaded or executed. No commits, posts, submissions or messages were made. No statistical prediction is involved, so predictor baselines and SBS do not apply.

**CODE VERDICT: CONFIRMED** — exact distance 54 verified; 54>53 at the live entry; not implied by the earlier listed codes; no earlier report found in the documented public search.

VERDICT: ACCEPT
