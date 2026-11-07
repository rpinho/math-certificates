# DB41: proposed uniform odd-square cyclic minus theorem

UNVERIFIED pending independent mechanical referee; no novelty, priority or
author-interest judgment by this driver. External Opus/Fable taste required.

Published target and location: Gonçalves, Oliveira e Silva, Ramos, *New Sign
Uncertainty Principles*, Discrete Analysis2023:9, arXiv2003.10771v4,
Problem3.1/equations(3.1),(3.3), Proposition3.6 and Conjecture3.7, printed
Section3.1. https://arxiv.org/html/2003.10771v4 . The paper supplies the sine
upper and numerical square evidence through ell100, and explicitly asks for
the uniform lower. The exact finite D003 three-instance claim is baseline.
All three authors are identity-checked in the primary metadata and journal:
https://discreteanalysisjournal.com/article/84266-new-sign-uncertainty-principles .

Our proposed number is an exact formula, with unchanged original even
unitary-DFT signs/common index/both endpoints:
 A_minus_disc((ell²−1)/2)=ell for EVERY ODD integer ell>=3.
No even-size adaptation, nonsquare values, first jump, monotonicity or
continuous improvement is claimed.

Code/data on Mini:
 friends_pf_diogo/DB41_cyclic_square_all_ell/ .
PROOF.md is the full universal proof, REPORT.md gives commands, PRIOR_ART.md
and initial/final receipts/archives give source provenance. pod_backup has
executed sources, logs, diagnostic and separate exact-check receipts.

Proof mechanism: explicit nonnegative self-Fourier G on residue classes
0,+1,-1 modulo ell, with every possibly negative inner coordinate zero,
forces a hypothetical minus eigenvector to vanish on those ENTIRE classes
(using subgroup Poisson to get the remaining +/-1 zeros). Explicit H>=0,
zero on the whole inner interval, has Fourier support in those forced zeros
and a strict positive endpoint. Orthogonality then contradicts normalization.
All-ell geometric/cosine identities are written out; no finite extrapolation.
An optional polynomial argument proves the stronger u=0 statement without
using endpoint normalization. The upper is entirely the authors' sine control.

Own verification, separately written from construction and importing none:
verify_original_comb.py passes direct ORIGINAL 256-bit Arb cosine DFT, every
G/H sign, self-duality/Fourier support, exact modular zeros, sine upper and
rational half-angle/integer root-count controls at ell3,5,7,9,11,15,21,31
in1.871s. Discovery-side FFT diagnostic passes through ell201 but is not
proof. Wrong deleted phase term and next feasible cutoff are negative
controls. All public math ran nice10/single-thread on sharedphys; no Mini
science. SHA-checked copyback and verifier source hash agree. The finite
checker is not itself a proof of the universal analytic quantifier.

Trivial controls: the published sine construction explains ALL matching
uppers; subgroup Poisson alone supplies only coset sums and is insufficient,
as explicitly recorded in STRUCTURAL_ROUTES.md. The new proof must justify
both successive separator support/sign implications. At cutoff ell the G
inner-zero requirement fails at ell-1, consistent with known feasibility.
No empirical hold-out exists and no original sealed artifact was reopened.

Worries: this is a short proposed resolution of an explicitly open uniform
question, so inspect carefully for convention/sign/support or endpoint errors.
No author-error assertion. Odd ell only is intentional. The source audit is
bounded, anonymous GitHub coverage is limited, and unpublished overlap is
unknown. Independent referee must rebuild the argument, preferably using a
new original-operator implementation. External taste alone evaluates novelty
and whether the author would care. No contact, publication or friend-note
promotion occurred. Freeze hashes are in MANIFEST.json next to this claim.
