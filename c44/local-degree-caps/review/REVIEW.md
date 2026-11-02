# Independent adversarial review of C44 round 4

**Overall verdict: PASS.** I found no mathematical gap or counterexample in the
claimed deduction of **C44 < 3.9819073803**. My subjective probability that this
upper bound is correct is **99%**, including the inherited dependencies. This is
a mathematical and computational review, not a proof-assistant formalization.

The suspiciously large gain survives scrutiny. My own implementation, importing
none of the target's programs, reproduced the claimed rational, the preceding
bound, and their exact difference **9/64**. The substantive minimum-support
structure is already covered by prior literature. I do not certify novelty.

Review scope: `../c44r4/PROOF.md`, its identical `frozen/PROOF.md`, `REPORT.md`,
and the retained baseline proofs and raw certificates. No target file was
modified. The independent code and receipts are in this review directory.

**1. Verdict per proof step.** Line numbers below refer to the target
`../c44r4/PROOF.md`; the frozen proof has the same lines.

| Exact lines | Step | Verdict | Reason |
|---|---|---|---|
| 10–15 | Definitions, finite extrema, CHS identity | PASS | Nisan–Szegedy bounds the relevant coordinate count; after relabeling this leaves finitely many functions. The weighted extremal identity is valid. |
| 22–38 | Corrected CHS duplication | PASS | All degree-d terms avoid the duplicated low-degree block and cancel in the selector difference. Every duplicated variable's weight is halved, two copies restore it, and the relevant selector adds positive weight. |
| 39–42 | Attribution of the correction | PASS | Chiarelli's thesis Proposition 8.5, Corollary 8.6, printed pp.116–117, gives this construction. Its footnote explicitly corrects the previous proof. |
| 44–50 | All local degrees of a variable-count maximizer equal d | PASS | Replacing a coordinate of local degree below d by an AND of two fresh bits raises the total degree by at most one on its terms, stays within d, and adds one relevant variable. This argument is used for count only. |
| 54–57 | Coefficient granularity | PASS | Integer bit Möbius coefficients and the substitution between bits and signs give denominators dividing 2^(d−1). The constant coefficient is covered as well. |
| 59–61 | Ternary derivative and minimum support | PASS | The derivative takes values 0,±1, its support density is the influence, and the nonzero polynomial support bound applies. |
| 64–65 | M² times influence is an integer sum of squares | PASS | This is precisely Parseval for the derivative with each Fourier coefficient multiplied by M. |
| 66–68 | Evenness from the all-plus input | PASS | The sum of the integer coefficients is M A_i(1), even for d≥2. Reducing squares modulo two proves the claimed parity. |
| 70–75 | Influence dichotomy and no-minimum case | PASS | The even integer energy is at least the even integer M; if it is not M, it is at least M+2. Summing influences then bounds the variable count. |
| 79–82 | Exactly M coefficients of size 1/M in the minimum case | PASS | The L1 coefficient bound and granularity force the sizes; Parseval forces the count. |
| 84–90 | Fourier masks form an affine (d−1)-cube | PASS | Fixed characters on the support give rank at most d−1; the M distinct masks give rank at least d−1. Both inequalities have the correct direction. |
| 92–98 | At most 2(d−1) controls | PASS | Each nonconstant affine coordinate is one with probability 1/2. Average mask size gives u/2+v≤d−1 and hence u+v≤2(d−1). Constant weight is unnecessary. |
| 102–104 | Active branches are dictators | PASS | If A=±1, requiring both B+A and B−A to be signs forces B=0 for every remaining assignment. |
| 106–112 | The controls hit every top-degree monomial | PASS | A top-degree monomial outside H cannot acquire canceling contributions from supersets containing H, since these would exceed degree d. Its coefficient vanishes on an active branch and therefore was zero originally. Terms involving i also meet H. |
| 114–116 | Restriction inequality | PASS | The inherited proof handles survival on both branches and on just one branch correctly; iterating proves the fixed-set inequality. See baseline/PROOF.md lines171–179. |
| 118–126 | Minimum-case budget and combination of cases | PASS | Control costs are at most (2d−2)/2^d for the chosen count maximizer. Active probability is 1/M, dictator potential is 1/2, and all other branches use a valid lower-degree cap. The cases combine by maximum. |
| 128–129 | Count bounds become universal weighted caps | PASS | This is a legitimate use of max D=R_d/2^d, including functions of smaller degree. A count bound alone would not suffice without this identity; the identity has been established. |
| 133–142 | Independent input caps and three arithmetic rows | PASS | The rows use inherited caps 5/4,31/16,5/2, respectively, rather than one another's conclusions. The inherited strict-cap proof supplies 31/16 without the new rows. |
| 151–155 | Inherited recurrence, block bounds, tail | PASS | The recurrence follows from maximum-monomial restrictions and the block-sensitivity drop. Raw spectral and Épi certificates passed my exact checks; the published Wellens inequality is used in its stated form. |
| 158–166 | Final rational and 9/64 gain | PASS | Reproduced independently at horizons96 and72. |

