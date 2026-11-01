# Conservative frontier competitors for binary edit distance

Candidate and unrefereed. The numerical claim is only the rational bound in the
frozen artifact after its independent exact/Arb checker passes. This refines
Jack's canonical-alignment first moment and the inherited c91r2 pattern and
typicality method. It remains a first-moment argument; the new structural input
is a finite dynamic program containing competing paths with their own gaps.

## Canonical paths and inherited restrictions

Columns, numbered 0 through 7, are 00,11,01,10,D0,D1,I0,I1. A diagonal consumes
both coordinates and costs its mismatch; a gap consumes one and costs one.
Choose the alignment minimizing (cost, number of gaps, operation word), with
operation order diagonal < D < I. Every prefix and contiguous segment is
canonical for its consumed substrings. A cheaper replacement improves cost;
an equally cheap replacement with fewer gaps improves the second key. At equal
cost and gaps the column counts also agree, since columns=(symbols+gaps)/2,
so an earlier operation word remains earlier after splicing.

Retain the following rules from Jack and c91r2, all for this same canonical
choice:

1. Opposite adjacent gaps are forbidden: one diagonal is cheaper.
2. A substitution cannot follow a gap: moving the diagonal earlier is cheaper
   or ties cost/gaps with an earlier operation word.
3. The match ending a gap run has a symbol absent from that run: otherwise
   match its earlier occurrence and move the displaced symbols into gaps.
4. D-match-I and I-match-D are forbidden: two diagonals cost at most two and
   have fewer gaps at equality.
5. After substitution (a,b), a D run contains no b, and an I run contains no a:
   matching at that symbol removes the substitution cost.

The run memory records the literal last diagonal or last gap direction; the
set of letters in a current run; its forbidden substitution letter; and the
previous gap direction for one step after the run-ending match. Initially
memories are empty. Terminal runs may contain both symbols and need not exit.

The artifact lists labeled forbidden words, each checked to be noncanonical
by a forward dynamic program storing the entire canonical key. Exhaustiveness
or minimality of this bank is not required: omitting a forbidden word enlarges
the language. Its matcher stores the longest suffix that is a proper prefix
of a listed word, rejects every listed forbidden suffix, and combines this
with the run memory. All states accept. Original states are numbered breadth
first from the empty state, with columns visited in order 0..7.

Before adding the new frontier, this deterministic labeled graph is minimized
while preserving the literal run memory. Start with one color, repeatedly
color each state by (run memory, ordered eight destination colors, including
missing edges), and number colors by first appearance in the original BFS.
Stop when the color count stabilizes. Equal final colors have identical
accepted labeled continuations and run memory. No words are lost. The start
class is zero. The checker independently reconstructs and minimizes this graph.

## Frontier invariant

Let an actual alignment prefix consume X[0:i],Y[0:j], with actual cost C and
gap count J. Fix width W and score cap B. At each vertical frontier vertex
(i-r,j) and horizontal vertex (i,j-r), 1<=r<=W, retain either nothing or an
integer score c with this invariant:

* there is a genuine full-prefix alternative ending at that vertex;
* its cost minus C equals c;
* its gap count minus J is at most -r;
* its operation word has an earlier first differing operation than the actual
  prefix, already determined within both words.

Only the cost is retained; any extra gap savings are deliberately forgotten.
At each vertex keep the lowest eligible cost score. It still has a witness.
The endpoint, r=0, has no retained active witness on an accepted prefix.

A gap immediately seeds a pending alternative at the vertex before it. That
alternative must emit a diagonal as its first operation, so its first difference
is diagonal versus the actual gap. A suffix of q consecutive D gaps gives a
pending origin at (i-q,j), with cost and gap differences both -q; an I run is
symmetric. All pending origins within width are determined by the current
run length capped at W. Pending alternatives cannot take gaps before their
first diagonal. Once active, alternatives can use their own arbitrary gaps
subject to the conservative frontier restriction below.

