# Supkar and Yaddanapudi (arXiv:2611.32684v1), Section 5: a counterexample to the non-negativity of γ

Supkar and Yaddanapudi, *Schnyder woods and the chromatic polynomial* ([arXiv:2611.32684v1](https://arxiv.org/abs/2611.32684v1)), Section 5, write that γ(G) = ½(−1)^{n−1} χ′_G(2) seems to be non-negative for 3-connected non-bipartite graphs, and that they checked this by computer for |G| ≤ 9. It is not true in general.

## The counterexample

Take two copies of K_{3,3} that share one vertex x, with shores {x, a, b} | {u₁, u₂, u₃} and {x, c, d} | {v₁, v₂, v₃}, and add the edges ac and bd. The graph G has 11 vertices and 20 edges, is 3-connected and is not bipartite, and χ′_G(2) = −2, so **γ(G) = −1 < 0**.

The edge list is [certificates/witness.json](certificates/witness.json) and the hand proof is [PROOF.md](PROOF.md).

## Verification

- **Exact check:** [referee/referee_verify.py](referee/referee_verify.py) uses integer arithmetic only. It computes χ_G four separate ways (deletion-contraction, an independent-set falling-factorial count, Whitney's broken-circuit forests and the closed form), checks brute-force colouring counts (χ_G(3) = 150, χ_G(4) = 20,760), checks all 55 two-vertex deletions for connectivity, and runs positive, negative and mutation controls. Verdict in [referee/REFEREE.md](referee/REFEREE.md): HOLDS.
- **Lean:** [lean/](lean/) holds a standalone Lean 4 proof, `Gamma.supkar_yaddanapudi_conjecture_false`, with no Mathlib. Its axioms are listed in [lean/AXIOMS.txt](lean/AXIOMS.txt).
- **Prior art:** a priority audit on 2026-11-27 found no earlier public counterexample (arXiv, GitHub code search, the 1337isnot1337/solved-conjectures catalogue, TrureTuring, Conjecture Desk, AmirMakir/broken-conjectures).

**Lean status:** complete (standalone, zero Mathlib).

**AI disclosure:** the counterexample was found by GPT-6.2 Astra (Codex) and audited in clean-room isolation, with the producer code withheld, by Gemini 4 Carbon High. No human mathematician has reviewed this packet.
