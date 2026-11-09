# C86: Schur–Siegel–Smyth trace constant

C86 is the smallest limiting trace-to-degree ratio of totally positive algebraic integers: the liminf of the mean of all conjugates, with finite exceptions allowed. The rigorous upper bound is `C86 ≤ 1561194641062402479525057156208744733/864691128455135125642991200018366464 < 1.8054939963`, computed by `verify_linear.py` and replayed by the clean-room referee’s own `referee/referee_check.py` with `referee/cover_check.py`. The fraction is the directly checkable mean T/m of the finite rational density certificate. Smith’s theorem realizes it as a limiting normalized trace; there is no separate extrapolated value.

Compared with V. Patankar’s [PR #270](https://github.com/teorth/optimizationproblems/pull/270), the margin below the displayed 1.8054956 is greater than 0.0000016037 (rigorous, `comparison.py`). The margin below our 1.80560940 currently filed in this PR (#298) is greater than 0.0001154037 (rigorous, `comparison.py`). The margin below the live table’s 1.8084990 is greater than 0.0030050037 (rigorous, `comparison.py`). Cited values are refreshed in PRIOR_ART.md.

The certificate uses 31 auxiliaries (11 with nonreal roots, maximum degree 21), 7,418 rational density nodes and 6,308 positive-density cells. Every auxiliary’s coefficients, weight and list or generation source are in auxiliary-provenance.json. The certificate SHA-256 is `e5fb93f6c31d2e3b38c986ac71c1d076414d680429fb2cbb91db77fb2e12c9d8`.

Two producer checkers and the cover/hash audit pass. A clean-room AI referee on a different model, GPT-6 Astra via Codex, wrote its own checks and returned HOLDS. This is AI review and replay, not human review. The earlier external replay of the adaptive-cone certificate applies only to that earlier value; it is not evidence of an external replay of this certificate. The table asterisk stays.

Verification level: L1 for the finite certificate; L0 for the bound as a whole because the all-size minimum-principle/resultant reduction remains in prose. Definitions: https://github.com/rpinho/math-certificates/blob/59eeb7097f806da05187b5f234445be3589204d4/VERIFICATION_LEVELS.md .

See PROOF.md for the argument, REPRODUCE.md for commands, CREDITS.md for attribution, and referee/REFEREE.md for the AI referee’s assessment. Producer receipts are under receipts/ and fresh release outputs under release_validation/. Regenerable leaf covers and corrupted witness certificates are omitted; hashes and regeneration commands identify them.

AI use and author review: Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also prepared the certificate, checker and submission text. This does not claim a line-by-line human verification.
