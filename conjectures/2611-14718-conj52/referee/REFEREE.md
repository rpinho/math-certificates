VERDICT: HOLDS WITH CAVEATS

# Conjecture 5.2 fails first at 15 vertices

There are exactly three non-isomorphic counterexamples at order 15. One is a tree and the other two are unicyclic. Each has maximum degree three. At threshold 6 all three have sequential CDF $64/3375$ and static CDF $1/55$. In the paper's order the sequential CDF must be the smaller one. The reduced cross-product difference is $64\cdot55-3375=145>0$, giving an exact gap of $29/37125$. An independent enumeration found zero counterexamples among 358,891 connected graphs through order 14 and three among 1,016,740 at order 15. Corollary 6.3 covers the disconnected cases. [Census](census.txt) · [Witness computations and vertex bijections](verification.json)

Two corrections affect the certificate and its description. The tree's stored size-7 RSA numerator should be **7,993,019** in place of **7,993,211**, over the same denominator 10,135,125. The submitted PMF sums to $1+64/3378375$. The report's size-7 *CDF* is correct. Also, both the tree and the triangle-containing graph are minimal under single vertex and single edge deletion. The tree is the unique 14-edge graph among the three. The threshold-6 calculation, both unicyclic mean reversals, and the sharp classification survive these corrections. [Submitted certificate](inputs/witness.json) · [Producer report](inputs/REPORT.md) · [Computed laws and deletions](verification.json)

## What the paper says

[Verbatim TeX excerpts](PRIMARY_SOURCE.md) give the full probabilistic definitions, Definition 2.1, the complete degree-four subsection, Conjecture 5.2 and Corollary 6.3. Line references are to `arxivV2.tex` inside the [supplied archive](inputs/2611.14718v2.tex.json.gz).

- Lines 72–101 define the process on a finite simple graph. The static measure gives each **maximal** independent set mass $1/|M(G)|$. The sequential measure chooses uniformly from all available vertices at each step and removes the chosen vertex and its neighbors. Occupancy counts the chosen vertices at jamming.
- Lines 107–117 require $F_{\rm stat}(k)\ge F_{\rm seq}(k)$ at every integer $k\ge0$ for sequential dominance. Strict stochastic dominance means weak inequality everywhere and different laws. Equality beyond the support is therefore expected.
- Lines 671–675 quantify over **every finite simple graph of maximum degree at most three**. The paper explicitly permits disconnected graphs. There is no minimum degree, regularity, acyclicity or cycle requirement. A tree and a graph with one cycle are both in scope.
- Lines 596–626 give a six-vertex example of maximum degree four. Lines 717–719 give the disjoint-union corollary. In the static model the maximal independent sets form a Cartesian product. In the sequential model the restrictions of a uniform random order to distinct components are independent uniform orders. Summing independent component occupancies preserves their common stochastic order.

## Laws from the raw edges

The verifier checked integer endpoints in $0,\ldots,14$, loops, repeated unordered edges, reachability, edge counts and degrees. To compute girth it removed each edge in turn and measured the shortest alternate path between its endpoints. The three topology triples $(|E|,\Delta,\text{girth})$ are $(14,3,\infty)$, $(15,3,5)$ and $(15,3,3)$. The respective counts of vertices of degrees 1, 2 and 3 are $(5,7,3)$, $(5,5,5)$ and $(6,3,6)$. Distinct edge counts and girths prove pairwise non-isomorphism. Explicit bijections also identify the first graph with the stated three-unit chain and the third with the three-unit ring. [Edge lists](inputs/witness.json) · [Computed topology and maps](verification.json)

Each graph has exactly 55 maximal independent sets. The table gives the complete laws. At omitted sizes the masses are zero. Below 6 the CDFs are zero, and above the largest displayed size for each graph they are one.

