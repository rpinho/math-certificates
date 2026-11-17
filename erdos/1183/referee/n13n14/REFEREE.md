# Referee: candidate exact values f(13)=8 and f(14)=8 for Erdős #1183

Clean-room referee, 2026-11-17 (UTC 05:29–06:30). Nothing from `../erdos_sat3` was run, imported or copied. I read only its REPORT.md and PRIOR_ART.md, and I used `certificates/n13_coloring.json` and `n14_coloring.json` as data. All code is in `src/`, written in this job:

- `src/enc.c` is the CNF encoder.
- `src/poset_search.py` is the exact non-SAT search, validated against brute force by `src/validate_small.py`.
- `src/balanced.py` checks the balanced rank words.
- `src/check_coloring.py` checks the colouring files, `src/model_check.py` checks solver models, and `src/find_drop.py` finds the deletion witness.
- `src/run_guard.py` runs each step at nice 10 under `/usr/bin/time -l`, with an RSS guard at 7.6 GB.

Solvers were built in `tools/` from the official repositories (`tools/COMMITS.txt`):

- CaDiCaL `c60730422e758ef1cebe7aeddf2dda31c996bf04`
- kissat `8af8e56f174b778aef3aa45af9f739b2a5f492c2`
- drat-trim `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`

Every drat-trim run used the default backward mode with `-t 20000`, on the exact CNF that was solved.

## Sources and public status (shared by both parts)

The problem page https://www.erdosproblems.com/1183 was fetched on 2026-11-17 at 05:29 UTC (`sources/problem.html`; its text is in `sources/problem.txt`). The statement, verbatim:

> Let $f(n)$ be maximal such that in any $2$-colouring of the subsets of $\{1,\ldots,n\}$ there is always a monochromatic family of at least $f(n)$ sets which is closed under taking unions and intersections. Estimate $f(n)$.
> Let $F(n)$ be defined similarly, except that we only require the family be closed under taking unions. Estimate $F(n)$. In particular, is it true that $F(n)\geq n^{\omega(n)}$ for some $\omega(n)\to \infty$ as $n\to \infty$, and $F(n)<(1+o(1))^n$?

The page notes, verbatim:

> #1183: [Er78,p.39] … A problem of Erdős and Ulam. It is trivial that $f(n)\geq \frac{n+1}{2}$, since there is a sequence of $n+1$ many nested subsets. This seems to be all that they knew; Erdős [Er78] wrote 'we have no plausible conjecture for the true order of magnitude of $f(n)$'. … In [Er78] Erdős wrote that if the colouring is such that all subsets of same size receive the same colour then Howorka had proved that $F(n)>n^{\omega(n)}$ for some $\omega(n)\to \infty$, but gave no reference.

Status: the fetched HTML has no open/solved label in its text; the page lists "Comments (11)" and "Proof claims (1)".

- **The proof claim** (`sources/proofclaims.txt`) is "claimed by Deep Bhattacharjee, Priyabrata Mandal, Ushashi Bhattacharya (using Claude Code)". It concerns the asymptotic Erdős–Ulam questions and contains no small-n values.
- **The 11 forum comments** (`sources/forum.txt`) are:
  - Chojecki ×4, Tang ×3, old-bielefelder, and Sothanaphan ×2, all on 18 Mar 2026. They discuss GPT-5.4 Pro partial results on the subexponential half.
  - Xiao Hu, 05 Oct 2026, linking arXiv:2610.02833v1.
  - Comment posting is now suspended. No comment mentions f(13), f(14) or any exact small value.

**Definition in the paper.** BMB (arXiv:2610.02833; current text `sources/Erdos.tex` from anaxia-research/Erdos-1183, latest commit 2842ef3a, 2026-10-14) defines the function in its Introduction, line 133: a family is a "*sublattice* if it is closed under both union and intersection". It sets f(n)=min_χ max{|L| : L ⊆ 2^[n] a monochromatic sublattice}. The omega note (`sources/omega.md`) quotes the same definition and adds "Sublattices here are nonempty".

**Published lower bounds.**

- `prop:flower` (Erdos.tex l.1657–1662): f(n) ≥ ⌈(n+1+q)/2⌉ with q=⌊(n+1)/12⌋.
- `thm:f20` (l.1695–1703): f(n) ≥ ⌈(n+1+2q+e)/2⌉, where n+1=20q+r and e=[r≥12].
- For n=13: q=1 in prop:flower gives 8, and q=0, e=1 in thm:f20 give ⌈15/2⌉=8.
- For n=14: prop:flower gives ⌈16/2⌉=8, and thm:f20 gives ⌈16/2⌉=8.
- The omega note proves f(n) ≥ (n+3)/2 for odd n ≥ 11, so f(13) ≥ 8.
- None of these exceeds 8 at n=13 or n=14, so none contradicts the candidates.

