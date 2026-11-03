# C47 half-cell candidate lower bound — unrefereed

For the centred Hardy–Littlewood maximal operator over axis-parallel squares in the plane, the frozen certificate gives the **candidate, unrefereed** bound

\[
C_{47}\ge q:=\frac{215956002657486428307163448091951082893881}{126800499112387565339223240212480000000000}
=1.7031163455127832\ldots>\frac{170311}{100000}=1.70311.
\]

This decimal claim is rounded down: `floor(100000*q)/100000 = 1.70311` (on the 1/10000 grid the largest lower value is 1.7031). No stronger rounded display is asserted.

`certificates/half59.json` contains **59 positive rational atoms and 559 explicit rational rectangle witnesses**, SHA-256 `b4d88847ef0c41577213a34ef6fda3d0d9b52b672f6ce20e998b006a2031ba99`. The exact verifier is copied unchanged from c47r1: **separately written (same agent)**, SHA-256 `f01475b149795e25821fc5c434ee2d535b941967897c758dbdc1391e8ae3edfe`. This is further hole-filling on Tomar's measure: the same insertion-and-refinement operation as his hf.py, applied by our own search scripts. No novelty claim is made.

## 1. A finite witness

Write Q(x,r) for the closed square of centre x and radius r in the sup norm; its area is 4r². Let μ be the periodic positive atomic measure specified by the certificate, and let λ>0. A witness consists of a rational box B=[a,b]×[e,f], a positive rational radius r, and a positive-area rectangle R=[u,v]×[s,t]. Let S be all periodic atoms in B. The checker verifies

\[
\mu(S)>4\lambda r^2,\qquad
u\ge b-r,\quad v\le a+r,\quad s\ge f-r,\quad t\le e+r.
\]

For every x∈R and every p∈S, the inequalities imply |p−x|∞≤r. Thus S⊆Q(x,r), and the average atomic mass of that square exceeds λ. This argument permits degenerate boxes containing a line or a single atom.

## 2. From the periodic measure to integrable functions

Let C=[0,Px)×[0,Py), and let R₁,…,Rₖ be finitely many validated witnesses clipped to C. Let U be the union of their period translates, A=|U∩C|, and m=μ(C). Put s₀=minᵢ(μ(Sᵢ)−4λrᵢ²)>0 and Rmax=maxᵢrᵢ. Choose

\[
0<\varepsilon\le\min\left(\frac12,\frac{s_0}{16\lambda(2R_{\max}+1)}\right).
\]

For every witness, the increase in required square mass after replacing rᵢ by rᵢ+ε is at most

\[
4\lambda(2r_i\varepsilon+\varepsilon^2)
\le4\lambda(2R_{\max}+1)\varepsilon\le s_0/4.
\]

Choose an integer h with h min(Px,Py)>Rmax, and truncate μ to the N×N block [0,NPx)×[0,NPy), N>2h. Replace each retained atom of mass mₚ at p by mₚ/(4ε²) times the indicator of Q(p,ε). The resulting function f is nonnegative, integrable, and has norm N²m, even if smeared squares overlap.

If x belongs to a translate of a witness rectangle in one of the (N−2h)² inner cells, every atom of its S lies inside the truncated block: its distance from x is at most rᵢ≤Rmax. The square Q(x,rᵢ+ε) contains the smeared mass of Sᵢ and has average strictly greater than λ by the preceding inequality. Consequently

\[
\lambda\,|\{Mf>\lambda\}|/\|f\|_1
\ge \frac{\lambda A}{m}\left(\frac{N-2h}{N}\right)^2.
\]

Letting N tend to infinity proves c₂≥λA/m. Boundaries of the half-open period cells have zero area. The constructed strict superlevel subset also proves the bound for the non-strict convention on the C47 page. This is Tomar's general finite-periodic rectangle formulation, Lemma 6.2 following Lin's truncation-and-smearing argument. The self-contained argument here checks its required strict margins.

## 3. Exact arithmetic performed by the verifier

The verifier checks λ,Px,Py>0, positive atom masses, unique atom positions in C, positive witness radii, and rectangle containment in C. It computes the mass of every S directly from the periodic measure, without the producer's finite window or prefix sums. For an atom (x,y,mₚ) in C, its number of translates inside B is exactly

\[
\max(0,\lfloor(b-x)/Px\rfloor-\lceil(a-x)/Px\rceil+1)
\max(0,\lfloor(f-y)/Py\rfloor-\lceil(e-y)/Py\rceil+1).
\]

It multiplies these counts by mₚ, sums, and checks the strict mass margin and the four containment inequalities in §1 as rational comparisons.

To compute A, it sorts the rational x endpoints of the retained rectangles. On each consecutive vertical slab it merges the active rational y intervals and multiplies their total length by the slab width. The sum is the exact union area. All decisions, areas, masses, and comparisons with the claimed bound use Python's exact fractions. The printed decimal is informational.

The producer derives candidate boxes from Tomar's floating C evaluator, reconstructs masses and dyadic radii exactly, and selects a small interval cover using a prefix-maximum tree. The final artifact uses full reconstructed rational rectangles, without inward grid quantization. Neither completeness of candidate selection nor correctness of pruning is needed for validity: the verifier checks the retained witnesses and computes their area anew. It imports no producer or search code.

