# Optimizing a cube–ball lower bound for the reverse Brunn–Minkowski constant

[Merged into Tao's optimization-constants table](https://github.com/teorth/optimizationproblems/pull/259)
on October 26, 2026 (UTC). The result remains unrefereed; table inclusion is not expert peer review or formal verification.

Ricardo Pinho · [ORCID 0009-0006-2744-2599](https://orcid.org/0009-0006-2744-2599)

This unrefereed preprint proves the claim
**C₇₀ ≥ exp(1/(2e)) > 1.20194336847** for the dimension-free reverse
Brunn–Minkowski constant for centrally symmetric convex bodies.
A separate finite witness certifies **C₇₀ > 1.20194336**.

Read the [paper (PDF)](paper/c70.pdf) and [TeX source](paper/c70.tex).
The argument optimizes one term in V. Patankar's cube-and-ball construction.
His preceding public proposal, 1.201927, uses dimension 300000 and
cube side / ball radius 13/1000; its unchanged script and our Arb replay
give approximately 1.20192714257250284496.
The new limiting decimal lower endpoint exceeds that witness by more
than 0.000016225897. This is an optimization of the same construction.
See [FINAL_LIVE_CHECK.md](FINAL_LIVE_CHECK.md) for the dated source audit.

The paper is **not peer reviewed and not formally verified**.
Exhaustive priority is not asserted. No optimality over all convex-body
pairs is claimed. The geometric positioning reduction and limiting theorem
are proved in prose; the programs verify the arithmetic comparisons.

## Reproduce

The recorded environment is Python 3.12.13, python-flint 0.9.0 and mpmath 1.3.0.
With [uv](https://docs.astral.sh/uv/) installed:

```sh
shasum -a 256 -c SHA256SUMS
sh reproduce.sh
```

The script runs these pinned commands (set `UV` if uv is outside PATH):

```sh
uv run -q --python 3.12 --with python-flint==0.9.0 --with mpmath==1.3.0 python -B verify_c70_arb.py certificates/c70_candidate.json
uv run -q --python 3.12 --with python-flint==0.9.0 --with mpmath==1.3.0 python -B independent/verify_c70_rational.py certificates/c70_candidate.json
uv run -q --python 3.12 --with python-flint==0.9.0 --with mpmath==1.3.0 python -B verify_c70_arb.py --baseline
```

Fresh outputs go to ignored `reproduction-output/`. The certificate uses
even dimensions n = 10¹² and k = 367879441172, and normalized cube side
(n−k)/k = 632120558828/367879441172. Its retained term is approximately
1.2019433684431505669948027797355, strictly above 1.20194336.
The separate limiting value is approximately 1.20194336847031446719424113938.

Checker A uses 256-bit Arb factorial and ball-volume evaluation. Checker B
uses only standard-library rational arithmetic, logarithm series and Robbins
factorial bounds, with a rational Taylor enclosure of e for the limiting
decimal comparison. Both checkers were written separately by the **same AI
agent**, without importing each other or search programs. This provides
algorithmic cross-checks, without independent human review or formalization.

Clean archive-extraction receipts are in [verification/](verification/).
The original rejection harness ran unchanged and rejected all 32 combinations,
including all 18 C70 checker/mutation combinations. The archived C70 results
cover excessive finite and limiting bounds, dimension and scale errors,
invalid schema, and a valid but insufficient half-dimensional term.
The paper's `python rejection_controls.py` command refers to the original
review harness, which also depends on another problem's inputs and is not
included in this C70 distribution. The public reproduction script runs both
C70 checkers and the preceding-bound Arb recurrence.

`SHA256SUMS` covers every distributed file except itself. To rebuild the paper,
run `pdflatex` twice on `paper/c70.tex` with amsart, lmodern, geometry,
amsmath, amssymb, booktabs, microtype, url and hyperref installed.

## Credit and provenance

V. Patankar (GitHub vidigoat) supplied the cube-and-ball construction and
its positioning reduction using Szász's principal-minor inequality, AM–GM
and Steiner's formula. The contribution here is its optimized single-term
limit and finite arithmetic certificate. Carlos Toledo independently replayed
the preceding witness. Robbins supplied the factorial inequalities used
by the rational checker. [PRIOR_ART.md](PRIOR_ART.md) links these sources.

## AI use and author review

Analysis and proof drafting by AI agents under my direction; I reviewed the
results at summary level. AI agents also prepared the certificate, checkers
and publication materials. This does not claim a line-by-line human verification.

Publication edits only update release status and this disclosure. The
same-AI-agent statement and Patankar credit were already in the approved
note and are retained. Mathematical content is unchanged; see
[PAPER_CHANGES.md](PAPER_CHANGES.md) for every paper change.

Code, certificate and documentation: [MIT](LICENSE).
Paper: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