| Graph | Size | MIS count | Static PMF | Sequential PMF | Static CDF | Sequential CDF |
|---|---:|---:|---:|---:|---:|---:|
| CE#1 | 6 | 1 | 1/55 | 64/3375 | 1/55 | 64/3375 |
| CE#1 | 7 | 50 | 10/11 | **7993019/10135125** | 51/55 | 8185211/10135125 |
| CE#1 | 8 | 4 | 4/55 | 1949914/10135125 | 1 | 1 |
| CE#2 and CE#3, each | 6 | 1 | 1/55 | 64/3375 | 1/55 | 64/3375 |
| CE#2 and CE#3, each | 7 | 54 | 54/55 | 3311/3375 | 1 | 1 |

The tree's CDFs cross. At 7 the sequential CDF is strictly below $51/55$, so neither model dominates globally. Its sequential and static means are $72703597/10135125$ and $388/55$. Each unicyclic graph has support $\{6,7\}$. The static CDF is strictly smaller at 6 and equal everywhere else, hence $N^{\rm seq} <_{\rm st} N^{\rm stat}$. Its static mean $384/55$ exceeds its sequential mean $23561/3375$ by $29/37125$. These mean and CDF statements use exact fractions throughout. [Full CDFs at integers 0–15](verification.json)

### Counting the two unicyclic laws by hand

On CE#3 the cycle is the triangle $(0,1,2)$. At each cycle vertex the off-cycle branch consists of a hub, its other leaf, and its pendant pair $a,b$. Each branch contains two occupied vertices. If the cycle vertex is selected, the branch has two completions. If the cycle vertex is unselected and has a selected cycle neighbor, the branch has three completions (one with its hub selected and two with its other leaf selected). If the cycle vertex needs its branch to dominate it, its hub is forced and the branch has one completion. With the triangle empty there is one size-6 set. With one triangle vertex selected there are $3\cdot2\cdot3^2=54$ size-7 sets.

On CE#2 write the five-cycle in the supplied labels as $(c,p,q,r,s)=(4,2,0,1,3)$. Vertices $q,r$ each carry the branch just described, and $c$ carries the pendant path $4-7-12$. Exactly five off-cycle vertices are occupied in every maximal independent set. Vertices $p,s$ have no off-cycle neighbor. Thus a singleton on the cycle must be $c$ to cover both, and it gives one size-6 set. Every independent pair on the cycle dominates the cycle. Pairs $\{c,q\},\{c,r\}$ have 6 completions each. Pairs $\{p,r\},\{q,s\}$ have 12 each, and $\{p,s\}$ has 18. The total is again 54 size-7 sets.

In both graphs the unique size-6 set consists of the three unit hubs and their three pendant tips. Reinstating the inter-unit leaf edges preserves this final set exactly when each isolated unit produces its own hub and tip, by the arrival-order argument for the tree below. The probability is $(4/15)^3$ in each graph. This recovers the two full unicyclic laws directly from the edge lists.

### A hand calculation of the disputed numerator

There are four size-8 sets on the chain. Both end hubs are absent, both hub leaves at each end are occupied, and each end independently contributes one of its pendant pair $a,b$. The central hub and its pendant leaf $b$ are occupied. For a fixed independent target, greedy produces exactly that target if and only if every outside vertex arrives after at least one of its target neighbors. This follows by scanning arrival times in order.

Condition on central hub time $x$, and write $s=1-x$. Averaging over the central pendant leaf's independent time gives probability $(1+s^2)/2$ of blocking the central $a$. At either end let $t$ be the arrival time of the occupied leaf nearest the central unit, and set $u=1-t$. Conditional on $t$, the probability of blocking the end hub and the unselected pendant vertex, summed over the two choices of selected pendant vertex, is
$$
 f(u)=\frac{3+u^4}{8}+\frac{1+u^2}{4}.
$$
For the first term the selected pendant vertex is $a$ with arrival time $z$. Its leaf must arrive after $z$, and the hub must arrive after the earliest of $t,z$ and the other occupied leaf. Averaging the product gives $1/2-\int_0^t(1-w)^3\,dw/2=(3+u^4)/8$. For the second term $b$ is selected, so the pendant pair has its required order with probability $1/2$, and the hub is blocked by the earlier of its two leaves.

The unselected central leaf adjacent to this end must also arrive after the earlier of $x,t$, with probability $\max(s,u)$. Each end thus contributes
$$
 G(s)=\int_0^1\max(s,u)f(u)\,du
     =\frac{95+75s^2+5s^4+s^6}{240}.
