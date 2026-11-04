# Same-agent adversarial review of the candidate and unrefereed packet

Reviewed packet: `frozen/c22b_7_1_smallcaps`. The packet is immutable;
this note supplements its exposition and does not replace any certificate.
The verifiers were separately written (same agent). This review is not
external referee review and makes no novelty judgment.

## The global thickness reduction

The body covers use the B bundle, with indices1 (outer) and0 (inner).
The A bundle is its exact rotation by pi about Z, so its corresponding
curvatures and within-bundle distances are identical. The screw symmetry
is common to both signed radii. It can move the first phase into a full
period even when the second body point lies outside the finite body:
certifying the infinite extension only enlarges the domain. Different
bundles are handled by the axis-distance estimate, without a phase grid.

Every omitted small body self pair lies along an actual body subarc of
length below pi. The upper speed estimate bounds that subarc for every
phase. The positive midpoint-tangent chord argument in Section2 excludes
both a doubly critical chord and coincident endpoints. It therefore does
not assume embeddedness in order to prove embeddedness. All other close
pairs must belong to the complete distance rectangles or explicit cap
cases. Once embeddedness is established, the quoted CKS thickness formula
applies to the resulting closed C^{1,1} curve.

The connector endpoint tangent matches the body tangent exactly. The
connector has radius Q; its final tangent is vertical. Every remaining
join has the same one-sided unit tangent. A jump in curvature at a join
does not violate C^{1,1}: on each of finitely many adjacent pieces the
unit tangent is Lipschitz with constant at most1, and concatenating their
arclength intervals preserves that bound.

The outer connector is longer than16 and its tail uses monotone absolute
Y clearance. The short inner connector can be wholly covered by the
interface rectangle. A checked rectangle containing a continuation beyond
its physical endpoint is a superset. The short-arc alternative is used
only for matching indices and, on its physical subset, follows the actual
body-to-connector join. No nonexistent continuation is needed for that
argument. The lower interfaces are exact X rotations, not new untested
interfaces.

The inner lower semicircle does not need the old large-radius Y bound.
Its far half has X separation at least X_->2 from its own A connector;
the B case is obtained by reversing its angle. Its near half uses either
joined arclength below pi or vertical separation at least2. The two new
upper semicircle planes are distinct parallel planes, with their
perpendicular distance certified above2. The four upper vertical segments
lie in the respective semicircle planes and below Zstar. Their own-piece
joins use the same short-arc/vertical dichotomy. Cross-plane pairs use
the plane separation.

The upper/upper pair-table entry “12 connector/vertical plane pairs” means
six connector/connector pairs and six vertical/vertical pairs. The next
entry accounts for all16 connector/vertical pairs, including four actual
joins. With the other blocks the count is210 unordered pairs including
piece self pairs. Cap primitive self pairs are circular or straight and
are covered analytically. Opposite-end pieces lie outside opposite sides
of a body slab of height H_n>2.

## Projection, topology, and the length denominator

Strict height monotonicity gives a unique inverse phase at each height.
The inverse-bracket residual signs, together with 1-e cos(u)>0, prove
each inverse enclosure without trusting numerical root finding. Each of
the four zero functions has a complete binary partition: empty leaves
exclude zero; root leaves prove a nonzero derivative and opposite signed
endpoints. Roots on partition boundaries cannot be silently lost because
the strict endpoint signs needed by either leaf would then fail.

The 188 root-event brackets are strictly disjoint between events. Within
an m or p event the two crossing pairs are disjoint, hence their adjacent
Artin generators commute. Depth signs are certified on entire event
brackets. Initial lane order follows the exact endpoint coordinates
(-X_-,-X_+,X_+,X_-) with Y=0. Final material permutation is identity.
Thus the actual physical braid, rather than a modeled cable word, gives
the checked matrix [[1,0],[232,1]]. The older analytic cable algebra in
the geometry checker is only a consistency check against this physical
certificate.

For the lower cap, the inner semicircle crosses each outer connector
line once in the X-Z projection: X decreases strictly from X_- to -X_-,
and +/-X_+ lies strictly between those endpoints. The crossing heights
are between Z_- and Z_-+D_-<Z_+-2, within the range of the strictly
Z-monotone outer connectors. The signs of Y determine the two over/under
relations. The outer semicircle cannot cross an inner connector because
its absolute X is at most X_+<X_-. Vertical separation rules out a
semicircle/semicircle crossing. The X rotation gives the bottom cap signs
used in Section5. The upper cap's sole crossing follows from the explicit
equal/supplementary-angle calculation there.

