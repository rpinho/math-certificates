# Fresh adversarial review of c44r8 — candidate, unrefereed

**Overall mathematical verdict: PASS, with one harmless missing hypothesis in the prose. My subjective probability that the claimed bound is correct is 99%.** This accepts the task's already reviewed c44r7 baseline, including its published catalogue, minimum-support and lattice premises. It is a fresh AI review, not independent human refereeing or a proof-assistant formalization.

My separately written exact optimizer reproduces

    R4 = 22,  46 <= R5 <= 50,  94 <= R6 <= 109,

    C44 <= 80880411492166173705437336107
           /39614081257132168796771975168
        = 2.04170862797946028691154129842849...
        < 2.0417086280.

The gain over the accepted round-seven rational is exactly

    3104740414275840613074929675/79228162514264337593543950336
    > 1/1000.

The universal lower bound remains 3/2. No Boolean function attaining the scalar upper ceilings has been produced. No substantive GAP or counterexample to the claimed bound was found.

There is one literal FALSE statement. **PROOF.md:229–232** quantifies (13) over integer-valued polynomials without saying they are nonzero. Take Q identically zero and r=1: its energy is zero, satisfying neither alternative. The repair is to insert “nonzero” at line 229. This does not affect any application: at **258–265**, j is relevant, so Q_j=2 Delta_j A is nonzero. The corrected lemma and all uses receive PASS. The same understood qualification applies to “nonminimal vector” at 246–247: the norm-gap theorem concerns nonzero lattice vectors. See the explicit exact receipt `receipts/negative_controls.json`.

Line references below use **P** = `../c44r8/PROOF.md`, **T** = `../c44r8/REPORT.md`, and **L** = `../c44r8/LOWER_ROUTE.md`. These refer to the live source files read for this review. The copied frozen P, L and both numerical certificates match their loose source originals. The c44r7 proofs and certificate match the accepted originals; its manifest is also compared, and every inherited manifest hash is checked. The round-eight manifest SHA256 is

    2a3e6b6a73a95fe6bf15f8abc34b62315a95fff921135d04a734969be0c1c6ab

It lists 221 mathematical/static entries totaling 17,369,793 bytes; including MANIFEST.json there are 222 files and 17,396,426 bytes. T:72 describes the 221 listed entries, rather than a count including the manifest. No hashed mathematical file was changed.

The inherited material is **P:24–225**: finite extrema; W_d=R_d/2^d; all local degrees d at a count extremum; R1–R4; the support/derivative and coordinatewise restriction inequalities; minimum influence; the integer Fourier grid; below-two Reed–Muller weights; and the nonintegral equality exclusion through cross-polytopal links. A textual diff shows these mathematical steps are reproduced from c44r7, with contextual/path changes. The Barnes–Wall gap is inherited too, but is newly applied to arbitrary-degree partials to find a control that can be retained. I replayed both accepted c44r7 scalar checkers and checked its manifest. I did not independently redo the entire already reviewed cubic catalogue classification or the earlier quartic/quintic case trees.

The following accounts for every new mathematical step and every new numerical use of inherited material. PASS means that the inference and its hypotheses were checked; finite tests corroborate the universal arguments and do not replace them.