$$
Conditional on the central hub time the two ends and the central pendant pair use disjoint arrival variables. Consequently the size-8 probability is
$$
 \int_0^1\frac{1+s^2}{2}G(s)^2\,ds
   =\frac{1949914}{10135125}.
$$
The size-6 probability is $(4/15)^3$ by the unit argument below. Subtracting both masses from one gives **7993019/10135125** at size 7. This calculation uses only the tree construction and independent uniform arrival times. The verifier also integrates the displayed polynomial term by term in exact rationals.

### Single deletions

Each entry counts deletions restoring the conjectured order at **every** threshold. Disconnected results were evaluated on all remaining vertices, including isolates.

| Graph | Vertex deletions restoring order | Edge deletions restoring order | Disconnected vertex / edge deletions |
|---|---:|---:|---:|
| CE#1 | 15/15 | 14/14 | 10 / 14 |
| CE#2 | 15/15 | 14/15 | 8 / 10 |
| CE#3 | 15/15 | 15/15 | 9 / 12 |

The sole surviving violation is CE#2 minus edge $(0,1)$, which is isomorphic to CE#1. For CE#3, any further deletion after removing an edge leaves at most 14 vertices or at most 13 edges on 15 vertices. In the second case the graph is disconnected and all components have order below 15. Thus the triangle example also refutes uniqueness under the stronger proper-subgraph interpretation of minimality. [All 89 deletion results and the edge-deletion bijection](verification.json)

## Independent verification and controls

The pure-Python calculation visits independent sets in increasing vertex-label order, accepting a set when its closed neighborhoods cover all vertices. It conditions RSA on the first available vertex and averages the residual laws with `fractions.Fraction`. Independent residual components are convolved. As a second calculation on the witnesses, it checks all $2^{15}$ subsets for independence and domination, then sums the paper's sequence probabilities separately for each final set. Prefixes with the same occupied subset can be combined because they leave precisely the same available vertices. On all three graphs the resulting size laws agree, including every numerator of the corrected tree law. [Verifier](referee_verify.py) · [Results](verification.json)

| Control | Full permutations | Static size counts | Sequential PMF |
|---|---:|---|---|
| Three-vertex path | 6 | 1→1, 2→1 | 1→1/3, 2→2/3 |
| Four-vertex path | 24 | 2→3 | 2→1 |
| Triangle | 6 | 1→3 | 1→1 |
| Seven-vertex tree | 5,040 | 3→4, 4→2 | 3→52/105, 4→53/105 |
| Paper's six-vertex graph | 720 | 2→1, 3→4 | 2→5/24, 3→19/24 |

These were run before accepting any witness calculation. The random-order control scans each permutation directly, records the occupied set and compares every size probability and distinct-set count. The paper's example violates the CDF inequality at 2 but is rejected by the subcubic guard. [Control definitions and permutation loop](referee_verify.py)

The mutation tests began from an otherwise consistent in-memory copy with the corrected size-7 field. All seven mutations were rejected. These comprised dropping edge $(0,1)$, adding edge $(0,4)$, changing the threshold probability, adding a loop, duplicating a reversed edge, using endpoint 15, and changing the size-7 mass. The added edge retains a genuine violation $6229/108000>3/59$ at 6. Its maximum degree of four is what excludes it. The submitted certificate itself fails strict checking on the size-7 mass. Its SHA-256 is `989e25338840e3b6fc084f285af950e0ba5e1ca00a23348782fe419cff9cba30`. [Mutation tests and strict checking](referee_verify.py)

## Why the census is exhaustive

The C++ generator starts at one vertex. For every larger connected subcubic graph, the following inverse operations decrease its order or, in the cubic case, its edge count at fixed order.

1. If there is a leaf, delete it. The inverse attaches a new leaf to any vertex of degree below three.
2. With minimum degree two and a degree-two vertex $v$, let $u,w$ be its distinct neighbors. If $uw$ is absent, suppress $v$ and add $uw$. This leaves a connected simple graph with the old degrees on all surviving vertices. The inverse subdivides the edge. If $uw$ is present, delete $v$ and retain $uw$. The inverse adds a common neighbor to the ends of that edge. Any leaves of this parent must be among $u,w$.
3. A cubic graph has a cycle. Removing one cycle edge leaves a connected graph of the same order with exactly two degree-two vertices, which is already generated in step 2. Joining the two deficient vertices restores the cubic graph. Cubic graphs have even order.

