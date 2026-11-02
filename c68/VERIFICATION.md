# Publication verification — 19 October 2026

PASS from a fresh filesystem copy of `hexagon_candidate/`, using Python 3.12
and python-flint 0.9.0. Certificate and checker bytes were compared to the
source bundle; discovery/search code was not used.

| Command | Result |
| --- | --- |
| `PYTHON=python sh reproduce.sh` | Both original-model exact checkers PASS, c = 0.42638465 |
| `PYTHON=python sh reproduce-jung.sh` | Both geometric-model exact checkers PASS, c = 54/125 = 0.432 |
| `python mutation_tight_controls.py` | All 8 checker/control combinations rejected as intended |
| `python mutation_jung_controls.py` | All 10 checker/control combinations rejected as intended |
| `python audit_jung_arithmetic.py` | All 17 elementary arithmetic enclosure checks PASS |

Both moment families include analytic infinite-tail arguments. Each mutation
run includes refusing Python execution with assertions disabled (`-O`). The
JSON receipts record the certificate hashes and individual diagnostics.
Raw rerun logs are retained in the research workspace under
`publication_checks/`. The checkers certify quantitative hypotheses, not the
analytic proof as a formal theorem. This unrefereed proof remains subject to
independent mathematical review.

The paper was built with Tectonic 0.17.0; the five-page PDF was checked for
the author, ORCID, bound, references, and summary-level author-review statement.
