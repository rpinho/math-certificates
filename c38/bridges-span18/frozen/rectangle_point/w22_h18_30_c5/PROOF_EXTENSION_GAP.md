# Upper comparison for the restricted extension attempts

Candidate and unrefereed; verifier separately written (same agent).
Credit Kesten, Jensen, Enting, Numaro and Vít Plánočka as in CREDITS.md.

The span17 stop certificate gives an exact rational U with
sum_(h<=17) A_h(400/1051)<=U<1, including every length and transverse range.
The separately replayed rectangle certificate gives an exact rational V
bounding its complete finite irreducible family at400/1051. Its target
upper value includes the exact (target/dyadic_point)^maximum_degree
correction proved in PROOF_RECTANGLE_POINT.md; an upper value at the
smaller dyadic point alone would not suffice.

The rectangle spans are all at least18. They are disjoint from the entire
span<=17 family. Nonnegative coefficient sums consequently add, and the
sum for any subfamily of their union is at most U+V. Only if the exact
rational comparison U+V<1 passes does this particular extension fail
the requested renewal bar even on top of the full span17 family.
This gives no upper bound on mu and uses no Numaro enumeration premise.

The comparison verifier rechecks both component artifacts, their completed
native receipts and exact corruption-control results. The span17 component
additionally requires its standard whole-union two-point replay receipt.
The comparison is itself accompanied by actual source-byte, overlap-scope,
missing-full-replay and incomplete-control corruptions, each with its
exact expected rejection. No unverified point diagnostic is admissible.