All augmentations preserve simplicity, connectivity and the degree bound. At a fixed order, color refinement and individualization give an exact graph key. At a discrete partition the key records **every** adjacency bit. Otherwise the algorithm branches on every vertex of a deterministically chosen color class, retaining the least leaf encoding. It can skip a twin only when the transposition preserves the adjacency matrix and all current colors. Isomorphisms induce the same search up to renaming, and equal leaf encodings explicitly describe isomorphic graphs. Hashes index the table, and equality compares the full encoding. These facts and the parent construction prove completeness and uniqueness without assuming the producer's counts. [Generator and canonical form](referee_census.cpp)

The integer evaluator enumerates maximal cliques of the complement via Bron–Kerbosch for the static histogram. For RSA let $Q_H(k)$ count permutations of $s=|H|$ vertices yielding occupancy $k$. If the first vertex is $v$ and the residual graph $R=H-N[v]$ has order $r$, each residual permutation lifts to $(s-1)!/r!$ orders following $v$. Thus $Q_H(k)=\sum_v ((s-1)!/r!) Q_R(k-1)$, with $Q_{\varnothing}(0)=1$. The sequential denominator is exactly $s!$. All counts and cross-products are integral. At order 15 the maximum possible common denominator is bounded by $15!\,2^{15}<2^{56}$. Comparison of two such fractions fits signed 128 bits. The independent low-order control compared both full histograms to explicit subsets and permutations on all 307 connected subcubic graphs through order 8 and 200 separately seeded eight-vertex draws. All 16,230,879 order enumerations agreed. [Census code](referee_census.cpp) · [Control totals](census_controls.txt)

The census reproduces every order's connected, well-covered and violation counts in the producer's table, its maximum interior CDF gap, an attaining threshold and probability pair, and the maximum ratio to the printed precision. Every maximal independent set occurs with positive sequential probability because its members can arrive first. The two supports coincide, so checking thresholds strictly inside the static CDF covers all possible violations. The 794 well-covered graphs have identical one-point size laws. At order 14 the largest interior gap is $-1/2475$, from $4/225-1/55$ at 5. At 15 it becomes $29/37125$ at 6. All three census hits were matched to the raw certificates by full vertex bijections checked edge by edge. Every disconnected graph through 15 has components of order at most 14, so the sharp threshold and the three classes also describe the unrestricted finite-simple-graph question at these orders. The empty graph has deterministic occupancy zero. [Exact extrema and census adjacency masks](census.txt) · [Bijections](verification.json)

A second evaluator compared the full laws on **all 1,375,631** generated graphs, totaling **4,604,216 supported size bins**. Python independently counted the maximal independent sets from each adjacency list. For RSA, the generator identified the connected components remaining after each possible first vertex, using the canonical adjacency key on the actual induced graph. Python checked the residual order, convolved the component laws in exact fractions, shifted by one and averaged over first vertices. These equations uniquely fix every law by induction from the empty graph. All rows, including the lower-order rows used as induction hypotheses, agreed with the integer permutation counts. This additional calculation shares the graph generator and its isomorphism keys. The witness-level paper sum and arrival-time derivations above use the raw edge lists independently. [Fraction replay](referee_replay.py) · [Full comparison by order](census_replay.txt)

## The infinite tree family

Let $A_m$ be the number of maximal independent sets of the chain of $m$ five-vertex units, with $A_0=1$. Use the producer's unit consisting of hub $h$, leaves $L,R$ adjacent to $h$, and pendant path $h-a-b$. An inter-unit edge joins $R_i$ to $L_{i+1}$. This gives a tree of order $5m$ and maximum degree three. The following count supplies a derivation of the recurrence quoted in the producer report.

