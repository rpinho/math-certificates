# A degree-three local-weight cap and an improved relevant-variable bound

**Newest result:** [reed-muller-caps/](reed-muller-caps/) proves C₄₄ < 2.1974348818 (unrefereed, 1 November 2026).

**Earlier result:** [local-degree-caps/](local-degree-caps/) proves C₄₄ < 3.9819073803 (unrefereed, 1 November 2026).

**Earlier result:** [fourier-granularity/](fourier-granularity/) proves C₄₄ ≤ 4.1225323803 (unrefereed, 30 October 2026). Preprint: [hexagon:2610.00694](https://hexagonmath.org/2610.00694).

[Merged into Tao's optimization-constants table](https://github.com/teorth/optimizationproblems/pull/258)
on October 26, 2026 (UTC). The result remains unrefereed; table inclusion is not expert peer review or formal verification.

Ricardo Pinho · [ORCID 0009-0006-2744-2599](https://orcid.org/0009-0006-2744-2599)

This unrefereed preprint proves the claim **C₄₄ ≤ 4.3576549226**: every
Boolean function of positive polynomial degree d has at most
**4.3576549226 · 2ᵈ relevant variables**.

Read the [paper (PDF)](paper/c44.pdf) and [TeX source](paper/c44.tex).
The argument sharpens the degree-three local-weight cap to 5/4 and inserts
it into Wellens's recurrence, using BakeLab/Épi's existing exact degree
certificates. The preceding method reproduces at approximately
4.365467422574458; the exact horizon-96 bound improves by **1/128**.
The strongest preceding public headline located was Épi's **4.3654674227**;
Tao's merged table still listed Wellens's **4.394** at the audit time.
See [FINAL_LIVE_CHECK.md](FINAL_LIVE_CHECK.md) for the dated source check.
Exhaustive priority is not asserted.

The proof is not peer reviewed and not verified in a proof assistant.
No optimality is claimed. The programs check finite identities, recurrences,
tails and finite cases of the new lemma; the universal prose argument and
published theorem R₃ ≤ 10 remain mathematical dependencies.

## Reproduce

The recorded environment is Python 3.12.13, python-flint 0.9.0 and mpmath 1.3.0.
Both C44 checkers themselves use the Python standard library and require
Python 3.12 or later for this reproduction. With [uv](https://docs.astral.sh/uv/):

```sh
shasum -a 256 -c SHA256SUMS
uv run -q --python 3.12 --with python-flint==0.9.0 --with mpmath==1.3.0 sh reproduce.sh
```

Or install the recorded packages in a Python 3.12 environment and run
`PYTHON=python sh reproduce.sh`. The script runs both exact checkers and
the unchanged preceding-bound reproduction. Fresh outputs go to ignored
`reproduction-output/` and `logs/` directories.

Individual checker commands:

```sh
python -B verify_c44_exact.py certificates/c44_candidate.json
python -B independent/verify_c44_fraction.py certificates/c44_candidate.json
python -B reproduce_c44.py
```

The first checker uses rational power moments and a dyadic row recurrence
at horizon 96. It proves the exact upper bound
`172624496193406565421448533795/39614081257132168796771975168`.
The second uses Lagrange residues and a Fraction column recurrence at
horizon 72; its exact upper bound is
`10289221775138769568521/2361183241434822606848`.
Both display approximately 4.357654922574458 and are strictly below the
claimed decimal bound. Their source code and certificate inputs are
unchanged from the reviewed package.

Both checkers were written by the **same AI agent**, separately and without
importing each other or search programs. This provides algorithmic
cross-checks, without independent human review or formalization.

Clean archive-extraction receipts are in [verification/](verification/).
The original review rejection harness was executed unchanged: all 14 C44
checker/mutation combinations rejected. The archived
[C44 rejection results](verification/rejection_controls.json) cover
overclaiming, an unsupported cap, an altered theorem, a wrong lemma,
source-digest corruption, and corrupt weights or nodes with refreshed digests.
The paper's `python rejection_controls.py` command refers to that original
review harness, which is not included in this distribution; the public
reproduction script runs the two exact checkers and preceding recurrence.

`SHA256SUMS` covers every distributed file except itself. Rebuilding the
paper requires a TeX installation with amsart, lmodern, geometry, microtype
and hyperref; run `pdflatex` twice on `paper/c44.tex`.

## Credit and provenance

Chiarelli, Hatami and Saks introduced the weighted-variable framework.
Wellens supplied the restriction recurrence, block-sensitivity inequality,
symmetrization and infinite tail. BakeLab/Épi supplied the unchanged
degree-48 exact polynomial certificates, rather than new polynomial data
from this work. Tarannikov and Kirienko proved the ten-variable result in
resilient-function language; Krotov and Valyuzhenich state its Boolean-degree
consequence and also credit Zverev's computer-free argument.
The paper cites these sources, and [PRIOR_ART.md](PRIOR_ART.md) links them.
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) identifies the upstream data.

## AI use and author review

Analysis and proof drafting by AI agents under my direction; I reviewed the
results at summary level. AI agents also prepared the certificate, checkers
and publication materials. This does not claim a line-by-line human verification.

The publication edits only add this disclosure and public-release status
wording, including the no-optimality statement. Mathematical content is unchanged.

Original code, new certificate and documentation: [MIT](LICENSE).
Paper: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Third-party data retains its upstream rights.
