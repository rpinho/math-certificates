# Exact degree powers in the completed disjoint certificate

Candidate and unrefereed. The verifier is separately written (same agent).
Credit Harry Kesten, Iwan Jensen, I. G. Enting, Michael Fekete, Numaro and
Vít Plánočka as in the parent packets' CREDITS.md and retained MIT license.
This uses their completed fresh native enumerations; it does not verify or
use Numaro's original enumeration as a numerical premise. No novelty
judgment, separate authorship, refereeing or formal acceptance is claimed.

Use precisely the completed disjoint family's decomposition F+G+E:
F contains main spans1–17, G main span18, E range22/cap5 spans19–30.
These are finite polynomials with nonnegative integer coefficients.
The pinned parent certificate establishes, at b=M/2^27, M=51081913,

    F(b)>=L17, G(b)>=L18>=0, E(b)>=e>=0,
    F(c)<=U, c=51082227/2^27,
    deg(G)<=1296, deg(E)<=690.

All quantities and memberships have already been proved and fully replayed.
The positive lower e bounds the genuine higher-span family; it is not a
coefficientwise subtraction of the two different rectangle range families.

Let 0<k<M, a=(M-k)/2^27 and r=a/b=(M-k)/M, so 0<r<1.
For each n<=N, r^n>=r^N: indeed r^N=r^n*r^(N-n), and0<r^(N-n)<=1.
For any nonnegative coefficient polynomial H of degree at most N,

    H(a)=sum_n h_n*b^n*r^n >= r^N*sum_n h_n*b^n=r^N*H(b).

Thus G(a)>=r^1296*L18 and E(a)>=r^690*e, using nonnegative multipliers.
The parent's explicit power-by-power secant proof gives
F(a)>=(1+k/314)*L17-(k/314)*U. Adding proves

    (F+G+E)(a) >= (1+k/314)*L17-(k/314)*U
                       +r^1296*L18+r^690*e = S(k).

The frozen certificate uses k=1353 and stores S(k) as one exact reduced
rational. The verifier requires its numerator>=denominator, and checks
the exact reciprocal mu=2^27/(M-k)=8388608/3192535>1051/400. The parent's
explicit irreducible-factor concatenation and SAW-series argument therefore
gives this candidate lower bound and the requested renewal bar. The full
expanded integer coefficient vector remains unmaterialized; its finite
family is unchanged, with exactly defined nonnegative integer counts.

The producer evaluates integer powers by repeated squaring on numerator
and denominator, then combines exact rationals and bisects a finite grid.
The separately written (same agent) verifier validates the pinned parent,
all actual native outputs, and27actual exact-code parent controls. It derives
L17,L18,U,e and the two degrees from those checked inputs, uses Fraction
powers and a different term order, and compares the entire claimed rational.
It also checks k+1 fails this sufficient inequality. S(k) is nonincreasing:
its secant part has slope-(U-L17)/314<=0, and both nonnegative degree-power
parts decrease as k increases. The next-step check is limited to this fixed
family, enclosures and sufficient inequality; it gives no upper bound on mu.
Inputs/proof/producer/verifier/test source freeze before checking. Actual
corruptions must each produce their exact expected rejection.
