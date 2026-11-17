# Proof of the finite equalities

Write M(χ) for the largest cardinality of a nonempty monochromatic family of subsets closed under binary union and intersection. Then f(n)=minχ M(χ). The minimum includes every colouring of all subsets. Rank colourings below are particular constructions giving upper bounds, not a restriction on that minimum. The n=11 and n=12 queries ask for at least eight members; the n=13 and n=14 queries ask for at least nine. These thresholds exclude every larger closed family as well, without assuming that a larger lattice contains a sublattice of exactly the threshold size.

## Lower bounds

At n=12, restrict any colouring to the thirteen prefixes ∅,{1},...,{1,...,12}. At least seven have one colour. Their union and intersection are their maximum and minimum in the chain, and thus still belong to that colour's selected subchain. This proves f(12)≥7 without prescribing ambient endpoints.

At n=11 the published Bhattacharjee–Mandal–Bhattacharya bound gives f(11)≥7. The first referee also reproduced the needed finite argument in [published_lower.py](referee/n11/published_lower.py) and explains the arbitrary-colouring reduction in section (c) of [REFEREE.md](referee/n11/REFEREE.md). Here are its steps.

If a colouring had no monochromatic closed family of seven members, each twelve-member maximal chain would have six members of each colour. Two chains can differ only in one r-subset, obtained by exchanging one element. Their colour counts force those two r-subsets to have the same colour. The exchange graph on each rank is connected, so every rank is monochromatic. It suffices to rule out balanced twelve-bit rank words.

The referee verifies the omega note's explicit construction for all balanced words: 924 possibilities, of which 874 admit a diamond on three consecutive occurrences of one colour with equally spaced ranks; ten explicit closed families cover the remaining 50. If a<b<c are such consecutive ranks and a+c=2b, let P_r={0,...,r−1}. Add P_a∪{b,...,c−1} to the six prefixes of that colour. It has rank b, forms a diamond with P_a,P_b,P_c, and is comparable with the remaining prefixes. This is a closed seven-member family. The residual families in the script are separately checked by set operations. The same script also checks the current BMB paper's eight product-of-chains gadgets against all 4096 rank words. Thus the lower bound is for arbitrary colourings, not only rank colourings. These are reproductions of published lower bounds.

## Producer membership CNF, n=11 and n=12

The two retained copies of encode_family.py implement the same construction. Enumerate, in increasing mask order, all subsets S of the chosen colour, with Boolean variable y_S. A true variable means S belongs to the family. For each incomparable pair S,T impose

    ¬y_S ∨ ¬y_T ∨ y_(S∪T)
    ¬y_S ∨ ¬y_T ∨ y_(S∩T).

If an operation's result has the other colour, omit that positive literal. Comparable pairs need no clause because their union/intersection is one of the pair. Therefore these clauses hold exactly when the selected family is closed. Duplicate binary clauses are retained as part of the byte-level encoding.

Let N be the number of candidate members, and enumerate them y_1,...,y_N. For every 1≤i≤N and 1≤j≤min(i,8), introduce A(i,j). The intended meaning is that at least j of the first i members are selected. Let b=A(i−1,j) when that node exists and c=A(i−1,j−1) when it exists. The encoder adds

    ¬A(i,j) ∨ b ∨ y_i
    ¬A(i,j) ∨ b ∨ c          (only for j>1),

omitting nonexistent b or c, and asserts A(N,8). For j=1, a true node forces a previous true node or y_i. For j>1, if b is false, both y_i and c must be true. Induction on i proves that every true A(i,j) implies at least j selected members. Conversely, the assignment A(i,j)=[the actual prefix count is at least j] satisfies every clause. Thus the counter is sound and complete for at least eight selected sets. It does not require all A variables to equal their intended meanings in every assignment.

Consequently, each base CNF is satisfiable exactly when that colour contains a closed family of at least eight members. The separate producer check_family.py scripts reconstruct every closure and counter clause using actual sets and no encoder imports. Their full checks are documented in REPRODUCE.md. The colouring checkers compare all mask colours with the membership lists and rank words.

## Colour-zero symmetry at n=12

The complete retained colour-zero proof uses the base CNF plus add_lex.py's comparisons with each of the 66 transpositions of the twelve coordinates. Permutations preserve the rank colouring, union, intersection and family size.

