# Erdős #1183: candidate values through f(24), with dependencies at f(20) and f(22)

The original packet gives the four finite equalities **f(11)=7**, **f(12)=7**, **f(13)=8** and **f(14)=8**, with explicit colourings, regenerable SAT queries and checkable DRAT certificates. The supplied clean-room AI agents acting as referees conclude **HOLDS** for all four values. These are candidate results with **no human review**. The extension gives **f(15)=9, f(16)=9, f(17)=10, f(18)=10, f(19)=11** and **f(20)≤12**. The equality **f(20)=12** uses BMB `lem:window20` via `thm:f20`; without that dependency, **11≤f(20)≤12**. The extension’s clean-room referee concludes **HOLDS WITH CAVEATS**. Round 5 adds **f(21)=12**, **f(24)=14**, **f(22)≤13** (equality given BMB `lem:window20`) and **13≤f(23)≤14**. Unconditionally **12≤f(22)≤13**; the rank-colouring minimum at n=23 is exactly **14**. These finite results do not settle the asymptotic problem.

**Priority.** The exact values of f(n) for every n up to twenty were already stated by Deep Bhattacharjee and Ushashi Bhattacharya in their BLLM manuscript (Theorem `fvalues`, using the same weighted-poset reduction as its Lemma `levelposet`), [public in creelie/eBLLM](https://github.com/creelie/eBLLM/blob/241326bbba4726afde74ae1858265878b2176c59/paper/bllm/paper/sections/sec10d_crossing.tex) and present in that file since its commit of 19 October 2026. We missed it in our earlier searches. Our values from eleven to twenty are therefore reproductions, found separately and published with certificates (SAT/DRAT proofs from eleven to fourteen, replayable proof trees from fifteen to twenty); earlier versions of this packet wrongly said that exact values were known only up to ten. The values from twenty-one to twenty-four go beyond that manuscript. The odd-n lower bound used here is also proved in Lean 4 by the OpenRefute project, as BLLM cites.

## Definition

The [problem page](https://www.erdosproblems.com/1183) defines the function as follows:

> Let $f(n)$ be maximal such that in any $2$-colouring of the subsets of $\{1,\ldots,n\}$ there is always a monochromatic family of at least $f(n)$ sets which is closed under taking unions and intersections. Estimate $f(n)$.

The [Bhattacharjee–Mandal–Bhattacharya paper](https://github.com/anaxia-research/Erdos-1183/blob/2842ef3a58604a8f4b35271d5753c2bf9bdecd0b/paper/Erdos.tex) defines

$$f(n)=\min_\chi\max\{|\mathcal L|:\mathcal L\subseteq 2^{[n]}\text{ is a monochromatic sublattice}\},$$

with the minimum over all two-colourings, and states:

> The family $\mathcal F$ is union-closed if $A\cup B\in\mathcal F$ whenever $A,B\in\mathcal F$, and it is a sublattice if it is closed under both union and intersection.

A family is nonempty and closed under binary operations; it need not contain the ambient empty set or full set. The separate union-only function F(n) is outside these claims.

## Certificates and conclusions

For each construction, colour a set S by the bit at position |S| of the rank word, starting at position zero. Full mask-indexed colourings are in [n11](certificates/n11_coloring.json), [n12](certificates/n12_coloring.json), [n13](certificates/n13_coloring.json) and [n14](certificates/n14_coloring.json); bit i of a mask denotes element i+1.

| n | Rank word, ranks zero through n | Lower bound | Upper bound |
|---|---|---|---|
| 11 | `100010011101` | Published Bhattacharjee–Mandal–Bhattacharya bound f(11)≥7; also reproduced by the first referee | Neither colour admits a closed family of at least eight sets |
| 12 | `1100101100011` | The thirteen-member maximal chain gives f(12)≥7 | Neither colour admits a closed family of at least eight sets |
| 13 | `11001011000110` | Published Bhattacharjee–Mandal–Bhattacharya Proposition `prop:flower` and the omega institute note give f(13)≥8; the referee also re-derived it by chain exchange and all 3,432 balanced rank words | Neither colour admits a closed family of at least nine sets |
| 14 | `110010110001101` | The fifteen-set maximal chain gives f(14)≥8 | Neither colour admits a closed family of at least nine sets |
| 15 | `1100101100011010` | 9: chain-exchange lemma plus all 12,870 balanced words; also BMB `prop:flower` | Both colour maxima are at most 9; f(15)≤9 |
| 16 | `00100111010011001` | 9: the seventeen-set maximal chain | Both colour maxima are at most 9; f(16)≤9 |
| 17 | `110010110001101001` | 10: chain-exchange lemma plus all 48,620 balanced words; also BMB `prop:flower` | Both colour maxima are at most 10; f(17)≤10 |
| 18 | `0010110011101001100` | 10: the nineteen-set maximal chain | Both colour maxima are at most 10; f(18)≤10 |
| 19 | `00110010111000101101` | 11: chain-exchange lemma plus all 184,756 balanced words; also BMB `prop:flower` | Both colour maxima are at most 11; f(19)≤11 |
| 20 | `110010110001101100110` | 11: chain (also `prop:flower`); 12 given BMB `thm:f20` through computer-assisted `lem:window20` | Both colour maxima are at most 12; f(20)≤12 |
| 21 | `0010011100101100011011` | 12: chain-exchange lemma plus all balanced words; also BMB `prop:flower` | Exact colour maxima 12/12; f(21)≤12 |
| 22 | `00100111010011100110100` | 12 unconditionally; 13 from BMB `thm:f20` via computer-assisted `lem:window20` | Exact colour maxima 13/13; f(22)≤13 |
| 23 | `001001110010110001101101` | 13: chain-exchange lemma plus all balanced words; also BMB `prop:flower` | Exact colour maxima 14/14; f(23)≤14 |
| 24 | `0011010011101001101010010` | 14: BMB `prop:flower`, without `lem:window20` | Exact colour maxima 14/14; f(24)≤14 |

For n=11..14 the producer supplies one UNSAT proof for each colour at each dimension. The second construction uses ordinary lexicographic symmetry clauses in colour zero; its colour-one query and both first-construction queries use no symmetry clauses. The CNFs are SAT encodings whose correspondence to the statement is argued in [PROOF.md](PROOF.md). An UNSAT log alone is insufficient: check the DRAT proof against the exact regenerated CNF.

The [first referee](referee/n11/REFEREE.md) and [second referee](referee/n12/REFEREE.md) each concluded that the finite equalities hold. These were clean-room AI agents running on a different model from the producer: the first on another OpenAI model (same provider as the producer), the second on an Anthropic model (a different model family). They wrote their own encoders and checked their own proofs. Both also supplied exact weighted-poset arguments; the second referee's argument proves the upper bound without SAT. Their original reports and scripts are preserved. The second referee's separate prior-art file and ledger verdict were absent from the supplied directory; its prior-art account and verdict remain in its original report.

The [new referee report](referee/n13n14/REFEREE.md), preserved byte-for-byte, concludes **HOLDS** for f(13)=8 and f(14)=8. This clean-room referee was an AI agent on an Anthropic model, a different model family from the producer's. It wrote its own encoder, generated and checked its own proofs, and also gave an exact argument without SAT using weighted posets and Birkhoff's representation theorem. Its [poset search](referee/n13n14/src/poset_search.py), [balanced-word check](referee/n13n14/src/balanced.py) and original [outputs](referee/n13n14/logs/n13_balanced_summary.log) are included. The balanced-word check rejects all 3,432 words with explicit closed families, completing the chain-exchange lower-bound argument. These are computational candidate proofs with **no human review**; the hand reductions are not formalized.

The four new producer queries use the standard transposition lex-leaders in both colours. Their soundness depends on the colouring being size-only. The lower bound at n=13 was already published; the new supplied contribution is the matching upper bound, and likewise at n=14. Eight-member witnesses are included in the colouring files. [PROOF.md](PROOF.md) explains the exact correspondence, symmetry argument and unrestricted lower bounds.

## Extension to n=15..20

The six full mask-indexed colourings are [n15](certificates/n15_coloring.json), [n16](certificates/n16_coloring.json), [n17](certificates/n17_coloring.json), [n18](certificates/n18_coloring.json), [n19](certificates/n19_coloring.json) and [n20](certificates/n20_coloring.json). Each includes the rank word and explicit maximum witnesses for both colours. Original results and proof filenames are in [results.json](producer/n15n20/certificates/results.json).

The upper-bound method is exact weighted-poset search using Birkhoff’s representation theorem, with replayable exhaustive proof trees, a separately written producer tree checker and brute-force validation. No SAT is used at these sizes. The [search](producer/n15n20/src/poset.cpp) and [tree checker](producer/n15n20/src/check.py) are separate implementations by the same producer; packaging replay is not another clean-room review. All twelve headline proof trees are included. The larger optional archive for exhaustive rank-minimum screens is a release asset; it is unnecessary for the six unrestricted upper bounds.

The byte-preserved [clean-room referee report](referee/n15n20/REFEREE.md) concludes **HOLDS WITH CAVEATS**. Its two caveats are: (1) the f(20) lower bound of twelve depends on BMB’s computer-assisted `lem:window20` in an unrefereed manuscript; the referee replayed the authors’ checker and corruption controls but did not reimplement the mixed-level case analysis; (2) all six upper bounds use the same weighted-poset enumeration algorithm, written separately by producer and referee and validated against brute force through n=6, with no second exact method at these sizes. Thus, withholding the lemma gives **11≤f(20)≤12**. No value fails the referee’s checks.

The referee’s own scripts and outputs are in [referee/n15n20](referee/n15n20). The authors’ third-party window checker and lists are not bundled: see the pinned references and recorded replay in [WINDOW20.md](referee/n15n20/WINDOW20.md). The ordinary maximal-chain argument proves the even lower bounds; the chain-exchange lemma and complete balanced-word witness lists prove the odd lower bounds. Those lower bounds were already published; the matching finite upper bounds are the supplied contribution. These remain **candidate** results with **no human review**.

## Extension to n=21..24

The four colourings are encoded exactly by their rank words in [n21](certificates/n21_coloring.json), [n22](certificates/n22_coloring.json), [n23](certificates/n23_coloring.json) and [n24](certificates/n24_coloring.json). A set's colour is the bit at its cardinality; these compact encodings specify every set without a redundant mask-indexed array. Both maximum families and links to both exhaustive no-trees are included in each file. Exact maxima are **12/12, 13/13, 14/14, 14/14**, respectively. All eight headline trees are in [producer/n21n24/certificates](producer/n21n24/certificates), each below 20 MB. The [search](producer/n21n24/src/poset.cpp), [separately written tree checker](producer/n21n24/src/check.py), [coverage checker](producer/n21n24/src/coverage.py), complete segmented rank screens, and saved G_L(T) word lists are included. These lists are inputs for later work; no non-rank search is claimed here.

The lower bounds at n=21 and n=23 follow from our chain-exchange lemma plus concrete closed families for **705,432** and **2,704,156** balanced words, respectively; BMB `prop:flower` and the omega note also supply them. At n=22, BMB `thm:f20` gives 13 using its computer-assisted `lem:window20`. The referee replayed the authors' checker and its three corruption controls but did not reimplement its mixed-level logic. Thus **f(22)=13 given that lemma; without it, 12≤f(22)≤13**. At n=24, BMB `prop:flower` gives 14 using the twelve-level window and separated stacking; it does **not** use `lem:window20`. The dependency trace is in [PROOF.md](PROOF.md).

At n=23, **13≤f(23)≤14**, while the rank-colouring minimum is **exactly 14**. This is the first n where size-only colourings miss the stated best lower bound. Every optimal n=22 rank word has a 13-member family in both colours; appending the full 23-set in its colour forces a 14-member family. The complete rank screen confirms this directly. This proves no unrestricted lower bound of 14. The unrestricted gap remains open; no non-rank construction was searched.

The byte-preserved [clean-room referee report](referee/n21n24/REFEREE.md) concludes **HOLDS WITH CAVEATS**: all four upper bounds, the odd lower bounds and the n=24 flower argument hold as stated; n=22 equality retains the external computational dependency, and n=23 remains open. The n=24 lower bound is in the revised GitHub manuscript, not arXiv v1; its cited Lean formalisation was not rerun. The referee used its own exact weighted-poset search, checked against brute force through n=6 and known n=11..20 values; it did not replay the producer's trees. Both implementations use the same enumeration method. Packaging replays the producer's trees and every delivered new witness with its packaged checker. All are **candidate** results with **no human review**. The original report's historical terminology is retained verbatim; our description of that review is clean-room.

The referee's [scripts and outputs](referee/n21n24/) include the raw [window20 replay output](referee/n21n24/out/window20_replay.txt). Authors' code and lists are cited by pinned URLs in [WINDOW20.md](referee/n21n24/WINDOW20.md), not bundled. The oversized n=23 balanced-witness list is a release asset at **erdos1183-v4**; [VERIFY.md](VERIFY.md) gives the exact download, hash and replay commands. Headline upper-bound checks need no release download.

## Checking

Start with [REPRODUCE.md](REPRODUCE.md). It gives the source-build pins, byte-for-byte CNF regeneration commands, lightweight colouring checks, referee computations and proof checks. [ASSETS.json](ASSETS.json) identifies the eight producer proofs, including the four new round-3 assets, their compressed release assets and all hashes. [VERIFY.md](VERIFY.md) explains downloading and checking those assets. Large CNFs and DRAT proofs are deliberately separate from the source packet.

The current public BLLM manuscript already gives exact values through n=20 by the same weighted-poset method. The supplied round-5 searches found no n=21..24 upper bounds in the material read; this is bounded evidence, not a guarantee of priority. Packaging itself claims no new mathematics. See [PRIOR_ART.md](PRIOR_ART.md).

## Credit and references

Credit Erdős and Ulam for the question; Bhattacharjee–Mandal–Bhattacharya for the published lower bound and membership-closure SAT method; the omega institute for its lower-bound note and explicit list of open finite cases; ipezygj for the SAT + DRAT approach that motivated this work; and the authors of CaDiCaL, kissat and drat-trim; Crawford, Ginsberg, Luks and Roy for lex-leader symmetry breaking; and Birkhoff for the finite distributive-lattice representation theorem used by the weighted-poset search. The constructions, producer checkers and clean-room referee code were written by AI agents. [CREDITS.md](CREDITS.md) distinguishes those roles. The earlier #609 reproduction is recorded only as a [short note](NOTES_609.md); no third-party research code or data from that reproduction is included.

- [Erdős problem #1183](https://www.erdosproblems.com/1183), statement and [discussion](https://www.erdosproblems.com/forum/discuss/1183).
- Deep Bhattacharjee, Priyabrata Mandal and Ushashi Bhattacharya, [Resolving Erdős-Ulam Monochromatic Union-Closed Family Conjectures](https://arxiv.org/abs/2610.02833v1); [pinned current paper](https://github.com/anaxia-research/Erdos-1183/blob/2842ef3a58604a8f4b35271d5753c2bf9bdecd0b/paper/Erdos.tex) and [earlier finite table](https://github.com/anaxia-research/Erdos-1183/blob/59e72f9511286e9e981b86eb3f7f9bc15e8d59ef/paper/Erdos.tex).
- The omega institute, [sublattice chain-bound note and open cases](https://github.com/the-omega-institute/trureturing/blob/c0bb36be76f99139a5068f434597476d4682e29b/Problems/bhattacharjee-mandal-bhattacharya-2026-sublattice-chain-bound-refutation.md).
- ipezygj, [problem #609 SAT + DRAT packet](https://github.com/ipezygj/erdos609-f4/tree/58472a0a0b0cb45a7804b4668011359ccf732689).
- A. Biere et al., [CaDiCaL source](https://github.com/arminbiere/cadical/tree/c60730422e758ef1cebe7aeddf2dda31c996bf04).
- A. Biere et al., [kissat source](https://github.com/arminbiere/kissat/tree/8af8e56f174b778aef3aa45af9f739b2a5f492c2).
- Crawford, Ginsberg, Luks and Roy, “Symmetry-Breaking Predicates for Search Problems,” KR 1996, pp. 148–159.
- Deep Bhattacharjee and Ushashi Bhattacharya, [BLLM finite-value theorem and weighted-poset method through n=20](https://github.com/creelie/eBLLM/blob/241326bbba4726afde74ae1858265878b2176c59/paper/bllm/paper/sections/sec10d_crossing.tex).
- Garrett Birkhoff, “Rings of sets,” Duke Mathematical Journal 3 (1937), pp. 443–454 (finite distributive-lattice representation).
- M. Heule et al., [drat-trim source](https://github.com/marijnheule/drat-trim/tree/2e3b2dc0ecf938addbd779d42877b6ed69d9a985).

Models (from the launcher records): GPT-6.1 Sol via Codex (producer: search, encodings, proofs, checkers and packaging); GPT-6 Astra via Codex (n=11 referee); Claude Opus 5.5 via Claude Code (n=12, n=13/n=14, n=15..20 and n=21..24 referees).
