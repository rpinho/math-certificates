Shipped: referee verdict on the candidate f(12)=7 for Erdős #1183: it holds. Two independent arguments of mine show the producer's colouring has no monochromatic sublattice with 8 or more members: (1) my own CNF, solved by my own CaDiCaL build with DRAT proofs checked by my own drat-trim build; (2) an exact weighted-poset search that needs no SAT. The chain bound gives 7 from below.

Did the producer find something new? **Yes.** f(12) was open on 14 Nov 2026 in every source I checked (section e). The omega note lists "Determine the exact values of f(n) for even n" as open, and BMB v1 gives exact values only for n ≤ 10.

Job directory: `math_wave_1030/e1183n12_referee/`. All code is mine (`ref.py`, `solve.sh`, `dfs_control.py`, `dfs_scan.py`), Python standard library only. I imported, ran and read no code from `../erdos_sat2`. I used only its REPORT.md, PRIOR_ART.md, `sources/` and the data file `certificates/n12_coloring.json` (sha256 `b42dbee6…4168`).

Tools, built from the official repositories in `tools/`:
- CaDiCaL rel-3.0.1, commit `c60730422e758ef1cebe7aeddf2dda31c996bf04` (github.com/arminbiere/cadical);
- drat-trim commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` (github.com/marijnheule/drat-trim).

Both are default builds. Every drat-trim check below is the default backward check.

## (a) Definition

**Site, verbatim** (https://www.erdosproblems.com/1183, fetched 2026-11-14 16:43 EST, `web/page.html`):
> Let $f(n)$ be maximal such that in any $2$-colouring of the subsets of $\{1,\ldots,n\}$ there is always a monochromatic family of at least $f(n)$ sets which is closed under taking unions and intersections. Estimate $f(n)$.
> Let $F(n)$ be defined similarly, except that we only require the family be closed under taking unions. Estimate $F(n)$. In particular, is it true that $F(n)\geq n^{\omega(n)}$ for some $\omega(n)\to \infty$ as $n\to \infty$, and $F(n)<(1+o(1))^n$?
> […] It is trivial that $f(n)\geq \frac{n+1}{2}$, since there is a sequence of $n+1$ many nested subsets. This seems to be all that they knew; Erdős [Er78] wrote 'we have no plausible conjecture for the true order of magnitude of $f(n)$'.

**Status:**
- The site shows no solved banner; the problem box has class `neutral`.
- teorth/erdosproblems `data/problems.yaml` (HEAD, fetched today) has #1183 `status: open`, last update 2026-03-07.
- The proof-claims page has 1 claim, which concerns the asymptotics of F and f.
- The forum (`web/forum.html`) has 11 comments, 5 Oct 2026 – 18 Mar 2026. They cover Chojecki's GPT-5.4 Pro partial results (the subexponential half for F; for f, an upper bound via Birkhoff's representation and bounded-width posets), Tang–He–Li's near-identical result, LLM comparisons, Xiao Hu's link to arXiv:2610.02833 and Sothanaphan's "Standard check" remarks. None mentions n = 12 or any exact small value of f. Commenting is suspended.
- My page, forum and claims texts are identical to the producer's 16:24 copies except for the Cloudflare token.

**Paper** (Bhattacharjee–Mandal–Bhattacharya, arXiv:2610.02833v1; current tex at anaxia-research/Erdos-1183, `../erdos_sat2/sources/final_creelie_paper.tex` lines 128–150):
- f(n) = min over 2-colourings χ of max{|L| : L ⊆ 2^[n] a monochromatic sublattice}, where a sublattice is a family closed under both union and intersection.
- "A single set is a sublattice", and the chain bound is stated as eq. (trivial).

**Omega note** (`../erdos_sat2/sources/omega_note.md` lines 21–25, 113):
- The same min–max definition; sublattices are nonempty.
- In the Lean version, "the largest cardinality of a nonempty union- and intersection-closed monochromatic family".

**Producer** (`../erdos_sat2/REPORT.md` line 5): M(χ) is the largest nonempty monochromatic family closed under binary union and intersection, and f(n) = min_χ M(χ).

**Verdict: the definitions match.**
- None of the three requires a sublattice to contain ∅ or [n], or any other particular set. The site's own trivial bound uses an arbitrary colour class of a chain, and the paper says a single set is a sublattice.
- "Maximal such that in any colouring there is always a family of ≥ f(n)" is the same number as min_χ max |L|.
- Nonemptiness is immaterial, because singletons are sublattices.
- The one reading under which the result would change is a "0,1-sublattice" that must contain ∅ and [n]. No source uses it, and under it the site's own chain bound would be false. Not a caveat.

## (b) Upper bound f(12) ≤ 7

**Colouring data** (`ref.py colour`, output in `colour_check.log`):
- All 4096 masks are coloured 0 or 1, and the colour depends only on |S|. The rank word for r = 0..12 is `1100101100011`.
- Colour 1 = ranks {0,1,4,6,7,11,12}, 2237 sets. Colour 0 = ranks {2,3,5,8,9,10}, 1859 sets. Both match the producer's claim (REPORT.md lines 9–13).

**A 7-member family exists.** In colour 1: ∅, {1}, {1..4}, {1..6}, {1..7}, {1..11}, {1..12} (masks 0, 1, 15, 63, 127, 2047, 4095). It is a chain, hence closed, and was checked directly. In colour 0, my SAT control returned {1,2}, {1,2,3}, {1..5}, {1..8}, {1..9}, {1..8,10}, {1..10}, which includes an incomparable pair; checked directly for colour and closure.

**My CNF** (`ref.py` lines 89–137).
- Variables: one per set of colour c.
- For every incomparable pair x, y, the clauses ¬x ∨ ¬y ∨ (x∪y) and ¬x ∨ ¬y ∨ (x∩y). If the union or intersection has the other colour, that literal is dropped.
- Comparable pairs need nothing, since their union and intersection are the pair itself.
- "At least 8": a totalizer with outputs truncated at 8 (the "o_j ⇒ count ≥ j" half only) plus the unit o_8. This is a different cardinality encoding from the producer's sequential counter.
- Soundness: the clauses ¬o_{i+j+1} ∨ a_{i+1} ∨ b_{j+1} force, by induction up the tree, count ≥ j whenever o_j holds.
- Completeness: every family of ≥ 8 sets satisfies the CNF when each o_j is set to [subtree count ≥ j].
- So the CNF is satisfiable exactly when colour c contains a sublattice with ≥ 8 members. Families larger than 8 are covered.

**Colour 1: plain CNF, no symmetry breaking, no rank assumption.**
- `cnf/c1_k8.cnf`: 11,177 variables, 4,869,986 clauses, sha256 `fb56c108…9217`.
- CaDiCaL: UNSAT in 58.4 s, 1.92 GB peak RSS (`logs/c1_k8.solve`, `logs/c1_k8.solve.time`).
- DRAT: 307,901,830 bytes, sha256 `2b4beae15d9ee5c9722f1a40d3da50b0ec9e3f481ffcdb8da2d18f03b4426182`.
- drat-trim: `s VERIFIED` in 108.8 s, 0.99 GB peak (`logs/c1_k8.check`, line "s VERIFIED").

**Colour 0: case split on the bottom and top of the family.**
- Any sublattice L has a least member B and a greatest member T.
- The colouring depends only on size (checked above), so a permutation of [12] taking B to {1..b} and T to {1..t} preserves colours, size and the lattice operations.
- So it suffices to look for families whose members all lie between B = {1..b} and T = {1..t}, with B and T as members, for colour-0 ranks b < t.
- Since |L| ≤ 2^(t−b), only t − b ≥ 3 is needed, which gives 10 cases: (2,5), (2,8), (2,9), (2,10), (3,8), (3,9), (3,10), (5,8), (5,9), (5,10).
- Each case uses the same encoding, restricted to the interval, plus the units B and T (`ref.py` lines 95–102). Each is UNSAT, and each DRAT proof is `s VERIFIED` (`logs/c0_iv_*.solve`, `logs/c0_iv_*.check`).
- The largest case, (2,10), has 502 variables and 8,413 clauses; its proof is 164,294 bytes and checked in 0.05 s.
- Proof sha256 prefixes: 2_5 `37909ddd`, 2_8 `9335f993`, 2_9 `869aaa54`, 2_10 `667967ad`, 3_8 `a9ea8b1f`, 3_9 `29c61564`, 3_10 `b545565f`, 5_8 `32f8eb5b`, 5_9 `e906138c`, 5_10 `a54dc5ba`. The proofs are kept in `proofs/`.
- The symmetry step is elementary but not formalised. Argument 2 below and the plain run do not depend on it.

**Colour 0: plain CNF, no symmetry breaking, no rank assumption.** This run makes the colour-0 result independent of the symmetry step above.
- `cnf/c0_k8.cnf`: 9,287 variables, 3,128,332 clauses, sha256 `fbb969f2…7d47`.
- CaDiCaL: UNSAT in 565.3 s, 1.84 GB peak (`logs/c0_k8.solve`).
- DRAT: 1,771,960,885 bytes, sha256 `adb6d3f14e71bdb6e6f6dbd2229609f33c47beb9d70961f9f638036a6cf3b7b3`.
- drat-trim: `s VERIFIED` in 2486 s, 2.78 GB peak; 8,986,506 of 14,265,817 lemmas in core (`logs/c0_k8.check`, `logs/c0_k8.check.time`).
- A first check attempt was killed by my tool's time limit before it finished. That was not a checker failure, and the rerun is the one reported here.

Both colours therefore have plain, symmetry-free UNSAT certificates checked by my own drat-trim build, so the upper bound needs neither the rank-symmetry argument nor the producer's lex-leader clauses.

**Second argument: exact search over weighted posets** (`ref.py cmd_dfs`, lines 53–86; output in `dfs.log`).
- Structure lemma (proved here). Let L ⊆ 2^[n] be a sublattice with least member B and greatest member T. For x ∈ T∖B let m(x) be the intersection of all members containing x; m(x) is itself a member. Order x ≤ y when x ∈ m(y).
- Then every member X equals B ∪ ⋃_{x∈X∖B} m(x), so X∖B is a down-set of this preorder. Conversely, every down-set D gives B ∪ D = B ∪ ⋃_{y∈D} m(y), which is in L by closure under union, or is B itself when D is empty.
- So L = {B ∪ D : D a down-set}, and |B ∪ D| = |B| + the sum of the block sizes in D. Hence, for a rank colouring, L is described by an offset b = |B| and a poset P with weights ≥ 1 summing to at most 12 − b, and L is monochromatic iff b + w(I) has colour c for every ideal I of P.
- Search. The DFS builds P one new maximal element at a time, choosing the element's down-set and weight. Ideals, and therefore member sizes, only get added, so pruning on colour is exact. Every poset is reached through one of its linear extensions.
- Result: the largest monochromatic sublattice has 7 members in both colours, so the colouring has none with 8 or more. Examples: colour 0 sizes {2,5,5,8,9,9,10}; colour 1 sizes {0,1,6,6,7,11,12}. Runtime 0.05 s.
- Controls for this argument:
  - (i) `dfs_control.py`: on every one of the 32 rank words at n = 4, it agrees (capped at 8) with brute-force enumeration of all 731 sublattices of 2^[4]: 0 mismatches.
  - (ii) `dfs_scan.py`: the minimum over all rank words of the largest monochromatic sublattice is ⌈(n+1)/2⌉ for n ≤ 10 (matching BMB v1, `creelie_v1_paper.tex` line 222: "f(n)=⌈(n+1)/2⌉ for n≤10"), 7 at n = 11 (matching the Lean-proved f(11) ≥ 7, omega line 124), and 7 at n = 12, attained by 24 rank words including the producer's.
  - (iii) It finds the paper's 8-member family for the word RRBRBBRRBR (paper Table, line 1531).
- How far it goes: argument 2 settles every rank colouring, and so by itself gives f(12) ≤ 7. It says nothing about non-rank colourings, which are not needed for an upper bound.

So two independent arguments, SAT+DRAT and the poset DFS, agree that this colouring's largest monochromatic sublattice has exactly 7 members.

## (c) Lower bound f(12) ≥ 7

- Every 2-colouring of 2^[12] colours the 13-member chain ∅ ⊂ {1} ⊂ … ⊂ [12]. One colour gets at least ⌈13/2⌉ = 7 of its members; checked over all 8192 colourings of a 13-chain (`colour_check.log`).
- Any subfamily of a chain is closed under union and intersection, because max and min stay in the subfamily.
- Under the site's statement this family is valid: the site uses exactly this argument ("a sequence of n+1 many nested subsets"). It is also valid under the paper's definition, which states the same bound as eq. (trivial), line 150.
- BMB Theorem (final paper lines 266–273) gives ⌈(n+1+q)/2⌉ with q = ⌊13/12⌋ = 1, which is also 7 at n = 12, so the published lower bound is the chain bound here.
- The producer's argument (REPORT.md line 15) is correct.

## (d) Controls

- **Positive, colour 1:** `cnf/c1_k7.cnf` (same encoder, k = 7) is SAT. The decoded family (`logs/c1_k7.model_check`) is the 7-chain above, checked directly for colour, distinctness and closure.
- **Positive, colour 0:** the k = 7 interval case (2,10) is SAT, with the incomparable 7-member family listed in (b), checked directly.
- **Corrupted proofs** (`controls/`), using a text DRAT proof for case (2,10) that is itself `s VERIFIED`:
  - a proof containing only the empty clause: `s NOT VERIFIED`, exit 1;
  - the same proof with its middle half of lines deleted: `s NOT VERIFIED`, exit 1;
  - the valid binary proof checked against the CNF with the at-least-8 unit removed: `s NOT VERIFIED`, exit 1. That CNF is SAT under CaDiCaL.

## (e) Anything else

**Prior publication: none found.** Searched today, 16:43–16:46 EST, results in `web/`:
- the erdosproblems.com page, forum and proof claims;
- teorth/erdosproblems problems.yaml and its 60 open PRs: none mention 1183;
- the GitHub repository search "erdos 1183" (2 repos);
- anaxia-research/Erdos-1183 (formerly creelie): last commit 2842ef3a, 2026-10-14; 19 issues/PRs, none mentioning f(12) or n = 12;
- the arXiv API: "Erdos AND Ulam AND sublattice" and "monochromatic sublattice" return nothing new; arXiv:2610.02833 has v1 only;
- the producer's own refresh (PRIOR_ART.md line 29).

The omega note (line 137) lists "[open] Determine the exact values of f(n) for even n", and BMB v1 gives exact values only for n ≤ 10. Limits of the search:
- I did not search X, Reddit, Discord or Zenodo.
- GitHub code search needs authentication, so I did not search code.
- Search misses do not prove priority.

**The statement that would go public:**
> f(12) = 7. The colouring χ(S) = word[|S|] with word = 1100101100011 (ranks 0–12) of 2^[12] has no monochromatic family of 8 or more sets closed under union and intersection. Every 2-colouring has a monochromatic 7-member chain. Hence f(12) = ⌈13/2⌉: the chain bound is sharp at n = 12, the first open even value.

Context worth adding: BMB's Question 9.3 equality f(n) = ⌈(n+1)/2⌉ fails for odd n ≥ 11 and for all n ≥ 23, but holds at n = 12.

**Gap between the CNF and the statement: none found.**
- Variables are distinct sets, so the number of true variables is the family size.
- Comparable pairs need no clause.
- A missing union or intersection literal exactly forbids that pair.
- The totalizer half used is sound and complete for "≥ 8".
- The colour-0 interval reduction uses rank invariance, which I checked on all 4096 masks. The plain colour-0 certificate does not need it.
- The remaining trust base is the CaDiCaL/drat-trim pipeline, which is not formally verified, together with my own encoder. That is mitigated by the independent poset DFS, which agrees.

**Notes on the producer's report** (not caveats on the result):
- REPORT.md line 34: the producer's colour-0 certificate depends on 66 transposition lex-leader clauses. My verification does not use them.
- The producer's novelty claim (REPORT.md line 3, "Yes, candidate") is consistent with what I found.

## Reproduction

From this directory, after building `tools/` (CaDiCaL: `./configure && make`; drat-trim: `make`, at the commits above). C is the producer's colouring file:

```sh
C=../erdos_sat2/certificates/n12_coloring.json
python3 -I ref.py colour $C            # colouring, 7-member witness, chain bound
python3 -I ref.py dfs $C               # argument 2
python3 -I dfs_control.py . ; python3 -I dfs_scan.py .
python3 -I ref.py cnf $C 1 8 cnf/c1_k8.cnf && ./solve.sh c1_k8 && tools/drat-trim/drat-trim cnf/c1_k8.cnf proofs/c1_k8.drat
python3 -I ref.py cnf $C 0 8 cnf/c0_k8.cnf && ./solve.sh c0_k8 && tools/drat-trim/drat-trim cnf/c0_k8.cnf proofs/c0_k8.drat -t 7000
python3 -I ref.py cnf $C 0 8 cnf/c0_iv_2_10.cnf 2 10   # same for the other 9 (b,t) cases
```

The four large CNFs and the two large proofs were deleted after their checks passed. Their SHA-256 hashes are in `SHA256SUMS`, and the CNFs regenerate byte-for-byte from `ref.py`.

Resources:
- Peak RSS: 1.92 GB (solve) and 2.78 GB (check). At most 3 processes ran at once, all at nice 10.
- Wall time: 16:37–17:55 EST.
- No solver or checker processes remain.

VERDICT: HOLDS
