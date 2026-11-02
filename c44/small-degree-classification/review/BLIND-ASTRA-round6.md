**I think the main bound is correct. I found no false mathematical inference, and an independent exact-arithmetic computation reproduces the claimed rational bound.** The supplied manuscript nevertheless has a reproducibility gap: its advertised certificate files and checkers are missing.

My literature-based expectation was
\[
3\cdot2^{d-1}-2\le R_d\le C2^d,
\]
with Nisan–Szegedy giving \(d2^{d-1}\), CHS giving \(C=6.614\), and Wellens giving about \(4.394\). Thus \(2.1974348818\) is a substantial improvement, but it does not conflict with known constructions. I would scrutinize it closely, not dismiss it as impossibly good. [CHS](https://arxiv.org/html/1801.08564), [Wellens](https://arxiv.org/html/2005.00566)

**1. First false or unjustified step**

**False mathematical step: none found.**

The first proof-critical assertion unsupported by the supplied files is **line 249**:

> “Every such budget is strictly below n in caps.json.”

There is no `caps.json` here. The earlier assertion about two implementations, and the later claims about their audit results, are likewise unverifiable as supplied. This is missing evidence, not a counterexample.

I repaired the main numerical gap independently: enumerating every permitted low weight and every occupied high floor cell, using exact rational arithmetic, reproduces
\[
c_{96}=\frac{174098727923678791596986393425}{2^{96}}.
\]
Adding the independently checked tail gives exactly
\[
\frac{174098727923678791596986402933}{2^{96}}
=2.197434881723198346348842568433\ldots
<2.1974348818.
\]

The substantive checks behind that conclusion were:

- **Support and extremizers, lines 22–73:** the induction works. The simultaneous duplication of all low-local-degree coordinates preserves their combined weight and adds a relevant selector. The separate AND substitution correctly establishes the count-extremizer reduction.
- **Ternary control bound, lines 87–111:** each relevant derivative contributes at least \(2^{-(k+1)}\) Fourier energy, while their total energy is at most \(kp\). The factor of four from the smallest nonzero derivative magnitude is handled correctly.
- **Restriction argument, lines 125–162:** the one-surviving-branch weight is exactly twice the original weight. Also, an active derivative assignment forces the remainder \(B\) to vanish identically. A degree-\(d\) monomial disjoint from \(H\) would retain its coefficient under restriction, giving the required contradiction. This is the crucial structural argument, and it works.
- **Lattice and spectrum, lines 173–218:** integer bit coefficients, Fourier granularity, and the parity argument all check out. Reducing \(A_i\), rather than \(A_i^2\), modulo two is legitimate and preserves the necessary degree bound.
- **Optimization and tail:** the first grid point maximizes the budget within each floor cell; the finite cover is complete. The tail is indeed \((H^2+3H+4)/2^H\).

**2. External theorems and their applications**

| Result | Assessment |
|---|---|
| Fourier orthogonality, Parseval, and the influence identity | Correct normalizations throughout. They apply to the real multilinear expansions used here. |
| Nisan–Szegedy relevance bound | Correct, and independently derived in lines 22–41. No external premise is needed for this part. |
| CHS identity \(W_d=R_d/2^d\) | Correct. The manuscript supplies a valid proof, so its application does not depend on trusting the citation’s proof or numbering. [CHS](https://arxiv.org/html/1801.08564) |
| \(R_3=10\), attributed to Tarannikov–Kirienko | Correct for arbitrary Boolean functions of real degree at most three. Krotov–Valyuzhenich explicitly state that general result; it is not confined to perfect colorings. Hence \(W_3=5/4\) is justified. I did not reproduce the original classification. [Section 3](https://arxiv.org/html/2311.05566v2) |
| Berlekamp–Sloane / Kasami–Tokura weights below twice minimum | Correct as a necessary condition. Carlet states weights \(2^{n-k+1}-2^{n-k+1-i}\), which normalize to \(2-2^{-j}\), \(j=i-1\). Here the support indicator really belongs to \(RM(k,n)\); padding with dummy coordinates is harmless; dropping parameter restrictions only enlarges the allowed set. [Carlet, p. 10613](https://www.aimspress.com/aimspress-data/math/2024/5/PDF/math-09-05-518.pdf) |
| Valyuzhenich minimum-support classification | The cited theorem is appropriate to degree-\(\le k\), minimum-support functions, and is consistent with the \(2k\) relevance bound. It is contextual, not a premise of this proof. [Theorem 2(2)](https://arxiv.org/html/2303.10995) |
| CHS/Shinkar–Tal construction | Correct; Booleanity, degree, and relevance follow directly from the displayed recursion. Its use in the tail is valid. [CHS construction](https://arxiv.org/html/1801.08564) |
| Wellens block restriction recurrence and \(3bs(bs-1)\le2(d^4-d^2)\) | Correctly stated; the hypotheses hold for Boolean functions of real degree \(d\). The latter implies the weaker integer bound \(bs\le d^2\). These are supplementary, not needed for the final bound. [Lemmas 3.8–3.9 and Theorem 4.1](https://arxiv.org/html/2005.00566) |
| Potapov’s ternary energy method | The description is accurate contextual attribution, not an invoked theorem. His root-of-unity encoding differs from the manuscript’s real ternary encoding. [Section 5](https://link.springer.com/article/10.1007/s12095-025-00797-4) |

The alleged KTA-table counterexample, inherited moment certificates, Fourier-lattice duals, and “round five” comparison cannot be audited from this directory. None is necessary for the main bound. I separately verified that the block recurrence with \(B_d=d^2\) reaches the scalar caps in all 96 columns.

**3. The single step I trust least**

**The exhaustive low-weight classification invoked at lines 199–218.** Its statement and application check out, but its exhaustiveness is a substantial external theorem that I did not independently reprove. Small computations cannot certify it in arbitrary dimension.

The bridge into that theorem is sound: an integer-valued ternary polynomial has integer bit coefficients, and reduction modulo two gives its support indicator. There is no illicit inference that an arbitrary binary affine change preserves real degree.

**4. Probability the final bound is correct**

**About 98%, subjectively.** The basis is the reconstructed argument, verified external statements, and independent exact numerical reproduction—not merely passing examples.

My computations checked:

- Every Boolean truth table on **at most four variables**, including all 65,536 four-variable functions.
- The weighted restriction inequality for every coordinate subset of those functions, plus derivative control bounds, lattice restrictions, and the top-degree hitting property.
- Every ternary truth table on at most three variables.
- Exact truth tables of \(\Xi_d\) for \(d=1,2,3,4\), with respectively **1, 4, 10, 22 relevant variables**. The last table has \(2^{22}\) entries.
- All scalar caps through degree 96, and both weaker variants quoted in the manuscript.

These are **not** exhaustive searches over all degree-three or degree-four functions on arbitrary numbers of variables. In particular, the computations do not prove \(R_4=22\); the manuscript proves only \(R_4\le24\).

**5. Recognition from the literature**

I recognize the CHS weighted restriction framework and lower-bound construction, and Wellens’s block-sensitivity recurrence. **I do not recognize this derivative-control scalar recursion or the constant \(2.1974348818\) as a published result.** My targeted searches did not establish prior publication; that is not evidence of novelty.

The large improvement is plausible because the manuscript introduces a different restriction set—the entire dependency set of a low-influence derivative—and exploits its dictator branches. It is doing more than rerunning Wellens’s numerical recurrence.

The independent scripts are [referee_scalar.py]((local scratch)) and [referee_small.py]((local scratch)). I did not inspect another local directory.