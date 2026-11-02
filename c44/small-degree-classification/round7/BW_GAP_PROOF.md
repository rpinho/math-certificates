# Expanded proof of the Barnes–Wall norm gap used here

Candidate, unrefereed exposition. The argument is Nebe's (2026), expanded
with the coefficient congruences and low-dimensional base arithmetic.
It is included so the recent gap statement need not be an unexplained
black box. Three classical Barnes–Wall facts remain stated published
premises, just as the minimum-support classification remains a premise
of PROOF.md. Finite tests do not prove these classical theorems.

## 1. Classical premises and exact lattice coordinates

Index real vector coordinates by n bit inputs. For T subset [n], let b_T
be the truth vector of the bit monomial product_(j in T)b_j. Define the
lattices Lambda_n and Delta_n by their affine-subspace generators as in
LATTICE_PROOF.md. We use the following classical facts.

1. The vectors 2^floor(|T|/2) b_T form a Z-basis of Lambda_n; replacing
   floor by ceil gives a Z-basis of Delta_n. In Barnes–Wall's original
   Theorem 3.1(ii), the basis uses coordinate subspaces through the origin,
   or products of (1-b_j). The two versions agree: expanding such products
   is triangular, and the coefficient at any subset U is divisible by
   the smaller prescribed power for U. Applying the same expansion in
   reverse proves equality of the two generated lattices.
2. Their minimum squared norms are a_n=2^{n-1} and 2a_n, respectively.
   This is the minimum formula of Barnes–Wall, Theorem 3.2.
3. There is an orthogonal group preserving both Lambda_n and Delta_n
   that is transitive on the minimum vectors of Lambda_n. This is the
   classical minimum-vector transitivity, stated in Nebe's Theorem 2.5
   with its n=3 stabilizer convention and credited there to Broué–Enguehard,
   Theorem II.4. The original theorem's transitivity statement and proof
   at printed pp.36–37 were inspected; the complete classical group
   classification is not re-proved here.

Primary sources:
Barnes–Wall (1959), https://doi.org/10.1017/S1446788700025064 ;
Broué–Enguehard (1973), https://www.numdam.org/item/10.24033/asens.1241.pdf ;
Nebe (2026), https://www.math.rwth-aachen.de/~Gabriele.Nebe/papers/BW.pdf .

Fact 1 says a truth vector is in Lambda_n exactly when its integer bit
coefficients of degree t are divisible by 2^floor(t/2). Delta_n uses
2^ceil(t/2). These coefficient congruences make all the steps below exact.

## 2. Similarity of the ordered lattice pair

Let S act on the two last-coordinate branches by S(u,v)=(u+v,u-v).
Then S²=2I and ||Sx||²=2||x||². We prove

    S Lambda_n=Delta_n,   S Delta_n=2 Lambda_n.          (B1)

For a bit monomial b_T not using the last coordinate, its branch pair is
(v,v). S sends it to (2v,0), or 2v(1-b_n). The Lambda prefactor is
2^floor(t/2). Both resulting coefficients are divisible by Delta's
requirements: floor(t/2)+1>=ceil(t/2) and
floor(t/2)+1=ceil((t+1)/2).

For a monomial using the last coordinate, write b_n v where v has degree t.
Its pair (0,v) is sent to (v,-v), or v-2b_n v. The Lambda prefactor is
2^floor((t+1)/2)=2^ceil(t/2). It meets Delta's degree-t requirement, and
its doubled coefficient meets Delta's degree-(t+1) requirement. Thus
S Lambda_n is contained in Delta_n.

The same two calculations with Delta prefactors show S Delta_n is
contained in 2 Lambda_n. In the first case the prefactor 2^ceil(t/2)
is doubled, giving exponents at least 1+floor(t/2) and
1+floor((t+1)/2). In the second case the prefactor is
2^ceil((t+1)/2), which is divisible by 2^{1+floor(t/2)};
the degree-(t+1) coefficient gets one more factor two. Applying S to
this containment and using S²=2I gives Delta_n contained in S Lambda_n.
The first equality follows, and applying S again gives the second.

In particular the two models have the same normalized norm spectrum.
Conjugating the transitive group in premise 3 by S gives a group
preserving Delta_n and 2 Lambda_n, transitive on Delta_n's minimum vectors.

## 3. Minimum-vector cosets have no intermediate norm below twice minimum

First let n be odd, and consider a minimum vector ell in Lambda_n and
x=ell+d with d in Delta_n. By the transitive group preserving both
lattices, we may choose ell=2^{(n-1)/2}e_0, where e_0 is a coordinate
unit vector. This is indeed in Lambda_n by its codimension-n generator
and has norm a_n. Suppose ||x||²>a_n.

Let j be the largest exponent for which all x coordinates are divisible
by 2^j. If j>=(n-1)/2, then the squared norm is a multiple of a_n, so
its strict excess forces ||x||²>=2a_n.

