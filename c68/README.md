# Korenblum’s constant: a certificate for C₆₈ ≥ 0.432

**Newest result:** [signed-contact/](signed-contact/) proves C₆₈ ≥ 0.44685 (unrefereed, 1 November 2026).

**Earlier result:** [contact-spectral/](contact-spectral/) proves C₆₈ ≥ 0.44667 (unrefereed, 30 October 2026). Preprint: [hexagon:2610.00696](https://hexagonmath.org/2610.00696).

[Merged into Tao's optimization-constants table](https://github.com/teorth/optimizationproblems/pull/239)
on October 26, 2026 (UTC). The result remains unrefereed; table inclusion is not expert peer review or formal verification.

Ricardo Pinho · [ORCID 0009-0006-2744-2599](https://orcid.org/0009-0006-2744-2599)

Preprint: [hexagon:2610.00399v1](https://hexagonmath.org/2610.00399?version=1) · Zenodo [10.5281/zenodo.23483542](https://doi.org/10.5281/zenodo.23483542)

This unrefereed preprint gives an analytic argument and an exact rational
certificate for **c₂ ≥ 54/125 = 0.432** in the unweighted Bergman space A²(D).
It combines a two-zero covering-strip Schwarz estimate, the classical hyperbolic
Jung inequality, and Wikström’s moment-duality criterion. A twelve-atom measure
with Lebesgue tail on [0.999, 1] supplies the required moment inequalities.
No optimality or proof-assistant formalization is claimed. The programs check
the quantitative hypotheses; the analytic proof requires mathematical review.

Read the [paper (PDF)](paper/korenblum.pdf), [TeX source](paper/korenblum.tex),
and [analytic derivation](GEOMETRIC_LEMMA.md). The strongest public certified
lower bound located before this publication is Wikström’s **0.4263**; see
[FINAL_LIVE_CHECK.md](FINAL_LIVE_CHECK.md) for the dated search and its limits.

## Reproduce

Python 3.12 and python-flint 0.9.0 were used for the publication checks.
From a fresh checkout:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
shasum -a 256 -c SHA256SUMS
PYTHON=python sh reproduce-jung.sh
PYTHON=python sh reproduce.sh
python mutation_jung_controls.py
python mutation_tight_controls.py
python audit_jung_arithmetic.py
```

The `reproduce-jung.sh` script runs two separately implemented checkers on
`certificate-jung.json`: Arb ball arithmetic and standard-library outward
integer interval arithmetic. Neither imports the search or the other checker.
Both cover every moment index, using finite recurrences and analytic infinite
tails. The rational checker also runs without third-party packages:

```sh
python3 verify_jung_rational.py certificate-jung.json
```

`reproduce.sh` checks the separately retained **0.42638465** certificate using
Wang’s original analytic estimate and Wikström’s moment lemma. Its checkers
are `verify_envelope_arb.py` and `verify_envelope_rational.py`. The published
0.4263 baseline measure and earlier verification receipts are also included.
The `verification-*.json` and mutation receipts record the clean-copy publication
rerun; timings and process IDs are informational. Mutation controls must reject
bad moments, unsafe envelopes, false infinite tails, and disabled assertions;
the Jung controls also reject the wrong analytic model. The arithmetic audit
checks 17 independent elementary enclosures against 100-digit Arb.

`SHA256SUMS` records all distributed files except itself. Reproduction rewrites
receipts, so check hashes before running commands if checking the archived bytes.
The certificate is the proof input; no optimizer is needed.

## Credit and review status

Korenblum introduced the maximum principle, and Hayman proved a positive radius
exists. Credit goes to Wang and Schuster for the annular-pseudodistance approach,
to classical Schwarz factorization and hyperbolic Jung, and to Frank Wikström
for moment duality, the atomic-plus-Lebesgue measure form, and the LP/refinement
strategy. The paper gives references, including [Wikström’s preprint](https://arxiv.org/abs/2607.17748)
and [original software](https://doi.org/10.5281/zenodo.21446369).

**AI use and author review:** Analysis and proof drafting by AI agents under my
direction; I reviewed the results at summary level. AI agents also prepared
the certificate, checking software, and publication materials. This does not
claim a line-by-line human verification. Independent review is welcome.

MIT license; see [LICENSE](LICENSE).
