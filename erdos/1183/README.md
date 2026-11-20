# Erdős #1183: candidate values through f(24), with dependencies at f(20) and f(22)

The original packet gives the four finite equalities **f(11)=7**, **f(12)=7**, **f(13)=8** and **f(14)=8**, with explicit colourings, regenerable SAT queries and checkable DRAT certificates. The supplied clean-room AI agents acting as referees conclude **HOLDS** for all four values. These are candidate results with **no human review**. The extension gives **f(15)=9, f(16)=9, f(17)=10, f(18)=10, f(19)=11** and **f(20)≤12**. The equality **f(20)=12** uses BMB `lem:window20` via `thm:f20`; without that dependency, **11≤f(20)≤12**. The extension’s clean-room referee concludes **HOLDS WITH CAVEATS**. Round 5 adds **f(21)=12**, **f(24)=14**, **f(22)≤13** (equality given BMB `lem:window20`) and **13≤f(23)≤14**. Unconditionally **12≤f(22)≤13**; the rank-colouring minimum at n=23 is exactly **14**. These finite results do not settle the asymptotic problem.

**Priority.** The exact values of f(n) for every n up to twenty were already stated by Deep Bhattacharjee and Ushashi Bhattacharya in their BLLM manuscript (Theorem `fvalues`, using the same weighted-poset reduction as its Lemma `levelposet`), [public in creelie/eBLLM](https://github.com/creelie/eBLLM/blob/241326bbba4726afde74ae1858265878b2176c59/paper/bllm/paper/sections/sec10d_crossing.tex) and present in that file since its commit of 19 October 2026. Earlier searches for this packet missed it. The packet’s values from eleven to twenty are therefore reproductions, found separately and published with certificates (SAT/DRAT proofs from eleven to fourteen, replayable proof trees from fifteen to twenty); earlier versions of this packet wrongly said that exact values were known only up to ten. The values from twenty-one to twenty-four go beyond that manuscript. The odd-n lower bound used here is also proved in Lean 4 by the OpenRefute project, as BLLM cites.

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

The four colourings are encoded exactly by their rank words in [n21](certificates/n21_coloring.json), [n22](certificates/n22_coloring.json), [n23](certificates/n23_coloring.json) and [n24](certificates/n24_coloring.json). A set's colour is the bit at its cardinality; these compact encodings specify every set without a redundant mask-indexed array. Both maximum families and links to both exhaustive no-trees are included in each file. Exact maxima are **12/12, 13/13, 14/14, 14/14**, respectively. All eight headline trees are in [producer/n21n24/certificates](producer/n21n24/certificates), each below 20 MB. The [search](producer/n21n24/src/poset.cpp), [separately written tree checker](producer/n21n24/src/check.py), [coverage checker](producer/n21n24/src/coverage.py), complete segmented rank screens, and saved G_L(T) word lists are included. These lists are inputs for later work.

The lower bounds at n=21 and n=23 follow from the chain-exchange lemma plus concrete closed families for **705,432** and **2,704,156** balanced words, respectively; BMB `prop:flower` and the omega note also supply them. At n=22, BMB `thm:f20` gives 13 using its computer-assisted `lem:window20`. The referee replayed the authors' checker and its three corruption controls but did not reimplement its mixed-level logic. Thus **f(22)=13 given that lemma; without it, 12≤f(22)≤13**. At n=24, BMB `prop:flower` gives 14 using the twelve-level window and separated stacking; it does **not** use `lem:window20`. The dependency trace is in [PROOF.md](PROOF.md).

At n=23, **13≤f(23)≤14**, while the rank-colouring minimum is **exactly 14**. This is the first n where size-only colourings miss the stated best lower bound. Every optimal n=22 rank word has a 13-member family in both colours; appending the full 23-set in its colour forces a 14-member family. The complete rank screen confirms this directly. This proves no unrestricted lower bound of 14. The unrestricted gap remains open.

The byte-preserved [clean-room referee report](referee/n21n24/REFEREE.md) concludes **HOLDS WITH CAVEATS**: all four upper bounds, the odd lower bounds and the n=24 flower argument hold as stated; n=22 equality retains the external computational dependency, and n=23 remains open. The n=24 lower bound is in the revised GitHub manuscript, not arXiv v1; its cited Lean formalisation was not rerun. The referee used its own exact weighted-poset search, checked against brute force through n=6 and known n=11..20 values; it did not replay the producer's trees. Both implementations use the same enumeration method. Packaging replays the producer's trees and every delivered new witness with its packaged checker. All are **candidate** results with **no human review**. The original report’s historical terminology is retained verbatim. The review was clean-room.

The referee's [scripts and outputs](referee/n21n24/) include the raw [window20 replay output](referee/n21n24/out/window20_replay.txt). Authors' code and lists are cited by pinned URLs in [WINDOW20.md](referee/n21n24/WINDOW20.md), not bundled. The oversized n=23 balanced-witness list is a release asset at **erdos1183-v4**; [VERIFY.md](VERIFY.md) gives the exact download, hash and replay commands. Headline upper-bound checks need no release download.

## Two-block colourings at n=23

For any partition `[23] = A ⊔ B` into two nonempty blocks, every two-colouring determined by `(|S∩A|, |S∩B|)` has a monochromatic sublattice of at least **14 sets**. This covers all eleven splits up to exchanging the blocks and extends the earlier one-pivot exclusion, which is the (22,1) split. The rank word `001001110010110001101101` attains 14 in both colours for every split. The unrestricted interval **13 ≤ f(23) ≤ 14** stays open. A value-13 colouring, if one exists, is not of two-block form for any split. [Two-block proof](producer/two-block/PROOF.md)

The clean-room AI referee concluded that the restricted claim holds. The all-splits LRAT certifies only the final incompatibility of overlapping windows. The witness induction does the elimination by checking explicit closed families and deriving the possible window tables. A separate certificate checks the (21,2) split posed in Bhattacharjee–Bhattacharya’s eBLLM experiment. This is a **candidate** result with **no human review**. Producer GPT-6.2 Astra via Codex and clean-room referee Claude Opus 5.5 are identified in the launcher records. [Original referee report](referee/two-block/REFEREE.md) · [Referee scripts and outputs](referee/two-block/) · [Prior art](PRIOR_ART.md)

From the packet root, with Python 3.10+ and NumPy installed, run:

```sh
(
  cd producer/two-block &&
  nice -n 10 python3 -B src/check_faces.py &&
  nice -n 10 python3 -B src/replay.py &&
  nice -n 10 python3 -B src/upper.py
)
```

The first command checks 86,466 face witnesses, redoes the induction and overlap calculation, regenerates the all-splits CNF and checks its LRAT. The second checks 146,641 physical witnesses, exhausts the row and window tables, regenerates the direct CNF and checks its LRAT. The third checks both size-14 witnesses and both exhaustive no-at-15 trees. The replay requires only the files in this packet. [Producer checkers](producer/two-block/src/)

Two lines of the all-splits LRAT use tabs between tokens. The Python checkers accept them directly. For Lean 4.36.0, restore single spaces into a temporary file before using the included checker:

```sh
(
  set -e
  cd producer/two-block
  w=$(mktemp -d ../../../two-block-lean.XXXXXX)
  awk '{$1=$1; print}' data/all-splits.lrat > "$w/all-splits.lrat"
  nice -n 10 lean --run src/CheckLRAT.lean data/all-splits.cnf "$w/all-splits.lrat"
  nice -n 10 lean --run src/CheckLRAT.lean data/exclusion.cnf data/exclusion.lrat
)
```

The separately written referee checkers also run from the packet root. Use a fresh working directory for their regenerated CNFs:

```sh
(
  set -e
  d=producer/two-block/data
  r=referee/two-block
  w=$(mktemp -d ../two-block-replay.XXXXXX)
  nice -n 10 python3 -B "$r/regen_all.py" "$w/all-splits.cnf"
  cmp "$w/all-splits.cnf" "$d/all-splits.cnf"
  nice -n 10 python3 -B "$r/faces_check.py" "$d/faces.jsonl.gz"
  nice -n 10 python3 -B "$r/excl_check.py" "$d" "$w/exclusion.cnf"
  cmp "$w/exclusion.cnf" "$d/exclusion.cnf"
  nice -n 10 python3 -B "$r/lrat_check.py" "$d/all-splits.cnf" "$d/all-splits.lrat"
  nice -n 10 python3 -B "$r/lrat_check.py" "$d/exclusion.cnf" "$d/exclusion.lrat"
  nice -n 10 python3 -B "$r/upper_check.py" "$d"
)
```

## Three-block colourings at n=23 and n=22

Partition [23] into nonempty blocks A, B and C. If the colour of S depends only on `(|S∩A|, |S∩B|, |S∩C|)`, some monochromatic family of **at least 14 sets** is closed under union and intersection. This holds for all 44 splits a ≥ b ≥ c ≥ 1 with a+b+c=23. The rank word `001001110010110001101101` attains 14 on every split. Together with the two-block result, this rules out a value-13 colouring of either form for any split. The unrestricted value **13 ≤ f(23) ≤ 14** stays open. [Three-block proof](producer/three-block/PROOF.md)

At n=22, **the two- and three-block minimum is 13 on every split**. The certificates cover 11 two-block splits, 40 three-block splits and one rank control. On a 21-dimensional facet, each surviving rank word admits a closed 12-set family in either colour. Choosing the colour of the full 22-set and adjoining that set gives 13. The rank word `00100111010011100110100` attains 13 in each colour and gives the unrestricted upper bound **f(22) ≤ 13**. The restricted lower bound uses only the face classification. [Rank replay](producer/three-block/logs/final-rank.log)

The earlier two-block face classification covers ten of the eleven singleton splits (a,b,1). The eleventh, (11,11,1), needs the additional face shape (11,10). Across all 48 shapes of dimension 21, the witness induction leaves the same four rank words, each with one exterior set of each colour. Two displaced windows of a putative value-13 colouring must agree on their overlapping ranks. Each of the 16 ordered word pairs disagrees at 10 or 11 positions. The LRAT proofs check the final propositional exclusions after the witness induction. [Induction replay](producer/three-block/logs/final-check.log) · [Producer LRAT replay](producer/three-block/logs/final-lrat.log)

The clean-room AI referee concluded that both restricted claims hold. The referee checked the producer's rejection witnesses for closure and colour without searching for replacements. Regenerating the split formulas confirmed clause-multiset equality for all 44 and 52 roots. For the 48 face formulas the referee confirmed structural equality up to variable renaming. The referee's exact rank search was compared with brute force through n=6. The producer's checkers were separately written (same agent). This is a **candidate** result with **no human review**. The producer was GPT-6.2 Astra via Codex (`math_e1183b3_1120`), and the clean-room referee was Claude Opus 5.5 (`math_e1183b3ref_1120`). [Original referee report](referee/three-block/REFEREE.md) · [Referee scripts and outputs](referee/three-block/) · [Prior art](PRIOR_ART.md)

### Replay the three-block certificates

From the packet root, use Python 3.10 or later with assertions enabled. The producer replay uses the standard library. It checks the physical witnesses and rebuilds the face and split DIMACS files in memory, checks all 144 LRATs (48 faces, 44 roots at n=23, 52 at n=22), then verifies both rank constructions. The last command verifies the packet's delivered bytes.

```sh
(
  set -e
  cd producer/three-block
  nice -n 10 python3 -B src/check_roots.py
  nice -n 10 python3 -B src/lrat.py
  nice -n 10 python3 -B src/upper.py
  cd ../..
  shasum -a 256 -c SHA256SUMS
)
```

For the clean-room replay, use Python with NumPy. The temporary directory reproduces the referee's original layout and receives its new outputs. The first root comparison matches the 33 largest-block formulas. The second matches the other 11 using the singleton-absent windows. [Root comparison](referee/three-block/roots.py) · [Singleton comparison](referee/three-block/roots_singleton.py)

```sh
(
  set -e
  w=$(mktemp -d)
  mkdir "$w/ref"
  ln -s "$PWD/producer/three-block/data" "$w/data"
  cp referee/three-block/*.py referee/three-block/run_lrat.sh "$w/ref/"
  cd "$w/ref"
  nice -n 10 python3 -IB induct.py ../data out
  nice -n 10 python3 -IB final_check.py
  nice -n 10 python3 -IB roots.py
  nice -n 10 python3 -IB roots_singleton.py
  nice -n 10 python3 -IB face_check.py
  nice -n 10 python3 -IB rank_exact.py 0010011100101100011011 0011001011100010110011 \
    1100110100011101001100 1101100011010011100100 00100111010011100110100 001001110010110001101101
  # With the pinned drat-trim lrat-check built and LRAT_CHECK set to its absolute path:
  # nice -n 10 sh run_lrat.sh
)
```

CaDiCaL produced the proofs. Lean 4.36.0 and drat-trim’s `lrat-check` also verified all 144. The delivered proofs are the producer’s original bytes, so its data checksum list verifies them directly. The commands below verify all 715 original entries, then replay Lean. The packet includes the checker entry points and producer logs. [CaDiCaL revision](https://github.com/arminbiere/cadical/commit/c60730422e758ef1cebe7aeddf2dda31c996bf04) · [Lean revision](https://github.com/leanprover/lean4/commit/611c117bfaf7b7ae1cfcf246ce6fba31e8f509e9) · [drat-trim revision](https://github.com/marijnheule/drat-trim/commit/2e3b2dc0ecf938addbd779d42877b6ed69d9a985) · [Lean replay](producer/three-block/logs/final-lean.log)

```sh
# From the packet root, with the pinned Lean installation on PATH
(
  set -e
  src="$PWD/producer/three-block"
  cd "$src"
  shasum -a 256 -c data/SHA256SUMS
  nice -n 10 src/external.sh
)
# To build the optional referee checker, from the pinned drat-trim source directory
cc -O2 -o lrat-check lrat-check.c
```

The producer's corruption checker damages temporary copies. Run it from the packet root with the command below. [Producer controls](producer/three-block/logs/final-controls.log) · [Referee controls](referee/three-block/corrupt/controls.log)

```sh
(cd producer/three-block && nice -n 10 python3 -B src/corrupt.py)
```

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
