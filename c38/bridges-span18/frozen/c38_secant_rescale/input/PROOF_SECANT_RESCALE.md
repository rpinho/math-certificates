# Two-point secant extension of the same finite bridge family

Candidate and unrefereed. The verifier is separately written (same agent).
Credit Harry Kesten, Iwan Jensen, I. G. Enting, Michael Fekete, Numaro and
Vít Plánočka as specified in the main packet's CREDITS.md and retained MIT
license. This extension uses fresh complete native transfer replays, not
Numaro's original enumeration or its coefficient table.

Let P=sum_(h=1)^18 P_h be the unchanged exact finite polynomial family in
the completed main packet. Every coefficient is a nonnegative integer.
Let b=M/2^27, M=51081913, and c=51082227/2^27. The main certificate gives

    F(b)>=L17,  G(b)>=L18,  F=sum_(h=1)^17 P_h,  G=P_18,

where L17 is the sum of its first17 finite-family alpha_h and L18=alpha_18.
The completed two-point stop artifact gives a full irreducible upper sum
U at c over spans1–17 and every transverse range and length. Its integer
upper potentials prove finiteness. Every path of F is in that larger
family, so F(c)<=U. This remains true although F is finite and the upper
sum is over an infinite family. No full span18 upper assertion is used.

For every integer n>=1 and 0<a<b<c,

    (b^n-a^n)/(b-a)=sum_(j=0)^(n-1) b^(n-1-j)*a^j,
    (c^n-b^n)/(c-b)=sum_(j=0)^(n-1) c^(n-1-j)*b^j.

Each term in the first sum is at most the corresponding term in the
second, since both bases are nonnegative, b<=c, and a<=b. Multiply by
each nonnegative coefficient of F and sum its finitely many terms:

    (F(b)-F(a))/(b-a) <= (F(c)-F(b))/(c-b).

Rearrange with t=(b-a)/(c-b)>0 to obtain

    F(a)>=(1+t)*F(b)-t*F(c)>=(1+t)*L17-t*U.

Both substitutions have the displayed valid signs. This proof uses only
integer powers and exact finite sums; no derivative or numerical estimate
is needed. Choose a=(M-k)/2^27 with 0<k<M. Then t=k/314 exactly.

The span18 finite polynomial has degree at most N18=18*72=1296. Provided
1-k*N18/M>=0, the explicitly proved Bernoulli inequality in the span-degree
proof gives G(a)>=(1-k*N18/M)*L18. Therefore

    P(a)>= (1+k/314)*L17-(k/314)*U+(1-k*N18/M)*L18
          = L17+L18-k*((U-L17)/314+N18*L18/M) = S(k).

Every displayed quantity is an exact rational from the frozen artifacts.
The producer chooses k by integer division of the available exact margin
by the positive linear slope. The separately written (same agent) checker
reassembles the main artifact and the two-point artifact, requires their
complete standard frozen-union native replay outputs and actual exact-code
controls, and computes the three-term lower expression directly. It checks
the multiplier, S(k)>=1, the immediate next-step failure for this sufficient
linear inequality, and the exact claimed reciprocal and target comparison.
The failed next step gives no upper bound on mu and excludes no other method.

By the main packet's explicit irreducible concatenation/SAW-series argument,
S(k)>=1 proves mu>=2^27/(M-k). This point is below400/1051 whenever the
claimed reciprocal exceeds1051/400, so coefficient nonnegativity also gives
the originally requested renewal inequality at that target. The full
expanded integer coefficient vector remains unmaterialized. The coefficient
family and its exact rational value enclosure are unchanged in meaning.
No claim of formal proof-system acceptance, refereeing or novelty is made.
