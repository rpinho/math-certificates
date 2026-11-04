# Exact arithmetic and finite-state implementation details

Candidate and unrefereed; verifier separately written (same agent).
This supplements PROOF_FINITE_STRIP.md for its frozen verify_strip.cpp.
Credit Kesten, Jensen, Enting, Numaro and Vít Plánočka as in CREDITS.md.

The verifier's unsigned128-bit value type holds integers0,...,2^128-1.
All left/right shifts below operate on unsigned values. A detected
capacity failure exits with rejection, so only an accepting execution is
considered in the following argument.

For the helper weighted(n,q,s,ceil), write
n=n0+2^64*n1 with0<=n0,n1<2^64 and0<=q<2^64. Form exact128-bit products
A=n0*q and B=n1*q. Put

    C=floor(A/2^64)+(B mod2^64),
    p0=A mod2^64, p1=C mod2^64,
    p2=floor(B/2^64)+floor(C/2^64).

Here C<2^65, so its128-bit calculation is exact. Multiplication gives
n*q=p0+2^64*p1+2^128*p2 exactly, and p2<2^64 because n*q<2^192.
Thus the indicated64-bit p2 addition cannot wrap. This applies both to
forward weights and to the tail-potential multiplier; the latter need
not be restricted to the forward weight's54-bit size.

All shifts s used by this helper satisfy1<=s<64: forward shifts are27
and54, while the recorded tail scale F is12 (or44 for older controls).
The test p2>>s=0 is equivalent to n*q/2^s<2^128. If it fails, reject.
When it passes, the low quotient limb is
(p0>>s) OR (p1<<(64-s)), and the high quotient limb is
(p1>>s) OR (p2<<(64-s)). OR combines disjoint bit positions, so these
are exactly floor(n*q/2^s). The discarded remainder is nonzero exactly
when p0 AND (2^s-1) is nonzero. A lower update keeps the quotient; an
upper update adds one precisely in that case. The possible final carry
is explicitly guarded. This proves floor/ceil correctness, without
hardware floating-point rounding assumptions.

A zero-edge transition copies the numerator unchanged. For each other
forward edge the multiplier is M or M^2 and the shift is27 or54, hence
its exact rational multiplier is (M/2^27)^k. Every nonzero forwarded
input is checked below2^107 before multiplication. The full192-bit
procedure above is exact even for a general128-bit tail input. Every
accumulation tests whether its next addend would exceed2^128-1 before
adding it. Completion multiplicity is at most4, since there are just
four choices of the two outgoing edge bits. Its input below2^107
therefore produces a product below2^109; its addition is also checked.
Final tail additions use the same capacity checks. Consequently none
of the accepted forward/completion/tail integers have wrapped.

The upper-potential routine stores each entry as a64-bit integer below
2^60, representing that integer divided by2^F. Transition weights use
a common denominator2^54 with integer numerators2^54,M*2^27,M^2.
Each is at most2^54 because0<M<2^26. There are at most3 outgoing
continuations, and at most4 completions. For F<=50, its exact128-bit
right-side numerator is less than

    4*2^(F+54)+3*2^(60+54) < 2^116.

Adding2^54-1 and shifting by54 therefore implements its ceiling
exactly with ample128-bit capacity. Each resulting entry is checked
below2^60 before storing it. Nonnegative monotonicity and a full
stabilized cycle yield the stagewise potential inequalities proved in
PROOF_FINITE_STRIP.md. This calculation concerns the empty coordinate
only after removing it: no nonempty continuation may reach that
coordinate and no empty state may complete, as the graph checks assert.

Each graph edge records a destination index in its lower30 bits and
an added-edge count k in its upper2 bits. Every accepted stage has
fewer than2^30 states, so no destination or transposed source index
uses those upper bits. Its local update has k in{0,1,2}; its packed
encoding is therefore lossless. A stage has at most3 continuations
per state; the explicit3*source-size<2^32 check bounds all its edge
prefix sums and32-bit edge offsets. Counts across finitely many stages
use64-bit totals. Every constructed continuation is looked up in the
complete next-stage key set; a missing key rejects.

Keys use two bits per boundary slot plus the two endpoint flags. At
span18 fewer than64 bits are occupied, so UINT64_MAX cannot be a valid
key and is an unambiguous sorting/hash-table sentinel. Sorted keys
are deduplicated exactly, with no probabilistic hash equality. The
hash table stores and compares full keys and uses collision resolution.
Thus a hash collision cannot identify different states. Its destination
lookup supplies precisely the index of the full matching canonical key.
The work-list closure proof is in the main proof; its finite turn cap
rejects if any unprocessed reachable state remains.

The transposed edge list is constructed from every outgoing edge once.
Its destination prefix sum counts the number of incoming entries, then
a cursor places the original source index and k in exactly that range.
Therefore destination accumulation sums exactly the same multiset of
nonnegative directed contributions as outgoing accumulation would.
Each destination/plane is owned by one parallel loop iteration. Integer
addition is associative when no overflow occurs, and its overflow checks
have just been established. Thread scheduling cannot change any accepted
numerator. The two-point replay reuses this same graph, resets the value
and potential arrays, and uses the separately recorded M at each point;
no first-point numerical array is reused as a second-point initial value.

For verify_finite_strip.cpp, the same graph and exact finite forward
arithmetic are retained. The upper-potential routine is not called. Its
output explicitly marks FINITE_LAST_SPAN_LOWER_ONLY and sets the unused
num_tail marker to zero. PROOF_LAST_FINITE.md derives the final-span
irreducible lower value using only smaller-span full upper bounds.
No span18 all-width tail inequality is inferred from that zero marker.

For the target comparison,400*134217728-1051*51081913=637>0.
Thus z0=51081913/134217728<400/1051, and

    134217728/51081913 - 1051/400 = 637/20432765200 > 0.

The located public comparison has the same positive numerator134217728
and denominator51082227=51081913+314, so the candidate reciprocal is
strictly larger. The Numaro comparison is checked by exact cross
multiplication against340282366920938463463374607431768211456 divided
by129513673858566230428673965530967449326. These are numerical comparisons
with attributed public fractions, without a novelty judgment.
