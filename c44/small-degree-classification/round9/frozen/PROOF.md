# C44 round nine — candidate, unrefereed

The candidate upper bound supplied by this packet is

    R4 = 22,  46 <= R5 <= 50,  94 <= R6 <= 107,

    3/2 <= C44 <=
    80058654243525646012949597587 / 39614081257132168796771975168
    = 2.0209645586343564549657602787563884778103580828967...
    < 2.0209645587.

The exact gain over the round-eight rational is greater than 1/10000.
The lower bound is unchanged. This is a computer-assisted candidate,
unrefereed by a human and without proof-assistant formalization. The two
exact implementations were written separately in the same agent session.
Passing them does not independently prove the classical completeness
premises listed below. No novelty, priority, or public-record claim is made.

## 1. Explicit inherited premises and notation

We use sign inputs and sign Boolean outputs. Write

    f(x) = sum_S fhat(S) x_S,
    D(f) = sum_(i relevant) 2^(-d_i(f)),
    R_d = max R(f) over degree <= d,   W_d = max D(f) over degree <= d.

Here d_i is the largest size of a nonzero Fourier mask containing i.
The constant is C44=sup_d R_d/2^d=lim_d W_d. The classes of Boolean
functions of degree at most d are nested, so W_d is nondecreasing; the
CHS identity identifies this with monotonicity of R_d/2^d. The upper
bounds and convergent tail below establish finiteness of this limit.
The finite maxima, CHS identity W_d=R_d/2^d, all-local-degrees-d reduction
for a count maximizer, and the coordinatewise restriction inequality are
proved in the retained input `inputs/round8/PROOF.md`, sections 1–2.
The elementary nonzero-support bound is: a nonzero real polynomial of
degree at most r is nonzero on a fraction at least 2^-r of its cube.
Its proof is induction after writing P=x_j U+V: whenever U is nonzero,
at least one of V+U,V-U is nonzero. Iterating gives the stated fraction.

The following are the inherited published inputs. Their precise sources,
normalizations and expanded proofs are retained in the input packet.

1. R1=1, R2=4, R3=10 and candidate R4=22. The last uses the complete
   Rasoolzadeh 761-class cubic catalogue, its exactly checked potential
   versus cubic-energy inequality, and Valyuzhenich's minimum-support
   classification. See `inputs/round8/inputs/round7/inputs/gap1/PROOF.md`.
   The catalogue completeness, rather than a finite test of it, is a
   published dependency. R3=10 is credited to Tarannikov–Kirienko.
2. For a nonzero integer-valued real polynomial Q of degree at most r,

       E Q^2 = 2^-r,  or  E Q^2 >= (3/2)2^-r.

   The integer-polynomial embedding into the two integral Barnes–Wall
   models, their exact scaling, and the norm-gap induction are in
   `inputs/round8/inputs/round7/BW_GAP_PROOF.md` and `LATTICE_PROOF.md`.
   The remaining external premises are the classical lattice basis,
   minimum and pair-preserving minimum-vector transitivity, credited to
   Barnes–Wall, Broué–Enguehard and Nebe. This is not inferred from a
   finite truth-table test or from preserving real degree under F2 maps.
3. Equality in the real support bound is classified by Valyuzhenich,
   arXiv:2303.10995, Theorem 2(2): up to signs and permutations, a minimum
   polynomial is a product on disjoint coordinate sets of point factors
   and blocks supported on two opposite strings. An m-block has degree
   m-1; for even m its two nonzero values have opposite signs, and for
   odd m they have the same sign. A point has degree one. This published
   completeness statement is an explicit dependency of the enumeration.
4. The support indicators of ternary derivatives are binary polynomials
   of degree at most their real degree, by reduction of their integer bit
   coefficients modulo two. The Berlekamp–Sloane/Kasami–Tokura below-two
   weight theorem then gives the allowed normalized weights used below.
   The bridge, dummy-variable parameter padding, exact even Fourier grid
   and sources are in input sections 3–4. The nonintegral equality
   exclusion for the general control bound is also inherited there.
