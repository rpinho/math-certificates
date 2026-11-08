# External replay

On 8 November 2026, GitHub user arhancanli posted an
[independent replay](https://github.com/teorth/optimizationproblems/pull/317#issuecomment-6724784097)
of the exact numerical point behind the **C30 >= 10.42 (521/50)** candidate on
PR #317. They used `FIRST_MOMENT_PROOF.md` and
`artifacts/candidate_certificate.json` at commit `4f0bbf8` and wrote their own
interval code; they did not read or run `verify_candidate.py`.

Their result: the envelope coordinates are the Section 5 limits at the stated
parameters, and Phi >= 0.000183097093883 at z = 50/521, above the stated
0.00018309709357909. Their controls: 1/z = 10.4208 fails (the document puts
break-even near 10.4207), and Norton's equitable profile in place of the
envelope fails at z = 50/521, so the gain comes from the envelope.

Not checked by them: the mathematics (the value-word lemma, the marginal
equations, the first-moment family, the two-leaf cap, the envelope lemma and
Norton's machinery). The replay checks the final evaluation from the stated
profile, not that the profile is achieved. It is not a peer review.

Code: [arhancanli/quantavane-replays @ 367e97d](https://github.com/arhancanli/quantavane-replays/tree/367e97d01f678aa561d181884bd70a0fc4929731/c30) (`c30/`).
They report no connection with the author and disclose AI assistance (Claude, Anthropic).
This file is outside this packet's SHA256SUMS and MANIFEST.json, which stay as frozen.

Erratum (8 November 2026): arhancanli
[corrected](https://github.com/teorth/optimizationproblems/pull/317#issuecomment-6724941484)
their interval class, whose unary minus and abs() had rounded to Python's default
28-digit Decimal context. The fix is
[quantavane-replays @ 77ebb85](https://github.com/arhancanli/quantavane-replays/commit/77ebb859d0e12b81d0ee642ac4eb77ade05dbded);
every results file is byte-identical after it, and every comparison has a margin
above 10^-13, so no conclusion changes.
