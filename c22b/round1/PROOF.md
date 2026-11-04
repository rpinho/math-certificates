# Candidate and unrefereed: a four-strand superhelix knot family

This is a proposed proof, with finite Arb and exact integer checks, not a
refereed theorem or a formal proof-assistant derivation. The finite checker
was separately written (same agent), without importing discovery code.
No novelty judgment is made. The claim is for a family of alternating **knots**, with all finite
closures specified below.

The final claimed C22b upper bound is1772603/250000=7.090412. The physical
length coefficient below is slightly larger; AppendixF divides it by the
certified thickness margin. All claims remain candidate and unrefereed.

## Claim and credited ingredients

For every integer n>=1 the explicitly defined C^{1,1} knot below has thickness
at least 1, is isotopic up to mirror to T(2,1104n+3), and has length

    L_n <= (3545553/500000)(1104n+3) + 150.

In particular its limiting length/crossing ratio is at most 7.091106<36/5.
The fixed additive term pays for explicit caps and has no effect on the
limiting coefficient.

The construction combines the four-strand superhelix idea of Huh–Kim–Oh
(2018, 2021) with the unequal coaxial double helix parameters/method of Youhua Li
and Claude (2026). It also builds on Olsen–Bohr, Klotz–Maldonado,
Kim–Oh–Huh (2024), and Diao. Thickness/reach and tangent-point formulas are
from Cantarella–Kusner–Sullivan (CKS, 2002), following
Litherland–Simon–Durumeric–Rawdon. The rational tangle/color fraction
classification used below is Conway's theory as proved and presented by
Louis Kauffman and Sofia Lambropoulou. Reduced alternating diagram crossing
minimality is the theorem of Murasugi, Kauffman and Thistlethwaite.
Full primary source snapshots, access qualifications, URLs and baseline
reproduction are recorded in PRIOR_ART.md. No full reading of the unavailable
Huh–Kim–Oh 2018/2021 or Kim–Oh–Huh 2024 journal articles is claimed.

## 1. Exact constants and conventions

All rational numbers in CONSTRUCTION.json are exact. Set

    P=276, Q=5, gcd(P,Q)=1, N=P/Q=276/5,
    R=293279789/100000000, a=193279689/100000000,
    i=3846709/50000000, b=16209211/50000000,
    lambda=10001/10000, Q_+=15/2, Q_-=63/2,
    h=(N-1)b, s=sqrt(R^2+h^2), w=N-h/s,
    kappa=R/s^2, tau=h/s^2, beta=s/w.

Here Q is the number of complete axis turns in one block, whereas Q_+
and Q_- are connector radii. N is an exact positive rational, not a rounded
integer. One block contains Q=5 core turns and P=276 complete minor screw
periods. This is a new exact geometry with R-a=1000001/1000000>1.
The checker parses N exactly, requires the integer core_periods to equal
its reduced denominator Q, and uses the reduced numerator P in every full
block crossing count, inverse-height right-hand side, and finite diagram.
No numerical phase approximation is used to close the curve.

Square roots are positive. Thickness means radius, not diameter. A distance
at least 2 between points implies their tangent-point radius is at least 1,
regardless of tangent direction. Let e(t)=(cos t,sin t,0),
f(t)=(-sin t,cos t,0), and ez=(0,0,1).

The unscaled axes and their Frenet vectors are

    alpha_c(t)=c R e(t)+h t ez,
    n_c(t)=-c e(t),
    b_c(t)=-c(h/s) f(t)+(R/s)ez,       c in {-1,+1}.

For each signed radius r in {a,-i}, define a physical strand

    P_c,r(t)=lambda[alpha_c(t)+r(cos(-Nt)n_c(t)+sin(-Nt)b_c(t))].   (1)

The finite body is the union of these four strands on [0,2pi Q n].
Its height is H_n=lambda 2pi Q n h. At either endpoint the four X coordinates,
from left to right, are -X_-, -X_+, X_+, X_-, where

    X_+=lambda(R-a), X_-=lambda(R+i).

Their Y coordinates vanish. Indeed t=2pi Q n changes the axis angle by
2pi Q n and the satellite phase by -N*2pi Q n=-2pi P n. Both P and Q
are integers, so the endpoint positions and tangents return exactly;
only the vertical translation H_n remains. Differentiating the physical Z coordinate gives
lambda[h-r(R/s)N cos(Nt)]>0. Thus every body strand is a graph over Z,
the body is between Z=0 and H_n, and its endpoint tangents are well defined.

## 2. Thickness tools and finite direct-body reduction

CKS Lemmas 1 and 2 identify thickness/reach with the minimum of curvature
radius and half the doubly critical distance, and also with the infimum of
tangent-point radii. We use these for the finite C^{1,1} closed link after
proving its embeddedness below.

The elementary short-arc fact is as follows. On a unit-speed C^{1,1} curve
with curvature<=1, an arc of length 0<ell<pi cannot have a chord perpendicular
to both endpoint tangents. For every u in [0,ell], the angle bounds obtained
by integrating curvature give

    T(u) dot [T(0)+T(ell)] >= cos u+cos(ell-u)
       =2cos(ell/2)cos(u-ell/2)>0.

