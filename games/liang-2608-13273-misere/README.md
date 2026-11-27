# Misère octal periodicity in Liang’s arXiv:2608.13273v2

Mikael (@exitcode0dev) and the Phoenix AI team first refuted the printed tuples for 0.355, 0.716 and 0.717. The 0.337 tuple was settled first by 1337isnot1337 in the Misère Domination Game proof. The other **45** refutations are new as far as the 2026-11-27 searches show. The searches covered arXiv versions and citing works, OpenAlex, Zenodo, OEIS records and histories, GitHub code, repositories and open changes, and public community posts. [Prior art and search details](PRIOR_ART.md), [Phoenix repository](https://github.com/md-exitcode0/math-conjectures), [solved-conjectures repository](https://github.com/1337isnot1337/solved-conjectures)

I give exact counterexamples to **49 of the 55 printed tuples**, with a P/N witness pair for each game. The tuples for **0.512 and 0.513 hold** by a boundary argument using Plambeck and Siegel’s misère quotients. The tuples for **0.552, 0.553, 0.734 and 0.735** agree on every eligible position through **56 tokens** and remain open here. Salem Levinstein’s 0.3122 result concerns a separate residue rule in Liang’s quaternary-games paper. [Proof and boundary checks](PROOF.md), [Plambeck–Siegel](https://arxiv.org/abs/math/0609825), [Levinstein](https://zenodo.org/records/24568032), [credits](CREDITS.md)

## What the tuples predict

Definition 3.4 says that a position with a sufficiently large largest heap “can always be reduced to a smaller position in one of the following two ways”. Sort the heaps from largest to smallest, and read a missing second heap as size zero. For a printed tuple `(p₁,t₁,p₂,t₂)`, the rule applies once the largest heap has size at least `p₁ + t₁`.

- If the second heap has size below `p₂ + t₂`, subtract `t₁` from the largest heap.
- If the second heap has size at least `p₂ + t₂`, subtract `t₂` from each of the two largest heaps.

The definition requires the misère outcome to stay the same. P means the previous player wins with perfect play. N means the next player wins. If a position and its prescribed reduction have opposite outcomes, the printed tuple is false. The 25 grouped rows of the p. 27 table give 55 tuples after expanding the grouped octal digits. [Definition 3.4 and the printed table](https://arxiv.org/pdf/2608.13273v2#page=24), [table transcription](certificates/TABLE.tsv)

## Witness pairs

Each pair is shown in P, N order. The branch and the original position are recorded in the data. The game 0.357 has a pair for each branch. [Witness data](certificates/WITNESSES.tsv), [tuple and sweep data](certificates/RULES.tsv)

| Octal game | Branch | P-position | N-position |
|---|---:|---|---|
| `0.157` | 2 | `(28,7,4,4)` | `(25,4,4,4)` |
| `0.175` | 2 | `(24,5,3,3,3,3)` | `(22,3,3,3,3,3)` |
| `0.260` | 2 | `(24,5,4,3,3,3)` | `(22,4,3,3,3,3)` |
| `0.261` | 2 | `(24,5,4,3,3,3)` | `(22,4,3,3,3,3)` |
| `0.262` | 2 | `(24,5,4,3,3,3)` | `(22,4,3,3,3,3)` |
| `0.263` | 2 | `(24,5,4,3,3,3)` | `(22,4,3,3,3,3)` |
| `0.270` | 2 | `(24,5,4,3,3,3)` | `(22,4,3,3,3,3)` |
| `0.271` | 2 | `(24,5,4,3,3,3)` | `(22,4,3,3,3,3)` |
| `0.272` | 2 | `(24,5,4,3,3,3)` | `(22,4,3,3,3,3)` |
| `0.273` | 2 | `(24,5,4,3,3,3)` | `(22,4,3,3,3,3)` |
| `0.326` | 2 | `(22,5,3,3,3,3,3)` | `(20,3,3,3,3,3,3)` |
| `0.327` | 2 | `(22,5,3,3,3,3,3)` | `(20,3,3,3,3,3,3)` |
| `0.337` | 2 | `(27,4,2,2,2,2,2,2,1)` | `(25,2,2,2,2,2,2,2,1)` |
| `0.355` | 2 | `(22,3,2,2,2,2,2,2,2,2)` | `(21,2,2,2,2,2,2,2,2,2)` |
| `0.357` | 2 | `(30,5,2,2,2,2)` | `(27,2,2,2,2,2)` |
| `0.357` | 1 | `(32,2,2,2,2,2,2,1)` | `(30,2,2,2,2,2,2,1)` |
| `0.516` | 2 | `(28,7,4,4)` | `(25,4,4,4)` |
| `0.517` | 2 | `(28,7,4,4)` | `(25,4,4,4)` |
| `0.534` | 2 | `(24,5,3,3,3,3)` | `(22,3,3,3,3,3)` |
| `0.535` | 2 | `(24,5,3,3,3,3)` | `(22,3,3,3,3,3)` |
| `0.556` | 2 | `(28,7,4,4)` | `(25,4,4,4)` |
| `0.557` | 2 | `(28,7,4,4)` | `(25,4,4,4)` |
| `0.570` | 2 | `(24,5,3,3,3,3)` | `(22,3,3,3,3,3)` |
| `0.571` | 2 | `(24,5,3,3,3,3)` | `(22,3,3,3,3,3)` |
| `0.574` | 2 | `(24,5,3,3,3,3)` | `(22,3,3,3,3,3)` |
| `0.575` | 2 | `(24,5,3,3,3,3)` | `(22,3,3,3,3,3)` |
| `0.716` | 2 | `(24,3,1)` | `(23,2,1)` |
| `0.717` | 2 | `(24,3,1)` | `(23,2,1)` |
| `0.724` | 2 | `(24,5,3,3,3,3,1)` | `(22,3,3,3,3,3,1)` |
| `0.725` | 2 | `(24,5,3,3,3,3,1)` | `(22,3,3,3,3,3,1)` |
| `0.726` | 2 | `(24,5,3,3,3,3,1)` | `(22,3,3,3,3,3,1)` |
| `0.727` | 2 | `(24,5,3,3,3,3,1)` | `(22,3,3,3,3,3,1)` |
| `0.732` | 2 | `(25,4,2,2,2,2,2,2,2,1)` | `(23,2,2,2,2,2,2,2,2,1)` |
| `0.733` | 2 | `(25,4,2,2,2,2,2,2,2,1)` | `(23,2,2,2,2,2,2,2,2,1)` |
| `0.736` | 2 | `(24,4,2,2,2,2,2,2,2)` | `(22,2,2,2,2,2,2,2,2)` |
| `0.737` | 2 | `(24,4,2,2,2,2,2,2,2)` | `(22,2,2,2,2,2,2,2,2)` |
| `0.754` | 2 | `(19,3,2,2,2,2,2,2,2,2,2,1)` | `(18,2,2,2,2,2,2,2,2,2,2,1)` |
| `0.755` | 2 | `(19,3,2,2,2,2,2,2,2,2,2,1)` | `(18,2,2,2,2,2,2,2,2,2,2,1)` |
| `0.756` | 1 | `(28,2,2,2,2,2,2,1)` | `(26,2,2,2,2,2,2,1)` |
| `0.757` | 1 | `(28,2,2,2,2,2,2,1)` | `(26,2,2,2,2,2,2,1)` |
| `4.06` | 2 | `(21,5,3,3,3,3,3)` | `(19,3,3,3,3,3,3)` |
| `4.07` | 2 | `(21,5,3,3,3,3,3)` | `(19,3,3,3,3,3,3)` |
| `4.26` | 2 | `(21,5,3,3,3,3,3)` | `(19,3,3,3,3,3,3)` |
| `4.27` | 2 | `(21,5,3,3,3,3,3)` | `(19,3,3,3,3,3,3)` |
| `4.16` | 2 | `(21,5,3,3,3,3,3,1)` | `(19,3,3,3,3,3,3,1)` |
| `4.17` | 2 | `(21,5,3,3,3,3,3,1)` | `(19,3,3,3,3,3,3,1)` |
| `4.52` | 2 | `(22,5,3,3,3,3,3,1)` | `(20,3,3,3,3,3,3,1)` |
| `4.53` | 2 | `(22,5,3,3,3,3,3,1)` | `(20,3,3,3,3,3,3,1)` |
| `4.70` | 2 | `(18,3,2,2,2,2,2,2,2,2,2,2)` | `(17,2,2,2,2,2,2,2,2,2,2,2)` |
| `4.71` | 2 | `(18,3,2,2,2,2,2,2,2,2,2,2)` | `(17,2,2,2,2,2,2,2,2,2,2,2)` |

## How I checked the result

Two producer solvers agreed on the exact outcome tables underlying all 177 witness rows. They use recursive move enumeration with memoization and forward evaluation in partition order, respectively. The producer witness replay recomputes every listed P/N pair. The clean-room referee from a different model family used its own two solvers to recompute those outcomes and checked the required reductions against its own transcription of Liang’s table. [Producer solver](direct.cpp), [forward solver](checker.cpp), [replay results](REPLAY.json)

The referee confirmed 149 rows, rejected zero and identified 24 singleton-template rows whose status depends on whether the p. 28 caption starts at heap size one or zero. Four other rows illustrate a separate claim of Liang’s about when folding fails. All 50 Definition 3.4 witness rows for the 49 refuted games were confirmed. The clean-room verdict on all 49 refutations is **HOLDS**. [Verbatim referee report](referee/REPORT.md)

From this folder, use Python 3 and a C++17 compiler. The referee command writes its JSON output in the referee directory. The bundled input for that script contains the p. 28 table excerpt it needs. The paper is available on arXiv. [Liang’s paper](https://arxiv.org/abs/2608.13273v2)

```sh
clang++ -std=c++17 -O3 -Wall -Wextra -Werror checker.cpp -o math_misere_1127_checker
python3 -B verify_witnesses.py certificates/WITNESSES.tsv
(cd referee && python3 -B check_witnesses.py)
```

**Lean status** · none.

**AI disclosure** · GPT-6.2 Sol (Codex) found the counterexamples. Claude Opus 5.5 refereed them in a clean room. No human mathematician has checked this work.
