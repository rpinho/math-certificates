# Prior art and comparison scope — 2026-11-05

This is a clean-room referee/replay, not a search for a new construction. The specific input restrictions override the broader repository/code-search requirements in RULES.md. No linked certificate packet or producer/replayer code has been accessed.

Allowed public sources read before implementation:
- https://github.com/teorth/optimizationproblems/blob/main/constants/82a.md — live definition uses logarithmic absolute height h(alpha)+h(1-alpha), and the supremum of finite-sublevel thresholds. The merged table lists 0.2534449* as its smallest upper bound.
- https://github.com/teorth/optimizationproblems/pull/280 — current v4 bound 0.2520079724*, V. Patankar, weighted closest-vector denominators and LLL numerator search. Body states rigorous upper endpoint 0.25200797232846; comments report an independent replay. Earlier v3 enclosure wording was corrected: an upper-bound quadrature tolerance is not a two-sided radius.
- https://github.com/teorth/optimizationproblems/pull/301 — 0.253091834*, R. Pinho, residue-class/LP method; earlier certificate and independent replay described in text.
- https://github.com/teorth/optimizationproblems/pull/330 — current bound 0.2519964890*, R. Pinho, joint degree-104 certificate built on Patankar v3; producer enclosure [0.2519964889882011564383,0.2519964889882011727026], independently replayed according to comments. This is the best of the allowed live PR texts.
- C. Doche, Zhang-Zagier heights of perturbed polynomials, JTNB 13 (2001), 103–110, https://www.numdam.org/item/JTNB_2001__13_1_103_0/ — primary construction and averaging lemma.

Bodies/comments and live definition are saved in sources/. Prior certificates cannot be reproduced here without violating the exclusive certificate-input rule. Comparison is therefore with their printed values, not a new replay of those certificates. The supplied new certificate alone will be replayed. No global priority claim is intended. Predictive-model baselines and SBS do not apply to a deterministic mathematical certificate.

Final scoped recheck: PR #280 and #330 bodies/comments were fetched again with the prescribed gh executable. Both were byte-equivalent as parsed JSON to the initial snapshots (updatedAt 2026-11-05T14:07:16Z and 2026-11-05T15:14:40Z respectively). Their printed comparison values remain 0.2520079724* and 0.2519964890*. No linked packet or code was read.
