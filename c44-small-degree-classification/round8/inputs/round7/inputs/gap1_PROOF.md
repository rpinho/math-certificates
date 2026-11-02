# Candidate R4=22 (unrefereed)

This is a written proof with a finite exact catalogue calculation. It is not
a proof-assistant formalization or an independent human review. The
completeness of the published cubic classification is an explicit external
dependency, as are the published minimum-support and Reed--Muller theorems.
The verifier checks the frozen catalogue and arithmetic, not those universal
published theorems. No priority claim is made.

Use sign Boolean functions, real Fourier degree, local degrees d_i, and
D(f)=sum_i 2^(-d_i). Put E3(g)=sum_(|S|=3) ghat(S)^2.

## 1. Published premises and the finite cubic calculation

We use R3=10 and the complete classification of (n-4)-resilient functions:
Rasoolzadeh, ToSC 2023(3), 213--226, DOI
https://doi.org/10.46586/tosc.v2023.i3.213-226 . Its public representative
file F10T6.txt is pinned at repository commit
eace0ce0edcb664cd5e4f84d7f5cb56dc7400925:
https://gitlab.science.ru.nl/shahramr/ResilientFunctions .
The source-file SHA256 is
d0ca4026c3bfa61f7c40945e4627feecd9264d7854114806c533d64e06836ba0.

For a bit-valued representative b(x), form g(x)=(-1)^(b(x)+sum x_i).
Multiplication by parity complements every Fourier mask. Thus b is
6-resilient on ten inputs exactly when g has real degree at most three.
Input permutations, input bit flips and output complementation commute with
this correspondence up to an output sign; all quantities used below are
invariant. Every cubic Boolean function has at most ten relevant variables
and can be padded to ten. Therefore the published list covers every case
needed here. The relevant translation is also Lemma 1 and Remark 1 of
Krotov--Valyuzhenich, https://arxiv.org/html/2311.05566v2 . That paper's
occasional number 961 differs from the primary paper and supplied list,
which have 761; this proof relies on the latter.

An integer Walsh calculation on all 761 representatives gives

    D(g) <= 1 + E3(g)/4.                                  (A)

Equality occurs in precisely three listed equivalence classes:

|file line|D|E3|relevant variables|all local degrees|
|--:|--:|--:|--:|--:|
|757|1|0|4|2|
|716|9/8|1/2|9|3|
|700|5/4|1|10|3|

In particular the E3=1 equality class is homogeneous cubic. More generally
any Boolean g with E3=1 is homogeneous cubic, by Parseval. Both a fast
Walsh calculation and a separately written direct character-sum verifier
check (A), all equality signatures, real degree, and Parseval on every row.
The calculation does not independently establish catalogue completeness.

## 2. Reduction to a minimum derivative

Choose a Boolean function attaining R4; the elementary Nisan--Szegedy bound
R4<=32 makes this maximum finite. Every relevant coordinate has local
degree four. Otherwise substitute an AND of two fresh bit variables for a
coordinate of local degree at most three; real degree remains at most four
and the relevant count increases by one, a contradiction.

For a coordinate i let A=(f_(i=1)-f_(i=-1))/2. It is ternary, degree <=3,
and Inf_i=Pr[A!=0]. Its real multilinear polynomial in bit inputs has
integer coefficients, by the Boolean-cube Mobius inversion formula.
Reducing these coefficients mod two gives its support indicator, of binary
algebraic degree <=3. The binary Reed--Muller second-weight theorem therefore
gives Inf_i=1/8 or Inf_i>=3/16. Dummy inputs can be appended to meet the
interior parameter range of that theorem. Sources and the full bridge are
also in baseline/c44r5/PROOF.md section 2. If no influence is 1/8, total
influence <=4 gives R4<=floor(64/3)=21.

Otherwise fix a minimum coordinate i. The complete minimum-support theorem
of Valyuzhenich, https://arxiv.org/html/2303.10995 , Theorem 2(2), classifies
A, up to coordinate/input/output signs, as disjoint tensor factors: r fixed
bit indicators and blocks of size m>=2 that are nonzero on the two constant
strings of that block. On an even block the two values have opposite signs,
and on an odd block they have equal signs. Their degrees are m-1. Thus

    r+sum(m-1)=3,  h=|H|=r+sum m<=6.                      (B)

