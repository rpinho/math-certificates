# C91: witnessed competing prefixes and a finite exact certificate

**Candidate and unrefereed C91 >= 0.263561 = 263561/1000000.**
The frozen artifact passed the independently written exact/Arb checker in
1098.60 seconds. Its gain over 0.259407 is exactly
2077/500000 = 0.004154 > 0.002. The result is a first moment with additional competing-path constraints,
with no priority or optimality claim.

The decisive point has L=12, W=3, absolute cost cap B=1 and four inherited
input tilts. The bank contains 136,974 explicitly listed noncanonical words.
Counts are base 262,713 -> 103,267; standalone tracker 11,028,253 -> 5,372,908;
reachable factored product 65,623,319; potential classes 9,409,061. All
268,855,220 edges participate in the exact full-row check. The 30,801,887-byte
artifact SHA-256 is
`2b408738acf654f6a0763d56a7a3283259310eff4c5e4f6cc72afc9993432302`.

All parameter denominators are 10^9: x numerator 1145519853, t numerator
356670822, and z numerators (1041421066,1016222687,1004130270,1002178291).
The frozen Arb threshold is 0.26356197613919511484993636936896579346...;
the exponent at the claimed rational bound is
1.0063428841284675404621617574378537... x 10^-6 > 0.

An earlier fallback at 0.259510 also passed, using the inherited round-3
frontier with a larger sampled forbidden bank. Only the stronger final
artifact is needed for the retained headline claim.

C91 is lim E ed(X_n,Y_n)/n for independent uniform binary strings of length n,
with unit-cost substitution, insertion and deletion. We build on Leandre
Jack's canonical first moment, the inherited c91r2 forbidden-pattern and
input-typicality construction, and c91r3's competing-prefix frontier. See
PRIOR_ART.md for primary references, the live-table checks and public PRs.

## Canonical alignments and the inherited language

Columns 0..7 mean 00,11,01,10,D0,D1,I0,I1. A diagonal consumes two symbols;
a gap consumes one. Costs are 0 for a match and 1 otherwise. For each pair
of input strings choose the alignment minimizing, in order, cost, number of
gaps, and operation word, with diagonal < D < I. This defines one labeled
column word for each pair. Every prefix and contiguous segment is canonical
for its own consumed substrings. A better segment could be spliced into the
whole path. At tied cost and gaps, its column count is also tied, because
columns=(consumed symbols+gaps)/2; hence the first different operation is
preserved by splicing, including nested segments and boundaries.

The following five restrictions hold for this choice.

1. Opposite adjacent gaps are impossible: one diagonal has cost at most one,
   versus two for the gaps.
2. A substitution cannot follow a gap. Replace D(a),S(b,c) by S(a,c),D(b):
   cost decreases or ties, gaps tie, and the diagonal moves earlier. The
   insertion case is symmetric.
3. The symbol of the match ending a gap run is absent from that run. Otherwise
   match its earlier occurrence in the run and move the displaced symbols
   into gaps; cost and gaps tie and a diagonal moves earlier.
4. D-match-I and I-match-D are impossible. Two diagonals cost at most two;
   at equal cost they have fewer gaps.
5. After S(a,b), a D run contains no b and an I run contains no a. Matching
   that occurrence instead removes the substitution cost while moving the
   displaced first symbol into the gap run.

The literal run memory stores the last diagonal or gap direction, symbols
in the current run, its forbidden substitution symbol, and the previous
run direction for one step after the ending match. The initial memory is
empty. All states accept, including terminal gaps containing both symbols.

The frozen artifact lists additional noncanonical labeled words. Each is
independently checked by a forward edit DP storing the entire canonical key.
Every such word is forbidden by the segment argument. The bank need not be
exhaustive or minimal. Later search branches omit many inherited words after
testing the standalone tracker as a heuristic resource tradeoff. Omitting
constraints always preserves canonical-path inclusion; no redundancy claim
is required, and the resulting entire matrix is checked independently. The matcher stores the longest suffix that is a proper
prefix of a listed word and rejects any listed suffix. Its product with run
memory is enumerated breadth first, columns 0..7 in order. The inherited
minimization preserves run memory and ordered labeled continuations. Colors
start equal and are repeatedly refined by (run memory, eight destinations),
with missing edges distinguished; colors are numbered by first appearance.
Stable refinement loses no word. The start class is zero.

## Compact upper keys at a trailing frontier

Let the actual prefix end at (i,j), with cost C and gap count J. For each
1<=r<=W, a vertical entry refers to (i-r,j), a horizontal entry to (i,j-r).
Each retained triple (c,g,t), t in {-1,+1}, has a witness alternative with
g either an integer or infinity. Infinity means that gap-count information
has been forgotten while the cost witness is retained. The invariant is:

- exactly those consumed full input prefixes;
- cost minus C exactly c;
- actual gap difference d at most g;
- a first differing operation established inside both words;
- if g is finite, d=g and t=-1, that first difference is earlier than the actual path.

There is no order promise when t=+1. When d<g, order is immaterial to the
upper key: a strict gap advantage suffices at tied cost. This conditional
order invariant is the substantive saturation change from the round-3
frontier. It does not claim that every t=-1 witness literally begins earlier.

Closing a lag-r witness with r gaps reaches the actual endpoint. It proves
the actual prefix noncanonical if c+r<0; or c+r=0 and g+r<0; or
c+r=g+r=0 and t=-1. In the last case either d<g, giving strictly fewer actual
gaps, or d=g and the established first difference is earlier. Such a first
difference persists after closure and after splicing the actual suffix.

Check every candidate completion for rejection before any dropout. Then
forget candidates with c>B, and do not retain endpoint r=0. A second
resource variant uses a completed-cost cap c+r<=Q instead of c<=B; Q is
serialized in the B field under its distinct schema. If g+r>2, replace
g by infinity and t by +1; an infinite bound stays infinite under extension.
This loses gap information but preserves a genuine exact cost witness. For
r>=1, if g<-r, replace (g,t) by (-r,-1). The true d is strictly below the
new bound, so the conditional order invariant holds. Otherwise g remains.
At each vertex retain the least (c,g,t) in lexicographic order. This selects
one genuine witness; no assumption that it is best among all paths is made.
Omitting or forgetting competitors only enlarges the accepted language.

Gap parity gives g+r even, including after saturation. On an accepted prefix
c>=-r; after dropout c<=B (or c+r<=Q), and g is -r, -r+2 or infinity. The frontier is finite. Its
width bounds the trailing frontier, not how long a witness may persist.

## Exact witness extensions and origins

All formulas below append real edit paths to an existing witness. Changes
are relative to the new actual prefix, after subtracting its cost and gaps
once per whole column. The order tag is unchanged by extension. Its invariant
holds because both gap differences receive the same increment, and an
established first differing operation remains established. Every candidate
is then processed by the rejection, cap, saturation and minimum rules above.
The horizontal case interchanges X/Y and D/I.

For a new actual diagonal (a,b), let e=[a!=b] and let X_ext[k] be the kth bit
back after appending a, with k=0 the new bit. From vertical lag q to vertical
lag r<=q, append one diagonal and q-r D gaps, placing the diagonal anywhere.
For every k in [r,q] this gives

    c_new = c + q-r + [X_ext[k]!=b] - e,
    g_new = g + q-r.

The consumed X segment has q-r+1 symbols and the consumed Y segment one,
so this is a genuine path at every placement. A vertical lag q can also
append q+1 D gaps to the new horizontal lag 1:

    c_new = c+q+1-e,   g_new = g+q+1.

Also, from lag q<W, append only I(b) to reach new vertical lag q+1:
its relative changes are (1-e,1). The horizontal case appends D(a).
This lag-growth route was absent from the earlier compact diagnostic.

No candidate from a nonexistent source or negative input coordinate is
created. Histories and retained witness coordinates make those cases absent.

For an actual D(a), a vertical source at lag q can reach any lag
0<=r<=min(W,q+1) by q+1-r D gaps, with relative changes (q-r,q-r).
The r=q+1 case simply pauses. For a horizontal source at lag q>=r, append D
and q-r I gaps, giving changes (q-r,q-r). If q>=r+1, alternatively append
one diagonal at any position among the q-r consumed Y symbols, with
q-r-1 I gaps before and after it, giving, for every k in [r,q-1],

    delta_cost = q-r-2 + [a!=Y_old[k]],
    delta_gaps = q-r-2.

These consume exactly the required prefixes. After generating a column, close
each fresh frontier under trailing gaps: a lag-q candidate can reach any
r<q by q-r gaps of the lagging string, adding (q-r,q-r) to its already-new
relative scores. Process q in descending order. This closure appends real
paths and is processed by the same cap and saturation rules. Endpoint
candidates are checked and then forgotten; there is no retained source at r=0.

Pending origins are provided by suffixes of the current actual gap run.
Before q D gaps, the actual prefix is a real pending path at (i-q,j), with
relative cost and gaps (-q,-q). On the next actual diagonal it may emit its
first diagonal and then q-r D gaps, for 0<=r<=q. Its tag is -1 because a
diagonal precedes the actual gap. Its new cost is
-r+[X_ext[q]!=b]-e and gap difference -r. An I run is symmetric. Capped run
length and the last W symbols identify all pending origins used here.

There are three additional origins/routes beyond the round-3 eligible
frontier:

- At a new actual diagonal, the actual prefix before it may instead append
  I to reach vertical lag 1, or D to reach horizontal lag 1. Each gives
  (c,g,t)=(1-e,1,+1): an alternative gap follows the actual diagonal in order.
