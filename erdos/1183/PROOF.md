# Proof of the finite equalities

Write M(χ) for the largest cardinality of a nonempty monochromatic family of subsets closed under binary union and intersection. Then f(n)=minχ M(χ). The minimum includes every colouring of all subsets. Rank colourings below are particular constructions giving upper bounds, not a restriction on that minimum. Families of more than eight members must also be excluded; the queries therefore ask for at least eight, not exactly eight.

## Lower bounds

At n=12, restrict any colouring to the thirteen prefixes ∅,{1},...,{1,...,12}. At least seven have one colour. Their union and intersection are their maximum and minimum in the chain, and thus still belong to that colour's selected subchain. This proves f(12)≥7 without prescribing ambient endpoints.

At n=11 the published Bhattacharjee–Mandal–Bhattacharya bound gives f(11)≥7. The first referee independently reproduced the needed finite argument in [published_lower.py](referee/n11/published_lower.py) and explains the arbitrary-colouring reduction in section (c) of [REFEREE.md](referee/n11/REFEREE.md). Here are its steps.

If a colouring had no monochromatic closed family of seven members, each twelve-member maximal chain would have six members of each colour. Two chains can differ only in one r-subset, obtained by exchanging one element. Their colour counts force those two r-subsets to have the same colour. The exchange graph on each rank is connected, so every rank is monochromatic. It suffices to rule out balanced twelve-bit rank words.

The referee verifies the omega note's explicit construction for all balanced words: 924 possibilities, of which 874 admit a diamond on three consecutive occurrences of one colour with equally spaced ranks; ten explicit closed families cover the remaining 50. If a<b<c are such consecutive ranks and a+c=2b, let P_r={0,...,r−1}. Add P_a∪{b,...,c−1} to the six prefixes of that colour. It has rank b, forms a diamond with P_a,P_b,P_c, and is comparable with the remaining prefixes. This is a closed seven-member family. The residual families in the script are separately checked by set operations. The same script also checks the current BMB paper's eight product-of-chains gadgets against all 4096 rank words. Thus the lower bound is for arbitrary colourings, not only rank colourings. These are reproductions of published lower bounds.

## Producer membership CNF, both dimensions

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

If a counterexample family exists, choose the lexicographically least membership vector in its finite coordinate-permutation orbit. It satisfies every transposition comparison. Extend its counter variables by actual prefix counts. This proves that the augmented CNF is satisfiable if and only if a counterexample family exists, although individual labelled counterexamples may be removed by symmetry. check_lex.py independently reconstructs the comparisons and checks that the base clauses are preserved.

The n=11 queries and the n=12 colour-one query need no such symmetry argument. DRAT checking of the four retained producer proofs establishes UNSAT of their exact CNFs, hence both upper bounds. ASSETS.json binds the exact CNF and proof hashes. The unfinished n=12 base colour-zero proof is excluded.

## Independent referee encodings and non-SAT argument

The first referee's encode.py uses an exact prefix-count equivalence, with all implications, rather than the producer's one-direction counter. The second referee's ref.py uses a truncated tree totalizer: a node output o_j means count at least j. For child outputs a,b it adds ¬o_(i+j+1)∨a_(i+1)∨b_(j+1), omitting nonexistent child outputs, and asserts root o_8. If the child counts are u,v and a true output had index greater than u+v, the clause for i=u,j=v would fail. Induction proves soundness. Assigning every output its actual subtree threshold count proves completeness. Closure clauses have the same direct set interpretation as above. The referee's plain queries cover both colours without any symmetry clauses. Its interval queries additionally fix least and greatest family members and use the rank-invariant coordinate permutation described in its report. Original referee proof hashes remain historical records; release assets are the producer proofs, not those deleted referee proofs.

Both referees also gave weighted-poset upper checks. The n=12 implementation and its mathematical argument are in [ref.py](referee/n12/ref.py), [dfs_scan.py](referee/n12/dfs_scan.py), [dfs_control.py](referee/n12/dfs_control.py) and section (b) of its original report. For completeness, the structure argument is as follows.

A finite nonempty sublattice L has a least member B and greatest member T. For each x∈T\B let m(x) be the intersection of members containing x, which lies in L. Define x≼y when x∈m(y). This is a preorder. Every X∈L is B∪⋃_{x∈X\B}m(x); conversely, every down-set D of the preorder gives B∪D∈L by taking that union (or B for the empty down-set). Collapse equivalent coordinates to blocks: the quotient is a poset with positive integer block weights and total weight at most n−|B|. The ranks in L are exactly |B| plus the weights of its ideals.

The DFS enumerates the offset |B| and builds every such weighted poset by adding one maximal element at a time in a linear extension. Its predecessor set can be any ideal D of the previous poset. New ideals are I∪{new} for previous ideals I containing D; previous ideals remain. Thus any wrong-colour ideal already present can never be repaired, making pruning exact. The DFS stops growing a branch once it has at least eight ideals; such a branch already disproves the desired upper bound. On the supplied word both colours have maximum seven, so no branch reaches eight. This exhaustive integer/set computation proves the upper bound without SAT. The first referee separately enumerated natural-labelled posets with at most five elements, justified by the six-member longest monochromatic chain at n=11; its rank_lattices.py obtains the same maxima.

The second referee's controls compare all rank words at n=4 with brute-force sublattice enumeration and scan dimensions through twelve. The scan is only over rank colourings; it is not an unrestricted lower-bound proof. The chain lower bound supplies the unrestricted n=12 conclusion.

## Scope

Combining the lower and upper bounds gives f(11)=7 and f(12)=7. These are conventional computational candidate proofs supported by two supplied clean-room AI referee verdicts HOLDS. The mathematical encoding and symmetry arguments are not kernel formalizations, drat-trim is not a formally verified checker, and there has been no human review. Priority searches have the limits recorded in PRIOR_ART.md and the original referee reports.