The matching explanatory claims in target `REPORT.md` lines38–56 pass the same
checks. Its lines15–16 correctly say that **B8≤32 is unproved**; the computation
uses **B8≤33**. Nothing in this review changes that conclusion.

**2. The critical algebra, independently checked.** Let
`z_S=M*a_(S∪{i})`. Then

    E_i = M² Inf_i = sum z_S²,
    E_i ≡ sum z_S = M A_i(1) ≡ 0 (mod 2).

This uses the actual Boolean function before averaging or symmetrization. It
does not impose granularity on an averaged polynomial. The restriction d≥2 is
essential to this parity argument and is present at line54. The dichotomy is
an implication; it does not assert that every energy above M is realizable.

For a minimum derivative A, equality in the coefficient estimate forces the
sign of A times each supported character to be constant on its support. If V
is the span of differences of Fourier masks, the support lies in an annihilator
coset of density2^(−rank V). Its actual density2^(−k) gives rank V≤k. Conversely,
the 2^k masks lie in a single coset of V, so rank V≥k. Thus the masks fill that
coset. This is an affine cube in the binary vector-space sense, not necessarily
a coordinate subcube. The ensuing average-weight argument remains valid.

The actual case budgets are:

| d | M | inherited lower-degree cap | no-minimum R bound | minimum-case potential | minimum-case R bound | conclusion |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 8 | 5/4 | 25 | 49/32 | 24 | R4≤25, D≤25/16 |
| 5 | 16 | 31/16 | 71 | 537/256 | 67 | R5≤71, D≤71/32 |
| 6 | 32 | 5/2 | 180 | 83/32 | 166 | R6≤180, D≤45/16 |

At the first excluded count, the no-minimum total-influence excesses are
1/16,1/16,5/512. The minimum-case potential excesses are 3/32,39/256,15/64.
All inequalities are strict with exact rational margins.

The obsolete claim that a single AND substitution preserves the entire D
potential is **FALSE**; it is explicitly not used by the target. Consider
the sign function

    f = (1+z)x1*x2/2 + (1−z)y1*y2*y3/2.

