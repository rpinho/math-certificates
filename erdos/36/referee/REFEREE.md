# Erdős #36 gap certificates — HOLDS, conditional on the stated two-scale convention

**AI referee, unrefereed, not human review.** The 94 type-K certificates cover every mean in $0\le |m|\le1/160$. Every bin clears Unktok's full rational $L=0.380627625876591043727074\ldots$. The smallest margin is **+3.05183471885e-10** on $[0,0.00007]$. Among the 77 bins meeting $[0.000146,1/160]$, it is **+1.86649151230e-9**, on $[0.0001459,0.0001532]$. Together with round 1's outer cover and analytic/PSD results, this gives $\mu\ge L>0.38062762$ under the scalar convention specified below. New mathematical bound? **No.**

| Requested item | Verdict | Evidence |
|---|---|---|
| 1. Type-K lemma | HOLDS, six steps and reflection | Derivation below for arbitrary measurable densities |
| 2. Kernel and S12 ledger | HOLDS under the stated two-scale $L_0$ convention, carrying forward round 1's analytic and PSD results | The exact $C$ agrees. The rigorously payable scalar exceeds $N_0$ by $2.28302711346\times10^{-27}$. |
| 3. Positive-part integral | HOLDS | Arb enclosure of width $1.651\times10^{-19}$ or less, entirely below the supplied upper bound |
| 4. Exact certificates | HOLDS | 94 contiguous closed bins, 6,160,384 cell inequalities, zero violations |
| 5. Controls | HOLDS | Both raised thresholds, an infeasible slope, a flipped multiplier and a missing bin all reject |
| 6. Lawful densities | HOLDS for all seven examples | Exact peaks at grid shifts, including both signs, a shared endpoint and $1/160$ |

The producer was Claude Opus 5.5. This is a cross-family Codex review of fixed witnesses. Inputs were the supplied documents, Wetch data and certificate coefficients. The claimant's code and the gap producer's code were neither read nor run. The calculations below use the type-K replacement for the inner cover. Round 1 supplies the 87 outer bins on $[1/160,1]$ and the 17 original plus one two-scale PSD witness. Those computations were outside this replay.

## 1. The six steps for measurable h

Write $g_0=1-h$ on $[0,2]$, and extend both densities by zero. To distinguish the two functions called $g$ in the claim, write $G(t)=|\Phi(t)|+|\Phi(2-t)|$ for the folded weight. Fubini gives $p\ge0$, support in $[-2,2]$, and $\int p=1$.

1. **Odd profile — HOLDS.** Set $H(x)=\int_0^x h$ on the support and $R(t)=\int h(x)h(x+t)\,dx$. A translation gives $R(-t)=R(t)$. For $0\le t\le2$ the two overlaps of $h$ with the translated support indicator integrate over $[0,2-t]$ and $[t,2]$. Hence $p(t)=H(2-t)-R(t)$, $p(-t)=1-H(t)-R(t)$, and $d(t)=p(t)-p(-t)=H(t)+H(2-t)-1$. Thus $d(0)=0$, $d(2-t)=d(t)$, and $d$ is absolutely continuous with $d'=h(t)-h(2-t)$ almost everywhere. In particular $|d'|\le1$. Pairing the positive and negative shifts gives $m=\int_0^2 td(t)\,dt$. The substitution $t\mapsto 2-t$ in the upper half gives $m=\int_0^1[t+(2-t)]d(t)\,dt=2\int_0^1 d$.
2. **Even and odd split — HOLDS.** For $e=(p(t)+p(-t))/2$, the lesser and greater of the pair are $e-|d|/2$ and $e+|d|/2$. They lie in $[0,M]$ almost everywhere, hence $|d|/2\le e\le M-|d|/2$. The odd part integrates to zero against the even kernel. On the positive part of the kernel use the upper bound on $e$, and on the negative part use the lower bound. With $D=\int_{-2}^2\Phi_+$, this gives $\int p\Phi\le MD-\tfrac12\int_{-2}^2|d||\Phi|$.
3. **Fold — HOLDS.** Absolute values remove the sign of the odd profile, so the half-integral is $\int_0^2 |d(t)||\Phi(t)|\,dt$. Reflect $[1,2]$ into $[0,1]$. The identity $d(2-t)=d(t)$ makes the sum $\int_0^1|d(t)|G(t)\,dt$. Values assigned at step jumps have zero integral.
4. **Insert S12 — HOLDS conditional on S12.** Combining $N_0+Cm^2\le\int p\Phi$ with steps 2 and 3 gives $MD\ge N_0+Cm^2+\int_0^1|d|G$.
5. **Dual and boundary terms — HOLDS.** Take Lipschitz $u$ with $u(1)=0$ and $|\lambda-u'|\le G$ almost everywhere. Then $d(\lambda-u')\le |d|G$, for either sign of $d$. Integrating the left side gives $\lambda m/2-[du]_0^1+\int_0^1 d'u$. Both boundary terms vanish, at 0 by $d(0)=0$ and at 1 by $u(1)=0$. The product rule applies to absolutely continuous factors. Since $d'u\ge-|u|$, the return is at least $\lambda m/2-\int_0^1|u|$.
6. **Uniform bin bound — HOLDS.** For fixed $u,\lambda$, let $A(m)=N_0+Cm^2+\lambda m/2-\int|u|$. Its second derivative is $2C<0$. A point in a closed bin lies on a chord whose ordinate is at least the smaller endpoint value, and concavity puts $A$ above that chord. Each endpoint minimum is positive in the exact replay. Thus $M\ge\min(A(\mathrm{lo}),A(\mathrm{hi}))/D_{\rm up}$, using $0<D\le D_{\rm up}$.

