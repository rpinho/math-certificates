# J012: few downward weight defects imply a linear path bound

Candidate theorem for independent referee review, 2026-11-03. No novelty or taste verdict is asserted here. Arithmetic certificates accompany this proof; they do not replace the universal argument.

## Statement and comparison

Consider the same problem as Bento–Furmaniak–Ray (2018), Eq.(2):

    min_x  (1/2) Σ_(j=1)^n (x_j-y_j)² + λ Σ_(i=1)^(n-1) α_i |x_(i+1)-x_i|,

with n≥2, every α_i>0, arbitrary y∈R^n and λ≥0. Count T as the number of maximal affine pieces of the entire solution path, including the final constant piece. Set a_0=a_n=0 and a_i=α_i for 1≤i<n. Let H be the least concave majorant of the points (i,a_i). Let

    k = #{i∈{1,...,n-1}: a_i < H(i)},     g = n+1-k.

Then

    T ≤ min{ 3^k (g-1),  1 + 8[2g-3 + gk + k(k-1)/2] }.                 (A)

In particular T=O(n(k+1)); if k is bounded independently of n, T=O(n) for every y. For k=0 the first bound recovers T≤n. For k=1 it gives T≤3(n-1). The constant 8 is inherited from the endpoint-pair argument of the source paper, not optimized here.

A directly usable sufficient condition: start from any positive concave edge-weight profile padded by zeros, and decrease at most k edge weights, retaining positivity. Bound (A) applies with at most k exceptions. This permits actual unfusions, unlike diagonal dominance. It is a sufficient family, not an if-and-only-if characterization of all linear-complexity profiles.

Published comparison: the unrestricted weighted problem has tight quadratic order (Bento–Furmaniak–Ray, Thms3–4). The equal-weight case has T≤n. Padded concavity alone already follows from Tibshirani–Taylor's diagonal-dominance condition and is not claimed as a result of this work. The claimed refinement concerns nonconcave weights with a bounded number of downward defects; it does not alter the unrestricted quadratic bound or prove a running-time improvement.

## 1. Taut-string coordinates and contact signs

Use c_0=0, c_i=Σ_(j=1)^i y_j. Up to the constant shift/reversal used in the source's Theorem1, its equivalent strictly convex problem is

    minimize_z (1/2) Σ_(j=1)^n (z_j-z_(j-1))²
    subject to z_0=0, z_n=c_n, |z_i-c_i|≤λ a_i (0<i<n).

The primal solution is x_j=z_j-z_(j-1). The transformation is injective after fixing z_0, so its maximal affine pieces coincide with those of x. At an upper contact z_i=c_i+λa_i set s_i=+1, at a lower contact set s_i=-1. Let B contain all contacts and the two fixed endpoints. If l<r are consecutive contacts, the free points between them satisfy

    z_i = [(r-i)z_l+(i-l)z_r]/(r-l).                                  (1)

This follows by the unconstrained quadratic first-order equations inside the gap. On an interval where contacts and signs are fixed, (1) makes the full solution affine in λ. The source paper supplies the same representation and proves that the path is continuous and has finitely many affine pieces. Alternatively, finite signed-face enumeration proves finiteness here directly: for each of 3^(n-1) contact/free states, (1) and the linear KKT inequalities describe an interval of λ.

## 2. Envelope contacts never return after becoming free

A padded weight index i belongs to G={i:a_i=H(i)} if and only if

    (r-l)a_i ≥ (r-i)a_l + (i-l)a_r          for all l<i<r.              (2)

For completeness, H(i) is the maximum of a_i and all chords through points to either side of i: maximize Σ p_j a_j subject to p≥0, Σp=1, Σj p_j=i. A maximizer has support on at most two points, by the two equality constraints. This is the upper boundary of the convex hull, hence the least concave majorant. Thus (2) is exactly the contact test.

Suppose i∈G is free. On any affine subinterval while it remains free, let l,r be its nearest contacts. Differentiating (1),

    z'_i = [(r-i)s_l a_l+(i-l)s_r a_r]/(r-l),
    |z'_i| ≤ [(r-i)a_l+(i-l)a_r]/(r-l) ≤ a_i.                          (3)

The endpoint slopes are zero at 0,n. Both distances to the box boundaries,

    (c_i+λa_i)-z_i,        z_i-(c_i-λa_i),

are therefore nondecreasing while i is free. Starting strictly positive, they cannot reach zero. The finitely many changes of l,r do not affect this conclusion, by continuity. A good index can leave B at most once and never re-enter. Its sign cannot switch while in B for λ>0. The active subset of G consequently only shrinks, and changes at most g-2 times. This argument holds with ties and collinear weights; it needs no genericity.

For a concave profile h lowered on at most k indices, every unchanged i satisfies a_i=h_i≥any chord of h≥the corresponding chord of a. Therefore all unchanged indices are in G and the actual number of exceptions is at most k. This also shows why an upward spike is not covered by simply counting modified entries.