It has degree4 and D=1/2. Replacing x1 by the sign encoding of AND of two fresh
bits gives degree4 and D=7/16: x2's local degree increases too. Thus preserving
the replaced coordinate's combined weight does not preserve the whole potential.
Duplicating both low-local-degree variables x1,x2 simultaneously and adding a
selector instead gives D=9/16. Both values were checked by exact sparse Fourier
arithmetic and Boolean convolution in `symbolic_attack.py`. The target avoids
the invalid original substitution argument for D. The primary correction is in
[Chiarelli's thesis, Proposition8.5 and Corollary8.6](https://sites.math.rutgers.edu/~zeilberg/Theses/JohnChiarelli.pdf).

There is no circularity: c3 comes from R3≤10; the old c4=31/16 follows from
the inherited influence-equality exclusion; c5=5/2 follows directly from
D≤I/2≤d/2. Their proofs do not assume any of the three new count bounds or the
final C44 number. The inherited graph argument for the strict cap also checks
out; it is retained in baseline/baseline/PROOF.md lines65–101.

**3. Sanity attack against constructions and exact values.** The strongest
published general construction located is the CHS/Shinkar–Tal family

    Xi_1=x,
    Xi_d(s,t,x,y)=(s+t)Xi_(d−1)(x)/2+(s−t)Xi_(d−1)(y)/2.

The two recursive copies use disjoint variables. The count satisfies
`L_d=2L_(d−1)+2`, yielding `3*2^(d−1)−2`. These are verified lower witnesses,
not claimed exact values of R4,R5,R6. The construction and independent
Shinkar–Tal attribution are in
[CHS, section3](https://arxiv.org/html/1801.08564v3).

| d | Ordinary address function | Complete distinct-query decision tree | CHS witness | Proposed upper bound | CHS normalized weight |
|---:|---:|---:|---:|---:|---:|
| 4 | 11 | 15 | 22 | 25 | 11/8 |
| 5 | 20 | 31 | 46 | 71 | 23/16 |
| 6 | 37 | 63 | 94 | 180 | 47/32 |

The ordinary address function with d−1 address bits has `2^(d−1)+d−1`
variables and degree d. None beats CHS here. Disjoint ordinary compositions
Xi2∘Xi2 give 16 variables at degree4; Xi2∘Xi3 and Xi3∘Xi2 give 40 variables
at degree6. Those also fail to refute the caps. Other familiar recursive
block-sensitivity examples have fewer relevant variables at these degrees.

Exact known values checked are **R1=1,R2=4,R3=10**. I found no source proving
exact values for R4,R5,R6. In particular, do not silently promote 22,46,94 to
equalities. The degree-three statement applies to arbitrary Boolean functions,
despite its appearance in a paper about perfect colorings; section3 and step(i)
say this explicitly. The same paper supplies the exhaustive counts used to
cross-check my enumeration. See
[Krotov–Valyuzhenich, section2.1 and section3](https://arxiv.org/html/2311.05566v2).

Wellens2019 explicitly credits the same construction and its Table2 reports
**upper** weighted bounds 2,5/2,3 at degrees4,5,6. That table is not a source of
larger lower constructions. See
[Wellens2019](https://arxiv.org/html/1903.08214v2).

The live C44 table gives the lower bound3/2. CHS witnesses approach that value
as d grows; their finite values above are all below the proposed local caps.
The new global upper bound3.9819073803 also exceeds3/2. There is no contradiction
between a finite-degree cap below3/2, such as the quartic witness value11/8,
and the limiting lower bound. See the
[C44 table](https://teorth.github.io/optimizationproblems/constants/44a.html).

**4. Independent computation and falsification coverage.** All mathematical
computation ran on a rented pod in `the job directory`, under tmux or
nohup, with nice10 launch priority and one BLAS/OpenMP thread. The original
replay's nested nice commands give some children still lower priority. At most
three review computation workers ran concurrently, below the eight-core limit.
Only small source reads, file preparation, and receipt transfers ran locally.

`independent_bound.py` uses only the Python standard library and raw JSON inputs.
It checks every Épi power moment, recomputes each spectral lattice functional
with explicit binomial sums, validates the strict exclusion margin, computes the
published quadratic block bound by integer binary search, and evaluates the
recurrence by row induction with integers scaled by2^H. It imports no target
search or verifier code. The receipt is `receipts/independent_bound.json`.

    horizon96:
    157739602520732550180509661243 / 39614081257132168796771975168
    = 3.981907380278645604364490105637827330171324002522007098545109293752...

    horizon72:
    9402012975259575456909 / 2361183241434822606848
    = 3.98190738027864568838388973520160674102186249001533724367618560791015625

The horizon96 finite part is
`78869801260366275090254595175/19807040628566084398385987584`; its tail is
`470893/39614081257132168796771975168`. The old bound is exactly
`163310332697516761417555720251/39614081257132168796771975168`. Subtraction
gives9/64. The strict decimal claim follows by rational comparison, without
rounding.

Independent exhaustive C++ checks have passed for:

- Every truth table on one through four variables: 65,804 nonconstant tables.
- Every function of real degree≤3 on five variables: 807,980 tables including constants.
- Every function of real degree≤3 on six variables: 16,750,860 tables including constants.

The latter two enumerations split on the last coordinate, require both
restrictions to have degree≤3, and match their degree-three Fourier vectors.
These conditions are necessary and sufficient; this is exhaustive enumeration,
not random sampling. Both totals match the published independent classification
counts. Across all these runs the final receipt records **17,624,640 nonconstant
function instances**, **25,774,416 minimum derivatives**, and **494,973,424
single-coordinate restriction checks**. Instances on different ambient cubes
are counted separately.

For every relevant coordinate the code checks granularity, Parseval against
direct truth-table edge counts, energy parity, the influence dichotomy, and,
where minimum influence occurs, the full affine-mask rank, number of controls,
top-degree hitting property, active density, and dictator branches. It also
checks the single-coordinate restriction inequality directly. Receipt:
`receipts/exhaustive6.json`. No counterexample was found.

`symbolic_attack.py` independently checks Xi2 through Xi6, the three compositions
above, the mixed-degree correction example, and a nonhomogeneous minimum
derivative with five controls whose mask degrees are2 and3. It uses exact
Boolean convolution, rather than only random evaluation, and explicitly
restricts representative control sets on all assignments. Xi6 has94 relevant
variables and1,024 Fourier terms; its minimum derivative uses10 controls and
has32 active dictator branches among1,024 control assignments. Receipt:
`receipts/symbolic_attack.json`.

The original frozen packet was separately replayed in a review-owned copy.
It passed both original verifiers, the structural controls, all17 corruption
controls, and the18 static input/code hashes. That replay corroborates, but does
not replace, the independent implementation. Original target receipts were
not overwritten.

An additional independent enumeration checked **all43,046,721 ternary tables**
on four coordinates. For each nonconstant table it checked coefficient
granularity at its actual degree k, energy parity at M=2^k, the support
dichotomy, and the affine-mask/control conclusion whenever the minimum was
attained. It passed, including 512 minimum-support tables. The smallest observed
nonminimum energy gaps were2,2,8,16 at k=1,2,3,4, respectively. Receipt:
`receipts/ternary.json`. The gap2 cases show the parity step is substantive,
rather than merely an unused integrality observation.

These finite searches do not constitute exhaustive verification on25,71 or180
relevant variables; the universal written argument supplies that step.

**5. Prior art and novelty.** The following ingredients are already established:

- Nisan–Szegedy influence/support method and Fourier granularity for bounded real degree.
- CHS weighted local degree, its extremal identity, and the corrected simultaneous duplication proof.
- Wellens restriction inequality, block-budget recurrence, and analytic block-sensitivity inequality.
- The CHS/Shinkar–Tal lower witnesses and the degree-three classification.
- Minimum-support structure: **Valyuzhenich2023, Theorem2(2)** classifies minimum-support functions in U_[0,k](n). Its product forms imply that a minimum-support derivative depends on at most2k coordinates. This is a stronger existing structural result than the control-count conclusion used here. See [the primary paper](https://arxiv.org/html/2303.10995).

For the last point, each nonconstant block in that classification uses at most
twice its polynomial degree: an odd equality-indicator block of lengthm≥3 has
degree m−1; an even signed block of lengthm≥2 has degree m−1; a point-indicator
block of lengthr has degree r. The remaining singleton equality-indicator
blocks are constant and add no relevant variables. Summing gives≤2k.

Consequently, the minimum-support phenomenon and CHS correction are not new.
The precise parity-based packaging into the numerical caps25,71,180 was not
located in the bounded literature/code search. That is not an originality
certificate. The target itself disclaims novelty, so the prior-art omission
does not invalidate its theorem.

The direct GitHub refresh read the current raw table, open PRs and issues,
all43 visible open-PR diffs, repository metadata sorted by update, and the
named public result-repository READMEs. Only PR285 and PR294 actually patch
constants/44a.md. Main remains4.3576549226*; PR294 files4.1225323803*.
The initial EinsteinArena repository guess returned404; the actual
`togethercomputer/EinsteinArena-new-SOTA` repository was then read successfully.
The Towell repository concerns degree-five block-sensitivity exclusions and
does not furnish a relevant-variable construction beating these caps.

Recent primary sources checked include Potapov's2025 discrete-function paper
and Valyuzhenich's September2026 Hamming-graph paper; neither supplies a
contradicting binary construction. Indexed X/Reddit and broader web searches
found no additional applicable result. Authenticated global code search and
private community sources were unavailable. Raw web search caching was stale
for one table response; the live direct-download receipt and rendered table
agree. `PRIOR_ART.md`, `sources/LITERATURE_NOTES.md`,
`sources/public_audit.json.gz`, and `sources/extra_receipt.json` record coverage.

**6. Reproduction and next action.** In the authorized pod job directory, run:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
tmux new-session -d -s c44_review_reproduce 'nice -n 10 bash run_review.sh'
```

`run_review.sh` runs the independent bound checker, compiles/runs the two
enumerators, and runs the sparse symbolic checks, retaining receipts locally
to the job. Inputs are the three small raw JSON files in `inputs/`. No target
program is needed for those independent checks. The separate original replay
command is `bash original_frozen/jobs/reproduce_frozen.sh` in the pod job copy.

Next action: a human mathematical reader should check the short universal
argument and cited theorem statements before filing the improvement. Add the
Valyuzhenich minimum-support citation if the proof is prepared for publication.
Further counterexample search is less urgent than that review. B8≤32 and
sharp R4,R5,R6 values remain unresolved by this packet. **Final mathematical
assessment: PASS, with 99% subjective confidence in the stated bound.**

Completed 2026-11-01 at 20:35 UTC. All receipt files have been pulled back;
the retained review packet is approximately 5.4 MB. The final pod process
inspection at 20:34:32 UTC found no remaining process with a working directory
inside the review job. `receipts/final_review_receipt.json` records this check
and code/input/receipt hashes. The local process check also found no review
computation worker. The pod remains running; other jobs were left alone.
