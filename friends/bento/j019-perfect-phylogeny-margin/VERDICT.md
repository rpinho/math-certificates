HOLDS WITH CAVEATS
Referee: gpt-6.1-sol

The all-tree singleton result and sharp strict threshold gamma=1+2/q survive
for fixed finite q under the paper's explicit Brownian increment-energy limit.
The published 1/(36e) coefficient is correctly identified and remains unchanged.
Relative to the paper, the extension covers every same-root candidate and
quantifies the allowed scalar relaxation; it does not reproduce a finite-grid gain.

I wrote independent code from descendant sums, generated undirected edge subsets,
and checked every ordered tree pair for q=3..7, including 282,475,249 pairs at q=7.
Every wrong-tree gap was at least 2; only the true tree attained the minimum.
Complete histograms matched the submitted data. Rational witnesses checked
thresholds through q=40. Integration reproduced 1/36; enumeration checked the leaf factor.
The all-q proof and survival-conditioning argument are valid: conditioning on
positive-probability survival preserves quadratic variation. Finite candidates
then give the simultaneous limit. Equality at the threshold remains unclaimed.

The covariance control reconstructed every tree exactly and ties singleton count 1.
Loh–Bühlmann (2014), Theorem 7/Lemma 27, already supplies global score strictness:
https://www.jmlr.org/papers/volume15/loh14a/loh14a.pdf .
Bento's homepage and arXiv confirm authorship; fresh primary PDFs match the frozen
hashes. No held-out prediction experiment is involved, so hold-out accuracy is inapplicable.
Source: https://arxiv.org/html/2512.24930v2 , equations 28–36.

Caveat: the explicit limit excludes an initial-state penalty. Adding ||M(0)||^2
breaks recovery: an exact feasible q=3 example has limiting wrong-minus-true
energy -1/5 (REPORT.md). The claim expressly adopts the increment-only convention.
Independent survival-conditioned grid diagnostics support both strict sides.
Evidence, executed code and hashes are backed up in evidence/.

Strongest author objection: existing minimum-score theory and direct covariance
already identify this idealized ensemble; this establishes the scalar DC extension,
with no demonstrated advantage for finite, noisy or projected observations.

NEXT BAR: Prove an explicit finite-N success bound over all same-root candidates
under the same conditioned ensemble and a fully specified increment-energy statistic.
