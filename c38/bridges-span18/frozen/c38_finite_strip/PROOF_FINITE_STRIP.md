# Finite strip bridge certificate — proof specification

Candidate and unrefereed. Written by one agent; the verifier is separately
written (same agent). This document specifies the mathematical reduction. Numerical acceptance is
recorded in the frozen input manifest and complete replay receipts; this text
alone supplies no numerical acceptance.

Credit: Harry Kesten's irreducible-bridge construction, Iwan Jensen's
span renewal, I. G. Enting's finite-lattice method, Numaro's published
span-17 coefficient baseline, and Vít Plánočka's documented point-evaluation
implementation and its directed-integer/tail construction. Our implementation
of vertex rules is separate from the production case table. No novelty
judgment, formal verification, human review, or separate authorship is claimed.

## 1. Exact finite coefficients and the target

A walk is an ordered list of distinct nearest-neighbor vertices of Z^2,
starting at (0,0). Its length is its number of edges. It is a bridge of span
l if every vertex after the start has first coordinate in {1,...,l}, and
its endpoint has first coordinate l. Let C_j be its number of horizontal
edges crossing x=j+1/2, for 1<=j<l. A bridge is irreducible if C_j>=3 for
every such j. At l=1 the condition is vacuous.

For positive integers w_l, define F_l to be ALL such irreducible bridges
whose transverse range max(y)-min(y) is at most w_l-1. Let

    a_n = sum_{l=1}^L |{ beta in F_l : length(beta)=n }|.

These are exact, nonnegative integers, specified by a finite combinatorial
class; different spans are disjoint. There are at most l*w_l vertices in
columns 1,...,l, and the unique vertex in column 0 is the start. Thus every
member of F_l has length at most l*w_l. With N=max_l l*w_l the polynomial

    P(z)=sum_{n=1}^N a_n z^n

is finite. The frozen artifact must specify every l,w_l and the coefficient
definition. The proposed computation certifies its value by an exact rational
lower enclosure; it does not materialize its expanded coefficient vector.
This distinction must remain explicit in any report. The archived Numaro
coefficient vector is a separate attributed baseline, not this vector.

The requested bar is P(400/1051)>=1. We evaluate at

    z0 = 51081913/134217728 <= 400/1051,

where the comparison is exact cross multiplication. Coefficient
nonnegativity gives P(400/1051)>=P(z0). All final acceptance uses integers
or rational numbers, never the printed decimals.

## 2. Why this implies a lower bound for mu

Concatenating two bridges after translating the second start to the first
endpoint gives a self-avoiding bridge: the first has x<=l_1, and every
noninitial vertex of the second has x>l_1. Their only shared vertex is the
join. Lengths and spans add.

For a bridge, a cut x=j+1/2 is crossed an odd number of times: starting on
its left and ending on its right changes sides an odd number of times.
If it is crossed once, the prefix ending just before that crossing and the
suffix starting there are both bridges. Conversely, in a concatenation of
bridges, the cut immediately to the right of the first endpoint's column
is crossed once. More precisely, a renewal at vertex v of first coordinate
j splits the path into a prefix in x<=j and a suffix with all later x>j;
its next edge is the sole crossing of that cut. A unique crossing supplies
exactly that split. Therefore irreducibility is equivalent to every interior
cut being crossed at least three times. Splitting at all singly crossed
interior cuts recovers a unique list of irreducible factors.

Consequently distinct ordered sequences of members of the finite family F
produce distinct walks. Let d_n count all sequences with total length n,
including the empty sequence at n=0. For nonnegative z, summation of finite
nonnegative terms gives

    sum_n d_n z^n = sum_{k>=0} P(z)^k.

