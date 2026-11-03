# Candidate, unrefereed four-letter LCS lower-potential certificate

This is a continuation of Leandre Jack's public construction in PR #272,
using Lueker's finite lookahead method (2009, Lemma 2.3), in the
k-letter form of Kiwi and Soto (2009), also used by Rosenfeld (2024).
Here k=4, the four-letter setting studied by Kiwi and Soto. The operator,
h=9 and class set are the same as in #272. The gain comes from refining
the fixed-point unit from 2^-27 to 2^-30. This is a precision refinement
of Jack's construction, not a new method.
More fixed-point bits do not change the mathematical operator. No novelty
judgment is made. A certificate value is claimed only when the frozen
metadata has a complete separate exact-check receipt.

## Model and finite operator

Let A and B be independent infinite sequences, each letter uniform on an
alphabet of k letters. A state (a,b) consists of the next h letters in each
sequence. Reading beyond a state always reveals fresh independent uniform
letters. Write w(a,b) for a bounded real potential. Define T(w) as follows.
If a[0]=b[0], consume both first letters, match them (reward one), append an
independent letter to each word, and set

    T(w)(a,b) = 1 + (1/k^2) sum_{c,d} w(a[1:]c,b[1:]d).

If a[0]!=b[0], discard one of the two first letters and choose the action
with the larger mean continuation potential:

    T(w)(a,b) = max((1/k) sum_c w(a[1:]c,b),
                   (1/k) sum_d w(a,b[1:]d)).

A finite witness is a function satisfying T(w)(a,b)>=w(a,b)+r for EVERY
state. The checker uses precisely these literal sums; it does not use the
producer's intermediate F-space, convergence criterion, or rounded drift.

## Why this implies gamma_k >= 2r/(1+r)

This is Lueker's Lemma 2.3, re-proved below for general k, including
the Kiwi-Soto four-letter setting.

Assume 0<r<1. Use the potential-maximizing action above on each mismatch,
and always match equal first letters. At a mismatch step one letter is
consumed and conditional expected potential increment is at least r.
At a matched step two letters are consumed and conditional expected
potential increment is at least r-1. After a bounded stopping time with
L consumed letters and M matches, summing conditional expectations gives

    E[w_final-w_initial] >= r E[L] - (1+r) E[M].

This identity follows also by writing the number of steps as L-M.
Stop the first time total consumption is at least N. Each step consumes
one or two letters, so N<=L<=N+1 and at most N steps occur. The potential
range is a fixed finite constant C, independent of N. Consequently

    E[M] >= (r N-C)/(1+r).

Every chosen match is a common subsequence of the consumed prefixes.
Thus M<=D_{N+1}, where D_n is the maximum LCS(A[:i],B[:j]) over i+j<=n.

For completeness relate D_n to the usual square-string constant gamma_k.
Put a_m=E LCS(A[:m],B[:m]). Concatenation gives a_{m+n}>=a_m+a_n,
and 0<=a_m<=m, hence a_m/m converges to its supremum gamma_k. For any
nonnegative i,j, concatenate two independent rectangular instances with
lengths (i,j) and (j,i). Their separate common subsequences concatenate,
so a_{i+j}>=2 E LCS(A[:i],B[:j]) by symmetry. Hence

    E LCS(A[:i],B[:j]) <= gamma_k (i+j)/2.

Changing any single letter changes LCS by at most one. The bounded-
differences inequality for i+j independent letters therefore bounds an
upper deviation t by exp(-2t^2/(i+j)). A union bound over at most (n+1)^2
pairs i+j<=n, followed by integration of this tail, gives

    E D_n <= gamma_k n/2 + O(sqrt(n log(n+2))).

Combine the last estimate with E M >= (r N-C)/(1+r), divide by N,
and let N tend to infinity. This yields gamma_k/2>=r/(1+r), as claimed.
No asymptotic convergence speed is needed in a certificate.

## Symmetries and complete enumeration

T commutes with simultaneous alphabet permutation and swapping the two
words. It suffices to assign w to the orbits under S_k times the two-word
swap. A simultaneous alphabet orbit has a unique restricted-growth word:
read a followed by b and rename first occurrences 0,1,2,... . Its length
is 2h and it uses at most k symbols. The separate checker enumerates every
such restricted-growth word in lexicographic order, computes the rank of
the swapped word after its own renaming, and marks the smaller rank as
the representative. Every rank maps to that representative. No action or
fresh symbol is omitted when the literal operator is evaluated.

The total number of pair orbits is checked using a separate Burnside formula:

    classes = (1/(2 k!)) sum_{pi in S_k}
              (fix(pi)^(2h) + fix(pi^2)^h).

The first summand counts pairs fixed without swap. With swap, the first
word determines the second and each of its h letters must be fixed by
pi^2, giving the second summand. The checker verifies the total class
count, enumerates all representatives, and checks every inequality.

## Integer scale and safety

The decoded witness consists of one nonnegative uint64 value W per orbit,
in increasing representative-rank order, with w=W/2^SHIFT. On a match,
check

    k^2*2^SHIFT + sum_{c,d} W(next) - k^2 W(current)
        >= k^2*2^SHIFT*r.

On a mismatch, check k*max(sum_left W,sum_right W)-k^2 W(current) against
the same right side. These are EXACT integer comparisons. The metadata
requires the right side to be integral. W<=2^50, k<=4, SHIFT<=35, and
nonnegative W ensure every sum, product and signed difference fits int64
(the largest positive sum is at most 16*2^50+16*2^35<2^55).

The index uses uint32 orbit identifiers and rejects class counts >=2^32.
Counts, lengths, ranks, file byte length, all visited representatives and
minimum drift are checked. Parallel enumeration chunks end on multiples
of 64, so writes to bitset words do not race. Threads change no arithmetic.

## Small procedural artifact

The raw h=9 vector is many gigabytes. To respect the retention limit, the
frozen artifact may encode it as an exact finite integer program: credited
producer source plus a fixed sequence of warm-start parameters and SHA256
for every decoded intermediate. The separately written (same agent) wrapper can expand this
recipe in an empty scratch directory, checks exact decoded bytes against
the normative metadata hash, then runs the separately written literal
operator checker on that complete vector. Generator claims and its
stopping logs are not trusted. A frozen receipt must describe the complete
check of all decoded classes. Reconstruction costs substantial RAM and
CPU; it is not a small-data claim about the uncompressed vector.

Any modified vector, operational metadata or decoder must be rechecked.
This release changes prose, source comments and their integrity hashes
only; REPRODUCE.md maps historical receipt hashes to .orig files.
It does not assert a new complete h=9 replay. The final
packet must include controls rejecting an increased drift and altered
bytes. The headline value and public comparison are recorded separately
only after verification and a fresh public-source audit.

## References and source credit

- Leandre Jack, [source linked by PR #272, bb3b815](https://github.com/leandrejack-afk/chvatal-sankoff-bound/tree/bb3b815/lower).
- George S. Lueker, Improved bounds on the average length of longest common subsequences, J. ACM 56(3), Article 17 (2009), [Lemma 2.3](https://mathematicaster.org/teaching/lcs22/lueker_lcs.pdf).
- Marcos Kiwi and José Soto, On a speculated relation between Chvátal-Sankoff constants of several sequences, Combinatorics, Probability and Computing 18 (2009), [doi:10.1017/S0963548309009900](https://doi.org/10.1017/S0963548309009900).
- Matthieu Rosenfeld, Upper bounds on the average edit distance between two random strings (2024), [arXiv:2407.18113](https://arxiv.org/abs/2407.18113).
