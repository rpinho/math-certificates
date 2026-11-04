# Span-specific degree extension of the completed finite bridge family

Candidate and unrefereed. The verifier is separately written (same agent).
This uses the exact family and complete native replays of the pinned main
packet, without another enumeration. Credit Harry Kesten, Iwan Jensen,
I. G. Enting, Michael Fekete, Numaro and Vít Plánočka, with the precise
construction attributions in that packet's CREDITS.md and MIT license.

For h=1,...,18 let P_h(z) count the main packet's irreducible bridges of
span h and transverse range at most w_h-1, with translation fixed by the
starting vertex. Write P_h(z)=sum_n a_(h,n) z^n. The main proofs establish
that these are finite polynomials with nonnegative integer coefficients.
Every such bridge has at most h*w_h+1 vertices: the start is the only
vertex on the initial horizontal coordinate, and the h subsequent
coordinates each have at most w_h vertices. Hence its number of edges
is at most N_h=h*w_h. The exact lower values alpha_h in the completed
main certificate satisfy P_h(z0)>=alpha_h>=0, where
z0=M/2^27 and M=51081913. At span18 only the finite final-span argument
is used; no infinite-range span18 upper assertion is introduced.

Choose the positive integer k=40 and put delta=k/M and z1=z0*(1-delta).
Here 0<delta<1. The frozen certificate checks 1-N_h*delta>=0 for every h.
For every nonnegative integer n, Bernoulli's inequality gives

    (1-delta)^n >= 1-n*delta.

For completeness, n=0 is equality. If the inequality holds for n, multiply
by the nonnegative 1-delta and expand:
(1-delta)^(n+1)>=(1-n*delta)*(1-delta)
=1-(n+1)*delta+n*delta^2>=1-(n+1)*delta. Induction proves the assertion.
For 1<=n<=N_h it follows that (1-delta)^n>=1-N_h*delta. Therefore

    P_h(z1)
    = sum_n a_(h,n)*z0^n*(1-delta)^n
    >= (1-N_h*delta)*P_h(z0)
    >= (1-N_h*delta)*alpha_h.

The second inequality uses the explicitly checked nonnegative multiplier.
Let L=sum_h alpha_h and T=sum_h N_h*alpha_h. Summing the preceding
inequalities proves

    P(z1)=sum_h P_h(z1) >= L-(k/M)*T = S.

The certificate supplies L,T,S as exact reduced rationals, and acceptance
requires S>=1 by integer comparison. The same exact, nonnegative integer
coefficients as in the main packet thus satisfy the finite renewal bar at
z1=51081873/134217728. The main packet's explicit unique-factorization,
concatenation and SAW generating-series argument applies verbatim, giving

    mu >= 134217728/51081873.

This is greater than 1051/400: 400*134217728-1051*51081873=42677>0.
Its decimal is diagnostic only. The expanded integer coefficient vector
remains unmaterialized; the family and exact value enclosure are certified.

The producer chooses k by exact integer division of M*(L-1)/T and freezes
the result before running the separately written (same agent) checker.
The checker reassembles the pinned main packet's alpha_h, confirms its
completed full replay receipt against every actual fresh span output,
and recomputes the weighted sum and all comparisons using Fraction.
It requires k+1 to fail this same linear sufficient inequality. That is
only an optimality check within this fixed sufficient inequality and
dyadic grid; it is neither an upper bound on mu nor a search exclusion.
Actual corrupted fixtures exercise each specified rejection code.
