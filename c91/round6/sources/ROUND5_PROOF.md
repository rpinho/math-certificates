# Round 5 proof specification

Candidate and unrefereed. The selected frozen artifact and exact verification
receipts establish the candidate C91 >= 264263/1000000, above 33/125.
Floating root estimates are diagnostics; no novelty judgment is made.
Credit Leandre Jack's #273 canonical first moment, Ganguly–Mossel–Rácz,
Bilardi–Schimd, Lueker, and the inherited rounds 2–4.

The round-4 frozen artifact was replayed successfully in this job on
2026-11-03: all 65,623,319 states and 268,855,220 edges passed strict integer
inequalities, with an Arb-positive exponent at 263561/1000000. Its unchanged
artifact hash is in BAR.json and the new receipt is logs/baseline.log.

## Canonical choice and local constraints

Columns 0..7 are 00,11,01,10,D0,D1,I0,I1, with costs 0,0,1,1,1,1,1,1.
Choose the alignment minimizing (cost, gap count, operation word), ordering
diagonal < D < I. At equal cost and gaps the number of columns is fixed by
the consumed lengths. Replacing a contiguous segment by a smaller key would
therefore improve the whole key. Every segment and prefix of the selected
alignment is canonical for its own consumed input strings.

The five inherited run restrictions have the following local exchange proofs.
Here D/I consume one X/Y symbol, M is a matching diagonal, and S is a
mismatching diagonal.

1. Adjacent opposite gaps can be replaced by one diagonal, reducing cost
   from two to at most one.
2. In D(a),S(b,c), move the diagonal first: diagonal(a,c),D(b). Its cost
   decreases or ties, its gap count ties, and at a tie its first operation
   is earlier. The insertion version is the same exchange with X/Y swapped.
3. If a match ending a D run uses a bit found in that run, match the earlier
   occurrence and delete the displaced symbols, including the old final
   matched X bit. Cost and gaps tie and a diagonal moves earlier. The I
   version is symmetric.
4. D(a),M(b,b),I(c) can be replaced by diagonal(a,b),diagonal(b,c).
   The new cost is at most two, and if cost ties, it has fewer gaps.
   The opposite orientation has the same argument.
5. After S(a,b), a D run cannot contain b: delete the displaced original a
   and match that occurrence to b, removing the substitution cost while
   retaining the gap count. After a substitution an I run similarly cannot
   contain the preceding X bit.

The run memory records the direction, symbols in the current run, forbidden
bit inherited from the preceding substitution, and the run direction for
one step after an ending match. These enforce exactly the stated tests.
Its initial memory is empty; terminal gap runs need not have a common bit.
Every explicitly listed word is an additional necessary exclusion. Every listed word must fail an exact
canonical-key DP. The bank may be incomplete. A matcher rejects a word iff
a listed word occurs as a contiguous factor. Its reachable states retain
all initial histories and all terminal states.

## Bounded gap-saving and gap-debt record

At actual endpoint (i,j), cost C and gaps J, a vertical lag r refers to
(i-r,j), a horizontal lag r to (i,j-r), for 1<=r<=W. Each retained
triple (c,g,t), t=-1 or +1, has one real edit-path witness Q with:

1. exactly those input prefixes consumed, and cost(Q)-C=c exactly;
2. a first differing operation already inside both Q and the actual word;
3. if g is finite, true gap difference d=gaps(Q)-J satisfies d<=g;
4. if g is finite, d=g and t=-1, that first difference is earlier in Q.

An infinite g forgets only the gap information. It retains the exact cost
and the real path. The tag carries no promise at +1, or when d<g.

Complete a lag-r witness by r gaps of the lagging string. Reject the actual
prefix if c+r<0, or if c+r=0 and finite g+r<0, or if c+r=g+r=0 and t=-1.
The completed path then has lower cost; or fewer gaps at tied cost; or, when
the actual gap bound is attained, an earlier established operation at tied
cost and gaps. If d<g in the last case, it instead has fewer gaps. Thus
every rejection is justified by a genuinely smaller complete-prefix key.

