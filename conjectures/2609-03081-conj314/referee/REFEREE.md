VERDICT: HOLDS WITH CAVEATS

The order-17 permutation in the certificate disproves Lewis and Won's Conjecture 3.14 as stated in v1. It has **104,476,798,194,769** complete placements. The conjectured family attains **103,460,138,813,701**, uniquely at $m=5$. The gap is **1,016,659,381,068**. The caveats concern the producer's search-history annotation and reporting. [Primary source](inputs/2609.03081v1.tex.json.gz) · [Submitted certificate](inputs/witness.json) · [Exact verifier](referee_verify.py)

## The comparison that decides the conjecture

The black columns in row order are $(5,4,3,2,1,8,7,6,9,12,11,10,17,16,15,14,13)$. Sorting gives precisely $1,\ldots,17$. Splitting at ascents gives decreasing runs on the successive intervals 1–5, 6–8, 9, 10–12 and 13–17. Thus its layered shape is $(5,3,1,3,5)$. Scanning the board gives 32 across words, 32 down words, and 272 white-square intersections.

| Equal endpoint size $m$ | Central singletons | Grid permanent = Proposition 3.15 |
|---:|---:|---:|
| 1 | 15 | 1 |
| 2 | 13 | 268,435,457 |
| 3 | 11 | 1,129,869,140,869 |
| 4 | 9 | 40,084,566,933,905 |
| **5** | **7** | **103,460,138,813,701** |
| 6 | 5 | 65,555,327,816,657 |
| 7 | 3 | 18,356,098,793,509 |
| 8 | 1 | 2,824,217,777,825 |

A composition has positive parts summing to 17. Thus the eight rows exhaust the equal-endpoint interpretation. The general formula in Proposition 3.15 covers $m_1=m_2=1$ even though its final “in particular” clause says $m>1$. The identity gives one placement by direct computation. Reading $m=0$ as omitting both empty blocks gives the same identity. The empty sum obtained by formally substituting zero into Proposition 3.16's objective is zero. Proposition 3.15 itself requires positive endpoints.

There is no integer solution to $2m=17$. A requirement of one or more middle singletons retains all eight rows. For unequal positive endpoints there are 128 ordered pairs, and the largest value is **59,058,819,009,961** at $(5,6)$ and $(6,5)$. The 16 pairs with no central singletons reach at most **864,806,272,861**. Omitting one zero-sized endpoint yields a case already covered by a size-one endpoint whenever a singleton remains. If the whole composition is a single part 17, the board is the reflected identity and has one placement. Reflections and transposition biject the placements. Allowing any of these readings preserves the strict win.

The maximum over the 136 ordered pairs, including the eight equal pairs, is therefore below an attained value in $S_{17}$. This suffices to refute even the interpretation that *one* global maximizer has the proposed shape. It also supplies the lower bound $r(17)\ge104{,}476{,}798{,}194{,}769$. The exact global maximum and the smallest counterexample order are separate questions.

## Why the exact counts can be checked

The verifier sets cell $(i,j)$ black exactly when $j=w(i)$. It collects maximal white runs in every row and column, including one-cell runs. A pair of words intersects in at most one square, which identifies each edge of the incidence matrix with a possible rook. A complete placement chooses each row and column of that matrix exactly once. This is the perfect-matching interpretation in the paper, lines 144–158 and 180–182.

