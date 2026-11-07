HOLDS
Referee: gpt-6.1-sol

The restricted-weight theorem survives independent mathematical review: T <= min{3^k(g-1), 1+8[2g-3+gk+k(k-1)/2]}, with the stated k and g=n+1-k.
It counts the same maximal affine solution-path pieces, including the constant tail, as [Bento–Furmaniak–Ray, Eq.(2), Theorems 2–4](https://arxiv.org/html/1801.04987v3).
The independent all-n argument in PROOF_AUDIT.md validates good-contact nonreturn, pair amortization, and simultaneous events; the conclusion does not rest on extrapolating finite tests.

Ran on phys: an original exact rational primal-block enumerator and a separately written interval KKT checker, importing no claimant code.
Both passed 570 complete paths: the two baselines, all 73 submitted certificates, and 495 fresh adversarial/exhaustive cases.
All submitted knots and coefficients agree exactly. Fig.1 has T=5 and knots 25/27,25/23,100/73,25/4; its equal-weight control has T=3.
The checker rejected five negative controls, including cutting the low-weight edge and testing that different objective's path under the original positive weights.
There is no statistical holdout: this is an all-input theorem, and the synthetic cases are diagnostics. No holdout-based performance gain is asserted.

Relative to the 2018 paper, the addition is an explicit O(n(k+1)) sufficient-family bound allowing unfusions; it neither improves the five-piece example nor the unrestricted quadratic order.
Concave weights already have the linear guarantee by [Tibshirani–Taylor 2011, §6 Eq.(23)](https://www.stat.berkeley.edu/~ryantibs/papers/genlasso.pdf); that control does not subsume the verified nonconcave examples with unfusions.
Also observed: [Le–Nguyen–Nguyen 2026, Appendix G.2](https://arxiv.org/html/2602.02406v2) explicitly uses the general 3^(n-1) signed-box-state count. No novelty or priority judgment is made here.
Identity matches: [Bento's author page](https://jbento.info/) lists this paper with Furmaniak and Ray, matching the primary source's affiliation and coauthors.

Strongest objection: small exact examples cannot prove an all-n bound, particularly at simultaneous contact changes. The separate analytic audit addresses that objection directly; it is not proof-assistant formalized.
Evidence, code, inputs, source snapshots and checksums are local under this directory; BACKUP_RECEIPT.json verifies the archive. No referee workers remain; pod cleanup leaves about 1.2 MB.
NEXT BAR: mechanize the simultaneous-event endpoint-pair charging lemma in a proof assistant.
