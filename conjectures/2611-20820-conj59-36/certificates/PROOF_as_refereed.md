# A sharp bound for close-skew pairs in the binary cube

**Theorem.** Both Conjectures 5.9 and 3.6 of S. Selvaraja hold. For every integer pair $n>r\ge1$, the maximum length of a close-skew system in the binary $n$-cube is $2^r$, and $\theta(\mathrm{VR}(I_n;r))=2^r$.

## 1. Double the sequence

Write $d$ for Hamming distance. Call a list $(a_i,b_i)_{i=1}^m$ skew if $d(a_i,b_i)>r$ for each $i$ and $d(a_i,b_j)\le r$ for $i<j$. Given the vertices and witnesses of Conjecture 5.9, form the following list of **ordered** pairs.
$$
 (v_1,w_1),\ldots,(v_k,w_k),\quad
 (w_k,v_k),\ldots,(w_1,v_1).
$$
All $2k$ diagonals are far. For an earlier first entry and a later second entry there are exactly three possibilities.

* In the first half they are $v_i,w_j$ with $i<j$, so the witness condition gives closeness.
* Across the two halves they are $v_i,v_j$, close by the diameter hypothesis, including when $i=j$.
* In the reversed half they are $w_i,v_j$ with $i>j$, again close by the witness condition.

Thus the doubled list is skew. The skew Hamming bound of Gao and Zhao, as stated in Selvaraja, gives $2k\le 2^{r+1}$. Section 2 proves the binary bound directly, so the conclusion is unconditional even without importing that preprint. The doubling extends Selvaraja’s use of both orientations of each edge of an induced matching (source lines 982–992). Reversal of the second half is what allows one-sided witnesses here.

