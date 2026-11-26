# Proof of Hongesberg, Konvalinka, and Linusson (arXiv:2610.07442v1) Conjecture 4.5

I present an unconditional algebraic proof of the closed-form formula conjectured by Hans Hongesberg, Matjaz Konvalinka, and Svante Linusson in *Pattern avoidance in alternating sign rectangles I: Extended avoidance* ([arXiv:2610.07442v1](https://arxiv.org/abs/2610.07442v1), Conjecture 4.5, `\label{conj:312-formula}`).

For all integers $0 \le d \le \min(r, k)$, the number $S^{312}_{r,k,d}$ of $r \times k$ alternating sign rectangles with $d$ nonempty rows that extendably avoid $312$ equals

$$F(r,k,d) = \sum_{i=1}^{d} 2^{i-1} \binom{k}{i} \left(\binom{r-2}{d-i} - 2\binom{r-2}{d-i-2}\right) + \binom{r}{d} + \sum_{i \ge 0} C_{2i} \binom{r-1+2i}{d-1-2i} + 2 \sum_{i=1}^{d} (-1)^i \binom{r}{d-i},$$

where $C_n = \frac{1}{n+1}\binom{2n}{n}$ is the $n$th Catalan number and polynomial binomial coefficients satisfy $\binom{-1}{0} = 1$ (matching line 578 of the arXiv source file Extended_avoidance (tex); no negative upper index ever meets a positive lower index across $0 \le d \le \min(r, k)$).

This is AI work. No human has checked it. **Lean status:** `none`.

## Proof summary

The complete self-contained proof is in [`PROOF.md`](PROOF.md). Let $S(x) = \sum_{n \ge 0} \mathrm{Sch}_n x^n = \frac{1 - x - \sqrt{1 - 6x + x^2}}{2x}$ be the large Schroder generating function.

1. **Compact generating function (Lemma 1):** For every $r, k \ge 0$ and $0 \le d \le r$, $F(r, k, d) = [z^d]\,\Phi_{r,k}(z)$, where
   $$\Phi_{r,k}(z) = (1 + z)^{r-2}\left(\frac{1 - 2z^2}{2}(1 + 2z)^k + \frac{3 + 2z - \sqrt{1 - 4z - 4z^2}}{4}\right) \in \mathbb{Q}[[z]].$$
2. **Schroder substitution identities (Lemmas 2 and 3):** In $\mathbb{Q}[[z]]$,
   $$S\!\left(\frac{z}{(1 + z)(1 + 2z)}\right) = 1 + 2z, \qquad -\frac{1 + 2z + \sqrt{1 - 4z - 4z^2}}{4}\, S\!\left(\frac{z}{1 + z}\right) = -\frac{3 + 2z - \sqrt{1 - 4z - 4z^2}}{4}.$$
   Extracting $[z^d]$ from a single formal power series identity shows that $F(r, k, d)$ satisfies both the interior recurrence ($1 \le d < \min(r, k)$, `\label{lem:general}`) and the row-complete recurrence ($1 \le d = r \le k$, `\label{lem:r=d}`) of the paper.
3. **Boundary faces and uniqueness (Lemmas 4, 5, and 0):** Formal Laurent residue invariance in $\mathbb{Q}((z))$ shows $F(r, r-1, r) = 0$ and $F(r, r, r) = \mathrm{Sch}_{r-1}$ for every $r \ge 1$. A Chu-Vandermonde linear operator identity shows that $F(r, k, d)$ satisfies the balanced recurrence ($1 \le d = k < r$, `\label{lem:k=d}`) of the paper. Strong induction on $r + k$ closes uniqueness across the entire cone $0 \le d \le \min(r, k)$.

## Clean-room cross-family verification

- **Producer:** Gemini 4 Carbon High via Antigravity CLI (`producer/REPORT.md`, `producer/verify_proof.py`). Checked all `7575` valid ASRs through $5 \times 5$, all `180441` triples with $0 \le d \le \min(r, k) \le 80$, exact formal power series over $\mathbb{Q}[[z]] \pmod{z^{43}}$, and `7` negative controls.
- **Clean-room Cross-Family Referee:** GPT-6.2 Astra via Codex (`referee/REFEREE.md`, `referee/referee_verify.py`, `referee/verification.txt`, producer code withheld). Returned **`VERDICT: HOLDS`** with zero mathematical gaps. Independently checked all `7575` legal ASRs through $5 \times 5$ (`1282` extendably avoiding, `6293` rejected including `3914` internal avoiders), all `429` order-5 ASMs (`90` avoiding, `1869` corner projections), all `51` populated cells of published Table 2, all `45526` grid triples through `50` plus larger cases including $S^{312}_{51,52,50} = 3456049809902016631568547840146318881$, exact formal-series and Laurent-residue identities through degree `36`, and `7` mutated negative controls. Also recorded three minor source-manuscript slips (line 507 row limit, unstated $d \ge 1$ in Theorem 4.4, and line 589 diagonal endpoint) handled cleanly by `PROOF.md`.

## Reproduction

Requires Python 3.10+ (standard library only, exact `int` and `fractions.Fraction`). From `conjectures/2610-07442-conj45/`:

```bash
# 1. Verify file integrity
shasum -a 256 -c SHA256SUMS

# 2. Run standalone clean-room referee verifier (~2.4s, 33 MB RSS; does not require arXiv TeX archive)
nice -n 10 python3 referee/referee_verify_standalone.py
```

The untouched original referee script `referee/referee_verify.py` (which additionally checks the verbatim raw TeX lines and Table 2 cells against the local arXiv source archive) produced `referee/verification.txt`.