**Was f(13) or f(14) already settled publicly before 17 Nov 2026? No, as far as I found.** I searched:

- the problem page, the forum and the proof-claims page;
- the BMB tex (grep for small-n values: none; it states "no step of these proofs depends on a computer calculation", l.428) and the omega note;
- all 20 anaxia-research/Erdos-1183 issues (`sources/issues.json`). Only #20 (rpinho, 2026-11-16, 0 comments) gives exact values, and those are f(11)=7 and f(12)=7;
- the anaxia commits (latest 2026-10-14);
- a GitHub repository search for "erdos 1183" (2 repos: anaxia, and QuanyuTang/erdos-problem-1183, last commit 2026-03-18);
- a GitHub issues search;
- rpinho/math-certificates (`erdos/1183`, latest commit 5d5c78b, 2026-11-14, "f(11)=7 and f(12)=7"; release erdos1183-v1);
- arXiv listing searches "Ulam union-closed", "\"union-closed\" monochromatic", "Bhattacharjee Mandal" and "monochromatic sublattice". The only relevant hit is 2610.02833, with v1 only. The arXiv API returned 503 and was not used.

The search is bounded: X, Reddit and Discord were not searched.

---

## Part I: n = 13

### (a) Definition

f(13) = min over 2-colourings χ of 2^[13] of the largest nonempty family L ⊆ 2^[13] with χ constant on L and L closed under ∪ and ∩. No particular sets (∅, [n], a common bottom or top) are required. The site's "monochromatic family … closed under taking unions and intersections", BMB's "sublattice" and the producer's definition (REPORT.md l.9) agree. Proving f(13)=8 therefore needs two things:

1. one colouring whose every monochromatic closed family has ≤ 8 members;
2. a proof that every colouring has one with ≥ 8.

### (b) Upper bound f(13) ≤ 8

**The colouring file** (`logs/coloring_check.log`):

- `n13_coloring.json` (SHA-256 37d17525…) has 8,192 entries with values {0,1}.
- The colour depends only on |S|, and the derived rank word is **11001011000110**, equal to the claimed word.
- Colour 0 is the ranks {2,3,5,8,9,10,13}; colour 1 is the ranks {0,1,4,6,7,11,12}.
- The producer's family 3,227,1795,2019,4067,6115,8163,8191 is 8 distinct sets, closed, colour 0, with sizes 2,5,5,8,9,9,10,13.
- My own search found another closed colour-0 family of 8: masks **3,7,31,255,511,767,1023,8191**, with sizes 2,3,5,8,9,9,10,13.

**SAT, my encoding (`src/enc.c`).**

- Variables are x_S for each S of colour c.
- For each incomparable pair S<T of colour c:
  - (¬x_S ∨ ¬x_T ∨ x_{S∪T}) if S∪T has colour c; likewise for S∩T;
  - otherwise the binary clause (¬x_S ∨ ¬x_T), emitted once.
- Comparable pairs need no clause.
- "At least 9" is a sequential counter, using only the sound direction s(i,j) → s(i−1,j) ∨ x_i and s(i,j) → s(i−1,j) ∨ s(i−1,j−1), with the unit s(N,9).

**Symmetry breaking** is a lex-leader constraint for each of the 78 coordinate transpositions (i j), with the variable order by mask. It is a chain over the pairs (S, S⊕{i,j}) with i∈S, j∉S, ascending. It is justified for this colouring as follows:

1. The colour depends only on |S|, so every coordinate permutation maps monochromatic closed families of colour c to monochromatic closed families of colour c of the same size.
2. Hence the lex-smallest member of any solution's S_13-orbit is a solution.
3. That member satisfies x ≤_lex x^σ for every σ. With the e-variables set to "equal so far" it satisfies every lex clause.

**Results.**

| colour | vars | clauses | solver | result | wall | peak RSS | drat-trim | wall | peak RSS |
|---|---:|---:|---|---|---:|---:|---|---:|---:|
| 0 | 113,188 | 12,953,275 | CaDiCaL | UNSAT (exit 20) | 2.6 s | 1.60 GB | **s VERIFIED** | 22.0 s | 1.43 GB |
| 1 | 128,476 | 13,666,546 | CaDiCaL | UNSAT (exit 20) | 24.6 s | 3.22 GB | **s VERIFIED** | 113.4 s | 1.50 GB |

