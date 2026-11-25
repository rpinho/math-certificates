# Credits

- Jinhao Huang with OpenAI Codex derived and reported the bounds and released the manuscript and trial data. [PR #393](https://github.com/teorth/optimizationproblems/pull/393), [Zenodo archive](https://doi.org/10.5281/zenodo.24502737).
- A. Biró developed the Newton-identity lower-bound method. The stress tests use the Biró–Harcos construction. [Biró’s lower bound](https://doi.org/10.1016/S0019-3577(00)80003-8), [Biró’s upper bound](https://doi.org/10.1016/S0019-3577(00)80018-X), [table bibliography](https://teorth.github.io/optimizationproblems/constants/42a.html).
- V. Bakeas proved Theorem A. R. Pinho supplied the arbitrary-knot form cited by Huang and the earlier explicit lower bound. [Bakeas’s paper and appendix](https://hexagonmath.org/2611.00069v1), [PR #310](https://github.com/teorth/optimizationproblems/pull/310).
- N. Vatopoulos supplied the phase profile used in the upper-bound claim. [Pinned input](https://github.com/NikosVat/turan-c42/blob/72703467aaac1082a123966b75f654a292c1e5f7/results/A_D96_4.json).
- A. Canli published earlier Theorem A certificate replays for the C42 upper bounds. [Canli’s replays](https://github.com/arhancanli/quantavane-replays).

Gemini 4 Neon High carried out the clean-room audit and replay. GPT-6.2 Sol packaged the replay artifacts. No human has checked this replay. The scripts use Python, python-flint with Arb, NumPy and mpmath.