5. At normalized weight 3/2, quartic ternary derivatives have at most ten
   controls and quintic ones at most twelve, as proved and separately
   exactly checked in input round-seven `PROOF.md` and `LATTICE_PROOF.md`.
   These sharp inputs are used here. The new packet does not claim a
   version of its headline number that omits them.

All elementary inherited arguments are included as text in the packet;
the above list separates the external completeness/group premises from
the new finite computation. The new mathematical result is the following
third-weight control ceiling and its effect on the restriction recurrence.

## 2. The new finite statement and integer energy bookkeeping

We prove the candidate statement

    A : {-1,1}^h -> {0,-1,1},  deg A <= 5,
    E A^2 = 7/128  ==>  h <= 13,                         (T)

where h counts precisely the relevant coordinates, with dummy inputs
deleted. An integer-valued cube function has integer coefficients in bit
coordinates by finite differences. Substitution bit=(1-sign)/2 shows
that a real-degree-at-most-five integer function has Fourier coefficients
in (1/32)Z. Therefore write

    A = sum_(|S|<=5) z_S x_S / 32,   z_S integers.

Parseval and the assumed energy give

    sum z_S^2 = 56.

For each relevant j define e_j=sum_(S contains j) z_S^2, and define

    L = sum_S (5-|S|) z_S^2 = 280 - sum_j e_j >= 0.

The polynomial Q_j=2 Delta_j A is integer-valued of degree at most four,
where Delta_j A=(A(j=1)-A(j=-1))/2. The norm-gap premise gives

    e_j = 16,  or  e_j >= 24.                            (1)

Indeed E(Delta_j A)^2=e_j/1024 and E Q_j^2=4e_j/1024;
its minimum is 1/16, and the next allowed energy is at least 3/32.
Every relevant partial is nonzero. In particular 16h<=280, so h<=17.
It suffices to exclude h=17,16,15,14.

Call j good if e_j=16, and let g be the number of good coordinates.
Summing (1),

    280-L >= 16g+24(h-g) = 24h-8g,
    g >= 3h-35+L/8.                                     (2)

At a good j, Q_j has minimum squared energy 1/16. Its support has density
at least 1/16 and its nonzero integer values have squared magnitude at
least one. Equality forces support exactly 1/16 and values 0,+/-1.
Thus Delta_j A has values 0,+/-1/2. By the minimum-support classification
it is a degree-cost-four tensor. Consequently its sixteen nonzero A
coefficients all have |z_S|=1. Each mask contains j. After deleting j,
every control in that tensor appears in eight masks, and no coordinate
appears in all sixteen. These assertions follow directly from the factor
Fourier supports described next; no signed consistency is assumed by
the unsigned search.

## 3. Every possible minimum partial and its degree loss

A point factor has Fourier support {empty,{u}}. An even m-block has every
odd subset of its m coordinates as Fourier support. An odd m-block has
every even subset. Each elementary nonzero coefficient has absolute value
2^(-degree cost). Disjoint multiplication forms all unions of the factor
masks, without overlap or cancellation. A cost-four tensor therefore has
exactly sixteen coefficients, each with absolute value 1/16 before the
additional factor 1/2 for Delta_j A.

The twelve possible multiplicity vectors (points,pairs,triples,fours,fives)
are exactly the nonnegative solutions of

    a+b+2c+3d+4e=4:

    (4,0,0,0,0), (3,1,0,0,0), (2,2,0,0,0),
    (1,3,0,0,0), (0,4,0,0,0), (2,0,1,0,0),
    (1,1,1,0,0), (0,2,1,0,0), (0,0,2,0,0),
    (1,0,0,1,0), (0,1,0,1,0), (0,0,0,0,1).

Each is embedded on disjoint labelled coordinates other than j. Multiplying
the corresponding mask lists and adjoining j gives the entire unsigned
minimum-partial template. Input/output sign changes change coefficients'
signs but do not change these unsigned supports. No binary affine change
of coordinates is used to shorten the list.

