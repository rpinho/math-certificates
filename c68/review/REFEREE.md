# Independent adversarial referee: candidate C68 ≥ 0.447

Job `math_c68ref_1104`, 4 November 2026. **No substantive mathematical defect or counterexample was found.** The contact-row argument, the one-coefficient correction, and the moment implication survive the checks below. Every finite moment and the entire scalar cover were recomputed, exceeding the requested sampling scope.

This review used fresh code, including a custom directed-rounding decimal interval implementation. **None of the candidate's or predecessor's verifiers was executed or imported.** Their saved PASS receipts and search counts are not evidence for this verdict. Floating searches below are explicitly separated from interval/exact checks. This is an independent AI mathematical review, not human specialist endorsement or proof-assistant formalization.

Unprefixed candidate-file references below are relative to `../c68r3/`.

The reviewed artifacts have SHA-256:

- `../c68r3/certificates/certificate-0447.json`: `d9dd308f94efb019368682367609d9fa71c9982bb7195b27da22bb80d02f4afe`.
- `../c68r3/certificates/row-cover.json`: `fda0aa1430313c3f896021073f3a44c3b1b920d2b07451d3b7d58d7d4d0bfc27`.

## (a) Definition match

**PASS.** I fetched upstream `main` into this job directory, without modifying the supplied external checkout. The fetched commit is `87b4ebbd426ff8db597a2004cc45da17903bdcf2`; its table is saved as `sources/upstream-68a.md`. The [rendered official table](https://teorth.github.io/optimizationproblems/constants/68a.html) was also read. The relevant source lines are `sources/upstream-68a.md:5–36`.

| Requirement | Finding and proof reference |
| --- | --- |
| Inequality direction | The hypothesis is $\lvert f\rvert\le \lvert u\rvert$, the conclusion is $\lVert f\rVert_2\le\lVert u\rVert_2$. Increasing the inner radius makes the hypothesis weaker. Proving admissibility at $447/1000$ therefore gives a **lower**, not upper, bound on the largest admissible radius. `../c68r3/PROOF.md:218–221,316–331`. |
| Annulus | The assumption is on the open outer annulus $447/1000<\lvert z\rvert<1$; it is not an inner-disk assumption. The moment variable is $t=r^2$, and its initial atom is $c^2=199809/1000000$. `PROOF.md:20–24,36–40,249–256`; `certificates/certificate-0447.json:3,8`. |
| Norm | Normalized area measure $dA/\pi$ gives $\lVert f\rVert_2^2=\sum \lvert a_k\rvert^2/(k+1)$, exactly the table's norm. `PROOF.md:327–329`. |
| Function class | Both functions are analytic on the whole disk and in $A^2$. The quotient need only be analytic on the annulus; its possible interior poles do not invalidate the whole-disk linear combinations. `PROOF.md:218–232`. |

The table's prose also says “analytic in the disk” without repeating finite norm. This does not create a mismatch: if the dominating function has finite norm, annular domination plus boundedness of the other analytic function on the compact inner disk implies its finite norm. If the dominating norm is infinite, the extended-norm inequality is automatic. The $u\equiv0$, constant-quotient, and unimodular cases are included.

The atom at $t=c^2$ is legitimate despite the strict annulus: the coefficient series are continuous there, and $g,\epsilon\to0$ as $t\downarrow c^2$. There is no atom at $t=1$, so no boundary values at the unit circle are assumed (`PROOF.md:246–256`).

## (b) Contact-row lemma and counterexample hunt

**PASS.** I checked the chain in `../c68r3/CONTACT_ROW_LEMMA.md:18–51` and `../c68r3/PROOF.md:46–98` step by step.

1. At a minimal enclosing hyperbolic disk, first variation gives a balancing convex combination of active image directions. Carathéodory reduces it to at most three contacts. Domain angles and image directions are different objects; the proof keeps them distinct (`PROOF.md:46–66`). Properness supplies the minimizing center. If the circle image is a point, the holomorphic map is constant by the identity theorem.
2. With the **same** balancing weights in every row, the Lorentz cosine rule gives $\sum_j\lambda_j\cosh d(p_i,p_j)=h^2$. Applying the pair bound in that row gives $h^2\le H^2-DT(\theta_i)$ for each contact. Taking the minimum of the right sides correctly yields $h^2\le H^2-D\max_iT(\theta_i)$. Averaging instead gives $S$. There is no unjustified interchange of extrema and averages (`CONTACT_ROW_LEMMA.md:18–27`; `PROOF.md:70–78`).
3. For $a>0$, $E X=a$, $E X^2=q_0$, and $-1\le X\le M$. Expanding the pointwise nonnegative product gives
   \[
   0\le E[(X+1)(M-X)]=M+(M-1)a-q_0.
   \]
   Thus $M\ge(q_0+a)/(1+a)$. At a support point attaining $M$, the first term of $T$ is $aM$, while its second term is nonnegative because $|m_2|\le1$. This proves the claimed $J$ bound with the correct sign and denominator (`CONTACT_ROW_LEMMA.md:29–42`). The extension $J=0$ at $a=0$ is continuous since $0\le J\le a$.
4. For any image point, $\zeta\le h$ and $h\zeta\le H^2-DT(\theta)$. Therefore both $\zeta^2\le h^2$ and $\zeta^2\le h\zeta$ are available. Combining them gives precisely $W=\max(S,J,T)$, and the positive-denominator estimate yields $v-g\ge QW$ (`PROOF.md:90–96,222–228`).

Fresh adversarial diagnostics in `attack_contacts.py` tested **200,000** probability measures with two, three, four, eight, or 32 support points, including highly concentrated weights, nearly coincident angles, and nearly antipodal supports. They tested the support inequality, both row floors, and PSD necessity. Apparent negative slacks were only floating roundoff, below $8\times10^{-16}$ in magnitude; no robust counterexample was found.

A separate **49,903** balanced three-contact construction generated image triangles enclosing zero, computed their balancing weights, and chose the largest radius allowed by every Fourier pair constraint. Every contact-row inequality passed; the smallest dimensionless slack was approximately $2.92\times10^{-8}$. These are geometric tests of the stated relaxation, not claims that arbitrary sampled contacts interpolate a holomorphic annular map. Receipt: `results/contact-attacks.json`.

`check_retained.py` also independently checked the exact two-contact endpoint and supplied rational three-contact example. The endpoint saturates the enclosing row bound with $S=J=0$. In the three-contact example, $S=666329/10291264\approx0.06475$, while $J\approx0.24821680556>S$; all rational pair constraints and balance identities pass. Receipt: `results/retained.json`; submitted data: `../c68r3/certificates/contact-configurations.json`.

**Retained falsification controls.** Fresh rational autocorrelations and interval trigonometric arc integration give:

| Test | Independent result |
| --- | --- |
| Old $0.105$ correction, $m_1=1/50,m_2=1$, retained degree-128 polynomial with $V_1=1$ | Old-weight energy lies in $[0.10445759407270062790,\ 0.10445759407270062791]$, strictly below $0.105$. |
| Same polynomial and moments, new row weight | Energy lies in $[0.66684114679730893521,\ 0.66684114679730893523]$, safely above $0.115$. |
| Naive three-coefficient $0.07$ extension at $m_1=0,m_2=1$ | Exact energy $87/400$, proposed right side $91/400$, exact gap **$-1/100$**. |

The first example is PSD: masses $51/100,49/100$ at $1,-1$ realize its moments. It must not be excluded using PSD. Those unequal masses do not by themselves give a balanced two-image-contact configuration; the old failure concerns the relaxed moment lemma. The submitted proof correctly makes no unsupported annular realizability claim (`CONTACT_ROW_LEMMA.md:95–98`; `PROOF.md:337–338`).

I also reproduced the failure of the tempting replacement $J=a$, using equal masses at $(\pm399+40i)/401$: $a=40/401$, $J=a^2\le S<a$. Thus the successful floor is materially weaker than an available false variant; it was not inadvertently strengthened in this review. The original construction is `../c68r3/AUXILIARY_FAILURES.md:7–20`.

## (c) The 23/200 correction, PSD, and Schur complement

**PASS, for coefficient one as stated.** The phase reduction preserves analyticity and $|U_1|$: rotation changes coefficient phases, reflection replaces $U(z)$ by $\overline{U(\bar z)}$, and a half-turn changes signs (`../c68r3/PROOF.md:108–124`).

For $m_2=b\ge0$, $m_1=x+iy$, the covariance matrix is
\[
\begin{pmatrix}(1+b)/2-x^2&-xy\\-xy&(1-b)/2-y^2\end{pmatrix}.
\]
Its determinant is one quarter of
$1-b^2-2(1-b)x^2-2(1+b)y^2$, exactly the submitted PSD condition. At $b=1$, the condition forces $y=0$. Only necessity is used; no PSD-to-contact-realizability theorem is assumed (`PROOF.md:110–121`; `CONTACT_ROW_LEMMA.md:61–78`).

The outer-function normalization is correct: the factor $1/2$ in the Herglotz kernel produces $C_0^2=\exp E\log W$ and $C_1/C_0=E(\log W e^{-i\theta})=d$. The first two product coefficients give
\[
E(W|U_r|^2)\ge C_0^2\bigl(|U_0|^2+|rU_1+dU_0|^2\bigr)
\ge\frac{C_0^2}{1+|d|^2}r^2|U_1|^2.
\]
The displayed square completion and the Hermitian $2\times2$ matrix have the correct conjugations. Uniform convergence of the Poisson integrals of continuous $\log W$ justifies the limiting integral without assuming boundary continuity of the harmonic conjugate (`PROOF.md:126–145`; `CONTACT_ROW_LEMMA.md:90–93`).

At the sole singular corner $a=0,b=1$, $W=(12/25)\sin^2\theta=(3/25)|1-e^{2i\theta}|^2$. The explicit even factor gives coefficient-one constant $3/25>23/200$. Its neighborhood is covered separately; it is not assigned a finite value of $\log0$. I checked the polynomial minorant, its unit-circle roots, integrable logarithms, and bin side conditions in `PROOF.md:185–213`. An independent density lower bound for the bins gives a strictly positive **log margin greater than 0.01569831525**, without using the submitted inverse-sine integration.

The full uniform scalar certificate passes; details are in (d). Additional floating searches made **79,528** scalar evaluations, including six differential-evolution searches over the PSD ellipse and near-singular endpoint paths. Refined quadrature values near the worst located parameters were about $0.11998$, above $0.115$; these are not certified global minima. Polynomial Toeplitz minimizations through degree 256 also found no violation. Coarse quadrature near the singular corner visibly shifts these estimates, so the verdict relies on the interval cover, not the optimization.

The correction is applied only to $y_1t$ in the disk coefficient inequality (`PROOF.md:238–244`) and only to $k=1$ in the weighted moments (`PROOF.md:258–263`). The failed third-diagonal claim is not reused. The dependence of the center $\alpha$ on $r$ is harmless: it cancels before integration, leaving a pointwise scalar inequality for fixed coefficient sequences.

## (d) Independent certificate and coverage checks

**PASS.** `intervals.py` uses 65-digit decimal endpoints with directed basic operations, integer powers by directed multiplication, outward-enclosed correctly rounded decimal square root/log/exp, Machin's formula for $\pi$, and Taylor trigonometry with explicit remainders. No Arb or mpmath arithmetic is used in the acceptance calculations. `audit_kernel.py` separately cross-checked exact rational operations and compared transcendental enclosures against 384-bit Arb; this is supplementary testing of the new kernel.

The atom ordering, positivity, $t_1=c^2$, $t_8=R=99/100$, and exact mass sum $\sum w_j=R$ pass (`../c68r3/certificates/certificate-0447.json:3–30`). The ordinary and weighted formulas match direct integration of the measure; $k=0$ is supplied by mass one and $\beta\le1$. Discarding the continuous $\epsilon$ correction has the favorable sign (`PROOF.md:254–263`).

`check_moments.py` independently checks **all** $1\le k\le5999$ ordinary moments and **all** $1\le k\le1799$ weighted moments. Relative margins below use the common normalization $(k+1)\,\mathrm{margin}/R^{k+1}$.

| Check | Certified result, rounded down |
| --- | --- |
| Ordinary minimum, $k=172$ | Relative margin $>7.8656249510\times10^{-6}$; absolute margin $>7.9905338710\times10^{-9}$. |
| Weighted minimum, $k=648$, cubic minorant | Relative margin $>7.6808224494\times10^{-6}$; absolute margin $>1.7394194542\times10^{-11}$. |
| Weighted $k=1$ | Absolute margin $>3.8546497770\times10^{-6}$. |
| Ordinary tail, every $k\ge6000$ | Exact $w_8\cdot6001-R=33/200000>0$. |
| Weighted tail, every $k\ge1800$ | Comparison at 1800 has gap $>8.8810763086\times10^{-10}$. |

Receipt: `results/candidate-moments.json`, including additional samples and full interval endpoints. The $0.44685$ predecessor's finite moments and both tails were also independently recomputed with this implementation, without its verifier (`results/baseline-moments.json`). This is a quantitative baseline check, not reliance on its old scalar certificate.

I rederived the cubic minorant by using the lower sine bound in the positive linear term and the upper sine bound in the negative square term; these directions are essential and correct (`PROOF.md:265–286`). To challenge that shared analytic formula, `check_integrals.py` independently encloses the **actual** continuous integrals using 1,000 interval cells and local log/sinc series for $g(t)/(1-t)$. It gives the weighted $k=648$ margin in
\[
[1.7604845344\times10^{-11},\ 1.8021775616\times10^{-11}],
\]
and also passes $k=1,2,172,647,649,1799$. Receipt: `results/direct-integrals.json`.

The ordinary tail follows from the last atom alone and monotonicity of $k+1$. For the weighted tail, $g(t)\ge\ell_0(1-t)$ on $[.999,.9992]$, so its integral is at least $\ell_0(1-b_0)(b_0-a_0)a_0^k$. After division by $a_0^k$, every atomic term decreases because $t_j/a_0<1$. This proves propagation, rather than merely testing some large indices (`PROOF.md:292–312`). Finite ranges and tail starting indices meet without an omitted integer.

**Scalar cover.** `check_scalar.py` reconstructs each box from its parent using exact rational splits, requires strict interior split points, visits both children, and checks the exact total volume. The root is precisely $[0,17/50]^2\times[7/10,1]$; outside it, the two elementary $S>23/200$ cases apply (`PROOF.md:123–124`). There are exactly **265 grid, 17 PSD, four constant, and one small leaf**.

For PSD leaves, the exact determinant expression is maximized at $(x_l,y_l,b_l)$, since its $b$-derivative is negative throughout the root. Every excluded box has strictly negative maximum. All constant floors pass. Grid leaves bound the whole angular cell and whole parameter box, rather than sampled points. My harmonic enclosure integrates the cell's phase exactly using $\sin(h)/h$, independently of the submitted midpoint phase-error estimate. Every grid leaf passes at its saved subdivision count; the minimum certified scalar difference is **greater than $2.7196904171\times10^{-5}$**. The small leaf is handled analytically as described in (c). There is no uncovered PSD boundary or $a=0$ endpoint. Receipt: `results/scalar-cover.json`; submitted coverage argument: `PROOF.md:147–214`.

Finally, the integrated coefficient series has nonnegative weights because $\beta-\epsilon>0$. Tonelli can therefore be used before asserting integrability, and the upper moment conditions supply its finite bound. The norm comparison follows with the correct sign (`PROOF.md:246–247,316–329`). As an extra floating diagnostic, 1,000 Laurent-quotient polynomial pairs at 30 radii passed the radial coefficient inequality and norm comparison (`results/transfer-attacks.json`).

## (e) Old-setting dependencies and final disposition

**No old-radius-only assertion was found in the dependencies actually used.** The mathematical content of `INPUT_GREEN_FLUX.md` and `INPUT_ANGULAR.md` is inherited from the predecessor, with attribution/textual edits. Both are formulated for a general $c$, conditional on explicit inequalities; their old date is not a hidden specialization to $0.44685$. The main proof imports only the first two sections of `INPUT_ANGULAR.md` (`PROOF.md:33–40`), not its old $9/320$ correction.

At the **new** $c=447/1000$, my interval lower bounds for the four required positive differences in `PROOF.md:28–31` exceed, respectively,
\[
0.3333143338,\quad277.9691994,\quad0.5272921787,\quad0.0895488135.
\]
Also $\Psi-6>26310.4966$. Thus the enclosing/Fourier hypotheses and the positivity argument are genuinely rechecked at the new radius, not inferred from an old receipt.

I independently reviewed the most sensitive inherited input. Distinct lifted poles are used in the strip Green comparison (`../c68r3/INPUT_GREEN_FLUX.md:23–62`). The selected zero contributes flux $-\phi(r)$, so the remaining flux is congruent to $\phi(r)$, with the correct sign (`INPUT_GREEN_FLUX.md:85–96`). In logarithmic coordinates the Green function has singularity $-\log\mathrm{distance}$; its Poisson representation therefore carries $1/(2\pi)$. Combining the inward derivative lower bound $K\pi/w$ with the two normalized boundary means gives exactly $K\pi|F_h|$, not twice or half that value (`INPUT_GREEN_FLUX.md:97–107`). Compact exhaustion avoids an assumption of boundary continuity of the original annular function (`INPUT_GREEN_FLUX.md:71–83`). The inverse-square conversion to hyperbolic distance is correct (`INPUT_GREEN_FLUX.md:112–126`).

The Fourier proof was checked in each of its three ranges, including the constants in the sine chord and decreasing $\tanh x/x$ comparisons (`../c68r3/INPUT_ANGULAR.md:27–53`). The obsolete half-actual-diameter interpretation is not needed: the submitted proof obtains its enclosing radius from balanced contacts directly.

As a further dependency check, the **same new measure** fails the old $19/200$ weighted $k=1$ condition. The independent direct-integral check gives an upper bound below $-0.00003325844346$, even after including an upper bound for the old continuous correction. Thus acceptance was not accidentally obtained by silently reusing the old constant or its moments. This says nothing about the optimal measure under the old criterion.

**Nonblocking documentation issues.** `../c68r3/CONTACT_ROW_LEMMA.md:6–7,84–88` still speaks prospectively about a numerical certificate; the completed statement and certificate are in `PROOF.md:100–214`. `INPUT_GREEN_FLUX.md:9,126–127` retains the old filename `ANGULAR_LEMMA.md`, whereas the supplied file is `INPUT_ANGULAR.md`. These are cross-reference/editorial defects, not missing mathematical premises. No mathematical repair is required by this review.

For reproduction, from this job directory, set `PY` to the shared research Python environment and run:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
nice -n 10 "$PY" -B audit_kernel.py
nice -n 10 "$PY" -B check_moments.py
nice -n 10 "$PY" -B check_scalar.py
nice -n 10 "$PY" -B check_integrals.py
nice -n 10 "$PY" -B check_retained.py
nice -n 10 "$PY" -B attack_contacts.py
nice -n 10 "$PY" -B attack_transfer.py
```

The four `check_*.py` calculations require only the Python standard library. The supplementary kernel comparison uses python-flint; the floating searches use NumPy/SciPy. All mathematical result files are in `results/`; `PRIOR_ART.md` records the source audit. `MANIFEST.json` pins the review code, mathematical receipts, and reviewed inputs. Work was local, at nice 10, with at most three concurrent numerical processes, and no pod use. No commits, pushes, PRs, posts, external messages, or original-verifier executions occurred. The next useful review would be human specialist scrutiny of the complex-analysis argument or formalization; the numerical hypotheses no longer depend solely on the submitting model's implementation.

VERDICT: HOLDS
