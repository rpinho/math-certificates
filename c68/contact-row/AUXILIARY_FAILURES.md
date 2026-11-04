# Two further falsification controls

Candidate/unrefereed diagnostic proof. Credit the retained contact Fourier
majorant and signed coefficient construction to Pinho, with Patankar's flux
input, Wang's coefficient approach and Wikström's moment integration.

The tempting replacement J=|m1| is false under the same pairwise geometric
relaxation. Use equal domain masses at z1=x+i*y,z2=-x+i*y, where
x=399/401,y=40/401, so x²+y²=1. Then m1=i*y,m2=b=x²-y²,
S=y²+(6/25)(1-b²), and T at BOTH support points equals S. The correct J
is y², since cos(theta-arg(m1))=y at both points, so q0=y² and
J=y*(y²+y)/(1+y)=y². Exact arithmetic gives J<=S<y.

For two antipodal image contacts, each of weight 1/2, choose h²=1+D*L,
where D=1 and L=(1+b)/2-(3/25)[1-(2b²-1)]=1-S. Their distance has
cosh(2rho)-1=2(h²-1)=2D*L, exactly saturating the retained Fourier
pairwise inequality. Thus all hypotheses of that geometric relaxation
hold, but h²=1+D-D*S>1+D-D*|m1|. This refutes the overly strong floor
as a consequence of those algebraic/pairwise hypotheses. It is not a
constructed holomorphic-annulus counterexample and does not refute C68.

The uniform one-coefficient constant 13/100 is also false, even for the
legitimate balanced two-point moments m1=0,m2=1. Here J=S=0 and
W=(3/25)|1-z²|² on the unit circle. Take

 V(z)=sum_(j=0)^12 ((13-j)/13)*z^(2j+1).

The polynomial (1-z²)V has coefficient one at z and coefficients -1/13
at the thirteen powers z^3,...,z^27. Orthogonality therefore gives

 mean W|V|²=(3/25)*(1+13/169)=42/325,
 (13/100)|V1|²=13/100,
 difference=-1/1300.

At the strict interior radius r=1/2 use U(z)=V(2z). This is an entire
polynomial and gives exactly the same weighted integral and r²|U1|²=1.
The frozen rational input is auxiliary_failures.json; verify_auxiliary.py
is separately written (same agent), uses only rational arithmetic, and
requires both exact expected rejection labels. This is a diagnostic
rejection of the two false auxiliary proposals, not a stronger C68 bound.
