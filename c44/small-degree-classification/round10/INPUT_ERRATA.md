# Input errata — candidate, unrefereed

Round-eight PROOF.md equation (13) requires **Q != 0** in its
integer-polynomial norm-gap statement. Every application in this chain
is to a relevant coordinate and hence a nonzero partial. The copied
round-nine PROOF.md states the nonzero hypothesis explicitly. No
certificate, case exclusion or numerical bound changes.

Round-eight INPUT_ERRATA.md already corrects round-seven's phrase
"budget at most 50": the real budget is **201/4 = 50.25**, whose floor
is 50. See `frozen/inputs/round8/INPUT_ERRATA.md` in round9, or the same
file below `frozen/baseline/` in round10 and `inherited/frozen/baseline/`
in round11. The round-eight proof itself is preserved.

Our own checkers are **separately written (same agent)**. Descriptions
of them as independent implementations do not claim separate authorship
or human refereeing. This also corrects the inherited round-eight
checker wording without changing its proof. Mathematical independence
of variables, components and projections is unrelated and is retained.
Copied round-seven LATTICE_PROOF.md has the four requested checker-wording
corrections; the earlier public round7/ and round8/ directories are not
modified by this release.