Integrating contradicts perpendicularity at both endpoints. The same
curvature argument shows that such an arc cannot have coincident endpoints:
its chord's projection on the midpoint tangent is at least
integral_0^ell cos(abs(u-ell/2))du=2sin(ell/2)>0.

Put u=Nt and use the infinite four-strand formula (1) only as a parametrized
extension of the finite body. Increasing u by 2pi rotates every point by
2pi/N about Z and translates it by lambda 2pi h/N vertically. This is a
common Euclidean isometry of all four strands, since the internal phase
changes by a whole turn. Thus curvature and pair distances are periodic in
the first phase u, with period2pi. Composing P such minor steps rotates by2pi*P/N=2pi Q
and translates by lambda2pi Q h. Thus a whole block repeats by exact
vertical translation with the same four endpoint labels. The rational interval [0,44/7] covers a
full period; the checker proves 44/7>2pi.

Let delta be the second point's phase minus the first's. At any phase the
physical speed per u is at most

    V_r=lambda sqrt[(s/N)^2(1+kappa abs(r))^2+(r w/N)^2].          (2)

To see the formula, use a Bishop normal frame along the axis with
E1=n cos(tau z)-b_c sin(tau z), E2=n sin(tau z)+b_c cos(tau z),
z=st, and reference phase v=-wt. The position is
alpha(z)+r cos(v)E1+r sin(v)E2; its tangent and normal velocity parts are
orthogonal, with respective magnitudes s(1-kappa r cos Nt) and abs(r)w.
Alternatively it follows by squaring the explicit derivative of (1).
The bound (2) follows by abs(cos u)<=1.

For same-bundle pairs with abs(delta)>=9, their physical vertical distance
is at least

    lambda[(h/N)abs(delta)-2aR/s]
      >=lambda[9h/N-2aR/s]>2,                                  (3)

a checked scalar inequality. For the outer strand abs(delta)<3/2, its arc
length is <=(3/2)V_a<pi, so it is not a doubly critical pair. The remaining
outer self pairs may be assumed delta>=0 by interchanging the points, and
are covered by the rectangle

    first phase u in [0,44/7], delta in [3/2,9].                 (4)

For the inner strand, all abs(delta)<=9 have arc length <=9V_-i<pi,
so no inner self rectangle is needed. For opposite signed radii in the same
bundle, retain both signs of delta and cover

    first outer phase u in [0,44/7], delta in [-9,9].            (5)

The finite Arb certificates prove squared physical distance>4 throughout
(4) and (5). They also certify curvature<1 for each signed radius on the
whole phase interval [0,44/7]. Specifically, with v=dP/du and A=d²P/du²,
the checker verifies |v|²>0 and |v|^6-|v cross A|²>0 on every curvature
leaf. This is exactly the physical curvature condition, with lambda already
included. The mean-value distance leaves verify

    f(mid)+partial_u f(box)*(U-mid_u)
          +partial_delta f(box)*(D-mid_delta)>4,

with both partial derivatives evaluated on the entire rectangle using
analytic derivatives. Natural distance leaves directly enclose f(box)>4.
The leaves form a complete rational binary partition reconstructed by the
checker; none of the discovered contact locations or sampled minima are
trusted. The producer uses cylindrical coordinates; the separately written
(same agent) checker uses the Frenet vectors and their derivatives.

For different bundles, axis points with parameter difference eta have
squared distance

    2R²(1+cos eta)+h² eta²
      >=4R²+(h²-R²)eta² >=4R²,

using 1-cos eta<=eta²/2 and the checked h²>R². Satellites are within a of
their axes, so their unscaled mutual distance is >=2R-2a>2. Scaling only
increases that separation. Every body-body pair that could be doubly
critical with distance<2 has therefore been excluded, and all body
curvatures are <1.

## 3. A rigorous length estimate without numerical quadrature

The exact squared speed per u for signed radius r is

    lambda²[(s/N)²(1-kappa r cos u)²+(r w/N)²].                 (6)

Its mean over [0,2pi] is lambda² A_r where

    A_r=(s/N)²[1+(kappa r)²/2]+(r w/N)².

This uses integral cos u=0 and integral cos²u=pi. Cauchy–Schwarz gives
integral_0^{2pi} |P'_u|du <=2pi lambda sqrt(A_r). A whole block, t in[0,2pi Q], contains exactly P full minor speed periods,
because u=Nt ranges from0 to2pi P. There are two copies of each signed
radius. Consequently n blocks have length

    L_body,n <=4pi n P lambda[sqrt(A_a)+sqrt(A_-i)].             (7)

Dividing by4Pn gives the checked bound

    c_body=lambda pi[sqrt(A_a)+sqrt(A_-i)]
       <3545553/500000=7.091106.

This estimate is an analytic integral inequality, not a quadrature output.

## 4. Explicit bottom cap and swapped upper cap