Fix integers S>=0, T>=1 and finite cost caps. Check rejection on every
offered candidate BEFORE forgetting anything. Do not retain r=0. Forget a
candidate when c>B (absolute mode), or c+r>Q (completion mode). If finite
g+r>2T, replace g by infinity and t by +1; infinity stays infinity under
extension. If finite g<-r-2S, replace it by -r-2S and t by -1. In this last
case the true difference is strictly less than the replacement bound, so
the conditional order promise is vacuous. Otherwise retain the tag.

At each vertex retain the lexicographically least complete triple (c,g,t),
with infinity larger than any finite gap bound. This selects one witness;
it never combines coordinates from different witnesses. No assertion that
this minimum finds every useful competing path is needed for soundness.

The surviving finite gap coordinate has values
g=-r+2k, -S<=k<=T, by gap parity. Accepted prefixes have c>=-r. Therefore
the frontier, histories and run memory form a finite state. Round 4 is the
special case S=0,T=1. S>0 retains extra gap savings that round 4 saturates;
T>1 postpones the loss of gap information at its unknown-gap placeholder.
These are changes in recorded path information, beyond retuning weights.

The separately written (same agent) checker uses completed scores
A=c+r and G=g+r rather than the search's c and g. Rejection becomes
A<0, or A=0 and finite G<0, or A=G=0 with t=-1. The finite G range is
[-2S,2T] in steps of two; the cost cap is A<=B+r or A<=Q. Appending
trailing gaps to a smaller lag leaves A and G unchanged. A same-side
diagonal changes A by mismatch-e and leaves G unchanged; lag growth and
cross-corner diagonal routes change (A,G) by (2-e,2). All-gap actual-gap
routes leave both unchanged; the alternative diagonal route changes them
by (mismatch-2,-2). These identities follow by substituting c=A-r and
g=G-r into the displayed relative-score formulas below.

## Witness propagation

Use the routes below in both orientations, interchanging X/Y and D/I.
All changes are relative to the NEW actual prefix, subtracting its cost
and gap count once. Appending the same genuine edit operations to a witness
preserves its established first difference and changes d and finite g by
the same amount. A strict d<g remains strict. The invariant survives every
route and each subsequent cap, saturation and minimum operation.

For an actual diagonal (a,b), let e=[a!=b] and let X_ext[k] denote the kth
symbol back after appending a, with k=0 the new symbol. From old vertical
lag q to new vertical lag 0<=r<=q, append one diagonal and q-r D gaps.
Putting the diagonal at any k in [r,q] gives

    delta_cost=q-r+[X_ext[k]!=b]-e; delta_gaps=q-r.

From the same source, append I(b) to reach vertical q+1 when q<W, with
changes (1-e,1), or q+1 D gaps to reach horizontal 1, with changes
(q+1-e,q+1). These consume exactly the required new prefixes.

For an actual D(a), from vertical q reach any vertical
0<=r<=min(W,q+1) by q+1-r D gaps, giving changes (q-r,q-r). The case
r=q+1 pauses the witness. From horizontal q to horizontal 0<=r<=q,
append D(a) and q-r I gaps, giving (q-r,q-r); when q>r, alternatively
append one diagonal at any position among the q-r buffered Y symbols
and q-r-1 I gaps, giving (q-r-2+mismatch,q-r-2).

After these routes, for each side and descending q, close its fresh lag-q
entry to each r<q by q-r trailing gaps, adding (q-r,q-r). All candidates
are processed through the same rejection and forgetting rules.