## 4. Applying the lemma to the fixed 59-atom half-cell

The exact period and level are

\[
P_x=164377561597/50000000000,\qquad
P_y=2744174966813/1000000000000,\qquad \lambda=1.
\]

`extract_half.py` retains precisely the parent atoms with `0 <= y < parent Py/2`, and halves only the parent vertical period. It preserves every selected rational coordinate and mass byte-for-byte. The selection has 50 inherited atoms and 9 added atoms. No further mass, coordinate or period tuning was done. The frozen 117-atom parent and exact zero-based selection indices are retained.

The verified cell mass and rectangle-union area are

\[
m=131978281545501/25000000000000,
\]
\[
A=647868007972459284921490344275853248681643/72057594037927936000000000000000000000000.
\]

Their quotient is exactly q above. The minimum strict witness mass slack is `3075015278326308311/115292150460684697600000000000000`. All 559 radii, periodic masses and containment inequalities pass the separately written (same agent) verifier. Tomar's unchanged v5 `check_exact2.py` enumerates **33,356** rectangles and returns **exactly the same rational q**. The bounded box reach is `1396/125`, and the radius denominator is `2^40`. Enumeration completeness is not needed to establish this lower bound.

All seven corruption controls reject with exit status 1: claim raised above q by 10^(-30), heavy mass reduced, oversized radius, expanded rectangle, atom outside the cell, zero mass, and duplicate atom. Receipts are `logs/half59-exact.json`, `logs/rejection-controls-half59.json`, and `certificates/half59-measure.check2.json`.

The explicit finite instance uses **h=2**, **N=2,147,177**, and

\[
\varepsilon=3075015278326308311/12117811236023199334400000000000000.
\]

The largest witness radius is `765408339251/274877906944`. It exceeds the new vertical period, so h=1 from the earlier packet cannot be reused; h=2 satisfies the strict boundary-distance condition. The finite ratio is exactly

\[
995633165425366706521571823654161860176724576687386449/584597099083230950188146828158179225811025920000000000
=1.7031100000097934\ldots>170311/100000.
\]

The finite function has L1 norm `608468587060572181137038829/25000000000000` and is encoded by N, the period cell and the smear radius, without listing its `272011775090411` atoms. Overlapping smear squares do not alter its norm. `logs/half59-finite.json` gives all parameters. Section 2 proves the ratio for integrable functions.

## 5. Construction, half-cell measurement, and provenance

The construction is **further hole-filling on Tomar's measure: the same insertion-and-refinement operation as his hf.py, applied by our own search scripts**: locate uncovered holes, insert small positive masses, and refine the configuration. Tomar's 50-atom measure itself refines Lin's weighted lattice. In the preceding c47r1 search our scripts duplicated the seed vertically, inserted sparse atoms, and numerically refined the configuration, applying Tomar's hole-filling idea.

The decisive measurement is the lower half-cell. The former 117-atom certificate gives 1.7031062130924713…, whereas its **59-atom lower half repeated with the half vertical period** gives the exact certified **1.7031163455127832…**, which is larger. The 59 atoms consist of the 50 inherited atoms in that half and 9 hole-filling additions; their inherited parameters were refined in c47r1 and are frozen here. Thus the improvement is already present in a single period. No novelty or optimality claim is made.

The bounded provenance experiment starts from Tomar's own published rational 50-atom measure, converted directly to numeric JSON, and executes his unchanged v5 `hf.py` with its default settings (20 rounds, grid 500, maxit 400, 6 tries), seed 1103, without a reach override. The objective is observed but not modified. It reached 1.7027237336 in 5.99 CPU-hours and stopped during the initial 50-atom polish, never inserting atoms. Its final best observed and best accepted values, CPU use and termination condition are reported in **README.md** and `logs/hf-summary.json`. This floating experiment does not replace the exact certificate, and a timed failure to reach q would not establish a new method. The construction attribution remains further hole-filling on Tomar's measure: the same insertion-and-refinement operation as his hf.py, applied by our own search scripts, regardless of the bounded replay's outcome.

The finite-periodic rectangle theorem used above is **Tomar's Lemma 6.2, following Lin**. The analytic explanation is included for inspection, and the executable witness verifier is separately written (same agent). The candidate remains unrefereed.

## 6. Attribution and scope

See [CREDIT.md](CREDIT.md) for Tomar's v5 source at commit `3af09fc359ce262f4a7f63d34b0d97e6d4d95d1a`, his paper and supplement, and Lin's source. Fresh raw copies of `hf.py` and `check_exact2.py` match the unchanged retained upstream files. Tomar's published exact 50-atom ratio, 1.7027237335962937…, was replayed in this job. His upper bound 3.59123 is attributed to his paper and source; it was not reverified here. No Lean rebuild was performed.

[REPRODUCE.md](REPRODUCE.md) gives exact commands. [TABLE_RECORD.md](TABLE_RECORD.md) contains unfiled rows crediting both Tomar's bounds and this candidate built by our scripts applying his hole-filling idea. This job makes no commit, push, PR, post or message and does not edit c47r1 source, proof, data or certificate files.
