# Certificate argument

This is the finite-periodic rectangle construction of **Tomar's Lemma 6.2, following Lin**, applied to the rational atoms supplied here. The candidate is unverified by a third party. `verify_exact.py` is **separately written (same agent)** and imports neither search nor producer code.

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

`finite_instance.py` supplies exact h,N,epsilon and checks this expression exceeds its stated rational claim. Letting N increase proves C47>=q itself; a finite instance realizes any fixed rational target strictly below q. All seven corruption controls test the independent exact verifier on altered data, and are not additional hypotheses in this argument.

Completeness of the floating box enumeration is unnecessary for soundness: every retained rational witness is checked separately. Uncovered parts of the certified union need not be uncovered by the true maximal function; they guide search and are not an upper-bound certificate.



Final exact instance

For the supplied final certificate, C=[0,Px)×[0,Py) has Px=328,944,569,115,789/100000000000000, Py=274626500374759/100000000000000.
Its atomic mass is m(C)=16531017364377/3125000000000, the sum of the 392 positive base masses.
The certified rectangle union has area A=57160787529186565434927719505838181711244340833364808847853/6338253001141147007483516026880000000000000000000000000000, hence q=A/m(C)=57160787529186565434927719505838181711244340833364808847853/33528886534937259000645393217902994011665203200000000000000.
The exact minimum strict witness mass slack is 34802060175181125102274071/129807421463370690713262408230502400000000000000.
The explicit finite instance uses h=2, N=301674819865
and epsilon=34802060175181125102274071/13650669794247065816537359446337126400000000000000; its ratio is 578007958689239466612634605872912728291646694993967246195937507629552189562609757/339042971614074466964801846249032273651166749002975200936439316480000000000000000,
strictly above the rounded claim 17048221231/10000000000. All these quantities are rational.
The general argument above, with N tending to infinity, proves C47≥q.
