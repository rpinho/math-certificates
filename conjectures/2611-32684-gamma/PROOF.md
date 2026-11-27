# A counterexample to the Discussion conjecture

Let two copies of \(K_{3,3}\) have shores

| Copy | First shore | Second shore |
|---|---|---|
| Left | \(x,a,b\) | \(u_1,u_2,u_3\) |
| Right | \(x,c,d\) | \(v_1,v_2,v_3\) |

They share only \(x\). Add the matching edges \(ac\) and \(bd\). The resulting simple graph \(G\) has 11 vertices and 20 edges. In the certificate the labels for \(x,a,b,c,d,u_1,u_2,u_3,v_1,v_2,v_3\) are \(0,1,2,3,4,5,6,7,8,9,10\), respectively. [Edge list](witness.json)

**Connectivity.** If at most two vertices are removed and \(x\) survives, each copy of \(K_{3,3}\) stays connected and contains \(x\). If \(x\) is removed, each copy becomes \(K_{2,3}\), which survives the removal of one more vertex connected. At least one of the two matching edges survives because their endpoints are disjoint. Thus \(G\) is 3-connected. Removing \(x,a,b\) isolates the three \(u_i\), so its vertex connectivity is exactly 3. The cycle \(x,u_1,a,c,v_1,x\) has length five.

**Derivative.** First colour \(x,a,b,c,d\), respecting the two matching edges. If the triples \((x,a,b)\) and \((x,c,d)\) use \(r\) and \(s\) colours, the remaining six vertices can be coloured in \((q-r)^3(q-s)^3\) ways. For any fixed equality pattern of the five colours the number of assignments is a falling factorial, hence a polynomial. All patterns with \(r=2\) or \(s=2\) therefore have derivative zero at 2.

If \(r=s=1\), edge \(ac\) is monochromatic. The remaining possibilities contribute as follows, with \((q)_3=q(q-1)(q-2)\).

| \((r,s)\) | Assignments to the five first-shore vertices | Extensions to the six remaining vertices |
|---|---|---|
| \((1,3)\) or \((3,1)\) | \((q)_3\) for each case | \((q-1)^3(q-3)^3\) |
| \((3,3)\) | \((q)_3\big((q-2)^2-(q-3)\big)\) | \((q-3)^6\) |

For the last row, fix distinct colours on \(x,a,b\). There are \(q-2\) choices each for \(c\) and \(d\) after excluding the colour on \(x\) and the colour on the matched vertex. The \(q-3\) assignments with \(c=d\) must be subtracted. The counting identities hold for all sufficiently large integer palettes and hence as polynomial identities.

Since \((q)_3\) vanishes at 2 and its derivative there is 2, the table gives

\[
\chi'_G(2)=2\left(2(1)^3(-1)^3+\big(0^2-(-1)\big)(-1)^6\right)=-2.
\]

As \(|V(G)|=11\), the paper's normalization gives \(\gamma(G)=\tfrac12(-1)^{10}(-2)=-1\). This disproves the conjecture.

## Full polynomial and the root in the open interval

The two integer algorithms in the verifier give \(\chi_G(q)=(q)_3Q(q)\), where

\[
Q(q)=q^8-17q^7+137q^6-677q^5+2228q^4-4969q^3+7284q^2-6363q+2509.
\]

In particular \(Q(2)=-1\). There is exactly one real chromatic root in \((1,2)\), counted with multiplicity. The substitution \(q=(1+2t)/(1+t)\) maps positive \(t\) bijectively to that interval. In ascending degree the coefficients of \((1+t)^8 Q((1+2t)/(1+t))\) are

\[
(133,600,1177,1284,828,304,51,-1,-1).
\]

There is one sign change, and the constant and leading coefficients have opposite signs. Descartes' rule and continuity give exactly one positive root. It lies between \(19/10\) and \(39/20\), as the two values of \(Q\) are \(3694111/100000000\) and \(-14608211579/25600000000\).

The conjecture, notation and normalization are from Aatman Supkar and Upamanyu Yaddanapudi, *Schnyder Woods and the Chromatic Polynomial*, Discussion (v1, November 2026). [Source](https://arxiv.org/abs/2611.32684v1)
