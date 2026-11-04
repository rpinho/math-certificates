# Explicit restricted bridge coefficient supplement

Candidate and unrefereed. This is the proof specification; acceptance is
pending complete counts, separately written (same agent) verification,
and the target inequality. No novelty judgment.

Credit Harry Kesten and Iwan Jensen for bridge renewal, Numaro for the
frozen span-17 baseline table, and Vít Plánočka for the boundary state/case
framework adapted by rectangle_counts.cpp and for the restricted-grammar
prior work. Enting's finite-lattice method underlies the transfer approach.
The source's infinite pumping/subset construction is not required by this
finite rectangle supplement. Its result remains an important public comparison.

## 1. The finite family

Use the same strict bridge convention as PROOF_FINITE_STRIP.md: start at
(0,0), all later first coordinates in {1,...,h}, endpoint first coordinate
h. An irreducible bridge crosses each interior cut x=j+1/2 at least three
times. The proof of that characterization and the finite-family growth
argument are given there.

Fix span h=18 and transverse range W. Let r_(n,W) count ALL irreducible
bridges of this span and length n with max(y)-min(y)<=W. These are finite
nonnegative integer counts. Since the start is the only vertex at x=0 and
there are at most h(W+1) other vertices, length<=h(W+1). A length cutoff
N may discard longer members; this only decreases the nonnegative sum.

Let C_(n,W) count paths placed in the fixed rectangle
{1,...,h} x {0,...,W}, with one start at (0,s), s in {0,...,W}, and with
the same strict bridge/irreducibility conditions. Every bridge with
transverse range R<=W has W-R+1 placements. In the analogous rectangle
with heights 0,...,W-1 it has W-R placements if R<W, and zero if R=W.
Subtracting therefore counts each translation class exactly once:

    r_(n,W) = C_(n,W) - C_(n,W-1).

Equivalently, subtract paths avoiding row 0 after shifting their heights
down by one. This is a set injection, so the difference is nonnegative.
No rotational or reflection quotient is taken: distinct oriented walks
from their starts remain distinct.

## 2. Exact production enumeration

The state across a moving kink records the occupied left/down frontier
stubs and their partial-path connectivity. A component not attached to a
terminal has exactly two stubs; the component attached to the start has
one. In the last column a second terminal may be introduced. Paired
stubs have noncrossing connectivity, encoded by matched brackets; terminal
stubs use singleton labels. The local invariant and lossless serialization
are established in the appendix of PROOF_FINITE_STRIP.md.

Initially choose each start height s once and put its sole rightward edge
into column 1 at that height. This accounts for one edge and one singleton
frontier stub. There are no other occupied vertices in column 0.

In columns 1,...,h-1, every occupied vertex has degree 2. At an empty pair
of incoming ports, either leave the vertex empty or create its two outgoing
edges. At one incoming port, choose exactly one outgoing port. At two
incoming ports, join them with no outgoing edge. Joining stubs already
connected would form a cycle and is rejected. No vertical edge leaves the
transverse rectangle. Every newly added outgoing edge increments length
by one; incoming edges were already counted.

After processing an interior column, the number of outgoing horizontal
stubs is exactly the crossing count at its right cut. Retain the state
only if that number is odd and at least 3. Thus no reducible bridge is ever
accepted. This condition removes an entire partial prefix only when it
has already fixed a disallowed interior cut; a later column cannot alter
that cut. All prefixes of every admissible bridge survive.

In the final column no edge may go right. Exactly one degree-1 terminal
must be introduced, at any height, either with an outgoing vertical edge
or by ending an incoming component. Other occupied vertices have degree 2.
A component can close only if it contains both terminals and no other
frontier component remains; otherwise reject it. The remaining unprocessed
vertices then have no incoming occupied edge and are empty. Each completed
graph has two degree-1 vertices and every other occupied vertex of degree 2,
so it is a single path with a unique orientation from its start.

Every path in the specified rectangle fixes a unique edge choice at each
processed vertex. Conversely all accepted choices produce just such a
path. This proves a bijection between accepted histories and the counted
walks, including multiplicities over start heights. Column pruning enforces
irreducibility and the length-indexed dynamic program enforces the cutoff.

Each state stores a polynomial of exact nonnegative integers. A transition
shifts by its number of newly occupied edges; branches add. Truncation
past N is sound because every edge increment is nonnegative. Production
uses a 1024-bit integer with checked overflow. A carry beyond its capacity
rejects, so no modular wraparound can be silently treated as an exact count.
The finite output retains both C_(n,W) and C_(n,W-1); their exact difference
is taken and checked separately.

