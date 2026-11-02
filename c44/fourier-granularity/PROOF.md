# Fourier granularity constraints for C44 (unrefereed)

All functions below have **real multilinear degree**, not algebraic degree over
F2. All Fourier expectations use the uniform measure. The finite certificates
and the exact final rational are in the accompanying verification outputs.
This is a written mathematical proof, not a proof-assistant formalization.

**Final result, 2026-10-30:** the exact row checker proves

    C44 <= 163310332697516761417555720251
           /39614081257132168796771975168
        < 4.1225323803 < 4.1225332506.

The standalone column checker proves the same printed claim at horizon72.
The final specification is `candidate.json`; its hash fixes the exact
`spectral_certificate_round3.json` bytes (37 accepted duals, degrees4 through40).
Degrees31–40 improve on the frozen round-two inputs; degrees4–30 are unchanged. Every proof step needed for this
checkpoint is below, with inherited cap proofs in `baseline/PROOF.md`.

## 1. Granularity and a necessary inequality

Let g:{0,1}^n -> {-1,1} have real degree at most d, with d>=1. Write
g(x)=sum_S a_S chi_S(x), chi_S(x)=(-1)^(sum_{i in S}x_i).
Every a_S is an integer multiple of delta=2^(1-d).

Proof: h=(1-g)/2 is {0,1}-valued and has degree at most d. Its multilinear
polynomial in the bits x_i has integer coefficients: the coefficient on T is
sum_{U subset T}(-1)^(|T|-|U|)h(1_U), with other bits fixed to zero.
Substitute x_i=(1-y_i)/2 and expand g=1-2h. Each Fourier coefficient is an
integer sum of terms with denominators dividing2^(d-1); the constant1 has the
same property. This proves granularity. The argument also applies when the
actual degree is less than d.

Put A_l=sum_{|S|=l}a_S, and a=A_0. Parseval gives sum_S a_S^2=1. For every
nonzero a_S, a_S^2 >= delta |a_S|. Consequently

    sum_{l=1}^d |A_l|
      <= sum_{S nonempty}|a_S|
      <= M(1-a^2),                 M=2^(d-1).                 (1)

The familiar weaker consequence is sum_S|a_S|<=M. Granularity and this Fourier
L1 estimate are standard; the present computation adds their constraints to
the block-sensitivity relaxation. We do not claim these general facts are new.

## 2. Compression and symmetrization preserve the needed information

Suppose a Boolean function f of degree at most d has at least n disjoint
sensitive blocks at some input z. Retain n such blocks. Fix every other
coordinate to its value at z, and replace all coordinates of block j by either
z_i or1-z_i according to a single new bit y_j (equivalently z_i XOR y_j).
Compose the output with a sign so that the resulting sign function g satisfies

    g(0)=1,          g(e_j)=-1 for all j=1,...,n.

The substitution does not raise degree: a monomial may repeat a y_j, but on
the Boolean cube y_j^r=y_j for r>=1, so multilinear reduction only lowers its
degree. Thus g has degree at most d. This argument works for **at least n**
blocks, not just exactly n; an exclusion on n bits proves bs(f)<=n-1.

Average g over permutations of its n coordinates. Denote its value on a
weight-k input by q(k). Then q(0)=1, q(1)=-1 and -1<=q(k)<=1 for0<=k<=n.
For a fixed set S of size l, the average of chi_S on the weight-k slice is

    Q_l(k) = K_l(k)/binom(n,l),
    K_l(k) = sum_j (-1)^j binom(k,j) binom(n-k,l-j).          (2)

To see (2), count l-subsets whose intersection with a fixed weight-k set has
size j. Averaging the Fourier expansion therefore gives

    q(k)=sum_{l=0}^d A_l Q_l(k).                            (3)

The A_l are the sums of the original Fourier coefficients, so they satisfy
(1). We do not apply Boolean granularity to the coefficients of the averaged
function individually; averaging can destroy that property.

## 3. A finite rational certificate criterion

Choose rational numbers alpha_0,...,alpha_n, most of which may be zero. Define

    c_l = sum_{k=0}^n alpha_k Q_l(k),
    L   = alpha_0-alpha_1-sum_{k=2}^n |alpha_k|.

If

    |c_l|<=1 for1<=l<=d,
    L > M + c_0^2/(4M),                  M=2^(d-1),         (4)

