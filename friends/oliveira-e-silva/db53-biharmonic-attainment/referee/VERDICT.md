HOLDS
Referee: gpt-6.1-sol

The proof supports reflection-even attainment and relative H² compactness of every Lp-normalized complex minimizing sequence for each fixed 3<=p<4 and epsilon>0. I found no gap in the stated scope.

The [published paper](https://doi.org/10.1007/s00526-023-02654-9) is coauthored by Diogo Oliveira e Silva. Its Appendix C/Theorem 4 gives axial attainment, and its reflection-even existence question is the relevant target. The claim retains the same complex space, quadratic form and Lp-squared denominator; no published numeric score is being beaten.

Why it holds: a real axial minimizer exists; the cited exponential-decay theorem applies below the free spectrum. The weighted convolution identity has the required positive transverse form, with PLUS lambda². Holomorphy handles zero ordinary axial mean. The real-power inequality gives strict binding below 2^(1-2/p)mG, and exact reflected residuals exclude escape even for complex profiles. REPORT.md details the functional justifications.

What I ran: independently written referee_checks.py on stats, importing no claimant code. Exact operator/Laplace/convolution checks passed on four polynomial-Gaussian profiles, including odd and even zero-mean controls; scalar mixed-derivative/cubic-sign checks and complex reflection controls passed. Also ran 6,400 scalar and 3,000 mass-splitting numerical stress controls, explicitly not proofs of continuous quantifiers.

Trivial control: infinitely separated reflected copies give exactly the escape threshold, not strict improvement. Zero-mean controls invalidate an assumed positive ordinary mean; the weighted argument survives. Gaussian controls are linear identities, not purported nonlinear minimizers. There is no empirical hold-out or fitted score to audit.

Relative to the paper, the added result is strict binding and reflection-even compactness/attainment throughout [3,4). Nonradiality for each fixed p at sufficiently small epsilon follows from its existing level bounds. The prior result encountered was [Lenzmann–Weth's unrestricted nonradial-ground-state theorem](https://doi.org/10.1007/s11854-023-0311-2). No novelty or priority judgment is made.

Strongest objection: finite symbolic controls cannot establish the weighted functional analysis or compactness of arbitrary complex sequences. I checked those analytically in REPORT.md; they are not mechanically formalized. No uniform epsilon margin, sharp level or unrestricted-ground-state comparison follows or is claimed.

Evidence is copied back and hash verified in this directory. All tracked pod workers finished; downloads were removed after copyback, leaving 70,494 bytes on the pod.

NEXT BAR: Obtain a PDE referee's line-by-line sign-off on the weighted-convolution lemma and its exponential-weight/Fubini bounds in REPORT.md.