The body projection direction can be changed continuously from X to
7X+Y while all endpoint Y coordinates remain zero and their order stays
fixed. These are different planar presentations of the same tangle with
the same boundary labels. The cap and body color calculations therefore
compose. Starting with a trivial two-arc tangle, adjoining any boundary
half twist preserves rationality. This rationality hypothesis is essential:
the matrix or determinant alone would not classify an arbitrary knot.
The full rational-tangle classification, with fraction -1/(232n+3), is
the stated theorem being invoked. The exact nilpotent identity proves
the action for every n, and the closure matchings form one cycle.

The represented knot has the usual reduced alternating two-strand torus
diagram; the physical projection need not itself be alternating. Crossing
minimality follows from the classical reduced-alternating theorem after
the rational-tangle identification. The finite diagram checker confirms
the standard diagram rather than substituting determinant equality for
that identification.

## Scaling and quantifiers

The margin transform multiplies lambda, Q, and upper clearance by the
same rational rho=19999/20000. In particular H_n=lambda*2*pi*n*h scales
by rho, as do every cap coordinate, vertical length, and translation.
It is a uniform scaling of the entire closed curve for every integer n.
Rechecking all20 geometry covers on the transformed artifact proves
thickness(original)>=1/rho, not just sampled clearance at one n.

The body coefficient is a Cauchy-Schwarz upper bound on its complete
period integral, with an exact speed-polynomial identity checked in a
quadratic field. No quadrature error is involved. Caps cost less than490
uniformly in n. Consequently the stated7.1 limiting bound and the finite
n=20 ratio below36/5 use the same explicit thickness-certified family.

## Remaining limits of this review

The checker verifies arithmetic, complete finite covers, and the stated
exact actions. The analytic domain reductions and classical geometric
and topological theorems still require human mathematical review. Papers
whose full texts could not be accessed remain explicitly qualified in
PRIOR_ART.md. Numerical adversarial cap probes are auxiliary falsification
attempts and provide no global certificate. Their results and any exact
selected-witness validation will be recorded separately.

## Split-radius packet reviewed after the initial packet

The later `frozen/c22b_7_1_splitcaps` packet uses outer connector radius
15/2, inner connector radius30, and upper clearance21/10. Its immutable
manifest hash is590238eb08289364ddd1084a7e5bc8d6a1fa5bd4f634bc1a540a1c57d6c863c4.
The body, certified physical word, and speed identity are unchanged. All
inherited certificates were rebound to the new construction bytes and
fully recomputed by the separately written (same agent) checkers.

Two new complete unit-square covers replace the earlier sufficient
lateral-separation estimate for an outer connector versus the inner
lower semicircle. Each has29 leaves, with the exact connector arclength
and circle angle used in its derivatives. These are different-radius
pieces, so neither cover permits a short-arc exclusion. All16 body/join
covers were regenerated for the smaller outer connectors. There are22
complete geometry covers with60590 leaves. The remaining analytic cap
cases retain their strict scalar inequalities, including inner height>2,
outer height above the entire inner semicircle by>2, distinct X planes,
and the parallel upper-plane gap>2. Thus the210-pair exhaustion is the
same, with these two pairs now certified by explicit interval partitions.

Uniform scaling multiplies both connector radii, lambda, and upper
clearance. The modified margin driver checks this transform and recomputes
all22 covers. The new packet passes full Mini and Linux frozen replay,
including86 exact expected rejection controls. It retains the candidate
and unrefereed bound71/10 and thickness margin20000/19999, with additive150
and finite T(2,1163) ratio<209191219/29075000<36/5. Both platforms use
python-flint0.9.0; these are environment replays, not external review.

## Numerical falsification probes and selected exact replay

The separate NumPy/SciPy model searched280 directed same-end piece-pair
cases for each of the Q30 and split-radius frozen packets, with24 local
starts and2048 random samples per case plus a31-by31 starting grid. It
skipped circular/straight primitive self pairs covered analytically, and
excluded a small diagonal and numerically flat chords for stability.
These exclusions and numerical local optimization preclude a completeness
claim. All eight chunks finished successfully on the pod.

