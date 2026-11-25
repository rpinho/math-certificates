# C42 PR #393 packaging prior art

The source audit captured the scoreboard, open changes, public code search, papers and community search on 2026-11-25 UTC. The packaging relies on that dated snapshot.

- The source audit checked the official C42a table at `83e93c3` and identified PR #393 as the only open C42a change. It records Biró's strict, non-explicit lower bound above 1/2, Pinho's asterisked explicit bound 1/2 + 2^-4096 and Vatopoulos's upper bound 0.686360751. [C42a table](https://teorth.github.io/optimizationproblems/constants/42a.html), [PR #393](https://github.com/teorth/optimizationproblems/pull/393)
- The audit records no repository hits for its GitHub search and no third-party replay in its web and community search. Its paper search includes Biró's lower-bound papers. Huang archives the claims and inputs on Zenodo. [Biró (2000)](https://doi.org/10.1016/S0019-3577(00)80003-8), [Biró (1996)](https://doi.org/10.1090/S0025-5718-96-00744-2), [Huang's archive](https://doi.org/10.5281/zenodo.24502737)
- The source replay records HOLDS for Huang's Theorem 1 and the one-box hand proof, and checks selected hypotheses for Theorem 2. The upper-bound inequality \(F<T\) remains unreplayed. This packaging job preserves the existing result and makes no new bound claim.