Equality is attained by Selvaraja’s subcube example. Use each $v=(x,0,0^{n-r-1})$ once, with $x\in\{0,1\}^r$, and pair it with $w=(\bar x,1,0^{n-r-1})$. The vertices have diameter $r$. Their diagonal distances are $r+1$, and the distance to the witness of any other vertex is $r+1-d(x,x')\le r$. This proves sharpness for every $n>r$.

## 2. A self-contained binary skew bound

Put $s=r+1$. Introduce independent variables $t_{hj}$ for $1\le h\le n$, $1\le j\le s$, and take the rational function field $K=\mathbb F_2(t_{hj})$. In the commutative $K$-algebra
$$
 A=K[e_1,\ldots,e_s]/(e_1^2,\ldots,e_s^2)
$$
the square-free monomials form a basis, so $\dim_K A=2^s$. Let $L:A\to K$ take the coefficient of $e_1\cdots e_s$. For coordinate $h$ set $u_h=\sum_{j=1}^s t_{hj}e_j$. In characteristic two $u_h^2=0$, so $(1+u_h)^2=1$. Encode a word $x$ by
$$
 P_x=\prod_{h:x_h=1}(1+u_h).
$$
Multiplying $P_x P_y$ cancels every common coordinate, leaving exactly the factors indexed by the difference set $D=\{h:x_h\ne y_h\}$.

**Threshold identity.** $L(P_xP_y)\ne0$ if and only if $|D|\ge s$. For $|D|<s$ the product has degree less than $s$ in the $e_j$. Otherwise choose distinct $h_1,\ldots,h_s$ in $D$. In the top coefficient the monomial $t_{h_1,1}\cdots t_{h_s,s}$ occurs exactly once. Its variables force the term drawn from each of those $s$ factors, and every other factor must contribute $1$. Its coefficient is one in $K$, even when $|D|>s$.

For any skew list form the $m\times m$ matrix $M_{ij}=L(P_{a_i}P_{b_j})$. Its entries above the diagonal are zero and its diagonal entries are nonzero by the threshold identity. Its rank is $m$. On the other hand, its columns are the evaluations of the linear functionals $z\mapsto L(zP_{b_j})$ on the $m$ vectors $P_{a_i}\in A$. Hence its rank is at most $\dim_K A=2^s$. This proves $m\le 2^{r+1}$ and completes the upper bound in Section 1.

There is also a direct way to read the factor of two from the same representation. The bilinear form $B(z,z')=L(zz')$ is nondegenerate since its matrix on square-free monomials pairs each subset with its complement. The $P_{v_i}$ are independent by their triangular matrix against the witnesses. Their span $U$ satisfies $U\subseteq U^\perp$ by pairwise closeness and the threshold identity. Thus $2k=2\dim U\le\dim A$. This gives the same bound without doubling the list.

## 3. Theta from deletion and link

Let $G$ be the graph on the cube joining pairs at distance greater than $r$. A set has diameter at most $r$ exactly when it is independent in $G$. Hence the complex in the question is $\operatorname{Ind}(G)$. Selvaraja’s inequalities give $2^r\le\theta(\operatorname{Ind}(G))\le d'(\operatorname{Ind}(G))$, where $d'$ equals the maximum close-skew length (source lines 828–841, 938–949, 1514–1526). Together with Section 1 this proves Conjecture 3.6. Here is a direct proof of these bounds for this application.

For any finite graph $H$ put $T(H)=\theta(\operatorname{Ind}(H))$. It is zero on edgeless graphs. For every nonisolated pivot $p$, deletion gives $H-p$ and link gives $H-N[p]$, where $N[p]$ is its closed neighborhood. The defining recurrence takes the minimum, over those pivots, of $\max(T(H-p),1+T(H-N[p]))$.

Let $s(H)$ be the longest list $(v_i,w_i)$ with the $v_i$ independent, each $v_iw_i$ an edge, and $v_jw_i$ a nonedge for $j<i$. It is monotone under taking induced subgraphs because each list remains valid in the larger graph. For any nonisolated $p$ choose a neighbor $q$. Prepending $(p,q)$ to any such list in $H-N[p]$ gives a list in $H$ because every entry from the smaller graph, including each later witness, is a nonneighbor of $p$. Therefore $1+s(H-N[p])\le s(H)$. Also $s(H-p)\le s(H)$. Induction on the vertex count in the recurrence gives $T(H)\le s(H)$. For the far-distance graph, Section 1 says $s(G)\le 2^r$.

For the lower bound, first note that adding an isolated vertex leaves $T$ unchanged. This follows by induction from the recurrence since every eligible pivot belongs to the old graph and both branches retain the isolate. Also $T$ is monotone on induced subgraphs. To see this, induct on $|V(H)|$ and take an optimal pivot $p$ of a nonedgeless $H$. For an induced $J\subseteq H$ omitting $p$, induction gives $T(J)\le T(H-p)$. If $p$ is isolated in $J$, discard it and use the same bound. Otherwise use $p$ as a candidate pivot in $J$ and compare its two branches by induction to the corresponding branches of $H$. The edgeless case is immediate.

In an $(r+1)$-coordinate subcube, the only edges of $G$ join antipodes. The induced graph is a matching with $2^r$ edges. A matching with $m$ edges has $T=m$ by induction. Deletion of a pivot leaves $m-1$ edges and an isolate, while the link branch leaves $m-1$ edges. Monotonicity gives $T(G)\ge 2^r$, as required. The argument also gives $\theta(\mathrm{VR}(Y;r))\le 2^r$ on every induced subset $Y$.

**Source and scope.** The conjectures, the subcube lower bound, the identification with Lew’s invariant, and the symmetric induced-matching doubling appear in [Selvaraja, arXiv:2611.20820v1](https://arxiv.org/abs/2611.20820v1). The paper attributes the unrestricted skew inequality to Gao and Zhao and the symmetric inequality to Alon, Jin and Sudakov. The proof above needs only the binary case and establishes it from linear algebra. All finite computations in the accompanying report are independent checks of consequences of the argument.
