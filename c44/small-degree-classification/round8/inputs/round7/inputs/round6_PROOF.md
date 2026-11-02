# Ternary derivative controls and higher weight caps

Candidate, unrefereed. This is a written mathematical proof with exact
arithmetic certificates, not proof-assistant formalization or independent
human refereeing. Two separately written implementations check the finite
artifact. Their finite controls do not prove the named external theorems.
No novelty or priority is claimed. The framework is due to CHS/Wellens; the
low binary weights are due to Berlekamp–Sloane and Kasami–Tokura.

## 1. Definitions, support, and extremizers

The cube has independent uniform sign coordinates. Every real function has
a unique multilinear Fourier expansion f=sum_S fhat(S) product_{i in S}x_i.
Its real degree is the largest |S| with nonzero coefficient. A coordinate
is relevant precisely when some such S contains it. Its local degree d_i
is the largest |S| containing it. Set

    D(f)=sum_{i relevant} 2^(-d_i),
    R_d=max number of relevant coordinates at degree at most d,
    W_d=max D(f) at degree at most d.

A nonzero multilinear real polynomial of degree at most k is nonzero on
at least a 2^-k fraction of the cube. Here is an induction proof. The case
k=0 is constant. For a nonconstant polynomial choose a coordinate j and
write P=x_j A+B with A nonzero and degree at most k-1. The induction
hypothesis gives support density of A at least 2^{-(k-1)}. For each input
in that support, the two values B+A and B-A cannot both vanish. Averaging
the two j branches gives support density at least 2^-k. This also handles
polynomials whose degree is strictly below the stated upper bound.

For a sign Boolean f, write

    A_i=(f(i=+1)-f(i=-1))/2.

Its values are 0,+1,-1, its real degree is d_i-1, and p_i=E A_i^2=Inf_i(f).
The support lemma gives p_i>=2^{1-d_i}. Parseval gives

    I(f)=sum_i p_i=sum_S |S| fhat(S)^2<=deg(f).

Consequently D(f)<=I(f)/2<=d/2 and every relevant variable has influence
at least 2^{1-d}. Thus R_d<=d 2^{d-1}. After removing dummy variables and
relabeling, only finitely many Boolean functions need be considered. The
two displayed maxima therefore exist.

