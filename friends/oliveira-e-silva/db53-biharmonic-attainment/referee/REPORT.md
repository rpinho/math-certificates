Independent referee result: HOLDS, by analytical audit with independent exact algebra controls. This is not a proof-assistant certificate. No claimant code was imported or executed. The audited INPUT_PROOF.md has SHA256 03f23a2ebddfa8ef9bd26c481c730562ec3f655cf92ab0426e56575fd2fb6cf3, matching the frozen MANIFEST.json entry.

The [version of record](https://link.springer.com/article/10.1007/s00526-023-02654-9) identifies Mandel and Diogo Oliveira e Silva as authors, uses complex inputs and the stated Rayleigh quotient, proves axial attainment in Appendix C/Theorem 4, and leaves the reflection-even existence issue unresolved. The arXiv version agrees on these points. There is no published numeric best value or empirical hold-out here. The addition relative to that paper is a strict escape-threshold inequality and the resulting reflection-even compactness/attainment for the claimed interval; the nonradiality deduction uses existing estimates. No global novelty or author-interest conclusion is made.

I checked the following functional argument independently. Put L=(Delta+1)^2+epsilon and fix epsilon>0 and 3<=p<4 throughout. The Fourier symbol ((|xi|^2-1)^2+epsilon) is strictly positive and comparable to 1+|xi|^4, with constants allowed to depend on epsilon. Thus q is an equivalent squared H^2 norm and both constrained levels are positive. No small-epsilon argument is used for binding or compactness.

For a complex axial minimizer u=v+iw, q(u)=q(v)+q(w), whereas Minkowski in L^(p/2) gives ||u||_p^2<=||v||_p^2+||w||_p^2. Combining these with the definition of the complex infimum forces every nonzero real component to have the same minimal quotient. Select a real component, normalize its Lp norm to one, and denote it by w and its level by m. Averaging tests over O(2) proves Lw=m|w|^(p-2)w against arbitrary tests; it is not merely an equation on the symmetry subspace.

H^2(R^3) embeds in bounded continuous functions vanishing at infinity. Hence V=-m|w|^(p-2) is real, bounded and tends to zero. The right side of Lw=m|w|^(p-2)w is in L2, so ellipticity gives w in H4. The self-adjoint operator L+V has eigenvalue zero, strictly below the free symbol's range [epsilon,infinity). These hypotheses are exactly alternative (1) of [Herbst–Skibsted I, Theorem 1.1](https://arxiv.org/html/1306.6878v1), also restated in [II, Theorem 1.1](https://arxiv.org/html/1504.07128v2). The potential-derivative conditions in alternative (2) are not required. Therefore some positive exponential L2 weight exists.

Here are details behind the weighted regularity assertion. The interior estimate on each ball B1(c) is

    ||w||_H4(B1(c)) <= C (||Lw||_L2(B2(c)) + ||w||_L2(B2(c)))
                       <= C(1+||V||_infinity) ||w||_L2(B2(c)).

The constant is independent of c. On either ball an exponential radial weight differs from its value at c by a bounded factor. Square the estimate and sum over a bounded-overlap covering. Reducing the available weight if necessary yields exp(b|x|) D^alpha w in L2 for all |alpha|<=4. This argument does not differentiate V or require smoothness of the noninteger nonlinearity.

For |Re lambda|<b, the vertical Bochner integral W_lambda=int exp(lambda z)w(.,z) dz belongs to transverse H4. Cauchy–Schwarz bounds its H4 norm by the weighted derivative norms times the square root of int exp(2 Re(lambda)z-2b|z|) dz. The same estimate works for Lw in L2. On a smaller strip, factors z^j are absorbed by the remaining exponential margin; consequently the transform is holomorphic as an H4-valued function. Cutoffs in z justify integration by parts and give

    int exp(lambda z)Lw dz = ((Delta_xprime+1+lambda^2)^2+epsilon) W_lambda.

For real lambda this is a real, strictly positive transverse quadratic form when paired with a nonzero W_lambda. If W_lambda vanished on the entire real interval, scalarizing the holomorphic function and applying the identity theorem would make it vanish on the strip, including its imaginary axis. Fourier injectivity then forces w=0. Hence some real lambda has nonzero W_lambda. This step covers zero ordinary axial mean, without a nonzero-moment hypothesis.

Let C(s)=(w*Lw)(0,s). Convolution of two L2 functions is continuous and vanishes at infinity: approximate both in L2 by compactly supported smooth functions and use the uniform convolution error bound. Weighted absolute vertical integrals of w and Lw belong to transverse L2 by the preceding estimate. Their product is integrable, so absolute Fubini applies. Transverse O(2) invariance includes xprime -> -xprime. It follows that

    int exp(lambda s)C(s) ds
      = ||(Delta_xprime+1+lambda^2)W_lambda||_2^2
          + epsilon ||W_lambda||_2^2 > 0

for some real lambda. Thus C is positive somewhere. Continuity and decay at positive infinity then give arbitrarily small positive values, without requiring such values at arbitrarily large separations. The ordinary integral need not be positive.

I used a different proof of the scalar inequality. For a,b>=0 set

    F(a,b)=(a+b)^p-a^p-b^p-p(a^(p-1)b+b^(p-1)a).

Both boundary values vanish, and

    F_ab=p(p-1)[(a+b)^(p-2)-a^(p-2)-b^(p-2)] >= 0

for every real p>=3. Indeed, for r>=1 the function (a+b)^r-a^r is increasing in a and is at least b^r. Integrate F_ab over [0,a]x[0,b]. For opposite signs, suppose a>=b>=0. The convex tangent inequality (a-b)^p>=a^p-pa^(p-1)b leaves the nonnegative remainder b^(p-1)(pa-b). Homogeneity, swapping and changing both signs cover all inputs. This proves the required inequality over the whole exponent interval, independently of finite sampling. At p=5/2 and A=B=1 the claimed extension would have remainder 4sqrt(2)-7<0; the stated endpoint p=3 is substantive.

For a_R=w(xprime,z-R), b_R=w(xprime,-z-R), the sum is exactly reflection even. Direct change of variables gives the real q cross pairing I=C(-2R). Both translated profiles satisfy the full Euler equation. Hence each nonlinear cross integral is I/m, q(a_R+b_R)=2m+2I, and the scalar inequality gives ||a_R+b_R||_p^p>=2+2pI/m. Choose x=I/m in (0,1/(2p)). Differentiating 2log(1+px)-p log(1+x) gives p[1+(2-p)x]/[(1+px)(1+x)]>0. Therefore the quotient is strictly below 2^(1-2/p)m. All factors and the sign of lambda^2 agree with the original metric.

The trivial control is a widely separated reflected pair. Its energy tends to 2m and its p-mass to 2, yielding exactly 2^(1-2/p)m. Doubling alone cannot give the strict bound. The positive overlap and the Euler equation give the first-order gain used above; a Gaussian which is not an eigenfunction cannot substitute for that equation.

For completeness, here is the complex compactness argument with the residual specified. Take any Lp-normalized G1 minimizing sequence. It is H2 bounded. The usual local nonvanishing lemma for bounded H1 sequences applies since 3<=p<4<6, and local Rellich gives a nonzero profile after translation. A diverging transverse center is impossible: for any fixed number of rotations, sufficiently large radius gives that many disjoint rotated balls of equal positive local mass, contradicting the bounded global mass. Thus only axial translations are needed, and the resulting profile u remains exactly O(2) invariant.

Write T_t u(xprime,z)=u(xprime,z-t) and Ru(xprime,z)=u(xprime,-z). If axial centers are bounded, a nonzero unshifted G1 weak limit exists. Brezis–Lieb and Hilbert norm splitting give m1>=m1[a^(2/p)+(1-a)^(2/p)], where a=||u||_p^p>0. Strict concavity forces a=1; the energy identity then gives strong H2 convergence.

If |t_n| tends to infinity, evenness supplies profiles T_tn u and T_-tn Ru. The residual

    r_n = u_n - T_tn u - T_-tn Ru

is exactly G1 invariant even for complex u; reflection does not conjugate it. The two translated profiles are weakly orthogonal in the q Hilbert space. Applying Brezis–Lieb successively in the two translated frames gives 0<2a<=1, residual p-mass 1-2a, and

    m1 >= 2mG a^(2/p) + m1(1-2a)^(2/p)
        > m1[(2a)^(2/p)+(1-2a)^(2/p)] >= m1.

The strict inequality uses m1<2^(1-2/p)mG and a>0; it also handles 2a=1. This contradiction rules out escape. The argument applies to every subsequence, proving relative compactness of the entire minimizing sequence, rather than just existence of one well-behaved minimizing sequence. Compact averaging over G1 proves the full complex Euler equation. Scaling by m1^(1/(p-2)) removes its multiplier.

Finally, substituting d=3 and gamma=2 into the paper's Theorem 1.3 gives m1<=C_p epsilon^(2/p), with radial lower rate epsilon^(1/2) for p>3 and epsilon^(1/2)|log epsilon|^(-2/3) at p=3. The ratio tends to zero for each fixed p<4. This proves the stated nonradiality with a p-dependent cutoff, without a uniform quantitative margin. [Source](https://link.springer.com/article/10.1007/s00526-023-02654-9).

The independent computation is referee_checks.py, run under nice 10 with one BLAS thread on stats. It rebuilds L from Delta^2+2Delta+1+epsilon and integrates polynomial Gaussians using exact normal moments. Four controls pass: odd z, even z^2-1, odd with transverse coupling, and mixed parity with transverse coupling, all multiplied by exp(-|x|^2/2). The first two have W_0=0. Their weighted averages are respectively 2pi^2 lambda^2 exp(lambda^2)(epsilon+lambda^4+1) and 2pi^2 lambda^4 exp(lambda^2)(epsilon+lambda^4+1). At epsilon=1 the odd control has negative C(0) and changing signs; a positive kernel or positive ordinary mean would be false assumptions. The checks also cover the mixed-derivative formula, all cubic sign/order cases, the strict-binding derivative, and exact complex reflection with a conjugation negative control. There are 6,400 scalar and 3,000 splitting numerical stress controls; these are explicitly not proofs of continuous quantifiers. The smallest scalar remainder is about -7.2e-66 at 65-digit precision, consistent with roundoff around cubic equality, within the declared 1e-60 tolerance.

Reproduction from this claim directory: `python3 _codex/friends_podsh.py stats pod_launch.sh 60` transfers only this referee's code and starts the tracked worker; use pod_check.sh to read the log. In an authorized clean pod directory with SymPy/mpmath, `nice -n 10 env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -u referee_checks.py` reproduces the mathematical controls. Source downloads are reproduced by pod_sources.sh. pod_backup contains the executed source, complete log, JSON result and public source receipts; its source bytes should match referee_checks.py.

PRIOR_ART.md and the saved public receipts document bounded comparisons, including the Lenzmann–Weth unrestricted symmetry-breaking result encountered during this audit. Some catalog requests failed or truncated and are recorded as such; no absence or priority proof is inferred. There is no empirical hold-out, fitted gain, PDE optimizer, or hidden test set. The claimant's archived failed draft was disclosed and is not used by the current proof. The strongest remaining objection is that Gaussian identities cannot certify weighted functional analysis or arbitrary complex profile splitting. Those steps are supplied analytically above, not inferred from finite PASS results. A subsequent PDE referee can check these two lemmas directly; that is the next concrete bar.

Closeout: 39 evidence files were copied back, every archived file hash was verified, and the executed referee source matches the local source byte for byte. POD_CLEANUP.txt records all five tracked worker PIDs finished, no audit worker in the process scan, and 70,494 bytes retained under /workspace/ref_diogo_DB51 after temporary downloads and archives were removed. Source evidence remains locally in pod_backup and pod_evidence.zip. The initial free-space gate passed; no infrastructure failure affected the result.