In each unit exactly one of $a,b$ belongs to a maximal independent set. If every hub is in the set, the result is the single set consisting of all $h_i,b_i$, of size $2m$. Consider a run of $t$ consecutive missing hubs. The two leaves at its ends are forced. At a chain boundary the leaf has only its missing hub as a neighbor, and at an internal boundary the next occupied hub excludes its own bridge leaf. Each of the $t-1$ internal bridge edges supplies one of its endpoints. Along with the $t$ pendant choices, this contributes $2t+1$ vertices. Thus $r$ runs give size $2m+r$, and only one set attains the minimum.

Let $W_t$ count the possibilities inside one such run. Orient each internal bridge toward its selected endpoint. Each unit has two pendant choices unless both incident bridge selections point away from it, in which case $a$ must dominate its hub. With bridges read left to right, this happens exactly at an $L,R$ transition. Hence $W_1=2$, $W_2=8$, $W_3=28$. For $t\ge2$ the orientation sum is
$$
W_t=4(1,1)\begin{pmatrix}2&1\\2&2\end{pmatrix}^{t-2}\binom{1}{1}.
$$
The two end units supply the factor four. The matrix has trace 4 and determinant 2, giving $W_t=4W_{t-1}-2W_{t-2}$ for $t\ge4$ and also at $t=3$ by the initial values. Consequently $W(z)=2z/(1-4z+2z^2)$. A chain starts with an occupied hub or with a run of missing hubs, which either ends the chain or precedes an occupied hub. Including the empty chain, its generating function obeys $A=1+zA+W(1+zA)$. Therefore
$$
 A(z)=\frac{1-2z+2z^2}{1-5z+4z^2-2z^3},\qquad
 A_m=5A_{m-1}-4A_{m-2}+2A_{m-3}\quad(m\ge3).
$$
This gives $1,3,13,55,229,951,3949$. For three units the missing-hub subsets contribute 1 with no missing hub, 6 with one missing, 4 with only the middle hub present, 16 with two consecutive missing, and 28 with all three missing. Grouping by size yields $1,50,4$ as computed from the edges.

For RSA, a single unit ends at $\{h,b\}$ when $h$ arrives first, or when $b$ arrives first and $h$ precedes both hub leaves. These disjoint possibilities have probabilities $1/5$ and $1/15$. In the second case $a$ may appear before $h$ in the raw arrival order because $b$ has already blocked $a$. When every isolated unit produces its target, no endpoint of an added bridge is selected, so inserting the bridges leaves the ordered greedy decisions unchanged by induction through the order. Conversely, if the global target is obtained, every such endpoint is unselected, so removing the bridges also preserves the decisions. The internal orders on disjoint vertex sets are independent. The probability of the unique minimum is therefore $(4/15)^m$.

The ratio at threshold $2m$ is $A_m(4/15)^m$. It exceeds one at $m=3$. For all $m\ge2$, $A_m>4A_{m-1}$ follows from $13>12$ and $A_{m+1}-4A_m=(A_m-4A_{m-1})+2A_{m-2}$. Each subsequent ratio grows by a factor greater than $16/15$. This proves failure for **every** $m\ge3$ without extrapolating from a numerical fit.

| $m$ | Order | MIS total | Sequential CDF at $2m$ | Static CDF at $2m$ |
|---:|---:|---:|---:|---:|
| 1 | 5 | 3 | 4/15 | 1/3 |
| 2 | 10 | 13 | 16/225 | 1/13 |
| 3 | 15 | 55 | 64/3375 | 1/55 |
| 4 | 20 | 229 | 256/50625 | 1/229 |
| 5 | 25 | 951 | 1024/759375 | 1/951 |
| 6 | 30 | 3,949 | 4096/11390625 | 1/3949 |

