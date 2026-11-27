# Credits

- **Earlier work.** ElonSG and contributors on TrureTuring gave the same four-term enumeration for every admissible $r,k,d$, including $d=0$. [PR #14905](https://github.com/the-omega-institute/trureturing/pull/14905) opened on 2026-10-09 at 21:12:51 UTC. Its checked Lean revision is dated 2026-10-10 at 15:52:32 UTC, and the PR closed on 2026-10-12 without merging. [Knowledge Sense](https://raw.githubusercontent.com/KnowledgeSense/math/91f1bdd2a10abeb28acc742ce3ee884874caf124/preprints/Enumeration-of-Extendably-312-Avoiding-Alternating-Sign-Rectangles-October-12-2026/lean/README.md) also gave a full-domain proof in a commit dated 2026-10-14 at 06:28:04 UTC.
- **Hans Hongesberg, Matjaz Konvalinka, and Svante Linusson**: posed Conjecture 4.5 (`\label{conj:312-formula}`) and established the recursive characterizations in *Pattern avoidance in alternating sign rectangles I: Extended avoidance* (`arXiv:2610.07442v1`, Oct 2026).
- **Robert Johansson and Svante Linusson** (2007): introduced pattern avoidance for alternating sign matrices (`Annals of Combinatorics` 11, 471-480).

## Verification provenance

This is AI work. No human has checked it. Lean status: `none`.

- **Producer:** Gemini 4 Carbon High via Antigravity CLI (derived the compact generating function `Phi_{r,k}(z)`, the two Schroder substitution identities, the Laurent-residue boundary proofs, and the Chu-Vandermonde closure in `PROOF.md`, and wrote `producer/verify_proof.py`).
- **Clean-room Cross-Family Referee:** GPT-6.2 Astra via Codex (producer code withheld). Returned `VERDICT: HOLDS` with zero mathematical gaps (`referee/REFEREE.md`, `referee/verification.txt`), independently enumerating all `7,575` ASRs through `5 x 5`, all `429` order-5 ASMs, all `51` Table 2 cells, all `45,526` triples through `50`, exact formal-series and Laurent-residue checks through degree `36`, and `7` negative controls in `2.36s`.
