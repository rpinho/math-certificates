# Credits

This result builds directly on earlier work on Erdős problem #1182:

- **Stephan Brandt** (2002): proved the published linear upper bound $F(n) \le 84n$ (and announced $11.75n$ without a proof) via balanced $C_5$ embeddings and random regular graphs.
- **Kataria** (`Sovi11/erdos-1182`, pinned commit `6d4f78c`): developed the $d=10$ random-regular configuration-model framework and unrefereed upper bound $F(n) \le 5.025n$ (after $5.03n$), including the naive first-moment analysis whose positive $+0.0033635$ barrier at $d=10$ motivated the Kempe-swap dichotomy used here.
- **Erdős Problems database** ([erdosproblems.com/1182](https://www.erdosproblems.com/1182)): problem statement and historical summary.

## Verification provenance

This is AI work. No human has checked it.

- **Producer:** GPT-6.2 Sol via Codex (proof, Kempe-swap Case I/II certificate generation, and surgical Case I upper-cutoff repair).
- **Clean-room Referee Round 1:** Claude Opus 5.5 via Claude Code (producer code withheld). Accepted the reduction, disconnection bound, odd-$n$ argument, Kempe-swap dichotomy (`83,966` swaps), `cert_naive_ab.json.gz`, `cert_case2.json.gz`, and finite-$n$ bound; caught a reversed cutoff direction in the initial Case I occupancy lemma.
- **Clean-room Referee Round 2:** Gemini 4 Carbon High via Antigravity CLI (producer code withheld). Independently re-derived the repaired Case I upper-cutoff and binary relative-entropy tail bounds, verified byte-identity of the two inherited archives, replayed all `1,525` leaves of `cert_case1.json.gz` in 160-bit Arb, verified the finite-$n$ bound at $n_0 = 550{,}000$, and rejected `10/10` certificate mutations (`VERDICT: HOLDS`).
