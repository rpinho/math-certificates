# Adversarial review of C44 round six

**Overall mathematical verdict: PASS.** I found no error in the claim
`C44 < 2.1974348818`. A new exact optimizer, importing no target code,
reproduces every cap and the final rational

    174098727923678791596986402933
    / 79228162514264337593543950336
    = 2.19743488172319834634884256843302804933247045...

There is a **GAP in full-original KTA source coverage**, explicitly confined
to the unused 1974/1976 higher-range classification. It is not a gap in
the argument giving the bound. The second weight gap plus the exact energy
grid already gives the identical numerical result; a short independent
proof of that second gap is in [SOURCE_NOTES.md](SOURCE_NOTES.md).

This is an independent agent review of the supplied proof, not independent
human refereeing or proof-assistant verification. My subjective probability
that the stated bound is correct is **98%**. No novelty claim is certified.

**1. Exact line-by-line verdicts.** Here `P` means the reviewed
[PROOF.md snapshot](target_snapshot/PROOF.md), byte-identical to
`../c44r6/PROOF.md` at review. `R` means the
[target report snapshot](target_REPORT.md). Ranges below are source lines.

| Step | Exact lines | Verdict | Reason |
|---|---|---|---|
| Support induction, influences, finite extrema | P12–43 | PASS | The derivative support argument gives the stated factor two, Parseval gives total influence at most degree, and the relevant-variable bound makes both maxima finite. |
| Count-to-weight extremal identity | P45–62 | PASS | Simultaneously duplicating every coordinate of local degree below d cancels the selector's degree-(d+1) terms, preserves the old total weight, and adds a relevant selector. This is the corrected CHS argument. |
| All local degrees in a count maximizer | P64–73 | PASS | An AND substitution increases count and keeps degree at most d. This is correctly separate from the weighted-maximizer proof. |
| Base caps and exact cubic input | P75–83 | PASS | R3=10 is an unrestricted real-degree result, not just a perfect-coloring result. W3=5/4 follows from the identity. The endpoint controls below agree with R2=4 and R3=10. |
| Ternary derivative energy lemma | P87–118 | PASS | A nonzero derivative has support at least 2^(-(k-1)) and squared nonzero values at least 1/4. Summing Fourier energies gives h<=k p 2^(k+1), with no binary affine change of variables. |
| Weighted restriction inequality | P122–137 | PASS | For each outside coordinate the expected weight cannot fall. The one-surviving-branch factorization gives exact compensation for averaging. Iteration concerns outside weights, so growing costs of successively fixed controls are not incorrectly charged at their original values. |
| Active branches become dictators | P139–144 | PASS | If A_i=+/-1, Booleanity of both x_i branches forces B=0 for all outside inputs. The active fraction is exactly the influence. |
| Controls meet every top-degree monomial | P146–152 | PASS | A degree-d coefficient disjoint from H cannot receive contributions from strict supersets. It survives restriction, contradicting B=0 on an active assignment. Terms involving i are handled separately; d>=2 is essential and respected. |
| Joint scalar inequalities | P154–169 | PASS | The same minimum-influence derivative supplies both the control budget and lambda<=d M/N. The factors in N<=2^d c+floor(2(d-1)lambda)+(1-2c)lambda are correct. |
| Fourier lattice and energy parity | P173–191 | PASS | Integer bit interpolation gives Fourier coefficients in M^-1 Z. Evaluation at the all-plus input and z^2=z mod 2 force an even sum of squares, hence lambda in (2/M)Z. |
| Binary support bridge | P193–197 | PASS | Reduction modulo two is applied to the integer-valued A_i itself. Its two nonzero signs both reduce to one; no degree-2k squaring error occurs. |
| Below-two spectrum and finite low list | P199–218 | PASS | The original 1970 publisher abstract's two forms yield 2-2^(-j). The energy parity excludes j=k and integrality excludes j>k. Relaxing parameter-dependent restrictions is safe. |
| Treatment of weights at and above two | P220–226 | PASS | Every high energy-grid value is allowed. The defective KTA final-table gap is not imposed. |
| Excluding all counts at once | P230–250 | PASS | For N>=n the influence interval shrinks to [1,dM/n]. Within each floor cell the budget decreases, so the first grid point is the correct maximizing representative. No endpoint-floor substitution is made. |
| Induction and displayed caps | P252–267 | PASS | Independently recovered 24,54,119,254,528,1083,2199,4439,8928 at degrees 4 through 12. Each uses only the preceding established cap. |
| Scalar witnesses and collapsed envelope | P268–284 | PASS | My optimizer avoids the target's collapsed-envelope shortcut entirely and gives the same largest feasible integer. The stated envelope inequality also has the correct sign and k>=3 range. |
| Numerical ablations | P286–292; R65–69 | PASS | The three reported numbers are correct. Additional separated ablations show that the grid and the higher gaps can independently recover the last improvement; the higher gaps are not necessary when the grid is retained. |
| Lower construction | P296–308 | PASS | Exactly one summand is active; all Fourier masks have size d and all variables remain relevant. L_d=3*2^(d-1)-2 gives R_d>=2M for d>=2. |
| Elementary tail inequality | P309–315 | PASS | It uses the actual W_(d-1), not a computed cap in a negative coefficient. The positive multiplier is at most 2d-2, and lambda<=d/2 follows from the lower construction. |
| Infinite tail and final rational | P317–343 | PASS | The tail is (H^2+3H+4)/2^H. At H=96 its numerator is 9508. It bounds all omitted degrees independently of block sensitivity. The final strict decimal comparison and round-five gain are exact. |
| Universal block recurrence | P347–360 | PASS | The cap is universal for D, and each restriction's exact degree j<=d is included. A top monomial supplies the additional disjoint sensitive block at every outside assignment. |
| Inactive block inputs | P362–374; R75–95 | PASS | Independent integer rows with B_d=d^2 and with the inherited B_d reach every cap. Saturation thresholds match; B8=32 changes nothing. |
| Meaning and limit of scalar relaxation | P376–404; R113–123 | PASS | Optimality is for the displayed scalar constraints, with the supplied exact cubic base. Feasible scalar points are not Boolean witnesses. Monotonicity, bounded increments, and the tail interval are justified. |
| Related ternary prior art | P406–412 | PASS | Potapov's root-of-unity encoding is related, but can double the degree and loses the small-support energy p. It does not contradict this real-energy calculation. |