then no sign Boolean g as in section2 exists, and every degree-at-most-d
Boolean f has bs(f)<=n-1.

Proof: the prescribed values q(0)=1,q(1)=-1 and the range of all other q(k)
give L <= sum_k alpha_k q(k). By (3), the latter equals sum_l c_l A_l. By (1)
and the bounds in (4),

    sum_l c_l A_l
      <= c_0 a + sum_{l>=1}|A_l|
      <= c_0 a + M(1-a^2)
       = M+c_0^2/(4M)-M(a-c_0/(2M))^2
      <= M+c_0^2/(4M).

This contradicts the strict inequality in (4). Every statement is a finite
rational equality or inequality except the elementary completed square.
There is no assumed existence of an optimizer, no floating-point premise,
no endpoint condition q(n)=+/-1, and no branch-enumeration completeness claim.

The retained `spectral_certificate_round3.json` records d,n and the nonzero alpha_k.
The final packet strengthens the criterion as follows. The independent
checker `verify_spectral.py` computes (2) by polynomial multiplication, checks
every c_l, and checks the strict gap in (4). A second checker uses the
Krawtchouk three-term recurrence; neither imports search code.

For a short hand-checkable example, take d=4,n=10 and

    (alpha_0,alpha_1,alpha_2,alpha_8,alpha_10)
        =(265,-880,795,15,-3)/32,

with every other alpha zero. Direct substitution in (2) gives
(c_0,c_1,c_2,c_3,c_4)=(6,1,-1,-1,1). Here L=83/8, whereas
M+c_0^2/(4M)=8+36/32=73/8. The gap is5/4, proving B4<=9.
This reproduces the exclusion asserted by the C37 PR283 lead with a different
short certificate; it is not claimed as the first proof of that exclusion.

### 3.1. Exact lattice strengthening used by the final packet

For rational c let h(c)=max_{z in Z}(cz-z^2). Completing the square shows
that a maximizing integer is either floor(c/2) or floor(c/2)+1, so this
maximum requires only two exact rational evaluations. In particular
h(c)=0 for |c|<=1, and h(c)<=c^2/4 for every real c.

Write each original Boolean Fourier coefficient as a_S=z_S/M with z_S
integer, using section1. Parseval now gives, for arbitrary c_0,...,c_d,

    sum_l c_l A_l
      = M + sum_{|S|<=d}(c_{|S|} a_S - M a_S^2)
      = M + (1/M)sum_{|S|<=d}(c_{|S|} z_S - z_S^2)
      <= M + (1/M)sum_{l=0}^d binom(n,l) h(c_l).          (4a)

Zero coefficients are included; h is nonnegative since z=0 is admissible.
No granularity is imposed on the averaged function. Thus if a rational
slice functional has the same c_l and lower bound L as above and satisfies

    L > M + (1/M)sum_{l=0}^d binom(n,l) h(c_l),           (4b)

it contradicts (4a), proving B_d<=n-1. This criterion has no separate norm
constraints on c_l: all of them are handled by the finite lattice penalty.
It contains (4), because its nonconstant penalties vanish when |c_l|<=1
and h(c_0)<=c_0^2/4.

Every final dual in `spectral_certificate_round3.json` uses (4b).
The exact checkers reconstruct all c_l and the full penalty independently,
including any small high-level rounding deviations. The LP and its cutting
planes serve only to discover rational alpha_k. Their optimality, solver
status and termination never enter this proof. The optional derivations in
LEVEL_PROOF.md and LATTICE_PROOF.md are retained, but (4a)–(4b) above are the
complete additional universal argument needed by the final result.

## 4. The inherited local-degree potential and recurrence

Use a sign representation for a Boolean function f. Let d_i(f) be the largest
Fourier monomial degree containing relevant i, and

    D(f)=sum_{i relevant}2^(-d_i(f)).

For a nonzero multilinear polynomial P of degree at most k, its support has
uniform density at least2^(-k). Induct on k: write P=x_j R+T with nonzero R of
degree at most k-1. Where R is nonzero, at least one of the two x_j branches is
nonzero, proving the claim from the induction hypothesis. Constants are the
base case. Apply this to the ternary derivative (f_{i=1}-f_{i=-1})/2 to obtain
Inf_i(f)>=2^(1-d_i), hence D(f)<=I(f)/2<=deg(f)/2 by Parseval.

