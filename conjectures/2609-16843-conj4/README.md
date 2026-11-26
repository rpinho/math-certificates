# Disproof and Complete Resolution of van Berkel and Bosma (arXiv:2609.16843v2) Conjecture 4

This packet refutes Conjecture 4 (`\label{conj:except}`) of Daan van Berkel and Wieb Bosma, *On $t$-sumfree sequences* ([arXiv:2609.16843v2](https://arxiv.org/abs/2609.16843v2)), and resolves the ultimate periodicity and minimal parameters $(k, p, m)$ of the greedy strict $3$-sumfree sequence $S_{1, d-1, 2d-1}$ for every integer $d \ge 3$.

This is AI work. No human has checked it. **Lean status:** `verified` (standalone Lean 4, zero Mathlib, zero `sorry`, standard axioms `[propext, Classical.choice, Quot.sound]`; see [`lean/`](lean/)).

## Conjecture 4 (as stated in v2)

> For every $d \ge 3$ the $3$-sumfree sequence $S_{1, d-1, 2d-1}$ is ultimately periodic, and, with the exception of $d=3$ or $d=5$, the preperiod length is $d+3$ and the period length is $d$ modulo $8d-1$.

## Exact disproof and complete resolution

Conjecture 4 is false as stated at **$d = 4$** (where both the minimal period and the modulus fail) and for **every $d \ge 6$** (where the true minimal modulus is $8d - 3$, not $8d - 1$). Every sequence in the family is ultimately periodic with exact minimal parameters $(k, p, m)$:

| Parameter $d$ | Minimal $(k, p, m)$ | Finite preperiod | First periodic block (step $m$) | Conjecture 4 status |
|---|---|---|---|---|
| $d = 3$ | `(5, 1, 5)` | `1, 2, 5, 6, 7` | `11` (mod `5`) | Listed exception |
| $d = 4$ | `(7, 3, 27)` | `1, 3, 7, 8, 9, 10, 15` | `29, 35, 36` (mod `27`) | **Refuted:** period `3` (not `4`), modulus `27` (not `31`) |
| $d = 5$ | `(13, 10, 104)` | `1, 4, 9, 10, 11, 12, 13, 19, 37, 45, 46, 72, 79` | `80, 81, 114, 115, 116, 123, 149, 150, 158, 176` (mod `104`) | Listed exception |
| Every $d \ge 6$ | `(d + 3, d, 8d - 3)` | `1, d - 1, [2d - 1, 3d - 2], 4d - 1` | `[10d - 5, 11d - 6]` (mod `8d - 3`) | **Refuted:** modulus `8d - 3` (not `8d - 1`; at $d = 6$, `45` vs `47`) |

Full elementary proofs (small cases $d = 3, 4, 5, 6$ via the authors' finite-computation criterion and residue-class generating functions, plus the all-$d \ge 6$ exclusion, inclusion, and minimality theorem) are in [`PROOF.md`](PROOF.md).

## Verification and clean-room referee audit

- **Producer:** Gemini 4 Carbon High via Antigravity CLI (`producer/verify.py`, `producer/witnesses_v1.json`).
- **Clean-room Cross-Family Referee:** GPT-6.2 Astra via Codex (`referee/REFEREE.md`, `referee/referee_verify.py`, producer code withheld). Independently certified all `40` finite cases ($d$ from `3` to `40`, plus `50` and `100`), the symbolic exclusion/inclusion/minimality proof for all $d \ge 6$, and rejected all `1174` mutants and negative controls.
- **Referee fixes applied before publication:** The referee returned `VERDICT: HOLDS WITH CAVEATS`, confirming the disproof and theorem while catching one symbolic witness encoding slip (`blocks.U1` written as `[[1,0],[1,0]]` instead of `[[0,1],[0,1]]` in `producer/witnesses_v1.json`) and six small-case prose slips in the initial draft proof. All `7` fixes are applied in [`certificates/witnesses.json`](certificates/witnesses.json) and [`PROOF.md`](PROOF.md). Re-running `referee/referee_verify_repaired.py` (identical to `referee/referee_verify.py` except for the updated witness SHA-256 lock) exited `0` with `0` scientific witness disagreements (`referee/referee_verify_repaired.log`).


## Standalone Lean 4 formalization

The [`lean/`](lean/) directory contains a self-contained Lean 4 (`leanprover/lean4:v4.36.0`, zero Mathlib dependencies) formalization defining strict greedy 3-sumfree sequences from first principles and proving `d3_minimal` (`(5, 1, 5)`), `d4_minimal` (`(7, 3, 27)`), `d4_refutes_conj4`, `d5_minimal` (`(13, 10, 104)`), `all_d_ge_6_minimal` (`(d + 3, d, 8d - 3)` for every `d >= 6`), and `all_d_ge_6_refutes_conj4`. It builds cleanly with zero `sorry`, zero `axiom`, zero `native_decide`, and standard core axioms `[propext, Classical.choice, Quot.sound]` only:

```bash
cd lean && python3 -B verify_lean.py
```

## Reproduction

Requires Python 3.10+ (standard library only). From `conjectures/2609-16843-conj4/`:

```bash
# 1. Verify file integrity
shasum -a 256 -c SHA256SUMS

# 2. Run producer standalone exact verifier on repaired certificate
python3 -c 'import shutil, subprocess, tempfile; d=tempfile.mkdtemp(); shutil.copy("certificates/witnesses.json", d); shutil.copy("producer/verify.py", d); subprocess.run(["python3", "verify.py"], cwd=d, check=True)'
```
