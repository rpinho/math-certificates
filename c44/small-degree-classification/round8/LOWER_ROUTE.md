# Lower construction classification — candidate, unrefereed

No 47-variable degree-five Boolean function was found. The complete
construction family examined here attains exactly 46 at degree five and
94 at degree six. This is not a classification of all degree-five/six
Boolean functions and is not a universal upper bound of 46 or 94.

The starting library is the complete 761-class cubic Boolean catalogue
from Rasoolzadeh, ToSC 2023(3), 213–226, pinned and hashed in
inputs/round7/inputs/gap1/PROOF.md. The resilient truth tables are converted
to sign Boolean cubic functions by multiplying by full parity. Input
permutations/flips and output complementation preserve the weighted
Fourier-mask optimization below. Completeness is the same explicit
published dependency as in the inherited R4=22 proof.

For each representative g and each of its relevant inputs j, substitute
a known Xi_(r_j) function on disjoint fresh inputs. Here r_j>=1 and
Xi_r has homogeneous real degree r and L_r=3*2^(r-1)-2 relevant variables.
The composition is Boolean. Its real degree is exactly

    max_(ghat(S)!=0) sum_(j in S) r_j,

and its relevant count is exactly sum_j L_(r_j). To see that there is no
cancellation in these assertions, every inner monomial is nonconstant,
and the sets of inner input blocks occupied by an expanded monomial
identify its outer mask S uniquely. Within one S, disjoint blocks make
the product terms distinct. Choosing a nonzero monomial containing any
specified inner variable proves relevance. Thus these exact weighted
mask inequalities, rather than a syntactic degree estimate, characterize
all allowed allocations in this family.

For output degree d, each r_j is at most d-d_j(g)+1: take an outer
monomial of size d_j(g) containing j and use weights >=1 on its other
coordinates. This bounds the enumeration without excluding an allocation.
The search enumerates every integer vector in those finite ranges and
checks every nonzero Fourier mask. It stores each representative's best
count, feasible-allocation count, and one attaining vector.

|Output degree|Maximum variables|Feasible allocations across 761 rows|
|--:|--:|--:|
|2|4|8|
|3|10|796|
|4|22|8,080|
|5|46|49,761|
|6|94|221,198|

Two separately written exact verifiers check the result. Checker A uses
integer Walsh transforms, reversed variable order and residual mask
budgets, comparing each individual row and its witness. Checker B instead
performs integer bit Mobius interpolation followed by an explicit Fourier
conversion, then enumerates the entire mixed-radix Cartesian allocation
box, independently checking every mask. It checks the global maxima and
the allocation totals above. Neither imports the generator or the other
verifier. The accepted artifact is compositions.json on the frozen packet.

For this closure argument the inner functions need not be homogeneous.
The same weighted degree formula still holds. Let S maximize the sum of
positive inner degrees over nonzero outer masks. A product of top-degree
inner monomials from S occupies every block in S and has that total
degree. Another outer mask could produce that exact input monomial only
if it contains S. A strict superset would have larger positive weighted
degree, contradicting maximality. Thus this top monomial survives.
Disjoint nonconstant Boolean inner functions each take both signs, so
all outer input assignments can be realized; each relevant inner variable
can therefore be made to change the outer output by fixing the other
blocks appropriately. The relevant counts also add for arbitrary inner
Boolean functions.

The same result excludes a stronger lower construction even for the
closure under arbitrary repeated *disjoint* compositions of cubic Boolean
functions. This follows by induction on output degree through six.
A nonprojection Boolean g has every relevant local degree >=2: if some
local degree were one, write g=a x_j+B with a a nonzero constant. For
both a+B and -a+B to be signs at every other input, one must have
a=+/-1 and B identically zero, so g is a signed projection. Consequently,
in every genuinely nonlinear outer composition each inner degree is
<=d-1. The induction hypothesis bounds its count by L_r at degree r;
replacing it by Xi_r cannot decrease that count and preserves the same
mask constraints. The finite optimization above then bounds the output
by L_d. Signed projections and constants add no new variables and do not
raise degree; they can be removed from a composition tree. The base case
d=1 is a dictator. Conversely, Xi_d belongs to this closure because its
outer two-selector function is quadratic, so every listed maximum is
attained. This proves the claimed closure ceiling through degree six.

This route ends at 46/94. Escaping it requires a seed or an operation
outside that disjoint cubic-composition closure, such as a degree-five
Boolean construction with shared input blocks and controlled cancellation.
The universal lower bound remains 1.5. If a 47-variable degree-five seed
is ever exactly verified, the two-selector lift gives C44>=49/32.
