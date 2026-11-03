# Explicit asymptotic steps for the lower-potential proof

Candidate and unrefereed. These details supplement PROOF_C31_LOWER.md.
They concern the analytic implication, not the finite integer checker.

Let a_m be the expected LCS of two independent uniform length-m strings.
Concatenating optimal subsequences from two disjoint blocks proves
 a_(m+n)>=a_m+a_n. Fix k>=1 and write m=qk+t, 0<=t<k. Then
a_m>=q*a_k+a_t>=q*a_k, since lengths are nonnegative. Dividing by m
and letting m increase gives liminf a_m/m>=a_k/k. Taking the supremum
in k, and using a_m/m<=sup_k a_k/k for every m, proves convergence to
 gamma=sup_k a_k/k. Also 0<=gamma<=1, since 0<=a_m<=m.

For fixed i,j, concatenate independent rectangular instances of lengths
(i,j) and (j,i). This produces two independent uniform strings of length
i+j and a common subsequence whose length is the sum of their two LCSs.
The expected rectangular LCS is symmetric in i,j. Therefore

    2 E[LCS(i,j)] <= a_(i+j) <= gamma*(i+j).

Here and below LCS(i,j) uses prefixes of the original independent infinite
strings. Its dependence among different pairs i,j does not affect a union
bound.

For completeness, the required concentration bound follows as follows.
For any random variable X in an interval of length1, let
 g(lambda)=log E exp(lambda*(X-E X)). Exponential tilting gives
 g''(lambda)=Var_lambda(X)<=1/4: for any distribution on [a,b],
 Var(X)<=E[(X-(a+b)/2)^2]<=(b-a)^2/4. Since g(0)=g'(0)=0,
integrating twice gives g(lambda)<=lambda^2/8 for lambda>=0.
This also proves the conditional version by applying the same argument
to each conditional distribution.

Reveal the i+j independent letters in a rectangular LCS one at a time.
Changing one letter changes the LCS by at most1: remove its possible use
from an old optimal subsequence, and use the reverse argument for the
opposite inequality. Coupling the unrevealed letters identically shows
that each conditional-expectation martingale difference has conditional
range at most1 and conditional mean0. Apply the preceding exponential
bound successively and use conditional expectation to obtain

    E exp(lambda*(LCS(i,j)-E LCS(i,j)))
        <= exp((i+j)*lambda^2/8).

Markov's inequality and lambda=4t/(i+j) give

    P(LCS(i,j)-E LCS(i,j)>=t) <= exp(-2t^2/(i+j)), t>0.

The case i+j=0 is deterministic0 and needs no division. Let D_n be the
maximum over pairs i+j<=n. There are at most (n+1)^2 pairs and every
rectangular mean is at most gamma*n/2. Thus for n>=1,

    P(D_n-gamma*n/2>=t) <= (n+1)^2 exp(-2t^2/n).

Choose t0=sqrt(n*log((n+1)^2)/2)>0. Integrating the upper tail and using
 t/t0>=1 for t>=t0 gives

    E D_n <= gamma*n/2 + t0
            +(n+1)^2 integral_(t0)^infinity exp(-2t^2/n) dt
          <= gamma*n/2 + t0 + n/(4t0).

For the last inequality replace the integrand by
 (t/t0)exp(-2t^2/n), integrate its exact antiderivative
 -(n/(4t0))exp(-2t^2/n), and use
 (n+1)^2 exp(-2t0^2/n)=1. Dividing both error terms by n shows that they
tend to zero. The logarithm grows more slowly than n, while t0 grows
without bound.

In the policy argument, let I,J be the two consumed-prefix lengths and
M the number of matches when total consumption first reaches N. Each
step consumes 1 or 2 letters, so N<=I+J<=N+1 and at most N steps occur.
Fresh appended letters remain uniform and independent conditional on
all past observations and current lookahead, because they have not yet
been revealed in the two original independent sequences. The chosen
mismatch action depends only on that current lookahead.

A mismatched step has expected potential increment at least r; a matched
step has expected increment at least r-1 and earns one match. Summing
conditional expectations over this bounded stopping time is legitimate
by inserting the indicators that each of the first N steps occurs.
Those indicators are known before the step's fresh letters are revealed.
If L=I+J and there are M matches, the total number of steps is L-M, so

    E[potential_final-potential_initial]
       >= r E[L-M] - E[M] = r E[L]-(1+r)E[M].

Let C be the finite range of the fixed potential. Its expected increment
is at most C. Rearranging and using L>=N gives

    E M >= (rN-C)/(1+r).

Every chosen match is part of a common subsequence of the consumed
prefixes, so M<=D_(N+1) samplewise, regardless of the policy's adaptive
choice of I,J. Combine this with the explicit bound for E D_(N+1),
divide by N, and let N tend to infinity. All error terms vanish, yielding

    r/(1+r) <= gamma/2, hence gamma>=2r/(1+r).

This completes the analytic implication used by the frozen potential,
without requiring a convergence rate for the search iteration.