- Logs: `logs/n13_c{0,1}.solve` and `logs/n13_c{0,1}.drat_check`.
- The CNF and proof SHA-256 values are in `logs/n13_hashes.txt`:
  - CNF c0 a916f0ac…, proof c0 457ea952…;
  - CNF c1 5f80f806…, proof c1 6a79853b….
- The CNFs are regenerated deterministically by `src/enc 13 11001011000110 C 9 1 0 out.cnf`.

My CNFs differ from the producer's, for example 12.95M against 14.75M clauses for colour 0, so this is an independent encoding.

The same colour-0 CNF without symmetry breaking (`src/enc … 9 0 0`) was also run: see **No-symmetry run** at the end of Part I.

**Second argument, without SAT (`src/poset_search.py`).**

1. Let L be a closed family with minimum A and maximum B. Put m(x)=⋂{S∈L : x∈S} for x∈B∖A. Then m(x) ∈ L and m(x) is join-irreducible in L.
2. Every S∈L equals A ∪ {x : m(x) ⊆ S}, and S ↦ {J join-irreducible : J ⊆ S} is a lattice isomorphism onto the down-sets of the poset P of join-irreducibles (Birkhoff).
3. |S_D| = |A| + Σ_{J∈D} w(J), where w(J) = #{x : m(x)=J} ≥ 1, and |A| + Σw ≤ n. Conversely, every weighted poset with these constraints is realised by blocks of coordinates.
4. So for a size-only colouring, a colour-c closed family of size m exists iff some (a, P, w) has every down-set sum a+w(D) in the colour-c rank set and has ≥ m down-sets.
5. The DFS adds the elements of P in a linear extension. Each prefix is a down-set of P, so its down-sets are members of the final family. It prunes as soon as a sum leaves the rank set and stops at ≥ t down-sets. The number of down-sets strictly grows at every step, so the search is complete.
6. Every witness found is turned into actual subsets and re-checked by direct closure (`closed()`).
7. Validation (`logs/validate_small.log`): for n=3,4,5, all 2^(n+1) rank words × 2 colours, its maximum equals the brute-force maximum over all sublattices of 2^[n] (73, 731 and 12,084 sublattices). There were 0 mismatches.

Result (`logs/poset_search.log`):

- colour 0: has 8 (the family above) and has **no family of 9 or more**, exhaustively in 204 nodes;
- colour 1: has **no family of 8**, exhaustively in 186 nodes.

The maximum is therefore exactly 8, and **this argument covers the whole upper bound without SAT or symmetry breaking**.

### (c) Lower bound f(13) ≥ 8

**The published argument** is BMB prop:flower with q=1, and thm:f20. Both rest on `lem:window`, "Every 2-colouring of 2^[11] has a red–blue pair of size at least 13" (l.1437–1440), a hand proof that I did not re-referee line by line.

**My finite re-derivation**, which does not use BMB:

1. Suppose every monochromatic closed family has ≤ 7 members.
2. A maximal chain has 14 sets, and each colour class of a chain is a chain, hence closed. So each maximal chain has exactly 7 sets of each colour.
3. Take k-sets T ≠ T′ with |T∩T′| = k−1. The two maximal chains through T∩T′ ⊂ T ⊂ T∪T′ and T∩T′ ⊂ T′ ⊂ T∪T′, identical elsewhere, differ only at rank k. The 7/7 count then forces χ(T)=χ(T′).
4. The Johnson graph J(13,k) is connected, so χ depends only on |S|, and the rank word is balanced (7 zeros and 7 ones).
5. `src/balanced.py` runs the exact search with t=8 on all C(14,7)=**3,432** balanced words, colour 0 first, then colour 1. Every word yields a family of ≥ 8 that is re-checked by direct closure (`logs/n13_balanced_summary.log`):
   - **3,432 of 3,432 rejected, 0 not rejected**;
   - 3,318 are rejected in colour 0 and 114 in colour 1;
   - by |P| in the witness: 1,139 with 3 elements, 1,179 with 4, 891 with 5 and 223 with 6.
6. The per-word rejection (word, colour, sizes, masks, poset) is listed in `logs/n13_balanced_words.txt`, one line per word.

No chain gives 8 here, because each colour has only 7 ranks. Every rejection is a non-chain lattice, for example the cube {7,8,8,8,9,9,9,10} over a base of 7 for 11111110000000. This agrees with the producer's summary (REPORT.md l.17) and with the omega note's route.

### (d) Controls (n=13)

