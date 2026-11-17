# Clean-room referee: f(15)..f(20) = 9, 9, 10, 10, 11, 12 for Erdős #1183

Referee job e1183n1520_referee, 2026-11-17. I wrote all code here myself: `src/wps.c` (weighted-poset search), `src/brute.py` (brute force over all sublattices), `src/check_witnesses.py` and `src/check_balanced.py` (direct closure checks). I did not read or run any code from ../e1183n15 or ../e1183n1314_referee/src. I used ../e1183n15/certificates/results.json only as data (words and witness masks). Raw outputs are in `out/`, and fetched sources are in `sources/` and `ext/window20/` (SHA256SUMS included).

Summary: f(15)=9, f(16)=9, f(17)=10, f(18)=10 and f(19)=11 hold under my own checks, with no dependency beyond elementary arguments that I re-derived. f(20)=12 holds only together with the revised BMB manuscript's computer-assisted Lemma `lem:window20`. I replayed the authors' own C checker for that lemma (PASS, and corrupted lists are rejected) and read its reduction without finding a gap, but I did not re-implement the mixed-level part. Without that lemma, what is proved is 11 ≤ f(20) ≤ 12.

## Sources (quoted)

- **erdosproblems.com/1183** (fetched 2026-11-17, `sources/erdos1183.html`): "Let $f(n)$ be maximal such that in any $2$-colouring of the subsets of $\{1,\ldots,n\}$ there is always a monochromatic family of at least $f(n)$ sets which is closed under taking unions and intersections. Estimate $f(n)$." The commentary says: "It is trivial that $f(n)\geq \frac{n+1}{2}$, since there is a sequence of $n+1$ many nested subsets. This seems to be all that they knew". Status: the page shows no solved marker (the problem box has `id=neutral`, and it lists "Comments (11)" and "Proof claims (1)"). The page, the discussion thread and the proof-claims thread give no exact value of f(n) for any n ≥ 15. I searched the extracted text for f(15)..f(29) and n=15..20 and found no match.
- **arXiv:2610.02833v1** (Bhattacharjee–Mandal–Bhattacharya, "Resolving Erdős-Ulam Monochromatic Union-Closed Family Conjectures", submitted 2 Oct 2026; only v1 exists). Its abstract concerns F(n). As REPORT.md says, the improved f lower bounds are not in v1. I did not re-read the v1 body.
- **Revised manuscript**, anaxia-research/Erdos-1183 at commit 2842ef3a, `paper/Erdos.tex`. HEAD is byte-identical, sha256 dd6dbb09…. Definition (lines 132–138): a family is a "sublattice if it is closed under both union and intersection", and $f(n)=\min_\chi\max\{|\mathcal L|: \mathcal L\subseteq 2^{[n]}$ is a monochromatic sublattice$\}$.
  - `prop:flower` (Erdos.tex:1657–1663): "Let $n\ge1$ and $q=\lfloor(n+1)/12\rfloor$. Every $2$-colouring of $2^{[n]}$ has a red--blue pair of size at least $n+1+q$. Consequently $f(n)\ge\lceil(n+1+q)/2\rceil$."
  - `thm:f20` (Erdos.tex:1695–1704): "Let $n\ge1$, write $n+1=20q+r$ with $0\le r\le19$, and put $e=1$ if $r\ge12$ and $e=0$ otherwise. Every $2$-colouring of $2^{[n]}$ has a red--blue pair of size at least $n+1+2q+e$. Consequently $f(n)\ge\lceil(n+1+2q+e)/2\rceil\ge 11n/20$." The text after it says the proof "rests on" `lem:window20` (Erdos.tex:1711–1715): "Every $2$-colouring of $2^{[19]}$ has a red--blue pair of size at least $22$". That lemma "is the only result of this paper that depends on a computer calculation".
