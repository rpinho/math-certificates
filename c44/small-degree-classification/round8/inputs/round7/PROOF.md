# C44 round seven — candidate, unrefereed

The resulting candidate bounds are R4=22, 46<=R5<=51, 94<=R6<=110 and

    3/2 <= C44 <=
    164865563398608188023949601889/79228162514264337593543950336
    < 2.0808959614.

The best value uses the additional lattice argument in LATTICE_PROOF.md
and its expanded norm-gap proof in BW_GAP_PROOF.md. The quartic-only
variant avoids lattice premises and gives C44<2.0963373341, R5<=51,R6<=112.

This is a written proof with exact finite certificates. It is not a
proof-assistant formalization or independent human refereeing. The two
verifiers are separately written implementations by the same agent; they
import neither the search nor each other's mathematics. Published theorem
completeness is an explicit dependency. No novelty or priority is claimed.

This proof combines the candidate R4=22 from inputs/gap1/PROOF.md with the
reviewed round-six derivative restriction argument, then classifies the
energy-equality case and a small quartic second-weight relaxation. All
inherited proofs, catalogue data and exact verifiers are copied under
inputs/. Their successful replay is recorded in receipts/. In particular
R4=22 and R5<=53 remain unrefereed mathematical inputs, despite agent reviews
passing them. A source-coverage gap for an unused KTA result in the round-six
review does not affect any step below.

## 1. Definitions, finite maxima and potential identity

For a sign Boolean function f on independent uniform sign inputs, write
f=sum_S fhat(S) x_S in its unique real multilinear expansion. A coordinate
i is relevant when some nonzero coefficient has i in its mask. Its local
degree d_i is the largest such mask size. Set D(f)=sum_i 2^(-d_i), R_d=max
number of relevant variables at degree <=d, and W_d=max D(f) at degree <=d.

A nonzero polynomial of degree <=r has support density >=2^-r. For r=0
this is immediate. Otherwise choose j with P=x_j A+B, A nonzero of degree
<=r-1. At every point with A nonzero the two values B+A and B-A cannot
both vanish. Induction and averaging give density >=(1/2)2^{-(r-1)}.

A_i=(f(i=+1)-f(i=-1))/2 is ternary, with degree d_i-1 and influence
p_i=E A_i². Hence p_i>=2^{1-d_i}. Fourier orthogonality gives
sum_i p_i=sum_S |S| fhat(S)²<=d. Thus R_d<=d2^{d-1} and D(f)<=d/2.
After deleting dummy inputs and relabeling, there are finitely many
Boolean functions to consider; both maxima exist.

