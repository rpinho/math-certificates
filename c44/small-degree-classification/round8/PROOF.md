# C44 round eight — candidate, unrefereed

The candidate bounds proved by this packet, subject to the explicitly
credited published premises and accepted exact replay, are

    R4=22, 46<=R5<=50, 94<=R6<=109,
    3/2 <= C44 <=
    80880411492166173705437336107/39614081257132168796771975168
    < 2.0417086280.

Both new scalar checkers are separately written by the same agent. This
is not independent human refereeing or a proof-assistant formalization.
The previous round's review is mathematical PASS with two prose errata,
recorded in INPUT_ERRATA.md and inputs/round7_REVIEW.md. Inherited files
are unchanged. No priority or public-record claim is made.

Sections 1–4 reproduce the credited definitions, elementary reductions and
nonintegral equality argument of the reviewed round-seven proof. The new
argument is sections 5–8. The main `simple` mode does not use the finite
quartic or quintic second-weight control classifications. An optional
`sharp` mode inserts their reviewed ten/twelve-control ceilings and gives
the same count sequence and final bound.

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
coverage is inherited in inputs/round7/inputs/round6/PROOF.md and its KTA audit.

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

## 5. Integer energy gap, with the scaling made explicit

We need the following inherited universal fact for integer-valued real
polynomials Q of degree at most r:

    E Q²=2^-r, or E Q²>=(3/2)2^-r.                    (13)

Here is its exact bridge to the cited lattice result. Integer bit
coefficients follow by the finite-difference formula in section 3. A
bit monomial of degree t is an affine-subspace indicator of codimension t.
For odd r, multiply Q's truth vector on n bit inputs by 2^((r-1)/2).
Every monomial prefactor is divisible by the generator prefactor
2^floor(t/2) of the integral Barnes–Wall model Lambda_n. Its squared norm
is 2^(r-1)2^n E Q²; the lattice minimum is 2^(n-1). Their ratio is exactly
2^r E Q². For even r use the model Delta_n with generator prefactors
2^ceil(t/2), scale 2^(r/2), and lattice minimum 2^n; the same ratio follows.
Dummy variables ensure n>=max(r,2) and multiply both norms and minima by
two, preserving the ratio.

Nebe's second-minimum theorem says that a nonminimal vector in either
model has norm at least 3/2 of the minimum. The integer-polynomial minimum
itself follows from the support lemma and nonzero integer values. These
facts give (13). The full norm-gap induction, coefficient congruences,
similarity, base arithmetic, and classical premises are expanded in
inputs/round7/BW_GAP_PROOF.md sections 1–5. The external classical premises
are the Barnes–Wall basis/minimum and Broué–Enguehard pair-preserving
minimum-vector transitivity, with the precise n=3 convention from Nebe.
Their group classification is an explicit published dependency; finite
checks do not prove it. No binary affine coordinate change is used to
preserve real degree.

For the ternary derivative A of section 2, put k=d-1 and e0=2^(-k-1).
For every relevant j, Q_j=2 Delta_j A is integer-valued of degree <=k-1.
Equation (13) gives

    e_j=E(Delta_j A)²=e0, or e_j>=3e0/2.             (14)

Also sum e_j<=kp=2k lambda e0. Thus if h>4k lambda/3, at least one j
has e_j=e0: otherwise the sum is at least 3h e0/2>2k lambda e0.

At e_j=e0, Q_j attains its minimum energy. Its support has density at
least 2^(-(k-1)) and each nonzero squared value is at least one. Equality
in the product of these bounds forces every nonzero Q_j to be +/-1.
Consequently Delta_j A has values only 0,+/-1/2.

## 6. Two Boolean completion budgets

All coordinates of the count maximizer have original weight 2^-d. The
coordinatewise restriction inequality from section 2 can be applied to
any specified set of coordinates outside the restricted controls; its
proof is a sum of individual nonnegative slacks.

First restrict all H. On active assignments, no Y variable survives. On
inactive assignments, the resulting Boolean function is independent of i,
has degree <=d-1, and its Y-potential is at most c for any c>=W_(d-1).
There are N-h-1 original Y variables, so

    (N-h-1)/2^d <= (1-p)c,
    N <= 2^d c+h+1-2c lambda.                       (15)

The earlier ordinary budget (4) discarded mandatory slack from i:
after restriction its mean potential is p/2=lambda/2^d, compared with
its original weight 1/2^d. Equation (15) gains exactly lambda-1 in the
count budget, and is valid even when lambda=1.

Now suppose lambda>1 and h>4k lambda/3. Choose j supplied by (14). Let q
be the fraction of j-edges, indexed by H minus j, with exactly one active
endpoint; let r be the fraction with two active endpoints. The two active
endpoints have the same sign, because Delta_j A never has magnitude one.
The only nonzero derivative values have square 1/4, so

    q=4e0=2^(1-k),  p=q/2+r,
    r=(lambda-1)2^-k>0.                             (16)

In particular the active set contains an edge parallel to j. Any real
affine polynomial in H that vanishes on the active set has zero x_j
coefficient: evaluate on the endpoints of this edge and subtract.

