# Scaled-radius Bloch constraints for the frozen certificate

Candidate and unrefereed. This is an additional necessary-inequality family
for PROOF_C57C_PARABOLIC.md, credited there to Wikström's normalization,
center and Grunsky framework. The complete finite R=0.61230 verification receipt accompanies this packet.
No novelty judgment is made.

Use all the notation and independently proved coefficient caps in that
proof. In particular u=sqrt(1-3s), a=a4=b(s)*x1+i*(3/2)*u*x2,
0<=u,x1,x2<=1, b(s)=2/3-s^2/2. When u=0 select x2=0 as the
representative of the actual tuple: Im(a)=0 by the parabolic lemma and
x2 is then redundant. Every actual normalized function has such a tuple.
For u>0 the representation is unchanged.

Fix rational c in (0,64], rational eta with |eta|<=8 and sigma in {-1,1}.
Put

    B=1/c+4u, r=u/B, tau=eta*r,
    xi=(2tau+i*sigma*(1-tau^2))/(1+tau^2), z=r*xi.

For u>0, 0<r<1/4, |xi|=1, and the ordinary Bloch derivative bound holds
at z. By Cauchy's coefficient formula on |z|=4/5 and |f'|<=25/9,
coefficients of the derivative after its seventh power have tail bounded by

    tail=K*r^8/(1-5r/4), K=(25/9)*(5/4)^8.

The degree-seven derivative polynomial is

    P=1-3s*z^2+4a*z^3+sum_{n=5}^8 n*a_n*z^(n-1).

The triangle inequality gives |P|<=1/(1-r^2)+tail. Therefore

    H(Y)=[(1/(1-r^2)+tail)^2-|P|^2]/r^4 >=0.             (S)

This is a real quadratic polynomial in the same eight unknowns Y as the
area and Grunsky forms. A positive rational multiple may be added to the
quadratic contradiction, since it is nonnegative for every actual omitted
value and every actual normalized function. It does not change the disk
center or eliminate any actual function.

The following formulas remove every division by u before interval
substitution. Write a=A+i*v, v=(3/2)*u*x2, h=r^2*p,
p=-3s*xi^2+4a*r*xi^3, and

    Q(Y)=sum_{n=5}^8 n*r^(n-5)*xi^(n-1)*a_n.

Then P=1+h+r^4*Q and

    H(Y)=H00-2 Re[(1+h)*conj(Q)]-r^4*|Q|^2.             (S2)

For an independently factored expression, put

    J=sigma*(1-eta^2*r^2)/(1+eta^2*r^2),
    E=2eta/(1+eta^2*r^2), so xi=r*E+i*J.

Use 1-3s=u^2, 1+Re(xi^2)=2r^2*E^2,
Re(xi^3)/r=r^2*E^3-3E*J^2 and
Im(xi^3)=3r^2*E^2*J-J^3. Direct expansion of (S) gives

    H00 = 2B^2 +12s*E^2 -8A*(r^2*E^3-3E*J^2)
          +12x2*B*(3r^2*E^2*J-J^3)
          +(3-2r^2)/(1-r^2)^2
          +2K*r^4/[(1-5r/4)*(1-r^2)]
          +K^2*r^12/(1-5r/4)^2 - |p|^2.               (S3)

For clarity, the first term comes from
[2/(1-r^2)-2 Re(-3s*xi^2)]/r^2:
its non-angular part is 2(1-3s)/r^2=2B^2. The remaining
identity [1/(1-r^2)^2-1-2r^2]/r^4=(3-2r^2)/(1-r^2)^2
accounts for the scalar rational term. The two tail terms follow by
squaring 1/(1-r^2)+tail. All denominators in (S2)-(S3) are strictly
positive even at u=0, and every unknown coefficient has a nonnegative
power of r. Thus the expressions and their core-coordinate derivatives
are continuous on the closed parameter cube.

Endpoint justification must be stated separately. For an actual function
with u=0 choose x2=0. Its coefficients s=1/3 and Im(a)=0 are fixed.
Apply the ordinary Bloch bound at radii rho>0, with the same angle rule
tau=eta*rho, then let rho decrease to zero in the normalized expression.
The terms 2(1-3s)/rho^2 and Im(a)/rho vanish exactly. Formula (S3) at
u=0,x2=0 equals that nonnegative limit plus 2/c^2>=0; (S2)'s other terms
have their ordinary continuous limits. Consequently (S) in its canceled
form remains a valid necessary inequality for the selected representative.
For redundant tuples with u=0,x2>0 validity is not asserted or needed:
every actual function is represented by u=0,x2=0 and the complete cover
must include that subset. This distinction is part of the analytic proof.

Discovery code c57c_scaled_bloch.py uses an expanded tau-polynomial H00
and an outer-product Gram. The separate c57c_checker_scaled_bloch.py uses
(S3), the factorization xi=rE+iJ and sparse polynomial multiplication of
Q. It imports no discovery code. All weights and descriptor parameters are
checked exactly; Arb evaluates the whole closed box. The complete cover
checker must check all previous and new leaf forms and every coverage edge.
Value/gradient controls and finite-radius identities are useful diagnostics
but do not replace that exhaustive check or referee review of this proof.