We use the corrected CHS identity W_d=R_d/2^d. Here is the extremal proof.
Take an f maximizing D at degree <=d, let L be all its coordinates of local
degree below d, and let Y be the others. If L is nonempty, take a disjoint
copy L' and selector z and put

    h=(1+z)f(L,Y)/2+(1-z)f(L',Y)/2.

Every degree-d term depends only on Y and cancels in the coefficient of z,
so deg h<=d. Every Y variable retains local degree d. Each L variable and
its copy has its local degree increased by exactly one, preserving their
combined old weight. The selector is relevant because f depends on L, so
it adds positive weight. This contradicts maximality. The D maximizer has
all local degrees d, giving W_d<=R_d/2^d; the reverse inequality follows
by applying D>=R_d/2^d to a count maximizer.

A count maximizer also has every local degree d: replacing any smaller
local-degree bit variable by the AND of two fresh bits keeps degree <=d,
preserves every other relevant variable, makes both fresh variables
relevant, and increases the count by one. This contradicts maximality.
This count argument is separate from the preceding potential argument.

Base counts are R1=1, R2=4, R3=10 and the input R4=22. The first two follow
from the influence bound and the usual two-selector construction; R3=10
is Tarannikov–Kirienko's published result. The gap1 proof of R4 uses the
complete Rasoolzadeh 761-class cubic catalogue, the exact cubic energy
envelope, and the Valyuzhenich minimum-support classification. Its full
written proof and independently checked catalogue are frozen in inputs/.
Thus c1=1/2,c2=1,c3=5/4,c4=11/8 are universal potential ceilings.

## 2. Controls from a derivative, valid at every influence

Let A be ternary of degree <=k>=1, p=E A², and h its relevant count. For
each relevant j, Delta_j A=(A(j=+1)-A(j=-1))/2 is nonzero of degree <=k-1.
Its nonzero values have magnitude >=1/2. The support lemma gives

    E(Delta_j A)² >= 2^{-(k+1)}.                         (1)

Summing Fourier derivative energies gives

    sum_j E(Delta_j A)²=sum_S |S| Ahat(S)²<=kp.

Consequently h<=k p 2^{k+1}. For a derivative A_i of a degree-d Boolean
function, put k=d-1, M=2^k and lambda=M p_i. Then

    h <= floor(2k lambda).                              (2)

For any control set H the weighted restriction inequality is

    D(f)<=sum_(j in H)2^{-d_j(f)}+E_alpha D(f_alpha).     (3)

For one restricted coordinate j, consider an outside coordinate i. If it
survives both branches, neither local degree increases, so its average
weight cannot decrease. If it survives just one branch, its derivative
has factor (1+/-x_j)/2 and its original local degree is exactly one larger
than the surviving branch degree. Half that branch weight equals the old
weight. It cannot disappear in both branches. Sum over outside i and
iterate over H to prove (3).

Choose a count maximizer f with all local degrees d, and choose i of
minimum influence. Let H be the relevant-coordinate set of A_i and Y the
remaining coordinates except i. Write f=x_i A_i(H)+B(H,Y). On an active
control assignment A_i=+/-1, both x_i branches being Boolean forces B=0
identically in Y. The restricted function is a signed dictator, of
potential 1/2. Such assignments have fraction p_i.

Every degree-d monomial meets H. If a degree-d monomial of B missed H,
its coefficient would survive restriction of H unchanged: a strict
superset that could change it would exceed degree d. This contradicts
B=0 on an active assignment. A degree-d monomial involving i also meets
H, since its other d-1 variables form a mask of A_i. Therefore every
restricted function has degree <=d-1 for d>=2.

For any c>=W_(d-1), c>=1/2, (3) gives, with N=R_d,

    N <= 2^d c + h + (1-2c)lambda.                      (4)

Since i has minimum influence and total influence <=d,

    1 <= lambda <= dM/N.                                (5)

All these statements concern the same derivative. Improving its control
ceiling h can therefore be inserted directly in (4).

## 3. Integer Fourier grid and allowed normalized weights

An integer-valued cube function has integer coefficients in bit variables:
the coefficient of T is sum_(U subset T)(-1)^{|T|-|U|}g(1_U), with other
bits zero. Substituting bit=(1-sign)/2 shows that real degree <=k gives
Fourier coefficients in 2^-k Z. For a sign Boolean f of degree <=d apply
this formula to (1-f)/2; its coefficients have the sharper grid 2^{1-d}.
Thus A_i's coefficients are z_S/M with integer z_S.

At the all-plus input, sum z_S=M A_i(+1), a multiple of M. For d>=2, M
is even, so sum z_S² is even by z²=z modulo two. Parseval gives

    lambda=(sum z_S²)/M in (2/M) Z.                     (6)

Reducing the integer bit coefficients of A_i itself modulo two gives its
binary support indicator, of binary degree <=k; both signs become one.
No squaring or binary affine substitution is used to infer real degree.
The published below-twice-minimum Reed–Muller theorem (Berlekamp–Sloane /
Kasami–Tokura) says every normalized weight <2 is 2-2^-j for integer j>=0.
Parameter restrictions may safely be relaxed. Append dummy coordinates to
meet the theorem's interior range. Combining with (6) excludes j>=k: the
j=k numerator is odd and j>k is nonintegral. Therefore we allow precisely

    lambda=2-2^-j, j=0,...,k-1, below 2;                 (7)
    every point of (2/M)Z at or above 2.

This is a relaxation, not an existence assertion. No 2..2.5 KTA table or
uncorrected higher-weight exclusion is used. The precise original source
coverage is inherited in inputs/round6/PROOF.md and its KTA audit.

## 4. Equality in the control energy bound

Suppose equality h=k p 2^{k+1} holds in (1),(2). Every Fourier term of A
then has degree k, and each nonzero Delta_j A has minimum support
2^{-(k-1)} and constant nonzero magnitude 1/2. Equality follows term by
term because all the summand inequalities have nonnegative slack.

Valyuzhenich, arXiv:2303.10995, Theorem 2(2), classifies a real polynomial
of degree r with support density 2^-r as a tensor product on disjoint
coordinates of point indicators and blocks supported on the two constant
strings. An even block of m coordinates has opposite output signs on the
two strings and degree m-1; an odd block has equal signs and degree m-1.
Their Fourier supports are, respectively, all odd and all even subsets of
the block. A point factor has support masks {empty,{u}}. The total degree
cost is r. This is an explicit published completeness premise.

If the product is homogeneous, point factors cannot occur. A block of
size m>=3 has at least two distinct Fourier degrees, so it cannot occur
either: disjoint tensor masks have distinct unions and cannot cancel.
Only two-coordinate factors remain. Thus each homogeneous partial is

    Delta_j A=+/- (1/2) product_(a=1)^(k-1)(x_u+/-x_v)/2, (8)

on disjoint pairs. Its Fourier support consists of all pair transversals.

For k>=3 form the pure simplicial complex generated by A's nonzero
Fourier masks, all of size k. The link at every vertex is a cross-polytope
boundary with k-1 opposite pairs. Each connected component is a k-cross-
polytope boundary, by the elementary lemma proved next. Each component
therefore has 2k vertices. Hence equality forces h to be a multiple of 2k,
so lambda=h/(2k) must be an integer. We need only the safe consequence

    k>=3, lambda nonintegral  ==> h<2k lambda,
    h <= ceil(2k lambda)-1.                             (9)

For integral lambda we retain (2); no stronger sign-factor claim is needed.

Here is the needed combinatorial lemma, credited to Masuda–Panov, Lemma
4.7, arXiv:math/0607094v2 pp.14–15. Let K be connected, pure of dimension
r>=2, with every vertex link the boundary of an r-cross-polytope. Each
vertex has 2r neighbors, each vertex lies in 2^r facets, and each ridge is
in two facets (read this last statement in any of its vertex links).
Fix v. Its link has r opposite pairs.

First suppose an opposite pair p,q in link(v) is not an edge of K. Let R
be the other 2r-2 neighbors of v. The link of p contains v and R, plus
one vertex p' outside {v} union R; q is excluded, so p' is outside link(v).
The star of v in link(p) is the cone from v on the cross-polytope boundary
on R. Since link(p) is itself cross-polytopal, its unique remaining vertex
p' is opposite v, and link(p)=R*{v,p'}. This follows by comparing the
opposite-pair partitions in that star; it also proves p' is joined to every
vertex of R. Similarly link(q)=R*{v,q'}. For each a in R, its neighbors
include its 2r-2 neighbors inside link(v), and v,p',q'. Since it has only
2r neighbors, p'=q'. Now link(v), these two links, and their opposite-pair
partitions give the full suspension of link(v) from {v,p'}. Every vertex
in this suspension already has its full link there. No extra edge can
leave it, and connectedness proves K is this cross-polytope boundary.

Otherwise every opposite pair in link(v) is an edge of K. All its 2r
vertices are mutually adjacent in K, and each is also adjacent to v.
Their degree 2r is exhausted, so connectedness gives exactly 2r+1 vertices.
Facet incidences would give F=2^r(2r+1)/(r+1). On the other hand any facet
not containing v uses r+1 vertices of link(v), so contains an opposite
pair p,q. The link of p is R*{v,q}, where R is the common link of p,q in
link(v); therefore that facet contains two ridges which are facets of
link(v), one using p and one q. Each such ridge can occur in only one
facet not containing v, because its other incident facet contains v.
There are 2^r ridges in link(v), so at most 2^{r-1} facets avoid v and
F<=2^r+2^{r-1}. But (2r+1)/(r+1)>3/2 for r>1. This contradicts the
incidence formula. The two cases prove the lemma.

## 5. A complete finite quartic second-weight exclusion

We prove the following stronger special case:

    A ternary, deg A<=4, E A²=3/32  ==> controls(A)<=10. (10)

The general bound gives h<=12. At h=12, equality would give the
nonintegral lambda=16*(3/32)=3/2, excluded by (9). It remains to exclude
h=11. Delete dummy coordinates and suppose there are eleven.

Write A=sum z_S x_S/16 with integers z_S, |S|<=4. Then sum z_S²=24.
For each j put e_j=sum_(S contains j)z_S². By (1), e_j>=8. Also e_j is
even: sum_(S contains j)z_S=16 Delta_j A(+1) is a multiple of eight,
and z²=z modulo two. Thus e_j is either 8 or at least 10. Since
sum e_j<=4*24=96, at most four coordinates have e_j>8. At least seven
are good, meaning e_j=8.

For a good j equality in (1) forces Delta_j A to be a scaled minimum-
support polynomial of degree three. The tensor classification above has
exactly these seven degree-cost types:

|point factors|other blocks|controls in the partial|
|---:|---|---:|
|3|none|3|
|2|one pair|4|
|1|one triple|4|
|1|two pairs|5|
|0|one block of size four|4|
|0|one pair and one triple|5|
|0|three pairs|6|

Every such partial has exactly eight nonzero Fourier coefficients, each
of magnitude 1/16. Every control occurs in exactly four of those masks;
their mask intersection is empty. If it is not homogeneous, its average
Fourier degree is at most 5/2 (the six-control three-pair type alone is
homogeneous degree three). In particular, writing

    L=sum_S (4-|S|)z_S²=96-sum_j e_j,  0<=L<=8,
    L_j=sum_(S contains j)(4-|S|)z_S²,

every nonhomogeneous good partial has L_j>=4. Moreover
sum_(good j)L_j<=3L: only |S|<=3 contribute and at most |S| good
coordinates can belong to such a mask. If all at least seven good partials
were nonhomogeneous, their sum would be >=28, while 3L<=24. Hence some
good partial is homogeneous. Relabel its coordinate 0 and its three pairs
(1,2),(3,4),(5,6). Its eight corresponding A masks are
{0} union one element of each pair. All have coefficient magnitude 1/16.

Choose any six other good coordinates. Up to permuting the three pairs,
swapping their members, and permuting coordinates 7..10, the counts of
chosen good members in the pairs form a sorted triple a<=b<=c, each in
{0,1,2}; the number outside is 6-a-b-c in {0,...,4}. There are exactly
eight possibilities. Every eleven-control A under consideration is in
one of these cases; the four unselected coordinates may themselves be good.

For each selected good coordinate j, the possible unsigned Fourier support
of its partial is exactly the seven-type list embedded in the other ten
coordinates. These give 11,880 distinct eight-term patterns. A point
factor contributes masks {empty,{u}}, an even block all odd subsets,
and an odd block all even subsets; tensor products take disjoint unions.
Multiplying masks by x_j gives the corresponding A masks. This enumerates
all unsigned possibilities; signs are deliberately relaxed.

The frozen quartic_certificate.json.gz contains these templates (at j=0,
with other j obtained by swapping labels), all eight case trees, and their
complete surviving unsigned models. Checker A verifies every branch of
the proof trace. Checker B constructs the templates independently using
actual tensor truth tables and direct integer character sums, then repeats
the completion search in fixed coordinate order without reading the trace.

Here is the full logic of each finite branch. Let E be the union of masks
already forced by selected good partials. All these coefficients have
squared numerator one. A new partial must include all masks of E using
its coordinate, and cannot introduce any new mask using a previously
completed good coordinate. Every candidate template satisfying these
conditions is branched over; an empty domain excludes that branch.
The following necessary conditions prune branches:

* |E|<=24, because the total squared numerator norm is 24.
* sum_(S in E)(4-|S|)<=8, because all omitted contributions to L are
  nonnegative.
* If t=24-|E| and j ranges over the four unselected coordinates, then
  sum_j max(0,8-number of E masks containing j)<=4t. All remaining
  coefficients use only these four coordinates, and each unit of squared
  coefficient can contribute to at most four of their derivative energies.

These are relaxations of exact integer conditions, so none removes a valid
A. The exhaustive completion leaves zero models in the first six cases,
one in case 6, and eight in case 7. All nine have |E|=16 and at least two
unselected coordinates absent from E. Their masks are listed explicitly
in the certificate; no statistical sampling or floating-point decision is
used in either verification.

Let u,v be two absent coordinates in any surviving model. Exactly eight
units of squared numerator norm remain. Each of e_u,e_v is at least eight,
so both must equal eight, and every remaining nonzero Fourier term must
contain both u and v. But u is now good: the minimum-support classification
requires its partial's Fourier masks to have empty intersection. Instead
every mask of Delta_u A contains v. This is a contradiction. It rejects
all nine models and completes (10).

## 6. Count propagation and the finite scalar certificate

Use (4),(5), the allowed weights (6),(7), and the following control ceilings:

* combined: (2), using the improved base c4=11/8;
* second_equality: additionally h<=3k-1 at lambda=3/2;
* refined: additionally (9) at every nonintegral lambda;
* quartic: refined, plus (10) at d=5, lambda=3/2.

The combined mode recovers R5<=53, exactly the second input from gap1.
The quartic mode improves this to R5<=51: at lambda=1 its budget is at
most 50; at lambda=3/2 its budget is 44+10-(7/4)(3/2)=411/8, so N<=51;
at lambda>=7/4, (5) gives N<=floor(80/(7/4))=45. These cases cover all
allowed values. This is an upper bound, not an exact determination of R5.

At degree d, suppose c bounds W_(d-1). To exclude every N>=n it suffices
to check the allowed lambda in [1,dM/n], because this interval contains
all possibilities for such N. Below 2 enumerate (7). Above 2 split into
old floor cells a<=2k lambda<a+1. On their grid, let

    z=ceil(a M/(4k)),  x=2z/M.

Within a cell, the budget 2^d c+h+(1-2c)lambda is nonincreasing except
possibly immediately after a demoted equality endpoint. Test the first
and second grid points, retaining only those in the cell and interval.
After the first point, the ceiling is the old constant floor throughout
the remaining cell. Thus these two representatives cover every grid point.
Testing only the first point after imposing (9) would be invalid.

Each row records the preceding cap, first excluded count, complete case
count, most dangerous budget, and a feasible scalar point at the retained
count. Checker A excludes the next integer by exact rational arithmetic.
Checker B maximizes the minimum of the control budget and the influence
budget at fixed lambda using integer arithmetic. It also enumerates every
individual grid point through degree thirteen. It reads the cap artifact
only after deriving all its counts. Both prove the finite scalar ceilings;
feasible scalar points are not Boolean existence witnesses.

## 7. Infinite tail and lower bound

The CHS/Shinkar–Tal family starts Xi1=x and uses disjoint copies in

    Xi_d=(s+t)Xi_(d-1)(X)/2+(s-t)Xi_(d-1)(Y)/2.

Exactly one summand is active. All nonzero Fourier masks have size d and
all variables remain relevant. Its count is L1=1,L_d=2L_(d-1)+2, hence
L_d=3*2^{d-1}-2. This supplies 22,46,94 at d=4,5,6 and C44>=3/2.
Explicit sparse polynomials and integer XOR convolutions verify these
constructions in the frozen controls. No stronger lower bound is claimed.

For d>=2, R_d>=2M. Therefore its minimum-influence derivative has
lambda<=d/2. Apply (4) with the actual c=W_(d-1), and discard the floor
in (2), to get

    W_d<=W_(d-1)+lambda(2d-1-2W_(d-1))/2^d
        <=W_(d-1)+d(d-1)/2^d.                          (11)

The multiplier is positive and at most 2d-2 because
1/2<=W_(d-1)<=(d-1)/2. The standard geometric identities
sum_(j>=1)2^-j=1, sum j2^-j=2, sum j²2^-j=6 follow by differentiating
x/(1-x) once and twice with x d/dx, then substituting x=1/2. Expanding
(H+j)(H+j-1) gives

    sum_(d>H)d(d-1)/2^d=(H²+3H+4)/2^H.                 (12)

All certified finite caps are nondecreasing; both checkers verify this.
Thus their cap at H=96 bounds every smaller degree. For larger degrees,
telescope (11) and add the exact tail 9508/2^96. The exact rationals and
strict decimal comparisons for every mode are in certificate.json and
verified independently. The classified mode gives the headline rational above. Its strict decimal
comparison and improvement by more than 1/1000 over round six are exact
rational comparisons in both scalar verifiers. The frozen replay receipts
record the acceptance status; a prose proof alone does not assert that a
particular artifact has passed that replay.

## 8. Scope and remaining barrier

The classifications used here are minimum-support classifications and a
complete finite relaxation of eleven-control second-weight quartic
polynomials. They do not classify all real quartic Boolean functions, and
they do not prove R5=46 or R6=94. The complete t+5 resilient-function table
is unavailable: the primary 2023 classification already has over one
billion classes at six inputs. The 2024 addendum restricts binary ANF
degree and cannot replace the missing unrestricted real-quartic catalogue.

Even the sharp second-weight control ceiling ten leaves the scalar point
N=51 feasible. Further progress needs compatibility between an actual
signed derivative and its Boolean completion, stronger energy envelopes
for restricted quartics, or joint constraints on multiple derivatives.
Iterating the same scalar relaxation farther cannot close its remaining
positive gap: feasible scalar points plus the tail already locate its
infinite limit to less than 1.3e-25 at H=96.

## 9. The limit statement is only about this scalar relaxation

At each step the stored feasible point and strict next-count exclusion
prove the largest feasible integer for the specified scalar constraints.
For any previous scalar cap c with denominator dividing 2^{d-1},
N0=2^d c is integral. The allowed lambda=1 has h=2(d-1), budget
N0+2d-1-2c>=N0, and satisfies N0<=dM whenever c<=d/2.
Thus the scalar caps are nondecreasing. Each retained feasible count is
at least the CHS lower witness, so the estimates of section 7 also bound
its increment by d(d-1)/2^d. After degree 96 this is less than 1/2 per
step and preserves c<=d/2 inductively. Therefore the infinite scalar
sequence exists and its limit is between c96 and c96+9508/2^96.
The width is less than 1.3e-25. This does not prove optimality for Boolean
functions or for richer uses of the signed derivative classification.
