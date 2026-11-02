# Typicality and unbounded one-gap tests for C91

Candidate and unrefereed. This extends the earlier sweep1 job's
canonical-alignment argument; it does not claim external review or priority.

The alphabet of columns, in order, is 00,11,01,10,D0,D1,I0,I1.
Choose the unique alignment minimizing (edit cost, gap count, operation word),
with diagonal < D < I. Every segment of it has the same canonical property:
replacing a segment with a better alignment improves the corresponding global
key. Equal consumption and gap count imply equal column count, making the
lexicographic replacement argument valid. We retain the five run rules and
forbidden noncanonical segments described in the inherited proof. Each listed
forbidden word is checked independently; completeness of that list is not
necessary. Completeness of the accepted automaton is necessary.

For completeness, the retained run rules and their common-canonical-choice
justifications are:

1. Adjacent opposite gaps are forbidden: one diagonal costs at most one
   instead of two.
2. A substitution cannot follow a gap: move the diagonal earlier, giving
   smaller cost or equal cost/gaps and an earlier diagonal.
3. A match ending a gap run has a symbol absent from that run: otherwise
   match at its earlier occurrence and move the displaced symbols into gaps,
   preserving cost/gaps and improving the operation word.
4. D-match-I and I-match-D are forbidden: two diagonals cost at most two,
   and at equal cost have fewer gaps.
5. After a substitution (a,b), a D run contains no b and an I run contains
   no a: matching at that symbol removes the substitution cost.

The deterministic memory stores the last diagonal or gap direction; the set
of letters in the current gap run; the banned letter if that run follows a
substitution; and the preceding run direction for one step after its ending
match. Opposite adjacent gaps are rejected. A diagonal after a run must be
a match whose letter is absent from the stored set, and it remembers the old
direction for one step. The next gap cannot have the opposite direction;
a second diagonal clears that memory. Within a run, update the letter set
and avoid any substitution ban. Initial memories are empty. Terminal runs
may contain both letters and never need to exit to a match.

## 1. Arbitrarily long one-gap tests

Consider a segment starting with D(a0), followed by k >= 1 diagonals
(a1,b0),...,(ak,b[k-1]). Compare it with the alignment whose k diagonals are
(a0,b0),...,(a[k-1],b[k-1]), followed by D(ak). Define

    S = sum(i=0..k-1) [a_i != b_i]
        - sum(i=1..k) [a_i != b_(i-1)].

Both paths have one gap. If S <= 0, the alternative is cheaper or has the
same cost/gap count and an earlier diagonal, so the original is noncanonical.
If the segment next takes I(bk), the gap-free comparison has cost difference

    S + [ak != bk] - 2.

If this is <= 0, it is cheaper or has equal cost and fewer gaps, so again
the original is noncanonical. Interchange X and Y for the analogous I test.

A deterministic tracker stores direction, the most recent symbol in that
direction, and S. Each new gap starts the tracker at S=0; a diagonal updates
S by its shifted mismatch minus its actual mismatch and updates the symbol.
Reject a diagonal if S <= 0. At an opposite gap reject if the second
displayed difference is <= 0, and otherwise start a new tracker at that gap.
A same-direction gap also starts a new tracker. If S exceeds a fixed cap B,
drop the tracker until the next gap. Dropping it forgets possible
noncanonicality and therefore only enlarges the accepted language. Every
rejection has an explicit better alignment of a contiguous segment, regardless
of the length of its diagonal run. Hence all canonical global alignments survive.

### General bounded-lag competitor (the width-two extension)

For every candidate segment starting with a D, retain a pure-diagonal
alternative followed by r residual D columns, where r is the difference
between its consumed X and Y lengths. Its diagonal part pairs the first
min(length X,length Y) symbols of the two segment substrings. The r residual
symbols are exactly the last r X symbols. Store S = alternative cost minus
actual segment cost. The initial D has r=1,S=0. While r>0:

* A D appends an X symbol, r increases by one, and S stays fixed.
* A diagonal (a,b) pairs b with the oldest of the r buffered X symbols in
  the alternative. Thus S increases by [buffer_oldest != b]-[a != b],
  while the buffer drops its oldest symbol and appends a.
* An I(b) replaces a residual D by a diagonal. Thus S increases by
  [buffer_oldest != b]-2 and r decreases by one.

After a diagonal or opposite gap, reject if S<=0. The alternate segment is
then cheaper, or has equal cost and no more gaps. If it has fewer gaps it
improves the second key; if gap counts agree, it begins with a diagonal
instead of D and improves the third key. At these rejection points at least
one Y symbol has been consumed, so that first diagonal exists. If r becomes
zero without rejection, drop that competitor. Drop competitors when r>W or
S>B as well. Start a new competitor at every D, and run the symmetric
construction starting at every I.

All competitors with the same current direction and r have the same residual
buffer, namely the last r input symbols. Their future S increments therefore
agree. Keeping only the smallest S is sufficient to represent every retained
candidate relevant to a rejection. After merging, dropping a tracker at the
caps can only forget candidate improvements. There are W scores per direction,
each absent or in {0,...,B}. Histories retain four bits, sufficient for W<=4
and the typicality features. This is finite memory and applies to arbitrarily
long segments, including segments with multiple interspersed gaps. It is not
a length-W window restriction.

## 2. Typical input correlation constraints