These six rows were computed directly from the graphs. At $m=4$ the gap is $7999/11593125$. At $m=5$ the ratio is $324608/253125$. The stated exponential divergence holds, with a numerical correction. The characteristic polynomial $p(x)=x^3-5x^2+4x-2$ has discriminant $-244$ and a simple positive root $4.15275<\lambda<4.15276$ by substitution. The conjugate roots have modulus $\sqrt{2/\lambda}<1$, and the numerator of $A(z)$ is positive at the dominant pole. Thus the ratio is asymptotic to a positive constant times $(4\lambda/15)^m$. Its growth factor rounds to **1.10740** at five decimal places. The producer prints 1.10835. [Direct checks](verification.json) · [Producer's family claims](inputs/REPORT.md)

## Other secondary claims

- **Cycle construction.** In the supplied triangle example the vertices $0,1,2$ are the three connected leaves, one per unit. Each becomes degree three. For the stated construction connecting one hub leaf per unit around a cycle, the exact maximum interior ratios at $m=4,5,6$ are $7424/10125$, $646144/759375$ and $236578321037/295415859375$. All are below one and reproduce the quoted three-decimal results. The exponential MIS growth rate has a small numerical correction. Fix the occupied cycle connectors, an independent set on the cycle. Each occupied connector has two local completions. An unoccupied connector has three if it neighbors an occupied connector, and one otherwise. An occupied connector followed by a gap of $d\ge1$ zeros therefore contributes $2\cdot3^{\min(d,2)}$ choices. The block series is $B(z)=6z^2+18z^3/(1-z)$. Marking a fixed occupied connector gives the series of cyclic tours starting there, $\sum_{r\ge1} B(z)^r$. Allowing other starting positions changes the count by at most a factor of $m$, apart from the single all-empty-connector state. The exponential growth base is the positive root of $x^3-x^2-6x-12=0$, between **3.59625 and 3.59626**. This corrects the rough estimate 3.65 and preserves the comparison with $15/4$. The growth calculation concerns the minimum-size event. Each of the three finite no-violation results uses the whole CDF. [Finite cycle checks](verification.json)
- **Pendant paths.** Appending one path to CE#3 at each of its nine degree-one or degree-two vertices, at every order 16 through 28, gives 117 labeled attachment cases. Exact CDF comparison finds zero violations. The assertion about static multiplicity needs qualification. At order 28, attachment at vertex 7 gives 207, 1,491, 577 and 12 maximal independent sets at sizes 11 through 14, respectively, or **2,287** in total versus 55 on CE#3. It is the CDF violation that disappears. [Attachment ratios and extremal histogram](verification.json)
- **Ladders.** The proposed claw-free question is distinct from the ladder question. The producer calls $2\times n$ ladders claw-free. For $n\ge3$ take the top vertex in column 2 and its left, right and downward neighbors. The three neighbors are pairwise nonadjacent, so these four vertices induce $K_{1,3}$. This corrects the example, leaving both possible sharpenings open. [Producer's next steps](inputs/REPORT.md)
- **Search history.** The four reported heuristic evaluation counts add to 159,889. The permitted inputs omit the sampled graphs, random seeds, trajectories and raw logs, including the alleged closest 22-vertex cubic graph. The reported evaluation and hit counts, that graph's extrema, the producer's runtimes and its original 200 random validation graphs cannot be independently authenticated from these inputs. The exhaustive census confirms zero cubic counterexamples through order 15. The independent 200 control draws here have a specified seed. The larger cubic and minimum-degree-two questions remain open in this audit. [Supplied search summary](inputs/REPORT.md)

## Referee self-check

**CONTROLS:** No assumption overrode the controls. All five named small graphs agreed with complete order enumeration, including the degree-four example's 5/24 versus 1/5. The graph-class guard rejected it. [Python control results](verification.json) · [Independent census controls](census_controls.txt)

**CONTRADICTING:** No conflicting result from the available evidence was suppressed. The size-7 tree mass failed strict validation, the tree reverses CDF sign at 7, exactly one of 89 single deletions retains the violation, and CE#3 contradicts uniqueness. The incomplete heuristic provenance is recorded above. [Computed laws and deletion outcomes](verification.json) · [Producer's claims](inputs/REPORT.md)

**LABELS:** No witness annotation determined the answer. All three topologies, static histograms and sequential laws were reconstructed from edges. Explicit permutations match the three census hits. Seven corruptions were rejected after correcting only the baseline in memory. [Verifier](referee_verify.py) · [Evidence](verification.json)

Reproduction commands, sources, limitations and next steps are in [REPORT.md](REPORT.md). This is AI work. No human has checked it.