The stronger interpretation “these caps are exact Boolean maxima” would be
**FALSE**, as would “scalar feasibility supplies Boolean functions.” The
target explicitly avoids both claims. Likewise the inference “a single AND
substitution preserves D” would be false; the target uses it only for count.
No such false step was found in the written argument.

**2. The main places I tried to break the proof.**

The new control lemma is not restricted to minimum-support derivatives.
For any relevant control j, Delta_j A has real degree at most k-1 and
values in {0,+/-1/2,+/-1}. Thus its energy is at least 2^(-(k+1)), while
the total derivative energy is at most k E A^2. Both facts hold for an
arbitrary signed ternary polynomial. There is no assumption that the
binary support's affine normal form preserves real degree.

The top-monomial argument also works above minimum influence. All that it
needs is one active assignment and the full relevant-coordinate set of
A_i. On such an assignment B vanishes identically. A degree-d monomial
disjoint from that coordinate set cannot be canceled by restricting it,
since cancellation would require a larger Fourier mask. Hence it cannot
exist. This is the substantive extension beyond round five.

The recurrence's domain is all Boolean functions of the stated exact degree
and bounded block sensitivity. An arbitrary restricted function need not
be a count maximizer and need not have uniform local degrees. That is not
a problem: the corrected identity first transfers the count ceiling to
the universal bound D(g)<=W_d=R_d/2^d for every degree-at-most-d g. The
recurrence then uses that universal bound. Uniform local degree is invoked
only where justified by the extremal reductions, or for coordinates of an
actual maximum monomial. This distinction survives all restrictions.

As an extra check, the count inequality can itself be extended without a
uniform-local-degree assumption: outside H, each original weight is at
least 2^-d, and its average restricted weight cannot decrease. Therefore
(N-h)2^-d<=E D(f_alpha) for any such f. My functional checker tests this
stronger statement on mixed local degrees. The identity is still needed
to turn a count ceiling into the universal D cap.

For the tail, inactive block inputs do not license using the inherited
cubic tail without justification. The target instead supplies a new proof:
R_d>=2M bounds the extremizer's least influence by lambda<=d/2. With the
actual W=W_(d-1),

    W_d <= W + lambda*(2d-1-2W)/2^d
        <= W + d(d-1)/2^d.

