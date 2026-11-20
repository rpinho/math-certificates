# The two-block minimum in dimension 23

**Candidate computational theorem, no human review.** For every partition $[23]=A\sqcup B$, any colouring determined by $(|S\cap A|,|S\cap B|)$ admits a monochromatic family of at least 14 distinct subsets closed under union and intersection. The minimum in each split is 14. The unrestricted Erdős–Ulam function still satisfies $13\le f(23)\le14$.

The decisive calculation is in §5. Two coordinates outside a 21-dimensional face must contribute to one or the other colour. Accounting for them leaves only four rank words on the face shapes we need. Neighbouring faces cannot carry any pair of these words. There is also a separate, direct exclusion of the requested $21+2$ split in §4.

## 1. Sublattices and the two-block representation

Let $L$ be a nonempty sublattice of a Boolean cube. Put $m=\bigcap L$, $M=\bigcup L$, and let $P$ consist of the nonbottom join-irreducibles of $L$, ordered by inclusion.

**A. Coordinate labelling.** For $x\in M\setminus m$, let $j_x$ be the intersection of all members containing $x$. This nonempty intersection belongs to $L$ and contains $x$. If $j_x=Y\cup Z$, one summand contains $x$ and therefore contains $j_x$. Thus $j_x$ is join-irreducible. Each $j\in P$ has a unique lower cover $j_*$, the join of all its strict predecessors. That join is strict by finite join-irreducibility. For any $x\in j\setminus j_*$, we have $j_x\subseteq j$ and $j_x\nsubseteq j_*$, so $j_x=j$. The labels are surjective.

For $X\in L$, $x\in X$ exactly when $j_x\subseteq X$. By Birkhoff's finite distributive-lattice representation, the sets of labels below members of $L$ are precisely the ideals (down-sets) of $P$. Directly, unions of the irreducibles in an ideal give its corresponding member, using $m$ for the empty ideal. A join-irreducible in this distributive lattice is join-prime, since intersecting a union with it expresses it as a join. Consequently no unwanted label enters that union. An ideal $D$ represents $m\cup\{x:j_x\in D\}$. Distinct ideals give distinct members. The elements outside $M$ never occur.

**B. Vector weights and converse.** Give each $p\in P$ the two counts of its labels from $A,B$, written $w(p)$. Each vector has nonnegative entries and positive total. Let β be the counts of $m$. Feasibility is β plus the sum of the weights at most $(a,b)$ componentwise. The family has $|J(P)|$ members, one for each ideal, and its cells are

$$
   \left\{\beta+\sum_{p\in D}w(p):D\in J(P)\right\}.
$$
It has colour $c$ exactly when all those cells have colour $c$. Conversely, allocate disjoint coordinate blocks of the specified sizes after a base of size β. Unused coordinates are absent. Taking the unions of blocks in ideals, together with the base, gives an injective lattice embedding. Distinct ideals can occupy the same cell, which is why the member count is the number of ideals.

## 2. Witness and window lemmas

**C. Halving.** For a nonempty $P$, choose a maximal element and separate the ideals containing it from those avoiding it. Both parts are nonempty proper sublattices. If there are at least 28 ideals, the larger part has at least 14. Repeat on that sublattice until the size is 14 through 27. Thus the decision threshold is *at least* 14.

**D. Footprints.** Inclusion of set families implies inclusion of their sets of cells. A subfamily obtained by halving therefore gives a monochromatic prohibition at least as strong as the original one.

**E. Translation.** Each placement of a weighted poset with a new nonnegative base and enough remaining coordinates is realised by B. In concrete families one may discard all never-used coordinates and the common base, then insert new fixed coordinates to obtain any feasible translated footprint.

**F. Complementation.** Set complement interchanges union and intersection, preserves cardinality and sends cell $(i,j)$ to $(a-i,b-j)$. Globally swapping the two colours also preserves the problem. No lexicographic symmetry clauses are used in either DIMACS file.

**G. Windows.** Fix coordinates in and out. The remaining free coordinates form a cube under a union- and intersection-preserving embedding. Its grid is the corresponding translated subrectangle. In a $21+2$ grid, fixing one small-block coordinate absent gives rows 0,1. Fixing it present gives rows 1,2. Fixing both yields each individual row.

**H. Counting.** Ideals correspond bijectively to antichains through their maximal elements. The empty antichain, singletons and incomparable pairs give $|J(P)|\ge1+|P|+\operatorname{inc}(P)$. A linear extension gives a chain of $|P|+1$ ideals with strictly increasing total weight, hence at least that many footprint cells. There are at most 23 elements when the ambient dimension is 23.

## 3. Exact component dynamic programme

The graph with an edge for every incomparable pair splits $P$ into its ordinally indecomposable components. Between different connected components every two elements are comparable. An element outside a component must be on the same side of both ends of any incomparable edge, by transitivity. Walking along edges in each component shows the direction is uniform between two components. The components are therefore totally ordered, and their ordinal sum is $P$. The components are unique by graph connectivity. A component with $k>1$ has at least $k-1$ incomparable pairs. By H, a component in a witness of at most 27 members has at most 13 elements.

