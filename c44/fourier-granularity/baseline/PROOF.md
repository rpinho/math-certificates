# A strict local-weight influence cap — written proof (unrefereed)

Use sign-valued Boolean functions on the sign cube. For each relevant coordinate
let d_i be its largest monomial degree, and D(f)=sum_i 2^{-d_i}.

**Claim.** If deg(f)<=d and d>=3, then

    D(f) <= d/2 - 2^{-d}.

The cap need not be sharp. For degree four it is 31/16, whereas the recursive
CHS witness gives 11/8. No claim that the sharp cap equals 31/16 is made.

## 1. Influence and its equality conditions

For a nonzero multilinear polynomial of degree at most k, the fraction of the
cube on which it is nonzero is at least 2^{-k}. Proof by induction: if it depends
on x_j, write x_j P+Q with deg P<=k-1. At every point where P!=0, at least one
of the two branches is nonzero, giving half the support fraction of P. Constants
are the base case. Thus for A_i=(f(x_i=1)-f(x_i=-1))/2, which is ternary and has
degree d_i-1, Inf_i(f)=Pr(A_i!=0)>=2^{1-d_i}. Hence

    D(f) <= I(f)/2 <= d/2.

The second inequality is Parseval: I(f)=sum_S |S| fhat(S)^2, while
sum_S fhat(S)^2=1. Equality D(f)=d/2 would force all Fourier mass to have degree
d, so every local degree is d, n=d 2^{d-1}, and every influence equals 2^{1-d}.

## 2. Coefficient granularity

For any sign Boolean function of degree at most d, every Fourier coefficient
is an integer multiple of 2^{1-d}. To prove this, put
p(z)=(f(2z-1)+1)/2 on {0,1}^n. Its multilinear coefficients are integers by the
inclusion-exclusion formula for coefficients from its integer-valued table.
Expand f(x)=2p((x+1)/2)-1; each coefficient is an integer multiple of 2^{1-d}.

Under equality in section 1, fix i and put k=d-1, A=A_i. A is homogeneous of
degree k, ternary, and Pr(A!=0)=2^{-k}. Its Fourier coefficients are multiples
of 2^{-k}, and each satisfies |Ahat(S)|<=E|A|=2^{-k}. Parseval gives exactly 2^k
nonzero coefficients, all equal to +/-2^{-k}; all their supports have size k.

## 3. Constant-weight affine cubes

Let T be those 2^k distinct size-k masks, and fix S0 in T. Equality in
|E A chi_S|<=E|A| implies that A chi_S is constant in sign on the support of A.
Thus chi_{S+S0} has a fixed value there for every S in T (addition is symmetric
difference). If V is the binary span of these differences and r=dim V, the
support of A lies in one consistent coset of the annihilator of V, of density
2^{-r}. Since the support density is 2^{-k}, r<=k. Conversely T lies in S0+V,
so 2^k=|T|<=2^r. Therefore r=k and T=S0+V is a full affine k-dimensional
binary cube all of whose masks have Hamming weight k.

Parametrize this affine cube by t in F2^k. Coordinate j of a mask is
alpha_j+v_j dot t. Since the total Hamming weight is identically k, expanding
these coordinate bits as (1-(-1)^{alpha_j} chi_{v_j}(t))/2 shows that, for every
nonzero v, the number of alpha_j=0 and alpha_j=1 among j with v_j=v is equal.
There must be at least k distinct nonzero classes v, since the coordinate
forms have rank k. Each class contributes at least one to the constant weight;
fixed-one coordinates also contribute one. Total weight k therefore forces
exactly k classes, each consisting of a complementary pair, and no fixed ones.
Those k classes are independent. Reparametrizing t, the masks in T select
exactly one coordinate from each of k disjoint pairs.

## 4. A graph lemma

**Lemma.** A connected simple k-regular graph, k>=4, in which every adjacent
pair has at least k-2 common neighbors has at most k+2 vertices.

If complete it has k+1 vertices. Otherwise connectedness supplies an induced
path u-v-w. Put A=N(v)\{u,w}, of size k-2. Since u and w are not adjacent,
common-neighbor counts on uv and wv force every a in A to be adjacent to both
u and w. Thus N(u)={v} union A union {x} and N(w)={v} union A union {y}, where
x,y are outside {u,v,w} union A. The edge ux has at least k-2 common neighbors;
v is not adjacent to x, so all of A must be adjacent to x. Likewise all of A
is adjacent to y.

If x!=y, each a in A has the five distinct neighbors u,v,w,x,y. The edge av
also forces at least k-4 neighbors in A, giving at least k+1 neighbors, a
contradiction. Thus x=y. Each a now has the four neighbors u,v,w,x and at least
k-4 neighbors in A; these exhaust its degree. The vertices u,v,w,x likewise
have all their neighbors among this set of k+2 vertices. It is a closed
connected component, hence the whole graph.

## 5. Excluding equality