At either end, the A=(c=+1) unit tangent for signed radius r is (0,p_r,c_r),
where

    y_r=R-r+r(h/s)N, z_r=h-r(R/s)N,
    p_r=y_r/sqrt(y_r²+z_r²), c_r=z_r/sqrt(y_r²+z_r²),
    e_r=sign(p_r), theta_r=acos(c_r), X_r=lambda(R-r).

The checker proves 0<c_r<1, p_a>0, p_-i<0. Thus theta_r is in (0,pi/2).
For signed radius r use Q_r=Q_+ when r=a, and Q_r=Q_- when r=-i.
The A connector, with endpoint height zero, is the radius-Q_r arc
parameterized by arclength l in [0,Q_r theta_r], v=l/Q_r:

    C_A,r(l)=(X_r,
       Q_r[p_r sin v+e_r c_r(cos v-1)],
       Q_r[e_r p_r(1-cos v)+c_r sin v]).                          (C1)

The B connector is rotation by pi about Z: negate X,Y and retain Z.
It starts with the exact body unit tangent and ends with +ez. At its A end
write

    Y_r=e_r Q_r(1-c_r), Z_r=Q_r abs(p_r), D_r=sqrt(X_r²+Y_r²).

Use + for r=a and - for r=-i. In particular X_+,X_->0, Y_+>0, Y_-<0.
The **lower** cap is the X-axis pi rotation of the following old nested
upper template: for each r join C_A,r to reversed C_B,r by

    S_r(theta)=(X_r cos theta,Y_r cos theta,Z_r+D_r sin theta),
                             0<=theta<=pi.                    (C2)

This connects each signed radius to the same signed radius in the other
bundle. Its tangent at A is +ez and at B is -ez.

The **actual upper** cap swaps the signed radii. Set

    y=-Y_->0, Zstar=Z_++21/10,
    V=(X_-+X_+, Y_+-y, 0), D=|V|/2,
    M=((X_--X_+)/2, -(Y_++y)/2, 0).

Extend each of the four connectors vertically from height Z_r to Zstar,
keeping its X,Y fixed. At height Zstar join A inner to B outer and A outer
to B inner by two semicircles

    S1(theta)= M+(V/2)cos theta+(Zstar+D sin theta)ez,
    S2(theta)=-M+(V/2)cos theta+(Zstar+D sin theta)ez,
                              0<=theta<=pi.                   (C3)

S1(0)=(X_-,-y,Zstar), S1(pi)=(-X_+,-Y_+,Zstar).
S2(0)=(X_+,Y_+,Zstar), S2(pi)=(-X_-,y,Zstar).
Each is a circle of radius D in a vertical plane, with initial tangent +ez
and final tangent -ez. Translate all actual upper pieces by H_n ez.
All tangent matches, including connector/vertical joins, are exact.
The paired analytic endpoints are identified as one curve-domain point;
such duplicate representations are not distinct-point self-intersections.
The lower cap matches reversed body tangents by its proper X rotation.
These formulas define one closed C^{1,1} curve; the component count is also
checked combinatorially below. Connector, old semicircle, new semicircle,
and straight-piece curvatures are 1/Q_r,1/D_r,1/D,0, all <=1.

Here is a complete cap clearance proof. It is deliberately split by
physical pieces so that no family of pairs is omitted. The checker proves

    X_+>1, X_->2, X_--X_+>2, D_+,D>4, D_->1,
    Z_->2, Z_+>Z_-+D_-+2,
    abs(Y_+)*sqrt(3)/2>2, Y_+>y.

All four connector and vertical-extension lines have constant distinct X
coordinates, whose minimum spacing exceeds 2. Pairs on different such
lines therefore are clear regardless of their heights and Y positions.

For the lower nested template it suffices to analyze its unrotated version,
since its X rotation preserves distances. The + semicircle is vertically
more than 2 above every - semicircle or - connector. For a + connector
versus the - semicircle, use two complete Arb
unit-square covers, one for each outer connector. Put

    l=Q_+ theta_+ x, theta=pi y, (x,y) in [0,1]^2,
    f_j(x,y)=|C_j(l)-S_-(theta)|^2, j in {B outer,A outer}.

The checker reconstructs each complete rational binary partition and
proves f_j>4 on every leaf. The semicircle is evaluated as its exact
circle-center formula. Its derivative with respect to y is
pi(-X_- sin(pi y),-Y_- sin(pi y),D_- cos(pi y)); the connector derivative
is its unit tangent times Q_+ theta_+. The natural leaves use the direct
interval squared distance. Mean-value leaves use the midpoint value plus
the interval gradient dot the displacement rectangle, with exact factor2
in each gradient of squared distance. Every leaf of both covers is checked.
Together with distinct-X connector pairs and
the vertical separation of the + semicircle, these are all pairs of
different signed radii in the lower template.

