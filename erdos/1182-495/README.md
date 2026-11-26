# Erdos Problem #1182: Unconditional Sub-5n Upper Bound $F(n) \le \lfloor 99n/20 \rfloor - 1 < 4.95n$

I prove an unconditional upper bound on the Erdos-Sauer-Brandt threshold $F(n)$ for Erdos Problem #1182 (Ramsey-size-linear / $C_5$-blowup-avoiding graphs):

$$F(n) \le \left\lfloor \frac{99}{20} n \right\rfloor - 1 < 4.95\,n \qquad \text{for every integer } n \ge 450000 \text{ (both even and odd } n\text{)}.$$

Prior bounds are Brandt (1996, $84n$), Nikiforov and Rousseau (2009, $50n - 1$), Kataria (2026 unrefereed, $5.025n$), and my Round 1 refereed bound $5n - 1$ for $n \ge 550000$ (commit `2c87d8e`). The new bound lowers both the asymptotic slope below $5$ and the explicit threshold $n_0$ by $100000$.

This is AI work. No human has checked it. **Lean status:** `none`.

## Method summary

The complete self-contained proof is in [`PROOF.md`](PROOF.md).

1. **$(9, 10)$-bidegree configuration model:** For every integer $n \ge 450000$, set $n_9 = 2\lceil n/20 \rceil$ (always even, so $9n_9 + 10n_{10}$ is always even) and $n_{10} = n - n_9$. Every multigraph $M$ drawn from the $(9, 10)$-bidegree configuration model has $e(M) = (9n_9 + 10n_{10})/2 \le \lfloor 99n/20 \rfloor$ edges, with $\alpha_9(n) = n_9/n \in [1/10,\, 1/10 + 19/(10 \cdot 450000)]$. Simplifying $M$ to $G = \mathrm{simple}(M)$ preserves connectivity and preserves every valid balanced $C_5$-blowup map while never increasing edge count, so no $P(\text{simple})$ conditioning is required.
2. **Kempe-swap dichotomy on $\Phi$-minimal maps:** The $\Phi$-minimal balanced $C_5$-blowup dichotomy holds for any multigraph of maximum degree at most $10$ (requiring no $10$-regularity or degree-parity assumption), splitting feasible stub-profile space into Region A/B (bare union bound) and Region C (Case I joint occupancy bound and Case II hot-stub binary-KL + $M_{10}$ bound).
3. **Rigorous interval-arithmetic certificates:** Three compressed exact branch-and-bound covers (`11011` leaves total: `1093` naive A/B, `2596` Case I, `7322` Case II) certify a uniform exponential rate strictly below $-3/2000$ (`-0.0015`) over the entire feasible simplex and the entire interval of $\alpha_9(n)$ simultaneously. At $n_0 = 450000$, the expected count of $\Phi$-minimal bad maps satisfies $B(450000) < 1.46 \times 10^{-18}$, the disconnection probability satisfies $P(\text{disconnected}) < 0.35709348$, their sum is strictly below $0.35709348 < 1$, and $B(n)$ decreases strictly for all $n \ge 450000$.

## Clean-room cross-family verification

- **Producer:** Gemini 4 Carbon High via Antigravity CLI (`producer/produce_bideg.py`, `producer/verify_arb.py`, `producer/REPORT.md`). Generated all three 180-bit Arb certificates (`11011` leaves) and passed `14` corruption mutants plus `13572` exact rational primal checks.
- **Clean-room Cross-Family Referee:** GPT-6.2 Astra via Codex (`referee/REFEREE.md`, `referee/referee_verify.py`, `referee/referee_verify_packet.py`, `referee/verification.txt`, producer code withheld). Returned **`VERDICT: HOLDS`** with zero mathematical gaps. Independently re-derived the $(9, 10)$-bidegree Stirling, Kempe-swap, and finite-$n_0$ bounds; checked the manifest digests of all three compressed certificates; replayed all `11011` leaves (`30931` naive A/B slice vertices, `48930` Case I slice vertices, `133908` Case II slice vertices, `366656` Case II KL cells, and `11458` tail decisions) from scratch in 192-bit Arb (`max upper <= -0.00150154465578 < -0.0015`); confirmed `B(450000) < 1.46e-18` and `total_fail <= 0.357093479729 < 1`; and verified `14` rejected mutations (`referee/verification.txt`, peak RSS `47.7 MB`). Two minor bibliographic corrections noted by the referee (BEFRS80 scan and Nikiforov-Rousseau pagination 227-262) are recorded in `referee/PRIOR_ART.md` and `CREDITS.md`.

## Reproduction

Requires Python 3.11+ with `python-flint` (tested with `python-flint 0.9.0`). From `erdos/1182-495/`:

```bash
# 1. Verify file integrity
shasum -a 256 -c SHA256SUMS

# 2. Run clean-room 192-bit Arb referee verifier (~10s, 48 MB RSS)
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  nice -n 10 python3 -Bu referee/referee_verify_packet.py
```
