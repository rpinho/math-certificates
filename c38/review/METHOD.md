# Referee computation and its invariants

These are independently written implementations, not wrappers around any
producer enumerator or verifier. The only shared external software is the
standard C++ library, Boost integer arithmetic and Python's standard library.

## Main bridge graph

At a processed vertex, choose its outgoing lattice edges. An ordinary
occupied vertex has degree two; the unique left-boundary start and the
unique endpoint on the terminal span boundary have degree one. Empty
vertices have degree zero. The start has only its edge into the strip.

The frontier records connected components, not walks modulo an equivalence
relation. A component without a terminal has two frontier stubs. A component
with one terminal has one stub, labelled by that terminal's identity.
Connecting the two stubs of the same component creates a cycle and is
rejected. Connecting different components merges them. A component with
both terminals can have no remaining stubs; accept it only if every other
component is absent. Otherwise it can never become part of a single path.

All processed degrees are fixed permanently. Thus every accepted graph is
a single simple path with the required endpoints, and its orientation is
unique. Conversely, the edge choices of any admissible bridge give exactly
one accepted history. Histories with the same state add their weights;
they are not identified as one walk. Canonical component labels merely
remove irrelevant component names. No planarity or bracket case table is
needed for the implementation: reachable states arise from actual planar
edge choices. A growing work list discovers every reachable (stage,state).

Normalize by requiring minimum transverse column zero. The empty history
survives all rows of the first column; remove just that contribution at the
column boundary. No nonempty history can enter the empty state, since a
disappearing component either completes and exits or is rejected. Hence
this removes precisely the histories with unused leading columns.
Completions after w columns are exactly bridges of range at most w−1.

For length-truncated coefficient runs, N+1 columns suffice: a path of at
most N edges cannot have transverse range exceeding N. Formal span renewal
then recovers exact irreducible coefficients through N without any
finite-range convolution assumption. Literal DFS checks this conversion
against actual cut crossing counts through length 20.

## Exact finite point values and tails

At point M/2^27, use the common denominator 2^(54t) after t processed
vertices. A transition with k outgoing edges multiplies its integer
numerator by M^k 2^(54−27k), for k=0,1,2. Completions have no outgoing
edges, so their accumulated total is rescaled by 2^54 at each subsequent
stage. Every operation is exact and performed with arbitrary-size integers.
After finishing, remove powers of two common to numerator and denominator.
This directly computes a rational finite bridge value, not a decimal or
an interval approximation.

For an all-width bound, assign each nonempty graph node a potential in
units 2^−32. Repeated backward stage sweeps start from zero and replace
each entry by the ceiling of its completion weight plus its weighted
successor potentials. Stop only at a fixed cycle. Independently recheck
every inequality after stabilization. The empty state's potential is zero;
it is not reachable from the final nonempty frontier distribution.

For any finite future horizon, repeated substitution bounds its completion
weight by the starting potential pairing. Nonnegative monotone convergence
therefore bounds the infinite tail. This requires neither an estimated
spectral radius nor an assertion that the iteration ought to converge.
Failure to stabilize or failure of an arithmetic guard yields no bound.

The extra large-span mode retains the same graph but computes two directed
planes at scale 2^160. Each nonnegative transition contribution is rounded
down/up before integer addition. Values below 2^192 multiplied by M^2<2^52
fit the 256-bit type. Additions are guarded. Potential arithmetic uses
128-bit integers: entries below 2^60 and weights at most 2^54 give a
right-hand side safely below 2^128. Tail products are below 2^252.

## Direct normalized rectangles

The rectangle implementation sweeps in the span direction and initializes
the unique first horizontal edge at every possible start height. Interior
columns permit degrees zero or two. A terminal-column fork permits one
degree-one endpoint and no outgoing horizontal edge. At every interior
column boundary, retain exactly 3 or 5 outgoing horizontal stubs. Prune a
partial column only when its already fixed horizontal edges exceed the
crossing cap. This is a condition on actual cut crossings, not a surrogate
based on occupied vertices.

A state also records whether the path has touched transverse row zero,
including its start. Accept only completed paths with this bit set. Each
rooted walk of range at most W has exactly one translate with minimum row
zero. This directly counts normalized walks and avoids subtracting the
counts in two frames. Per-span terminal forks keep spans disjoint and
also give a direct lower bound for the genuine spans-19–30 supplement.

The initial arithmetic uses scale 2^160 and 256-bit unsigned integers.
An optional faster mode (`-DFAST_RECT`) uses scale 2^112 and native
128-bit unsigned integers. For a multiplication by q/2^s, s=27 or 54,
split x=2^s H+L and compute Hq+floor(Lq/2^s); the remainder is
Lq mod 2^s. The guard x<2^124 and q<2^s ensures Hq<2^124,
Lq<2^108, and the result including its ceiling fits in 128 bits.
Every accumulation is separately checked for overflow. Thus both modes
are rigorous directed enclosures, with sixteen extra fractional bits in
the faster mode compared with the producer's 96-bit scale.

Both modes were checked against a complete literal enumeration for range
4, spans 3–5, cap 3. That test examines 458,261 path prefixes and evaluates
the resulting integer coefficient polynomial with exact rational arithmetic.
Only completed, successful large runs may be used as evidence; interrupted
or timed-out attempts are recorded solely as resource outcomes.