Otherwise j<(n-1)/2. The vector ell is divisible by 2^{j+1}, so the odd
coordinate positions of x/2^j and d/2^j are identical. Since d's truth
coordinates are divisible by 2^j, so are its integer bit coefficients
(each is an integer finite difference of truth values). After division,
Delta's coefficient requirement implies that coefficients of degree t>2j
are even, because ceil(t/2)>j. Therefore (d/2^j) modulo two has binary
degree at most 2j. It is nonzero, since x/2^j has an odd coordinate.
The binary minimum-weight theorem gives at least 2^{n-2j} odd positions.
Each contributes at least 2^{2j} to ||x||², so ||x||²>=2^n=2a_n.

For even n use the ordered pair (Delta_n,2 Lambda_n). Its minimum vector
may be taken as ell'=2^{n/2}e_0 by the conjugated transitivity above.
Write x'=ell'+d', d' in 2 Lambda_n, with squared norm >2^n. If all
coordinates have common factor 2^j with j>=n/2, norm divisibility gives
||x'||²>=2^{n+1}. Otherwise ell' is divisible by 2^{j+1}; the odd
positions come from d'/2^j. Its binary degree is at most 2j-1, because
a degree-t bit coefficient of d' is divisible by 2^{1+floor(t/2)}, and
1+floor(t/2)>j whenever t>2j-1. If j=0 this says all coefficients are
even, impossible for a nonzero odd residue. For j>=1 the binary support
bound gives at least 2^{n-2j+1} odd positions and again
||x'||²>=2^{n+1}. Transporting by S proves for even n the same conclusion
for the original ordered pair. Thus for every n,

    ell minimal in Lambda_n, d in Delta_n:
    ||ell+d||²=a_n or ||ell+d||²>=2a_n.                 (B2)

Only the ordinary binary minimum-weight bound is needed here; it follows
by induction on branches exactly as for low-degree binary polynomials.
When one branch is zero the other loses one degree; when both are nonzero
sum their inductive minima. Boundary constant/full-degree cases are
immediate. No assumption about preserving real degree under a binary
change of variables occurs in this lattice argument.

## 4. Recursion and low-dimensional base cases

The coefficient bases in premise 1 give the exact recursion

    Lambda_(n+1) = { (ell+d,ell): ell in Lambda_n,
                                      d in Delta_n }. (B3)

Indeed an unused-last-coordinate bit monomial has branches (v,v) with
Lambda_n's floor prefactor. A used-last-coordinate monomial of total
degree t+1 has branches (0,v) with prefactor 2^floor((t+1)/2)=2^ceil(t/2),
so both branches are in Lambda_n and their difference is in Delta_n.
Conversely (ell,ell) is generated by unused-last-coordinate monomials,
and a Delta_n generator d of degree t gives (d,0), namely d(1-b_n),
whose codimension-(t+1) Lambda prefactor is exactly 2^ceil(t/2).
This proves both containments in (B3).

For n>=2, every norm in Lambda_n is a multiple of 2^ceil(n/2). To see
this, its basis vector of degree t has squared norm
2^{n-t+2floor(t/2)}, either 2^n or 2^{n-1}. The cross term twice the
inner product of degree-t and degree-u basis vectors is

    2^{1+floor(t/2)+floor(u/2)+n-|T union U|}.

Its exponent is at least ceil(n/2). If t+u<=n, use
floor(t/2)+floor(u/2)>=(t+u-2)/2 and |T union U|<=t+u to get an exponent
at least n-(t+u)/2>=n/2. If t+u>=n, use |T union U|<=n to get at least
(t+u)/2>=n/2. Integer exponents give the ceiling. Diagonal terms also
have sufficient divisibility since n-1>=ceil(n/2) for n>=2.

For n=2,3,4,5, this divisor is at least a_n/2. Therefore every norm
strictly above a_n is at least a_n+a_n/2. For n=1 the integer lattice
has minimum one and next norm at least two. These prove the needed base
cases without a theta-series computation.

## 5. Norm-gap induction

Assume Lambda_n and hence its similar Delta_n have no norm strictly
between their minimum and 3/2 of their minimum. Take x in Lambda_(n+1)
with norm strictly above 2a_n. By (B3), x=(ell+d,ell). Exchanging the
branches preserves this representation (replace ell by ell+d and d by -d),
so assume ||ell||<=||ell+d||.

If ell=0, then x=(d,0), d in Delta_n. Its norm is above Delta_n's
minimum 2a_n; induction on the similar lattice gives norm >=3a_n.
If ell is nonzero and not minimal in Lambda_n, induction gives
||ell||²>=3a_n/2, so both branches together have norm >=3a_n.
Finally suppose ell is minimal. By (B2), the other branch is either
minimal or has norm >=2a_n. Both minimal would give total norm 2a_n,
contrary to the strict assumption. Hence the total is >=3a_n.
These exhaustive cases prove the induction and Nebe's norm gap.

The integer-polynomial embedding in LATTICE_PROOF.md now follows from
this written norm-gap proof and the three explicitly stated classical
premises. The exact verifiers check the finite C44 artifacts and arithmetic,
not the classical lattice group theorem. No proof-assistant claim is made.
