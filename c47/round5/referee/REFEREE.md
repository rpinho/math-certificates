# Clean-room AI referee: C47 ≥ 1.7048221231

The supplied bound holds. The periodic ratio recomputed by the referee is exactly the claimed rational number, and the supplied finite integrable function gives a ratio strictly above the requested decimal. All four requested items were completed; there are no mathematical caveats or failures.

This review uses only the permitted producer documents/data and a checker written here from the definition. No producer or predecessor verifier, search code, compiled library, Tomar code, or Doldrums code was read, imported, copied, or executed. The candidate certificate is `../certificates/final.json`, SHA-256 `c37382e18f55d07f442fe65b259d4e04d195f696d7ef06aed698143cfbe00ae3`. The referee’s own computation is in `check_certificate.py`; its results are in `CHECK_RESULTS.json` and `check.log`.

## (a) Definition match and periodic-to-finite lemma

The [live table](https://teorth.github.io/optimizationproblems/constants/47a.html) was fetched on 2026-11-09. The definition below is quoted verbatim from its [raw source](https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/47a.md), saved as `sources/47a.md:4–25` (Apache-2.0, license saved as `sources/table-LICENSE`):

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

Thus the target concerns integrable functions on the plane, centered **squares**, and the weak-type area-to-L1-mass ratio. An infinite periodic atomic measure is an intermediate construction, not itself an admissible L1 function. Section (c) supplies that passage explicitly at level 1. Strict superlevel membership obtained below also implies the table's non-strict membership, so there is no level-set convention mismatch.

The precise result used is **Tomar, v5, Section 6, Lemma 6.2**, in [Bounds for the weak type (1,1) constant of the centred maximal operator over squares](https://doi.org/10.5281/zenodo.23716077), page 8 (consulted PDF identified in sources/SOURCES.md). Its statement, with notation retained, is: let μ be a positive atomic measure periodic under Pxℤ × Pyℤ, with finitely many atoms in C=[0,Px)×[0,Py), and λ>0. Let U comprise all lattice translates of finitely many rectangles Ri. For each i, require a finite atom set Si and a radius 0<ρi<√(μ(Si)/(4λ)), with Ri⊆∩p∈Si Q(p,ρi). Then c2≥λ|U∩C|/μ(C). Positivity and local finiteness are specified immediately before Lemma 6.1. I read Lemmas 6.1–6.2 and the truncation-and-smearing proof.

Tomar explicitly follows Lin. Lin's [mathematical account, Sections 4–6](https://github.com/CoolRmal/centered-maximal-constant/blob/72c022ba09032b522c878cca2f9b6c68217d77ea/docs/PROOF.md) (consulted lines 69–130; omitted source hash in sources/SOURCES.md) gives finite lattice witnesses, normalized square smearing, interior-cell coverage, and the limiting area/mass inequality. I also read the definition and introduction of Lin's [c2 < 4 manuscript](https://coolrmal.github.io/assets/papers/c2-less-than-4.pdf) (consulted PDF identified in sources/SOURCES.md); it concerns the upper bound. The lower-bound antecedent cited as [8] by Tomar is Lin's formalization and accompanying mathematical account, not the upper-bound paper [7]. No existing formal proof was executed here.

Every hypothesis is met:

| Hypothesis | Check for this certificate |
| --- | --- |
| Positive periods | Px=328,944,569,115,789/100000000000000 and Py=274626500374759/100000000000000 are strictly positive. |
| Positive, locally finite periodic atomic measure | Exactly 392 positive rational masses at distinct points in C. Extend them over the specified lattice; positive periods and finitely many base atoms imply finitely many atoms in every bounded set. |
| Correct fundamental-cell mass | All base coordinates satisfy 0≤x<Px and 0≤y<Py; μ(C) is their sum, 16531017364377/3125000000000>0. |
| Positive level and finite rectangle family | λ=1 and exactly 4735 rectangles, all of positive area and contained in the closed cell. |
| Finite witness atom sets | Si is all periodic atoms in the ith bounded closed box Bi; these were counted without using the producer's search reach. |
| Strict radius inequality | All 4735 satisfy ρi>0 and μ(Si)>4ρi². The minimum positive slack is given in (b). |
| Containment | For every point of Ri, its centered square of radius ρi contains the entire Bi, hence every atom of Si. All endpoint inequalities passed. |
| Area of the periodic union in C | Nonzero cell translates of the clipped rectangles can meet C only on its boundary. These sets have zero Lebesgue area. Therefore |U∩C| equals the recomputed area of the base rectangle union. |

The data checks implementing these hypotheses are `check_certificate.py:106–170`. In particular, the argument uses no symmetry assumption, equal-period assumption, or completeness of a box search.

## (b) Every witness and the exact ratio

The checker parses all mathematical data directly as `fractions.Fraction`. For a base atom (xj,yj) with mass mj and a box B=[a,b]×[c,d], its translated copies in B have exactly the integer indices

\[
\left\lceil\frac{a-x_j}{P_x}\right\rceil\le k\le
\left\lfloor\frac{b-x_j}{P_x}\right\rfloor,\qquad
\left\lceil\frac{c-y_j}{P_y}\right\rceil\le l\le
\left\lfloor\frac{d-y_j}{P_y}\right\rfloor.
\]

The product of the two nonnegative index counts, times mj, is its contribution to μ(B). Summing over all 392 base atoms gives the full closed-box mass. This includes atoms on box boundaries and counts each periodic image once. No floating approximation, tolerance, image-window cutoff, stored witness mass, or producer calculation is used (`check_certificate.py:138–152`). Across all witnesses there are 1,070,846 atom-image incidences, including 30,022 incidences on box edges; individual boxes contain between 1 and 1372 atoms.

For every witness R=[u,v]×[s,t], the referee checked:

\[
0\le u<v\le P_x,\quad 0\le s<t\le P_y,\quad r>0,\quad
\mu(B)>4r^2,
\]
\[
u\ge b-r,\quad v\le a+r,\quad s\ge d-r,\quad t\le c+r.
\]

The last four inequalities imply B⊆Q(z,r) for every z∈R. They certify more than just containment of the atoms in B. All **4735/4735** witnesses satisfy all these requirements.

The minimum exact mass slack is

\[
\delta=\min_i(\mu(B_i)-4r_i^2)
=\frac{34802060175181125102274071}{129807421463370690713262408230502400000000000000}>0,
\]

approximately 2.68105319271×10⁻²². It is attained at zero-based witness 2994 (its box begins at `../certificates/final.json:46884`). This agrees with `sources/producer-proof.md:38`.

For the union area, I used the standard vertical-slab method (`check_certificate.py:43–91`). All rectangle endpoints were converted exactly to integers using a common denominator of 112589990684262400000000000000 on each axis. Between successive distinct x endpoints, the active rectangles are constant. Sorting and merging their y intervals gives the section length; multiplying by the slab width and summing gives the union area. There are 8515 slabs and at most 493 active rectangles. This counts overlap only once and discards only zero-area edges.

| Quantity | Claimed in `sources/producer-proof.md:36–37` | Recomputed by the referee |
| --- | --- | --- |
| μ(C) | 16531017364377/3125000000000 | 16531017364377/3125000000000 |
| A=|U∩C| | 57160787529186565434927719505838181711244340833364808847853/6338253001141147007483516026880000000000000000000000000000 | 57160787529186565434927719505838181711244340833364808847853/6338253001141147007483516026880000000000000000000000000000 |
| q=A/μ(C) | 57160787529186565434927719505838181711244340833364808847853/33528886534937259000645393217902994011665203200000000000000 | 57160787529186565434927719505838181711244340833364808847853/33528886534937259000645393217902994011665203200000000000000 |

Each equality is exact, not agreement to a displayed precision. For orientation,

\[
q=1.7048221231452095305513160686588723524842222041693437806685094244\ldots.
\]

The witness union leaves approximately 0.0153074646712092 of the cell's area uncovered. That is not a claim about the complement of the full maximal superlevel set; only the certified union is needed.

## (c) The finite integrable instance

I checked `sources/producer-proof.md:12–27` and every mathematical parameter in `../producer_logs/final-finite.json:4–11`, without relying on the producer's finite-instance program. The supplied values are

\[
h=2,\quad N=301674819865,\quad
R_{\max}=\frac{12849444897914546765}{4611686018427387904},
\]
\[
\epsilon=\frac{34802060175181125102274071}{13650669794247065816537359446337126400000000000000}>0.
\]

The largest witness radius is approximately 2.78627921471035. Exact comparison gives h min(Px,Py)>Rmax. For an inner-cell index h≤k,l<N−h and a point z in that cell's closed witness union, every needed atom lies within radius Rmax of z and hence strictly inside the outer block's upper boundary and beyond its lower boundary. Thus it is retained in [0,NPx)×[0,NPy). The actual image indices counted above also provide a direct check: all lie in −1≤k≤1 and −1≤l≤2, so translating by any inner-cell index places their indices in 0,…,N−1.

Retain precisely N² copies of each base atom, and define

\[
f(z)=\sum_{k,l=0}^{N-1}\sum_{j=1}^{392}
\frac{m_j}{4\epsilon^2}\,\mathbf 1_{Q(p_j+(kP_x,lP_y),\epsilon)}(z).
\]

All smeared squares are kept in full. This finite sum is nonnegative, bounded, measurable and compactly supported, so f∈L1. Integrating each summand gives mj regardless of overlaps or support extending beyond the block. Consequently,

\[
\|f\|_1=N^2\mu(C)
=\frac{60177992736667633653561800669518833}{125000000000},
\]

and the finite construction contains exactly 35675017200707437858344200 atomic summands before smearing. Both numbers match the log. The function is specified by a finite formula; enumerating this enormous block is unnecessary.

The exact checks give 0<ε≤1/2 and

\[
4(2R_{\max}+1)\epsilon<\delta.
\]

For each witness,

\[
4(r_i+\epsilon)^2-4r_i^2
=8r_i\epsilon+4\epsilon^2
\le4(2R_{\max}+1)\epsilon<\delta
\le\mu(B_i)-4r_i^2.
\]

Hence μ(Bi)>4(ri+ε)². The checker also compares this inequality **directly for all 4735 witnesses** (`check_certificate.py:175–182`). If z is in a retained translate of Ri, Q(z,ri+ε) contains every full smeared atom belonging to Bi. Its average of f exceeds 1. The (N−2h)² interior witness unions have disjoint interiors, so their areas add and yield

\[
\frac{|\{M_2f\ge1\}|}{\|f\|_1}
\ge q\left(\frac{N-2h}{N}\right)^2
=\frac{578007958689239466612634605872912728291646694993967246195937507629552189562609757}{339042971614074466964801846249032273651166749002975200936439316480000000000000000}.
\]

This matches `../producer_logs/final-finite.json:11` and `sources/producer-proof.md:40` exactly. Its decimal expansion begins

\[
1.7048221231000000000005908082355583061266753919624593819828741998\ldots.
\]

Subtracting the requested target 17048221231/10000000000 gives the exact positive number

\[
\frac{200309379837756205244409166590255918827923953805770874609757}{339042971614074466964801846249032273651166749002975200936439316480000000000000000}
\approx5.9080823555830613\times10^{-22}.
\]

Therefore this finite function proves the requested decimal lower bound. Moreover, the same h and ε work for every integer N>2h. Taking N→∞ proves the stronger C47≥q claimed in `sources/producer-proof.md:42`; this is a limit of inequalities for admissible finite functions, not an application of the L1 inequality to an infinite periodic measure.

## (d) Periods, boundary conventions, duplicates, rounding and scope

**Half-open cell.** `sources/producer-proof.md:5` explicitly defines C=[0,Px)×[0,Py), distinguishes its closure, and assigns each base atom exactly one lattice cell. Lines 10, 12 and 17 use the same convention for cell mass and finite-block mass; lines 35–36 give the actual periods and mass. This wording and its use are correct. The present certificate actually has no atoms on any cell edge, but the proof also correctly handles atoms on the left or bottom boundary. Every base atom lies in C; no normalization by wrapping an outside atom was silently performed. All 392 positions are distinct, hence there are also no duplicates modulo the period lattice.

**Closed boxes versus cell mass.** Closed witness boxes must include edge atoms; the exact translation counts do so. Closed witness rectangles can overlap on cell edges without affecting Lebesgue area. Those zero-area overlaps cannot be used to ignore atomic mass on a fundamental-cell boundary; that is precisely why the mass convention remains half-open. The finite argument retains entire smeared squares rather than cropping them at a cell boundary. No boundary correction to their integral is needed.

**Period and radius metadata.** Positive unequal periods are allowed by Lemma 6.2. The stored `reach` and `D` are producer metadata, not hypotheses: actual rational radii, boxes and atom translations were checked directly. The proof needs no assertion that these are minimal periods, largest allowable radii, or all possible witnesses.

**Rounding.** Exact arithmetic gives floor(10¹⁰q)=17048221231. Thus 1.7048221231 is a valid ten-decimal downward truncation. The next ten-decimal number, 1.7048221232, exceeds q and is not established by this certificate. The finite log's floating display at `../producer_logs/final-finite.json:12` alone cannot reveal the small strict margin; the exact fraction on line 11 does, and was checked above.

**Scope and novelty.** No requested item remains unchecked. There are no mathematical caveats or failures to list. This is a rational-arithmetic and written-proof review using the referee’s own checks, not a new formalization or an optimality result. Did this referee job find something new? **No:** it verifies the supplied candidate rather than producing a new measure or bound. Public context and the distinction between the deployed table and open PRs are documented in [the prior-art note](../PRIOR_ART.md); no exhaustive priority claim is made.

Reproduce from this directory with Python 3.9+ and its standard library:

```sh
python3 check_certificate.py --certificate ../certificates/final.json --finite ../producer_logs/final-finite.json --out ../release_validation/referee-results.json
```

The actual run used the shared science Python, one CPU process, and took 9.34 seconds. It inherited nice 15; requesting nice 10 was denied by the operating system, so it ran at the lower priority. No producer code or third-party computational checker is required. This execution detail does not qualify the mathematical verdict.

VERDICT: HOLDS
