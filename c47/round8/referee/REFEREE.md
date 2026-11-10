# Clean-room referee: C47 ≥ 1.7055022252

**The candidate holds.** The referee’s own rational arithmetic reproduces the claimed periodic ratio exactly, and the supplied finite integrable function has a ratio strictly greater than 1.7055022252. All requested mathematical checks (a)–(d) are complete; no caveats or failures affecting the bound were found.

Reviewed 10 November 2026. Input: `../certificates/final.json`, SHA-256 `1afaf5d5c8968fffd3f98cf77de4d462dd1070b9dea4ec1456dd5a91087bfb44`. I wrote `referee_check.py` here, using only Python's standard library. No producer, prior-referee, Tomar or Doldrums executable source was read, copied, imported or run. The allowed producer prose and JSON supplied claims to compare. The permitted the previous round’s AI referee report was read for historical context and primary-source locations; its checker was not read.

## (a) Definition match and the precise periodic lemma

The [official table](https://teorth.github.io/optimizationproblems/constants/47a.html) was fetched live, both as HTML and raw Markdown. Its definition follows verbatim, including formulas; source citation markers are retained. The consulted table files and Apache-2.0 license are omitted and identified in sources/SOURCES.md.

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

In dimension two the denominator is exactly $4r^2$, and the averaging regions are centered axis-parallel **squares**. The constant concerns integrable functions on the plane. A periodic measure alone is not such a function; truncation and smearing are needed.

The result used is **Tomar's Lemma 6.2, following Lin**, in [*Bounds for the weak type (1,1) constant of the centred maximal operator over squares*, v5, Section 6](https://doi.org/10.5281/zenodo.23716077). I read the rectangle lemma, periodic lemma, and proof (consulted v5 source lines 302–323; see sources/SOURCES.md). The exact mathematical statement, with notation expanded, is as follows.

Let $P_x,P_y>0$, $\Lambda=P_x\mathbb Z\times P_y\mathbb Z$, and let $\mu$ be a positive locally finite atomic measure invariant under $\Lambda$, with finitely many atoms per half-open cell $C=[0,P_x)\times[0,P_y)$. Given $\lambda>0$, finitely many rectangles $R_i$, finite sets $S_i$ of atoms of $\mu$, and numbers $\rho_i$, assume

\[
0<\rho_i<\sqrt{\mu(S_i)/(4\lambda)},\qquad
R_i\subseteq R_{S_i}(\rho_i):=\bigcap_{p\in S_i}Q(p,\rho_i).
\]

Then, with $U_{\rm per}=\bigcup_{t\in\Lambda}\bigcup_i(R_i+t)$,

\[
C_{47}=c_2\ge\frac{\lambda|U_{\rm per}\cap C|}{\mu(C)}.
\]

The surrounding definition at consulted v5 source line 302; see sources/SOURCES.md supplies positive masses and local finiteness. Positive periods and nonzero cell mass are explicit here. I also read [Lin's proof notes, sections 4–6](https://github.com/CoolRmal/centered-maximal-constant/blob/72c022ba09032b522c878cca2f9b6c68217d77ea/docs/PROOF.md#L83), especially the finite smearing and limiting proof (consulted proof lines 119–150; see sources/SOURCES.md). Lin's separate [*c₂ < 4* manuscript](https://coolrmal.github.io/articles/c2-less-than-4/) defines the same square operator in its introduction; its upper-bound kernel theorem is not needed here.

Every hypothesis is met for this certificate:

- The two periods are positive rationals. There are 440 distinct support points in $C$, all with positive rational masses. Periodic extension is a positive locally finite measure: a bounded box intersects only finitely many translates of these finitely many points.
- The level is $\lambda=1$. There are 7,806 finite closed boxes $B_i$, positive radii $r_i$, and nonempty closed rectangles $R_i\subseteq\overline C$. Set $S_i=\operatorname{supp}\mu\cap B_i$.
- For every witness, the referee’s own count proves $\mu(S_i)>4r_i^2$, and endpoint inequalities prove $B_i\subseteq Q(z,r_i)$ for every $z\in R_i$. Thus the required intersection containment holds.
- Because the rectangles lie in $\overline C$, nonzero lattice translates can contribute within $C$ only on its edges. Those have zero Lebesgue area, so $|U_{\rm per}\cap C|=|\bigcup_iR_i|=A$.

Section (c) separately supplies the entire passage to finite $L^1$ functions. It gives $Mf_N>1$ on the certified sets, which also satisfies the table's non-strict level-set convention.

## (b) Witness masses, containment, union area and ratio

The periods read by the referee and summed half-open cell mass are

\[
P_x=\frac{328960566924801}{100000000000000},\quad
P_y=\frac{274654026549117}{100000000000000},\quad
m=\mu(C)=\frac{529088934896347}{100000000000000}.
\]

For each base atom $(x_j,y_j)$ and closed witness box $B=[a,b]\times[c,d]$, its translated copies in $B$ have exactly the integer indices

\[
\left\lceil\frac{a-x_j}{P_x}\right\rceil\le k\le
\left\lfloor\frac{b-x_j}{P_x}\right\rfloor,\qquad
\left\lceil\frac{c-y_j}{P_y}\right\rceil\le l\le
\left\lfloor\frac{d-y_j}{P_y}\right\rfloor.
\]

An empty index interval contributes zero; otherwise the contribution is its two interval lengths multiplied by $m_j$. Summing this over all 440 base atoms counts **every** periodic copy in the box, with no floating-point comparisons or finite search cutoff (`referee_check.py:116–130`). Across all witnesses the count is 2,124,106 atom-copy incidences. The metadata `reach` is unused.

For every $R=[u,v]\times[s,t]$, the checker establishes $r>0$, $a\le b$, $c\le d$, $0\le u<v\le P_x$, $0\le s<t\le P_y$, and

\[
v-a\le r,\quad b-u\le r,\quad t-c\le r,\quad d-s\le r,\qquad
\mu(B)-4r^2>0.
\]

The four inequalities compare extreme coordinates and imply containment of the whole box in each centered square. They do not merely test a rectangle's midpoint (`referee_check.py:104–113`). The minimum mass slack is

\[
\delta=\frac{648464387435490448162039}
{519229685853482762853049632922009600000000000000}>0.
\]

It occurs at zero-based witness 3991, whose box begins at `../certificates/final.json:62079`. It equals the claim in `sources/producer-proof.md:37`. The omitted regenerable per-witness table records every witness's source line, mass counted by the referee, number of copies, strict slack and smeared slack. Its SHA-256 and regeneration command are in README.md.

For union area I used a standard sweep over rectangle x-endpoints, maintaining the covered y-length with interval multiplicities in a segment tree (`referee_check.py:26–66`). Between successive x-events the active intervals are constant. A node covered by any full interval has its entire y-length; otherwise its length is the sum of its children. Integrating this exact length over all 14,131 positive-width slabs counts overlaps once. All rectangle coordinates become integers after multiplying by `112589990684262400000000000000`; dividing the accumulated integer area by the square of that scale is exact. Shared edges contribute zero area.

| Quantity | Claimed in `sources/producer-proof.md:37` | Recomputed by the referee |
| --- | --- | --- |
| Union area $A$ | `114388018195906255044427129545533845966664904690010061034899/12676506002282294014967032053760000000000000000000000000000` | `114388018195906255044427129545533845966664904690010061034899/12676506002282294014967032053760000000000000000000000000000` |
| Ratio $q=A/m$ | `114388018195906255044427129545533845966664904690010061034899/67069990589546886330812144279013633721316147200000000000000` | `114388018195906255044427129545533845966664904690010061034899/67069990589546886330812144279013633721316147200000000000000` |

Both differences are exactly zero. The ratio is

\[
q=1.70550222521924825896273136488801056848923317252846622506580\ldots.
\]

The exact complement of the rectangle union has area

\[
P_xP_y-A=\frac{144649963715372748487231576316102574802581818829740419693}
{12676506002282294014967032053760000000000000000000000000000}>0.
\]

This complement is not asserted to be the complement of the true maximal superlevel set. The rectangle family need only give a subset of that set. All numerical results are in `exact_results.json`.

## (c) Finite instance and the full periodic limit

I checked `sources/producer-proof.md:12–27,37` and all substantive exact fields of `../producer_logs/final-finite.json:3–11`. Use the supplied

\[
h=2,\quad N=708844255899,\quad
\varepsilon=\frac{648464387435490448162039}
{54604958511434414859528008769942323200000000000000}.
\]

The recomputed largest witness radius is

\[
R_{\max}=\frac{12850077540310281447}{4611686018427387904},\qquad
h\min(P_x,P_y)>R_{\max}.
\]

Retain the atoms $p_j+(kP_x,lP_y)$ for $0\le k,l<N$. For a center in an inner cell, $h\le k,l<N-h$, the strict radius bound places every required atom inside the retained block. I additionally checked the discrete cell offsets of all atoms in all boxes: x offsets are in $[-1,1]$, y offsets in $[-2,2]$. Adding any inner-cell index keeps these between 0 and $N-1$, including endpoints (`referee_check.py:125–129`). Thus boundary retention is checked directly as well as geometrically.

Define the finite function by the explicit formula

\[
f_N(z)=\sum_{k,l=0}^{N-1}\sum_{j=1}^{440}
\frac{m_j}{4\varepsilon^2}\,
\mathbf1_{Q(p_j+(kP_x,lP_y),\varepsilon)}(z).
\]

Keep each smeared square in full, including portions extending outside the block. This is a finite sum of nonnegative bounded measurable functions with compact support. Each summand has integral $m_j$, regardless of overlap, and therefore

\[
\|f_N\|_1=N^2m=
\frac{265846120998961322852534371318637571747}{100000000000000}.
\]

The exact number of summands is $440N^2=221082478813243078371208440$. The formula specifies a finite instance completely; explicitly allocating that list is unnecessary.

The smear parameter satisfies $0<\varepsilon\le1/2$ and

\[
4(2R_{\max}+1)\varepsilon=\delta/4<\delta.
\]

For any witness radius $r$,

\[
4(r+\varepsilon)^2-4r^2
=8r\varepsilon+4\varepsilon^2
\le4(2R_{\max}+1)\varepsilon<\delta,
\]

hence $4(r+\varepsilon)^2<\mu(B)$. This last strict inequality was also checked separately for every witness (`referee_check.py:131–134`). If $z\in R_i+t$, the square $Q(z,r_i+\varepsilon)$ contains every complete smeared square associated with $S_i+t$. Its integral is at least $\mu(B_i)$, so $Mf_N(z)>1$.

Different inner cells' witness unions intersect only on edges. Their total area is $(N-2h)^2A$. The defining inequality for $C_{47}$, at level 1, consequently gives

\[
C_{47}\ge q\left(\frac{N-2h}{N}\right)^2
=\frac{2299016964454535926164008318906010429285009516613200633736490794747466283233740859}
{1347999979410719285506487968385821088532379413340370461131840304447488000000000000}.
\]

This equals the supplied finite fraction exactly. Its decimal expansion begins

`1.705502225200000000000103100733744866923511531088911030635744940634841...`.

Its excess over the target $4263755563/2500000000=1.7055022252$ is exactly

\[
\frac{138979786965310663950224910528247283787044941230042683443259}
{1347999979410719285506487968385821088532379413340370461131840304447488000000000000}
>0,
\]

approximately $1.0310073374486692351\times10^{-22}$. This comparison uses rational arithmetic, not the rounded `finite_ratio_float` field.

The same proof, with fixed $h$ and $\varepsilon$, works for every integer $N>2h$. Letting $N\to\infty$ proves the stronger bound $C_{47}\ge q$. Only finite integrable functions are inserted into the defining weak-type inequality.

## (d) Periods, cells, boundaries, duplicates, rounding and scope

**Half-open cell.** `sources/producer-proof.md:5` explicitly defines $C=[0,P_x)\times[0,P_y)$, with $\overline C$ separately used for rectangles. Lines 10, 12, 17 and 37 consistently count mass in the half-open cell and the finite block. This wording and its use are correct. There are no atoms outside $C$, none on its included left/bottom boundary, and none on its excluded right/top boundary. The earlier closed-cell wording problem is absent.

**Periods and duplicates.** All 440 masses are positive and all 440 support pairs are distinct. Since every point lies in one half-open cell, distinct base points are also distinct modulo the period lattice. The two periods need not be equal or primitive. The fundamental cell and center rectangles are rectangular, but every averaging region is a square with area $4r^2$.

**Boundary atoms and rectangle edges.** Exact ceiling/floor counts include atoms on the closed box boundaries. There are 30,626 base-atom/witness incidences with a nonempty translation range and at least one translated coordinate on a box boundary; none are silently dropped. There are 2,440 rectangles touching a cell edge. Such edges have zero Lebesgue area and cannot create positive-area double counting. Atomic mass on a boundary would require the half-open convention even though that convention is immaterial to Lebesgue area. Smearing is never clipped at a cell or block boundary.

**Decimal rounding.** Exact integer division verifies that 1.7055022252 is the downward truncation of $q$ to ten decimal places. The positive periodic gap is

\[
q-1.7055022252=
\frac{1290980547495554154492643993822458967719311594899}
{67069990589546886330812144279013633721316147200000000000000}
\approx1.9248258962731364888\times10^{-11}.
\]

The finite fraction also lies strictly above the printed decimal, as proved in (c). `../producer_logs/final-finite.json:12` displays the target itself as a floating number; this display loses the finite margin but does not contradict the exact fraction at line 11.

**Scope and novelty.** Every requested mathematical item was fully checked. No claim is made about optimality, completeness of the producer's search, or a Lean formalization. Did this referee find something new? **No:** this is a verification using its own checks of the supplied construction. The candidate exceeds the public printed comparison 1.7052517050 in [open PR #350](https://github.com/teorth/optimizationproblems/pull/350). The live merged table still shows Lin's older bound. [the prior-art note](../PRIOR_ART.md) records this distinction and the bounded public-source searches. Predictive scores and SBS are inapplicable to an exact certificate; [the baseline scope note](../BASELINES.json) records that scope.

**Reproduction.** From this folder, run `nice -n 10 python3 referee_check.py` with Python 3.9 or later; fresh aggregate results go to ../release_validation/referee-results.json and the regenerable per-witness table goes to ../release_validation/witness_results.json. It uses only the standard library and reads only the two permitted JSON inputs. The completed run used the shared science Python, one CPU process, and took 14.29 seconds. Its inherited scheduling resulted in nice 20 after `nice -n 10`, a lower priority than the requested nice 10. Its aggregate exact_results.json and referee_run.log are retained; its per-witness table is omitted. The proof above supplies the mathematical implication from those arithmetic results to the table's constant.

**Caveats or failures affecting the lower bound:** none.

VERDICT: HOLDS
