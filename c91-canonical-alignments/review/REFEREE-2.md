I found no false or unjustified step in the proof as written. The one gap is in the specification: F_4 has to be defined over sliding windows. The number 0.256801 itself is not backed by anything I was given, because no certificate and no verifier output came with the proof. I claim no bound.

**Scoreboard, checked 2026-11-01.**
- teorth/optimizationproblems main has no C91 page; the constants stop at 90a.
- Open PR #273 (leandrejack-afk, head 9cb4226, last updated 2026-10-26) proposes the page with lower bound 0.216276* from J2026 (self-archived, asterisked) and upper bound 0.315514 from Rosenfeld 2024. [LIT]
- An arXiv search turned up no newer lower bound.
- Monte Carlo estimate on that page (from Bilardi–Schimd 2026): 0.27496, with 0.999-confidence interval [0.26108, 0.28884].

**Your four priorities.**

1. **Tilts on spin correlations.** PASS. The proof never needs the extra weight to be exp(o(n)). The order of choices is: the certificate fixes z, then ε is chosen so that ε·Σ|log z_j| < 2 log x + a log t, then n → ∞. Lag products and sliding four-spin products are pairwise uncorrelated, so Var F_j = n − j exactly and P(T_n) → 1 for every fixed ε.
   - This only works for sliding windows. With disjoint four-symbol blocks the increment depends on position mod 4, which the 4-bit history does not store.
2. **Tilted statistics and path sums.** PASS.
   - Each increment is spin(new symbol) × spin(the symbol j back in the same string), a function of the stored history only. Summed over a path it gives H_j exactly.
   - A column word determines (X, Y), so distinct pairs give distinct paths. Overcounting from accepted non-canonical paths only loosens an upper bound.
   - [MEASURED] exact n = 7 check: left side 0.001953 ≤ right side 0.5949.
3. **Unbounded competitor tracker; every canonical alignment accepted.** PASS. I checked every update, the tie-break ("at least one Y symbol consumed, so the first diagonal exists"), merge-by-min (all competitors with the same direction and lag hold the same buffer, the last r symbols) and dropping at the caps. [MEASURED]:
   - **Exhaustive:** 0 of 261,121 canonical alignments rejected (all length pairs 0..8), at W=4, W=1, W=2/B=3, and unmerged.
   - **Long random pairs:** 0 of 400 rejected at n≈200 with W=50 and no cap.
   - **Window patterns:** L=6 plus W=2 plus K=2 rejects 0 of 65,025.
   - **Second implementation:** written directly from the definition, with no merging. It agrees with the incremental merged tracker on 30,000 random words at each of W=1, 2, 3, 6 (0 differences).
     - My first run of this comparison reported 24,138 differences. That was a bug in my test harness (`not tuple`), not in the tracker; the corrected run is the one above.
   - **Mutations:** two deliberately unsound changes each wrongly reject 7,408 of 16,129 canonical alignments, so the tests can catch errors.
   - **Caveat:** both implementations are mine, so this is a second implementation, not independent review.
4. **Tail bound to expectation.** PASS. P(ed ≤ an) → 0 gives E[ed] ≥ an(1 − o(1)), and Fekete's lemma gives the limit.

The run rules 1–5, the segment-replacement lemma, the pattern automaton and the integer coefficients (checked exactly) also PASS.

**How far the method goes.** These are floating-point estimates, not bounds, with about 1e-5 optimiser noise. L is the forbidden-pattern window, W the tracker width, K the number of tilt statistics.

| (L, W, B, K) | states | a (estimate) |
|---|---|---|
| five rules only | 37 | 0.216276 (reproduces J2026) |
| + tilt K=2 | 145 | 0.217021 |
| + tracker W=2 | 2,421 | 0.235661 |
| exact window L=6 / 7 / 8 | 3,935 / 15,317 / 59,597 | 0.239028 / 0.242760 / 0.245830 |
| L=7, W=2, K=2 | 69,389 | 0.248268 |

- **Patterns are the lever.** Lag 3 and the four-spin term add under 1e-5. Each unit of L adds about +0.002 at W=2/K=2, so 0.256801 would need roughly L≈11: plausible, but I saw nothing showing it.
- **Ceiling.** With the exact canonical language the method reaches every a < C91; this is a sketch, written out in the report, not a written proof. Nothing shows that finite automata actually converge to it.
- **Best next structural idea.** A band-DP competitor: track all alternative paths within lag ±W from any earlier point on the path, not just the single staircase shape.

VERDICT
- No false step in the reduction.
- First gap: F_4 must be defined over sliding windows.
- 0.256801 is unsupported until a certificate is replayed. The same-agent verifier is a separate implementation, not independent review.

PROBABILITIES
- 0.90 that the reduction has no fatal error. Basis: lemma-by-lemma review plus the exhaustive and cross-implementation tests.
- 0.5 that a certificate exists and passes an exact replay. Basis: weak; my float estimates reach 0.248268 at 69,389 states.
- 0.97 that C91 ≥ 0.256801 is true. Basis: the Monte Carlo interval's lower end is 0.26108.
- 0.25 that this family (L ≤ 12, W ≤ 4, K ≤ 4) exceeds 0.26 at ≤ 10⁷ states. Basis: extrapolating the window gains gives about 0.260.

IDEAS
1. Band-DP competitor. Test: exhaustive soundness to 8×8 plus a definition-level cross-check. Bar: at least +0.003 over the staircase tracker at matched state count.
2. Get the certificate and replay it with our own reconstruction. Test: the state count matches the vector length, AV < V holds exactly, the Arb exponent check passes, and at least 7 corrupted certificates are rejected. Bar: all pass. Even then the asterisk needs a second party.
3. Minimise the window automaton before taking the product. Bar: at least 4× fewer states, so L=10 fits under 10⁶ states; run on Codex, not the Mini.
4. A full k-block tilt. Bar: at least +0.001 at (L, W, B) = (5, 2, 3); otherwise drop the tilt.

OUT_OF_BOUNDS
- Re-rounding x and t to gain digits.
- L ≥ 9 product automata on the Mini.
- Any PR #273 comment or "beats 0.216276" wording.
- Formalisation.

Delegation is off for this session, so the reviewer pass was my definition-level second implementation plus a single-shot text critique. The critique's ceiling and extrapolation objections were accepted and fixed in the report; its overcounting objection was rejected.

Files are in `c91_referee/`:
- [CS-2026-11-01-c91-typical-strip-referee.md]((not included)) — full lemma-by-lemma report, reviewer pass, and the VERDICT block
- [c91_referee_tests.py]((not included)) — the tests and estimates, standalone and rerunnable
- [tests_output.txt]((not included)) — output of that script