A frontier witness lagging by r can append the remaining r gaps to reach the
actual endpoint. Its cost difference becomes c+r and its gap difference is
at most zero. Thus c+r<=0 proves a strictly smaller canonical key and safely
rejects the actual prefix. This includes tied cost/gaps because the alternative
already has an earlier first diagonal. Every selected canonical global path
therefore survives every rejection.

## Exact transition definition

Let V[r],H[r] be vertical/horizontal scores; missing entries and V[0],H[0]
are infinity. Negative-coordinate vertices are absent. Last W input symbols,
plus short-prefix lengths, suffice. Actual cost is subtracted once per whole
column. The following defines the conservative frontier language exactly.

For an actual diagonal consuming (a,b), let X_ext[k],Y_ext[k] be the kth bit
back after appending the new bit: index zero is the new bit, index one the
previous last bit. For 0<=r<=W, collect active vertical candidates

    V[q] + (q-r) + [X_ext[k] != b] - [a != b],
    r <= q <= W, r <= k <= q.

These append exactly one diagonal and q-r D gaps, placing the diagonal at
any position. Collect the symmetric horizontal candidates from H[q], pairing
a with Y_ext[k]. If the previous actual run is D, every q with
1<=q<=min(W,run length) and q>=r additionally gives the pending candidate

    -r + [X_ext[q] != b] - [a != b].

Here the diagonal must be first, pairing the oldest symbol. An I run supplies
the symmetric horizontal pending candidate. Take minima at each vertex;
merge the two endpoint minima. Active gap differences remain at most
-q+(q-r)=-r. Pending differences equal -r. Every cost is an actual witness cost.

For an actual D(a), take

    V_new[r] = V[r-1] - 1                       (1<=r<=W),
    H_new[r] = min over finite H[q] of:
        H[q] + q-r                             (r<=q<=W),
        H[q] + q-r-2 + [a != Y_old[q-1]]        (r+1<=q<=W).

The first horizontal option appends D followed by q-r I gaps. The second
appends a diagonal followed by q-r-1 I gaps. Their gap-count differences after
subtracting the actual gap are at most -r and -r-2 respectively. Set
V_new[0]=H_new[0]. An actual I uses the symmetric rule. The search implements
this update by a backwards recurrence; the independent checker enumerates
source positions using these formulas. Pending origins on an opposite run
cannot occur at an allowed gap step because adjacent opposite gaps are forbidden.

Reject if any new c+r<=0. Then drop every retained score c>B. All remaining
finite scores satisfy -r<c<=B; dropping scores only forgets witnesses. Update
input histories and the capped actual run length. Initial active frontiers
are entirely absent. The automaton is finite, but alternative witnesses can
persist for unboundedly many columns and contain multiple gaps. It is not a
length-W or length-L segment test. The parameters do not claim to include every
alternative of a geometric band.

The induction above proves the invariant for every retained score. Merging
requires no assumption about a common origin: future appended symbols and
cost increments depend on the current frontier vertex, and every retained
origin has already established an earlier first difference. The conservative
bound on gaps applies separately to each witness.

## Typical input strings and the first moment

For a binary string U, F_j(U), j=1,2,3, is the sum of spin products at lag j.
F_4(U) is the sum of products on every SLIDING consecutive four-symbol window.
Each has mean zero on uniform independent bits and variance at most |U|:
distinct terms are distinct Walsh monomials and are orthogonal, even when their
supports overlap. With H_j=F_j(X)+F_j(Y), define the typical event
|H_j|<=n^(3/4) for all four j. Chebyshev and a union bound give exception
probability at most 8/sqrt(n). In particular this exception is o(1), and no
exponential estimate is asserted for it.

Last max(W,4) bits of each input, with initial short lengths distinguished,
determine feature increments h_j in {-2,-1,0,1,2}. A gap emits only its consumed
coordinate's increment. Summing them on any path gives exactly H_j, regardless
of gap positions. Every complete new sliding window is emitted once.

