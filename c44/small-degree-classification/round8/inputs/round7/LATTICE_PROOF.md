# Integer energy gap and quintic second-weight controls

Candidate, unrefereed. This extends PROOF.md using Barnes–Wall lattice theory. Nebe's 2026
second-minimum theorem is expanded from classical premises in
BW_GAP_PROOF.md. The quartic-only bound
in PROOF.md does not need this dependency. The finite templates, traces,
and independent exhaustive completions are exact; they do not prove the
external lattice theorem.

## 1. Exact embedding, with all scaling factors specified

Let Q be a nonzero integer-valued real-degree-at-most-r polynomial on an
n-dimensional bit cube. Its bit coefficients are integers by the finite-
difference formula proved in PROOF.md. Each degree-t bit monomial is the
indicator of an affine coordinate subspace of codimension t.

In Nebe's Definition 2.1 and Theorem 2.3, the integral Barnes–Wall model
Lambda_n is generated over Z by 2^floor(t/2) times every codimension-t
affine-subspace indicator. Its minimum squared norm is 2^{n-1}. The model
Delta_n uses 2^ceil(t/2), has minimum squared norm 2^n, and is similar to
Lambda_n. Source: G. Nebe, The second minimum of Barnes–Wall lattices,
arXiv:2603.23133, author's primary PDF
https://www.math.rwth-aachen.de/~Gabriele.Nebe/papers/BW.pdf .
Theorem 3.3 states that a nonminimal nonzero vector of Lambda_n has squared
norm at least 3/2 times its minimum. Similarity gives the same ratio for
Delta_n. These are stated published premises, not properties inferred
from finite tests or a binary affine change of coordinates.

If r is odd, scale the Q truth vector by 2^{(r-1)/2}. For each t<=r,
floor(t/2)<=(r-1)/2, so every scaled bit monomial is an integer multiple
of a generator of Lambda_n. The scaled truth vector belongs to Lambda_n
and has squared norm 2^{r-1}2^n E Q². The lattice minimum 2^{n-1}
corresponds exactly to E Q²=2^-r.

If r is even, scale by 2^{r/2}. Since ceil(t/2)<=r/2 for every t<=r,
the vector belongs to Delta_n, with squared norm 2^r 2^n E Q². Its
minimum 2^n again corresponds exactly to E Q²=2^-r.

Append dummy variables if needed to ensure n>=max(r,2). Each appended
variable duplicates the truth vector and doubles its squared norm; the
lattice minimum also doubles. No normalized ratio changes. Thus in all
cases Nebe's theorem gives

    E Q² = 2^-r, or E Q² >= (3/2)2^-r.                 (L1)

The support lemma also supplies the minimum directly, since Q is integer
and every nonzero value has squared magnitude at least one. For energy
exactly 2^-r, equality forces minimum support and constant magnitude one;
Valyuzhenich's minimum-support classification then applies.

## 2. Quintic partial energies and their tensor templates

Let A be ternary, degree <=5, with E A²=3/64. Write

    A=sum_(|S|<=5) z_S x_S/32,    sum z_S²=48,
    e_j=sum_(S contains j)z_S²,
    L=sum_S (5-|S|)z_S²=240-sum_j e_j.

For each relevant j, Q=2 Delta_j A is integer-valued of real degree <=4.
By (L1), its energy is either 1/16 or at least 3/32. Hence

    e_j=16 or e_j>=24.                                (L2)

Call j good when e_j=16. Equality forces a scaled degree-four minimum-
support tensor. Its partial has exactly sixteen nonzero Fourier
coefficients, each of magnitude 1/32. Every control occurs in exactly
eight masks, and the mask intersection is empty. These statements follow
directly from the factors: a point has masks {empty,{u}}, an even m-block
all odd subsets, and an odd m-block all even subsets. In every factor
there are 2^{degree cost} masks, and each control occurs in half of them.
Disjoint products multiply counts. There is no forced coordinate in the
intersection. The coefficients all have magnitude 2^{-degree cost}/2.

