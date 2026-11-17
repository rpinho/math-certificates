Shipped: referee report on the candidate values f(21)=12, f(22)=13 (conditional on BMB lem:window20), 13≤f(23)≤14 and f(24)=14 for Erdős #1183. All four hold as stated, with the caveats listed at the end.

Referee job e1183n2124_referee, 17 Nov 2026. I wrote all the code here myself: `src/wp.c` (exact weighted-poset search; every positive witness is converted to coordinate masks and checked by direct pairwise closure), `src/brute.c` (all sublattices of 2^[n], n≤6), `src/check_witnesses.py` (direct closure check of the producer's families) and `src/words12.py`. I did not read, import or run any code from ../e1183n21, ../e1183n15, ../e1183n1314_referee/src or ../e1183n1520_referee/src. I used ../e1183n21/certificates/upper_n2{1,2,3,4}.json as data only (words and witness masks), and the word list in ../e1183n1520_referee/out/max_words.txt as data for the n=11..20 controls. Raw outputs are in `out/`. Fetched sources are in `sources/` and `ext/window20/`, with SHA256SUMS.

Convention: a rank word W of length n+1 colours every k-set of [n] with W[k], with the first letter for rank 0.

**Summary.** I checked both colours of all four best words by direct closure and with my own exact search: n=21 12/12, n=22 13/13, n=23 14/14, n=24 14/14. The odd lower bounds 12 (n=21) and 13 (n=23) follow from the chain-exchange lemma, which I re-derived, and my own check of all 705,432 and 2,704,156 balanced words. They are also public through BMB prop:flower and the omega note. f(24)≥14 is BMB prop:flower, an elementary proof that I checked step by step and that does not use lem:window20. f(22)≥13 needs BMB thm:f20 and hence the computer-assisted lem:window20. I replayed the authors' checker (PASS, with all three corruptions rejected) and checked its size-only case with my own code, but I did not re-implement its mixed-level case. Without it, 12≤f(22)≤13. My own exhaustive rank-word screen confirms that no size-only colouring of 2^[23] has maximum 13. So f(23) stays open between 13 and 14; settling it needs a non-rank construction or a new lower-bound argument.

## Sources (fetched 17 Nov 2026, ~19:40 UTC)

- **erdosproblems.com/1183** (`sources/erdos1183.html`): "Let $f(n)$ be maximal such that in any $2$-colouring of the subsets of $\{1,\ldots,n\}$ there is always a monochromatic family of at least $f(n)$ sets which is closed under taking unions and intersections. Estimate $f(n)$." It also defines F(n) for union-closed families. Status: open, with the question "estimate f(n)". The page says "It is trivial that $f(n)\geq \frac{n+1}{2}$ … This seems to be all that they knew". It lists one proof claim, by BMB (submitted 2026-10-05), about the asymptotic F(n) conjectures, and 11 comments. The forum thread (`forum1183.html`) and the proof-claims page (`forum_proofclaims.html`) contain no value of f(n) for n≥21.
- **BMB arXiv:2610.02833** (`arxiv_abs.html`, `arxiv_v1.html`): only v1 exists. It contains the chain bound and asks whether ⌈(n+1)/2⌉ is sharp. I searched the v1 HTML: it contains neither prop:flower nor the twelve-level window. Those are only in the revised manuscript.
- **Revised manuscript**: anaxia-research/Erdos-1183 `paper/Erdos.tex` at commit 2842ef3a (2026-10-14). That commit is still HEAD; the HEAD and pinned files are byte-identical (`sources/Erdos_HEAD.tex`, `sources/Erdos_2842ef3a.tex`).
  - `prop:flower` (Erdos.tex:1657–1662): "Let $n\ge1$ and $q=\lfloor(n+1)/12\rfloor$. Every $2$-colouring of $2^{[n]}$ has a red--blue pair of size at least $n+1+q$. Consequently $f(n)\ge\lceil(n+1+q)/2\rceil$."
  - `thm:f20` (Erdos.tex:1695–1703): "Let $n\ge1$, write $n+1=20q+r$ with $0\le r\le19$, and put $e=1$ if $r\ge12$ and $e=0$ otherwise. Every $2$-colouring of $2^{[n]}$ has a red--blue pair of size at least $n+1+2q+e$. Consequently $f(n)\ge\lceil(n+1+2q+e)/2\rceil\ge 11n/20$." Erdos.tex:1705–1709 adds: "it is larger for $n=20$, for $n=22$ and for every $n\ge110$. Its proof rests on the following lemma … the only result of this paper that depends on a computer calculation."
  - `lem:window20` (Erdos.tex:1711–1715): "Every $2$-colouring of $2^{[19]}$ has a red--blue pair of size at least $22$." Its proof is at Erdos.tex:1724–1817.
  - **Dependency trace.** The proof of prop:flower (Erdos.tex:1664–1683) cites only `lem:window` (1437–1441) and (L1)–(L3). lem:window's proof (1628–1652) cites `lem:adjacent` (1446–1476), `lem:gadgets` (1550–1563) and `lem:words` (1565–1623). None of these refers to lem:window20; the first reference to it comes after prop:flower (1711 onward). The proof of thm:f20 (1819–1836) applies lem:window20 to each 19-coordinate window. **prop:flower does not depend on lem:window20; thm:f20 does.** The manuscript also says (2044–2045) that lem:window, lem:adjacent and prop:flower are formalised in Lean, with lem:window's size-only case checked by a 294-family list (2060–2074). I did not rerun Lean.
  - Issues (`sources/gh_issues.json`): #1–#19 are closed, dated 2026-09-30 to 2026-10-14. #20 ("f(11) = 7 and f(12) = 7", opened 2026-11-16) has one comment (2026-11-17 12:03 UTC) giving f(13)=8 and f(14)=8. Neither mentions n≥21.
- **Omega-institute note** (the-omega-institute/trureturing, `sources/omega.md`): "[proved: Lean `odd_lower_bound`] For every odd n ≥ 11, f(n) ≥ (n+3)/2" (omega.md:123), by the balanced-word rigidity route. That gives 12 at n=21 and 13 at n=23.
- **BLLM** (creelie/eBLLM `sec10d_crossing.tex` at HEAD 241326bb, 2026-11-17 13:13 UTC, `sources/bllm_sec10d_HEAD.tex`): I found no value of f(n) for n≥21 in it.
- **Other 2026 claims**: a GitHub repository search for "erdos 1183" (`sources/gh_code_search.json`) returns only anaxia-research/Erdos-1183 and QuanyuTang/erdos-problem-1183. The latter was updated 2026-03-18 and holds PDFs and a README; I did not read the PDFs. I ran three arXiv API searches (`arxiv_search.xml`, `arxiv_q.xml`, `arxiv_q2.xml`, `arxiv_q3.xml`; Erdős/Ulam/sublattice/1183) and they returned no paper on f(n) for n≥21.

## (a) Definition — PASS

The site's f(n) is the largest m such that every 2-colouring of 2^[n] has a monochromatic family of ≥m sets closed under ∪ and ∩. That equals the minimum over colourings of the largest monochromatic closed family. The family need not contain ∅ or [n]. BMB use the same notion ("sublattice": closed under union and intersection; a red–blue pair gives f(n)≥⌈size/2⌉). The producer's definition (PROOF.md:3; REPORT.md:5) is the same: nonempty families, ∅ and [n] not required. My code uses this definition. Brute force enumerates all nonempty sublattices with no other condition, and its counts 73, 731, 12,084 and 319,987 for n=3..6 (`out/brute_counts.txt`) match the producer's.

## (b) Method, lemma by lemma (PROOF.md)

- **§1 Reduction (PROOF.md:5–15): PASS.** For S∈L and x∈B\A, x∈S ⇔ m(x)⊆S, because m(x) is the intersection of the members containing x. So S=A∪{x: m(x)⊆S}. Every join-irreducible equals some m(x), so all weights are positive. Birkhoff's bijection then gives |S|=a+w(D). The converse realisation on disjoint blocks is injective and preserves ∪ and ∩. The remark that "exactly m" is not equivalent is right: with at most 3 poset elements the possible down-set counts are 1,2,3,4,5,6,8, never 7.
- **§2 Search completeness (PROOF.md:17–28): PASS.** It uses linear extensions; every prefix is a down-set, so pruning an invalid size is sound. All predecessor down-sets I and all weights within the budget are tried, and depth is bounded by positive weights. My `src/wp.c` implements the same scheme independently. Brute force validates it on every rank word and both colours for n=1..6 (`out/brute_n*.txt` vs `out/wp_all_n*.txt`, identical; 252 words).
- **§3 Certificates (PROOF.md:30–34):** not replayed. The clean-room rule bars running the producer's checker, and I did not write a tree checker. My own exact search decides every maximum instead (section c).
- **§4 Symmetries and prunes (PROOF.md:36–44): PASS.** Colour swap is trivial. Complementation exchanges ∪ and ∩ and sends rank k to n−k, so reversal is a symmetry. The chain prune holds because prefix sets [k] give an r-chain. Factor monotonicity holds: S↦[s]∪(s+S) is an injective lattice map that shifts ranks by s, and it needs s+l−1≤n, which holds. My screen uses only colour swap (first letter 0) and prefix pruning (the factor at offset 0).
- **§5 Chain exchange (PROOF.md:46–52): PASS.** For odd n with every monochromatic closed family ≤(n+1)/2, each maximal chain has n+1 members and each colour's subchain is closed, so each colour gets exactly (n+1)/2. Two chains that differ only at rank k through exchange-adjacent k-sets S and T force χ(S)=χ(T). Exchanges connect all k-sets, so the colouring is size-only and balanced. The step from "every balanced word has a family ≥(n+3)/2" to "f(n)≥(n+3)/2" is valid, and only that far, as PROOF.md:52 says.
- **§6 Published lower bounds (PROOF.md:58–73): PASS** for the prop:flower chain; my own re-reading is under (d). The window20 description matches Erdos.tex:1711–1817.
- **§7 Monotonicity f(n)≤f(n+1) (PROOF.md:77): PASS.** Restrict a colouring of 2^[n+1] to the sets avoiding coordinate n+1. A closed family there is closed in the big cube, so every colouring of 2^[n+1] has a monochromatic closed family ≥f(n). The rank-minimum and prefix/suffix statements follow in the same way.
- **§9 Rank colourings at n=23 (PROOF.md:95–99): PASS.** If a length-24 word had value ≤13, its length-23 prefix would also have value ≤13. It would then be a complete-list word with 13-families in both colours, and adding the full set [23] (it contains every member) gives a closed 14-family. My own screen confirms the conclusion directly (section e).
- **One-pivot remark (REPORT.md:61; PROOF.md:101): PASS** under the obvious reading: the colour depends on the size and on whether the set contains the pivot. The layer avoiding the pivot is then a rank colouring of 2^[22], and [23] lies above everything. This is a restricted class and supports no claim.

## (c) Upper bounds — PASS

Witnesses (`out/witness_check.txt`): each family in upper_n21..24.json has 12, 12; 13, 13; 14, 14; 14, 14 members. In each, the masks are distinct, lie inside [n], have the stated colour at every member's rank, and are closed under every pairwise ∪ and ∩.

Exact maxima with my search (`out/best_words_max.txt`). The run raises the threshold until it fails; the failing run is the full search. Each run takes under 10 ms.

| n | word | colour 0 | colour 1 | nodes in the final no-run (0/1) |
|---|---|---|---|---|
| 21 | 0010011100101100011011 | 12 | 12 | 7,137 / 7,147 |
| 21 | 0011001011100010110011 | 12 | 12 | 6,968 / 6,970 |
| 22 | 00100111010011100110100 | 13 | 13 | 14,309 / 9,161 |
| 23 | 001001110010110001101101 | 14 | 14 | 19,198 / 19,820 |
| 24 | 0011010011101001101010010 | 14 | 14 | 39,675 / 21,682 |

So f(21)≤12, f(22)≤13, f(23)≤14 and f(24)≤14. The upper bounds depend only on the explicit families (for "≥") and my exact search (for "no larger family"). The value of each colouring is the larger of its two colour maxima, and for the upper bound on f only the witnessed colouring matters. The search is validated by brute force for all words at n≤6. It also reproduces the known maxima of the n=11..20 words (7/7, 7/7, 8/7, 8/8, 9/8, 9/9, 10/10, 10/10, 11/11, 12/12), which match ../e1183n1520_referee/out/max_words.txt.

## (d) Lower bounds

- **n=21, f≥12: PASS without BMB.** Chain exchange (above) plus `wp balanced 21` over all C(22,11)=705,432 balanced words. Every word has a family of ≥12 in some colour, and each witness was converted to masks and checked by direct closure. There were 0 failures (`out/bal_n21_p*.txt`, 0.4 s). The same bound comes from prop:flower (q=1: ⌈23/2⌉=12) and from the omega note.
- **n=23, f≥13: PASS without BMB.** The same check over all C(24,12)=2,704,156 balanced words found ≥13 every time, with 0 failures (`out/bal_n23_p*.txt`, 2.2 s). prop:flower (q=2: ⌈26/2⌉=13) and the omega note give it too.
- **n=22, f≥13: CONDITIONAL on lem:window20.** thm:f20 at n=22 has n+1=23=20·1+3, so q=1, r=3, e=0. A 19-coordinate window with a pair ≥22 (lem:window20) plus the 3 chain sets S_20, S_21, S_22 gives 25, so f(22)≥13. I checked this arithmetic and the stacking proof (Erdos.tex:1819–1836) and they are correct. prop:flower gives only 12 here (q=1: ⌈24/2⌉=12), and n is even, so chain exchange does not apply.
  - Authors' checker (`ext/window20/check_window.c` and the lists at 2842ef3a): I read it (it only opens its argument file), compiled it and ran it (`out/window20_replay.txt`). certs_11.txt: PASS, 288 certificates. certs_19_22.txt: "m=19 K=22 band=8,9,10,11: 63272 certificates, 5308416 patterns, 242 settled by pivots, 708872 word choices, least pair 22 / PASS". All three corruptions from their run_checks.sh are rejected: K=23 → "level outside the band not settled"; pivots removed → "pattern below the bound"; a member removed → "not a sublattice". I did not run their C++, Python, Julia or Lean versions.
  - My own check of the size-only case of lem:window20: over all 2^20 rank words of 2^[19] (first letter fixed; colour swap covers the rest), min(max0, 22)+min(max1, 22) ≥ 22. The least capped sum is exactly 22 (`out/splitsum_n19.log`, 175 s on 4 cores). Control at m=11: the least sum is 13, and 13 is tight (`wp splitsum 11 0 1 14` returns 13).
  - The mixed-level reduction (Erdos.tex:1724–1817) and its 63,272-family case analysis were not re-implemented. The confidence in it rests on the authors' self-certifying list (every family is checked to be a sublattice) plus the authors' case logic, which I replayed and did not rewrite.
  - **Without lem:window20: 12≤f(22)≤13.** The 12 comes from prop:flower and also, independently of BMB, from f(22)≥f(21)=12 by monotonicity. My screen shows every *size-only* colouring of 2^[22] has value ≥13 (section e), so any colouring with value 12 at n=22 would have to be non-rank.
- **n=24, f≥14: PASS via prop:flower, without lem:window20.** q=⌊25/12⌋=2, so the pair is ≥25+2=27 and f≥14. I re-read the chain step by step:
  - (L1)–(L3) are standard.
  - lem:adjacent (1453–1476): the minimal-distance exchange argument is correct, and the m-member chain through S∩T and S∪T plus S on the red side and T on the blue side gives m+2.
  - lem:gadgets: my exact search on each of the eight table words gives a colour-R maximum of 4, 4, 4, 6, 6, 8, 8, 8 against R-counts 3, 3, 3, 5, 5, 6, 6, 5, so each table word is beaten (`out/words12.txt`).
  - lem:words: all 4,096 length-12 words contain a forbidden block (0 missing). The paper's length-11 counterexample RRBRBBRRBBR is confirmed (4 length-11 words avoid every block).
  - lem:window (1628–1652): the mixed and pure cases are correct, and the embedded gadget with outside chain sets is closed by (L2).
  - prop:flower's stacking (1664–1683): W_j⊆[n] because 12q−1≤n; the windows' rank ranges [12j,12j+11] and the tail chain are disjoint and pairwise nested, so the count 13q+(n+1−12q) is right.
  - thm:f20 also gives 14 (q=1, r=5, ⌈27/2⌉=14), but it is not needed.

## (e) n=23: no size-only colouring has maximum 13 — ESTABLISHED (rank restriction only)

`wp screen` runs a DFS over words with first letter 0 (colour swap covers the rest). It extends prefixes one letter at a time and keeps a prefix only if both colours have an exact maximum ≤T at its own cube. Pruning is justified by factor monotonicity at offset 0: a family in a prefix's cube embeds unchanged in every extension's cube, with the same ranks. All length-12 prefixes are themselves checked at every length 1..12. No symmetry other than colour swap is used, and no intermediate prefix is discarded on symmetry grounds. Results (`out/screen_T1{1,2,3,4}_*`, `out/screen_n21_T11_*`):

| T | survivors (first letter 0) by n | consistent with |
|---|---|---|
| 11 | n=19: 17; n=20: 0; n=21: 0 | known rank minimum 12 at n=20 |
| 12 | n=21: 2 (0010011100101100011011, 0011001011100010110011); n=22: 0 | producer: 2 orbits / 4 words at n=21; rank minimum ≥13 at n=22 |
| 13 | n=22: 14 (all with exact maxima 13/13, `out/controls.txt`); **n=23: 0** | producer: 7 orbits / 28 words at n=22 |
| 14 | n=23: 268; n=24: 2 (the best word and its reversal) | producer: 536 words at n=23 and 4 words / 1 orbit at n=24 |

So the rank-colouring minimum is exactly 12, 13, 14, 14 at n=21..24. The minimum is ≥ these values by the screen, and the best words attain them. **What is established about f(23): 13≤f(23)≤14, and no size-only colouring attains 13.** What is not established: whether some non-size-only colouring of 2^[23] has maximum 13. Neither the producer nor I searched non-rank colourings, and chain exchange only forces rank colourings under the hypothesis "max ≤12".

## (f) Controls — PASS

- Brute force vs my search: identical for every rank word and both colours at n=1..6.
- Known families: my search reproduces the n=11..20 maxima, and each run's witness passes a direct closure check inside `wp`. The splitsum overflow below shows that this check does trip when something is wrong.
- Corrupted witnesses (`out/witness_check.txt`): flipping one coordinate of one member of each of the 8 producer families is always rejected (wrong colour or not closed). Dropping the top member gives either a non-closed family or a smaller valid one, as expected. Flipping the word's last letter rejects every family that uses the full set.
- Single-letter flips of each best word (`out/controls.txt`): every one of the 22+23+24+25 flips strictly raises the value. The minimum over flips is 14 at n=21, 14 at n=22, 15 at n=23 and 17 at n=24. This is consistent with the screen, where the only value-T words are the listed survivors.
- Two bugs in my own code were caught and fixed before any result was taken:
  - The first screen null-terminated the shared prefix buffer, so every word looked good. The counts doubled at each length, which gave it away. I fixed it, re-ran, and checked the corrected screen against the known n=20 minimum.
  - Uncapped `exact_max` overflowed the down-set buffer on all-one-colour words. The direct witness check aborted the run. I capped it. The buffer never exceeded 136 entries in the reported runs.

## (g) Novelty, public statements, gaps

- **Public before 17 Nov 2026?** The *lower* bounds 12, 13, 13, 14 at n=21..24 are implied by public results: BMB thm:f20 and prop:flower in the revised manuscript of 2026-10-14, and for odd n the omega note. The *upper* bounds 12, 13, 14, 14 (the four colourings) and hence the exact values were not found in any source I checked: erdosproblems.com/1183 with its forum and proof claims, the anaxia-research/Erdos-1183 manuscript and all its issues including #20 (which stops at f(14)), the arXiv listing and API searches, creelie/eBLLM at HEAD, the omega note, and a GitHub repository search. Checks were made 17 Nov 2026, ~19:40 UTC. The search is bounded: I did not read the QuanyuTang PDFs or search X, Reddit or Discord. So the answer to "new?" is **yes**: exact values beyond the public n≤20 table, under the site's definition.
- **Statements that would go public:**
  - f(21)=12. Upper bound: the size colouring 0010011100101100011011 (both colours max 12). Lower bound: BMB prop:flower, the omega note, or chain exchange plus a check of all balanced words.
  - 12≤f(22)≤13, and f(22)=13 assuming BMB's computer-assisted lem:window20. Upper bound: 00100111010011100110100.
  - 13≤f(23)≤14. Upper bound: 001001110010110001101101. No size-only colouring of 2^[23] attains 13.
  - f(24)=14. Upper bound: 0011010011101001101010010. Lower bound: BMB prop:flower.
- REPORT.md:81–88 compares the new upper bounds with BMB's printed asymptotic upper formula (463, 496, …) and an "inherited" 12·2^(n−20). These are weak comparators and are not needed. The real contribution is the exact values themselves.

## Caveats (apply to the claims named)

1. **f(22)=13** depends on BMB lem:window20 (Erdos.tex:1711–1817), a computer-assisted lemma in an unrefereed manuscript. I replayed the authors' C checker and confirmed the size-only case with my own code. I did not independently implement the mixed-level case. The producer states the condition correctly (REPORT.md:1, REPORT.md:12). Without the lemma, 12≤f(22)≤13.
2. **f(24)=14** rests on BMB prop:flower (Erdos.tex:1657–1683), which is only in the revised GitHub manuscript at 2842ef3a, not arXiv v1, and has not been refereed by a journal. I checked its elementary proof chain and its two finite lemmas myself (REPORT.md:14; PROOF.md:62–68). It does not depend on lem:window20. The Lean formalisation the manuscript cites (Erdos.tex:2044–2045) was not rerun.
3. **All four claims**: the exact maxima and the rank screens rest on my own search code (`src/wp.c`), validated by brute force at n≤6 and by known values. I did not replay the producer's No-trees (REPORT.md:18–21). Both the producer and I are AI agents in the same lane, and no human has checked these results.
4. **13≤f(23)≤14**: the rank restriction is settled (minimum 14), but the unrestricted value is open (REPORT.md:13; PROOF.md:99).

VERDICT: HOLDS WITH CAVEATS
