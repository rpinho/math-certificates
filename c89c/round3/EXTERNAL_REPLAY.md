# External replay

On 8 November 2026, GitHub user arhancanli posted an
[independent replay](https://github.com/teorth/optimizationproblems/pull/308#issuecomment-6724784525)
of the **C89c >= 0.000033123924116** finite inequality on PR #308. They used
the certificate and `sources/graph8.g6` at commit `603b40c` and wrote their own
counting code; they did not read or run the checkers in `scripts/`.

Their result: the inequality holds for all 12,346 graph classes on 8 vertices.
The minimum, 1854939862512854832021/56000000000000000000000000, is at graph 905
and its complement, graph 11716, with the slack this packet states. They also
checked that the graph list is complete (orbit sum 2^28) and the certificate's
block structure, and their red controls were refused.

Not checked by them: the passage from the finite inequality to the asymptotic
bound (flag-algebra averaging and the disjoint-extension error term in
`PROOF.md`), which they read but did not formalize. It is not a peer review.

Code: [arhancanli/quantavane-replays @ 32d083f](https://github.com/arhancanli/quantavane-replays/tree/32d083f4bcb3fb91441e27adceb50137dec2a334/c89c) (`c89c/`).
They report no connection with the author and disclose AI assistance (Claude, Anthropic).
This file is outside this packet's SHA256SUMS and MANIFEST.json, which stay as frozen.