Each concatenated walk starts at the origin, so d_n<=c_n, the number of all
n-step SAWs. The connective constant mu=lim_n c_n^(1/n) exists by
submultiplicativity, with the following explicit argument. Splitting a
walk at step n gives its prefix and its suffix translated to the origin;
the pair uniquely reconstructs the original, so c_(n+m)<=c_n*c_m.
Set c_0=1 and b_n=log(c_n). These are finite because
1<=c_n<=4*3^(n-1) for n>=1 (a straight walk gives the lower inequality;
a nonbacktracking walk has at most four first steps and three later choices).
Thus b_(n+m)<=b_n+b_m. Put h=inf_(k>=1)b_k/k>=0. Every b_n/n>=h.
For any fixed k>=1 write n=qk+r with0<=r<k. Repeated subadditivity gives
b_n<=q*b_k+b_r. Dividing by n and taking the limit superior gives
limsup b_n/n<=b_k/k, because the finitely many b_r are bounded and
q/n tends to1/k. Taking the infimum over k gives limsup<=h; the earlier
lower inequality gives liminf>=h. Hence b_n/n tends to h and
c_n^(1/n) tends to mu=exp(h).

If P(z0)>=1, the right side diverges. If mu<1/z0, choose q with
mu<q<1/z0. For all sufficiently large n, c_n<=q^n by the defining limit;
therefore sum_n c_n z0^n converges geometrically. This contradicts d_n<=c_n
and divergence. Hence mu>=1/z0>=1051/400. This finite-family proof does not
need the infinite critical renewal identity as an additional premise.

## 3. Enumerating all bridges in a strip

Rotate the picture so the span direction is rows 0,...,l and the transverse
direction is columns. Translate every bridge so its minimum column is 0.
There is exactly one such translate. The start may occur at any column of
row 0; there is only one occupied vertex in row 0. All other occupied
vertices are in rows 1,...,l; the other endpoint is in row l.

Process lattice vertices column by column, bottom to top. A frontier state
records all occupied edges crossing the moving boundary, their connectivity
through already processed vertices, and two flags saying whether the start
and endpoint have been introduced. Every partial component is a path.
A component with neither terminal has two frontier stubs; one with one
terminal has one stub. A completed path with both terminals is accepted only
when no other component remains. A closed cycle is rejected.

The executable verifier implements this using explicit component identities:
- an unoccupied vertex has degree 0;
- a nonterminal occupied vertex has degree 2;
- row 0 can introduce the unique degree-1 start, with an edge to row 1;
- row l can introduce the unique degree-1 endpoint;
- no edge leaves rows 0,...,l;
- joining two stubs of the same component creates a cycle and is rejected;
- joining two terminal components accepts only the completed sole path;
- otherwise the remaining stubs inherit the merged component identity.

At each vertex the incoming left/down and outgoing right/up edge choices
are explicit. Each outgoing occupied edge contributes one factor z; an
incoming edge was already counted at its other endpoint. Every lattice edge
is thus counted once. A degree-1 terminal can also attach to an incoming
stub, with no new edge factor. These rules enumerate each edge subset once.
A finite connected graph with precisely two degree-1 vertices and all other
vertices degree 2 is a single path. Its orientation from the row-0 terminal
is unique. Thus every accepted graph is one bridge, and each bridge's edge
choices produce exactly its unique accepted history.

Components cannot cross in the planar strip. Their ordered boundary stubs
are serialized by matched brackets (paired stubs), singleton terminal labels,
and empty slots. The verifier decodes these to component identities before
using the degree rules, and checks the resulting bracket serialization.
The two outgoing kink slots change boundary order after processing a vertex;
right precedes up in that order. No unproved symmetry quotient is applied.

The finite state sets are generated from the empty initial state by a
monotone work list. Each newly found (stage,state) is enqueued once; set
difference against all known keys prevents duplicate enqueues. Processing it
adds every local successor to the next stage. All inserted states are reachable
by induction. When the work lists are empty, every known state has had all
successors inserted, so induction on path length proves that every reachable
state is known. A cap exit with pending states rejects. Thus each state need
be processed once for reachability, without changing the closure. Sorted
canonical state keys are retained for edge construction. Each outgoing
transition must land in the next stage's completed set. The full state and
edge counts are retained.

The all-empty state can persist through unused leading columns. At the end
of the first column remove only its surviving all-empty contribution. Every
nonempty bridge then has its first occupied column exactly 0. A nonempty
partial graph cannot reach the all-empty state without completing, which is
checked on every graph edge. The empty state has no completion. Hence this
removal discards only duplicate translates, not any bridge. Completions in
the first w columns count precisely bridges of range at most w-1.

