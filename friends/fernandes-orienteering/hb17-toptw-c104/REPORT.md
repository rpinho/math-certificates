# Independent referee report: HB17

The exact optimum claim holds for the official short Solomon c104 TOPTW with at most four routes. This is a certificate for one public deterministic instance, not a statistical generalization result. No claimant search or verifier source was read or imported. Only its raw data, primal routes, penalties, certificate states and descriptive documents were used. All scientific computation ran on mscr under /workspace/ref_hugo_HB17, nice 10.

## Primary source and model

The freshly downloaded [official archive](https://www.mech.kuleuven.be/en/mim/op/instances/righiniTOPTW2) contains a c104.txt identical to the claimed input: SHA256 931c01e136e690c05aeb9a62f7c4fcc095fa693e22ef67695abb19b3a548cc53. The [official format](https://www.mech.kuleuven.be/en/mim/op/instances/TOPTWformat) specifies service-start windows, a common start/end depot, variable fleet size, and Euclidean distances rounded down to one decimal for Solomon. Its capacity/header fields are irrelevant. I independently used exactly these definitions.

Ševeček's retained actual thesis PDF, Table C.6, printed68/PDF76, explicitly says four vehicles and reports c104=1260 for the +F2 variant. The title page and [university thesis record](https://is.muni.cz/th/uuuxx/) identify Jan Ševeček, Spring2026; the thesis is about pickup/delivery but this table is explicitly the classical TOPTW benchmark. A fresh direct thesis download returns a 947-byte HTML challenge, so its retained PDF is identified explicitly rather than misrepresented as a successful fresh retrieval. The public record independently authenticates title, author and year.

The freshly retrieved [Peng et al. accepted manuscript](https://lirias.kuleuven.be/retrieve/ec847f07-8b23-4cf1-9c91-b459df258a7a), Table6 printed/PDF29, reports four-vehicle c104=1260 in LMRoman10-Regular at7200s. The same row's proven two-vehicle760 uses LMRoman10-Bold. Its definition of bold versus nonbold is §5.5 printed27, not §5.4 as CLAIM.md says. This is a citation typo, not a changed result. Screenshots, extracted text/font records and PDFs are retained under evidence/. The older Amarouche supplement also contains1260; exhaustive priority was not assessed.

## Independent reconstruction

`primary_and_primal.py` uses Fraction arithmetic and integer square roots to reconstruct travel times from the raw decimal coordinates. Its four-route replay obtains scores330+310+300+320=1260 and47 distinct customers. Depot returns are1234.1,1207.2,1235.6,1235.8, all at most1236. Its independently written simple profit/insertion-time greedy control obtains1180. Replacing downward with upward tenth rounding makes the supplied witness infeasible (node98 service start1115.3 exceeds1115): the official rounding is material.

`independent_upper.cpp` is a new implementation of a proof closure checker, including a separately derived completion bound. It reconstructs all travel times with integer square roots, and APSP lower bounds using Floyd-Warshall because rounded Euclidean travel need not satisfy triangle inequality. It reads only certificate data; saved objective values or claimed verifier status have no authority.

For each saved state it checks direct return and every legal next-customer transition. The transition must be dominated by a saved state with no later departure, no smaller accumulated weighted reward, and a subset of its memory, or closed by a safe bound on a distinct-customer suffix. Local certificate masks are independently translated through the declared neighborhoods. All neighborhoods must contain their current vertex; invalid mask bits are rejected.

My suffix bound: let C be all nonremembered customers that could fit individually according to shortest-travel lower bounds and their windows. For each j in C, assign cost 2*service(j)+minimum incoming edge from C or current vertex+minimum outgoing edge to C or depot. Subtract the smallest possible first and last edges from twice the remaining depot time. Every actual distinct suffix has total assigned cost at most this remaining budget: internal travel is counted twice and the two boundaries once. Fractional knapsack, followed when necessary by exact 0/1 knapsack, upper-bounds its reward. Candidate filtering uses shortest travel, never a triangle-inequality assumption. All arithmetic deciding acceptance is integer.

The crucial induction does not assert that a relaxed prefix is an elementary route. Follow any fixed elementary route's actual suffix. At each replacement, the saved state's memory is a subset of the actual visited prefix; its departure is no later and its reward no smaller. A next unvisited customer is therefore admissible. The projected memory plus that customer, and then any dominating subset, stays a subset of the actual visited prefix. If a leaf bound is used, the actual remaining distinct suffix is among its candidates even when the relaxed prefix has forgotten earlier visits. Thus every elementary route's total weighted reward is bounded. This addresses the claimant's stated ng-memory objection directly.

Result:44166 saved states,3130101 transitions,2785588 dominance closures,344513 leaf calls, zero unresolved cases. Of the leaf calls,2648 require fractional knapsack and282 require exact knapsack; the others close by summing possible rewards. With q_i=1000*p_i-u_i, U=181976, nonnegative penalties sum542092, at most four routes and no repeated customer give

    1000*score <= 4*181976+542092 =1269996.

Every prize is a multiple of10, so score<=1260. The independently replayed witness attains it. No floating solver termination or LP objective is accepted.

## Adversarial checks and limits

`independent_controls.py` independently exhaustively enumerates elementary routes for36 random6/7-customer fixtures. It checks full-memory, thinned and empty certificates against exact and deliberately false upper bounds:216 runs, all expected implications pass. Removing all real states, setting the real upper bound to zero, using a negative penalty, and using an oversized penalty all reject. These controls support implementation correctness; the induction above supplies the mathematical justification for forgetting memory.

The worker's config/plan explicitly says there is no hold-out. It predeclared c103/c104, then retained c104 after success; c103 stayed1210–1220. These are selected public instances, not evidence of untouched test data or broad success rates. Selection cannot invalidate a per-instance exact certificate. I did not rerun the public stochastic SISRs executable: reconstructing its published1260 score is sufficient for the exact-value comparison, and no heuristic runtime claim is being validated.

Relative to the inspected papers the added artifact is a verified upper certificate closing1260, not an improved score. Standard route-master dual penalties and ng relaxations already occur in the cited literature. Public-code/recent-paper checks and their access limits are recorded in PRIOR_ART.md; no universal priority assertion follows from them.

## Reproduction

Transport only these referee files and evidence/input plus evidence/sources/official_c104.txt to the authorized pod directory. On the pod, use:

    g++ -O3 -std=c++17 independent_upper.cpp -o independent_upper
    nice -n 10 ./independent_upper evidence/sources/official_c104.txt evidence/input/BEST.dual evidence/input/BEST.proof

This yields score_upper1260 and unresolved0. For the full original layout, input/ contains the three certificate data files and primal.json; sources/official_c104.txt is the official raw. Run `nice -n 10 python3 primary_and_primal.py` (PyMuPDF needed for PDF extraction) and `nice -n 10 python3 independent_controls.py` (standard library). Receipts and original sources needed to interpret the verdict are saved locally. No optimization code is required for replay.

The complete replay recipe is `reproduce_referee.sh`; transport it, the three independent source files and evidence/ to /workspace/ref_hugo_HB17 on the authorized pod. It makes the original input/sources layout explicitly. `controls_receipt.json` records every fixture run; the generator's seed is fixed, so the fixtures are reproducible without retaining bulky enumerations.