1. **Matching recurrence.** Process the across words in board order. For each partial assignment, choose one unused incident down word. When a down word has reached its final incident row, require it to be used and then forget its bit. If two unused down words expire together the state contributes zero. Partial assignments with identical surviving bits have identical completions, so their integer multiplicities add. The empty matrix has one empty matching.
2. **Ryser inclusion–exclusion.** In a separate implementation, expand the bit rows into a square binary matrix. A row or column of degree one has a mandatory edge. Remove that row and column, repeating as possible. On the order-17 witness, exactly eight edges were forced, leaving a 24-by-24 matrix. With the verifier’s one-based scan ordering the forced pairs were (1,7), (3,5), (5,3), (7,1), (26,32), (28,30), (30,28) and (32,26). On the remaining $d\times d$ matrix evaluate $(-1)^d\sum_{S\subseteq[d]}(-1)^{|S|}\prod_i\sum_{j\in S} A_{ij}$. A class of $q$ identical columns chosen $j$ times has weight $(-1)^j\binom qj$. Multiply a row's sum when its last column class has been visited. A zero product contributes zero. This counts surjective row-to-column assignments by inclusion–exclusion, hence exactly the bijections. It uses signed Python integers and shares only the grid incidence data with the matching recurrence.
3. **Proposition 3.15.** Independently of either permanent routine, compute $S(a,k)=kS(a-1,k)+S(a-1,k-1)$ with $S(0,0)=1$ and zero outside its support. Reindex the paper's general formula by $k=m-i$. The result is $\sum_{k=1}^{\min(a,b)} S(a,k)S(b,k)(k^{n-a-b}k!)^2$. Both the matching recurrence and the horizontal-cut calculation described below matched these formula totals for all 136 endpoint pairs at 17 and all nine symmetric pairs at 18. No appeal to Proposition 3.16's optimization is needed.

At order 18 the witness shape $(5,3,1,1,3,5)$ gives **2,949,333,362,474,113** by both permanent algorithms. All nine equal-endpoint shapes reach at most **2,445,624,351,454,501**, again at $m=5$. The strict excess is **503,709,011,019,612**. The empty-center case $(9,9)$ gives 12,020,754,177,001 and is included among those nine. [Calculation transcript](verification.txt)

## Certificate fields and adverse evidence

| Fields in `inputs/witness.json` | Independent check | Finding |
|---|---|---|
| `paper`, `authors`, `title` | Supplied archive identifier and TeX lines 67–68 | All match. The archive filename supplies the version identifier. |
| `conjecture`, `conjecture_label` | Section and shared-environment counters, literal label on TeX line 753 | 3.14, `conj:maxlayered` |
| `n`, `permutation`, `layered_shape` | Exact entry set, run lengths, reconstruction as descending consecutive blocks | 17, the displayed permutation, and `(5,3,1,3,5)` |
| `rook_placements` | Matching recurrence and signed inclusion–exclusion | 104,476,798,194,769 |
| `best_m_1_m_shape`, `best_m_1_m_m`, `best_m_1_m_rook_placements` | Maximize the eight direct counts above and identify all ties | Seven interior ones, endpoints 5, unique count 103,460,138,813,701 |
| `excess_over_best_m_1_m` | Subtract the two verified totals | 1,016,659,381,068 |
| `minimality_note` | Compare the attained values, restricted search spaces and claimed historical effort separately | Mixed. See the census scope below. The inputs contain no trajectory of the randomized searches. |

The report's table gives **264k SA** at 15 and **290k SA** at 16 (lines 55–56). The note in the JSON (line 15) says **“>300,000 SA/2-opt evaluations at n = 15 and n = 16.”** The table cannot support a per-order reading of that figure. A combined figure would fit, and the units “SA” and “SA/2-opt evaluations” may refer to different counters. A correction should specify the unit, the per-order figures and whether the threshold is pooled. The original run counts cannot be authenticated from these three files. [Submitted JSON](inputs/witness.json) · [Submitted report](inputs/REPORT.md)

Two further corrections follow directly from the supplied source and the grids. The report cites TeX line 759 for the conjecture (report line 11). That line starts Proposition 3.15. The conjecture's statement is at line 754. The report also describes a “loss of 6 diagonal black squares” when comparing the two order-17 grids (report line 46). Each reversal of three consecutive elements fixes its middle element. The seven fixed points of the central identity block become three fixed points, so **four** diagonal black squares move off the diagonal. Finally, the report's phrase “136 asymmetric” includes the eight symmetric cases. There are 136 ordered pairs in all and 128 strictly unequal pairs. [TeX source](inputs/2609.03081v1.tex.json.gz) · [Submitted report](inputs/REPORT.md)

