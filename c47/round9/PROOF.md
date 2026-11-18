# Certificate argument

This is the finite-periodic rectangle construction of **[Tomar, v5, Section 6, Lemma 6.2](https://doi.org/10.5281/zenodo.23716077), following Lin**, applied to the rational atoms supplied here. A clean-room AI referee on a different model used its own checks and concluded HOLDS; this is AI review, not human review. `verify_exact.py` is **separately written (same agent)** and imports neither search nor producer code.

Let C=[0,Px)×[0,Py) be the half-open fundamental cell, with rational positive periods. Put every supplied atom in this cell and extend the positive atomic measure periodically. Each atom belongs to exactly one cell, including atoms on the left or bottom boundary, so m(C) is exactly the sum of the supplied masses. Write Cbar=[0,Px]×[0,Py] for its closure. A witness gives a box B=[a,b]×[c,d], radius r>0 and rectangle R=[u,v]×[s,t] inside Cbar. The verifier directly counts every periodic translate of each atom in B and sums its rational mass m(B). It checks

    m(B) > 4r²,
    u >= b-r, v <= a+r, s >= d-r, t <= c+r.

For every x in R, the centered square Q(x,r) contains B. Its average atomic mass is therefore greater than 1. If U is the finite union of all witness rectangles, exact slab integration and interval merging give its area A. The periodic candidate ratio is q=A/m(C). The shared edges of adjacent closed witness cells have Lebesgue area zero; they do not change A or any union-area sum. Atomic mass is always counted in the half-open cell C.

For the actual L1-function bound, retain the atoms p_j+(kPx,lPy), for 0<=k,l<N, from an N×N block of the half-open cells C. These are exactly N² copies of each base atom, so their total mass is N²m(C). Let Rmax be the largest witness radius and choose an integer h with h·min(Px,Py)>Rmax. Every atom needed for a witness in an inner cell, at least h cell layers from the block boundary, is retained. For a positive rational epsilon define

    f(z) = sum_{k,l=0}^{N-1} sum_j m_j/(4 epsilon²)
           · 1_{Q(p_j+(kPx,lPy),epsilon)}(z).

Keep each smeared square in full, including any part outside the block. This is a finite nonnegative bounded compactly supported function. Each summand integrates to m_j; overlap does not change the integral of a sum. Thus f is integrable and ||f||_1=N²m(C), with atomic cell mass always taken in the half-open C.

Write delta=min_B(m(B)-4r_B²)>0. Taking epsilon<=1/2 and

    4(2Rmax+1)epsilon < delta

ensures 4(r_B+epsilon)² < m(B) for every witness. For x in the translated R, Q(x,r_B+epsilon) contains all smeared masses belonging to B. Thus Mf(x)>1 throughout the translated witness union in each inner cell. There are (N-2h)² inner cells, so the finite ratio is at least

    q ((N-2h)/N)².

`finite_instance.py` supplies exact h,N,epsilon and checks this expression exceeds its stated rational claim. Letting N increase proves C47>=q itself; a finite instance realizes any fixed rational target strictly below q. All seven corruption controls test the separately written (same agent) exact verifier on altered data, and are not additional hypotheses in this argument.

Completeness of the floating box enumeration is unnecessary for soundness: every retained rational witness is checked separately. Uncovered parts of the certified union need not be uncovered by the true maximal function; they guide search and are not an upper-bound certificate.




The closing retained-family producer transforms occupied bounds from an earlier witness family using integer periodic copies and nearest periodic continuations of moved atoms. The rational producer freshly recounts box mass, chooses a strictly smaller rational radius, and retains every resulting witness. Its mapping and proposal priorities are not assumptions in this proof: verify_exact.py separately recomputes each supplied box mass and containment. The final certificate is self-contained; its source-family file is needed only to regenerate proposals.


Final exact instance

The half-open cell [0,Px) × [0,Py) has Px=65792295535231/20000000000000, Py=274655344395649/100000000000000, and mass 529089970243997/100000000000000, the sum of the 452 positive base masses. Its exact witness-union area is 22878843460258009274861600625288681562329176839147945011303/2535301200456458802993406410752000000000000000000000000000, so q=22878843460258009274861600625288681562329176839147945011303/13414024367090776613897918866165655414442557440000000000000. Minimum strict witness mass slack is 5544964724257579515302707/25961484292674138142652481646100480000000000000. The finite instance uses h=2, N=333020005938, epsilon=5544964724257579515302707/2730244964481409688451714901784657920000000000000, with finite ratio 211443076519550480268373711401841739495027970445032200793701027082601051542104989/123970540105353714391020257438714119850224408123125640972549257953280000000000000 > 341118263/200000000. Letting N increase proves C47 ≥ q.
