# What the twelve public theorems say

The independent target is the measurable-set upper bound on the ordinary unit sphere in ambient dimension n ≥ 3, with normalized surface measure and the literal open double cap D. I used the literature summary frozen before checkout, the paper abstract recorded there, and the authors’ public statement to distinguish the core conjecture from the additional rigidity and projective claims. I did not use the paper’s proof. [Prior-art record](PRIOR_ART.md) · [Paper](https://arxiv.org/abs/2610.27523) · [Pinned statement and definitions](https://github.com/allenibiapina/LeanShadow/blob/19deb3ed555cc8404958c1804f9b29898a918d10/ComparatorChallenges/Shadow.lean) · [Authors’ mathematical statement](https://github.com/allenibiapina/LeanShadow/blob/19deb3ed555cc8404958c1804f9b29898a918d10/MAIN_STATEMENT.md)

## The five double-cap statements

In the table, area is the *real value* of the normalized spherical measure obtained from an additive Haar measure on the ambient Euclidean space. The normalization divides by the measure of the entire sphere. The frozen instance uses Lebesgue volume. In finite positive measure the conversion to real preserves order. The index type has cardinality n and its Euclidean space has that finrank. The usual sphere is therefore Sⁿ⁻¹, and the exponent in δ is n−2. Independence means that every ordered pair of points has nonzero real inner product, including pairs of opposite points and self-pairs. Self-pairs never add a restriction on a unit sphere. No antipodal symmetry is assumed of A.

| Declaration and challenge line | Literal statement | Published claim and differences | Attainment and non-vacuity |
|---|---|---|---|
| double_cap_bound, 129 | Every completed-measurable independent A has area ≤ δ(n−2) when finrank > 2. | Witsenhausen–Kalai upper bound. Completed measurability includes the Borel-measurable sets in the frozen spec. The formula becomes the area of **each** literal open double cap by the first part of caps_attain at π/4. | The independent proofs give measurable D, strict positivity and pointwise independence. No supremum occurs. |
| double_cap_equality, 134 | If such an A has area δ(n−2), some axis gives A equal almost everywhere to the open double cap of radius π/4. | The authors’ extra rigidity claim for maximizers, with the same dimension, normalization and completion. It gives a.e. equality. It does not transfer pointwise independence through arbitrary null edits. | The equality hypothesis holds for D by caps_attain, and D satisfies the independence hypothesis. No supremum occurs. |
| double_cap_attainment, 141 | Some Borel-measurable independent A has area δ(n−2) in each allowed dimension. | Attainment of the authors’ numerical maximum. This existential theorem does not name its witness or its axis. Combining caps_attain with the independent D_avoids identifies the literal **open** caps as witnesses. | Positive mass excludes the empty set as a maximizer. No supremum occurs. |
| double_cap_conjecture, 146 | δ(n−2) is a greatest element of the set of real masses of completed-measurable independent sets, for finrank > 2. | Maximum formulation of the conjecture. IsGreatest contains both membership and an upper bound for every admissible mass. Competitors use the same normalization and exact orthogonality. The cap formula still needs its geometric identification. | Membership rules out an empty set of masses. The unit total bounds all competitors by 1. No fallback value of sSup can establish greatestness. |
| s2_double_cap_bound, 177 | In ℝ³, every completed-measurable independent subset of S² has normalized area ≤ 1−√2/2. | The ordinary-sphere value 1−1/√2. The dimension is fixed by Fin 3. The separate hdim parameter for the general theorems is omitted. This is the numerical upper bound only. | D attains it by the cap integral at exponent one. The explicit real bound is independent of any sSup. |

## The other seven

| Declaration and challenge line | Scope |
|---|---|
| sharp_shadow_inequality, 107 | Given a completed-measurable spherical A with the mass of the open caps of radius r ∈ [0,π/2], its orthogonality shadow has compact-inner area at least beltMass(n−2,r). The radius is supplied with its mass equation. |
| sharp_shadow_equality, 114 | At interior mass, equality in that shadow bound forces A to agree a.e. with open caps of that radius. |
| caps_attain, 123 | For an arbitrary axis, the actual open caps have the specified cap mass and their literal shadow has the specified inner area. The first conjunct supplies the bridge. |
| alpha_eq_delta, 149 | The real supremum of the admissible masses equals δ(n−2). The separate greatest-element theorem supplies nonemptiness and boundedness, excluding a junk supremum. |
| projective_shadow_inequality, 152 | The pushforward probability on the antipodal quotient gives the same lower bound on compact-inner shadow measure for completed-measurable sets of the stated mass. Orthogonality is witnessed by representatives. |
| projective_shadow_equality, 159 | At interior mass, equality forces a.e. agreement with the image of **closed** opposite caps. This is a rigidity statement on the quotient. |
| projective_caps_attain, 169 | Projected closed caps realize the cap and belt formulas for every radius in the closed interval. The definition of projectiveCap differs at the boundary from the spherical open D. |

## Duplicate definitions

The full unified diff has two hunks. The first changes the introductory documentation. The second leaves the common definition of alpha intact, adds a blank line, universe and variable declarations, include/omit directives and all twelve theorem signatures with intentional placeholders, then closes the same namespace. The shared mathematical definitions, instances and setoid proof have identical source text. [Full diff](logs/definitions.diff)