## 4. Exact directed arithmetic

Use integer scale D=2^96. For each edge adding k=0,1,2 lattice edges, multiply
by (M/2^27)^k. Lower values use floor; upper values use ceiling. All input
values, transition weights, and completion multiplicities are nonnegative.
Induction on the finite sequence of stage updates shows that each lower
numerator/D is at most the exact value and each upper numerator/D is at
least the exact value. Zero integer terms may be skipped, since both floor and ceiling of a zero
product are zero. Addition is exact. Completion accumulation uses the
same nonnegative values. Thus after w columns

    b_l^- <= B_l^[w](z0) <= b_l^+,

where B_l^[w] counts bridges whose normalized columns lie in 0,...,w-1.

Unsigned products use explicit limbs and exact shifts; overflow guards
reject. The verifier accumulates each destination from transposed incoming
edges; there are no concurrent writes to a sum and integer addition has no
order-dependent rounding. The unmodified production kernel pushes outgoing contributions. The span-18
search adaptation transposes its own public-case-table graph for destination
accumulation as well; the verifier separately derives its graph from component
identities and constructs its upper potential by integer ceilings. Whole-state and
whole-edge recomputation, not sampling, is required.

## 5. Bounding the infinite-width bridge sums

For each stage r write its nonnegative linear transition as T_r and its
completion functional as c_r. On nonempty states find dyadic u_r>=0 with

    u_r >= c_r + T_r^t u_(r+1),

cyclically in r. The empty coordinate is fixed to zero; all its incoming
nonempty edges and completions are absent as checked above. For a nonnegative
in-flight state vector v_r, the displayed inequality gives

    <v_r,u_r> >= <v_r,c_r> + <T_r v_r,u_(r+1)>.

Iterating this inequality bounds any finite future completion sum by
<v_r,u_r>. Nonnegative monotone convergence then bounds ALL future
completions, even without any assertion about spectral radii.

The separate verifier constructs u with scale 2^-F (F=12 or F=44, recorded per replay), by repeated exact
integer-ceiling backward cycles, starting at zero. Each stage is the ceiling
of its rational right side. Monotonicity makes the sequence nondecreasing.
It accepts only a full stabilized cycle. Intermediate stage vectors from
that cycle and the fixed stage-0 vector satisfy every displayed inequality;
there is no floating-point candidate assumption. Overflow and failure to
stabilize reject. The finite full cycle is the certificate.

Pair the upper forward vector after w columns with u_0, rounding every
product upward. This is a rational t_l bounding the omitted completion
mass. Consequently

    b_l^- <= B_l(z0) <= b_l^+ + t_l =: U_l,

and B_l(z0) is finite. This proof only uses the finite inequality, not an
uncertified assertion that the fixed point should converge.

## 6. Two-sided renewal and a finite-family lower bound

Let A_l be the full irreducible-bridge generating sum at span l, evaluated
at z0. All sums are finite by 0<=A_l<=B_l<=U_l. The unique first irreducible
factor yields exactly

    B_l = A_l + sum_(j=1)^(l-1) A_j B_(l-j).

Suppose 0<=alpha_j<=A_j<=beta_j for smaller spans. Define

    lower_l = b_l^- - sum_(j<l) beta_j U_(l-j),
    alpha_l = max(0,lower_l),
    beta_l  = U_l - sum_(j<l) alpha_j b_(l-j)^-.

Nonnegative products and the renewal equality show alpha_l<=A_l<=beta_l.
An inverted or negative upper bracket rejects.

More strongly, alpha_l bounds the FINITE family F_l of section 1. Its
bridge sum B_l^[w_l] is its finite irreducible sum I_l^[w_l] plus its finite
reducible sum R_l^[w_l]. Every member of R_l^[w_l] also occurs in the full
renewal product, so

    R_l^[w_l] <= sum_(j<l) A_j B_(l-j)
                 <= sum_(j<l) beta_j U_(l-j).

