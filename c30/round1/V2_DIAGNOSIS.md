# Precise checks on the withdrawn v2

Candidate audit, unrefereed. This note does not judge novelty or claim the withdrawn bound false.

The author identifies v1's unjustified concavity inference in v2's abstract comments. The [v3 arXiv Comments](https://arxiv.org/abs/2608.20292v3) explicitly identify two v2 withdrawal causes: the pairing need not make the two cells of a member agree, and the Appendix F argument count tests only arc endpoints. The original packet overlooked these Comments. Both reviewers found no reliance on either failed assertion in our candidate: it permits unequal boundary corrections and uses a uniform whole-contour Rouché bound. These documented causes are distinct from the following reproducible normalization defect.

## Printed normalization error in Lemma 5.11

In the paragraph preceding v2 (27), the printed definition of C_R includes a factor rho^2:

    C_R = rho^2 t s (C_A+C_F-rho C_A C_F)
          / ((1-rho C_A)(1-rho C_F)).

The subsequent proof claims R(z,v) <= C_R |z|^2 on its disc. These two statements are incompatible. C_R as defined is the boundary value of R, rather than the coefficient multiplying |z|^2.

There is an exact rational test within the stated hypotheses. Take t=s=1, rho=z=4/27, u=1/2, v=0, and lambda=16. The disc radius is 16*z^2, so v=0 belongs to it. Its maximal v modulus is 364/729 < omega0=1/2. At this point A(z,0)=27/16; the smaller kernel root for F is v1=1/4, giving F(u;z,0)=27/20. Formula (17) therefore gives R=8/81.

For the printed C_R, nonnegative coefficients bound C_A by A(rho,omega0)=9/4 and C_F by 2. The latter follows from F(1;rho,omega0)=108/(23+3*sqrt(161))<2. The nonnegative series defining R is increasing in both arguments. These bounds give a rational upper bound C_R<1. Thus the printed claim would require R<z^2=16/729, contradicting R=8/81=72/729. The certificate and its separately written (same agent) verifier use the sharper rational upper bound, and reject a corrupted R value.

The appendix `tilt.py` defines `CR` **without** the rho^2 and uses the corrected normalization. Consequently this is an identifiable defect in the written argument, with an apparent repair already in its code. It does not establish that the numerical 10.466425 is false, and it must not be advertised as the author's documented reason for withdrawing it.

## Removed inputs and the candidate's separate route

Exact enumeration agrees with the marginal strip tower on the computed finite range. The removed v2 route also needs an asymptotic tilted family, joint analytic continuation for the marked series, and concentration of the strip profile. The local marked recurrence and numerical evaluations alone prove none of those. In particular, the proof of Lemma 6.7 extends majorants beyond a convergence boundary; that extension needs an analytic argument on a slit neighbourhood, rather than the asserted continuity of the same convergent positive series past its radius. This is an audit concern, not a certified counterexample to the analytic conclusion.

The gate cannot accept the withdrawn v2 limiting-profile theorem as input. The historical withdrawal causes are now recorded correctly; the full removed asymptotic argument has not been repaired here. The separate FIRST_MOMENT_PROOF.md uses a weaker first-moment constraint, rebuilt marginal equations, and a real derivative argument. Its balancing step permits different output profiles, and its Rouché proof controls the complete contour. It does not assert that v2's full limiting profile, concentration, or tilted bound has been verified. Credit remains due to v2 for the marginal/kernel algebra and local algebraic setup.