- **Positive control.** The same lex encoding with K=8, colour 0, is SAT. Its model is 8 sets {6144,7168,7936,8160,8168,8176,8184,8191} with sizes 2,3,5,8,9,9,10,13, checked closed by `src/model_check.py` (`logs/n13_c0_k8.model_check`).
- **Deletion control** (`logs/n13_drop_control.log`, `logs/n13_drop_witness.txt`):
  - Witness: the 9-set family {3,5,7,31,255,511,767,1023,8191} violates exactly one encoder clause, closure clause #2, (¬x_3 ∨ ¬x_5), because 3∪5=7 is in the family but 3∩5=1 has the other colour.
  - Without symmetry breaking, deleting only that clause gives SAT. The model is exactly that 9-set family, and its only violated pair is (3,5).
  - With the lex clauses kept, the same deletion stays UNSAT. This is expected, not an inconsistency: permuted copies of the deleted clause remain, and the lex-leader of the witness's orbit violates one of them.
- **Corrupted proofs** (`logs/n13_corrupt_*.check`): drat-trim gives **s NOT VERIFIED** (exit 1) for:
  - the proof `0\n` (empty clause only);
  - the second half of a text DRAT proof of the colour-0 CNF with the first 6,061,603 lines removed. The intact text proof verified (exit 0, `logs/n13_c0_text.check`).

### (e) Gaps between the CNF and the statement (n=13)

- The CNF only allows colour-c sets, which is monochromatic by construction. Closure is required for every pair; comparable pairs are trivially closed.
- "≥ 9" covers all larger families.
- The lex clauses are sound as argued in (b).
- The upper bound is also proved without SAT, so a hypothetical encoding error would not change the conclusion.
- What is not machine-checked: the hand reasoning in (b) (Birkhoff and weights) and in (c) (the chain exchange), and the Python search code itself. That code was validated only against brute force for n ≤ 5.

**No-symmetry run.** The colour-0 CNF without lex clauses (221,365 fewer clauses than the lex CNF, 12,731,910 in total) was given to CaDiCaL with a 1,500 s limit. Result: **c UNKNOWN** after 1,500.2 s at 5.30 GB peak RSS, with an unfinished proof of 3.96 GB (`logs/n13_c0_nolex.solve`). The SAT route therefore depends on the lex-leader clauses. The exact poset search, which uses no symmetry breaking, does not.

**n=13 conclusion: f(13)=8 holds.** The upper bound rests on the colouring 11001011000110 (DRAT-verified for both colours and, independently, the exact poset search). The lower bound rests on my exhaustive check of the 3,432 balanced words and is also implied by the published BMB bounds.

---

## Part II: n = 14

### (a) Definition

The definition is the same as in Part I, with n=14. A maximal chain now has 15 sets.

### (b) Upper bound f(14) ≤ 8

**The colouring file** (`logs/coloring_check.log`):

