Shipped: Clean-room cross-family referee verification (`VERDICT: HOLDS`) of the repaired Case I proof and 160-bit Arb certificate (`09fba47458edf71cf255b63bb3842e4360b7d275748543c61c9b6fe494bf0611`) establishing $F(n) \le 5n - 1$ for every integer $n \ge 550{,}000$ (including odd $n$) in Erdős #1182.

## Summary & Verification Status
- **Novelty of this referee job:** **no** — this job is an independent sealed cross-family referee audit of `gpt-6.2-sol`'s repaired Case I proof and certificate for $F(n) \le 5n - 1$ ($\forall n \ge 550{,}000$, which itself beats Kataria's cited unrefereed $5.025n$ bound under the same definition of $F(n)$). No statistical holdout applies because the certificate proves a deterministic universal inequality over a compact polytope partition.
- **Hash locks verified (`verify.log` lines 2–6):**
  - `inputs/cert_naive_ab.json.gz`: `b4cbc312f5f1a042990c031df8b35542eb6f192639ea93edf024b61002ec5989` (EXACT MATCH)
  - `inputs/cert_case2.json.gz`: `c68d3339047880b19de426b6bde3114630ce10ad853ecc409926f621d5c3bab8` (EXACT MATCH)
  - `inputs/cert_case1.json.gz`: `09fba47458edf71cf255b63bb3842e4360b7d275748543c61c9b6fe494bf0611` (RECORDED & CERTIFIED)
