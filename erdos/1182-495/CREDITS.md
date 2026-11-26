# Credits

- **P. Erdos, R. J. Faudree, C. C. Rousseau, and R. H. Schelp** (1980): *An extremal problem in generalized Ramsey theory*, Ars Combinatoria 10 (1980), 193-203 (original problem statement).
- **S. Brandt** (1996): first linear upper bound `84n`.
- **V. Nikiforov and C. C. Rousseau** (2009): *Ramsey goodness and beyond*, Combinatorica 29 (2009), 227-262 (`50n - 1` upper bound).
- **S. Kataria** (2026): community unrefereed `5.025n` bound (`Sovi11/erdos-1182`).
- **Round 1 (`erdos/1182`, commit `2c87d8e`):** earlier refereed `5n - 1` ($n \ge 550,000$) bound using the $d = 10$ regular configuration model and Kempe-swap dichotomy.

## Verification provenance

This is AI work. No human has checked it. Lean status: `none`.

- **Producer:** Gemini 4 Carbon High via Antigravity CLI (generalized the Kempe-swap dichotomy to the $(9, 10)$-bidegree configuration model at $c = 99/20 = 4.95$, wrote `PROOF.md`, generated all three 180-bit Arb certificates totaling `11,011` leaves, and wrote `producer/verify_arb.py`).
- **Clean-room Cross-Family Referee:** GPT-6.2 Astra via Codex (producer code withheld). Returned `VERDICT: HOLDS` with zero mathematical gaps (`referee/REFEREE.md`, `referee/verification.txt`), independently replaying all `11,011` leaves at 192-bit Arb precision, verifying `B(450,000) < 1.46e-18` and `total_fail < 0.3571 < 1`, rejecting `14/14` mutations, and noting two bibliographic corrections in `referee/PRIOR_ART.md`.
