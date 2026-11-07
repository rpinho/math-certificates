HOLDS
Referee: gpt-6.1-sol

The stated formula A_minus_disc((ell^2-1)/2)=ell survives for every odd ell>=3.
I rederived the universal proof; it uses the paper's original unitary DFT,
common cutoff, origin signs and both normalized endpoint constraints.
The two nonnegative separators force whole residue classes to vanish, then
contradict the positive endpoint: H(q)=1+cos(pi/ell)>0.

The [paper](https://arxiv.org/html/2003.10771v4) already supplies the sine upper and conjectures equality;
relative to it, this contribution is the uniform lower proof, not a better upper.
I reproduced the sine control and explicitly rescaled it to meet both endpoints.
[Journal metadata](https://discreteanalysisjournal.com/article/84266-new-sign-uncertainty-principles) confirms Diogo Oliveira e Silva is a coauthor.

I wrote independent code, reading/importing none of the claimant's implementations.
On stats: exact cyclotomic DFT identities passed at ell=3,5,7,9,11,15;
256-bit Arb full-DFT/sign/support checks passed at eleven ell values through 51.
Fresh original/eigen primal LPs gave 20 feasible upper-cutoff results and
18 infeasible lower-cutoff diagnostics; two ell=31 runs were UNKNOWN, inconclusive.
Finite checks supplement the all-ell algebra; they do not prove its quantifier.
Broken-phase and next-cutoff controls were rejected. Subgroup sums alone fail
as a proof: an explicit relaxed vector satisfies them but fails the eigen equation.

Hold-out: none applies to this deterministic theorem; checks were post-proof.
Related prior work seen: Ismoilov's [trigonometric-polynomial result](https://arxiv.org/abs/2606.02299),
which does not itself state this simultaneous cyclic minus-eigenvector theorem.
Evidence, hashes and derivation: REPORT.md, evidence.tar.gz, PRIOR_ART.md.
Workers finished; evidence copied back; pod directory cleaned to about 100 KB.

Strongest objection: Poisson gives zero coset sums, not pointwise zeros.
Here G first kills every other entry in the exceptional cosets, so their
remaining entries really vanish before H's Fourier-support argument is used.

NEXT BAR: Kernel-check the universal G/H support implications in Lean with
the original Problem 3.1 endpoint constraints.
