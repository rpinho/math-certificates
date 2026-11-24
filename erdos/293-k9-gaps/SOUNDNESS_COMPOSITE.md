# Exhaustiveness for composite fixed denominators

The search adapts our prior Erdős #293 solver, whose rational bounds, reduction, and two-term proof are in [the previous soundness note](SOUNDNESS.md). The release checker and the full control enumerator are separate from the fixed-denominator search.

## Removing the fixed denominator

For any integer $m>1$, removing $1/m$ gives a bijection between the desired representations and strictly increasing lists of $k-1$ distinct integers at least 2, excluding $m$, whose reciprocals sum to $(m-1)/m$. The root fraction is reduced since consecutive integers are coprime. At each prefix the solver stores the positive reduced remainder $p/q$. Write $t$ for the number of terms still required and $u$ for the previous denominator, with $u=1$ at the root.

For $t\geq 2$, the next denominator $a$ satisfies $a>u$, $a>q/p$ and $p/q<t/a$. The last inequality is strict because at least one further denominator exceeds $a$. Thus the ordinary inclusive interval is

$$
\max(u+1,\lfloor q/p\rfloor+1)\leq a\leq\lfloor(tq-1)/p\rfloor.
$$

The solver excludes $a=m$. A zero residual cannot be extended by positive terms.

## Prime-power rule for composite $m$

Let $P^e$ exactly divide $m$. In a full representation of 1, subtracting $1/m$ leaves $(m-1)/m$, whose reduced denominator is $m$. If the remaining denominators are $a_1,\ldots,a_{k-1}$, their reciprocal sum has a denominator dividing $L=\operatorname{lcm}(a_1,\ldots,a_{k-1})$. Therefore $m\mid L$. In particular $v_P(L)=\max_i v_P(a_i)\ge e$, so at least one other term is divisible by $P^e$. Each prime power has this requirement separately. The terms witnessing different powers may differ. For example, in $(2,3,7,42)$ the three powers of 42 occur separately in the remaining terms.

The same lcm argument at any prefix gives $q\mid\operatorname{lcm}(a_1,\ldots,a_t)$ for a valid completion of $p/q$. If one of the root powers $H=P^e$ divides $q$, one remaining denominator is a multiple of $H$. That term is at most $1/H$. Each of the $t-1$ other terms is at most $1/a$, giving $p/q\le 1/H+(t-1)/a$. When $p>q/H$, this bounds $a$ above by $\lfloor(t-1)q/(p-q/H)\rfloor$. Otherwise it imposes no upper bound. Among powers dividing $q$, the largest $H$ gives the strongest upper bound when one exists, since $q/H$ decreases as $H$ increases. If the largest gives no bound then no smaller applicable power does. The solver checks the root powers in decreasing order until one divides $q$. The separate manifest replay applies every applicable inequality with Python fractions.

## Factorization and arithmetic bounds

The reduced denominator after choices $a_1,\ldots,a_j$ divides $\operatorname{lcm}(m,a_1,\ldots,a_j)$, since this is a common denominator for $1-1/m-\sum_{i=1}^{j}1/a_i$. Thus every prime dividing $q$ comes from $m$ or a chosen denominator. The prime exponent in $q$ is bounded by the maximum of the exponents in those denominators. The factorization of $m$ itself is obtained by the sieve and exact trial division, just as for any input denominator.

The incremental reduction uses $g=\gcd(q,a)$, $Q=q/g$, $A=a/g$. The unreduced numerator and denominator are $pA-Q$ and $qA$. The numerator is coprime to $A$ and $Q$ because $\gcd(A,Q)=\gcd(p,Q)=1$, so the entire cancellation is $h=\gcd(pA-Q,g)$. The new factor list adds the factors of $A$ and subtracts those of $h$. Both divide $a$, and the exact product of the resulting list is checked against the new $q$. A prime larger than the sieve may remain from $m$, or from an out-of-campaign input after trial division. The solver declares an unfactored cofactor prime only after confirming the trial-prime table covers its square root. Unsupported arithmetic, factorization and counter overflow issue a skipped diagnostic and abort the shard.

For the campaign interval, the five-term bound in the geometry module replays the finite search for the maximum sum of $j\le5$ increasing unit fractions strictly below 1. Its maximum $G_j$ is the sum of the first $j$ reciprocals from $(2,3,7,43,1807)$. Set $G_0=0$. If a prefix sum $s<G_j$ has $\ell$ terms left, a completion reaching $G_j$ has next denominator at most $\lfloor\ell/(G_j-s)\rfloor$. The replay checks all denominators through that bound. A prefix reaching $G_j$ before the last choice would give a strict improvement by adding sufficiently large denominators while staying below 1. No such prefix occurred.

For $13{,}856{,}993\le m\le20{,}000{,}000$, the residual after $j$ choices is at least $1-1/m-G_j$, which increases with $m$ and is positive for $0\le j\le5$. Thus the coordinate caps for all six prefix choices are bounded by their values at $m=13{,}856{,}993$,

$$
8,\quad14,\quad36,\quad210,\quad7224,\quad12{,}806{,}327.
$$

Each is below 13,000,000 and below every campaign $m$. For these choices, $A,h\le a$ are covered by the smallest-prime-factor table. The root $m$ needs trial primes only up to $\sqrt{20{,}000{,}000}<4473$. The product of $m$ and the six caps bounds every prefix denominator and its unreduced product at each update. This fits in 128 bits, including the small multipliers in the bounds. The verifier calculates the caps and bit bounds separately for each $m$ from the exact residual lower sums. The solver also checks its arithmetic at runtime. Outside the campaign, an input can be refused if trial division or the word limits do not suffice.

## Closing the search

For one remaining denominator, the reduced numerator must be 1, and $q$ is accepted only if $q>u$ and $q\ne m$.

For two remaining denominators $a<b$, clearing denominators gives $(pa-q)(pb-q)=q^2$. Both factors are positive and the smaller one $d=pa-q$ satisfies $1\le d<q$ and $d\ge p(u+1)-q$. The solver traverses all divisors of $q^2$ in this interval by a product of prime powers with exponents ranging from 0 to twice each exponent of $q$. Partial products above the interval cannot decrease. Given an admissible divisor, the congruence $p\mid(q+d)$ gives the integral $a=(q+d)/p$. Since $\gcd(d,p)=1$ and $pa=q+d$, the condition $d\mid q^2$ implies $d\mid aq$. Then $b=aq/d$ is integral, is strictly larger than $a$ because $d<q$, and yields the required sum. GMP evaluates $aq$, the division, and the resulting $b$. Both terms are checked against $m$.

The manifest routes each allowable depth-five choice to an interval below a depth-four prefix or splits its depth-six interval into adjacent pieces below that depth-five prefix. The separate partition replay checks all these intervals by exact rational inequalities and gives an expected count of two-term states per shard. Every completed zero shard must visit this many states and report zero skips. An interrupted or not-started shard leaves the candidate unsettled in the absence of a witness. A first hit ends early only after a separate exact Python check of nine positive, distinct integer terms, membership of $m$, and reciprocal sum 1. Its prefix must also match its shard. The same sum check is reapplied when harvesting raw outputs.

The separate GMP release checker validates the raw denominator integers of each line and checks their sum before using its label. It additionally checks whether any absent labels occur as terms on other valid rows. The separate low-order enumerator uses a direct denominator scan and exact division at the end, with no fixed denominator, factorization or prime-power pruning. These are finite exact statements about fixed integers, so there is no statistical holdout.
