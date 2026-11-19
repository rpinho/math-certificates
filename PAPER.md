![Terence Tao's optimization constants: new bounds](assets/banner.png)

# Math certificates: the full record

**AI for Math.**

Part of my AI-for-science work: [biology](https://github.com/rpinho/ai-biology) · [physics](https://github.com/rpinho/ai-physics).

Explicit, machine-checkable bounds on open optimization constants.

Start with the [short retro](RETRO.md): what we did, what broke, what I would do differently and where I think this is going.

## What this is, and what it isn't

Verification levels are defined in [VERIFICATION_LEVELS.md](VERIFICATION_LEVELS.md). Every bound below is L0 as a whole: AI-written proofs, checkers by the same AI agent unless a row says otherwise, AI reviews, no human referee. The C91 finite certificate is L1 (checked by code from a different model), and the C30 finite parts have exact checks written by the same agent, which is L0 under these definitions. External replays by a different party are linked in the C44, C70, C82 and C86 rows.

On Tao's optimization-constants table, 6 of my pull requests are merged (#227, #229, #239, #251, #258, #259) and 17 are open, as of 14 November 2026. The merged values are the older ones; most rows below are newer candidates in open PRs.

Nothing here has been refereed by a journal, and no priority is claimed.

This file puts the full record of every result in one place, for readers and reviewers who want it in a single document. Each section below is copied word for word from the result's own folder in this repository: the claim, the first paragraph of the proof, and the clean-room referee's verdict. The full proof, referee report and prior-art check are linked from each section.

---

# C42: Turán's pure power-sum constant, upper bound

Folder: [c42/volterra-quadratic-knots](c42/volterra-quadratic-knots)

**Status** (from the table in [README.md](README.md))

Bound: C<sub>42</sub> ≤ **0.6863607950**

Previous best: 0.6873358063* on the table (Koshta); 0.68637* in open [PR #302](https://github.com/teorth/optimizationproblems/pull/302) (Bakeas), whose Theorem A this rests on

Status: Unrefereed; mostly certifies the optimum of Bakeas's family. [Tao-table PR #305](https://github.com/teorth/optimizationproblems/pull/305) closed on 13 November 2026: NikosVat's open [PR #327](https://github.com/teorth/optimizationproblems/pull/327) (0.686360751*) is below it, on the same Theorem A. Bakeas checked the bundle and found no error. The earlier 0.6888863712 was [merged 2026-10-26 (UTC)](https://github.com/teorth/optimizationproblems/pull/251), preprint [hexagon:2610.00485](https://hexagonmath.org/2610.00485). No optimality claimed

**Claim** (opening of [c42/volterra-quadratic-knots/README.md](c42/volterra-quadratic-knots/README.md))

### C42 <= 0.6863607950 on Bakeas's Theorem A

Unrefereed. This certifies an upper bound on Turán's pure power-sum constant, 42a in [Tao's optimization-constants table](https://teorth.github.io/optimizationproblems/constants/42a.html).

This is Vasileios Bakeas's method, not a new construction. Theorem A, the residual lemma and the phase construction are theirs ([turan-c42-bound v1.1.0](https://doi.org/10.5281/zenodo.23836302)), building on Harcos's and Biró's finite linearization. Their notes already report about 0.686361 as the floating optimum of this family, so this mostly certifies that value.

New here are the non-uniform grid, 49 rational phases on knots j²/4608, and two error-propagation bounds, an integrated residual estimate and a smaller kernel cap near 0.

Theorem A is stated for knots j/48. Its proof uses only a finite piecewise-linear phase, with |d(u)| ≤ TΛu for Λ the largest slope, so it applies verbatim to these knots. Bakeas confirmed this. It also assumes Re γ ≥ 0. Here a = Re γ = 0.1118, and both programs check a > 0.

The claim is max(T,F) ≤ T = 0.6863607950. Two Arb verifiers give F ≤ 0.6863607743 and F ≤ 0.6863607774.

**Method** (first paragraph of [c42/volterra-quadratic-knots/VOLTERRA_VERIFIER_MATH.md](c42/volterra-quadratic-knots/VOLTERRA_VERIFIER_MATH.md))

Written from Bakeas, turan-c42-bound/NOTES.md (Theorem A, Lemma 3), after
reproducing its new public T=.6865 certificate with both public checkers.
No code from either checker is imported. The new phase optimizer has not
yet been written. This is an unrefereed extension of the computation, not
a new claim about the validity of Bakeas's analytic theorem.

**Review** (opening of [c42/volterra-quadratic-knots/review/README.md](c42/volterra-quadratic-knots/review/README.md))

### Separate AI review: direct Volterra solve

`independent_check.py` imports neither verifier nor the search. It solves the original Volterra equation by Picard iteration, with exact convolution of piecewise-linear interpolants. It's a numerical diagnostic, not an interval certificate.

The only change from the reviewed file is the certificate path on line 17. Run it from this folder with `python independent_check.py volterra`. Needs python-flint, numpy and scipy.

`receipts/` holds its output at N = 73,728 to 2,359,296. The last two give F ≈ 0.6863607440163906 and 0.6863607440081801.

Full record: [Result](c42/volterra-quadratic-knots/README.md) · [Verifier mathematics](c42/volterra-quadratic-knots/VOLTERRA_VERIFIER_MATH.md) · [Adaptation](c42/volterra-quadratic-knots/BAKEAS_ADAPTATION.md) · [Review](c42/volterra-quadratic-knots/review/README.md)

---

# C42: Turán's pure power-sum constant, lower bound

Folder: [c42/biro-explicit-lower](c42/biro-explicit-lower)

**Status** (from the table in [README.md](README.md))

Bound: C<sub>42</sub> ≥ **1/2 + 2<sup>-4096</sup>**

Previous best: >1/2 on the table (Biró 2000, constant not computed)

Status: Unrefereed; an explicit value for Biró's strict bound by his own method, gain about 10<sup>-1233</sup>. Proof and exact checker by one AI agent; two blind AI reviews. [Tao-table PR #310](https://github.com/teorth/optimizationproblems/pull/310) open, not merged. [Independently replayed](https://github.com/teorth/optimizationproblems/pull/310#issuecomment-6717401133) by GitHub user arhancanli on 2026-11-08: all 39 numerical steps hold exactly; the geometric steps were read, not computed ([note](c42/biro-explicit-lower/EXTERNAL_REPLAY.md))

**Claim** (opening of [c42/biro-explicit-lower/README.md](c42/biro-explicit-lower/README.md))

### C42: an explicit value for Biró's strict lower bound

Candidate, unrefereed.

**Claim.** For every n >= 1, R_n > 1/2 + 2^(-4096); hence C42 = limsup R_n >= 1/2 + 2^(-4096).

This makes explicit the strict bound of A. Biró, "An improved estimate in a power sum problem of Turán", Indag. Math. 11 (2000), 343-358 ([author copy](https://users.renyi.hu/~biroand/pdfs/Turan1.pdf)). Biró proved R_n > q for an effectively computable q > 1/2 but did not evaluate q. The method here is his: the first-escape geometry, the summed Newton identities and the attractive fixed point. What this note adds is explicit estimates and one concrete constant. The gain over 1/2 is about 10^(-1233), so it says nothing about where C42 lies.

**Method** (first paragraph of [c42/biro-explicit-lower/LOWER_PROOF.md](c42/biro-explicit-lower/LOWER_PROOF.md))

Candidate, unrefereed. This note quantifies the method of András Biró,
“An improved estimate in a power sum problem of Turán”, Indagationes
Mathematicae 11 (2000), 343–358, DOI 10.1016/S0019-3577(00)80003-8.
It does not claim a new method or a stronger qualitative theorem than
Biró's published result. The first-escape geometry, summing the Newton
identities, and the attractive fixed point below are his ideas. The
explicit estimates and constant in this note are derived here.

**Review** (opening of [c42/biro-explicit-lower/reviews/astra_gpt-6-astra.md](c42/biro-explicit-lower/reviews/astra_gpt-6-astra.md))

**(1) First false or unjustified step: none found.** I checked the entire proof, certificate, manifest and checker; ran the checker successfully; and compared the relevant passages with Biró’s paper and the live table. I found no counterexample or missing hypothesis.

Here is the lemma-by-lemma audit of [LOWER_PROOF.md](c42/biro-explicit-lower/LOWER_PROOF.md). All statements in §§1–7 are conditional on an arbitrary fixed \(n\ge2\), an arbitrary complex tuple with \(z_1=1\), and \(|S_\ell|\le q\) for **every** \(1\le\ell\le n\). No assumption \(|z_i|\le1\) enters those sections.

| Location | Quantifiers and audit |
|---|---|
| **§1, lines 38–74, (1)–(4)** | Identity (1) holds for every \(1\le t\le n\), including \(t=n\) with \(b_n=0\). Identity (3) holds for every \(1\le t\le n-1\). Both generating-function derivations have the correct signs and indices. The bounds follow by the triangle inequality. Formal power series suffice even when some \(|z_i|>1\). |
| **§2, lines 79–132, (5)–(11)** | The first escape \(k\) exists in \(1,\ldots,n-1\). Zero increments and zero partial sums are excluded before they could invalidate the angles. At escape, \(\pi/4<\theta_k<\pi/2\), giving (6) in the stated direction. For every \(0\le j<k\), (7) follows by telescoping successive **norm increases**; it does not require a common projection axis. Summing the stronger projection inequalities gives (8), including the positive initial contribution \(1-r\). Thus \(A>2^{4093}\). Both growth bounds in (10) hold for every \(1\le t\le k\), and their product gives (11). |
| **§3, lines 136–202, (12)–(16)** | “Bad” and “good” refer to indices \(1\le j<k\); the endpoint \(j=k\) is handled separately. The radicand is correct: \(q^2-r^2[1-(r+\eta)^2]=\delta+\delta^2+r\eta+\eta^2/2\). Here \(r+\eta<1\), so substituting the lower bound for \(X\) has the correct direction. In (13), the error from \(X-rA_{j-1}\) is at most \(eA\), since \(\cos\theta_j\le1\). Bad indices contribute at most \(20teA/\eta\). The identities and inequalities in (15) are correct. Recomputing the endpoint and denominator errors gives exactly the coefficients claimed in (16). |
| **§4, lines 206–237, (17)–(20)** | The least \(t_0\in\{0,\ldots,k-1\}\) exists because \(\lambda<1\). The lower bound \(\lambda A>2^{2045}\) excludes \(t_0=0,1\). Polynomial growth gives \(t_0>2^{1021}\). Minimality gives \(A_{t_0}<3\lambda A\), and the subsequent product bound gives \(k/t_0>2^{1022}\), with the correct inequality direction. Since \(A_t\ge\lambda A\) for **every** \(t_0\le t\le k\), (16) yields the uniform error (20), including \(t=k\). |
| **§5, lines 241–309, (21)–(24)** | The nonvanishing and angle induction applies for every \(1\le t\le k\), since \(k\le n-1\). An offending angle forces \(q\ge2\cos(\pi/8)\sin(\pi/8)=r\), a contradiction. The squared-distance inequality gives the stated **lower** bound on \(\cos\beta_t\). The perturbation constants in (22) are valid. The recurrence is iterated only for \(t_0\le t<k\). Taking positive parts before substituting \(w_t\ge1/t\) correctly avoids a sign error when \(g_t-a<0\). The cubic inequality and telescoping direction are correct, giving (24). |
| **§6, lines 316–358, (25)–(28)** | All divisions are justified by established nonvanishing. The weights \(w_j\), \(0\le j<k\), sum to one. The phase discrepancy is at most \(2\sqrt\varepsilon\); the radial discrepancy is at most \(3\varepsilon\). The conversion from complex coefficients to positive weights is valid. Crucially, (27) gives a lower bound on the weighted real part, so subtracting it in the second-moment identity gives the **upper** bound in (28). No unjustified conversion from cancellation to pointwise closeness occurs. |
| **§7, lines 362–400, (29)–(32)** | The established size of \(k\) ensures \(1\le m=\lfloor\sigma k\rfloor<k\) and \(m\ge\sigma k/2\). Raising the growth product to the eighth power gives \(A_{m-1}/A\le(m/k)^{1/8}\), in the correct direction. For every \(m\le j<k\), \(V\le kA\) gives (30). The early part includes \(j=0\). The error is \(79A/2048<A/16\). Finally, (1) actually gives \(\left|\tfrac12C_{k-1}-kb_k\right|\le E\); the triangle inequality then gives (32). Combining this with escape yields the impossible \(r(r-\tfrac12)\le1/16\). |
| **§8, lines 404–415** | Rotation and permutation take every tuple with maximum modulus one to a tuple with first component one, preserving every power-sum modulus. The normalized domain is compact, so its continuous objective attains its minimum. Consequently the pointwise strict bound implies \(R_n>q\). Conversely, dividing a tuple with \(z_1=1\) by a largest component decreases each modulus by \(M^{-\ell}\), establishing equality of the two infima. Hence \(\limsup R_n\ge q\); strict inequality for the limsup is correctly not claimed. |

**External replay** (opening of [c42/biro-explicit-lower/EXTERNAL_REPLAY.md](c42/biro-explicit-lower/EXTERNAL_REPLAY.md))

### External replay

On 8 November 2026, GitHub user arhancanli posted an
[independent replay](https://github.com/teorth/optimizationproblems/pull/310#issuecomment-6717401133)
of the explicit **C42 >= 1/2 + 2^-4096** on PR #310. They used
`inputs/lower_certificate.json` and `LOWER_PROOF.md` at commit `36325fa` and
wrote their own code; they did not read or run `verify_lower_exact.py`.

Their result: they re-derived sections 1 to 8 step by step and found no false
step, and all 39 numerical steps of the parameter chain, (5) to (32), hold
exactly, with every inequality in r = 1/sqrt(2) and cos(pi/8) decided in
Q(sqrt 2). Their red controls were refused, including the claim strengthened
to 1/2 + 2^-4094 with the same auxiliary parameters.

Not checked by computation: the geometric and analytic steps (the projections,
the first-escape angle, the law of cosines, the Cauchy-Schwarz steps and the
compactness argument of section 8). They read each and found no gap, which
they describe as a reading, not a computation. It is not a peer review.

Full record: [Result](c42/biro-explicit-lower/README.md) · [Proof](c42/biro-explicit-lower/LOWER_PROOF.md) · [Review](c42/biro-explicit-lower/reviews/astra_gpt-6-astra.md) · [External replay](c42/biro-explicit-lower/EXTERNAL_REPLAY.md) · [Prior art](c42/biro-explicit-lower/PRIOR_ART.md)

---

# C44: relevant variables in bounded-degree Boolean functions

Folder: [c44/small-degree-classification](c44/small-degree-classification)

**Status** (from the table in [README.md](README.md))

Bound: C<sub>44</sub> < **1.9916994577**; R<sub>4</sub> = 22, R<sub>6</sub> ≤ 107, R<sub>7</sub> ≤ 227

Previous best: 4.3576549226 on the table (mine)

Status: Candidate and unrefereed. [Tao-table PR #294](https://github.com/teorth/optimizationproblems/pull/294) open, not merged. Earlier steps 2.0417086280 (preprint [hexagon:2610.00694](https://hexagonmath.org/2610.00694)), 2.1974348818, 3.9819073803 and 4.1225323803. The earlier 4.3576549226 was [merged 2026-10-26 (UTC)](https://github.com/teorth/optimizationproblems/pull/258) and [independently replayed](https://github.com/teorth/optimizationproblems/pull/258#issuecomment-6625127605) by GitHub user arhancanli on 2026-11-04 (see [c44](c44/README.md#independent-external-replay)). Separately written (same agent) exact checkers; two AI reviews (Claude Opus 5.5 via Claude Science, GPT-6 Astra) found no false step. Rests on published classification premises and our own case searches; no human referee, formalization or optimality claimed

**Claim** (opening of [c44/small-degree-classification/README.md](c44/small-degree-classification/README.md))

### C44 < 1.9916994577: R4 = 22 and classification at small degree (rigorous, round11/frozen_parity/verify_b.py)

Candidate, unrefereed. This certifies an upper bound on C44, the constant in r(f) <= C 2^deg(f), Tao table [44a](https://teorth.github.io/optimizationproblems/constants/44a.html), and the exact value R4 = 22 for the maximum number of relevant variables at degree 4. No human referee has checked this chain. Please read it with suspicion. The asterisk stays.

    R4 = 22,  46 <= R5 <= 50,  94 <= R6 <= 107,
    R7 <= 227,  R8 <= 474
    3/2 <= C44 <= 39449672077327653986659243787 / 19807040628566084398385987584 < 1.9916994577 (rigorous, round11/frozen_parity/verify_b.py)

It updates the earlier 2.0417086280 candidate and rests on the 2.1974348818 argument in [c44-certificate/reed-muller-caps](https://github.com/rpinho/c44-certificate/tree/e44b9b0cc91c656a680854ce341927c5a7b337c4/reed-muller-caps), including its inequality (3) (rigorous, round8/verify_completion_b.py). The lower bound stays at 3/2.

**Method** (first paragraph of [c44/small-degree-classification/round11/frozen_parity/PROOF.md](c44/small-degree-classification/round11/frozen_parity/PROOF.md))

No novelty, priority or public-record claim. This extends frozen_accepted/
without changing it or the earlier rounds. All its explicit published and
inherited premises, and its two exact replays, remain dependencies. The
finite result is accepted only if the new frozen replay passes. The two
implementations were written separately by the same agent; this is not
independent human refereeing or proof-assistant formalization.

**Review summary** (opening of [c44/small-degree-classification/round11/review/astra/ASTRA_SUMMARY.md](c44/small-degree-classification/round11/review/astra/ASTRA_SUMMARY.md))

### GPT-6 Astra review — publication summary

Astra accepted the candidate bound on its published premises and found no unjustified inference affecting it. Fresh accepted-predecessor and final-parity replays passed with 76 and 120 rejections. Both implementations gave zero leaves in all 15 parity cases, 78,066 nodes each. All 184 scalar recurrence rows matched. The inherited round-eight norm-gap statement needs Q != 0, satisfied by all applications. The full portable referee report is REFEREE_REPORT.txt in this folder.

This is a summary prepared for the release, not a replacement referee report. The supplied original markdown, whose workstation links are local, is retained verbatim in the release job's private provenance records. Original markdown SHA256: `509668f80f813300516e7e7a8d98796f72fe2332d71305bbdb6d205e35b00c35`. This is an AI review; no human referee is claimed.

Full record: [Result](c44/small-degree-classification/README.md) · [Proof (round 11)](c44/small-degree-classification/round11/frozen_parity/PROOF.md) · [Review summary](c44/small-degree-classification/round11/review/astra/ASTRA_SUMMARY.md) · [Prior art](c44/small-degree-classification/round11/PRIOR_ART.md)

---

# C70: reverse Brunn–Minkowski constant

Folder: [c70](c70)

**Status** (from the table in [README.md](README.md))

Bound: C<sub>70</sub> ≥ **exp(1/(2e)) > 1.20194336847**; finite witness > **1.20194336**

Previous best: 1 on the table; 1.201927 proposed by V. Patankar

Status: Unrefereed; [Tao-table PR #259](https://github.com/teorth/optimizationproblems/pull/259) **merged 2026-10-26 (UTC)**; two arithmetic checkers by the same AI agent pass; [independently replayed](https://github.com/teorth/optimizationproblems/pull/259#issuecomment-6625128151) by GitHub user arhancanli on 2026-11-04 and in Brendan Byrne's open [PR #326](https://github.com/teorth/optimizationproblems/pull/326) (see [c70](c70/README.md#independent-external-replay)); not formally verified; exhaustive priority and optimality are not asserted

**Claim** (opening of [c70/README.md](c70/README.md))

### Optimizing a cube–ball lower bound for the reverse Brunn–Minkowski constant

[Merged into Tao's optimization-constants table](https://github.com/teorth/optimizationproblems/pull/259)
on October 26, 2026 (UTC). The result remains unrefereed; table inclusion is not expert peer review or formal verification.

Ricardo Pinho · [ORCID 0009-0006-2744-2599](https://orcid.org/0009-0006-2744-2599)

This unrefereed preprint proves the claim
**C₇₀ ≥ exp(1/(2e)) > 1.20194336847** for the dimension-free reverse
Brunn–Minkowski constant for centrally symmetric convex bodies.
A separate finite witness certifies **C₇₀ > 1.20194336**.

Read the [paper (PDF)](c70/paper/c70.pdf) and [TeX source](c70/paper/c70.tex).
The argument optimizes one term in V. Patankar's cube-and-ball construction.
His preceding public proposal, 1.201927, uses dimension 300000 and
cube side / ball radius 13/1000; its unchanged script and our Arb replay
give approximately 1.20192714257250284496.
The new limiting decimal lower endpoint exceeds that witness by more
than 0.000016225897. This is an optimization of the same construction.
See [FINAL_LIVE_CHECK.md](c70/FINAL_LIVE_CHECK.md) for the dated source audit.

The paper is **not peer reviewed and not formally verified**.
Exhaustive priority is not asserted. No optimality over all convex-body
pairs is claimed. The geometric positioning reduction and limiting theorem
are proved in prose; the programs verify the arithmetic comparisons.

**Verification** (opening of [c70/verification/README.md](c70/verification/README.md))

### Verification receipts

Both C70 checkers ran from a fresh extraction of the approved source archive,
without changes to the checkers, certificate or original rejection harness.
Every execution used Python 3.12 with python-flint 0.9.0 and mpmath 1.3.0
through the pinned uv command in the repository README.

`c70_arb.log` and `c70_rational.log` record PASS for the finite witness
above 1.20194336 and the limiting decimal lower endpoint 1.20194336847.
`c70_original_baseline.log` records the unchanged Patankar script;
`c70_arb_baseline.log` records the independent parity-recurrence reproduction.

The original review rejection harness executed unchanged and rejected all
32 combinations, including all 18 C70 combinations. `rejection_controls.json`
contains those C70 receipts, selected from the completed harness output.
No extracted or edited replacement harness was executed. The original harness
also depends on another problem's inputs and is not included in this distribution.

Full record: [Result](c70/README.md) · [Verification](c70/verification/README.md) · [Prior art](c70/PRIOR_ART.md)

---

# C86: Schur–Siegel–Smyth trace constant

Folder: [c86/round5](c86/round5)

**Status** (from the table in [README.md](README.md))

Bound: C<sub>86</sub> ≤ **1.8054939963**

Previous best: 1.8084990* on the table (Koshta); 1.8054956 in open [PR #270](https://github.com/teorth/optimizationproblems/pull/270) (V. Patankar); 1.8070808 in Tomar's preprint

Status: Candidate. 31-auxiliary exact density certificate; separately written (same agent) checkers. A clean-room AI referee on a different model (GPT-6 Astra) wrote its own checks, HOLDS ([referee](c86/round5/referee/)); no human review. [Tao-table PR #298](https://github.com/teorth/optimizationproblems/pull/298) open, not merged; it was first filed at 1.80560940 ([c86/adaptive-cone](c86/adaptive-cone/), preprint [hexagon:2610.00695](https://hexagonmath.org/2610.00695)). The earlier 1.8117251 was [merged 2026-10-18](https://github.com/teorth/optimizationproblems/pull/227), preprint [hexagon:2610.00425](https://hexagonmath.org/2610.00425). [Independently replayed](https://github.com/teorth/optimizationproblems/pull/298#issuecomment-6638029022) by GitHub user arhancanli on 2026-11-04 (see [c86/adaptive-cone](c86/adaptive-cone/README.md#independent-external-replay)); that replay covers the 1.80560940 certificate only. No independent human review or optimality claimed

**Claim** (opening of [c86/round5/README.md](c86/round5/README.md))

### C86: Schur–Siegel–Smyth trace constant

C86 is the smallest limiting trace-to-degree ratio of totally positive algebraic integers: the liminf of the mean of all conjugates, with finite exceptions allowed. The rigorous upper bound is `C86 ≤ 1561194641062402479525057156208744733/864691128455135125642991200018366464 < 1.8054939963`, computed by `verify_linear.py` and replayed by the clean-room referee’s own `referee/referee_check.py` with `referee/cover_check.py`. The fraction is the directly checkable mean T/m of the finite rational density certificate. Smith’s theorem realizes it as a limiting normalized trace; there is no separate extrapolated value.

Compared with V. Patankar’s [PR #270](https://github.com/teorth/optimizationproblems/pull/270), the margin below the displayed 1.8054956 is greater than 0.0000016037 (rigorous, `comparison.py`). The margin below our 1.80560940 currently filed in this PR (#298) is greater than 0.0001154037 (rigorous, `comparison.py`). The margin below the live table’s 1.8084990 is greater than 0.0030050037 (rigorous, `comparison.py`). Cited values are refreshed in PRIOR_ART.md.

The certificate uses 31 auxiliaries (11 with nonreal roots, maximum degree 21), 7,418 rational density nodes and 6,308 positive-density cells. Every auxiliary’s coefficients, weight and list or generation source are in auxiliary-provenance.json. The certificate SHA-256 is `e5fb93f6c31d2e3b38c986ac71c1d076414d680429fb2cbb91db77fb2e12c9d8`.

Two producer checkers and the cover/hash audit pass. A clean-room AI referee on a different model, GPT-6 Astra via Codex, wrote its own checks and returned HOLDS. This is AI review and replay, not human review. The earlier external replay of the adaptive-cone certificate applies only to that earlier value; it is not evidence of an external replay of this certificate. The table asterisk stays.

**Method** (first paragraph of [c86/round5/PROOF.md](c86/round5/PROOF.md))

Let `mu` be the finite positive measure whose density is given by the certificate's exact rational node heights, linearly interpolated on the exact rational edges and zero elsewhere. Let `m=mu(R)>0`, `T=int x dmu`, and let the selected `Q_j` be distinct primitive irreducible integer polynomials with positive leading coefficients. Their roots may be complex. All polynomial arrays in our certificates are constant coefficient first.

**Referee** (opening of [c86/round5/referee/README.md](c86/round5/referee/README.md))

### Clean-room AI referee

GPT-6 Astra via Codex, in a separate commissioned session, wrote its own checks without reading or running the producer’s code. It read the five permitted producer inputs: proof, certificate, report, comparison-bar JSON and auxiliary provenance. This is an AI referee, not a human review. Its verdict is **HOLDS**; see REFEREE.md.

Its own exact/Arb checks cover structure, every auxiliary, normalization, every log integral, the whole closed support and the decimal comparison. The original recorded cover has 131,912 closed leaves over 6,308 support cells. The archived receipts are under receipts/. Fresh release outputs are under ../release_validation/.

The cover checker’s executable code is unchanged; its opening docstring now says “its own” enclosures. The structure checker replaces only the primitive-content calculation using math.gcd with FLINT fmpz.gcd, the same exact integer gcd operation, because the installed static linter misclassifies every math import as floating arithmetic. Its opening docstring also uses the public clean-room description. The original checker hash is retained in the source hashes; the release-adapted checker is freshly replayed. The corruption runner changes its opening description and its certificate path to `../certificate.json`. The referee’s original producer proof input is published as sources/producer-proof.md with portable citations and updated status wording. Original source hashes and all omitted-cover hashes are recorded in ../sources/input-hashes.json and ../sources/omitted-artifacts.json. No new historical isolation claim is created by these hashes.

Full record: [Result](c86/round5/README.md) · [Proof](c86/round5/PROOF.md) · [Referee](c86/round5/referee/README.md) · [Prior art](c86/round5/PRIOR_ART.md)

---

# C82: essential minimum of the Zhang–Zagier height

Folder: [c82/degree104-joint](c82/degree104-joint)

**Status** (from the table in [README.md](README.md))

Bound: C<sub>82</sub> < **0.2519696460**

Previous best: 0.2534449* on the table (mine); 0.2519889614 in open [PR #280](https://github.com/teorth/optimizationproblems/pull/280) (V. Patankar, @vidigoat; v5, which reused four of our denominators), whose v3/v4/v5 certificates, numerator bank, iterated LLL numerator search and closest-vector method this builds on

Status: Candidate and unrefereed; [Tao-table PR #330](https://github.com/teorth/optimizationproblems/pull/330) open, not merged, updated 13 Nov 2026 (earlier versions 0.252404806, 0.2520179248, 0.2519964890, 0.2519923410, 0.2519744488). Six degree-104 denominators and 40 numerators: Doche's five P-factors plus 35 found in this search, which started from the union with #280 v3/v4/v5; no #280-specific factor remains in this certificate; a separate AI referee rebuilt the interval checker from the proof and certificate and reproduced the bound (HOLDS WITH CAVEATS). The earlier degree104-cvp search used two MIT-licensed files from V. Patankar ([notice](c82/degree104-cvp/THIRD_PARTY_NOTICE.md)); the degree104-joint packet uses none of his code, only his public MIT-licensed coefficient data ([notice](c82/degree104-joint/THIRD_PARTY_NOTICE.md)). The earlier degree-44 result, C<sub>82</sub> < 0.253091834 in [PR #301](https://github.com/teorth/optimizationproblems/pull/301), was [independently replayed](https://github.com/teorth/optimizationproblems/pull/301#issuecomment-6628606867) by GitHub user arhancanli; the earlier 0.2534449 was [merged 2026-10-18](https://github.com/teorth/optimizationproblems/pull/229). No independent human review or optimality claimed

**Claim** (opening of [c82/degree104-joint/README.md](c82/degree104-joint/README.md))

### C82 degree-104 joint certificate

This packet gives **C82 < 0.2519696460*** (rigorous interval bound, verify_best.py), a candidate, unrefereed upper bound for the essential minimum of the logarithmic Zhang-Zagier height in Tao's 82a definition. The asterisk stays. Verification level L0 applies to the bound as a whole. The producer verifier was written separately from the search code by the same AI agent lineage. The separate AI referee and its provenance limits are described below.

Under the same definition, the exact certified upper endpoint is below V. Patankar's public [#280 v5](https://github.com/vidigoat/optimization-records/blob/191064e7ccd88718853fe239dfd3890a8dc0fa37/tao/certificates/c82/v5/README.md) printed bound 0.2519889614* by at least 0.0000193154127508999188, and below [our previous packet for this PR](https://github.com/rpinho/math-certificates/blob/dadec7353c435a081befca73888e3ab6cef3134a/c82/degree104-joint/README.md), 0.2519744488*, by at least 0.0000048028127508999188. That previous packet was round 9 of this search. The gap below [our earlier certificate in this PR](https://github.com/rpinho/math-certificates/blob/a12c3622120c39af776902dbe49b6eff97a4d189/c82/degree104-joint/README.md), 0.2519923410*, is at least 0.0000226950127508999188. The gaps below [#280 v4](https://github.com/vidigoat/optimization-records/blob/79ce0dfb211a67ff7e387b58b0d19ff1d6accfba/tao/certificates/c82/v4/README.md)'s 0.2520079724* and [#280 v3](https://github.com/vidigoat/optimization-records/blob/197962c9610f583e9bc56efe37bfb994c1eeb834/tao/certificates/c82/v3/README.md)'s 0.2520591386* are at least 0.0000383264127508999188 and 0.0000894926127508999188, respectively. The exact comparison gaps are computed by certificate_facts.py in receipts/certificate-facts.json: each is the exact printed comparator minus the exact certified upper endpoint, rounded downward. These are deterministic mathematical comparisons, with no predictive score.

**Method** (first paragraph of [c82/degree104-joint/PROOF.md](c82/degree104-joint/PROOF.md))

The claim is C82 <= B < 0.2519696460 (rigorous interval enclosure, verify_best.py), conditional on the mathematical argument below and the trusted exact/ball arithmetic backend. This is a candidate, unrefereed result, verification level L0 for the bound as a whole.

**Referee** (opening of [c82/degree104-joint/review/README.md](c82/degree104-joint/review/README.md))

### Clean-room round-10 referee archive

The referee received only review/inputs/CLAIM.md, review/inputs/PROOF.md and review/inputs/certificates/certificate.json. The input certificate is byte-identical to the packet root certificate. It attacked the reduction and exact hypotheses and wrote its own interval checker without reading or running producer code. INPUTS_SHA256SUMS verifies from review/inputs/.

Verdict: HOLDS WITH CAVEATS. B is enclosed in [0.2519696459872490990419691935079545, 0.2519696459872490990419691935079546], inside the producer enclosure. The exact serving-model ID is unavailable, so model separation cannot be authenticated. AI review does not remove the candidate/unrefereed asterisk. REFEREE.md and PRIOR_ART.md are byte-for-byte originals, including historical live links and initial-status prose.

replay/REPLAY.original.json and replay/REPLAY.json preserve the original receipt. Root REPLAY.json changes input path keys, canonical inputs_hash and checker/report paths, and adds a note. Hashes of input bytes, checker and replay report are unchanged. The preserved logs include development attempts and the completed replays; only the final checker is used for reproduction.

Full record: [Result](c82/degree104-joint/README.md) · [Proof](c82/degree104-joint/PROOF.md) · [Referee](c82/degree104-joint/review/README.md) · [Prior art](c82/degree104-joint/PRIOR_ART.md)

---

# C68: Korenblum's constant in the Bergman space

Folder: [c68/contact-row](c68/contact-row)

**Status** (from the table in [README.md](README.md))

Bound: C<sub>68</sub> ≥ **0.447**

Previous best: 0.432 on the table (mine); 0.446 in open [PR #274](https://github.com/teorth/optimizationproblems/pull/274) (V. Patankar), whose flux lemma this builds on

Status: Candidate and unrefereed; contact-row moment lemma ([c68/contact-row](c68/contact-row/)), separately written (same agent) verifiers, an adversarial AI referee on a different model (GPT-6 Astra) found no defect ([c68/review](c68/review/)). [Tao-table PR #299](https://github.com/teorth/optimizationproblems/pull/299) open, not merged. [Independently replayed](https://github.com/teorth/optimizationproblems/pull/299#issuecomment-6717401424) by GitHub user arhancanli on 2026-11-08: every quantitative hypothesis holds ([note](c68/contact-row/EXTERNAL_REPLAY.md)). The earlier 0.44685 step: preprint [hexagon:2610.00696](https://hexagonmath.org/2610.00696), [c68/signed-contact](c68/signed-contact/). The earlier 0.432 was [merged 2026-10-26 (UTC)](https://github.com/teorth/optimizationproblems/pull/239), preprint [hexagon:2610.00399](https://hexagonmath.org/2610.00399), Zenodo [10.5281/zenodo.23483542](https://doi.org/10.5281/zenodo.23483542). The analytic argument needs mathematical review

**Claim** (opening of [c68/contact-row/README.md](c68/contact-row/README.md))

### Candidate C68 >= 447/1000 = 0.447 (rigorous, verify_measure.py)

**The frozen bar is met by a candidate, unrefereed analytic proof.** The exact
rational artifacts and all quantitative hypotheses pass verification. Both
methods were tried. Verification programs are **separately written (same agent)**;
there is no human mathematical endorsement or formalization, and no novelty
judgment is made.

The candidate is larger than the supplied 8937/20000 baseline by exactly
3/20000 = 0.00015. The written implication is: for every f,u in A²(D),
|f|<=|u| on 447/1000<|z|<1 implies ||f||₂<=||u||₂ (rigorous, verify_measure.py).

Credit first to **V. Patankar** (@vidigoat), [PR #274](https://github.com/teorth/optimizationproblems/pull/274),
for the retained flux and enclosing input; **Chunjie Wang** for the
[coefficient approach](https://doi.org/10.1090/proc/17112);
**Frank Wikström** for [moment integration](https://arxiv.org/abs/2607.17748);
and **Ricardo Pinho** for
the covering-strip, contact and signed outer-factor constructions. Schuster's
annular pseudodistance approach is an antecedent cited in the retained paper.

**Method** (first paragraph of [c68/contact-row/PROOF.md](c68/contact-row/PROOF.md))

Unrefereed computer-assisted analytic proof, 4 November 2026. The programs
verify rational and Arb quantitative hypotheses, not arbitrary prose or
complex analysis. Acceptance verification is separately written (same agent).
No human expert verification, formalization, or novelty judgment is claimed.

**External replay** (opening of [c68/contact-row/EXTERNAL_REPLAY.md](c68/contact-row/EXTERNAL_REPLAY.md))

### External replay

On 8 November 2026, GitHub user arhancanli posted an
[independent replay](https://github.com/teorth/optimizationproblems/pull/299#issuecomment-6717401424)
of the **C68 >= 0.447** candidate on PR #299. They used `PROOF.md`,
`CONTACT_ROW_LEMMA.md`, `certificates/certificate-0447.json` and
`row-cover.json` at commit `09c8423` and wrote their own code; they did not
read or run `verify_measure.py` or `verify_row.py`.

Their result: every quantitative hypothesis holds. The 287-leaf row cover tiles
its box and every leaf holds, with smallest grid ratio 0.11502033 against
z = 0.115 (matching the cover's `proposal_min`). Both moment families hold at
every k; for the integral over [R, 1] they used their own piecewise-linear
lower bound on g instead of this packet's cubic. Their red controls were
refused, and three of them fail at B_1, so the new constant is load-bearing at
k = 1, as `INEQUALITY_AUDIT.md` says.

Full record: [Result](c68/contact-row/README.md) · [Proof](c68/contact-row/PROOF.md) · [External replay](c68/contact-row/EXTERNAL_REPLAY.md) · [Prior art](c68/contact-row/PRIOR_ART.md)

---

# C91: average edit distance of two random binary strings

Folder: [c91/round6](c91/round6)

**Status** (from the table in [README.md](README.md))

Bound: C<sub>91</sub> ≥ **0.265988**

Previous best: 0.216276 in PR #273 (Leandre Jack), whose method this extends

Status: Unrefereed; [Tao-table PR #306](https://github.com/teorth/optimizationproblems/pull/306) open, not merged (it earlier claimed 0.263561, [c91/round4](c91/round4/)). Separately written (same agent) verifier, plus a full independent recheck of the finite certificate by a checker from a different model (finite part L1, whole bound L0); two AI reviews; no second party, no optimality claimed

**Claim** (opening of [c91/round6/README.md](c91/round6/README.md))

### Candidate, unrefereed C91 >= 0.265988

Round 6 records **265988/1000000 = 0.265988**, updating PR #306's previous
claim 0.263561. This remains candidate and unrefereed; no priority or
optimality claim is made.

The canonical-alignment first moment builds on **Leandre Jack's #273**:
https://github.com/teorth/optimizationproblems/pull/273. Earlier canonical
counting includes Ganguly–Mossel–Rácz and Bilardi–Schimd; Lueker and inherited
local rounds 2–5 are also credited. Round 6 adds **4,000 longer exact-DP-verified
forbidden words** and uses **eight even Walsh input-correlation statistics**
on round 5's W=3, B=2, S=0, T=2 gap-debt frontier with a bit-complement
quotient. The bank has 59,550 words of actual lengths 8–16; 21 is only its cap.
The feature family appeared in earlier local rounds; parameter retuning
also contributed, so no numerical gain is assigned solely to one component.

**Verification level: L0** for the whole bound: the universal bridges are
proved only in prose. **Finite component: L1**: an independently written
different-model checker rechecked the exact certificate in full. See
VERIFICATION_SCOPE.md and verification/PROVENANCE.md. This does not assert
external human refereeing or a formal proof.

The independent replay checked 121,332,798 complete representative rows,
499,034,690 edges with multiplicity and 32,774,059 potential classes.
Complement lifting covers 242,665,595 states. Every strict integer majorant
row inequality passed; minimum slack is 4736028943110 over denominator 2^42.
The rational exponent at 0.265988 is strictly positive. Rounding upward to
0.265989 is unsafe. The full independent run took 2141.69722533226 seconds;
it is preserved as hashed evidence, rather than rerun during packaging.

**Method** (first paragraph of [c91/round6/PROOF.md](c91/round6/PROOF.md))

Candidate and unrefereed. The verified numerical instantiation is given below.
Credit Leandre Jack's #273 canonical-alignment first moment; Lueker;
Ganguly–Mossel–Rácz; Bilardi–Schimd; and inherited rounds 2–5. The inherited
round-5 proof is retained as sources/ROUND5_PROOF.md and is an explicit
premise for its unchanged frontier, base rules and bit-complement quotient.

**Reviews** (opening of [c91/round6/reviews/README.md](c91/round6/reviews/README.md))

### Review status

- Astra: ACCEPT; see astra.md for scope and skipped checks.
- CS review: ACCEPT within argument scope; see cs.md (argument referee plus a final-bytes check of the PR text).

Full record: [Result](c91/round6/README.md) · [Proof](c91/round6/PROOF.md) · [Verification scope](c91/round6/VERIFICATION_SCOPE.md) · [Reviews](c91/round6/reviews/README.md)

---

# C89b: Ramsey multiplicity constant of K5

Folder: [c89b/round4](c89b/round4)

**Status** (from the table in [README.md](README.md))

Bound: C<sub>89b</sub> < **0.001648970526**

Previous best: Round 3: 0.001653032; Feinstein–Even-Zohar announcement: 0.001652, no public certificate located that we could check

Status: Candidate and unrefereed; [Tao-table PR #307](https://github.com/teorth/optimizationproblems/pull/307) open, not merged. Two separately written (same agent) exact counters; AI review statuses linked; no human referee

**Claim** (opening of [c89b/round4/README.md](c89b/round4/README.md))

### C89b < 0.001648970526 — round 4 (rigorous exact threshold comparison: scripts/check_cayley_matrix_r4.py)

Candidate and unrefereed. The exact upper certificate has density
15058298592194934908767847/9131939205947984819238469632 (rigorous exact count: scripts/check_cayley_exact_r4.cpp).
It defines a 256-part binary Cayley step graphon with probabilities
0, 2648/4041 and 1. Repeated parts are counted.

- PROOF.md: construction, counting argument, polynomial and prior credit.
- certificates/: selected full matrix, kernel, two-mask definition and optional simpler upper witness.
- scripts/: two separately written (same agent) exact counters, wrappers and controls.
- receipts/: exact totals, acceptance and controls; release_* files are fresh package replays.
- REPRODUCE.md: Python >= 3.10, C++17 and GMP instructions.
- review/README.md: AI review scope and corrections; no human referee.
- PROVENANCE.json, MANIFEST.json and SHA256SUMS: source identity and package integrity.

Written and checked by AI agents under Ricardo Pinho's direction.
No human referee; no priority or optimality claim. See PRIOR_ART.md,
including the Feinstein–Even-Zohar announcement.

**Method** (first paragraph of [c89b/round4/PROOF.md](c89b/round4/PROOF.md))

Candidate and unrefereed. Two separately written (same agent) exact counting implementations agree. They were prepared in one Codex session; both share the same agent authorship, and there is no human referee. No priority or optimality claim is made. See PRIOR_ART.md for the public methods and comparisons.

**Review** (opening of [c89b/round4/review/README.md](c89b/round4/review/README.md))

### Two AI reviews of the frozen round-4 upper candidate

Candidate and unrefereed. Both reviews found no false proof step and returned
**FLAG for wording, decimal presentation or credit**. They are AI reviews,
not a human referee report. No human referee has checked this candidate.
The original read-only reviews are identified by SHA-256 in PROVENANCE.json.

- **GPT-6 Astra:** rebuilt and ran both supplied counters, 36 literal
  comparisons and ten malformed-input controls; the optional seven-point
  polynomial replay also passed. Its additional ordered-tuple count
  reproduced both colour totals and the polynomial. It checked matrix
  symmetry, ranges, masks, equal masses, repetitions, and the normalization
  against PR #307's pinned proposed page. It flagged downward-rounded decimal
  presentations and the omitted Feinstein–Even-Zohar announcement.
- **Claude Opus 5.5 via Claude Science:** used its own exact polynomial
  evaluations at eleven points and a direct CRT count at denominator 4041,
  agreeing separately on red, blue and the total; six small literal-kernel
  controls passed. It did not rerun the supplied counters and could not
  refresh live priority sources. It flagged stale prior-art numbers,
  task-brief wording, decimal rounding, and explicit credit to Jeetu SK ([SK2026]),
  to Ricardo Pinho's work in this PR (#307,
  [Pin2026]) and to its round 3. Its two counting methods were written by that same
  reviewer agent; they are not a further independent review.

Full record: [Result](c89b/round4/README.md) · [Proof](c89b/round4/PROOF.md) · [Review](c89b/round4/review/README.md) · [Prior art](c89b/round4/PRIOR_ART.md)

---

# C89c: Ramsey multiplicity constant of K6

Folder: [c89c/round3](c89c/round3)

**Status** (from the table in [README.md](README.md))

Bound: C<sub>89c</sub> ≥ **0.000033123924116**

Previous best: 0.000025987 (our round 2); about 1.08e-9 from de Caen with R(6,6) ≤ 165; 3e-12 in PR #279 (Jeetu SK)

Status: Candidate and unrefereed; [Tao-table PR #308](https://github.com/teorth/optimizationproblems/pull/308) open, not merged. The finite inequality was [independently replayed](https://github.com/teorth/optimizationproblems/pull/308#issuecomment-6724784525) by GitHub user arhancanli on 2026-11-08 ([note](c89c/round3/EXTERNAL_REPLAY.md)). Exact order-8 flag-algebra certificate, separately written (same agent) exact checkers; two AI reviews; no human referee, no optimality claimed

**Claim** (opening of [c89c/round3/README.md](c89c/round3/README.md))

### C89c round 3: C89c >= 0.000033123924116

**Candidate and unrefereed. No human referee.** Written and checked by AI agents
under Ricardo Pinho's direction. Two AI reviews: Claude Opus 5.5 via Claude Science,
and GPT-6 Astra. Our exact checkers were separately written in one AI session.

The exact bound is `8280981029/250000000000000 = 0.000033123924116`, about 27.46%
above #308's previously printed 0.000025987. The certificate uses ambient order
eight, ordered roots and type families (t,m)=(0,4),(2,3),(4,2),(6,1), with 340
integer-square PSD blocks. The gain comes from enlarged root families, including
six-root types. No genuine nine-vertex product or Ramsey-number input is claimed.
Credit: Razborov, PPSS, KPS, and Jeetu SK's proposed pages in #277/#279; the #279
upper construction is distinct from this lower-bound method. Historical baseline
credit to Conlon, de Caen and Mackey is preserved.

- `PROOF.md`: relevant complete sections of the frozen proof.
- `CERTIFICATES.json`, `certificates/`: selected certificate and unchanged hashes.
- `scripts/`: two separately written exact checkers and selected rejection controls.
- `receipts/`: frozen accepted receipts plus explicitly named `release_*` replays.
- `review/README.md`, `PRIOR_ART.md`, `PROVENANCE.json`: review findings and sources.
- `REPRODUCE.md`, `MANIFEST.json`, `SHA256SUMS`: portable reproduction and integrity.

**Method** (first paragraph of [c89c/round3/PROOF.md](c89c/round3/PROOF.md))

Candidate and unrefereed. These are computational proof candidates, with separate exact implementations; there has been no external human referee review. Standard flag-algebra reasoning is credited to Razborov, PPSS, KPS and the preceding public certificates. See PRIOR_ART.md.

**Review** (opening of [c89c/round3/review/README.md](c89c/round3/review/README.md))

### Two AI reviews

The two source reviews concern the frozen round-3 results. This file summarizes
them; the original review files remain read-only in the local review archive.
No human referee has reviewed these candidates.

- **GPT-6 Astra:** ACCEPT. No false or unjustified step was found. Both K6
  coefficient replays, exhaustive labelled coverage, both K5 upper counts, and
  the selected controls passed. The reconstructed upper matrix matched all
  65,536 entries. Astra requested Python >=3.10 in reproduction notes, removal
  of the inherited K6 “out of reach” assertion, and reconciliation of the
  18,528 optimization variables with 1,248 changed entries.
- **Claude Opus 5.5 via Claude Science:** FLAG for wording and credit, with no
  false proof step found. Its separately written evaluators reproduced all
  12,346 K6 inequalities and the exact K5 upper density. It requested
  “separately written” for our own checkers, comparison against #307's exact
  fraction, and explicit credit to Jeetu SK (SK2026) and #307 as the three-layer
  member of the graphon family. It could not refresh live priority sources.

**External replay** (opening of [c89c/round3/EXTERNAL_REPLAY.md](c89c/round3/EXTERNAL_REPLAY.md))

### External replay

On 8 November 2026, GitHub user arhancanli posted an
[independent replay](https://github.com/teorth/optimizationproblems/pull/308#issuecomment-6724784525)
of the **C89c >= 0.000033123924116** finite inequality on PR #308. They used
the certificate and `sources/graph8.g6` at commit `603b40c` and wrote their own
counting code; they did not read or run the checkers in `scripts/`.

Their result: the inequality holds for all 12,346 graph classes on 8 vertices.
The minimum, 1854939862512854832021/56000000000000000000000000, is at graph 905
and its complement, graph 11716, with the slack this packet states. They also
checked that the graph list is complete (orbit sum 2^28) and the certificate's
block structure, and their red controls were refused.

Not checked by them: the passage from the finite inequality to the asymptotic
bound (flag-algebra averaging and the disjoint-extension error term in
`PROOF.md`), which they read but did not formalize. It is not a peer review.

Full record: [Result](c89c/round3/README.md) · [Proof](c89c/round3/PROOF.md) · [Review](c89c/round3/review/README.md) · [External replay](c89c/round3/EXTERNAL_REPLAY.md) · [Prior art](c89c/round3/PRIOR_ART.md)

---

# C57c: univalent Bloch–Landau constant

Folder: [c57c/round1](c57c/round1)

**Status** (from the table in [README.md](README.md))

Bound: C<sub>57c</sub> ≥ **0.61230**

Previous best: 0.5708858 on the table; 0.612242 by F. Wikström ([arXiv:2610.34580](https://arxiv.org/abs/2610.34580)), whose framework this extends

Status: Candidate and unrefereed; [Tao-table PR #311](https://github.com/teorth/optimizationproblems/pull/311) records Wikström's 0.612242 ≤ C<sub>57c</sub> < 0.6562681 and adds this row. 489,994-leaf Arb certificate; separately written (same agent) checker; two AI reviews; no human referee

**Claim** (opening of [c57c/round1/README.md](c57c/round1/README.md))

### Candidate, unrefereed C57c lower bound

This packet supports the candidate statement

    U >= 6123/10000 = 0.61230.

Complete verification is recorded in verification.json: complete
global coverage and every arithmetic range. A partial receipt proves no
constant bound. The gain over Wikström's arXiv lower bound 0.612242 is exactly
29/500000 = 0.000058 (+5.8e-5). The gain over our own earlier
0.612294 candidate, which was never filed, is 3/500000 = 0.000006
(+6e-6). Frank Wikström's normalization, bounded-image transform,
Grunsky framework, equation-(9) center and equation-(12) phase congruence are credited in the proof.
No novelty judgment or independent human review is claimed.

The center adds a localized sixth-coefficient term. Higher Grunsky forms,
the exterior area theorem and Bloch derivative disks eliminate four higher
complex coefficients through a quadratic contradiction. The exact dyadic
forest covers the remaining four real parameters. PROOF.md collects the
analytic reductions; the component proof files give the same arguments.
The classical area/Grunsky theorems and ordinary complex analysis are
explicit mathematical inputs, not formalized by the arithmetic checker.

The separately written (same agent) checker imports no discovery/SDP code. Its
formal-series construction, sparse quadratic assembly, core derivatives
and strict Arb positivity test differ from discovery. Both implementations
were written by the same agent; this is not independent authorship.
All arithmetic replay uses python-flint Arb at192 bits. A floating
Cholesky factor only proposes an exactly checked dyadic congruence.

**Method** (first paragraph of [c57c/round1/PROOF.md](c57c/round1/PROOF.md))

All489994 leaves of the twelve-part artifact passed the separately
implemented Arb checker. This document collects every analytic reduction
and finite-cover argument. Classical area/Grunsky and complex analysis
inputs remain explicit; no independent human review or novelty judgment.

**Review** (opening of [c57c/round1/review/README.md](c57c/round1/review/README.md))

### Supplied AI review reports

These are AI reviews, not human refereeing. Both returned FLAG and found
no false mathematical step. Astra reports a partial fresh replay, with
stress ranges selected by subdivision density rather than certified margins.
Claude Science did not replay certificate leaves. See the reports for limits.

Machine-local paths in the publication copies of astra.md and
ASTRA_REPORT_REFEREE.txt were replaced by relative paths or neutral source
labels; their conclusions and numerical claims are unchanged. The CS link
identifies its original external review document; this packet contains the
supplied summary, cs.md.

The release fixes the missing prior-art file, gains/source descriptions,
checker-authorship wording, phase credit, endpoint convention and ineffective
controls. Review verdicts have not been retrospectively changed.

Full record: [Result](c57c/round1/README.md) · [Proof](c57c/round1/PROOF.md) · [Review](c57c/round1/review/README.md) · [Prior art](c57c/round1/PRIOR_ART_RELEASE.md)

---

# C47: centred Hardy–Littlewood maximal constant over squares

Folder: [c47/round9](c47/round9)

**Status** (from the table in [README.md](README.md))

Bound: C<sub>47</sub> ≥ **1.7055913150**

Previous best: 1.6855099933 (Lin) on the table; 1.7027237335 by T. S. Tomar ([Zenodo](https://doi.org/10.5281/zenodo.23716077)), whose measure and hole-filling operation this continues; 1.7032090736 proposed by Doldrums / SCiEL in open [PR #341](https://github.com/teorth/optimizationproblems/pull/341), whose move set this uses

Status: Candidate. 452-atom exact certificate with a finite instance; separately written (same agent) verifier. A clean-room AI referee on a different model (GPT-6 Astra) wrote its own exact checker and reached the same fraction, HOLDS ([referee](c47/round9/referee/)); no human review. [Tao-table PR #350](https://github.com/teorth/optimizationproblems/pull/350) open, stacked on #341, not merged; it was first filed at 1.7040280575 ([c47/round2](c47/round2/)). The intermediate certificates 1.7048221231 ([c47/round5](c47/round5/)), 1.7050503714 ([c47/round6](c47/round6/)), 1.7052517050 ([c47/round7](c47/round7/)) and 1.7055022252 ([c47/round8](c47/round8/)) were refereed too. Our earlier 1.70311 is in open [PR #321](https://github.com/teorth/optimizationproblems/pull/321) ([c47/round1](c47/round1/))

**Claim** (opening of [c47/round9/README.md](c47/round9/README.md))

### C47: centred Hardy–Littlewood maximal constant over squares

C47 is the optimal weak-type (1,1) constant of the centred Hardy–Littlewood maximal operator over axis-parallel squares in dimension d = 2, as defined on [Tao page 47a](https://teorth.github.io/optimizationproblems/constants/47a.html).

This packet gives **C47 ≥ 1.7055913150** (rigorous exact arithmetic, finite_instance.py with verify_exact.py and referee/referee_check.py; L0 for the bound as a whole). The printed improvement is **0.0000890898** over our round-8 **1.7055022252** (live on this PR), **0.0003396100** over our round-7 **1.7052517050**, **0.0005409436** over our round-6 **1.7050503714**, **0.0007691919** over our round-5 **1.7048221231**, **0.0015632575** over our round-2 **1.7040280575** in [this PR (#350)](https://github.com/teorth/optimizationproblems/pull/350) as first filed, **0.0023822414** over Doldrums / SCiEL’s **1.7032090736** in [#341](https://github.com/teorth/optimizationproblems/pull/341), and **0.0024813150** over our round-1 **1.70311** in [#321](https://github.com/teorth/optimizationproblems/pull/321) (rigorous decimal subtraction, comparison.py; prior printed values are cited comparisons). The asterisk remains appropriate: a commissioned AI referee is not a human review or a second-party confirmation in the Tao PR.

The exact periodic ratio is **q = 22878843460258009274861600625288681562329176839147945011303/13414024367090776613897918866165655414442557440000000000000** (rigorous, verify_exact.py). Its decimal expansion begins 1.705591315040… (rigorous downward prefix, sources/claim_facts.py). This is the periodic limit proved by the truncation-and-smearing argument in [PROOF.md](c47/round9/PROOF.md).

The directly checkable finite lower value is **211443076519550480268373711401841739495027970445032200793701027082601051542104989/123970540105353714391020257438714119850224408123125640972549257953280000000000000** (rigorous, finite_instance.py and referee/referee_check.py), with decimal prefix 1.705591315000… (rigorous downward prefix, sources/claim_facts.py). It strictly exceeds the printed bound. The finite construction has h = 2 and N = 333020005938 (rigorous parameters, referee/referee_check.py), with its exact positive rational smear radius in [the finite receipt](c47/round9/release_validation/finite.json); the enormous finite block is specified by formula without expanding it.

**Method** (first paragraph of [c47/round9/PROOF.md](c47/round9/PROOF.md))

This is the finite-periodic rectangle construction of **[Tomar, v5, Section 6, Lemma 6.2](https://doi.org/10.5281/zenodo.23716077), following Lin**, applied to the rational atoms supplied here. A clean-room AI referee on a different model used its own checks and concluded HOLDS; this is AI review, not human review. `verify_exact.py` is **separately written (same agent)** and imports neither search nor producer code.

**Referee** (opening of [c47/round9/referee/README.md](c47/round9/referee/README.md))

### Clean-room AI referee

GPT-6 Astra via Codex wrote its own checks without reading or running producer code. Verdict: **HOLDS**. This is an AI referee, not a human review.

It checked the table definition and Tomar v5, Section 6, Lemma 6.2 following Lin; all 452 atoms and 8443 witnesses; exact masses, strict radii, containments, union area and q; the half-open cell, boundaries, duplicates, finite retention, smearing, finite ratio and downward truncation. It did not establish optimality or search completeness.

From this folder:

```sh
/usr/bin/time -l nice -n 10 python3 referee_check.py
```

The aggregate output is ../release_validation/referee-results.json. This checker emits no per-witness table; no such table is shipped or needed. The original producer proof is retained byte-for-byte in sources/producer-proof.md. Numerical fields in the retained original aggregate and historical run logs are unchanged. Paths printed by historical logs identify original inputs; the public replay uses the defaults above.

Full record: [Result](c47/round9/README.md) · [Proof](c47/round9/PROOF.md) · [Referee](c47/round9/referee/README.md) · [Prior art](c47/round9/PRIOR_ART.md)

---

# C22b: tight alternating knot constant

Folder: [c22b/round4](c22b/round4)

**Status** (from the table in [README.md](README.md))

Bound: C<sub>22b</sub> ≤ **7.087559024** (442972439/62500000)

Previous best: 7.31 on the table; 7.2012719* proposed by Youhua Li / Claude Opus 5.5; 7.087662112* proposed by Doldrums / SCiEL in [PR #342](https://github.com/teorth/optimizationproblems/pull/342)

Status: Candidate. Round 4 extends SCiEL's even-radius modulation of our earlier T(2,1104n+3) family: T(2,1324n+3), radius terms up to cos 6u and a phase modulation, with interval certificates; separately written (same agent) verifiers. A clean-room AI referee on a different model (GPT-6 Astra) wrote its own checks and found it holds ([referee](c22b/round4/referee/)); no human review. [Tao-table PR #347](https://github.com/teorth/optimizationproblems/pull/347) open, stacked on #342, not merged. Our earlier 7.090412 is in open [PR #324](https://github.com/teorth/optimizationproblems/pull/324) ([c22b/round1](c22b/round1/)). Prose reductions need mathematical review

**Claim** (opening of [c22b/round4/README.md](c22b/round4/README.md))

### Candidate C22b <= 7.087559024 — round 4

[C22b, Tao page 22b](https://teorth.github.io/optimizationproblems/constants/22b.html)
is the infimum of ropelength per crossing over alternating knots (and links).
Ropelength is the infimum of contour length divided by thickness over
embeddings; **thickness is a radius**, so unit thickness requires nonlocal
separation 2.

**Candidate bound: C22b <= 7.087559024**, below **Doldrums / SCiEL's
7.087662112*** ([PR #342](https://github.com/teorth/optimizationproblems/pull/342))
by **0.000103088**, under the same definition.

The producer's interval verifiers were separately written by the same AI
agent as the search. A clean-room AI referee, **GPT-6 Astra via Codex**,
did not read or run the producer's code, wrote its own checks, and found
**VERDICT: HOLDS**. This is an AI referee, not a human review.

**Verification level: L0** for the bound as a whole (definitions: https://github.com/rpinho/math-certificates/blob/59eeb7097f806da05187b5f234445be3589204d4/VERIFICATION_LEVELS.md)
The interval verifiers were separately written by the same AI agent, a clean-room AI referee on a different model wrote its own checks and found it holds, and the prose reductions still need mathematical review.

**Method** (first paragraph of [c22b/round4/PROOF.md](c22b/round4/PROOF.md))

The finite verifier is **separately written (same agent)** from the numerical search.
The modulated-radius and phase steps here are prose. A clean-room AI referee
on a different model wrote its own checks and found the claim holds; see
[its report](c22b/round4/referee/REFEREE.md). Human mathematical review is still needed.
This is a proposed computer-assisted argument, not a proof-assistant theorem.
Doldrums / SCiEL / CPIL lab MBZUAI's even-radius modulation of our #324 is
the starting point. Their exact coefficients were inaccessible; see
PRIOR_ART.md. No third-party construction/search/verifier code was run.

**Referee** (opening of [c22b/round4/referee/README.md](c22b/round4/referee/README.md))

### Clean-room AI referee — GPT-6 Astra via Codex

**VERDICT: HOLDS.** This is an AI referee, not a human review.
The referee did not read, import, run or copy the producer's code or
certificate partitions. It read the permitted construction/contact data,
prose and selected logs, wrote its own geometry and checks, and regenerated
full-domain covers and a different physical projection.

It checked the Tao definition and radius convention, curvature and global
thickness over bodies, caps and joins, embeddedness and pair exhaustion,
actual-speed length, knot type for every n, its own n=1 determinant,
uniform cap allowance, and the limit. It found no caveat affecting the
specified mathematical upper bound; human mathematical review is still
needed. See [REFEREE.md](c22b/round4/referee/REFEREE.md) for the full argument and access limits.

Full record: [Result](c22b/round4/README.md) · [Proof](c22b/round4/PROOF.md) · [Referee](c22b/round4/referee/README.md) · [Prior art](c22b/round4/PRIOR_ART.md)

---

# C38: connective constant of the square lattice

Folder: [c38/bridges-span18](c38/bridges-span18)

**Status** (from the table in [README.md](README.md))

Bound: μ(Z²) ≥ **2.6275696** (8388608/3192535)

Previous best: 2.6273856 on the table (Numaro, span 17); 2.627483880 claimed by V. Plánočka (public, unrefereed)

Status: Candidate and unrefereed. Kesten irreducible-bridge renewal bound with span-18 strips and a disjoint span 19–30 supplement, extending Numaro's certificate with Jensen's finite-family criterion; separately written (same agent) verifiers; an adversarial AI referee on a different model (GPT-6 Astra) recounted independently through span 15 ([c38/review](c38/review/), HOLDS WITH CAVEATS: five span 16–18 inputs not independently regenerated), and a clean-room replay on a different model (GPT-6) reproduced 8388608/3192535 from the proof text and certificates alone ([REPLAY.json](c38/bridges-span18/REPLAY.json)). The renewal argument needs mathematical review. [Tao-table PR #328](https://github.com/teorth/optimizationproblems/pull/328) open, not merged

**Claim** (opening of [c38/bridges-span18/README.md](c38/bridges-span18/README.md))

### C38: span-18 bridge candidate release

Based on the frozen research report dated 2026-11-04. See REPRODUCE.md for current commands and release validation.

Candidate and unrefereed:

\[
\mu(\mathbb Z^2)\ge \frac{8388608}{3192535}
=2.6275696272711184\ldots>\frac{1051}{400}=2.6275.
\]

The verifier is **separately written (same agent)**. No novelty judgment, separate authorship, refereeing, or formal proof-system acceptance is claimed.

The [best frozen certificate](c38/bridges-span18/frozen/c38_power_secant/VERIFIED.json), [written proof](c38/bridges-span18/frozen/c38_power_secant/input/PROOF_POWER_SECANT.md), and [22 actual corruption controls](c38/bridges-span18/frozen/c38_power_secant/REJECTION_CONTROLS.json) pass on the pod and the copied Mini artifact. The exact lower value at the reciprocal of this bound is approximately **1.0000001143720572**. Acceptance uses its exact rational numerator and denominator, with no decimal tolerance. The exact excess above the requested bound is 17783/255402800.

The best input-manifest SHA256 is

    9797a748df2e4f4e12bd56578e10d68ebdd8d350e8fd9180cfb8cc445d161281

**The full expanded integer coefficient vector is unmaterialized.** Its coefficients are specified exactly as counts of the finite family below, and its generating value is enclosed with exact rational arithmetic. Rational enclosure endpoints are not coefficient counts. An optional length-24 prefix was expanded and fully checked; it is not needed for the best bound.

**Method** (first paragraph of [c38/bridges-span18/PROOF.md](c38/bridges-span18/PROOF.md))

Candidate, unrefereed; verification level L0 for the bound as a whole. The enumeration and verifier were separately written by the same AI agent. The mathematical reductions below are prose proofs requiring mathematical review. Frozen inputs and certificate values are unchanged.

**Clean-room replay** (opening of [c38/bridges-span18/replay/report.md](c38/bridges-span18/replay/report.md))

### C38 clean-room replay — PASS

Verdict: **PASS.** This independent clean-room computation reproduced the bound

**mu(Z²) >= 8388608/3192535**

with the complete frozen rational S(1353) reproduced exactly and S(1353) >= 1 checked using integers/Fractions. Every required native enumeration finished, including spans 16, 17, and 18. No certificate enclosure was left as an unverified numerical premise. The expanded coefficient vector was not materialized; this is a complete replay of the specified finite-family point enclosures and exact final assembly.

Full record: [Result](c38/bridges-span18/README.md) · [Proof](c38/bridges-span18/PROOF.md) · [Clean-room replay](c38/bridges-span18/replay/report.md) · [Prior art](c38/bridges-span18/PRIOR_ART.md)

---

# C49: 3-sunflower-free capacity

Folder: [c49/round1](c49/round1)

**Status** (from the table in [README.md](README.md))

Bound: C<sub>49</sub> ≥ **1.5678643845** ((64728+√3019700660)<sup>1/26</sup>, rounded down)

Previous best: 1.5678599* on the table (D. Koshta with Claude, [merged PR #260](https://github.com/teorth/optimizationproblems/pull/260)), whose 28-point two-pendant block this builds on

Status: Candidate. The same block and gluing theorem, with the 21 exceptional sets replaced by 32 new seven-element sets (252303 sets, N<sub>00</sub> up by 11). Separately written (same agent) checker; a clean-room AI referee on a different model (GPT-6 Astra) wrote its own exhaustive check and reproduced Koshta's block first ([referee](c49/round1/referee/)), HOLDS WITH CAVEATS (decimal rounding only). [Tao-table PR #370](https://github.com/teorth/optimizationproblems/pull/370) open, not merged. No human review or optimality claimed

**Claim** (opening of [c49/round1/README.md](c49/round1/README.md))

### C49 round-one candidate certificate

This packet establishes the candidate lower bound

\[
C_{49}\ge R=(64728+\sqrt{3019700660})^{1/26}
>\mathbf{1.5678643845}
\]
(rigorous, `release_validation/adapted/exact_rates_integer.py`).

The displayed ten-place decimal is **ROUNDED DOWN**. The exact expression is authoritative. Here C49 is the asymptotic capacity of families of subsets with no sunflower of three distinct members, as defined in the pinned table reference below.

Koshta's exact incumbent is
\(R_0=(64728+\sqrt{3018723123})^{1/26}=1.5678599024\ldots\).
The exact margin is \(R-R_0\), strictly between
`0.0000044821482170935091180159147830749067693242554392250907328019176417`
and
`0.0000044821482170935091180159147830749067693242554392250907328019176419`.
These bounds are certified by integer surd comparisons in `release_validation/adapted/exact_rates_integer.py` (the release-lint job's integer-only adaptation of the referee's `referee/exact_rates.py`, same comparisons) and its retained and fresh outputs; no floating-point comparison decides the claim.

| Block | Members | N00 | N01 | N10 | N11 |
|---|---:|---:|---:|---:|---:|
| Koshta baseline | 252292 | 33969 | 64728 | 64728 | 88867 |
| Candidate | 252303 | 33980 | 64728 | 64728 | 88867 |

The block has 28 points and distinct ports 0 and 1. Replace the incumbent's 21 exceptional members by 32 seven-element sets, sixteen wholly inside each pendant: N00 increases by 11. The 252271 common members include all 250659 product members and all 806 lifted augmentation members at each pendant. The augmentation is not merely fifteen unlifted sets per pendant. The exact subtraction is in `certificates/best_delta.json`.

**Method** (first paragraph of [c49/round1/PROOF.md](c49/round1/PROOF.md))

Let f(n) be the largest size of a family of subsets of an n-point set with no three distinct members A,B,C satisfying A∩B=A∩C=B∩C. Define C49=limsup f(n)^(1/n). Sperner (no proper containment between members) is a hypothesis of the gluing construction; it is not an added restriction on the capacity definition.

**Referee** (opening of [c49/round1/referee/README.md](c49/round1/referee/README.md))

### Clean-room AI referee archive

REFEREE.md and PRIOR_ART.md are byte-for-byte originals from the commissioned clean-room AI referee on a different model (GPT-6 Astra). Their historical headings and terminology, GitHub discussion/repository links, and the rounded-up numeral discussed as a rejected lower bound remain intact for fidelity. Release claims and pinned references are in the packet README.md. These archived reports are not new publication prose. The sole caveat is decimal rounding; use the exact surd or the rounded-down 1.5678643845.

The source scripts and scientific logs are copied from that job. `independent.cpp` is the referee's own code; its filename is historical. The archive does not redistribute the referee's third-party source snapshots or process inventories. Data needed for replay are supplied by the packet certificate, delta and MIT baseline; REPRODUCE.md stages them in a scratch directory. The original 1997 PDF was not inspected; REFEREE.md proves the operative gluing statement explicitly. Hashes identify the supplied reports and inputs; they do not attest historical isolation or model identity.

Full record: [Result](c49/round1/README.md) · [Proof](c49/round1/PROOF.md) · [Referee](c49/round1/referee/README.md) · [Prior art](c49/round1/PRIOR_ART.md)

---

# Erdős #1183: the Erdős–Ulam two-colouring sublattice function

Folder: [erdos/1183](erdos/1183)

**Status** (from the table in [README.md](README.md))

Bound: **f(11)=7, f(12)=7, f(13)=8, f(14)=8, f(15)=9, f(16)=9, f(17)=10, f(18)=10, f(19)=11; f(20)≤12; f(21)=12; f(22)≤13; 13≤f(23)≤14; f(24)=14**

Previous best: Exact values through n=20 were already stated by Bhattacharjee and Bhattacharya (BLLM manuscript, same weighted-poset method); ours for n=11..20 reproduce them with certificates, and n=21..24 go beyond. Lower bounds: BMB; chain and chain exchange plus all balanced words

Status: Candidate; no human review. SAT/DRAT for n=11..14; exact weighted-poset trees and separately written checker for n=15..24. Method after ipezygj’s SAT + DRAT proof for #609. Clean-room referees: GPT-6 Astra at n=11; Claude Opus 5.5 at n=12, n=13/14, n=15..20 and n=21..24. HOLDS WITH CAVEATS: **f(20)=12 and f(22)=13 depend on BMB lem:window20**, replayed from authors’ checker but mixed levels not reimplemented; without it **11≤f(20)≤12 and 12≤f(22)≤13**. **f(23) stays 13..14; rank minimum exactly 14**. f(24) lower bound uses flower, without window20

**Claim** (opening of [erdos/1183/README.md](erdos/1183/README.md))

### Erdős #1183: candidate values through f(24), with dependencies at f(20) and f(22)

The original packet gives the four finite equalities **f(11)=7**, **f(12)=7**, **f(13)=8** and **f(14)=8**, with explicit colourings, regenerable SAT queries and checkable DRAT certificates. The supplied clean-room AI agents acting as referees conclude **HOLDS** for all four values. These are candidate results with **no human review**. The extension gives **f(15)=9, f(16)=9, f(17)=10, f(18)=10, f(19)=11** and **f(20)≤12**. The equality **f(20)=12** uses BMB `lem:window20` via `thm:f20`; without that dependency, **11≤f(20)≤12**. The extension’s clean-room referee concludes **HOLDS WITH CAVEATS**. Round 5 adds **f(21)=12**, **f(24)=14**, **f(22)≤13** (equality given BMB `lem:window20`) and **13≤f(23)≤14**. Unconditionally **12≤f(22)≤13**; the rank-colouring minimum at n=23 is exactly **14**. These finite results do not settle the asymptotic problem.

**Priority.** The exact values of f(n) for every n up to twenty were already stated by Deep Bhattacharjee and Ushashi Bhattacharya in their BLLM manuscript (Theorem `fvalues`, using the same weighted-poset reduction as its Lemma `levelposet`), [public in creelie/eBLLM](https://github.com/creelie/eBLLM/blob/241326bbba4726afde74ae1858265878b2176c59/paper/bllm/paper/sections/sec10d_crossing.tex) and present in that file since its commit of 19 October 2026. We missed it in our earlier searches. Our values from eleven to twenty are therefore reproductions, found separately and published with certificates (SAT/DRAT proofs from eleven to fourteen, replayable proof trees from fifteen to twenty); earlier versions of this packet wrongly said that exact values were known only up to ten. The values from twenty-one to twenty-four go beyond that manuscript. The odd-n lower bound used here is also proved in Lean 4 by the OpenRefute project, as BLLM cites.

**Method** (first paragraph of [erdos/1183/PROOF.md](erdos/1183/PROOF.md))

Write M(χ) for the largest cardinality of a nonempty monochromatic family of subsets closed under binary union and intersection. Then f(n)=minχ M(χ). The minimum includes every colouring of all subsets. Rank colourings below are particular constructions giving upper bounds, not a restriction on that minimum. The n=11 and n=12 queries ask for at least eight members; the n=13 and n=14 queries ask for at least nine. These thresholds exclude every larger closed family as well, without assuming that a larger lattice contains a sublattice of exactly the threshold size.

**Referee** (opening of [erdos/1183/referee/n21n24/REFEREE.md](erdos/1183/referee/n21n24/REFEREE.md))

Shipped: referee report on the candidate values f(21)=12, f(22)=13 (conditional on BMB lem:window20), 13≤f(23)≤14 and f(24)=14 for Erdős #1183. All four hold as stated, with the caveats listed at the end.

Referee job e1183n2124_referee, 17 Nov 2026. I wrote all the code here myself: `src/wp.c` (exact weighted-poset search; every positive witness is converted to coordinate masks and checked by direct pairwise closure), `src/brute.c` (all sublattices of 2^[n], n≤6), `src/check_witnesses.py` (direct closure check of the producer's families) and `src/words12.py`. I did not read, import or run any code from ../e1183n21, ../e1183n15, ../e1183n1314_referee/src or ../e1183n1520_referee/src. I used ../e1183n21/certificates/upper_n2{1,2,3,4}.json as data only (words and witness masks), and the word list in ../e1183n1520_referee/out/max_words.txt as data for the n=11..20 controls. Raw outputs are in `out/`. Fetched sources are in `sources/` and `ext/window20/`, with SHA256SUMS.

Full record: [Result](erdos/1183/README.md) · [Proof](erdos/1183/PROOF.md) · [Referee](erdos/1183/referee/n21n24/REFEREE.md) · [Prior art](erdos/1183/PRIOR_ART.md)

---

# C30: growth rate of 1324-avoiding permutations

Folder: [c30/round1](c30/round1)

**Status** (from the table in [README.md](README.md))

Bound: C<sub>30</sub> ≥ **10.42** (521/50), conditional

Previous best: 10.27 on the table; 10.412263 by Norton (unrefereed arXiv v3), recorded in open [PR #313](https://github.com/teorth/optimizationproblems/pull/313) (maximusrufus)

Status: Candidate and unrefereed, and conditional on BBEP and Norton's unrefereed v3. First-moment two-leaf bound with a value-word lemma; exact Arb certificate with a thin margin (about 1.8e-4); separately written (same agent) checker; two AI reviews; no human referee. Two finite lemmas are in Lean ([c30/lean-m1](c30/lean-m1/)); the bound is not. [Tao-table PR #317](https://github.com/teorth/optimizationproblems/pull/317) open, stacked on #313. The final evaluation was [independently replayed](https://github.com/teorth/optimizationproblems/pull/317#issuecomment-6724784097) by GitHub user arhancanli on 2026-11-08; the mathematics was not checked ([note](c30/round1/EXTERNAL_REPLAY.md))

**Claim** (opening of [c30/round1/README.md](c30/round1/README.md))

### A candidate lower bound of 10.42 for C30

**Claim.** The growth rate of permutations avoiding the pattern 1324 is at least **521/50 = 10.42**, conditional on the cited BBEP results and the retained machinery of **Norton's unrefereed v3**. A permutation avoids 1324 when no four entries, read left to right, have that relative order. The growth rate describes how quickly the number of avoiders increases with length. This is an AI-written candidate argument, with no human referee and no priority claim.

**What is new in this packet's argument.** The additions amount to about two pages of core mathematics, expanded in the manuscript for review. The **value-word lemma** proves how the leaf/non-leaf word changes when a terminal arch chain is attached: its subobjects lie above the chain in reverse value order, and their leaf marks are preserved. This supplies the missing all-size explanation behind the strip-counting equations; it is proved from BBEP's inverse arch map.

The **two-leaf first-moment bound** gives an actual density of about **0.06627960057**, below **1/10**. The **family-selection argument** uses this mean and positivity of generating functions to obtain a full-growth subsequence whose members obey a two-leaf cap. It does not infer concentration from a mean. Physical arch concatenation then gives balanced dominoes satisfying common per-cell inequalities. Finally, an **integer majorization envelope**, including its parity correction, provides a uniform placement lower bound for every permitted ordered strip pattern. Its synthetic two-leaf coordinate is **7/50**, distinct from the mean and the selection threshold.

**Method** (first paragraph of [c30/round1/PROOF.md](c30/round1/PROOF.md))

These are the initial baseline and reduced-model notes. The final candidate proof of 521/50 is in **FIRST_MOMENT_PROOF.md**, with its separate candidate certificate. The baseline certificate discussed below replays the **external Norton v3 baseline**, conditional on the combinatorial results listed in REFEREE.md. See RELEASE_NOTES.md for the source-digest provenance check used by this trimmed release.

**Referee** (opening of [c30/round1/REFEREE.md](c30/round1/REFEREE.md))

### Norton v3 referee notes — candidate, unrefereed

Audit by the same agent as the arithmetic replay. This is not human refereeing and is not a novelty judgment. Frozen source: `sources/norton-v3.html`, hash in BAR.json. Source was reopened from arXiv on 2026-11-03. Results below distinguish checked arguments, imported theorems, and unfinished gates.

**External replay** (opening of [c30/round1/EXTERNAL_REPLAY.md](c30/round1/EXTERNAL_REPLAY.md))

### External replay

On 8 November 2026, GitHub user arhancanli posted an
[independent replay](https://github.com/teorth/optimizationproblems/pull/317#issuecomment-6724784097)
of the exact numerical point behind the **C30 >= 10.42 (521/50)** candidate on
PR #317. They used `FIRST_MOMENT_PROOF.md` and
`artifacts/candidate_certificate.json` at commit `4f0bbf8` and wrote their own
interval code; they did not read or run `verify_candidate.py`.

Their result: the envelope coordinates are the Section 5 limits at the stated
parameters, and Phi >= 0.000183097093883 at z = 50/521, above the stated
0.00018309709357909. Their controls: 1/z = 10.4208 fails (the document puts
break-even near 10.4207), and Norton's equitable profile in place of the
envelope fails at z = 50/521, so the gain comes from the envelope.

Not checked by them: the mathematics (the value-word lemma, the marginal
equations, the first-moment family, the two-leaf cap, the envelope lemma and
Norton's machinery). The replay checks the final evaluation from the stated
profile, not that the profile is achieved. It is not a peer review.

Full record: [Result](c30/round1/README.md) · [Proof](c30/round1/PROOF.md) · [Referee](c30/round1/REFEREE.md) · [External replay](c30/round1/EXTERNAL_REPLAY.md)

---

# C31b: four-letter LCS constant

Folder: [c31b/h9-unit30](c31b/h9-unit30)

**Status** (from the table in [README.md](README.md))

Bound: C<sub>31b</sub> ≥ **0.617356908308**

Previous best: 14982218/24268325 in PR #272 (Leandre Jack), same operator

Status: Not filed: a precision refinement (2<sup>-30</sup> unit) of Jack's construction, offered to him [on #272](https://github.com/teorth/optimizationproblems/pull/272#issuecomment-6603405770). Separately written (same agent) checker; two AI reviews

**Claim** (opening of [c31b/h9-unit30/README.md](c31b/h9-unit30/README.md))

### C31b: h=9 lower bound with fixed-point unit 2^-30

Candidate, unrefereed:

    gamma_4 >= 3835447842/6212691217 > 0.617356908308.

This refines Leandre Jack's construction in [PR #272](https://github.com/teorth/optimizationproblems/pull/272).
The gain comes from the finer fixed-point unit, 2^-30 instead of 2^-27.
The operator, h=9 and set of 1,431,743,147 classes are the same as in #272.
This is a precision refinement of Jack's construction, not a new method.

The exact gain over Jack's stated 14982218/24268325 is
570425344/150771609578801525, about 3.7834e-9. His exact witness may
support a higher value, so the gain over that witness may be smaller.
Both values have the same six-place floor, 0.617356.

**Method** (first paragraph of [c31b/h9-unit30/PROOF_C31_LOWER.md](c31b/h9-unit30/PROOF_C31_LOWER.md))

This is a continuation of Leandre Jack's public construction in PR #272,
using Lueker's finite lookahead method (2009, Lemma 2.3), in the
k-letter form of Kiwi and Soto (2009), also used by Rosenfeld (2024).
Here k=4, the four-letter setting studied by Kiwi and Soto. The operator,
h=9 and class set are the same as in #272. The gain comes from refining
the fixed-point unit from 2^-27 to 2^-30. This is a precision refinement
of Jack's construction, not a new method.
More fixed-point bits do not change the mathematical operator. No novelty
judgment is made. A certificate value is claimed only when the frozen
metadata has a complete separate exact-check receipt.

Full record: [Result](c31b/h9-unit30/README.md) · [Proof](c31b/h9-unit30/PROOF_C31_LOWER.md) · [Value proof](c31b/h9-unit30/VALUE_PROOF.md)

---

# C10a: real Grothendieck constant

Folder: [c10a](c10a)

**Status** (from the table in [README.md](README.md))

Bound: Recording only: 1.773 ≤ C<sub>10a</sub> ≤ 1.77987164. **Not my bounds**

Previous best: [SLXCKKM26] and earlier on the table

Status: Replay receipts for Heilman-Jones-Malavolta and Peng; [Tao-table PR #300](https://github.com/teorth/optimizationproblems/pull/300) open, not merged. No new bound

**Claim** (opening of [c10a/README.md](c10a/README.md))

### Replay of two real Grothendieck constant bounds

Receipts from replaying two public certificates on 30 October 2026, for the Tao table entry
[10a](https://teorth.github.io/optimizationproblems/constants/10a.html).

**These bounds are not mine.** They belong to the cited authors. This repository holds no new bound and no author source.

| Claim | Authors | Replay |
| --- | --- | --- |
| K_G < 1.77987164 | Bo Peng, [arXiv:2610.24417v1](https://arxiv.org/abs/2610.24417v1), using Junyu Ren's construction | Published source replayed in full, plus a separately written exact check of the final inequality. Passed. |
| K_G ≥ 1.773 | Heilman, Jones and Malavolta, [arXiv:2610.10477v1](https://arxiv.org/abs/2610.10477v1), [source](https://github.com/christophsjones/RealGrothendieck/tree/b02621d9f9aaf7114c433dd4c11bab6d4a25be39) | All 35 fibre certificates replayed with the authors' numerical drivers, and the final rational assembly checked by separate code. Passed. |
| K_G ≤ 1.7799 (Theorem 4.2, 1.779893) | Heilman, Jones and Malavolta | **Not replayed.** Theorem and construction read, final printed arithmetic checked. |

This is a replay of certificates, not a review of the proofs. The analytic reductions are the authors'.

Junyu Ren's public claim of 1.779754412112 was not audited and is treated as unverified.

Full record: [Record](c10a/README.md)

---

# Tetrahedron cylinder cover (openai/math problem 100)

Folder: [tetrahedron-cover](tetrahedron-cover)

**Status** (from the table in [README.md](README.md))

Bound: C < **0.499613830783714149** (saving 3.86 × 10⁻⁴ below 1/2)

Previous best: ≈ 5.4 × 10⁻¹⁰ saving (the problem's explicit example)

Status: Hexagon [2610.00304](https://hexagonmath.org/2610.00304); an arXiv submission (17 Oct 2026) is on hold in moderation and not listed as of 7 Nov 2026; reported at [plasma-ai/erdos#55](https://github.com/plasma-ai/erdos/issues/55) and [kisonecat/openai-math#1](https://github.com/kisonecat/openai-math/issues/1)

**Claim** (opening of [tetrahedron-cover/README.md](tetrahedron-cover/README.md))

### A finite cylinder cover of the tetrahedron saving 3.86 × 10⁻⁴ below the half-area bound

Unrefereed construction note: [Hexagon 2610.00304v2](https://hexagonmath.org/2610.00304?version=2)
and [Zenodo](https://doi.org/10.5281/zenodo.23483539).
The later structural/radius extensions credited below are separate repository contributions;
they are not claimed to be included in the original deposited note.

This repository contains an explicit cover of the regular tetrahedron by **4,096 cylinders** with compact triangular
perpendicular bases, and two independently written exact checkers proving that its normalized total base area is

    0.499613830783714148 ≤ C < 0.499613830783714149,

a saving of more than **0.000386169** below 1/2. This is problem 100 of the OpenAI math release
([openai/math](https://github.com/openai/math), *Finite angular cylinder covers below the half-area bound*,
27 Sep 2026; [lean/docs/100.md](https://github.com/openai/math/blob/main/lean/docs/100.md)), whose explicit small-tilt
example saves about 5.4 × 10⁻¹⁰ with 16,000,000 cylinders. The construction here uses the same angular-sector family
as that preprint, with a finite tilt τ = 9/20 and numerically optimized rational radii.

No claim of optimality or priority is made: we found no larger rigorously published saving as of 15 Oct 2026, but the
search was not exhaustive. A target of 10⁻³ was **not** reached, and `structural_bound.py` proves C ≥ 0.4993 for the
final symmetric axis family with arbitrary shared even radial cutoffs, for every tilt 0 ≤ τ ≤ 1.

Full record: [Result](tetrahedron-cover/README.md) · [Separately computed radii](tetrahedron-cover/INDEPENDENT_RADII.md)

---

# Linear code records (codetables.de)

Folder: [codetables](codetables)

**Claim** (opening of [codetables/README.md](codetables/README.md))

These are nine candidate improvements to lower bounds in Markus Grassl’s codetables.de tables. The first six were sent to the maintainer on 6 November 2026; the last three, [92,13,61], [106,12,72] and [85,15,54] over GF(9), were not part of that submission and have not been sent. None is yet accepted or listed in the tables. The search and checks were run by AI agents (OpenAI Codex models): the search on GPT-6.1 Sol, and each clean-room check on GPT-6 Astra, which wrote its checker without reading the search code.

| parameters | field | table lower–upper before (fetch time, UTC) | ours | construction | how d was checked |
|---|---|---|---:|---|---|
| [[74,12,43]](codetables/q5_n74_k12_d43/) | GF(5) | [42–50](https://www.codetables.de/BKLC/BKLC.php?q=5&n=74&k=12), 2026-11-06 17:21:02.261807 UTC | 43 | Construction XX: cyclic [62,12,35], subcodes [62,9,39] and [62,9,39], intersection [62,6,43], two [6,3,4] tails. | exhaustive enumeration of all projective messages |
| [[128,14,79]](codetables/q5_n128_k14_d79/) | GF(5) | [78–90](https://www.codetables.de/BKLC/BKLC.php?q=5&n=128&k=14), 2026-11-06 17:21:02.252889 UTC | 79 | Construction X: cyclic [124,14,76] containing [124,12,79], with a [4,2,3] tail. | exhaustive enumeration of all projective messages |
| [[129,14,80]](codetables/q5_n129_k14_d80/) | GF(5) | [79–91](https://www.codetables.de/BKLC/BKLC.php?q=5&n=129&k=14), 2026-11-06 18:41:07.276405 UTC | 80 | Construction XX: cyclic [124,14,75], subcodes [124,13,76] and [124,13,82], intersection [124,12,83], tails [1,1,1] and [4,1,4]; also last-coordinate puncturing of [130,14,81]. | provably complete Brouwer–Zimmermann information-set search |
| [[130,14,81]](codetables/q5_n130_k14_d81/) | GF(5) | [80–92](https://www.codetables.de/BKLC/BKLC.php?q=5&n=130&k=14), 2026-11-06 18:41:07.985385 UTC | 81 | Construction XX: cyclic [124,14,75], subcodes [124,13,76] and [124,13,82], intersection [124,12,83], tails [1,1,1] and [5,1,5]. | provably complete Brouwer–Zimmermann information-set search |
| [[130,16,77]](codetables/q5_n130_k16_d77/) | GF(5) | [76–90](https://www.codetables.de/BKLC/BKLC.php?q=5&n=130&k=16), 2026-11-06 18:41:08.432788 UTC | 77 | Construction XX: cyclic [124,16,73], subcodes [124,15,74] and [124,13,76], intersection [124,12,79], tails [1,1,1] and [5,3,3]. | provably complete Brouwer–Zimmermann information-set search |
| [[99,12,67]](codetables/q9_n99_k12_d67/) | GF(9) | [66–78](https://www.codetables.de/BKLC/BKLC.php?q=9&n=99&k=12), 2026-11-06 18:41:08.887505 UTC | 67 | Construction X: cyclic [91,12,61] containing [91,9,67], with an [8,3,6] Reed–Solomon tail. | provably complete Brouwer–Zimmermann information-set search |
| [[92,13,61]](codetables/q9_n92_k13_d61/) | GF(9) | [60–71](https://www.codetables.de/BKLC/BKLC.php?q=9&n=92&k=13), 2026-11-06 20:17:14.279255 UTC | 61 | Construction X: cyclic [91,13,60] containing [91,12,61], with a [1,1,1] tail. | provably complete Brouwer–Zimmermann information-set search |
| [[106,12,72]](codetables/q9_n106_k12_d72/) | GF(9) | [71–84](https://www.codetables.de/BKLC/BKLC.php?q=9&n=106&k=12), 2026-11-07 12:28:23 UTC | 72 | Construction XX: cyclic [91,12,61], subcodes [91,9,66] and [91,9,67], intersection [91,6,72], tails [7,3,5] and [8,3,6]. | exhaustive enumeration of all projective messages |
| [[85,15,54]](codetables/q9_n85_k15_d54/) | GF(9) | [53–63](https://www.codetables.de/BKLC/BKLC.php?q=9&n=85&k=15), 2026-11-08 01:00:38.935 UTC | 54 | Construction XX: cyclic [80,15,51], subcodes [80,14,52] and [80,12,53], intersection [80,11,54], tails [1,1,1] and [4,3,2]. | BCH bound plus a complete Brouwer–Zimmermann search on a shortened subcode |

Full record: [Result](codetables/README.md)

---

# Replays of other people's results

Folder: [replays/3a](replays/3a)

**Claim** (opening of [replays/3a/README.md](replays/3a/README.md))

### Clean-room replays of three starred 3a rows

These are replays of other people's finite certificates for the sum-difference constant on
[Tao's table, page 3a](https://teorth.github.io/optimizationproblems/constants/3a.html). They are not our results.
Each replay was written from the row's definition and the claimant's prose notes. The claimants'
code was neither read nor run; their data files were used only for comparison. The replays were
prepared with AI assistance (Claude) and fact-checked by a second model (GPT-6 Astra). No human
has reviewed them.

| Row | Claim | Replay | Folder |
|---|---|---|---|
| M2026 ([PR #236](https://github.com/teorth/optimizationproblems/pull/236), mizopl) | > 1.19230254 | PASS: θ ≥ 1.192302540705685029…, with n0 = 17074745018 and L = 50031092045455301 rebuilt from the page text and equal to the page's | [M2026/](replays/3a/M2026) |
| Syl2026, k = 2 ([PR #238](https://github.com/teorth/optimizationproblems/pull/238), xSyllaa) | > 1.19281555 | PASS: θ ≥ 1.192815557092986…, margin 7.1·10⁻⁹. The cost histogram was rebuilt in full and is byte-identical to the claimant's | [Syl2026_k2k3/](replays/3a/Syl2026_k2k3) |
| Syl2026, k = 3 ([PR #238](https://github.com/teorth/optimizationproblems/pull/238)) | > 1.19359680 | PASS conditional on the high-cost part (cost > 17500) of the claimant's histogram. That part was checked only statistically, and the low-cost part exactly | [Syl2026_k2k3/](replays/3a/Syl2026_k2k3) |

Full record: [Replay](replays/3a/README.md)

---

# Results for other people's papers

Folder: [friends](friends)

**Claim** (opening of [friends/README.md](friends/README.md))

### Results for other people's papers

The rest of this repository is bounds on open constants from [Terence Tao's optimization-problems table](https://github.com/teorth/optimizationproblems) and [openai/math](https://github.com/openai/math). This folder is the same thing applied to papers by mathematicians and scientists I know: an exact value where a paper printed a bound, a settled case the paper left open, or a certificate for a number that was only conjectured.

The format is the same as every other folder here. Each item says what was asked, what we found, how a clean-room referee checked it, and where it is still a candidate. The referee is a separate agent on a different model that rebuilds the claim from the primary source and may not import the finder's code; it is still our own pipeline, not a third-party check. Nothing here has been refereed by a journal or by a human, and no priority is claimed over anyone.

Everything below has been sent to the author it concerns. Results that were not sent are not here.

| Person | Paper | What we found | Referee |
|---|---|---|---|
| Oliveira e Silva | [arXiv:2609.11644](https://arxiv.org/abs/2609.11644), Remark 1.3(c) | At d = 5, Gaussians are not local maximizers at the Keel–Tao endpoint: a certified family beats them by more than 11ε⁴, with an exact checker | candidate: no clean-room referee; three model reviews found no false step |
| Oliveira e Silva | Mandel and Oliveira e Silva, *Calc. Var.* 63 (2024) 45, [arXiv:2306.03720](https://arxiv.org/abs/2306.03720), Appendix C | A reflection-even axial attainment theorem for the biharmonic NLS ground states left open there, for all 3 ≤ p < 4 | HOLDS |
| Oliveira e Silva | Gonçalves, Oliveira e Silva and Ramos, *New Sign Uncertainty Principles*, [arXiv:2003.10771](https://arxiv.org/abs/2003.10771), Conjecture 3.7 | The conjecture for odd ℓ, plus an exact adjacent cyclic-minus jump at q = 7320/7321 in the paper's own feasibility problem | HOLDS |
| José Bento | Safavi, Joshi, França and Bento, [arXiv:1801.04492](https://arxiv.org/abs/1801.04492), Thm 5 | An exact finite-κ certificate: at κ = 25 and the paper's tuned β, q = 3599/5000 is a universal squared-distance factor, improving the matched published 18/25 | HOLDS |
| José Bento | Bento, Furmaniak and Ray, [arXiv:1801.04987](https://arxiv.org/abs/1801.04987), §IV | A weight condition under which the weighted fused lasso path has O(n) pieces, which §IV asks for; Tibshirani–Taylor diagonal dominance is credited as the stronger prior control | HOLDS |
| José Bento | Marangola, Sheikholeslami and Bento, [arXiv:2512.24930](https://arxiv.org/abs/2512.24930), Thm 3 | The all-tree extension and the sharp strict threshold γ = 1 + 2/q | HOLDS WITH CAVEATS |
| Hugo L. Fernandes | Gama and Fernandes, *C&OR* 133 (2021) 105357, [arXiv:2011.03647](https://arxiv.org/abs/2011.03647), Table B.7 | Exact optima for 15 single-day OPTW instances; t204 is 179 against a published best-known 171 | HOLDS WITH CAVEATS |
| Hugo L. Fernandes | The same benchmark family (TOPTW, Solomon/Righini instances) | pr11 with three vehicles closed at 654 with an exact certificate; c104 with four vehicles closed at 1260, moving its status from best-found to proven | HOLDS WITH CAVEATS / HOLDS |
| Hugo L. Fernandes | [arXiv:2411.14411](https://arxiv.org/abs/2411.14411), Table 4.1 | Exact CVRPTW50 optima for all 2,048 instances, mean 14.4717 against the quoted 14.478; TOPTW50 mean profit 34.09 with 2,006 of 2,048 certified optimal | candidate: exact-solver result with its own verification file, not refereed |
| Kris Sankaran | Sankaran, Raskutti and Ye, [arXiv:2609.19511](https://arxiv.org/abs/2609.19511) | A zero causal Shapley value implies a causal null if and only if h₋ ≥ h₊ | candidate: no clean-room referee; two model reviews found no false step |
| Marco Sampaio | Alves et al., FiFAR, *Sci Data* 2025, Table 7 | All five team deferral costs drop (138.1 → 102.0 among them) and reproduce exactly | HOLDS WITH CAVEATS |

Two caveats worth repeating rather than burying: prior art already improves the FiFAR solver on its own (nguyetvo's public repository), and that benchmark has no unused hold-out, so the comparison is to a published table, not to a fresh test set.

Full record: [Overview](friends/README.md)

---

# José Bento: Nesterov certificate

Folder: [friends/bento/j011-nesterov-certificate](friends/bento/j011-nesterov-certificate)

**Verdict** (opening of [friends/bento/j011-nesterov-certificate/VERDICT.md](friends/bento/j011-nesterov-certificate/VERDICT.md))

HOLDS
Referee: gpt-6.1-sol

The exact theorem survives independent reconstruction: at kappa25 and
beta21/32, q=3599/5000=0.7198 is a universal squared-distance upper factor,
improving the matched published q18/25 by1/5000.
The paper's norm factor is sqrt(q); the metric and recurrence match.
[Primary source](https://www.jbento.info/papers/nesterov_sdp.pdf), Algorithm1,
Eqs25–26 and Theorem7. José Bento's identity matches the author block and
[his publication page](https://www.jbento.info/).

I wrote independent code from the definitions and ran it on mscr: exact
source-baseline reproduction at kappa5,13,25,41; rational reconstruction
of the submitted certificate; 35/36 positive LDL pivots; exact function
cancellation, nonnegative multipliers, and coercivity. Three corrupted
certificates were rejected. Code, logs, hashes and receipts are retained here.

No hold-out or dataset exists. The trivial quadratic control gives
q=441/625=0.7056 and cannot certify the nonquadratic class. The basic
matched off-by-one frequency test fails exactly at the proposed factor.

Full record: [Claim](friends/bento/j011-nesterov-certificate/CLAIM.md) · [Referee report](friends/bento/j011-nesterov-certificate/REPORT.md) · [Verdict](friends/bento/j011-nesterov-certificate/VERDICT.md) · [Prior art](friends/bento/j011-nesterov-certificate/PRIOR_ART.md)

---

# José Bento: weighted fused lasso

Folder: [friends/bento/j012-weighted-fused-lasso](friends/bento/j012-weighted-fused-lasso)

**Verdict** (opening of [friends/bento/j012-weighted-fused-lasso/VERDICT.md](friends/bento/j012-weighted-fused-lasso/VERDICT.md))

HOLDS
Referee: gpt-6.1-sol

The restricted-weight theorem survives independent mathematical review: T <= min{3^k(g-1), 1+8[2g-3+gk+k(k-1)/2]}, with the stated k and g=n+1-k.
It counts the same maximal affine solution-path pieces, including the constant tail, as [Bento–Furmaniak–Ray, Eq.(2), Theorems 2–4](https://arxiv.org/html/1801.04987v3).
The independent all-n argument in PROOF_AUDIT.md validates good-contact nonreturn, pair amortization, and simultaneous events; the conclusion does not rest on extrapolating finite tests.

Ran on phys: an original exact rational primal-block enumerator and a separately written interval KKT checker, importing no claimant code.
Both passed 570 complete paths: the two baselines, all 73 submitted certificates, and 495 fresh adversarial/exhaustive cases.
All submitted knots and coefficients agree exactly. Fig.1 has T=5 and knots 25/27,25/23,100/73,25/4; its equal-weight control has T=3.
The checker rejected five negative controls, including cutting the low-weight edge and testing that different objective's path under the original positive weights.
There is no statistical holdout: this is an all-input theorem, and the synthetic cases are diagnostics. No holdout-based performance gain is asserted.

Full record: [Claim](friends/bento/j012-weighted-fused-lasso/CLAIM.md) · [Referee report](friends/bento/j012-weighted-fused-lasso/REPORT.md) · [Verdict](friends/bento/j012-weighted-fused-lasso/VERDICT.md) · [Prior art](friends/bento/j012-weighted-fused-lasso/PRIOR_ART.md)

---

# José Bento: perfect phylogeny margin

Folder: [friends/bento/j019-perfect-phylogeny-margin](friends/bento/j019-perfect-phylogeny-margin)

**Verdict** (opening of [friends/bento/j019-perfect-phylogeny-margin/VERDICT.md](friends/bento/j019-perfect-phylogeny-margin/VERDICT.md))

HOLDS WITH CAVEATS
Referee: gpt-6.1-sol

The all-tree singleton result and sharp strict threshold gamma=1+2/q survive
for fixed finite q under the paper's explicit Brownian increment-energy limit.
The published 1/(36e) coefficient is correctly identified and remains unchanged.
Relative to the paper, the extension covers every same-root candidate and
quantifies the allowed scalar relaxation; it does not reproduce a finite-grid gain.

I wrote independent code from descendant sums, generated undirected edge subsets,
and checked every ordered tree pair for q=3..7, including 282,475,249 pairs at q=7.
Every wrong-tree gap was at least 2; only the true tree attained the minimum.
Complete histograms matched the submitted data. Rational witnesses checked
thresholds through q=40. Integration reproduced 1/36; enumeration checked the leaf factor.
The all-q proof and survival-conditioning argument are valid: conditioning on
positive-probability survival preserves quadratic variation. Finite candidates
then give the simultaneous limit. Equality at the threshold remains unclaimed.

Full record: [Claim](friends/bento/j019-perfect-phylogeny-margin/CLAIM.md) · [Referee report](friends/bento/j019-perfect-phylogeny-margin/REPORT.md) · [Verdict](friends/bento/j019-perfect-phylogeny-margin/VERDICT.md) · [Prior art](friends/bento/j019-perfect-phylogeny-margin/PRIOR_ART.md)

---

# Hugo L. Fernandes: OPTW optima

Folder: [friends/fernandes-orienteering/hb01-optw-optima](friends/fernandes-orienteering/hb01-optw-optima)

**Verdict** (opening of [friends/fernandes-orienteering/hb01-optw-optima/VERDICT.md](friends/fernandes-orienteering/hb01-optw-optima/VERDICT.md))

HOLDS WITH CAVEATS
Referee: gpt-6.1-sol

All fifteen stated rewards are exact optima for the explicitly claimed service-start, exact floor-to-two-decimals model. Each has a verified same-score unrounded-Euclidean witness. I found no mathematical counterexample.

The [primary paper](https://arxiv.org/pdf/2011.03647v2) is by Ricardo Gama and Hugo L. Fernandes. Every historical BKS/neural number matches Tables B.7/B.1, pp. 27/22. These are single-day benchmark rewards, not generated-tourist averages. Fresh public inputs match the frozen bytes and official commit a21f70183b6a92bbfa71fa67b8cbb36b59888dcf.

What I ran: newly written C++ raw parser/upper-certificate checker, importing no claimant search or verifier code; 225,910 states and 11,439,464 successor checks passed. Independent rational route checks passed for all fifteen under both travel conventions. Eighty brute-force fixtures passed; forged false uppers and empty covers were rejected on every claimed benchmark.

Full record: [Claim](friends/fernandes-orienteering/hb01-optw-optima/CLAIM.md) · [Referee report](friends/fernandes-orienteering/hb01-optw-optima/REPORT.md) · [Verdict](friends/fernandes-orienteering/hb01-optw-optima/VERDICT.md) · [Prior art](friends/fernandes-orienteering/hb01-optw-optima/PRIOR_ART.md)

---

# Hugo L. Fernandes: TOPTW pr11

Folder: [friends/fernandes-orienteering/hb16-toptw-pr11](friends/fernandes-orienteering/hb16-toptw-pr11)

**Verdict** (opening of [friends/fernandes-orienteering/hb16-toptw-pr11/VERDICT.md](friends/fernandes-orienteering/hb16-toptw-pr11/VERDICT.md))

HOLDS WITH CAVEATS
Referee: gpt-6.1-sol

The exact optimum is 654 for classical TOPTW long-window Cordeau pr11 with three vehicles. I found no counterexample or gap in the submitted numerical certificate.

My independently written checker closes all 46,749 states and 1,180,957 transitions, using exact integer travel and safe dominance. No claimant search/verifier code, suffix-knapsack pruning, or solver optimality status was used.
The verified bound is 1000×score ≤623716+3×11082=656962, hence score≤656. Raw prizes total657 and each is at least3, excluding655/656. Independently replayed routes attain654, omitting only customer19.

What I ran: fresh official download and byte comparison; independent primal and upper checks;40 exhaustive small fixtures with false-bound/missing-root attacks; five malformed-route attacks; fresh compilation/run of the unmodified public SISR baseline, whose new654 routes also pass my checker. My simple insertion control scored544. A separate all-customers CP test was inconclusive after120seconds and supplies no proof.

Full record: [Claim](friends/fernandes-orienteering/hb16-toptw-pr11/CLAIM.md) · [Referee report](friends/fernandes-orienteering/hb16-toptw-pr11/REPORT.md) · [Verdict](friends/fernandes-orienteering/hb16-toptw-pr11/VERDICT.md) · [Prior art](friends/fernandes-orienteering/hb16-toptw-pr11/PRIOR_ART.md)

---

# Hugo L. Fernandes: TOPTW c104

Folder: [friends/fernandes-orienteering/hb17-toptw-c104](friends/fernandes-orienteering/hb17-toptw-c104)

**Verdict** (opening of [friends/fernandes-orienteering/hb17-toptw-c104/VERDICT.md](friends/fernandes-orienteering/hb17-toptw-c104/VERDICT.md))

HOLDS
Referee: gpt-6.1-sol

The official short Solomon c104 TOPTW has optimum 1260 with at most four vehicles.
I independently reconstructed the official model and verified both bounds; no claimant search or verifier code was imported or read.
The freshly downloaded official raw file matches the claim's SHA256 exactly.
Travel truncation, service-start windows, depot return and disjoint customers match the official definitions.

Published comparison: Ševeček 2026 Table C.6 (printed 68/PDF 76) reports 1260 for c104 with four vehicles.
The university thesis record and PDF title page authenticate Jan Ševeček as its author.
Fresh thesis downloads were challenged; I inspected the retained actual PDF, not the challenge HTML.
Fresh Peng 2025 Table 6 reports 1260 in regular font at 7200 seconds, hence unproved by that run.
The convention is §5.5, printed 27; CLAIM.md's §5.4 citation is a harmless typo.

Full record: [Claim](friends/fernandes-orienteering/hb17-toptw-c104/CLAIM.md) · [Referee report](friends/fernandes-orienteering/hb17-toptw-c104/REPORT.md) · [Verdict](friends/fernandes-orienteering/hb17-toptw-c104/VERDICT.md) · [Prior art](friends/fernandes-orienteering/hb17-toptw-c104/PRIOR_ART.md)

---

# Oliveira e Silva: sign uncertainty, odd ℓ

Folder: [friends/oliveira-e-silva/db41-sign-uncertainty-odd/referee](friends/oliveira-e-silva/db41-sign-uncertainty-odd/referee)

**Verdict** (opening of [friends/oliveira-e-silva/db41-sign-uncertainty-odd/referee/VERDICT.md](friends/oliveira-e-silva/db41-sign-uncertainty-odd/referee/VERDICT.md))

HOLDS
Referee: gpt-6.1-sol

The stated formula A_minus_disc((ell^2-1)/2)=ell survives for every odd ell>=3.
I rederived the universal proof; it uses the paper's original unitary DFT,
common cutoff, origin signs and both normalized endpoint constraints.
The two nonnegative separators force whole residue classes to vanish, then
contradict the positive endpoint: H(q)=1+cos(pi/ell)>0.

The [paper](https://arxiv.org/html/2003.10771v4) already supplies the sine upper and conjectures equality;
relative to it, this contribution is the uniform lower proof, not a better upper.
I reproduced the sine control and explicitly rescaled it to meet both endpoints.
[Journal metadata](https://discreteanalysisjournal.com/article/84266-new-sign-uncertainty-principles) confirms Diogo Oliveira e Silva is a coauthor.

I wrote independent code, reading/importing none of the claimant's implementations.
On stats: exact cyclotomic DFT identities passed at ell=3,5,7,9,11,15;
256-bit Arb full-DFT/sign/support checks passed at eleven ell values through 51.
Fresh original/eigen primal LPs gave 20 feasible upper-cutoff results and
18 infeasible lower-cutoff diagnostics; two ell=31 runs were UNKNOWN, inconclusive.
Finite checks supplement the all-ell algebra; they do not prove its quantifier.
Broken-phase and next-cutoff controls were rejected. Subgroup sums alone fail
as a proof: an explicit relaxed vector satisfies them but fails the eigen equation.

Full record: [Claim](friends/oliveira-e-silva/db41-sign-uncertainty-odd/referee/CLAIM.md) · [Referee report](friends/oliveira-e-silva/db41-sign-uncertainty-odd/referee/REPORT.md) · [Verdict](friends/oliveira-e-silva/db41-sign-uncertainty-odd/referee/VERDICT.md) · [Prior art](friends/oliveira-e-silva/db41-sign-uncertainty-odd/referee/PRIOR_ART.md)

---

# Oliveira e Silva: sign uncertainty, adjacent jump

Folder: [friends/oliveira-e-silva/db41-sign-uncertainty-odd/referee-d003](friends/oliveira-e-silva/db41-sign-uncertainty-odd/referee-d003)

**Verdict** (opening of [friends/oliveira-e-silva/db41-sign-uncertainty-odd/referee-d003/VERDICT.md](friends/oliveira-e-silva/db41-sign-uncertainty-odd/referee-d003/VERDICT.md))

HOLDS
Referee: gpt-6.1-sol

Independent rigorous checks establish A_minus_disc(7320)=121, A_minus_disc(7321)=122, and A_minus_disc(7440)=122. The adjacent 121-to-122 change survives.

The [primary paper](https://arxiv.org/html/2003.10771v4), Problem 3.1, uses exactly the tested even unitary DFT, origin signs, common tail index and endpoint normalization. The [journal](https://discreteanalysisjournal.com/article/84266-new-sign-uncertainty-principles) confirms Diogo Oliveira e Silva is a coauthor.

Figure 3 really reports k=120,q=7081 and a minimum-tail-energy vector. I reproduced feasibility at that index; neither the submission nor this referee reproduces its energy minimum.

Ran independently written `independent_check.py` on the shared pod: 320-bit Arb, direct cosine sums over every tail coordinate, exact rational seeds, certified nonsingular correction systems, matching upper witnesses, and the q=5 direct-LP/exact controls. No claimant search or verifier code was opened or imported. Receipts and hashes: `pod_evidence/`.

All three lower certificates passed. Exact inner zeros follow algebraically from the correction equations, rather than numerical tolerances. Their remaining signs and positive endpoints contradict every feasible vector at the preceding index through DFT orthogonality. Five negative controls were rejected, including zero-endpoint and incorrectly strengthened certificates.

Full record: [Claim](friends/oliveira-e-silva/db41-sign-uncertainty-odd/referee-d003/CLAIM.md) · [Referee report](friends/oliveira-e-silva/db41-sign-uncertainty-odd/referee-d003/REPORT.md) · [Verdict](friends/oliveira-e-silva/db41-sign-uncertainty-odd/referee-d003/VERDICT.md) · [Prior art](friends/oliveira-e-silva/db41-sign-uncertainty-odd/referee-d003/PRIOR_ART.md)

---

# Oliveira e Silva: biharmonic attainment

Folder: [friends/oliveira-e-silva/db53-biharmonic-attainment/referee](friends/oliveira-e-silva/db53-biharmonic-attainment/referee)

**Verdict** (opening of [friends/oliveira-e-silva/db53-biharmonic-attainment/referee/VERDICT.md](friends/oliveira-e-silva/db53-biharmonic-attainment/referee/VERDICT.md))

HOLDS
Referee: gpt-6.1-sol

The proof supports reflection-even attainment and relative H² compactness of every Lp-normalized complex minimizing sequence for each fixed 3<=p<4 and epsilon>0. I found no gap in the stated scope.

The [published paper](https://doi.org/10.1007/s00526-023-02654-9) is coauthored by Diogo Oliveira e Silva. Its Appendix C/Theorem 4 gives axial attainment, and its reflection-even existence question is the relevant target. The claim retains the same complex space, quadratic form and Lp-squared denominator; no published numeric score is being beaten.

Why it holds: a real axial minimizer exists; the cited exponential-decay theorem applies below the free spectrum. The weighted convolution identity has the required positive transverse form, with PLUS lambda². Holomorphy handles zero ordinary axial mean. The real-power inequality gives strict binding below 2^(1-2/p)mG, and exact reflected residuals exclude escape even for complex profiles. REPORT.md details the functional justifications.

Full record: [Claim](friends/oliveira-e-silva/db53-biharmonic-attainment/referee/CLAIM.md) · [Referee report](friends/oliveira-e-silva/db53-biharmonic-attainment/referee/REPORT.md) · [Verdict](friends/oliveira-e-silva/db53-biharmonic-attainment/referee/VERDICT.md) · [Prior art](friends/oliveira-e-silva/db53-biharmonic-attainment/referee/PRIOR_ART.md)

---

# Marco Sampaio: FiFAR deferral costs

Folder: [friends/sampaio-fifar-deferral](friends/sampaio-fifar-deferral)

**Verdict** (opening of [friends/sampaio-fifar-deferral/VERDICT.md](friends/sampaio-fifar-deferral/VERDICT.md))

HOLDS WITH CAVEATS
Referee: gpt-6.1-sol

The five costs reproduce exactly: 102.04408, 107.65252, 84.82136, 102.34236, 98.75168.
They improve the paper's best costs 138.10604, 141.97164, 126.16748, 141.57996, 132.00812.
Both use total FN + .057 FP on the same 4,457 alerts, averaged over the same 25 variants per team, with identical review quotas.

I wrote independent code, downloaded fresh public sources, checked 250 original and 1,000 candidate evaluations, and refitted 2,000 logistic components.
All 500 selected heads' coefficients match; all conditional and classifier validation winners reproduce.
An independent integer solver reconstructs every one of the 125 headline assignments exactly; separate exact certificates check optimality for the registered rounded utilities.
The independently optimized class-frequency control costs 171.26268, 162.14964, 158.68900, 156.80104, 158.30044. Counts alone do not explain the gain.

Full record: [Claim](friends/sampaio-fifar-deferral/CLAIM.md) · [Referee report](friends/sampaio-fifar-deferral/REPORT.md) · [Verdict](friends/sampaio-fifar-deferral/VERDICT.md) · [Prior art](friends/sampaio-fifar-deferral/PRIOR_ART.md)

