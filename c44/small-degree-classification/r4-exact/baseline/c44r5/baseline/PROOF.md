# Minimum influence and exact local-degree caps (candidate, unrefereed)

This is a mathematical proof with finite rational arithmetic certificates,
not a proof-assistant formalization or an independent human review.
The inherited block-sensitivity certificates are unchanged. In particular,
this work does not prove B8 <= 32. No priority or optimality is claimed.

## 1. Definitions and the published extremal reduction

Use sign Boolean functions. Write d_i(f) for the largest Fourier monomial
degree containing relevant i, D(f)=sum_i 2^(-d_i(f)), and R_d for the maximum
number of relevant variables at degree at most d. The Nisan–Szegedy bound
R_d <= d*2^(d-1) ensures that this integer maximum is attained.

We use the published CHS extremal theorem: max_{deg(f)<=d} D(f)=R_d/2^d.
In the final Combinatorica 40 (2020), 237–244 version this is Corollary 2.2,
following Proposition 2.1. Primary source:
https://par.nsf.gov/servlets/purl/10201042 . The arXiv preprint
https://arxiv.org/abs/1801.08564 labels the equality Proposition 2.1.
This is an explicitly identified external theorem, not a numerical premise.

For completeness, its corrected extremal argument can also be given here.
Choose a degree-at-most-d function maximizing D; the Nisan–Szegedy variable
bound makes the maximum well defined. If its set L of relevant coordinates
with local degree below d is nonempty, duplicate all coordinates in L into
a disjoint copy L', leave all other coordinates Y shared, and add a new bit z.
In bit inputs, form

    h(x_L,x_L',Y,z)=z f(x_L,Y)+(1-z) f(x_L',Y).

The output is Boolean. All degree-d monomials of f avoid L and are identical
in the two copies, so their terms multiplied by z cancel; h still has degree
at most d. Every shared coordinate keeps local degree d. Each old coordinate
in L and its copy has local degree exactly one larger than its old degree:
a highest monomial containing it gives a noncancelling term multiplied by z.
The two resulting weights therefore sum to the old weight. The new selector
is relevant and has positive weight. Hence D(h)>D(f), a contradiction.
Thus every D-maximizer has all local degrees d, proving max D=R_d/2^d.
This is the corrected CHS duplication argument (also Chiarelli's thesis,
Proposition 8.5 and Corollary 8.6, pp. 116–117):
https://sites.math.rutgers.edu/~zeilberg/Theses/JohnChiarelli.pdf . The older
arXiv proof's single-variable AND claim is not used to preserve D.

For the argument below, choose a function attaining R_d. Every relevant
coordinate has local degree exactly d: otherwise substitute the AND of two
new bit variables for that coordinate. Monomials containing it grow by at
most one, so degree stays at most d; the new function is Boolean and has
R_d+1 relevant variables, a contradiction. Thus D(f)=R_d/2^d for this f.
This substitution argument concerns variable count only; it does not assert
that an arbitrary substitution preserves D for an arbitrary function.

## 2. An exact gap above minimum influence

Let d>=2 and M=2^(d-1). Write f=sum_S a_S chi_S on a sign cube.
Each M*a_S is an integer: convert f to a bit-valued function and use integer
Möbius coefficients, then change from bit to sign variables. This is the
same granularity lemma proved in baseline/PROOF.md.

For relevant i, the ternary derivative A_i=(f_{i=1}-f_{i=-1})/2 has degree
at most d-1. Its support density equals Inf_i(f). The elementary nonzero
polynomial support bound gives Inf_i>=2^(1-d)=1/M. Its Fourier coefficients
are a_{S union {i}}, so

    E_i := M^2 Inf_i = sum_{S containing i}(M a_S)^2

is an integer. Evaluate A_i at the all-plus input: sum_{S containing i}M a_S
equals M*A_i(1), hence is even because M is even and A_i(1) is 0 or +/-1.
Since z^2=z modulo 2 for every integer z, E_i is even. Therefore

    Inf_i=1/M, or Inf_i >= (M+2)/M^2.                   (1)

If no coordinate has minimum influence, Parseval's total-influence bound
sum_i Inf_i <= d gives

    R_d <= floor(d M^2/(M+2)).                         (2)

## 3. A minimum derivative has at most 2(d-1) controls

Suppose Inf_i=1/M and set k=d-1. Each Fourier coefficient of A=A_i has
absolute value at most E|A|=1/M. Its coefficients are integer multiples of
1/M, so each nonzero coefficient is +/-1/M. Parseval gives exactly M=2^k
nonzero coefficients. Let T be their distinct Fourier masks.

