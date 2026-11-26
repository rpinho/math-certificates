# Pairing counts and the certified upper bounds

All logs are natural. Put \(d=10\), \(D=dn\), \(v_i=na_i\), and \(S_i=dv_i\). In formulae below \(0\log0=0\). The packing model and recoloring lemma are in [PROOF.md](PROOF.md).

## 1. Exact count for all pairing types

For a map \(f\), let \(K_{ij}\) be the count of stubs of part \(i\) matched to part \(j\). The matrix is symmetric, its row sums are \(S_i\), and \(K_{ii}\) is even. A valid type has zero entries on the red pairs. For any such nonnegative integer type,
\[
 p_K=\Pr(K\mid f)
 =\frac{2^{D/2}(D/2)!}{D!}
 \frac{\prod_i S_i!}
      {\prod_i 2^{K_{ii}/2}(K_{ii}/2)!\prod_{i<j}K_{ij}!}.
\]
To see this, assign destination labels to the stubs of each part with the given counts. Pair each pair of distinct directed label pools by a bijection and pair each internal pool by a perfect matching. The product of these counts, divided by \((D-1)!!\), gives the formula. The number of completions is the same for every destination labeling. Consequently, conditional on \(K\), destination assignments are independent uniform permutations of their row labels, and all interpart bijections and internal matchings are independent uniform given those assignments.

For integers \(m\ge1\), \((m/e)^m\le m!\le e\sqrt{m+1}(m/e)^m\). Indeed, \(\int_1^m\log x\,dx\le\log(m!)\) by right endpoints. Concavity bounds the same integral below by the trapezoidal sum \(\log(m!)-\tfrac12\log m\). The displayed bounds also hold for \(m=0\) using \(0^0=1\). Apply the upper bound to the six numerator factorials and the lower bound to the denominators. The multinomial count of maps of profile \(v\) is at most \(\exp(-n\sum_i a_i\log a_i)\) by the multinomial theorem at probabilities \(a_i\). With \(Q=K/D\) this gives
\[
 \binom{n}{v_0,\ldots,v_4}p_K
 \le 3^6(D+1)^3\exp(nL(a,Q)),\qquad
 L(a,Q)=9\sum_i a_i\log a_i-5\sum_{ij}Q_{ij}\log Q_{ij}.
\]
Here the powers of \(2\) cancel the use of \(K_{ii}/2\) in the internal factorials; the \(\log D\) and linear terms cancel by the row and total constraints.

For fixed profile there are at most \((D+1)^5\) types, because the five off-diagonal blue counts specify the diagonal via the row sums. The count includes every admissible symmetric \(K\), with even diagonal required for a nonzero term. At most \((n+1)^4\) profiles arise.

## 2. Naive entropy bound and its edge tails

For any positive \(t=(t_0,\ldots,t_4)\), let \(Z=\sum_{ij}A_{ij}t_i t_j\) and \(B_{ij}=A_{ij}t_it_j/Z\). For any supported symmetric \(Q\) with rows \(a\),
\[
 L(a,Q)=U_t(a)-5D_{\rm KL}(Q\Vert B),\qquad
 U_t(a)=9\sum_i a_i\log a_i-10\sum_i a_i\log t_i+5\log Z.
\]
Expand \(\log B_{ij}\) and use both marginals \(a\) to obtain the identity. For any blue edge \(\{i,j\}\), its two directed entries form a single cell of mass \(2Q_{ij}\). The log-sum inequality gives
\[
 D_{\rm KL}(Q\Vert B)\ge
 {\cal D}(2Q_{ij},2B_{ij}),\qquad
 {\cal D}(x,b)=x\log(x/b)+(1-x)\log((1-x)/(1-b)).
\]
The right side decreases for \(x<b\) and increases for \(x>b\), by differentiation and continuity at the endpoints. Thus a cutoff \(q_*\) on the correct side of \(B_{ij}\) implies the one-sided upper \(L(a,Q)\le U-5{\cal D}(2q_*,2B_{ij})\) for types on the far side, whenever \(U_t(a)\le U\). Conditional events have probability at most one in those tails.

