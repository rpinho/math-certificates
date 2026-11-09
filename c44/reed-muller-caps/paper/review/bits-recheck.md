Shipped: acceptance of the v3-to-v4 edit for release of the supplied PDF. R1 is fixed, the replacement notation preserves the mathematics, and the requested passages render correctly.

Recheck dated 2026-11-09. I compared `inputs4/paper_v3.tex` and `inputs4/paper_v4.tex`, read both supplied v3 reviews, and inspected the rendered `inputs4/paper_v4.pdf`. The supplied `v3_to_v4.diff` exactly matches the source comparison apart from the diff file headers. It contains five hunks; there are no other source changes.

1. **Front matter (`@@ -50,12 +50,10 @@`): R1 fixed.** The text now says the numbered sections “follow” the frozen `PROOF.md`, identifies its ±1 convention, and describes the conversion to bits and the rewriting and shortening of Section 4. This implements the second reviewer's proposed replacement. The stale assertion that the sections transcribe the source, except for a step-by-step expansion of Section 4, is gone.

2. **Derivative and notation definition (`@@ -108,12 +106,12 @@`): correct and unambiguous.** The displayed formula is now `A_i = f(x_i=1) - f(x_i=0)`, immediately followed by the definition that `f(x_i=a)` means evaluation with coordinate i set to a. The other coordinates remain the free input coordinates, held equal between the two evaluations. This is a restriction of the multivariate function, not evaluation on the truth value of an equality. It is exactly the former coordinate-replacement notation. The derivative is still the full bit difference, with the same sign, values, degree and influence normalization.

3. **Section 2 half-difference (`@@ -199,7 +197,7 @@`): correct and unambiguous.** `Delta_j A = (A(x_j=1) - A(x_j=0))/2` applies the already defined evaluation convention to A and coordinate j. The denominator 2 remains; this is still a half-difference, distinct from the full difference defining A_i. Its values, degree bound, Walsh sign and squared-energy identity are unchanged.

4. **Section 3 decomposition (`@@ -288,7 +286,7 @@`): correct and unambiguous.** `B = f(x_i=0)` is the zero branch as a function of the remaining coordinates `(x_H,x_Y)`. Thus `f = x_i A_i(x_H) + B(x_H,x_Y)` still has branches B and B+A_i. On active control inputs, A_i=1 forces B=0 and A_i=-1 forces B=1, giving x_i and 1-x_i respectively. The notation introduces no change to the decomposition or its consequences.

5. **Section 4 editorial note (`@@ -342,8 +340,8 @@`): editorial only.** The repeated attribution becomes “see the note at the start,” which points to the corrected front matter. Attribution remains there and in the closing credit. The revision date, unchanged-conclusions statement and historical commit link remain intact. No proof text changes in this hunk.

Everything else in the TeX is unchanged, including the numbered equations, numerical bounds, corrections, certificate descriptions and candidate/unrefereed qualifications. The old coordinate-replacement notation has no remaining uses. The other optional suggestions in the second review were not required changes and do not prevent acceptance.

I visually read PDF pages 1–2, including the corrected provenance and derivative definition, page 3's Section 2 half-difference, page 4's Section 3 decomposition, and page 5's revised editorial note. These passages match the source. The equals signs, subscripts, minus signs and fraction denominator are legible and correctly placed; no missing glyph, overlap or clipping was found in the inspected passages.

Did this recheck find a new mathematical result? No. This accepts the small edit under the same scope and external premises as the prior acceptance; it is not a fresh numerical-certificate replay.

Required changes before this PDF goes out: none.

VERDICT: ACCEPT