For every S in T, equality in |E[A chi_S]|<=E|A| implies A chi_S has a
fixed sign on the support of A. Choose S0 in T and let V be the binary span
of S symmetric-difference S0 for S in T, of dimension r. Every character
from V is fixed on the support of A. Thus that support lies in one consistent
annihilator coset, of density 2^(-r). Its actual density 2^(-k) gives r<=k.
Conversely T lies in S0+V and has 2^k elements, so r>=k. Hence r=k and
T=S0+V is a full affine k-dimensional cube.

Every mask has size at most k. Parametrize T by k independent binary bits.
Each coordinate of a mask is either constantly zero, constantly one, or a
nonconstant affine linear form. Let u be the number of nonconstant coordinate
forms and v the number of fixed-one coordinates. The average mask size is
u/2+v<=k, and the union H of the masks has size u+v<=2k. A depends only on H;
in particular i is outside H. This step uses an affine cube inside a Hamming
ball, and does not require the masks to have constant weight.

## 4. Restriction at the controls

Write f=x_i A(x_H)+B, with B independent of i. On each assignment alpha to H
where A(alpha)=+/-1, Booleanity forces B to vanish identically, and f_alpha
is a signed dictator. Such assignments have probability 1/M.

There is at least one such assignment. Any degree-d Fourier monomial of B
disjoint from H would retain its coefficient after fixing H: a term properly
containing that monomial and a control would exceed degree d. But on an
active assignment B vanishes, so that coefficient must be zero. There is
also no degree-d monomial involving i and disjoint from H, since A depends
only on H. Therefore H hits every degree-d monomial of f. Every restriction
to H has degree at most d-1.

The inherited restriction inequality (baseline/PROOF.md, section 4) says

    D(f) <= sum_{j in H}2^(-d_j(f)) + E_alpha D(f_alpha).

All coordinates of our variable-count maximizer have local degree d. If c
is any valid universal cap on D at degree at most d-1, with c>=1/2, then

    R_d/2^d <= G_d(c)
       := (2d-2)/2^d + 1/(2M) + (1-1/M)c.             (3)

The dictator has D=1/2; on the remaining branches use c. Combining (2),(3),

    R_d <= max(floor(d M^2/(M+2)), floor(2^d G_d(c))).  (4)

By the published CHS equality in section 1, the integer bound in (4) divided
by 2^d is a universal local-degree cap, including functions of smaller degree.

## 5. Three independently usable caps

Each row below uses an inherited cap, so these deductions are not circular.
The cubic 5/4 cap uses the inherited external theorem R3<=10; the quartic
31/16 cap has its complete inherited proof in baseline/baseline/PROOF.md.
The degree-five 5/2 cap is simply D<=I/2<=deg(f)/2.

|d|M|inherited lower-degree cap c|no-minimum R bound|G_d(c)|minimum-case R bound|resulting cap|
|--:|--:|--:|--:|--:|--:|--:|
|4|8|5/4|25|49/32|24|25/16|
|5|16|31/16|71|537/256|67|71/32|
|6|32|5/2|180|83/32|166|45/16|

The finite certificate records these exact rational quantities. The separate
verifiers check both branches at the first excluded integer, including strict
inequalities, without a numerical solver. These arithmetic checks accompany
the universal written lemmas above; they do not mechanize their proof.

## 6. The C44 recurrence

Use the inherited exact block bounds and recurrence in baseline/PROOF.md,
sections 4–6, replacing c4,c5,c6 by 25/16,71/32,45/16. Keep c3=5/4,
c7=447/128 and c_d=d/2 otherwise. The frozen spectral certificate is unchanged.
At horizon H the tail is (H^3+6H^2+18H+26)/2^H. All finite degree columns,
the freezes at B_d, and the tail are checked with exact arithmetic.

Both independent exact verifiers pass on the frozen specification, at
horizons 96 and 72. The horizon-96 rational is

    157739602520732550180509661243 / 39614081257132168796771975168
      < 3.9819073803.

The exact gain over c44r3, with identical tail, is 9/64. This is a certified
candidate under the written proof and listed external dependencies; it remains
unrefereed. All three cap improvements are used jointly. Individual ablations
and the conditional ladder are in conditional_cap_ladder.json.

The desired quartic cap 23/16 is not proved here. At the inherited inputs it
would save 1/32. After all three caps above, it would give no additional gain;
cap4=11/8 would conditionally save 3/128. The latter is not assumed either.

The inherited external dependencies (Wellens's block-sensitivity theorem,
R3<=10, and the CHS/Wellens restriction method) remain identified in the
retained baseline proofs. No SDP output supports these caps or the result.