New witness origins are the inherited ones. On an actual diagonal,
replace that diagonal by I or D, obtaining vertical or horizontal 1 with
(c,g,t)=(1-e,1,+1). Before a suffix of q actual D gaps the common actual
prefix has relative scores (-q,-q). On the following actual diagonal,
its first diagonal followed by q-r D gaps gives vertical r<=q with
(-r+[X_ext[q]!=b]-e,-r,-1). Instead its first I reaches vertical q+1
with (1-q-e,1-q,+1), when q+1<=W. For a suffix of I gaps the latter tag
is -1 because D<I; the earlier diagonal origin has tag -1 in either
orientation. The run length capped at W identifies exactly these origins.
No absent or negative-coordinate source is used.

Induction from empty frontiers proves the invariant. Every rejection
contradicts canonical prefix optimality, so every selected canonical word
survives at every input length. This is a sound finite overcount, with no
completeness assertion about band dynamic programming. Small exhaustive
tests supplement this proof and do not replace its universal induction.

## Minimization and first moment

All states accept. Minimize the standalone tracker by ordered signatures
of the eight labels, feature increments and destination classes, including
missing edges. Stable equality preserves every labeled future continuation
and weight by induction on its length. Minimize the pattern matcher before
taking the reachable product. The product permits a label exactly when both
components permit it. A second partition by multisets of (weight monomial,
destination class), preserving multiplicity, only indexes the potential.
The exact verifier must reconstruct these partitions and check every full
product row, rather than trust search graphs or partitions.

For the inherited four features use sliding spin products: pairs at lags
1,2,3 and consecutive four spins, summed over X and Y. Every sum has mean
zero and variance <=2n, since distinct translates of a nonempty finite
Walsh pattern are orthogonal. Chebyshev gives probability <=8/sqrt(n) that
any absolute feature exceeds n^(3/4). Each complete alignment counts each
input feature once, independent of the alignment.

Weight a column consuming ell bits and costing k by
2^(-ell) x^ell t^k product z_j^h_j, for rational x>1,0<t<1,z_j>0.
If a positive exact potential satisfies AV<V in every reachable product row,
the all-path sum G is finite: max_i(AV)_i/V_i=theta<1 and a fixed multiple
of V dominates the all-ones vector. Each low-distance typical pair has its
canonical word in this sum, of weight at least
4^(-n)x^(2n)t^(an)exp(-n^(3/4)sum_j|log z_j|). Distinct input pairs have
distinct labeled words. Thus their probability is at most
G exp(-n(2log x+a log t)+O(n^(3/4))). A positive exponent, plus the vanishing
atypical probability, proves liminf E ed/n>=a. Subadditivity and Fekete
give existence of C91. A round-5 claim requires a>=33/125 and complete
exact verification of its frozen artifact.

## Different method: longer words and higher-order input statistics

For any fixed collection of nonempty finite spin patterns P containing
offset zero, normalize the maximal offset to span(P). Sum the product over
every valid translate in each input. Every translate has mean zero; two
distinct translates have different supports and are orthogonal, so the
combined variance is <=2n for each P, even with overlapping windows.
A union bound gives typicality for every fixed finite collection. More
explicitly, changing a bit affects at most |P| translates and changes its
feature by at most 2|P|. Bounded differences gives
P(|H_P|>u)<=2 exp(-u^2/(4n|P|^2)) for two length-n inputs. At u=n^(3/4)
this also tends to zero. Consequently the discarded strings are o(4^n)
and the retained set has log-cardinality n log 4+o(n); its entropy-rate
penalty is zero. None of these estimates assumes independence of overlapping
windows.

New columns emit each pattern exactly when its last input bit is consumed;
short histories suppress windows not yet present. The same first moment
therefore applies with more correlation weights. A candidate alternative
uses longer explicitly noncanonical words mined by exact short-string DP
and even spin patterns of span four. Each word must be verified exactly;
sampling finds prohibitions but is never itself a proof of a lower bound.
This method is distinct from expanding the gap coordinate. Its concrete
tested models, results and certificate status must be recorded separately.

