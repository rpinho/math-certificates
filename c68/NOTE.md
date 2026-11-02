# A sixteen-atom certificate for Korenblum's constant

Both independently written exact checkers prove

$$C_{68}\geq\frac{8527693}{20000000}=0.42638465.$$

The best public certified lower bound located is Wikström's $0.4263$. The gain
is exactly $1693/20000000=0.00008465$. This is an improvement of his explicit measure,
using the same annular estimate and moment-duality lemma. His paper already
reports an apparent numerical limiting value near $0.42639$; no new method or
proof of that limit is claimed here. The current priority audit is documented
in `FINAL_LIVE_CHECK.md`. This retained note is part of an unrefereed preprint.

## Analytic input

Normalize the Bergman norm by $dA=dx\,dy/\pi$. Then
$\|\sum a_kz^k\|_2^2=\sum |a_k|^2/(k+1)$. Korenblum's constant is the supremum
of radii $c$ such that $|f|\leq |g|$ on $c<|z|<1$ implies
$\|f\|_2\leq\|g\|_2$ for all $f,g\in A^2(\mathbb D)$.

We use Wang's annular coefficient estimate as recorded in Proposition 2.1 of
Frank Wikström, [*Moment duality and an improved lower bound for Korenblum's
constant*, arXiv:2607.17748](https://arxiv.org/abs/2607.17748). For $c<r<1$, set

$$K_c(r)=2r(1+c/r^2)\prod_{n\geq1}
\frac{(1+r^2c^{2n-1})(1+r^{-2}c^{2n+1})(1+c^{2n})^2}
{(1+r^2c^{2n-2})(1+r^{-2}c^{2n})(1+c^{2n-1})^2},$$

$$G_c(r)=\frac12\left(1+\sqrt{\frac{1+3K_c(r)^2}{1-K_c(r)^2}}\right),
\qquad \beta_c(r)=1-\frac1{G_c(r)}.$$

Use the limiting endpoint conventions $\beta_c(c)=\beta_c(1)=1$.
Wikström's Lemma 3.1 says that $c$ is admissible if a probability measure $\mu$
on $[c^2,1]$, with no atom at $1$, satisfies

$$\int t^k\,d\mu(t)\geq\frac1{k+1}\quad(k\geq0),\qquad
\int\beta_c(\sqrt t)t^k\,d\mu(t)\leq\frac1{k+1}\quad(k\geq1).$$

The reduction is short. Write $d_k=|a_k|^2-|b_k|^2$,
$x_k=(d_k)_+$, $y_k=(-d_k)_+$, $X(t)=\sum_{k\geq0}x_kt^k$, and
$Y(t)=\sum_{k\geq1}y_kt^k$. Wang's estimate gives
$X(t)\leq y_0+\beta_c(\sqrt t)Y(t)$. Integration and the two moment inequalities
then give $\sum x_k/(k+1)\leq y_0+\sum_{k\geq1}y_k/(k+1)$, which is the norm
comparison. Monotone convergence applies to the nonnegative series. This is
the existing lemma, recalled to specify precisely the analytic input being used.

## Frozen rational measure

Take $c=8527693/20000000$, $s=c^2$, $R=9999/10000$, and

$$d\mu(t)=\sum_{j=1}^{16}w_j\,d\delta_{t_j}(t)+\mathbf1_{[R,1]}(t)\,dt.$$

Every number in the following table is an exact terminating decimal, generated
from `certificate-tight.json`. The first node is $s$, the last is $R$, the
weights are positive, and their sum is exactly $R$. Thus the total mass is one
and there is no atom at one.

| j | Exact t_j | Exact w_j |
|---:|---:|---:|
| 1 | 0.1818038697556225 | 0.392591370153232813 |
| 2 | 0.578860901323522081 | 0.335102037116834284 |
| 3 | 0.816748526665954211 | 0.155658604815309881 |
| 4 | 0.920636280782610061 | 0.065163284137667435 |
| 5 | 0.964292839891460529 | 0.027734797819002267 |
| 6 | 0.983207912383541771 | 0.012312342738629063 |
| 7 | 0.991771010123177366 | 0.005713278100737342 |
| 8 | 0.99581760378264883 | 0.002760807795092819 |
| 9 | 0.997804910520264654 | 0.001382494612372999 |
| 10 | 0.9988141037359759 | 0.000713743357541805 |
| 11 | 0.999341144341006515 | 0.000377584152859495 |
| 12 | 0.999622064978637259 | 0.000202606269915487 |
| 13 | 0.999772642549583868 | 0.000107779049291705 |
| 14 | 0.999850996068241016 | 0.000053743284896758 |
| 15 | 0.999887570912487478 | 0.000022358102741742 |
| 16 | 0.9999 | 0.000003168493874105 |

The earlier published measure has eight atoms and $R=0.99$. We enlarged the
support, moved the cutoff closer to one, and reoptimized the nodes and weights.
After rounding the interior data to rational numbers, the first weight was set
by exact mass balance. Floating search values have no certification status.

## A polynomial lower bound replaces numerical quadrature

Put $g(t)=1/G_c(\sqrt t)$ and $e=1-10^{-10}$. The certificate supplies four
rational coefficients $a_1,\ldots,a_4$ for

$$L(t)=\sum_{m=1}^4 a_m(1-t)^m.$$

| m | Exact a_m |
|---:|---:|
| 1 | 281978918242459592675501/12500000000000000000000000 |
| 2 | 1102471797710579921122539/100000000000000000000000000 |
| 3 | -687233054144974275316103/125000000000000000000000000 |
| 4 | -168163398237114755212421/12500000000000000000000000 |

The checkers prove $0<L(t)<1$ and $L(t)\leq g(t)$ throughout $[R,e]$.
The fit used to propose the coefficients is irrelevant to this proof.

Let $K_{c,N}$ be the product truncated at $N=52$. For $t\geq R$, the sum of the
absolute values of the omitted logarithms is at most

$$E=\left(1+3c+2c^2+\frac{c^3+c^2}{R}\right)
\frac{c^{2N}}{1-c^2}.$$

Indeed, bound each omitted $|\log(1+x)|$ by $x$ and sum the geometric series.
Since $0<E<1$, $\exp(E)\leq(1-E)^{-1}$. Write the rational function
$K_{c,N}(\sqrt t)^2=P(t)/Q(t)$, where $Q(t)>0$ on $[R,e]$. Thus
$K_c(\sqrt t)^2\leq P(t)/(Q(t)(1-E)^2)$.
For $0<L<1$, direct algebra gives

$$\frac{2}{1+\sqrt{(1+3q)/(1-q)}}\geq L
\quad\Longleftrightarrow\quad
q\leq\frac{1-L}{1-L+L^2}.$$

It therefore suffices to prove positivity of the rational polynomial

$$F(t)=(1-L(t))(1-E)^2Q(t)-(1-L(t)+L(t)^2)P(t).$$

The polynomial has degree **218**. After clearing denominators and removing
its positive integer content, its independently reconstructed integer
coefficient vector has SHA-256

```
c2af0de448f090d881795bf106a05eb3a56f04d60e9ef8d88594ee3e2da496e5
```

The first checker composes $F(R+(e-R)x)$ exactly with Flint, then checks every
Bernstein coefficient on $[0,1]$ is positive. The second independently clears
all input denominators using only Python integers and applies homogenized
Horner evaluation to

$$(1+x)^{218}F\!\left(\frac{R+ex}{1+x}\right)\qquad(x\geq0),$$

with a common positive denominator cleared. Every resulting integer
coefficient is positive. One interval covers the entire $[R,e]$; this is not a
sampled positivity test. Both methods give the same primitive-polynomial hash.
The elementary coefficient bounds in the checkers also prove $0<L<1$.

Consequently, writing $L(t)=\sum_{j=0}^4\ell_jt^j$, a rigorous integral lower
bound for every integer $k\geq1$ is

$$\int_R^1g(t)t^k\,dt\geq
\sum_{j=0}^4\ell_j\frac{e^{k+j+1}-R^{k+j+1}}{k+j+1}.$$

The positive contribution on $[e,1]$ is explicitly discarded. The right side
is a finite rational expression; neither checker uses numerical quadrature.

## Every moment index is covered

Define

$$A_k=\sum_jw_jt_j^k-\frac{R^{k+1}}{k+1},$$

$$B_k=\int_R^1g(t)t^k\,dt+\frac{R^{k+1}}{k+1}
-\sum_jw_j\beta_c(\sqrt{t_j})t_j^k.$$

The desired two moment families are exactly $A_k\geq0$ and $B_k\geq0$.
Both checkers verify the following:

- $A_0=0$ by exact mass balance. The finite indices $1\leq k\leq315574$
  are checked explicitly. For $k\geq315575$, the atom at $R$ alone gives
  $w_{16}(k+1)\geq R$, proving the whole tail.
- The finite indices $1\leq k\leq239999$ in the second family are checked
  using the proven polynomial integral lower bound and rigorous upper bounds
  for the atomic $\beta$ values.
- For the second tail take $t_0=0.99998$, $t_1=0.99999$. Both checkers explicitly
  prove $-L'(t)>0$ there by bounding the nonconstant derivative coefficients
  in absolute value. Thus $g(t)\geq L(t)\geq L(t_1)$ on $[t_0,t_1]$. The exact check is
  $(t_1-t_0)L(t_1)t_0^{240000}>\sum_jw_jt_j^{240000}$.
  Every atom is at most $R<t_0$, so this strict inequality persists at every
  larger exponent. Since $\beta\leq1$ and the omitted target term is positive,
  it proves $B_k>0$ for all $k\geq240000$.

The first checker certifies relative finite margins greater than
$8.80\times10^{-10}$ in the first family and $8.82\times10^{-10}$ in the
second. The independent integer checker agrees. These are rigorous lower
margins, not numerical optimization tolerances.

`verify_envelope_arb.py` uses exact rational polynomials and outward-rounded
Arb balls for atomic products and moments. `verify_envelope_rational.py` uses
only the Python standard library: integers, `Fraction`, and `isqrt`. Its
moment calculations round every operation outwards on denominator $2^{180}$;
its atomic product uses the rational enclosure
$\exp(\pm E)\in[1-E,(1-E)^{-1}]$. The polynomial construction, positivity
algorithm and arithmetic backend are independently implemented. Neither
checker imports the search, the original author's checker, or the other
checker. Both also pass the exact original eight-atom $0.4263$ measure.

The certificates verify the quantitative hypotheses of the existing analytic
lemma. Wang's annular estimate and Wikström's lemma are cited analytic inputs;
they have not been formalized in a proof assistant by this project.

## Reproduction, credit and scope

Run `./reproduce.sh` from this directory. The two checker outputs refer to the
same frozen certificate; see `SHA256SUMS` for hashes and `FINAL_LIVE_CHECK.md` for the live-source
recheck. The standard-library checker needs no third-party packages; the Arb
checker uses python-flint 0.9.0. The supplied frozen measure is sufficient;
reproducing a floating optimum is not needed.

Credit goes to Wang for the annular estimate and to Wikström for the moment
criterion, the atomic-plus-Lebesgue construction and the LP/refinement strategy.
His official [software archive, doi:10.5281/zenodo.21446369](https://doi.org/10.5281/zenodo.21446369),
contains both search code and the original rigorous $0.4263$ certificate.
Wettergren's [2020 thesis](https://lup.lub.lu.se/student-papers/record/9022204)
was also consulted for the separate upper-bound construction and its limitations.

The contribution here is the explicit sixteen-atom rational measure at the
larger radius, together with the polynomial integral certificate and two
independent exact implementations. No optimality of the measure, support size,
cutoff, moment criterion, or Korenblum constant is asserted. Numerical searches
with larger claimed radii failed in the tested runs; they do not prove an
upper barrier. This note and the exploration and checking software were
prepared with AI assistance for human mathematical review.