For a connector versus its own semicircle near A, with remaining bend angle
delta and semicircle angle theta in [0,pi/2], the vertical gap is
Q_r sin delta+D_r sin theta >=(2/pi)(Q_r delta+D_r theta). The quantity in
parentheses is the joined arc distance. If it is >=pi the distance is >=2;
otherwise the short-arc fact excludes a doubly critical pair. For the
outer radius r=a, theta in[pi/2,5pi/6] gives vertical gap>=D_+/2>2;
theta in[5pi/6,pi] gives opposite-Y gap>=Y_+sqrt(3)/2>2. For the inner
radius r=-i, the entire far half theta in[pi/2,pi] instead has X gap
X_-(1-cos theta)>=X_->2. It needs no lower bound on abs(Y_-) and only
D_->1 for curvature. The B endpoint uses theta->pi-theta. Connector pairs
on different X planes were already covered.

For the new upper cap, its two semicircle planes are parallel, each spanned
by V and ez. Their perpendicular distance is exactly

    d_planes=2(X_-Y_++X_+y)/|V|>2.                      (C4)

This follows by taking the planar determinant of 2M and V and dividing by
|V|; every term has the indicated positive sign. Each vertical extension
lies in the plane of the semicircle to which it attaches. Thus a semicircle
and either vertical ray belonging to the other semicircle are separated
by >=d_planes, as are the two semicircles themselves.
All common connectors have height <=Z_+, while the new semicircles have
height >=Zstar=Z_++21/10, so every semicircle/connector pair is vertically
clear. For a connector and its own vertical extension, if its remaining
bend angle is delta and the vertical distance after its end is k>=0, the
vertical gap is Q_r sin delta+k >=(2/pi)(Q_r delta+k). This is at least 2
when the joined arc distance is >=pi; otherwise the short-arc fact applies.
For a new semicircle and its own vertical endpoint ray, let k>=0 be the
height below Zstar. For theta in [0,pi/2], their vertical gap is
k+D sin theta >=(2/pi)(k+D theta); use the same arc-distance dichotomy.
For theta in [pi/2,pi], their horizontal distance along V is
D(1-cos theta)>=D>2. The other endpoint follows by theta->pi-theta.

Pairs on a single circular piece have chord
2 radius sin(ell/(2 radius))>=2ell/pi for their arc separation
ell<=pi radius. Thus ell>=pi gives distance>=2 and ell<pi is excluded
as a doubly critical pair. On a single straight piece, chord equals ell,
so the same dichotomy applies. All upper/lower within-cap pair types have
now been treated.

Every semicircle and every upper vertical extension is vertically more
than 2 outside the body slab. Only the four common connectors at either
end need finite interface certificates. For an upper body point put
u=N(t-2pi Q n)<=0. If u<=-8, its height below H_n is at least
lambda[8h/N-aR/s]>2, by the exact Z formula. For connector l>=16, either
16c_r>2 proves vertical separation, or the checked inequality

    abs(Y_connector(16))>lambda(R+a)+2

proves horizontal separation, whenever the connector length exceeds16.
If its length is <=16, the entire actual connector is already in the
rectangle below and no tail argument is needed. The checker requires one
of these two certain cases, never an ambiguous interval comparison.
Every body point has abs(Y)<=lambda(R+a), and abs(Y_connector(l)) is
nondecreasing on the actual connector: its derivative is
sin(theta_r-l/Q_r)>=0. The rectangle may include a continuation of the
circular formula beyond a short connector's endpoint; this only enlarges
the checked set. Consequently the only unresolved interface rectangle is

    body phase u in [-8,0], connector arclength l in [0,16].    (I)

All 16 choices of body strand and connector are covered. For matching
indices, a leaf may instead prove (-u_min)V_r+l_max<pi, using (2), so the
short-arc fact applies along the actual body/connector join. Other leaves
prove squared distance>4 with analytic Arb enclosures. The lower interfaces
are exact rotations of these: P_c,r(-t) is the X-axis rotation of P_c,r(t),
because X is even and Y,Z are odd; a full body period returns its X,Y.
Opposite-end free cap pieces are separated by H_n>2. The checker proves
the stronger one-axis-turn inequality lambda2pi h>2; Q n>=1 gives H_n>2.

The body tests, the cap cases, and all interfaces prove embeddedness before
using CKS: nonlocal pairs are separated, and a short curvature-bounded arc
has a positive chord projection as proved in Section2. Curvature is <=1
everywhere in arclength, including the finite tangent-matched joins in the
C^{1,1} sense. Every possible doubly critical pair of distance<2 has been
excluded. CKS Lemma1 therefore gives thickness>=1 for the entire finite
closed curve, not merely for its periodic body.

## 5. Certified physical braid, cap tangles, and crossing number

Use increasing Z as braid direction. A positive Artin generator sigma_j
has its left strand over in the chosen horizontal projection. Endpoint
order is(B,-i),(B,a),(A,a),(A,-i). The cap calculations use projection
along Y; the physical braid certificate uses horizontal coordinate7X+Y
and depth7Y-X. This is an orientation-preserving horizontal rotation and
scaling and retains the endpoint order. Thus its color action composes
with the same four cap labels; see AppendixA.