The membership bit vector is ordered by increasing mask, with false before true. For one transposition, ignore fixed positions and keep each exchanged pair (a_i,b_i) only at its earlier endpoint. Its comparison is the same as the comparison of the full vector with its image: the first differing position is an earlier endpoint. With p_0=true, the clauses are

    ¬p_(i−1) ∨ ¬a_i ∨ b_i
    ¬p_(i−1) ∨ ¬a_i ∨ ¬b_i ∨ p_i
    ¬p_(i−1) ∨  a_i ∨  b_i ∨ p_i.

While prefixes agree, equal bits force p_i=true and the difference 1>0 is forbidden. At the first difference 0<1, remaining prefix variables can be false. Thus the clauses admit an extension exactly for a lexicographically nonlarger vector.

If a counterexample family exists, choose the lexicographically least membership vector in its finite coordinate-permutation orbit. It satisfies every transposition comparison. Extend its counter variables by actual prefix counts. This proves that the augmented CNF is satisfiable if and only if a counterexample family exists, although individual labelled counterexamples may be removed by symmetry. check_lex.py separately reconstructs the comparisons and checks that the base clauses are preserved.

The n=11 queries and the n=12 colour-one query need no such symmetry argument. DRAT checking of the four retained producer proofs establishes UNSAT of their exact CNFs, hence both upper bounds. ASSETS.json binds the exact CNF and proof hashes. The unfinished n=12 base colour-zero proof is excluded.

## Clean-room referee encodings and non-SAT argument

The first referee's encode.py uses an exact prefix-count equivalence, with all implications, rather than the producer's one-direction counter. The second referee's ref.py uses a truncated tree totalizer: a node output o_j means count at least j. For child outputs a,b it adds ¬o_(i+j+1)∨a_(i+1)∨b_(j+1), omitting nonexistent child outputs, and asserts root o_8. If the child counts are u,v and a true output had index greater than u+v, the clause for i=u,j=v would fail. Induction proves soundness. Assigning every output its actual subtree threshold count proves completeness. Closure clauses have the same direct set interpretation as above. The referee's plain queries cover both colours without any symmetry clauses. Its interval queries additionally fix least and greatest family members and use the rank-invariant coordinate permutation described in its report. Original referee proof hashes remain historical records; release assets are the producer proofs, not those deleted referee proofs.

Both referees also gave weighted-poset upper checks. The n=12 implementation and its mathematical argument are in [ref.py](referee/n12/ref.py), [dfs_scan.py](referee/n12/dfs_scan.py), [dfs_control.py](referee/n12/dfs_control.py) and section (b) of its original report. For completeness, the structure argument is as follows.

A finite nonempty sublattice L has a least member B and greatest member T. For each x∈T\B let m(x) be the intersection of members containing x, which lies in L. Define x≼y when x∈m(y). This is a preorder. Every X∈L is B∪⋃_{x∈X\B}m(x); conversely, every down-set D of the preorder gives B∪D∈L by taking that union (or B for the empty down-set). Collapse equivalent coordinates to blocks: the quotient is a poset with positive integer block weights and total weight at most n−|B|. The ranks in L are exactly |B| plus the weights of its ideals.

The DFS enumerates the offset |B| and builds every such weighted poset by adding one maximal element at a time in a linear extension. Its predecessor set can be any ideal D of the previous poset. New ideals are I∪{new} for previous ideals I containing D; previous ideals remain. Thus any wrong-colour ideal already present can never be repaired, making pruning exact. The DFS stops growing a branch once it has at least eight ideals; such a branch already disproves the desired upper bound. On the supplied word both colours have maximum seven, so no branch reaches eight. This exhaustive integer/set computation proves the upper bound without SAT. The first referee separately enumerated natural-labelled posets with at most five elements, justified by the six-member longest monochromatic chain at n=11; its rank_lattices.py obtains the same maxima.

The second referee's controls compare all rank words at n=4 with brute-force sublattice enumeration and scan dimensions through twelve. The scan is only over rank colourings; it is not an unrestricted lower-bound proof. The chain lower bound supplies the unrestricted n=12 conclusion.

## The n=13 and n=14 membership queries

