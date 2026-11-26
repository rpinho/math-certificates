# Erdős #1182: F(n) <= 5n - 1 for all n >= 550,000

I present a candidate computer-assisted proof that in [Erdős problem #1182](https://www.erdosproblems.com/1182),

$$F(n) \le 5n - 1 \qquad \text{for every integer } n \ge 550000$$

(including odd $n$).

This is AI work. No human has checked it. The proof and 160-bit Arb certificates were produced by GPT-6.2 Sol (Codex) and audited clean-room across two other model families with producer code withheld: Claude Opus 5.5 (Round 1, which accepted everything outside Case I and caught a reversed cutoff direction in the initial Case I occupancy lemma) and Gemini 4 Carbon High (Round 2, which independently verified the repaired Case I proof, certificate, finite-$n$ bound, and 10 corruption controls with `VERDICT: HOLDS`).

## Context and prior art

The official problem page records Stephan Brandt's published bound $F(n) \le 84n$ and an announced bound $11.75n$ without proof. In [Sovi11/erdos-1182](https://raw.githubusercontent.com/Sovi11/erdos-1182/6d4f78c/BOUNDS.md) (pinned commit `6d4f78c`), Kataria developed the random-regular configuration-model approach and obtained the unrefereed bound $F(n) \le 5.025n$. At regular degree $d = 10$ ($5n$ multiedges, giving at most $5n - 1$ simple edges after deleting one loop or parallel edge), the bare first-moment rate over balanced $C_5$ embeddings is strictly positive (`+0.0033635` in Region C), blocking a naive $d = 10$ proof.

## Method: Kempe-swap dichotomy at d = 10

Instead of raising the degree above $d = 10$, I work directly with the bare $10$-regular configuration model (where $10n$ is even for all integers $n$, including odd $n$) and restrict the first-moment count to $\Phi$-minimal balanced $C_5$-embeddings, where $\Phi = \sum_{i=0}^4 |V_i|^2$:

- **Regions A and B** are ruled out directly by the naive first-moment certificate [`certificates/cert_naive_ab.json.gz`](certificates/cert_naive_ab.json.gz) (`805` leaves, certified upper bound `-0.0011788362183`).
- **Region C** (where $\min(a_0, a_2) - a_3 \ge 3/20$ after normalizing $a_3 \ge a_4$): a $\Phi$-minimal embedding cannot admit a valid single-vertex or $2$-vertex Kempe swap decreasing $\Phi$. This forces a dichotomy:
  - **Case I (donor occupancy):** almost every vertex in $V_0$ has a neighbor in $V_3$. Bounded by an upper cutoff $Q_{03} \le q_*$ combined with the conditional occupancy rate below $q_*$ and a binary relative-entropy tail above $q_*$, certified in [`certificates/cert_case1.json.gz`](certificates/cert_case1.json.gz) (`1,525` leaves: `766` naive and `759` occupancy, certified upper bound `-0.001000001000007`).
  - **Case II (pair-avoidance):** certified in [`certificates/cert_case2.json.gz`](certificates/cert_case2.json.gz) (`1,978` leaves, certified upper bound `-0.001000001000009`).
- **Finite threshold:** at $n_0 = 550000$, the combined first-moment bound is below `4.261e-11`, and with the disconnection bound of `3/13` (tight bound $e/(16 - e) < 0.2047$), the total failure probability is below `0.231 < 1` and strictly decreasing for all $n \ge n_0$.

Full proof details are in [`producer/PROOF.md`](producer/PROOF.md) and [`producer/LEMMAS.md`](producer/LEMMAS.md).

## Certificates and verification summary

All `4,308` leaves across the three certificates are verified in 160-bit Arb (`python-flint`):

| Region / Case | Archive | Leaves | Certified upper bound | SHA-256 |
|---|---|---:|---:|---|
| Regions A and B | [`cert_naive_ab.json.gz`](certificates/cert_naive_ab.json.gz) | 805 | `-0.0011788362183` | `b4cbc312f5f1a042990c031df8b35542eb6f192639ea93edf024b61002ec5989` |
| Region C, Case I | [`cert_case1.json.gz`](certificates/cert_case1.json.gz) | 1,525 | `-0.001000001000007` | `09fba47458edf71cf255b63bb3842e4360b7d275748543c61c9b6fe494bf0611` |
| Region C, Case II | [`cert_case2.json.gz`](certificates/cert_case2.json.gz) | 1,978 | `-0.001000001000009` | `c68d3339047880b19de426b6bde3114630ce10ad853ecc409926f621d5c3bab8` |

Clean-room referee reports:
- Round 1 (Claude Opus 5.5): [`referee/round1-opus/REFEREE.md`](referee/round1-opus/REFEREE.md)
- Round 2 (Gemini 4 Carbon High, repaired Case I): [`referee/round2-gemini/REFEREE2.md`](referee/round2-gemini/REFEREE2.md)

## Reproduction

Requires Python 3.11+ with `python-flint` (Arb). From `erdos/1182/`:

```bash
# 1. Verify file integrity
shasum -a 256 -c SHA256SUMS

# 2. Run the standalone Round 2 clean-room referee verifier on Case I and finite-n bound
python3 referee/round2-gemini/arb_case1_referee.py --cert certificates/cert_case1.json.gz --inputs-dir certificates --also-finite

# 3. Run the producer verifier and finite-n script
(cd producer && cp ../certificates/*.json.gz . && python3 verify.py && python3 finite.py)
```
