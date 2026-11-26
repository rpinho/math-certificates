# Disproof of Banerjee-Smoot Conjecture 6.1 (arXiv:2611.09681v1)

## Result

Both parts of Conjecture 6.1 (`\label{conj:families}`) in Koustav Banerjee and Nicolas Allen Smoot, *On a problem of Gordon and Hughes: The 11-adic properties of meromorphic modular functions on X_0(22)* (`arXiv:2611.09681v1`, Section 6), are **false** as stated for general integers `a`.

For `a in Z`, define the two generating functions:

- `P^{[1]}_a(q) = prod_{m>=1} (1 + q^m)^a / (1 - q^m) = sum_{n>=0} p^{[1]}_a(n) q^n`
- `P^{[2]}_a(q) = prod_{m>=1} (1 + q^m)^a / (1 - q^m)^5 = sum_{n>=0} p^{[2]}_a(n) q^n`

Taking `alpha = 3` (`11^3 = 1331`, claimed modulus `11^ceil(3/2) = 121`), `n = 0`, and `delta = 54` (`24 * 54 = 1296 == -35 (mod 1331)`):

| Part | `a` | `b` | `a mod 11` | `delta` | Exact coefficient `[q^54]` | Residue mod `121` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| (1) | `36` | `1` | `3` | `54` | `62043410886974649205238011198` | `33` |
| (2) | `40` | `5` | `7` | `54` | `66134580699742235651549220246110` | `55` |

Because `36 == 3 (mod 11)` satisfies Part (1) and `40 == 7 (mod 11)` satisfies Part (2) (`a != 1, 3, 5 mod 11`), both nonzero residues modulo `121` refute Conjecture 6.1 as stated.

## Minimality and Controls

Across all `151` integers `a in [-50, 100]`, all `alpha in {1, 2, 3}`, and all `n in {0, 1, 2, 3, 4, 5}` (`5436` progression checks total):

- Zero counterexamples occur at `alpha = 1` or `alpha = 2`.
- At `alpha = 3`, `a = 36` (Part 1) and `a = 40` (Part 2) are strictly minimal in both positive `a` and `|a|`.
- Theorem 1.2 (`a = 2, b = 5`) passes all `38` tested progression indices (`alpha = 1, 2, 3`), ordinary partitions (`a = 0, b = 1`) and overpartitions (`a = 1, b = 1`) match OEIS checkpoints and Ramanujan congruences, and all `6` mutated negative controls fail as expected.

## Verification

- **Producer:** GPT-6.1 Sol via Codex (initial discovery and exact finite truncation check).
- **Clean-room cross-family referee:** Gemini 4 Carbon High via Antigravity CLI (producer code withheld), returning `VERDICT: HOLDS` via two independent exact integer algorithms (direct truncated product expansion and Euler logarithmic-derivative divisor recurrence).
- **Lean status:** none (standalone Lean 4 formalization pending as an upgrade; no human referee review).
- **Prior-art check (2026-11-26):** Live arXiv check (`v1` only), GitHub repositories and issues (`trureturing`, `solved-conjectures`, global search), OpenAlex, and X search (`grok-x-search`) found zero prior counterexamples or corrections.

Reproduce with zero external dependencies (Python 3 standard library):

```sh
python3 referee/referee_verify.py
```

## Files

- `certificates/witness.json` - exact machine-readable counterexample parameters and coefficients
- `referee/REFEREE.md` - complete clean-room cross-family referee report (`VERDICT: HOLDS`)
- `referee/referee_verify.py` - standalone zero-dependency exact integer verifier (dual algorithms, positive and mutation controls, full `[-50, 100]` minimality scan)
- `referee/verification_results.json` - exact output log of `referee/referee_verify.py`
- `CLAIMS.json`, `REPLAY.json`, `CREDITS.md` - verification metadata and credits