H is the set of controls on which A depends. Write f=x_i A(H)+B(H,Y),
where Y excludes H and i. On the active control assignments, of density
1/8, B=0 and the restricted function is a signed dictator. H hits every
quartic Fourier monomial: a quartic monomial of B disjoint from H would
retain its coefficient on an active assignment where B vanishes. Hence
every restriction f_alpha to H has degree at most three.

The weighted restriction inequality is

    D(f) <= h/16 + E_alpha D(f_alpha).                   (C)

Indeed, for each outside coordinate its weight cannot decrease on average
under restriction. If it survives only one of two branches, its original
local degree is exactly one larger than the surviving branch degree; if
both survive, each branch degree is at most the original degree. Iterate.
All original local degrees here are four. Equality in (C) requires equality
for each individual outside coordinate, because all individual slacks are
nonnegative.

If h<=4, the ordinary cubic cap 5/4 and dictator branches give

    R4/16 <= h/16 + (1/8)(1/2)+(7/8)(5/4) <=45/32,

so R4<=22. Only three types in (B) have h>=5. We handle all of them below.

## 3. Cubic parts of the restrictions

Let Q_alpha(Y) be the homogeneous cubic part of f_alpha. It is independent
of i. Each coefficient of a Y-triple is an affine function of H, since
deg f<=4, and vanishes on every active control assignment. In particular
||Q_alpha||_2^2=E3(f_alpha)<=1. Denote its control average by e.

Apply (A) on inactive assignments. On active assignments E3=0 and D=1/2,
which improves (A) by 1/2 there. Combining with (C),

    R4/16 <= h/16 + 15/16 + e/4.                        (D)

All vector norms and inner products below are in the finite-dimensional
Hilbert space of homogeneous cubic polynomials in Y. No assumption of
independence of their Fourier supports is made.

### Type h=5: one fixed coordinate and two pairs

Normalize the active conditions to u=1, s=t, v=w. Vanishing of an affine
function on these assignments implies

    Q = (1-u)P0/2 + (s-t)P1/2 + (v-w)P2/2.

On u=-1, s=-t, v=-w, average ||Q||^2<=1 over the four independent signs:
sum_(j=0)^2 ||Pj||^2<=1. The full control average is half this sum, so
e<=1/2. Equation (D) gives R4<=22.

### Type h=5: one pair and one triple block

Normalize the active conditions to s=t, u=v=w. Then

    Q=(s-t)P/2 + u C1+v C2+w C3,   C1+C2+C3=0.

Taking s=-t and the nonconstant triple assignments yields vectors
plus/minus P plus/minus 2Cj. Averaging their squared norms over the signs
gives ||P||^2+4||Cj||^2<=1 for j=1,2,3. Consequently

    e=||P||^2/2+sum ||Cj||^2 <=3/4-||P||^2/4 <=3/4.

Equation (D) gives R4<=23. Equality at 23 requires P=0 and each
||Cj||^2=1/4. Every nonconstant triple assignment then has E3=1, so its
whole Boolean restriction is the homogeneous cubic plus/minus 2Cj.
In particular -2C1,-2C2,-2C3 are three sign Boolean functions whose sum
is zero. This is impossible pointwise, because a sum of three signs is odd.
Thus this type also gives R4<=22.

## 4. The exceptional type h=6: three pairs

The active conditions are s_j=t_j for j=1,2,3. The affine vanishing condition
gives

    Q=sum_(j=1)^3 (s_j-t_j) Pj/2.

Put ej=||Pj||^2. On the eight assignments with all pairs unequal, averaging
norms gives sum ej<=1; the full average is e=(sum ej)/2<=1/2. Equation (D)
therefore gives R4<=23.

Suppose R4=23. Every inequality in (C),(A),(D) and e<=1/2 is an equality.
All eight full-mismatch norms are one, because their average is one and
each is <=1. Expanding these eight squared norms shows
<Pj,Pk>=0 for j!=k. Hence on any mismatch set K,

    E3(f_alpha)=sum_(j in K) ej.

Each nonempty singleton K is inactive, so the equality table in section 1
forces ej in {0,1/2,1}. Since sum ej=1, there are only two cases.