**Reflection — HOLDS.** The reflected pair $h(2-x),g_0(2-x)$ is admissible. Substitution in the correlation gives $p_{\rm ref}(t)=p(-t)$. This reverses the first moment and preserves the norm. Since the joined cover is finite, its least bin bound applies to every $h$, and taking the infimum preserves the claimed lower bound.

## 2. Rebuilding the kernel and paying for S12

The kernel on positive shifts was assembled from the exact constant, quadratic and 314 merged cosines in selected-exact-kernel.json, the 241 fine-grid heights, the 17 Wetch rows and the periodic families. The extension is even. In particular, the claimant's ANALYTIC-REVIEW gives a normalized even hat with height $\gamma_0/a$ at 0 and $\gamma_k/(2a)$ at positive knots, where $a=2/n$. Each Wetch row contributes its piecewise linear interpolant times its multiplier. All data-file hashes in the proof manifest and both Wetch input hashes were checked. Analytic review (unktok repo, `proof/ANALYTIC-REVIEW.md`) · Coupling lemmas (unktok repo, `proof/COUPLING-LEMMAS.md`) · [Source arithmetic](referee_data.py)

For an occupied periodic source cell $i$, a positive integer lag ℓ sends its density to cells $\ell i$ through $\ell(i+1)-1$ modulo 131,072, with factor $1/ℓ$. This follows by substituting the dilated variable on that cell and folding successive periods. The source height is $nz_i/2$. Multiply by the signed pair weight and add the reflected cell with half weight in each orientation. The result equals exact-periodic-offsets.json on **all 131,072 cells**, with exactly 8,442 nonzero. The nine families each have three distinct positions, signs in $\{-1,1\}$, and nonpositive $z_i$.

| Contribution at zero mean | Rebuilt value, rounded |
|---|---:|
| Constant | −1.793955247275635 |
| Quadratic, $2y_2/3$ | −0.959846756670292 |
| 314 nonpositive retargeted cosine coefficients times sinc² | −0.0000810456238122923 |
| Nine periodic floor-weight sums | −0.000000113890756647 |
| 17 Wetch phase-Gram row scalars | +3.768773415151186 |
| Two-scale scalar times $2^{-20}$ | −0.0000000348680922851 |
| 52 stored paid-row charges with negative sign | −0.0148902168225982 |

For a single Wetch row the scalar is $\gamma\cdot B-d\cdot(1/3,1,\ldots,1,1/3)-z\cdot B-\sum w-\eta/12$. Here $B_0=1/2-a/12, B_n=a/24, B_k=(2-ka)/4$ at interior knots. The periodic scalar is the sum over families of $\lfloor(\sum b_i)^2/4\rfloor\sum z_i$. The quadratic coefficient combines $y_2/2$, the 17 weighted terms $-\eta/a^2$ and the fine/coarse terms $-2^{-20}(\eta+\lambda)/a_{\rm scale}^2$. This gives **exactly** the rational $C$ in target.json, approximately −0.719890984450839191.

