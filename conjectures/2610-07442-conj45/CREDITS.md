# Credits

- **Hans Hongesberg, Matjaz Konvalinka, and Svante Linusson**: posed Conjecture 4.5 (`\label{conj:312-formula}`) and established the recursive characterizations in *Pattern avoidance in alternating sign rectangles I: Extended avoidance* (`arXiv:2610.07442v1`, Oct 2026).
- **Robert Johansson and Svante Linusson** (2007): introduced pattern avoidance for alternating sign matrices (`Annals of Combinatorics` 11, 471-480).

## Verification provenance

This is AI work. No human has checked it. Lean status: `none`.

- **Producer:** Gemini 4 Carbon High via Antigravity CLI (derived the compact generating function `Phi_{r,k}(z)`, the two Schroder substitution identities, the Laurent-residue boundary proofs, and the Chu-Vandermonde closure in `PROOF.md`, and wrote `producer/verify_proof.py`).
- **Clean-room Cross-Family Referee:** GPT-6.2 Astra via Codex (producer code withheld). Returned `VERDICT: HOLDS` with zero mathematical gaps (`referee/REFEREE.md`, `referee/verification.txt`), independently enumerating all `7,575` ASRs through `5 x 5`, all `429` order-5 ASMs, all `51` Table 2 cells, all `45,526` triples through `50`, exact formal-series and Laurent-residue checks through degree `36`, and `7` negative controls in `2.36s`.

## Prior unmerged public work note

A subsequent check of `the-omega-institute/trureturing` showed open issue #14736 (2026-10-09), which records an unmerged lane branch (PR #14905, closed without merge on 2026-10-12) reporting a Lean formalization of Conjecture 4.5. The proof and standalone exact verification in this directory were produced independently from the arXiv preprint without reading that branch.