The round-3 source is in [producer/n13n14](producer/n13n14). For each colour the increasing-mask member list is exactly the sets of that colour in the full colouring. The n=13 encoder is `encode_family.py`; the n=14 `encode_family_stream.py` emits the same clause scheme and order while streaming its output. `add_lex.py` adds the transposition comparisons. The separately written same-producer `check_statement.py` reconstructs every clause directly from frozenset operations without importing either encoder; it covers closure, the counter and the lex clauses. It is a separate implementation, not an independent referee.

Put K=9. For each incomparable pair S,T of the chosen colour emit both closure clauses from the earlier section, deleting the positive literal if the operation has the other colour. Every selected pair must therefore have both results selected and in the colour class. Conversely any closed family satisfies these clauses. Comparable pairs already contain their union and intersection. Duplicate binary clauses are retained for exact regeneration.

For each 1≤i≤N and 1≤j≤min(i,9), the counter node A(i,j) has the two backwards implications given above, with the j=1 clause only and missing predecessors omitted. Assert A(N,9). Induction on i shows that a true A(i,j) requires at least j selected members in that prefix. In the reverse direction set each node to the truth of its actual prefix count being at least j. This extends every selection of at least nine members to a satisfying counter assignment. Thus each base CNF is satisfiable **exactly when its colour class contains a union-and-intersection-closed family of at least nine sets**. No ambient endpoints are imposed.

Both colours use all coordinate-transposition lex comparisons: 78 at n=13 and 91 at n=14. The recurrence and orbit-minimum proof in the n=12 section apply verbatim, since both new colourings depend only on set size. Any coordinate permutation preserves colour, cardinality and the two operations. The lexicographically least membership vector in a solution's entire permutation orbit satisfies every comparison; its prefix-count variables can be recomputed. Comparing only transpositions need not fully break symmetry; soundness only needs the orbit minimum to survive. Therefore the extended CNF is satisfiable exactly when such a closed family exists. This is the standard lex-leader technique of Crawford et al., credited in README.md.

| n | Colour | Variables | Clauses | Matching retained proof |
|---|---|---:|---:|---|
| 13 | 0 | 113152 | 14751865 | [n=13 colour-zero asset](ASSETS.json) |
| 13 | 1 | 128440 | 17916013 | [n=13 colour-one asset](ASSETS.json) |
| 14 | 0 | 274105 | 69563843 | [n=14 colour-zero asset](ASSETS.json) |
| 14 | 1 | 262399 | 61463499 | [n=14 colour-one plain asset](ASSETS.json) |

All four original producer proofs passed default backward drat-trim; their original check logs and hash records are in `producer/n13n14`. The packaging reruns the n=13 colour-0 and smaller n=14 colour-0 proof from the compressed release streams against fresh byte-identical CNFs. Exact CNF commands and hashes are in REPRODUCE.md, N13N14_CNF_SHA256SUMS and ASSETS.json. Default n=14 solvers hit recorded resource limits in the producer job; the successful colour-0 proof uses kissat, and colour 1 uses kissat `--plain`. The unfinished non-plain colour-1 trace and zero-byte colour-0 CaDiCaL file are not certificates and are excluded.

## Chain-exchange lemma and the new lower bounds

Let n be odd and suppose every monochromatic closed family has at most (n+1)/2 members. Each maximal chain has n+1 sets. The sets of either colour on that chain form a closed subchain, so every maximal chain must have exactly (n+1)/2 of each colour. For two k-sets T,T′ with |T∩T′|=k−1, choose chains agreeing below T∩T′ and above T∪T′, and differing only in their rank-k member T or T′. The equal colour counts force χ(T)=χ(T′). Single-element exchanges connect the k-sets, so each rank is monochromatic. The endpoints have only one set each. Thus **an odd-n colouring attaining the chain bound depends only on set size**, and its rank word is balanced.