Form the interaction graph of f: coordinates are adjacent if some nonzero
Fourier monomial contains both. By section 3, the neighbors of each coordinate
i are exactly 2(d-1) coordinates grouped in d-1 pairs, and its monomials select
one member of each pair. For an edge ij, each of the 2(d-2) coordinates in the
other pairs shares a monomial with both i and j. Thus the graph is k-regular
with k=2(d-1)>=4 and every edge has at least k-2 common neighbors.

This graph is connected. Otherwise the Fourier polynomial is a sum of two or
more nonconstant functions on disjoint variable blocks, plus a constant.
Selecting minimum/maximum values in each independent block produces at least
three distinct sum values (vary two nonconstant blocks from their minima),
which cannot all belong to {-1,1}.

Section 4 yields n<=2d. Equality in section 1 instead requires
n=d 2^{d-1}>2d for d>=3. Contradiction. Hence D(f)<d/2. Since D(f) is an integer
multiple of 2^{-d}, the claimed D(f)<=d/2-2^{-d} follows. Functions of smaller
degree also satisfy the argument (equality in the d/2 bound cannot occur).

## 6. What this does not establish

This excludes one lattice endpoint, not all larger candidates down to the
CHS witness. The exact optimal degree-four cap remains between 11/8 and31/16.
The degree-three cap 5/4 from the previous work remains stronger than this
lemma's degree-three consequence 11/8.

## 7. Restriction inequality and finite recurrence

For a coordinate j and an unrestricted relevant i, compare the local degrees
of i in f_{j=+1} and f_{j=-1}. If i survives in both, each local degree is at
most its original local degree, so the average restricted weight is at least
the original weight. If i survives in exactly one branch, f's derivative in i
is (1+/-x_j)/2 times that branch derivative, and its local degree is exactly
one larger. Its original weight is exactly half the surviving weight. If i
survives in neither, it was irrelevant. Summing proves

    D(f) <= 2^{-d_j(f)} + (D(f_{j=+1})+D(f_{j=-1}))/2.

Iterating over a set H gives
D(f)<=sum_{i in H relevant}2^{-d_i(f)}+E_alpha D(f_alpha): restricted weights
of later removed coordinates can only increase in expectation by the same
argument, or, equivalently, iterate the per-coordinate inequality directly
for the coordinates outside H.

Choose H to be a degree-d monomial. Every coordinate in H has local degree d,
so its original cost is d2^{-d}. For every assignment of the complementary
coordinates, the function on H is nonconstant: its full monomial coefficient
is the unchanged nonzero degree-d coefficient. From every input on H some
nonempty block within H therefore flips the output. For a restriction alpha
to H, take a point attaining block sensitivity of f_alpha. Its sensitive
blocks outside H, together with this additional block inside H, are disjoint
sensitive blocks of f. Hence bs(f_alpha)<=bs(f)-1.

Let B_d be a valid upper bound on block sensitivity at degree d. For b>=1 put

    U(b,d)=min(c_d, d2^{-d}+max_{1<=k<=d} U(b-1,k)),
    U(0,d)=0, and U(b,d)=U(B_d,d) for b>B_d.

Here c_3=5/4, c_4=31/16, c_7=447/128, and c_d=d/2 otherwise. Induct on b;
the restriction inequality and block decrease just proved show that U(b,d)
bounds every degree-exactly-d Boolean function with block sensitivity<=b.
Constant branches have potential zero. The convention beyond B_d is valid
because every function there already belongs to the smaller class b<=B_d.

## 8. The inherited degree-three cap

External published theorem used: R_3<=10 (Tarannikov–Kirienko; explicitly stated
for Boolean functions in Krotov–Valyuzhenich, arXiv:2311.05566v2, section 3,
step (i)). This classification theorem is cited, not independently reproved.
The following weighted deduction is reproduced in full from Pinho's previous
certificate to state exactly what the new calculation assumes.

Degrees<=2 satisfy D<=1 by section 1. A local-degree-one coordinate in a sign
Boolean function forces a dictator: writing f=x_i a+g with nonzero constant a,
the two numbers g+a,g-a both being signs forces a=+/-1 and g=0. Thus at degree
three all relevant local degrees are >=2. If all are three, R_3<=10 gives
D<=10/8=5/4. Otherwise take i of local degree two and write f=x_i A(y)+B(y).
A is nonzero affine ternary. Each nonzero linear coefficient has absolute
value >=1/2, since twice it is a nonzero integer difference of ternary values.
The range width is twice the sum of their absolute values and is at most2.
Thus A depends on at most two controls H.

On each branch with A=+/-1, B vanishes identically and f is a dictator. On
branches with A=0, f is independent of i and has degree at most two. Indeed,
any degree-three coefficient disjoint from H is unchanged by restrictions
to H (a term including an extra control would exceed total degree three).
Since at least one active branch is a dictator, every such cubic coefficient
is zero on all branches. Let s=|H| and p=Pr(A!=0). Each control's original
weight is <=1/4. Section 7 gives D<=s/4+p/2+1-p. The nonzero affine ternary
forms, up to signs, are 1, x, (1+x)/2, (x+y)/2. This list follows from the
coefficient range bound above; its (s,p) pairs are (0,1),(1,1),(1,1/2),(2,1/2).
Their budgets are 1/2,3/4,1,5/4. This proves the inherited cap.

