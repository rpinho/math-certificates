# Lower-side routes — candidate, unrefereed

The universal lower bound remains 3/2 unless a separately frozen and exactly
verified improvement is added to this report. The known Xi recursion uses
L_d=3*2^(d-1)-2 variables. From a degree-d, n-variable seed it gives
C44>=(n+2)/2^d; thus the next degree-five target is 47 variables.

## Shared parity substitutions

For a seed f=sum a_S x_S, choose new independent inputs y_j and columns
v_j in F2^n, and substitute x_i=product_(j:(v_j)_i=1)y_j. The resulting
function remains Boolean. Its exact Fourier mask for old S is
{j:S dot v_j=1}. Combining equal resulting masks with signed integer
coefficients determines the actual degree and relevant count. This permits shared-input operations beyond the disjoint composition
operations enumerated in round eight.

The numerical MILP uses multiplicities of columns of Hamming weight at
most two, then three. Every resulting row has weight <=5. It additionally
separates every distinct pair of old Fourier rows; this prevents
cancellation and makes the objective exactly the number of new variables.
That restriction can miss valid constructions with cancellations. Solver
bounds are numerical exploration, not exact nonexistence certificates.

Six randomized local searches use columns of weights up to two, three
and four, and explicitly combine cancelling Fourier rows when evaluating
the actual relevant count. They start at Xi5 and remove/refill collections
of columns under the degree budget. Every stored best artifact is checked
by exact integer XOR convolution. They search a finite heuristic sample,
not every parity map. No failed heuristic search proves a universal bound.

## Shared cubic branches inside a quartic outer selector

A second family starts from any two representatives in the 761-class cubic
catalogue, with random input permutations/flips and overlapping input
sets. The outer Boolean function is either

    (g+h)/2+s(g-h)/2,

or the two-selector version

    s(g+h)/2+t(g-h)/2.

Both are Boolean by their two/four control assignments. After collecting
all exact coefficient cancellations, replace each relevant outer input by
a disjoint Xi_r. Each outer nonzero mask must have sum of allocated r's
at most five. Because inner Xi functions are homogeneous on disjoint
blocks, different outer masks occupy different sets of input blocks and
cannot cancel; degree is exactly this weighted mask maximum and counts
add as sum L_r. The search checks every resulting mask budget and samples
many allocations. A count of at least 47 triggers complete exact sparse
expansion and a Boolean convolution check before saving a candidate seed.
This parameterization permits overlapping cubic branches inside quartic
outer functions; round eight did not enumerate this parameterization.
No classification of its functional overlap with the old family is claimed.

## Why minimum-support gate partitions do not help this construction

Here is a structural obstruction, conditional on the explicitly cited
published affine-partition theorem. Consider

    F(X,Y_1,...,Y_m)=sum_j A_j(X) Xi_(r_j)(Y_j),

where each A_j is a minimum-support ternary polynomial of degree t_j,
their nonzero supports partition the X cube, the Y blocks are disjoint,
and t_j+r_j<=d. Supports have densities 2^-t_j, so their sum is one.
The minimum-support classification makes each support an affine set
specified by fixed-bit equations and equal/opposite-pair equations inside
blocks. Let H be the total number of X coordinates used in these equations.

Combine the homogeneous parts of all equations into a graph, adjoining a
ground vertex for fixed-bit equations. An ungrounded connected component
with v>=2 input vertices contributes rank v-1; a grounded component with
v input vertices contributes rank v. A spanning tree proves these formulas:
its edge incidence vectors are independent by leaf deletion, and every
other edge is the sum along its tree path. No used input is isolated.
Thus total row rank r satisfies H<=2r.

The intersection K of the supports' direction spaces has codimension r.
Quotienting by K gives a tight affine partition of an r-dimensional binary
space into m sets. Filmus, Hirsch, Kurz, Ihringer, Riazanov, Smal and
Vinyals, *Irreducible subcube partitions*, arXiv:2212.14685, Theorem 4.7,
gives m>=r+1. Consequently H<=2m-2. For r=0, m=1 and H=0 directly.
This is an external published premise, not a theorem inferred from a
finite partition search. Source: https://arxiv.org/html/2212.14685 .

Therefore the relevant count in this construction is at most

    H+sum_j L_(r_j)
      <= H+sum_j (3*2^(d-t_j-1)-2)
      = H+3*2^(d-1)*sum_j 2^-t_j-2m
      <= 3*2^(d-1)-2 = L_d.

The first inequality merely counts all possible controls and inner inputs;
the second uses r_j<=d-t_j and monotonicity of L; the equality uses the
partition densities; the last uses H<=2m-2. This explains why general
shared minimum-support gate partitions cannot improve this Xi-based
construction, even beyond disjoint cubic composition. It does not cover
nonminimum gates, shared Y blocks, or arbitrary Boolean functions. It is
not used as an input to the accepted upper-bound computation.

Final search counts, limits and outcomes belong in REPORT.md and the
process receipts. No novelty or priority claim is made for this obstruction.

## Local-degree potential and shared duplication

Counting relevant inputs alone can miss an improvement: a degree-five
function with potential above 46/32 would imply a better count via the
CHS identity. Even equality 46/32 with a coordinate below local degree
five would improve potential after simultaneous duplication of those
coordinates with a fresh selector. This job therefore also enumerated
potential for every cubic/Xi allocation through degrees five to eight,
and sampled weighted shared-selector outer functions with potential as
the objective. For disjoint homogeneous inner blocks, an inner variable's
local degree is exactly the largest weighted outer mask touching its block.
Its block contributes L_r times that local-degree weight. These are
exploratory finite-family searches, not a universal classification.

The cubic family returned best normalized potential units 46,94,190,382
at degrees 5,6,7,8; the best with a smaller local degree was two units
below in each case. These observations are search receipts rather than
new universally quantified theorems. The separately checked stored seeds
only certify their own Booleanity, degree, count and asymptotic lift.
