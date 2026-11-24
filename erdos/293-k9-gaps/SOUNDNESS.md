# Why the search is exhaustive

For $m>1$, remove $1/m$ from a representation containing it. This is a bijection with strictly increasing lists of $k-1$ distinct denominators, each at least 2 and different from $m$, whose reciprocal sum is $(m-1)/m$. The solver searches this latter set. The explanations below apply to the unmutated executable.

## Rational state and bounds

Write the positive residual as a reduced fraction $p/q$. Write $t$ for the number of terms still to choose and $u$ for the last prefix denominator, or 1 at the root. If $t\ge2$ and the next denominator is $a$, positivity of the remaining terms gives $a>q/p$. Increasing order gives $a>u$ and makes the residual strictly less than $t/a$. Thus the inclusive search bounds are

$$
\max(u+1,\lfloor q/p\rfloor+1)\le a\le\left\lfloor\frac{tq-1}{p}\right\rfloor .
$$

The solver discards $a=m$. A branch with zero residual and terms still to place has no continuation because every term is positive.

For the prime-power bound, the reduced denominator $q$ divides the least common multiple of the remaining denominators. If $P^e\mid q$, at least one remaining denominator is divisible by $P^e$. Its term is at most $1/P^e$, and each of the other $t-1$ terms is at most $1/a$. When $p>q/P^e$, this gives a second inclusive upper bound

$$
a\le\left\lfloor\frac{(t-1)q}{p-q/P^e}\right\rfloor .
$$

The implementation picks a prime power of $m$ at the root and applies the bound only while that power divides the current reduced $q$. Requiring another multiple of $m$ would lose the valid representation $1/2+1/3+1/7+1/42=1$ at $m=42$.

To update the reduced fraction after choosing $a$, let $g=\gcd(q,a)$, $Q=q/g$ and $A=a/g$. The unreduced residual is $(pA-Q)/(qA)$. Since $\gcd(Q,A)=1$ and $\gcd(p,Q)=1$, its numerator is coprime to both $Q$ and $A$. All cancellations therefore come from $g$, and dividing numerator and denominator by $h=\gcd(pA-Q,g)$ reduces the fraction exactly.

## Closing one or two terms

For one remaining term the reduced numerator must be 1. The sole denominator $q$ is accepted if it exceeds $u$ and differs from $m$.

For two remaining terms $a<b$, clearing denominators gives

$$
(pa-q)(pb-q)=q^2.
$$

Both factors are positive because $p/q>1/a$ and $p/q>1/b$. The smaller factor $d=pa-q$ therefore satisfies $1\le d<q$. The required prefix order also gives $d\ge p(u+1)-q$. Conversely, for every divisor of $q^2$ in this interval, the solver first checks that $a=(q+d)/p$ is integral. The gcd of $p$ and $d$ is 1 because $d=pa-q$ and $\gcd(p,q)=1$. Then $d\mid q^2$ implies $d\mid paq$, so $b=aq/d$ is integral. The identity gives the required sum, and $d<q$ gives $b>a$. The solver checks that both terms differ from $m$. These conditions are necessary and sufficient, and a valid pair determines its own unique $d$.

If $q=\prod_j P_j^{e_j}$, the divisor loop enumerates each product with exponents from 0 through $2e_j$. Once a partial product exceeds the upper bound, adding more prime powers can only increase it. The loop tests the lower bound only after all exponents are assigned. This enumerates the divisors of $q^2$ without materializing $q^2$. The product $aq$ and the returned $b$ are calculated with GMP. The Sylvester control exercises an 87-bit $q$ and a 174-bit last term.

## Prime sources and integer bounds

For any DFS prefix, its reduced denominator divides $m$ times the product of its chosen denominators. In the update described above, the solver adds the factors of $A$, removes the factors of $h$, and asserts that the factorization multiplies back to the actual reduced denominator. It also asserts that every such product fits the native type. The smallest-prime-factor table covers integers through 13,000,000. Factors of larger inputs, including the fixed $m$ and deep control prefixes, are obtained by trial division by the sieve primes, with an asserted square-root coverage check before a remaining cofactor is declared prime.

Here is the finite derivation of the sieve bound for the target. For $j=1,\ldots,5$, let $G_j$ be the sum of the reciprocals of the first $j$ entries of $(2,3,7,43,1807)$, and put $G_0=0$. The first part of `geometry.py` checks exactly that no increasing $j$-term sum below 1 exceeds $G_j$. At a partial sum $s<G_j$ with $\ell$ terms left, any completion reaching $G_j$ has next denominator at most $\lfloor\ell/(G_j-s)\rfloor$. All values to that bound are checked and a partial sum at least 1 cannot complete below 1. If $s\ge G_j$ before length $j$, it is already enough to refute the proposed bound because distinct sufficiently large terms can extend it while keeping the sum below 1. The exact replay found equality only at the given greedy prefixes. Numerators, denominators, and the visited counts are in `logs/geometry.log`.

After $j$ choices, the residual is at least $1-1/m-G_j$. At $m=13{,}856{,}993$ this gap is positive for all $j=0,\ldots,5$. Applying the ordinary $t/a$ bound at each level gives these inclusive bounds for the six DFS choices.

$$
8,\quad14,\quad36,\quad210,\quad7224,\quad12{,}806{,}327 .
$$

The last is the choice made with three terms left. These bounds are all within the sieve limit and below $m$. The product of the bounds times $m$ has 80 bits and bounds every main $q$, even if there is no cancellation. The 128-bit prefix representation, the doubled $q$ in the bounds, and the partial divisor products below $q$ therefore fit. The solver checks its native arithmetic, the sieve coverage, and the factorization at runtime. An invariant failure is explicit and cannot produce a successful shard record.

## Partition and verification

The manifest fixes four initial choices and an interval for the next choice. Where that interval would create a large shard, it fixes five choices and partitions the final DFS choice into adjacent intervals. `run_main.py` reconstructs allowable ranges with Python exact fractions. It requires that every allowable prefix before the two-term step is routed to exactly one shard and that every shard visits its computed number of two-term states. Any positive answer must also pass a separate Python rational check. The sum of the predicted two-term state counts is independent of the C search's visit counters.

`enumerator.c` uses a separate full search with no fixed $m$, no factorization, and no prime-power pruning. It scans the next denominator and tests the remaining one-term residual by exact division. The certificate checker in `check_certificates.c` independently parses labels and denominators and tests each sum with GMP rational arithmetic. Distinctness, membership, and coverage are checked on the parsed records. This is an exact existence and absence claim over fixed integers, so a statistical holdout does not apply.
