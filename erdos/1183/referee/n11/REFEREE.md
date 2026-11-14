Independent referee finding: **f(11)=7 holds** for the original Erdős–Ulam two-colouring sublattice function. Checked on 14 November 2026.

## (a) Definition and source statement

Let [n]={1,...,n}. A colouring is an arbitrary map χ:2^[n]→{0,1}, including colours for ∅ and [n]. For a colouring χ, let M(χ) be the maximum cardinality of a **nonempty** family L⊆2^[n] such that χ is constant on L and A∪B,A∩B∈L for every A,B∈L. Then

    f(n) = minχ M(χ).

The live [problem page](https://www.erdosproblems.com/1183) asks for families “closed under taking unions and intersections. Estimate $f(n)$.” The complete original statement, including the separate union-only function F, is preserved verbatim in the downloaded source at `sources/site1183.txt:25` and `sources/site1183.txt:26`; the original HTML is `sources/site1183.html`. Short quotations are used here rather than duplicating the full page and comments. The second question concerns the growth of F(n), including superpolynomial and subexponential bounds, and is not the finite assertion reviewed here.

The site's current source shows “Proof expositions (0)”, “Comments (11)” and “Proof claims (1)” (`sources/site1183.txt:41`, `:47`, `:48`). Tao's public table records status “open” (`sources/problems.yaml:19529`), with an older status-update date. The page still mentions only the elementary chain lower bound; its prose is not a complete account of the October lower-bound results. All eleven comments and the proof-claim text are preserved verbatim in `sources/forum1183.txt:88` and `sources/claims1183.txt:83`; their mathematical content is summarized in (e).

The [current Bhattacharjee–Mandal–Bhattacharya paper](https://github.com/creelie/Erdos-1183/blob/587d4b9cf88575a474777743ed71e2863c7c2cf6/paper/Erdos.tex) defines exactly this minimum and maximum (`sources/Erdos_pinned.tex:128`). Its statement that a singleton family is a sublattice (`:143`) rules out any requirement to include prescribed ambient endpoints. The [omega note](https://github.com/the-omega-institute/trureturing/blob/c0bb36be76f99139a5068f434597476d4682e29b/Problems/bhattacharjee-mandal-bhattacharya-2026-sublattice-chain-bound-refutation.md) explicitly uses nonempty sublattices (`sources/omega.md:112`). Allowing the empty family among competitors would not change the maximum, since a singleton is always available.

**No sublattice is required to contain ∅ or [n].** It has its own least and greatest members, obtained by intersecting and uniting its members. Closure is under binary operations, not nullary ambient operations. The producer's report and the definition field of `certificates/1183_n11_coloring.json:3` agree with the site and paper. Colour labels 0/1 instead of 1/2 make no difference.

## (b) Upper bound f(11) ≤ 7

The supplied colouring has rank word **100010011101**, indexed by sizes 0 through 11. Colour 0 occupies ranks {1,2,3,5,6,10}, containing **1,166** sets; colour 1 occupies ranks {0,4,7,8,9,11}, containing **882** sets. My set-based check compares all 2,048 entries with their ranks, checks the domain and colour values, and verifies these counts (`check_data.py:21`; `logs/data_check.txt:1`). Only the permitted JSON files were copied from the producer, as data.

A colour-0 seven-member sublattice is

    { {1}, {1,2}, {1,3}, {1,2,3},
      {1,2,3,4,5}, {1,2,3,4,5,6}, {1,2,3,4,5,6,7,8,9,10} }.

Its bit masks are [1,3,5,7,31,63,1023], with bit i representing element i+1. The two incomparable members {1,2} and {1,3} have intersection {1} and union {1,2,3}; all other pairs are comparable. Their ranks are 1,2,2,3,5,6,10. Every pair was also checked using actual Python sets (`check_data.py:13`; `logs/data_check.txt:2`).

**Fresh CNF and its exact interpretation.** For each set S of the selected colour, introduce x_S. For each pair of distinct sets A,B in that colour, impose

    ¬x_A ∨ ¬x_B ∨ x_(A∪B),
    ¬x_A ∨ ¬x_B ∨ x_(A∩B).

A result in the opposite colour is represented by false, leaving a binary exclusion. Tautologies are removed. Pairs A=A are automatically closed. These clauses are therefore equivalent to closure of the selected family; they impose no additional geometric or endpoint restriction (`encode.py:34`).

For the N membership variables in mask order, D(i,j) denotes that at least j of the first i variables are true, for 1≤j≤k. Set D(i,0)=true and D(i,j)=false for j>i. The encoder enforces the full equivalence

    D(i,j) ↔ D(i−1,j) ∨ (x_i ∧ D(i−1,j−1))

using four clauses. Writing q=D(i,j), a=D(i−1,j), b=D(i−1,j−1), these are (¬a∨q), (¬x_i∨¬b∨q), (¬q∨a∨x_i), (¬q∨a∨b). It finally requires D(N,k) (`encode.py:40`). Induction on i proves the interpretation. Conversely, the actual prefix counts extend any chosen family to a satisfying assignment of the counter. Thus the formula is SAT **if and only if** the chosen colour contains a closed family of at least k members. For k=8 this excludes families of every size ≥8, without assuming that a larger lattice contains an eight-member sublattice. No symmetry breaking is used.

I cloned and compiled the official repositories locally, independently of the producer's tools: [CaDiCaL](https://github.com/arminbiere/cadical) at `c60730422e758ef1cebe7aeddf2dda31c996bf04` and [drat-trim](https://github.com/marijnheule/drat-trim) at `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Commands are in `BUILD_COMMANDS.txt`. Both default CaDiCaL solves emitted binary DRAT proofs, and both were accepted by default **backward** drat-trim, without forward-mode shortcuts.

| Query | Variables | Clauses | Result | Solve wall s | Proof bytes | Check wall s |
|---|---:|---:|---|---:|---:|---:|
| Colour 0, at least 8 | 10,466 | 1,311,675 | UNSAT; VERIFIED | 92.85 | 401,008,334 | 120.46 |
| Colour 1, at least 8 | 7,910 | 733,093 | UNSAT; VERIFIED | 37.14 | 153,624,504 | 37.82 |

The conclusive lines are `logs/c0_k8.check:8` and `logs/c1_k8.check:8`. Solver exits are 20; checker exits are 0. CNFs, metadata, solver outputs, checker outputs and resource measurements are retained. SHA-256 proof hashes are in `PROOF_HASHES.json:5` and `:10`. After checking and hashing, the two large proofs were moved to macOS Trash as permitted by the task; they can be regenerated from the retained CNFs using `REPRODUCE.sh`. A hash alone is not a substitute for a proof; the reported checks were performed on the complete proof bytes before their removal from this directory.

**Second complete upper-bound argument, independent of SAT.** A monochromatic chain uses at most six ranks. A finite distributive lattice L is the ideal lattice J(P) of its poset P of join-irreducibles. A linear extension of P gives a chain of |P|+1 ideals, so |P|≤5 here.

The concrete embedding in a powerset gives a base of b always-present coordinates and a positive integer weight w_p for each p∈P. Precisely, let B=min L, T=max L. For x∈T\B let M_x be the intersection of all members containing x. If M_x=A∪C, then x belongs to one of A,C, forcing that member to contain M_x; hence M_x is join-irreducible. Conversely, for any join-irreducible J, choose x in J\J_*, where J_* is its unique lower cover. Then M_x⊆J but M_x⊈J_*, so M_x=J. Thus each join-irreducible receives at least one coordinate. For an ideal I, its corresponding set has rank

    b + Σ_(p∈I) w_p,       b≥0, w_p≥1, b+Σ_p w_p≤11.

This is the usual weighted ideal-lattice representation, also explicitly described in the March He–Li–Tang chat translation (`sources/tang_page_4.png`). No new representation theorem is claimed.

My `rank_lattices.py:16` enumerates every relation i<j on m≤5 naturally ordered elements, retains exactly the transitive ones, and enumerates all their ideals. Every finite poset has a linear extension, so this covers every isomorphism type, possibly repeatedly. It then enumerates every b and positive weight vector satisfying the displayed budget (`rank_lattices.py:33`). A choice is monochromatic exactly when all its ideal ranks have the same colour.

The numbers of naturally labelled posets for m=0,...,5 were **1,1,2,7,40,357**. Among **365,531** poset/base/weight choices, the largest valid ideal lattice in either colour had **7** members (`logs/rank_lattices.log:7`; `certificates/rank_lattices.json`). This is a second exhaustive proof of the full upper bound, not a check of a selected list of candidate families. It uses integer/set operations only and took 0.97 seconds. It also gives a colour-1 seven-member example with masks [0,15,127,383,255,511,2047].

## (c) Lower bound f(11) ≥ 7

The lower bound is published, not a discovery of the producer or this referee. I checked the needed argument and independently reproduced three finite checks.

**Reduction for arbitrary colourings.** Suppose a colouring has no monochromatic sublattice with seven or more members. Each maximal chain has 12 members, and either colour's part of a chain is itself closed. Consequently every maximal chain has exactly six members of each colour. If two r-subsets S,T differ by exchanging one element, choose common chain segments below S∩T and above S∪T. Completing them through S or through T gives two maximal chains differing in exactly one member. Their colour counts force χ(S)=χ(T). Any pair of r-subsets is connected by such exchanges: replacing an element in S\T by one in T\S decreases |S\T| by one. Therefore the colouring depends only on rank, and its twelve-rank word is balanced. This is the omega argument (`sources/omega.md:43`), verified here as a mathematical argument, not assumed from a solver log.

**Producer data.** For all 1,254 listed families, `check_data.py:33` checks distinct masks in 0,...,2047, cardinality at least seven, and closure under every union and intersection using decoded sets. Their sizes range from 7 to 11. For each of all 4,096 rank words, at least one checked family is monochromatic (`logs/data_check.txt:3`). `certificates/lower_coverage.json` stores one family index per word, in lexicographic order on (g(0),...,g(11)). Combined with the preceding reduction, this proves the unrestricted lower bound. The 4,096-word computation alone is not represented as an enumeration of arbitrary colourings of 2^[11].

**Omega's published base case.** In a balanced word there are 924 possibilities. When three consecutive occurrences a<b<c of one colour satisfy a+c=2b, add to the six corresponding prefix sets the set P_a∪{b,...,c−1}, using zero-based coordinates. The new member has rank b and supplies a diamond with P_a,P_b,P_c; it is comparable with the other selected prefixes. My code builds and checks these actual families, obtaining **874** covered words. The remaining **50** are covered by the ten explicit families in the note; each family was decoded and checked independently (`published_lower.py:17`; `logs/published_lower.log:1`). The result reproduces the published n=11 lower bound without trusting the producer's 1,254-family construction.

**Current paper's proof.** The paper proves a red–blue pair with at least thirteen members in every colouring of 2^[11] (`sources/Erdos_pinned.tex:1437`). If rank colours are not constant, choose differently coloured equal-size sets with minimum exchange distance; the distance is one. The common chain below their intersection and above their union has eleven members. Add the red exceptional set to its red part and the blue exceptional set to its blue part. Both resulting families are chains, and their total is thirteen. If the colouring is rank-constant, the paper's eight product-of-chains gadgets cover all twelve-letter words, allowing reversal and colour swap. Each gadget replaces its block of one colour with more sets of that colour. Exterior prefixes are comparable with every gadget member, so the replacement is closed and the two colours together have at least thirteen members.

I checked this adjacent-set reasoning and all eight gadget constructions. Instead of relying solely on the paper's run-length case analysis, I also exhaustively checked its finite word-cover conclusion and every placed family for all **4,096** words (`published_lower.py:55`; `logs/published_lower.log:2`). This reproduces exactly the n=11 lemma needed here. The paper's later nineteen-dimensional computations, general asymptotic claims and Lean builds were not rerun; none is needed for this conclusion. The omega general odd-dimensional extension likewise was not needed.

## (d) Controls

With the same fresh encoder and k=7 in colour 0, CaDiCaL returns SAT, exit 10. The full assignment satisfies all **1,307,040** clauses of the **9,307**-variable CNF. Decoding membership gives exactly the seven masks [1,3,5,7,31,63,1023], independently confirmed closed and colour 0 (`logs/c0_k7.modelcheck:5`; `check_data.py:48`). This is a solver-found positive control, not merely an externally supplied family.

For the negative control I removed every justification from the colour-0 proof, leaving only the claimed terminal empty clause, represented in text DRAT as `0`. Against the unchanged colour-0 at-least-eight CNF, drat-trim reports **s NOT VERIFIED**, exit **1** (`certificates/corrupt.drat:1`; `logs/corrupt.check:5`; `logs/corrupt.exit:1`). The intended rejection is not an implementation failure. This control shows rejection of this corruption; it is not a proof of checker correctness for all possible corruptions.

CONTROLS: The same encoding finds and directly validates seven members in colour 0 (`logs/c0_k7.modelcheck:5`); the same checker rejects the empty-clause-only corrupted proof (`logs/corrupt.check:5`).

## (e) Prior public status, scope, and exact public statement

I found **no earlier public settlement of f(11)=7** in the sources searched before writing this verdict. This is a bounded literature finding, not a guarantee of priority. `PRIOR_ART.md` records the queries, snapshots, source dates and limitations. The strongest directly relevant earlier result found is **f(11)≥7**, and the omega note explicitly leaves equality open (`sources/omega.md:138`). The v1.0.0 BMB table gives exact f(n) only through n=10 (`sources/Erdos_v1.tex:1184`); the current paper supplies the stronger lower bound, not a matching n=11 colouring.

The live forum's eleven comments were all read. In source order: Xiao Hu (5 October) links the BMB preprint; Chojecki (18 March, 12:06) announces subexponential progress using VC-dimension and distributive lattices; Tang (12:40) reports similar work with He and Li; Chojecki (13:03) requests English; Tang (13:29) supplies a translation; Chojecki (13:44) acknowledges it; Tang (13:58) reports a comparison of the F upper-bound proofs; old-bielefelder (13:22) reports another comparison and questions about growth rates; Chojecki (13:43) acknowledges that comparison; Sothanaphan (14:45 and 14:47) reports provisional checking observations. None announces f(11)=7. The sole proof claim, submitted 5 October by creelie, concerns the two asymptotic union-closed conjectures, not this exact value (`sources/claims1183.txt:87`). I read the nine-page He–Li–Tang translation as rendered images because its PDF has no text layer; it discusses small values through n=5 and asymptotic bounds, not f(11)=7.

Other searches covered the live GitHub repository search sorted by update date, all 19 creelie issues/PRs, omega's source-path history, Tao's raw table and 60 open PRs, arXiv's newest-first search for monochromatic union-closed families and arXiv:2610.02833, plasma-ai's E1183 page and claim, and the named AI-result repositories. Exact f(11) web/issue queries were noisy and are not used as evidence that no result exists. A final source refresh again found no matching prior upper bound. The live web tool returned 403 for the problem page; ordinary direct retrieval succeeded, so the live site was actually read rather than inferred from that failure.

**Exact statement suitable for public use:** Every two-colouring of all subsets of [11] contains a nonempty monochromatic family of at least seven sets closed under binary union and intersection. The colouring χ(S)=1 exactly when |S|∈{0,4,7,8,9,11} has no such family with eight or more members. Hence the Erdős–Ulam sublattice function satisfies f(11)=7.

Credit the earlier lower bound to the omega institute and Bhattacharjee–Mandal–Bhattacharya, and the candidate colouring to the producer of the supplied certificate. The closure-SAT method is already in the BMB paper. This referee supplies independent code, freshly built solvers, checked proofs and an additional weighted-poset verification. **Did this referee find something new? No:** this job validates the supplied candidate; it does not claim to have originated the colouring or a new general method. The candidate answers the specific finite question left open in the sources examined. It does not settle the asymptotic problem #1183 or determine F(11).

**Gap between CNF and mathematical statement:** none found. The closure clauses and exact cardinality recurrence establish both directions of the translation in (b). Binary operations, arbitrary selected cardinality ≥8, and the absence of endpoint restrictions all match (a). The arbitrary-colouring reduction in (c) is essential and has been supplied explicitly.

**Limits, with file references:** (1) Priority is not exhaustive: the OpenAI recursive tree response is truncated (`sources/lab_scan.json:21`), and the named repository_of_problems and EinsteinArena endpoints return 404 (`:16`, `:26`); OpenAI's overview was separately searched. Off-allowlist community sources and private work were not consulted. (2) This is a conventional computational/mathematical referee result, not a newly kernel-checked formal proof; the executable proof checker is the C implementation pinned in `BUILD_COMMANDS.txt:6`. (3) The large DRAT bytes were removed from the job after successful checking and hashing, as allowed; replay regenerates them (`PROOF_HASHES.json:3`, `:8`). These are provenance, priority and verification-framework limits, not unresolved mathematical conditions on the finite equality. No required mathematical item was left unfinished for lack of time.

CONTRADICTING: The old conjectural chain equality would give f(11)=6, but the earlier published lower bound already disproves it (`sources/omega.md:123`). The site's older chain-only discussion is incomplete, not contrary evidence. The fresh no-eight proofs and weighted-poset enumeration agree, and no conflicting f(11) certificate or earlier exact claim was found in the stated search.

LABELS: Independently checked exact finite equality, f(11)=7; published lower bound reproduced; supplied upper-bound construction verified. Not a solution of the full asymptotic problem, not a new general method, and not a guarantee of publication priority. Evidence: `logs/c0_k8.check:8`, `logs/c1_k8.check:8`, `logs/rank_lattices.log:7`, `logs/published_lower.log:1`.

VERDICT: HOLDS