**One ej is one.** Relabel it e1=1. Whenever s1=-t1, Q=s1 P1 has norm one,
so f=s1 P1(Y) on that entire slice, independently of all other controls.
P1 is a sign Boolean cubic. The following elementary pair lemma now bounds
the full variable count by 2+2R3=22, a contradiction.

Pair lemma: if a Boolean F(s,t,Z) has degree <=d and
F(s,-s,Z)=s g(Z) for a Boolean g of degree <=d-1, then it has at most
2+2R_(d-1) relevant variables. Write

    F=U(Z)+s V(Z)+t W(Z)+st T(Z).

The slice identity forces U=T and V-W=g. Here deg U<=d-2 because U=T,
and deg(V+W)<=d-1. The function

    h(s,Z)=s F(s,s,Z)=V+W+2sU

is Boolean of degree <=d-1. Every relevant Z-coordinate of F appears in
g or h, since V,W,U,T can be recovered from g and h. Thus the count is
at most 2+R(g)+R(h)<=2+2R_(d-1). Counting s in h only weakens the bound.

**Two ej are one half.** Relabel them e1=e2=1/2; P3=0. For mismatch set
K={1}, equality in (A) says that the restriction has nine relevant variables,
all of local degree three, and cubic part plus/minus P1. Therefore P1 uses
exactly nine Y-coordinates. The same holds for P2. But |Y|=23-6-1=16,
so some coordinate y occurs in both P1 and P2.

The events 'pair 1 unequal, pair 2 equal' and the reverse each have
probability 1/4 (pair 3 is unrestricted). On both, y has local degree three.
When pairs 1 and 2 are both unequal, probability 1/4, the whole restriction
is the homogeneous cubic s1 P1+s2 P2. At least one of
partial_y(P1+P2), partial_y(P1-P2) is nonzero. Thus on at least half these
sign choices y again has local degree three. Its expected restricted weight
is therefore at least

    (1/4+1/4+1/8)/8=5/64 >1/16.

This is strict slack for an outside coordinate in (C), contradicting the
required equality. It excludes the second case and proves R4<=22.

## 5. Attainment and what the lower-bound recursion actually says

The CHS/Shinkar--Tal polynomial Xi_1=x and

    Xi_d=(s+t)Xi_(d-1)(X)/2+(s-t)Xi_(d-1)(Y)/2

uses disjoint copies. Exactly one summand is active, proving Booleanity.
Its degree is d and its relevant count obeys L_d=2L_(d-1)+2,
so L4=22. The explicit 64-term Fourier polynomial is retained and checked
by integer convolution. Combining the two directions gives candidate R4=22.

For ANY degree-d Boolean seed with n relevant variables, the same construction
iterated k times yields degree d+k and 2^k(n+2)-2 relevant variables. Hence

    C44 >= (n+2)/2^d.

This confirms the prompt's thresholds: n>=23 at d=4 would give at least
25/16, and n>=47 at d=5 would give at least 49/32. The quartic route is
excluded by this proof; degree five remains open here. The corrected CHS
weighted extremal identity W_d=R_d/2^d is inherited from its final Corollary
2.2; its simultaneous-duplication proof is in baseline/c44r5/PROOF.md.
Consequently c4=11/8. Subsequent caps and the universal upper-bound recurrence
are checked separately against the frozen block certificates and tail.

In particular the inherited minimum-influence restriction argument gives

    R_d <= max(floor(d*2^d/3), floor(2d-1+(2^d-2)c_(d-1))).

With c4=11/8 it yields R5<=max(53,50)=53 and c5=53/32. The subsequent caps
are unchanged from c44r5. Inserting them into the inherited exact recurrence
and its tail at horizon 96 yields

    C44 <= 124779448974759300361320478779
           /39614081257132168796771975168 <3.1498761303.

The exact gain over the reproduced c44r5 candidate is 9/512. Raw block
certificates, recurrence, tail proof and the corrected CHS identity are
retained in baseline/c44r5/; the independent packet checker rechecks all raw
block duals and computes rational columns, while the primary calculation
uses integer recurrence rows. B8 remains <=33. This is an upper-bound
improvement; the C44 lower bound remains 3/2.