## 3. Case I bound

For one \(V_0\) vertex let \(P_+\) count length-\(d\) words on destination labels \(0,2,3\) containing both \(2\) and \(3\), weighted by the corresponding variables, and \(P_2\) count words containing \(2\). Define \(P_0\) on destinations \(0,2,4\) for a \(V_2\) vertex by requiring label \(0\). Write \(b=2d-1=19\). For a fixed exemption set of \(b\) vertices the conditional count of row-0 assignments is the relevant coefficient of \(P_+^{v_0-b}P_2^b\), divided by the row multinomial. The row-2 conditional probability is the corresponding coefficient of \(P_0^{v_2}\) divided by its row multinomial. Multiply by row independence and sum over possible exemption sets. This gives the usual Chernoff upper bound by evaluation at any positive tilt and division by the target monomial. The coefficient inequality holds for every cell, including cells with zero coefficient.

For certification a simpler upper bound suffices. Retain the requirement that at least \(v_0-b\) vertices in \(V_0\) are touched by \(V_3\) stubs. Conditional on \(K\) the \(K_{03}\) such slots in row 0 are uniform. Let \(p=K_{03}/(dv_0)=Q_{03}/a_0\), and \(f(p)=1-(1-p)^d\). Under independent Bernoulli selection with probability \(p\), conditional on exactly \(K_{03}\) successes the slots have the same law. This total is a mode of its binomial law, including at \(p=0,1\): for \(0<p<1\) the ratio of successive masses crosses \(1\) at that count. Its probability is at least \(1/(dv_0+1)\). For each fixed exemption set, independence across vertex blocks bounds the conditional probability by \((dv_0+1)f(p)^{v_0-b}\).

A nonzero event requires \(K_{03}\ge v_0-b\). For \(v_0\ge2b\) this implies \(p\ge1/(2d)\), and \(f(p)\ge p\). The union over all exemption sets therefore gives
\[
 \Pr(\mathcal E_{\rm I}\mid K)
 \le (D+1)n^{19}20^{19}\exp\bigl(n a_0\log f(Q_{03}/a_0)\bigr).
\]
For \(a>0\) and \(0\le q\le a\), write \(g(a,q)=a\log f(q/a)\), with \(g(a,0)=-\infty\). For \(0<q<a\) put \(p=q/a\). At fixed \(a\),
\[
 \frac{\partial g}{\partial q}=\frac{10(1-p)^9}{1-(1-p)^{10}}>0.
\]
At fixed \(q\),
\[
 \frac{\partial g}{\partial a}
 =\log(1-(1-p)^{10})-\frac{10p(1-p)^9}{1-(1-p)^{10}}<0,
\]
since the logarithm is negative and the subtracted fraction is positive. The first monotonicity extends to \(q=0,a\) by limits. For fixed \(q>0\), extend \(g(a,q)\) to \(a\le q\) by setting it to \(0\), its value at \(a=q\). This is the continuous nonincreasing function \(a\log f(\min(1,q/a))\).

In a leaf with \(U_t(a)\le U\), let \(a_{\min}>0\) be the lower endpoint of the tightened part-0 interval. For an upper cutoff \(q_*>0\), the near cell \(Q_{03}\le q_*\) has
\[
 L(a,Q)+g(a_0,Q_{03})
 \le U+a_{\min}\log f(\min(1,q_*/a_{\min})).
\]
Indeed, first use \(Q_{03}\le\min(a_0,q_*)\) and monotonicity in \(q\), then the extended monotonicity in \(a\). If \(q_*=\min(a_{0,\max},a_{3,\max})\), every feasible type is in the near cell. Otherwise the verifier requires \(q_*>B_{03}\) and checks \(U-5{\cal D}(2q_*,2B_{03})\) on the tail \(Q_{03}>q_*\), by §2. The tail bounds \(L\) itself and hence \(L+g\), since \(g\le0\). The cutoff equality belongs to the near cell. The tail uses the conditional probability bound by one, with no extra type count.

