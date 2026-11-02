# Two covering zeros, a hyperbolic enclosing disk, and the moment criterion

UNREFEREED PREPRINT. The derivation below uses classical Schwarz factorization and
hyperbolic Jung; no novelty is claimed for either theorem. The quantitative
hypotheses for c=54/125 pass two independently implemented exact checkers.
This is an unrefereed analytic proof, separate from the retained certificate
using Wang’s original estimate. No proof-assistant formalization is claimed.

Let 0<c<1, c<r<1, w=-log c, A=pi^2/w, and
X=sinh(A/2)^2. If omega maps the annulus c<|z|<1 holomorphically into the unit
disk, its image of |z|=r has pseudohyperbolic diameter at most

    K = X / (X + sin(pi log r / w)^2).

Here is a direct proof, requiring no assertion about the angular maximum in
Simha's annular product. Lift omega to h(zeta)=omega(exp zeta) in the vertical
strip log c<Re zeta<0. The map exp(i*pi*(zeta-log c)/w) maps that strip
biholomorphically to the upper half-plane. Rotate the annulus so the first
point has lift a=log r and choose the other lift a+i*theta, 0<=theta<=2*pi.
A disk automorphism makes h(a)=0. Periodicity also gives h(a+2*pi*i)=0.
Two applications of Schwarz's lemma (divide by one Blaschke factor, then the
other) bound the value at the second point by the product of its two
pseudohyperbolic distances to those zeros.

Put phi=pi*log(r/c)/w, v=pi*theta/w. Those distances are p(v) and p(2*A-v),
where

    p(v) = sinh(v/2) / sqrt(sinh(v/2)^2 + sin(phi)^2),  v>=0.

For v>0, differentiating log p(v) with respect to u=v/2 gives

    sin(phi)^2*coth(u)/(sinh(u)^2+sin(phi)^2).

This is positive and strictly decreasing: coth is positive decreasing and the
positive denominator is increasing. Thus log p is concave. Consequently
p(v)*p(2*A-v)<=p(A)^2=K, including endpoints by continuity. This proves the
diameter bound for every pair and every such omega.

Use hyperbolic distance d=2*artanh(pseudohyperbolic distance), so the image
has hyperbolic diameter at most D=2*artanh K. Hyperbolic Jung in dimension two
places a compact set of diameter D in a hyperbolic disk of radius rho_h with

    sinh rho_h <= (2/sqrt 3)*sinh(D/2).

A short proof of the needed version: a smallest enclosing disk exists for a
compact subset of the hyperbolic plane. At its center, the directions to its
boundary contacts cannot lie in an open semicircle, or a small motion of the
center would shrink the radius. There are two opposite contact directions or
three whose convex hull contains zero; some pair has angular separation at
least 2*pi/3. The hyperbolic cosine rule gives for that pair
cosh d_pair >=1+(3/2)*sinh(rho_h)^2. Since d_pair<=D, the stated inequality
follows. The two-contact case gives an even stronger inequality. This is the
classical hyperbolic Jung argument, also stated as Theorem 17 of
Baguley–Maus–Ruff–Skretas, STACS 2025, doi:10.4230/LIPIcs.STACS.2025.13,
which cites Dekster's theorem.

The enclosing disk has pseudohyperbolic radius rho=tanh(rho_h/2) and center
alpha in the disk. Therefore

    1/(1-rho^2) <= G = (1+sqrt((3+K^2)/(3*(1-K^2))))/2.

Now let f=sum a_k z^k and g=sum b_k z^k satisfy |f|<=|g| in the annulus.
The quotient omega=f/g has removable singularities there and maps to the
closed disk. The constant or boundary cases are immediate, so assume the
image is in the open disk. Set F=f-alpha*g and H=g-conj(alpha)*f. On |z|=r,
|F|<=rho*|H|, and coefficient by coefficient

    |H_k|^2-|F_k|^2=(1-|alpha|^2)(|b_k|^2-|a_k|^2).

For Y(r^2)=sum_{k>=1, |a_k|<|b_k|} (|b_k|^2-|a_k|^2)r^(2k),
Parseval and the displayed identities give

    Y <= M_H(r)^2/(1-|alpha|^2)
      <= (M_g(r)^2-M_f(r)^2)/(1-rho^2)
      <= G*(M_g(r)^2-M_f(r)^2).

The first inequality merely drops the negative |F_k|^2 contributions and
adds nonnegative |H_k|^2 terms. There is no restriction that alpha be real,
and alpha may depend on r. This is precisely the coefficient estimate
required by Wikström's unchanged moment-duality Lemma 3.1, with beta=1-1/G.
The moment lemma's elementary proof is recalled in NOTE.md.

For t=r^2, write y=sin(pi*log(t)/(2*w))^2/X and H=3*y*(2+y). Then

    g(t)=1/G=2*sqrt(H)/(sqrt(H)+sqrt(H+4)).

This is increasing in y. For t in [R,1], delta=1-t and
U=-pi*log R/(2*w)<sqrt(6), elementary log and sine bounds give

    y >= a*delta^2,
    a=(pi/(2*w))^2*(1-U^2/6)^2/X >0.

Indeed -log t>=delta, |pi log t/(2*w)|<=U, and sin v>=v-v^3/6 for v>=0.
Thus g(t)>=l*delta on [R,1], where any positive rational l below

    2*sqrt(6*a) /
      (sqrt(3*a*(1-R)^2*(2+a*(1-R)^2))
       +sqrt(4+6*a*(1-R)^2+3*a^2*(1-R)^4))

is valid. The numerator was bounded below and denominator above separately.
Both exact checkers must independently enclose these constants, all atomic
g(t_j), both finite moment families and both infinite tails. The linear
integral is exact: l*((1-R^(k+1))/(k+1)-(1-R^(k+2))/(k+2)).