For n=13, an upper bound seven would therefore require a balanced word of length fourteen. The referee's [balanced.py](referee/n13n14/src/balanced.py) enumerates all binomial(14,7)=3,432 such words and uses its exact poset search with threshold eight. Each rejection has an actual monochromatic family of at least eight masks, checked directly for union/intersection closure. The [per-word output](referee/n13n14/logs/n13_balanced_words.txt) and [summary](referee/n13n14/logs/n13_balanced_summary.log) record 3,432 rejected, zero remaining (3,318 in colour zero and 114 in colour one). Together with the lemma this proves f(13)≥8 for arbitrary colourings, independently of the published lower-bound proof. The producer's separately written rank-screen checker and its witness list reproduce the same known lower bound.

This bound is already published: Bhattacharjee–Mandal–Bhattacharya Proposition `prop:flower` gives f(n)≥ceil((n+1+floor((n+1)/12))/2), which is eight at n=13. The omega institute note gives f(n)≥(n+3)/2 for odd n≥11. The pinned sources are linked in README.md; the referee's original report discusses both. The packet does not claim these lower bounds as new.

At n=14 every maximal chain has fifteen sets, so at least eight share a colour. Any subchain is closed under union and intersection. This proves f(14)≥8 for every colouring.

## The new referee's exact weighted-poset argument

The byte-preserved [REFEREE.md](referee/n13n14/REFEREE.md) supplies a clean-room [encoder](referee/n13n14/src/enc.c), its own solver/proof checks and a separate upper-bound argument in [poset_search.py](referee/n13n14/src/poset_search.py). Its counter uses all nine thresholds even on short prefixes, with impossible nodes at the first prefix set false. Closure binaries are deduplicated when both results have the other colour. Hence its CNFs differ from the producer's. Its own large proofs were discarded after verification and are not the release assets; the original hashes and check logs are preserved.

The weighted-poset reduction above is Birkhoff's representation theorem in this concrete setting. For a finite closed family L with minimum A and maximum B, each coordinate x∈B\A has a least member m(x) containing it. This member is join-irreducible: in a union decomposition one part contains x, so minimality forces that part to be m(x). Every join-irreducible arises this way: it is the union of the m(x) it contains, so join-irreducibility forces equality with one. Assign to each join-irreducible J the positive integer weight w(J)=#{x:m(x)=J}. Under the isomorphism with ideals D of the poset P of join-irreducibles, the corresponding set has rank |A|+sum(J∈D)w(J), and |A|+sum w≤n. Conversely use disjoint coordinate blocks with these weights and a common base of size |A| to realize every such weighted poset as a closed family in 2^[n].

For a size-only colouring it therefore suffices to enumerate a base size a, a finite poset P and positive weights within n, requiring every ideal rank a+w(D) to have the chosen colour. The referee DFS builds P in a linear extension. When adding a maximal element its predecessor set is any ideal D0 of the old poset. Exactly the old ideals I containing D0 give new ideals I∪{new}; the old ideals remain. It tries all positive weights within the remaining coordinate budget and prunes if any new ideal has a forbidden rank. That pruning is permanent, since future additions retain all current ideals. Every weighted poset has such a linear extension and appears in this enumeration. Positive weights bound the depth by n−a, and each step strictly increases the ideal count, so the search terminates and is complete up to any requested threshold t.

For t=9, the [original output](referee/n13n14/logs/poset_search.log) finds no family at either dimension, exhausting 204 nodes in colour zero for both words, 186 in n=13 colour one, and 403 in n=14 colour one. At t=8 it constructs and directly checks eight-member families in n=13 colour zero and both n=14 colours; n=13 colour one has none of eight. The upper bounds eight thus hold without SAT or lex symmetry. The referee's `validate_small.py` compares the search with brute-force enumeration of all sublattices for every rank word and both colours at n=3,4,5 (73, 731 and 12,084 sublattices); its original output records zero mismatches. This finite control does not formalize the representation or DFS proof.

## Scope

Combining the lower and upper bounds gives f(11)=7, f(12)=7, f(13)=8 and f(14)=8. These are conventional computational candidate proofs supported by the supplied clean-room AI agents’ referee verdicts HOLDS. The mathematical encoding and symmetry arguments are not kernel formalizations, drat-trim is not a formally verified checker, and there has been no human review. Priority searches have the limits recorded in PRIOR_ART.md and the original referee reports.

## Extension: weighted-poset certificates for n=15..20

