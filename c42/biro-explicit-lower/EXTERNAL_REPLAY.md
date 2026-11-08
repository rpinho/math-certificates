# External replay

On 8 November 2026, GitHub user arhancanli posted an
[independent replay](https://github.com/teorth/optimizationproblems/pull/310#issuecomment-6717401133)
of the explicit **C42 >= 1/2 + 2^-4096** on PR #310. They used
`inputs/lower_certificate.json` and `LOWER_PROOF.md` at commit `36325fa` and
wrote their own code; they did not read or run `verify_lower_exact.py`.

Their result: they re-derived sections 1 to 8 step by step and found no false
step, and all 39 numerical steps of the parameter chain, (5) to (32), hold
exactly, with every inequality in r = 1/sqrt(2) and cos(pi/8) decided in
Q(sqrt 2). Their red controls were refused, including the claim strengthened
to 1/2 + 2^-4094 with the same auxiliary parameters.

Not checked by computation: the geometric and analytic steps (the projections,
the first-escape angle, the law of cosines, the Cauchy-Schwarz steps and the
compactness argument of section 8). They read each and found no gap, which
they describe as a reading, not a computation. It is not a peer review.

Code: [arhancanli/quantavane-replays @ f425a19](https://github.com/arhancanli/quantavane-replays/tree/f425a192d48a91d72421190d79eaff9f72a16e6a/c42) (`c42/`).
They report no connection with the author and disclose AI assistance (Claude, Anthropic).
This file is outside this packet's SHA256SUMS, which stays as frozen.