| Step | Exact source lines | Verdict | Review evidence |
|---|---|---|---|
| Integer-polynomial gap as literally quantified | P:229–232 | **FALSE, harmless wording** | Q=0 is an exact counterexample. Insert “nonzero.” All actual Q_j are nonzero. |
| Odd-r lattice embedding and norm ratio | P:234–240 | PASS | For every t<=r, (r−1)/2>=floor(t/2). Scaling an integer bit-monomial vector lands in Lambda_n; norm/minimum is 2^r E Q². |
| Even-r embedding and dummy inputs | P:241–244 | PASS | r/2>=ceil(t/2); Delta_n minimum 2^n gives the same ratio. Dummy inputs double both norms and minima. |
| Apply the inherited second-minimum theorem | P:246–256 | PASS for nonzero Q | Nebe's primary Theorems 2.3 and 3.3, similarity of the pair, and the accepted expanded BW proof support precisely this normalization. External lattice classification remains a premise. |
| Half-integer partials obey minimum-or-3/2 gap | P:258–262 | PASS | Q_j=2 Delta_j A is a nonzero integer polynomial of degree <=k−1. Divide its energy gap by four: e0=2^(−k−1). |
| Many controls force at least one minimum partial | P:264–265 | PASS | If all h energies were >=3e0/2, their sum would exceed 2k lambda e0 when 3h>4k lambda. Strict inequality is used correctly. |
| Minimum partial has only values 0,+/−1/2 | P:267–270 | PASS | Support density times minimum nonzero integer square already exhausts E Q_j², so all nonzero values have magnitude one. |
| Restriction inequality for a specified subset | P:274–277 | PASS | The earlier proof is a sum of per-coordinate nonnegative inequalities; dropping selected summands preserves it. No independence of different coordinate slacks is assumed. |
| New ordinary budget, excluding selected i from the sum | P:279–285; T:35–40 | PASS | Original Y weights sum to (N−h−1)/2^d. They all vanish in active sections and have potential <=c in inactive sections. |
| Mandatory selected-coordinate slack | P:287–290 | PASS | Its expected section weight is p/2=lambda/2^d. Relative to its original 2^(−d), this improves the old count budget by exactly lambda−1. |
| q,r identities and same signs on double-active edges | P:292–299 | PASS | A minimum partial forbids opposite active signs. Only one-active edges contribute squared derivative 1/4, giving q=4e0 and r=(lambda−1)2^(−k). |
| Active edge and affine coefficient vanishing | P:301–303; T:42–45 | PASS | lambda>1 forces r>0. Subtracting the affine polynomial at the endpoints kills its j coefficient. |
| All degree-d terms meet K=H\{j} | P:305–312 | PASS | A missing-K B term has Y-size d or d−1; its constant or j-affine coefficient vanishes on the support. An i A term using only i,j has degree <=2<d. The intended use is d>=5. |
| Three section cases and selector representation | P:314–319 | PASS | Neither active: no i. Both active: signed i, independent of j,Y. Exactly one active: the stated selector with an arbitrary sign Boolean g. |
| Bound the selector's degree and local potentials | P:321–327 | PASS | The j times top-degree g term cannot cancel. Hence deg g<=d−2. The local degrees are 2, t+1 and old Y-degrees plus one, exactly as stated. |
| Constant-g exception and b_d envelope | P:329–333 | PASS | Constant g gives j-weight 1/4. Taking max over every lower degree t, plus 1/2, covers every section; no monotonicity of individual section degrees is presumed. |
| Retained-control count budget | P:334–339; T:45–56 | PASS | The outside set {j} union Y has N−h original coordinates. Direct averaging gives c(1−q−r)+(b−1/4)q and exactly (18). |
| q scaling and selected i slack after retaining j | P:341–344 | PASS | 2^d q=4 and q/4+r/2=p/2. No factor of two is missing. |
| Maximize over possible actual h, not just its upper cap | P:346–352 | PASS | Below the threshold only ordinary budget applies; above it take the smaller budget. Both increase by one with h within their range. The two upper endpoints h0,hmax suffice. |
| Degree-five b and lambda=1 case | P:356–357 | PASS | b5=15/16; maximum real budget 201/4, so integer N<=50. This also fixes the previous round's prose erratum. |
| Degree-five second weight and all remaining weights | P:357–362 | PASS | h<=11 follows from nonintegral equality. At h<=8 ordinary budget <=391/8; at 9..11 retained budget <=407/8. Other weights give N<=45. |
| Degree-six b and lambda=1 case | P:364–366 | PASS | c5=25/16, b6=31/32, retained correction −1/4. Ordinary real budget is 863/8. |
| Degree-six second weight and remaining weights | P:366–370 | PASS | h<=14; ordinary/retained maxima 1701/16 and 1745/16. The other weights give floor(768/7)=109. Thus R6<=109. |
| Remove need for finite second-weight classifications | P:372–383; T:52–56 | PASS | The above R5/R6 arguments use only general equality exclusion. Independent simple and sharp propagation gives identical rows 5..96. |
| Energy grid, equality demotion, joint floor cells | P:385–392 | PASS | Both hmax and applicability endpoint h0 changes are included. Between changes, valid budgets and influence decrease with lambda; equality demotion is accounted for. |
| Complete representative indices, including point after demotion | P:394–401 | PASS | Both families of floor transitions are tested, as is lambda=2. Omitting the first point after demotion would be unsafe; the implementation includes it. |
| Checker A next-count exclusion and scalar feasible witnesses | P:403–409; T:76–81 | PASS | Source inspection and replay pass. The influence interval covers all N>=R+1. The stored feasible point is correctly described as scalar feasibility. |
| Checker B common-denominator numerators | P:411–419 | PASS | Substitution c=C/(2G) gives (2C+h+1)G²−Cz. The retained-minus-ordinary numerator is (2B−C−2G)G; taking min with zero is correct. |
| Checker B maxima/full-grid verification and final comparison | P:421–427 | PASS | Replay agrees with the new reviewer algorithm, which enumerates each h first. My additional exhaustive original-grid/every-h check reaches d=13; the supplied B's d<=16 scan also passes. |
| Iterate Xi lift from any seed, and conditional 47-variable lower bound | P:431–444; T:111–114 | PASS | Disjoint lift sends n to 2n+2 without losing degree or relevance. Limit is (n+2)/2^d, giving 49/32 for a degree-five 47-variable seed. |
| Xi lower witnesses and inherited exact controls | P:431–439; T:102–109 | PASS | Elementary induction and exact sparse controls give 22,46,94. These are existence lower bounds. |
| Tail estimate applied to the new c96 | P:446–466 | PASS | Actual extremizers have lambda<=d/2. The old weaker inequality gives increment <=d(d−1)/2^d. The sum is (H²+3H+4)/2^H; finite caps are nondecreasing. |
| Exact headline rational, decimal and improvement | P:3–9, 464–474; T:6–19 | PASS | Independent exact arithmetic reproduces the bound and gain above; no floating-point decision is used. |
| R5=50 and R6=109 surviving scalar points | P:476–485; T:116–123 | PASS | Sharp R5=50 can use lambda=1, real budget 201/4. For R6=109, lambda=7/4,h=17 gives 3561/32 and influence 768/7. h<=14 would instead give 3465/32. These are not Boolean witnesses. |
| Fixed scalar sequence is nondecreasing and has the stated limit interval | P:487–495; T:125–130 | PASS | N0=2^d c is feasible at lambda=1,h=2(d−1), when c<=d/2. Lower witnesses and the weaker recurrence bound its increments. After 96, the remaining tail <1/2 preserves c<=d/2; the width is <1.3e−25. No optimality for Boolean functions is inferred. |

