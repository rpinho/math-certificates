# Clean-room referee: C47 ≥ 1.7052517050

The candidate holds. The referee’s own computation reproduces the entire claimed rational ratio, and the stated finite integrable function gives a strictly larger ratio than 1.7052517050. No mathematical caveats or failures were found in items (a)–(d).

Reviewed on 10 November 2026. Input: `../certificates/final.json`, SHA-256 `0cd5cc0954f8cc01ac1184b7cf095ce22bb3cdaa9a602fe25c20d8c1bd2bfe04`. The checker in this directory was written from the definition and elementary geometry. No producer, earlier-referee, Tomar, or Doldrums verification/search code was read, imported, copied, or executed. The allowed producer prose and two JSON data files supplied the claims to compare.

## (a) Definition match and the periodic lemma

The [live table](https://teorth.github.io/optimizationproblems/constants/47a.html) was fetched during this review; its HTML and raw Markdown are omitted and identified by URL and SHA-256 in sources/SOURCES.md. The defining formulas are reproduced verbatim:

\[
M_d f(x)\ :=\ \sup_{r>0}\ \frac{1}{\lvert Q(x,r)\rvert}\int_{Q(x,r)} \lvert f(y)\rvert\,dy,
\]

\[
\alpha\,\bigl\lvert\{x\in\mathbb{R}^d:\ M_d f(x)\ge \alpha\}\bigr\rvert\ \le\ c_d\,\lVert f\rVert_1.
\]

\[
C_{47}\ :=\ c_2,
\]

The table's verbal definition, verbatim:

> the optimal weak-type $(1,1)$ constant of the centered Hardy–Littlewood maximal operator associated to axis-parallel squares in $\mathbb{R}^2$.

Here (Q(x,r)=\prod_{j=1}^d[x_j-r,x_j+r]), (r>0), and bars denote Lebesgue measure. The inequality must hold for every integrable (f) and every positive \(\alpha\); (c_d) is the least admissible constant. Thus this is the centered **square** operator, with area (4r^2) in the plane. It is not a torus operator or an assertion just about measures. Source: consulted raw table lines 5–27 (omitted-source inventory in sources/SOURCES.md).

The applicable result is **Tomar's Lemma 6.2 (periodic measures), following Lin**, in [Bounds for the weak type (1,1) constant of the centred maximal operator over squares, v5, Section 6](https://doi.org/10.5281/zenodo.23716077). Its exact mathematical statement, with notation expanded, is:

Let \(P_x,P_y>0\), \(\Lambda=P_x\mathbb Z\times P_y\mathbb Z\), and let \(\mu\) be a positive, locally finite atomic measure invariant under \(\Lambda\), with finitely many atoms per half-open cell \(C=[0,P_x)\times[0,P_y)\). Fix \(\lambda>0\). For finitely many rectangles \(R_i\), suppose finite atom sets \(S_i\) and radii \(\rho_i\) satisfy

\[
0<\rho_i<\sqrt{\mu(S_i)/(4\lambda)},\qquad
R_i\subseteq\bigcap_{p\in S_i}Q(p,\rho_i).
\]

Then, for \(U_{\rm per}=\bigcup_{t\in\Lambda}\bigcup_i(R_i+t)\),

\[
C_{47}=c_2\ge\frac{\lambda|U_{\rm per}\cap C|}{\mu(C)}.
\]

I read the statement and proof in the consulted v5 source at lines 302–323 (see sources/SOURCES.md), including Lemma 6.1's atom-to-rectangle observation. I also read [Lin's proof notes, sections 4–6](https://github.com/CoolRmal/centered-maximal-constant/blob/72c022ba09032b522c878cca2f9b6c68217d77ea/docs/PROOF.md#L83), especially the truncation, smearing, and limiting argument (consulted proof lines 119–150; see sources/SOURCES.md). The table's older commit `8e1ee3d` has the same proof notes. Lin's separate *c2 < 4* manuscript concerns upper bounds; its introduction confirms the operator convention, but its kernel theorem is not used here.

Every hypothesis is met. The periods below are positive; all 454 base masses are positive, their support points are distinct and belong to (C), and periodic repetition of finitely many atoms with positive periods is locally finite. The level is \(\lambda=1\). There are 6920 finite closed boxes (B_i); set (S_i=\operatorname{supp}\mu\cap B_i). The referee’s own check counts every lattice translate in each box, establishes the strict mass/radius inequality, and proves (R_i\subseteq\bigcap_{p\in S_i}Q(p,r_i)). All rectangles lie in \(\overline C\). Consequently nonzero translates can change the union inside (C) only on cell edges, which have zero area. Hence \(|U_{\rm per}\cap C|=|\bigcup_i R_i|=A\).

The infinite periodic measure itself is not integrable. Section (c) below proves the passage to actual (L^1(\mathbb R^2)) functions directly, including boundary retention and smearing. It also produces (Mf>1), so the table's non-strict level-set convention poses no problem.

## (b) Referee’s own witness checks, union area, and ratio

The base data are

\[
P_x=\frac{10279929107097}{3125000000000},\qquad
P_y=\frac{54929897595917}{20000000000000},\qquad
m=\mu(C)=\frac{529075929443469}{100000000000000}.
\]

For an atom ((x_j,y_j)) with mass (m_j), the translates in a closed box (B=[a,b]\times[c,d]) have integer indices

\[
\left\lceil\frac{a-x_j}{P_x}\right\rceil\le k\le
\left\lfloor\frac{b-x_j}{P_x}\right\rfloor,\qquad
\left\lceil\frac{c-y_j}{P_y}\right\rceil\le l\le
\left\lfloor\frac{d-y_j}{P_y}\right\rfloor.
\]

If the two ranges have lengths (n_x,n_y), including zero for an empty range, their contribution is exactly (m_jn_xn_y). Summing over all 454 atoms counts the full periodic box mass, without a search window or floating-point coordinate comparisons. Integer scaling by (10^{14}) represents all atom coordinates, periods, box endpoints, and masses exactly. Source: `referee_check.py:94–139`.

For **every** witness (R=[u,v]\times[s,t]), I checked (r>0), (0\le u<v\le P_x), (0\le s<t\le P_y), and

\[
\max(v-a,b-u,t-c,d-s)\le r,\qquad \mu(B)-4r^2>0.
\]

The first inequality proves (B\subseteq Q(z,r)) for every (z\in R). The exact minimum mass slack over all 6920 witnesses is

\[
\delta=\frac{1851161072028377713189111}
{32451855365842672678315602057625600000000000000}>0.
\]

It occurs at zero-based witness 4808 (`../certificates/final.json:74404`, beginning of its box). This matches `sources/producer-proof.md:37`. The regenerable per-witness table gives each witness's source line, mass counted by the referee, atom-copy count, strict slack, and smeared slack; all pass. Its original SHA-256 and regeneration command are in README.md.

For the area I swept all distinct rectangle x-endpoints. Within each open slab, I sorted and merged the active closed y-intervals, then multiplied their exact union length by the slab width. There are 12,575 slabs. All rectangle coordinates are integers after scaling by `112589990684262400000000000000`; division by the square of this scale recovers the rational area. Endpoint lines have area zero, so the event ordering cannot lose area. This directly computes the union, without adding overlapping rectangle areas or using sampling (`referee_check.py:38–71`).

| Quantity | Producer claim (`PROOF.md:37`) | Referee’s own result |
| --- | --- | --- |
| Union area (A) | `11436840446775366245825984602005252649658962678483718696299/1267650600228229401496703205376000000000000000000000000000` | `11436840446775366245825984602005252649658962678483718696299/1267650600228229401496703205376000000000000000000000000000` |
| Ratio (q=A/m) | `11436840446775366245825984602005252649658962678483718696299/6706834195253218266545949032739264680888893440000000000000` | `11436840446775366245825984602005252649658962678483718696299/6706834195253218266545949032739264680888893440000000000000` |

Both differences are exactly zero. In decimal, (q=1.70525170502497644718575543381577025762356163446673908845531\ldots). The exact complement area is positive:

\[
P_xP_y-A=
\frac{3227677412390415207438669102650597132151269743802096977}
{253530120045645880299340641075200000000000000000000000000}.
\]

This is the complement of the certified union, not a claim about the complement of the true superlevel set. Numerical output is in `exact_results.json`.

## (c) The finite instance and passage to the limit

I checked `sources/producer-proof.md:12–27,37` and every substantive exact numerical field of `../producer_logs/final-finite.json:3–11`. They agree with the referee’s own calculation.

Use the supplied integers and radius

\[
h=2,\quad N=546195122900,\quad
\varepsilon=\frac{1851161072028377713189111}
{3412776071486564665201364584051507200000000000000}.
\]

The largest witness radius is

\[
R_{\max}=\frac{51399709122411996673}{18446744073709551616},
\qquad h\min(P_x,P_y)>R_{\max}.
\]

Retain the atoms (p_j+(kP_x,lP_y)) for (0\le k,l<N). The checker establishes additionally that every atom used in every base witness has cell offsets (k\in[-1,1]), (l\in[-2,2]). Translating a witness to any cell with (h\le k,l<N-h) therefore uses only retained atoms. This is a direct discrete check of boundary retention, as well as the geometric radius bound (`referee_check.py:124–133,159`).

Define the finite function explicitly by

\[
f_N(z)=\sum_{k,l=0}^{N-1}\sum_{j=1}^{454}
\frac{m_j}{4\varepsilon^2}
\mathbf1_{Q(p_j+(kP_x,lP_y),\varepsilon)}(z).
\]

The smeared squares are kept whole, including portions outside the block. This finite sum is nonnegative, bounded, measurable, and compactly supported, so is integrable. Each summand integrates to (m_j), regardless of overlap. Thus

\[
\|f_N\|_1=N^2m=
\frac{15783875235945169116843847206659829}{10000000000}.
\]

The atom count is exactly (454N^2=135441416975004731402140000). A formula defines this finite function completely; enumerating that enormous list is unnecessary.

The given smear radius satisfies (0<\varepsilon\le1/2) and, exactly,

\[
4(2R_{\max}+1)\varepsilon=\delta/4<\delta.
\]

For any witness,

\[
4(r+\varepsilon)^2-4r^2
=8r\varepsilon+4\varepsilon^2
\le4(2R_{\max}+1)\varepsilon<\delta.
\]

Therefore (4(r+\varepsilon)^2<\mu(B)). The checker also verifies this last inequality separately for all 6920 witnesses. For a center (z\in R), the enlarged square (Q(z,r+\varepsilon)) contains the full smeared square about every retained atom of (B). Its integral is at least \(\mu(B)\), giving (Mf_N(z)>1). Positivity makes any other smeared atoms harmless.

The ((N-2h)^2) translated unions in the inner cells have total area ((N-2h)^2A): different cells can overlap only on edges. Applying the table definition at level 1 proves

\[
C_{47}\ge q\left(\frac{N-2h}{N}\right)^2
=\frac{13327900225475061974800945466043839770149633691825540982064004325933564036861539}
{7815796451864601404869911741078304796710014829470292952639078400000000000000000}.
\]

This equals the claimed finite fraction exactly. Its decimal value is
`1.705251705000000000000144984119983273036287667720391949902621...`.
Subtracting the target (341050341/200000000=1.7052517050) gives the strictly positive rational

\[
\frac{1133166370541977050202513296039677726731634704892036861539}
{7815796451864601404869911741078304796710014829470292952639078400000000000000000}
\approx1.44984119983273\times10^{-22}.
\]

Finally the same retention and smearing proof works for every integer (N>2h). Letting (N\to\infty) proves (C_{47}\ge q), the full periodic rational bound. This limit is taken over legitimate finite integrable functions, not over an infinite function inserted into the weak-type inequality.

## (d) Periods, half-open cells, duplicates, boundaries, and rounding

**Half-open cell wording and use.** `sources/producer-proof.md:5` explicitly defines (C=[0,P_x)\times[0,P_y)) and reserves its closure for rectangle clipping. Lines 10, 12, 17 and 37 use the half-open cell for atomic mass and the (N\times N) finite block. This is correct throughout; the old closed-cell mass error is absent. The referee’s own computation found no atoms outside the cell, none on its left or bottom boundary, and none on its excluded top or right boundary. The wording is nevertheless necessary for the general periodic argument.

**Multiplicity and periods.** There are exactly 454 positive masses at 454 distinct support points. Since they are in one half-open cell, no pair is equivalent modulo the periods. The extension therefore counts each copy once. The periods need not be primitive or equal. Their inequality does not turn the averaging squares into rectangles: only the period cell and sets of allowable centers are rectangular; each averaging region remains a square of side (2r).

**Closed boxes and rectangle boundaries.** Atom masses on box boundaries are included by the exact ceiling/floor formulas. There are 30,429 atom/witness incidences with at least one coordinate congruent to a box boundary and with both translation ranges nonempty; these incidences are not discarded. The proof uses closed squares, so inclusion is appropriate. There are 1,956 witness rectangles touching a cell edge; those edges have zero Lebesgue area, and periodic copies do not introduce positive-area double counting. Smearing is not clipped at a cell boundary.

**Rounding.** The target is exactly the downward truncation of (q) to ten digits after the decimal point. Its gap below (q) is

\[
\frac{167512890061360553083520732126896224360403496299}
{6706834195253218266545949032739264680888893440000000000000}
\approx2.49764471857554\times10^{-11}>0.
\]

The `finite_ratio_float` display (`../producer_logs/final-finite.json:12`) hides the much smaller finite margin and is not evidence for strictness. The exact fraction at line 11 does prove strictness. Metadata such as `reach`, producer timing, and the search-source filename is not needed: all translates are counted without a cutoff, and all witness radii are used as exact rationals.

**Scope and novelty.** All requested mathematical checks (a)–(d) were completed. No search completeness, optimality, Lean formalization, or global priority claim is made. Did this referee find something new? **No:** it verifies the supplied construction with its own checks. The candidate exceeds the public printed number 1.7040280575, but the current live table still displays Lin's older bound; [PR #350](https://github.com/teorth/optimizationproblems/pull/350) is open. [the prior-art note](../PRIOR_ART.md) distinguishes these facts and records the bounded source checks. Predictive baselines and SBS do not apply to this exact mathematical certificate.

**Reproduction.** Run `nice -n 10 python3 referee_check.py` from this folder, without `-O`, using Python 3.9 or newer. Fresh results go to ../release_validation/referee-results.json and a regenerable per-witness table. The supplied completed run used one CPU process; its aggregate exact_results.json and referee_run.log are retained. That check took 2.41 seconds. The source references and arithmetic above establish the mathematical reduction in addition to the program's checks.

**Caveats or failures affecting the lower bound:** none.

VERDICT: HOLDS
