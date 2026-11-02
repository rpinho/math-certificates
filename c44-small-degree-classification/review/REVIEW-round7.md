# Fresh adversarial review: C44 round seven

**Overall mathematical verdict: PASS, with a harmless arithmetic wording
correction. My subjective probability that the claimed bound is correct is
99%.** I found no mathematical GAP in the new classifications. The exact
result independently reproduced is

\[
46\le R_5\le51,\qquad94\le R_6\le110,\qquad
C_{44}\le
\frac{164865563398608188023949601889}{79228162514264337593543950336}
=2.0808959613183706681908997860183346818609863425714\ldots
<2.0808959614.
\]

This accepts the task's already reviewed gap1 and c44r6 inputs. It is a fresh
AI review, not a proof-assistant formalization or independent human review.
Published completeness and lattice theorems remain mathematical premises.
The source packet was read only; all replay writes and heavy computation
were made in the review's own authorized pod directory.

There are two literal reporting defects:

| Location | Verdict | Finding and effect |
|---|---|---|
| `../c44r7/PROOF.md:342–343` | **FALSE as a real-budget statement** | At lambda=1, the budget is `44+8−7/4=201/4=50.25`, not at most 50. Its integer consequence is correctly `N<=50`. Replace the phrase by “its integer count bound is 50.” This changes no claimed bound. |
| `../c44r7/REPORT.md:138–141`, especially line 140 | **FALSE as the current PR baseline** | PR294 had already been updated at `2026-11-01T22:41:38Z` to `2.1974348818*`, explicitly replacing `3.9819073803*`. The report describes the latter as current after its 22:50 audit. Direct live API receipt: `sources/pr294_live.json:17,39,44`. This affects the public-audit description, not the mathematics or the comparison with round six. |

“PASS” below means that I checked the inference and its stated hypotheses,
with exact independent computation where finite enumeration is involved.
An unsuccessful SAT run is not a PASS certificate and is not counted as an
exclusion. There is no unresolved mathematical GAP in the new bound found
by this review.

For exact line references, `P` denotes [c44r7/PROOF.md](../c44r7/PROOF.md),
`L` denotes [LATTICE_PROOF.md](../c44r7/LATTICE_PROOF.md),
`B` denotes [BW_GAP_PROOF.md](../c44r7/BW_GAP_PROOF.md), and `T` denotes
[c44r7/REPORT.md](../c44r7/REPORT.md). The loose and frozen versions of P,
L, B and certificate.json match byte for byte. All 196 frozen manifest
entries matched before and after replay: `receipts/artifact_audit.json`.

The inherited material is P:28–158: finite extrema, the CHS identity,
count-extremizer local degrees, weighted restrictions, minimum influence,
the integer Fourier grid, and the below-two Reed–Muller weight spectrum.
The cubic catalogue argument and R4=22 are from gap1. The energy/restriction
and scalar/tail framework are from c44r6. Both inherited c44r6 checkers were
replayed successfully. I did not reopen the full reviewed gap1 catalogue
classification. The following table accounts for the new mathematical
steps and the new numerical uses of inherited steps.

The inherited P files under inputs/gap1 and inputs/round6 are byte-identical
to the corresponding `../gap1/PROOF.md` and `../c44r6/PROOF.md`; both copied
round-six verifier sources also match their originals. No changed inherited
proof is concealed by the input-directory names.