The separate lower-construction classification is also new. It does not support a better universal upper bound, so its scope matters.

| Step | Exact source lines | Verdict | Review evidence |
|---|---|---|---|
| Cubic library equivalences preserve weighted support optimization | L:8–14 | PASS on inherited completeness premise | Input flips and output sign change coefficients' signs only; permutations relabel weights. All 761 inherited rows are used. |
| Exact degree and relevant count for disjoint homogeneous substitutions | L:16–30 | PASS | Every inner monomial is nonconstant; its occupied block set uniquely identifies the outer mask, so cancellation cannot remove the maximum degree or an inner variable. |
| Finite per-coordinate weight ranges | L:32–37 | PASS | A largest outer mask using j yields r_j+(d_j(g)−1)<=d. All finite integer allocations in these ranges are tested. |
| All allocation maxima and totals | L:39–54; T:102–106 | PASS | Both exact supplied implementations replay. Degree 2..6 maxima are 4,10,22,46,94; totals are 8,796,8080,49761,221198. One checks every artifact row; the other enumerates independently from the catalogue. |
| Degree and relevance for arbitrary nonconstant inner functions | L:56–67 | PASS | A maximum positive weighted outer mask's top monomial cannot be cancelled by any strict superset, whose weight would be larger. Surjectivity of each disjoint Boolean block proves relevance. |
| Nonprojection outer functions have local degrees >=2 | L:72–75 | PASS | For nonzero constant derivative a, both B+a and B−a being signs forces a=+/−1 and B=0. |
| Closure induction and removal of constants/projections | L:69–84; T:106–109 | PASS | In a nonlinear outer node every inner degree is <=d−1. Replacing each inner by Xi of its degree weakly increases its variable count, while preserving the weighted degree constraints. Constants can first be substituted into the outer function and irrelevant blocks discarded. |
| Lower-route scope and no 47-variable seed in that family | L:3–6, 86–90; P:442–444; T:111–114 | PASS | The ceiling concerns disjoint cubic-composition closure through degree six. Shared-input constructions and arbitrary degree-five functions remain outside it. |
| Unfinished optional third-weight search supplies no bound | T:119–123; P:483–485 | PASS as scope limitation | Its unverified exclusions are not used in either accepted scalar mode. I do not accept an h<=15 or h<=14 theorem from that exploration. |