For an unrestricted coordinate i and a restricted coordinate j!=i, its
expected restricted weight is at least its original weight. If i survives
both branches, both local degrees are at most d_i(f). If i survives exactly
one, its derivative factors as (1+/-x_j)/2 times that branch derivative, so
its original local degree is exactly one larger. These facts prove the
single-coordinate assertion. Iterating it for each i outside a fixed set H
and then summing proves

    D(f)<=sum_{i in H relevant}2^(-d_i(f)) + E_alpha D(f_alpha).  (5)

Choose H to be a maximum-degree monomial of size d. Its cost in (5) is d/2^d.
For every assignment outside H, the function on H remains nonconstant: its
full-degree coefficient cannot change. For every restriction alpha to H,
choose outside H an input attaining bs(f_alpha). The sensitive blocks there
remain sensitive blocks of f at the combined input. Since the function on H
is nonconstant, there is in addition some nonempty block inside H that flips
the output from this input. The blocks are disjoint, proving

    bs(f_alpha)<=bs(f)-1.                                  (6)

For valid degree-specific upper bounds B_d and local caps c_d, define

    U(0,d)=0,
    U(b,d)=min(c_d, d/2^d + max_{1<=k<=d} U(b-1,k)), b>=1,
    U(b,d)=U(B_d,d) when b>B_d.

Induction on b using (5),(6) proves that U(b,d) bounds D for every function of
degree exactly d with bs<=b. Constants contribute zero. Freezing above B_d is
valid because the class of actual functions is unchanged beyond that bound.
The numerical programs check all lower-degree columns, not just the top one.

## 5. Other inputs, their proofs and scope

The unchanged degree1..48 certificates from BakeLab/Épi have SHA256
ce66f1097a7284e9845113fa1dc39267932cc934fd23d9019ff13d3dcb39cf49.
They use the standard symmetrized {0,1} polynomial p on m compressed blocks,
with p(0)=0,p(1)=1 and0<=p(k)<=1. Their d+1 positive integer nodes x_i and
rational weights w_i satisfy

    sum_i w_i x_i^j=0 (j=1,...,d),
    x_0=1, w_0>0, w_0+sum_{i>=1,w_i<0}w_i>0.

The first identities annihilate every such polynomial (its constant is zero).
The second line forces sum_i w_i p(x_i)>0, a contradiction, so B_d<=max x_i-1.
One checker verifies each power moment; another uses the equivalent common
Lagrange residue w_i x_i prod_{j!=i}(x_i-x_j). No numerical dual is trusted.

External theorem: Wellens, Discrete Analysis2022:20, Theorem4.1, gives
3b(b-1)<=2(d^4-d^2). We intersect its largest allowable integer b with the
Épi bounds and section3 certificates. In particular it implies b<=d^2:
substitution of b>=d^2+1 violates the inequality. This external theorem is
cited, not independently reproved here.

The certified recurrence may also use the already audited local caps
c3=5/4,c4=31/16,c7=447/128. Their complete proofs are retained verbatim in
`baseline/PROOF.md`, sections1–8. The c3 proof uses the published theorem
R3<=10 (Tarannikov–Kirienko, as stated in Krotov–Valyuzhenich2311.05566v2).
The other two caps use the elementary strict influence equality exclusion.
All remaining c_d=d/2. The specification fixes these caps; an arbitrary
user-supplied cap is never accepted by the exact verifier. Reported ablations
show whether these inputs remain active after the block improvements.

## 6. Infinite tail and passage to C44

Fix a horizon H. At degree e>H, keep restricting maximum-degree monomials
until the degree drops. Each restriction costs e/2^e by (5) and lowers block
sensitivity by at least one by (6). There can be at most e^2 such restrictions
along any branch because bs<=e^2. Therefore the maximum potential among
degree-at-most-e functions is at most its degree-at-most-(e-1) counterpart
plus e^3/2^e. Iterating gives the universal bound

    D(f)<=max_{1<=d<=H}U(B_d,d)+sum_{e>H} e^3/2^e.

The infinite series is exactly

    (H^3+6H^2+18H+26)/2^H.

