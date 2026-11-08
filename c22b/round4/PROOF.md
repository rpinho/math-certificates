# Candidate C22b bound: Fourier-radius and phase-modulated superhelices

The finite verifier is **separately written (same agent)** from the numerical search.
The modulated-radius and phase steps here are prose. A clean-room AI referee
on a different model wrote its own checks and found the claim holds; see
[its report](referee/REFEREE.md). Human mathematical review is still needed.
This is a proposed computer-assisted argument, not a proof-assistant theorem.
Doldrums / SCiEL / CPIL lab MBZUAI's even-radius modulation of our #324 is
the starting point. Their exact coefficients were inaccessible; see
PRIOR_ART.md. No third-party construction/search/verifier code was run.

This note extends our original proof, published in [the round 1 proof](../round1/PROOF.md), with its Q correction:
full block height is lambda*2*pi*Q*n*h. Its cap formulas C1–C4, all 210 unordered
piece-pair cases, rational-tangle classification, and alternating crossing
minimality are reused below. Both arguments still need human mathematical review; AI review does not
replace that review.

## Exact body and closure

Each CONSTRUCTION.json contains exact rational parameters. Write N=P/Q in
lowest terms, h=(N-1)b, s=sqrt(R^2+h^2), and lambda for the uniform body
scale. Let the signed radius r(u) be a(u)>0 on the outer strand and -i(u)<0
on the inner strand, where a and i are the cosine polynomials in
modulation. The selected construction has six cosine-radius orders and four sine-phase
orders, v(u)=u+sum p_k sin(ku). The inherited checker implements these
terms and the argument below applies when its stated inequalities pass. No sine-radius construction
is certified: generic sine radii destroy the reflection used for the
lower cap and their nonzero endpoint derivatives would require new joins.

Use the original axes and Frenet frames

    alpha_c(t)=(c R cos t,c R sin t,h t), c in {-1,+1},
    n_c(t)=(-c cos t,-c sin t,0),
    b_c(t)=(c(h/s)sin t,-c(h/s)cos t,R/s).

Set u=N*t and

    X_c,r(u)=lambda*(alpha_c(u/N)
                     +r(u)*(cos(v(u))*n_c(u/N)-sin(v(u))*b_c(u/N))).

The four strands use labels (c,r)=(-1,-i),(-1,a),(+1,a),(+1,-i),
indices 0,1,2,3. A finite body is u in [0,2*pi*P*n]. Both axis and
minor phases return exactly at its ends, so one complete block repeats by
vertical translation H=lambda*2*pi*Q*h. The block endpoint material labels
return unchanged. The inverse-height and physical braid certificate uses
this entire block, not a fractional or rounded period.

For explicit cylindrical coordinates, with A=R-r cos v and B=(h/s)r sin v,

    (X,Y,Z)=lambda*(c*(A cos(u/N)-B sin(u/N)),
                    c*(A sin(u/N)+B cos(u/N)),
                    h*u/N-(R/s)*r sin v).

The checker differentiates the Frenet-vector formula by the full product
rule, including r', r'', v', v''. The producer uses the cylindrical
formula. The search uses numerical cylindrical expressions. Search
samples, estimated contact locations, optimizer termination, and
finite-difference derivatives are not used to prove any inequality.

The derivatives of a cosine polynomial are the explicit finite sums
r'=-sum k*r_k sin(ku), r''=-sum k^2*r_k cos(ku). The phase derivatives
are analogous. Even r and odd v give X(-u)=X(u), Y(-u)=-Y(u), Z(-u)=-Z(u),
which is the original proper X-axis rotation between lower and upper
interfaces. At u=0, r'=0, v=0 and the endpoint is
(lambda*c*(R-r(0)),0,0). The endpoint tangent is calculated from the actual
modulated derivative, normalized, and is used in C1. Thus the cap joins
are exact C1 joins, including when phase modulation changes v'(0).

The connector radii and upper clearance in each exact construction define
all lower and upper cap pieces by [the round 1 proof](../round1/PROOF.md) C1–C4. The verifier
uses the same inherited circle-center formulas, evaluated with the new
endpoint tangents. It checks their stated tangent signs, curvature,
plane distances, vertical gaps and total length. The selected caps are
unchanged in their connector radii (15/2,63/2) and clearance (21/10).

## Global geometry and thickness

The classical CKS thickness criterion used in the original proof says
that a closed embedded C^{1,1} curve has thickness at least 1 when its
curvature is at most 1 and no doubly critical pair has distance less than
2. The original short-arc argument excludes any pair on a joined arc of
length less than pi. Its positive chord projection also excludes
self-intersections on these short arcs. These tools are unchanged.

