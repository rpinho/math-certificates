# Results for other people's papers

The rest of this repository is bounds on open constants from [Terence Tao's optimization-problems table](https://github.com/teorth/optimizationproblems) and [openai/math](https://github.com/openai/math). This folder is the same thing applied to papers by mathematicians and scientists I know: an exact value where a paper printed a bound, a settled case the paper left open, or a certificate for a number that was only conjectured.

The format is the same as every other folder here. Each item says what was asked, what we found, how a clean-room referee checked it, and where it is still a candidate. The referee is a separate agent on a different model that rebuilds the claim from the primary source and may not import the finder's code; it is still our own pipeline, not a third-party check. Nothing here has been refereed by a journal or by a human, and no priority is claimed over anyone.

Everything below has been sent to the author it concerns. Results that were not sent are not here.

| Person | Paper | What we found | Referee |
|---|---|---|---|
| Oliveira e Silva | [arXiv:2609.11644](https://arxiv.org/abs/2609.11644), Remark 1.3(c) | At d = 5, Gaussians are not local maximizers at the Keel–Tao endpoint: a certified family beats them by more than 11ε⁴, with an exact checker | candidate: no clean-room referee; three model reviews found no false step |
| Oliveira e Silva | Mandel and Oliveira e Silva, *Calc. Var.* 63 (2024) 45, [arXiv:2306.03720](https://arxiv.org/abs/2306.03720), Appendix C | A reflection-even axial attainment theorem for the biharmonic NLS ground states left open there, for all 3 ≤ p < 4 | HOLDS |
| Oliveira e Silva | Gonçalves, Oliveira e Silva and Ramos, *New Sign Uncertainty Principles*, [arXiv:2003.10771](https://arxiv.org/abs/2003.10771), Conjecture 3.7 | The conjecture for odd ℓ, plus an exact adjacent cyclic-minus jump at q = 7320/7321 in the paper's own feasibility problem | HOLDS |
| José Bento | Safavi, Joshi, França and Bento, [arXiv:1801.04492](https://arxiv.org/abs/1801.04492), Thm 5 | An exact finite-κ certificate: at κ = 25 and the paper's tuned β, q = 3599/5000 is a universal squared-distance factor, improving the matched published 18/25 | HOLDS |
| José Bento | Bento, Furmaniak and Ray, [arXiv:1801.04987](https://arxiv.org/abs/1801.04987), §IV | A weight condition under which the weighted fused lasso path has O(n) pieces, which §IV asks for; Tibshirani–Taylor diagonal dominance is credited as the stronger prior control | HOLDS |
| José Bento | Marangola, Sheikholeslami and Bento, [arXiv:2512.24930](https://arxiv.org/abs/2512.24930), Thm 3 | The all-tree extension and the sharp strict threshold γ = 1 + 2/q | HOLDS WITH CAVEATS |
| Hugo L. Fernandes | Gama and Fernandes, *C&OR* 133 (2021) 105357, [arXiv:2011.03647](https://arxiv.org/abs/2011.03647), Table B.7 | Exact optima for 15 single-day OPTW instances; t204 is 179 against a published best-known 171 | HOLDS WITH CAVEATS |
| Hugo L. Fernandes | The same benchmark family (TOPTW, Solomon/Righini instances) | pr11 with three vehicles closed at 654 with an exact certificate; c104 with four vehicles closed at 1260, moving its status from best-found to proven | HOLDS WITH CAVEATS / HOLDS |
| Hugo L. Fernandes | [arXiv:2411.14411](https://arxiv.org/abs/2411.14411), Table 4.1 | Exact CVRPTW50 optima for all 2,048 instances, mean 14.4717 against the quoted 14.478; TOPTW50 mean profit 34.09 with 2,006 of 2,048 certified optimal | candidate: exact-solver result with its own verification file, not refereed |
| Luís Diogo | Abouzaid and Diogo, *Monotone Lagrangians in cotangent bundles of spheres*, [arXiv:2011.13478](https://arxiv.org/abs/2011.13478), Remarks 4.2 and 4.10 | Remark 4.2: the cotangent fibre generates, not only split-generates, over the integral Novikov ring, for all spheres, odd and even. Remark 4.10: the predicted sign is proved, w = ±u(e₁ + e₂), with only the global sign left open | HOLDS WITH CAVEATS (4.2), HOLDS (4.10) |
| Kris Sankaran | Sankaran, Raskutti and Ye, [arXiv:2609.19511](https://arxiv.org/abs/2609.19511) | A zero causal Shapley value implies a causal null if and only if h₋ ≥ h₊ | candidate: no clean-room referee; two model reviews found no false step |
| Marco Sampaio | Alves et al., FiFAR, *Sci Data* 2025, Table 7 | All five team deferral costs drop (138.1 → 102.0 among them) and reproduce exactly | HOLDS WITH CAVEATS |

Two caveats worth repeating rather than burying: prior art already improves the FiFAR solver on its own (nguyetvo's public repository), and that benchmark has no unused hold-out, so the comparison is to a published table, not to a fresh test set.

## Folders

- [`oliveira-e-silva/`](oliveira-e-silva/) — the d = 5 endpoint note with its exact checker; the biharmonic attainment and odd-ℓ sign-uncertainty notes, each with its exact checker and the referee's claim, report and verdict.
- [`bento/`](bento/) — three claims with certificates and the referee's own checkers.
- [`fernandes-orienteering/`](fernandes-orienteering/) — the OPTW/TOPTW notes, the exact closures with their C++ checkers, and the CVRPTW/TOPTW report.
- [`luis-abouzaid-lagrangians/`](luis-abouzaid-lagrangians/) — both Remark 4.2 cases and the Remark 4.10 sign, with claims, proofs, referee verdicts and the validation report.
- [`sankaran-causal-shapley/`](sankaran-causal-shapley/) — the note and its checker.
- [`sampaio-fifar-deferral/`](sampaio-fifar-deferral/) — claim, referee scripts and verdict.

## References

- Brian Armstrong, [publicly funded science as open source](https://x.com/brian_armstrong/status/2119150702446420027), November 7, 2026 — the argument for shipping each result as a repo anyone can rerun.
- Every paper linked in the table above; each folder's `PRIOR_ART.md` lists the methods and public code the result builds on, including Tibshirani and Taylor (2011), Taylor, Van Scoy and Lessard (2018), Pokutta and Stellato (2026), Ševeček's SISR implementation, Amarouche et al. (2020) and PyVRP.
- The exact arithmetic throughout is Arb/FLINT or Python rationals.