The following reduction, completeness, symmetry/prune proofs and chain-exchange lemma are from the producer’s PROOF.md. In this extension, search code is `producer/n15n20/src/poset.cpp`, tree and witness checks are `producer/n15n20/src/check.py`, and proof data are `producer/n15n20/certificates/`. The clean-room referee’s separate implementation is `referee/n15n20/src/wps.c`; its original report is `referee/n15n20/REFEREE.md`. The original producer document is retained alongside its code; historical statements that the external computation was not rerun refer to the producer session.

We study the Erdős–Ulam function. The problem page says “a monochromatic family of at least f(n) sets which is closed under taking unions and intersections”. BMB call a family a “sublattice if it is closed under both union and intersection”. Here families are nonempty; neither ∅ nor [n] is required. Equivalently f(n)=min over all two-colourings of the largest such family. A rank word W of length n+1 assigns W[|S|] to S.

## 1. Reduction in both directions

Let L be any nonempty finite sublattice of 2^[n]. Its bottom A=∩L and top B=∪L belong to L by finite binary closure. For x∈B\A put m(x)=∩{S∈L:x∈S}. This is a nonempty intersection, belongs to L, contains x, and is not A. If m(x)=U∪V with U,V∈L, then x belongs to one of U,V, say U; minimality gives m(x)⊆U, so U=m(x). Thus m(x) is join-irreducible.

Conversely every join-irreducible J equals some m(x). Indeed J=A∪⋃_{x∈J\A}m(x), since each m(x)⊆J contains x. The index set is nonempty because J≠A. Finite join-irreducibility implies one of those m(x) equals J. This proves the positivity assertion needed below (review lemma 1c).

Let P be the join-irreducibles ordered by inclusion. Since L is distributive, Birkhoff's representation theorem identifies L with the down-sets D of P, by S↦{J:J⊆S}. In concrete coordinates S=A∪{x∈B\A:m(x)⊆S}. Define a=|A| and w(J)=#{x∈B\A:m(x)=J}. Every w(J) is a positive integer and a+Σw=|B|≤n. The size of the member associated with D is a+Σ_{J∈D}w(J).

Conversely, take a≥0, a finite poset P, and positive integer weights with a+Σw≤n. Choose disjoint coordinate blocks A, X_J of sizes a, w(J). To every down-set D associate A∪⋃_{J∈D}X_J. Nonempty blocks make this map injective. Disjointness makes it preserve union and intersection. Thus it realises the down-set lattice as a nonempty sublattice of the cube with exactly the stated sizes. P=∅ gives the singleton family {A}.

Therefore a colour class R contains a closed family of **at least m** members if and only if there is such a weighted poset with at least m down-sets and all its down-set sizes in R. “Exactly m” is not interchangeable: the Boolean cube on three coordinates has no seven-member sublattice.

## 2. Exhaustive search

A state contains a and a naturally labelled weighted poset: element i is added after all its strict predecessors. Its strict predecessor mask I must be a down-set of the existing poset. Every such I is permitted. When a new element of weight w is added, old down-sets persist; new down-sets are D∪{new} for exactly the old down-sets D containing I. Their sizes are a+w(D)+w. Branch over every w=1,…,n−a−Σw. Reject a branch if any new size has the wrong colour. Accept a witness when the number of down-sets is at least the threshold, including jumps past it. We count down-sets, not distinct sizes.

Completeness has four parts:

1. Every finite poset has a linear extension, hence a natural labelling generated by this scheme.
2. Each prefix in that extension is a down-set of the final poset. Every down-set of a prefix is also a down-set of the final poset. All its sizes must therefore be allowed; pruning an invalid size cannot remove a valid final witness.
3. At every state the scheme considers every down-set I and every positive weight within the full remaining coordinate budget, for every start a∈R. These include the predecessor masks and weights of every possible next element in the linear extension.
4. The positive weights bound the depth by n−a. Finite branching and finite depth prove termination. A target witness has a first prefix with at least the target number of down-sets, and is found there.

No poset isomorphism pruning or sum-only memoisation is assumed. Caching identical (n,R,threshold) decision problems is allowed because they are literally the same problem. A no-tree has at least 2^|R|−1 valid nodes: each nonempty subset of R supplies the distinct chain state with a its least rank and successive weights the rank differences (unless R empty, when zero nodes are required).

## 3. Certificates