The proposed eight-pattern feature list, encoded by bit masks relative to
the newest input bit at offset zero, is [3,5,9,15,17,23,27,29]. These are
the inherited lag-1/2/3 pairs and consecutive four spins, followed by the
lag-4 pair and the four-spin supports {0,1,2,4}, {0,1,3,4}, {0,2,3,4}.
Every feature increment is in [-2,2]. The inherited tracker already keeps
four preceding input bits; only the feature labels and their minimized
future-equivalence classes need change.

## Exact certificate arithmetic

The gap-record schema fixes W,B,S,T and absolute or completed cost cap;
the higher-order schema additionally fixes the eight feature supports above.
The frozen object contains the complete explicit forbidden-word bank as
[length, base-eight integer], all rational parameters, expected reconstruction
counts and a positive potential. Counts are checked, not assumed. A normal
positive binary32 potential entry denotes an exact dyadic rational, decoded
by integer bit operations; zero, negative, subnormal and nonfinite entries
are rejected. Byte-plane transposition is inverted exactly. Clearing a
common power of two gives positive uint64 integer potentials; overflow is
rejected. No floating inequality certifies a row.

For x=p/q, t=r/s and z_j=u_j/v_j, choose

    D=4 q^2 s product_j u_j^2 v_j^2.

For feature increments h_j in [-2,2], each edge coefficient times D is

    match: p^2 s product_j u_j^(2+h_j) v_j^(2-h_j);
    substitution: p^2 r product_j u_j^(2+h_j) v_j^(2-h_j);
    gap: 2pqr product_j u_j^(2+h_j) v_j^(2-h_j).

The checker requires sum_edges coefficient*V_destination < D*V_source in
EVERY complete reachable row, with multiplicity. At K features and positive
64-bit parameters/potentials, each diagonal summand is <2^(256K+256), each
gap summand <2^(256K+257), and summing four of each is <2^(256K+260).
Thus 1536 bits suffice for K=4 and 2560 bits for K=8, with explicit overflow
rejection. The final exponent 2 log x+a log t is enclosed by 256-bit Arb.
A separate exact rational atanh-series enclosure on the same frozen artifact
checks this exponent and a>=33/125 again. These are separately written
(same agent) checks, with the inherited components identified in
VERIFICATION_SCOPE.md; no external referee or independent authorship is claimed.

The four-feature orbit checker also performs a necessary root-row test before
building the full graph. All one-column words are canonical, hence a bank
already checked to contain only noncanonical words cannot exclude them.
Empty run memory and empty frontiers permit all eight columns; all root
feature increments vanish. Weighted partition classes are numbered by first
appearance, so the root has class zero. If m is the minimum potential,
the complete root row is at least
m[x^2(1+t)/2+2xt]. For x=p/q and t=r/s, rejecting when
(2p^2s+2p^2r+8pqr)m >= 4q^2s V_0 is therefore sound.
Passing this necessary test proves no row; full reconstruction and every
strict integer row check still follow. This lets a positive corrupted root
potential fail an exact row consequence before an expensive rebuild.

## Direct construction and global bit-complement quotient

The standalone tracker need not be materialized or minimized first. One may
instead update its finite frontier while simultaneously following the
already minimized forbidden-word matcher. This enumerates the same reachable
intersection from its initial state. Omitting forbidden words in this route
remains sound and requires no claim of redundancy. A finite prefix trie of
candidate words can be used to test their cold-start tracker acceptance
without enumerating the standalone tracker: each trie vertex has one input
prefix, hence one deterministic tracker state. This is only a bank-selection
heuristic, not a proof premise for a numerical certificate.

The base automaton here also includes the actual alignment's literal run
memory. Its minimization signature explicitly retains that memory tag, so
every merged class has one unambiguous run memory for frontier propagation
and origin creation. This may be finer than the minimum partition for the
word language alone; that additional distinction preserves soundness.

All stored input features have even spin degree. Complementing every input
bit therefore preserves each feature increment, column cost, consumption,
the canonical operation order, and every frontier score. The five run rules
are invariant too. Require the explicit forbidden bank to be closed under
column complementation phi=(0 1)(2 3)(4 5)(6 7). Its minimized matcher has a
root-fixing involution F with

    edge(F(q),phi(c)) = F(edge(q,c)),