| New step | Exact lines | Verdict | Audit |
|---|---|---|---|
| Combine R4=22 with round-six restrictions | P:19–26, 334–341; T:29–38 | PASS | Gives R5<=53 and R6<=117 before refinements; independently propagated. |
| Equality forces homogeneous A and minimum partials | P:162–165 | PASS | Both sources of energy slack are nonnegative; equality forces every one to vanish. |
| Minimum-partial tensor classification and homogeneous reduction | P:167–183 | PASS | Correct specialization of Valyuzhenich Theorem 2(2); point factors and blocks of size >=3 have varying Fourier degrees and cannot occur in a disjoint homogeneous product. |
| Fourier links give components of size 2k | P:185–195 | PASS | Every vertex link is exactly the transversal complex of k−1 pairs. The resulting h is divisible by 2k. Only the safe strict inequality at nonintegral lambda is used. |
| Cross-polytope lemma, first case | P:197–216 | PASS | The two extra vertices coincide by the degree bound at any vertex of R. The resulting suspension exhausts all links and hence its connected component. |
| Cross-polytope lemma, second case | P:218–229 | PASS | The complete 1-skeleton has 2r+1 vertices. Incidence count and at most 2^(r−1) facets avoiding v contradict one another for r>=2. Source checked; the expanded proof also covers the endpoint directly. |
| Quartic second-weight case h=12 | P:235–239 | PASS | Nonintegral equality exclusion, k=4, lambda=3/2. |
| Quartic grid, parity and seven good coordinates | P:241–246 | PASS | Norm 24, e_j even and >=8, total derivative energy <=96, hence at most four e_j>=10 among eleven coordinates. |
| Seven minimum cubic-partial types | P:248–266 | PASS | Exactly the degree-cost-three partitions; each has eight unit numerator terms, balanced coordinate incidences, and empty intersection. |
| Force a homogeneous good quartic partial | P:268–277 | PASS | If all seven were nonhomogeneous, sum L_j>=28 but <=3L<=24. |
| Quartic orbit and template completeness | P:279–299 | PASS | Eight orbits, all 11,880 templates. Independent construction/search and full table comparison both pass. |
| Quartic branch compatibility and prunes | P:301–322 | PASS | Forced coefficients have square one; no omitted term can use a completed good coordinate. Norm, degree deficit and unselected-energy prunes are necessary conditions. |
| Reject all nine quartic unsigned models | P:324–330 | PASS | Two absent variables each need all eight remaining norm units. One must occur in every Fourier mask of the other's minimum partial, contradicting empty intersection. |
| Derive R5<=51 | P:341–345 | PASS after wording correction above | Cases lambda=1, lambda=3/2, lambda>=7/4 are exhaustive. Exact integer bounds are 50, 51, and 45. |
| Revised scalar cells after equality demotion | P:347–368 | PASS | Both first and second grid points are necessary. I recomputed the cell optimization and also scanned every energy-grid point through degree 16. |
| New 46/94 witness checks | P:372–380; CONTROLS.md:8–11 | PASS | Independently built integer polynomials and verified f^2=1, degree, all variable incidences and counts. The family itself is inherited CHS/Shinkar–Tal. |
| Apply the inherited elementary tail to new caps | P:382–405 | PASS | Sum is (H^2+3H+4)/2^H; at H=96 the numerator is 9508. Finite caps are nondecreasing. |
| Scalar feasible points and limit interpretation | P:417–438; T:155–166 | PASS | The witnesses are scalar feasibility, not Boolean functions. The tail bounds the scalar increment as well; no Boolean optimality conclusion is drawn. |
| Odd/even integer-polynomial lattice embeddings | L:12–49 | PASS | Scaling exponents meet every bit-coefficient divisibility condition. The ratio to the appropriate lattice minimum is exactly 2^r E Q^2, in both parities. Dummy inputs preserve the ratio. |
| Quintic energy gap e_j=16 or >=24 | L:53–72 | PASS | For Q=2 Delta_j A, E Q^2=e_j/256; apply r=4 gap. Minimum partials have sixteen coefficients of numerator magnitude one. |
| Twelve degree-four partial types and deficit bounds | L:74–101 | PASS | The type equation is exhaustive. Nonhomogeneous means <=7 controls, hence L_j>=8. Two absent good variables require >=24 norm units. |
| Quintic h=15 exclusion | L:103–106 | PASS | Nonintegral equality exclusion, k=5, lambda=3/2. |
| Quintic h=14 reduction to twelve good coordinates | L:108–120 | PASS | At most two energies can exceed 16; deficit forces a homogeneous good partial. Four pair-count orbits are exhaustive. |
| h=14 finite exclusion and local shortcut | L:122–143 | PASS | The required masks already use seven controls, so only the three types with >=7 controls can occur, on those controls plus at most one extra. My independent search used full compatible tensors and did not rely on this shortcut. |
| Quintic h=13 split and good-count inequalities | L:147–158, 176–180 | PASS | g>=9+L/8. With no homogeneous good partial, 8g<=4L, hence L>=24 and g>=12. These two cases exhaust h=13. |
| Nine homogeneous-seed h=13 cases | L:155–174 | PASS | Complete search leaves ten unsigned models, all excluded by the sixteen remaining units and empty intersection. |
| Eleven nonhomogeneous seed types, 31 positions | L:176–198 | PASS | Every unselected-coordinate position is represented under permutations of equal factors and within each block. “Unselected” may still be good; the model allows this. |
| Nonhomogeneous residual coefficients and rejection | L:200–217 | PASS | Only empty and singleton-unselected masks remain; all integer solutions of a^2+c^2=48−|E| are covered, with both degree deficit and the energy gap checked. If the remaining coordinate is good its full nonhomogeneous template is checked. No residual survives. |
| Sharp h<=12 and R6<=110 | L:219–238 | PASS | Budgets at lambda=1 and 3/2 are 1757/16 and 3543/32; lambda>=7/4 gives N<=109. |
| New sharp ternary h=10/12 witnesses | L:223–224; CONTROLS.md:13–26; T:155–159 | PASS | Exact A^3=A convolution, norm, degree and controls pass. These witnesses also survive all prunes of my independent search at the smaller feasible control counts. |
| Classical lattice basis, minima and pair-preserving transitivity | B:17–41 | PASS as cited premises | Checked the primary theorem statements and Nebe's precise n=3 stabilizer convention. The group classification is not independently re-proved here. |
| Similarity of the ordered lattice pair | B:45–73 | PASS | The two generator calculations and S^2=2I prove both containments/equalities with the claimed norm scaling. |
| Minimum-vector coset gap, odd n | B:77–95 | PASS | Dividing by the largest common power of two gives a nonzero binary residue of degree <=2j. Its support alone supplies norm >=2a_n. |
| Minimum-vector coset gap, even n | B:97–118 | PASS | Use (Delta,2 Lambda); the residue degree is <=2j−1. The j=0 case cannot occur. Similarity transports the result back. The coset cannot contain zero because Delta's minimum is twice Lambda's. |
| Exact lattice recursion | B:122–134 | PASS | Bit-monomial bases give both containments; the branch difference has precisely the Delta prefactor. |
| Norm divisibility and base cases | B:136–152 | PASS | Diagonal and twice-cross-term exponents have the asserted divisibility; n=2,3,4,5 give the required gap, with n=1 handled separately. |
| Norm-gap induction | B:156–174 | PASS | Zero, nonminimal and minimal smaller branches exhaust the possibilities. Each gives total norm >=3a_n above the minimum 2a_n. |
| Exact final rational and claimed gains | P:3–11, 397–403; T:3–25, 29–35 | PASS | Independent arithmetic agrees in every checked mode; all decimal comparisons use exact rationals. |

