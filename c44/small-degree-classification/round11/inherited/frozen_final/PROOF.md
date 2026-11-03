# Sign completion extension — candidate, unrefereed

This extends the already frozen round-ten packet in ../frozen. It does not
modify that packet or round nine. All its explicit published premises and
replayed finite results are retained. In particular the integer norm gap,
minimum-support classification, cross-polytope-link lemma, restriction
budgets, scalar energy grid and infinite-tail bound remain dependencies.
The new observation is the following completion of the signs in section 2
of that proof. No priority or novelty claim is made.

Let A be ternary, of real degree at most k>=3, with h relevant coordinates,
lambda=2^k E A^2>=1. If h>2k lambda-1/2, the frozen deficit proof already
shows that every nonzero partial is minimum and homogeneous: its Fourier
support consists of the transversals of k-1 disjoint pairs, with coefficient
numerators of absolute value one on the denominator 2^k grid. Deleting the
constant term, every connected component of the Fourier-mask complex is
the boundary of a k-cross-polytope. The components have disjoint sets of
2k coordinates. Write A=c+sum_(a=1)^s P_a, where P_a is the Fourier sum
on one component. Since lambda>=1, the displayed strict inequality forces
h>0; hence s>=1.

Label the opposite pairs in a component (u_i,v_i), i=1,...,k. Its Fourier
terms are indexed by epsilon in {0,1}^k, selecting u_i when epsilon_i=0
and v_i otherwise. Every coefficient is (-1)^b(epsilon)/2^k. For each
vertex u_i or v_i, the corresponding minimum partial is a signed product
of pair factors. Therefore b restricted to each face epsilon_i=0 or 1
is affine over F_2 in the remaining k-1 coordinates.

Here is the complete passage from face signs to global signs. For any
distinct i,j choose l distinct from both, possible because k>=3. On each
of the two faces epsilon_l=0 and 1 the second discrete derivative
D_i D_j b is zero, because that face is affine. Those faces cover the
cube, so D_i D_j b=0 everywhere. In the unique square-free polynomial
expansion of b over F_2, D_i D_j kills precisely the terms not containing
both i and j and maps the others injectively to distinct monomials.
Its vanishing forbids every monomial containing i,j. Doing this for all
pairs leaves b(epsilon)=b_0+sum b_i epsilon_i. Consequently, exactly,

    P_a = (-1)^b_0 product_(i=1)^k (x_(u_i)+(-1)^b_i x_(v_i))/2.

Each P_a attains both -1 and +1: choose each pair equal or opposite as
required by b_i, and choose their resulting signs with either product.
Different components involve disjoint variables, so their extrema can be
chosen independently. Thus A attains c-s and c+s. Since A takes values
in {-1,0,1}, both numbers lie in [-1,1]; subtracting gives 2s<=2. As s>=1,
s=1. The two inequalities c-1>=-1 and c+1<=1 give c=0. The single product
has support density 2^-k and squared value one on its support. Therefore

    h>2k lambda-1/2  implies  h=2k and lambda=1.       (SC)

This resolves the constant coefficient retained in the frozen proof; it
is not silently discarded. For lambda>1, (SC) excludes every integer h
satisfying the strict inequality, including multiples of 2k. At lambda=1,
the existing ceiling 2k is retained. At most the largest allowed integer
can satisfy the strict inequality. This replaces only the near-equality
predicate in the inherited scalar calculation. The budgets themselves,
their applicability regimes and the degree-96 tail are unchanged. The
half-cell grid transitions already included in the frozen proof cover
this stronger predicate as well. All arithmetic is rational/integer.

Two separately written exact scalar implementations check the submitted
rows, exclusions, bounds and strict improvement. They import neither the
generator nor each other. One explicitly scans square-face relations on
the sign cube; the other constructs affine constraints on vertex faces
using a distinct elimination order. They check rank 2^k-k-1 through k=8,
matching the k+1 dimensional space of global characters. The universal
argument is the preceding paragraph, not extrapolation from these ranks.
Positive controls include the lambda=1 product and negative controls keep
the strict threshold and k>=3 hypothesis. Corrupted artifacts must be
rejected by both implementations on the frozen extension before acceptance.

These checks and the inherited receipt are evidence for an unrefereed,
computer-assisted candidate. They are not independent human refereeing or
proof-assistant formalization. The lower bound remains 3/2 unless a new
seed is separately certified. The unfinished quartic and lower searches
do not enter this proof.

## Frozen final scalar result

The stronger predicate gives R5<=50, R6<=107, R7<=229, R8<=479,
R9<=985, R10<=2005, R11<=4054, R12<=8161. Propagating through degree 96
and adding the exact unchanged tail gives

    C44 <= 79671833529611582591986228957 / 39614081257132168796771975168
        < 2.0111998311.

The improvement over round nine's rational is

    193410356957031710481684315 / 19807040628566084398385987584,

which exceeds 1/10000. Both verifiers, separately written (same agent), check the exact
comparison to the retained round-ten baseline, and the report also checks
the round-nine comparison. The baseline's entire static manifest is checked
before and after replay. The historical baseline receipt is retained here;
a fresh replay may change its timestamps while preserving its mathematical
fields. No baseline certificate, classifier, or proof is modified.
