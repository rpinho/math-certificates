# Stronger low-coefficient estimate via an outer factor

Work in progress, unrefereed. This file is not a certified numerical result
until its uniform scalar integral bounds have passed interval verification.

Retain the notation and Fourier majorant of ANGULAR_LEMMA.md. The following
replaces only its low-coefficient subsection. Put zeta=3/50 and kappa=3/25.
For all contact moments m_1,m_2, and all analytic U on the disk, we claim

 integral max(S,T(theta)) |U(r exp(i theta))|^2 dtheta/(2pi)
       >= zeta (|U_0|^2+|U_1|^2 r^2).                     (SLC)

Write a=|m_1|, b=|m_2|. If a>=1/4, use S>=1/16>zeta. If
b<=sqrt(3)/2, use S>=2 kappa(1-3/4)=zeta. Otherwise a<1/4,
b>sqrt(3)/2. Set ell=6 sqrt(3)/25 and theta_0=arg(m_2)/2.
The pointwise bound already used in ANGULAR_LEMMA.md gives

 max(S,T(theta)) >= h_a(theta-theta_0),
 h_a(theta)=max(a^2, ell sin^2(theta)-a).

It suffices to prove, uniformly for 0<=a<=1/4,

 exp((1/(2pi)) integral_0^{2pi} log h_a(theta) dtheta) >= 3/50. (GM)

For a>0, h_a is positive, continuous and pi-periodic. Let C be its analytic
outer factor, explicitly

 C(z)=exp((1/(4pi)) integral (exp(i theta)+z)/(exp(i theta)-z)
                                     log h_a(theta) dtheta).

The real part is one half the Poisson integral of log h_a; C is bounded,
and C(0)^2 is the geometric mean in (GM).
The pi-periodicity gives C(-z)=C(z), so C's linear coefficient is zero.
For 0<s<1 apply Parseval to C(exp(-i theta_0)z) U(rz) on |z|=s:
its constant and linear coefficients are C(0)U_0 and C(0)U_1 r.
Let s increase to one. The Poisson integral of the continuous function log h_a
converges uniformly to that function, while U(rs exp(i theta)) converges
uniformly to U(r exp(i theta)) because r<1. Thus the integrals converge to
integral h_a(theta-theta_0)|U(r exp(i theta))|^2. This proves (SLC) from (GM)
without assuming a boundary extension for C's harmonic conjugate. Uniform
Poisson convergence follows directly by splitting the kernel integral into
a small arc, where uniform continuity applies, and its complement, where the
Poisson kernel tends uniformly to zero.
For a=0 the outer factor is explicitly sqrt(ell)(1-z^2)/2, so its constant
coefficient squared is ell/4>zeta. These statements also follow directly by
harmonic conjugation of the displayed Poisson integral.

## Uniform scalar integral certificate

Symmetry reduces the mean in (GM) to (2/pi) integral_0^{pi/2} log h_a(theta).
The independent checker verifies the following two bounds with outward Arb
interval arithmetic, using exact rational parameter endpoints.

For 1/10000<=a<=1/4, use the 70 rational parameter cells [a_l,a_h] in
spectral-cover.json and divide [0,pi/2] into 8192 equal cells.
The checker verifies the cells cover the parameter interval without gaps.
Since sin^2 is increasing on this angular interval,
the lower sum

 (1/8192) sum_{j=0}^{8191}
    log max(a_l^2, ell sin^2(pi j/(2*8192))-a_h)

is a lower bound for the mean for every a in that parameter cell. The checker
requires every such lower sum to exceed log(3/50). It can discard any terms
above a previously chosen safe lower endpoint; it cannot replace a lower bound
by an unrounded approximation. The finite covering includes both endpoints.

For 0<a<=1/10000, put x=sin^2(theta), x_0=a(a+1)/ell, d=x_0/2.
Here x_0<1 and 4ell>(1+a)^2. The polynomial proof in ANGULAR_LEMMA.md gives

 h_a(theta) >= ell(x-d)^2.

The circle mean of log(x-d)^2 is -log 16 for 0<=d<=1: multiply by 16,
write as |z^4-2(1-2d)z^2+1|^2, factor the four roots on the unit circle,
and use the zero circle mean of log|exp(i theta)-zeta| for |zeta|=1.
This last elementary identity follows from the mean-value formula with radius
less than one followed by the integrable logarithmic endpoint limit.

On each x-bin [u,v] in

 [1/1024,1/256], [1/256,1/64], [1/64,1/16],
 [1/16,1/4], [1/4,1/2], [1/2,3/4],

we also have h_a/[ell(x-d)^2]>=gamma_v=1/v-(1/10000)/(ell v^2).
Indeed d<=u, so (x-d)^2<=x^2, and 1/x-a/(ell x^2) decreases on these bins,
as x>=1/1024>2/(10000 ell). Every gamma_v>1. The normalized angular measure
of each bin is p_uv=(2/pi)(asin sqrt(v)-asin sqrt(u)). Thus

 mean log h_a >= log(ell/16)+sum p_uv log gamma_v.

The checker proves this is greater than log(3/50), verifies every rational
side condition above, and handles a=0 by ell/4>3/50.

## Consequence

Replace 9/320 by 3/50 in section 4 of ANGULAR_LEMMA.md:

 epsilon(t)=(3/50) D/[H(1+H)^2]=(3/100)g(t)(1-1/H).

The moment criterion and both infinite-tail arguments are unchanged. Since
Psi>6, H>2, g<2/3 and epsilon<(3/100)g, beta-epsilon remains positive.
