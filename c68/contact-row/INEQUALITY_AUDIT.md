# Which inequality changed, and why the frozen measure uses it

Candidate and unrefereed. Credit V. Patankar's Green/flux lemma, Pinho's
covering-strip/contact and signed outer-factor constructions, Wang's
coefficient approach, and Wikström's positive moment integration. Arithmetic
verification is separately written (same agent); no novelty judgment is made.

The Green/period normalization, two-lift comparison, Fourier majorant with
kappa=3/25, and automorphism coefficient identity are retained. The changed
step is the averaging of contact geometry. The old reduction averaged all
contact pairs immediately and obtained h²<=H²-D*S. At each individual
contact the balancing identity is also exactly h². Retaining every row gives
h²<=H²-D*max_i T(theta_i). The projected first/second moment calculation
then gives max_i T(theta_i)>=J=a(q0+a)/(1+a). The scalar weight therefore
rises from max(S,T) to max(S,J,T), with its actual relative phase retained.

The old outer-factor/Schur-complement construction remains valid for this
stronger weight. The probability moment Gram constraint is used in the
parameter certificate; it does not by itself discard the retained .105
counterexample, whose moments are PSD. The new row inequality changes that
example's constant floor from .0004 to .02. The verified uniform constant
for the new weight is 23/200=.115. No third diagonal is asserted.

All other moment inequalities retain Wikström's form. The global cubic
continuous-tail minorant simplifies arithmetic; an alternate 5000-cell
minorant also passes. This change of integration implementation is not the
source of the analytic gain.

There is a strict same-measure check of the gain at c=447/1000. Let beta=1-g,
epsilon_new=(23/400)g(1-1/H), epsilon_old=(19/400)g(1-1/H). The old full
weighted k=1 sufficient margin would be

 B_old=R²/2-sum_j wj beta(tj)tj
              +sum_j wj epsilon_old(tj)tj
              +integral_R^1 [g(t)+epsilon_old(t)]t dt.

For R<=t<=1, the logarithm integral gives -log t<=(1-t)/R.
Writing p=pi/(2w), the checked sine range is positive, and sin x<=x gives
sqrt(sigma)<=p(1-t)/R. The rationalized denominator in g is at least
sqrt(Psi), so

 g(t)<=K_upper*(1-t), K_upper=sqrt(2)*pi/[w R sqrt(Psi)],
 epsilon_old(t)<=(19/400)*g(t).

Moreover epsilon_old=(19/23)*epsilon_new at every atomic node. Since
integral_R^1 t(1-t)dt=(1-R²)/2-(1-R³)/3=:J1, it follows explicitly that

 B_old<=R²/2-sum_j wj beta(tj)tj
        +(19/23)sum_j wj epsilon_new(tj)tj
        +(419/400)*K_upper*J1.

This is precisely the Arb expression recomputed from the frozen rational
measure by verify_measure.py. Its verified upper endpoint is less than
-0.00003324623828. The new sufficient margin, even after discarding the
favorable continuous epsilon_new contribution, exceeds 0.000003854649777.
Thus this particular accepted measure fails the preceding .095 criterion,
including its full continuous correction. The new row input is quantitatively
used; this is not scalar-.095 LP polishing. No statement about the best
possible old-criterion measure, the best two-radius method, or optimal C68
follows from this comparison.