The body is a four-strand braid because every strand is strictly
Z-monotone, an inequality checked from (1). AppendixA and
projection.json.gz give a complete interval isolation of every crossing
in one physical block of Q core turns. The separately written (same agent) verifier
recomputes the inverse-height brackets, proves all zero/nonzero leaves,
orders the root events and derives the over/under word. It checks the
material permutation is the identity. This uses actual physical
coordinates, without a sampled crossing-count or winding-number assumption.

For colors c0,c1,c2,c3 with c0-c1+c2-c3=0 put p=c0-c1 and q=c1-c2.
At a positive crossing the two input colors(x,y), left first, become
(2x-y,x). Substitution on an integer basis gives

    sigma1,sigma3: U=[[1,0],[1,1]],
    sigma2:       V=[[1,-1],[0,1]].

Negative crossings use the inverse matrices, with the off-diagonal sign
reversed. The checker verifies these inverses and the braid relation
UVU=VUV exactly, then multiplies the actions along the certified
1560-crossing physical word. Its exact product is

    M=[[1,0],[1104,1]]=I+J, J²=0.

The full Q-core-turn block repeats by exact vertical translation, with the same
ordered endpoint configuration. Therefore the n-block body has action
M^n=I+nJ, namely[[1,0],[1104n,1]], for every integer n>=1. The helper also
checks the nilpotent identity exactly. No inference from finitely many
numerical n values is used.

The bottom cap has q=2p. To verify its signs, analyze the old nested upper
template first: the - semicircle crosses the + connector lines twice.
At the right crossing + is over (positive Y versus negative Y); at the
left crossing + is under. Propagating colors gives
c2=2c0-c1, c3=3c0-2c1, hence q=-2p. Rotation about X reverses the two
depths in its X-Z projection. The actual lower cap then has
c3=2c1-c0, c2=3c1-2c0, hence q=2p. These are direct crossing-rule
calculations, also checked on an integer basis in the program.

The actual swapped upper cap has exactly one projected crossing. Write
uX=X_-+X_+, dX=X_--X_+>0 and vY=Y_+-y>0. Two points on its semicircles
can share Z only at equal angles or supplementary angles. Equal angles
have distinct X coordinates dX apart. Supplementary angles meet in X
precisely when cos(theta1)=-dX/uX, a unique value in (-1,0), with
cos(theta2)=dX/uX. Their crossing has X=0. Its depths are

    Y1=-(Y_++y)/2-vY*dX/(2uX)<0,
    Y2= (Y_++y)/2+vY*dX/(2uX)>0.

Thus S2, connecting endpoints0 and2, is over S1, connecting1 and3.
The vertical extensions and connectors have four distinct constant X
coordinates below Zstar and cause no additional projected crossing.
The cap coloring is c2=c0, c3=2c0-c1, or q=-p.

A nested crossing-free cap pairs0 with3 and1 with2, and has q=0.
The lower cap is its U² image. Its two crossings are the only crossings
in its X-Z diagram: the inner semicircle has strictly monotone X; each
outer connector has constant X and strictly monotone Z, with crossing
heights inside its range by Z_+>Z_-+D_-+2. The outer semicircle lies
above both inner connectors, and the semicircles are vertically disjoint.
One crossing can be peeled off by a boundary half-twist at the adjacent
endpoints0,1 and the other at2,3. The remaining diagram is the crossing-free
nested cap. Their checked color actions are both U. This supplies the
rational-tangle construction, in addition to the color computation.
The upper diagram has exactly one crossing as calculated above; sliding
that crossing to an adjacent endpoint pair and undoing its boundary
half-twist leaves a nested crossing-free cap. Straightening the upper cap applies U,
since q=-p becomes q+p=0. These are rational tangles: begin with two trivial arcs and apply the
body word and cap twists, each an adjacent-endpoint boundary half twist.
Induction on this sequence is precisely the rational-tangle construction. Therefore the complete
rational tangle before the final nested closure has action

    U (I+nJ) U² = [[1,0],[4Pn+3,1]].                           (T)

The verifier checks separately its constant matrix U³ and its n coefficient
UJ U², as well as J²=0. This establishes (T) for every integer n>=1.
The projection verifier checks the material permutation of the actual
word is the identity, so all n blocks return the four labels.
The lower matching (0,3),(1,2) and upper matching (0,2),(1,3) form one
four-vertex cycle, so the closed curve has exactly one component for all n.

Set NW=c0, NE=c1, SW=c3, SE=c2. The Kauffman–Lambropoulou color fraction
is (NE-NW)/(NE-SE)=-p/q. Starting with primitive nested-cap colors
(p,q)=(-1,0), (T) gives fraction -1/(4Pn+3). Rational tangle classification
identifies the tangle, with its fixed endpoints, with the vertical integer
twist tangle of that fraction. This uses the classification theorem, not
merely equality of determinants. Its denominator closure (NW joined SW,
NE joined SE) is T(2,4Pn+3), up to mirror. Here 4Pn+3 is odd, so it is a
knot, consistently with the direct component check.

