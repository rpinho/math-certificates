# Candidate and unrefereed: C30 >= 521/50

This is a written candidate proof, conditional on BBEP and the retained machinery of unrefereed Norton v3; it is not a novelty judgment or human refereeing. Arithmetic is checked by a separately written (same agent) exact Arb verifier. Credit: Bevan–Brignall–Elvey Price–Pantone (BBEP), arXiv:1711.10325 v3, supply the domino/arch construction, its enumeration and concentration, coefficientwise log-convexity, and the coefficient-extraction lemma. Norton v3, arXiv:2608.20292 v3, supplies the two-axis relaxation and Harris separation. Norton's withdrawn v2 supplies the marginal/kernel algebra and local algebraic setup (Proposition 5.2, equations (18)–(21), and Corollary 5.5). The needed untilted statements are re-derived here and checked against actual objects, rather than assumed to validate v2's withdrawn bound, tilt, or profile-concentration theorem.

All external sources were reopened and archived before mathematical work. BAR.json freezes the unrefereed 10.412263 baseline and minimum 521/50. No assertion about priority is made.

## 1. Published inputs and notation

A vertical domino consists of a 213-avoiding top cell and a 132-avoiding bottom cell with a common position axis, and itself avoids 1324. BBEP identify dominoes with two interleaved noncrossing arch systems. Arches connect consecutive increasing values of a cell. Concatenating two arch configurations gives another domino; it takes the skew sum in each cell. Rotating a domino by 180 degrees exchanges its cells.

Write D(z) for all dominoes counted by their total number n of points. BBEP's unmarked equation has the positive curve parameter

    z = w/(1+w)^3,       D = (1-w)(1+w)^3,
    rho = 4/27,          w0 = 1/2.

BBEP give D_n = 2(3n+3)!/((n+2)!(2n+3)!), with exponential growth 27/4. Their leaf and empty-strip concentration implies the following: for any a_- < 5/9 < a_+ and b_- < 5/27, the fraction of n-point dominoes having, in both cells, leaf counts between a_- n/2 and a_+ n/2 and empty-strip counts at least b_- n/2+2 tends to one. An additive constant in the thresholds does not change this consequence of their variance bounds. A leaf is a right-to-left maximum in a top cell and a left-to-right minimum in a bottom cell. Non-leaves cut a cell into strips along the value axis.

We use these published facts, the arch inverse construction, BBEP's coefficientwise log-convexity of H_j, and their finite-factor coefficient lemma. The relevant statements and their use in Norton v3 are audited in REFEREE.md. We do not assume any tilted ensemble or any concentration theorem for k-leaf strips from withdrawn v2.

## 2. An exact marginal strip generating function

For the top cell, read in increasing value order the binary word nu that places 0 at a leaf (a right-to-left maximum) and 1 at a non-leaf.

**Lemma 2.1 (value word of a terminal upper chain).** Let an arch prefix have no open upper arcs, and take its upper-point projection. Suppose its rightmost point is upper. If it is isolated, deleting it leaves a prefix B and

    nu = 0 nu(B).

Otherwise let t1,...,tm, m>=2, be the upper chain ending at that point, listed in position order. Let B0 be the subprefix before t1 and, for 1<=i<m, let Bi be the subprefix strictly between ti and t(i+1). These are the m ordered subobjects in BBEP's decomposition. Statements about a Bi's values refer only to its upper points. The chain has consecutive increasing upper-cell values; every upper point of every Bi is above every chain point; and every upper point of Bi is above every upper point of Bj whenever i<j. Consequently

    nu = 1^(m-1) 0 nu(B(m-1)) ... nu(B1) nu(B0).

Each subword uses the leaves of that subobject alone. If the rightmost point is lower instead, its removal, with the appropriate lower-arc update, leaves nu unchanged. Thus the lemma applies to all six recursive cases, including subprefixes with open lower arcs.

