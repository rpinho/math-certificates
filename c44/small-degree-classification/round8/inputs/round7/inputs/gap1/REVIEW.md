# Internal proof audit (same agent; no independent human review)

The candidate R4=22 is an upper-bound proof, not an UNSAT report from an
incomplete SAT model. Its finite computational premise is exactly the cubic
energy envelope on a published complete catalogue. Catalogue completeness
remains an external published premise. The direct verifier does not prove it.

Checked dependencies and potential failure points:

1. The catalogue's equivalence is input permutations and bit flips plus
   output complementation, as defined in the primary paper, Definition 1.
   It does not include arbitrary affine output additions. Parity conjugates
   these operations into the same equivalence up to output sign. Therefore
   local degrees, D and E3 are preserved. The paper's truth-table ordering
   uses increasing binary masks, matching the calculation; even reversing
   the coordinate order would preserve every invariant used here.
2. Every real cubic Boolean function is covered: pad to ten inputs using
   the external R3=10 theorem, then multiply by full parity to obtain a
   balanced 6-resilient sign function. Constants are covered too. A real
   cubic in fewer inputs need not itself be balanced; parity padding is
   still valid. The supplied 761 rows match the primary paper's class count
   and nonlinear-coordinate distribution 1,1,2,10,44,198,322,142,34,6,1.
3. The no-minimum case uses the binary support of the integer-valued
   derivative, not the real square of the derivative. Its binary degree is
   at most three. The second-weight theorem is applied in its allowed
   parameter range, appending dummy coordinates if needed.
4. All local degrees equal four only for the chosen variable-count
   maximizer. An arbitrary Boolean function is not asserted to have this
   property. A single AND substitution proves the count statement; the
   weighted extremal identity uses corrected simultaneous duplication.
5. The minimum-support classification has seven degree-three types. The
   four types with at most four controls need only the ordinary cubic cap.
   The other three have exactly the affine kernels used in the proof.
   Active assignments have density 1/8 in every type. Norm/covariance
   calculations use arbitrary Hilbert-space vectors, without assuming
   disjoint Fourier support or orthogonality prematurely.
6. Cubic coefficients in remaining variables are affine in controls
   because the original real degree is at most four. They vanish on active
   assignments because there the entire restriction is a dictator in i.
   There is no cubic term containing i. This justifies the exact kernels.
7. The pair-plus-triple contradiction only uses equality in its 23-variable
   budget. Saturation forces P=0 and all three norms to be 1/4. Parseval
   then makes all three corresponding cubic parts actual sign Boolean
   functions, whose sum cannot be zero pointwise.
8. In the three-pair case, R4=23 forces equality at every step, including
   the individual-coordinate weighted restriction inequality. Averaging
   the eight full-mismatch norms forces pairwise orthogonality. Singleton
   mismatch rows are inactive, so the complete equality signatures apply.
   This leaves one norm-one vector or two norm-one-half vectors, with all
   permutations included.
9. The pair lemma retains a possible even-in-(s,t) component U. The degree
   bound on U follows from U=T, not from assuming it vanishes. The encoded
   matched branch is h=s F(s,s,Z), of degree at most three. Counting s in h
   only weakens the junta-count upper bound. Exhaustive controls include
   all 65,536 four-input truth tables, with 4,096 admissible slice patterns.
10. In the two-half case, the nine variables in each cubic part follow from
    *all* local degrees being three in the catalogue equality class. Their
    intersection is forced by 9+9>16. An intersecting coordinate survives
    with local degree three on at least 5/8 of all control assignments.
    Its expected weight is at least 5/64, strictly above its original 1/16;
    other coordinates cannot compensate with negative restriction slack.

The independent packet calculation checks raw block duals, all finite
degree columns and the analytic tail separately from the primary integer-row
calculation. The R4 proof does not depend on the block duals or C44 recurrence.
Finite controls corroborate universal lemmas; they do not formalize them.
