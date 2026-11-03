# Reed–Muller influence gap and joint local caps (candidate, unrefereed)

This is a written mathematical proof using precisely stated published
theorems and small exact rational certificates. It is not a proof-assistant
formalization or independent human review. No novelty or priority is claimed.
The exact arithmetic verifier does not mechanize the universal lemmas below.

## 1. Definitions and extremal reduction

Use sign Boolean functions on a uniform sign cube. Real degree means the
degree of their multilinear Fourier polynomial. A coordinate is relevant
when some nonzero Fourier coefficient contains it. Its local degree d_i is
the largest size of such a mask. Define

    D(f) = sum_i 2^(-d_i),
    R_d = maximum number of relevant coordinates at real degree <= d,
    W_d = maximum D(f) at real degree <= d.

The elementary support bound says that a nonzero multilinear polynomial of
degree at most k is nonzero on a fraction at least 2^(-k). Proof by induction:
write P=x_j A+B with A nonzero of degree at most k-1. On every input where
A is nonzero at least one of the two j-branches is nonzero. Constants start
the induction. Apply this to A_i=(f_{i=1}-f_{i=-1})/2, whose values are
0,+1,-1 and whose support density is Inf_i(f). Its degree is at most d_i-1,
so Inf_i>=2^(1-d_i). Parseval gives

    D(f) <= I(f)/2 <= deg(f)/2,
    I(f) = sum_S |S| fhat(S)^2.

In particular R_d<=d*2^(d-1), so after removing dummy coordinates and
relabeling there are finitely many relevant functions and both maxima exist.

We use the published CHS identity

    W_d = R_d/2^d.                                           (1)