A separate table heading needs a symmetry qualification. At order 10, reflecting the columns of the symmetric maximizer `(4,3,2,1,5,6,10,9,8,7)` gives `(7,8,9,10,6,5,1,2,3,4)`. Its first decreasing run has length one and starts at 7, so it cannot be a direct sum of decreasing blocks. Nevertheless, reflection bijects its placements with the maximizer's, and its directly computed count is **255,569**. The producer's line 50 gives **226,409** under “Best Non-… Found”. A table of alternatives restricted to the searched representatives, or excluding the entire symmetry orbit of the proposed family, should say so. An unrestricted maximum outside the literal shape family is at least 255,569. This tied reflection does not challenge the existential conjecture at order 10. [Producer's table](inputs/REPORT.md) · [Direct reflection check](verification.txt)

## Adversarial controls

Before the target comparison, both permanent algorithms agreed on every one of the 46,233 permutations at orders 1 through 8. Their successive maxima were **1, 1, 1, 5, 17, 73, 469, 3493**. The separate order-eight permutation `(2,7,4,8,1,6,3,5)` gave **155**. Order one uses the unique empty placement on the all-black board.

| Submitted mutation | Recomputed result or reason for rejection |
|---|---|
| Duplicate the second entry in the first position | Fails the permutation test |
| Swap the first two entries | 3,697,126,675,213, below the family maximum |
| Raise the witness count by one | Disagrees with the recomputed permanent |
| Raise the best family count by one | Disagrees with the maximum of the family counts |
| Submit the symmetric maximizer with its correct count and zero excess | Equality at 103,460,138,813,701 fails the required strict comparison |

All five went through the same certificate check. The losing swap reached the numerical comparison, and equality failed even with internally consistent annotations. [Verifier](referee_verify.py) · [Calculation transcript](verification.txt)

## A short arithmetic certificate for the witness

Cut a palindromic layered grid with shape `(5,3,1^t,3,5)` at both ends of its singleton region. In a decreasing block of size $d$, each triangular half has $S(d,d-j)$ ways to put $j$ nonattacking rooks in it. To see this, identify its cells after reflection with pairs $i<k$ in $[d]$. Chosen cells are directed edges $i\to k$ with at most one predecessor and one successor per index. They decompose $[d]$ into $d-j$ increasing chains, including isolated indices. Each set partition gives precisely one such collection by connecting consecutive elements of every part. Lewis and Won use these same triangular rook numbers in the proof of Proposition 3.15, TeX line 816.

Process the upper-left blocks first. After the outer block of size 5, let $p$ east words and $p$ south words remain open. Its outer triangle is forced, since all its west and north words must be filled there. Its inner triangle contributes $S(5,p)$ choices. In the following size-3 block let $a$ west words and $a$ north words remain after placing the northwest triangle's rooks, and $b$ east words and $b$ south words after placing the southeast triangle's rooks. The triangle factors are $S(3,a)S(3,b)$. The new north and west words must use distinct members of the previous east and south pools respectively. There are $(p!/(p-a)!)^2$ choices. This leaves $h=p-a+b$ open words of each kind. Thus the number $D_h$ of partial placements is

$$
D_h=\sum_{\substack{1\le p\le5,\;1\le a\le\min(3,p),\;1\le b\le3\\p-a+b=h}}
 S(5,p)S(3,a)S(3,b)\left(\frac{p!}{(p-a)!}\right)^2.
$$

Each central singleton consumes one open word of each kind and contributes one new word of each kind, giving $h^2$ choices and preserving $h$. The bottom-right half is the half-turn of the top-left half. Both halves must leave the same $h$ to finish. The remaining words can be paired in $(h!)^2$ ways because the rectangles connecting the halves are entirely white. The full count is therefore $\sum_h(D_h\,h^t h!)^2$.

| $h$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| $D_h$ | 1,081 | 11,763 | 34,786 | 34,315 | 12,250 | 1,435 | 25 |
| $D_h\,h\,h!$ | 1,081 | 47,052 | 626,148 | 3,294,240 | 7,350,000 | 6,199,200 | 882,000 |

Squaring the seven entries in the last row and adding gives **104,476,798,194,769**. For the best competing shape, Proposition 3.15 gives $1^2+3840^2+328050^2+3932160^2+9375000^2=103{,}460{,}138{,}813{,}701$. These two short sums give the strict excess by subtraction. For order 18, multiply each entry of the witness row by its column’s $h$ before squaring. The same calculation with three singletons at 19, and inner block size four and two singletons at 20, reproduces the producer's displayed witnesses and their strict comparisons with Proposition 3.15. This verifies those two table comparisons algebraically. [Integer coefficients and totals](verification.txt)

## Scope of the minimality note

The JSON gives five proposed values for $r(10),\ldots,r(14)$. Its claim that they are attained is easy to check by constructing the five endpoint-family grids. Whether these values are global maxima requires bounds over arbitrary permutations. The supplemental checks address this distinction. They were written independently of the producer's search code.

For the smaller unrestricted censuses, take one representative of each orbit under row reversal, column reversal and transposition. These are symmetries of the square board, and each sends complete placements bijectively to complete placements. The verifier evaluates the matching permanent on each representative and sums its actual orbit size, including smaller orbits with stabilizers. The final sum must equal $n!$.

For the horizontal-cut census, split the board between two rows. Scanning inward from either edge, store the count of partial placements for each subset $M$ of columns whose current vertical word already contains a rook. At a black square, the old word in that column must have a rook before it closes, except when the black square is on the initial row. Clear that column's bit and take one unused column in each nonempty horizontal white run of the new row. This follows the grid definition directly. At the cut, a top mask $M$ pairs with precisely the complementary bottom mask because the open word at each column gets exactly one rook. The complete count is their dot product with these complementary indices.

For a fixed set of top black columns and its complement below, each ordering of both row lists gives one permutation. An entrywise maximum of partial-count vectors bounds the compatible dot product because every entry is nonnegative. The order-12 run computes these maxima by listing half orders. The refined calculation bounds an unordered set recursively. For each possible last black column it applies that row’s nonnegative transition to the smaller set’s bound, then takes the coordinatewise maximum over these choices. This bounds every true ordering by induction. When a dot-product bound exceeds the incumbent, fix another row nearest the cut and repeat. With both orders determined the dot product is exact and is checked against the full grid. The refined census starts one below an attained count, so at least one improving exact leaf must be recovered. The covered multiplicities are products of the factorials of the unfixed row counts and the actual symmetry orbit sizes of the cut sets. The coverage check is independent of the score cutoff.

The following whole-group results complete the mathematical audit of the five numbers in the JSON.

| Order | Permutations covered | Global maximum |
|---:|---:|---:|
| 9 | 362,880 | 28,549 |
| 10 | 3,628,800 | 255,569 |
| 11 | 39,916,800 | 3,316,625 |
| 12 | 479,001,600 | 46,301,969 |
| 13 | 6,227,020,800 | 680,707,985 |
| 14 | 87,178,291,200 | 10,353,226,769 |

At 14 the verifier covered 890 cut classes. It recovered an improving leaf from the raw grid and bounded all other completions. The producer’s mathematical census claim through 14 is independently reproduced. The producer’s particular branch-and-bound implementation and timings are outside this replay. [Orders 9–11](census/orders9-11.txt) · [Explicit half orders](census/explicit-halves.txt) · [Orders 12–13](census/refined-through13.txt) · [Order 14](census/order14.txt)

At 15 and 16, the verifier ran the two finite searches named in the note:

| Search space | Order 15 | Order 16 |
|---|---:|---:|
| All layered compositions, one per choice of cuts between consecutive values | 16,384 | 32,768 |
| All positive $a,b$ and $J_a\oplus u\oplus J_b$, $0\le k=|u|\le8$ | 284,397 | 330,631 |
| Representatives directly counted in the bounded-middle search | 72,991 | 85,072 |
| Maximum in both searches | 202,352,501,701 | 4,493,953,750,501 |

For the bounded middle, choose the $k$-permutation and one of the $n-k-1$ positive endpoint splits. Transpose sends $u$ to its inverse and a half-turn exchanges the two end sizes. Every orbit is weighted, checked against $(n-k-1)k!$ at each $k$. Both restricted maxima are attained by the equal-endpoint shape with $m=5$. These figures use positive endpoints. [Layered census](census/layered.txt) · [Order-15 middle census](census/middle15.txt) · [Order-16 middle census](census/middle16.txt)

Allowing one empty endpoint adds 92,468 oriented descriptions at each order, with two endpoint orientations for each permitted middle permutation. Counting 23,675 representatives per order gives maxima **48,250,834,453** at 15 and **435,716,292,061** at 16. Both are below the corresponding positive-endpoint maxima. The counts of descriptions include any coincident boards. [Order 15](census/empty15.txt) · [Order 16](census/empty16.txt)

The short historical phrase “all $n!$ permutations via exact branch-and-bound” describes their computation. Our independent runs check mathematical extrema, and cannot authenticate what software the producer ran.

One endpoint convention matters at order one. The unique grid has one empty placement. The positive two-endpoint family stated in the producer's formula $1\le m\le\lfloor n/2\rfloor$ is empty there. Counting the identity as a degenerate case recovers the paper's claim about its first eight cases. At 17 the admissible family is nonempty and both readings give the same strict disproof.


## Verdict checks and reproduction

CONTROLS: No assumption overrode the controls. Both permanent algorithms and the direct black-column scan agreed on all 46,233 permutations. For each order, the proposed family attained the maximum under the order-one convention above. The separate order-eight count is 155. A tied baseline, a genuinely losing swap and the three other mutations were all rejected for the stated reasons. [Exact results](verification.txt)

CONTRADICTING: No contrary count was dropped. The 136 endpoint pairs include all 128 unequal choices and all 16 choices with an empty center. The incompatible readings of the search-effort annotation and the reflected order-10 maximizer are retained above. The unobserved historical trajectories remain unverified. [Witness annotation](inputs/witness.json) · [Producer table](inputs/REPORT.md) · [Direct results](verification.txt)

LABELS: No annotation was accepted as numerical evidence. The TeX counter gives conjecture 3.14 at label line 753. Sorting and cutting the raw permutation recovers the shape. There are 272 independently identified intersections. The signed permanent and the seven-square calculation give the same integer. [Verifier](referee_verify.py) · [Source](inputs/2609.03081v1.tex.json.gz)

Run `nice -n 10 python3 -B -u referee_verify.py` from this directory to reproduce the certificate. The supplemental commands are in [REPORT.md](REPORT.md#census-scope-and-limitations). An exact finite comparison exhausts its candidate family, so no statistical holdout applies. This referee reproduces the supplied disproof. Global priority was outside the allowed sources.

This is AI work. No human has checked it.

## Appendix. Primary-source definitions and statements

Line numbers below are one-based in the only member of the supplied gzip/JSON file, `Nonattacking_rook_placements_arxivsubmission.tex`. Lines 38–49 define a section-reset conjecture counter shared by propositions, theorems, examples, remarks, questions and the other listed environments. In section 3 the thirteenth item is the question at line 746. The following conjecture begins at 752, has its label at 753 and its statement at 754. The next proposition begins at 759 with its label at 760. Counting the environments recovers **3.14** and **3.15**. Line 750 describes layered permutations through their diagonal blocks and names the associated composition their shape. The arbitrary composition used here is the direct sum of decreasing blocks of its part sizes. The following are verbatim extracts. [Supplied TeX](inputs/2609.03081v1.tex.json.gz)

**Crossword grid** (line 139)

```tex
An $m \times n$ \emph{crossword grid} or \emph{grid} is an $m \times n$ array of squares, some of which are white and some of which are black. (We do not impose the symmetry, connectedness, or minimum word length assumptions that are the usual conventions for American-style crossword puzzles.)  To any crossword grid, we can associate an $m \times n$ matrix whose $(i,j)$ entry is $0$ if the corresponding square is white and $1$ if the corresponding square is black. We also refer to the squares in the grid by their row and column, using the matrix convention for numbering rows and columns. We refer to rows $1$ and $m$ as \emph{edge rows} and columns $1$ and $n$ as \emph{edge columns}. The squares in the edge rows and edge columns are called \emph{edge squares}. All non-edge squares in a crossword grid are called \emph{interior squares}. The squares $(1,1)$, $(1,n)$, $(m,1)$, and $(m,n)$ are called \emph{corner squares}.
```

**Words and their intersections** (line 144)

```tex
An \emph{across word} in a crossword grid is a maximal contiguous sequence of white squares within a single row. Similarly, a \emph{down word} is a maximal contiguous sequence of white squares within a single column. We say that an across word and down word \emph{intersect} if they share a common square.
```

**Non-attacking placement** (line 148)

```tex
A \emph{(non-attacking) rook placement} on a crossword grid $G$ is a subset $R$ of the white squares in the grid such that no two squares in $R$ lie in the same across word or the same down word. We call the squares in $R$ \emph{rooks} and picture the rook placement by drawing $G$ and placing a chess rook into each square in $R$:
```

**Completeness** (line 158)

```tex
A rook placement $R$ on $G$ is called \emph{maximal} if for any rook placement $R'$ on $G$, if $R \subseteq R'$ then $R = R'$. We call $R$ \emph{maximum} if for any other rook placement $R'$ on $G$, we have $|R| \geq |R'|$. Finally, $R$ is called \emph{complete} if $R$ contains exactly one white square in every across word and every down word of $G$. We remark that no two of maximal, maximum, and complete coincide in general (see Figure~\ref{fig:maxcomp}) but complete implies maximum implies maximal. A rook placement on $G$ is equivalent to a matching on $\Graph{G}$, while a complete rook placement is equivalent to a perfect matching.
```

**Meaning of RP(G)** (line 180)

```tex
Henceforth, throughout this paper, by a \emph{rook placement}, we mean a complete non-attacking rook placement. Given a grid $G$, let $\RP(G)$ denote the set of all possible (complete, non-attacking) rook placements on $G$. 
```

**Permutation grid** (line 443–444)

```tex
We now turn our focus specifically to permutation grids, that is, grids with exactly one black square in each row and column.
We adopt the convention that if a permutation matrix has a $1$ in position $(i,j)$ then the corresponding permutation maps $i$ to $j$. Equivalently, for a permutation $w \in S_n$, we define the crossword grid $\Grid{w}$ to be the grid with black squares in $(i, w(i))$ for all $i \in [n]$.
```

**Layered shape and published small-order maxima** (line 750)

```tex
Let $r(n) = \max_{w \in S_n} |\RP(\Grid{w})|$ denote the maximum number of rook placements over all $n \times n$ permutation grids. For $1 \leq n \leq 8$, exhaustive computer computation shows that the sequence $r(n)$ begins $1, 1, 1, 5, 17, 73, 469, 3493$. This sequence does not appear in the On-Line Encyclopedia of Integer Sequences. For these first eight cases, the permutation grid admitting the most rook placements is a block-diagonal permutation whose first and last blocks are anti-diagonal of the same size and whose central block is an identity matrix. In other words, they are layered permutations whose block-sizes are indexed by compositions $(m, 1, 1, \ldots, 1, m)$ for some $m$. For a layered permutation, we call the associated composition its \emph{shape}. 
```

**Conjecture 3.14** (line 752–755)

```tex
\begin{conj}
\label{conj:maxlayered}
For each $n$, the $n \times n$ permutation grid admitting the most rook placements is given by $\Grid{w}$ where $w \in S_n$ is a layered permutation of shape $(m,1,1,\dots, 1,m)$ for some $m$.
\end{conj}
```

**Stirling numbers and Proposition 3.15** (line 757–769)

```tex
For layered permutations of shape $(m_1, 1, 1, \dots, 1, m_2)$, we can compute the number of rook placements on the permutation grid exactly. Recall that the \emph{Stirling number of the second kind} $S(a, b)$ is the number of ways to partition a set of $a$ objects into $b$ non-empty sets.

\begin{prop}
\label{prop:countlayered}
    Suppose $m_1, m_2 > 0$ and let $m = \min(m_1, m_2)$. For the layered permutation $w \in S_n$ of shape $(m_1, 1,1,\dots,1, m_2)$, the number of rook placements on $\Grid{w}$ is given by 
    \[
    \sum_{i = 0}^{m-1} S(m_1, m - i)S(m_2, m - i)\left((m-i)^{n - m_1 - m_2} \cdot (m-i)!\right)^2.
    \]
    In particular, if $m > 1$ then for the layered permutation in $S_n$ of shape $(m,1,1,\dots,1,m)$, the number of rook placements on $\Grid{w}$ is given by 
    \[
    \sum_{k = 1}^m \left[S(m, k) \cdot k^{n-2m} \cdot k!\right]^2.
    \]
\end{prop}
```