The proof checks deserve emphasis. After restricting H, summing only Y's coordinatewise inequality is enough for (15); it never subtracts a possibly negative total-potential slack. For (18), B vanishes identically in Y at every active H assignment. In particular, each Y Fourier coefficient of B vanishes on that support. A degree-d term missing K can only have zero or one H-coordinate, and the active edge removes exactly the latter possibility. This proves the degree drop before applying a lower-degree cap to any section. The one-active section cap includes every t<=d−2, including the constant exception; it does not presume all branches have the same degree.

My new exact optimizer, `independent_scalar.py`, was written before reading either supplied scalar checker or generator. It imports no packet code. For each d it enumerates **every integer h** up to floor(2kU), where U=d·2^(d−1)/L_d and the exact Xi construction proves the lower count L_d. Below two it tests the full permitted spectrum. For fixed h above two, budgets decrease until the sole retained-control applicability endpoint; it tests the first feasible grid point and the first point after that endpoint. Equality demotion is handled directly as a forbidden equality for this h. This is a different completeness reduction from the packet's energy floor cells and two h endpoints. `REVIEW_PROOF.md` supplies the written proof. All 92 new caps in both modes match. A second path enumerates every original energy-grid point and every h through degree 13. Its final cap plus the exact tail reproduces the headline fraction. See `receipts/independent_scalar.json` and `receipts/independent_ledger.json`.

I tried to break the universal completion lemmas using exact truth tables, without restricting to homogeneous count-extremizer tables. `adversarial_tables.cpp` checks all 65,812 Boolean truth tables on one through four inputs and every one of the 761 cubic catalogue rows, for 66,573 functions total. It checks the original coordinate weights individually, both averaged inequalities, all eligible j, and every resulting restriction section. It passes 265,518 relevant partials, 114,809 retained-control cases and 593,134 sections; 976 eligible functions have mixed local degrees. `ternary_attack.cpp` exhausts all 43,046,721 four-input ternary tables. Nonzero energy gaps pass, and 956,672 minimum-partial/above-minimum-support active-edge cases pass. These are finite corroborations, not proofs in arbitrary dimension.

The negative controls exhibit real failures when hypotheses are removed:

- Besides Q=0 refuting the wording of (13), four-variable parity has d=4, lambda=8,h=3. The ordinary budget is exactly four, whereas (18), if incorrectly applied without its control-count threshold, would give three. Its h fails the threshold, as required.
- In the ten-variable Xi3 function, take the leaf coordinate i=0 and retain j=8 in the polynomial stored in `negative_controls.json`. Its derivative has lambda=1, minimum j-energy 1/8 and no double-active j-edge. Four degree-three monomials miss K. Thus the lambda>1 premise cannot simply be discarded from the active-edge/degree-drop argument. The packet does not discard it.

The accepted c44r7 scalar replay reproduces R5<=51, R6<=110 and 164865563398608188023949601889/79228162514264337593543950336. The new supplied A/B scalar checkers, both composition checkers, both finite completion controls and the inherited finite integer-gap control replay PASS. No full re-refereeing of the already accepted earlier classifications is asserted. Historical author process/resource claims in T:175–184 are recorded as history, not reconstructed by this review.

Exact reproduction uses Python's standard library and g++17. Copy this review directory to the authorized pod directory first. On a rented pod, from `the job directory`:

```sh
mkdir -p build

nice -n 10 python3 run_tasks.py independent independent_tasks.json
nice -n 10 python3 run_tasks.py replay replay_tasks.json
nice -n 10 python3 run_tasks.py attack attack_tasks.json
nice -n 10 python3 run_tasks.py ternary ternary_tasks.json
nice -n 10 python3 run_tasks.py negative negative_tasks.json
nice -n 10 python3 run_tasks.py final_audit final_audit_tasks.json
```

Use `--replay` after the two file arguments to bypass only the historical 2026-11-02 03:45 UTC launch guard. The wrapper enforces nice>=10, single-threaded BLAS, an 8 GB address-space cap, a 20-minute child timeout and child cleanup, and records every child PID/exit code. The replay task now prepares the disposable `baseline_work/frozen` directory before its two baseline steps; their receipt path depends on whether its directory is named `frozen`. Our historical run initially wrote two generated receipt files into the review copy's `frozen/inputs/round7/receipts`; those files were moved into `receipts/baseline_generated` before the successful strict file-set audit. No hashed file changed. The initial public-audit seed-transfer race was likewise retried successfully and retained in the ledger. The first closeout audit counted its own administrative PID; the corrected filter excludes the currently running audit and its supervisor, and the final process audit passes. All target-source directories remained read only.

`PRIOR_ART.md` and source receipts document the initial live raw table and open PRs, public code and AI-result repositories, recent arXiv, primary theorem sources, and indexed community checks. The directly fetched table lists Ricardo Pinho's 4.3576549226* candidate (retaining Épi's data), and Wellens 4.394 as the published baseline. The current applicable PR294 diff records Pinho's earlier 2.1974348818* candidate. Cached search snippets contain older numbers and were not used as the controlling evidence. No applicable stronger public bound was located in the bounded coverage. No novelty, priority, or public-record claim is made.

The final live refresh at 23:59:09 UTC confirmed the same table and applicable PR294 diff. One extra exact-constant GitHub repository query returned HTTP 429; primary live sources and all other final fetches succeeded, as documented in PRIOR_ART.md. The final strict manifest and process audit passed at 2026-11-02 00:02:36 UTC, checked 29 distinct started child PIDs, and found no remaining own workers. Its mathematical files match the original manifest. All checks finished before both the four-hour review deadline and the 05:35 UTC pod cutoff. Retained pod data is about 35.9 MB and local review data about 19 MB, below 50 MB. Compute used nice 10, single-threaded BLAS and 8 GB per-child address-space limits; at most two mathematical children ran concurrently. The pod was left running, and no other job was modified. No commits, pushes, PRs, posts, external messages, branch operations or file deletions occurred. All conclusions remain candidate and unrefereed. Recommended next mathematical work is minimum-support quartic Boolean completion or a certified quintic third-weight control bound, rather than further iteration of the same scalar system. The only requested correction to this packet is “nonzero” in P:229.
