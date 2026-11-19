HOLDS
Referee: gpt-6.1-sol
NEW confirmed: yes

The target is real: I opened Abouzaid–Diogo arXiv:2011.13478v2,
Remark 4.10 on printed p21, and the journal PDF on printed p26.
Luís Diogo is a coauthor. Both predict equality of Lemma 4.9(2)'s signs.
Sources: https://arxiv.org/pdf/2011.13478v2 and
https://www.diva-portal.org/smash/get/diva2%3A1783421/FULLTEXT01.pdf.

The proof addresses that original integral identity, w=±u(e1+e2).
Its step beyond the paper is the signed comparison of the two small
triangle correspondences. Endpoint equivariance excludes circle inversion;
the combined coefficient lines are trivial; Ono's sign formula gives
equal degree dependence after normalization. Independent overall signs
for the two families are allowed. Thus ordinary trace is ±4*alpha≠0.
Opposite integral signs would give trace(U⊕(-U))=0 for every U.

I wrote and ran independent_audit/recompute.py, importing no supplied code:
exact torus local-coefficient complexes, Ono (3.1)/(3.4) parity checks,
symbolic correspondence normalization with arbitrary corner terms, and
the formal two-by-two U trace identity. All pass; RSS ≈70 MiB, nice 10.
Unsigned, inversion, odd-shift and supertrace controls correctly give zero.
Geometry and source comparison are documented in independent_audit/AUDIT.md.
Ono source: https://arxiv.org/pdf/2504.20489, Proposition 3.1 and (3.4).
No ML score is involved; SBS and predictive baselines are inapplicable.

Strongest objection: symbolic checks cannot certify curve orientations or
regularity. I checked the critical-corner removability and flat-line argument;
the proof still uses the published global triangle classification and Floer
foundations. No independent compactification is claimed or needed as a new theorem.

NEXT BAR: Write the critical-corner family's signed clean-Morse count explicitly
in the original paper's conventions, including its de Rham comparison map.