The published statements were checked at their primary sources:
[Valyuzhenich, Theorem 2(2)](https://arxiv.org/html/2303.10995),
[Masuda–Panov, Lemma 4.7](https://arxiv.org/pdf/math/0607094v2),
[Barnes–Wall, Theorems 3.1(ii), 3.2](https://doi.org/10.1017/S1446788700025064),
[Broué–Enguehard, Theorem II.4, printed pp.36–37](https://www.numdam.org/item/10.24033/asens.1241.pdf),
and [Nebe, Theorems 2.3, 2.5, 3.3](https://www.math.rwth-aachen.de/~Gabriele.Nebe/papers/BW.pdf).
The expanded argument matches the needed lattice normalization. In particular
I found no misuse of binary affine substitutions to preserve real degree.

The complete finite case list follows. These cases classify ternary
derivatives (degree four for the R5 argument and degree five for R6), not
all Boolean functions at degree five or six. The selected “good” coordinates
are coordinates whose derivative energy is minimum. All other coordinates
are merely unselected and may also be good. Signs are relaxed throughout
the unsigned search, which can add models but cannot omit an actual signed
polynomial.

For homogeneous seeds, the pair tuple gives the selected-good counts in
the seed's disjoint pairs, sorted increasingly; b gives the selected-good
count outside those pairs. Coordinate 0 is also selected. Permuting pairs,
swapping pair members and permuting outside coordinates makes precisely
the following orbits. `Terminal` counts unsigned supports before the final
residual contradiction. `Nodes` are from my independent adaptive search,
not the target's trace.

| Quartic h=11 case | Pair tuple | b | Nodes | Terminal | Verdict |
|---|---|---:|---:|---:|---|
| Q4-0 | (0,0,2) | 4 | 2439 | 0 | PASS |
| Q4-1 | (0,1,1) | 4 | 17 | 0 | PASS |
| Q4-2 | (0,1,2) | 3 | 17 | 0 | PASS |
| Q4-3 | (0,2,2) | 2 | 54 | 0 | PASS |
| Q4-4 | (1,1,1) | 3 | 17 | 0 | PASS |
| Q4-5 | (1,1,2) | 2 | 53 | 0 | PASS |
| Q4-6 | (1,2,2) | 1 | 147 | 1 | PASS: final model rejected |
| Q4-7 | (2,2,2) | 0 | 49 | 8 | PASS: all eight rejected |

Exact source lines for all Q4 cases: P:279–284 (orbit reduction),
286–322 (domains/search), 324–330 (terminal contradiction). At least seven
good coordinates are forced by P:241–275. Their six nonseed coordinates
give `b=6−sum(tuple)`, with 0<=b<=4; this proves the eight-case exhaustiveness.
All nine terminal supports match the target certificate exactly.

| Quintic h=14 case | Pair tuple | b | Nodes | Terminal | Verdict |
|---|---|---:|---:|---:|---|
| Q5-14-0 | (0,2,2,2) | 5 | 22 | 0 | PASS |
| Q5-14-1 | (1,1,2,2) | 5 | 21 | 0 | PASS |
| Q5-14-2 | (1,2,2,2) | 4 | 21 | 0 | PASS |
| Q5-14-3 | (2,2,2,2) | 3 | 22 | 0 | PASS |

Exact source lines for all four cases: L:108–120 (reduction and orbit list),
122–143 (exclusions). There are eleven additional selected-good coordinates,
only five outside the four pairs, so the tuple sum is at least six. The four
listed tuples are all sorted four-tuples in {0,1,2} satisfying that condition.

| Quintic h=13, homogeneous seed | Pair tuple | b | Nodes | Terminal | Verdict |
|---|---|---:|---:|---:|---|
| Q5-13-H0 | (0,0,2,2) | 4 | 20 | 0 | PASS |
| Q5-13-H1 | (0,1,1,2) | 4 | 19 | 0 | PASS |
| Q5-13-H2 | (0,1,2,2) | 3 | 19 | 0 | PASS |
| Q5-13-H3 | (0,2,2,2) | 2 | 32 | 0 | PASS |
| Q5-13-H4 | (1,1,1,1) | 4 | 19 | 0 | PASS |
| Q5-13-H5 | (1,1,1,2) | 3 | 19 | 0 | PASS |
| Q5-13-H6 | (1,1,2,2) | 2 | 31 | 0 | PASS |
| Q5-13-H7 | (1,2,2,2) | 1 | 73 | 1 | PASS: final model rejected |
| Q5-13-H8 | (2,2,2,2) | 0 | 73 | 9 | PASS: all nine rejected |

Exact source lines for these nine cases: L:155–165 (case reduction and
constraints), 167–174 (terminal exclusions). Here `b=8−sum(tuple)`,
0<=b<=4. At least nine good coordinates follow from L:147–153. The ten
terminal supports match the target certificate exactly; all have 32 terms
and at least two absent coordinates.

For the no-homogeneous-good-partial case, write the seed type as
`(points,pairs,triples,fours,fives)`. The complete equation is
`points+pairs+2*triples+3*fours+4*fives=4`; removing the four-pair type leaves
the eleven types below. Coordinates are assigned in that factor order,
starting at 1. `u` is the one unselected coordinate; the first coordinate
of each occurring factor size and the first outside coordinate are all
its orbit representatives. Every case below has zero feasible residual.

| Quintic h=13 nonhomogeneous case | Seed type | u | Nodes | Verdict |
|---|---|---:|---:|---|
| N0 | (0,0,0,0,1) | 1 | 17 | PASS |
| N1 | (0,0,0,0,1) | 6 | 17 | PASS |
| N2 | (0,0,2,0,0) | 1 | 19 | PASS |
| N3 | (0,0,2,0,0) | 7 | 19 | PASS |
| N4 | (0,1,0,1,0) | 1 | 19 | PASS |
| N5 | (0,1,0,1,0) | 3 | 20 | PASS |
| N6 | (0,1,0,1,0) | 7 | 20 | PASS |
| N7 | (0,2,1,0,0) | 1 | 19 | PASS |
| N8 | (0,2,1,0,0) | 5 | 20 | PASS |
| N9 | (0,2,1,0,0) | 8 | 20 | PASS |
| N10 | (1,0,0,1,0) | 1 | 17 | PASS |
| N11 | (1,0,0,1,0) | 2 | 17 | PASS |
| N12 | (1,0,0,1,0) | 6 | 17 | PASS |
| N13 | (1,1,1,0,0) | 1 | 20 | PASS |
| N14 | (1,1,1,0,0) | 2 | 19 | PASS |
| N15 | (1,1,1,0,0) | 4 | 19 | PASS |
| N16 | (1,1,1,0,0) | 7 | 19 | PASS |
| N17 | (1,3,0,0,0) | 1 | 20 | PASS |
| N18 | (1,3,0,0,0) | 2 | 9 | PASS |
| N19 | (1,3,0,0,0) | 8 | 9 | PASS |
| N20 | (2,0,1,0,0) | 1 | 17 | PASS |
| N21 | (2,0,1,0,0) | 3 | 17 | PASS |
| N22 | (2,0,1,0,0) | 6 | 17 | PASS |
| N23 | (2,2,0,0,0) | 1 | 19 | PASS |
| N24 | (2,2,0,0,0) | 3 | 19 | PASS |
| N25 | (2,2,0,0,0) | 7 | 19 | PASS |
| N26 | (3,1,0,0,0) | 1 | 17 | PASS |
| N27 | (3,1,0,0,0) | 4 | 17 | PASS |
| N28 | (3,1,0,0,0) | 6 | 17 | PASS |
| N29 | (4,0,0,0,0) | 1 | 10 | PASS |
| N30 | (4,0,0,0,0) | 5 | 10 | PASS |

Exact source lines for all N cases: L:176–188 (why twelve selected good
coordinates, all eleven types, all 31 positions), 190–198 (complete domains),
200–217 (all prunes and residual rejection). The residual test is important:
an omitted Fourier coefficient cannot use any of the twelve completed
coordinates. Only the constant and the singleton u remain. Thus this is an
exhaustive integer square equation, not a heuristic support cutoff.

My independent search in `independent_classification.py` generates a tensor
domain from the required masks themselves. Each nonpoint block imposes a
parity equation on those masks; the blocks must be disjoint and cover every
required coordinate, with total degree cost k−1. It then chooses the next
good coordinate having the most forced coefficients. It reads no target
template or trace until comparing its final terminal supports. This covers
all 52 cases in about ten seconds on the pod. Separately, its unrestricted
template generation exactly reproduces all 11,880 quartic and 359,502 quintic
patterns. The degree-four and degree-five sharp examples are positive
controls for the entire pruning search, not just template membership:
their actual unsigned supports survive at h=10 and h=12, respectively.
Receipts: `independent_classification.json` and `positive_controls.json`.

Direct signed counterexample attempts were also made with Z3 5.3.3.0:

| Encoding | Search domain | Result | Interpretation |
|---|---|---|---|
| Integer truth values, all high Walsh coefficients zero | n=5, real degree <=3, squared norm 5 (minimum 4) | UNSAT | Finite corroboration of the integer energy gap only. |
| Same | n=6, degree <=4, norm 5 | UNKNOWN: 60-second timeout | No exclusion proved by this run. |
| Same | n=7, degree <=4, norms 9–11 | UNKNOWN: 60-second timeout | No exclusion proved by this run. |
| Same | n=8, degree <=4, norms 17–23 | UNKNOWN: 60-second timeout | No exclusion proved by this run. |
| Signed integer Fourier coefficients, exact norm, every ternary truth value, homogeneous minimum-partial seed | Quartic with all eleven controls | UNKNOWN: memory limit | No exclusion proved by this run. |
| Same | Quintic with all thirteen controls | UNKNOWN: memory limit | No exclusion proved by this run. |
| Linear truth-coordinate encoding, same seed, exact energy and relevance, without template or lattice assumptions | Eleven controls | UNKNOWN: timeout, about 120 seconds solving | No exclusion proved by this run. |
| Same | Thirteen controls | UNKNOWN: timeout, about 140 seconds solving after about 106 seconds building | No exclusion proved by this run. |

The Fourier formulation fixes the seed derivative to a product of pairs;
coordinate/output sign changes justify this normalization. The alternative
truth formulation uses Q=2B: on active seed assignments Q is a sign; on
inactive assignments it is 0 or +/-2. Exactly 32 (quartic) or 64 (quintic)
inactive assignments must be nonzero. Both formulations enforce actual real
degree, not binary degree. No SAT model giving a counterexample was found.
The direct solver failures are retained honestly and are not used to raise
confidence in any universal assertion.

The independently recomputed scalar outcomes are:

| Added information | R5 cap | R6 cap | Strict C44 ceiling |
|---|---:|---:|---|
| Combine reviewed R4=22 with round six | 53 | 117 | 2.1720558669 |
| Exclude nonintegral energy equality | 52 | 114 | 2.1255305914 |
| Quartic second-weight exclusion | 51 | 112 | 2.0963373341 |
| Quintic second-weight exclusion as well | 51 | 110 | 2.0808959614 |

`independent_arithmetic.py` reads the artifact only after computing its
counts. It scans every original control-count cell, handles the demoted
endpoint and its next grid point, and verifies the result against a full
grid scan through degree 16. It separately constructs the CHS lower
polynomials using integer numerators, verifies exact XOR convolution
f^2=1, and checks every relevant variable. The degree-five witness has
256 terms and denominator 16 on 46 variables; degree six has 1024 terms
and denominator 32 on 94 variables. These prove only the lower endpoints,
not R5=46 or R6=94. The matching upper-control examples are ternary
polynomials, not Boolean completions with counts 51 or 110.

The final step adds the exact inherited tail `9508/2^96` to the newly
computed cap at 96. The classified result and all four comparison modes
match the target's exact rationals. The scalar witness points at 51 and
110 remain feasible, so iterating these same scalar constraints cannot
establish the exact Boolean maxima 46 and 94.

For reproduction, all heavy commands belong on the authorized pod. From
this review directory, copy files into its own remote directory:

```sh
ssh a rented pod 'mkdir -p the job directory the job directory'
rsync -a ../c44r7/frozen/ a rented pod:the job directory
rsync -a *.py a rented pod:the job directory
ssh a rented pod 'cd the job directory && tmux new-session -d -s review_c44r7_reproduce "nice -n 10 python3 run_review.py > receipts/reproduce.log 2>&1"'
```

After that replay completes, run the independent arithmetic/classification
and optional signed searches under the same conditions. Install Z3 into
the review-owned `deps` directory if it is absent; only the SAT attacks
require it. The arithmetic, classifications, controls and target checkers
use the standard library.

```sh
ssh a rented pod 'cd the job directory && mkdir -p tmp && TMPDIR=the job directory nice -n 10 pip install --no-cache-dir --no-input --target deps z3-solver==5.3.3.0'
ssh a rented pod 'cd the job directory && tmux new-session -d -s review_c44r7_independent_reproduce "nice -n 10 python3 run_independent.py > receipts/independent_reproduce.log 2>&1"'
ssh a rented pod 'cd the job directory && tmux new-session -d -s review_c44r7_supplement_reproduce "nice -n 10 python3 run_supplement.py > receipts/supplement_reproduce.log 2>&1"'
ssh a rented pod 'cd the job directory && tmux new-session -d -s review_c44r7_truth_reproduce "nice -n 10 python3 run_truth.py > receipts/truth_reproduce.log 2>&1"'
ssh a rented pod 'cd the job directory && tmux new-session -d -s review_c44r7_positive_reproduce "nice -n 10 python3 run_positive.py > receipts/positive_reproduce.log 2>&1"'
```

Run the last two sessions after the preceding sessions finish to preserve
the conservative four-worker limit. Supervisors set single-threaded BLAS,
track child PIDs, impose deadlines and reap every child; `nice` is inherited.
The initial recorded baseline invocations passed a directory where those
old scripts expect a JSON filename, producing two wrapper errors. Correct
invocations in `supplement_processes.json` passed both checks. The initial
replay ledger is preserved separately as `replay_initial.json`.

Pull receipts without overwriting the preserved initial replay ledger:

```sh
rsync -a --exclude replay.json a rented pod:the job directory receipts/
rsync -a a rented pod:the job directory receipts/replayed_target/
```

Literature/source coverage is recorded in `PRIOR_ART.md`. I checked the
[official table](https://teorth.github.io/optimizationproblems/constants/44a.html),
its raw source, open PR/issue pages and the current
[PR294 record](https://github.com/teorth/optimizationproblems/pull/294),
the named AI-result repositories and recent indexed papers/community
results. Cached web results were stale; direct no-cache HTTP reads supplied
the live table and PR correction above. Public global code search was
incomplete, and private communities were not accessed. This review makes
no priority claim. The principal public method is the CHS/Wellens weighted
restriction framework, and the lower construction is credited to
CHS/Shinkar–Tal. No stronger applicable public bound than the reviewed target
was located in this limited coverage.

The next useful work is compatibility with Boolean completion and other
derivatives, or a genuine quartic energy/potential envelope. Reducing the
isolated second-weight control ceilings below ten/twelve would be false,
as the checked sharp ternary examples show. Correct the two prose defects
above before using this packet as an externally reviewed statement.

Finished 2026-11-01 at 23:30 UTC, about 21 minutes after starting. Final
worker closeout at 23:30:03 UTC found no review workers or recorded child
PIDs remaining, and all 196 manifest hashes still matched. The audit is in
`receipts/closeout.json`; all SAT results are in `receipts/sat_attack.json`
and `receipts/sat_truth.json`. `receipts/REVIEW_RECEIPT.json` records the
overall result. The local retained review is below 1 MB. No other job was
changed, and the pod itself was not terminated. No commits, pushes, PRs,
posts, external messages or deletions were performed.
The overall verdict remains **PASS for the claimed bound; probability 99%**.
