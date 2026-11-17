# Exact statement and separately written checks (same agent)

For each total two-colouring χ of all subsets of [n], M(χ) is the maximum size of a nonempty monochromatic family closed under binary union and intersection. The function is f(n)=minχ M(χ). Endpoints ∅ and [n] are not required to belong to a family. A singleton is allowed.

The membership CNF has one y_S for each set in the queried colour. For every unordered incomparable pair S,T, it has ¬y_S∨¬y_T∨y_(S∪T) and ¬y_S∨¬y_T∨y_(S∩T). If a result has the other colour, its positive literal is omitted. Comparable pairs are tautological. The closure clauses are exactly the binary-closure conditions, including duplicate clauses where both results are forbidden.

The target is **at least nine**, not exactly nine. Prefix node A(i,j) has the one-way meaning that at least j of the first i member variables are true. Its backwards recurrence is A(i,j)⇒A(i−1,j)∨(y_i∧A(i−1,j−1)); A(i,0)=true and impossible indices=false. The two distributed clauses encode this implication. The unit A(N,9) forces at least nine members by induction. Conversely any actual family of size ≥9 extends to all these clauses using the true prefix counts. Larger families are included.

For rank colourings, every ground-coordinate permutation preserves colour, cardinality, union and intersection. Member variables are ordered by increasing integer bit mask, false before true. We add the standard lexicographic inequality y≤π(y) for every coordinate transposition. Every orbit of counterexample families has a global lexicographically least member vector; it satisfies all these comparisons. Its counter auxiliaries can be recalculated. This proves equisatisfiability with the base family query; it does not require the chosen generators' local minima to be global minima.

For a transposition, omit fixed positions and retain each exchanged pair only at its earlier position. The first differing coordinate must be such an earlier endpoint. With p_0=true, the clauses for a pair (a_i,b_i) are

    ¬p_(i−1) ∨ ¬a_i ∨ b_i
    ¬p_(i−1) ∨ ¬a_i ∨ ¬b_i ∨ p_i
    ¬p_(i−1) ∨  a_i ∨  b_i ∨ p_i.

Equal bits force the next prefix true as long as previous pairs were equal. At the first difference, 1>0 is forbidden; 0<1 permits all subsequent prefixes to be false. Thus these clauses extend exactly when the lex inequality holds. check_statement.py exhausts the comparator recurrence through length four, and this induction proves the general case.

check_statement.py was written separately in this job by the same agent, with no encoder imports. It creates frozensets, derives the permitted member list from rank colours, reconstructs every closure clause by actual set union/intersection, reconstructs all prefix-counter clauses, and reconstructs every lex clause by actual set permutations. It compares the entire clause sequence, variables and clause count, so it cannot pass a formula with an extra or missing clause. This is separately written checking, never independent verification. Its mathematical arguments are not formalised; drat-trim is not a formally verified checker.

For n=13, the chain lower bound is only seven, but the public omega/BMB bound is eight. We also check this finite case directly: assuming every monochromatic lattice has size ≤7 forces every maximal chain of 14 subsets to have exactly seven of each colour. Two maximal chains differing only at one rank force their two sets at that rank to have the same colour. Single-element exchanges connect all sets of a given size. Therefore the colouring depends only on rank. check_rank_screen.py checks actual frozenset witnesses for all 8,192 colour-swap representatives of the 16,384 rank words, including all 1,716 representatives of balanced words. Each has a monochromatic lattice of size ≥8, a contradiction. The initial rank screen is merely a cheap finite construction; this rigidity argument supplies the unrestricted conclusion. This reproduces a published lower bound, not a new lower bound.

For n=14 the ordinary maximal chain has 15 members. Its larger colour class is a monochromatic subchain of at least eight members; every subchain is closed under union and intersection. Thus f(14)≥8 for arbitrary colourings.

check_coloring.py separately checks the full colouring against the rank formula and both CNF member lists; it verifies the explicit family and chain by original set operations. check_control.py confirms one actual closure clause was deleted, every other clause is unchanged, the deleted clause is false under the model, and every remaining clause is true. It also reconstructs the selected actual sets and confirms exactly one missing closure implication.
