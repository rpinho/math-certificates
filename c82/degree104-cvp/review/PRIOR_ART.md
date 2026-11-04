# Prior art — clean-room scope

Started 2026-11-04. This is an independent referee/replay, not a search for a new construction. The job's explicit clean-room restrictions override the broader discovery checklist in RULES.md. Only the supplied proof/certificate, public literature, teorth/optimizationproblems, and public PR #280/#301 text will be consulted. No linked producer code will be opened or run. AI-lab repositories and community/code searches outside this allowlist are excluded.

Live table, PR text, and Doche's original theorem: retrieval pending. The claimed comparison is PR #280's 0.2524177045, to be checked from the live PR. Replaying that certificate is outside the allowed inputs; the comparison will be to its public stated value.

Novelty: no new construction is sought; an independent reproduction is not new. No predictive model or predictive score is involved, so the SBS baseline rule is not applicable.

## Live sources checked

- https://github.com/teorth/optimizationproblems/blob/main/constants/82a.md (saved as sources/82a.md): the definition is the essential minimum of the *logarithmic* height h(alpha)+h(1-alpha). Merged table's smallest upper bound is 0.2534449* (Pinho).
- https://github.com/teorth/optimizationproblems/pull/280 (body/comments via the specified gh, saved as sources/pr280.json): live open claim 0.2524177045*, vidigoat, updated 2026-11-04T17:11:45Z. Claimed independent enclosure in A. Canli's comment: [0.2524177044473123, 0.2524177044473124]. This is a quoted comparison, not locally reverified.
- https://github.com/teorth/optimizationproblems/pull/301 (sources/pr301.json): 0.253091834*, superseded numerically by #280.
- https://www.numdam.org/item/JTNB_2001__13_1_103_0/: Doche, *Zhang-Zagier heights of perturbed polynomials*, JTNB 13 (2001), 103–110. The input proof gives the title of Doche's other 2001 paper. Original theorem inspection underway.

No external code downloaded. Comparison baseline is the live PR's printed mathematical bound; SBS is inapplicable to a deterministic proof certificate.

The complete live open-PR title index was also downloaded from teorth/optimizationproblems (sources/open-prs.json). The C82 entries are #242, #280 and #301; no smaller printed bound appears in these allowed live sources. No exhaustive priority claim is made outside the allowlist. Doche's Bordeaux PDF was saved and formulas (5)–(9), pages 108–109, inspected as rendered images. Attempts to retrieve the older Math. Comp. PDF from AMS and CiteSeer were refused (HTTP 403 and 404); no reliance on uninspected lemmas from that paper is needed because the distinct-algebraic-number step will be supplied directly.

Recent-paper check: searched arXiv for Zhang–Zagier essential-minimum upper bounds in 2026 and inspected https://arxiv.org/abs/2601.18978 (v2, 2026-03-20), Burgos Gil–Menares–Qu–Sombra, *Closing the gap around the essential minimum of height functions with linear programming*. Its abstract concerns duality, generic sequences of algebraic integers and computability; it does not state a new numerical C82 bound. This is contextual literature, not an input to the verifier. No linked code was opened.

Final live re-check, 2026-11-04T23:36:49Z: downloaded 82a, both #280/#301 bodies/comments and the open-PR title index again using the specified gh client. The definition page and both PR snapshots are byte/content-equivalent to the first retrieval. The relevant open C82 PRs remain #242, #280, #301; #280 still prints 0.2524177045*. Final snapshots have `-final` in their names under sources/. The verified supplied candidate is below that printed value; no global priority claim beyond these permitted sources is made.