## 3. Independent face-count bound, valid directly with degeneracies

The at most g-2 departures of good contacts partition λ>0 into at most g-1 open phases in which all good statuses and signs are fixed. On a phase, each of the k exceptional coordinates has one of three statuses: free, upper contact or lower contact. There are at most 3^k full patterns.

For any one pattern, (1) fixes a unique affine candidate z(λ). Its validity is expressed by box inequalities at free coordinates and the signed quadratic-gradient inequalities at contacts. All are linear inequalities in λ. Requiring the free inequalities to be strict still gives an interval. Thus one exact pattern cannot occur on two separated subintervals of a phase. Each phase contains at most 3^k affine pieces. Adding over the phases gives

    T ≤ 3^k(g-1).

Isolated status ties cannot add an affine piece, by continuity. This bound does not rely on the endpoint-pair counting lemma or on a generic perturbation.

## 4. Amortized endpoint pairs give the polynomial bound

First take generic weights/data, so events are single contact changes and none of the chord/boundary affine equations used below is an identity. For an event at interior index j, let l<j<r be its two neighboring contacts on the side of the event where j is free. Charge the event to (l,r).

Fix (l,r) and endpoint signs (s_l,s_r). The interpolating line (1) fits within every interior box exactly when λ belongs to an intersection of one-dimensional halfspaces, hence one closed interval I_(l,r,s_l,s_r), possibly empty, unbounded or a singleton. At a charged event, at least one interior box inequality is tight. By genericity it is a nonconstant equality, so the event is an endpoint of I. There are at most two such finite values per sign pair and at most four sign pairs. Therefore each endpoint pair receives at most eight distinct critical values. This is the same argument as Bento–Furmaniak–Ray's Theorem3, restricted here to endpoint pairs that can actually arise.

Count the pairs that can arise over the entire path:

1. Both endpoints in G: they must be consecutive in the current ordered active G-set. Initially there are g-1 adjacent G-pairs. Deleting one internal G element creates at most one additional adjacent pair. No G element returns. Thus at most (g-1)+(g-2)=2g-3 such pairs ever occur.
2. One endpoint in G and the other in its complement: at most gk pairs, without needing any assumption on the exceptional statuses.
3. Both endpoints exceptional: at most k(k-1)/2 pairs.

Writing P=2g-3+gk+k(k-1)/2, there are at most 8P critical values and hence T≤1+8P.

Since g≤n+1 and k≤n-1, P=O(n(k+1)). More explicitly, substituting g=n+1-k gives

    P = (k+2)n - 1 - (k²+3k)/2.

Together with §3 this proves (A) in the generic case.

## 5. Removing genericity without enlarging the exceptional set

This step is needed for the polynomial bound only. Keep the original certified good set G fixed. Perturb the padded weights by

    a_i^(ε)=a_i+ε i(n-i),  ε>0.

For every original good i and every l<i<r, the chord-dominance slack increases by exactly

    ε (r-l)(i-l)(r-i) > 0.                                            (4)

For fixed n there are finitely many inequalities. Sufficiently small further perturbations of internal weights preserve all of them and preserve positivity. We may therefore choose weights and data outside the finite exceptional algebraic sets for event ties/affine identities, converging to the original instance, while every member of the original G remains good. The argument in §4 used only a certified good set, not its maximality, so the same value P bounds every approximant.

The minimizer converges on every compact λ interval: strong convexity, bounded minimizers and continuously varying objectives imply pointwise convergence; the subgradient bound for the positively weighted total variation gives a common Lipschitz bound in λ and hence uniform convergence. A uniform limit of continuous piecewise-affine functions with at most M pieces on a compact interval has at most M pieces. To see this, take a subsequence along which all M-1 ordered breakpoints converge (allow zero-length pieces). On every open interval between their limits, the approximants, and hence their limit, are affine. If the original full path had more than M pieces, finitely many of those knots would lie in one compact interval, a contradiction. This proves T≤1+8P for all weights/data covered by the statement.

## 6. Nontrivial control and verification scope

The source Fig.1 profile a=(0,1/50,1/2,1/2,0) has exactly one deficit, i=1. It violates 2a_1≥a_0+a_2 and has an exactly verified unfusion at λ=25/23. Thus this family includes paths outside the known no-unfusion condition. Bound (A) gives T≤9 at n=4; the exact path has T=5. The example is a control demonstrating genuine inclusion, not a new numerical record.

The separate verifier verify_paths.py checks primal subgradient KKT identities and inequalities over complete rational λ intervals, including infinity, continuity, coverage and actual slope changes. verify_panel.py independently tests hull membership by all rational chords, checks good-contact monotonicity and (A) on the finite diagnostic panel. verify_theorem.py checks the exact symbolic slack identity (4), count formulas, and exhaustive finite monotone-deletion pair accounting. Those computations certify their stated arithmetic/combinatorial checks; the universal all-n theorem rests on the written proof above and its cited standard convex facts, not extrapolation of finite tests and not a Lean/Isabelle formalization.