For a binary string U, define F_j(U) as the sum of +1 for equal and -1 for
unequal symbols at lag j, for j=1,2,3. Define F_4(U) as the sum over consecutive
four-symbol blocks of (-1)^(sum of the four bits). Each has mean zero on
independent uniform bits. For every fixed j, F_j(U)/n -> 0 in probability.
One elementary proof partitions terms into finitely many residue classes with
disjoint supports and applies the weak law to each class. Equivalently, the
variance is O(n), since only O(n) pairs of terms have overlapping support.

Write H_j=F_j(X)+F_j(Y). For each fixed epsilon>0, the event T_n that
|H_j| <= epsilon*n for all used j has probability tending to one. It is
enough to use j=1,2; the four-feature variant additionally uses lag 3 and the
four-spin statistic. These statistics depend only on the consumed strings,
not on the alignment. Initial short prefixes contribute no terms. On each
column an input history of at most four bits determines the integer increment
h_j in {-2,-1,0,1,2}. Gaps update only the history of the consumed coordinate.

Give a column consuming ell symbols and with edit cost c the rational weight

    2^(-ell) x^ell t^c product_j z_j^(h_j),

where x>1, 0<t<1, and each z_j>0. If a positive vector V satisfies AV<V,
the sum G over all accepted paths is finite. Indeed set
theta=max_i (AV)_i/V_i<1 and kappa=max_i 1/V_i. Then
A^k 1 <= kappa*theta^k V, so G <= kappa*V_start/(1-theta).
Every pair of length-n strings with ed<=a*n
has an accepted canonical alignment. On T_n its correlation factor is at least

    exp(-epsilon*n*sum_j |log z_j|).

Consequently

    P(ed<=a*n and T_n)
      <= G exp(n*(-2 log x - a log t + epsilon*sum_j |log z_j|)).

If 2 log x + a log t > 0, choose a fixed sufficiently small epsilon>0 so
the exponent is negative. Adding P(not T_n)=o(1) proves P(ed<=a*n)->0.
It follows that liminf E[ed]/n >= a. Subadditivity supplies the known limit.
This is a typical-set refinement of the first moment; it is not an
unjustified assertion that all strings have exactly uniform block frequencies.

## 3. Exact verification obligations

The frozen artifact must specify rational x,t,z_j,a, a positive integer
vector, the list of noncanonical forbidden words, B, and the history rule.
An independently written verifier must check every listed word by an exact
canonical DP; reconstruct every reachable allowed transition of the pattern,
run-rule, tracker, and input-history product; ensure complete state coverage;
check every row of AV<V using rational/integer arithmetic; and check
2 log x+a log t>0 with rigorous Arb balls. Search eigenvalues, search
minimization, and floating optimization are not proof evidence.

All states are accepting, including the empty path and terminal gaps. Input
lengths need not agree during counting; the probability argument uses just
the subset consuming n symbols in each coordinate. No boundary transitions
or first/last input correlation terms are omitted.

## 4. Frozen schema and reconstruction

Schema `c91-typical-strip-v1` is a gzip JSON object. `L,W,B,K` specify the
maximum listed pattern length, competitor width, score dropout cap, and number
of typical statistics (2 or 4). `x,t,bound` and each element of `z` are
positive numerator/denominator pairs. `forbidden_patterns` consists of
`[length,base8_word]` pairs; base-8 digits are the eight labeled columns above,
oldest first. Leading zero columns are retained by length. `vector` contains
positive integers, with an arbitrary common denominator omitted. The status
is explicitly candidate and unrefereed.

First reconstruct the pattern/run-rule automaton. The pattern state is the
longest suffix which is a proper prefix of any listed word; reject appends
having any forbidden suffix. Combine it with the run memory above. Number
reachable states breadth first, starting with empty prefix and empty run
memory, and visiting outgoing column labels in order 0 through 7. This defines
the original-state IDs. `original_states` is an asserted count, independently
recomputed and checked.

Next combine the original states with the two last-four-bit histories and
the W competitor scores in each direction. Histories initially are empty;
all scores are absent. Apply exactly the tracker update in section 1, including
the specified dropout. Number this product by the same breadth-first rule.
Its vector entries are in this order. The verifier discovers and checks all
states and transitions itself and requires the final count to equal the vector
length. The certificate contains no editable edge list whose omissions could
escape the reconstruction.

For x=p/q, t=r/s, z_j=u_j/v_j, choose the integer common denominator

    D = 4 q^2 s product_j (u_j^2 v_j^2).

For an allowed edge with increments h_j, its integer coefficient is

    match:        p^2 s product_j u_j^(2+h_j) v_j^(2-h_j)
    substitution: p^2 r product_j u_j^(2+h_j) v_j^(2-h_j)
    gap:          2pqr  product_j u_j^(2+h_j) v_j^(2-h_j).

All exponents are nonnegative because each column changes each statistic by
at most two. The verifier requires the sum of these coefficients times the
destination vector entries to be strictly less than D times the source entry,
for every reachable state. Python integers give exact arithmetic. A separate
256-bit Arb test checks the exponent. An additional rational-only logarithm
series check is supplied as a cross-check.

The candidate's mathematical reduction, tracker proof, and typical-set
argument remain unrefereed. The independently written implementation is by
the same AI agent; the separate review of the inherited certificate did not
review these new contributions.