Put K=H minus j. We prove that K hits every degree-d Fourier monomial.
For a Y-mask T of size d, its B coefficient is constant in H and vanishes
on an active assignment, so it is zero. For |T|=d-1, that coefficient is
affine in H, vanishes on all active assignments, and hence its x_j
coefficient is zero by the edge just found. These are all degree-d
monomials of B missing K, since only one H-coordinate j remains outside K.
A monomial of x_i A missing K uses at most i,j and has degree <=2<d.
Thus restriction of K always leaves degree <=d-1.

Consider a section F(i,j,Y) after this restriction. If neither endpoint
is active, F is independent of i and D_{j,Y}(F)<=c. If both are active,
F is a signed dictator i and D_{j,Y}(F)=0. If exactly one endpoint is
active, change input/output signs to write

    F=(1+j)i/2+(1-j)g(Y)/2.                         (17)

The function g is sign Boolean. If deg g=t>=1, then t<=d-2: each nonzero
Y-monomial of degree t in g gives a nonzero monomial of degree t+1 with j
added in (17), while F has degree <=d-1. Coordinate i has local degree
two, j has local degree t+1, and each relevant Y-coordinate has its old
local degree in g increased by exactly one. Therefore

    D_{j,Y}(F)=2^(-t-1)+D(g)/2.

If g is constant, D_{j,Y}(F)=1/4. For certified caps c_t>=W_t define

    b_d=max(1/2, max_(1<=t<=d-2)(1/4+2^(-t-1)+c_t/2)).

Then D_{j,Y}(F)<=b_d-1/4 on every one-active edge, including constant g.
The number of original variables in {j} union Y is N-h. Restrict K and
apply the coordinatewise inequality only to this set. Using (16),

    (N-h)/2^d <= c(1-q-r)+(b_d-1/4)q,
    N <= 2^d c+h-2c lambda
         +4(b_d-(c+1/2)/2).                         (18)

Every term is explicit: q=2^(1-k), so 2^d q=4; and q+r=p+q/2. This
also explains why i contributes exactly the same mandatory slack as in
(15): its section potential is 1/4 on one-active edges and 1/2 on
two-active edges, with average q/4+r/2=p/2.

For a fixed lambda and its certified h ceiling, use (15) at every integer
0<=h<=hmax, and additionally (18) where lambda>1 and 3h>4k lambda.
Take the smaller valid budget at each h, then maximize over h. This
explicit maximization prevents an unsupported inference about the actual
number of controls. Both budgets increase with slope one as functions
of h within each of the two applicability ranges. It suffices to test
hmax and h0=min(hmax,floor(4k lambda/3)); (15) alone covers lambda=1.

## 7. R5 and R6, without the finite second-weight classifications

At degree five, c4=11/8 and b5=15/16. If lambda=1, h<=8 and (15) gives
44+8+1-11/4=201/4=50.25, hence integer N<=50. If lambda=3/2,
section 4 gives h<=11. For h<=8, (15) gives at most 391/8=48.875.
For 9<=h<=11, (18) applies and gives at most
44+11-(11/4)(3/2)=407/8=50.875. Thus integer N<=50 here too.
Every other allowed lambda is >=7/4, so (5) gives
N<=floor(80/(7/4))=45. These cases exhaust the spectrum, proving R5<=50.

At degree six, c5=50/32=25/16 and b6=31/32, so
4(b6-(c5+1/2)/2)=-1/4. For lambda=1, (15) and h<=10 give
100+10+1-25/8=863/8=107.875. For lambda=3/2 section 4 gives h<=14.
When h<=10, (15) gives at most 1701/16=106.3125. For 11<=h<=14,
(18) gives at most 100+14-75/16-1/4=1745/16=109.0625.
Every remaining lambda is >=7/4, giving
N<=floor(192/(7/4))=109. Thus R6<=109.

These arguments use neither h<=10 for quartic second-weight derivatives
nor h<=12 for quintic ones. Inserting those reviewed classifications
excludes additional scalar cases but leaves the same maximal counts.

## 8. Complete exact scalar propagation

completion_certificate.json contains two modes. `simple` uses the general
control ceiling (2) with the nonintegral equality exclusion (9).
`sharp` also imposes h<=10 at d=5,lambda=3/2 and h<=12 at d=6,lambda=3/2,
proved in the reviewed input PROOF.md section 5 and LATTICE_PROOF.md.
Both use (15),(18), the spectrum (6),(7), and the influence constraint (5).
They give identical integer counts at every degree through 96.

Here are all discretization details. Put G=2^(d-2), so the energy grid is
lambda=z/G with integer z. Below two, enumerate exactly all allowed values
(7). Above two, hmax is floor(2kz/G), except for its one-unit demotion when
lambda is nonintegral and 2k lambda is integral. The other applicability
endpoint is h0=floor(4kz/(3G)), clipped at hmax. Between changes of these
two floors and away from a demoted endpoint, the maximized budget has a
constant intercept and slope -2c in lambda, hence is nonincreasing. The
influence ceiling d2^(d-1)/lambda is also nonincreasing.

