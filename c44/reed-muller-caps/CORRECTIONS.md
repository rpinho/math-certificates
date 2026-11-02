# Corrections to PROOF.md

`PROOF.md` is frozen so that its hash matches the receipts. A referee found two wording defects. Neither changes the mathematics.

1. Section 3, "Applying them successively to coordinates in H, or equivalently inducting on |H|". Read literally, this charges each later coordinate at its weight after restriction, and that inequality runs the wrong way. The correct reading: iterate over H for each coordinate outside H, then charge H at its original weights.
2. Sections 4 and 5 credit the third and higher below-two weights for the final bound. The referee's ablation finds that, given the energy grid, the single fact that no normalized weight lies in (1, 3/2) already gives the same rational. Section 5's ablation numbers disagree with that, and this hasn't been resolved. Treat the attribution as open. The bound doesn't depend on it.

External premises are R3 = 10 and the second Reed-Muller weight 3/2. The Kasami-Tokura-Azumi 1976 results aren't a premise. The claim in `KTA_AUDIT.md` about a table omission is unverified.
