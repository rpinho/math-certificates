# Round 10 upper bound — candidate, unrefereed

This proof builds on the unchanged round-nine packet in baseline/frozen/.
All claims remain candidate and unrefereed. The two new exact verifiers
are separately written implementations in this agent session, not independent
human referees or proof-assistant formalization. Published completeness,
classification and lattice premises are explicit mathematical dependencies.

The candidate result is R7<=229, with R5<=50 and R6<=107 unchanged, and

    3/2 <= C44 <=
    159363009872336981657958180965 / 79228162514264337593543950336
    < 2.0114439717.

The rational gain over round nine is approximately 0.009520587008,
strictly greater than 1/10000. Verification status belongs in REPORT.md;
this text alone is not a receipt of successful frozen replay.

## 1. Definitions and inherited premises

Use uniform independent sign inputs, real multilinear Fourier expansion
f=sum fhat(S)x_S, local degree d_i=max{|S|:i in S,fhat(S)!=0},
D(f)=sum_i 2^(-d_i), R_d=max relevant count at degree <=d, and
W_d=max D(f). We retain the CHS identity W_d=R_d/2^d, all-local-degree-d
reduction for count maximizers, and coordinatewise restriction inequality.
The elementary proofs, finite maxima, and support bound are in
baseline/frozen/inputs/round8/PROOF.md sections 1–2, copied unchanged.
In particular nonzero real degree-r polynomials have support density
at least 2^-r: write P=x_j U+V, apply induction to U, and observe that
V+U and V-U cannot both vanish wherever U does not.

We retain R1=1,R2=4,R3=10,R4=22 and round nine's R5<=50,R6<=107.
The R4 proof is baseline/frozen/inputs/round8/inputs/round7/inputs/gap1/PROOF.md.
It uses the published complete Rasoolzadeh 761-class cubic catalogue and
Valyuzhenich's minimum-support classification. R3 is credited to
Tarannikov–Kirienko. Finite replay checks the representatives and arithmetic;
it does not itself establish published catalogue completeness.

For integer-valued real degree-r Q, the inherited Barnes–Wall norm gap is

    E Q^2 = 2^-r, or E Q^2 >= (3/2)2^-r.              (G)

Its explicit normalization and elementary induction are retained in round
seven's BW_GAP_PROOF.md and LATTICE_PROOF.md. External premises are the
classical integral Barnes–Wall basis/minimum and pair-preserving minimum-
vector transitivity, credited to Barnes–Wall, Broué–Enguehard and Nebe.
No real-degree invariance under arbitrary binary affine substitution is
assumed. The sharp second-weight control bounds and round-nine third-
weight bound are retained with their complete proof and exact verifiers.

The minimum-support theorem used below is Valyuzhenich, arXiv:2303.10995,
Theorem 2(2). At equality, up to input/output signs and coordinate permutation,
a minimum degree-r polynomial is a product of disjoint point factors and
blocks supported on opposite strings. A point costs one degree. A block
of size m>=2 costs m-1; its Fourier masks are the odd subsets for even m,
and even subsets for odd m. All nonzero Fourier coefficients have equal
magnitude. A point's masks are empty and singleton. This is a published
completeness premise, not a finite experimental inference.

## 2. Near-equality deficit lemma

Let A be ternary of real degree <=k>=3 and have precisely h relevant
coordinates, p=E A^2 and lambda=2^k p. Integer-valued cube functions have
integer bit coefficients, by finite differences. Substituting bit=(1-sign)/2
puts every Fourier coefficient of A on the grid 1/2^k. Write

    A=sum z_S x_S/2^k, N=sum z_S^2=2^k lambda,
    e_j=sum_(S contains j) z_S^2,
    L=sum_S (k-|S|)z_S^2=kN-sum_j e_j >=0.

For every relevant j, Q_j=2 Delta_j A is a nonzero integer-valued polynomial
of degree <=k-1. Applying (G), after multiplying by the exact Fourier
scaling 2^(2k-2), gives

    e_j=m=2^(k-1), or e_j>=m+q, q=2^(k-2).           (1)

Suppose h>2k lambda-1/2. Then kN-hm<q, because m*(1/2)=q.
If any partial were nonminimum, sum e_j>=hm+q>kN, impossible.
Thus every e_j=m and 0<=L=kN-hm<q.