The unique homogeneous minimum partial is four pairs; its A masks all
have size five. Every other type uses at most seven controls. The average
mask size within a nontrivial m-block is m/2; the same formula holds for
a point with m=1. Thus a nonhomogeneous good partial has average A-mask
size at most 1+7/2=9/2. Its contribution to L, summed only over masks
containing j, satisfies

    L_j := sum_(S contains j)(5-|S|)z_S^2 >= 16/2=8.     (3)

Only masks of size at most four contribute to L. Each such mask is counted
in L_j for at most four good j. Therefore

    sum_(j good) L_j <= 4L.                             (4)

If no good partial is homogeneous, (3),(4) give 8g<=4L.
For h=17, (2) gives g>=16+L/8 while L<=280-17*16=8;
these contradict 8g<=4L. For h=16 the same calculation gives
g>=13+L/8 and L<=24; it would require 104+L<=4L, impossible.
For h=15, g>=10+L/8 and 8g<=4L imply L>=80/3, hence integer L>=27,
and g>=ceil(10+27/8)=14. For h=14 with no homogeneous good partial, the same inequalities give
56+L<=4L, hence L>=19 and g>=ceil(7+19/8)=10. These are all the needed
reductions.

## 4. All 189 canonical cases

First suppose a homogeneous good partial exists. Relabel it as coordinate
0, with pair controls (1,2),(3,4),(5,6),(7,8). Its sixteen forced masks are
coordinate 0 plus one member from each of the four pairs. Select a total
of 16,13,10 good coordinates when h=17,16,15, respectively, including 0.
This is possible by (2). Within each pair let a_i be the selected count.
The seed is invariant under pair permutations and swaps inside each pair,
so take 0<=a1<=a2<=a3<=a4<=2. If b good coordinates are selected outside
the seed, then

    b = (selected good count)-1-sum a_i,
    0 <= b <= h-9.

Taking every such integer tuple gives exactly 2,6,11 cases. All outside
coordinates are equivalent under the seed symmetry, so select the first b.
There is no assumption that the unselected coordinates are non-good.

For h=15 with no homogeneous good partial, select fourteen good coordinates
including 0. Exactly one coordinate is unselected. The seed at 0 has one
of the eleven nonhomogeneous types. The unselected coordinate may occur
in a point block, in an m-block of each size present, or outside the seed.
Within a block its coordinates are symmetric in unsigned support, and
identical blocks may be permuted. Thus one position for each present size
and one outside position exhausts the possibilities. The numbers of such
positions, for the eleven types in lexicographic multiplicity order, are

    2,2,3,3,3,4,3,3,3,3,2,

which sum to 31. There are 2+6+11+31=50 cases at h=17,16,15.
`certificates/third_weight.json` fixes all selected sets, seed blocks,
expected zero unresolved leaves, and exact input files. There are two
additional h=14 branches. If a homogeneous good partial exists, select
seven good coordinates including 0. The same four-pair count enumeration
with b=6-sum a_i and 0<=b<=5 gives twelve cases.

If none exists, select ten good coordinates including 0, using the last
reduction of section 3. Fix any of the eleven nonhomogeneous seed types.
For each block of size m choose how many of its coordinates are among
the nine further selected good coordinates. Within a block only this
number matters; for multiple blocks of the same size sort their chosen
counts. The remaining selected coordinates are the first b outside the
seed, where b=9 minus the sum of all block counts and 0<=b<=h-1 minus
the total seed-control count. Enumerating these integers gives 127 cases.
This covers every placement under all seed symmetries, without assuming
that unselected coordinates are bad. Total case count is 50+12+127=189.

Both Python
packet verifiers, separately written (same agent), reconstruct these cases and compare them
with the artifact; one uses multiplicity vectors and one uses cost
partitions. This checks that a missing case cannot silently pass.

## 5. Complete unsigned completion and all its pruning rules

