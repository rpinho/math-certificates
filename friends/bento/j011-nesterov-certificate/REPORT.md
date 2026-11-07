Independent referee result: the stated universal theorem verifies exactly.
The squared-distance upper factor is 3599/5000=0.7198, an improvement of
1/5000 over the same algorithm's 2018 analytical upper factor 18/25.
The distance factor is its square root; there is no metric substitution.
[Primary paper](https://www.jbento.info/papers/nesterov_sdp.pdf), equations
(25)-(26), Algorithm1 and Theorem7, and the
[author's publication page](https://www.jbento.info/) establish the baseline
and José Bento's identity. The starting-pair convention differs only by an
index shift. Source baseline matrices and all 15 relevant principal minors
were independently reconstructed at kappa5,13,25,41.

The independent checker reads only certificate.json, SHA256
651ce2bf58ca9cfdf1732aa357f335709de93928ce8fb035aaef69e747df3f6f.
No claimant search, reconstruction, verifier, or baseline code was read or
imported. The proof and coefficient data were read as the submitted claim.
The public 2018 method code was inspected after the independent checker
had been written and run.

For a direct derivation of the necessary interpolation inequality, put
h(x)=f(x)-mu||x||²/2. Convex (L-mu)-smooth h obeys
h_i-h_j-grad(h_j)·(y_i-y_j) >= ||grad(h_i)-grad(h_j)||²/[2(L-mu)].
Multiplication and substitution give the quadratic used in independent_check.py.
This is also consistent with the interpolation theorem in
[Taylor–Van Scoy–Lessard2018](https://proceedings.mlr.press/v80/taylor18a.html).
The algorithm recursively supplies every query vector; the optimizer is
included with zero query, gradient, and function value.

Exact python-flint arithmetic checks the multiplier signs, P symmetry,
all function-coefficient equalities, and all positive residual function
coefficients. Exact LDL elimination has 35 positive pivots for storage
and 36 for decrease. This differs from the claimant's rational-congruence
and diagonal-dominance procedure. No floating-point test decides acceptance.
Moreover, exact LDL proves V-(1/1000000)I positive definite.

These checks yield W_t >= 10^-6||x_t-x*||² and W_{t+1} <= q W_t.
The finite look-ahead window does not introduce a convergence assumption:
||grad f(y)|| <= ||y|| and the recurrence bound every one of its first
33 gradients by a finite multiple of the initial-pair norm. The resulting
exact rational initial bound and explicit uniform K are saved in
pod_evidence/independent_result.json; K is approximately3.11746e43.
The constants are independent of the function and finite dimension.
Scaling f by1/L handles arbitrary positive L. No useful finite-time gain
or optimal factor is proved.

Adversarial checks rejected negative interpolation weight, broken function
cancellation, and zero/noncoercive quadratic storage. An independent exact
analysis of every scalar quadratic curvature in[1/25,1] gives worst squared
spectral factor441/625=0.7056. Orthogonal diagonalization covers positive
definite quadratic objectives of any finite dimension. This is a necessary
lower bound and a quadratic-only result, not an all-function upper bound.
It therefore does not refute the nonquadratic theorem. In the basic
fixed-rho off-by-one frequency test, the exact minimum is0 at q18/25,
but negative at q3599/5000. Thus that simple matched control cannot explain
away the improvement as numerical baseline tolerance. See
pod_evidence/off_by_one_control.json.

There is no training/evaluation dataset or hold-out. Parameter and history
selection do not compromise an exact theorem valid for every objective in
the stated class. I found no evidence of a hidden evaluation or data claim.

PRIOR_ART.md records the current sources and incomplete coverage. The
published 2018 interpolation framework already contains the method family.
The [October2026 exact-rate paper](https://arxiv.org/abs/2610.15125) treats standard momentum; its reported
optimal factors are not beaten on matching parameters by this claim.
The addition relative to the primary paper is one exact fixed-kappa bound,
not a new optimization algorithm, method, or all-kappa formula. No novelty,
priority, or author-interest judgment is made.

Reproduction (all scientific computation on mscr): from this claim directory,
run `python3 transport.py certificate.json independent_check.py baseline_and_controls.py prior_comparisons.py`.
Then use the authorized friends_podsh.py helper with launch_check.sh,
launch_controls.sh, and launch_prior_comparisons.sh, followed by poll scripts.
Each launcher uses nohup/nice10 with one-thread numerical-library caps;
PIDs and complete logs are retained. Pod dependencies were Python3.12.3,
python-flint0.9.0, SymPy1.13.3. No SDP solver is required to verify the claim.
`download_artifacts.py` returns the supporting public and derived artifacts
and checks the archive SHA256 before cleanup; RETURN_RECEIPT.txt records it.
Only local editing and small-file transport/extraction ran on the Mini.

Strongest technical objection is that future gradients could hide an
unproved bound on initial storage. The explicit finite-window bound above
closes that gap, at the expense of the enormous prefactor. The next bar is
an exact finite-time comparison that improves the source guarantee with
both prefactors included.
