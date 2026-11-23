# Cross-family lemma check of PROOFS.md (Claude Opus 5.5, in the math session, 2026-11-23)

Producer: GPT-6.2 Sol (math_e982replay_1123). Checked: every clause family in PROOFS.md, by reading the argument and re-deriving it; no code run. Verdict per family:

- Domain/deletion: HOLDS (strict convexity <=> convex position with no three collinear; subsets stay in strict convex position; odd n from n - 1 by deleting a vertex).
- ASYM/TRANS: HOLDS (total preorder on edge lengths, shared by both endpoints).
- FIRST/BOUND: HOLDS (exactly one representative per class per row; BOUND forbids K + 1 representatives, i.e. at most K distinct incident distances).
- BISECTOR: HOLDS. For cyclic a, b, c, d the perpendicular bisector of ad meets the quadrilateral boundary at one interior point of ad and one point of the chain a-b-c-d (it cannot contain an edge, since it separates a and d); along the chain the sign of |xa| - |xd| changes once, so bd <= ab forces cd < ac.
- CROSS: HOLDS (diagonals cross at an interior point; strict triangle inequalities give ac + bd > ab + cd and > ad + bc).
- CAP: HOLDS. With b = (-1,0), d = (1,0), a = (0,-h), c = (u,v), h, v > 0 (a, c on opposite sides of bd), ac <= ab gives u^2 + v^2 + 2hv <= 1, so c lies strictly inside the circle with diameter bd, and bc, cd < bd.
- SYM: HOLDS (rotate a minimum boundary edge to 01; FIRST lift recomputed; BOUND invariant).
- FAN: HOLDS. For v and a, b, c, d in boundary order the rays are ordered inside the angle at v and angle avb + bvc + cvd = avd < pi. If in every sector the opposite side were >= both radii, each angle at v would be the largest angle of its (nondegenerate) triangle, hence >= pi/3, and the sum would be >= pi. The clause (OR over the three sectors of xy < vx or xy < vy) is exactly the negation.

FAN and CAP full premises were rarely exercised by the generators (FAN: 1 G3 sample plus 818 in a targeted panel; CAP: 909 G3 samples), so the n = 10 and n = 12 verdicts rest on these written proofs; both proofs are short and, as above, correct.

Overall: n = 8..13 HOLDS (UNSAT at K = floor(n/2) - 1 for n = 8, 10, 12, checked by cake_lpr and drat-trim; odd n by deletion). AI work; no human has checked it.
CONTROLS: No. Positive controls at K = floor(n/2) are SAT for n = 5..13 (regular polygons); every one of the 11 false variants was killed by a generator before solving; corrupted proofs and an altered core clause were rejected by cake_lpr (REPORT.md tables).
CONTRADICTING: No. The original n = 10 SAT model is kept and exactly refuted in SURVIVORS.md (it led to FAN); the n = 12 no-ASYM SAT witness and the 90-second cap are reported.
LABELS: No. The two encoders' CNF hashes were compared, not trusted; the family proofs were re-derived here rather than accepted from the generator counts, since FAN/CAP premises were barely sampled.