The usual two-strand torus diagram has k=4Pn+3 crossings, is connected and
alternating, and is reduced. One can see the last property from its
checkerboard graph: the k-cycle and parallel-edge dual have no bridge
or loop corresponding to a nugatory crossing for k>=3. The theorem of
Murasugi, Kauffman and Thistlethwaite that a reduced connected alternating
diagram realizes crossing number therefore gives exactly C_n=4Pn+3,
which is 1104n+3 for the frozen P=276. This applies to every finite closure.
The physical projection is not required itself to be reduced alternating;
the represented knot admits the displayed standard diagram.

## 6. Total length and the proposed upper bound

The lower cap length is

    E_lower=2(Q_+ theta_++Q_- theta_-)+pi(D_++D_-).

The upper cap has the same connector total, four vertical extensions, and
two radius-D semicircles, so

    E_upper=2(Q_+ theta_++Q_- theta_-)+4Zstar-2(Z_++Z_-)+2pi D.

The checker gives E_lower+E_upper<135<150.
From (7) the body length is at most c_body(4Pn), with
c_body<3545553/500000=7.091106. Hence

    L_n <= c_body(4Pn)+E_lower+E_upper
        <= (3545553/500000)(4Pn+3)+150.

Thickness>=1 implies the ropelength of this knot is at most L_n.
For any constant B satisfying ropelength(K)>=B crossing(K) for all
alternating knots, applying it to these knots gives
B<=L_n/(4Pn+3). Letting n tend to infinity yields the proposed upper
bound C22b<=3545553/500000=7.091106, strictly below36/5 and both frozen public comparison
values. The same conclusion also holds under the knots/links convention
in the frozen bar.

This is candidate and unrefereed. The finite Arb/integer checker is
separately written (same agent), imports no discovery code, and verifies
all finite covers and scalar reductions. The analytic reductions and
standard topological theorems above still require mathematical review;
this is not a machine-formalized proof or a novelty judgment.

## Appendix A. Complete physical braid projection certificate

This is the complete physical projection certificate used in Section5. At normalized body height x=Z/(lambda2pi Q h) in[0,1],
the phase for signed radius r is the unique real solution of

    u-e_r sin u=2pi P x, e_r=N rR/(sh), abs(e_r)<1.

The last strict inequality is checked. The derivative1-e_r cos u is
positive everywhere; a rational lower/upper bracket with the left residual
negative and the right residual positive therefore contains the unique
inverse phase. All24849 stored inverse brackets are verified this way.

Use projected horizontal coordinate F=7X+Y and depth G=7Y-X. This is an
orientation-preserving horizontal rotation and scaling, and it retains the
endpoint order0,1,2,3. For the two A strands write Fa,Fi and Ga,Gi at a
common height. The B strands have the same inverse phases and opposite
horizontal coordinates and depths. Their four projected coordinates are
[-Fi,-Fa,Fa,Fi]. Thus all six unordered crossing pairs reduce exactly to
four scalar zero conditions:

    m=Fa-Fi: pairs(0,1),(2,3);
    p=Fa+Fi: pairs(0,2),(1,3);
    a=Fa: pair(1,2); i=Fi: pair(0,3).

Complete binary partitions of[0,1] certify33800 leaves. An empty leaf has
an interval value excluding zero. A root leaf has a derivative interval
excluding zero on the whole leaf and a rational sub-bracket with opposite
endpoint signs. The inverse derivative is exactly
2pi P/(1-e_r cos u), and analytic coordinate derivatives are evaluated on
the full inverse interval. Therefore a root leaf has exactly one simple
zero, and every zero on the entire Q-core-turn body block is covered. Strictly disjoint root
sub-brackets order the908 events and rule out coincidences between
different zero types. The two pairs within an m or p event are disjoint
and simultaneous; their adjacent braid generators commute.

The verifier starts with the exact endpoint order and performs the forced
lane swaps at these events. It proves each participating pair is adjacent
and uses the interval sign of the depth difference to decide over/under.
It derives the1560-crossing word, compares the stored word only after this
recomputation, and checks its exact color action is[[1,0],[1104,1]] and its
material permutation is the identity. Root counts are542,110,246,10 for m,p,a,i.
Changing the horizontal projection direction without exchanging endpoint
order changes braid words by braid relations, which preserve the coloring
rule. Thus this is the physical body action used with the cap endpoint
labels in Section5. The full Q-core-turn block repeats by exact translation, so
its n-period action follows from J²=0 as before. The projection check does not assume a geometric cabling or winding
count for the physical body.

## Appendix B. Exact algebra for the speed identity

Let eta=1/s, with eta²=1/(R²+h²), and put
W=1-h eta/N, B=h eta-1/N, C=R eta. After rotating the velocity into the
local cylindrical basis and removing the common physical factor lambda,
its components are

    [rW sin u, R/N+rB cos u, h/N-rC cos u].

Using sin²u=1-cos²u, the squared norm is c0+c1 cos u+c2 cos²u, where

    c0=(R²+h²)/N²+r²W²,
    c1=-2Rr/N²,
    c2=r²R²/((R²+h²)N²).

