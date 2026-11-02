# C44 sources and scope

The claim is an improved upper bound on the maximal number of relevant
variables in a bounded-degree Boolean function, using the existing
weighted-potential framework. It does not claim a new polynomial dual certificate.

- [Tao and contributors, entry 44a](https://teorth.github.io/optimizationproblems/constants/44a.html): definition, historical bounds, and the degree-three theorem references.
- [Chiarelli, Hatami and Saks](https://arxiv.org/abs/1801.08564): weighted-variable argument and universal constant framework.
- [Wellens, Discrete Analysis 2022:19](https://arxiv.org/html/2005.00566v2): recurrence, symmetrization, block-sensitivity inequality, and Corollary 3.10's tail extension. The table lists 4.394.
- [BakeLab/Épi, pinned Wellens artifacts](https://github.com/BakeLab/Epi-results/tree/97fa6a420f417458e11723c8bceb70f1529e447a/mathematics/wellens): preceding bound 4.3654674227 and exact degree-48 data. The unchanged reproduction gives approximately 4.365467422574458; the added cap improves the exact horizon-96 recurrence by 1/128.
- [Huang et al., Épi report, Appendix A.1](https://arxiv.org/html/2610.24944v1#A1.SS1): the preceding public bound and its verification scope.
- [Tarannikov and Kirienko, IACR ePrint 2000/050](https://eprint.iacr.org/2000/050), and [Krotov and Valyuzhenich, Section 3](https://arxiv.org/html/2311.05566v2): the published R₃ = 10 dependency, cited rather than independently classified here. Krotov and Valyuzhenich also cite Zverev's computer-free argument.
- [Valyuzhenich, September 2026](https://arxiv.org/html/2609.12540v1): concerns q-ary Hamming graphs for q ≥ 3 and records Wellens's 4.394 for the binary case; it does not supply a stronger binary C44 bound.

The pre-publication refresh is recorded in [FINAL_LIVE_CHECK.md](FINAL_LIVE_CHECK.md).
No stronger C44 bound was located in the checked sources. Exhaustive priority
is not asserted. The paper and its universal analytic argument remain unrefereed.