The first index in a floor(2kz/G) cell is ceil(aG/(2k)); test it and the
next index to cover the possible demotion at the first point. Changes of
floor(4kz/(3G)) occur at ceil(3aG/(4k)); test each such index as well.
The generator and checker A harmlessly include one extra following point.
Include the first grid point at lambda=2. These representatives cover the
first index in every joint cell and the point after each demotion. No
untested interior index can improve the budget. All rounding is integer
ceiling/floor arithmetic.

For each row, checker A takes n=R+1 and tests every representative in
[1,d2^(d-1)/n]. Each control budget is strictly less than n. If an actual
count were >=n, its minimum influence would be in that interval and could
not satisfy (15),(18), proving the claimed R ceiling. It checks every h
through degree twelve, the exact two-endpoint reduction thereafter, and
an allowed feasible point at the retained R. The feasible point is only
a witness for these scalar constraints.

Checker B uses a separately written integer optimization, with denominator
G². If C is the preceding integer count, c=C/(2G), and B=b_d*(2G), the
ordinary budget numerator is

    (2C+h+1)G²-Cz.

Where applicable the retained-control improvement adds

    min(0,(2B-C-2G)G).

It independently maximizes the smaller of the resulting integer budget
and floor(2dG²/z), derives all counts before comparing with the artifact,
and scans every individual original energy-grid point through degree
sixteen. It uses neither generator code nor checker A's implementation.
The two checkers verify the same exact rational bound and strict decimal
comparison. Their proof depends on the written universal lemmas above;
finite tests cannot replace the published completeness or lattice premises.

## 9. Tail, lower family, and where the scalar route ends

The CHS/Shinkar–Tal family is Xi1=x and, on disjoint inputs,

    Xi_d=(s+t)Xi_(d-1)(X)/2+(s-t)Xi_(d-1)(Y)/2.

Exactly one summand is active. Induction proves sign Booleanity,
homogeneous real degree d, and relevant count L_d=2L_(d-1)+2
=3*2^(d-1)-2. Thus L4=22,L5=46,L6=94. The sparse integer convolution
control independently verifies f²=1 and every variable through degree six.
Iterating this construction from any degree-d seed with n variables gives
2^t(n+2)-2 variables at degree d+t, and hence C44>=(n+2)/2^d. A
47-variable degree-five seed would therefore imply C44>=49/32; none was
found by the construction classification described in LOWER_ROUTE.md.
The unconditional lower bound remains 3/2.

For completeness, the tail bound does not rely on eventual behavior
observed in the finite rows. Since R_d>=L_d>=2^d for d>=2, (5) gives
lambda<=d/2. Revert to the weaker valid budget (4), set c to the actual
W_(d-1), and use h<=2(d-1)lambda. Then

    W_d <= W_(d-1)+lambda(2d-1-2W_(d-1))/2^d
         <= W_(d-1)+d(d-1)/2^d.

The last multiplier is positive and <=2d-2, since
1/2<=W_(d-1)<=(d-1)/2. To sum the tail, differentiate x/(1-x) once
and twice with x d/dx, and set x=1/2. This gives sums of 1,j,j² times
2^-j equal to 1,2,6. Expand (H+j)(H+j-1) to obtain

    sum_(d>H)d(d-1)/2^d=(H²+3H+4)/2^H.

Both checkers verify nondecreasing certified finite caps. At H=96,
add 9508/2^96 to the certified c96, giving

    C44 <= 80880411492166173705437336107 /
           39614081257132168796771975168
        < 2.0417086280.

The exact gain over the round-seven rational is

    164865563398608188023949601889/79228162514264337593543950336
    -80880411492166173705437336107/39614081257132168796771975168,

which both independent checkers compare with 1/1000 using integer/rational
arithmetic. No displayed floating-point decimal enters a proof.

The feasible scalar points explain the remaining limitations. With the
reviewed sharp input controls, R5=50 remains feasible only at lambda=1
among the possible low weights; its ordinary budget is 201/4. Thus the
new obstacle there is completion of a minimum-support quartic derivative,
including the four-pair case. R6=109 remains feasible at lambda=7/4 with
h=17; its retained budget is 3561/32=111.28125, while its influence budget
is 768/7>109. These are not Boolean existence witnesses. A third-weight
quintic control ceiling h<=14 would lower that case's budget to 3465/32
=108.28125, but no such ceiling is asserted in this packet.

For the fixed scalar system, let c be a prior cap with denominator dividing
2^(d-1). The integer N0=2^d c is feasible at lambda=1,h=2(d-1): its budget
is N0+2d-1-2c>=N0 and its influence budget allows N0 when c<=d/2.
Thus the maximal scalar caps are nondecreasing. They also exceed L_d/2^d,
so the preceding tail increment estimate applies to this scalar sequence.
The checked rows maintain c<=d/2. Beyond degree 96 the remaining tail is
less than 1/2, so c stays below d/2 inductively, and the same estimate
continues. Consequently the infinite limit of this *fixed scalar
relaxation* lies between c96 and c96+9508/2^96, an interval narrower than
1.3e-25. Iterating it farther will not reach 1.5. This is no optimality
assertion about Boolean functions or richer completion constraints.
