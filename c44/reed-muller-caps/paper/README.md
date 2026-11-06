# PDF write-up of the C44 < 2.1974348818 candidate proof

`c44_reed_muller_caps.pdf` (13 pages) is a typeset transcription of [`../PROOF.md`](../PROOF.md) with the errata in [`../CORRECTIONS.md`](../CORRECTIONS.md) applied and marked. `c44_reed_muller_caps.tex` is its source (compiles with Tectonic).

Status: candidate, unrefereed. The proof and its checkers were produced by AI agents under Ricardo Pinho's direction; there has been no human line-by-line review. The exact comparison with the rational Q is non-strict (C44 <= Q, as in PROOF.md equation (12)); since Q < 2.1974348818, the decimal bound is strict.

An AI review (GPT-6 Astra) checked the PDF against PROOF.md, CORRECTIONS.md, candidate.json and caps.json and accepted it. Copy-pasted formulas from the PDF text layer can be garbled (floor and ceiling delimiters, large brackets); the rendered page is correct.

Revision of 6 November 2026: the opening of Section 4 (the energy grid and the Reed-Muller reduction, PROOF.md lines 173-197) is rewritten as Steps 1-7 with every step stated, and the paragraph combining equations (6) and (7) now treats d = 2 explicitly. The conclusions are unchanged, and the revised passage is marked in the PDF. A separate AI referee (GPT-6 Astra) checked the rewritten passage step by step and flagged two gaps: the ambient dimension n >= k+2 had to be fixed before the minimum-distance statement, and the case k = 1 was missing. Both are fixed, and its recheck accepted them. See [`review/section4-referee.md`](review/section4-referee.md) and [`review/section4-recheck.md`](review/section4-recheck.md). The earlier version is at commit [5cec092](https://github.com/rpinho/math-certificates/tree/5cec092/c44/reed-muller-caps/paper).
