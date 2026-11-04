# C86 <= 1.80560940: classical auxiliaries on an adaptive density cone

Unrefereed. Upper bound on the Schur-Siegel-Smyth trace constant, Tao table [86a](https://teorth.github.io/optimizationproblems/constants/86a.html). No human expert has reviewed it line by line.

    C86 <= 288897505229428473 / 160000001279369600 < 1.80560940

It improves the 1.80580911 in [`../classical-half-cells/`](../classical-half-cells/) by about 0.0002, with the same proof by Smith's criterion. There are 28 auxiliaries from classical lists, 10 with nonreal roots, largest degree 21, on 5,375 rational nodes. `adaptive_checked-provenance.json` gives the source of each.

## What's here

- `certificate.json`: SHA-256 `10d68ec249f47c0504182d419fd8ddd1ca1c917e42a4bba59d944b9d1de0dad5`.
- `PROOF.md`, `METHOD.md`, `VERIFIER_NOTES.md`.
- `verify_linear.py`, `independent_verify.py`: two checkers, with their receipts and a closed-cover audit.
- `review/REVIEW.md`: a separate AI review with its own full-support proof check.

## What this doesn't show

The review passed every step and all 28 auxiliaries. It's AI, so it isn't a second party. No priority or optimality is claimed.

## Independent external replay

On 4 November 2026, GitHub user arhancanli posted an
[independent replay](https://github.com/teorth/optimizationproblems/pull/298#issuecomment-6638029022)
of the **C₈₆ ≤ 1.80560940** bound on PR #298, pinned to this folder at commit `0d82162`
(`certificate.json`, sha256 `10d68ec2…0dad5`). They wrote their own standard-library code
from the 86a page and this folder's README, PROOF.md, METHOD.md and VERIFIER_NOTES.md,
without reading or running our checkers or audit scripts. All six checks pass (E1–E6),
and their red controls are refused as expected. They recompute
T/m = 288897505229428473/160000001279369600 = 1.80560939324616691129…, so the printed
1.80560940 is T/m rounded up. Code:
[arhancanli/quantavane-replays @ bd52e926](https://github.com/arhancanli/quantavane-replays/tree/bd52e92675d1f7802d39dd2945a3184ca3ad15d1) (`c86/`).
They report no connection with the author and disclose AI assistance (Claude, Anthropic).

Their note: METHOD.md says the floating LP enforced a potential margin of 2·10⁻⁶ and
auxiliary integrals of 10⁻⁷. In the exact certificate the minimum of f is about
5.57·10⁻⁷ and the smallest integral about 8.95·10⁻⁸. Neither number is part of the claim,
which needs only both to be positive (PROOF.md), and both are. The replay checks the
computation; the minimum principle and Smith's results are cited theorems. It is not a peer review.

## Credit

The auxiliaries come from Flammang's and McKee's lists, as the provenance file records. Smith for the criterion, and Tomar for the adaptive nodes.

## AI use

Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also prepared the certificates, verifiers and this text. This does not claim a line-by-line human verification.
