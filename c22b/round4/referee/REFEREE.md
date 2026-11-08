# Clean-room referee of C22b ≤ 7.087559024

The requested upper bound **holds**. Its own calculations and the argument below establish the specified family of closed C¹,¹ curves, thickness at least 1, knot type T(2,1324n+3) up to mirror, and length less than 7.087559024·1324n+150 for every integer n≥1.

The input is `../candidate_high/CONSTRUCTION.json`; the sharper coefficient is in `BOUND.json:4`. I read only the permitted data, prose, previous referee prose, and selected saved logs. I did not read, import, run, or copy any supplied Python or certificate partitions. The referee’s own programs here are `geometry.py`, `scalar.py`, `covers.py`, `caps_contact.py`, and `topology.py`. Their numerical proofs use python-flint Arb at 160 bits. Displayed decimal endpoints below are rounded outward; the more detailed results are in the corresponding JSON files.

## (a) Definition match

The [live official page](https://teorth.github.io/optimizationproblems/constants/22b.html) and its [raw Markdown](https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/22b.md) were fetched on 2026-11-08. The saved copies are `table22b.html` and `table22b_raw.md`; the repository's Apache-2.0 license is saved as `table_license.txt`. The definition, verbatim from the raw Markdown, is:

> $C_{22b} = b_{o}$ is the largest constant for which one has an inequality
> $$ L \geq b_{o} C $$
> for all knots that admit an [alternating](https://en.wikipedia.org/wiki/Alternating_knot) diagram, where $L$ is the ropelength of a knot (or link) with [crossing number](https://en.wikipedia.org/wiki/Crossing_number_(knot_theory)) $C$.
> The _ropelength_ $L$ is the infimum over all embeddings of the knot (or link) of the ratio of the contour length of the knot to its thickness. The _thickness_ is defined as the radius of the smallest circle that passes through any three points on the knot (where collinear points yield an infinite radius). Colloquially, the ropelength is the least amount of rope required to tie a specific knot in a rope of unit radius. See [CKS2002] for the full definition.

Thus thickness is a **radius**, and the required nonlocal distance is 2. “Smallest” includes the infimum and coalescing-point limits, as in CKS. Write ℓ for embedding length, τ for thickness, and Rop(K)=inf ℓ/τ over embeddings of a knot type K. The table quantity is inf Rop(K)/C(K) over the alternating class. The family below consists of knots admitting alternating diagrams, so it is admissible with or without the parenthetical extension to links. The physical projection need not itself be alternating or crossing-minimal. A family limit bounds this infimum; no finite member has to attain the limiting coefficient.

The rendered table still displays the proposed 7.2012719. [PR #324](https://github.com/teorth/optimizationproblems/pull/324), read live, proposes 7.090412. The task identifies [PR #342](https://github.com/teorth/optimizationproblems/pull/342), Doldrums / SCiEL / CPIL lab MBZUAI, as the newer public proposal 7.087662112. Attempts to fetch #342 in this job timed out or returned a GitHub error page, so I do not claim a live recheck of that PR. This access limitation does not enter the mathematical referee result. See `PRIOR_ART.md` for the scoped literature check. No public priority claim is made here.

## (b) Thickness over the entire closed curve

I use [Cantarella–Kusner–Sullivan, Lemmas 1–2](https://www.jasoncantarella.com/downloads/papers/ropelength/ropelen.pdf): for an embedded C¹,¹ closed curve, τ is the minimum of the infimal curvature radius and half the infimal double-critical self-distance, and also the infimum of tangent-point radii. Embeddedness is proved along with the distance exclusions, before applying this characterization.

**Derivatives.** Put q=h/s, k=R/s, C=r cos v, D=r sin v, A=R−C, B=qD. In the cylindrical frame rotating by u/N, after division by λ, position, velocity, and acceleration are

    position = (A, B, hu/N−kD),
    velocity = (−C′−B/N, qD′+A/N, h/N−kD′),
    acceleration = (−C″−2qD′/N−A/N²,
                    qD″−2C′/N−B/N², −kD″).

The phase-dependent terms used are

    C′ = r′cos v − r sin v v′,
    D′ = r′sin v + r cos v v′,
    C″ = (r″−r(v′)²)cos v − (2r′v′+rv″)sin v,
    D″ = (r″−r(v′)²)sin v + (2r′v′+rv″)cos v,
    v′ = 1+Σ k p_k cos(ku),  v″ = −Σ k² p_k sin(ku).

The r derivatives are the derivatives of all six cosine orders. These formulas are implemented in `geometry.py:16–35`. Series differentiation of these same full expressions supplies higher derivatives used in centered enclosures and length integration; the phase terms remain present there too.

**Curvature.** Complete interval subdivision of [0,44/7] proves

    |X′|⁶ − ρ² |X′×X″|² > 0

with ρ=1.98 for the outer strand and ρ=1.44 for the inner strand (`covers.py:6–19`, `cover_curvature.json`). The covering period is valid because 44/7>2π and one minor period is a common screw isometry. Natural interval evaluation is supplemented by the mean-value enclosure F(m)+F′(cell)(u−m). All speeds are positive. The respective full-period lower bounds use 256 and 76 leaves.

For comparison, `../PROOF.md:113–120` claims curvature radius >1, rather than a tight numerical minimum. My enclosures for the infimal body curvature radii, using a single exact-phase evaluation for each upper endpoint, are

| Part | Referee enclosure of its infimal curvature radius |
|---|---:|
| Outer body | [1.98, 1.986541448753726] |
| Inner body | [1.44, 1.446688670786879] |
| Outer/inner connectors | 7.5 / 31.5 exactly |
| Lower outer semicircle | [7.56636538050878436, 7.56636538050878437] |
| Lower inner semicircle | [3.01095362967353650, 3.01095362967353651] |
| Upper semicircles | [4.22156854536413939, 4.22156854536413940] |
| Straight extensions | infinite |

At joins the tangent is continuous and one-sided curvatures are bounded; there is no corner curvature. Hence the entire closed curve's infimal curvature radius is in **[1.44, 1.446688670786879]**, in the C¹,¹ sense. Upper sample enclosures and phases are in `caps_contact.json`.

**Body distance reductions.** The separately bounded speeds satisfy V_outer<1.928951113071 and V_inner<0.331859184841. Thus 1.5V_outer<2.894<π and 9V_inner<2.987<π. With curvature ≤1, an arc of length ℓ<π cannot be double-critical: integrating

    T(t)·(T(0)+T(ℓ)) ≥ cos t+cos(ℓ−t) > 0

contradicts a chord perpendicular to both endpoint tangents. Its chord also has positive projection on the midpoint tangent, at least 2 sin(ℓ/2), excluding self-intersection.

For |δ|≥9 the height gap of any same-bundle pair exceeds 2.2282138392838805, using λ(9h/N−2a_max R/s). The remaining outer-self domain [0,44/7]×[3/2,9] and outer/inner domain [0,44/7]×[−9,9] are covered from scratch in `covers.py:21–40,60–64`. Natural or centered interval evaluation proves squared distance >4 on every leaf. The centered gradient differentiates both moving points, including the rotating frame; its extra skew rotation has zero dot product with the chord.

| Full distance domain | Referee lower bound for squared distance | Distance leaves |
|---|---:|---:|
| Same-bundle outer self, nonshort range | 4.00000001522790 | 1,762 |
| Same-bundle outer/inner | 4.00000000005039 | 179,184 |
| Body/connector interfaces, after symmetry | 4.00000000204870 | 1,398, plus 12 short-arc leaves |
| Lower outer connector / inner semicircle | 4.58835758766350 | 32 |

These are conservative bounds from the finite covers, not estimates of the true minimum. They exclude all relevant pairs, not only sampled or stationary pairs.

**Tight cross-bundle separation.** Opposite axis points with axis-parameter difference η have squared separation

    2R²(1+cos η)+h²η² ≥ 4R²+(h²−R²)η² ≥ 4R²,

since h²−R²>299.7588. The radius polynomial has its maximum at zero: factoring its derivative by sin u and using |U_(k−1)(cos u)|≤k gives

    a₁−Σ_(k=2)^6 k²|a_k| = 0.000638443145 > 0.

Thus a_max=a(0)=1.932410534396 exactly. The inner radius is positive and <0.078727, so it is also bounded by a_max. Consequently all opposite-bundle distances are at least

    λ(2R−2a_max) = 2.000001999997999998.

This value is attained by the two outer endpoints at u=0, so it is also the minimum opposite-bundle body distance. The source's looser interval lower bound is 2.000001973435384954… (`../README.md:143` and `../producer_logs/candidate_high_replay.json`). The **2.000003999878… in the job prompt is not the selected λ=1.000001 candidate's value**. It should not be used for this geometry. The corrected figure still exceeds 2.

**Caps, interfaces, and exhaustion.** All connector geometry uses the actual modulated endpoint tangent. Independent scalar enclosures give

    X_outer = 1.000000999998999999,
    X_inner ∈ [3.01014067434766420, 3.01014067434766422],
    X_inner−X_outer > 2.010139674348,
    Z_inner > 2.098285210408,
    Z_outer−Z_inner−D_inner > 2.390761159914,
    Y_outer sqrt(3)/2 > 6.495183777501,
    upper semicircle plane distance > 5.364355652009.

The new semicircles start 2.1 above the highest connector. These separately verified inequalities imply the scalar cap separations in `../../round1/PROOF.md:263–330`. In detail:

- Different connectors or vertical lines have distinct constant X coordinates separated by more than 2. The lower outer semicircle is vertically more than 2 above every inner connector and semicircle. The two remaining lower outer-connector/inner-semicircle pairs have complete unit-square interval covers.
- A lower connector and its own semicircle near the attachment have vertical gap Q sin δ+D sin θ ≥ (2/π)(Qδ+Dθ). If the joined arclength is ≥π this is ≥2; otherwise use the short-arc exclusion. For the far half, the outer case uses D_outer/2>2 or the opposite-Y gap; the inner case uses X_inner>2. The other endpoint is its reflection.
- The upper semicircle planes are parallel and more than 2 apart. Each attached vertical extension lies in its semicircle's plane. Connector/semicircle pairs have vertical gap ≥2.1. A connector and its own extension, or a semicircle and its own endpoint ray, uses the same joined-arc dichotomy. The far semicircle half has horizontal separation ≥D_upper>2.
- A single circular piece of radius ≥1 and arclength separation ℓ≤π radius has chord ≥2ℓ/π. Single straight pieces have chord ℓ. Again the short-arc/distance dichotomy covers their self pairs.
- Semicircles and upper vertical extensions are more than 2 outside the body slab. Only the connector interfaces remain. For body phase u≤−8 their vertical gap exceeds 2.2281942734873945. On [−8,0]×[0,16], I checked all eight choices with body bundle c=+1; the exact π rotation around Z gives the other eight choices. Matching-index leaves may use the actual joined arc bound −u_min V_r+l_max<π. Both actual connector lengths are <16 (11.780964655715197 and 2.099840065068977), so there is no unexamined connector tail.
- The exact X-axis rotation gives the lower interfaces. Opposite-end caps lie in opposite exterior half-spaces and are separated by H_n≥662.00163538553988>2.

The 20 pieces have 210 unordered pairs including self pairs. The preceding cases cover body/body 10, body/lower 24, body/upper 40, lower/lower 21, upper/upper 55, and lower/upper 60. This is a geometric exhaustion, not a reliance on the producer's reported count. Nonlocal positive distances and positive short-arc chords prove embeddedness, and the same exclusions prove **half the infimal double-critical self-distance ≥1** for the whole curve.

**Tangent-point upper enclosure and global conclusion.** At the permitted exact contact phases u=4536120203/10⁹ (outer), w=781958743/250000000 (inner), I obtain

    distance ∈ [2.00000199980471854144, 2.00000199980471854146],
    tangent-point radius ∈ [1.00000099990235927617,
                            1.00000099990235927619].

These agree with `../producer_logs/candidate_high_contact.json:7–8`. The tangent-point formula used is |d|²/(2 sqrt(|d|²−(d·X′)²/|X′|²)). These selected points are **not asserted to be exactly double-critical**: their chord-dot-tangent values are about 1.27×10⁻⁸ and 1.47×10⁻⁸. Nevertheless they rigorously bound thickness from above. Since the curvature radius is ≥1.44, CKS then also bounds half the infimal double-critical distance from above by this tangent-point radius. For every n≥1, the whole closed curve therefore satisfies

    inf curvature radius ∈ [1.44, 1.446688670786879],
    (inf double-critical distance)/2
        ∈ [1, 1.00000099990235927619],
    τ ∈ [1, 1.00000099990235927619].

The required lower bound 1 holds. No global minimizer is inferred from the selected contact alone.

## (c) Body length and cap term

`scalar.py:48–65` integrates the norm of the full modulated velocity, with λ included. On each of 512 cells in [0,2π], Arb series give coefficients at the midpoint through degree seven and bound the degree-eight coefficient on the entire cell. For half-width d, the remainder is bounded by

    (2d⁹/9) sup_cell |f⁽⁸⁾/8!|.

Odd polynomial terms integrate to zero. Positive speed ensures the square-root series represents the actual norm. Arb encloses π, endpoints, coefficients, and remainders. This is a Taylor theorem enclosure, not a heuristic quadrature error estimate. The combined coefficient remainder is <9.10×10⁻²¹.

The referee’s full-period speed integrals are

    I_outer ∈ [12.09067079234877660435, 12.09067079234877660445],
    I_inner ∈ [2.084447254378702151703, 2.084447254378702151705].

There are two copies of each radius and 331n complete minor periods. Thus

    ℓ_body = 662n(I_outer+I_inner),
    ℓ_body/(1324n) = (I_outer+I_inner)/2
      ∈ [7.08755902336373937805, 7.08755902336373937815]
      < 7.087559024.

This agrees with the producer's [7.087559023364 ±3.23×10⁻¹³] (`../README.md:16`). No additional thickness normalization or factor of two is missing.

For actual endpoint angles θ_± and radii D_±,D, the complete cap length is

    E = 4(Q₊θ₊+Q₋θ₋)+π(D₊+D₋+2D)+4Zstar−2(Z₊+Z₋)
      ∈ [134.48117361686018859660, 134.48117361686018859662]
      < 150.

It agrees with `../README.md:150`. Consequently the requested bound holds exactly as stated:

    ℓ_n < 7.087559024·(1324n)+150,  for every n≥1.

## (d) Knot type for every n, and an separately computed n=1 computation

**Physical projection.** I use F=X+Y/4 and depth G=Y−X/4, different from both the producer's 7X+Y and the previous referee's X+Y/5. The outer phase u=πx, x∈[0,662], parametrizes height. At that height the inner phase w is the unique solution

    H_inner(w)=H_outer(u),
    H_r(u)=u−(NR/(sh))r(u)sin v(u).

The separately proved strict height monotonicity justifies this inverse. SciPy proposes brackets only; both residual signs are checked in Arb. A whole height interval uses the two endpoint inverse brackets. Derivatives use dw/du=Z′_outer(u)/Z′_inner(w), with all phase terms included. The four crossing functions F_outer−F_inner, F_outer+F_inner, F_outer, F_inner exhaust all six pairs by bundle symmetry.

`topology.py:35–68` covers the entire phase interval. Every leaf either excludes zero by interval values, or has a derivative of fixed sign and verified endpoint signs proving zero or one simple root. Root brackets are disjoint and ordered. For every event, I check adjacent lanes and the nonzero depth difference before applying the Artin crossing rule. The simultaneous two-pair events involve disjoint lanes and commuting generators.

| Projection output | Referee result | Producer's different projection |
|---|---:|---:|
| Roots by the four functions | 650, 130, 296, 14 | 650, 130, 296, 12 |
| Events | 1,090 | 1,088 |
| Physical body crossings | 1,870 | 1,868 |
| Artin left-over / left-under signs | 1,561 / 309 | not used |
| Endpoint material permutation | identity | identity |
| Reduced color action | [[1,0],[1324,1]] | [[1,0],[1324,1]] |

These crossing counts are projection-dependent and are not claimed as minimal crossing numbers. Signs use increasing height as braid direction; they are not the writhe of the fully oriented closed knot. Data are in `topology.json`, `roots.json`, and `word.json`.

**Caps and projection alignment.** The separately computed lower nested-template crossings occur at outer-connector arclength in [9.16657098887217228,9.16657098887217230], strictly inside its 11.78096… length. The right connector-minus-circle depth is in [7.07215999275020606,7.07215999275020608]; the left has the opposite sign. The lower proper X rotation reverses these depths. Propagating the Fox rule gives its boundary colors

    (c₀,c₁,c₂,c₃)=(a,b,3b−2a,2b−a).

The upper semicircles have exactly one crossing, at supplementary angles: S₂ is over S₁ with depth gap in [11.29436160898679218,11.29436160898679220]. They impose c₂=c₀ and c₃=2c₀−c₁. Their constant-X connectors and extensions introduce no other crossings. These signs come from the actual circle formulas in `caps_contact.py:23–42`.

To match the cap X–Z projection to the body projection, replace body depth by G+F/4=(17/16)Y; depth differences at crossings do not change. In the original coordinates the family of height-preserving maps is (X,Y,Z)↦(X+tY/4,(17/16)Y,Z), 0≤t≤1. It starts with the common positive Y rescaling and fixes every body endpoint because Y=0 there. Keep the rescaled caps fixed in their exterior half-spaces. This is an endpoint-fixed body isotopy, so no extra braid is introduced by the projection change.

**Referee determinant.** Applying (x,y)↦(2x−y,x) for left-over crossings and its inverse for left-under crossings to four initial color variables gives

    M₄ = [ 651  −650   −12    12 ]
         [ 650  −649   −12    12 ]
         [ −12    12   651  −650 ]
         [ −12    12   650  −649 ].

Insert the lower-cap colors and impose the two upper relations. Both are −1327a+1327b=0. After quotienting the constant color, the integral Fox presentation is Z/1327Z. The determinant of the actual n=1 projected closed curve is therefore **1327**, without substituting a prespecified torus diagram.

**All-n identification.** Determinant alone would not identify the knot. On colors with c₀−c₁+c₂−c₃=0 put p=c₀−c₁, q=c₁−c₂. The computed body action is M=[[1,0],[1324,1]]. The lower cap is rational: its two crossings can be removed by adjacent boundary half twists, leaving the nested trivial cap. Their actions on (p,q) are each U=[[1,0],[1,1]], giving q=2p. Adding successive adjacent boundary half twists of the actual body word preserves rationality. The one-crossing upper cap is one such twist away from the nested cap; straightening it applies U, changing its q=−p relation to q=0.

A whole block returns all endpoint labels exactly. Since (M−I)²=0, the rational tangle before the final nested closure has action

    U Mⁿ U² = [[1,0],[1324n+3,1]].

In the boundary layout NW=c₀, NE=c₁, SW=c₃, SE=c₂, its color fraction is (NE−NW)/(NE−SE)=−p/q, hence −1/(1324n+3). [Kauffman–Lambropoulou's rational-tangle classification and color fraction theorem](https://arxiv.org/html/math/0311499) identify this with the vertical integer twist tangle, whose denominator closure is T(2,1324n+3), up to mirror. Rationality and endpoint alignment were established before applying the fraction classification.

The lower matching (0,3),(1,2) and upper matching (0,2),(1,3), with identity body permutation, also give one component directly. The usual two-strand diagram with k=1324n+3 crossings is alternating and reduced: its checkerboard graphs are a k-cycle and the parallel-edge dual, with no nugatory crossing. Reduced alternating diagram minimality gives C(T(2,k))=k. This proves the all-n knot and crossing-number claims, rather than extrapolating from n=1.

## (e) Uniform additive constant and valid limit

One block has u∈[0,2π·331] and axis angle change 2π·6. Every radius, phase correction, and derivative returns to its initial value; v changes by the integer multiple 2π·331. The whole block translates vertically by

    H=λ2π·6h ∈ [662.00163538553988383,662.00163538553988385].

Consequently endpoint positions relative to the top and all tangents are independent of n. The lower cap is fixed; the upper cap is only translated by nH. Both caps have the identical fixed total E above for every n≥1, and increasing n only strengthens opposite-end separation. No omitted connector grows with n.

For K_n=T(2,1324n+3),

    Rop(K_n) ≤ ℓ_n/τ_n ≤ ℓ_n,
    C22b ≤ Rop(K_n)/(1324n+3)
          < (7.087559024·1324n+150)/(1324n+3).

Letting n→∞ gives **C22b≤7.087559024** under the live definition. The extra three crossings and additive 150 have been handled with the correct signs and uniformity.

## (f) Closure, new modulation steps, and qualifications

The six cosine orders and four sine-phase orders preserve r(−u)=r(u), v(−u)=−v(u). Thus X is even and Y,Z are odd, proving the proper X-axis rotation used for the lower interfaces. At u=0, r′=0 and v=0. The endpoint is (λc(R−r(0)),0,0), and its tangent is computed with the **new v′(0)**. Independent endpoint tangent components include

    outer vertical unit component
        ∈ [0.00000103936620377460151,0.00000103936620377460152],
    inner vertical unit component
        ∈ [0.99777893892421284,0.99777893892421285].

The outer transverse component is positive, the inner negative. Each connector starts at the correct point with this actual tangent and ends with +e_z. Semicircles have endpoint tangents +e_z and −e_z; vertical extensions match them. Reversing return pieces gives continuous oriented tangents, and the lower rotation matches the reverse body tangent because its X component is zero. This establishes closure and C¹,¹ regularity, with no appeal to an unchanged constant-radius tangent.

Independent full-period height bounds are

| Quantity | Referee lower bound | Reported lower bound |
|---|---:|---:|
| Outer Z′(u) | 1.95359055182118×10⁻⁶ | 1.95513097602306×10⁻⁶ |
| Inner Z′(u) | 0.30516849898498078 | 0.30531691206203527 |

The referee’s own bounds are slightly weaker and strictly positive. They use the full phase derivatives and complete intervals (`scalar.py:8–26`), not samples. Therefore the new phase modulation has not invalidated height inversion, the cap reflections, or the derivatives required for curvature and length. This verifies the new steps in `../PROOF.md:24–28,54–67,90–120,164–179,198–211`.

Resolved source discrepancies, rather than conditions left for future work:

- `../candidate_high/CONSTRUCTION.json:16` retains 7.087581. `BOUND.json:4` and `../README.md:36–42` explicitly identify 7.087559024 as the sharper final claim; that is the value checked here.
- `../../round1/PROOF.md:587` has an old appendix height missing Q. Its Appendix I and `../PROOF.md:10–12` explicitly prescribe H_n=λ2πQnh. The body definition already gives that value. I used Q=6 everywhere.
- The prompt's 2.000003999878… separation is not the selected candidate's claim; the source's λ=1.000001 value is at `../README.md:143`. Section (b) supplies the correct referee’s lower bound and does not use the obsolete figure.

No requested mathematical item remains unchecked. This is a computer-assisted mathematical referee conclusion using stated classical theorems, not a proof-assistant formalization or a claim that the competing public proposals have been verified.

**Did this job find something new? No.** It checks with its own programs the supplied candidate; tighter intermediate enclosures are referee calculations, not a new construction or record claim. Predictive baselines do not apply.

Reproduce from this directory with the dependencies in ../REPRODUCE.md; all these commands were run successfully:

```sh
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=python
nice -n 10 "$PY" scalar.py
nice -n 10 "$PY" covers.py curvature
nice -n 10 "$PY" covers.py body
nice -n 10 "$PY" covers.py interfaces
nice -n 10 "$PY" covers.py lower
nice -n 10 "$PY" caps_contact.py
nice -n 10 "$PY" topology.py
```

Only the permitted construction and contact JSON files are read from the candidate. Programs regenerate full-domain covers and the physical projection rather than replaying supplied partitions. Caveats or failures affecting the requested mathematical upper bound: **none found**.

VERDICT: HOLDS

Release note: source citations and three Python input paths were remapped to this directory layout; formulas and saved JSON are unchanged. Source line numbers refer to documents before release editing. References to an old missing Q describe the historical proof; the linked published round 1 proof incorporates that correction. Fresh runs are saved in ../release_validation/. This is GPT-6 Astra via Codex, a clean-room AI referee using its own checks, not a human review.
