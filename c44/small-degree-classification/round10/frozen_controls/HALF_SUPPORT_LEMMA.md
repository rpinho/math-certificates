# Quartic half-support completion — exploratory, candidate, unrefereed

This lemma is not yet part of an accepted R5 exclusion. The complete cubic
catalogue is an explicit published premise. Two separate exact scans give
the potential envelope by number of variables (units of 1/8):

    0,4,4,6,8,8,8,8,8,9,10  for budgets 0,...,10.

All six nine-variable classes are balanced with all local degrees three;
every ten-variable cubic is homogeneous. Sources: cubic_stats_a.py (Walsh)
and cubic_stats_b.cpp (direct character sums), on the inherited frozen
F10T6.txt. These scans passed; their first attempt had an incorrect expected
line number for the ten-variable class (757 instead of 700), corrected
against the actual coefficient calculation. No accepted bound used that
failed assertion or an unchecked catalogue statistic.

Let f be a Boolean quartic using 22 variables, all of local degree four.
Split coordinates into X,Z,Y such that f=T(X,Z)+U(Z,Y), T has zero X mean,
and all coefficients containing X are known. Suppose T is nonconstant as
an X polynomial on exactly half the Z assignments, a set C. On C, Booleanity
forces U to be independent of Y: a nonconstant T has at least two values,
and adding U must put both in {-1,1}, fixing U uniquely. On the complement,
T=0. Suppose |X|>=9.

Every coefficient involving X vanishes off C, so a nonzero such coefficient
has positive degree in Z. Every fixed-Z section therefore has X degree at
most three. Coordinatewise restriction gives E_Z D_X(f_Z)>=|X|/16. If
|X|>10, the cubic cap on half the assignments contradicts this. If |X|=9
or 10, the catalogue envelope gives E_Z D_X(f_Z)<=|X|/16, so equality holds.
Every active section uses all |X| inputs and is balanced. It has a nonzero
X-triple coefficient; that coefficient is an affine function of Z, supported
on precisely C. The linear minimum-support classification makes C either
a one-coordinate half cube or an equality/opposition of two coordinates.

Normalize signs. If C={s=1}, write the two Boolean branches g(X,Z') and
h(Y,Z'). Degree four means their quartic parts agree and depend only on
Z'. Balance of every active X section says mean_X g=0 identically in Z',
so that common quartic part is zero. Both branches are cubics, giving at
most 1+R3+R3=21 variables, a contradiction.

If C={s=-t}, write

    f=U0+sV+tW+stT0,
    G=V-W, J=V+W, H=U0-T0, K=U0+T0.

On active branches f(s,-s)=sG+H; on inactive branches f(s,s)=sJ+K.
G,H avoid Y, and J,K avoid X. We have deg G,deg J<=3 and K-H=2T0 of
degree <=2. Thus the common degree-three/four parts of H,K can involve
only Z'. Balance of both active branches implies mean_X H=mean_X G=0,
so those common high parts vanish. Hence deg H,deg K<=2.

Now G+sH and J+sK are both Boolean cubics: multiplying the corresponding
original branch by s gives these signs. Their unions of outside variables
each have size at most ten, and if H or K is nonzero their new selector s
is relevant, leaving at most nine outside variables for that cubic. Since
f has 22 variables, the bound 2+10+10 must be an equality. Therefore both
outside unions have size ten, they are disjoint, and H=K=0. The two cubics
G,J on ten variables are homogeneous. Consequently

    f=(s-t)G/2+(s+t)J/2

is homogeneous quartic. In particular its top energy is one.

Thus a nonhomogeneous quartic on 22 variables cannot have this half-support
configuration with |X|>=9. This uses no assumption that the eight or more
Y inputs are common to both inactive branches. The earlier exploratory
shared-input shortcut is unnecessary and has not been promoted to a proof.

The prototype filter applies this only if some already forced Fourier
term has degree below four, proving nonhomogeneity directly. Xi4 positive
controls are homogeneous and remain admissible. Whole R5 acceptance would
still require all cases, an explicit reduction, two separately written
complete exact implementations, frozen artifacts and rejection controls.