Advancing u by 2*pi is a common screw isometry of the four strands.
Radii, their derivatives and v(u)-u are 2*pi periodic. Thus the full
rational interval [0,44/7], with 44/7>2*pi checked in Arb, covers every
body phase for curvature, speed, radius and height-derivative purposes.

The verifier encloses the spatial speed norm, signed radius, and height
derivative on every one of 512 equal rational subintervals of [0,44/7].
It takes outward upper/lower endpoints. Let a_max be its outer-radius
upper bound. It verifies 0<a, 0<i<=a_max throughout, and Z'(u)>0
throughout for both strands, rather than using the constant-radius
monotonicity formula. It verifies, for their respective speed upper
bounds V_a,V_i,

    (3/2)*V_a<pi, 9*V_i<pi,
    lambda*(9*h/N-2*a_max*R/s)>2,
    lambda*(8*h/N-a_max*R/s)>2.

The last two follow from the exact Z formula using |r sin v|<=a_max.
They handle all same-bundle |delta|>=9 tails and the body-end interface
tail u<=-8. Inner self pairs with |delta|<=9 are short. Outer self pairs
with |delta|<3/2 are short. All remaining same-bundle body pairs are
covered by complete partitions of

    outer self: (u,delta) in [0,44/7] x [3/2,9],
    outer/inner: (u,delta) in [0,44/7] x [-9,9].

Every distance leaf proves squared distance >4, either by natural Arb
evaluation, or by the midpoint plus the full interval gradient times the
rectangle displacement. Every curvature leaf proves

    F(u)=|X'(u)|^6-|X'(u) cross X''(u)|^2 > 0.

It uses either a natural enclosure or F(mid)+F'(interval)*(u-mid), with
F' propagated by Arb series arithmetic through the explicit product
rules. Speeds are nonzero since Z'>0. Therefore the curvature inequality
is exactly curvature<1, including all modulation derivative terms.

For opposite bundles the original axis-separation proof applies unchanged:
axis distance >=2R when h^2>R^2, and each satellite is at distance at most
a_max from its axis. The checker verifies lambda*(2R-2*a_max)>2. This
excludes all different-bundle pairs on the infinite body.

For caps the original scalar cases remain applicable because their
formulas and endpoint tangent signs are unchanged in form. Semicircles
and upper vertical extensions are outside the body slab by more than 2.
Only connector interfaces remain. All 16 index pairs have complete
partitions of [-8,0] x [0,16]. A matching-index leaf can use the actual
joined arc bound (-u_min)*V_r+l_max<pi. Every other leaf proves distance>2.
The connector tail beyond l=16, when present, is separated by its checked
vertical height or lateral displacement, using the new R+a_max cylinder
bound. Reflection supplies the lower interfaces exactly, not by sampling.
The two lower outer-connector/inner-semicircle cases are covered on their
complete unit squares by inherited exact circle formulas.

The inherited 20-piece exhaustion still has precisely 210 unordered
piece pairs (including self pairs): body/body 10, body/lower 24,
body/upper 40, lower/lower 21, upper/upper 55, lower/upper 60. Their
assignment to distance covers, cap scalar inequalities, slab separation,
same-piece circle bounds, or short joined arcs is exactly the table in
[the round 1 proof](../round1/PROOF.md) Appendix E and its Section 4. No new piece is introduced
by radius modulation. Curvature is checked for both body strands, every
connector and semicircle, and straight extensions. Positive nonlocal
distances and positive short-arc chords first establish embeddedness;
then CKS supplies thickness>=1 for every finite n, with tangent-matched
piece joins interpreted in the C^{1,1} sense.

The certificate verifier reconstructs every binary partition from its
full rational root box. It rejects missing child boxes, overlaps,
duplicates, hash mismatches, or any failed inequality. The producer may
ask the verifier whether a proposed leaf encloses tightly enough, to
avoid expression-dependent interval overestimation. The verifier replays
all leaves from scratch and does not trust producer margins or minima.
Sharing an acceptance function with the partition producer is not
independent verification of that function; the separately written claim
is relative to the numerical search. All of this work is by the same
agent.

## Rigorous length

Body speed is periodic with period 2*pi, since the screw is an isometry.
For the selected constructions the speed is positive everywhere by Z'>0.
Let f_r(u)=|X'_r(u)|. Instead of assuming the constant-radius speed
identity, the checker integrates this actual norm, including all radial
derivatives, by interval Taylor arithmetic.