There are exactly twelve degree-cost-four types. Equivalently, choose
nonnegative integers (r,b2,b3,b4,b5) with

    r+b2+2b3+3b4+4b5=4,

where r counts point factors and bm counts m-block factors. Every good
partial has at most eight controls. The unique homogeneous type is four
pairs. Every nonhomogeneous type has at most seven controls and average
Fourier degree at most 7/2: each point contributes degree average 1/2,
and each m>=2 block contributes m/2 (this is immediate from the uniform
parity-mask list, including m=2). Its degree cost is four, so control count
at most seven gives the stated average. Consequently every nonhomogeneous
good partial has

    L_j=sum_(S contains j)(5-|S|)z_S² >=8.              (L3)

Only |S|<=4 contribute to L, and such a mask contains at most |S| good
coordinates. Therefore

    sum_(good j) L_j <=4L.                             (L4)

Two good coordinates absent from an already forced set of unit-squared
Fourier terms require at least 24 new units of squared norm. Each needs
sixteen new unit coefficients. Their overlap can have at most eight terms,
because in the first minimum partial any specified other coordinate occurs
in at most eight masks. Thus the union has size at least 16+16-8=24.
One absent good coordinate alone requires sixteen new units. These are
necessary conditions, independent of coefficient signs.

## 3. Excluding fifteen and fourteen controls

The general energy bound gives h<=15. At h=15 equality would have
lambda=32*(3/64)=3/2 nonintegral, contradicting PROOF.md section 4.

Suppose h=14. Then sum e_j>=224, so L<=16. At most two coordinates can
have energy above sixteen: three such coordinates would add at least
3*8 to 14*16=224, exceeding 240. Thus at least twelve are good. If none
were homogeneous, (L3),(L4) would give 96<=4L<=64. Hence a homogeneous
good partial exists. Relabel it as coordinate 0 with pairs
(1,2),(3,4),(5,6),(7,8). The sixteen seed A masks are coordinate 0 plus
one member from each pair.

Select eleven more good coordinates. Their counts in the four pairs,
up to pair permutations and member swaps, are the sorted tuples
(0,2,2,2),(1,1,2,2),(1,2,2,2),(2,2,2,2); the numbers outside are,
respectively, 5,5,4,3. These are all possibilities because the selected
counts sum to eleven and there are only five outside coordinates.

The frozen quintic14_certificate.json.gz is a complete unsigned completion
trace for these four cases. There are no terminal models. A completed good
partial contributes one of the twelve tensor types. A new partial must
include every existing mask using its coordinate and must introduce no
new mask using a previously completed good coordinate. Every remaining
choice is included. Norm >48, degree deficit >16, insufficient energy
for the two unselected coordinates, and the absent-good-coordinate bounds
above are the only prunes.

For the few chosen branching coordinates, eight existing top masks have
the form coordinate j, coordinate v, and one member of three known pairs.
Thus their partial already depends on seven controls. All compatible
minimum tensors use those seven and at most one extra. Enumerating the
degree-cost-four tensors on these seven plus one possible extra gives
exactly five local patterns. In structural language these are four pairs,
one point with three pairs, or two pairs with a triple; lower-control
types cannot contain the seven known coordinates. Checker A enumerates
all twelve types on eight inputs before verifying complete trace coverage.
Checker B independently computes the three high-control types by tensor
truth tables and Walsh transforms, then excludes the four cases in fixed
coordinate order without consulting the trace. Both pass. This proves
h<=13 for the quintic second-weight case.

## 4. Excluding thirteen controls, both possible kinds of good partial

Suppose now h=13. We have L<=32. If g is the number of good coordinates,
(L2) gives

    240-L=sum e_j >=16g+24(13-g)=312-8g,
    g >=9+L/8.                                        (L5)

In particular g>=9. There are two exhaustive cases.

**A homogeneous good partial exists.** Relabel it as the four-pair seed
above, and select eight further good coordinates. Their sorted pair counts
a1<=a2<=a3<=a4 in {0,1,2} and outside count b=8-sum ai, 0<=b<=4,
give exactly nine cases. The certificate
quintic13_homogeneous_certificate.json.gz contains complete completion
trees. The rules are the same as in section 3, now with norm 48, degree
deficit <=32, nine selected good coordinates and four unselected ones.
The necessary unselected energy condition is

    sum_(unselected j) max(0,16-current number of masks containing j)
        <=4*(48-current number of masks).

