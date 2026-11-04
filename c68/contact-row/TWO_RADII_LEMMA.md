# Coupled radii: necessary geometry and valid positive mixtures

Candidate analytic work, unrefereed; numerical feasibility not yet asserted.
Credit: V. Patankar for the retained flux lemma, Pinho for the contact and
coefficient construction, Wang for the coefficient approach, Wikström for
positive moment integration. This is the second method required by the sweep.

Fix two radii c<r<s<1 for the SAME annular disk map omega. Let the minimal
enclosing disks of the two image circles have centers alpha,beta and cosh
radii h_r,h_s. Let their balancing probability contact measures be lambda_i
on points p_i and mu_j on points q_j, with domain angles theta_i,phi_j.
Using curvature -1 Lorentz coordinates (cosh R,sinh R*v), balance implies

 sum_i lambda_i P_i=h_r A, sum_j mu_j Q_j=h_s B.

The Lorentz scalar product is bilinear and cosh distance is its value.
Therefore the true contact measures satisfy the exact coupled identity

 sum_ij lambda_i mu_j cosh d(p_i,q_j)
          =h_r*h_s*cosh d(alpha,beta).                 (CR)

This is not an assumption that the two centers or contact phases coincide.

A direct cross-radii upper bound follows already from Schwarz–Pick on the
covering strip. Write u=pi*(log r+w)/w and v=pi*(log s+w)/w in (0,pi),
and reduce the angular difference eta to [-pi,pi]. The half-plane images
have radial ratio exp(-pi*eta/w). Their hyperbolic distance has cosine

 K_rs(eta)=[cosh(pi*eta/w)-cos(u)*cos(v)]/[sin(u)*sin(v)].

Derivation: in the upper half-plane cosh distance is
1+|Z-B|²/(2*ImZ*ImB). Write |Z|/|B|=exp(-pi*eta/w), expand the numerator,
use cos(u-v)=cosu*cosv+sinu*sinv, and simplify. Schwarz–Pick bounds image
distance by this strip distance. Any distinct lift gives a valid bound, so
choosing the representative eta of minimum absolute value is legitimate.
Combining with (CR) gives the necessary coupled constraint

 h_r*h_s*cosh d(alpha,beta)
       <=sum_ij lambda_i mu_j K_rs(theta_i-phi_j).      (NC)

The stronger flux version can replace K_rs only after its unequal-radii
normalization is proved; no same-radius formula is substituted there.

For the same-angle radial transport the upper-half-plane geodesic is the
semicircle centered at zero. Its length is

 R_rs=|log(tan(v/2)/tan(u/2))|,

since the metric along it is dangle/sin(angle). Thus pointwise
d(omega(r e^(i theta)),omega(s e^(i theta)))<=R_rs.
Relative to a single anchor center alpha this implies

 cosh d(omega(s e^(i theta)),alpha)
    <=cosh(arcosh(cosh d(omega(r e^(i theta)),alpha))+R_rs).

If the anchor row weight is W and its upper squared distance is H²-DW,
the transported upper distance is obtained by this explicit increasing
function. This is a valid joint constraint on the same map, although the
transported anchor contacts need not be balancing contacts of the second
disk. They must not be mislabeled as such.

Individually established coefficient inequalities C(t), C(u), at t=r²,u=s²,
may always be added with nonnegative weights a,b:

 a X(t)+b X(u) <= sum_k [a beta(t)t^k+b beta(u)u^k
       -1_(k=1)(a epsilon(t)t+b epsilon(u)u)] y_k.     (PM)

Their separate centers disappear before this addition. If there is no extra
use of (CR)/(NC) or the shared-center transport, optimizing all such positive
mixtures is EXACTLY optimizing a positive measure: a delta_t+b delta_u.
It therefore cannot improve the best existing moment LP merely by naming
two radii. Any claimed gain from identifying distinct centers without justification is invalid.
The second-method screen will distinguish genuine coupled constraints from
this measure reparameterization and record any failure explicitly.

For a genuine shared-center version anchor at r, use the proved row weight
W and h(theta)<=sqrt(H²-DW). Put R=R_rs and

 Z=H*cosh R+sqrt(H²-1)*sinh R,
 g_s^tr=2/(1+Z), Q_s^tr=D*cosh R/[H*(1+Z)²].

The transported weight is at least g_s^tr+Q_s^tr W. Indeed differentiate
2/[1+cosh(arcosh sqrt(H²-DX)+R)] in X. Its derivative is

 D*(cosh R+h/sqrt(h²-1)*sinh R)/[h*(1+h*cosh R+sqrt(h²-1)*sinh R)²]
       >=Q_s^tr,

because 1<=h<=H and all factors are nonnegative. Integrate from zero to X.
At h=1 use continuity of the increasing function; an unbounded derivative
is favorable. For genuine probability moments the Fourier majorant is
nonnegative, giving T<=1; also S<=1 and J<=a<=1, so 0<=W<=1 and h is real.

This supplies two valid inequalities with one common alpha and one analytic
U=u-conj(alpha)f. Let G=exp(mean log W), d=mean(log W exp(-i theta)),
A=a*Q_r+b*Q_s^tr, V=a*Q_r*r²+b*Q_s^tr*s², M=a*Q_r*r+b*Q_s^tr*s.
The two outer-factor estimates, before square completion, give a lower
bound on their summed correction of

 G*[A*(1+|d|²)|U0|²+2 Re(d*M*U0*conj(U1))+V*|U1|²].

Minimizing over U0 gives the valid joint coefficient correction

 E=G*[V-|d|²*M²/((1+|d|²)*A)].                    (SC)

At A=0 define E=0 by continuity. Compared with separately completing the
two squares, the gain is G*|d|²/(1+|d|²)*(V-M²/A)>=0 by Cauchy–Schwarz.
It vanishes when r=s or d=0. This is a true coupled coefficient necessity;
its transport costs and possible variance gain can now be screened in a
paired moment LP. A sampled infimum of (SC) is not a universal certificate.