Each of the560 retained parameter pairs was converted to exact decimal
rationals and replayed with the separate Arb helper against its frozen
packet. Every selected radius was certified above1, with no inconclusive
case or counterexample. The smallest selected radius interval is
[1.000325820914728961199234137780648995441 +/-5.43e-41]. This is only a
pointwise check. The full universal thickness proof remains the complete
frozen covers and the analytic reductions in PROOF.md. Each packet also
passes12 exact expected rejections for this auxiliary helper. Receipts are
results/probes_caps_arb.json and results/probes_split_arb.json.

The first auxiliary replay stopped with E_METRIC_FLAT because its integer
power call on a zero-straddling projection ball returned NaN under this
python-flint version. Replacing projection**2 with projection*projection
restored the intended interval square. This was a false rejection in the
unsealed auxiliary helper. The frozen bound verifiers were unchanged;
their interval comparisons reject NaN. The corrected full selected replay
and all auxiliary controls then passed.

## Canonical contracted packet and final proof audit

The reviewed canonical packet is `frozen/c22b_70948`, manifest
`8e90fb3e16c4fbc04fdea6fdbcea0134e26156a9bf65d0b41d2f0993e30e8048`.
Its complete Mini and Linux replays pass, with 107 exact expected
corruptions. This packet uses gamma=2499311/2500000, 22 complete geometry
covers, and 158801 leaves. The lower cap's two special pair covers now
have 30 leaves each. Counts in the earlier sections above describe their
named earlier packets and are not transferred to this one.

The final physical length coefficient is 8868943/1250000. The proved
thickness lower bound is 20000/19999, so the exact limiting ropelength
coefficient is 177369991057/25000000000<17737/2500. The minimum over all
embeddings of a knot type is bounded above by this specified embedding's
L/tau; it is not identified with that quotient. The selected contact
upper bound concerns only this spatial family. No knot-type optimality
or novelty claim follows.

The point-pair upper radius is enclosed by
[1.00005013111848486189752762885227664857780225 +/-3.13e-45].
Shrinking by the consistently rebound false margin
99967341383/99972440000 gives a selected radius below 1. The complete
checker must reject E_DISTANCE_LEAF after all changed geometric hashes
and reciprocal factors have been updated. Thus this rejection tests the
geometry and is not explained by a deliberately stale digest.

Appendix H now makes the projection-frame comparison explicit. Write
F=7X+Y, G=7Y-X, and D=G+F/7=(50/7)Y. At a crossing, DeltaF=0, so
DeltaD=DeltaG and the body word has unchanged over/under signs. The maps
A_v(X,Y,Z)=(7X+vY,(50/7)Y,Z), 0<=v<=1, have horizontal determinant 50
and fix every endpoint (7X,0,Z). They give an isotopy of embedded body
braids while the A_0 cap images are held fixed outside the body slab.
Intermediate joins need not remain tangent matched for this purely
topological comparison. No cap/body intersections can appear in their
disjoint height interiors. Metric calculations always use the original
physical coordinates, without applying this anisotropic map.

The bottom nested tangle's primitive colors may be chosen with
(p,q)=(-1,0): c0=c3 and c1=c2=c0+1. The checked action gives
(p,q)=(-1,-(232n+3)), hence Kauffman–Lambropoulou's fraction -p/q
is -1/(232n+3). The cited classification applies because starting with two
trivial arcs and adjoining boundary half twists preserves rationality.
The cap matching confirms a single component. Classification identifies
the vertical integer twist tangle; its specified denominator closure is
T(2,232n+3), up to mirror. This is stronger information than a determinant.
The standard alternating torus diagram is reduced, and the classical
crossing-minimality theorem supplies its exact crossing count for all n.

A fresh reading of the retained primary texts confirms the hypotheses:
CKS Lemma 1 states the tangent-circle and curvature/doubly-critical
characterizations for C1 links; Lemma 2 equates thickness with reach.
The explicit finitely joined, tangent-matched pieces here are C1,1, with
arclength tangent Lipschitz constant at most 1. Kauffman–Lambropoulou
Theorem 1 classifies rational tangles by fractions, and their coloring
section uses (NE-NW)/(NE-SE). Thistlethwaite's Corollary 1 gives crossing
minimality for an irreducible alternating diagram; the companion
Murasugi theorem was also retained. These are invoked mathematical
theorems, not additional claims proved by the arithmetic checker.

