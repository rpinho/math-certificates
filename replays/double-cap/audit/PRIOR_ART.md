# Prior art: clean-room audit of LeanShadow, the Lean 4 proof of the double-cap conjecture (idea b9a1ff75)

Captured 2026-11-22 (UTC 23:55).

## The problem
- Witsenhausen (1974) asked for the largest density alpha_n of a measurable A in S^{n-1} with no two orthogonal vectors. Kalai conjectured the double cap (two opposite open caps of angular radius pi/4) is optimal for every n >= 3; for n = 3 that density is 1 - 1/sqrt(2) = 0.29289...
- Upper bounds before the claimed proof: 0.2977 for n = 3 (Bekker et al., 2025); 0.2953 (arXiv:2605.28709, 27 May 2026, 33-point set via the geometric fractional chromatic number of Ambrus et al. 2024).
- Survey/background: arXiv:2609.34845 (completely positive hierarchies for distance-avoiding sets), MathWorld "Double-Cap Conjecture" (https://mathworld.wolfram.com/Double-CapConjecture.html), which says neither complete proof has been independently checked.

## The claim being audited
- A. Ibiapina, C. A. Gomes, A. Pio, S. Belo, E. Ferreira, "An orthogonality inequality in RP^{n-1} and the double-cap conjecture", arXiv:2610.27523v1 (19 Oct 2026): caps minimize orthogonal-neighbourhood measure in RP^{n-1}, n >= 3, hence the double-cap conjecture. The abstract says a separate Lean 4 proof of the main inequality and the double-cap result, by a different argument, was carried out almost entirely with AI-assisted tools.
- Lean: https://github.com/allenibiapina/LeanShadow, single commit 19deb3ed555cc8404958c1804f9b29898a918d10 (2026-09-12), 159 files, lean4:v4.33.0, 0 issues, 0 stars. ComparatorChallenges/Shadow.lean states twelve main results importing only Mathlib; LeanShadow/ComparatorSolution.lean proves them; workflow after the OpenAI NavierStokesAndEuler release (comparator + lean4export + nanoda 0.4.17). Their README says the reference was written for the package from MAIN_STATEMENT.md and "Comparator checks agreement with this reference, not whether the reference is the intended mathematical problem."

## Baseline (what exists)
- The authors' own comparator challenge and verification-tools.json (producer-written statement, producer-run checks). No third-party replay, review, issue, or post found.
- Method precedent: Lean and Mathlib communities' four criteria for the RH verification (statement correct, library compiles, code proves that statement via an isolated statement file + comparator, kernel recheck by several kernels), https://leanprover-community.github.io/blog/posts/riemann-hypothesis/ ; our own c30/lean-m1 audit (math-certificates 2ce3345: separate-model Spec.lean, Lean bridges, mutants, nanoda + leanchecker).

## This round's contribution
Criterion (1) by a separate model: write Spec.lean of the double-cap conjecture from the literature (not from their files), prove Spec <-> their Shadow.lean main theorem in Lean, refute one-change mutants; plus (2)-(4) replay at the pinned commit.

## Search
- arXiv API: "double cap" OR Witsenhausen, newest first (hits above; nothing after 2610.27523 on this problem).
- Web: "double cap conjecture" proof Lean LeanShadow Ibiapina (paper, MathWorld; no replay).
- GitHub: repository and issues of allenibiapina/LeanShadow (no issues, no forks checked as replays).
- X live search (captured): "double cap" conjecture; "double-cap" OR LeanShadow OR Witsenhausen sphere: nothing on the proof.
Not an exhaustive claim.

```rh-prior-art
{
 "schema": 1,
 "baseline": "LeanShadow@19deb3e ComparatorChallenges/Shadow.lean (producer-written statement) and its comparator workflow",
 "sources": {
  "github": {
   "status": "none",
   "query": "LeanShadow double cap conjecture Lean",
   "searched_at": "2026-11-22T23:51:50+00:00",
   "hits": [],
   "note": "GitHub repository search, top 0 by best match."
  },
  "x": {
   "status": "none",
   "query": "\"double cap\" conjecture (X live search); \"double-cap\" OR LeanShadow OR Witsenhausen sphere (X live search)",
   "searched_at": "2026-11-22T23:50:19Z",
   "hits": [],
   "note": "Captured X search (browser, 2026-11-22T23:50:19Z) for key b9a1ff750d524eb3b71346ec013eaeed; 0 posts. Key-level capture; no new X search was performed.",
   "capture_path": "(local capture file, not published)",
   "capture_sha256": "693de6b494bc13b3ab5d85e6a2ca9de7554b49a6f2ec914a46f9669409d703aa"
  },
  "papers": {
   "status": "none",
   "query": "double cap conjecture Witsenhausen orthogonal",
   "searched_at": "2026-11-22T23:51:50+00:00",
   "hits": [],
   "note": "Europe PMC relevance search, top 0 (after OpenAlex: HTTP 429, retry-after 492s; Semantic Scholar: HTTP 429); the worker reads them before modelling.",
   "source": "Europe PMC"
  },
  "leaderboards": {
   "status": "none",
   "query": "LeanShadow double cap conjecture Lean",
   "searched_at": "2026-11-22T23:51:50+00:00",
   "hits": [],
   "note": "Hugging Face spaces/datasets search and GitHub \"<q> benchmark\" repos."
  }
 }
}
```

## Local reproduction, 2026-11-23 UTC

The pinned proof built offline, and the challenge and proved adapters each yield the frozen statement. All twelve public axiom queries returned only propext, Classical.choice and Quot.sound. The pinned comparator's comparison and axiom functions passed on local exports, and Lean replayed the proof closure from an empty environment. On the Mac, the authors' full configured command stopped at the missing landrun executable before reaching nanoda. No fresh mathematical result or public novelty claim. The detailed verification status and controls are in [REPORT.md](REPORT.md).

The ordinary Lake default target subsequently passed (8,847 jobs). The bundled leanchecker accepted all 140 modules with local declarations checked in their imported environments. Re-exporting the final Lake outputs reproduced all three streams, including the corruption control, byte for byte.
