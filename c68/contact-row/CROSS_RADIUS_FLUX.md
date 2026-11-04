# Unequal-radii flux and a sharper coupled contact necessity

Unrefereed analytic analysis for method 2. Credit V. Patankar's flux lemma;
the strip and contact setup is Pinho's, with Wang's coefficient approach
and Wikström's moment integration retained. No additional C68 bound is
asserted by this file.

Let a,z be arbitrary points in the annulus, phi_b=(log|b|+w)/w, and
s=sin(pi phi_a)*sin(pi phi_z)>0. The retained period proof extends directly
to different radii:

 -log|omega(z)| >= G(z,a)+s*sech²(A/2), omega(a)=0.    (U1)

Here are the needed details. On a compact subannulus, remove the selected
zero a from the Green decomposition of -log|omega|. Each remaining zero b
contributes at z at least K*|sin(pi F_b)|, with
K=sin(pi phi_z)*sech²(A/2), by the all-radii Green lower bound. The harmonic
remainder contributes at least K*pi*|F_h|>=K*|sin(pi F_h)|, by the same
inward Poisson derivative argument. On a zero-free test circle just outside
|a|, the remaining flux sum is congruent to phi_a modulo one. Subadditivity
and integer periodicity of |sin(pi x)| therefore give K*sin(pi phi_a).
The evaluation radius |z| need not equal the test-circle radius. Increase
the compact subannuli to the given annulus, as in the retained proof.
If z is a zero the inequality is automatic; otherwise all quantities have
their usual finite limiting values. A disk automorphism supplies the zero
for any nonconstant disk-valued omega, as before.

Write u=pi*phi_a, v=pi*phi_z, Delta=u-v and e=1-cos Delta>=0. For two strip
lifts with vertical separation corresponding to angle eta, direct substitution
in the half-plane cross ratio gives

 delta_strip^-2-1 = 2s/[cosh(pi eta/w)-cos Delta].

Choose the two distinct adjacent lifts and put x=A*eta/(2pi) in [0,A].
Their two inverse-square terms, together with (U1) and exp(y)>=1+y,
yield the pairwise bound

 cosh d(omega(a),omega(z))-1 <= (2/s)*Phi_e(x),
 Phi_e(x)={2/[cosh(2x)-1+e]+2/[cosh(2(A-x))-1+e]
                                      +2sech²(A/2)}^-1. (U2)

For completeness, the product of the two strip inverse squares is at least
one plus the sum of the two displayed nonnegative increments. The flux
factor contributes at least 2s*sech²(A/2) to the full inverse square minus
one. Dropping their nonnegative cross terms gives the denominator in (U2).

There is a useful exact comparison with the old same-radius profile. Set
C1=cosh(2x)-1,C2=cosh(2(A-x))-1,h0=sech²(A/2). For e>0, define
b_i=2/(C_i+e), so Phi_e=1/(b1+b2+2h0). Differentiation gives

 dPhi_e/de=Phi_e²*(b1²+b2²)/2<=1/2.

The inequality follows from b1²+b2²<=(b1+b2)² and
Phi_e*(b1+b2)<=1. Integrating from zero and using continuous endpoint
limits at x=0,A gives Phi_e<=Phi_0+e/2. Thus the already certified Fourier
majorant F(eta)=(1-cos eta)/2-kappa*(1-cos(2eta)) gives

 cosh d(omega(r e^(i theta)),omega(s e^(i psi)))-1
       <=(Psi/[sin u sin v])*F(theta-psi)+e/[sin u sin v]. (U3)

This is much sharper than the strip-only cross-radius constraint and does
not substitute a same-radius formula at unequal radii without justification.

Let m_j(r),m_j(s) be the TWO true balancing contact measures, and h_r,h_s
the cosh enclosing radii. Their Lorentz identity from TWO_RADII_LEMMA.md,
followed by averaging (U3), proves the joint analytic necessity

 h_r*h_s*cosh d(alpha_r,alpha_s)
 <=1+sqrt(D_r D_s)*[1-Re(m1(r)*conj(m1(s)))
                   -2kappa*(1-Re(m2(r)*conj(m2(s))))]
             +e/[sin u sin v].                      (NC2)

No equality of centers, image directions, or domain contact angles is imposed.
The exact same construction also bounds the whole second circle relative
to the first center by averaging over its anchor contact measure.

This necessary constraint alone does not remove the retained relaxed .105
moment obstruction. Set m1(r)=m1(s)=a real, m2(r)=m2(s)=1 and choose equal
centers in the relaxed algebraic model. Put K=(Psi/2)*(1-a²)>0 and
h_i=sqrt(sin²(u_i)+K)/sin(u_i), the old scalar floors. Then (NC2) reduces to

 sqrt((sin²u+K)(sin²v+K))<=sin u sin v+K+e.

Both sides are positive. Subtracting their squares gives exactly

 K*[2e-(sin u-sin v)²]+2e*sin u*sin v+e²>=0,

because (sin u-sin v)²=4cos²((u+v)/2)sin²((u-v)/2)<=2e.
Thus this cross-moment relaxation admits those bad moments for EVERY pair
of radii. They are not realizable balanced contacts at m2=1,a>0; the row
condition from method 1 supplies the missing exclusion. This is a specific
failure of this proposed coupled necessary relaxation, not an impossibility
theorem for all two-radius approaches or for C68.
