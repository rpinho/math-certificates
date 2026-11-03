# Verification levels

Each result here states a verification level. The level describes the evidence for the stated bound, not its novelty, priority or acceptance, and it is never human refereeing.

| Level | Evidence |
| --- | --- |
| L0 | AI review, prose proof, or checkers written by the same AI agent that produced the result. |
| L1 | An exact finite certificate, checked by a checker written by a different model or party, with a recorded run receipt and output hash. A new all-size step left in prose keeps the whole bound at L0 even when its finite certificate is L1. |
| L2 | A pinned Lean project that builds, proving our new step; inherited published results appear as named axioms with exact citations. |
| L3 | The full stated bound in Lean, using only Lean's standard axioms. |

"Finite component" gives the level of the exact certificate alone. "Same-agent" means our checker was written by the same AI agent as the search. Levels follow the research harness rule of 3 November 2026; a strict L1, L2 or L3 claim in a pull request is backed by a receipt packet next to its text.
