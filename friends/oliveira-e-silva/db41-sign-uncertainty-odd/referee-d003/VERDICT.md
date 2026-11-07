HOLDS
Referee: gpt-6.1-sol

Independent rigorous checks establish A_minus_disc(7320)=121, A_minus_disc(7321)=122, and A_minus_disc(7440)=122. The adjacent 121-to-122 change survives.

The [primary paper](https://arxiv.org/html/2003.10771v4), Problem 3.1, uses exactly the tested even unitary DFT, origin signs, common tail index and endpoint normalization. The [journal](https://discreteanalysisjournal.com/article/84266-new-sign-uncertainty-principles) confirms Diogo Oliveira e Silva is a coauthor.

Figure 3 really reports k=120,q=7081 and a minimum-tail-energy vector. I reproduced feasibility at that index; neither the submission nor this referee reproduces its energy minimum.

Ran independently written `independent_check.py` on the shared pod: 320-bit Arb, direct cosine sums over every tail coordinate, exact rational seeds, certified nonsingular correction systems, matching upper witnesses, and the q=5 direct-LP/exact controls. No claimant search or verifier code was opened or imported. Receipts and hashes: `pod_evidence/`.

All three lower certificates passed. Exact inner zeros follow algebraically from the correction equations, rather than numerical tolerances. Their remaining signs and positive endpoints contradict every feasible vector at the preceding index through DFT orthogonality. Five negative controls were rejected, including zero-endpoint and incorrectly strengthened certificates.

The trivial sine control explains every upper bound. It does not explain away the matching lower bounds. No hold-out applies to this deterministic certificate problem; selecting these instances gives no statistical evidence about untested instances.

Relative to the paper: rigorous matching lower certificates at three larger fixed q, including its conjectured ell=121 square case. The paper already supplies the sine construction and predicts the pattern. The bounded public audit found continuous-plus results on different quantities, but no superseding same-object table; see `PRIOR_ART.md`. No priority judgment follows.

Evidence was copied back and hash-checked. All referee workers finished; temporary pod dependencies were removed. The pod directory ends at 380 KB.

Strongest author objection: these are three anticipated finite instances, using an existing upper construction, without a uniform explanation of the lower-bound pattern or a reproduced energy optimum.

NEXT BAR: Prove A_minus_disc((ell²−1)/2)>=ell uniformly for every odd ell>=3, clearing the lower-bound side of Conjecture 3.7.