For rational x>1, 0<t<1, z_j>0, weight a column consuming ell symbols and edit
cost c by

    2^(-ell) x^ell t^c product_j z_j^(h_j).

Let A be the complete transition matrix on the reachable product of the
minimized inherited graph, histories, capped run length, and frontier scores.
All states accept, including the empty state and terminal gaps. If a positive
vector v has Av<v, theta=max_i(Av)_i/v_i<1. Taking kappa with 1<=kappa*v gives
A^k*1<=kappa*theta^k*v, so the total all-path sum G is finite.

Every pair of length-n inputs with ed<=an has its selected canonical path in
this language. On the typical event its tilt factor is at least
exp(-n^(3/4)*sum_j |log z_j|). Consequently

    P(ed<=an and typical)
      <= G exp(-n*(2 log x+a log t)+n^(3/4)*sum_j |log z_j|).

If delta=2 log x+a log t>0 this tends to zero; adding the o(1) exception shows
P(ed<=an)->0. Nonnegativity implies liminf E[ed]/n>=a. Concatenation makes
expected distances subadditive, so Fekete supplies the limit C91 and C91>=a.
Unequal endpoints merely contribute extra positive terms to G. No boundary,
first-history or terminal-run factors are discarded.

## Frozen schema and independent exact verification

Schema `c91-conservative-frontier-v1` specifies L,W,B,K=4, the forbidden words,
expected original/minimized/product/weighted-class state counts, rational
x,t,z,a, and a positive potential. Forbidden words are [length,base8_word],
oldest digit first, retaining leading zeros by their length.

The product is numbered BFS from its empty state, visiting columns 0..7.
Weighted colors start at zero. Repeatedly form the sorted multiset of eight
(weight monomial, destination color) pairs, including missing-edge sentinels,
and assign colors by first appearance in full BFS order until the count
stabilizes. This defines the coordinates of the compressed potential. Search
uses hash refinement; the independently written checker sorts state signatures.
It reconstructs every full reachable row and checks that row using its own
computed colors. Thus neither a search graph nor a search partition is trusted.
Weighted coloring is a compression of the potential; the full rows still pass.

The potential is either a list of positive integers, or base64 of little-endian
IEEE binary32 bit patterns. In the latter case the checker rejects nonpositive,
nonfinite and subnormal values and interprets each bit pattern EXACTLY as
m_i*2^(e_i). With e_min=min e_i, it uses the positive integer
v_i=m_i*2^(e_i-e_min). No floating arithmetic enters an inequality. Encoding
search approximations as dyadic rationals does not certify them; the following
strict integer checks do.

For x=p/q, t=r/s, z_j=u_j/v_j, choose

    D = 4 q^2 s product_j u_j^2 v_j^2.

An allowed edge with feature vector h has integer coefficient

    match:         p^2 s product_j u_j^(2+h_j) v_j^(2-h_j),
    substitution:  p^2 r product_j u_j^(2+h_j) v_j^(2-h_j),
    gap:           2pqr  product_j u_j^(2+h_j) v_j^(2-h_j).

For EVERY full reachable source state, the checker requires the sum of these
coefficients times its destination potentials to be strictly less than D times
its source potential. It checks positive entries, exact counts and complete
reachability, and independently verifies every forbidden word. Exact unsigned
base-2^32 arithmetic uses at most 1536 bits with overflow rejection; this covers
all allowed 64-bit parameters and potentials (at most 1283 bits per row).
A separate Python test compares its multiplication, addition, subtraction and
comparison against Python integers on 10,000 cases through 1344 bits. The
wrapper independently checks delta>0 and the threshold with 256-bit Arb balls.

The frozen artifact, rather than mutable search files, is the proof object.
The checker imports no generator, optimizer, inherited verifier, edge list or
partition. Implementation independence means separately written code by the
same AI agent; this round's new argument has not received independent external
review or human refereeing. The completed review_c91r2 PASS covers the inherited
bound, not this extension.