Equality in the support and integer-magnitude bounds for Q_j forces its
values to be 0,+1,-1 and its support density to be 2^(-(k-1)). The complete
minimum-support classification applies. Its Fourier support has m terms;
the corresponding z_S in A have absolute value one. Let v be the number
of controls of this tensor, excluding j. A point or size-m block contributes
one coordinate occurrence to precisely half of its Fourier masks. This is
immediate for a point and follows by toggling a different block coordinate
for every parity block of size at least two. Therefore the mean cardinality
of its A masks is 1+v/2.

For each factor, the number of controls is at most twice its degree cost.
Equality holds only for pairs: a point has 1<2; a block of size m>=3
has m<2(m-1). If the tensor is not solely k-1 pairs, v<=2k-3. Its
contribution to the global deficit L, summing only masks containing j,
is consequently at least

    m*(k-1-v/2) >= m/2=q.                            (2)

All deficit terms are nonnegative, so this contradicts L<q. Every partial
is therefore homogeneous and consists of k-1 pairs. Any nonconstant
Fourier mask of A contains a relevant coordinate and is consequently of
size k. A possible constant term must be retained; we do not infer it is
zero from homogeneity of all partials.

Delete the constant term and form the simplicial complex generated by the
size-k Fourier masks. It is pure of dimension k-1. The link at each vertex
is exactly the boundary of a (k-1)-cross-polytope, since its masks are
all transversals of k-1 disjoint pairs. Each connected component is then
the boundary of a k-cross-polytope. Hence every component has 2k vertices,
and

    h>2k lambda-1/2 implies 2k divides h.              (NE)

The combinatorial lemma is Masuda–Panov, Lemma 4.7, arXiv:math/0607094v2,
pp.14–15; its hypotheses apply since k-1>=2. Its elementary proof is
included in the unchanged round-eight PROOF.md section 4, and expanded
again below. The constant term does not change the complex or any link.