It is Corollary 2.2 after Proposition 2.1 in the final CHS paper,
Combinatorica 40 (2020), 237–244,
https://par.nsf.gov/servlets/purl/10201042 . Here is the corrected proof,
also Chiarelli's thesis, Proposition 8.5 and Corollary 8.6, pp.116–117,
https://sites.math.rutgers.edu/~zeilberg/Theses/JohnChiarelli.pdf .
Choose f maximizing D at degree <=d. Let L be the relevant coordinates with
local degree below d, and Y all others. If L is nonempty, make a disjoint
copy L', share Y, and use a new bit selector z to form

    h=z f(x_L,Y)+(1-z)f(x_L',Y).

The degree-d terms avoid L and cancel in the selector difference, so h has
degree <=d. Each shared coordinate retains local degree d. Each duplicated
coordinate's degree rises exactly one, and its two copies' weights sum to
its old weight. The selector is relevant and adds positive weight. This
contradicts maximality. Thus every coordinate of a D-maximizer has local
degree d. It follows that W_d<=R_d/2^d; the reverse inequality follows by
taking an R_d-maximizer, whose D is at least R_d/2^d. This proves (1).

An R_d-maximizer also has every local degree exactly d: otherwise replace a
low-local-degree bit by an AND of two fresh bits. The new Boolean function
has degree <=d and one extra relevant coordinate, contradicting R_d. This
argument is about count; it does not assert preservation of D by a single
AND substitution. We always apply the case arguments below to this
all-local-degrees-d maximizer.

We use the external exact result R3=10, explicitly for arbitrary Boolean
functions of real degree <=3, not only perfect colorings. Sources:
Tarannikov–Kirienko, ePrint 2000/050, and Krotov–Valyuzhenich,
https://arxiv.org/html/2311.05566v2 , section 3 and its first enumeration step.
Hence W3=5/4. The preceding influence argument supplies W1<=1/2 and W2<=1.

## 2. The stronger influence gap

We explicitly invoke this classical binary Reed–Muller theorem:

    For 2<=k<=n-2, a nonzero polynomial over F2 of degree at most k
    on F2^n has weight 2^(n-k), or weight at least 3*2^(n-k-1). (2)

Weight means the number of inputs with value one. This is the second-weight
consequence of Kasami–Tokura (1970), DOI 10.1109/TIT.1970.1054545, and
Kasami–Tokura–Azumi (1976), DOI 10.1016/S0019-9958(76)90355-7.
Accessible published statements are Klein–Storme (2011), Theorem 2,
https://backoffice.biblio.ugent.be/download/2140143/2939938 , and Rolland,
https://arxiv.org/pdf/0902.0058 , introduction p.2. We use (2) only in the
displayed parameter range. It is a named external theorem, not a finite
enumeration premise or an assertion about real polynomial degree.

Here is the full bridge from real degree to (2). Express the ternary A_i in
bit inputs. Its unique real multilinear polynomial has integer coefficients:
the coefficient of T is sum_{U subset T}(-1)^(|T|-|U|) A_i(1_U), with other
bits zero. These are integers because A_i is integer valued. The real degree
is at most k=d-1. Reducing these integer coefficients modulo two therefore
gives a polynomial over F2 of degree at most k. Its value is precisely the
support indicator of A_i, since both +1 and -1 reduce to one and zero reduces
to zero. In particular we reduce A_i itself, not its real square A_i^2
(the latter could have degree 2k).

For d>=3 append unused bit coordinates if needed so the ambient dimension
n is at least k+2. Appending them leaves degree and support density unchanged
and doubles both weight and cube size at each step. Now (2) applies even
if the actual algebraic degree is smaller than k. With M=2^(d-1), every
relevant coordinate satisfies

    Inf_i = 1/M, or Inf_i >= 3/(2M).                       (3)

This improves the inherited gap (M+2)/M^2 when M>4. If there is no coordinate
with minimum influence, summing (3) and using I<=d yields

    R_d <= floor(d*2^d/3).                                (4)

No numerical optimization, guessed divisibility, or averaged Boolean
polynomial occurs in this deduction. In particular, the Reed–Muller theorem
is not being applied to a symmetrized Fourier polynomial.

The factor 3/2 is sharp for actual Boolean derivatives, not only abstract
codewords. Let g=(s+t)x/2+(s-t)y/2 and h=(s+u)x/2+(s-u)v/2. Each is Boolean
of real degree two, and their Fourier expansions share only sx, with
coefficient 1/2 in each. Thus E[gh]=1/4 and Pr[g!=h]=3/8. The Boolean
selector f=(1+z)g/2+(1-z)h/2 has degree three, and Inf_z(f)=3/8, exactly
3/2 times its minimum 1/4. Replacing f by (1+w)f/2+(1-w)/2 raises the degree
by one and halves Inf_z. Induction gives sharp examples at every d>=3.
Exact Boolean convolution and influence checks through d=8 are retained.

## 3. Full minimum-support structure and its sharp control budget

Suppose Inf_i=1/M, and write k=d-1. Apply Valyuzhenich (2023),
https://arxiv.org/html/2303.10995 , Theorem 2(2) with spectral interval [0,k].
This interval is exactly the space of real degree-at-most-k polynomials.
The theorem says that, up to coordinate permutations, bit flips and nonzero
scalar, A_i is a tensor product on disjoint coordinate blocks of:

* psi_m on odd m: value +1 at both constant bit strings and zero elsewhere;
* phi_m on even m: values +1,-1 at the two constant strings, zero elsewhere;
* a point indicator I_r on r further coordinates.

Singleton psi_1 is constant and uses no relevant coordinate; omit it. All
nonconstant psi blocks have odd size m>=3, and phi blocks have even size
m>=2. The scalar is +/-1 because the nonzero values of A_i are +/-1.
The Fourier expansion of psi_m contains exactly the even masks, and phi_m
exactly the odd masks, each with coefficient 2^(1-m). Thus in their respective
parity cases both blocks have degree m-1. I_r has degree r. Disjointness
makes degrees add. If the nontrivial block sizes are m_1,...,m_b, then

    k = r + sum_j(m_j-1),
    h := |H| = r + sum_j m_j = k+b <= 2k,
    2k-h = r + sum_j(m_j-2).                              (5)

The equality of the degree to k also follows from the elementary support
bound: smaller degree would give support density strictly larger than 2^-k.
H is the actual relevant-coordinate set of A_i. Formula (5) gives smaller
type-specific budgets whenever r>0 or any block has size >2. The worst
case h=2k remains possible: a product of k phi_2 blocks. It occurs in the
CHS witnesses. We do not claim a smaller universal control set from the
classification. The certificate uses the safe worst budget; finite controls
also check the individual types. This credits the classification rather than
presenting the inherited affine-support observation as new.

## 4. Minimum-influence restriction and sequential caps

Write f=x_i A_i(x_H)+B(x_H,x_Y), with B independent of i. On every control
assignment where A_i=+/-1, Booleanity of both x_i branches forces B=0 for
all Y. Therefore f restricted there is a signed dictator, with D=1/2.
These active assignments have probability 1/M.

H hits every degree-d Fourier monomial of f. To see this for B, suppose a
degree-d mask T disjoint from H has a nonzero coefficient. After fixing H,
its coefficient cannot acquire any additional contribution: a proper
superset of T containing a control would have degree >d. But on any active
assignment B vanishes identically, contradicting that coefficient. Any
degree-d monomial involving i also meets H: A_i is supported on H and
d>=3. Thus all restrictions f_alpha have degree at most d-1.

For completeness the weighted restriction inequality is

    D(f) <= sum_{j in H}2^(-d_j(f)) + E_alpha D(f_alpha).   (6)

For one fixed coordinate j and another coordinate l: if l survives both
branches its local degrees cannot increase, so its expected weight is at
least its original weight. If it survives one branch, its derivative factors
as (1+/-x_j)/2 times the nonzero branch derivative; its original local degree
is exactly one larger. Half the branch weight again equals its original
weight. Iteration for coordinates outside H proves (6).

Apply (6) to the R_d-maximizer. All local degrees are d. For any valid cap
c>=1/2 on W_{d-1}, (5), the dictator branches and the other restrictions give

    R_d/2^d <= (2d-2)/2^d + 1/(2M) + (1-1/M)c.

Consequently the minimum-influence case satisfies

    R_d <= floor(2d-1 + (2^d-2)c).                        (7)

Combining cases (4),(7) and using (1) gives a valid universal cap

    c_d = 2^(-d) max(floor(d*2^d/3),
                     floor(2d-1+(2^d-2)c_{d-1})).        (8)

Start with c3=5/4 and proceed in increasing d; no conclusion is used before
it is proved. This joint use of lower caps substantially improves the
minimum-influence budgets at degrees 5 and higher as well as the no-minimum
branch. Every floor and the contradiction at its first excluded integer
are checked exactly in cap_certificate.json by separately written programs.

|d|input c_(d-1)|minimum-case R ceiling|no-minimum R ceiling|new R ceiling|c_d|
|--:|--:|--:|--:|--:|--:|
|4|5/4|24|21|24|3/2|
|5|3/2|54|53|54|27/16|
|6|27/16|115|128|128|2|
|7|2|265|298|298|149/64|
|8|149/64|606|682|682|341/128|
|9|341/128|1375|1536|1536|3|
|10|3|3085|3413|3413|3413/1024|
|11|3413/1024|6840|7509|7509|7509/2048|
|12|7509/2048|15033|16384|16384|4|

These are upper ceilings, not claims of attainability. Known CHS/Shinkar–Tal
lower counts at degrees 4,5,6 are 22,46,94; their headrooms here are 2,8,34.
They are independently checked as witnesses, not promoted to exact maxima.
The degree-d construction is Xi_1=x and

    Xi_d=(s+t)Xi_(d-1)(x)/2+(s-t)Xi_(d-1)(y)/2,

on disjoint variables. Exactly one term is active at a sign input, so the
function is Boolean. Induction gives homogeneous degree d and relevant
count L_d=2L_(d-1)+2=3*2^(d-1)-2. The source is CHS section 3,
https://arxiv.org/html/1801.08564v3 .

## 5. The unchanged certified block inputs

We retain the round-four exact block-sensitivity certificates byte for byte.
Their full original proof is baseline/baseline/PROOF.md, sections 1–5.
Here are all ingredients needed for their use.

If bs(f)>=n, compress n disjoint sensitive blocks at a witnessing input to
n new bits, fix all other bits, and change output sign so g(0)=1 and
g(e_j)=-1. Substitution and multilinear reduction do not raise real degree.
Symmetrizing g gives q(0)=1,q(1)=-1 and |q(x)|<=1 for integer 0<=x<=n.
At degree d,

    q(x)=sum_{l=0}^d A_l K_l(x)/binom(n,l),
    K_l(x)=sum_j (-1)^j binom(x,j)binom(n-x,l-j),
    A_l=sum_{|S|=l} ghat(S).

Every original ghat(S) is an integer multiple of 1/M, M=2^(d-1): write
(1-g)/2 as an integer-coefficient bit polynomial and substitute bits by
(1-sign)/2. With z_S=M ghat(S), Parseval gives sum z_S^2=M^2. Define
h(t)=max_{z in Z}(tz-z^2), attained at floor(t/2) or floor(t/2)+1.
For any rational alpha_x put

    t_l=sum_x alpha_x K_l(x)/binom(n,l),
    L=alpha_0-alpha_1-sum_{x>=2}|alpha_x|.

Then

    L <= sum_l t_l A_l
      = M+(1/M)sum_S(t_|S| z_S-z_S^2)
      <= M+(1/M)sum_l binom(n,l)h(t_l).                   (9)

A strict reverse inequality certifies B_d<=n-1. All 37 retained spectral
duals satisfy it exactly. The files and their pinned hashes are in
candidate.json. No integrality is imposed on individual symmetrized
coefficients, and no solver output is accepted without rational checking.

The retained Épi certificate at each degree 1..48 has d+1 distinct positive
integer nodes x_0=1<...<x_d, and rational weights w_i such that

    sum_i w_i x_i^j=0 for j=1,...,d,
    w_0>0, and w_0+sum_{i>=1,w_i<0}w_i>0.

For the bit-output compressed polynomial p=(1-q)/2, p(0)=0,p(1)=1 and
0<=p(x_i)<=1, so the first identities force sum w_i p(x_i)=0 and the second
line forces it to be positive. This proves B_d<=x_d-1. One checker verifies
all power moments, the other independently checks their common Lagrange
residues w_i x_i product_{j!=i}(x_i-x_j), which are equivalent to the
annihilation identities by polynomial interpolation. Épi's raw certificate
hash is ce66f1097a7284e9845113fa1dc39267932cc934fd23d9019ff13d3dcb39cf49.

Finally, the explicitly external Wellens block theorem is

    3 bs(f)(bs(f)-1) <= 2(d^4-d^2),                       (10)

Theorem 4.1, equation (4.3) in https://arxiv.org/html/2005.00566 . At every
degree take the smallest of these valid inputs. In particular B8 stays 33;
B8<=32 is not proved here. Credit for the inherited improvements remains
with Épi, Koshta (B4<=9), Stepanovs (B5<=14), and the preceding Fourier
integer-energy work including Towell; see PRIOR_ART.md.

## 6. Joint block recurrence and tail

For a degree-exactly-d function choose a top-degree monomial H of size d.
Each of its coordinates has local degree d, costing d/2^d in (6). For every
outside assignment the polynomial on H stays nonconstant: the full H
coefficient cannot change, since any proper superset would exceed degree d.
Take a witnessing input for bs(f_alpha) after fixing H. Its sensitive blocks
outside H are sensitive in f. Nonconstancy on H supplies another nonempty
sensitive block inside H, disjoint from the others. Thus

    bs(f_alpha) <= bs(f)-1.

With valid local caps c_d (the new caps above and d/2 otherwise), define

    U(0,d)=0,
    U(b,d)=min(c_d, d/2^d+max_{1<=j<=d}U(b-1,j)) for 1<=b<=B_d,
    U(b,d)=U(B_d,d) for b>B_d.                            (11)

Constants contribute zero. Induction on b using (6) and the block drop
proves (11) bounds D at exact degree d and bs<=b. Freezing above B_d is
legitimate because the actual class of functions does not grow. All degree
columns, including smaller degrees, are evaluated; no top-column-only
monotonicity assumption is used. By (1), the maximum through horizon H
bounds R_d/2^d for every d<=H.

For higher degrees, at most B_d successive maximum-monomial restrictions
are required to drop degree d on every branch: each reduces bs by one, and
bs=0 means a constant. Each restriction costs d/2^d. Hence

    W_d <= W_(d-1)+d B_d/2^d.

The integer root in (10) is <=d^2 for d>=1 (substitute d^2+1 to exclude it).
Thus sum_{d>H}d B_d/2^d <= sum_{d>H}d^3/2^d. Expanding (H+j)^3 and using
sum_{j>=1}2^-j=1, sum j2^-j=2, sum j^2 2^-j=6, sum j^3 2^-j=26, obtained
by differentiating the geometric series, gives exactly

    tail_H = (H^3+6H^2+18H+26)/2^H.                     (12)

The rational row calculation at H=96 and separately written (same agent) rational
column calculation at H=72 check all finite steps plus (12). The proposed
H=96 upper bound is

    125475790246857326765951236155 / 39614081257132168796771975168
      < 3.1674542553.

With identical horizon and tail its exact improvement over the inherited
round-four bound is 417/512, strictly greater than 1/10000. Acceptance
requires both verifiers to pass on the final frozen bytes. Their receipts
and the hash manifest are part of the accompanying artifact. The conclusion
remains a candidate, unrefereed by a human, conditional on the explicitly
identified published theorems in the normal mathematical sense.
