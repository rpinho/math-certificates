# Prepared C47 table rows — not filed

All starred entries are preprints or **candidate, unrefereed**. The candidate is further hole-filling on Tomar's measure: the same insertion-and-refinement operation as his hf.py, applied by our own search scripts, with no novelty claim.

Suggested main table row, preserving the table's existing link style:

| [47](https://teorth.github.io/optimizationproblems/constants/47a.html) | Centered Hardy–Littlewood maximal constant in dimension $2$ | 1.70311* | 3.59123* |

Append these chronological entries under the respective C47a lower/upper tables:

| Bound | Reference | Comments |
| --- | --- | --- |
| $1.7027237335^*$ | [Tom2026] | **Tejasvi Singh Tomar's lower bound.** His 50-atom rational periodic measure refines Lin's lattice. Exact certificate ratio $482167717377842991882283179477574801392641890014291050323/283174368139841919615520431313000857449005056000000000000=1.7027237335962937\ldots$, rounded down here. Reproduced by his unchanged v5 checker. Preprint, unrefereed. |
| $1.70311^*$ | [C47r2] | **Candidate:** further hole-filling on Tomar's measure (the same insertion-and-refinement operation as his hf.py; our scripts). The 59-atom single-period half-cell has exact witness ratio $215956002657486428307163448091951082893881/126800499112387565339223240212480000000000=1.7031163455127832\ldots$. The display is rounded down. Explicit rational witnesses pass a verifier **separately written (same agent)** and Tomar's unchanged checker; all seven corruption controls reject. Uses **Tomar's Lemma 6.2, following Lin**. Candidate, unrefereed; no distinct-method or novelty claim. |

| Bound | Reference | Comments |
| --- | --- | --- |
| $3.59123^*$ | [Tom2026] | **Tejasvi Singh Tomar's upper bound**, using Lin's kernel comparison principle. Certificate parameters $\alpha=47/40$, $R=33/20$, $h=1/32$; half-integral approximately $3.5912243275064523$, rounded up. His source provides interval checkers and Lean proofs. This job did not rerun the upper-bound verification. Preprint, unrefereed. |

Suggested “Reading the tables” sentence:

> The strongest bounds in these proposed rows are the candidate lower bound $1.70311^*$, obtained by further hole-filling on Tomar's measure (the same insertion-and-refinement operation as his hf.py; our scripts) [C47r2], and Tomar's upper bound $3.59123^*$ [Tom2026]. Tomar's own certified lower bound is $1.7027237335^*$. Starred entries are unrefereed.

References:

- **[Tom2026]** Tomar, Tejasvi Singh. *Bounds for the weak type (1,1) constant of the centred maximal operator over squares.* October 2026, preprint, not peer reviewed. [Author page](https://www.mefyi.com/papers/weak-type-squares/); [v5 paper](https://doi.org/10.5281/zenodo.23716077); [supplement](https://doi.org/10.5281/zenodo.23716078); [v5 source](https://github.com/tejasvi/square-maximal-weak-type/tree/v5), commit `3af09fc359ce262f4a7f63d34b0d97e6d4d95d1a`. Lower: Section 6, Lemmas 6.1–6.2, `lowerbound/c2lower_1p70272.json`, `lowerbound/search/hf.py`. Upper: Sections 2–5, `cert/cert_h32_a4740_R3320_3p59123.json`.
- **[C47r2]** Local candidate certificate and report, math_c47r2_1103, 3 November 2026: [PROOF.md](PROOF.md), [README.md](README.md), [59-atom witness certificate](certificates/half59.json). This is an unfiled local reference, not a public publication or priority assertion. Attribution: further hole-filling on Tomar's measure: the same insertion-and-refinement operation as his hf.py, applied by our own search scripts, using his Lemma 6.2 following Lin.

No table was modified outside this job directory. No commit, push, PR, post or message was made.