Maintain E, the union of Fourier masks already forced by completed good
partials, and J, the set of completed good coordinates. Every coefficient
on E has squared integer numerator one. All other squared coefficients
have total

    r = 56-|E|.

No unknown nonzero coefficient can involve a coordinate of J: that
coordinate's complete sixteen-term minimum partial has already been fixed.
For each selected good j not in J, consider every degree-cost-four tensor
on the actual h-1 labelled controls. It must contain every current E mask
using j and introduce no new mask involving J. Each surviving tensor is a
branch, replacing E by its union with the tensor and adding j to J.
Thus every actual A remains in at least one branch throughout. Ignoring
signs only enlarges this necessary-condition search space.

The following prunes are all necessary conditions, with nonnegative
squared-coefficient accounting:

* |E|<=56 and forced degree deficit <=280-16h.
* A selected good coordinate has at most sixteen current masks.
* Each unselected coordinate needs eventual energy at least sixteen.
  If c_j current masks use it, the sum of max(0,16-c_j) over unselected
  coordinates is at most their number times r. Each unknown coefficient
  contributes its squared numerator to each coordinate it contains, so
  this inequality remains valid for coefficients of magnitude greater
  than one.
* One selected good coordinate absent from E needs sixteen new unit
  coefficients. Two absent good coordinates need at least twenty-four:
  each needs sixteen, and their two minimum partials can overlap in at
  most eight masks, because every other control occurs in only eight
  masks of a fixed minimum partial. Therefore r<16 excludes one absent
  good coordinate, and r<24 excludes two.
* A complete tensor domain can be empty; this is checked exhaustively,
  rather than inferred from a heuristic sampling of embeddings.

After all initially selected good coordinates are completed, continue
with any still-unfinished coordinate j for which c_j+r<24. If c_j+r<16,
the branch is impossible. If c_j>16 but c_j+r<24 it is also impossible
by (1). In the remaining case, energy sixteen is forced, so complete its
entire minimum tensor just as above. In the case with no homogeneous good
partial, any newly forced good partial must also be nonhomogeneous.
Each such completion adds a new coordinate to J, so this process terminates.

The additional rejections are the independent-residual lemma and the
affine-sign minimum-piece lemma in the next section. A terminal state not rejected by these rules is counted as
unresolved and makes the verifier fail. Thus an unclassified residual
signing or an unfinished branch cannot be counted as an exclusion.

## 6. Independent-residual lemma, including the strict threshold

Suppose every E mask uses only coordinates in J and has odd cardinality.
Write the forced polynomial as T(X)=sum_(S in E) z_S x_S/32. Every unknown
coefficient uses only coordinates outside J, so A=T(X)+U(Y) on disjoint
inputs. The variables X cover all coordinates of T. For each X coordinate
the corresponding partial of A has energy sixteen, and hence values
0,+/-1/2, as proved in section 2. Therefore each edge difference of T is
an integer. The X cube is connected, so every T value belongs to one
fixed coset alpha+Z.

All E masks have odd size, so T(-X)=-T(X). The two values T(X),-T(X)
belong to the same coset; hence 2alpha is an integer. The coset is Z or
Z+1/2. If it were Z+1/2, every squared value would be at least 1/4.
But Parseval gives

    E T^2 = |E|/1024 < 1/4

in every use of this rejection. Thus T is integer-valued. It is nonzero
since E is nonempty, and oddness gives a value at least +1 and a value at
most -1. Fix any Y, and write u=U(Y). Because T+u is ternary, a T value
at least +1 forces u<=0, and a T value at most -1 forces u>=0. Therefore
u=0 for every Y. This contradicts positive remaining squared norm r>0.

The test requires a strict inequality. At the boundary, T=x/2 and U=1/2
give a ternary sum despite nonzero U. This boundary counterexample is an
explicit rejection control. No unsigned sign-factorization assertion is
needed for the lemma; integrality follows from the actual minimum partials.


## 6a. Affine-sign minimum-piece lemma

