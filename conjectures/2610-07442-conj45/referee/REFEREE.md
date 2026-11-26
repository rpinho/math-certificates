VERDICT: HOLDS

The proof establishes Conjecture 4.5 for every integer triple \(0\le d\le\min(r,k)\). The decisive step is the endpoint cancellation in Lemma 3. Extracting degree \(d\) leaves precisely the paper's correction term in the interior and makes that correction zero on the row-complete face. The independent diagonal and balanced-face arguments then supply everything needed for uniqueness. I found two source boundary issues, detailed below. Neither enters an induction step used by the proof. [Proof under review](inputs/PROOF.md) · [Verifier](referee_verify.py)

## Target and source conventions

I read `Extended_avoidance.tex` from the supplied gzip/JSON archive. Line 86 gives *Pattern avoidance in alternating sign rectangles I: Extended avoidance*. Lines 88, 93 and 97 give Hans Höngesberg, Matjaž Konvalinka and Svante Linusson, in that order. Line 70 puts the pattern in the superscript and \(r,k,d\) in that order in the subscript. Counting the shared theorem environments from the actual section boundary identifies 4.2, 4.3, 4.4 and 4.5. The verifier matches the raw equations, inequalities and target labels, including `conj:312-formula` and `eq:conj312`. [Supplied source](inputs/2610.07442v1.tex.json.gz) · [arXiv v1, 2026-10-05](https://arxiv.org/abs/2610.07442v1)

Writing \(B(n,j)=\binom nj\), the four terms at lines 571 and 572 are
\[
\sum_{i=1}^{d}2^{i-1} B(k,i)\{B(r-2,d-i)-2B(r-2,d-i-2)\}
+B(r,d)+\sum_{i\ge0} C_{2i}B(r-1+2i,d-1-2i)
+2\sum_{i=1}^{d}(-1)^iB(r,d-i).
\]
The third term stops at \(2i\le d-1\). Line 574 defines \(C_n=B(2n,n)/(n+1)\). Line 407 supplies \(r,k\ge d\ge0\) for the shorter quantifier at line 569. With positive dimensions these are ASRs as defined at lines 202 to 207. A zero dimension is covered by the counting convention.

- **\(d=0\) and impossible counts.** The three sums vanish and \(B(r,0)=1\). The all-zero rectangle admits a completion. For \(d>r\) there are too few rows. For \(d>k\), summing by rows gives \(d\) and each column sum is in \(\{0,1\}\), an impossibility. Line 407 therefore supplies exactly the outside zero used on the square boundary.
- **Negative upper indices.** On the cone the only negative top with a nonnegative bottom is \(B(-1,0)\) at \(r=d=1\). Here the other three terms add to \(1+1-2=0\), so the formula gives \(kB(-1,0)\). Line 578 explicitly gives \(F(1,k,1)=k\), forcing \(B(-1,0)=1\). The full polynomial-binomial convention in the submission extends this evidence to auxiliary series with negative exponents. No further negative-top convention is needed to interpret the conjecture. At \(d=1\), \(F=r+k-1\), including \(F(r,1,1)=r\).
- **Schröder numbers.** Lines 279 to 282 identify the large Schröder numbers, their radical with constant-one square root, and the extra value \(\mathrm{Sch}_{-1}=1\). Line 412 gives the axes and the square ASM diagonal. The verifier computes \(\mathrm{Sch}_n\) for \(n\ge0\) by lattice walks with horizontal, vertical and diagonal steps below or on the diagonal. The extra index is absent from the power series. [Johansson and Linusson, 2007](https://people.kth.se/~linusson/artiklar/ASMpattern.pdf)

## Recurrence boundaries in the paper

| Source | Domain and endpoint check |
|---|---|
| Proposition 4.2, `lem:r=d`, lines 447 to 452 | \(1\le r\le k\). At \(k=r\) the first term \(S_{r,r-1,r}\) is zero by line 407. At \(r=1\) the sum from 2 is empty and the second term is \(1\). In the decomposition, \(i=1\) has weight \(\mathrm{Sch}_{-1}=1\), already absorbed into that second term. |
| Proposition 4.3, `lem:k=d`, lines 520 to 525 | \(1\le k<r\) ensures a first empty row \(j+1\). The cases \(j=0\) and \(j=k\) both exist. The last weight is \(B(r-k-1,0)=1\), even at \(r=k+1\). After the first empty row, its compulsory exterior 1 forces subsequent original-column 1s into decreasing order across rows. For each choice of the \(k-j\) occupied rows the remaining columns are filled in that order. For \(k=1\), the two contributions are \(r-1\) and 1. |
| Theorem 4.4, `lem:general`, lines 555 to 563 | For \(1\le d<r,k\), all subscripts exist. At \(d=1\) the sum from 2 is empty and the \(d-1\) term is the base value. In the subtracted case the smaller rectangle has an empty first row. A compulsory 1 to its right prevents a subsequent increasing pair in the original columns, including the 1s still required below them. Thus the occupied rows take the remaining columns in decreasing order. Choosing their \(d+1-i\) positions among \(r-i\) gives the stated subtraction. |

**Source boundary and prose notes.** Line 507 prints \(\sum_{i=1}^{k}\) in the first case of the proof of Proposition 4.2. Here \(i\) is the row containing the first-column 1, so its upper limit is \(r\). For \((r,k)=(1,2)\), the extra \(i=2\) would produce a negative row index. With the row bound, the terms for \(2\le i\le r\) cancel those explicitly subtracted at line 512. In line 510 the count \(S_{r-i,k-i,r-i}\) counts the excluded top-left-1 objects, as the subtraction at line 512 confirms. Line 450 already gives the correct final recurrence.

The abbreviated proof at line 563 also uses the fact that, in the strict interior, no empty row can precede the first-column 1 in row \(i\). Indeed \(d<k\) leaves a deficient column, and column 1 already sums to 1. A right-hand 1 forced by an earlier empty row, the 1 in column 1, and a future 1 below the deficient column would witness 312. Thus the first \(i\) rows in this case are nonempty and \(i\le d\), which justifies the upper limit.

Line 556 literally says \(d<r,k\). Substituting \(d=0\) at \((r,k)=(1,1)\) references \(S_{0,0,-1}\), outside the domain fixed at line 407. One can extend counts by zero for negative \(d\), but the source already assigns all \(d=0\) values directly. The submitted proof uses Theorem 4.4 only with \(d\ge1\). A separate endpoint slip occurs in the earlier diagonal argument at line 589. At \(n=1\) the little and large Schröder numbers of index zero both equal 1, so the stated half-factor there applies only for \(n\ge2\). Line 578 settles \(n=1\) directly, and Lemma 4 below covers it independently.

## Audit of the submitted proof

**Lemma 1, lines 78 to 124.** Put \(A=1+z,\ B=1+2z,\ D=\sqrt{1-4z-4z^2},\ P=(1-2z^2)/2,\ H=(3+2z-D)/4\). Every square root here has constant term 1. Such a root is unique since the sum of two candidate roots is a unit. From \(C=1+tC^2\) the even part of the Catalan series is \((\sqrt{1+4u}-\sqrt{1-4u})/(4u)\). For \(u=zA\), the first radical equals \(B\), as \(1+4u=B^2\) and \(B(0)=1\). Multiplication by \(z\) leaves \((B-D)/(4A)\). Each cancelled monomial divides the numerator.

Generating in \(d\), the four terms respectively give
\[
 A^{r-2}P(B^k-1),\qquad A^r,\qquad
 A^{r-2}(B-D)/4,\qquad -2zA^{r-1}.
\]
After extracting \(A^{r-2}\), the constant-in-\(k\) part is \(H\), giving \(\Phi_{r,k}=A^{r-2}(PB^k+H)\). Every coefficient uses finitely many Catalan terms. At \(r=2\) the prefactor is 1. At \(r=0,1\) the prefactors are powers of the unit \(A^{-1}\). The former case needs only constant coefficient 1. In the latter, \(PB^k+H=1+(k+1)z+O(z^2)\), giving coefficients 1 and \(k\) after multiplication by \(A^{-1}\). This includes \(k=0\) and justifies the auxiliary extraction \(F(1,0,1)=0\). More generally Lemma 1 requires \(d\le r\) here, with no \(d\le k\) restriction. This matters in Lemma 4.

**Lemma 2, lines 126 to 154.** Write \(S\) for the large Schröder generating function. Squaring \(1-x-2xS=\sqrt{1-6x+x^2}\) and cancelling \(4x\) in the formal domain gives \(xS^2-(1-x)S+1=0\). For \(a=z/(AB)\), multiplying the discriminant by \((AB)^2\) gives \((1-2z^2)^2\). Its principal root after division is \((1-2z^2)/(AB)\), and substitution gives \(S(a)=B\). For \(b=z/A\), the discriminant is \(D^2/A^2\), with root \(D/A\). Consequently \(S(b)=(1-D)/(2z)\). Multiplication by \(H-A=-(B+D)/4\) gives \(-H\), since \((B+D)(1-D)=2z(3+2z-D)\). Both substitutions have order one, so composition exists and the removals of a factor \(z\) are exact.

**Lemma 3, lines 156 to 197.** In (3.1) each term of index \(m\) has valuation at least \(m+1\), also for signed \(r,k\). Subtracting the two \(\Phi\)'s on the left gives \(2zPA^{r-2}B^{k-1}\). Regrouping the tail on the right gives
\[
 zA^{r-3}\{PB^{k-1}S(a)+(H-A)S(b)\}.
\]
The separate leading term contributes \(zA^{r-3}(PB^{k-1}+H)\). Lemma 2 cancels \(H\), and \(1+B=2A\) gives precisely the left side.

In degree \(d\ge1\), the leading term supplies \(F(r-1,k-1,d-1)\). Terms with \(m\ge d\) have negative requested degree. The possible endpoint \(m=d-1\) requests the constant coefficient of a difference of units with constant terms \(1-1=0\), even when \(r=d\). Only \(0\le m\le d-2\) remains. With \(i=m+2\), the coefficient is
\[
 \mathrm{Sch}_{i-2}\{F(r+1-i,k+1-i,d+1-i)-\binom{r-i}{d+1-i}\}.
\]
All shifted dimensions dominate the shifted positive degree. Thus the interior gives line 558 exactly. At \(r=d\) the subtraction has bottom \(r-i+1\) and top \(r-i\ge0\), so every subtraction is zero. At \(d=1\) the tail is empty on both faces. The \(i=1\) contribution of the paper is the separate leading term and no \(i=0\) is generated. At \(k=r=d\), Lemma 1 permits the off-cone predecessor, which Lemma 4 evaluates.

**Lemma 4, lines 199 to 239.** For a formal substitution \(t=u g(u)\), \(g(0)\ne0\), \(t^m t'\) has valuation \(m\). A Laurent series has a finite principal part, so only finitely many monomials can affect its residue after substitution. For \(m\ne-1\), the pullback is \((t^{m+1})'/(m+1)\), whose residue is zero because the differentiated degree-zero term has multiplier zero. For \(m=-1\), \(t'/t=u^{-1}+g'/g\) and \(g'/g\) is regular. This establishes (4.1) in \(\mathbb Q((u))\), including substitutions whose linear coefficient differs from 1.

For the \(H\) summand substitute \(z=w/(1-w)\) into the differential with pole \(z^{-r-1}\). The Jacobian \((1-w)^{-2}\) leaves regular numerator \((1-w)H(w/(1-w))=(1+wS(w))/2\). At \(r\ge1\) its degree-\(r\) coefficient is \(\mathrm{Sch}_{r-1}/2\).

For the \(PB^k\) summand set \(t=(S(u)-1)/2=u+O(u^2)\). The quadratic gives \(t=u(1+t)(1+2t)\). Differentiation yields \((1-2t^2)t'=(1+t)^2(1+2t)^2\). After removing the pole \(u^{-r-1}\), the transformed numerator is \((1+2t)^{k-r+1}/(2(1+t))\). Rationalization uses \((1+u)^2-(1-6u+u^2)=8u\), giving \(1/(2(1+t))=(1-uS(u))/2\). Multiplication by \(1+2t\) gives \((1+uS(u))/2\). Thus for \(k=r-1,r\) the first summand contributes respectively the negative and positive halves. Adding the \(H\) contribution proves \(F(r,r-1,r)=0\) and \(F(r,r,r)=\mathrm{Sch}_{r-1}\), including \(r=1\). The proof does not need the older hypergeometric diagonal computation.

**Lemma 5, lines 243 to 268.** Both sides of (5.1) depend linearly on \(g_0,\ldots,g_k\). On \(G=z^n\), \(0\le n\le k\), write \(M=k-n\) and \(m=j-n\). The terms with \(j<n\) vanish. Upper negation changes the two remaining factors to
\[
 (-1)^m\binom{1-n}{m},\qquad
 (-1)^{M-m}\binom{M-r+n}{M-m}.
\]
The product sign is \((-1)^M\). Extracting degree \(M\) from the product of the two integer powers of \(1+z\) gives \((-1)^M\binom{M-r+1}{M}=\binom{r-2}{M}\), the left side. Upper negation follows by reversing all signs in the falling factorial, including its empty product at \(M=0\). Vandermonde works for negative upper indices because \(1+z\) is a unit. This includes \(n=0,k\) and the \(j=0,1\) negative exponents. Choosing \(G=PB^k+H\) gives Proposition 4.3 for the full strict face \(1\le k<r\).

**Lemma 0 and the conclusion, lines 48 to 76 and 272 to 281.** The \(d=0\) stratum contains both axes and the origin. For \(1\le r=d<k\), the first predecessor lowers \(r+k\) by 1, the second by 2 and the indexed ones by \(2i-2\ge2\). All are row-complete or already at degree zero. The diagonal is settled for every \(r\ge1\) by Lemma 4 and the known square ASM theorem. On \(1\le k=d<r\), every term of Proposition 4.3 belongs to the already settled row-complete or zero stratum. In the interior the first predecessor enters that balanced face or lowers \(r+k+d\) by 1. The second enters degree zero or lowers the sum by 3. The indexed terms stay in the interior and lower it by \(3i-3\ge3\). Subtracting two solutions cancels the explicit binomial. The smallest interior triple is \((2,2,1)\), whose predecessors are already settled. These cases partition the cone, so uniqueness proves the claim for all dimensions. The phrase “three stages” at line 59 introduces four numbered items, one initialization and three positive-degree strata. This is an editorial count.

## Independent enumeration and rejection certificates

I generated each row from \(\{-1,0,1\}^k\) under the alternation and end-sign rules. Requiring every column prefix sum to be 0 or 1 is equivalent to column alternation starting with \(+1\). For every resulting rectangle I formed a square ASM of order \(r+k-d\). Each empty row gets a 1 in its own new right column, assigned in increasing row and column order. Each original column of sum zero gets a 1 in its own new bottom row, assigned in decreasing column order. All remaining new entries are zero. There are \(r-d\) new columns and \(k-d\) new rows. I checked row and column alternation, sums and dimensions of every resulting square.

A 312 witness consists of three strictly increasing rows with 1s in columns \(h,\ell,m\) satisfying \(\ell<m<h\). A new right entry can only be the first of such a triple. If it were third, the first would have to be an earlier, larger right entry, contrary to their order. If it were second, the third would also be on the right and the same contradiction applies. A new bottom entry can only be last, since a witness with its second entry at the bottom would require an increasing pair of bottom columns. Consequently each witness survives in **every** extension: retain its interior entries, use a compulsory 1 to the right in the same empty row if the first is exterior, and a compulsory 1 below in the same deficient column if the last is exterior. Their strict inequalities persist regardless of the extension's size. For example, the rows \((0,0),(1,0)\) contain no internal triple, but their completion forces the three columns “right of 2, 1, 2” in increasing rows. An avoiding constructed square certifies acceptance. This proves that the direct test decides the existential definition without a conjectural size cutoff.

| Exact comparison | Observed result |
|---|---|
| All positive dimensions through \(5\times5\) | 7,575 legal rectangles, 1,282 extendably avoiding, 6,293 rejected. Of the rejected rectangles, 3,914 avoid 312 internally. |
| All 91 triples through 5, including the axes | All agree with \(F\). All 55 positive-degree counts agree with the applicable printed recurrence evaluated from the independently enumerated counts. The \(5\times5\) counts by \(d=0,\ldots,5\) are \(1,9,41,111,168,90\). |
| Separate square enumeration | 429 order-five ASMs, 90 avoiding. Projecting their avoiding corners agrees on all 1,869 rectangle candidates with \(r+k-d\le5\). An avoiding square of smaller order can be padded by a bottom-right identity block. |
| Published Table 2, raw lines 1100 to 1105 | All 51 populated entries match, including \(S_{4,6,4}=236\) and \(S_{5,10,5}=9086\). |
| \(0\le d\le\min(r,k)\), \(0\le r,k\le50\) | 45,526 triples, zero discrepancies. The recurrence uses Pascal addition and lattice-walk counts. The formula uses falling products. The grid computes the square face by Proposition 4.2 as a further check against the independent diagonal. |
| Larger triples \((51,52,50),(67,58,19),(60,91,60),(77,53,53),(64,64,64),(99,1,1)\) | All six match. For example \(S_{51,52,50}=3456049809902016631568547840146318881\). The command prints all six integers. |
| Formal series | Exact rational coefficients through degree 36 inclusive, with four internal guard degrees. Tests cover the four generating functions separately, both radicals and substitutions, (3.1) with signed and boundary parameters, normalized Laurent integrands, the two diagonal halves, and every monomial of degree through \(k\) for \(1\le k\le36\) at \(r=k+1,k+11\). Residue tests include all pole orders 1 through 37 and a substitution with linear coefficient \(-2\). |

## Adversarial controls and self-review

| Mutation in the four-sum formula | First \((r,k,d)\) | Mutant | Exact object count |
|---|---:|---:|---:|
| Set the negative-top binomial to zero | (1,1,1) | 0 | 1 |
| Replace \(2^{i-1}\) with \(3^{i-1}\) | (2,2,2) | 3 | 2 |
| Replace the first sum's \(-2\) with \(-1\) | (3,3,3) | 9 | 6 |
| Reverse the alternating sign | (1,1,1) | 5 | 1 |
| Double the standalone binomial | (0,0,0) | 2 | 1 |
| Replace \(C_{2i}\) with \(C_i\) | (3,3,3) | 5 | 6 |
| Remove the final multiplier 2 | (1,1,1) | 2 | 1 |

CONTROLS: No. `numbers()` in `referee_verify.py` compares each mutant with the raw rectangle counts in lexicographic order. All seven have explicit discrepancies above. `objects()` also checks 1,869 completion decisions against independent projections of actual order-five ASMs.

CONTRADICTING: No. `objects()` retained all 6,293 rejections, including the 3,914 that would have passed a corner-only test. `numbers()` checked all 45,526 grid cells and the 50 off-cone predecessors \(F(r,r-1,r)\). I recorded the source exceptions at lines 507, 556 and 589.

LABELS: No. `paper()` reads the 1,605 raw source lines and reconstructs the numbering from the shared LaTeX counter. It checks equation contents at lines 450, 523, 558, 571 and 572, the line-578 boundary value, and the actual Table 2 cells. The pattern check reads individual \(+1\) entries in strictly ordered rows and columns.

## Reproduction, scope and next step

From this directory, run

```sh
nice -n 10 python3 referee_verify.py
```

I ran this under `/usr/bin/time -l` on macOS. It exited 0 in 2.36 seconds, with peak RSS 32,899,072 bytes. The checker uses one process, no worker threads, exact integers and `fractions.Fraction`. It reads only the supplied archive and requires no third-party package or network connection. The final output is `All exact comparisons passed.`

**Did this referee job find a new theorem? No.** The proof under review establishes the full conjecture. My result is an independent mathematical verification of that submission. The all-dimensions verdict rests on the identities and induction above. The finite calculations can expose transcription or boundary errors. All comparisons are exact and there is no statistical holdout, training, or predictive score. A public priority claim would require a fresh literature check. For an editorial revision, I would specify \(d\ge1\) when citing Theorem 4.4 and note the corrected row limit in the citation to Proposition 4.2. [Prior art and reproduction](PRIOR_ART.md)
