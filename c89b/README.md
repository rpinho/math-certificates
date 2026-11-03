# C89b < 0.001648970526

Candidate and unrefereed. The selected round-4 certificate has exact density
15058298592194934908767847/9131939205947984819238469632.
It is a 256-part binary Cayley step graphon with probabilities 0, 2648/4041
and 1. [Proof, certificates, counters and reproduction](round4/).

Two separately written (same agent) exact counters agree on the fraction
and separately on red and blue totals. Both were replayed for the package,
with 36 literal comparisons, ten malformed-input rejections and two
false-threshold rejections. Requires Python >= 3.10, C++17 and GMP.

Written and checked by AI agents under Ricardo Pinho's direction.
[Two AI review statuses](round4/review/README.md): Claude Opus 5.5 via
Claude Science, and GPT-6 Astra. There is no human referee. No priority
or optimality claim is made.

Builds on Jeetu SK's [#277](https://github.com/teorth/optimizationproblems/pull/277),
Thomason, and Parczyk–Pokutta–Spiegel–Szabó. Kiem–Pokutta–Spiegel's
numerical lower-bound discussion is credited separately in
[PRIOR_ART.md](round4/PRIOR_ART.md). No round-4 lower-bound material is released.

Feinstein's [Technion announcement, 21 January 2026](https://math.technion.ac.il/events/noam-feinstein/)
gives c5 < 0.001652; the [RSA 2025 abstract](https://dmg.tuwien.ac.at/rsa2025/)
credits joint work with Chaim Even-Zohar. This is an announcement with no
public certificate we could check. Its displayed threshold is stronger than
our round-3 0.001653032 and weaker than this round.

Earlier packages remain historical: [round 3](round3/) and the original
symmetry-breaking construction in this directory. The current proposed
Tao-table update is [#307](https://github.com/teorth/optimizationproblems/pull/307).

## Earlier rounds

- This folder's top level holds the 1 November candidate C89b <= 2405659597/1427496763392 < 0.00168523 (Jeetu SK's step graphon with its symmetry broken): `PROOF.md`, `candidate.json.gz`, `independent_verify.py`, `independent_count.cpp` and their logs, and `review/`.
- [round3/](round3/): C89b < 0.001653032, a four-layer folded-Hamming step graphon.