Both verifiers enumerate all minimum-partial templates on the actual
thirteen coordinates, so the earlier local shortcut is not trusted for
completeness. Exactly ten unsigned terminal models survive. All have
32 forced masks and at least two variables absent from them. Sixteen
units of squared numerator norm remain. Each absent variable needs at
least sixteen, so both attain the minimum and every remaining nonzero
term contains both. But a minimum partial has empty mask intersection.
This contradiction excludes all ten terminal models.

**No good partial is homogeneous.** By (L3),(L4), 8g<=4L. Combining with
(L5) gives 72+L<=4L, hence L>=24 and g>=12. Choose twelve good coordinates;
only one coordinate is unselected. Their partials all have nonhomogeneous
tensor types. Pick one good coordinate as 0. There are eleven possible
nonhomogeneous types for its sixteen-term seed.

For each seed, the single unselected coordinate can be put in any of its
point-factor coordinates, any nontrivial block size that occurs, or the
outside coordinates. Within each factor size the seed's unsigned support
is invariant under permutations, and identical factors may be permuted.
Thus one representative for each such position is complete. There are
31 cases, listed explicitly in
quintic13_nonhomogeneous_certificate.json.

The full frozen table quintic_minimum_templates.bin.gz contains all
359,502 distinct sixteen-term degree-four minimum-partial patterns on
coordinate 0 and twelve possible controls. The number of nonhomogeneous
ones is 307,527. Checker A verifies the complete branch trace against this
table with no local-template shortcut. Checker B rebuilds the table from
independently computed elementary-factor Walsh transforms, enumerates the
eleven seed types and all unselected-coordinate positions, and repeats
all completions in fixed coordinate order. No target search code is
imported, and the independent search reads no trace to select branches.

The only prunes are: more than 48 unit coefficients; degree deficit >32;
a completed good coordinate needing more than sixteen coefficients;
an empty complete tensor domain; insufficient remaining energy to give
the unselected coordinate sixteen; and the absent-good bounds of section 2.
If all twelve selected coordinates are completed, any remaining Fourier
term can use only the one unselected coordinate b. Therefore the only
unknown coefficients are a/32 at the empty mask and c/32 at {b}. Their
squared numerators obey a²+c²=48-|E|. Every integer solution is tested
using nonnegative |a|,|c|, since signs are relaxed. It must satisfy

    current L+5a²+4c²<=32,
    e_b=current e_b+c² is 16 or >=24.

If e_b=16, b is also good: all its coefficients must have magnitude one
in numerator units, so |c|<=1, and its complete support must be one of
the nonhomogeneous minimum templates. These are necessary conditions for
any actual A and cover every residual coefficient possibility. No case
has a feasible residual. The 31 cases have zero surviving models.

The two cases exhaust h=13, so together with section 3 we obtain

    deg A<=5, A ternary, E A²=3/64 ==> controls(A)<=12. (L6)

The bound is attained by the exact ternary witness in CONTROLS.md. This
is a control-count statement, not a Boolean R6 existence statement.

## 5. Resulting count ceiling and limitations

In (4) of PROOF.md at d=6, c5=51/32, the lambda=1 budget is
102+10-35/16=1757/16<110. At lambda=3/2 use (L6) to get
102+12-(35/16)(3/2)=3543/32<111. Every lambda>=7/4 gives
N<=floor(192/(7/4))=109. Thus R6<=110.

The classified mode of certificate.json uses (10) of PROOF.md at d=5 and
(L6) here at d=6, plus the nonintegral equality exclusion in all subsequent
degrees. All higher scalar rows and the elementary infinite tail are
checked by the two separately written scalar verifiers. The extra lattice
premise is stated explicitly so the quartic-only bound remains available
if it is not accepted. R5=46 and R6=94 remain unproved by this work.
