# C44 <= 4.1225323803 (unrefereed)

Exact upper bound on C44, the constant in the relevant-variable bound r(f) <= C 2^deg(f), Tao table
[44a](https://teorth.github.io/optimizationproblems/constants/44a.html).

    C44 <= 163310332697516761417555720251 / 39614081257132168796771975168 < 4.1225323803

The previous table value is 4.3576549226, in this repository's root.

## What changed

Two inputs to Wellens's recurrence, with Épi's degree-48 certificates unchanged:

1. Equality in D(f) <= d/2 is excluded for d >= 3, which gives caps 31/16 at degree 4 and 447/128 at degree 7.
2. Fourier coefficient granularity plus Parseval gives a rational certificate criterion for block sensitivity,
   with 37 certificates at degrees 4 to 40.

The written proof is `PROOF.md`, with the inherited caps in `baseline/PROOF.md`.

## Credit

Wellens's recurrence and block-sensitivity theorem, Chiarelli, Hatami and Saks's weighted method, and BakeLab/Épi's
certificates are the base. R3 <= 10 (Tarannikov and Kirienko) and Wellens's inequality are cited, not reproved.
B4 <= 9 was already public in [PR 283](https://github.com/teorth/optimizationproblems/pull/283) (Koshta), and
B5 <= 14 follows from [Stepanovs's 2012 thesis](https://igors.org/theses/2012-boolean-deg-sens-gap-msc.pdf). Coefficient
granularity and the Fourier L1 estimate are standard. No exhaustive priority or optimality is claimed.

## Check it

Needs Python 3 and the standard library.

    python3 verify_spectral.py spectral_certificate_round3.json
    python3 verify_bound.py
    python3 verify_column.py
    python3 verify_controls.py
    python3 verify_rejections.py

`verify_bound.py` and `verify_column.py` are separately written and use horizons 96 and 72. The checkers write their own
`verification_*.json` receipts.

## Status

Unrefereed. No proof-assistant formalization and no independent human review. The checkers were written by AI agents.
A third checker by a different AI agent, written from the proof text, reproduced the certificates and the endpoint, and
separate AI reviews found no mathematical gap. None of that is a second party.

Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also
prepared the certificates, checkers and this text. This does not claim a line-by-line human verification.