**Proof.** The exact source inputs are [BBEP v3, Proposition 3.2 and its proof, equation (1)](https://arxiv.org/html/1711.10325v3#S3.Thmtheorem2): an upper arc joins consecutive increasing values; the inverse map Pi_213 sends concatenation to skew sum; and it reconstructs the objects enclosed by a connected chain above that chain. The terminal decomposition into one initial subprefix and one per enclosed arc is [Proposition 3.4, proof, cases (v)–(vi), Figure 8](https://arxiv.org/html/1711.10325v3#S3.Thmtheorem4). Proposition 3.3 identifies these upper/lower configurations with dominoes. Here we spell out why these inverse-map rules give the claimed value order and preserve the leaf marks, which the unmarked generating-function equation alone would not establish.

First discard lower points and lower arcs when reconstructing the upper permutation. Its upper arch system is complete even if some lower arcs are open. The rightmost upper chain is a connected component. No upper arc can join two distinct intervening gaps without crossing a chain arc; an arc spanning the entire component would enclose its terminal point and end farther right, which is impossible. Nor can an additional arc enter a chain point, since each point has at most one incoming and one outgoing arc. The upper projection therefore has the stated initial and enclosed subobjects. The inverse in Proposition 3.2 reconstructs exactly its 213-avoiding upper permutation.

Along the chain, successive values differ by one. In particular no other upper value lies numerically between any successive pair, and the chain values form one interval. For a point x inside the gap between ti and t(i+1), x is either below both endpoints or above both. The former possibility would make the position-ordered triple (ti,x,t(i+1)) an occurrence of 213. Hence x is above both, and consecutiveness of the whole chain interval puts x above the entire chain. For two nonempty enclosed subobjects Bi,Bj with 1<=i<j<m, choose arbitrary upper points x in Bi and y in Bj. The chain point t(i+1) lies between them in position and below both in value. If x<y, the triple (x,t(i+1),y) is 213. Thus x>y, proving the reverse value order for every pair of enclosed subobjects, not just their extrema. The initial upper subobject B0 is separate from the chain component: noncrossing excludes an arc from B0 into a gap, since it would cross the chain arc over that gap. Concatenation becomes skew sum under Pi_213, so all its upper values exceed those of the entire terminal component, including the enclosed subobjects. Empty upper subobjects cause no exception to these comparisons.

Every chain point except tm has a larger chain point to its right and is a non-leaf. The terminal point tm is the rightmost upper point and is a leaf. For any upper point in Bi, all upper points outside Bi that lie to its right are smaller: they are later chain points or points in later subobjects. This also holds for B0 by skew sum. Such outside points cannot destroy a right-to-left maximum or create one where an internal larger point to the right already exists. Thus leaf status in each subobject agrees with its status in the whole prefix. Reading in increasing value order now encounters the chain first, giving 1^(m-1)0, and then the upper subobjects in order B(m-1),...,B0, with their unchanged internal subwords. This proves the chain formula.

An isolated terminal upper point is the last singleton component of a concatenation. Skew sum makes it smaller than all earlier upper values; it is a leaf, and its presence does not change their leaf status. Its zero therefore precedes nu(B) in value order. Finally, the four lower-point operations change neither the upper arch system nor its inverse upper permutation. They leave nu unchanged. Induction on the number of points, starting with the empty word, proves these rules at every recursive node. ∎

The local check `check_value_word.py --max-n 9` tests the lemma itself on every 213-avoiding upper cell of size at most 9, including every recursive subobject. It constructs arcs from consecutive values and compares the predicted word with right-to-left maxima measured directly on the permutation; it also checks the above-chain and pairwise reverse-order assertions. This covers every possible upper projection in that size range, independently of a choice of lower interleaving. It is a finite control, not the proof of the lemma.

Each maximal run of ones is consequently a nontrivial top chain, called a block here. A block owns the zero-run following it. If a later block occurs this is a closed strip; otherwise it is the terminal strip. The leading zero-run has no owner. Thus each top-cell j-leaf strip, j>=1, is counted by closed owned strips except for at most two boundary strips.

Let v mark open lower arches of an arch prefix with no open upper arch. Let A(z,v) count all such prefixes and put D=A(z,0). The six cases of BBEP's decomposition give

    A = 1 + z(2+v)A + z(1+v)(A-D)/v + g(A),
    g(x) = z^2 x^2/(1-zx).

This equation and each division by v below mean the formal difference quotient: A-D has zero constant term in v. All coefficientwise recurrences are well-defined, with nonnegative combinatorial coefficients.

Introduce u and four series. F counts words without a one, with u on each zero. S counts zeros before the first block, excluding words with no block. T counts a marked block whose strip extends to the end, with u on the additional zeros following its own zero. P counts a marked block owning a closed strip, with u^(j-1) on a j-leaf strip. Subscript 0 denotes evaluation at v=0. Define

    K0 = 1-z(1+v)-z(1+v)/v,       KA = K0-z,
    R = z^2(A+F-zAF)/((1-zA)(1-zF)),
    Y = g'(A),
    V = S z^2/((1-zA)^2(1-zF)).

The four exact equations are

    (K0-uz)F = 1 - z(1+v)F0/v,
    (K0-uz)S = g(A) - z(1+v)S0/v,
    (KA-R)T = g(F) - z(1+v)T0/v,
    (KA-Y)P = S R + T V - z(1+v)P0/v.                 (M)

Here is a counting derivation, including the joint roles of the subobjects. Lower-point cases contribute z(1+v) and the difference quotient; an isolated top point contributes z, or uz when it extends the particular zero-run being recorded. A top block has an ordered list of m>=2 subobjects, with weight z^m. For F the block is excluded. For S its own word starts with a one, and all subobjects are unrestricted, giving g(A). For a marked terminal strip, either the root block is marked and all its subobjects are F, giving g(F), or the marked block is in one subobject and every later subobject is F. Summing the free objects before and F objects after gives

    R = sum_{m>=2} z^m sum_{a+b=m-1} A^a F^b.

For a closed marked strip there are exactly three disjoint possibilities: the root block owns it and its first later block arrives in an S subobject (source SR); it is already closed inside a marked subobject (propagation YP); or it is terminal within its marked subobject and a later subobject closes it (source TV). Pointing at a free subobject gives Y; summing the last case gives V=S(Y-R)/(A-F), equal to the displayed expression after cancellation. This proves (M), with the isolated-point and lower-point contributions already accounted for. No independent-neighbour pairing or averaging over strip order is used.

Every right-hand-side combinatorial recurrence raises z-degree. Thus these equations specify the series uniquely by induction. Their exact coefficients, including all u coefficients of P0, agree through n=14 with actual value cuts of every 1324-avoider of those sizes: 1,209,639,642 avoiders and 1,390,594,458 valid gridded domino encodings at n=14. This finite check is a control; the preceding decomposition is the all-size argument.

## 3. Local evaluation of the first moment

The F/S kernel has the smaller root v1=z+O(z^2) of

    z v1^2 - (1-z(2+u))v1 + z = 0.

Let v1' be the other root, and let r=z+O(z^2) be the formal root of KA-R=0. Kernel cancellation in (M) gives

    F = 1/[z(1+v1)(v1'-v)],
    F0 = v1/[z(1+v1)],
    S0 = v1 g(A(z,v1))/[z(1+v1)],
    T0 = r g(F(u,z,r))/[z(1+r)],
    P0 = w [S(u,z,w)R(u,z,w)+T(u,z,w)V(u,z,w)]/[z(1+w)].       (K)

In the last equation z=w/(1+w)^3 and A(z,w)=(1+w)^2, which make KA-Y=0. Substitution is legitimate first as formal series at z=0 and then for real 0<z<rho. Marked counts are bounded by n times unmarked counts, so the needed series converge inside rho.

For completeness the analytic branch of r at the critical point is certified without assuming v2's complex-circle or profile-concentration claims. Set

    vmax = rho(1+16 rho) = 364/729 < 1/2,
    CA = A(rho,vmax),       CF = F(1,rho,vmax),
    CR = (CA+CF-rho CA CF)/((1-rho CA)(1-rho CF)).

There is no factor rho^2 in CR. Nonnegative coefficients imply |R|<=CR |z|^2 on |z|<=rho, |u|<=1, |v|<=vmax. These series are finite there: the physical unmarked branch has critical discriminant

    Delta(v,rho,D(rho)) = (2v-9)(2v-1)^3/729,

so A(rho,v) is analytic for |v|<1/2, with the quadratic-coefficient zero removable. Along the positive curve the remaining discriminant factor is positive for 0<=w<1/2 and 0<=v<=1/2. Indeed it decreases in v there, and its value at v=1/2 is

    (1+w)^2(2w-1)(2w^3-9w^2+4w-4)/4 > 0.

At a zero of the quadratic coefficient, z=v/(1+v)^2, the physical branch has already crossed w=v and the linear coefficient is z^2(1+v)D>0, so this is the finite, removable branch. This also shows there is no earlier positive singularity for these v; nonnegative coefficients then give the asserted absolute convergence and complex modulus bounds. F is dominated by A at |u|<=1 and has the displayed explicit form.

For chi(v)=v(KA-R), compare with v-z on |v-z|=16|z|^2. One has

    |chi(v)-(v-z)| <= |z|^2(1+16|z|)
                         [3+|z|(1+16|z|)+CR|z|].

At |z|=rho the bracketed expression including its prefactor is certified below 15.270542<16. Both 1-rho CA and 1-rho CF are positive. The bound is monotone in |z|. Rouché therefore selects a unique simple root in the disc for every 0<|z|<=rho; at z=0 it is the formal root r=z+O(z^2). This is a v-disc argument at each z, not an assertion that a positive z-series converges beyond its radius.

At (w,u)=(1/2,0), the exact certificate isolates

    r = 0.38944473029025026068...,
    partial_v(KA-R) = 0.7358159158... > 0.

All square roots and denominators in (K) are locally analytic with nonzero denominators, as certified by the verifier. In particular A is evaluated in the stable form -2P0/(P1+sqrt(Delta)); the alternate quadratic formula has a removable 0/0 at v1 when u=0. The implicit function theorem makes r analytic in (w,u) near this critical point. No continuation round |z|=rho is needed below.

Write p(w,u) for P0 after this substitution. Since z'(w0)=D'(w0)=0, auxiliary quantities depending only on z,D,u have zero w derivative there, also after differentiating in u. At the kernel point itself A=(1+w)^2. Hence the four-coefficient jet computation in verify_mean_two_leaf.py gives exactly the mixed derivative p_wu. Its certified enclosure implies

    mu2 := (4/27) p_wu(w0,0)
        = 0.06627960057204584443150090889068205402... < 1/10.    (C)

The certificate contains rational root endpoints; sign checks isolate the root, its derivative is bounded away from zero, and all evaluations use outward-rounded Arb balls. There is no floating differentiation in this verification.

## 4. A first-moment family, with no strip-concentration hypothesis

Let N2(D) be the total number of two-leaf strips in both cells, including boundary strips. Put M(z)=sum_D N2(D) z^|D|. By rotation symmetry and the two boundary exceptions per cell,

    M(z) = 2 [u]P0(z,u) + E(z),       0 <= E_n <= 4 D_n.

Set epsilon=rho-z. The explicit unmarked curve gives

    epsilon = (16/81)(w-w0)^2 + O((w-w0)^3),
    D(z) = D(rho) - a epsilon + (2187/16)epsilon^(3/2)
                                      + O(epsilon^2).

These are local real expansions of algebraic functions. They may be differentiated on the real branch. Analyticity of p(w,u) near (w0,0) gives the leading square-root term of [u]P0. Since D'(rho) is finite, the bound on E_n makes E'(rho) finite. It follows, by differentiating these local expansions, that

    lim_{z increasing to rho} z M'(z)/(z^2 D''(z)) = mu2.       (L)

The factor is exactly 4/27 because 3*rho*(2187/16)*(4/9)=27. Notice that (L) is a ratio of positive generating-function derivatives. It needs no coefficient asymptotics for the marked strip series, no Delta-domain beyond rho, and no second moment of N2.

Take s2=1/10. If a domino has N2>s2 n, then n(n-1)<=n N2/s2. Therefore the total n(n-1)-weighted generating function of these bad dominoes is at most z M'(z)/s2. The bad leaf/empty-strip events of Section 1 have coefficient counts o(D_n); their n(n-1)-weighted generating function is o(z^2 D''(z)). To see the last assertion, bound their fraction by any fixed eta for all sufficiently large n; the finite initial part is bounded, while D''(z) diverges at rho, and then let eta decrease to zero.

Let G count dominoes satisfying N2<=s2 n and the leaf/empty events with

    a_- = 5555552/10^7,       a_+ = 555556/10^6,
    b_- = 1851851/10^7.

The strict inequalities a_-<5/9<a_+ and b_-<5/27 hold. From (L),

    liminf G''(z)/D''(z) >= 1-mu2/s2 > 0.

Consequently G'' diverges at rho. Since G<=D coefficientwise, G has radius exactly rho. Thus along an infinite sequence of sizes m, G_m=(27/4)^(m-o(m)). Only this limsup assertion is needed.

For each such m, pigeonhole the top cell size, both leaf counts, both empty-strip counts, and both two-leaf-strip counts. There are at most (m+1)^7 classes, so one class L_m has the same exponential size. Concatenate the arch configurations of any sigma in L_m and the 180-degree rotation of any tau in L_m. BBEP's injection recovers the inputs by splitting at their common total length m, and produces a balanced domino with m points in each cell. The leaves add. In each cell just one boundary strip is merged; empty strips decrease by at most one and the two-leaf-strip count increases by at most two. Because both input cell statistics were fixed in L_m, each output cell consequently has

    leaves between a_- m and a_+ m,
    empty strips at least b_- m-1,
    two-leaf strips at most s2 m+2.

The family B_m so obtained satisfies |B_m|>=(27/4)^(2m-o(m)) along the same subsequence. This is the published physical arch-concatenation injection, not a pairing of independently counted neighbours of one connecting cell.

## 5. A common finite strip envelope

Fix

    alpha=555555/10^6,       beta=185185/10^6,       c2=7/50.

For each cell in B_m, restrict surplus leaves until exactly L=ceil(alpha m) points remain free. Every restricted leaf splits its old strip into two; it cannot decrease the number of empty strips and can create at most two two-leaf strips. For sufficiently large m, the resulting ordered pattern therefore has

    r=m-L+1 strips,     n0>=B=ceil(beta m)+1,
    n2<=U=floor(c2 m),   total free points L,

since s2+2(a_+-alpha)=0.100002<c2 and b_->beta. Imposing these extra conditions only reduces the available placements.

Here is the envelope lemma, including its integer issue. Let y be any r-vector of nonnegative integer strip sizes with sum L, at least B zeroes and at most U entries equal to two. Choose e2 from {U,U-1} so that L-r+B-e2 is even, and set

    e0=B,
    e1=[3(r-B)-L-e2]/2,
    e3=[L-r+B-e2]/2.

In the present application these are nonnegative integers for all sufficiently large m (indeed the linear lower estimate e1>0.0411125*m-3.5 suffices). Let x have e_j entries equal to j for j=0,1,2,3. Then x is majorized by y.

Proof: their lengths and sums agree. At threshold one the excess sum for y is L-r+n0, at least L-r+B, the value for x. At threshold two it is L-2r+2n0+n1. With T=sum_{j>=4}(j-3)n_j>=0, the count identities give

    2(2n0+n1)=3r-L+n0-n2+T >= 3r-L+B-U.

The left half is an integer. Taking its ceiling if necessary gives at least (3r-L+B-e2)/2=2B+e1, the value required for x. At threshold zero the excess sums agree; at thresholds at least three x has no excess. Between integers the excess sums are linear. These inequalities characterize majorization. The choice U-1 exactly handles the odd case, so there is no fractional strip count. This proves the lemma.

By BBEP's strong coefficientwise log-convexity, transferring one unit from a larger part to a smaller part cannot increase the product of the corresponding H_j. An integer majorization is a finite sequence of such transfers. Hence coefficientwise in z and q,

    product_i H_{y_i} >= H0^e0 H1^e1 H2^e2 H3^e3.             (E)

All tested finite integer controls of this envelope are recorded in artifacts/profile_envelope_controls.json; the preceding argument proves it for every size. Write eta_j for the limiting envelope coordinates. The normalized exponents tend to

    eta0=37037/200000,    eta1=3289/80000,
    eta2=7/50,           eta3=31259/400000.

Here eta2=c2 is the synthetic envelope coordinate, mu2 is the actual density in (C), and s2=1/10 is the family-selection threshold. These are three distinct quantities. The envelope has sum eta_j=1-alpha and sum j eta_j=alpha. It preserves the complete ordered-placement count as a lower bound; it does not assume that the joint count is determined by an unordered profile.

## 6. Transfer to 1324 avoidance and the exact numerical point

Use B_m for the vertical dominoes and its reflected family for the horizontal ones in the period-six staircase. Their non-leaves obey Norton's v3 two-axis gap rule. Every 1324 lies in two adjacent cells, so this constructs 1324-avoiders. A gridded output recovers every domino, connecting cell, and row/column interleaving, so the choices are counted injectively as gridded permutations. Each row and column meets only two consecutive staircase cells; specifying its shuffle introduces no further consistency choice. For a connecting cell with c_m components, fixed total size is **not** imposed. The v3 Harris argument gives its true shared-neighbour count at a fixed z at least the product of the two one-sided sums divided by Q(z)^c_m, where Q=(1-sqrt(1-4z))/2. Equation (E) gives the same one-sided lower function on every adjacency.

Define

    J_m(z)=[q^c_m] product_{j=0}^3 H_j(z,q)^e_j(m),
    H_j = (d/dz)^j[z^j/(1-qQ(z))]/j!.

BBEP's finite-factor coefficient lemma provides a sequence c_m/m->kappa with

    J_m(z)^(1/m) -> exp(Lambda),
    Lambda=min_q[-kappa log q+sum_j eta_j log H_j(z,q)].

All four limiting eta_j are positive; the q-series are nonnegative and aperiodic, and the verifier brackets the saddle strictly inside q<1/Q(z). The lemma is applied to this common finite envelope, not to an unknown actual limiting profile. Its component-count sequence is defined for all sufficiently large m and can therefore be restricted to the subsequence on which B_m has full exponential size.

For fixed k, the staircase through 6k+2 cells has a subfamily whose GF value dominates

    |B_m|^(2k+1) z^((4k+2)m) J_m(z)^(4k) Q(z)^(-2k c_m).

As in v3, a positive

    Phi=2 log(27z/4)+2 Lambda-kappa log Q(z)

makes the m-root exceed one for sufficiently large fixed k along the subsequence. If the ungridded avoidance GF converged strictly inside a larger radius, the fixed finite grid's GF would converge there too: the number of possible row/column divisions of an n-point permutation is polynomial in n. It would uniformly bound every such subfamily value, contradicting that exponential divergence. Therefore the avoidance GF radius is at most z. The use of a limsup subsequence for B_m suffices for this contradiction.

Take the exact rational point

    z=50/521,           kappa=515801757591/10^12,
    q1=1, q2=9,        q0=3049509956240/10^12.

The bracket is convex in log(q). Its derivative in that variable is negative at q1 and positive at q2; both are inside its convergence radius. A tangent at q0 bounds its global minimum below. verify_candidate.py, using the frozen certificate and the separately verified first moment, proves

    Phi > 0.00018309709357909 > 0.

It checks every rational threshold, all profile identities, root isolation and Rouché selection, the positive saddle bracket, and the tangent error with outward-rounded Arb arithmetic. Since 1/z=521/50 exactly, the conclusion is

    C30 >= 521/50 = 10.42.

This is a **candidate, unrefereed** bound, conditional on BBEP and the retained two-axis/Harris machinery of Norton v3. The Phi margin is about 1.8e-4; the review's numerical break-even estimate for this profile is about 10.4207, not an additional certified bound. The separately written (same agent) verifier confirms the stated exact arithmetic, while this document supplies the combinatorial and analytic proof. Rejection controls and frozen artifact hashes accompany it. No matrix certificate is claimed; this is method 2's generating-function route. No heavy search or scaled pod phase was needed.

Primary sources: [BBEP v3](https://arxiv.org/html/1711.10325v3), [Norton v3](https://arxiv.org/html/2608.20292v3), and [withdrawn Norton v2](https://arxiv.org/html/2608.20292v2). Their downloaded snapshots and hashes are retained locally; the withdrawn source is credited for the marginal equations, not used as a verified asymptotic-profile theorem.