The finite cover verifier reconstructs a complete binary partition and
recomputes every leaf. All mean-value distance gradients are evaluated
on entire rectangles. The producer's extra factor 8 is conservative
search slack; the checker uses the exact gradient factor 2. Curvature
identities, connector arclength derivatives, all tail inequalities,
and the short-arc alternatives use physical scale factors explicitly.
The short-arc coincidence exclusion proves embeddedness before CKS is
invoked, avoiding circular reliance on a thickness formula for a curve
not yet known to be embedded. Strict Arb comparisons reject ambiguous
or NaN enclosures; numerical search output is not an acceptance path.

## New N56 experiment during the remaining budget

A later gauge search removed two artificial numerical restrictions and
found a promising N56 shape. It is a different geometry, not a uniform
scaling of N58. At the time of this note its exact scalar/speed/contact
prechecks pass, but full geometry and physical projection results cannot
yet be recovered because pod SSH began timing out around 09:04 UTC.
It is UNVERIFIED and supplies no accepted C22b bound at this checkpoint.
The canonical packet above remains unchanged. A later dated addendum
will identify any completed replay; silence does not promote N56.

## Final N55 packet, reviewed after recovery

The final accepted candidate packet is `frozen/c22b_709144_n55`, manifest
`f7253113420045e83d0b8573c24f03479066603f59d69b3d10da4b4e9960bd64`.
All preceding sections refer to their explicitly named historical packets.
The N55 packet is a different exact geometry, with R-a=1000001/1000000,
not a homothety of N58. Both complete environment replays and all107 exact
expected corruptions pass. Its22geometry covers have122748 leaves; both
original and499951/500000-shrunk inputs are checked. The new physical
projection has6611leaves4833inverse brackets180events308raw crossings,
root counts108,20,48,4, exact body action[[1,0],[220,1]] and identity
material permutation. No N58 word, root count, or certificate hash is
assumed to remain valid. The unchanged analytic pair exhaustion still
has210types and all22covers/scalars were checked afresh.

The exact speed coefficient interval is
[7.0921350063942189116511177000549550 +/-1.07e-35], below709213501/1e8.
Caps cost less than135. Globaltau>=500000/499951 and the exact length
bound give limit354571999038451/5e13<88643/12500=7.09144. Aselected
contact bounds this specified family's tau above by1000099/1e6, with
radius[1.00009887460819911673982346676390087267910916 +/-1.16e-45].
The consistently rebound false shrink999901/1e6 gives selectedradius
[0.999999864819612905027266224240691246492713927 +/-3.89e-47]<1 and
the full checker rejectsE_DISTANCE_LEAF. Atrial coefficient7.092135
failedexactly; the final rational coefficient is strictly above its Arb
enclosure. Atrial uppercontact bound also failed; the corresponding
unsealed draft is not an accepted bound.

The geometric rebound corruption now decreasesouterradius and uses the
body_cross partition. This creates an actual false distance while retaining
the monotone height/scalar domain. The old large pitch decrease is unsuitable
as this particular N55 geometric control because height monotonicity is
near its boundary. Both the corruption and its expected rejection remain
explicit, and all107 controls pass. Only the new unsealed source was changed;
every earlier sealed packet remains immutable. The final proof and checker
map use T(2,220n+3), finiteT(2,1103), and the correct new projection counts.

The podSSHoutage09:04–09:30prevented heartbeat and one backup; mathematical
outputs were retrieved on recovery before they were accepted. This is an
operational exception, not a mathematical rejection or evidence of a bound.

## Final rational-period packet

The final candidate is now `frozen/c22b_7090412_rational`, manifest
`8e9a8979855ecf4b5eb75dce191d5e24d4df4bd7151024ed9fce7f4ebe5106a9`.
The named integer packets above remain unchanged. Exact N=276/5 gives
P276 minor screw periods and Q5 axis turns in a closed body block. Both
axis and satellite phases return exactly. The new checker requires Q to
be the reduced denominator and uses P in every whole-block inverse-height
RHS, derivative, crossing slope and finite diagram. WrongQ4 rejects
E_PERIODS. Metric formulas continue to use the exact rational N.