The separately written exact checker expands the velocity components in
the quadratic fieldQ(eta), compares every rational coefficient pair with
the certificate, and checks mean=c0+c2/2. Multiplication by lambda² and
Cauchy–Schwarz then give exactly the coefficient in Section3. Its Arb
interval is below3545553/500000=7.091106. No numerical quadrature or
floating-point identity test is used.

## Appendix C. A positive margin for the entire finite knot

Put rho=499951/500000. Multiply only lambda,Q_+,Q_-,and the upper vertical clearance
21/10 by rho. Formula(1) scales the entire body by rho; unit tangents p_r,c_r
are unchanged. In(C1) X scales through lambda and Y,Z through Q_r. The
body height H_n=lambda*2pi*Q*n*h also scales by rho. Therefore
all connector images scale by rho (their arclength parameter scales too).
Old semicircle radii and centers, all new M,V,D,Zstar, and all vertical
extensions consequently scale by rho. This is a uniform spatial scaling
of the whole finite knot, including both caps.

The scaling verifier recomputes all22 covers and scalar reductions on
this exact scaled artifact; it does not infer acceptance from the old
inequalities. These checks pass, so the scaled curve has thickness>=1.
All circumcircle radii scale by rho, hence

    thickness(original K_n)>=1/rho=500000/499951>1,

for every n>=1. margin.json freezes the original hash, scale factor,
reciprocal, and hash of the deterministically transformed artifact.
This is a certified margin for the closed family, not a sampled estimate.

## Appendix D. A finite witness below the requested bar

For n=1 the knot is T(2,1107), up to mirror. The certificate verifies
c_body<3545553/500000 and E_caps<135. Thus its physical length is less
than

    (3545553/500000)*1104+135=248861907/31250.

Thickness>=1 and exact crossing count1107 give

    ropelength/crossings <27651323/3843750 <36/5.

Cross-multiplication gives
5*27651323=138256615 <138375000=36*3843750.
The stronger margin division appears in AppendixF.
The all-n closure/action proof gives
its knot type. The finite checker also constructs the standard two-strand
diagram's exact traversal, verifies alternating over/under visits, and
recognizes its connected cycle projection graph. A cycle with>=3 vertices
has no loop or cut vertex, hence this alternating diagram is reduced.
The crossing-minimality theorem used in Section5 therefore applies to
this particular finite witness as well. The auxiliary general diagram
checker verifies three auxiliary cases1107,2211,3315; those examples do not
replace the all-n argument.

## Appendix E. Exhaustion of piece-pair types

There are four body pieces, six lower-cap pieces(four connectors,two
semicircles), and ten upper-cap pieces(four connectors,four vertical
extensions,two semicircles). Unordered pairs including each piece paired
with itself total20*21/2=210. Section2 and Section4 exhaust them as follows:

| Pair block | Count | Coverage |
| --- | ---: | --- |
| body/body |10|outer self and inner short/tail; same-bundle cross cover; different-bundle axis clearance|
| body/lower |24|16 connector interfaces;8 semicircle slab separations|
| body/upper |40|16 connector interfaces;24 vertical/semicircle slab separations|
| lower/lower |21|6 same-piece cases;6 connector-plane pairs;1 different-semicircle vertical case;8 connector/semicircle cases|
| upper/upper |55|10 same-piece cases;6 connector/connector plane pairs;6 vertical/vertical plane pairs;16 connector/vertical cases;8 connector/semicircle cases;8 vertical/semicircle cases;1 parallel-semicircle case|
| lower/upper |60|opposite-end height separation|

The sum is210. Curvature is checked for every piece type separately; every
short-arc exclusion uses actual adjacent pieces or a single body strand.

## Appendix F. Exact ropelength corollary using the global margin

Let C_n=1104n+3, a0=3545553/500000, E=150 and t0=500000/499951.
The preceding complete checks establish L_n<=a0*C_n+E and tau_n>=t0.
All quantities divided by below are positive. Write Rop_min(K_n) for the
infimum over embeddings of its knot type. The specified curve is an
admissible embedding, so

    Rop_min(K_n)<=L_n/tau_n <= (a0/t0)*C_n+E/t0.

Thus any constant B valid in Rop_min(K)>=B*C(K) for all alternating knots
satisfies B<=a0/t0+E/(t0*C_n). Since C_n tends to infinity with n,

    C22b <= a0/t0 = 1772602767903/250000000000 <1772603/250000=7.090412.

In the common denominator250000000000, the strict comparison is
1772602767903 < 1772603000000;
their difference is232097.
The exact ropelength additive term is E/t0=1499853/10000.
For the finite n1 witness the stronger ratio bound is

    Rop_min(K_1)/1107 < (27651323/3843750)/t0 = 13824306585173/1921875000000 <36/5.

ROP_BOUND.json freezes these exact rational computations. Its checker
imports no discovery code and is separately written (same agent).
The global entrypoint also recomputes the full geometry and margin on
which this arithmetic corollary depends. Scaling alone leaves ropelength
unchanged; the sharper bound comes from tighter global thickness checking
and explicit use of that verified margin.

