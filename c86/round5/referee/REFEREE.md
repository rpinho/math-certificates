# Clean-room referee: C86 ≤ 1.8054939963

The supplied exact bound holds:

\[
C_{86}\le B=\frac{1561194641062402479525057156208744733}
{864691128455135125642991200018366464}
=1.80549399628008990359439902988223894\ldots
<1.8054939963.
\]

Date: 2026-11-09. Input: `../certificate.json:1`, SHA256 `e5fb93f6c31d2e3b38c986ac71c1d076414d680429fb2cbb91db77fb2e12c9d8`. I wrote the checker in this directory. I read only the five permitted producer files, not any producer program or any prohibited repository program. The producer's reported checks were comparison data, not premises of this verdict. Arithmetic uses Python exact fractions and standard FLINT/Arb at 192 bits, with one FLINT thread per worker.

## (a) Definition and theorem

The [live table](https://teorth.github.io/optimizationproblems/constants/86a.html), fetched on 2026-11-09 and retained in the table source identified in sources/SOURCES.md, defines the constant verbatim as follows:

> The Schur–Siegel–Smyth trace constant is the smallest limiting trace-to-degree ratio
>
> \[C_{86} \;:=\; \liminf_{\alpha \in \mathcal{A}} \overline{\mathrm{tr}}(\alpha),\]

Here \(\mathcal A\) consists of algebraic integers whose conjugates are all real and strictly positive, and \(\overline{\mathrm{tr}}\) is the sum of the conjugates divided by their number. The liminf disregards finitely many exceptional algebraic integers. The certificate bounds this constant, not a finite-degree or restricted-auxiliary variant.

I located **Theorem 1.5 and Proposition 5.15** in Alexander Smith, [*Algebraic integers with conjugates in a prescribed distribution*](https://arxiv.org/html/2111.12660v2#S1.Thmthm5), Annals of Mathematics 200 (2024), 71–122; the paper’s URL and source hash are listed in sources/SOURCES.md. Theorem 1.5 concerns a compact real set Σ with at most countably many connected components and capacity greater than one. A Borel probability measure ν supported there is a limit of conjugate-counting measures of distinct irreducible monic integer polynomials with roots in Σ if and only if every nonzero integer polynomial P satisfies \(\int\log|P|\,d\nu\ge0\). Proposition 5.15 supplies a sufficient criterion using distinct primitive irreducible integer auxiliaries, positive weights, weighted degree at most one, their nonnegative log integrals, and a potential inequality on **all of the complex plane**. Smith defines potential with a minus sign.

Here is the exact criterion used by this referee, written for the certificate's unnormalized measure μ and positive-log convention. Let \(m=\mu(\mathbb R)>0\), \(T=\int x\,d\mu\), and \(D=\sum_j b_j\deg Q_j\). It suffices that:

1. μ has a bounded continuous nonnegative density with compact support K contained in a positive interval Σ of capacity greater than one.
2. The \(Q_j\) are distinct primitive irreducible nonconstant integer polynomials, and \(b_j>0\). Zero-weight auxiliaries could simply be omitted. Neither real-rootedness nor monicity nor any restriction on their traces is required.
3. \(D<m\), and every \(\int\log|Q_j|\,d\mu\ge0\).
4. With \(U_\mu(z)=\int\log|z-t|\,d\mu(t)\),
   \[f(x)=U_\mu(x)-\sum_j b_j\log|Q_j(x)|\ge0\qquad(x\in K).\]

The strict degree inequality is stronger than Proposition 5.15 requires, and permits the following extension. The bounded density gives a finite continuous potential. Outside K and the auxiliary roots, f is harmonic; at each auxiliary root f tends to positive infinity. Uniformly at infinity,
\(f(z)=(m-D)\log|z|-\sum b_j\log|\operatorname{lc}Q_j|+o(1)\to+\infty\).
Apply the minimum principle inside a large disk with K and small disks about auxiliary roots removed. Its boundaries have nonnegative limiting values. Consequently f≥0 throughout ℂ, including the gaps of K, negative real numbers and nonreal points. No numerical truncation of the plane is being assumed.

Normalize **both** measure and weights: \(\nu=\mu/m\), \(a_j=b_j/m\). These satisfy Proposition 5.15. For completeness, the resultant calculation also explains the criterion. For a primitive irreducible integer P, distinct up to sign from all selected auxiliaries, with leading coefficient c and roots αₖ,

\[
\begin{aligned}
\int\log|P|\,d\mu
&=m\log|c|+\sum_k U_\mu(\alpha_k)\\
&\ge(m-D)\log|c|+\sum_j b_j\log|\operatorname{Res}(P,Q_j)|\ge0.
\end{aligned}
\]

The resultants are nonzero integers. The selected factors have their own verified integrals; factorization and integer constants cover all other P. This also handles nonmonic auxiliaries: their leading-coefficient contributions must be retained.

For this certificate take \(\Sigma=[1/1000,13]\), one compact positive interval, whose capacity is its length divided by four, \(12999/4000>1\). All hypotheses above are checked in (b)–(d). Theorem 1.5 then gives limiting conjugate measures inside Σ; since x is continuous on that compact interval, their normalized traces converge to T/m. Thus \(C_{86}\le T/m=B\). B is the **mean**, not the threshold in the potential inequality; that threshold is zero.

## (b) All 31 auxiliaries

Every coefficient is an integer, every polynomial is primitive, and exact FLINT factorization returns the polynomial itself with exponent one. All 31 are distinct, have positive rational weights, and happen to be monic. These checks are in `referee_check.py:60`; complete coefficients, certified root enclosures and integral enclosures are in `receipts/structure.json:1`. I compared each index, coefficient array, degree, weight and nonreal-root count with the permitted provenance JSON, and all agree.

The table follows **certificate order, starting at zero**, not sorted degree order. R and C count real and nonreal roots respectively. FLINT encloses all roots; multiplicities are one. A real root has exactly zero imaginary part, while each nonreal enclosure excludes zero in its imaginary part; no root classification remains unresolved.

| Index | Degree | R | C | Exact weight |
|---:|---:|---:|---:|---|
| 0 | 1 | 1 | 0 | 6234769750467/156250000000000 |
| 1 | 1 | 1 | 0 | 320579733556009/10000000000000000 |
| 2 | 1 | 1 | 0 | 95603495557957/5000000000000000 |
| 3 | 2 | 2 | 0 | 26623593314633/1250000000000000 |
| 4 | 3 | 3 | 0 | 58 677 979 602 683/5000000000000000 |
| 5 | 4 | 4 | 0 | 82007373033751/10000000000000000 |
| 6 | 4 | 4 | 0 | 16 874 132 497 017/2000000000000000 |
| 7 | 5 | 5 | 0 | 40114062658883/10000000000000000 |
| 8 | 5 | 5 | 0 | 6000772835327/1250000000000000 |
| 9 | 5 | 5 | 0 | 19393015927477/10000000000000000 |
| 10 | 5 | 5 | 0 | 56555045423073/10000000000000000 |
| 11 | 10 | 10 | 0 | 43136630913737/10000000000000000 |
| 12 | 10 | 10 | 0 | 14993265284203/5000000000000000 |
| 13 | 10 | 10 | 0 | 11201415865187/5000000000000000 |
| 14 | 8 | 8 | 0 | 2084779942869/625000000000000 |
| 15 | 8 | 8 | 0 | 441378712113/200000000000000 |
| 16 | 7 | 7 | 0 | 22930634261769/10000000000000000 |
| 17 | 2 | 2 | 0 | 39528074436539/5000000000000000 |
| 18 | 3 | 3 | 0 | 22174717/5000000000000000 |
| 19 | 8 | 6 | 2 | 21581298302833/10000000000000000 |
| 20 | 12 | 8 | 4 | 68032205277937/10000000000000000 |
| 21 | 12 | 8 | 4 | 55050453782297/10000000000000000 |
| 22 | 14 | 10 | 4 | 2456478340843/625000000000000 |
| 23 | 14 | 12 | 2 | 33965908274817/10000000000000000 |
| 24 | 14 | 10 | 4 | 29914773051193/10000000000000000 |
| 25 | 17 | 15 | 2 | 26370879922467/10000000000000000 |
| 26 | 21 | 17 | 4 | 13173823606147/5000000000000000 |
| 27 | 14 | 12 | 2 | 9028531/10000000000000000 |
| 28 | 20 | 14 | 6 | 1627952347/10000000000000000 |
| 29 | 16 | 16 | 0 | 76637/1250000000000000 |
| 30 | 13 | 11 | 2 | 1020657/10000000000000000 |

There are 269 roots in total: 233 real and 36 nonreal. Exactly 11 auxiliaries have nonreal roots; the maximum degree is 21. The root enclosures also show that 176 real auxiliary roots lie in K and 57 lie outside it. The former are included in the closed-cover treatment; the latter and all nonreal roots are covered by the minimum-principle argument.

Exact weighted degree and slack are

\[
D=\frac{8987862395895077}{10000000000000000},\qquad
m-D=\frac{101213760410492177}{1000000000000000000}>0.
\]

This agrees exactly with the claimed weighted degree. Direct analytic integration, with certified root enclosures, proves **all 31** log integrals strictly positive. The smallest is for index 11:

\[
\int\log|Q_{11}|\,d\mu
\in[9.999628196720546414081188216203904009\times10^{-11}
\ \pm\ 5.23\times10^{-48}].
\]

The producer reports approximately \(9.99962819672\times10^{-11}\) (the producer’s report), in agreement. Root integrals use \(m\log|\operatorname{lc}Q|+\sum_{Q(r)=0}U_\mu(r)\); the leading-coefficient term is included even though it vanishes for these monic inputs.

## (c) Density, exact mass and normalization

All **7,418** nodes are rational and strictly ordered. Every rational height is nonnegative: 6,270 are positive and 1,148 are zero. Both endpoint heights are zero, so linear interpolation followed by zero outside the grid gives a continuous bounded nonnegative density. “Positivity” here means nonnegativity everywhere, not strict positivity at every node. There are **6,308** cells with positive density in their interiors, forming 37 closed support components.

The support's extreme endpoints are
\[
\frac{7602076171001397}{144115188075855872}
\quad\hbox{and}\quad
\frac{6325868626595283}{1125899906842624},
\]
approximately 0.05275 and 5.6185, so it lies strictly inside Σ. The enclosing node grid starts earlier, approximately 0.0215; its initial zero cells carry no mass.

For an edge interval [u,v] with heights a,b, I sum its exact mass \((v-u)(a+b)/2\) and exact first moment \((v-u)((2u+v)a+(u+2v)b)/6\). This gives

\[
m=\frac{999999999999999877}{1000000000000000000},\qquad
T=\frac{1561194641062402479525057156208744733}
{864691128455135232000000000000000000}.
\]

The mass deficit is exactly \(123/10^{18}\). The checker verifies **exactly** that the declared B equals T/m (`referee_check.py:48`). Treating T alone as the bound would be incorrect. Dividing μ and every auxiliary weight by m preserves the potential and log-integral inequalities and yields a probability measure. No atom, tail, or unverified correction is added to fill the mass deficit.

## (d) Rigorous potential inequality and closed cover

The referee’s own implementation is `cover_check.py:13`, using 192-bit Arb arithmetic and order-32 Taylor models. It proves f≥0 over the entire closed support, including every density-node endpoint and neighborhoods of every auxiliary root in the support. The remaining plane is handled analytically in (a).

Here are the formulas underlying the implementation. Extend the piecewise-linear density by zero and let sᵢ be its slope jump at eᵢ. Define

\[
H(t)=\tfrac12t^2\log|t|-\tfrac34t^2,\quad H(0)=0.
\]

Since H″=log|t|, integration by parts twice gives
\(U_\mu(x)=\sum_i s_iH(x-e_i)\).
There are 6,324 nonzero slope jumps; their sum and their first moment are checked to vanish exactly. For nonreal z, the corresponding formula is the real part of \(\sum_i s_i((z-e_i)^2\log(z-e_i)/2-3(z-e_i)^2/4)\), giving the analytic log integrals in (b). The real limit is evaluated with H, including its continuous value at zero.

On a parent interval x=c+ht, −1≤t≤1, terms with distance d from the center satisfying |d|>4h are expanded through degree n=32. With q=h/|d|, their rigorous remainder bounds are

\[
|s_i|\,|d|^2\frac{q^{n+1}}{(n+1)n(n-1)(1-q)}
\quad\text{for }s_iH,
\qquad
b_j\frac{q^{n+1}}{(n+1)(1-q)}
\quad\text{for }-b_j\log|x-r|.
\]

The first follows from the coefficients of H, whose absolute degree-k coefficient for k≥3 is \(h^k/(k(k-1)(k-2)|d|^{k-2})\); the second is the logarithm series. Arb encloses the coefficients, root uncertainty and remainder. The constant error ball bounds function values uniformly; derivative estimates below are for the polynomial approximation itself, so no derivative bound on that constant error is assumed.

Near density nodes, the implementation explicitly checks |x−eᵢ|<1 on the parent interval. H is concave there, including across zero. A positive slope-jump multiple is bounded below by its chord on each leaf; a negative multiple is bounded below by its tangent. This avoids differentiating through a logarithmic singularity. Near an auxiliary root, an interval excluding that root uses the exact log value and first derivative with a lower second-derivative enclosure. An interval possibly containing the root uses \(-b\log(\max|x-r|)\); at the root itself the term is +∞.

After combining these lower functions, a leaf of normalized midpoint v and radius r has lower bound
\(g(v)-|g'(v)|r+\min(0,L)r^2/2\), where L bounds the second derivative of the remaining smooth lower function throughout that leaf. All inequalities are outward enclosed; no floating-point scan establishes positivity.

The run subdivided wide initial cells to width at most 1/256, yielding 6,435 parent pieces, then used exact rational bisection. It produced **131,912 closed leaves**, maximum bisection depth 15. I also reassembled their rational endpoints: every parent is covered without a gap, and the parents cover exactly all 6,308 original positive-density cells. The regenerable leaves are omitted; their SHA-256 and regeneration command are in sources/SOURCES.md. Summary numbers are in receipts/cover.jsonl.summary.json and receipts/results.json.

The smallest proven lower bound is

\[
[6.66440388580153139845456961216701913478817308780529906273
\times10^{-14}\ \pm\ 5.04\times10^{-71}],
\]

so the simple decimal lower bound **6.6644×10⁻¹⁴** is rigorous. It occurs on the leaf

\[
\left[
\frac{321990484858387835}{144115188075855872},
\frac{160995805379147339}{72057594037927936}
\right]
\subseteq[e_{4255},e_{4256}],
\]

approximately [2.2342578125000000719, 2.2342656250000000745]. Indices are zero-based.

| Checker | Smallest proven leaf lower bound | Location reported |
|---|---:|---|
| This referee | >6.6644×10⁻¹⁴ | Exact leaf above, original cell 4255 |
| Producer, first | 1.88431271694×10⁻¹³ | Not stated in the permitted REPORT.md |
| Producer, second | approximately 5.02539848201868×10⁻¹³ | Not stated in the permitted REPORT.md |

The producer values are at the producer’s report and the producer’s report. I did not access its unpermitted cover files to recover those locations. These are different conservative cover bounds, not competing estimates of the true minimum. The reported LP target of 5×10⁻¹⁰ (the producer’s report) is a search setting and is not claimed here as a certified uniform margin.

## (e) Referee corruption controls

All controls are implemented in `corruption_controls.py:16` using this referee's routines, with outcomes in `receipts/corruptions.json:1`.

| Corruption | Rejection |
|---|---|
| Raise declared B by 1/1,000,000 | Exact equality B=T/m fails. |
| Raise weight of Q₀=x by 1/1,000 | The weighted-degree condition still passes, but f(3) lies in [−0.0010968345264709833068173688513248962296441681873 ± 7.84×10⁻⁵⁰]. |
| Lower node 4475's height by 1%, keeping nodes ordered and heights nonnegative, and **recompute B=T/m** | The Q₀ log integral lies in [−1.72472692348227489735615670062670094315095516×10⁻⁵ ± 4.48×10⁻⁵⁰]. |

The density node was selected by this referee as the largest-height node at coordinate greater than 2. Its coordinate is 5206724119193715/2251799813685248. This differs from the producer's node-5538 control. For the weight control the remaining degree slack is still exactly 100 213 760 410 492 177/10¹⁸, so rejection genuinely uses the potential inequality. Both negative intervals exclude zero by a large margin.

A raised numerical upper bound would, of course, remain a valid weaker consequence of the original proof. The first control rejects it **as a falsely declared exact normalized mean**, not as a false mathematical upper bound. The other two controls demonstrate substantive violations of the sufficient criterion, not merely mismatched metadata.

## (f) Decimal, public comparison and proof review

Exact arithmetic gives

\[
1.8054939963-B
=\frac{168125817662203443341292651223243}
{8444249301319678961357335937679360000000000}
=1.9910096405600970\ldots\times10^{-11}>0.
\]

Thus the stated ten-decimal round-up is valid. The [live PR #270](https://github.com/teorth/optimizationproblems/pull/270) gives the comparison fraction
\(P=780597977251274792019360777060007/432345564227458232572250425393152\).
The exact improvement is

\[
P-B=
\frac{1313440541894730750781924990269697769655655727}
{864691128454916358787492050831578787226395353284608}
=1.518970761550043454167272764237\ldots\times10^{-6}>0.
\]

This comparison uses the same constant and the exact public fraction, not merely its displayed 1.8054956. The official table itself still displays the older 1.8084990. Prior-source searches and their limits are recorded in `../PRIOR_ART.md`; this referee does not make an exhaustive worldwide priority claim.

I find no mathematical error or missing hypothesis in the application in `sources/producer-proof.md:3`, `sources/producer-proof.md:13`, `sources/producer-proof.md:15`, `sources/producer-proof.md:23`, or `sources/producer-proof.md:27`. In particular:

- Complex auxiliary roots are allowed by Proposition 5.15 and the minimum-principle extension.
- Mass below one is handled by normalizing both density and weights, and by using T/m.
- Integrality alone is not substituted for irreducibility: all selected factors were checked.
- Nonnegative log energy follows from the checked inequalities; Smith's negative-log energy consequently has the opposite sign (`sources/producer-proof.md:25`). There is no extra unverified energy hypothesis in this application.
- Strict positivity at the nodes is unnecessary. The density's zeros and all closed support endpoints were included.
- The producer's implementation and search-history statements at `sources/producer-proof.md:31` and `sources/producer-proof.md:43` were not replayed and are not used. No global optimality or originality of auxiliary polynomials is inferred.

**Did this referee find something new? No.** This is a clean-room AI verification of the supplied candidate, which numerically improves the specified public fraction. All mathematical items (a)–(f) have been checked; none was left unfinished for lack of time. No caveat qualifies the bound. The producer's undisclosed minimum-leaf locations are the reporting limitation identified in (d), not a missing part of this proof.

Reproduce from this directory, with ordinary Python assertions enabled:

```sh
nice -n 10 python referee_check.py ../certificate.json --output structure.json
nice -n 10 python cover_check.py ../certificate.json --workers 4 --output cover.jsonl
nice -n 10 python corruption_controls.py
```

The full support run took approximately 115 seconds with four workers. No prohibited code was used in the referee run.

VERDICT: HOLDS
