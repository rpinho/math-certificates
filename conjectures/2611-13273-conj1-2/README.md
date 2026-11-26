# Crew et al. (arXiv:2611.13273v1), Dichromatic Shameful and Monotonicity Conjectures: Unconditional Proof

Unconditional proof settling both Conjecture 1 (`conj:shameful_conj`, the Dichromatic Shameful Conjecture) and Conjecture 2 (`conj:monotonicity_conj`, the Dichromatic Monotonicity Conjecture) of Lila Crew, Benjamin Keller, Katharina Kuehr, Shao Yuan Lin, Megan Ixchel Monroy Rodriguez, and Tabitha Williams, *Properties of the Dichromatic Polynomial* (`arXiv:2611.13273v1`), audited in clean-room isolation (`VERDICT: HOLDS`) with an exact-integer polynomial verifier (`referee/referee_verify.py`).

## Main Theorem

For every finite loopless digraph $D$ on $n \ge 2$ vertices and every real $x \ge n - 1$,
$$H_D(x) := x P_D^{\prime}(x) - n P_D(x) \ge 0.$$
Consequently:
1. **Dichromatic Monotonicity (`conj:monotonicity_conj`):** $F_D(x) = P_D(x) / x^n$ is nondecreasing on $[n - 1, \infty)$.
2. **Dichromatic Shameful Inequality (`conj:shameful_conj`):** $P_D(n) / n^n \ge P_D(n - 1) / (n - 1)^n$.
3. **Strictness and DAG characterization:** If $D$ contains a directed cycle, then $H_D(x) > 0$ for all $x > n - 1$ and the inequality is strict. If $D$ is acyclic, then $P_D(x) = x^n$ and $F_D(x) = 1$ identically. The threshold $x \ge n - 1$ is sharp, as $H_{\overset{\leftrightarrow}{K}_3}(1) = -1$ and $H_{\overset{\leftrightarrow}{K}_4}(2) = -4$.

## Proof Outline (Marked-Vertex Identity)

Fix a vertex $v \in V(D)$ and call a subset $S \subseteq V$ allowed when $D[S]$ is acyclic. Grouping proper $x$-colorings by the color class $S$ of $v$ yields $P_V(x) = x \sum_{S \ni v} P_{V \setminus S}(x - 1)$. Differentiating, multiplying by $(x - 1)$, and double-counting the remaining weight by deleting $v$ and grouping over allowed partitions $\pi$ of $V \setminus \{v\}$ gives the exact polynomial identity
$$(x - 1) H_V(x) = x^2 \sum_{S \ni v\;\mathrm{allowed}} H_{V \setminus S}(x - 1) + \sum_{\pi} (x)_{|\pi|} \sum_{B \in \mathcal{B}(\pi)} (x |B| - (n - 1)),$$
where $\mathcal{B}(\pi) = \{B \in \pi : B \cup \{v\}\text{ is not allowed}\}$. For $x > n - 1$, every inductive term satisfies $x - 1 > n - 2 \ge |V \setminus S| - 1$, every falling factorial $(x)_{|\pi|}$ is positive, and every forbidden block satisfies $x|B| - (n - 1) > 0$. Dividing by $x - 1 > 0$ and taking $x \to (n - 1)^+$ completes the induction. The argument uses only heredity of allowed sets and admissibility of singletons, generalizing Dong (2000) to all hereditary hypergraph colorings.

## Verification and Disclosure

- **Exact-integer audit:** `referee/referee_verify.py` (pure Python integer arithmetic, zero `math`, `float`, or `/` division) verifies Identities 1, 2, and 3 in $\mathbb{Z}[x]$ across all 4164 labeled loopless digraphs on $n = 2, 3, 4$ (reproducing exact OEIS A003024 DAG counts 3, 25, 543) plus 312 structured and sampled digraphs on $n = 5, 6$ (4478 digraphs, 18241 marked pairs total), along with 8 mutant checks across 4 deliberate mutations, in under 10 seconds.
- **Prior art:** Checked on arXiv (`v1`), GitHub, and X as of 2026-11-26 with no prior proofs or counterexamples found.
- **Lean status:** None yet (standalone Lean 4 formalization queued as follow-up upgrade).
- **AI disclosure:** Proof constructed by GPT-6.2 Astra (Codex) and audited in strict clean-room isolation (producer code withheld) by Gemini 4 Carbon High (Antigravity CLI), returning `VERDICT: HOLDS`. No human mathematician has reviewed this packet.

## Reproduction

```bash
python3 referee/referee_verify.py
```