## 9. Exact block-sensitivity inputs

External published theorem used: Wellens, Discrete Analysis 2022:20, Theorem
4.1, gives 3b(b-1)<=2(d^4-d^2) for b=bs(f), d=deg(f). This inequality implies
b<=d^2, since substituting b>=d^2+1 contradicts it. The checkers use the largest
integer satisfying the stronger inequality, intersected with the following
exact finite certificates from Épi for degrees1 through48.

To justify the certificate criterion, assume bs(f)>=m and retain m disjoint
sensitive blocks at a point, shifting that point and the output to zero.
Substitute a single variable simultaneously into every coordinate of each
block, and fix unused coordinates. Multilinear reduction cannot raise degree,
and the resulting Boolean g on m variables has g(0)=0,g(e_i)=1. Average its
polynomial over coordinate permutations. A symmetric multilinear polynomial
of degree<=d is a combination of elementary symmetric polynomials of orders
0,...,d. On a weight-k input these equal binomial(k,j), giving a univariate
polynomial p of degree<=d with p(0)=0,p(1)=1,0<=p(k)<=1 at integer0<=k<=m.

Each retained Épi certificate consists of d+1 increasing positive integer
nodes x_0=1,...,x_d=m and weights w_i satisfying
sum_i w_i x_i^j=0 (1<=j<=d), w_0>0, and
w_0+sum_{i>=1,w_i<0}w_i>0. A polynomial p as above would satisfy
sum_i w_i p(x_i)=0 by moment annihilation, but the same sum is at least the
strictly positive displayed gap because p(1)=1 and other values lie in[0,1].
Contradiction. Therefore B_d<=m-1. Verifier A checks every moment; verifier B
checks equivalent Lagrange residues: w_i x_i prod_{j!=i}(x_i-x_j) is a common
nonzero constant. The latter identity implies the moments because partial
fractions, or Lagrange interpolation, gives
sum_i x_i^r/prod_{j!=i}(x_i-x_j)=0 for0<=r<d.

## 10. Elementary infinite extension (independent of the sharper Wellens tail)

At degree e>H, keep restricting a monomial of maximum degree until the degree
falls below e. Section 7 lowers block sensitivity at every step. The bound
bs<=e^2 ensures at most e^2 such steps along every branch. Each step costs
e2^{-e}, so D_e<=D_{e-1}+e^3 2^{-e}, where D_e is the maximum potential among
functions of degree<=e. Iterating down to H proves

    D(f) <= max_{1<=d<=H} U(B_d,d) + sum_{e=H+1}^infinity e^3/2^e.

The exact checkers verify that the maximum of all finite columns occurs at H.
With e=H+1+j and geometric moments
sum 2^{-j}=2, sum j2^{-j}=2, sum j^2 2^{-j}=6, sum j^3 2^{-j}=26,
the tail equals (H^3+6H^2+18H+26)/2^H. The moments follow by applying
q(d/dq) to 1/(1-q) zero through three times and substituting q=1/2.

At H=96 the resulting rigorous bound is

    171386556154121185146549647419 / 39614081257132168796771975168
    < 4.3264049226.

Finally each relevant coordinate has local degree<=deg(f), so
r(f) 2^{-deg(f)}<=D(f). Thus this is an upper bound on C44.
The sharper original Wellens corollary gives a tiny smaller rational endpoint;
that tail precision is not counted as any mathematical gain.

## 11. Dependencies and verification scope

Every additional lemma and reduction used above has a proof here. Two
published external theorems are explicit dependencies: R3<=10 and Wellens's
block-sensitivity inequality. Neither is independently reproved or formalized.
Épi's finite data are verified exactly. The prior cubic deduction is reproduced;
the new equality exclusion uses no classification theorem. Finite cross-checks
are in verify_structure.py, but are not advertised as a formalization of the
universal proof. Both arithmetic verifiers and the prose were prepared by the
same AI agent. There is no independent human review or proof-assistant check.

## Primary references

- Wellens, *Relationships between the number of inputs and other complexity
  measures of Boolean functions*, Discrete Analysis 2022:20,
  https://discreteanalysisjournal.com/article/57741 and
  https://arxiv.org/html/2005.00566v2 .
- Krotov–Valyuzhenich, *On degree-3 and (n-4)-correlation-immune perfect
  colorings of n-cubes*, https://arxiv.org/html/2311.05566v2 .
- Chiarelli–Hatami–Saks, https://arxiv.org/abs/1801.08564 .
- Épi exact data, unchanged source revision:
  https://github.com/BakeLab/Epi-results/tree/97fa6a420f417458e11723c8bceb70f1529e447a/mathematics/wellens .
- Previous weighted cubic cap and its full inherited proof:
  https://github.com/rpinho/c44-certificate/tree/f3fb25dfb88de3da8b1a0b30f03fdb51b78ccef9 .