The second rejection applies when E has thirty-two masks and their affine
span over F2 has dimension five. Translating by one mask and checking
linear rank five establishes that E is an entire affine five-flat: its
span contains exactly 32 points and E already has that size. This is
linear algebra on Fourier mask indices, not a change of real input
coordinates.

Write z_S=(-1)^{a_S} on E, with 32 unknown sign bits. On every completed
good partial, the sign vector is an affine character of its sixteen-mask
four-flat. To justify this, the canonical tensor factors in section 3
have all positive Fourier coefficients on their listed supports. Input
sign changes multiply a coefficient by a character of its mask, and an
output sign adds a constant sign bit. The minimum-support classification
exhausts the actual partials by these operations. Thus every actual
signing satisfies the local affine-sign equations.

Both verifiers assemble these linear equations over F2 on the 32 sign
bits. A uses a chosen affine basis of each local four-flat and imposes
each of its eleven remaining values as an affine combination of the
basepoint and four basis values. B instead takes every linear dependence
among the sixteen evaluation vectors (1,S) and imposes the same dependence
on the sign bits. Each construction exactly characterizes the local
affine functions; no signed sampling is used.

Global affine functions on a five-flat form a vector space of dimension
six and satisfy all local equations. Therefore the local equations have
rank at most 32-6=26. If their exactly computed rank is 26, their full
solution space is precisely this global six-dimensional space. In that
case the actual coefficients have a_S=b+u dot S on E, for some b and u.
Every affine function on the flat extends to this form on the ambient
mask space by extending a basis.

Write E=S0+V with dim V=5. The forced Fourier polynomial is then

    T(x)=(-1)^b/32 * sum_(S in S0+V) (-1)^(u dot S) x_S.

Its sum is a character at S0 times the character sum on V. If this
character is trivial on V, the inner sum is 32. Otherwise choose v in V
where it is -1; pairing each w with w+v cancels the sum. Hence T takes
only values 0,+/-1. It is an integer-valued polynomial of real degree at
most five because every original E mask has size at most five.

Consequently A-T is integer-valued of degree at most five. All its
Fourier coefficients are outside E, so its squared energy is r/1024,
where r=56-32=24. It is nonzero since r>0. But the real support bound
and integer values give E(A-T)^2>=1/32=32/1024, a contradiction.
This rejects the branch. The implementation requires exactly these
conditions: 32 forced unit coefficients, affine dimension five, local
equation rank 26, and 0<r<32. A smaller rank is not an exclusion.

This extra lemma is what completes the four formerly unresolved h=14
homogeneous cases. The other eight homogeneous and 127 nonhomogeneous
cases already close without it. It makes no claim that every unsigned
pattern is a signed minimum polynomial; the computed rank is essential.

## 7. Two separately written exact finite verifiers

`verify_third_a.cpp` computes each elementary factor's Fourier support
by direct character sums on its truth table, enumerates every disjoint
block embedding, and indexes the complete resulting template catalogue.
It maintains a mutable coefficient-incidence array, installs/removes
templates under backtracking, and chooses its next coordinate by a
rarest-index estimate. It memoizes compatibility by the next coordinate,
the completed-coordinate set and the already required masks at that
coordinate. This key suffices: every candidate mask contains that next
coordinate, so membership in E is exactly membership in its required-mask
list. The no-new-mask-at-completed-coordinates rule therefore depends
only on this key. Norm and degree-deficit bounds are checked afresh outside
the cache. Cached domains are never used as heuristic samples. Its complete catalogues have respectively
359502,752752,1479478,2757118,4910178 templates on 13,14,15,16,17
coordinates.

`verify_third_b.cpp` uses no global template catalogue. Given the currently
required masks of a partial, it enumerates all possible blocks satisfying
their local parity conditions, then every disjoint degree-cost-four block
partition. It also requires that the union of blocks contain every control
already present in a required mask. These conditions are necessary for
every compatible tensor; the final generated mask list is checked to
contain all required masks. The whole conditional domain is enumerated,
not one guessed normal form. It uses a different branching order, copied
sorted support sets, and energies and deficits recomputed by a separately written (same agent) checker.