## Appendix G. A selected contact upper bound and a false-margin control

For this appendix write P_j(u)=P_(c_j,r_j)(u/N), with indices
0=(B,-i),1=(B,a),2=(A,a),3=(A,-i), where B means c=-1 and A means c=+1.
CONTACT.json specifies indices1,0 and exact phases
u_p=-6252895448239407/1000000000000000, u_q=-970222336641621/200000000000000.
They lie strictly between -2*pi*P and0. For each n>=1, translate the
points P_1(u_p),P_0(u_q) by H_n*ez: by the full-block identity
these are actual points on the last body block of K_n. Translation
preserves the chord, tangents and tangent-point radius. Use the derivative
at the first point as the nonzero tangent v, and put d=q-p, D=d dot d,
V=v dot v and Q=d dot v. The checker proves D,V and DV-Q^2 positive.
The tangent-point circle radius is

    R=sqrt(D^2*V/(4*(D*V-Q^2))).

Indeed the circumradius of p,p+epsilon*v+o(epsilon),q tends to this
value: its numerator divided by abs(epsilon) tends to D*sqrt(V), and
four times its triangle area divided by abs(epsilon) tends to
2*sqrt(DV-Q^2). Thickness is the infimum of three-point circumradii,
so tau_n<=R. This is also CKS Lemma1's tangent-point characterization.
Arb proves t0<R<1000099/1000000. Combining this upper bound with the
complete global lower bound gives, for every n>=1,

    500000/499951 <=tau_n<1000099/1000000.

This is a bound for the specified family, not an optimality statement
about its knot types or C22b. The same checked point also gives

    R*rho_bad<1, rho_bad=999901/1000000.

Consequently a proposed margin t_bad=1/rho_bad is false. The semantic
rejection control updates rho, its reciprocal, and the transformed
construction digest consistently, then requires the full geometry checker
to reject E_DISTANCE_LEAF. Thus the control tests geometric content,
rather than relying on a stale hash. The selected-contact checker uses
interval products for Q^2 and verifies the exact witness afresh.

## Appendix H. Explicit alignment of the body and cap projection frames

The body certificate uses F=7X+Y and G=7Y-X, whereas the cap crossing
calculation uses X and Y. Define D=G+F/7=(50/7)Y. At an actual projected
body crossing the two F coordinates are equal, so their D difference
is exactly their G difference. Therefore using (F,D) gives the same
crossing positions, over/under signs and word as using (F,G).

For 0<=v<=1, let A_v(X,Y,Z)=(7X+vY,(50/7)Y,Z). Its horizontal
determinant is50, so it is an invertible orientation-preserving linear
map for every v. It preserves height and hence the strict Z-monotonicity
of the body strands. At every body endpoint Y=0, its value is(7X,0,Z),
independent of v. Consequently A_v applied to the body is an explicit
isotopy of braids with all four endpoints fixed, joining A_0's positive
coordinate rescaling to A_1's (F,D) presentation. The cap diagrams under
A_0 have exactly their original over/under signs and endpoint labels.
One may keep these A_0 cap images fixed while varying the body: caps
lie outside the body slab and their endpoints agree throughout. Thus
no additional endpoint braid or conjugation enters the cap composition.

This justifies using the physically certified body color action with the
cap color actions in Section5. The Artin inverse, adjacent braid, and
far-generator commuting relations preserve the displayed matrices;
U=action(sigma1)=action(sigma3), UVU=VUV, and the inverses are checked
exactly. These linear maps are used solely for topological comparison.
All length, curvature and thickness checks use the original physical
coordinates, as specified in CONSTRUCTION.json.

## Appendix I. Exact rational-period binding

All phase geometry and speed formulas above hold for the displayed positive
rational N. Four endpoint labels return after exactly Q axis turns, because
N Q=P is an integer. The certificate verifies one entire block, not one
axis turn or a fractional number of sampled periods. Its normalized height
range[0,1] is Z in[0,lambda2pi Q h], its inverse phases range from0 to2pi P,
and its derivative uses2pi P. The actual derived body matrix is
[[1,0],[1104,1]], with identity material permutation. No integer-N word
is reused or extrapolated to the rational case.

The complete geometric reductions use a minor phase period2pi, followed by
an exact common screw isometry; integer N is unnecessary there. Repeating
P minor periods gives the stated Q-axis-turn block. Length integrates
exactly P complete speed periods per block and uses crossing denominator
4P, as shown in(7). The same cap formulas attach because both axis and
satellite phases return at the block ends. All-n cap classification and
crossing minimality therefore apply to T(2,1104n+3) for every n>=1.

The new period-domain control changes core_periods from5 to4 while holding
N=276/5. It must reject E_PERIODS, so an incorrect claimed closure period
cannot enter the accepted artifact. Every other domain, geometric,
projection, length, margin, finite, arithmetic and byte control is replayed
on this new frozen packet. There are108 exact expected corruptions.