A no-certificate binds n, the full word, colour, and threshold. It lists every root a∈R and a preorder traversal of the search tree. Each node lists all (I,w) branches. An invalid branch records a down-set D containing I for which a+w(D)+w∉R. Each valid branch has its complete child subtree. Exhaustion at the coordinate budget is a valid leaf. The separately written checker reconstructs the poset from the path, enumerates its down-sets from the predecessor relation, verifies all branch labels and invalidity witnesses, rejects nodes at or above the threshold, checks all roots and end of file. Thus deletion of a subtree or alteration of a label cannot be accepted. The expected word is an external checker argument, so a changed word in the header is rejected as well.

Positive certificates are actual distinct coordinate masks, all within [n], all of the stated colour, with at least the threshold members. Checking every pair's bitwise union and intersection directly proves the claim, without trusting the weighted-poset search or reduction for positive witnesses.

## 4. Word symmetries and pruning

Colour swap only exchanges the two maxima. Set complementation is a bijection on 2^[n], exchanges unions with intersections, and sends rank k to n−k. It therefore proves reversal symmetry. A canonical word is the least of W, complement(W), reverse(W), complement(reverse(W)); one may keep one representative and transport witnesses by complementation and/or relabelling colours. The witness transformation for reversal is S↦((1<<n)−1) xor S.

A colour appearing in r ranks contains an r-member chain, using the prefix sets [k] at those ranks. Therefore a word with a class larger than T is rejected with that chain as an explicit witness.

Factor monotonicity: if V=W[s:s+l], a family in 2^[l−1] with rank word V embeds via S↦[s]∪{s+i:i∈S}, using fresh coordinates after the first s. This preserves both operations and increases every rank by s. Its family size is unchanged. In weighted-poset terms replace a by a+s. Therefore a witnessed failure of a prefix or any contiguous factor is a witnessed failure of every extension. Prefix branch-and-bound is permitted only on such explicit failures. Class-size prefix pruning is the same argument using a chain witness. Symmetry elimination must still cover every full word by its orbit; symmetry is not used to remove arbitrary intermediate prefixes.

A screening catalogue may reuse an explicit family whenever its member-rank set is a subset of the current allowed rank set, on the same n coordinates. Its operations and cardinality are unchanged, so direct closure and membership checking certify every such rejection. This does not infer a no-result or remove any unexamined search branch.

## 5. Chain-exchange lemma and odd lower bounds

Let n be odd and m=(n+1)/2. Suppose a colouring has no monochromatic closed family larger than m. Any maximal chain has 2m members. Each colour's subchain is closed, so each colour occurs exactly m times in every maximal chain.

For k-sets S,T differing by one exchanged element, extend S∩T⊂S⊂S∪T and S∩T⊂T⊂S∪T to maximal chains identical at all ranks except k. Equality of colour counts forces χ(S)=χ(T). Any two k-sets can be joined by repeatedly replacing an element of S\T by one of T\S, reducing |S\T| each time. Thus all k-sets have one colour, for every k. The colouring is size-only, and its rank word is balanced.

Consequently, if every balanced rank word of length n+1 has an explicitly checked monochromatic closed family of at least m+1=(n+3)/2, the assumption is impossible and f(n)≥m+1. This proves only that lower bound; it cannot upgrade it when the rank minimum is larger, because the rigidity hypothesis was ≤m.

## Credits and scope

Erdős and Ulam posed the problem. The published lower bounds belong to Bhattacharjee–Mandal–Bhattacharya; the omega-institute note gives the general odd lower bound with the same rank-rigidity route. Birkhoff's representation theorem supplies the reduction. The n=13/14 referee job identified this weighted-poset search; the pre-launch review supplied the missing positivity argument, the four-part completeness argument, and certificate requirements. This job's implementations and the referee's are separately written within the same lane, not an additional clean-room review. All conclusions remain candidate and unrefereed.

## 6. Published-source lower bounds and dependency review

Source distinction: arXiv:2610.02833v1 (2 October 2026) contains the chain lower bound and asks whether its ceiling is always sharp. The public GitHub manuscript at commit 2842ef3a (14 October 2026), fetched in this job, is substantially revised: `prop:flower` and `thm:f20` are in that manuscript, not the arXiv v1 text. We cite the actual revised source, not the older arXiv version for these improvements. No journal refereeing was established.