Combining B_l^[w_l]>=b_l^- gives I_l^[w_l]>=lower_l; since I_l^[w_l]>=0,
it also gives I_l^[w_l]>=alpha_l. The subtractions therefore do not invent
signed bridge coefficients or claim that a truncated renewal is exact.
They certify a lower value for the exact nonnegative finite polynomial.
Finally

    P(z0)=sum_l I_l^[w_l](z0) >= sum_l alpha_l.

Acceptance requires the last rational sum to be at least 1. This proves the
frozen bar with the exact finite coefficients specified in section 1.

## 7. Verification scope

A passing assembler on untrusted JSON numbers proves only arithmetic.
Acceptance additionally requires complete frozen-artifact recomputation by
verify_strip.cpp at every span and every specified column, complete equality
of the lower/upper finite numerators, valid separately constructed tail
bounds, source/artifact hash bindings, and corruption controls with their
exact expected rejection codes. Baseline coefficients are not silently
adopted as verified enumeration. Small-span literal/series controls test the
implementation; the general proof supplies the all-span reduction.

## Appendix: the bracket invariant is preserved locally

No state is discarded merely because a geometric noncrossing property is
hoped to hold. Begin with no paired stubs. At a vertex, the two incoming
boundary slots are adjacent, as are the two outgoing boundary slots in the
new boundary order. The possible nonterminal degree cases are:

1. zero incoming and zero outgoing: nothing changes;
2. zero incoming and two outgoing: introduce an adjacent matched pair;
3. one incoming and one outgoing: move that stub across only the other,
   empty local slot, so the cyclic order of occupied stubs does not change;
4. two incoming and zero outgoing: remove two adjacent stubs. If they were
   paired to each other, reject the cycle. If their mates are distinct,
   join those mates. For a noncrossing matching, the two adjacent removed
   stubs' arcs are either nested, or disjoint with these as the adjacent
   inner ends. Joining the two remaining mates preserves noncrossing in
   both cases. If one removed stub is terminal-singleton, make the other
   mate a singleton. If both are terminal-singletons, accept only the sole
   completed path.

The terminal degree-1 cases insert one singleton at the local empty slot,
or remove one stub and replace its surviving mate by a singleton. They
introduce no new paired arc. Thus all reachable free-component pairings
remain noncrossing by induction. Matched-bracket serialization is lossless:
left-to-right scanning pairs every closing stub with the most recent
unclosed opening stub. Singleton labels and the endpoint flags complete
the component description. The verifier explicitly checks its stack and
component cardinalities, rejecting malformed serialization. This supplies
the state invariant without an assumed random-access encoding identity.

## Appendix: testing the all-length span-17 stop condition

Evaluate the same graph and exact interval argument at both
x0=51081913/2^27 and x1=51082227/2^27 for all l<=17. Exact cross
multiplication gives x0<t<x1, where t=400/1051. Put
lambda=(t-x0)/(x1-x0), so 0<lambda<1 and t=(1-lambda)x0+lambda*x1.

For every integer n>=1, f(z)=z^n is convex on z>=0. For n=1 this is
linearity; for n>=2 its second derivative is n(n-1)z^(n-2)>=0.
The defining convexity inequality therefore gives

    t^n <= (1-lambda)*x0^n + lambda*x1^n.

Multiplying by each nonnegative irreducible-bridge count and summing finite
partial series preserves the inequality. Taking their monotone limits
preserves it as well. The upper potentials establish finiteness at x1,
and hence throughout [0,x1], so every quantity below is finite. If U0
and U1 are the separately recomputed renewal upper sums for spans<=17,
then

    sum_(l<=17) A_l(t) <= (1-lambda)*U0 + lambda*U1.

Only if this last exact rational expression is below1 may the span-17
stop certificate be accepted. A restricted class of irreducible bridges
at spans<=17 has coefficientwise counts at most these full A_l, even
if it uses arbitrary lengths or transverse widths. It consequently cannot
pass the requested renewal bar under that span restriction. This is an
upper certificate for a restricted renewal sum, rather than an upper
bound on the connective constant. Acceptance requires all seventeen
auxiliary-point replays as well as the complete main frozen replay,
exact upper-endpoint assembly, and rejection controls. The construction
and point-evaluation framework are credited above; no novelty judgment
is made.