- Before q D gaps, append I on the next actual diagonal to reach vertical
  lag q+1, with (1-q-e,1-q,+1). Before q I gaps, append D to reach horizontal
  lag q+1 with (1-q-e,1-q,-1), since D<I. Use only q+1<=W.
- The active cross-corner all-gap route above lets an earlier witness incur
  one normalized pair of gap debt and later recover it.

These constructions establish the upper-key invariant by induction from
empty histories, zero run length and absent active frontiers. Every rejection
has a strictly better full-prefix canonical key. Therefore every globally
selected canonical alignment survives the entire language, for every pair
of input lengths. The proof asserts soundness, not completeness of band DP.

For a literal refinement of round 3's accepted language, define
L_round4 = L_round3 intersect L_certified. Every selected canonical word
belongs to both languages. Its word weight is the same in each, since the
features depend only on the emitted inputs. The total weighted path sum of
L_round4 is at most the verified finite sum for L_certified. Thus the same
bound holds for an accepted language contained in the inherited one, without
materializing that larger intersection. The checker deliberately certifies
the enclosing language, which is sufficient for this refinement as well.

## Minimize the tracker before intersecting the word matcher

First build the reachable standalone tracker with run rules and histories,
without the forbidden bank. All states accept. Minimize it by ordered
signatures: for each of the eight columns record a missing-edge sentinel,
or (weight monomial, destination color). A weight monomial records column
kind and the four feature increments defined below. Colors start equal;
refine to stability and number by first appearance in original BFS order.

Stable equal colors have identical allowed labeled continuations and the
same feature increments on every continuation. Induction on word length
proves equality of their weighted labeled languages. Histories may merge
only when this equality holds. The checker uses sorting, independently
reconstructs every original tracker row, and checks every class member
against its representative after refinement.

Take the reachable product of this minimized tracker and the minimized
forbidden-word matcher, visiting columns 0..7 in order. An edge exists iff
both components permit it; it inherits the tracker's feature increments.
Thus the product accepts precisely the intersection of two languages
containing every canonical alignment and computes the same path weights as
the unminimized tracker. Start states and all terminal states are retained.

A second weighted minimization, now using sorted MULTISETS of
(weight monomial, destination color), only compresses the potential vector.
It may forget labels but preserves multiplicity. Its colors are numbered by
first appearance in the full product BFS. The checker reconstructs these
colors and checks every full product row, so neither a search graph nor a
search partition is trusted.

## Typicality and the first moment

For a binary string U write s_i=(-1)^U_i. Define F_j(U), j=1,2,3, by summing
s_i s_(i-j) over all valid lag-j pairs. Define F_4(U) by summing the product
of spins on every SLIDING consecutive four-symbol window. Each has mean zero
and variance at most |U|: distinct summands are distinct Walsh monomials and
are orthogonal, including overlapping windows. For H_j=F_j(X_n)+F_j(Y_n),
Var H_j<=2n. Chebyshev and a union bound show

    P(any |H_j|>n^(3/4)) <= 8/sqrt(n) = o(1).

Last max(W,4) symbols and short-history lengths determine each new feature
increment h_j. A gap emits its consumed string's increment and a diagonal
emits both. Thus summing increments along ANY complete alignment gives H_j;
all sliding windows are counted once, independent of the alignment.

For rational x>1, 0<t<1 and z_j>0, weight a column consuming ell symbols
and having cost k by

    2^(-ell) x^ell t^k product_j z_j^(h_j).

Let A be the full product transition matrix, summing all labeled edges.
Suppose a positive vector V satisfies AV<V strictly in every row. Let
θ=max_i(AV)_i/V_i<1. Choose κ with 1<=κV componentwise. Then
A^m 1<=κ θ^m V; hence the all-path sum G from the empty start is finite.
This includes the empty word, unequal endpoints, initial histories, terminal
gap runs and dead ends. No endpoint or terminal factor is discarded.

Each ordered length-n input pair has its selected canonical word in the
language. Distinct pairs have distinct labeled words. If ed<=an and all
|H_j|<=n^(3/4), its weight is at least

    4^(-n) x^(2n) t^(an)
      exp(-n^(3/4) sum_j |log z_j|).

Overcounting other accepted words only increases G. Therefore

    P(ed<=an and typical)
      <= G exp(-n(2 log x+a log t)+n^(3/4) sum_j |log z_j|).

When δ=2 log x+a log t>0, this tends to zero. Adding the o(1) atypical
probability shows P(ed<=an)->0 and liminf E ed/n>=a. Concatenation makes
E ed(X_n,Y_n) subadditive, so Fekete supplies C91 and C91>=a.

## Frozen exact verification