**The convention.** Start the two-scale $L_0$ from the fine $\gamma\cdot B$. At each scale subtract the endpoint/interior diagonal payment, $\eta/12$, $2\lambda/19$ and $\beta(n-1)$. Subtract $\tau(z_c\cdot B_c+\sum w_c)$ for the fixed coarse terms. The source describes which terms receive τ and refers the complete scalar to code. This is the convention assumed here. Subtracting the paid hat heights from the assembled fine heights determines the common scale $2^{-20}$ from the first knot and reproduces all 241. Under this reading, $c_0-y_{0,\rm legacy}-\sum w\,c_{\rm paid}+2^{-20}L_0=0$ **exactly**. The reconstructed cosine sum also agrees exactly at all 314 frequencies. These equalities support the interpretation.

**The printed charges alone fall short.** Their sum with the other six contributions gives $N_0-3.13790137479\times10^{-28}$. For each Jensen row the coupling identity supplies $J=c\cos-aK_W+\kappa$ with nonnegative expectation. Here $c=\operatorname{sinc}^2(\xi a/2)$, $W_0=1, W_k=2\cos(\xi ak)$, and $\kappa=aW\cdot B-c\operatorname{sinc}^2\xi$. Thus the charge for the stored nonconstant coefficients is bounded above by κ plus the absolute cosine-coefficient error and the sum of absolute hat-weight errors. This uses $|E\cos|\le1$ and $0\le E K_{e_k}\le1$, since $p\le1$ and the normalized even hats have integral at most one. Arb at 220 bits enclosed each term and checked the supplied coefficient error bounds. All 52 row weights are nonnegative, and each stored charge covers its recalculated charge. Recovering only these justified savings supplies $2.59681725094\times10^{-27}$. The resulting lower expectation minus the exact stored $N_0$ is **positive**, $2.28302711346\times10^{-27}$ to the digits shown. This reproduces the section 6 ledger under the stated convention. [Exact ledger and per-bin results](replay.json)

## 3. Positive-part integral

A separate quadrature gives the following outward decimal enclosure. The replay uses its exact dyadic upper endpoint.

```text
2.62723966335267905439856972989 ≤ ∫ Φ₊ ≤ 2.62723966335267905456360040462
```

The upper endpoint is **1.37343639960e-15 below** the supplied 2.627239663352680428. It gives $N_0/D_{\rm up}=0.38062762752442546330\ldots$, or $L+1.64783441957\times10^{-9}$ at zero mean.

The union of the 1/65536 grid and all hat knots gives 131,948 smooth pieces on $[0,2]$. On blocks of width 1/512, a degree-36 Taylor polynomial encloses the cosine sum. Its derivative of order $d=0,1,2$ has uniform truncation error bounded by $\sum |z|\,|\xi|^{37}(1/1024)^{37-d}/(37-d)!$. The quadratic is included exactly. On each smooth interval the range uses the value and first two derivatives at its midpoint, the local affine term, and the third-derivative bound $\sum |z|\,|\xi|^3$. All evaluations use Arb balls. On sign-positive intervals the polynomial primitive and exact affine area are integrated with the uniform remainder paid. Negative intervals contribute zero. A sign-indefinite interval is bisected or charged between zero and its width times its upper bound. The calculation ended with 103,992 positive intervals, 61,543 negative intervals and 1,814 charged brackets. Doubling for evenness gives enclosure width $1.65031\times10^{-19}$. [Quadrature](referee_kernel.py)

## 4. Exact type-K replay

For each spatial cell, take the minimum of the absolute-value lower enclosures over its smooth pieces, round down to a multiple of $2^{-80}$, then add the corresponding bound for its reflected cell. On the omitted zero-slope prefix, comparison with the prefix minimum proves all its cell inequalities at once. All 188,365 explicitly supplied slopes were checked individually. The total is **94 × 65,536 = 6,160,384**. No slope failed. The smallest certified slack was **+1.317702029e-7**.

Starting at $u(1)=0$, integrate each rational slope backwards. All 94 prefixes came out exactly zero. For endpoint values $v,w$ on a cell of width $h_c$, the unsigned area is $h_c(|v|+|w|)/2$ if the signs agree or an endpoint is zero. For opposite signs the two triangles give $h_c(v^2+w^2)/(2|w-v|)$. There were zero interior sign crossings in these certificates. Each bin's exact integral, endpoint pair and rational margin appear in replay.json. For example, bin 17 gives $U=19669439415389818855661/1267650600228229401496703205376$.