The dependency chain for `prop:flower` was read lemma by lemma:

- L1–L3: chains are closed, separated sublattices can be concatenated because cross-pairs are comparable, and products on disjoint blocks preserve both operations and multiply cardinalities.
- `lem:adjacent`: connect equal-size sets by exchanges and choose oppositely coloured adjacent sets S,T. Outside their shared missing rank a common chain has m members; adding S to its red part and T to its blue part gives m+2. The two colour families need not be closed jointly: each is separately a subchain, which is sufficient.
- `lem:gadgets`: each of the eight displayed products of weighted chains has all ranks of one colour and strictly more members than that colour's occurrence count in the block. Their rank multisets and counts are direct sums/products; disjoint blocks establish closure. We also compute these eight families directly in producer/n15n20/src/lower_review.py.
- `lem:words`: the hand run-length proof forbids 111 and 212 internally, the listed five-entry patterns, four consecutive length-two runs, and the endpoint exception. If inner 1-runs separate 2-runs, their total length is six, too short. Otherwise the possible inner totals ≥8 force either three consecutive 2-runs with forbidden endpoints or the forbidden two-2-run endpoint pattern. We additionally enumerate all 4,096 words of length twelve to check coverage by the eight patterns and their reversals/swaps. This is a finite confirmation of that lemma, not a new result.
- `lem:window`: a mixed rank uses `lem:adjacent`; pure ranks use a forbidden block and its gadget. Embed that gadget into the interval and append same-coloured chain members outside; these are comparable to every gadget member. The gadget gains at least one member over that colour's chain count. The other colour's chain gives total at least thirteen.
- `prop:flower`: put q eleven-coordinate windows at rank intervals [12j,12j+11]. They are disjoint intervals of ranks with a separating coordinate, so each colour's window families concatenate. The remaining n+1−12q chain members give a red–blue total 13q+n+1−12q=n+1+q. One colour has at least its half-ceiling. This supplies 9,9,10,10,11,11 in our six dimensions.

Our exhaustive balanced-word witnesses and the chain-exchange lemma give the odd lower bounds at 15,17,19 without relying on these manuscript lemmas. The even lower bounds at 16 and 18 are the chain argument alone.

At n=20, `thm:f20` gives twelve. Its stacking argument is the same separated-window construction, now using a nineteen-coordinate window with red–blue total twenty-two, plus the remaining rank (twenty-three in total at n=20). We read `lem:window20`: mixed ranks outside 8..11 are disposed of by a pivot and `prop:flower`; mixed ranks inside that band reduce to pure lower/upper pivot subcubes unless another gain already exists. The residual mixed-level cases are asserted to be covered by a public computational check over 5,308,416 pure/mixed assignments and further pivot-colour choices, using 63,272 listed sublattices. **That external computational check was not rerun here.** The candidate equality f(20)=12 therefore uses the stated revised-manuscript theorem as a lower-bound dependency. Our complete rank-word rejection at threshold twelve proves the rank-colouring minimum is twelve; it does not itself prove the unrestricted lower bound twelve. If that manuscript theorem is withheld, this job gives 11≤f(20)≤12.


### Packaged dependency status

The clean-room referee subsequently replayed BMB’s authors’ checker at [2842ef3a58604a8f4b35271d5753c2bf9bdecd0b](https://github.com/anaxia-research/Erdos-1183/blob/2842ef3a58604a8f4b35271d5753c2bf9bdecd0b/checks/window20/check_window.c), including corruption controls, and read the reduction without finding a gap. This is a replay of the authors’ mixed-level case analysis, not a reimplementation. The exact recorded outcome and source hashes are in [WINDOW20.md](referee/n15n20/WINDOW20.md). No third-party checker or list is bundled. The lower bound f(20)≥12 uses [BMB `thm:f20` and `lem:window20`](https://github.com/anaxia-research/Erdos-1183/blob/2842ef3a58604a8f4b35271d5753c2bf9bdecd0b/paper/Erdos.tex); without that dependency, the packet establishes 11≤f(20)≤12. A rank minimum does not prove an unrestricted lower bound at even n. All conclusions are candidate, no human review.
