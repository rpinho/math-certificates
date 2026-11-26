# Credits

- **Daan van Berkel and Wieb Bosma**: posed Conjecture 4 (`\label{conj:except}`) and proved the finite-computation periodicity criterion (Lemma 7, `\label{lemma}`) in *On t-sumfree sequences* (`arXiv:2609.16843v2`, 2026).
- **Neil J. Calkin and Steven R. Finch** (1996): periodicity criteria for sum-free sets.

## Verification provenance

This is AI work. No human has checked it. Lean status: `none`.

- **Producer:** Gemini 4 Carbon High via Antigravity CLI (disproof at `d=4` and `d=6`, complete algebraic proof for all `d>=6`, exact finite certificates for `d=3..40, 50, 100`, and `producer/verify.py`).
- **Clean-room Cross-Family Referee:** GPT-6.2 Astra via Codex (producer code withheld). Independently certified all 40 cases, the general `d>=6` exclusion/inclusion/minimality proof, and 1,174 negative controls (`VERDICT: HOLDS WITH CAVEATS`), catching one symbolic schema typo (`blocks.U1` encoded as `[[1,0],[1,0]]` instead of `[[0,1],[0,1]]`) and six minor prose slips in `PROOF.md`. All seven referee corrections were applied to the published `certificates/witnesses.json` and `PROOF.md`, after which `referee/referee_verify_repaired.py` (identical to `referee/referee_verify.py` except for the updated witness SHA-256 lock) exited 0 with 0 scientific witness disagreements (`referee/referee_verify_repaired.log`).