Both implementations branch over all compatible domains, apply only the
rules proved in sections 5–6, and demand zero unresolved states for every
one of the 189 canonical cases. Neither imports the exploratory search or
the other verifier. Exact integer computations suffice throughout.
Their successful replay excludes h=17,16,15,14. Since h<=17 by energy, (T)
follows, subject to the explicitly stated classical premises.

## 8. Consequence for Boolean R6 and the exact restriction budgets

For clarity, the inherited budgets used here are restated. Let f be an
R_d extremizer with every local degree d. Choose a minimum-influence
coordinate i, set k=d-1, M=2^k, A=Delta_i f, p=E A^2 and lambda=Mp.
Let H be the h controls of A and let Y be the remaining variables other
than i. Then 1<=lambda<=dM/R_d, h<=floor(2k lambda), and every restriction
to H has degree at most d-1. On the active fraction p the Y function
vanishes. Applying the coordinatewise restriction inequality only to Y
gives, for c>=W_(d-1),

    R_d <= 2^d c+h+1-2c lambda.                         (C2)

If lambda>1 and 3h>4k lambda, the norm gap supplies a control j whose
partial of A has minimum energy. There is an active j-edge: exactly-one-
active edges have fraction q=2/M and both-active edges fraction
r=(lambda-1)/M>0. The endpoint difference cannot be 2, since that partial
has values 0,+/-1/2. An affine coefficient vanishing on the active set
therefore has zero j coefficient. Consequently H minus j hits every
degree-d monomial. After this restriction, a one-active section is
(1+j)i/2+(1-j)g(Y)/2 with degree g<=d-2. Its potential on {j} union Y is
2^(-t-1)+D(g)/2 when degree g=t>=1, or 1/4 for constant g.
Set

    b_d=max(1/2, max_(1<=t<=d-2)(1/4+2^(-t-1)+c_t/2)).

Neither-active sections have potential at most c, both-active sections
zero on {j} union Y, and one-active sections at most b_d-1/4. Applying
the coordinatewise inequality to these N-h original coordinates gives

    R_d <= 2^d c+h-2c lambda
           +4(b_d-(c+1/2)/2).                         (C3)

This derivation is expanded in input sections 5–6; in particular the
applicability condition is checked for the actual h, not merely its cap.

At d=5 the inherited caps give R5<=50: lambda=1 has C2 budget 201/4;
lambda=3/2 uses the sharp h<=10 and has maximum budget 399/8 once C3
applies (smaller h use C2); every lambda>=7/4 has influence budget
80/lambda<=320/7<46. Thus c5=50/32=25/16.

Now suppose R6>=108. Then lambda<=192/108<15/8. The below-two spectrum
and Fourier grid leave only lambda=1,3/2,7/4. At d=6, b6=31/32 and the
correction in C3 is -1/4.

* lambda=1: h<=10, so C2 gives R6<=863/8<108.
* lambda=3/2: the inherited sharp ceiling is h<=12. For h<=10, C2 is
  at most 1701/16<107. For 11<=h<=12, C3 applies and is at most
  100+12-75/16-1/4=1713/16<108.
* lambda=7/4: A has energy 7/128, so (T) gives h<=13. For h<=11,
  C2 is at most 3409/32<107. For 12<=h<=13, C3 applies and is at most
  100+13-175/32-1/4=3433/32<108.

Every possible case is incompatible with R6>=108. Hence R6<=107.
The known 94-variable degree-six Xi function supplies the unchanged
lower witness; no claim that R6=107 is made.

## 9. Complete finite scalar propagation and infinite tail

