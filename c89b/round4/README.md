# C89b < 0.001648970526 — round 4 (rigorous exact threshold comparison: scripts/check_cayley_matrix_r4.py)

Candidate and unrefereed. The exact upper certificate has density
15058298592194934908767847/9131939205947984819238469632 (rigorous exact count: scripts/check_cayley_exact_r4.cpp).
It defines a 256-part binary Cayley step graphon with probabilities
0, 2648/4041 and 1. Repeated parts are counted.

- PROOF.md: construction, counting argument, polynomial and prior credit.
- certificates/: selected full matrix, kernel, two-mask definition and optional simpler upper witness.
- scripts/: two separately written (same agent) exact counters, wrappers and controls.
- receipts/: exact totals, acceptance and controls; release_* files are fresh package replays.
- REPRODUCE.md: Python >= 3.10, C++17 and GMP instructions.
- review/README.md: AI review scope and corrections; no human referee.
- PROVENANCE.json, MANIFEST.json and SHA256SUMS: source identity and package integrity.

Written and checked by AI agents under Ricardo Pinho's direction.
No human referee; no priority or optimality claim. See PRIOR_ART.md,
including the Feinstein–Even-Zohar announcement.
