# C68 >= 0.44667 (unrefereed)

Lower bound on Korenblum's constant in the Bergman space, Tao table
[68a](https://teorth.github.io/optimizationproblems/constants/68a.html).

## What changed

David Niedbala Giraudin's flux and half-diameter lemmas ([PR 274](https://github.com/teorth/optimizationproblems/pull/274))
give 0.446, with a certificate at 0.44605. That scalar framework stops near 0.44607. This proof keeps an angular
coefficient term that the framework throws away, through an even outer factor and a contact-parameter estimate, and
certifies c = 0.44667. `PROOF.md` is the entry point. The other lemma files hold the analytic steps.

## Credit

The flux input is Niedbala Giraudin's. The moment integration is Wikström's method (arXiv:2607.17748), the coefficient
estimate is Wang's, and the covering-strip approach is from this repository's earlier 0.432 certificate.

## Check it

Needs Python 3, python-flint and mpmath.

    python3 verify_exact.py certificate-contact-044667.json --output arb.json
    python3 verify_interval.py certificate-contact-044667.json --output interval.json
    python3 verify_controls.py

`verify_exact.py` uses Arb at 320 bits and `verify_interval.py` uses mpmath intervals at 340 bits. They check the
numerical hypotheses of the lemmas, not the prose. `verify_controls.py` corrupts the certificate and covers and confirms each is rejected.

## Status

Unrefereed. No proof-assistant formalization and no independent human review. The checkers were written by an AI agent. A
separate AI review found no substantive gap in this proof or in PR 274. That is not a second party.

Analysis and proof drafting by AI agents under my direction; I reviewed the results at summary level. AI agents also
prepared the certificates, checkers and this text. This does not claim a line-by-line human verification.