On each of 256 equal cells in [0,2*pi], let m be the exact midpoint and
hcell the exact half width. An Arb series centered at m gives Taylor
coefficients f^(k)(m)/k!. A second series with constant coefficient the
entire closed cell encloses f^(6)(xi)/6! for every xi in the cell. This
works because all arithmetic, trig operations and the positive square
root are differentiated by rigorous series operations; the cell's speed
norm interval is checked positive. Taylor's theorem gives

    integral_cell f <= sum_{k=0,2,4} 2*hcell^(k+1)/(k+1)*f^(k)(m)/k!
                       +2*hcell^7/7 * sup_cell |f^(6)/6!|.

Arb enclosures for pi, the cell endpoints, all coefficients and remainder
are outward. This is a rigorous Taylor integral bound, not an estimate
from ordinary quadrature. The factor for body length per crossing is
exactly one half times the sum of the two full-period speed integrals:
two copies of each radius and P periods give body length
2*P*n*(I_a+I_i), while the crossing slope is 4P. Cap length is a fixed
constant E<150. Thus if c is the rational claimed coefficient,

    L_n <= c*(4P*n) +150, thickness>=1.

No separate thickness margin is divided into this number; the small
lambda expansion is already in the spatial derivatives and the length.
A uniform scale alone cannot improve the ropelength ratio. It supplies
room to certify unit thickness after optimizing the shape.

## Physical braid and knot type

At normalized height x in [0,1] define

    H_r(u)=u-(N*R/(s*h))*r(u)*sin(v(u)),
    H_r(u)=2*pi*P*x.

The global height-derivative lower bound proves H'_r>0 everywhere.
Rational brackets with opposite residual signs contain the unique inverse
phase. verify_projection.py checks each bracket with Arb, and uses the
exact derivative du/dx=(2*pi*P)/H'_r(u). It computes actual coordinates
and spatial derivatives via the verification geometry. It exhausts the
same four scalar crossing functions of F=7X+Y and G=7Y-X as original
Appendix A, verifies every empty/root leaf, root order, adjacency and
over/under sign, and reconstructs the physical braid word and identity
material permutation. The color action is required to be [[1,0],[4P,1]].

The cap labels and body endpoint order are unchanged; all endpoint Y
coordinates are exactly zero. The original Appendix H shear isotopy
therefore aligns the body and cap projection frames with fixed endpoints.
The exact cap diagrams and color calculations remain those in original
Section 5 because their checked inequalities, tangent signs and formulas
still hold. Their boundary half-twist descriptions show they are rational
tangles, rather than asserting rationality from a determinant alone.
Starting from the lower rational tangle, successive adjacent-endpoint
half twists from the actual physical body word preserve the rational
tangle construction. The coloring theorem and classification used in
the original proof then give action

    U * [[1,0],[4P*n,1]] * U^2 = [[1,0],[4P*n+3,1]].

The denominator closure is T(2,4P*n+3), up to mirror. The two cap
matchings with identity body permutation also directly give one component.
The reduced alternating two-strand torus diagram has exactly 4P*n+3
crossings by the same classical crossing-minimality theorem. The original
exact finite-diagram checker is reused for small illustrative n, while
the all-n claim uses the rational-tangle argument and matrix nilpotence.

Consequently C22b<=c by applying the closed unit-thickness knots for every
n and letting n tend to infinity. See [README.md](README.md) for the actual replayed
construction, its rational c, the comparison, qualifications, and checks.

## Higher-order extension and determinant check

The formulas and analytic reductions above are stated in full in this note.
This extension removes no geometric hypothesis: the numerical height floor was
reduced from 0.00002 to 0.000002, while the checker still proves strictly
positive height derivative on complete intervals. Increasing Fourier
orders to six for radii and four for phase introduces no new piece types
or proof reductions; every derivative term is included by the displayed
finite sums and full product rules. The application to these higher-order coefficients and the determinant
explanation below were addressed by the clean-room AI referee; they still
need human mathematical review.

The supplementary check_determinant.py applies the actual physical braid
word, with exact integer Fox color updates (x,y)->(2x-y,x) for a positive
crossing and (x,y)->(y,2y-x) for a negative crossing. By the inherited
cap-crossing descriptions, the lower-cap endpoint colors are
[x,y,3y-2x,2y-x]; the upper cap requires c2=c0 and c3=2c0-c1.
After quotienting the constant coloring by y=0, the two remaining
integer relations are both -(1324n+3)x=0 for n=1,2,3. Thus their gcd
gives determinants 1327,2651,3975. The all-n statement also follows from
the already checked two-dimensional action and its nilpotent increment.
The determinant is an additional consistency check; the rational-tangle
argument, actual braid action, cap identification and alternating-diagram
minimality together supply the claimed knot family.
