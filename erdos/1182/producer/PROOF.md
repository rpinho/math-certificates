# Erdős #1182: \(F(n)\le 5n-1\) for every \(n\ge550{,}000\)

Write \(F(n)\) for the largest integer edge budget for which every connected \(n\)-vertex graph is triangle-good. All logarithms are natural. The argument uses the triangle-free \(C_5\) blow-up and random-regular framework of Brandt and Kataria, also used by Nikiforov and Rousseau. The new step is a recoloring argument for a potential-minimal map. [Credit and baseline comparison](PRIOR_ART.md)

## Reduction to part maps

Fix \(n\ge550{,}000\). Form \(H_n\) on \(2n-1=5h+s\) vertices by blowing up \(C_5\) into independent parts of sizes \(k_i\in\{h,h+1\}\), with \(s\) larger parts. Its red edges are between parts whose indices differ by \(1\) modulo \(5\). The blue adjacency matrix \(A\) allows differences \(0,2,3\). There is no red triangle.

Pair \(D=10n\) labelled stubs uniformly, with ten at each vertex. The resulting multigraph \(M\) simplifies to a graph \(G\) on the same vertices with at most \(5n\) edges. A map \(f:V(M)\to\mathbb Z_5\) is valid if it obeys the capacities and all its paired stubs have blue part-index pairs. Such maps exist exactly when \(G\subseteq\overline{H_n}\). An embedding induces a map. A valid map extends to an embedding by injecting into each part. Loops always satisfy \(A_{ii}=1\), and parallel edges repeat the same constraint. Simplification preserves connectivity. Since \(D\) is even for every integer \(n\), this construction applies to odd \(n\) as well.

Given any valid map, choose one minimizing \(\Phi=\sum_i v_i^2\), where \(v_i=|f^{-1}(i)|\). We bound the expectation of the count \(X_{\rm rigid}\) of valid maps satisfying the necessary conditions below. If there is a valid map, a minimizing map contributes to \(X_{\rm rigid}\).

## Canonical regions and the integer hypotheses

Each feasible profile \(a_i=v_i/n\) has \(\sum_i a_i=1\) and \(\max a_i\le 2/5+3/(5n)\le4001/10000\). Choose any pair of two largest parts. If red-adjacent, rotate and reflect so \(a_0\ge a_1\ge\max(a_2,a_3,a_4)\), Region A. Otherwise rotate the unordered blue pair to \(\{0,2\}\), and apply the reflection \((0\ 2)(3\ 4)\) if needed to achieve \(a_3\ge a_4\). This leaves \(a_0,a_2\) unordered. With \(\delta=3/20\), Region B has \(\min(a_0,a_2)-a_3\le\delta\), and Region C has \(\min(a_0,a_2)-a_3\ge\delta\). Both take their common boundary. This covers every tie as well. There are ten dihedral maps. They permute the capacities, whose range remains \(\{h,h+1\}\).

In C, \(v_0-v_3\ge\delta n\), \(v_2-v_3\ge\delta n\), and \(v_2-v_4\ge\delta n\). These imply gaps of at least two already for \(n\ge14\). If \(v_i\ge v_j+2\), then \(v_j+1\le h\), since \(v_i\le h+1\). A net transfer from such an \(i\) to \(j\) fits the capacities. The proof uses no condition on \(v_3-v_1\).

## Kempe-swap dichotomy

Use \(n_i(u)\) for the number of stubs at \(u\) whose mates are in part \(i\). A one-vertex move from \(V_0\) to \(V_3\) is valid when \(n_2(u)=0\), because the other possible neighbor parts are \(0,3\). A move from \(V_2\) to \(V_4\) is valid when \(n_0(v)=0\), because the other possible neighbor parts are \(2,4\). A self-loop follows its vertex in both moves. A net transfer \(i\to j\) changes \(\Phi\) by \(2(v_j-v_i+1)\le-2\). Hence every vertex of \(V_0\) has \(n_2\ge1\) and every vertex of \(V_2\) has \(n_0\ge1\).

