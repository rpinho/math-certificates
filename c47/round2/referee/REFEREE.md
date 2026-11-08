# Clean-room referee: C47 ≥ 1.7040280575

The lower bound holds. The recomputed by its own checks periodic ratio is exactly the claimed fraction, and the supplied finite L1 construction proves the printed decimal strictly. The earlier half-open-cell wording issue is fixed. There are no mathematical caveats or unchecked items in (a)–(d).

I read only the supplied producer proof, report, prior-art note, certificate and finite receipt, and two earlier referee reports. No producer or earlier referee code was read, copied, imported, or run; no Tomar or Doldrums checker was used. The new checker is [independent_check.py](independent_check.py). Its mathematical comparisons use Python integers and `fractions.Fraction`; decimal arithmetic is only for display. Copies of the two supplied JSON inputs are retained in `sources/`, with the same line numbering as the originals.

## (a) Definition match and the precise reduction

The [live official table](https://teorth.github.io/optimizationproblems/constants/47a.html) was fetched on 2026-11-08. Its definition follows verbatim from the [raw source](https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/47a.md), retained at `sources/47a.md:5–28`. Attribution: teorth/optimizationproblems contributors; the repository's Apache-2.0 license is retained at `sources/table-LICENSE`.

> In $\mathbb{R}^d$ ($d\ge 1$), let $M_d$ denote the **centered Hardy–Littlewood maximal operator associated to cubes**, defined by
>
> $$
> M_d f(x)\ :=\ \sup_{r>0}\ \frac{1}{\lvert Q(x,r)\rvert}\int_{Q(x,r)} \lvert f(y)\rvert\,dy,
> $$
>
> where $Q(x,r)$ is a closed $\ell_\infty$ ball of radius $r$ and center $x$ in $\mathbb{R}^d$, that is, a closed cube centered at $x$, with sides parallel to the coordinate axes, and sidelength $2r$, and $\lvert\cdot\rvert$ denotes Lebesgue measure.
> <a href="#Ald2011-def-Md">[Ald2011-def-Md]</a> <a href="#Ald2011-def-Qxr">[Ald2011-def-Qxr]</a>
>
> Let $c_d$ be the smallest constant such that for every $f\in L^1(\mathbb{R}^d)$ and every $\alpha>0$,
>
> $$
> \alpha\,\bigl\lvert\{x\in\mathbb{R}^d:\ M_d f(x)\ge \alpha\}\bigr\rvert\ \le\ c_d\,\lVert f\rVert_1.
> $$
>
> <a href="#Ald2011-def-cd">[Ald2011-def-cd]</a>
>
> We define
>
> $$
> C_{47}\ :=\ c_2,
> $$
>
> the optimal weak-type $(1,1)$ constant of the centered Hardy–Littlewood maximal operator associated to axis-parallel squares in $\mathbb{R}^2$.

Thus C47 concerns integrable functions on the entire plane, with **centered axis-parallel squares**. It is not a torus constant or a constant for uncentered rectangles. Rectangles here describe sets of centers of admissible squares. A periodic atomic measure alone is not an L1 function; the reduction below is essential.

The exact result applied is **Tomar, Lemma 6.2**, *Bounds for the weak type (1,1) constant of the centred maximal operator over squares*, Section 6, `lem:periodic`, [v5, Lemma 6.2, Section 6](https://doi.org/10.5281/zenodo.23716077). I read the statement and proof directly (`sources/tomar-main.tex:302–317`), not just the producer's attribution. In explicit notation, its statement is:

Let μ be a positive atomic measure with finitely many atoms in each bounded set, periodic under Λ = Px Z × Py Z, and with finitely many atoms in C = [0,Px) × [0,Py). Given λ > 0, finitely many finite atom sets Sᵢ, and radii

\[
0<r_i<\sqrt{\mu(S_i)/(4\lambda)},
\]

choose rectangles \(R_i\subseteq\bigcap_{p\in S_i}Q(p,r_i)\). With \(U_{\rm per}=\bigcup_{i,t\in\Lambda}(R_i+t)\), the conclusion is

\[
c_2\ge\frac{\lambda|U_{\rm per}\cap C|}{\mu(C)}.
\]

The preceding Lemma 6.1 gives the containment observation. The strict radius inequality in Lemma 6.2 permits smearing while retaining the level λ. The statement imposes no symmetry, grid arrangement within the cell, or exhaustive witness enumeration.

Tomar credits Lin's truncation and smoothing argument. The relevant lower-bound source is Lin's [written proof, Sections 5–6](https://github.com/CoolRmal/centered-maximal-constant/blob/main/docs/PROOF.md#5-from-the-lattice-to-integrable-functions), read directly and retained at `sources/lin-PROOF.md:119–150`: truncate the lattice, replace each mass by a square indicator of the same integral, count disjoint translated good sets, and pass to the limit. Lin proves the particular lattice ratio Φ through finite-function bounds approaching Φ. We use Tomar's general finite-atom lemma, not Lin's special lattice hypotheses. Lin's manuscripts *c₂ < 4* and *Two partial balayage principles for weak-type estimates* were also fetched; their introductions concern upper bounds. They are not the lower-bound lemma invoked here. No Lean formalization was executed or assumed as a substitute for the argument in (c).

Every hypothesis is satisfied:

| Hypothesis | Referee finding |
| --- | --- |
| Positive periods | Px = 164412227795641/50000000000000 and Py = 137238469612441/50000000000000. |
| Positive atomic measure | All 98 weights are positive; the minimum is 953391807/20000000000000. A finite set repeated at positive periods is locally finite. |
| Fundamental cell and mass | All 98 locations lie in [0,Px) × [0,Py); all are in fact strictly interior. The mass is the sum of the 98 listed weights. |
| Periodicity | Define μ by all integer lattice translates of the 98 atoms. Reindexing proves invariance under Λ. Minimal periods are unnecessary. |
| Level | `measure.lam` is exactly 1. |
| Finite witness family | 1500 bounded boxes and rectangles; Sᵢ comprises exactly the periodic atoms in closed box Bᵢ. Each Sᵢ is finite. |
| Strict radius bound | All 1500 radii are positive, and μ(Bᵢ) − 4rᵢ² > 0 exactly. |
| Containment | Each rectangle lies inside the closed cell, and Q(x,rᵢ) contains Bᵢ for every x in that rectangle. |
| Area normalization | Nonzero lattice translates of the closed-cell rectangles can meet C only on cell boundaries. Those have zero Lebesgue area, so the ordinary union area A equals the lemma's periodic area in C. |

These findings use `independent_check.py:55–104`. The full periodic-to-finite implication is also established directly in (c).

## (b) Exact masses, containment, union area, and ratio

Input: `sources/final.json`, copied unchanged to [sources/final.json](sources/final.json). Its SHA-256 is `bc342d18f9fe219828856bcaa9531669a1051c2685394e41dfbeb3e794e818eb`. The measure is at lines 3–500 and the witness array starts at line 502.

For each base atom (xⱼ,yⱼ,mⱼ) and closed box B = [a,b] × [c,d], the checker derives all required integer translates directly:

\[
\left\lceil\frac{a-x_j}{P_x}\right\rceil\le k\le
\left\lfloor\frac{b-x_j}{P_x}\right\rfloor,\qquad
\left\lceil\frac{c-y_j}{P_y}\right\rceil\le l\le
\left\lfloor\frac{d-y_j}{P_y}\right\rfloor.
\]

It sums mⱼ over every resulting (j,k,l), including atoms on box edges. Thus no atom is omitted by a fixed neighborhood, and the producer's `reach = 6.0` is irrelevant. There are **90,257 atom incidences** across the 1500 witnesses. Different witnesses may use the same atom; their masses are not added together in any single-square estimate.

For R = [u,v] × [s,t], the maximum of all endpoint distances between [a,b] and [u,v], and between [c,d] and [s,t], is exactly the greatest sup-distance between B and R. The checker verifies this maximum is ≤ r, as well as the corresponding condition separately for every selected atom. Equivalently,

\[
u\ge b-r,\quad v\le a+r,\quad s\ge d-r,\quad t\le c+r.
\]

All 1500 boxes satisfy the condition; all rectangles have positive area and lie within [0,Px] × [0,Py]. Containment equality is legitimate for closed squares.

The minimum strict mass slack is

\[
\delta=\min_i\{\mu(B_i)-4r_i^2\}
=\frac{2797727194076023938027}{24178516392292583494123520000000000000}>0.
\]

It occurs at witness **297** (zero-based), `sources/final.json:4959`; the corresponding row is `witness_results.tsv:299`. The radius range is

\[
\frac{15182753187}{4398046511104}\le r_i\le
\frac{783931254261799}{281474976710656}.
\]

[witness_results.tsv](witness_results.tsv) records the source line, counted mass, radius, exact slack, smeared slack, and required cell-offset range for every witness. The radius-grid denominator D = 281474976710656 is consistent with every radius, although that grid choice is not a lemma hypothesis.

To compute the union area, I partitioned at the **2265 distinct x endpoints**, giving 2264 vertical slabs. Within each open slab, the active rectangles are constant. Sorting and merging their y intervals gives the covered height; summing slab width times covered height gives the area. Boundary lines have area zero. This direct exact integration, implemented at `independent_check.py:30–47`, counts overlaps only once.

The obtained by its own checks quantities are

\[
m_0=\mu(C)=\frac{528259641268587}{100000000000000},
\]

\[
A=\frac{5313661371249717212564607254255950500629401796019}
{590295810358705651712000000000000000000000000000}
=9.00169250400194986375655056785581354656\ldots.
\]

They agree exactly with the producer's mass and area in `../README.md:7`. The ratio comparison is:

| Quantity | Exact value |
| --- | --- |
| Claimed q (`../README.md:1`) | 1771220457083239070854869084751983500209800598673/1039431510074799032049552767561236480000000000000 |
| Recomputed A/m₀ | 1771220457083239070854869084751983500209800598673/1039431510074799032049552767561236480000000000000 |
| Difference | 0 |

\[
q=1.704028057563676727063841350116855506575603324931662133\ldots.
\]

See `exact_results.json:67–81`. No sampling, binary floating-point comparisons, or numerical tolerance enters this result.

## (c) Finite instance and the L1-function bound

All exact numeric fields of `sources/final-finite.json:3–11` agree with the referee’s own computations. In particular,

\[
h=2,\quad N=214084879817,\quad
\varepsilon=\frac{932575731358674646009}
{847236695290453741755432960000000000000}>0.
\]

This ε is a **radius**, approximately 1.10072632186801655 × 10⁻¹⁸. Define, using the listed atom coordinates pⱼ and weights mⱼ,

\[
f(z)=\sum_{k,l=0}^{N-1}\sum_{j=1}^{98}
\frac{m_j}{4\varepsilon^2}
\mathbf1_{Q(p_j+(kP_x,lP_y),\varepsilon)}(z).
\]

This is an explicitly specified finite, nonnegative, bounded, compactly supported L1 function. Each smeared square is retained in full, even outside the original block. The integral of each summand is mⱼ, and overlap does not change the integral of their sum. Consequently

\[
\|f\|_1=N^2m_0
=\frac{24211373250385585233621505566014750043}{100000000000000}.
\]

The number of atom contributions is exactly **98N² = 4491568905093414727441922**, as claimed. Expanding that many terms is unnecessary: the formula specifies them all and the translation argument applies uniformly to every inner cell.

**Retention.** Set Rmax = 783931254261799/281474976710656. The strict inequality h min(Px,Py) > Rmax holds; its exact margin is `exact_results.json:77`. A center in an inner cell has more than Rmax clearance from the exterior of the block, so all selected atoms are retained. Directly, all selected atoms have offsets k ∈ {−1,0,1} and l ∈ {−1,0,1,2}. Translating to any cell with indices in {2,…,N−3} places every selected atom in a cell indexed between 0 and N−1. The checker verifies these index inequalities for every incidence (`independent_check.py:95–97`). This establishes the boundary assertion in `sources/producer-proof.md:12` including the upper-cell endpoint convention.

**Smearing.** The checker confirms ε ≤ 1/2 and

\[
\delta-4(2R_{\max}+1)\varepsilon
=\frac{8393181582228071814081}{96714065569170333976494080000000000000}>0.
\]

For each radius,

\[
4(r_i+\varepsilon)^2-4r_i^2
=8r_i\varepsilon+4\varepsilon^2
\le4(2R_{\max}+1)\varepsilon<\delta.
\]

Hence μ(Bᵢ) > 4(rᵢ+ε)². The checker also verifies this last inequality separately for all 1500 witnesses, without relying only on the common bound. If x belongs to its rectangle, every smeared square corresponding to an atom in Bᵢ is contained in Q(x,rᵢ+ε), by the triangle inequality in the sup norm. Therefore Mf(x) > 1 on every retained rectangle. This validates `sources/producer-proof.md:19–23`.

**Area and finite ratio.** The (N−4)² inner cells have witness unions of area A each, overlapping only on null boundaries. At α = 1, the table's defining inequality gives

\[
c_2\ge\frac{|\{Mf\ge1\}|}{\|f\|_1}
\ge q\left(\frac{N-4}{N}\right)^2
=\frac{81179170702072811560461937774649547472268267876630428381100034109236137}
{47639573975778160894755636560089704255253920609263650078720000000000000}.
\]

This is exactly the fraction in `sources/final-finite.json:11`. Its value is

\[
1.704028057500000000001029154249129824567183295051365907\ldots,
\]

and its excess over 1.7040280575 is exactly

\[
\frac{49028469983906704438445371567674232099070422836137}
{47639573975778160894755636560089704255253920609263650078720000000000000}
>0.
\]

This excess is about 1.02915424913 × 10⁻²¹ (`exact_results.json:91–94`). Thus the specified finite instance proves the decimal bound. Keeping h and ε fixed and letting N increase gives the stronger conclusion c₂ ≥ q, as in `sources/producer-proof.md:27`. The floating display in `final-finite.json:12` rounds away this tiny finite excess and was not used as evidence for a strict inequality.

## (d) Periods, duplicates, boundaries, decimal rounding, and scope

**The half-open-cell issue is fixed.** `sources/producer-proof.md:5` explicitly defines C = [0,Px) × [0,Py), defines Cbar separately, and identifies μ(C) with the supplied mass sum. Line 10 uses μ(C) in the ratio and reserves the zero-area boundary argument for rectangle unions. Lines 12 and 17 use precisely N² copies of each base atom and the same half-open-cell mass. Those are the correct conventions throughout the proof. The earlier wording caveats at `the earlier referee report, section on cell boundaries` and `the subsequent referee report, section on cell boundaries` do **not** apply to this proof.

**Atoms and periods.** Every supplied atom lies strictly inside its fundamental cell, and all 98 locations are distinct. Thus there are no outside-cell atoms, boundary atoms, duplicate locations, or duplicate locations modulo the periods. Indeed, for this particular certificate even μ([0,Px] × [0,Py]) happens to equal μ(C), because no atom lies on any cell boundary (`exact_results.json:11–14`). The half-open convention remains the appropriate general formulation. Both periods are positive; the proof requires periods, not proof that they are the smallest periods.

**Other boundary effects.** Witness boxes are closed, so atoms exactly on their edges are included. Geometric equalities in square containment are allowed; mass inequalities are strict. Shared rectangle and cell edges have zero Lebesgue area, but no such null-set argument is used to discard atomic mass. Smearing is never cropped to a cell or the finite block. These distinctions prevent the previous atomic-boundary ambiguity and loss of finite mass.

**Rounding.** The printed 1.7040280575 is the downward truncation of q at ten decimal places, checked by integer division. The exact periodic excess is

\[
q-1.7040280575
=\frac{66187596568589438500860688897262998673}
{1039431510074799032049552767561236480000000000000}>0.
\]

Ordinary rounding to nearest at ten decimal places would produce **1.7040280576**, which is greater than q and is not justified by this certificate. The producer's chosen decimal is valid.

**Scope and novelty.** All requested mathematical checks (a)–(d) are complete. This checks a lower bound, not the exact maximal-function level-set area, optimality of the measure, completeness of the witness search, or an upper bound on C47. No corruption controls or producer search logs are required by the proof or were relied upon. **Did this referee job find something new? No:** it checks the supplied candidate, rather than discovering a new construction. Its value exceeds the specified public printed bar 1.7032090736, but no exhaustive priority claim is made. [PRIOR_ART.md](../PRIOR_ART.md) records the live source checks and their scope. Predictive-model baselines are inapplicable; no predictive score is claimed.

Reproduce the mathematical checks from this directory with a standard Python 3 interpreter (do not disable assertions):

```sh
nice -n 10 python3 independent_check.py > check-run.log
```

The source run used Python, exited successfully, and produced [exact_results.json](exact_results.json) and [witness_results.tsv](witness_results.tsv). Caveats: none. Failures: none.

VERDICT: HOLDS

Release note: source citations were made portable and review wording updated; source line references to the producer report refer to the original report. The checker and saved mathematical inputs are unchanged. This is an AI referee, not human review.
