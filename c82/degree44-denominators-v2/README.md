# C82 < 0.253091834 with degree-44 denominators, second run (rigorous, verify_exact.py)

Unrefereed. This certifies an upper bound on the essential minimum of the Zhang-Zagier height, constant 82a in [Tao's optimization-constants table](https://teorth.github.io/optimizationproblems/constants/82a.html). No human expert has reviewed it line by line.

It replaces [`../degree44-denominators/`](../degree44-denominators/), 0.253123275, with the same construction and proof. Three of the denominators and most of the numerators are new.

The rigorous upper endpoint is 0.25309183355151 from `verify_exact.py` at 256 bits. That file is byte-identical to the earlier folder's. The separate integrator in `review/`, which shares no code with it, gives the numerical estimate 0.25309183355146 (estimate, review/integrate_gauss.py). That numerical estimate is diagnostic only: an independent replay (below) puts the true value about 1.3 · 10⁻¹⁵ above it. Only the `verify_exact.py` endpoint is rigorous.

## What's here

- `certificate.json`: 9 monic denominator factors, D = 1,000,000,000,064, and 47 numerator factors with exact rational exponents. SHA-256 `adfca0754f4d8b3a64398df22a506932743de7b0e49df542961530cb26c67ac2`.
- `METHOD.md`: what this run did and why it stopped.
- `verify_exact.py`, `check_verifier.py`: the checker and its controls. It imports no search code.
- `review/`: the separate exact algebra audit, root audit, derivative identities and whole-circle Gaussian integrator from the earlier review. They were rerun on this certificate. In `audit_algebra.py`, only the pinned hash and degrees changed.
- `receipts/`: output of every run.

The proof is `../degree44-denominators/PROOF.md`. It doesn't depend on which factors are used.

## Reproduce

Needs python-flint 0.9.0, and sympy for the controls. Run from this folder.

    python verify_exact.py certificate.json --target 0.253091833552 --precision 256 --tol 1e-11 --out out.json
    python check_verifier.py
    python review/audit_algebra.py certificate.json algebra.json
    python review/audit_roots.py certificate.json roots.json
    python review/check_derivation.py
    python review/integrate_gauss.py certificate.json --workers 8 --precision 256 --tol 1e-14 --target 0.253091833552 --out gauss.json

## What this doesn't show

Nobody re-derived anything new for this run, because the proof is unchanged. The review tools are AI-written and were rerun by the same agents that ran the search, so this isn't a second party.

The search stopped by a preset rule, so this says nothing about optimality.

## Credit

Doche's limit-point formula and factors, Grinsztajn's factors, and Épi's Ed5 and unequal multiplicities. The certificate format, joint LP and dual lattices come from the earlier certificates in this repository. The iterated IRLS/LLL numerator search and public baseline are vidigoat's. New here: three degree-44 denominators and the regenerated numerators.

## AI use

Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also prepared the certificate, checkers and this text. This does not claim a line-by-line human verification.

Code MIT, as in the repository licence.

## Independent external replay

On 4 November 2026, GitHub user arhancanli posted an
[independent replay](https://github.com/teorth/optimizationproblems/pull/301#issuecomment-6628606867)
of this folder's **C₈₂ ≤ 0.253091834** and of the first filing's 0.253123275
(`../degree44-denominators/`), on PR #301 (rigorous, verify_exact.py). With their own standard-library code,
written from the 82a page and the certificates' notes and sharing no code with the claimant’s
checkers, they enclosed B in [0.2530918335514613, 0.2530918335514614]
(printed bound minus upper end 4.5 · 10⁻¹⁰) and the first filing's B in
[0.2531232746206604, 0.2531232746206605] (3.8 · 10⁻¹⁰). Their red controls behaved
as expected. Code:
[arhancanli/quantavane-replays @ 087d768d](https://github.com/arhancanli/quantavane-replays/tree/087d768de15d74095bfc8f00ee9b35677e87b106) (`c82/`).
They report no connection with the claimants and disclose AI assistance (Claude, Anthropic).

Their note: the `review/` integrator's numerical estimate 0.25309183355146 is diagnostic only,
since the true B is about 1.3 · 10⁻¹⁵ above it (estimate, review/integrate_gauss.py). The PR's bound is unaffected, and
`verify_exact.py`'s 0.25309183355151 is a rigorous upper end, consistent with theirs.
The replay checks the computation; the reduction C₈₂ ≤ B for certificates meeting
H1–H3 remains a mathematical argument. It is not a peer review.

Primary PR attribution: @vidigoat (#280); author evidence is retained in sources/pr-280.json.
