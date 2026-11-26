Shipped: Unconditional proof of Conjecture 4.5 of Höngesberg, Konvalinka & Linusson (arXiv:2610.07442v1) for all integers 0 <= d <= r, k in PROOF.md, verified independently by verify_proof.py.
Why: Summing the conjectured closed form F(r,k,d) over d yields an explicit algebraic generating function Phi_{r,k}(z) whose formal-power-series identities simultaneously satisfy all base cases and the complete recurrence system of Section 4 (Propositions 4.2-4.3 and Theorem 4.4).

RESULT: yes

## Summary of Result and Novelty

- **Did I find something new? Yes.** I unconditionally settled **Conjecture 4.5 (`\label{conj:312-formula}`, `eq:conj312`)** of Hans Höngesberg, Matjaž Konvalinka, and Svante Linusson, *"Pattern avoidance in alternating sign rectangles I: Extended avoidance"* (`arXiv:2610.07442v1`, Oct 2026), proving that for all integers $0 \le d \le r, k$,
  $$S^{312}_{r,k,d} = \sum_{i=1}^{d} 2^{i-1} \binom{k}{i} \left( \binom{r-2}{d-i} - 2\binom{r-2}{d-i-2} \right) + \binom{r}{d} + \sum_{i \ge 0} C_{2i} \binom{r-1+2i}{d-1-2i} + 2 \sum_{i=1}^{d} (-1)^i \binom{r}{d-i},$$
  under the standard polynomial binomial convention ($\binom{n}{0} = 1$ for all $n \in \mathbb{Z}$, $\binom{n}{m} = 0$ for $m < 0$, and $\binom{n}{m} = \prod_{j=0}^{m-1}\frac{n-j}{j+1}$ for $m > 0$).
- **Key mechanism**: In [PROOF.md](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_312/PROOF.md), I prove (Lemma 1) that for all $r, k \ge 0$ and $0 \le d \le r$, $F(r, k, d) = [z^d] \Phi_{r, k}(z)$ where
  $$\Phi_{r, k}(z) = (1 + z)^{r-2} \left( \frac{1 - 2z^2}{2}(1 + 2z)^k + \frac{3 + 2z - \sqrt{1 - 4z - 4z^2}}{4} \right) \in \mathbb{Q}[[z]].$$
  Using two algebraic evaluations of the large Schröder generating function $S(x)$ at $x = \frac{z}{(1+z)(1+2z)}$ (where $1 - 6x + x^2$ becomes the rational square $\bigl(\frac{1 - 2z^2}{(1+z)(1+2z)}\bigr)^2$, giving $S(x) = 1 + 2z$) and $x = \frac{z}{1+z}$ (Lemma 2), a single formal power series identity in $\mathbb{Q}[[z]]$ (Lemma 3) simultaneously proves Theorem 4.4 (`lem:general`, $1 \le d < r, k$) and Proposition 4.2 (`lem:r=d`, $1 \le d = r \le k$). Formal Laurent residue change of variables proves $F(r, r-1, r) = 0$ and $F(r, r, r) = \operatorname{Sch}_{r-1}$ from scratch (Lemma 4), and a universal Chu-Vandermonde linear operator identity proves Proposition 4.3 (`lem:k=d`, $1 \le d = k < r$, Lemma 5), closing strong-induction uniqueness (Lemma 0).
- **Why no statistical holdout or SBS baseline applies**: This task is an exact mathematical theorem and symbolic/enumerative certificate task rather than a statistical prediction benchmark on noisy data; there is no train/test split or predictive loss metric. Following the job rules for exact certificate tasks, verification is performed by an independent zero-dependency exact verifier ([verify_proof.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_312/verify_proof.py)) over `int` and `fractions.Fraction`.

## Verification Status

Executed `nice -n 10 python3 verify_proof.py` (exit code `0`, wall time `5.2s`, peak RSS `35.1 MB` << `2 GB` limit):
1. **Verbatim archive check**: Parsed [2610.07442v1.tex.json.gz](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_312/inputs/2610.07442v1.tex.json.gz) (`Extended_avoidance.tex`, 1,605 lines) and asserted exact strings and line numbers for `\label{sec:def}`, `\label{lem:r=d}`, `\label{lem:k=d}`, `\label{lem:general}`, `\label{conj:312-formula}`, `\label{eq:conj312}`, and line 578 (`F(1,k,1)=k`).
2. **First-principles ASR/ASM enumeration**: Verified $312$-avoiding $m \times m$ ASMs match $\operatorname{Sch}_{m-1}$ for $1 \le m \le 7$, enumerated all $7,575$ valid $r \times k$ ASRs for $1 \le r, k \le 5$ from the Section 2 axioms, tested extendable $312$-avoidance directly by searching for square ASM extensions at $m_0 = r + k - d$ (and checked $m_0 + 1 \le 10$ to confirm no larger extension rescues any rejected ASR), and verified 100% agreement across all $91$ triples $0 \le d \le r, k \le 5$ with Section 4 recurrences, Corollary 5.3, and $F(r, k, d)$.
3. **Exact grid verification**: Verified $S^{312}_{r,k,d} = F(r, k, d)$ with `0` mismatches across all `23,821` triples $0 \le d \le r, k \le 40$ and all `180,441` triples $0 \le d \le r, k \le 80$.
4. **Symbolic formal-power-series verification**: Verified every intermediate identity in Lemmas 1, 2, 3, 4, and 5 of [PROOF.md](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_312/PROOF.md) over $\mathbb{Q}[[z]] \pmod{z^{43}}$ in exact `Fraction` arithmetic.
5. **Negative controls**: Verified that 7 distinct constant/index/convention perturbations of $F(r, k, d)$ each fail immediately on $0 \le d \le r, k \le 5$.

