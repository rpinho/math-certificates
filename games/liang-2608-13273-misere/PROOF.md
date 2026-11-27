# Why the witnesses refute the tuples

## Counterexamples

An octal digit for removing a given number of tokens encodes which moves are allowed on a single heap. Bit 1 allows removing the whole heap, bit 2 allows leaving one nonempty heap, and bit 4 allows leaving two nonempty heaps. The leading digit can allow a split without removing tokens. Every move decreases the sum of squared heap sizes, including a split without token removal. This gives a terminating exact recurrence. A terminal position is N. A nonterminal position is N if some option is P, and P if every option is N. [Liang, §§2.1, 3.2 and 3.4.2](https://arxiv.org/pdf/2608.13273v2)

Each Definition 3.4 witness in [the data](certificates/WITNESSES.tsv) supplies a position with largest heap at least the printed first threshold. Its second heap determines which reduction applies. Sorting the resulting heaps gives the other position in the pair. The [clean-room referee](referee/REPORT.md) checked those thresholds and reductions against an independent transcription of the table, and checked by exact recurrence that the pair has opposite outcomes. This contradicts the equality required by the printed tuple. The certificate uses finite exact positions, so there is no statistical holdout.

## The two tuples that hold

For both games 0.512 and 0.513 the printed tuple is `(16,6,3,6)`. Plambeck and Siegel give a quotient of order eight and a quotient-valued heap map with period six and preperiod 16. Adding a heap context corresponds to multiplication in the quotient. Positions in the same quotient class have equal outcomes in every context. [Plambeck–Siegel, Fact 2.2 and Fig. 4](https://arxiv.org/pdf/math/0609825)

For each game, the producer’s [quotient check](certify_512.py) evaluates outcomes after adding every context of total at most ten to each candidate representative. The eight pairwise distinct outcome signatures occur at `()`, `(1)`, `(4)`, `(4,1)`, `(4,4)`, `(4,4,1)`, `(9)` and `(9,1)`. Distinct signatures imply distinct quotient classes, so the published order makes these representatives exhaustive.

- The check compares a heap of size 22 to one of size 16 in all eight classes. Together with the published heap-map period, this covers every permitted subtraction by six from the largest heap, including the preperiod boundary.
- The two-heap branch also subtracts six from the second heap, whose initial size is at least nine. The same heap-map period covers sizes 22 and up. For sizes 9 through 21, replace the original largest heap by its quotient-equivalent size in 16 through 21. For each of these six representatives of the largest heap, each of the 13 second-heap sizes and each of the eight context classes, check that the outcome agrees after subtracting six from the second heap.

The eight preperiod boundary comparisons and the 624 two-heap comparisons have zero mismatches in each game. The recurrence checked every representative context, and quotient equivalence extends the equalities to arbitrary finite heap positions. [Boundary data](certificates/QUOTIENT_512.tsv)
