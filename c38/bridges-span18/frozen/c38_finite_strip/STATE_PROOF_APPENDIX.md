# Why the frontier record is sufficient

Candidate and unrefereed; verifier separately written (same agent).
Credit Kesten, Jensen, Enting, Numaro and Vít Plánočka as in CREDITS.md.
This supplements the state proof without changing the frozen native code.

A processed partial component is a path. Regard each occupied frontier edge
as a dangling endpoint. Every processed nonterminal occupied vertex has
degree two. A component with no lattice terminal therefore has two dangling
endpoints; one with one lattice terminal has one. A component with both
lattice terminals has no dangling endpoint. A cycle has no terminals and
no dangling endpoint and is rejected. A path containing both terminals can
never be attached to a later vertex, since all its processed vertices have
their prescribed degrees. It is accepted only when it is the sole component;
otherwise it can never become part of one connected accepted path.

The retained state records the paired dangling endpoints of every terminal
free component, each single dangling endpoint of a component containing one
terminal, and flags sf and ef recording creation of the two lattice terminals.
It does not record which of two singleton components contains which terminal.
This omission is valid, for the following explicit reason. The only possible
future questions about an existing component are whether two incoming stubs
belong to the same component, whether it contains a terminal, and how many
terminals a newly joined component contains. Each is determined by the record.
The flags alone determine whether a new terminal may be introduced. If both
flags are set, any two distinct singleton components contain different
terminals: each terminal was introduced once, and each retained component
contains at most one. If only one flag is set, there is just one singleton
and its terminal identity is already fixed. Terminal names consequently
cannot change a legal edge choice, its edge weight, or completion acceptance.

The invariant can also be checked by a count. In every retained state the
number of singleton components equals sf+ef. Initially both sides are zero.
A new terminal adds one flag and changes a free component to a singleton or
creates one. If instead it attaches to an existing singleton, the two-terminal
path closes and is accepted or rejected immediately, never retained. Creating
a free component, leaving a vertex empty, or transferring a stub does not
change either side. Joining a free
component to a singleton leaves one singleton. Joining two singleton components
closes the two-terminal path and is accepted or rejected immediately, never
retained. Joining two free components leaves one free component. A same-component
join would close a cycle and is rejected. These exhaust the local degree cases.

The bracket encoding is lossless for the noncrossing pairing of the free
components, as proved in PROOF_FINITE_STRIP.md. A singleton marker records a
terminal-bearing component. The record is thus sufficient for all future
transitions even though it is not a reconstruction of the processed lattice
geometry. Different histories having the same record are added with their
full multiplicities; they are not identified as one walk. Each concrete final
edge set still has its unique sequence of local edge choices. Its orientation
from the unique row-zero terminal is unique, so completion weights count the
desired oriented bridges once.

The same reasoning applies to the rectangle verifier, where the starting
terminal is present in the initial frontier and only the endpoint flag can
change later. In both implementations the final graph has exactly two vertices
of degree one, all other occupied vertices of degree two, is connected, and
has no cycle. It is therefore a simple path. Distinct vertices of the lattice
are processed once and their degree choices are fixed once, establishing
self-avoidance and the asserted path/edge-set correspondence.