The ideals of an ordinal sum are obtained by gluing the top of each component's ideal lattice to the bottom of the next. Their counts add with one subtraction per join. In the grid, fix the canonical set at $(x,y)$ to be the first $x$ coordinates of $A$ and the first $y$ of $B$. Start a singleton family at every cell of the requested colour. For every monochromatic indecomposable component placement from $s$ to $t$, update

$$
  h(t)\gets\max\{h(t),h(s)+|J(C)|-1\}.
$$
Each component fits in the coordinates between its canonical endpoints. All elements of the preceding family are contained in all elements of the new one. Their union is closed with precisely one common member. A larger prefix ending at the same cell can thus always replace a smaller one. Row-major cell order is topological, because both coordinates are nondecreasing and at least one increases. The maximum over all endpoints allows arbitrary base and top.

**Completeness of the component generator.** Any finite poset with connected incomparability graph has a linear extension whose nonempty prefixes have connected incomparability graph. Start with any minimal element. If every remaining minimal element lay strictly above *every* prefix element, the entire remainder would lie above the entire prefix. This would disconnect the graph. Hence one available minimal element is incomparable with some prefix element and may be added. Conversely every such addition preserves connectivity.

To add an element choose its strict predecessor ideal $I$ in the current prefix, and choose any feasible nonzero vector weight. The new ideals are the old ones and the supersets of $I$ with the new element adjoined. After the first element exclude only the choice $I=\text{entire prefix}$, which would give no new incomparability edge. The generator carries the actual coordinate sets of the ideals. The last one is always the top. It tests each newly created cell before descending. An old ideal remains an ideal of any later extension, so a colour failure is permanent. This enumerates every necessary connected component, and the dynamic programme combines every needed ordinal sum. Feasibility bounds the depth. Sections 1–3 prove both soundness and completeness for every supported grid, regardless of the tests.

The implementation returns a family upon first meeting a requested threshold. If it exhausts the search it returns a true maximum. A threshold of $2^{a+b}+1$ requests an exact maximum outright. A single decision proof of absence at $h+1$, together with an $h$-family, also gives the exact value. The proof of either exclusion below needs only validity of the concrete rejection families.

## 4. Direct certificate for the 21+2 split

Let $W$ consist of the 22-letter rank words on 21 coordinates with both maxima at most 13. Let $V$ be the ordered pairs of words forming an admissible 21+1 grid on 22 coordinates. For every stored physical family forbid the two monochromatic assignments on its footprint. A positive clause forces a 1, and its negative counterpart forces a 0.

The row witnesses remove every word containing one of their monochromatic rank patterns. Exhausting the binary array leaves 1,198 rows. Applying the two-row witnesses to the Cartesian square leaves 28 ordered windows. Membership in these sets was also checked positively by exact search for both maxima. All 28 windows equal a rank word restricted to the two rows. Four paths of length two survive the common-middle-row condition. Each has a stored family of exactly 14 in dimension 23.

**Table-selector lemma.** In each adjacent window introduce one Boolean selector per surviving pair. Require at least one selector and require each selected pair's 44 cell values. Any valid grid extends to these auxiliary variables by selecting its actual pair, by G and the two coverage calculations. No uniqueness axiom is needed. Thus UNSAT for the physical clauses and table clauses excludes every valid grid. The checker checks the distinct subsets and every binary union and intersection of the 146,641 physical families. It builds its own binary and pair arrays, checks the four paths and regenerates the complete DIMACS. A fresh LRAT proof is checked separately.

## 5. Exterior colour counts and the all-splits certificate

For a local rectangle of shape $(u,v)$ let $d=u+v$, $t=23-d$. Write $H_c$ for its true monochromatic maximum, zero for an absent colour. Define a context by the integer $z\in[0,t]$. A local table is admissible in this context if

$$
    H_0+z\le13,\qquad H_1+(t-z)\le13.                         \tag{1}
$$

**Exterior-chain lemma.** In any face of a putative value-13 colouring, take a chain from the empty set up to, but excluding, the face bottom. Then take a chain from just above the face top to the full set. With one coordinate changed at a time these give exactly $t$ outside sets. Each is strictly comparable with every face member, and all outside sets are mutually comparable. Add the outside sets of colour $c$ to a largest inside family of colour $c$. This gives a closed family of size $H_c$ plus their count, also when $H_c=0$. Taking $z$ to be the exterior zero count proves (1). In particular $H_0+H_1\le d+3$. Recording the two counts individually gives a stronger necessary condition.

