# Retaining both contact-moment parameters

Unrefereed extension of SPECTRAL_LEMMA.md. The same even outer-factor argument
proves the low-coefficient constant zeta=7/100 if the uniform scalar bounds
below pass. There is no change to the flux input, Fourier majorant, coefficient
identity, or final moment criterion.

Write a=|m_1| and b=|m_2|. If a>=27/100 then S>=a^2>=0.0729>zeta.
If b<=21/25 then S>=2 kappa(1-b^2)>=0.070656>zeta. Otherwise, after shifting
theta by arg(m_2)/2, retain the two nonnegative terms discarded by the earlier
one-parameter reduction:

 max(S,T(theta)) >= h_ab(theta),
 h_ab(theta)=max(a^2+(6/25)(1-b^2),
                 (6/25)(1-b)+(12/25)b sin^2(theta)-a).

The uniform target is mean(log h_ab)>=log(7/100) for
0<=a<=27/100 and 21/25<=b<=1. The outer-factor construction and radial
Parseval limiting argument in SPECTRAL_LEMMA.md apply verbatim, since h_ab
is positive for a>0 and pi-periodic. The resulting epsilon is

 epsilon=(7/200)g(1-1/H).

For 0<a<=1/10000, use h_ab>=max(a^2,ell sin^2(theta)-a), ell=252/625,
since b>=21/25 and the other terms are nonnegative. Apply the small-parameter
polynomial/logarithmic argument of SPECTRAL_LEMMA.md with this ell and the
finer x-bins obtained by splitting each interval with consecutive endpoints
2^-10,2^-9,...,2^-1,3/4 into four equal rational subintervals.
All inequalities, including the final
logarithmic lower bound, are checked with intervals. At a=0 the explicit
outer factor of ell sin^2(theta) gives ell/4>7/100.

For 1/10000<=a<=27/100, contact-cover.json is a binary tree partition of the
rectangle [1/10000,27/100] x [21/25,1]. Every split is at an exact rational
interior point in one coordinate. The verifier recursively reconstructs the
children's rectangles, so coverage and absence of gaps do not depend on a
floating area test. Each leaf has its own uniform angular grid of n cells.
On a leaf [a_l,a_h] x [b_l,b_h], at angular left endpoint theta_j, use

 S_l=a_l^2+(6/25)(1-b_h^2),
 T_lj=min_{b=b_l,b_h}[(6/25)(1-b)+(12/25)b sin^2(theta_j)]-a_h.

Both are lower bounds throughout that parameter box and angular cell:
S increases with a and decreases with b; T increases with sin^2(theta),
decreases with a, and is affine in b. Thus

 (1/n) sum_j log max(S_l,T_lj)

is a valid lower bound for the circle mean of log h_ab. The exact checker
requires every leaf's lower bound to exceed log(7/100). It independently
rounds all elementary functions outward and accepts only positive lower gaps.
The geometric mean, and therefore the low-coefficient estimate, is uniform
over both contact parameters. Global beta-epsilon>=0 still follows from
Psi>6, since epsilon<(7/200)g and g<2/3.
