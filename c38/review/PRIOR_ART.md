# Prior art for the adversarial C38 referee

Opened 2026-11-04 11:27 UTC, before writing any referee code. This is a
bounded independent review of an existing claim, not a search for a new bound.

The live [official table](https://teorth.github.io/optimizationproblems/constants/38a.html)
and its [raw source](https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/38a.md)
identify the ordinary square-lattice SAW connective constant and list Numaro's
lower bound 2.6273856. The exact attributed fraction is
2^128/129513673858566230428673965530967449326. The
[Numaro report](https://numaro.tech/research/self-avoiding-walk-connective-constant-2026/)
describes span 17, length 260, Kesten renewal and exact CRT enumeration.
Its [archive](https://doi.org/10.5281/zenodo.21546041) is already downloaded in
the producer's sources; the web reader could not open the Zenodo record.
Its polynomial arithmetic was independently checked without running its checker.
The original enumerator is reportedly absent, so full baseline reproduction
cannot be asserted from the certificate alone.

The stronger public method located is
[Vít Plánočka's point-evaluation transfer matrix](https://github.com/vitplanocka/saw-connective-constant),
with claimed bound 134217728/51082227. Public read-only repository and open
PR checks are recorded below. No producer or public enumerator/verifier
will be executed as evidence for this referee report.

The primary mathematical reference is
[Jensen 2004](https://arxiv.org/abs/cond-mat/0409381), implementing Kesten's
irreducible-bridge renewal and finite-lattice enumeration. Independent web
queries for 2026 self-avoiding-walk connective-constant lower bounds and the
two decimal claims found no additional lower-bound source in their returned
results. They did find recent upper-bound work, which is a different question.

Initial public-code/agent-repository queries included teorth's issues/PRs,
BakeLab/Epi-results, AlphaEvolve, EinsteinArena and openai/math terms.
Further bounded checks included the remaining mandated repositories,
GitHub recently-updated repository search and public community sources.
Search-index absence is not proof of absence. No novelty claim is made here.

## Completed bounded source checks

Read-only GitHub API retrieval found 58 open PRs. Title/body searches for
38a, connective and self-avoiding identified #313; its C38 patch changes an
upper bound, not the lower bound under review. Returned open issues were
also retained. `sources/open_pulls.json`, `sources/open_issues.json` and
`sources/pull313_files.json` preserve the queried material; this was not an
exhaustive inspection of every file patch in every PR.

The [repository search sorted by update time](https://api.github.com/search/repositories?q=self-avoiding+connective&sort=updated&order=desc&per_page=20)
returned Plánočka's repository and a simulation repository. Plánočka's
README confirms the stronger public fraction 2^27/51082227. This uses a
point-evaluation bridge transfer matrix and a disjoint supplemental family.
It is credited as relevant prior work, not executed as referee evidence.

Repository roots and READMEs were fetched directly for BakeLab/Epi-results,
google-deepmind/alphaevolve_results, openai/math, plasma-ai/erdos and
kisonecat/openai-math. The READMEs yielded no additional occurrence of
“connective”, “self-avoid” or “38a”. This is a README-level search, not a
claim to have audited all those repositories. The requested
google-deepmind/repository_of_problems endpoint returned HTTP 404.
EinsteinArena's public landing page and Erdős problem 528 were read.
Web queries for the two numerical lower bounds, recent arXiv work, and
public X/Reddit discussion returned no further relevant lower-bound
certificate in this bounded search. No account or posting operation was used.

The baseline arithmetic was independently reproduced in `baseline_audit.py`
from the local public bridge table, with exact positive renewal slack
approximately 2.046044770793534e-38. The table's entries through length 40
and spans 1–12 were independently enumerated. The original full span-17,
length-260 enumeration remains attributed; its generator was not available
in the supplied archive. See `results/BASELINE_AUDIT.json` and
`results/RECOUNT_COMPARISON.json`.

Primary-source downloads and errors are recorded in
`sources/READ_RECEIPTS.json`. The live table still lists Numaro's 2.6273856
lower bound; the stronger Plánočka public claim is therefore the relevant
public comparison even though it is not that table's current row. None of
these priority observations is needed for the candidate's finite-family proof.

The Zenodo API was subsequently accessible directly at
`https://zenodo.org/api/records/21546041` (saved as
`sources/zenodo_record.json`). All seven supplied archive files match their
published MD5 checksums, including the span-17 bridge table
`17a65c9ac2990e13785b79639abc6861`. The API file list confirms that the
original enumerator is not among the archived files. This repairs the
initial web-reader access gap without executing any archive program.
