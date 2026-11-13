# Prior art for this referee job
Scope is restricted to the three supplied input files, Doche's public paper, the public teorth/optimizationproblems constant 82a, and PR bodies/comments #280, #301, #330. The task explicitly excludes producer repositories and code, so the broader repository searches and reproductions in the general RULES.md do not apply. This is an independent replay, not a search for a new construction.

Live sources are being read before checker implementation. Numerical references in the task are #280 v5: 0.2519889614* and #330: 0.2519744488*. These are pending live confirmation.

Confirmed live on 2026-11-12 (UTC retrieval date recorded in final report):
- https://github.com/teorth/optimizationproblems/blob/main/constants/82a.md : logarithmic h(alpha)+h(1-alpha), essential minimum defined using finite closed sublevel sets; merged asterisked best 0.2534449*.
- https://github.com/teorth/optimizationproblems/pull/280 : v5 0.2519889614*, updated 2026-11-10; last independent replay comment reports B in [0.2519889613870203,0.2519889613870204].
- https://github.com/teorth/optimizationproblems/pull/330 : live candidate 0.2519744488*, updated 2026-11-12, from Doche construction and joint degree-104 search. This is the smallest printed bound among the permitted sources checked.
- https://github.com/teorth/optimizationproblems/pull/301 : 0.253091834*, superseded numerically by the above.
- C. Doche, Zhang-Zagier heights of perturbed polynomials, JTNB 13 (2001), 103–110, https://www.numdam.org/item/JTNB_2001__13_1_103_0/ . Read the averaging lemma and equations (5)–(9), not search code.
No linked producer packets/code were followed. Older certificates cannot be replayed within this job's only-input rule; comparison is against their live printed bounds. This referee supplies no new construction or globally exhaustive priority claim.

Final live check on 2026-11-13 UTC: #280 remains open at 0.2519889614*, updatedAt 2026-11-10T03:24:50Z; #330 remains open at 0.2519744488*, updatedAt 2026-11-12T21:50:17Z. The current constants/82a.md blob SHA is 3c01b653bc3c50908d4a409003c510b30adbdeb6. The initial read and this final check agree. No repository code search was performed because the job explicitly prohibits those producer inputs.