## 3. Separately written modular verification

verify_rectangle.cpp does not import the production case table or its
integer type. It decodes stubs into explicit component identities, loops
through outgoing edge subsets, imposes the degree conditions just described,
merges component identities, and serializes the surviving connectivity.
It performs the entire finite polynomial dynamic program modulo 21
pairwise coprime positive integers less than 2^31. This is a separately
written (same agent) implementation, not separate authorship.

For each modulus p, adding two residues below p fits unsigned 32 bits:
2p-2 < 2^32. One conditional subtraction gives the correct residue.
Completion multiplicity is handled by repeated addition. There are no
floating-point decisions.

The exact Python verifier checks gcd(p_i,p_j)=1 for every pair, forms
Q=product p_i, and requires

    Q > 4(W+1)*3^(N-1).

For n>=1 there are at most 4*3^(n-1) nonbacktracking walks from a specified
start: four choices for the first step and at most three subsequently.
Every self-avoiding walk is nonbacktracking. There are W+1 allowed starts,
so C_(n,W)<=4(W+1)*3^(n-1). This also bounds the smaller-height count.
Thus all true final coefficients for n<=N are strictly below Q. Intermediate
partial graph counts need no such bound: modular arithmetic is always
valid, and only the final coefficients are reconstructed.

Successive exact CRT reconstruction yields the unique integer in [0,Q)
with the computed residues. The count bound proves it is the true exact
coefficient. The verifier compares every reconstructed coefficient against
the production all/without-bottom values, checks nonnegativity of their
difference, and checks the minimum length 3h and finite vertex length bound.
All coefficients, not a sample, must match.

## 4. Adding to the attributed baseline

The frozen Numaro bridge table has b_(n,l), 1<=l<=17, n<=260. Its documented
span renewal gives exact irreducible coefficients a^base_n=sum_(l<=17)a_(n,l)
through that length. Our separate baseline checker rederives that renewal
and the exact polynomial arithmetic. The original hundreds-of-millions-state
enumeration is an attributed public computational premise, not verified
by hashing its table or replaying its lightweight checker. Its provenance,
original table hash, retrieved archive checksums and small-span controls
are stated in PRIOR_ART.md and the final report.

The rectangle family has span 18 and the baseline family has span<=17.
They are disjoint even if their lengths coincide. Therefore, setting

    a_n = a^base_n + r_(n,W) for n<=260,

where missing/truncated terms are zero, gives exact nonnegative counts of
a disjoint finite family of irreducible bridges. If the rectangle cutoff
exceeds 260, retain its terms separately at those lengths as well; no
baseline counts are asserted beyond 260.

The expanded vector a_n is the explicit certificate. The separate verifier
must check every coefficient addition and evaluate

    sum_n a_n * 400^n * 1051^(D-n) >= 1051^D,

where D is the maximum retained degree. This is one exact integer
comparison. The finite-family argument in PROOF_FINITE_STRIP.md then gives
mu>=1051/400. The slightly stronger dyadic point used for strip diagnostics
is not needed for this explicit polynomial's target test.

If the inequality fails, the family is a documented negative attempt, not
a bound. If only a subset of the complete modular replays is available,
no certificate acceptance is permitted. Rejection controls must change
actual frozen artifacts and produce their exact prescribed rejection codes.

## 5. A finite interval of supplemental spans

The same construction may retain every span h in a finite interval
h_min,...,h_max with h_min>=18. Let r_n be the sum of r_(n,W,h) over this
interval, with n<=N. Distinct spans are disjoint, and every retained span
exceeds the baseline's 17. All statements above remain valid with these r_n.
The maximum degree is min(N,h_max*(W+1)), with retained zero padding allowed.

The implementation forks the current prefix dynamic program at each allowed
terminal column: one copy imposes the final-column endpoint rules and adds
its completions, while the other continues with ordinary degree-2 rules
and the >=3 crossing filter. No complete path is retained in the continuation
branch, which has not introduced an endpoint. Each accepted path has a
unique final span, hence appears in exactly one terminal fork.

The exact verification repeats every terminal fork and every ordinary
prefix update. The coefficient bound remains 4(W+1)3^(n-1), without a factor
for the number of spans: the disjoint union is still a subset of all n-step
SAWs from the W+1 allowed starts. The original fixed-span code is also a
control, since [h,h] must reproduce the same coefficient vector exactly.