All22covers146198leaves pass on both original and margin geometry; the
210-pair exhaustion is unchanged. The body phases still reduce by the
common minor-period screw isometry. Composing P minor steps gives exactly
Q full axis turns. Length integrates P complete speed periods per block,
not a noninteger number of periods. Appends/joins have the same phases
at both ends; H_n=lambda2piQnh scales withlambda under the margin map.
Opposite-cap separation follows even from the stronger one-core-turn
height inequality checked by the scalar routine. No unit convention changes.

The actual five-core-turn projection has33800leaves24849inversebrackets
908events1560rawcrossings, action[[1,0],[1104,1]], identitypermutation,
rootcounts542,110,246,10. It is newly isolated and checked, not an
interpolation of an integerN word. Nilpotent all-n action and cap
classification give T(2,1104n+3); standard alternating crossing minimality
gives C_n=1104n+3. The lower cap's two crossings can be peeled by
adjacent-endpoint boundary twists, leaving the trivial nested cap; the
upper cap has one twist. This makes the rationality hypothesis explicit.

The physicalcoefficientCI is[7.0911059675486719886727558957752231 +/-5.05e-37],
below3545553/500000. Caps<135. Alln globaltau>=500000/499951 and
selectedtau<1000099/1e6 give the stated exactrope limit
1772602767903/250000000000<1772603/250000=7.090412. The selectedpoint
radius is[1.00009831283308338696074802072457480516242448 +/-3.44e-45];
its999901/1e6shrink is[.999999303100112911705438906670523072256713397
+/-4.58e-46]<1. The fully rebound false margin rejectsE_DISTANCE_LEAF.
Both frozenenvironment replays and all108expectedcorruptions pass.
The finite witness is n1,T(2,1107), with ratio
13824306585173/1921875000000<36/5. This is candidate and unrefereed,
separately written (same agent); no knot-type optimality or novelty judgment.

Final analytic review (2026-11-04, after the source refresh): rechecked the
primary retained CKS Lemmas 1–2, Kauffman–Lambropoulou Theorems 1 and 4,
and the original reduced-alternating crossing statements of Murasugi and
Thistlethwaite. The endpoint assignment NW=c0, NE=c1, SW=c3, SE=c2 turns
the checked diagonal relation into NW+SE=NE+SW, and their coloring fraction
is exactly -p/q. The nested cap is the infinity tangle, and the final
-1/(4Pn+3) tangle's denominator closure is the two-strand torus knot up
to mirror. This review uses the explicit boundary-twist rationality argument,
not a determinant-only identification.

Rechecked the analytic metric cases against the actual checker formulas:
opposite-bundle separation follows from h²>R² and R-a>1; a complete minor
phase screw isometry justifies the same-bundle rectangles for rational N.
Short arcs stay on actual joined pieces. Each cap's near-end bound uses
sin(v)>=2v/pi only on [0,pi/2]; its far halves use the separate vertical,
Y, or X bounds. The upper plane distance is the determinant of 2M and V
in absolute value divided by |V|. Connector/vertical lines have distinct
constant X values. All other free cap pieces are outside the body slab
by more than 2, and connector tails reduce to the 16 covered interfaces.
The exact scaling keeps Q=5 fixed and sends H_n to rho*H_n, as corrected
in ERRATA.md. No additional mathematical or numerical acceptance was
introduced; the frozen packet and the 108-control receipts are unchanged.

2026-11-04 final prose correction: [ERRATA.md](ERRATA.md), pinned by results/prose_errata.json, corrects one omitted Q in Appendix C and the README decimal. The main proof definition and exact construction are correct. No frozen file changed.

2026-11-04T11:06:45Z: Auxiliary exact derivative audit passed on the pinned frozen verify.py point-method AST. Using Q(eta,i) and exact exponential polynomials, compared 12 position,12velocity,12acceleration component identities to direct coordinates and their formal derivatives. Three in-memory code corruptions return exactly E_POSITION,E_VELOCITY,E_ACCELERATION. No floating arithmetic or discovery imports. Source audit_frozen_derivatives.py and receipt results/frozen_derivative_audit.json are hash-bound. This supplements the proof read, not the global geometry certificate; main packet and its108controls unchanged.
