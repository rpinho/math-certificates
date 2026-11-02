# Prior art and scope — C70

This note optimizes V. Patankar's existing cube-and-ball construction.
It does not introduce a new class of convex-body pairs, and exhaustive
priority is not asserted. The dated live audit is in
[FINAL_LIVE_CHECK.md](FINAL_LIVE_CHECK.md).

- [Tao and contributors, entry 70a](https://teorth.github.io/optimizationproblems/constants/70a.html):
  the dimension-free reverse Brunn–Minkowski constant for centrally symmetric
  convex bodies, with a determinant-one-in-absolute-value relative linear map.
- [Patankar's source, pinned tree](https://github.com/vidigoat/optimization-records/tree/c7c811aa06430527cccd5f992e41cd38dd9548ca/tao),
  [proof](https://github.com/vidigoat/optimization-records/blob/c7c811aa06430527cccd5f992e41cd38dd9548ca/tao/PROOFS.md)
  and [PR #226](https://github.com/teorth/optimizationproblems/pull/226):
  preceding lower bound 1.201927, cube side / ball radius 13/1000 in
  dimension 300000. Szász's inequality, AM–GM and Steiner's formula show
  that a relative linear position cannot improve this pair below the cube's value.
- [Patankar's unchanged interval script](https://github.com/vidigoat/optimization-records/blob/c7c811aa06430527cccd5f992e41cd38dd9548ca/tao/certificates/rbm_cube.py)
  was rerun with `--n 300000 --t 0.013`; an independently implemented Arb
  parity recurrence also encloses its value near 1.20192714257250284496.
  The unchanged script's displayed zero width is a formatting artifact,
  not a claim of an exact singleton. Raw receipts are in `verification/`.
- [Carlos Toledo's replay](https://carlostoledo.co/reports/optconst-queue.html),
  dated 16 October 2026, separately encloses that same preceding witness.
- H. Robbins, *A remark on Stirling's formula*, American Mathematical Monthly
  62 (1955), 26–29: factorial inequalities used by the rational checker.

The present paper optimizes a single normalized Steiner term, proves its
limit exp(1/(2e)), and gives a separate finite witness at n = 10¹².
The exact/interval programs certify arithmetic comparisons; they do not
formally verify the universal geometric argument or passage to the limit.

The public package distributes original checker code and certificate inputs;
Patankar's code and proof are linked, rather than relicensed or redistributed.