**Canonical physical witness for (1).** Identify the $d$ local coordinates with the first $d$ bits, $A$ first. Use as exterior sets the prefixes $[d+1],\ldots,[23]$. Give the first $z$ prefixes colour zero and the rest colour one. A closed family consisting of local sets and these exterior sets is a genuine set system in $2^{[23]}$. To pass from the canonical arrangement to the actual face, embed the local sets in that face and select equally many exterior sets of the same colour on its outside chain. The union with the local family remains closed, since every cross pair is comparable. Counts and distinctness are preserved. If a witness contains only exterior sets, the same argument uses the chain alone. Thus a checked canonical witness of size 14 or more forbids its local monochromatic pattern in context $z$. This argument requires the checked exterior sets to have one colour. It places no condition on their order in the actual cube. When checking an arbitrary canonical witness, its local members are themselves closed, since their unions and intersections remain in the local cube.

**Induction lemma.** Split a nontrivial rectangle along one free coordinate into its two translated child windows. If the parent is admissible in context $z$, the lower child must be admissible in context $z+[\text{parent top is zero}]$. Its extra exterior set is the parent top. For the upper child the extra set is the parent bottom, giving context $z+[\text{parent bottom is zero}]$. These additions are strict and preserve closure by comparability. The argument applies to both colour inequalities. The two child patterns must agree on all cells of their intersection. Width-one branches can have an empty overlap, in which case all pairs are tried.

Start with the two one-cell patterns and all contexts. Build rank rows from their left and right windows, then build rectangles from lower and upper windows. Join every pair allowed by the preceding lemma in its appropriate context. Reject a join only if a stored canonical physical set family has one colour under the pattern and its exterior. By induction the surviving tables contain every admissible one. Any superfluous survivor could only weaken the exclusion. The producer also exhausted the exact finder on survivors. The separate checker derives its own candidate sets from scratch, using integer grids and a bit mask of possible exterior counts, and directly tests every supplied witness. It requires neither the producer's tables nor its finder.

The certificate covers the 22 rank shapes $(u,0)$ for $0\le u\le21$, and $(u,v)$ for $12\le u\le20$, $1\le v\le21-u$. At dimension 21 the ten terminal shapes are $(12,9),(13,8),\ldots,(21,0)$. On **each**, only context $z=1$ survives, and the tables are precisely the rank embeddings of

```text
0010011100101100011011
0011001011100010110011
1100110100011101001100
1101100011010011100100
```
These four words have no suffix of length 21 equal to a prefix of length 21 in the list, including their own. Their earlier certified colour maxima are 12/12, so all four do meet (1) at $z=1$.

**Covering every split.** Relabel blocks so $a\ge b$, $a+b=23$. For $b=0,1,2$ shorten the $A$ axis by two. For $3\le b\le11$ shorten the $B$ axis by two. The resulting 21-dimensional shape is one of the ten above, and the shortened axis still has at least one free coordinate. Take two windows of that shape, at offsets 0 and 1 along that axis, realised by fixing two coordinates. By the exterior-chain lemma their tables must both occur in the four-word list. Their overlap sees *every* rank from 1 to 21 in the first window, corresponding to ranks 0 through 20 in the second. For example, after translating the second window up one row, the common rows are 1 through the last row of the first window, for all horizontal indices. The argument for columns is identical. Equality on the overlap would give a matching suffix and prefix, which is impossible.

**Final disjunction and selector lemma.** The all-splits DIMACS chooses at least one of the twelve splits (including the all-rank case). Each has its own grid variables. For each chosen split and each of its two windows, a disjunction requires a selector for one of the certified terminal patterns. Each selector implies every cell value of that pattern. A valid colouring would satisfy this formula by taking its split, actual cells and actual window patterns, with the other selectors false. Conversely, the two imposed patterns always disagree in the overlap. The root SAT instance uses only these table implications, the two conditional disjunctions per split and the split disjunction. All local eliminations are justified by the separately replayed physical-witness induction. The root LRAT proof certifies the resulting finite incompatibility calculation. The direct overlap test also checks it without SAT.

Finally the earlier rank word `001001110010110001101101` defines the table $C(i,j)=w_{i+j}$ in every split. Both maxima are exactly 14, by its explicit families and the separately replayed no-at-15 trees. This proves attainability as well as exclusion, with no use of the unrestricted lower bound. The producer wrote the certificate checkers separately from the search. The clean-room AI referee confirmed the result with its own checkers. Human review remains open. [Referee report](../../referee/two-block/REFEREE.md)

**Attribution.** Erdős and Ulam posed the problem. The manuscripts of Bhattacharjee–Mandal–Bhattacharya and of Bhattacharjee–Bhattacharya (BLLM) give the earlier bounds and constructions. Bhattacharjee and Bhattacharya posed the (21,2) two-block search using lazy witness clauses in their eBLLM experiment. [Prior art](../../PRIOR_ART.md) Birkhoff supplies the representation theorem. The earlier rank and one-pivot rounds supply the scalar control and physical prefix witnesses. The pre-launch review supplied the component decomposition, threshold reduction, window strategy and certificate requirements. The exterior-count induction above uses those windows to cover the remaining splits.