## 4. Case II exact joint probability and certificate bound

Condition on a valid \(K\). For \(v\in V_2\), mark its \(0\)-destination stubs hot when \(n_4(v)\ge1\). Write \(R\) for their total number. The row-2 conditional probability that every \(v\in V_2\) has an \(0\)-destination stub and that \(R\) is the displayed integer is
\[
 P_{V_2}(K_{2,\cdot},R)=
 \frac{[x^{K_{20}}y^{K_{24}}w^{K_{22}}z^R]\,
 \left(\sum_{\substack{j\ge1,\ k,\ell\ge0\\j+k+\ell=d}}
 {d\choose j,k,\ell}x^j y^k w^\ell z^{j\boldsymbol1_{k>0}}\right)^{v_2}}
 {{dv_2\choose K_{20},K_{24},K_{22}}}.
\]
Given any fixed row-2 labeling with \(R\) hot stubs, the uniform \(0\)-to-\(2\) bijection sends them to a uniform \(R\)-subset of the \(K_{02}\) corresponding row-0 slots. Those \(K_{02}\) slots are themselves a uniform subset of all \(dv_0\) slots, independently of row 2. Thus the received hot slots are a uniform \(R\)-subset of all \(dv_0\) slots. The conditional **joint** event that the row-2 requirements and this \(R\) occur and every vertex in \(V_0\) receives a hot stub has exact probability
\[
 \Pr(\mathcal E_{\rm II}(K,R)\mid K)
 = P_{V_2}(K_{2,\cdot},R)
 \frac{[z_h^R]\big((1+z_h)^d-1\big)^{v_0}}{\binom{dv_0}{R}}.
\]
This conditioning retains the label placement within vertices of row 2.

