# The relative-sign prediction in Abouzaid–Diogo Remark 4.10

## Result and exact target

In the integral wrapped Floer algebra and identifications of
Abouzaid–Diogo, *Monotone Lagrangians in cotangent bundles of spheres*,
https://arxiv.org/abs/2011.13478v2 (Adv. Math.427(2023)109114), the fundamental
class w of the T2 component in Lemma4.9(2) is

    w = ±u(e1+e2).

This proves the relative-sign prediction of Remark4.10 (preprint p21;
journal p26). The overall sign depends on orientation and is not determined.
The original coefficients, not new objects or a restricted characteristic,
are being compared. Luís Diogo is coauthor.

We use the paper's standard regular triangle computations, retaining all
orientation and coefficient lines. We use its published Floer foundations
and polygon classification, not a new reconstruction of those foundations.
Ono, SIGMA21(2025)030, https://arxiv.org/abs/2504.20489,
https://doi.org/10.3842/SIGMA.2025.030, supplies explicit conventions for the
same standard Bott–Morse orientation-line correspondences.

## 1. Normal published calculation and the missing sign

Write A=K[u], K=Lambda(C), and |u|=−2. Proposition4.6 identifies
N≃F⊕F[1] over the integers, up to an immaterial overall shift, and identifies
its endomorphisms with the graded matrix algebra over Z[u]. Let e1,e2
be its two diagonal idempotents and e=e1+e2.

The normal product-complex-structure calculation of Lemma4.9 uses the
T2-family of lifts of the triangle in Figure3. Inserting the fundamental
class leaves an integral isomorphism. It gives

    w = s1*u*e1+s2*u*e2,       s1,s2 ∈ {−1,1}.

This is the reproduced baseline. Integral invertibility alone does not
identify the signs. No unsigned calculation or characteristic-two
specialization will do so.

Choose the source's T_alpha, alpha=T^(−2*tau)*U^(−1) nonzero,
tau>0. Lemma4.17 and its proof give dim_K HF(N_i,T_alpha)=4 and
M=HF(F,T_alpha) of dimension2. Composition with e is invertible. In the
source's clean Morse bases the unit-normalized action

    B = phi_w * phi_e^(−1)

is triangular. Its small Figure7 triangle families give diagonal entries
of magnitude alpha. The other, four-dimensional family gives only a
strictly off-diagonal corner. The printed signs are independent; no common
sign is assumed. We prove that common sign next.

## 2. Geometry of the two small correspondences

In the source's model

    X = {u1*v1=z+1, u2*v2=z−1},

G=(S1)^2 acts by (ui,vi)↦(ai*ui,ai^(−1)*vi). The underlying boundary
Lagrangians N0,N1,T_alpha are invariant. Each endpoint clean component
C_i=N_i∩T_alpha is a single free G-torsor, a two-torus.

Use the original two small triangle families described in Lemma4.17.
Keep the critical corner; do not move it off the critical value while
asserting equivariance. The simultaneous invariant and regular choice can
be checked directly, without averaging a generic almost complex structure.
In the natural holomorphic model, choose roots r_i(z)^2=z-c_i on each small
base triangle's interior. The balanced boundary conditions become
|u_i/r_i|=1, with v_i/r_i=(u_i/r_i)^(-1). The lifts are constant phase
multiples, hence G-orbits. At ordinary corners the roots are nonzero. At
the critical corner a root has exponent beta=theta/(2*pi) in (0,1), where
theta is the interior angle of the simple base triangle in (0,2*pi).
Both a quotient and its inverse have growth slower than a pole; reflection
of the unit-circle boundary condition removes a possible boundary
singularity. The maximum principle then gives constant unit modulus.

For regularity with that original corner retained, a vertical infinitesimal
variation has h=delta u_i/u_i=−delta v_i/v_i and boundary condition Re(h)=0.
Its endpoint variation is bounded (and vanishes in the collapsed factor),
so h grows at most as |s|^(−beta) in a disk coordinate at the corner.
Since beta<1, Schwarz reflection of the imaginary boundary condition gives
a removable singularity. Thus h is a constant imaginary phase variation.
There is one per factor and no other vertical kernel. The base simple
triangle is rigid and regular modulo domain automorphisms. Together with
the published Fredholm index2 this gives regularity of the invariant small
family. This is a local regularity check of the existing family; the
published global contribution classification is still an input.

On each small regular two-dimensional family G acts freely: a stabilizer
would fix an endpoint in the free torsor C_i. An orbit is open (full
dimension) and closed (G is compact), so every connected component is a
free G orbit.
The two endpoint evaluations are equivariant maps between free G-torsors,
hence diffeomorphisms. In phase coordinates their comparison is translation.
It cannot invert either circle. Thus its action on every cohomology degree
of a torus is the identity.