- **Omega-institute note** (the-omega-institute/trureturing, `Problems/bhattacharjee-mandal-bhattacharya-2026-sublattice-chain-bound-refutation.md`): for odd n ≥ 11, f(n) ≥ (n+3)/2, by the same balanced-word rigidity route, labelled "[proved: Lean]" (omega.md:104–109). I did not rerun the Lean proof.
- **GitHub**: the anaxia-research/Erdos-1183 issues (#1–#20) contain only our own f(11)..f(14) candidates in #20 (body and one comment, last updated 2026-11-17T12:03Z), and nothing for n ≥ 15. `gh search repos "Erdos 1183"` returns only that repository. Two arXiv API searches ("Erdos AND Ulam", "sublattice AND monochromatic") found nothing relevant after 2610.02833.

## (a) Definition — PASS

- Site: a monochromatic family closed under unions and intersections, with f(n) the guaranteed size.
- Manuscript: f(n) = min over 2-colourings of the max size of a monochromatic sublattice, where a sublattice is closed under union and intersection.
- Producer (PROOF.md:3): families are nonempty and closed under binary union and intersection, and need not contain ∅ or [n]. Also f(n) = min over colourings of the largest family.

These agree. Binary closure gives closure under all nonempty finite unions and intersections. Neither source requires ∅ or [n]. Allowing the empty family changes no maximum. The rank-word convention (word letter r = colour of all r-sets, r = 0..n, length n+1) matches every word in results.json: lengths are 16..21 for n = 15..20.

## (b) The reduction (PROOF.md), lemma by lemma

1. **Join-irreducibles m(x), positivity (PROOF.md:7–9) — PASS.** For x ∈ B\A, m(x) = ∩{S∈L : x∈S} lies in L and is not A. If m(x) = U∪V, then x lies in U (say) and m(x) ⊆ U ⊆ m(x). For a join-irreducible J, every m(x) with x ∈ J\A is ⊆ J and contains x, and A ⊆ m(x). So J = ⋁ m(x), and join-irreducibility makes J one of them. Hence w(J) ≥ 1.
2. **Birkhoff (PROOF.md:11) — PASS.** A finite sublattice of 2^[n] is distributive. It is therefore isomorphic to the down-sets of its join-irreducible poset. x ∈ S iff m(x) ⊆ S for S ∈ L, so |S| = a + Σ_{J∈D} w(J), and a + Σw = |B| ≤ n.
3. **Converse realisation (PROOF.md:13) — PASS.** Disjoint nonempty blocks give an injective map that preserves ∪ and ∩, with the same sizes. Colours depend only on size, so a colour class R contains a closed family of at least m members iff some weighted poset with a + Σw ≤ n has at least m down-sets, all of whose sizes lie in R.
4. **Search completeness (PROOF.md:19–26) — PASS.**
   - Every finite poset has a linear extension.
   - Each prefix of that extension is a down-set, and down-sets of a down-set are down-sets of the whole poset. So every size checked at a prefix is a member size of the final family, and colour pruning is sound.
   - The strict down-set of the next element is a down-set of the current prefix, and every such down-set and every weight in the remaining budget is branched on.
   - The number of down-sets never decreases along prefixes, so stopping at "≥ threshold" is sound.
   - Depth is at most n−a.
   - The chain-node floor 2^|R|−1 (PROOF.md:28) is correct: the chains on nonempty subsets of R are distinct reachable states. It is a certificate sanity property, not part of the proof.
5. **Symmetries and prunes (PROOF.md:38–44) — PASS.** Colour swap is immediate. Complementation S↦[n]\S swaps ∪ and ∩ and maps rank k to n−k. Class size above T is ruled out by a chain witness. Factor monotonicity holds: S↦[s]∪(s+S) stays inside [n] because s+l ≤ n+1, preserves both operations and shifts ranks by s. Catalogue reuse is a direct membership check. These prunes feed only the producer's rank-minimum claims (REPORT.md:58–67). They play no part in the six f(n) values, whose upper bounds use one word each and whose lower bounds use the arguments in (d). I did not re-check the 1.5 M screen records or 55,893 packed trees, because they are not needed for the values.
6. **Chain-exchange lemma, odd n (PROOF.md:48–52) — PASS.** Re-derived in (d).

I checked the method on more than paper: my implementation of exactly this search agrees with brute force over all sublattices on every rank word at n ≤ 5 and n = 6.

## (c) Upper bounds — PASS for all six words

The method is `src/wps.c` in `max` mode: an exhaustive enumeration of every valid state, with no threshold and no symmetry pruning. It returns the exact maximum for each colour and rebuilds a witness as coordinate masks, recomputing the down-sets from the predecessor relation and checking closure directly.

**Validation against brute force.**
- `src/brute.py` enumerates every nonempty sublattice by closure growth. It counts 3, 12, 73, 731 and 12,084 sublattices at n = 1..5, matching the producer's 73, 731 and 12,084 at n = 3..5.
- For all 2^(n+1) words at each n ≤ 5, the colour maxima from brute force and from wps agree, with 0 differing lines (`out/brute_n*.txt` vs `out/wps_all_n*.txt`).
- n = 6: brute force finds 319,987 sublattices (matching the producer's count), and both colour maxima agree on all 128 words, with 0 differing lines (465 s, 314 MB RSS).

**Refereed words (out/max_words.txt).**

| n | word | c0 / c1 max | overall |
|---|---|---|---|
| 11 | 100010011101 | 7 / 7 | 7 |
| 12 | 1100101100011 | 7 / 7 | 7 |
| 13 | 11001011000110 | 8 / 7 | 8 |
| 14 | 110010110001101 | 8 / 8 | 8 |

The required 7, 7, 8, 8 are reproduced.

**Headline words (out/max_words.txt; each run under 0.05 s and 2.7 MB RSS).**

| n | word | my exact max c0 / c1 | claimed | producer's listed witnesses (own Python check) |
|---|---|---|---|---|
| 15 | 1100101100011010 | 9 / 8 | 9 / 8 | both closed, right colour, sizes 9 and 8 |
| 16 | 00100111010011001 | 9 / 9 | 9 / 9 | both OK |
| 17 | 110010110001101001 | 10 / 10 | 10 / 10 | both OK |
| 18 | 0010110011101001100 | 10 / 10 | 10 / 10 | both OK |
| 19 | 00110010111000101101 | 11 / 11 | 11 / 11 | both OK |
| 20 | 110010110001101100110 | 12 / 12 | 12 / 12 | both OK |

The decision mode agrees: NONE at claimed+1 and FOUND at claimed, for both colours at n = 15 and n = 20 (`out/controls.txt`). Every witness my own search finds passes the direct closure check.

My valid-node counts (498/403, 1114/552, 1255/1043, 2369/1330, 2709/2606, 3577/7471) equal the producer's reported tree sizes. That is expected, because both enumerate the same set of valid states. It confirms we agree on the state space. It is not an independent algorithm: my exactness argument is the completeness proof in (b) plus the brute-force agreement at small n.

So f(n) ≤ 9, 9, 10, 10, 11, 12 for n = 15..20.

## (d) Lower bounds

- **n = 16, 18 (chain) — PASS.** A maximal chain has n+1 members, and each colour's part of it is closed, so f(n) ≥ ⌈(n+1)/2⌉ = 9 and 10.
- **n = 15, 17, 19 (chain exchange) — PASS.**
  - Re-derivation: let m = (n+1)/2 and suppose no monochromatic closed family has more than m members. A maximal chain has 2m members, and each colour's subchain is closed. So each colour occurs exactly m times in every maximal chain.
  - For k-sets S, T with |S∩T| = k−1, two maximal chains through S∩T ⊂ S ⊂ S∪T and S∩T ⊂ T ⊂ S∪T can agree everywhere else. Equal colour counts then force χ(S) = χ(T).
  - Exchange paths connect all k-sets, so the colouring depends only on size, and its rank word has m letters of each colour.
  - Hence, if every balanced word has a monochromatic closed family of at least m+1 members, then f(n) ≥ m+1.
  - My check (`./src/wps bal n`, then the independent `src/check_balanced.py`) covered every balanced word: 12,870 at n=15, 48,620 at n=17 and 184,756 at n=19. Each word received an explicit coordinate-mask witness of size ≥ 9, ≥ 10 and ≥ 11 respectively. The Python check confirms the word set is exactly all balanced words and all witnesses are distinct, of one colour, inside [n] and closed, with 0 bad (`out/balanced_check.txt`). Runtimes were 0.06 s, 0.2 s and 0.75 s, with at most 2.5 MB RSS.
  - **Compare prop:flower:** q = 1 for n = 15, 17, 19 gives ⌈17/2⌉ = 9, ⌈19/2⌉ = 10 and ⌈21/2⌉ = 11, the same values. The omega note's (n+3)/2 also gives 9, 10, 11. That makes three independent routes.
- **n = 20 — HOLDS CONDITIONALLY.**
  - The chain gives 11. prop:flower gives ⌈(21+1)/2⌉ = 11.
  - thm:f20 with n+1 = 21 = 20·1 + 1 (q = 1, r = 1, e = 0) gives a red–blue pair of size ≥ 23, hence f(20) ≥ 12. It depends on `lem:window20` (Erdos.tex:1711–1825), whose proof reduces to a finite computation.
  - I read the reduction:
    - The pivot bound p(k−1)+p(18−k)+2 ≥ 22 for mixed levels k ≤ 7 or k ≥ 12 is correct, using prop:flower's p(m) ≥ m+2 for m ≥ 11.
    - The cube step via lem:adjacent is correct.
    - Families (a)–(d) are monochromatic sublattices as stated. The permutation in (d) exists because U ⊂ S ⊂ W (or U ⊂ T ⊂ W) is a chain of sizes k−1, k, k+1.
    - The enumeration space is 2^16 · 3^4 = 5,308,416 level patterns, plus one lower/upper colour bit per other mixed level at each pivot.
    - I found no gap.
  - Dependency check:
    - I downloaded the published `checks/window20/check_window.c` and the list `certs_19_22.txt` (63,272 sublattices) at commit 2842ef3a into `ext/window20/`, read the C source (it only reads the list and prints), compiled it and ran it.
    - Result: "63272 certificates, 5308416 patterns, 242 settled by pivots, 708872 word choices, least pair 22 / PASS" in 0.2 s and 15.7 MB. `certs_11.txt` (the m=11 window behind prop:flower) also passes, with "least pair 13".
    - Their three corrupted lists (target 23, pivot sublattices removed, one member deleted) are each rejected.
    - The checker verifies that every listed family is a sublattice, so the computation's inputs are self-certifying. The case logic, however, is the authors', and I replayed it; I did not re-implement it.
    - Independently, with my own code, I checked the size-colouring case of lem:window20 (the part the authors also checked in Lean): every rank colouring of 2^[19] has max(red) + max(blue) ≥ 22. That is 524,288 words with rank 0 fixed by colour swap, 0 failures, least capped sum exactly 22 (`out/split_n19_K22.txt`, 404 s, 3 MB). As a control, the same code at m = 11 gives ≥ 13 on all words, while K = 14 fails on 62 of the 2,048 words, so 13 is tight there.
  - **What is proved without thm:f20:** 11 ≤ f(20) ≤ 12. The rank-colouring minimum at n = 20 does not lift to all colourings, because n = 20 is even and there is no chain-exchange rigidity. PROOF.md:73 says this correctly.

## (e) Controls — PASS

- **Known families found.** My search attains every claimed maximum and reproduces 7, 7, 8, 8 on the refereed words.
- **Corrupted witnesses rejected** (`out/witness_check.txt`):
  - Flipping one coordinate of one member is rejected as "wrong colour" or "duplicate".
  - Swapping in a duplicate member is rejected.
  - Relabelling the colour-0 witness as colour 1 is rejected.
  - Deleting a member is rejected as "not closed" at n = 15, 16, 17, 19. At n = 18 and 20 the shorter family is still closed but one smaller than claimed, so the size check catches it.
- **Flipped letters** (`out/controls.txt`), all n+1 single-letter flips of the n=15 and n=20 words:
  - The colour that gains a rank never loses maximum, and the colour that loses a rank never gains, as monotonicity requires.
  - At n = 20 every flip pushes one colour above 12 (to 14..24). At n = 15, 15 of the 16 flips push one colour above 9. The exception is the last letter (rank 15, 0→1), which gives (8, 9), another word at the bound.
  - The answer changes where expected.

## (f) Anything else

- **Public before 17 Nov 2026?** No. I searched:
  - erdosproblems.com/1183, its discussion thread and its proof-claims thread;
  - anaxia-research/Erdos-1183 (issues #1–#20 with comments, commit log to 14 Oct, file tree);
  - GitHub repo and issue search for "Erdos 1183";
  - arXiv 2610.02833 (v1 only) and two arXiv API queries;
  - the omega-institute note.

  None gives an exact f(n) for n ≥ 15. The strongest public lower bounds are prop:flower (9, 9, 10, 10, 11, 11) and thm:f20 (12 at n=20). No public upper bound comes close: the manuscript's is min{n²+n+1, …}. This was a bounded search and does not cover all publications.
- **Exact statements that could go public:**
  - f(15)=9, f(16)=9, f(17)=10, f(18)=10, f(19)=11.
  - f(20)=12, given Bhattacharjee–Mandal–Bhattacharya's computer-assisted Lemma (Twenty levels) in the revised manuscript; unconditionally 11 ≤ f(20) ≤ 12.
  - The upper bounds come from rank colourings with the six words above, read by set size 0..n.
  - The odd lower bounds come from the chain-exchange lemma plus an exhaustive check of all balanced rank words. They were already public via prop:flower and the omega note.
- **Did this job find something new?** It is a referee, so no new mathematics. The values it confirms, the upper bounds that make them exact, are not public as of today.
- **Gaps and limitations:**
  - My exact search is the same weighted-poset enumeration as the producer's, written independently from the mathematics. Its correctness rests on the completeness proof in (b) and brute-force agreement at n ≤ 6, not on a second algorithm.
  - The f(20) lower bound has the dependency described above.
  - The manuscript is not journal-refereed.

## Caveats and failures

1. **f(20) only.** The lower bound 12 depends on BMB `lem:window20`, a computer-assisted lemma in an unrefereed manuscript (Erdos.tex:1711–1825; producer REPORT.md:14, REPORT.md:16, PROOF.md:73). I replayed the authors' C checker (PASS) and their corruption controls, read the reduction without finding a gap, and checked its size-colouring case with my own code. I did not write an independent implementation of its mixed-level case analysis. Without it, 11 ≤ f(20) ≤ 12.
2. **All six, minor.** The exactness of the upper bounds rests on one algorithm (exhaustive weighted-poset enumeration, PROOF.md:19–28), proved complete in (b), validated by brute force at n ≤ 6, and independently implemented. There is no second exact method such as SAT at n = 15..20.

No value fails.

VERDICT: HOLDS WITH CAVEATS