Summing from d=H+1 gives (H^2+3H+4)/2^H. No block certificate or block
theorem remains in this chain. The final cap at H bounds every smaller
degree because the certified caps are nondecreasing.

**3. Known-degree controls and the gap1 comparison.**

At d=2, M=2, c=W1=1/2. The minimum case lambda=1 has h<=2 and budget
2+2=4. Influence excludes any N>4. This endpoint needs no interior
Kasami–Tokura theorem. The method recovers the exact R2=4.

At d=3, M=4, c=W2=1. Lambda=1 has h<=4 and budget 8+4-1=11. The next
count N=12 allows only lambda<=1, whose budget remains 11. Therefore the
relaxation gives R3<=11, consistent with the known exact R3=10. It does
not prove 10; that exact external result is correctly supplied as the
base of the d>=4 iteration. Scalar optimality is not claimed for replacing
this externally sharpened base by a fresh d=3 scalar computation.

The two proofs do not assert incompatible values:

| d | CHS lower witness | Round-six count ceiling | gap1 claim |
|---:|---:|---:|---:|
|2|4|4 by the endpoint control|not at issue|
|3|10|11 by scalar constraints; exact input 10|exact input 10|
|4|22|24|22 exactly|
|5|46|54|53 as an upper bound|
|6|94|119|round-five cap 128 retained|

I read all of `gap1/PROOF.md`. Its extra cubic inequality D(g)<=1+E3(g)/4
and equality-case arguments are not inputs of round six. I independently
checked the finite premise on all 761 pinned author representatives and
recovered exactly lines 700,716,757 with signatures (5/4,1), (9/8,1/2),
and (1,0). See [extra receipt](receipts/extra.json). This verifies that
finite premise; it does not independently regenerate the classification
or turn this report into a full separate certification of gap1.

For gap1's exact locations: lines 36–51 give the cubic premise; 56–104
give the count reduction; 122–150 handle the two five-control types;
152–210 handle the six-control equality cases; 214–221 give attainment;
236–245 give R5<=53 and the older global recurrence. Nothing there
contradicts a weaker R4<=24 or R5<=54 ceiling. Its worse global constant
comes from retaining older higher-degree caps, not from a larger lower
bound on C44.

As a compatibility diagnostic, inserting only gap1's c4=11/8 into my
round-six optimizer yields R5<=53, R6<=117 and R7<=250. That calculation
is conditional on gap1 and is not substituted for the bound under review.

**4. KTA audit, omission, and the smaller sufficient dependency.**

