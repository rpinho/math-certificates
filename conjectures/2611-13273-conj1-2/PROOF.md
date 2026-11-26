# Monotonicity of the normalized dichromatic polynomial

**Theorem.** Let $D$ be a finite loopless digraph on $n\ge2$ vertices. For every real $x\ge n-1$,
$$
H_D(x):=xP_D'(x)-nP_D(x)\ge0.
$$
Consequently $P_D(x)/x^n$ is nondecreasing on $[n-1,\infty)$, and $P_D(n)/n^n\ge P_D(n-1)/(n-1)^n$. If $D$ contains a directed cycle, then $H_D(x)>0$ for $x>n-1$ and the last inequality is strict. For a DAG the normalized polynomial is identically one.

## Decompose at one vertex

Call a set *allowed* when it induces an acyclic subdigraph. Every singleton is allowed, and every subset of an allowed set is allowed. Write $P_U$ for the coloring polynomial of $D[U]$ and $H_U(t)=tP_U'(t)-|U|P_U(t)$. For the empty set take $P_\varnothing=1$ and $H_\varnothing=0$.

Fix $v\in V$. Sum over all allowed $S$ containing $v$, and write $R=V\setminus S$, $m=|R|$ in each summand. At a positive integer $x\ge n$, the color class of $v$ is exactly one such $S$. Choose its color and then color $R$ with the other $x-1$ colors. Thus, as a polynomial identity,
$$
P_V(x)=x\sum_S P_R(x-1). \tag{1}
$$
Differentiate (1), multiply by $x$, and subtract $nP_V(x)$. This gives $H_V=x\sum_S[xP_R'(x-1)-(n-1)P_R(x-1)]$. Using $m=n-|S|$ now gives
$$
(x-1)H_V(x)=x^2\sum_S H_R(x-1)
 +x\sum_S\big[(n-1)-x(|S|-1)\big]P_R(x-1). \tag{2}
$$

## Count the second sum by deleting the marked vertex

Let $\pi$ range over partitions of $V\setminus\{v\}$ into nonempty allowed blocks. Set $k=|\pi|$ and
$$
\mathcal B(\pi)=\{B\in\pi:B\cup\{v\}\text{ is not allowed}\},\quad
b=|\mathcal B(\pi)|,\quad h=\sum_{B\in\mathcal B(\pi)}|B|.
$$
For an integer $x\ge n$, assign distinct colors to the blocks of $\pi$ in $(x)_k=x(x-1)\cdots(x-k+1)$ ways. There are $x-b$ ways to extend this assignment to $v$. Each unused color makes $v$ a singleton. Each allowed existing color puts $v$ into its block $B$, giving $|S|-1=|B|$. Hence the sum of $|S|-1$ over all extensions of this fixed assignment equals $(n-1)-h$.

The second term of (2) counts all proper colorings with weight $(n-1)-x(|S|-1)$. The total weight of the extensions of the fixed assignment is
$$
(n-1)(x-b)-x((n-1)-h)
= xh-(n-1)b
= \sum_{B\in\mathcal B(\pi)}(x|B|-(n-1)).
$$
This proves the following identity at every integer $x\ge n$. Both sides are polynomials, so it holds at every real $x$:
$$
\boxed{(x-1)H_V(x)
=x^2\sum_{S\ni v\;\mathrm{allowed}}H_{V\setminus S}(x-1)
+\sum_\pi (x)_{|\pi|}\sum_{B\in\mathcal B(\pi)}\big(x|B|-(n-1)\big).} \tag{3}
$$

## Induction and endpoints

For empty and one-vertex digraphs $H\equiv0$. Assume the theorem for all smaller orders and take $n\ge2$, $x>n-1$. In the first sum in (3), $m\le n-1$, so $x-1>n-2\ge m-1$. Every $H_R(x-1)$ is nonnegative by induction or the base cases. In the second sum, $k\le n-1$, so every falling factorial is positive. Each forbidden block is nonempty, whence $x|B|-(n-1)>0$. Thus $(x-1)H_V(x)\ge0$, and $x-1>0$. Polynomial continuity gives $H_V(n-1)\ge0$, including $n=2$.

On the claimed interval $x>0$ and $(P_V(x)/x^n)'=H_V(x)/x^{n+1}$. This proves Conjecture 2. Applying it at $n-1$ and $n$ proves Conjecture 1.

For strictness choose an inclusion-minimal cyclic vertex set $C$ and $v\in C$. The partition with block $C\setminus\{v\}$ and all remaining vertices singleton is allowed upon deletion of $v$. That block is forbidden for the extension, giving a strictly positive term in (3) for $x>n-1$. If $D$ is acyclic, all $x^n$ maps are proper at integral $x$, giving $P_D=x^n$.

The paper's order-one ratios at zero have a removable singularity. For the loopless singleton $P_D=x$ and the normalized function extends as the constant one. If directed loops are admitted as cycles, the presence of a loop makes $P_D$ identically zero, and the inequalities hold with equality wherever defined (also by continuous extension at zero).

The proof uses only heredity of allowed blocks and admissibility of singletons, so the same argument applies to colorings excluding monochromatic hyperedges of size at least two. The marked-class decomposition follows the color-class argument used in Section 5 of Crew et al. Identity (3) supplies the derivative sign for the two conjectures in Section 8. Dong's graph theorem is the bidirected special case. The argument above is self-contained. [Crew et al., v1](https://arxiv.org/abs/2611.13273v1)