## Referee Self-Review

- `CONTROLS:` No assumption overrode the controls. In [verify_proof.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_312/verify_proof.py#L510-L597), `check_negative_controls` ran 7 explicit mutant perturbations against `S[d][r][k]` and caught all 7 on $0 \le d \le r, k \le 5$ (`2^{i-1}->2^i` at `(1,1,1)`, `-2->-1` at `(3,3,3)`, `r-2->r-1` at `(2,2,2)`, `+C(r,d)->+2C(r,d)` at `(0,0,0)`, `C_{2i}->C_i` at `(3,3,3)`, `2*sum->1*sum` at `(1,1,1)`, and naive `C(-1,0)=0` at `(1,1,1)`), while `check_first_principles_small` ([verify_proof.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_312/verify_proof.py#L365-L413)) verified at $m_0 + 1 \le 10$ across all $7,575$ small ASRs that extending to a larger ASM size never rescues a non-extendable ASR.
- `CONTRADICTING:` No contradicting case or boundary convention was dropped or hidden. In [verify_proof.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_312/verify_proof.py#L416-L443), `check_grid_equality` tested all `180,441` triples $0 \le d \le r, k \le 80$ (`0` mismatches under `binom_poly`) and explicitly compared against `binom_naive_nonneg` (`C(n,m)=0` for all $n<0$ even at $m=0$), isolating the exact `40` triples `(1, k, 1)` ($1 \le k \le 40$) sensitive to $\binom{-1}{0} = 1$ and verifying directly from line 578 of `Extended_avoidance.tex` (`We easily see that F(0,k,0)=F(r,0,0)=1 as well as F(1,k,1)=k`) that $\binom{-1}{0} = 1$ is the authors' explicit convention (documented in [PRIOR_ART.md](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_312/PRIOR_ART.md#L121-L141)).
- `LABELS:` No label, macro, or title was trusted without checking raw data. In [verify_proof.py](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_312/verify_proof.py#L335-L362), `check_paper_verbatim` inspected raw `Extended_avoidance.tex` (1,605 lines) inside [2610.07442v1.tex.json.gz](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_312/inputs/2610.07442v1.tex.json.gz), confirming line 70 (`\newcommand{\s}[4]{S^{#1}_{{#2},{#3},{#4}}}`), line 86 (exact title *"Pattern avoidance in alternating sign rectangles I: Extended avoidance"* vs the prompt's informal title), lines 202-207 (three ASR axioms checked against 7,575 generated matrices), and lines 447, 520, 555, and 568-575 (`\label{lem:r=d}`, `\label{lem:k=d}`, `\label{lem:general}`, `\label{conj:312-formula}`, `\label{eq:conj312}`).

## Reproduction Commands

```bash
nice -n 10 python3 verify_proof.py
```

## Sources

1. Hans Höngesberg, Matjaž Konvalinka, and Svante Linusson, *"Pattern avoidance in alternating sign rectangles I: Extended avoidance"*, `arXiv:2610.07442v1` (Oct 2026), raw source in [2610.07442v1.tex.json.gz](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_312/inputs/2610.07442v1.tex.json.gz).
2. Robert Johansson and Svante Linusson, *"Pattern avoidance in alternating sign matrices"*, Annals of Combinatorics 11 (2007), 471-480 (`[JL07]`).
3. Ronald L. Graham, Donald E. Knuth, and Oren Patashnik, *Concrete Mathematics*, 2nd ed., Addison-Wesley (1994), Chapter 5 (polynomial binomial coefficients, upper negation, and Chu-Vandermonde).

## Limitations and Next Steps

- **Algebraic vs. bijective proof**: My proof in [PROOF.md](file:///Users/ricardo/dev/open-science/math_wave_1030/csweep_312/PROOF.md) is a complete algebraic / formal-power-series proof rather than a direct combinatorial bijection explaining the alternating and even-Catalan terms in `eq:conj312`. Finding a direct sign-reversing involution or lattice-path bijection for general $(r, k, d)$, as well as a combinatorial interpretation of the refinement $c_{k,j} = S^{312}_{j,k,j} - S^{312}_{j-1,k,j-1}$ posed on line 1075 of `Extended_avoidance.tex`, remains a natural next step.
- **Other length-3 patterns**: Applying the same $z$-generating-function method to the recursive systems in Sections 4.2-4.4 of `arXiv:2610.07442v1` to seek closed-form or algebraic generating-function formulas for $S^{132}_{r,k,d}$, $S^{213}_{r,k,d}$, and $S^{231}_{r,k,d}$ is an immediate follow-up direction.
