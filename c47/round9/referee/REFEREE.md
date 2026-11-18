# Clean-room AI referee: C47 ≥ 1.7055913150

The supplied lower bound holds. All four requested items were completed; no mathematical caveats or failures were found.

Reviewed 2026-11-10 America/New_York (2026-11-11 UTC). The reviewed certificate is ../certificates/final.json, SHA-256 ead3bb2464b4ea93a2f0643ddfc0d68ed77a41309e0347034b53b019a1d32a41. Identical input bytes are retained in [../certificates/final.json](../certificates/final.json). Only the expressly permitted producer documents and data were read. No producer, earlier-referee, Tomar, or Doldrums code was read, imported, run, or copied. The mathematical computation is the freshly written, standard-library-only [referee_check.py](referee_check.py).

## (a) Definition match and the reduction lemma

The [live table](https://teorth.github.io/optimizationproblems/constants/47a.html) currently lists Lin's lower bound **1.6855099933** and upper bound **3.879**. Open [PR #350](https://github.com/teorth/optimizationproblems/pull/350) proposes **1.7055022252**. These are distinct publication states. The supplied 444-atom predecessor is 1.7055305518; the present candidate is not the value displayed on the live table. See [PRIOR_ART.md](../PRIOR_ART.md) for the bounded source search and final recheck.

The definition below is quoted verbatim from the table's [raw source](https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/47a.md), with its original notation and reference markers. The consulted source and Apache-2.0 license are omitted and identified in sources/SOURCES.md.

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

Thus the quantity is the optimal weak-type (1,1) constant for **centered, axis-parallel squares**, using Lebesgue area and the function's $L^1$ norm. A periodic atomic measure is not itself an admissible integrable function; part (c) supplies the required finite function.

The exact reduction used is **Tomar's Lemma 6.2**, Section 6, printed p. 8 of [Tomar v5](https://doi.org/10.5281/zenodo.23716077), following Lin. Its complete mathematical statement is:

- Let $\mu$ be a positive, locally finite atomic measure, periodic under $P_x\mathbb Z\times P_y\mathbb Z$, with finitely many atoms in $C=[0,P_x)\times[0,P_y)$, and let $\lambda>0$.
- For each of finitely many rectangles $R_i$, choose a finite set $S_i$ of atoms and a radius $0<r_i<\sqrt{\mu(S_i)/(4\lambda)}$, with $R_i\subseteq\bigcap_{p\in S_i}Q(p,r_i)$.
- For $\mathcal U=\bigcup_{i,k,l}(R_i+(kP_x,lP_y))$, the conclusion is $c_2\ge\lambda|\mathcal U\cap C|/\mu(C)$.

Lemma 6.1 gives the elementary containment step; the **strict** radius inequality in Lemma 6.2 permits smearing. Lin's [mathematical proof, Sections 4–6](https://raw.githubusercontent.com/CoolRmal/centered-maximal-constant/main/docs/PROOF.md), treats the weighted lattice, replaces a finite block of atoms by small squares, and lets the boundary loss vanish. I read those sections. Lin's [*c2 < 4* manuscript](https://coolrmal.github.io/assets/papers/c2-less-than-4.pdf) gives the same square operator but concerns the upper bound; the repository exposition is the lower-bound source cited by Tomar. No upper-bound result is needed here.

Every hypothesis is met:

| Hypothesis | Finding using its own checks |
| --- | --- |
| Positive periods | $P_x=65792295535231/20000000000000>0$, $P_y=274655344395649/100000000000000>0$. |
| Positive, locally finite periodic measure | All 452 rational masses are positive; their distinct coordinates are in $C$. Lattice extension gives a periodic measure with finitely many atoms in every bounded set. |
| Finite positive cell mass | $\mu(C)=529089970243997/100000000000000>0$, summing each base mass once. |
| Positive level | $\lambda=1$. |
| Finite witnesses and supports | There are 8,443 bounded rational boxes. For each, $S_i$ contains all periodic atoms in the closed box. Each support has between 1 and 1,580 atoms, including lattice copies. |
| Strict radius condition | Every $r_i>0$ and every separately counted $\mu(S_i)-4r_i^2>0$. |
| Containment | All four rectangle-containment inequalities hold for every witness; each rectangle lies in $\overline C$. |
| Area in the lemma | The base union has area $A$. Its other lattice translates meet $C$ only on null boundary sets, so the area of $\mathcal U\cap C$ is $A$. |

Part (c) proves $Mf>1$ on the retained union. This implies the table's non-strict condition $Mf\ge1$, so there is no level-set convention mismatch.

## (b) Every witness and the exact ratio

For each base atom $(x_j,y_j,m_j)$ and closed box $B=[a,b]\times[c,d]$, I count **all** periodic copies using

$$
k_-=\left\lceil\frac{a-x_j}{P_x}\right\rceil,\quad
k_+=\left\lfloor\frac{b-x_j}{P_x}\right\rfloor,\qquad
l_-=\left\lceil\frac{c-y_j}{P_y}\right\rceil,\quad
l_+=\left\lfloor\frac{d-y_j}{P_y}\right\rfloor.
$$

The atom contributes $m_j\max(0,k_+-k_-+1)\max(0,l_+-l_-+1)$ to $\mu(B)$. Exact integer scaling of the rational coordinates makes negative shifts and equality at box boundaries unambiguous. No search window or floating-point membership test is assumed. For $R=[u,v]\times[s,t]$, I check

$$
0\le u<v\le P_x,\quad 0\le s<t\le P_y,\qquad
u\ge b-r,\quad v\le a+r,\quad s\ge d-r,\quad t\le c+r,
$$

and $\mu(B)>4r^2$. These imply $B\subseteq Q(z,r)$ for every $z\in R$. Closed boxes of zero width or height are legitimate atomic witnesses. All **8,443** witnesses pass. The full recount and containment checks are at referee_check.py:127; the input witnesses start at ../certificates/final.json:2272.

The minimum strict mass slack is

$$
\delta=\frac{5544964724257579515302707}{25961484292674138142652481646100480000000000000}
\approx2.13584272060371694\times10^{-22}>0.
$$

It occurs at zero-based witness 4646 (../certificates/final.json:71963). The minimum containment margin is exactly zero, which is valid for closed squares. The mass-versus-area inequality is strict throughout.

For the area I use the standard x sweep with a segment tree of covered y intervals (referee_check.py:43). Between consecutive x endpoints the active y coverage is constant; its exact length times the slab width gives that slab's area. Positive coverage counts an interval once regardless of overlap. Events at the same x contribute no intermediate width. The sweep computes the union, not the sum of rectangle areas.

There are 15,394 distinct x endpoints and 15,590 distinct y endpoints. All endpoints are represented on the exact common grid with denominator $112589990684262400000000000000$; integration uses integers followed by rational division. This is exact rational arithmetic, with no approximation or rounding in the area.

The comparison with sources/producer-proof.md:39 is:

| Quantity | Claimed | Recomputed by the referee |
| --- | --- | --- |
| Base atoms | 452 | 452 |
| Witnesses | 8443 | 8443 |
| Cell mass | 529089970243997/100000000000000 | 529089970243997/100000000000000 |
| Union area $A$ | 22878843460258009274861600625288681562329176839147945011303/2535301200456458802993406410752000000000000000000000000000 | 22878843460258009274861600625288681562329176839147945011303/2535301200456458802993406410752000000000000000000000000000 |
| Ratio $q=A/\mu(C)$ | 22878843460258009274861600625288681562329176839147945011303/13414024367090776613897918866165655414442557440000000000000 | 22878843460258009274861600625288681562329176839147945011303/13414024367090776613897918866165655414442557440000000000000 |

Claimed minus recomputed ratio is **exactly zero**. The decimal expansion begins

$$
q=1.7055913150409727051741893221762880736469403435789\ldots.
$$

This is the exact area ratio of the **certified witness union**. It does not assert that all points outside that union fail the maximal-function condition. All exact results are in [referee-results.json](referee-results.json).

## (c) The finite instance and the integrable function

I checked the argument beginning at sources/producer-proof.md:12, its smearing and limiting steps, and the explicit parameters at line 39. All numerical fields in ../producer_logs/final-finite.json:3–12 agree with the referee’s own calculation. The file's free-text producer status is provenance, not a mathematical hypothesis.

Retain the atoms

$$
p_j+(kP_x,lP_y),\qquad 1\le j\le452,\quad 0\le k,l<N,
$$

with $h=2$ and $N=333020005938$. Separately,

$$
R_{\max}=\frac{12850061102957074811}{4611686018427387904}
\approx2.7864128328795075551.
$$

The maximum occurs at zero-based witness 1876 (../certificates/final.json:30420). The boundary condition has positive exact margin

$$
h\min(P_x,P_y)-R_{\max}
=\frac{76186664610341770599284249613}{28147497671065600000000000000}>0.
$$

Every witness atom needed in an inner cell, $h\le k,l<N-h$, is therefore retained. Directly counting the periodic copies also shows that their relative x indices range from $-1$ to $1$ and their relative y indices from $-2$ to $2$. Adding these to any inner-cell index leaves both indices between 0 and $N-1$. Thus $h=2$ suffices, including at the boundary cells.

The supplied smearing radius is

$$
\varepsilon=
\frac{5544964724257579515302707}{2730244964481409688451714901784657920000000000000}
\approx2.03094037216210213\times10^{-24}.
$$

It satisfies $0<\varepsilon\le1/2$ and

$$
\delta-4(2R_{\max}+1)\varepsilon
=\frac{16634894172772738545908121}{103845937170696552570609926584401920000000000000}>0.
$$

For every witness,
$4(r+\varepsilon)^2-4r^2=8r\varepsilon+4\varepsilon^2
\le4(2R_{\max}+1)\varepsilon<\delta$.
I also checked $\mu(B)-4(r+\varepsilon)^2>0$ **separately for every witness**, using its freshly counted mass (referee_check.py:155).

Define the finite function

$$
f(z)=\sum_{k,l=0}^{N-1}\sum_{j=1}^{452}
\frac{m_j}{4\varepsilon^2}\,
\mathbf1_{Q(p_j+(kP_x,lP_y),\varepsilon)}(z).
$$

It is nonnegative, bounded and compactly supported, hence integrable. The proof keeps each smeared square in full, including parts outside the block (sources/producer-proof.md:17). Each summand integrates to its mass; overlap does not change the integral of the sum. Consequently,

$$
\|f\|_1=N^2\mu(C)
=\frac{14669326873237061904924463702854039117}{25000000000000}.
$$

The number of retained atoms/summands is exactly
$452N^2=50127850608435390977449488$.
No expansion of this enormous finite set is necessary: the displayed indexing formula specifies the function exactly.

For every center in a translated witness rectangle in an inner cell, $Q(z,r+\varepsilon)$ contains every full smeared square belonging to the witness box. Its average is strictly greater than 1. The $(N-2h)^2$ translated witness unions have total area $(N-2h)^2A$: different cells meet only on null edges. The defining inequality at level 1 gives

$$
C_{47}\ge q\left(\frac{N-2h}{N}\right)^2=:q_N.
$$

Claimed and recomputed finite lower values are identical:

$$
q_N=
\frac{211443076519550480268373711401841739495027970445032200793701027082601051542104989}
{123970540105353714391020257438714119850224408123125640972549257953280000000000000}.
$$

The decisive exact comparison is

$$
q_N-\frac{341118263}{200000000}
=\frac{59046325306791910616119149213656897112859307792007778904989}
{123970540105353714391020257438714119850224408123125640972549257953280000000000000}
>0.
$$

Its margin is approximately $4.76293\times10^{-22}$, and

$$
q_N=1.70559131500000000000047629320043788349\ldots.
$$

The stored floating approximation 1.705591315 (../producer_logs/final-finite.json:12) rounds away that margin. The conclusion uses the exact fraction. Holding $h,\varepsilon$ fixed and letting $N$ increase proves the stronger $C_{47}\ge q$. The proof does not assert that a single finite function attains the periodic limit.

## (d) Periods, boundaries, rounding, and scope

**Half-open cell.** sources/producer-proof.md:5 explicitly defines $C=[0,P_x)\times[0,P_y)$ and distinguishes its closure. Line 10 uses the half-open cell for atomic mass and null shared edges for area. Lines 12 and 17 use it again for the finite mass, and line 39 for the numerical instance. This is correct throughout. All base atoms in this particular certificate actually lie strictly inside the cell, although the checker correctly permits atoms on its left/bottom edges.

**Atoms and periods.** All 452 masses are positive; zero atoms are outside the cell, and no two base atoms have the same coordinate pair. Their coordinates therefore also do not collide modulo the periods. The periodic extension uses the two supplied positive periods; they need not be the smallest possible periods. Each radius denominator divides $D=18446744073709551616=2^{64}$. Search reach, producer timing, and source-family metadata are not mathematical hypotheses and were not used to compute any mass or area.

**Boundary effects.** Membership in a closed box includes both endpoints via exact inclusive integer ranges. Containment can be non-strict because the averaging squares are closed. Shared rectangle/cell edges have zero Lebesgue area. Truncation retains every needed witness atom, and smearing discards no part of any retained mass. These are different issues, all addressed by the computation and proof.

**Rounding.** Exact arithmetic gives

$$
\frac{17055913150}{10^{10}}<q_N<q<\frac{17055913151}{10^{10}}.
$$

Both $q_N$ and $q$ therefore have downward-truncated ten-place decimal **1.7055913150**. The claimed decimal is valid without rounding upward. Its difference from the supplied previous printed value 1.7055305518 is exactly 0.0000607632; from the open #350 value it is 0.0000890898. The publication states and bounded comparison sources are recorded in PRIOR_ART.md.

**Scope and completion.** Every requested mathematical item was completed. This establishes a lower bound, not optimality, an exact value of $C_{47}$, or search completeness. No prior referee's verdict was used as evidence. **Did this referee find something new? No:** it confirms the supplied candidate; it did not discover another construction or establish global priority.

To reproduce the complete mathematical check from this directory, using the archived input bytes:

~~~sh
/usr/bin/time -l nice -n 10 python3 referee_check.py ../certificates/final.json ../producer_logs/final-finite.json --out ../release_validation/referee-results.json
~~~

The original run used the identical permitted producer data and is recorded in referee-run.log and referee-time.log (retained historical logs): one CPU, nice 10, **1.81 seconds wall time**, maximum resident set size **67,256,320 bytes**, below the 4 GB limit. The calculation uses exact rational/integer arithmetic throughout; decimals are explanatory only.

Caveats or failures requiring file/line references: **none**. Affirmative checks and the relevant producer claims are referenced above.

VERDICT: HOLDS