The second factor is at most \((D+1)f(R/(dv_0))^{v_0}\), by the binomial-mode argument in §3. With \(0<u<1\), set \(\beta=f'(u)/f(u)>0\) and \(\gamma=\log f(u)-\beta u<0\). Concavity of \(\log f\) gives
\[
 f(R/(dv_0))^{v_0}\le \exp(na_0\gamma+(\beta/d)R).
\]
Use the convention of zero probability at \(R=0\) for \(v_0>0\). We bound the nonnegative moment of \(\exp((\beta/d)R)\) over row-2 labelings, keeping all \(R\). Dropping the row-2 requirement \(n_0\ge1\) can only raise it.

Expose the positions of the \(K_{24}\) label-4 slots first. At most \((d-1)K_{24}\) remaining slots belong to blocks with a label 4. Write \(m\) for their actual number and \(S=dv_2-K_{24}\) for all remaining slots. The \(K_{20}\) labels 0 are uniform among those \(S\) slots. For \(w=e^{\beta/d}\), expand \(w^R=\prod_{\ell=1}^m(1+(w-1)I_\ell)\), where \(I_\ell\) marks label 0 in an eligible slot. For a \(j\)-subset of these slots its all-0 probability is \((K_{20})_j/(S)_j\le(K_{20}/S)^j\), and equals zero if \(j>K_{20}\). Thus the conditional moment is at most \((1+(K_{20}/S)(w-1))^m\). This bound holds for every arrangement of label 4. We use it on boxes with \(S>0\).

Let \(a_{\min}\) and \(a_{2,\min}\) be lower bounds on \(a_0,a_2\). In a near cell assume \(Q_{02}\le h_{02}\), \(Q_{24}\le h_{24}<a_{2,\min}\). Use \(p_{\max}=\min(1,h_{02}/(a_{2,\min}-h_{24}))\). By monotonicity and \(\gamma<0\),
\[
 \sum_{R=0}^{K_{02}}\Pr(\mathcal E_{\rm II}(K,R)\mid K)
 \le (D+1)
 \exp\!\left(n\left[a_{\min}\gamma+
       90 h_{24}\log(1+p_{\max}(e^{\beta/10}-1))\right]\right).
\]
In a far cell, where either bound on \(Q_{02}\) or \(Q_{24}\) is exceeded, each corresponding edge tail in §2 bounds the rate. Each upper cutoff is either implied by \(Q_{ij}\le\min(a_i,a_j)\) or certified by its own edge-tail inequality. All types and all hot counts are included.

## 5. Why the finite certificate covers the required domain

The exact root consists of the box \([0,4001/10000]^5\) sliced by \(\sum_i a_i=1\). There is one tree for A and B and one for each constrained case on C. Each split replaces one closed coordinate interval by its two closed subintervals and covers the parent. Common boundary points may occur in both. Each profile box is tightened using the regional inequalities and the sum constraint. For an inequality \(a_i\ge a_j+c\), replace the lower endpoint of \(a_i\) by at least the lower endpoint of \(a_j\) plus \(c\), and the upper endpoint of \(a_j\) by at most the upper endpoint of \(a_i\) minus \(c\). For B the box is excluded if both lower large endpoints exceed the upper endpoint of \(a_3\) by more than \(\delta\). In the joint A/B tree the verifier takes the coordinate hull of the surviving boxes. Every point of the corresponding region stays in its clipped box and on the mass hyperplane.

With \(t\) fixed, \(U_t\) is convex by convexity of \(x\log x\). A vertex of a box sliced by the mass hyperplane has at most one coordinate strictly between its endpoints: if two coordinates were interior, one could be increased and the other decreased in both directions. The verifier enumerates the exact vertices and checks each at 160-bit Arb precision. An accepted naive leaf has \(U\le-1/1000\). An accepted occupancy leaf checks every required tail and the profile-level near bound in §3 or §4 against the same margin. These checks are pointwise in \(Q\), because the tail/near cases exhaust every feasible \(Q\). Zero-mass vertices are evaluated by continuity. Tree cardinality and rejection of missing or trailing records are additional checks on the inductive cover. No statistical holdout is relevant to a deterministic universal inequality.

For comparison, the proposed whole-row fixed-tilt vertex bound loses substantial entropy. For any given feasible rows, take in each row the probability mixture of its pure vertices with weights \(Q_{ij}/a_i\). Affine terms, including antisymmetric multipliers, retain their value in the mixture and cancel where the rows agree. The convex term \((d/2)\sum_jQ_{ij}\log Q_{ij}\) gains precisely \((d/2)a_i H(Q_{i,\cdot}/a_i)\). In Case II use row-0 vertices with the \(02\) mass split into hot and cold categories, and row-2 vertices with \(r_2\) at either \(0\) or \(Q_{20}\). All affine terms still retain their values. The relative split entropy term vanishes at those row-0 pure vertices, so the mixture gains its negative as well. At any feasible row entropy law the linear-polynomial tilt objective is at least its Chernoff-optimal row entropy. The loss therefore lower-bounds the unsplit fixed-tilt architecture regardless of multiplier choice. Numerical examples are in [reference_table.json](reference_table.json). Its role is diagnostic. The exact proof uses the smaller set of explicit edge tails and profile vertices above.

## 6. Finite count after certification

For every compatible profile and type, the naive case has the pairing factor in §1. For each Case I occupancy leaf, the verifier checks the near-cell rate at \(q_*\) and \(a_{\min}\). It also checks the upper tail at \(q_*\) unless the box cap makes that tail empty. Both rates are at most \(-1/1000\). A type uses the near bound with extra factor \((D+1)n^{19}20^{19}\) or the tail bound with extra factor one. The cutoff classifies existing types, so it adds no multiplier to their count. Case II has at most \(D+1\) hot counts, since \(0\le R\le K_{02}\le D\). For every count the near bound in §4 applies because it upper-bounds the sum of the nonnegative conditional probabilities. A tail needs only the bound by one. Thus a conservative uniform extra prefactor across the three terms is \((D+1)^2n^{19}20^{19}\), even counting every \(R\) separately. By §1, the two count factors are \((n+1)^4\) and \((D+1)^5\). These factors and the at most \(10\) orientations and \(3\) terms give the bound in [PROOF.md](PROOF.md). [Independent numerical check](finite.log)
