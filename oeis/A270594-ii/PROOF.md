# Exact exhaustion for the A270594(ii) counterexample

Let $N=1782381$. For integers $x,y,z$, define
`pen(x) = x(3x+1)/2`, `T(y) = y(y+1)/2`, and `hep(z) = z(5z+3)/2`.
All three are integers and all summands in the target formula are nonnegative.

## Why the ranges are exhaustive

For integer $x$, $|3x+1|\ge 2|x|$, so $4\operatorname{pen}(x)^2\ge 4x^4$. Also $\operatorname{hep}(z)-z^2=3z(z+1)/2\ge 0$ for every integer $z$. For any target $m$ in $[0,N]$, it is enough to test both signs up to the largest absolute $x$ with $4x^4\le m$ and, for each $x$, the largest absolute $z$ with $z^2\le m-4\operatorname{pen}(x)^2$.

For each admissible pair, let $t=m-4\operatorname{pen}(x)^2-\operatorname{hep}(z)\ge 0$. If $T(y)=t$, then $(2y+1)^2=8t+1$. Conversely, if $8t+1=s^2$, the nonnegative root $s$ is odd and $y=(s-1)/2$ gives $T(y)=t$. The other integer root corresponds to $-1-y$.

The exact integer calculation in `check_a270594.py` at $m=N$ succeeds in enumerating all 62,229 admissible pairs, with zero square discriminants. The adjacent targets have 184 and 156 ordered witnesses, respectively. [Producer output](certificates/a270594-replay.txt)

## Why the counterexample is smallest

Form a bitset with bit $T(y)$ set for every $y\ge 0$ with $T(y)\le N$. This covers all triangular values up to $N$ because $T(y)=T(-1-y)$. Shifting by a nonnegative integer adds it to all represented values. Taking the bitwise union over all allowable $\operatorname{hep}(z)$ gives exactly the pair sums. Taking the bitwise union of those bitsets shifted by each allowable $4\operatorname{pen}(x)^2$ gives exactly the three-term sums. Truncation above $N$ is valid at each stage because all shifts are nonnegative. The complement in $[0,N]$ has the single position $N$ set.

The clean-room checker `referee/referee_check.py` uses its own two-sided ranges and adds the pentagonal term before the heptagonal term in its sieve. Its only missing value on $[0,2000000]$ is $N$. It also checks nonrepresentation at $N$ in a fixed wide box and by testing for a generalized pentagonal number after enumerating the triangular and heptagonal terms. The sieve and direct tests agree at every point checked. The full outputs include witnesses for both neighbors and controls that need negative $x$ or negative $z$. [Referee output](referee/run.log)

This is an exact finite certificate. Both checkers exhaust the relevant domain, so a statistical holdout does not apply.
