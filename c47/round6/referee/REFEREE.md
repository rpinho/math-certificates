# Clean-room AI referee of C47 ≥ 1.7050503714

**Conclusion: the claimed lower bound holds.** The exact periodic ratio and the supplied explicit finite L1 construction both check. All 474 atoms and all 6292 witnesses were checked, without importing, reading, copying, or running any producer verifier or search code. The computational proof uses only this referee's newly written `referee_check.py`, Python's standard-library rational/integer arithmetic, and the permitted JSON data. The producer's proofs were treated as claims to check, not as computational evidence.

Certificate: `../certificates/final.json`, SHA-256 `5a9baac31ca5e4875e9495a81469402018bf2cccb8889f9d85f396d4d38f32c4`. Sources accessed 2026-11-10 UTC (2026-11-09 in the job's local timezone). The full output of the referee’s own checks is [CHECK_RESULTS.json](CHECK_RESULTS.json); the per-witness table is regenerable and omitted; its SHA-256 and command are in README.md. CSV row 2 is witness index 0.

## (a) Definition match and the precise reduction

The [live official table](https://teorth.github.io/optimizationproblems/constants/47a.html) defines the centered, axis-parallel **square** weak-type constant for **integrable functions on the plane**. The following is its definition verbatim from [the raw source](https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/47a.md), lines 5–28, including its source-reference markup. The source is distributed under [Apache 2.0](https://github.com/teorth/optimizationproblems/blob/main/LICENSE); the consulted source and license are omitted and identified by URL and hash in sources/SOURCES.md.

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

The applicable result is **Tomar, v5, Section 6, Lemma 6.2, p. 8**, with the definition preceding Lemma 6.1: [paper](https://doi.org/10.5281/zenodo.23716077), consulted text lines 438–463 (omitted source hash in sources/SOURCES.md). In mathematical notation, its exact statement is: for a positive locally finite atomic measure μ, periodic under Λ=Pxℤ×Pyℤ with finitely many atoms in C=[0,Px)×[0,Py), and λ>0, suppose finitely many rectangles Rᵢ satisfy

\[
R_i\subseteq\bigcap_{p\in S_i}Q(p,\rho_i),\qquad
0<\rho_i<\sqrt{\mu(S_i)/(4\lambda)},
\]

where Sᵢ is a finite set of atoms of μ. With U=⋃ᵢ⋃ₜ∈Λ(Rᵢ+t), the conclusion is

\[
c_2\geq\lambda\,|U\cap C|/\mu(C).
\]

Tomar credits Lin's truncation-and-smearing argument. I read Lin's [lower-bound exposition, §§5–6](https://github.com/CoolRmal/centered-maximal-constant/blob/72c022ba09032b522c878cca2f9b6c68217d77ea/docs/PROOF.md), consulted lines 119–148 (omitted source hash in sources/SOURCES.md). Lin truncates the lattice, spreads each atom over a square, obtains a finite-function weak-type lower bound, and takes a limit. Lin's separately linked *c2 < 4* paper was also read for its definition; it concerns the upper bound, whereas the lower-bound argument is in that exposition. No upper-bound comparison principle is needed here.

Every hypothesis of Lemma 6.2 is satisfied:

| Hypothesis | Referee’s own check for this measure |
| --- | --- |
| Positive periods | Px=328954332323709/100000000000000>0; Py=17164908257263/6250000000000>0. |
| Positive locally finite atomic measure | There are exactly 474 atoms, every mass is strictly positive, and every position is in the bounded half-open cell. A positive-period lattice has only finitely many translates meeting any bounded region, so this extension is locally finite. |
| Periodicity and finite cell mass | Define μ=ΣⱼΣₖ,ₗ∈ℤ mⱼδₚⱼ₊₍ₖPx,ₗPy₎. Integer reindexing proves periodicity. Base positions are distinct modulo the periods, so μ(C)=Σⱼmⱼ=529047036568853/100000000000000. |
| Positive level and finitely many witnesses | The certificate's λ is exactly 1; it contains exactly 6292 witnesses. |
| Finite sets Sᵢ | Take Sᵢ to be **all** periodic atoms in the witness's closed bounded box Bᵢ. Exact integer ranges count these copies without a search cutoff. |
| Strict radius inequality | Every radius is positive and μ(Bᵢ)−4rᵢ²>0. The minimum is explicitly reported in (b). |
| Rectangle containment | Every rectangle is nonempty, lies in the closed cell, and satisfies Rᵢ⊆⋂ₚ∈SᵢQ(p,rᵢ), as proved and checked in (b). |
| Area entering the lemma | Rectangles lie in the closed cell. Translates from other cells can intersect C only on edges, a Lebesgue-null set. Hence |U∩C| equals the union area A computed in (b). |

These are checks of the table's full constant, not a restricted variant. A periodic atomic measure is not itself an L1 function; section (c) explicitly supplies that passage. The strict level set obtained below is contained in the table's non-strict level set, so no convention change is needed. More generally the two conventions have the same constant by applying a strict-level inequality at β<α and taking β↑α.

## (b) All witnesses, union area, and the ratio

For a box B=[a,b]×[c,d], I computed its mass directly from each base atom (xⱼ,yⱼ,mⱼ). Its admissible horizontal translations are the inclusive integers

\[
\left\lceil\frac{a-x_j}{P_x}\right\rceil\leq k\leq
\left\lfloor\frac{b-x_j}{P_x}\right\rfloor,
\]

and likewise ⌈(c−yⱼ)/Py⌉≤l≤⌊(d−yⱼ)/Py⌋. If their counts are nₓ,nᵧ, this atom contributes exactly mⱼnₓnᵧ to μ(B). This accounts for atoms on **closed box boundaries**, negative translations, and multiple periodic copies of a base atom. The certificate supplies no precomputed mass that this computation trusts. Code: `referee_check.py:123–160`; input witnesses begin at `../certificates/final.json:2382`.

For every R=[u,v]×[s,t] and r, the checker established

\[
0\leq u<v\leq P_x,\quad0\leq s<t\leq P_y,\quad r>0,
\]
\[
u\geq b-r,\quad v\leq a+r,\quad s\geq d-r,\quad t\leq c+r,
\qquad\mu(B)>4r^2.
\]

To see the geometry directly, for any center z∈R we have zₓ−r≤v−r≤a and zₓ+r≥u+r≥b, with the identical y inequalities. Thus B⊆Q(z,r), so μ(Q(z,r))/(4r²)>1. Equivalently R⊆⋂ₚ∈S Q(p,r), exactly the lemma's hypothesis.

**6292 of 6292 witnesses pass.** The minimum containment slack is zero, which is allowed because the averaging squares and boxes are closed. Every witness box contains at least one atom on a box boundary; replacing closed membership by strict membership would be an incorrect check. The minimum strict mass slack, attained by zero-based witness 5520 (radius at `../certificates/final.json:85190`), is

\[
\delta=
\frac{121866966319552490346558479}
{519229685853482762853049632922009600000000000000}
=2.3470723966645687250\ldots\times10^{-22}>0.
\]

The largest radius is

\[
R_{\max}=\frac{12849756647665607181}{4611686018427387904}
=2.78634681466182077273947836904000041613471694290637969970703125.
\]

Both values match `sources/producer-proof.md:37` and `../producer_logs/final-finite.json:8` exactly. The very small slack was compared as a rational, not rounded to machine precision.

For the union area I used an exact vertical sweep of all rectangle endpoints. All rational coordinates are scaled by their derived least common denominator

`112589990684262400000000000000`.

Within each open x-slab the active y-intervals are fixed. A coverage-count segment tree gives their exact union length, counting overlap once; summing width times covered length gives A. This is ordinary rectangle-union integration, implemented by the referee in `referee_check.py:35–81`. There are 11445 x-slabs and 11609 elementary y-intervals. Coincident endpoints contribute zero width; boundary choices do not affect area. The sweep ends with every coverage count zero. No grid approximation, random sampling, or numerical quadrature is used.

Let

\[
T=28587164107974856086021451670774323985081039148875463526401.
\]

| Quantity | Claimed in `sources/producer-proof.md:35–37` | Recomputed by the referee |
| --- | --- | --- |
| Cell mass μ(C) | 529047036568853/100000000000000 | 529047036568853/100000000000000 |
| Union area A | T/3169126500570573503741758013440000000000000000000000000000 | T/3169126500570573503741758013440000000000000000000000000000 |
| Ratio q=A/μ(C) | T/16766169836386813382037844357636904350593843200000000000000 | T/16766169836386813382037844357636904350593843200000000000000 |

Thus the requested exact fraction is reproduced, with zero difference:

\[
q=\frac{28587164107974856086021451670774323985081039148875463526401}
{16766169836386813382037844357636904350593843200000000000000}
=1.705050371488752691248892603145594251487715813487417673054191457915\ldots
\]

The area is 9.020518462367465376147412046515… . It is less than the full cell area; the uncovered part of this particular witness union has exact area

\[
\frac{43844972561195315608759030091114652022978828898471507967}
{3169126500570573503741758013440000000000000000000000000000}.
\]

No assertion that this is the full maximal-function superlevel area is necessary or made.

## (c) The explicit finite L1 instance

I checked the reasoning in `sources/producer-proof.md:12–27` and all mathematical numerical fields in `../producer_logs/final-finite.json:4–11`. They agree with the certificate values recomputed by the referee.

Retain atoms pⱼ+(kPx,lPy), 0≤k,l<N, with

\[
h=2,\qquad N=153690020890,
\qquad\varepsilon=
\frac{121866966319552490346558479}
{54603802373838430093659704754857574400000000000000}.
\]

Define the actual function

\[
f(z)=\sum_{k,l=0}^{N-1}\sum_{j=1}^{474}
\frac{m_j}{4\varepsilon^2}
\mathbf1_{Q(p_j+(kP_x,lP_y),\varepsilon)}(z).
\]

This is a finite sum of nonnegative, bounded, compactly supported measurable functions, hence it is integrable. Each summand has integral mⱼ. Overlap between smear squares does not change the integral of the sum; smear squares are kept whole, including any portions outside the truncation block. Exact arithmetic gives

\[
\|f\|_1=N^2\mu(C)=
\frac{124964203467357763224365811331552613}{1000000000000},
\]

and exactly 474N²=11196175075033933649855400 atomic summands. The symbolic definition specifies every summand; expanding that enormous list is unnecessary.

The retained interior has h≤k,l<N−h. The referee’s own check gives

\[
h\min(P_x,P_y)-R_{\max}
=\frac{76179058386042140176822121771}
{28147497671065600000000000000}>0.
\]

For a center in an inner cell, every atom within a witness radius therefore belongs to the retained block. This also follows directly from the actual translation indices: all atoms counted in all witness boxes have horizontal indices between −1 and 1 and vertical indices between −2 and 2. Translating any such box by an inner-cell index leaves all of its atoms at indices 0,…,N−1. These ranges were derived from the exact floor/ceiling counts, not assumed from `reach`.

The smear radius is positive, less than 1/2, and approximately 2.2318402935605989×10⁻²⁴. Its uniform enlargement cost satisfies the **exact identity**

\[
4(2R_{\max}+1)\varepsilon=\delta/4<\delta.
\]

For every witness radius r, since ε≤1/2,

\[
4(r+\varepsilon)^2-4r^2
=8r\varepsilon+4\varepsilon^2
\leq4(2R_{\max}+1)\varepsilon<\delta.
\]

Consequently μ(B)>4(r+ε)² for every witness. I also checked these 6292 enlarged-square inequalities directly with the computed box masses (`referee_check.py:177–182`). For z in a translated witness rectangle, Q(z,r+ε) contains the full smeared square of every atom in its translated box. Therefore M₂f(z)>1 throughout each inner copy of the witness union.

Distinct cell interiors are disjoint, so the certified level-set area is at least (N−2h)²A, with (N−2h)²=23620622519939116224996. Applying the table's inequality at α=1 yields

\[
C_{47}\geq q\left(\frac{N-4}{N}\right)^2
=\frac{168811653077506525697921248259438253206685113380240382951724856442390598275529849}
{99006842207774158957432850704263475565623260511339911602430279680000000000000000}.
\]

This equals the supplied finite ratio exactly. Its decimal value is

`1.705050371400000000002300137753057040673377724491976033003416392957…`.

Its excess over 1.7050503714=8525251857/5000000000 is the strictly positive rational

\[
\frac{227729375573062630064347972901312762357938931400725123529849}
{99006842207774158957432850704263475565623260511339911602430279680000000000000000}
=2.3001377530570406733777\ldots\times10^{-21}>0.
\]

Thus this finite function already proves the requested decimal bound. Keeping h and ε fixed and letting N→∞ gives C47≥q as well. There is no reliance on treating an infinite periodic measure as an integrable function.

## (d) Periods, duplicates, boundaries, rounding, and scope

**Half-open cell:** `sources/producer-proof.md:5` explicitly sets C=[0,Px)×[0,Py), places the atomic mass there and distinguishes its closure. Lines 10, 12, 17 and 35 maintain that convention. It is used correctly: the N×N block contains exactly N² copies of each base atom. This version has no closed-cell mass-counting defect.

**Atoms and periods:** all 474 base atoms are inside C, all masses are positive, and no two positions coincide. Because each base position is in the half-open cell, this also excludes duplicates modulo the periods. There are zero atoms on the left or bottom edge, and none on the excluded right or top edges. It is not necessary to prove that the stated periods are minimal; they are valid periods by the definition of the extension. See `referee_check.py:105–116` and `CHECK_RESULTS.json:5–13`.

**Boundary effects:** 1678 witness rectangles touch the cell boundary. Their shared edges have zero Lebesgue area and cause no area double-counting. Atomic membership in closed witness boxes is handled inclusively; such atomic boundary mass is not discarded as a null set. These are two different measures, and the proof uses the appropriate convention for each. In the finite construction, h=2 and the positive radius margin above eliminate any ambiguity at the retained block's excluded upper edges.

**Rounding:** the requested decimal is a downward truncation, not round-to-nearest. Exact arithmetic establishes

\[
1.7050503714<q<1.7050503715.
\]

Rounding q to nearest at ten decimal places would give 1.7050503715, which this certificate does not prove. The producer correctly claims 1.7050503714. The finite JSON's `finite_ratio_float` at line 12 displays only 1.7050503714 and loses the tiny positive excess; the exact field at line 11 and the rational comparison above are what establish strictness. This display limitation is not a defect in the bound.

**Scope:** every atom, every box mass, every radius, every containment, the whole rectangle-union area, and the finite-instance inequalities were checked. No requested mathematical item was left unchecked for time. The producer's optimizer, discovery chronology, corruption controls, and claims about search completeness were not inspected or reproduced; none is needed for the lower bound. The `reach`, `D`, timing, and status metadata are not used as mathematical premises. No producer or third-party mathematical program was run. This is an exact computational referee with a written analytic proof, not a new Lean formalization.

**Novelty:** did this referee find a new construction? **No.** It confirms the supplied candidate. The resulting bound exceeds the named public candidate 1.7040280575 and the supplied prior 1.7048221231 under the same definition. [the prior-art note](../PRIOR_ART.md) distinguishes the live table's older displayed row from the pending public PRs and records the bounded discovery searches; no exhaustive priority or optimality claim is made.

**Reproduction:** from this job directory run the following. The checker requests absolute nice 10 itself, using one process; on this host the OS denied increasing the inherited priority, so it ran at nice 15, a lower CPU priority. Its first complete run succeeded in 18.61 seconds. No mathematical changes or corrective reruns were needed.

```sh
nice -n 10 python3 -u referee_check.py \
  --certificate ../certificates/final.json \
  --finite ../producer_logs/final-finite.json \
  --output ../release_validation/referee-results.json \
  --witness-output ../release_validation/witness_checks.csv
```

The program uses only the Python standard library. `check.log` retains the completed run. The numerical worker exited and was reaped; no numerical worker remains running.

**Caveats or failures affecting the claim: none.**

VERDICT: HOLDS