We use the CHS identity W_d=R_d/2^d, and include its proof because its
extremal reduction matters here. Choose f maximizing D at degree at most d.
Let L be its relevant coordinates of local degree below d, and Y the
others. If L is nonempty, take a disjoint copy L' and a fresh sign selector z,
and form

    h=(1+z)f(x_L,Y)/2+(1-z)f(x_L',Y)/2.

This is Boolean. All degree-d terms of the two f copies involve only Y,
so those terms cancel in the coefficient of z. Hence deg(h)<=d. Every Y
coordinate retains local degree d. Each original L coordinate and its
copy have local degree exactly one more than before: a largest Fourier
term containing that coordinate gives a noncanceling term also containing z.
Their two weights sum to the original weight. The selector is relevant
because the two copies differ for some inputs whenever L is nonempty.
It adds positive weight. Thus D(h)>D(f), a contradiction. An extremizer
for D has every relevant local degree d, proving W_d<=R_d/2^d. Conversely,
an R_d extremizer has D>=R_d/2^d. This proves the identity.

We also need every coordinate of an R_d extremizer to have local degree d.
In bit coordinates, replace a coordinate of smaller local degree by the
AND of two fresh bits. The new polynomial has degree at most d, since
terms using that coordinate increase degree by at most one, and other
terms keep their degrees. Both fresh coordinates are relevant: fix the
other fresh bit to 1 and use a witnessing pair of inputs for the original
coordinate. All other relevant coordinates remain relevant, by realizing
either value of the substituted AND. The relevant count increases by one,
contradicting maximality. This proves the required all-local-degrees-d
reduction for count extremizers separately.

The published exact result R_3=10 supplies W_3=5/4. The elementary influence
bound supplies W_1<=1/2 and W_2<=1. The R_3 premise is the result for
arbitrary degree-at-most-three Boolean functions, not a restricted coloring
class; see Tarannikov–Kirienko, ePrint 2000/050, and Krotov–Valyuzhenich,
https://arxiv.org/html/2311.05566v2 , section 3. CHS's identity is Corollary
2.2 in the final Combinatorica paper, https://par.nsf.gov/servlets/purl/10201042 ;
the corrected duplication proof also appears in Chiarelli's thesis,
Proposition 8.5 and Corollary 8.6,
https://sites.math.rutgers.edu/~zeilberg/Theses/JohnChiarelli.pdf .

## 2. A general control bound for ternary polynomials

Let A take values 0,+1,-1, have real degree at most k>=1, and have h
relevant coordinates. Put p=E A^2. For a relevant coordinate j,

    Delta_j A=(A(j=+1)-A(j=-1))/2

is a nonzero real polynomial of degree at most k-1. Its nonzero values
belong to {+1/2,-1/2,+1,-1}, so their squared magnitude is at least 1/4.
By the support lemma,

    E(Delta_j A)^2 >= (1/4) 2^{-(k-1)}=2^{-(k+1)}.

On the other hand Fourier orthogonality, first for each derivative and
then summed over coordinates, gives

    sum_j E(Delta_j A)^2
      =sum_S |S| Ahat(S)^2 <= k sum_S Ahat(S)^2=kp.

There are h nonzero summands, each at least 2^{-(k+1)}. Therefore

    h <= floor(k p 2^{k+1}).                            (1)

For the derivative A_i of a degree-d Boolean function set k=d-1,
M=2^k and lambda=M p_i. Formula (1) becomes

    h_i <= floor(2k lambda).                            (2)

No affine change of coordinates over F2 is being used to infer real
polynomial degree. Formula (1) is a direct real Fourier calculation. At
lambda=1 it recovers the worst 2k budget in the minimum-support
classification of Valyuzhenich, Theorem 2(2),
https://arxiv.org/html/2303.10995 . That external classification is useful
context but is not needed as a premise of (1).

## 3. Restrictions controlled by any nonzero derivative

For completeness, the weighted restriction inequality for a coordinate
set H is

    D(f)<=sum_{j in H}2^{-d_j(f)}+E_alpha D(f_alpha).       (3)

To prove it for one fixed coordinate j, consider another relevant
coordinate i. If i survives in both branches, its local degrees cannot
increase, so both branch weights are at least its original weight. If it
survives in exactly one branch, its derivative factors as (1+/-x_j)/2 times
the nonzero branch derivative. Its original local degree is exactly one
larger than its surviving branch local degree. Half that branch weight
therefore equals the original weight. A relevant i cannot disappear in
both branches. Sum these inequalities over i other than j. Applying them
successively to coordinates in H, or equivalently inducting on |H|, proves
(3) for the coordinates outside H; the original weights of H supply the
first term. Disappearing coordinates contribute zero on their branches.

Choose a count extremizer f with N=R_d and all local degrees d. Choose
one of its coordinates i and let H be the full relevant-coordinate set of
A_i; write h=|H|. Decompose f=x_i A_i(x_H)+B(x_H,x_Y). On any control input
alpha with A_i(alpha)=+/-1, both x_i branches being Boolean forces B=0
for every Y. Thus f_alpha is a signed dictator and has D=1/2. The fraction
of such control assignments is exactly p_i.

Every degree-d monomial meets H. For a monomial in B disjoint from H, its
coefficient cannot change on restricting H, since every larger monomial
containing it would have degree above d. But that coefficient must vanish
on any active control assignment, since B vanishes identically there. This
is a contradiction. A degree-d monomial involving i contains a nonempty
mask of A_i (of size d-1), hence also meets H for d>=2. Consequently every
f_alpha has degree at most d-1.

Let c>=W_{d-1} with c>=1/2. Formula (3), all original local degrees being d,
and the dictator branches imply

    N/2^d <= h/2^d +p_i/2+(1-p_i)c.

Use (2) and lambda=M p_i to obtain the essential inequality

    N <= F_d(c,lambda)
       :=2^d c+floor(2(d-1)lambda)+(1-2c)lambda.          (4)

Choose i of minimum influence. Since sum_i p_i<=d,

    1 <= lambda <= d M/N.                               (5)

Equations (4),(5) apply to the SAME chosen derivative. They do not assume
that every low-weight derivative has the same normal form.

## 4. Exact energy grid and the higher low-weight spectrum

We give the degree-to-lattice bridge explicitly. For a Boolean bit-output
function g=(1-f)/2, its unique real bit polynomial has integer coefficients:
the coefficient of a mask T is

    sum_{U subset T}(-1)^{|T|-|U|} g(1_U),

where other bits are zero. Substituting bit=(1-sign)/2 shows every Fourier
coefficient of the sign Boolean f is an integer multiple of 2^{1-d}=1/M.
Indeed a term of bit degree t<=d contributes a multiple of 2^{1-t} to f;
the constant term is also on this grid. The derivative A_i inherits this
grid. Write its coefficients z_S/M with integers z_S. Parseval gives

    lambda=M E A_i^2=(sum_S z_S^2)/M.

At the all-+1 input, sum z_S=M A_i(+1), an integer multiple of M. For d>=2,
M is even. Since z^2=z modulo two for every integer z, sum z_S^2 is even.
Therefore

    lambda belongs to (2/M) Z.                          (6)

Independently, A_i itself has integer coefficients in bit variables, by
the same finite-difference formula, since its values are integers. Reduce
those coefficients modulo two. The result has F2 degree at most k and
value 1 exactly on the support of A_i, since both signs reduce to 1.
We do not reduce A_i squared, whose real degree could be 2k.

The external below-twice-minimum Reed–Muller theorem states: for order
k>=2, any nonzero binary RM(k,n) word of weight strictly below
2*2^{n-k} has normalized weight

    lambda=2-2^{-j}, for an integer j>=0.                (7)

Only necessity is used, so all parameter-dependent restrictions on j may
be dropped. Append unused coordinates if necessary to have n>=k+2;
normalized weight and degree bounds do not change. The statement applies
to degree at most k; if the algebraic degree is smaller, a weight below
twice this minimum is already impossible by the support bound. This
statement is due to Berlekamp–Sloane / Kasami–Tokura (1970), DOI
10.1109/TIT.1970.1054545. A published explicit statement and the two
normal forms appear in Carlet (2024), section 2, p.10613,
https://www.aimspress.com/aimspress-data/math/2024/5/PDF/math-09-05-518.pdf .

Combine (6),(7). For j>=k the value M(2-2^{-j}) is either nonintegral
(j>k) or odd (j=k). Hence the safe finite list below 2 is exactly

    {2-2^{-j}: j=0,...,k-1}.                             (8)

The first terms are 1,3/2,7/4,15/8,31/16,... . Thus third and higher
weights are used, rather than replacing the sharp 3/2 factor by a false
uniform gap. We allow ALL grid values lambda>=2. In particular we do
not silently use the uncorrected final KTA table for 2..2.5. The reason
and an exact counterexample are in KTA_AUDIT.md. Our proof does not depend
on reconstructing the inaccessible full 1974 preprint or assuming its
published final table is complete.

## 5. Finite scalar optimization, with the floor treated correctly

Suppose c bounds W_{d-1}. To exclude N>=n, (5) puts lambda in [1,t],
where t=dM/n. Since the set of possible lambda for N>=n is contained in
this interval, it suffices to show every allowed lambda in [1,t] has
F_d(c,lambda)<n. This excludes all N>=n at once, not merely N=n.

Use c in [1/2,(d-1)/2], checked inductively in the certificate. Within a
cell h<=2k lambda<h+1, the value (4) is

    2^d c+h+(1-2c)lambda,

which is nonincreasing in lambda. It is NOT safe to substitute t directly
inside its floor. Below 2 we test every member of (8) not exceeding t.
For lambda>=2, the possible cell indices are 4k through floor(2kt).
On the grid (6), the first value in cell h is

    lambda_h=(2/M) ceil(h M/(4k)).                       (9)

Discard it if lambda_h>t or 2k lambda_h>=h+1. Every other grid value in
that cell has no larger budget. Thus (8),(9) form a complete finite cover
of all possible cases. Every such budget is strictly below n in caps.json.
The resulting c_d=(n-1)/2^d is valid by (4),(5) and the CHS identity.

Starting with c_1=1/2,c_2=1,c_3=5/4, proceed through d=96. The certificate
uses each already established c_{d-1} before deriving c_d. There is no
circular use of the eventual constant. Some initial ceilings are:

| d | R_d ceiling | c_d |
|---:|---:|---:|
|4|24|3/2|
|5|54|27/16|
|6|119|119/64|
|7|254|127/64|
|8|528|33/16|
|9|1083|1083/512|
|10|2199|2199/1024|
|11|4439|4439/2048|
|12|8928|279/128|

The frozen packet stores the most dangerous finite case at each first
excluded count, its complete case count, and a feasible scalar point at
the preceding count. Checker B independently enumerates all floor cells;
checker A uses an independently derived collapsed envelope. For the latter,
write a=2c-1 in [0,k-1]. Consecutive first grid values in occupied cells
h<h' differ by at most (h'-h)/(2k)+2/M. Therefore their maximal budgets
increase by at least

    (h'-h)(1-a/(2k))-2a/M
      >=1-a/(2k)-2a/M>0.

The last strict inequality is checked exactly for every degree; universally
it follows for k>=3 from (k-1)/(2k)+2(k-1)/2^k<1 (at k=3 this is 5/6;
at k>=4 the first term is below 1/2 and the second is at most 3/8).
Thus the rightmost occupied high cell suffices for checker A. It locates
that cell from the last grid point below t and tests its first grid point.
Checker B uses none of this envelope shortcut.

Two additional certified variants quantify the inputs. Dropping the RM
gaps altogether and allowing a continuum lambda>=1 gives a bound below
2.2952887883. Retaining only lambda=1 or lambda>=3/2 gives a bound below
2.2108998048. The third and higher below-two weights give the displayed
2.1974348818 bound. Each variant has its own inductive caps and both
checkers verify them. These are candidate, unrefereed consequences of the
same written lemmas, not claims about the exact Boolean maxima.

## 6. An elementary infinite tail

We need a global bound, not just a horizon calculation. The CHS/Shinkar–Tal
lower family starts with Xi_1=x and, on disjoint variables, uses

    Xi_d=(s+t)Xi_{d-1}(x)/2+(s-t)Xi_{d-1}(y)/2.

On a sign input exactly one summand is active, proving Booleanity by
induction. Its nonzero Fourier masks have size d. The two input copies
and the two fresh selectors remain relevant, so its count L_d satisfies
L_1=1 and L_d=2 L_{d-1}+2. Solving this recursion gives

    L_d=3*2^{d-1}-2=3M-2.

Thus R_d>=3M-2>=2M for d>=2. For the least-influence coordinate of its
count extremizer, (5) now yields lambda<=d/2. Apply (4) with the ACTUAL
c=W_{d-1}, discard its floor downward, and divide by 2^d. Since
1/2<=W_{d-1}<=(d-1)/2, the multiplier 2d-1-2W_{d-1} is positive and at
most 2d-2. Hence

    W_d <= W_{d-1}+lambda(2d-1-2W_{d-1})/2^d
        <= W_{d-1}+d(d-1)/2^d.                          (10)

No block-sensitivity theorem or inherited numerical block certificate is
required for (10). For H>=1, write d=H+j and sum j>=1. The elementary
geometric-series identities are

    sum 2^{-j}=1, sum j2^{-j}=2, sum j^2 2^{-j}=6.

The first follows by summing the geometric series; applying x d/dx to
sum_{j>=1}x^j=x/(1-x) once and twice, then setting x=1/2, gives the
other two. Expansion of (H+j)(H+j-1) gives

    sum_{d>H}d(d-1)/2^d=(H^2+3H+4)/2^H.                 (11)

The computed caps are nondecreasing through H. Every smaller degree is
therefore bounded by c_H; for larger degrees telescope (10) and apply
(11). Consequently C44=sup_d R_d/2^d satisfies

    C44 <= c_96+9508/2^96
      =174098727923678791596986402933/79228162514264337593543950336
      <2.1974348818.                                    (12)

The exact improvement over round five's frozen rational is

    76852852570035861934916069377/79228162514264337593543950336
      >1/1000.

This is an exact rational comparison. Rounding displayed decimals never
enters the proof.

## 7. What the recurrence and the scalar limit do and do not establish

The inherited valid block recurrence is

    U(0,d)=0,
    U(b,d)=min(c_d,d/2^d+max_{1<=j<=d}U(b-1,j)),
    U(b,d)=U(B_d,d) for b>B_d.

Its proof and raw block duals are retained in baseline/PROOF.md, sections
5–6. In outline, restricting a maximum monomial of size d costs d/2^d
in (3) and lowers block sensitivity by one: the nonzero full monomial
coefficient guarantees nonconstancy on its coordinates at every outside
input; this gives one sensitive block disjoint from all sensitive blocks
of the restricted function. Induct on b and take the maximum over every
degree j<=d. Freezing a column above B_d is valid because that class of
functions cannot grow further.

Checker B rechecks every retained Épi moment certificate and all 37
Fourier-lattice duals before re-running this recurrence with the inherited
B_d. Checker A separately computes integer recurrence rows using only
B_d=d^2, a consequence of the external Wellens theorem
3bs(bs-1)<=2(d^4-d^2), Theorem 4.1, equation (4.3),
https://arxiv.org/html/2005.00566 . Both reach exactly c_d in EVERY final
column through degree 96. Thus the current block inputs are inactive at
the saturation rows of this run. The accepted global bound (12) has the
stronger elementary tail (11) and does not rely on those block premises.
The saturation thresholds and slack are in analysis.json. A smaller B_d
can help only if it crosses below its saturation threshold, with other
inputs fixed; a decrement that leaves it at or above that threshold has
zero effect in this recurrence.

There is also a precise limit for the scalar relaxation just specified.
Define its next count as the largest integer N for which (4),(5),(6),(8)
are jointly feasible, allowing every high grid value >=2. The packet's
feasible scalar points at its count ceilings and the strict exclusions at
the next integers prove that the computed counts are exactly optimal for
THIS relaxation. Those scalar points are not Boolean existence witnesses.

Let c be the previous scalar cap. Its denominator divides 2^{d-1}, so
N_0=2^d c is an integer. The case lambda=1 has budget
N_0+2d-1-2c>=N_0 and satisfies N_0 lambda<=dM whenever c<=d/2.
It belongs to every allowed low spectrum. Hence the next cap is at least c.
Every feasible scalar point at the largest count also has N>=3M-2, so the
same estimates as in (10) bound the scalar increment by d(d-1)/2^d.
The maintained upper condition c_d<=d/2 continues after d=96 by induction,
since this increment is less than 1/2 for d>=6. Therefore the infinite
scalar sequence exists, is nondecreasing, and its limit lies in

    [174098727923678791596986393425/2^96,
     174098727923678791596986402933/2^96].                (13)

This pins its limit to 2.197434881723198... with interval width
9508/2^96<1.3*10^-25. It quantifies the end of this particular energy and
weight-spectrum relaxation. It is not an optimality theorem for all uses
of Reed–Muller structure. Full signed real-degree compatibility, sharper
control sets for actual higher-weight derivatives, correlations between
derivatives, or new block bounds crossing the saturation thresholds could
improve it. The known lower bound is 3/2 from the family above, leaving a
candidate gap about 0.6974348817. The remaining gap cannot be removed by
merely iterating this already saturated scalar relaxation farther.

Related energy prior art: Potapov, *On the number of relevant variables for
discrete functions*, Cryptography and Communications 17 (2025), 989–998,
https://link.springer.com/article/10.1007/s12095-025-00797-4 , section 5,
also uses Fourier energy and changed edges to bound ternary relevance.
Its root-of-unity output encoding can double the real degree of a ternary
polynomial in our encoding. We credit the related method; no novelty is
claimed for the elementary real-energy argument in section 2.