If a small family has more than one connected component, each contributes
a scalar times that identity; their sum still has that form. The magnitude
of the sum and the contribution classification are the ones already
computed in the source. This argument changes neither polygon classes nor
perturbation count.

## 3. The coefficient lines, without an assumed equivariant brane lift

Individual branes need not admit a G-equivariant lift: T_alpha has holonomy
−1 along both fiber circles. Instead work with the actual combined Floer
line of source Section3.2,

    E_i = Hom(xi_{N_i},xi_T) tensor o_{C_i}.

Its monodromies along the two fiber circles are ±1. The coefficient bundle
of N_i is trivial, xi_T has holonomy−1 there, and the Floer orientation line
has O(1) monodromy.

These combined lines are trivial. Otherwise a circle has monodromy−1,
and the torus cellular/Morse complex with coefficients E_i is acyclic over
K: the corresponding Koszul coefficient 1−(−1)=2 is invertible. This is the
energy-zero part of the clean Floer complex. The other strip contributions
have strictly positive energy. Over the complete Novikov field, the usual
convergent perturbation series for a contraction then makes the full complex
acyclic as well. This contradicts the published nonzero rank4 group. The
source identifies just one clean torus at each endpoint, so no extra clean
component invalidates this argument.

The corner inputs e and w are the maxima on their clean components.
In the de Rham model they are degree-zero forms, with their flat orientation
coefficients; their existence as fundamental-class cycles supplies these
flat sections. Their clean Floer shifts are respectively0 and−2.

Ono Proposition3.1 gives the relative determinant-line isomorphism over the
polygon moduli space. Tensor it with the usual flat local-system transport
on the boundary arcs. After inserting the corner's flat zero-form, this is
a flat morphism between the pulled-back E_i lines at the endpoints. Since
E_i are trivial and endpoint evaluations are diffeomorphisms, it is one
constant scalar on each connected orbit. The area and holonomy weight are
constant on that orbit too. This establishes a scalar-weighted translation
correspondence without asserting equivariance of the individual branes.

## 4. The sign on different Morse degrees

Constantness of a determinant-line scalar alone is insufficient; the
operation's explicit degree sign must also be compared.
For k=2, Ono Definition3.3/equation(3.4) has exponent, modulo2,

    epsilon(xi1,xi2) = (deg xi1−1)
                       +(2+mu(R1))*(deg xi2−1)+1.

If the e/w corner is first, its form degree is0 and its clean Floer shift
is even for both inputs. The degree-dependent factor is the same in both
products. If it is second, the degree-dependent factor is again identical.
Their ratio therefore has one sign independent of the other input's Morse
degree. Changing from de Rham to the perfect Morse model does not change
the cohomological product or its ordinary trace.

Combining this with Sections2–3, the two small-family maps are scalar times
translation, with the same dependence on the other input's degree. After
normalizing by phi_e, all four diagonal coefficients have ONE common sign.
The magnitude ratio is alpha by the source's equation(4.6). Consequently,

    tr(B) = 4*epsilon*alpha != 0,       epsilon ∈ {−1,1}.

The large triangle family is strictly off-diagonal as in Lemma4.17; its
trace is zero.

## 5. Integral conclusion

Under N≃F⊕F[1], HF(N,T_alpha)≃M⊕M[1], dim_K M=2. If U_M denotes the
even action of u on M, the unit-normalized action of w is conjugate to

    diag(s1*U_M, s2*U_M).

This uses ordinary trace, not supertrace. Because u is even, shifting a
summand by1 does not negate its action. If s1=−s2, this trace is zero for
every U_M. That contradicts Section4. Hence s1=s2.

The coefficients were integers ±1 before extension to characteristic zero,
so detecting their equality over K proves the original integral identity
w=±u(e1+e2). This is exactly the prediction stated in Remark4.10.

## Verification and limits

The independently requested agent referee supplied and accepted the completed
orientation/local-system argument; see referee/VERDICT.md and referee/FINAL_PACKET_REVIEW.md. The initial
candidate is preserved in PROOF_CANDIDATE.md to expose its earlier missing
justification. Exact pod algebra and a separately written rational verifier
check the conditional trace calculation and the self-Ext controls. They do
not certify holomorphic curve orientations. check_sign_convention.py checks
only the explicit parity formula.

The proof accepts the published small-family regularity and complete list of
contributions in Lemma4.17. It does not provide a formal proof-assistant
certificate or an independent analytic reconstruction of compactifications.
It claims no absolute sign, new Floer ranks, or integral surgery-cone theorem.
Priority checks are documented separately in ../PRIOR_ART.md.
