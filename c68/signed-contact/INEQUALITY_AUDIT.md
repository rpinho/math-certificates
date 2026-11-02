# Where the contact-moment proof loses slack

Unrefereed analytic audit. Exact numerical claims refer to the frozen artifacts
and independent Arb verifier. Earlier floating geometry diagnostics are leads,
not impossibility results. The chain was read in INPUT_GREEN_FLUX.md,
INPUT_ANGULAR.md and the preceding contact/outer-factor proof, together with
the adversarial review in ../review_c68.

| Step | Inequality or identity | Loss and disposition |
|---|---|---|
| Annular Green versus strip lifts | G_ann >= sum of finitely many distinct lift Green functions | Discards other positive lifts. Retained. Distinctness matters: repeated lifts would invalidate it. Compact exhaustion and the positive remainder are explicit in the input proof. |
| Strip Green lower bound | -log delta >= (1-delta^2)/2; denominator <= (|Z|+|B|)^2 | Both can lose slack. Retained. Earlier near-extremal diagnostics put their practical scale far below the requested gain; this is not a certified limitation. |
| Uniform flux kernel | sech^2(u)+sech^2(A-u)>=2 sech^2(A/2) | Replaces angular/radial dependence by a uniform lower bound. Retained; convexity hypotheses are rechecked for the new c. |
| Period constraint | |sin pi F|<=pi|F| and sine subadditivity | Loses cancellation and integer-distance information among other zeros/harmonic flux. Retained. The flux congruence itself is exact, and the Poisson normalization is correct. |
| Pairwise conversion | exp(2E)>=1+2E and positive cross terms dropped | Genuine positive loss, retained. Earlier geometry tests indicate small headroom, without an upper-bound theorem. |
| Fourier majorant | L(theta)<=sin^2(theta/2)-kappa(1-cos 2theta) | Replaces the sharp peaked profile by two harmonics, with conservative sufficient scalar hypotheses. Retained with kappa=3/25; all four hypotheses pass at the new c. |
| Smallest disk contact balance | Hyperbolic cosine-rule contact averages | Exact identities; no slack. Domain contact preimages need not be the image's central angles. |
| Squared radius gap | zeta^2<=h*zeta; zeta^2<=h^2 | Loses the distinction between the actual enclosing radius h and the point radius zeta. Their maximum gives W=max(S,T). Retained. A future proof could keep the unsquared h*zeta constraint jointly. |
| Denominator in v-g | H+zeta<=2H and 1+zeta<=1+H | Loses a nonlinear favorable correction when W is appreciable. Retained, so all changes below are isolated from flux/diameter estimates. |
| Earlier contact scalar reduction | Re(e^(i theta) conjugate(m1)) >= -|m1| | **Main repaired loss.** This simultaneously replaces a harmonic by its minimum at every angle. It forgets that it changes sign under theta->theta+pi. The new lemma retains it, including its relative phase with m2. No contact-PSD constraint is needed. |
| Earlier even outer factor | Keep C0 U0 and C0 U1 because C1=0 | The even minorant was convenient but expensive. The new outer factor need not be even; keeping C0 U0 and C0 U1+C1 U0, then completing a square, yields C0^2/(1+|C1/C0|^2) times |U1|^2. This sacrifices the constant correction, which the norm argument never needed. |
| Remaining outer coefficients | Parseval drops all terms from degree 2 onward | Still loses slack. Retaining them at the same diagonal constant is false: see the exact counterexample below. A positive matrix inequality could retain cross terms. |
| Coefficient selection | |U_k|^2>=(1-|alpha|^2)y_k, plus discarded nonselected terms | Retained and valid coefficient by coefficient, including the linear one used for the new correction. It does not assume signs of the original analytic coefficients. |
| Moment criterion | Require every ordinary lower moment and weighted upper moment separately | Sufficient conditions, not necessity for the original extremal problem. No framework optimality is claimed. This job changes its analytic input, not merely the LP mesh. |
| k=0 | Probability mass one and beta<=1 | Exact sufficient closure. Losing the old favorable y0 correction imposes no additional restriction. |
| k=1 tail | Continuous epsilon contribution discarded | Favorable term discarded for simplicity. The frozen measure has positive margin without it. |
| Tail envelope | Lower bound sin, -log t and increase rationalized denominator | Conservative cellwise lower bound. The new certificate uses 3200 rational cells; its verification integrates their lower envelopes exactly. |
| Infinite-index closure | Last atom for A; one tail interval versus all atoms for B | Discards favorable terms but proves every remaining integer index. No finite-sample extrapolation. |

The signed scalar lemma raises the certified linear-coefficient constant from
7/100 to 19/200. A frozen rational measure then proves the candidate c=0.44685.
Its same-node weighted k=1 condition with the old 7/100 correction is strictly
negative, even after an upper bound for both continuous g and old epsilon is
included. Thus this accepted measure does not pass the earlier criterion.
The independent verifier computes that upper bound using

    g(t)<=sqrt(2)*pi/(w*R*sqrt(Psi))*(1-t),
    epsilon_old(t)<=(7/200)*g(t), R<=t<=1,

because sin x<=x, -log t<=(1-t)/R and the rationalized denominator for g
is at least sqrt(Psi). It integrates (1-t)t exactly. The signed lemma,
rather than an LP-only refinement, is therefore quantitatively necessary
for this particular certificate. This is not an impossibility theorem for
all measures using the old lemma.

## A false third-coefficient extension, with an exact counterexample

The tempting statement

    integral max(S,T)|V|^2 >= (7/100)(|V0|^2+|V1|^2+|V2|^2)

is false. Take the legitimate two-point contact moments m1=0,m2=1 (equal
masses at domain angles 0 and pi). Then S=0 and W=(12/25)sin^2(theta).
Set

    V(z)=1+(3/2)z^2+(9/8)z^4+(3/4)z^6+(3/8)z^8.

Since W=(3/25)|1-z^2|^2 on the unit circle, Parseval gives exactly

    integral W|V|^2 = 87/400 = 0.2175,
    (7/100)(|V0|^2+|V1|^2+|V2|^2) = 91/400 = 0.2275.

The difference is -1/100. To put this at an interior radius r=1/2, use the
entire polynomial U(z)=V(2z), so U(rz)=V(z). The right side then has exactly
|U0|^2+r^2|U1|^2+r^4|U2|^2. `counterexample.json` freezes the example and
`verify_counterexample.py` checks it with independent exact Fraction arithmetic.
This disproves that proposed low-coefficient lemma, not the possibility of a
more careful matrix-valued third-coefficient estimate.