Every relevant use is separated in [SOURCE_NOTES.md](SOURCE_NOTES.md).
The original 1970 publisher abstract's two forms give the required
below-two weight spectrum; [Carlet 2024, p.10613](https://www.aimspress.com/aimspress-data/math/2024/5/PDF/math-09-05-518.pdf)
states it explicitly. The integer-coefficient reduction and the energy
parity are separate real-degree arguments, so the normal forms are never
used to infer coordinate controls.

For the target's `KTA_AUDIT.md`, lines 25–33 are **PASS** against
[Klein–Storme, Lemma 1](https://backoffice.biblio.ugent.be/download/2140143/2939938):
order at least four, a strict 2.5-minimum threshold, and two nonparallel
affine hyperplanes. Lines 35–40 are **PASS as an attribution** to
[Krotov's public discussion](https://www.researchgate.net/post/What_is_the_next_admissible_weight_of_codewords_of_the_Reed-Muller_code_RMm_r_after_2d_where_d2m-r_is_the_code_distance).
It identifies the issue after equation (23), a missing sequence, and the
codimension condition. Inspecting the original defective table and all
preprint proofs remains **GAP**; full text was not recovered.

Lines 43–56 are **PASS mathematically**: direct enumeration gives weight
528 in RM(2,10), normalized weight 33/16. The order-four lift on twelve
variables also has weight 528 and the same minimum 256. The blanket gap
(2,17/8) is therefore false. These indicators have real degree ten/twelve,
not two/four; they are not admissible derivative witnesses merely because
they are low binary-degree codewords. The target makes that distinction.

Lines 58–63 are **PASS** against
[Lou–Wang, section 2 equation (5)](https://arxiv.org/html/2610.36687):
the quoted list is specialized to codimension seven, whereas the example
has codimension eight. There is no conflict and no unrestricted extension
of the newer paper in the accepted bound.

I separated the two numerical refinements that the target's reported
variants change together:

| Allowed coding weights | Energy grid? | Recomputed global upper bound |
|---|---|---:|
|all lambda>=1|no|2.295288788242174...|
|all lambda>=1|yes|2.295288788242174...|
|1 or lambda>=3/2|no|2.210899804709738...|
|1 or lambda>=3/2|yes|2.197434881723198...|
|full below-two list; all lambda>=2|no|2.197434881723198...|
|full below-two list; high energy grid|yes|2.197434881723198...|

The last three variants give the same caps through degree 96, checked by
exact equality in [ablation.py](ablation.py). Thus the target's reported
numbers are correct, and higher weights alone can supply the reported
last improvement; they are redundant when the grid is retained. This is
a simplification opportunity, not a counterexample to the bound. The
second gap needed by the simpler route has an elementary induction proof
in SOURCE_NOTES, eliminating dependence on the full low-weight
classification for this numerical conclusion.

**5. Independent computation and what the finite tests establish.**

[independent_scalar.py](independent_scalar.py) optimizes in the opposite
direction from the target's count-exclusion search. At each fixed lambda it
maximizes

    min(floor(F_d(c,lambda)), floor(dM/lambda)).

Both quantities are nonincreasing within a floor cell. I enumerate the
first admissible lattice point in every occupied high cell and every
allowed low value, then take the largest count directly. Through degree
14 this is separately checked against every individual allowed energy-grid
point. Only after deriving all caps does the program read the target
packet for comparison. No target verifier or generator is imported.

The finite cap is

    c96 = 174098727923678791596986393425 / 2^96,
    tail = 9508 / 2^96.

Their sum is the headline rational. The exact difference from round five is
76852852570035861934916069377/2^96, approximately 0.970019373555447258.
The scalar feasible points do not assert Boolean attainability.

[functional_attack.cpp](functional_attack.cpp) independently checks every
Boolean truth table on one through four inputs, plus all 761 published
cubic representatives padded to ten inputs: 66,573 functions total. It
tests all relevant derivatives, not just those of minimum influence:

    266,329 derivatives; 241,358 above minimum influence;
    266,308 energy and grid checks;
    2,143,114 complete control branches;
    374,293 top-monomial incidence checks;
    3,922 mixed-local-degree control checks.

It checks integer interpolation, the binary support bridge, the weight
list, active dictators, every branch's degree drop, the weighted
restriction inequality, and the scalar count budget. It recovers maxima
R1=1,R2=4,R3=10 and W1=1/2,W2=1,W3=5/4 on these inputs. Coverage of
all larger-cube cubic functions relies on the published classification,
not on a new exhaustive enumeration of 2^1024 truth tables.

[sparse_attack.py](sparse_attack.py) checks 42 exact sparse Boolean
polynomials through degree six: CHS witnesses through 94 variables,
distinct-query decision trees, mixed-degree selectors, overlapping cubic
branches and products. Integer XOR convolution verifies Booleanity. It
checks 719 derivatives, 58,458 control branches, 235 complete restriction
means, 13 corrected duplications and 13 count-increasing AND substitutions.
For 86 large control sets the branch checks are sampled, explicitly
recorded as such; their means are not represented as exhaustively checked.

[independent_recurrence.py](independent_recurrence.py) uses integer-scaled
rows and all exact-degree columns. It recovers the saturation rows
1,2,3,4,6,8,10,13,16,20,24,28,33,39 at degrees 1 through 14. Both the
inherited B_d and B_d=d^2 reach all caps. Setting B8=32 leaves every
terminal column unchanged. The new elementary tail is checked separately.

The entire copied frozen target replay also passes: both target checkers,
all inherited raw block certificates, all 43,046,721 four-input ternary
tables, Boolean controls, and eleven corruption rejections. These are
corroborating finite checks, not replacements for the universal proofs.
The static manifest is checked before and after the replay. The accepted
fresh-run ledger and process audit are in `receipts/`.

**6. Why no comparable bound in the serious literature?**

This remains a reason to demand scrutiny; a repository search cannot
explain what CHS, Wellens, Filmus or Ihringer knew or chose to pursue.
The located published binary bound is still
[Wellens's 4.394](https://arxiv.org/html/2005.00566), and the
[official table](https://teorth.github.io/optimizationproblems/constants/44a.html)
lists an unrefereed 4.3576549226. The inspected PR294 and public C44
repository contain 3.9819073803. No located public source states the new
2.197 bound. Detailed coverage and limitations are in PRIOR_ART.md.

There is a concrete mathematical change, not merely inserting old coding
tables into the same recurrence. The old method chooses a top monomial
or a collection of disjoint top monomials. The new method fixes every
variable on which a carefully chosen derivative depends. The real ternary
energy calculation bounds that set, and Booleanity makes it a top-degree
hitting set with a positive fraction of dictator branches. Round five
uses this control idea only in the minimum-influence case; round six
extends it to every influence and optimizes the influence/count tradeoff.

Numerically, the elementary control method without any coding gap already
gives 2.2952887883. Most of the fall from 3.167 therefore comes from that
new universal control argument, rather than third/higher Reed–Muller
weights. [Wellens 2019, Table 2](https://arxiv.org/html/1903.08214v2) uses
the elementary d/2 caps through degree seven; the proposed proof instead
propagates sharper count-to-potential caps from small degrees.

[Filmus–Ihringer](https://www.cs.utoronto.ca/~yuvalf/const_degree.pdf)
transfers the optimal cube bound to thick slices; it does not supply a
contradictory cube lower construction.
[Potapov](https://arxiv.org/html/2410.21937) supplies related ternary
energy prior art but uses a different output encoding whose degree can
double. These comparisons make the result plausible; they do not prove
that the combination is new or establish why it was previously missed.

The sharpest remaining external review would focus on P87–118 and
P139–169, the bridge from general ternary relevance to the common
derivative's control/count inequalities. I have checked those deductions
directly and found no missing hypothesis. Expert human scrutiny or a
formalization would provide a different kind of assurance from further
replaying the same finite certificate.

**7. Reproduction and compute discipline.**

All mathematical computation ran on the authorized `math-cpu-6` pod under
`/root/os/math_review_c44r6_1101`. It ran under nohup, at nice 10 or lower
priority, with BLAS/OpenMP thread counts one. The target wrapper adds its
own niceness and therefore ran at nice 19. No more than one mathematical
worker plus the three-thread read-only network audit ran concurrently;
the ten-core budget was respected. Local actions were source reading,
code/file preparation, small comparisons and receipt transfers.

With the retained review directory populated on the authorized pod, run:

```sh
ssh math-cpu-6 'cd /root/os/math_review_c44r6_1101; nohup nice -n 10 env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 run_review.py > receipts/run.log 2>&1 < /dev/null & echo $! > receipts/run.pid'
```

The runner records every direct child PID and exit status. It executes the
new scalar optimizer, full copied target replay, C++ functional attack,
independent recurrence, sparse attacks, catalogue/KTA checks and six
ablations sequentially. Python's standard library and g++ suffice.
Public-source refresh is separate: `python3 source_audit.py final`, under
the same nohup/nice/thread wrapper. `python3 final_audit.py` verifies all
receipts and audits live processes after those commands finish.

The first replay launch preceded completion of the snapshot upload and
failed because its script was not yet present. That failure is preserved
in `receipts/startup_ledger.json`; it is not confused with a passing
mathematical replay. The corrected final runner uses a memory ceiling
compatible with the target wrapper. Its final eight-stage ledger says PASS
and ended at 21:59:40 UTC on 1 November 2026.

No original job files were modified. No commits, pushes, PRs, posts or
messages to other people were made. The pod was not terminated. Source
and receipt artifacts are below the 50 MB retention limit. The final
process audit at 22:03:20 UTC found no remaining review workers. The final
public refresh made 74 successful requests with no errors and confirmed
the same live values. Receipts were pulled into this directory; the audit
is `receipts/final_review_receipt.json`. All 18 review code/receipt hashes
were checked again after transfer and match. Both reviewed proofs still
match their saved snapshots. Work completed at 22:06 UTC on 1 November
2026, about 23 minutes after starting. The retained directory is about
11 MB. See `STATUS.md` for completion state.

**Overall verdict: PASS for the bound; GAP only in unused full-KTA source
coverage. Subjective probability that C44 < 2.1974348818 is correct: 98%.**
