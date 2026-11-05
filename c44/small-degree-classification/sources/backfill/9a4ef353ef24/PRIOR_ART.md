# C44 round 3 prior art — 2026-10-30

First file created in this directory, before code or search. This continues
../c44r2, whose unpublished exact candidate is 4.1225332505327437219488527317.
Its PROOF.md, REPORT.md, PRIOR_ART.md and post_sensitivity outputs have been read.
No novelty or public record claim is made. The sibling review directory is
currently empty; watch ../review_c44r2/REPORT.md and stop if a flaw is found.

Best located public method from the predecessor: weighted local degree
(Chiarelli–Hatami–Saks), Wellens's restriction/block-sensitivity recurrence,
and BakeLab/Épi rational discrete polynomial certificates. The predecessor
reported the official table at Pinho 4.3576549226*, with PR285 citation-only.
Our baseline strengthens block bounds by Fourier granularity plus Parseval.

Public sources to refresh before improvement:
- https://github.com/teorth/optimizationproblems/blob/main/constants/44a.md
- https://github.com/teorth/optimizationproblems/pulls and /issues
- https://github.com/BakeLab/Epi-results
- https://github.com/google-deepmind/alphaevolve_results
- https://github.com/google-deepmind/alphaevolve_repository_of_problems
- https://github.com/openai/math
- https://github.com/EinsteinArena
- https://github.com/plasma-ai/erdos
- https://github.com/kisonecat/openai-math
- https://github.com/queelius/boolean-degree-sensitivity
- https://arxiv.org/abs/2005.00566
- https://arxiv.org/abs/1801.08564
- Recent arXiv, updated GitHub metadata, indexed X/Reddit/blog sources.

Reproduce the inherited bound on the authorized CPU pod before improvements.
All heavy computation belongs on math-cpu-2. Only this authorized pod receives
job files; no publication, commits, pushes or messages to others.

## Initial gate and reproduction (18:55 UTC; notes consolidated)

Both independent inherited exact verifiers passed on the authorized pod before
improvement searches. Outputs: inherited/reproduced_row.json and reproduced_column.json.
Initial read-only audit receipts are sources/public_initial.json.gz and its
summary. All fetches succeeded. Main remained87b4ebbd, the live table listed
Pinho4.3576549226*, and all inherited visible open PR heads were unchanged.
Only PR285 touched44a and was citation-only; new PR293 concernedC9.

Named result-repository refs/READMEs, openai/math CONTENTS, awesome-ai-for-math,
and recently updated GitHub repository metadata searches were refreshed.
No stronger applicable public bound was located. Authenticated global code
search was unavailable; this is a bounded audit, not exhaustive absence evidence.
Web searches covered recent real-degree/sensitivity/Fourier-spectrum work,
indexed X/Reddit and relevant-variable bounds, with primary Wellens, CHS and
Krotov–Valyuzhenich opened. Recent elementary/rotation-symmetric papers concern
special classes and supply no universal improvement used here. A future Toulouse
seminar supplies no usable bound. Private communities were not searched.

## Review and corrected credit

The sibling review's final REPORT.md gives mathematical PASS and reports no
substantive gap, with subjective98% confidence. It identifies a prior-art
attribution GAP. Retained copy: inherited/REVIEW_c44r2.md.

- B4≤9 is prior public work of Koshta, PR283:
  https://github.com/teorth/optimizationproblems/pull/283 .
- B5≤14 follows from Stepanovs's 2012 computer-assisted exclusion of a fully
  sensitive15-variable degree-five function. We directly opened the thesis
  English abstract (PDFp3) and slides on2026-10-30:
  https://igors.org/theses/2012-boolean-deg-sens-gap-msc.pdf and
  https://igors.org/talks/2012-boolean-degree-sensitivity-gap.pdf .
  We read the claim; we did not replay the old C++ search.
- Towell already applies Fourier integer energy and exact linear certificates
  to conditional degree-five exclusions:
  https://github.com/queelius/boolean-degree-sensitivity and
  https://zenodo.org/records/23496542 . The full14-variable problem remains open
  in that work. The GitHub report web fetch missed cache; the direct public audit
  fetched its README and the sibling review retained/read the full report.
- Published CHS already gives the local-weight cap equivalence with R_d/2^d;
  the cubic cap is credited accordingly.

Neither B4/B5 nor the broad Fourier integer-energy methodology is claimed new.
The final gain uses exactly the inherited universal lattice criterion, with a
better-conditioned search implementation. Optional additional moment lemmas
are exploratory and do not support a bound unless their exact checker passes.

## Final source check, 19:27:42 UTC

sources/public_final.json.gz and public_final_summary.json contain the final
fresh refs, raw44a row, all34 visible PR diffs, issues, named repository
README/index reads, and sorted recent repository metadata searches. All reads
succeeded. Main87b4ebbd and the public4.3576549226* row are unchanged. Only PR285
edits44a and is citation-only; there is no newly located public C44 bound.
The final accepted local claim is C44<4.1225323803, using the inherited criterion
with stronger degree31–40 certificates. No public record or priority assertion
is made. Nothing was published or written to an external service.
