# Adversarial referee report: C22b ≤ 7.090412

Job `math_c22bref_1104`, 2026-11-04. The corrected construction withstands
the attacks described below. I found no unresolved geometric or topological
gap. The two caveats are the already disclosed prose errors in the frozen
packet; their precise locations and required corrections appear at the end.

The conclusion independently supported here is

\[
C_{22b}\le 7.090411071612 < 7.090412.
\]

I did **not read, run, import, or copy any candidate verifier or discovery
program**. I used the mathematical definitions, PROOF.md, the exact construction
parameters, and the stated contact points. All interval subdivisions and the
physical braid word were generated afresh. The independent programs and
their outputs are retained in this directory. In particular, the candidate's
claimed successful verifier runs and 108 corruption tests are not evidence
for this report.

## (a) Definition match

The [live table](https://teorth.github.io/optimizationproblems/constants/22b.html)
was read, and upstream main was freshly fetched into this job directory.
The pinned upstream commit is `87b4ebbd426ff8db597a2004cc45da17903bdcf2`.
Its source agrees byte-for-byte with the requested existing
`../c44_release/tao/constants/22b.md`. See `sources/22b_upstream.md:5` and
`PRIOR_ART.md` for retrieval details. The following is the **verbatim Markdown
definition**, including the source's mathematical notation and links. The
source's Apache 2.0 license is retained in `sources/tao_LICENSE`.

```text
$C_{22b} = b_{o}$ is the largest constant for which one has an inequality
$$ L \geq b_{o} C $$
for all knots that admit an [alternating](https://en.wikipedia.org/wiki/Alternating_knot) diagram, where $L$ is the ropelength of a knot (or link) with [crossing number](https://en.wikipedia.org/wiki/Crossing_number_(knot_theory)) $C$.
The _ropelength_ $L$ is the infimum over all embeddings of the knot (or link) of the ratio of the contour length of the knot to its thickness. The _thickness_ is defined as the radius of the smallest circle that passes through any three points on the knot (where collinear points yield an infinite radius). Colloquially, the ropelength is the least amount of rope required to tie a specific knot in a rope of unit radius. See [CKS2002] for the full definition.
```

Consequently, for nonzero crossing number,

\[
C_{22b}=\inf_{K\ {
m alternating}}\frac{\operatorname{Rop}_{\min}(K)}{C(K)}.
\]

The denominator is the **minimal crossing number of the knot type**, not the
family index n, number of axis turns, number of minor periods, or crossing
count of the displayed physical projection. The table imposes no prime-knot
restriction, and does not require the particular spatial embedding to be an
ideal/tight minimizer. “Alternating” means that the knot type admits an
alternating diagram. The parenthetical inclusion of links is immaterial here:
the proposed examples have one component, so they are admissible with either
knots-only or knots-and-links quantification. The unknot's zero crossing number
does not constrain this constant.

Thickness is **radius**, not diameter. For an embedded C1,1 curve it is the
minimum of the essential infimum of curvature radius and half the minimal
doubly critical self-distance. This matches CKS Lemmas 1–2, checked in the
primary paper (`sources/CKS.txt:116`). A radius-τ tube gives ropelength
Len/τ; there is no factor of two missing in the candidate.

The table is neither a limsup nor a liminf over all knots of a specified
crossing number. Nevertheless, a sequence of alternating knot types with
certified ratios bounded above by numbers converging to B proves C22b ≤ B.
The all-n family therefore has exactly the needed logical form. Section (c)
checks its minimal crossing number, and section (d) checks the limit.

## (b) Independent thickness, reach, and length checks

### Arithmetic and geometry reconstructed

`independent_geometry.py` uses python-flint 0.9.0 Arb at 160 bits. Rational
subdivision endpoints are Python Fractions converted to Arb without floating
rounding. The programs read no candidate certificate partitions. Every
unresolved box is replaced by **both** halves; termination requires acceptance
of every leaf. Acceptance uses a natural interval evaluation or a midpoint
mean-value enclosure with the gradient evaluated over the entire box.

For clarity, my independent Cartesian implementation of the body, with
u = Nt, is

\[
\begin{aligned}
x&=c\lambda[(R-r\cos u)\cos(u/N)-(rh/s)\sin u\sin(u/N)],\\
y&=c\lambda[(R-r\cos u)\sin(u/N)+(rh/s)\sin u\cos(u/N)],\\
z&=\lambda[hu/N-(rR/s)\sin u].
\end{aligned}
\]

I differentiated these coordinates independently. In the rotating horizontal
frame, the velocity divided by λ is

\[
\big(rW\sin u,\ R/N+rB\cos u,\ h/N-rC\cos u\big),
\quad W=1-h/(sN),\ B=h/s-1/N,\ C=R/s.
\]

Its acceleration divided by λ is

\[
\big(r(W-B/N)\cos u-R/N^2,\ r(W/N-B)\sin u,\ rC\sin u\big).
\]

An exact symbolic differentiation audit also checks all three velocity and
acceleration components, both distance-gradient components, and the speed
identity, independently of the interval acceptance decisions
(`independent_audit.py`, `audit_results.json`).

The global target was set directly to

\[
t_0=500000/499951=1.000098009604941284245856\ldots.
\]

Thus the distance tests on the **original geometry** require squared distance
strictly greater than `4*t0^2`, rather than trusting a successful rescaling
receipt. This threshold is approximately 4.000784115263060916953286.

### Enclosures compared with the claim

All decimal intervals below are rounded outward from the retained Arb results.
“Length upper expression” means an enclosure of a proved upper bound, not an
interval containing the actual length from both sides.

| Quantity | Candidate claim | Independent result |
|---|---|---|
| Minimum outer-body curvature radius | ≥ t0 after the margin check | `[1.98788, 1.987887177]` |
| Minimum inner-body curvature radius | ≥ t0 after the margin check | `[1.46347, 1.463478204]` |
| Minimum curvature radius over the whole closed curve | ≥ t0 | `[1.46347, 1.463478204]` |
| Half the minimum doubly critical self-distance, every n ≥ 1 | ≥ t0 | `[t0, 1.000098312834]` |
| Thickness/reach, every n ≥ 1 | `[t0, 1.000099)` | `[t0, 1.000098312834]` |
| Body length coefficient upper expression | `< 7.091106`; reported Arb value near 7.09110596754867 | `[7.09110596754867198867, 7.09110596754867198868]` |
| Lower-cap length | included in caps `<135` | `[60.84909611102712516589, 60.84909611102712516590]` |
| Upper-cap length | included in caps `<135` | `[73.50036383250236680519, 73.50036383250236680520]` |
| Total cap length | `<135` | `[134.34945994352949197108, 134.34945994352949197109]` |
| n=1 physical-length upper expression | `<7963.581024` | `[7962.93044811726336746580, 7962.93044811726336746582]` |
| Body upper expression divided by t0 | below final rational coefficient | `[7.09041103916385221881, 7.09041103916385221882]` |

Sources for the candidate column are
`../c22br2/frozen/c22b_7090412_rational/PROOF.md:147`, `:191`, `:491`,
`:598`, `:610`, and `:702`, and `../c22br2/REPORT.md:84`.
Independent enclosures and counts are in `geometry_all.json`.

For the curvature lower bounds I proved
`|v|^6 - r0^2*|v×acc|^2 > 0` and `|v|^2 > 0` on each phase box,
with r0 = 1.98788 or 1.46347. The fresh covers have respectively 128855
and 2212 leaves. Evaluation at u=0 gives the displayed upper endpoints
for the minimum. The circular-piece radii are 7.5, 31.5,
7.56598469874190..., 3.01074332620561..., and 4.22340229513133...;
straight pieces have zero curvature. Thus the body's inner strand controls
the global curvature enclosure. At joins, curvature is interpreted in the
C1,1/essential-bound sense, not as a nonexistent classical second derivative.

The upper endpoint for thickness is independently obtained from the stated
two exact rational phases using the tangent-point radius formula. My enclosure
is `1.000098312833083386960748020724574805...`, with Arb radius below
`6e-46`. These points occur inside the last complete body block for every n.
Since this is smaller than the proved global curvature-radius lower bound,
CKS implies that half the minimum doubly critical distance has the same upper
bound. This reasoning does **not** assert that the selected pair itself is
exactly doubly critical, or that a sampled minimum is a global minimum.

### Exhaustion of distances, caps, and joins

I reviewed the reductions rather than assuming that interval success covers
the intended domain. The minor-phase screw symmetry is valid for rational N:
u ↦ u+2π rotates by 2π/N and translates vertically by λ2πh/N. Consequently
`[0,44/7]` covers one full first-phase period, including all block boundaries.

For same-bundle pairs, the vertical tail at |δ| ≥ 9 exceeds 2.22861000397,
which is greater than 2t0. Inner self-pairs with |δ| ≤ 9 have arc length
at most 2.98529226645 < πt0, and outer self-pairs with |δ| < 3/2 have
arc length at most 2.88999557599 < πt0. A curvature bound 1/t0 excludes
doubly critical chords on these short arcs. The proof is the integrated
positive projection of the tangent on the sum of the two endpoint tangents;
the same midpoint-tangent argument excludes coincident endpoints.

The remaining outer-self and outer/inner rectangles were independently
covered. Here are accepted-leaf counts and conservative lower bounds for
**squared distance on distance-accepted leaves**, not claimed exact minima:

| Domain | Fresh leaves | Certified squared-distance lower bound |
|---|---:|---:|
| Outer self, u ∈ [0,44/7], δ ∈ [3/2,9] | 1668 | >4.00078424919 |
| Outer/inner, u ∈ [0,44/7], δ ∈ [-9,9] | 19220 | >4.00078411640 |
| Two lower-cap connector/other-circle rectangles | 32 | >4.33485336006 |
| Eight interface rectangles representing all 16 by half-turn symmetry | 964 | >4.00078414403 on the distance leaves |

Twelve of the 964 interface leaves use a proved short-arc exclusion instead
of distance. The other 952 are distance leaves. There are 21884 distance/arc
leaves altogether; the candidate's own leaf counts are neither read nor needed.

Different bundles are separated analytically: their axis distance is at least
2R because h²>R², and subtracting the satellite radii gives distance at least
`2*lambda*(R-a)=2.0002020002 > 2*t0`. Thus no pair of body strands from
different bundles was omitted.

The connector/body interfaces cover u ∈ [-8,0], l ∈ [0,16]. The body tail
below that window is more than 2.22850602207 away vertically. Both actual
connector lengths are **less than 16**, so no uncertain continued-connector
tail is needed. A half-turn about Z negates both bundle labels and preserves
distance, reducing 16 interfaces to eight fresh interval covers. Reflection
by the proper X-axis half-turn maps the lower interface problem to the same
checked upper-interface problem. The n-block translation is exact.

I also checked the cap reductions independently:

* All four connector/vertical-line X coordinates are distinct, with minimum
  spacing 2.0002020002 > 2t0.
* The lower inner semicircle starts 2.02869022076 outside the body slab.
  The outer semicircle is more than 2.46056644208 above the whole inner
  semicircle/connector assembly. The two unresolved outer-connector/inner-
  semicircle pairs are the interval rectangles in the table above.
* A connector and its own semicircle/vertical continuation are handled by
  the actual joined arc: either its length is below πt0, or the vertical-gap
  inequality `sin x >= 2x/pi` on `[0,pi/2]` gives distance at least 2t0.
  The far semicircle halves are covered by their X, Y, or vertical separation,
  with the inequalities evaluated at target t0 rather than only at 1.
* The upper semicircles' planes are 5.36047192516... apart. Their connectors
  lie at least 2.1 below them; their own vertical rays use the same short-arc/
  separation dichotomy. Vertical rays in the other plane are separated by
  the plane distance. On a single circular or straight piece, the elementary
  chord bound handles every remaining self-pair.
* Opposite caps lie outside opposite faces of the body slab; already H1 is
  552.05768231546... > 2t0. All more distant n are automatically covered.

For an independent count, the four body, six lower-cap, and ten upper-cap
pieces give these unordered pair blocks, including self-pairs:

| Piece blocks | Count | Reason no pair is missing |
|---|---:|---|
| body/body | 10 | phase covers, short arcs, vertical tails, bundle separation |
| body/lower | 24 | 16 interfaces and 8 slab-separated semicircle pairs |
| body/upper | 40 | 16 interfaces and 24 slab-separated vertical/circle pairs |
| lower/lower | 21 | 6 self, 6 connector pairs, 1 circle pair, 8 connector/circle pairs |
| upper/upper | 55 | 10 self, 6 connector pairs, 6 vertical pairs, 16 connector/vertical, 8 connector/circle, 8 vertical/circle, 1 circle pair |
| lower/upper | 60 | opposite-slab separation |
| **Total** | **210** | all 20×21/2 pairs |

At the joins, `sin(theta_r)=|p_r|`, `cos(theta_r)=c_r`, and
`p_r^2+c_r^2=1` give exact position and unit-tangent matches in C1.
The connector ends have tangent +ez; the semicircles start with +ez and end
with -ez; the lower rotation supplies the reversed body tangents. These are
exact identities, not conclusions drawn from small floating residuals.
Bounded one-sided curvatures and these tangent matches imply C1,1 regularity.
Coincident endpoint descriptions identify the same domain point and do not
create a second branch. Positive local chord projections and the nonlocal
distance tests establish embeddedness before applying CKS.

These checks establish **both** global radius-of-curvature ≥ t0 and global
half-doubly-critical-distance ≥ t0 on every finite closed curve. They are
not an infinite-body-only thickness calculation.

### Length

Squaring the independently differentiated velocity and using
`s^2=R^2+h^2` gives the polynomial in cos u

\[
|P'_u|^2/\lambda^2=
(R^2+h^2)/N^2+r^2W^2
-2Rr\cos u/N^2+r^2R^2\cos^2u/(s^2N^2).
\]

The average is obtained exactly from the vanishing average of cos u and
the average 1/2 of cos²u. Cauchy–Schwarz gives the body upper expression
reported above. There are exactly 276n complete minor periods per strand,
and two copies of each signed radius. Integrating connector and semicircle
speeds gives the two cap lengths in the table; all four upper straight
extensions are included. Thus, with c the independently enclosed body upper
expression and E the total cap length,

\[
\operatorname{Len}(\Gamma_n)\le 1104n\,c+E,
\quad c<7.091106,\quad E<135.
\]

No quadrature error or extrapolation is involved.

## (c) Knot type, all n, and the n=1 invariant

The physical braid certificate was regenerated in a **different projection**:
F = 5X+Y with depth Y, instead of the candidate's 7X+Y projection. The strict
height inequality is independently positive for both signed radii; its
smallest unscaled endpoint margin is 0.005739227035... . Hence all four body
strands are graphs over height, not curves with concealed turnbacks.

At normalized height x, the inverse phase solves

\[
u-e_r\sin u=2\pi\,276x,
\qquad e_r=NrR/(sh),\qquad |e_r|<1.
\]

`independent_topology.py` proposes inverse brackets numerically but accepts
them only after **strict Arb residual signs** at exact rational endpoints.
The positive derivative proves existence and uniqueness. Thus no libm
accuracy assumption enters the proof. Fresh subdivisions of [0,1] either
exclude a crossing or prove exactly one simple root using derivative and
endpoint signs. Distinct event brackets are disjoint, and the participating
strands are checked to occupy adjacent lanes. Over/under decisions use
interval-separated depth coordinates.

The four scalar root counts are 542, 110, 246, and 10. The first two types
each represent two simultaneous disjoint crossings, whose generators commute.
The independent result is **908 events and 1560 crossings**, with material
permutation the identity. In the convention “positive = left strand over”,
the generator counts are:

| Generator | σ1 | σ3 | σ2 | σ1^-1 | σ3^-1 | σ2^-1 |
|---|---:|---:|---:|---:|---:|---:|
| Count | 592 | 592 | 118 | 60 | 60 | 138 |

The complete new word and rational event brackets are retained in
`independent_braid.json`; they were never supplied to the computation from
the candidate. The fresh complete root partition has 6972 leaves. The full
four-color action, obtained directly by propagating colors at every crossing,
is

\[
\begin{pmatrix}
543&-542&-10&10\\
542&-541&-10&10\\
-10&10&543&-542\\
-10&10&542&-541
\end{pmatrix}.
\]

On `p=c0-c1`, `q=c1-c2`, with `c0-c1+c2-c3=0`, this gives exactly

\[
M=\begin{pmatrix}1&0\\1104&1\end{pmatrix}.
\]

The projection change introduces no endpoint braid: the maps
`(X,Y,Z) -> (5X+vY,Y,Z)`, 0≤v≤1, are invertible and fix all four body
endpoints after their common positive X scaling. The cap images can remain
fixed outside the body slab. This explicitly connects the body projection
to the cap X–Z diagrams.

### The cap isotopies and rational-tangle identification

The bottom cap is not accepted merely because its colors happen to give a
desired determinant. Its diagram can be checked directly. Each inner-circle
crossing of an outer connector occurs at height
`4.86839113304026764129...` in the unrotated template, inside the connector's
height range. Strict X monotonicity of the semicircle and strict connector
height monotonicity make both crossings unique. The depth gap is
`7.04447248131238909363...`. The X-axis rotation reverses these depths for
the actual bottom cap. There are no other crossings by the separations in
section (b).

Moving the left crossing into the collar of endpoints 0,1 and the right
crossing into the disjoint collar of endpoints 2,3 exhibits the lower cap
as `sigma1 sigma3` applied to the crossing-free nested cap `(0,3),(1,2)`.
Both are positive in the stated convention. Removing those two boundary
half-twists leaves two disjoint nested arcs. This is a real rational-tangle
construction, not an inference from a picture or an invariant match.
Color propagation consequently gives `c2=3c1-2c0`, `c3=2c1-c0`, or q=2p.

The upper semicircles have just one crossing. Equal heights require equal
or supplementary angles; equal angles give different X coordinates, while
supplementary angles give one solution. The two depths there are
`-5.64555428502292876502...` and `+5.64555428502292876502...`.
The arc joining 0 to 2 is over the arc joining 1 to 3. Peeling this one
crossing into an endpoint collar leaves the nested cap; straightening it
appends one positive sigma1, with action
`U=[[1,0],[1,1]]`. Directly, the upper cap imposes `c2=c0`,
`c3=2c0-c1`, or q=-p. The computed cap crossings and signs are retained in
`audit_results.json`.

Every braid generator attached to a trivial two-string cap is an
adjacent-endpoint boundary half-twist. Therefore the bottom cap plus any
number of body blocks is a **rational tangle**. This is precisely the
boundary-homeomorphism construction described in Kauffman–Lambropoulou,
Note 1, page 8 (`sources/rational_tangles.txt:345`). Their classification
theorem and coloring fraction apply; they would not apply to an arbitrary
tangle with the same determinant.

After one block both geometric phases and all four labels return. Repetition
is actual translation, and `(M-I)^2=0`, so the all-n calculation is

\[
UM^nU^2=\begin{pmatrix}1&0\\1104n+3&1\end{pmatrix}.
\]

With boundary labels `(NW,NE,SW,SE)=(c0,c1,c3,c2)`, the coloring fraction
is `(NE-NW)/(NE-SE)=-p/q`. Starting from the nested tangle, its final value
is `-1/(1104n+3)`. Rational-tangle classification gives the vertical integer
twist tangle, and the nested denominator closure is
`T(2, ±(1104n+3))`. The sign depends on the handedness convention; the
candidate explicitly claims the type **up to mirror**, which is sufficient
because reflection preserves thickness and length.

The bottom matching `(0,3),(1,2)` and upper matching `(0,2),(1,3)` form a
single cycle when the body permutation is the identity. Thus every n gives
one component. The standard two-strand diagram has 1104n+3 crossings and is
reduced alternating: its checkerboard graph is a cycle with no bridge, and
the dual parallel-edge graph has no bridge or loop. Alternating-diagram
crossing minimality therefore gives **C(Kn)=1104n+3**, not the 1560n+3
crossings of this physical projection.

### Independent n=1 invariants

Using the full four-color matrix and the geometrically derived cap relations
gives the integral Fox relation matrix

\[
\begin{pmatrix}
2&-3&1&0\\
1&-2&0&1\\
-553&552&553&-552\\
-554&553&552&-551
\end{pmatrix}.
\]

All sixteen 3×3 minors have absolute value **1107**. Its Smith normal form
is `diag(1,1,1107,0)`. This independently gives determinant **1107**, using
the actual projected body word and caps, rather than a preconstructed
standard torus-knot diagram (`topology_results.json`).

I also computed the Alexander module of the same four-plat. The local
abelianized Wirtinger relation is `(1-t)O+tU-V=0`; reversing the over-meridian
replaces t by t^-1. Tracking the upward/downward material orientations
through all 1563 crossings gives two reduced relations that are associates,
with normalized polynomial

\[
\Delta(t)=\sum_{j=0}^{1106}(-1)^j t^j
          =\frac{t^{1107}+1}{t+1}.
\]

It has degree 1106, Δ(1)=1, and |Δ(-1)|=1107, as required for T(2,1107).
The calculation is in `independent_alexander.py` and `alexander_results.json`.
These invariant matches corroborate the isotopy/classification argument;
they are not substituted for it.

## (d) The n → infinity claim

The rational-period issue is real and was checked explicitly. With
N=276/5, the body interval is `[0,2*pi*5*n]`, not `[0,2*pi*n]`.
The axis angle changes by 2π·5n and the satellite phase by -2π·276n.
Thus endpoints, tangents, and material labels return **exactly**, with
height `Hn=lambda*2*pi*5*n*h`. No rounding of N is permissible or used.

The length of the body is exactly n times the one-block length, whereas
the cap lengths are independent of n. The upper cap is translated by Hn,
which changes no length or curvature. All distance reductions have fixed
phase/interface domains, and opposite-end separations only improve with n.
The thickness lower bound t0 is therefore uniform for **every n≥1**.

Put `a0=3545553/500000`, `rho=499951/500000`, and `Cn=1104n+3`.
The independently checked bounds imply

\[
\frac{\operatorname{Rop}_{\min}(K_n)}{C_n}
\le\frac{\operatorname{Len}(\Gamma_n)}{t_0C_n}
\le \rho a_0+\frac{150\rho}{C_n}.
\]

The exact limit of this **stated finite upper bound** is

\[
\rho a_0=\frac{1772602767903}{250000000000}
         =7.090411071612.
\]

Its gap below the displayed 7.090412 is exactly
`232097/250000000000 = 0.000000928388`.
The additive term after scaling is exactly `1499853/10000 = 149.9853`.
These identities and the finite witness arithmetic are independently
cross-multiplied in `independent_audit.py`.

The n=1 example alone does not attain the headline 7.090412 ratio. To check
that the limiting argument is not concealing a finite-family obstruction,
the stated coarse upper bound already lies strictly below 7.090412 for
every **n≥146336**. This follows by exact rational arithmetic; the first
such example has crossing number 161554947. No numerical construction of
that many crossings is needed because the geometric and topological
arguments are uniform in n.

There is no need to prove that the optimal ropelength ratios themselves
converge, or that this rational upper coefficient equals the geometric
family's exact limiting ratio. Cauchy–Schwarz and thickness lower bounds
introduce slack. The candidate calls it a limiting **upper** bound, and the
infimum defining C22b is at most the limit of these admissible upper bounds.
Scaling by rho also leaves the knot type and actual ropelength invariant;
the gain comes from proving a stronger thickness lower bound, not from
scaling alone.

## Other attacks, caveats, and reproducibility

The selected contact independently rules out the stronger proposed radius
`1/0.999901`: its tangent-point radius multiplied by 0.999901 is below 1.
Thus the margin check is capable of distinguishing nearby false statements.
The near-flat outer endpoint, the very small height derivative there,
simultaneous disjoint braid events, inner-cap curvature, cap self-pairs,
endpoint duplicate representations, and the smallest allowed n=1 were all
included in the checks above. None produced a counterexample.

The two caveats are editorial, already disclosed, and must accompany the
unaltered frozen packet:

1. **Missing Q in a height formula.**
   `../c22br2/frozen/c22b_7090412_rational/PROOF.md:587` writes
   `H_n=lambda*2pi*n*h`. It must be `lambda*2pi*Q*n*h`, Q=5,
   as specified correctly by the defining body interval at
   `PROOF.md:72` and explicitly corrected in `../c22br2/ERRATA.md:10`.
   Using the erroneous height literally to place the upper cap would fail
   closure. The actual defined geometry and this independent review use the
   correct five-turn height. Uniform scaling still scales it by rho.
2. **False decimal equality in the README.**
   `../c22br2/frozen/c22b_7090412_rational/README.md:3` writes
   `1772603/250000=7.09041`. The exact decimal is **7.090412**,
   as corrected in `../c22br2/ERRATA.md:20`. The rational fraction and
   `../c22br2/REPORT.md:6` are correct. The truncated 7.09041 would be a
   strictly stronger decimal bound than the one this proof establishes.

There are no additional unresolved mathematical caveats in this review.
In particular, the supplied errata are not treated as evidence that the
geometry checks passed: those checks were performed independently here.

To reproduce all mathematical checks from this directory:

```sh
sh run_referee_checks.sh
```

The default interpreter is the shared open-science virtual environment;
`REFEREE_PYTHON=/path/to/python sh run_referee_checks.sh` selects another
environment with python-flint, scipy, and sympy. Expected last stdout line:
`ALL_INDEPENDENT_REFEREE_CHECKS_PASS`. The script sequentially runs the
fresh geometry, projection, Alexander, symbolic/cap/arithmetic, and prior
periodic-baseline checks, and writes their JSON and text receipts. No
candidate program is part of this command.

The Mini was used exclusively. Every computation was launched with
`nice -n 10`; the inherited process priority made the observed nice value
20, recorded explicitly in `geometry_all.json`. Mathematical workers were
sequential in the final reproduction; earlier independent geometry tasks
used at most three worker processes. The read-only source inventory used
one Python coordinator and at most two gh children. No pod was used.
The final process audit is retained in `process_audit.txt`; no job worker
remains. No commit, push, PR, post, or third-party message was made.

`PRIOR_ART.md` records the bounded public-source audit and the independent
periodic-body reproduction of the pinned Li/Claude baseline. No priority or
novelty conclusion is asserted. `INPUTS.json` pins the reviewed mathematical
inputs, and `OUTPUTS.json` pins the independent programs and receipts.

VERDICT: HOLDS WITH CAVEATS