The 93 shared boundaries agree as rationals, with first endpoint 0 and last endpoint $1/160$. The strict rational comparison against the full $L$ succeeds 94 times. Bin 17 begins at 0.0001459 and intersects the requested range starting at 0.000146. Its reported margin uses the whole certified bin. After the replay, comparison with the producer's vK_main.json found a maximum difference below $1.990\times10^{-16}$ across all 94 printed margins, consistent with the slightly tighter denominator. [Certificate checker](referee_check.py) · [Producer comparison](../results/vK_main.json)

## 5. Controls

| Mutation made in this replay | Rejection |
|---|---|
| Raise full $L$ by $10^{-9}$ | Exactly 1 of 94 bins fails. Bin 0 has margin −6.94816528115e-10. All 77 target-subrange bins still pass. |
| Raise full $L$ by $10^{-6}$ | 79 of 94 bins fail, indices 0–78. |
| Change only bin 17's last slope to λ plus a rigorous upper bound on that cell's $G$, plus $1/65536$ | Exactly one violation, cell 65,535. The numerical bin margin still reads +1.70044e-9, so a margin-only check would accept a false witness. |
| Reverse λ in bin 17, keep its slopes | 549 cell violations and margin −2.324498272e-8. |
| Remove bin 17 | An open interval remains uncovered between $1459/10000000$ and $383/2500000$. The neighboring closed bins retain the two endpoints. |

## 6. Lawful density spot-checks

On equal cells of width Δ with heights $h_i$, $p(k\Delta)=\Delta\sum_i h_i(1-h_{i+k})$, restricting both indices to the support. Between grid shifts the intersections of the translated cells vary affinely, so the maximum over **both** signs of the shift is the exact norm. The replay also integrated this interpolant to obtain its mass and first moment and checked the latter against $2-2\int xh$. At a shared bin endpoint the table uses the larger applicable bound.

| Density | $m$ | Exact peak rounded for display | Bin bound rounded | Bins (zero-based) |
|---|---:|---:|---:|---|
| Constant | 0 | 0.500000000 | 0.380627626 | 0 |
| Two half-interval heights | 0.002 | 0.499998000 | 0.380628105 | 70 |
| Symmetric 128-cell density | 0 | 0.381245447 | 0.380627626 | 0 |
| Tilted density at shared endpoint | 0.000070 | 0.381262071 | 0.380627628 | 0, 1 |
| Positive tilt | 0.000146 | 0.381280121 | 0.380627628 | 17 |
| Negative tilt | −0.000146 | 0.381280121 | 0.380627628 | 17 |
| Last gap endpoint | 0.006250 | 0.382735528 | 0.380631534 | 93 |

The symmetric example came from a bounded SLSQP fit that reached its 250-iteration limit. The heights were rounded to rationals, mass restored exactly, and the tilts formed by mixing with a unit-height half-interval density. The exact normalized examples suffice for spot-checks. No optimality claim is needed. The smallest fixture slack was **+0.00061782092349**. [Fixture construction](referee_fixtures.py) · [Rational heights and peak values](fixtures.json)

## Referee questions and scope

- **CONTROLS:** No assumption overrode a control. In replay.json, controls.raise_1e-9 rejects only bin 0, controls.slope rejects one cell despite a positive margin, and controls.flip rejects 549 cells. The raised target and punctured cover results are recorded above.
- **CONTRADICTING:** No adverse result was discarded. replay.json records the negative stored-minus-$N_0$ balance and the separately recomputed actual-minus-$N_0$ balance. The fixture optimizer's iteration limit is retained in fixtures.json. The universal claim follows from the inequalities, while the seven examples test their consequences.
- **LABELS:** No producer pass flag, float estimate or stored integral entered the inequalities. referee_data.py reads $L$ from RESULT.md and checks it exceeds the smaller target.json threshold. It rebuilds 314 cosines, 241 fine heights and the 131,072-cell scatter. referee_check.py computes every margin from the raw slopes. The inherited round-1 results and the inferred scalar convention are explicit premises here.

There is no statistical holdout. The witnesses were fixed before this review, there is no producer in this job, and the claim quantifies over all admissible densities. Finite arithmetic, a universal lemma and documented inherited results carry that quantifier. The remaining interpretive step is to match the written two-scale scalar above to the claimant's intended convention. No publication or outreach was performed. [Reproduction and sources](../README.md)