Put \(Z_0=\{u'\in V_0:n_3(u')=0\}\) and \(G_2=\{v\in V_2:n_4(v)=0\}\). If \(|Z_0|<2d\), we have Case I, with at most \(2d-1=19\) exceptions to \(n_3\ge1\) on \(V_0\). Otherwise, suppose some \(u\in V_0\) has all its \(V_2\) neighbors in \(G_2\). List its \(r\) distinct \(V_2\) neighbors as \(v_1,\ldots,v_r\), so \(1\le r\le d\). Choose \(r-1\) distinct donors in \(Z_0\setminus(N_M(u)\cup\{u\})\), possible since the latter set has at least \(2d-(d-r)-1\) vertices. Simultaneously change \(u:0\to3\), each \(v_j:2\to0\), and each donor \(0\to2\). This is a net transfer \(2\to3\), so it fits and strictly decreases \(\Phi\). In the case \(r=0\), the one-vertex move above is the net transfer \(0\to3\).

To check the swap, the old \(V_2\) neighbors of \(u\) are all moved to \(0\). Its other neighbors are in \(0,3\) and none are donors. A moved \(v_j\) had no neighbors in \(4\) and originally could touch only \(0,2,4\). Its new possible neighbor parts are \(0,2,3\), all blue from its new part \(0\). A donor had no neighbors in \(3\), could originally touch only \(0,2,3\), and is nonadjacent to \(u\). Its new possible neighbor parts are \(0,2\), both blue from its new part \(2\). This also checks edges within each moved class and loops. Thus the minimizing map cannot have such a vertex \(u\). This gives Case II: every \(u\in V_0\) has some neighbor \(v\in V_2\setminus G_2\), and every \(v\in V_2\) has \(n_0(v)\ge1\).

## Certified first moment and connectivity

[LEMMAS.md](LEMMAS.md) counts the valid maps by exact pairing type, gives the exact Case II joint law, and derives finite upper bounds for both cases. In Case I the occupancy exponent increases with \(Q_{03}\) and decreases with \(a_0\) at fixed \(Q_{03}\). Each occupancy leaf bounds the near types \(Q_{03}\le q_*\) at the upper cutoff and the lower part-0 endpoint. If the box permits \(Q_{03}>q_*\), the verifier requires \(q_*>B_{03}\) and uses the binary relative-entropy bound for that upper tail. Each type is counted once within its case, with the conditional probability bounded by one in the tail.

The three Arb certificates verify a rate upper bound of \(-1/1000\) in A and B and for each case in C. The verifier reconstructs every tree from the common exact root and checks outward-rounded profile vertices, edge-divergence cutoffs and occupancy bounds. [Certificate replay](verify.log)

At most \(10\) orientations, \(3\) terms, \((n+1)^4\) profiles, and \((10n+1)^5\) symmetric integer types per profile give the finite bound derived in the lemmas, including the sum over every possible hot count in Case II:
\[
 \mathbb E X_{\rm rigid}
 \le 30\cdot 3^6(n+1)^4(10n+1)^{10}\,n^{19}20^{19}\,e^{-n/1000}.
\]
A disconnected pairing has a nonempty isolated set of \(k\le n/2\) vertices. For a fixed set, revealing its internal stub partners in order gives isolation probability at most \((k/n)^{5k}\). At each step with \(j\) internal pairs already revealed, its next mate is inside with probability \((10k-2j-1)/(10n-2j-1)\le k/n\). Since \(\binom nk\le(en/k)^k\) and \(e<3\), the union bound over \(k\) is at most \(\sum_{k\ge1}(3/16)^k=3/13<1/2\).

At \(n=550{,}000\), the first-moment upper bound is less than \(4.261\times10^{-11}\). Its logarithmic derivative is at most \(33/n-1/1000<0\) thereafter. The cap, gap and exemption conditions also persist. Thus \(\Pr(X_{\rm rigid}>0)+\Pr(M\text{ disconnected})<1\) for all \(n\ge550{,}000\). Some connected \(M\) has no valid map. Its simplification satisfies \(R(K_3,G)>2n-1\) and \(e(G)\le5n\), so \(F(n)\le e(G)-1\le5n-1\). [Finite check](finite.log)
