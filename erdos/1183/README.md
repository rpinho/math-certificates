# Erdős #1183: candidate exact values f(11)=7 and f(12)=7

This packet gives the two finite equalities **f(11)=7** and **f(12)=7**, with explicit colourings, regenerable SAT queries and checkable DRAT certificates. Both supplied clean-room AI referee verdicts are **HOLDS**. These are candidate results with **no human review**. They do not settle the asymptotic problem.

## Definition

The [problem page](https://www.erdosproblems.com/1183) defines the function as follows:

> Let $f(n)$ be maximal such that in any $2$-colouring of the subsets of $\{1,\ldots,n\}$ there is always a monochromatic family of at least $f(n)$ sets which is closed under taking unions and intersections. Estimate $f(n)$.

The [Bhattacharjee–Mandal–Bhattacharya paper](https://github.com/anaxia-research/Erdos-1183/blob/587d4b9cf88575a474777743ed71e2863c7c2cf6/paper/Erdos.tex) defines

$$f(n)=\min_\chi\max\{|\mathcal L|:\mathcal L\subseteq 2^{[n]}\text{ is a monochromatic sublattice}\},$$

with the minimum over all two-colourings, and states:

> The family $\mathcal F$ is union-closed if $A\cup B\in\mathcal F$ whenever $A,B\in\mathcal F$, and it is a sublattice if it is closed under both union and intersection.

A family is nonempty and closed under binary operations; it need not contain the ambient empty set or full set. The separate union-only function F(n) is outside these claims.

## Certificates and conclusions

For each construction, colour a set S by the bit at position |S| of the rank word, starting at position zero. Full mask-indexed colourings are in [n11](certificates/n11_coloring.json) and [n12](certificates/n12_coloring.json); bit i of a mask denotes element i+1.

| n | Rank word, ranks zero through n | Lower bound | Upper bound |
|---|---|---|---|
| 11 | `100010011101` | Published Bhattacharjee–Mandal–Bhattacharya bound f(11)≥7; independently reproduced by the first referee | Neither colour admits a closed family of at least eight sets |
| 12 | `1100101100011` | The thirteen-member maximal chain gives f(12)≥7 | Neither colour admits a closed family of at least eight sets |

The producer supplies one UNSAT proof for each colour at each dimension. The second construction uses ordinary lexicographic symmetry clauses in colour zero; its colour-one query and both first-construction queries use no symmetry clauses. Some formats in this packet are SAT encodings whose correspondence to the statement is argued in [PROOF.md](PROOF.md). An UNSAT log alone is insufficient: check the DRAT proof against the exact regenerated CNF.

The [first referee](referee/n11/REFEREE.md) and [second referee](referee/n12/REFEREE.md) independently concluded that the finite equalities hold. These were clean-room AI referees from a different model family than the producer, as specified in the supplied job records. They wrote their own encoders and checked their own proofs. Both also supplied exact weighted-poset arguments; the second referee's argument proves the upper bound without SAT. Their original reports and scripts are preserved. The second referee's separate prior-art file and ledger verdict were absent from the supplied directory; its prior-art account and verdict remain in its original report.

## Checking

Start with [REPRODUCE.md](REPRODUCE.md). It gives the source-build pins, byte-for-byte CNF regeneration commands, lightweight colouring checks, referee computations and proof checks. [ASSETS.json](ASSETS.json) identifies the four producer proofs, their compressed release assets and all hashes. [VERIFY.md](VERIFY.md) explains downloading and checking those assets. Large CNFs and DRAT proofs are deliberately separate from the source packet.

Did this packaging job find something new? **No.** It packages two previously produced and refereed candidate finite values. The supplied priority searches found these finite questions open; this is bounded evidence, not a guarantee of priority. See [PRIOR_ART.md](PRIOR_ART.md).

## Credit and references

Credit Erdős and Ulam for the question; Bhattacharjee–Mandal–Bhattacharya for the published lower bound and membership-closure SAT method; the omega institute for its lower-bound note and explicit list of open finite cases; ipezygj for the SAT + DRAT approach that motivated this work; and the authors of CaDiCaL and drat-trim. The constructions, producer checkers and independent referee code were written by AI agents. [CREDITS.md](CREDITS.md) distinguishes those roles. The earlier #609 reproduction is recorded only as a [short note](NOTES_609.md); no third-party research code or data from that reproduction is included.

- [Erdős problem #1183](https://www.erdosproblems.com/1183), statement and [discussion](https://www.erdosproblems.com/forum/discuss/1183).
- Deep Bhattacharjee, Priyabrata Mandal and Ushashi Bhattacharya, [Resolving Erdős-Ulam Monochromatic Union-Closed Family Conjectures](https://arxiv.org/abs/2610.02833v1); [pinned current paper](https://github.com/anaxia-research/Erdos-1183/blob/587d4b9cf88575a474777743ed71e2863c7c2cf6/paper/Erdos.tex) and [earlier finite table](https://github.com/anaxia-research/Erdos-1183/blob/59e72f9511286e9e981b86eb3f7f9bc15e8d59ef/paper/Erdos.tex).
- The omega institute, [sublattice chain-bound note and open cases](https://github.com/the-omega-institute/trureturing/blob/c0bb36be76f99139a5068f434597476d4682e29b/Problems/bhattacharjee-mandal-bhattacharya-2026-sublattice-chain-bound-refutation.md).
- ipezygj, [problem #609 SAT + DRAT packet](https://github.com/ipezygj/erdos609-f4/tree/58472a0a0b0cb45a7804b4668011359ccf732689).
- A. Biere et al., [CaDiCaL source](https://github.com/arminbiere/cadical/tree/c60730422e758ef1cebe7aeddf2dda31c996bf04).
- M. Heule et al., [drat-trim source](https://github.com/marijnheule/drat-trim/tree/2e3b2dc0ecf938addbd779d42877b6ed69d9a985).

Models: producer and clean-room referees are AI agents from different model families according to the supplied job specification; exact model identifiers are not attested in the retained reports. Packaging: GPT-6-based Codex.