The schemas distinguish the compact diagnostic, band extensions, and the
retained-cost version `c91-factored-band-infinite-v1` (or
`c91-factored-band-infinite-completion-v1` with completed-cost cap Q): L,W,B,
K=4, the forbidden bank, original/minimized base and tracker counts,
product and potential-class counts, rational x,t,z,a and a positive potential.
Only the frozen artifact is a proof object; search outputs are diagnostics.
Words use [length, base8_word], oldest column first, preserving leading zeros.
The checker independently rebuilds every graph from these specifications.

The potential may be stored in ordinary byte order or by an invertible
transpose into four byte planes; the checker reverses this using integer
byte operations. A normal positive binary32 bit pattern denotes EXACTLY m*2^e with the implicit
mantissa bit included. Zero, negative, subnormal and nonfinite entries are
rejected. Remove the smallest common power of two to obtain positive integer
potentials V_i, checked to fit 64 bits. Floating-point search and export give
these numbers no validity; the following strict integer checks do.

Write x=p/q, t=r/s, z_j=u_j/v_j, and let

    D=4 q^2 s product_j u_j^2 v_j^2.

For feature vector h, the integer edge coefficients with denominator D are

    match:        p^2 s product_j u_j^(2+h_j) v_j^(2-h_j),
    substitution: p^2 r product_j u_j^(2+h_j) v_j^(2-h_j),
    gap:          2pqr  product_j u_j^(2+h_j) v_j^(2-h_j).

The checker requires, in EVERY complete reachable product row, the sum of
coefficients times destination potentials to be strictly below D times its
source potential. It verifies all forbidden words, reachability and counts,
positive potentials, both partitions, all feature increments and multiplicity.
Unsigned base-2^32 arithmetic uses 1536 bits with overflow rejection; the
universal pre-rejection row-size upper bound for permitted 64-bit parameters
is 1284 bits. Finally 256-bit Arb balls independently prove δ>0.

The old-frontier fallback at 0.259510 uses exactly the separately written
round-3 checker with the B=0 interface condition repaired, and the same
canonical/typicality/positive-vector argument. Its new sampled forbidden
words are all checked from the frozen bank. No sampling estimate is used as
proof. Separate new-frontier and factoring code checks the compact language.
Implementation independence here means separately written code by the same
AI agent, with inherited audited arithmetic/base machinery; it is not an
external human review. All round-4 results remain candidate and unrefereed.

## How far a complete canonical-window hierarchy can reach

This statement concerns ALL noncanonical words through length L, with L and
integer precision unbounded. It does not assert convergence of the tested
fixed-L, bounded-frontier family or of the 64-bit certificate encoding.

Let C=C91 and fix a<C. For independent strings of lengths i,j put m=i+j
and D_ij=ed(X_i,Y_j). Concatenate independent pairs of lengths (i,j) and
(j,i). Symmetry and subadditivity give

    Cm <= E D_(m,m) <= 2 E D_ij.

Exposing the m independent input bits gives Doob martingale differences
whose conditional ranges have length at most one: changing one bit changes
edit distance by at most one. Hoeffding's conditional mgf lemma, iterated,
gives for λ>0

    E exp(-λ D_ij) <= exp(-λ E D_ij+λ^2 m/8)
                   <= exp((-λ C/2+λ^2/8)m).

Choose a<b<C, 0<λ<4(C-b), t=exp(-λ), x=exp(λ b/2), and
ε=λ(C-b)/2-λ^2/8>0. Then 2 log x+a log t=λ(b-a)>0.
Let Z_k be the total weight 2^(-m)x^m t^cost of all canonical k-column
words. Each corresponds uniquely to an input pair and k<=m<=2k, hence

    Z_k <= sum_(m=k)^(2k) (m+1) exp(-ε m).

The expectation already includes all 2^m input pairs at each (i,j); there
is no additional exponential counting factor. This decays exponentially, so
Z_L<1 for some finite L. In the language forbidding every noncanonical word
of length at most L, every disjoint L-column block and final shorter block
is canonical. Multiplicativity of column weights bounds the total weight of
kL+r columns by Z_L^k Z_r. Its total path sum is finite. Strictness and finite
continuity allow rational x,t nearby, still with positive exponent at a.
All states are reachable and all edge weights positive, so finiteness from
the root implies finiteness from every state and convergence of the matrix
series. A finite rational matrix then has the positive rational certificate
V=(I-A)^(-1)1, since AV=V-1; clearing denominators gives an integer certificate.

Thus the unrestricted canonical-window first moment can establish every
rational a<C. This supplies a written ceiling/convergence proof for the
complete window hierarchy, beyond the sketch in ref91.md. It gives no
practical state count or precision bound and no numerical lower bound without
an independently checked finite construction. The tested resource ceiling
must be reported from completed experiments, not extrapolated to 0.27/0.28.