- **Mathematical & 160-bit Arb audit (`REFEREE2.md`, `verify.log`, `finite.log`):**
  - Re-derived from scratch the strict increase of $g(a_0, Q_{03}) = a_0 \log(1 - (1 - Q_{03}/a_0)^{10})$ in $Q_{03}$, its strict decrease in $a_0$ for $a_0 > Q_{03} > 0$ (continuous nonincrease on $(0,\infty)$), the upper-cutoff split ($Q_{03} \le q_*$ occupancy at $(a_{0,\min}, q_*)$ vs. $Q_{03} > q_*$ binary-KL tail $U - 5\mathcal{D}(2q_*, 2B_{03})$), and the exempt-set prefactor $\le (10n+1) n^{19} 20^{19}$ over all $(10n+1)^5$ symmetric blue matrices $K$ with zero typical-$K$ truncation.
  - Standalone verifier `arb_case1_referee.py` (`python-flint 0.9.0`, 160-bit outward-rounded Arb, stdlib only) reconstructed all `3,049` records from exact `[0, 4001/10000]^5` (`1,524` strictly interior splits, `766` `'N'` leaves, `759` `'C'` leaves, `0` uncovered/truncated/trailing records).
  - Recomputed leaf bounds from scratch (ignoring stored leaf bounds) passed `<= -1/1000` on every leaf under both the outer tightened sliced-box superset $H(B')$ (`15,523` `'C'` vertices, max `-0.0010000010201557`) and the exact Region C polytope $P_C(B)$ (`15,446` `'C'` vertices, max `-0.0010000010201557`), and matched `-0.0010000010000072` with stored $U_t$. Every occupancy leaf (`759/759`) satisfied $q_* \ge B_{03}$ strictly ($\min(q_* - B_{03}) \ge +7.814076 \times 10^{-4}$).
  - At $n_0 = 550{,}000$, $\mathbb{E} X_{\mathrm{rigid}} \le 4.260164364954 \times 10^{-11} < 4.261 \times 10^{-11}$; adding disconnection bound $3/13$ (or $e/(16-e)$) gives $0.230769230812 < 1$, with log-derivative $\le 33/n - 1/1000 \le -0.00094 < 0$ for all $n \ge 550{,}000$ (even and odd $n$).
- **Referee controls (`controls.log`):** `1,518/1,518` feasible $(a, Q)$ pairs (`759` near + `759` tail) satisfied `true_rate <= recomputed_leaf_bound <= -0.001`; the $d = 10$ positive bare witness (`+0.00336352695 > +0.00336`) was rejected when `record[716]` was mutated `C -> N`; and `10/10` corrupted Case I certificates exited non-zero.

## Mandatory Audit Checks
- `CONTROLS:` No — no assumption overrode what the controls show (`controls.log` lines 4–29, `verify.log` lines 8–18, run via `OPENBLAS_NUM_THREADS=1 nice -n 10 /Users/ricardo/dev/open-science/.venv/bin/python -B controls_referee.py`): `1,518/1,518` feasible $(a, Q)$ checks passed (`min_near_slack = 8.7899e-2`, `min_tail_slack = 9.8555e-2`); the $d = 10$ bare witness (`L = +0.00336352695`, line 12) caused immediate rejection under a naive leaf check (`record[716]`, $U = +0.01095225$, line 16); the old lower-cutoff formula failed by `+0.101660554` (line 17); and `10/10` corrupted certificates exited `1` (lines 19–29), including surgical `mutant_2_cutoff_below_B03` on `record[22]` (line 22).
- `CONTRADICTING:` No — no contradicting data, region, or tail was dropped or ignored (`controls.log` lines 5–17, `verify.log` lines 9–15, `finite.log` lines 6–15, `inputs/LEMMAS.md` lines 24 & 115): the positive bare first-moment region (`+0.00336352695`) is retained and certified via occupancy leaf `record[716]` (`L + g = -0.0171654 < -0.001`); all `759` upper-tail cells ($Q_{03} > q_*$) are evaluated alongside all `759` near cells ($Q_{03} \le q_*$); and the finite-$n$ bound counts all $(n+1)^4$ profiles, all $(10n+1)^5$ symmetric blue matrices $K$, and all $10n+1$ Case II hot counts $R$ without truncation.
- `LABELS:` No — no stored bound or pre-assigned label was trusted without checking raw data (`arb_case1_referee.py` lines 78–103 & 330–710, `controls_referee.py` lines 51–73 & 185–278, `verify.log` lines 2–16, `controls.log` lines 4–29): SHA-256 digests were verified on raw `.gz` files; `arb_case1_referee.py` recomputed $U_t$, $B_{03}$, near occupancy, and binary-KL tail bounds directly from exact rational vertices (`15,523` outer / `15,446` exact Region C), tilts, and cutoffs; and `controls_referee.py` checked exact symmetry, nonnegativity, red-pair zeros, and row sums of $Q$ and assigned near/tail directly from $Q_{03} \le q_*$ vs. $Q_{03} > q_*$.

## Exact Reproduction Commands
```sh
cd /Users/ricardo/dev/open-science/math_wave_1030/e1182kempe_referee2
export OPENBLAS_NUM_THREADS=1
PYTHON=/Users/ricardo/dev/open-science/.venv/bin/python
nice -n 10 "$PYTHON" -B arb_case1_referee.py | tee verify.log
nice -n 10 "$PYTHON" -B arb_case1_referee.py --finite-only | tee finite.log
nice -n 10 "$PYTHON" -B controls_referee.py | tee controls.log
```

## Sources, Limitations & Next Steps
- **Sources:** Clean-room staged inputs `inputs/{PROOF.md, LEMMAS.md, REPORT.md, cert_case1.json.gz, cert_naive_ab.json.gz, cert_case2.json.gz}` and Round 1 sealed audit invariants documented in the job spec (`PRIOR_ART.md`, `REFEREE2.md`).
- **Limitations:** Non-Case-I components (`cert_naive_ab.json.gz`, `cert_case2.json.gz`, Kempe-swap dichotomy) rely on the SHA-256 lock to the Round 1 Claude Opus 5.5 audit as specified; the threshold $n_0 = 550{,}000$ is sufficient rather than sharp, and unstaged producer-process logs cited in `inputs/REPORT.md` (`produce.log`, `PRIOR_ART.md`) lie outside the clean-room perimeter (none enter the theorem proof).
- **Next steps:** None required for $n \ge 550{,}000$; reducing $n_0$ further would require tighter Stirling/exempt-set constants or finer certificate margin below $-1/1000$.

VERDICT: HOLDS
