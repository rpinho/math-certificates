# Round 10 lower route — candidate, unrefereed exploration

This round searches nonminimum ternary gate partitions. Round nine searched
shared parity substitutions, overlapping cubic branches and disjoint cubic/Xi
closures, and gave a conditional obstruction for minimum-support partitions.
Here each gate is allowed to have nonminimum support and its own signing.
There is no claim that the resulting Boolean functions are all distinct
from all previously sampled functions, or that this is a new general method.

For controls H and disjoint nonconstant payload inputs Y_j, construct

    F(H,Y)=sum_j A_j(H) Xi_(d-t_j)(Y_j),

where each A_j is ternary, has real degree t_j, and the nonzero gate
supports partition the control cube. At each control assignment exactly
one summand is active, so F is sign Boolean. Its degree is exactly d:
each payload is homogeneous of positive degree d-t_j, different payload
blocks have nonempty Fourier masks on disjoint coordinate sets, and terms
from different gates cannot coincide or cancel. Every relevant gate
control and every payload input remains relevant. Consequently the count
is the size of the union of gate controls plus sum_j [3*2^(d-t_j-1)-2].
A degree-d, n-variable seed lifts via Xi recursion to C44>=(n+2)/2^d.

Gate banks contain signed minimum tensors of degrees one through four,
and differences/sums P+/-Q of overlapping minimum tensors. A proposed
sum is retained only when direct exact truth values are ternary. Overlap
can cancel and produce a nonminimum support not covered by round nine's
minimum-gate obstruction. Exact Walsh transforms recover the actual degree
and relevant controls, including any degree drop. Sampling nearby signed
permutations encourages supports of small nonminimum weight.

For each sampled bank, a single-threaded CP-SAT model chooses an exact
cover of every control assignment and maximizes the above relevant count.
The banks use 8,10,12 controls and degree-five/six payload budgets. Numerical
or solver bounds are not universal mathematical bounds. Even OPTIMAL applies
only to the finite stored bank, not all ternary gates or all Boolean seeds.

Verifier A evaluates all gate tables by inverse Walsh, checks their ternary
values and exact support partition, expands every disjoint Xi payload, and
checks the full resulting polynomial's square by integer XOR convolution.
Verifier B uses direct character evaluation on every control assignment,
checks the partition, and verifies the four-selector Boolean identity and
Xi degree/count induction. Different payload blocks cannot cancel, so this
structured verification also certifies degree and count exactly. Neither
verifier imports the search or the other verifier. Every reported saved
seed is checked separately, with corruption controls before any new claim.

No improved lower bound has yet been accepted. Final outcomes and precise
search coverage belong in REPORT.md and the retained process receipts.

## Sparse extension to 20–32 controls

The wider route stores each minimum tensor and its exact sparse Fourier
polynomial P. For two such ternary functions, P+epsilon*Q is ternary iff
P^2 Q^2=-epsilon*PQ: on an overlap P,Q are signs, and the equality says
their contributions cancel. Off the overlap their sum is already ternary.
All operations use exact integer XOR convolution on denominator sixteen.

In particular P=product_j(a_j+b_j)/2 and
Q=product_j(b_j+c_j)/2 agree on their overlap. Their difference is ternary
of degree t on 3t controls, has 2^(t+1)-2 nonzero Fourier coefficients of
magnitude 2^-t, and normalized weight 2-2^(1-t). At t=3 this is degree
three on nine controls, energy 7/32. Four gates of this type plus one
minimum cubic gate would have total density one. If they partitioned the
cube and used at least 27 relevant controls jointly, their five disjoint
Xi2 payloads would give a degree-five seed on at least 47 variables.
This is a search target, not an asserted partition or seed.

The new banks mix these gates, other exact differences and minimum tensors.
An integer exact-cover model starts with the necessary energy identity and
a small set of control assignments. For each proposed cover compute the
whole sparse polynomial sum_j A_j^2-1. If it is nonzero, repeatedly fix a
coordinate to a sign preserving a nonzero restriction. At least one sign
does so, because both zero restrictions would make the polynomial zero.
After all coordinates are fixed, the resulting assignment is an exact
counterexample, which is added to the model. A zero identity certifies
coverage on the entire cube. No full truth table on 20–32 controls is
needed. The solver remains an exploratory proposer; any actual seed must
still pass two separate frozen verifiers and rejection controls.

Separately written finite controls evaluate the alternating-path gate
family completely at t=2,3,4. The t=2 instance is a genuine six-control
quadratic cycle, illustrating the essential dimension hypothesis k>=3
in the upper proof's cross-polytope lemma.