including missing edges. Construct F from the root by paired labeled BFS,
check this identity at every matcher vertex and label, check F squared is
the identity, and check the literal run memory is complemented correctly.
Thus F is verified on the actual minimized matcher, not assumed from a hash.

Complement a full intersection state by F on its matcher coordinate and
bitwise complementation of every valid stored input-history bit. History
lengths, run length and frontier scores remain unchanged. Call this
involution C. For every actual transition s --c--> t the complemented
transition is C(s) --phi(c)--> C(t), with the identical weight monomial.
The extension formulas use only symbol equalities, real gaps and operation
order, so this follows also directly from the witness invariant.

Choose one representative of each orbit: make its most recent X bit zero
when X has a bit, otherwise make its most recent Y bit zero; the empty root
is fixed. From a representative compute all eight transitions and normalize
each target by this rule. Keep every edge and its multiplicity, even when
two labels lead to the same orbit. Only these reachable representatives are
materialized. Each original reachable state normalizes to a reachable
representative by induction on its path, and every representative path
lifts to an original path, since complementation permutes the labels.

Let V be a positive potential on representatives passing every strict row
inequality. Lift it by Vtilde(s)=V(normalize(s)). For a nonrepresentative
source the eight outgoing labels are permuted by phi, their weights are
unchanged, and their target orbits agree. Its weighted row sum is therefore
exactly the checked representative row sum. Consequently AVtilde<Vtilde
on every original reachable state. The original graph has the canonical
inclusion and the original input-based weights already proved above, so
the same first-moment bound follows. The quotient's emitted label sequence
need not itself spell the original input strings; the lifted-potential
argument avoids making that false identification.

For a direct canonical-path audit, before each original column use its label
complemented iff the most recent original X bit is one (or the most recent
Y bit when X is still empty). The representative histories are the original
histories uniformly flipped by exactly that flag. Even feature increments
therefore agree with the original strings at every column. This supplies
an explicit path lift for exhaustive small-pair testing. Any result using
the quotient must report representative counts as such and pass a frozen
checker that reconstructs the matcher involution and the quotient rows.

A cost cap can also be specified separately at each lag: fixed integers
b_r >= -r, retaining a witness only when c<=b_r. In completed scores this
is A<=b_r+r. This changes only the forgetting step, so the same witness
induction and canonical-survival argument apply without modification.
The artifact must contain the complete vector. The per-lag schema writes
signed 32-bit caps; the frozen checker rejects a missing coordinate or an
out-of-range cap and rebuilds every row with exactly that vector. This
allows narrower new lags while retaining the old cost range at old lags.

## Selected numerical instantiation

The frozen object `frozen/candidate_c91r5.json.gz`, SHA256
`d10ed2cc774a853b2f7719984aae0d93161f651403d8db8eb1bd6b849af949b9`,
uses W=3, absolute cost cap B=2, S=0 and T=2, with 55,550 explicitly listed
words of length at most 12. All parameter denominators are 10^9:
x has numerator 1145933884, t has numerator 356670822, and the four z
numerators are 1041421066, 1016222687, 1004130270, 1002178291.
The four weights and t equal those of round 4.

Its proposed rational conclusion is C91 >= 264263/1000000, exceeding the
frozen 33/125 bar by 263/1000000 and round 4 by 351/500000.
The separately written (same agent) rational logarithm enclosure on these
frozen bytes proves 2 log x + (264263/1000000) log t > 0, with lower
endpoint approximately 2.4517986932761248e-8. The Arb threshold is
0.2642630237821207938573172551207910559... . The complete exact
strict-row replay and all five actual-artifact rejection controls passed,
as recorded in REPORT.md and logs/main_exact_summary.json. All120,590,405
rows and496,043,318 edges passed strict integer inequalities, instantiating
the first-moment theorem at264263/1000000. This remains candidate and unrefereed.
