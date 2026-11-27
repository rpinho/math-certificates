# Reproduction of the sharp sub-quorum bound in Conjecture 9.2 (arXiv:2609.25128v4)

> Not first. Derek Blair proved the same universal inequality for the two optimum partial sub-quorum colorings and sharpness for every $n\ge 2$ using palette incidence. [PR #54, opened on 2026-11-25 at 23:35:23 UTC](https://github.com/derekblair/math-proofs/pull/54).

I present an unconditional elementary proof of Conjecture 9.2 (`\label{conj:ng-upper}`) of Haobo Ma, Rafik Sahbi, and Wenlin Zhang, *Sub-quorum colorings of graphs* ([arXiv:2609.25128v4](https://arxiv.org/abs/2609.25128v4)):

$$\psi_{sq}(G) + \psi_{sq}(\overline{G}) \le n + 2 \qquad \text{for every finite simple graph } G \text{ of order } n \ge 2.$$

This is AI work. No human has checked it. **Lean status:** `verified` (standalone Lean 4, zero Mathlib, zero `sorry`, standard axioms `[propext, Classical.choice, Quot.sound]`; see [`lean/`](lean/)).

## Proof summary

The complete self-contained proof is in [`PROOF.md`](PROOF.md). Let $f_1, f_2$ be optimal sub-quorum colorings of $G$ and $\overline{G}$ with supports $S_1, S_2$, and assign each vertex $v$ the reciprocal color-class weight $w_{f}(v) = 1/|C_{f(v)}|$ (or $0$ if uncolored), so that $\sum_v w_{f_1}(v) = \psi_{sq}(G)$ and $\sum_v w_{f_2}(v) = \psi_{sq}(\overline{G})$.

1. **Exterior $V \setminus I$ (where $I = S_1 \cap S_2$, $m = |I|$):** every $v \notin I$ is colored in at most one of $f_1, f_2$, so $w_{f_1}(v) + w_{f_2}(v) \le 1$, contributing at most $n - m$.
2. **Intersection $I$ (Lemma 1):** by the paper's sub-quorum majority definition (weak majority among colored vertices in the closed neighborhood, including $v$ itself), every $v \in I$ satisfies $|C_{f_1(v)}| \ge 1 + \lfloor d_I(v)/2 \rfloor$ in $H = G[I]$ and $|C_{f_2(v)}| \ge 1 + \lfloor (m - 1 - d_I(v))/2 \rfloor$ in $\overline{H}$.
3. **Handshaking degree-weight bound (Lemma 3):** for every simple graph $H$ on $m$ vertices,
   $$\Sigma(H) := \sum_{v \in V(H)} \left(\frac{1}{1 + \lfloor d_H(v)/2 \rfloor} + \frac{1}{1 + \lfloor (m - 1 - d_H(v))/2 \rfloor}\right) \le m + 5/2.$$
   This bound is exact: on the double star $S_{2,2}$ (order `6`, $\psi_{sq}(S_{2,2}) = 5$, $\psi_{sq}(\overline{S_{2,2}}) = 3$, sum `8`), $H = G[I] \cong P_3$ (order `3`) attains $\Sigma(P_3) = 11/2 = 3 + 5/2$, with exterior weight `5/2`.
4. **Integrality (Theorem 1):** summing both parts gives the integer inequality $\psi_{sq}(G) + \psi_{sq}(\overline{G}) \le n + 5/2$, hence $\psi_{sq}(G) + \psi_{sq}(\overline{G}) \le n + 2$. Equality is attained by $K_n$ and $\overline{K_n}$ (`2` + $n$) for every $n \ge 2$.

## Clean-room cross-family verification

- **Producer:** Gemini 4 Carbon High via Antigravity CLI (`producer/REPORT.md`, `producer/verify_proof.py`).
- **Clean-room Cross-Family Referee:** GPT-6.2 Astra via Codex (`referee/REFEREE.md`, `referee/referee_verify.py`, `referee/verification.txt`, producer code withheld). Upheld Theorem 1 and Lemmas 1-3 for every finite simple graph of order $n \ge 2$, independently checking Definition 2.2 verbatim, all `33868` labeled graphs through order `6` (`249299` optimal partitions, `13047409` Lemma 1 subset-vertex checks), all `268435456` labeled graphs of order `8` for Lemma 3, all `16348842` graphical degree sequences of orders `8` through `15`, all even degree-sum layers up to order `30`, and all `288265` unlabeled graphs of orders `2` through `9`.
- **Referee clarifications applied:** The referee returned `VERDICT: HOLDS WITH CAVEATS` for two non-mathematical-core clarifications: (a) a wording slip in Remark 3 (`PROOF.md` line 125 now accurately states that reciprocal weights retain a necessary class-size bound rather than preserving the full quorum constraint, since `1122` and `1212` on $P_4$ share weights); and (b) clarifying the census counts of strict dissociation gaps $\psi_{sq} > \beta_2$ for orders `6` through `9`: one-sided counts (in $G$) are `1`, `13`, `133`, `1236`, while either-side counts (in $G$ or $\overline{G}$) are `2`, `26`, `264`, `2450`.


## Standalone Lean 4 formalization

The [`lean/`](lean/) directory contains a self-contained Lean 4 (`leanprover/lean4:v4.36.0`, zero Mathlib dependencies) formalization of Definition 2.2, Lemma 1 (`class_size_lower_bound`), Lemma 3 (`handshaking_weight_bound`), Theorem 1 (`theorem_1`), Conjecture 9.2 (`conjecture_9_2`), sharpness on $K_n$ (`sharpness_Kn`) and $S_{2,2}$ (`sharpness_S22`), tightness on $P_3$ (`handshaking_weight_bound_sharp_P3`), and two kernel-checked negative controls (`not_upper_bound_n_plus_one`, `no_three_color_K3`). It compiles standalone in under a second with zero `sorry`, zero `axiom`, zero `native_decide`, and standard core axioms `[propext, Classical.choice, Quot.sound]` only:

```bash
cd lean && python3 verify_lean.py
```

## Reproduction

Requires Python 3.10+ (standard library only, exact `int` and `fractions.Fraction`). From `conjectures/2609-25128-conj92/`:

```bash
# 1. Verify file integrity
shasum -a 256 -c SHA256SUMS

# 2. Run producer exact verifier (seconds)
python3 producer/verify_proof.py

# 3. Run full clean-room referee verifier (~15 min on Apple M5 Pro, checks 268M order-8 graphs + 16.3M degree lists)
nice -n 10 python3 -B -u referee/referee_verify.py
```