At each d>=5, the certificate uses C2 for every integer 0<=h<=hmax and
also C3 where lambda>1 and 3h>4(d-1)lambda, taking the smaller valid
budget. The general h ceiling is floor(2(d-1)lambda), demoted by one
when lambda is nonintegral but 2(d-1)lambda is integral. The inherited
special ceilings are ten/twelve at (d,lambda)=(5,3/2),(6,3/2); the new
ceiling thirteen is inserted at (6,7/4). The h maximization tests the
top of each applicability regime, since each budget has slope one in h.

Write G=2^(d-2), lambda=z/G. Below two, enumerate exactly
2-2^-j for j=0,...,d-2. At and above two, z is any integer. Within a
joint cell of floor(2(d-1)z/G) and floor(4(d-1)z/(3G)), the maximized
control budget has constant intercept and nonpositive slope in z; the
influence budget d2^(d-1)/lambda also decreases. It suffices to test the
first index of every cell, the point after a possible endpoint demotion,
and the first point at lambda=2. These indices are computed by exact
integer ceilings. Both verifiers include the required endpoints; B also
checks every individual grid point through degree sixteen.

Verifier A assumes the next count n=R+1, restricts lambda<=d2^(d-1)/n,
and checks that every possible budget is strictly less than n. It also
checks an allowed feasible scalar point at R; this is not a Boolean
witness. It enumerates every h through degree fourteen and the two exact
regime endpoints thereafter. Verifier B, separately written (same agent), derives the maximal
integer count at fixed influence before reading the submitted row. If C
is the preceding integer count and B=b_d*(2G), its ordinary numerator
with denominator G^2 is

    (2C+h+1)G^2-Cz,

and where applicable the retained improvement adds

    min(0,(2B-C-2G)G).

It maximizes the smaller of this budget and floor(2dG^2/z), then compares
all rows with the artifact. The resulting first caps are 50,107,230,481,
990,2015 at d=5,...,10. The checked certificate contains every row through
degree 96, with exact witnesses and exclusion budgets.

For the tail, the input support/restriction argument proves universally

    W_d <= W_(d-1)+d(d-1)/2^d.

Explicitly, the Xi lower construction gives R_d>=2^d for d>=2, hence
lambda<=d/2. In the weaker valid restriction budget use h<=2(d-1)lambda
and 1/2<=W_(d-1)<=(d-1)/2. The increment is then at most d(d-1)/2^d.
In detail, restricting all controls and retaining the dictator potential
on active assignments gives the weaker but valid inequality

    W_d <= c + [h+(1-2c)lambda]/2^d,  c=W_(d-1).

Since h<=2(d-1)lambda, c>=1/2 and lambda<=d/2, its increment is at most
[2(d-1)+1-2c]lambda/2^d <= d(d-1)/2^d. The upper bound c<=(d-1)/2
also follows directly from total influence. Summing the geometric first
and second moments gives

    sum_(d>H) d(d-1)/2^d = (H^2+3H+4)/2^H.

For an explicit summation check set q_H=(H^2+3H+4)/2^H. Then
q_H-q_(H+1)=H(H+1)/2^(H+1), exactly the summand at d=H+1, and q_H
tends to zero. Telescoping proves the displayed tail formula.
At H=96 this is 9508/2^96. Both exact scalar verifiers check nondecreasing
finite caps, add this exact tail, compare the resulting rational with
2.0209645587, and compare its gain over the round-eight rational with
1/10000. This proves the candidate headline upper bound.

## 10. Scope of the lower side

Xi1=x and Xi_d=(s+t)Xi_(d-1)(X)/2+(s-t)Xi_(d-1)(Y)/2 on disjoint inputs
are sign Boolean, of degree d and relevant count 3*2^(d-1)-2. Exactly one
summand is active. Induction proves these statements and C44>=3/2. More
generally a degree-d seed with n variables lifts to degree d+k with
2^k(n+2)-2 variables, so C44>=(n+2)/2^d. A 47-variable degree-five seed
would give 49/32. No such seed is asserted in this proof.

Exploratory shared-parity, shared-gate and higher-control routes are
reported separately. Their unsuccessful searches do not classify all
Boolean functions and do not justify a universal upper bound of 3/2.