- `n14_coloring.json` (SHA-256 b2fc8bb8…) has 16,384 entries.
- The colour depends only on size, with derived word **110010110001101**, equal to the claimed word.
- Colour 0 is the ranks {2,3,5,8,9,10,13}; colour 1 is the ranks {0,1,4,6,7,11,12,14}.
- Families of 8, checked closed and monochromatic:
  - colour 1, the chain 0,1,15,63,127,2047,4095,16383 (the producer's);
  - colour 1, the non-chain family **0,1,15,113,127,2047,4095,16383**, sizes 0,1,4,4,7,11,12,14 (mine);
  - colour 0, the family **3,7,31,255,511,767,1023,8191**.

**SAT.** The encoding is the same, with 91 transpositions, run one process at a time.

| colour | vars | clauses | solver | result | wall | peak RSS | drat-trim | wall | peak RSS |
|---|---:|---:|---|---|---:|---:|---|---:|---:|
| 0 | 274,141 | 59,954,034 | CaDiCaL (default) | UNSAT | 18.4 s | 7.03 GB | **s VERIFIED** | 190.3 s | 5.49 GB |
| 1 | 262,435 | 48,313,426 | CaDiCaL (default) | stopped by guard at 107.5 s, sampled 8.04 GB, no result | | | | | |
| 1 | same CNF | | kissat (default) | UNSAT (exit 20) | 69.7 s | 6.55 GB | **s VERIFIED** | 499.3 s | 4.97 GB |

- Logs: `logs/n14_c0_cadical.solve`, `logs/n14_c0.drat_check`, `logs/n14_c1_cadical.solve`, `logs/n14_c1_kissat.solve` and `logs/n14_c1.drat_check`.
- SHA-256 values (`logs/n14_hashes.txt`):
  - CNF c0 ef023db0…, proof c0 7da8b7eb… (437,628,780 B);
  - CNF c1 9596129f…, proof c1 d23150ca… (543,046,390 B).
- After their checks passed and were hashed, both proofs were moved to the Trash.

**Second argument, without SAT** (`logs/poset_search.log`):

- colour 0: has 8, **none of 9 or more** (exhaustive, 204 nodes);
- colour 1: has 8, **none of 9 or more** (exhaustive, 403 nodes).

So the maximum is exactly 8 in both colours. This also covers the whole upper bound.

### (c) Lower bound f(14) ≥ 8

The chain argument holds. Any maximal chain ∅=S_0⊂…⊂S_14=[14] has 15 sets, so one colour has ≥ 8 of them, and any subchain is closed under ∪ and ∩. BMB prop:flower and thm:f20 also give 8 (see Sources).

### (d) Controls (n=14)

- **Positive control.** The K=8 lex encoding is SAT for both colours, run with kissat (`logs/n14_controls.log`):
  - colour 0: model {12288,14336,15872,16320,16336,16352,16368,16382}, sizes 2,3,5,8,9,9,10,13, closed;
  - colour 1: model {0,8192,15360,16128,16256,16376,16380,16383}, sizes 0,1,4,6,7,11,12,14, closed.
- **Deletion control** (`logs/n14_drop_witness.txt`, `logs/n14_drop_control.log`):
  - Witness: colour 1, the family {0,1,15,63,113,127,2047,4095,16383}, which violates exactly one clause, closure clause #221,632 (¬x_63 ∨ ¬x_113). Here 63∩113=49 has 3 elements and the other colour.
  - Without symmetry breaking, deleting only that clause gives SAT with kissat. The model is exactly that 9-set family, with one violated pair, (63,113).
- **Corrupted proofs** (`logs/n14_controls.log`), against the colour-1 CNF: drat-trim gives **s NOT VERIFIED** (exit 1) for:
  - `0\n`;
  - the first half of the verified colour-1 binary proof (271,523,201 of 543,046,390 bytes, cut at a record boundary).

### (e) Gaps (n=14)

- The same remarks as for n=13 apply.
- The colour-1 SAT certificate comes from kissat, not CaDiCaL, because default CaDiCaL exceeded the memory guard. This is a resource stop and has no bearing on correctness. The resulting proof was checked by backward drat-trim.
- The exact poset search proves the upper bound independently of both solvers.

**n=14 conclusion: f(14)=8 holds.** The upper bound rests on the colouring 110010110001101 (DRAT-verified for both colours and, independently, the exact poset search). The lower bound is the 15-set chain.

---

## Did the referee find anything new?

No new value. The values f(13)=8 and f(14)=8 are the producer's, and I confirm them. They appear not to be public before 2026-11-17 (see Sources).

What I add is:

- a short exact non-SAT proof of both upper bounds (the weighted-poset search, under 1 s);
- an independent finite proof of f(13) ≥ 8 that does not rely on BMB.

## Exact statements that would go public

1. **f(13)=8.** Colour S ⊆ [13] by c(|S|), with c read from rank 0 to 13 as 11001011000110. Every union- and intersection-closed monochromatic family then has at most 8 members, and colour 0 contains one of 8: {3,7,31,255,511,767,1023,8191} as bit masks, bit i = element i+1. Conversely, every 2-colouring of 2^[13] has a monochromatic such family of 8 members. This follows from BMB prop:flower and thm:f20, from the omega note, and from the finite argument in Part I(c).
2. **f(14)=8.** The same holds with the word 110010110001101 (each colour attains 8). The lower bound is the 15-set chain.

## Limitations of this referee (none changes either value)

1. REFEREE.md, "No-symmetry run" (end of Part I). Without lex-leader clauses, CaDiCaL did not finish n=13 colour 0 in 1,500 s, so every DRAT certificate relies on the symmetry-breaking argument in Part I (b). That argument is standard (Crawford et al.), and it holds here because the colouring is invariant under coordinate permutations. The non-SAT search confirms the same bounds without it.
2. REFEREE.md Part II (b), table row "colour 1, CaDiCaL (default), stopped by guard" (and STATUS.md line 8). The n=14 colour-1 SAT proof uses kissat after default CaDiCaL hit the 8 GB guard. This is resource-only: the proof is verified, and the poset search also covers this case.
3. REFEREE.md Part I (c), "My finite re-derivation", and Part I (b), "Second argument, without SAT". The chain-exchange reduction and the Birkhoff weighted-poset reduction are hand proofs, written out here but not formalised. The search code was validated against brute force only for n ≤ 5. BMB `lem:window` (Erdos.tex l.1437) was not re-refereed; f(13) ≥ 8 does not depend on it, given the 3,432-word check.
4. All checks were made by AI models. No human has checked either value.

VERDICT: HOLDS