Here are the combinatorial details. Let K be connected of dimension r>=2,
with every vertex link a cross-polytope boundary of dimension r-1. Each
vertex has 2r neighbors, each vertex lies in 2^r facets, and each ridge
is incident with exactly two facets, by reading these facts in the links.
Fix v and its r opposite neighbor pairs. Suppose a pair p,q in link(v)
is not an edge of K. Let R be the other 2r-2 neighbors of v. The link
of p contains v and R, and has exactly one more vertex p'; it excludes q.
The star of v in link(p) is the cone from v over the cross boundary on R.
This fixes all opposite pairs on R and forces p' opposite v. Therefore
link(p)=R*{v,p'}, and p' is adjacent to all of R. Likewise q has q'.
For each a in R, its 2r-2 neighbors in link(v), together with v,p',q',
would exceed its allowed 2r neighbors unless p'=q'. The resulting
suspension link(v)*{v,p'} gives every one of its vertices its full link.
There can be no edge leaving it. Connectedness gives all of K, a cross
boundary with 2r+2 vertices.

Otherwise all opposite pairs in link(v) are edges of K. The 2r vertices
of link(v) are mutually adjacent and adjacent to v; their allowed 2r
neighbors are exhausted, so connectedness gives exactly 2r+1 vertices.
Facet incidences then give F=2^r(2r+1)/(r+1). Any facet not containing v
uses r+1 vertices of link(v), so contains an opposite pair p,q. The link
of p is R*{v,q}, and likewise for q, by the opposite-pair partition in
the star of v. This facet contains at least two ridges that are facets of
link(v), each incident with just one facet avoiding v. At most 2^(r-1)
facets avoid v, and 2^r contain v. Thus F<=3*2^(r-1), contradicting
(2r+1)/(r+1)>3/2 for r>=2. This proves the lemma.

## 3. Direct R7 improvement without the combinatorial lemma

The specific decisive exclusion also has a shorter arithmetic proof.
At k=6, lambda=31/16, h=23, we have N=124, m=32, q=16 and
kN-hm=8. Equations (1),(2) force every partial homogeneous minimum.
All nonconstant terms have size six. Thus, retaining the constant z_empty,

    6*(124-z_empty^2)=23*32=736,
    z_empty^2=4/3.

This contradicts z_empty being an integer. Therefore h<=22 at this scalar
point. Both verifiers enumerate all nineteen degree-cost-five tensor
types using separately written (same agent) checkers, verify their mask counts and nonhomogeneous deficits,
and check this exact contradiction. The universal argument in section 2,
not enumeration at k=6, supplies the general recurrence strengthening.

## 4. Inserting the ceiling into the accepted budgets

Retain the inherited grid and low-weight spectrum. For d=k+1, G=2^(d-2),
lambda=z/G is on the integer grid. Below two the possible relaxed weights
are precisely 2-2^-j, j=0,...,k-1; above two every grid point is allowed.
The grid follows from integer bit coefficients and sum z_S^2 even; reducing
A modulo two and applying the Berlekamp–Sloane/Kasami–Tokura below-two
weight theorem gives the spectrum. These are necessary conditions only.
Their full bridge and parameter padding are retained in the input proof.

Start with the old ceiling floor(2k lambda), demoted by one at nonintegral
lambda where 2k lambda is integral, and impose the inherited sharp ceilings
at (d,lambda)=(5,3/2),(6,3/2),(6,7/4). If the resulting ceiling H is not
divisible by 2k and 2k lambda-H<1/2, (NE) excludes H, so demote once.
Every smaller integer then has slack at least one and cannot satisfy the
strict inequality. This is the exact rule in the artifact.

For c>=W_(d-1), choose a minimum-influence coordinate of an all-local-degree-d
count maximizer. The inherited ordinary and retained-control budgets are

    R_d <= 2^d c+h+1-2c lambda,                        (C2)
    R_d <= 2^d c+h-2c lambda+4*(b_d-(c+1/2)/2),        (C3)

where C3 is used only when lambda>1 and 3h>4k lambda, and
b_d=max(1/2,max_(1<=t<=d-2)(1/4+2^(-t-1)+c_t/2)). Also
R_d*lambda<=d*2^(d-1). These formulas and their complete section-potential
proof are retained in round eight sections 5–6 and round nine section 8;
we change only the ceiling on h. They apply to the same derivative.
At each lambda maximize the smaller valid budgets over all integer h
below its ceiling. Each applicability regime has slope one in h; its top
endpoint suffices. A enumerates every h through degree sixteen as a check.

To exclude R7>=230, influence bounds lambda<=448/230<2. The below-two
list through this endpoint is 1,3/2,7/4,15/8,31/16. Their control ceilings
are respectively 12,17,20,22,22; the last is the new exclusion. With
c6=107/64 and b7=67/64 the C3 correction is -5/32. At lambda=1,
C2 is 214+13-107/32=7157/32<230. At the other four weights the
maxima are respectively 14453/64,29183/128,58771/256,117435/512,
all <230. The exact verifiers check these rational budgets and all lower
h regimes, rather than trusting the displayed arithmetic. Hence R7<=229.

## 5. Complete scalar propagation and tail

The certificate contains all 92 degree rows from five through 96. Within
each joint cell of floor(2k lambda) and floor(4k lambda/3), the old budgets
have constant intercept and nonpositive slope. The new ceiling may change
at 2k lambda=a+1/2, and has the divisibility exception when floor(2k lambda)
is a multiple of 2k. Include the first grid point at every ordinary cell,
the next point after a possible equality demotion, the first point at each
half-cell, the first point of each C3 applicability cell, all integer
lambda values, and the first grid point at lambda=2. These form a complete
cover: between adjacent such transitions the ceiling and applicability
endpoints are constant, and both the control budget and influence budget
decrease. Exact integer ceilings locate every first grid point. Special
low-weight caps are all in the explicitly enumerated below-two list.

Verifier A proves the next-count exclusion rationally, checks the worst
budgets, exact previous caps, selector envelopes, all artifact rows and a
scalar feasible point at the retained integer. Verifier B, separately written (same agent),
maximizes integer numerators with denominator G^2, derives the counts
before reading their submitted values, and scans every energy-grid point
through degree sixteen. A feasible scalar point is not a Boolean witness.
Neither verifier imports the generator, search code or the other verifier.
The first resulting ceilings are 50,107,229,479,985,2005.

For all larger degrees the inherited tail inequality is
W_d<=W_(d-1)+d(d-1)/2^d. Its proof uses the weaker valid restriction budget,
Xi_d's R_d>=2^d for d>=2 and hence lambda<=d/2, together with
1/2<=W_(d-1)<=(d-1)/2. Explicitly the increment is bounded by
[2(d-1)+1-2W_(d-1)]lambda/2^d<=d(d-1)/2^d.
The tail after H is (H^2+3H+4)/2^H: subtract consecutive such expressions
to obtain H(H+1)/2^(H+1), the next summand, and telescope to infinity.
Thus the degree-96 cap plus 9508/2^96 bounds every degree. Both verifiers
check this exact rational, the strict decimal comparison, and gain >1/10000.
The unchanged Xi construction proves the lower bound 3/2; unsuccessful
lower searches do not establish its optimality.
