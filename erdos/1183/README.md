# Erdős #1183: candidate exact values f(11)=7, f(12)=7, f(13)=8 and f(14)=8

This packet gives the four finite equalities **f(11)=7**, **f(12)=7**, **f(13)=8** and **f(14)=8**, with explicit colourings, regenerable SAT queries and checkable DRAT certificates. The supplied clean-room AI agents acting as referees conclude **HOLDS** for all four values. These are candidate results with **no human review**. They do not settle the asymptotic problem.

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

The producer supplies one UNSAT proof for each colour at each dimension. The second construction uses ordinary lexicographic symmetry clauses in colour zero; its colour-one query and both first-construction queries use no symmetry clauses. The CNFs are SAT encodings whose correspondence to the statement is argued in [PROOF.md](PROOF.md). An UNSAT log alone is insufficient: check the DRAT proof against the exact regenerated CNF.

The [first referee](referee/n11/REFEREE.md) and [second referee](referee/n12/REFEREE.md) each concluded that the finite equalities hold. These were clean-room AI agents running on a different model from the producer: the first on another OpenAI model (same provider as the producer), the second on an Anthropic model (a different model family). They wrote their own encoders and checked their own proofs. Both also supplied exact weighted-poset arguments; the second referee's argument proves the upper bound without SAT. Their original reports and scripts are preserved. The second referee's separate prior-art file and ledger verdict were absent from the supplied directory; its prior-art account and verdict remain in its original report.

The [new referee report](referee/n13n14/REFEREE.md), preserved byte-for-byte, concludes **HOLDS** for f(13)=8 and f(14)=8. This clean-room referee was an AI agent on an Anthropic model, a different model family from the producer's. It wrote its own encoder, generated and checked its own proofs, and also gave an exact argument without SAT using weighted posets and Birkhoff's representation theorem. Its [poset search](referee/n13n14/src/poset_search.py), [balanced-word check](referee/n13n14/src/balanced.py) and original [outputs](referee/n13n14/logs/n13_balanced_summary.log) are included. The balanced-word check rejects all 3,432 words with explicit closed families, completing the chain-exchange lower-bound argument. These are computational candidate proofs with **no human review**; the hand reductions are not formalized.

The four new producer queries use the standard transposition lex-leaders in both colours. Their soundness depends on the colouring being size-only. The lower bound at n=13 was already published; the new supplied contribution is the matching upper bound, and likewise at n=14. Eight-member witnesses are included in the colouring files. [PROOF.md](PROOF.md) explains the exact correspondence, symmetry argument and unrestricted lower bounds.

## Checking

Start with [REPRODUCE.md](REPRODUCE.md). It gives the source-build pins, byte-for-byte CNF regeneration commands, lightweight colouring checks, referee computations and proof checks. [ASSETS.json](ASSETS.json) identifies the eight producer proofs, including the four new round-3 assets, their compressed release assets and all hashes. [VERIFY.md](VERIFY.md) explains downloading and checking those assets. Large CNFs and DRAT proofs are deliberately separate from the source packet.

The priority searches found these finite questions open; this is bounded evidence, not a guarantee of priority. See [PRIOR_ART.md](PRIOR_ART.md).

## Credit and references

Credit Erdős and Ulam for the question; Bhattacharjee–Mandal–Bhattacharya for the published lower bound and membership-closure SAT method; the omega institute for its lower-bound note and explicit list of open finite cases; ipezygj for the SAT + DRAT approach that motivated this work; and the authors of CaDiCaL, kissat and drat-trim; Crawford, Ginsberg, Luks and Roy for lex-leader symmetry breaking; and Birkhoff for the finite distributive-lattice representation theorem used by the weighted-poset search. The constructions, producer checkers and clean-room referee code were written by AI agents. [CREDITS.md](CREDITS.md) distinguishes those roles. The earlier #609 reproduction is recorded only as a [short note](NOTES_609.md); no third-party research code or data from that reproduction is included.

- [Erdős problem #1183](https://www.erdosproblems.com/1183), statement and [discussion](https://www.erdosproblems.com/forum/discuss/1183).
- Deep Bhattacharjee, Priyabrata Mandal and Ushashi Bhattacharya, [Resolving Erdős-Ulam Monochromatic Union-Closed Family Conjectures](https://arxiv.org/abs/2610.02833v1); [pinned current paper](https://github.com/anaxia-research/Erdos-1183/blob/2842ef3a58604a8f4b35271d5753c2bf9bdecd0b/paper/Erdos.tex) and [earlier finite table](https://github.com/anaxia-research/Erdos-1183/blob/59e72f9511286e9e981b86eb3f7f9bc15e8d59ef/paper/Erdos.tex).
- The omega institute, [sublattice chain-bound note and open cases](https://github.com/the-omega-institute/trureturing/blob/c0bb36be76f99139a5068f434597476d4682e29b/Problems/bhattacharjee-mandal-bhattacharya-2026-sublattice-chain-bound-refutation.md).
- ipezygj, [problem #609 SAT + DRAT packet](https://github.com/ipezygj/erdos609-f4/tree/58472a0a0b0cb45a7804b4668011359ccf732689).
- A. Biere et al., [CaDiCaL source](https://github.com/arminbiere/cadical/tree/c60730422e758ef1cebe7aeddf2dda31c996bf04).
- A. Biere et al., [kissat source](https://github.com/arminbiere/kissat/tree/8af8e56f174b778aef3aa45af9f739b2a5f492c2).
- Crawford, Ginsberg, Luks and Roy, “Symmetry-Breaking Predicates for Search Problems,” KR 1996, pp. 148–159.
- Garrett Birkhoff, “Rings of sets,” Duke Mathematical Journal 3 (1937), pp. 443–454 (finite distributive-lattice representation).
- M. Heule et al., [drat-trim source](https://github.com/marijnheule/drat-trim/tree/2e3b2dc0ecf938addbd779d42877b6ed69d9a985).

Models (from the launcher records): GPT-6.1 Sol via Codex (producer: search, encodings, proofs, checkers and packaging); GPT-6 Astra via Codex (n=11 referee); Claude Opus 5.5 via Claude Code (n=12 referee and n=13/n=14 referee).