For example, expand (H+1+j)^3 and use sum_{j>=0}j^r/2^j=2,2,6,26 for
r=0,1,2,3, respectively; these follow by differentiating the geometric
series. The exact row and column checkers use separate finite implementations
and different horizons and confirm that the final finite column dominates
every smaller one.

Every relevant coordinate has d_i<=deg(f), so r(f)/2^deg(f)<=D(f). This proves
that the verified rational upper bound on D is an upper bound on C44.

## 7. Rejected approaches and verification limits

A numerical integer-slice branch search initially reported infeasibility at
d8,n38. Exact interpolation found a feasible rational slice polynomial; the
floating-point rejection was false. It is explicitly not used in this proof.
That polynomial suggested the Fourier L1 constraint, but no search output
is needed to justify sections1–3.

The degree-four local cap23/16 has not been proved in this work. In particular, none of
the computations is a classification of all degree-four functions. A sharp
R4 claim is not made. Every added universal lemma used here is proved above;
the inherited cap proofs and external theorem dependencies are identified.
Arithmetic PASS does not imply human review or proof-assistant verification.

## References and credit

- Chiarelli–Hatami–Saks, weighted local-degree method:
  https://arxiv.org/abs/1801.08564 .
- Wellens, restriction recurrence, symmetrization and block-sensitivity theorem:
  https://arxiv.org/abs/2005.00566 and https://discreteanalysisjournal.com/article/57741 .
- BakeLab/Épi, unchanged rational block certificates:
  https://github.com/BakeLab/Epi-results/tree/97fa6a420f417458e11723c8bceb70f1529e447a/mathematics/wellens .
- Tarannikov–Kirienko and Krotov–Valyuzhenich, R3<=10:
  https://eprint.iacr.org/2000/050 and https://arxiv.org/abs/2311.05566 .
- Pinho, inherited local caps: baseline/PROOF.md.
- Koshta, B4<=9: https://github.com/teorth/optimizationproblems/pull/283 . Stepanovs, MSc thesis 2012, from which B5<=14 follows: https://igors.org/theses/2012-boolean-deg-sens-gap-msc.pdf . The certificates here reprove these two bounds; they are not new.
- Standard coefficient granularity: Hatami lecture notes, Theorem6.4,
  https://cs.mcgill.ca/~hatami/Boolean_function_analysis.pdf .

Stepanovs's 2012 thesis/slides already claim the fully-sensitive degree-five
exclusion implying B5<=14; Towell's public conditional degree-five work already
uses Fourier integer energy. Neither B4/B5 nor the broad integer-energy method
is claimed new. See https://igors.org/theses/2012-boolean-deg-sens-gap-msc.pdf,
https://igors.org/talks/2012-boolean-degree-sensitivity-gap.pdf, and
https://github.com/queelius/boolean-degree-sensitivity . The old Stepanovs search
was not replayed; the present finite B5 certificate is checked exactly.

Prior-art coverage and dated scoreboard checks are in PRIOR_ART.md. No claim
of exhaustive novelty, optimality or independent human verification is made.


## 8. Round-three certificate changes and scope

The added degree-specific conclusions, all using the already proved criterion
(4b), are B31<=470, B32<=501, B33<=533, B34<=565, B35<=597, B36<=630,
B37<=665, B38<=701, B39<=738, B40<=777. Their finite rational slice weights
are in spectral_certificate_round3.json, bound to candidate.json by SHA256.
Both independent exact implementations reconstruct every moment and the full
lattice penalty; no coefficient returned by an optimizer is presumed valid.
The exact row bound is the rational in the headline; the independent horizon72
column bound proves the same printed claim. FINAL_RECEIPT.json records exact
agreement of the shared finite72 value and every common block bound.

No new universal lemma is needed for this numerical gain. The practical change
is a Chebyshev basis for search, with an exact finite-difference transformation
to Fourier levels and well-scaled energy cuts. This transformation is used only
by search. Neither verifier imports it or relies on solver status, termination,
branch completeness, interpolation accuracy, or an optimality claim.

Exploratory restriction and quadratic-moment inequalities are proved separately
in RESTRICTION_PROOF.md and MOMENT_PROOF.md. None is an input to the final bound:
no low-degree complete exclusion passed their independent exact checks. In
particular B8<=32, the quartic cap23/16, higher-moment exclusions and any altered
recurrence are not assumed. The recurrence, caps, external theorem dependencies
and infinite-tail proof are exactly those stated above.
