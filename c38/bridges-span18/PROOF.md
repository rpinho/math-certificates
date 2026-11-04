# Candidate lower bound for the square-lattice connective constant

Candidate, unrefereed; verification level L0 for the bound as a whole. The enumeration and verifier were separately written by the same AI agent. The mathematical reductions below are prose proofs requiring mathematical review. Frozen inputs and certificate values are unchanged.

The claim is

\[
\mu(\mathbb Z^2)\ge 8388608/3192535=2.6275696272711184\ldots.
\]

Credit Harry Kesten for irreducible-bridge renewal, Iwan Jensen for the span-enumeration method, Numaro for the preceding span-17/length-260 coefficient certificate, I. G. Enting for the finite-lattice framework, Michael Fekete for the subadditive limit argument, and Vít Plánočka for the point-evaluation implementation adapted by the producer. See [CREDIT.md](CREDIT.md) and the retained MIT license. This candidate extends Numaro's span level and renewal framework; it uses fresh point evaluations rather than Numaro's original enumeration as a numerical premise.

## Finite family

A strict bridge is a self-avoiding nearest-neighbor path starting at (0,0), with all later first coordinates positive, and ending at its maximum first coordinate h. Its interior horizontal cuts must have at least three crossings. Translate to fix the start, and count both transverse orientations without a reflection quotient.

The polynomial P counts the disjoint union of all these irreducible bridges with spans 1–18 and the span-specific transverse range caps w_h-1 in [packet.json](frozen/c38_finite_strip/packet.json), and all such bridges with spans 19–30, transverse range at most 22, and at most five crossings at each interior cut. Its coefficients are exact nonnegative integer counts. The full expanded coefficient vector is not materialized. The geometry bounds its degree by 6817, including degree at most 1296 for span 18 and 690 for the supplement.

The [finite-strip proof](frozen/c38_finite_strip/PROOF_FINITE_STRIP.md), [state appendix](frozen/c38_finite_strip/STATE_PROOF_APPENDIX.md), and [arithmetic appendix](frozen/c38_finite_strip/ARITHMETIC_PROOF.md) specify the transfer states, path-counting correspondence, directed integer rounding and upper potentials. Every native replay output is retained. The [last-span proof](frozen/c38_finite_strip/PROOF_LAST_FINITE.md) replaces the all-range upper-potential step at span 18: its zero tail field is an unused marker, with infinite_tail_certified=false. Only the smaller spans supply the full upper values used to subtract reducible bridges.

The rectangle [geometric proof](frozen/rectangle_point/w22_h18_30_c5/input/PROOF_RECTANGLE.md) and [point-arithmetic proof](frozen/rectangle_point/w22_h18_30_c5/input/PROOF_RECTANGLE_POINT.md) justify normalization and the supplement's enclosures. Here W is a transverse range: W=22 allows 23 rows. These are finite families with lengths bounded by geometry, without a further series cutoff.

## Exact comparison

Write P=F+G+E for the first 17 spans, span 18, and the span 19–30 supplement. Put b=M/2^27, M=51081913, and c=51082227/2^27. The main and two-point packets establish

\[
F(b)\ge L_{17},\quad G(b)\ge L_{18}\ge0,\quad F(c)\le U.
\]

The range-22 rectangle includes spans 18–30. Its span-18 part is contained in the range-23 span-18 rectangle. Therefore

\[
E(b)\ge e=\max(0,(\mathrm{lo}_{22}-\mathrm{hi}_{23})/2^{96})>0.
\]

This bounds the value of a genuine nonnegative family; subtracting these two rectangle polynomials is not a definition of its coefficients. See the [disjoint-supplement proof](frozen/c38_disjoint_extension/input/PROOF_DISJOINT_EXTENSION.md).

For a=(M-k)/2^27 and r=(M-k)/M, the coefficientwise secant inequality proved in [PROOF_SECANT_RESCALE.md](frozen/c38_secant_rescale/input/PROOF_SECANT_RESCALE.md) gives

\[
F(a)\ge(1+k/314)L_{17}-(k/314)U.
\]

For each n≤N and 0<r<1, r^n≥r^N. The degree bounds and coefficient nonnegativity give G(a)≥r^1296 L_18 and E(a)≥r^690 e. Thus

\[
P(a)\ge S(k)=(1+k/314)L_{17}-(k/314)U+r^{1296}L_{18}+r^{690}e.
\]

At k=1353 the verifier recomputes the entire exact rational S(k), checks equality with the frozen value, and checks numerator≥denominator. Its decimal diagnostic is 1.0000001143720572. Then 1/a=8388608/3192535. All rational endpoints and parameters are collected in [EXACT_ENCLOSURES.json](EXACT_ENCLOSURES.json), derived from the frozen inputs. The [exact-power proof](frozen/c38_power_secant/input/PROOF_POWER_SECANT.md) supplies this final step. Failure of the sufficient inequality at k+1 gives no upper bound on μ.

Concatenation of members of the family produces self-avoiding walks, with factors recovered uniquely from singly crossed join cuts. Consequently the generating series of all walks dominates Σ_{j≥0}P(z)^j. If P(a)≥1 this series diverges at a. The explicitly proved submultiplicative limit for the walk counts implies that μ<1/a would force convergence there, a contradiction. This is the prose renewal-to-growth argument in section 2 of the finite-strip proof.

## Wording cautions in the frozen prose

The frozen main proof's section 6 initially discusses full A_l and B_l and a two-sided renewal formula at every span. For this packet that discussion applies through span 17; PROOF_LAST_FINITE.md explicitly replaces it at span 18. Reading section 6 alone as asserting a full span-18 upper enclosure would be incorrect.

The source report sometimes says “width 22” or “width 23” for rectangle parameters W=22 and W=23. Their proofs and sources define W as transverse range, giving 23 and 24 allowed rows respectively. This release uses “range.”

The exact-power proof says its verifier “validates … all actual native outputs.” In the fast mode it reads and binds saved outputs and historical native receipts, checking equality and arithmetic; it does not execute the native enumeration. Fresh native reconstruction is a separate procedure in [REPRODUCE.md](REPRODUCE.md). These are scope clarifications, not changes to the frozen certificate. No numerical inconsistency was found in the family parameters, degrees, fractions, or final exact comparison.
