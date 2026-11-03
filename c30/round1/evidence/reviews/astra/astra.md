**FLAG: two definite errors in the source audit; no counterexample found to the candidate’s mathematical route.**

Full results, every check, hashes, and reproduction commands are in [REFEREE_REPORT.md](REFEREE_REPORT.md). Exact external statements, hypotheses, and withdrawal dependencies are in [EXTERNAL_PREMISES.md](EXTERNAL_PREMISES.md). The original folder remains unchanged.

The first false item is **GATE.md:13**, which says the sources do not identify v2’s withdrawal cause. Norton’s v3 Comments explicitly identify unequal cells after pairing and an Appendix F argument count checked only at arc endpoints. This explanation already exists in the packet’s hash-matching archived abstract. [Norton v3 withdrawal comments](https://arxiv.org/abs/2608.20292v3).

**REFEREE.md:36 also reverses the entropy sign.** The concave expression in v1 is \(J+2\operatorname{Ent}\), not \(J-2\operatorname{Ent}\). Neither audit error enters the candidate proof.

Checks completed:

- **Arb:** positive \(\Phi>0.00018309709357909\), root isolation, corrected Rouché selection, first moment \(0.0662796005720\ldots<1/10\), saddle bracket, tangent error, rational thresholds and profile identities. **All 13 rejection controls rejected.**
- **Integrity:** all **131 manifested files** and **32 BAR source hashes** match; fresh BBEP and Norton version downloads match archived hashes.
- **Fresh enumeration through \(n=14\):** **1,209,639,642 avoiders**, **1,390,594,458 domino roundtrips** at \(n=14\); OEIS and every coefficient of all five marginal series agree. Runtime: **374 seconds**.
- **Independent exact checks:** 120 coefficients using \([z^nu^k]F_0=\binom nk\mathrm{Cat}_{n-k}\); direct \(F_0/P_0\) enumeration through \(n=7\); symbolic derivative, discriminant and normalization identities; 5,313 physical pairing tests.
- **Additional replays:** Python five-series enumeration, leaf/block marking, 1,068,643 envelope controls, baseline certificate and seven corruptions, ordering counterexample, v2 normalization counterexample, and reduced-model obstruction.

The candidate accommodates unequal boundary corrections and uses a uniform Rouché estimate. I found no reliance on the withdrawn equal-profile, endpoint-winding, or tilted-concentration claims. Credit remains due to BBEP, Norton’s retained Harris argument, and Norton v2’s marginal/kernel algebra.

The live table still lists \(10.27\)–\(13.5\). Among **52 open PRs and six issues**, only [#313](https://github.com/teorth/optimizationproblems/pull/313) changes constant 30, proposing Norton’s \(10.412263\). I found no unwithdrawn unconditional public lower bound above \(10.42\). A stronger public **upper** bound is Brignall’s \(13.167248\); Franklín’s \(10.418\) lower bound is conditional. [Brignall](https://arxiv.org/abs/2610.02535), [Franklín](https://arxiv.org/abs/2512.19462).

VERDICT: FLAG