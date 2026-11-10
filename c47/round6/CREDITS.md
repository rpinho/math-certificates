# Credits and review scope

Doldrums / SCiEL (#341) supplied the public comparison and moves/insertions/removals idea. Our #321 and this PR (#350), by rpinho, supplied starting measures. T. S. Tomar (Tejasvi Singh Tomar) supplied the 50-atom measure and [v5, Section 6, Lemma 6.2](https://doi.org/10.5281/zenodo.23716077), following Yongxi Lin’s periodic construction and finite truncation-and-smearing argument.

No Tomar or Doldrums code was used for this continuation, verification or packaging. The historical round-1 packet did use Tomar’s unchanged exact checker, as its record says. The continuation uses the same mathematical method; no distinct-method or optimality claim is made.

Models: GPT-6.1 Sol via Codex (producer search, rational certificate, separately written verifier, controls, finite-instance check and packaging); GPT-6 Astra via Codex (clean-room AI referee using its own checker); Claude Code with Claude Opus 5.5 (coordination and prior PR-text revisions). Earlier review credits retained for the inherited construction: GPT-6 Astra and Claude Opus 5.5 via Claude Science. This is AI review, not human peer review.

Third-party consulted papers and repository files are omitted and identified by URL, version and hash in referee/sources/SOURCES.md. The consulted Tao table and its license are also omitted and identified in that inventory.
