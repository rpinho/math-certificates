# Disjoint higher-span supplement to the secant certificate

Candidate and unrefereed. The verifier is separately written (same agent).
Credit Harry Kesten, Iwan Jensen, I. G. Enting, Michael Fekete, Numaro and
Vít Plánočka, with the construction attributions and MIT license retained
by the main and rectangle packets. No original Numaro enumeration is used
as a numerical premise. No novelty judgment is made.

Let P be the main finite family of spans1–18, with each span's transverse
cap, and let F22 count all normalized irreducible bridges with spans18–30,
transverse range<=22, and every interior crossing count at most5. Let
H22 be its span18 part and E its spans19–30 part. Thus F22=H22+E exactly
as nonnegative coefficient polynomials. Let H23 count normalized span18
irreducible bridges with transverse range<=23 and the same crossing cap5.
The inclusion H22 subset H23 preserves each length and orientation:
raising the allowed transverse range changes no other membership rule.
The rectangle proof's difference-of-frame normalization counts each walk
translated to start at(0,0) exactly once, with no reflection quotient.
It is the same normalization as in P.

At b=51081913/2^27 the fully frozen native rectangle replays give

    F22(b)>=lo22/2^96,   H23(b)<=hi23/2^96.

Both are exact directed enclosures. It follows that

    E(b)=F22(b)-H22(b)>=F22(b)-H23(b)
         >=(lo22-hi23)/2^96,
    E(b)>=e=max(0,(lo22-hi23)/2^96).

This subtraction bounds the value of the true nonnegative family E.
It does not define coefficient counts by subtracting H23 from F22;
that different coefficientwise difference need not be nonnegative.

Every member of E has span at most30 and transverse range at most22,
so it has at most30*23+1 vertices including the unique initial vertex.
Its length is at most NE=690. For a=(M-k)/2^27, M=51081913, and a
checked nonnegative 1-k*NE/M, the explicit Bernoulli proof gives

    E(a)>=(1-k*NE/M)*E(b)>=(1-k*NE/M)*e.

The whole family P+E is disjoint: P has spans<=18 and E has spans>=19.
Every coefficient of P+E is therefore an exact nonnegative integer
count of irreducible bridges. Combine the preceding inequality with
the fully proved secant bound, writing its frozen exact values as
L17,L18,U,N18=1296:

    (P+E)(a)>=(1+k/314)*L17-(k/314)*U
               +(1-k*N18/M)*L18+(1-k*NE/M)*e = S(k).

All substitutions have been made with nonnegative multipliers or the
explicit negative coefficient of an upper value. The frozen certificate
requires both linear multipliers nonnegative, S(k)>=1, and the exact
claimed reciprocal mu=2^27/(M-k)>1051/400. The main packet's explicit
irreducible concatenation and SAW-series proof then gives that candidate
lower bound. Since a<400/1051, nonnegative coefficients also establish
the originally requested renewal sum at400/1051.

The full integer coefficient vector remains unmaterialized. The finite
family is specified exactly, with no length truncation beyond its geometry,
and its value is enclosed by exact rational arithmetic. The completed
length24 concrete prefix is a separate, weaker refinement and is not
needed as a numerical premise of this disjoint supplement.

The producer uses an exact single-slope formula and integer division.
The separately written (same agent) verifier first validates the pinned
secant artifact, the complete native main/two-point replays, and their
actual controls. It checks both rectangle artifacts using the frozen
scalar packet checker, their completed native receipts, exact full replay
matches and12actual exact-code corruptions each. It validates the exact
family parameters before using range inclusion and span disjointness,
then assembles the displayed four terms separately. It checks the next
grid step fails this particular sufficient inequality. That failure and
the separate extension-gap stop results imply no upper bound on mu.
The new input/proof/verifier/controls freeze before the final exact check.
