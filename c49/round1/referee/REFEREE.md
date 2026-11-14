# Independent referee of the C49 candidate

The exact claim under review is
\[
C_{49}\ge (64728+\sqrt{3019700660})^{1/26}
 =1.567864384572806979362033445047060687\ldots.
\]
The complete finite certificate and the finite-to-asymptotic argument support this claim. The task title's ten-place number `1.5678643846` needs a rounding qualification: it is larger than this certificate's rate. This is the sole caveat to the verdict; it does not qualify the exact algebraic bound.

## (a) Definition and gluing

The [live table](https://teorth.github.io/optimizationproblems/constants/49a.html), fetched on 2026-11-14, defines the constant as follows (verbatim mathematical definition, also saved at `sources/live49a.md:11`):

> Let $[n]:=\\{1,2,\dots,n\\}$ and let $f(n)$ denote the maximum size of a sunflower-free family $\mathcal{F}\subseteq 2^{[n]}$.
> Define
> $$
> C_{49}\ :=\ \mu^{\mathrm S}\_3\ :=\ \limsup\_{n\to\infty} f(n)^{1/n}.
> $$

For three **distinct** members, the forbidden condition is exactly
\(A\cap B=A\cap C=B\cap C\). Sperner is an additional hypothesis of the construction, not a restriction in the definition of the capacity. Indexing the certificate's points from 0 instead of 1 is a bijective relabelling.

The table lists **“$\ge 1.5678599$”** for Koshta, whose exact value is
\((64728+\sqrt{3018723123})^{1/26}\). [PR #260](https://github.com/teorth/optimizationproblems/pull/260) is merged; [PR #322](https://github.com/teorth/optimizationproblems/pull/322) is open and clarifies the augmentation count without changing that bound. Both were read with the specified `gh` executable; their complete responses are `pr260.json` and `pr322.json`.

**Finite gluing statement used.** Let \(\mathcal A\subseteq2^X\) and \(\mathcal B\subseteq2^Y\) be Sperner and 3-sunflower-free, with disjoint ground sets, and distinguished points \(a\in X,b\in Y\). Retain pairs \((A,B)\) whose memberships at \(a,b\) are opposite, and map them to
\[
(A\setminus\{a\})\cup(B\setminus\{b\}).
\]
The resulting family is Sperner and 3-sunflower-free on \((X\cup Y)\setminus\{a,b\}\), and its cardinality is
\[
|\mathcal A_{a=1}|\,|\mathcal B_{b=0}|+
|\mathcal A_{a=0}|\,|\mathcal B_{b=1}|.
\]
This is the DEGKM1997 Lemma 4.4 statement used by [Koshta's pinned proof](https://github.com/DennisKoshta/sunflower3-49a-certificate/blob/c4ee81737f9f6a4ae9793586a27004553a12d5c0/PROOF.md) and the [IRSI construction](https://github.com/Aspect5/sunflower-free-capacity/blob/e478c81d8b57eba956fdaf621643eb6f0781f820/README.md). I did not retrieve the original 1997 journal PDF, whose linked host is outside this job's network whitelist. I independently prove the required statement next, so the conclusion does not rest on accepting an unchecked lemma citation.

**Independent proof.** Suppose one glued output is contained in another. If their \(a\)-memberships agree, restoring the deleted points makes both factor projections inclusions; Sperner forces equality. If the first has \(a=0\) and the second \(a=1\), restoring \(a\) gives a strict inclusion in \(\mathcal A\). If the memberships are reversed, the complementary \(b\)-memberships give a strict inclusion in \(\mathcal B\). Both cases are impossible. This also proves that different retained pairs cannot yield the same output, establishing the cardinality formula.

In a Sperner, 3-sunflower-free family, any three members with equal pairwise intersections, **allowing repetitions**, are all identical: three distinct ones are forbidden, and two equal ones would be contained in the third. Now suppose three glued outputs have equal pairwise intersections. Their projections away from the deleted points have this property in both factors. Let \(r\) be the number of their three \(a\)-bits equal to 1. If \(r=1\), restoring \(a\) preserves equal intersections in the first factor, so its three originals must be identical, contradicting their differing bits. If \(r=2\), restoring \(b\), which occurs once, gives the same contradiction in the second factor. If \(r=0\) or \(3\), restoring both ports preserves equal intersections in both factors; both triples of originals are identical, hence so are the outputs. Thus no three distinct outputs are a sunflower.

**Exact chain statement.** For a valid block on \(n\) points with distinct input/output ports \(p,q\), put
\[
N_{ab}=\#\{S:[p\in S]=a,[q\in S]=b\},\qquad
T=\begin{pmatrix}N_{10}&N_{11}\\N_{00}&N_{01}\end{pmatrix}.
\]
Using a row vector \((u_k,w_k)\) for the counts avoiding/containing the current output port gives
\[
(u_{k+1},w_{k+1})=(u_k,w_k)T,\qquad
(u_1,w_1)=(N_{00}+N_{10},N_{01}+N_{11}).
\]
This follows directly from the opposite-bit pairing in the two branches of the lemma. Fresh copies have disjoint relabelled ground sets, and \(p\ne q\) leaves the new output port available. After \(k\) copies the ground set has
\(kn-2(k-1)=k(n-2)+2\) points. If all four counts are positive, the positive start vector and a positive Perron eigenvector give \(|\mathcal R_k|\ge c\rho(T)^k\) for a constant \(c>0\). Therefore
\[
\boxed{C_{49}\ge \rho(T)^{1/(n-2)}}.
\]
The defining limsup already suffices for this subsequence argument. The page also states that it is a limit; no stronger limit assumption is needed here.

**Hypotheses for this candidate.** Sections (b) and (c) establish a distinct Sperner, sunflower-free family on 28 points; ports 0 and 1 are different and all four counts are positive. Disjointness between copies is obtained by relabelling. Thus each new copy adds exactly **26** points. This is the same chain and rate formula used by the earlier IRSI, Cla2026, Syl2026 and Kos2026 entries, not the finite-family quantity \(|\mathcal B|^{1/28}\). IRSI's present/absent column convention has matrix \(JT^tJ\), where \(J\) swaps the two coordinates; it has the same eigenvalues. Here \(N_{01}=N_{10}\), so the displayed matrices agree even before taking their spectra.

## (b) Finite validity and exhaustiveness of my code

I wrote `independent.cpp` in this job directory. No producer checker, control program, search script, binary, or third-party code was read, copied, imported or run. Allowed producer reports and certificate data were read. The actual validity method uses a merged binary trie (a decision diagram), rather than the producer's Cartesian-box method. It derives every branch from the complete masks and assumes no product decomposition, uniformity, or validity of ingredient families.

First the code parses integers, checks \(0\le m<2^{28}\), sorts, and rejects duplicates (`independent.cpp:79`). The metadata is separately checked in `inspect_data.py`. Every sorted mask is inserted through all 28 bit positions, from bit 27 to bit 0. Identical suffix subtrees are shared; no bit position is skipped. The empty-family node and accepting terminal are different. Thus sharing preserves exactly the family of accepted bit strings.

Let \(P(x,y)\) count ordered accepted pairs from two diagram nodes with first set contained in second. For a bit, its permitted patterns are exactly \(00,01,11\). Summing these three disjoint recursive cases, with terminal count 1 and empty-node count 0, counts every containment pair once (`independent.cpp:48`).

Let \(Q(x,y,z)\) count ordered accepted triples with equal pairwise intersections, allowing repeated sets. At every bit the permitted patterns are exactly
\[
000,\quad100,\quad010,\quad001,\quad111.
\]
A pattern with exactly two 1s would make one pairwise intersection differ from the other two. The five recursive cases are disjoint and exhaustive (`independent.cpp:58`). Permuting the three nodes does not change this count, so sorted node triples share memoized counts; all five branch contributions are still added with their multiplicities. Induction on remaining bits proves exactness. Hash collisions are resolved by full key equality, not treated as equality of subproblems.

For a family of \(M\) distinct sets, write \(P=P(r,r)\), \(Q=Q(r,r,r)\). Then \(P-M\) is the number of proper containment pairs and
\[
Q=M+3(P-M)+6s,
\]
where \(s\) is the number of unordered sunflowers of three distinct members. The three terms represent all equal triples, triples with exactly two equal members, and all distinct triples. All counts fit in unsigned 64-bit integers: even the allowed input maximum \(300000^3\) is below \(2^{64}\). Acceptance requires both \(P=M\) and \(s=0\).

| Complete family | Members M | Ordered containment pairs P | Ordered sunflower tuples Q | Proper containments | Distinct sunflowers |
|---|---:|---:|---:|---:|---:|
| Koshta baseline, checked first | 252292 | 252292 | 252292 | 0 | 0 |
| Candidate | 252303 | 252303 | 252303 | 0 | 0 |

Evidence: `logs/baseline_check.json:1`, `logs/candidate_check.json:1`. The diagrams have 842 and 855 nodes including the two terminals, with 44,167 and 45,149 nonterminal triple subproblems respectively. These are exact complete-family checks, not samples.

**Literal cross-checks.** With seed 491114, I sampled 2048, 2500, and 3072 members from each complete family. On all six samples the dynamic program and an actual \(i<j<k\) triple loop agreed: zero sunflowers and zero proper containments. Twenty additional random families on seven points, including non-Sperner families, also matched exact literal counts; these exercise the repeated-member correction. `cross_checks.py` and `logs/cross_checks.json` retain the samples' results and seed.

The independently identified 21-member baseline exceptional subfamily was checked by both methods, including all \(\binom{21}{3}=1330\) literal triples (`logs/exceptions21_check.json:1`). To also cover the broader interpretation of “21-exception region,” `literal_region.cpp` separately loops over **each of those 21 pivots and every unordered pair of other members in the full 252292-member baseline**. It completed 668,330,212,095 pivot-triple incidences, with zero sunflowers and zero proper containments involving an exception (`logs/baseline_exception_region.json:1`). Each pivot contributed 31,825,248,195 literal triples. Triples involving more than one exceptional member are counted more than once; all triples involving at least one are covered. No structural pruning or intersection buckets were used in this loop.

## (c) Ports and exact rate

Ports are mask bits 0 and 1, corresponding to the edges 01 and 02 of the underlying \(K_5\). The count order here is \((N_{00},N_{01},N_{10},N_{11})\), with the first subscript referring to bit 0. `independent.cpp:90` recounts these directly from every mask.

| Quantity | Published/claimed | Independently obtained |
|---|---|---|
| Baseline port counts | (33969,64728,64728,88867) | (33969,64728,64728,88867) |
| Candidate port counts | (33980,64728,64728,88867) | (33980,64728,64728,88867) |
| Baseline Perron root | \(64728+\sqrt{3018723123}\) | \(64728+\sqrt{33969\cdot88867}\), equal exactly |
| Candidate Perron root | \(64728+\sqrt{3019700660}\) | \(64728+\sqrt{33980\cdot88867}\), equal exactly |
| Baseline rate | 1.56785990242458988585… | 1.567859902424589885852915429132277612… |
| Candidate rate | 1.56786438457280697936… | 1.567864384572806979362033445047060687… |

The candidate matrix is
\[
T=\begin{pmatrix}64728&88867\\33980&64728\end{pmatrix}.
\]
Its characteristic equation is \((x-64728)^2-3019700660=0\); the plus root is the Perron root. The baseline uses 33969 instead of 33980. Since
\[
3019700660-3018723123=977537=11\cdot88867>0,
\]
the exact candidate rate is strictly larger. The exponent and underlying definition are the same, so this is a comparison against the exact incumbent, not merely against its truncated table entry.

`exact_rates.py` uses Python integers only. For \(x=h/d>0\), it compares \(x^{26}\) with \(a+\sqrt b\) by first checking the sign of \(z=h^{26}-ad^{26}\), then comparing \(z^2\) with \(bd^{52}\) when \(z>0\). Integer binary search provides consecutive 70-place decimal endpoints. Separately, `isqrt(b*10**140)` encloses the Perron root. The resulting strict enclosures are in `logs/exact_rates.json`:

\[
\begin{aligned}
1.5678643845728069793620334450470606872892287108640663818058357542363321
&<\rho(T)^{1/26}\\
&<1.5678643845728069793620334450470606872892287108640663818058357542363322.
\end{aligned}
\]

The exact improvement over the baseline is between
`0.0000044821482170935091180159147830749067693242554392250907328019176417`
and the same prefix ending `6419`. No floating-point score is used. These are extremal-capacity bounds, not predictive metrics; the predictive-baseline/SBS rule is inapplicable.

## (d) Published baseline and exact delta

The baseline was downloaded as data from [the required commit](https://github.com/DennisKoshta/sunflower3-49a-certificate/blob/c4ee81737f9f6a4ae9793586a27004553a12d5c0/two_pendant_extra_1.5678599.txt.xz), before checking the candidate. `prepare_data.py` parses the point-list format, checks every point list, verifies the block header `(28,0,1,252292)`, and converts to masks. Its decompressed SHA-256 is

`10ee18f93204468f3611d2c909a9eee443f3b4769cf7fddd964209edfebd4838`.

The same independent checker accepts the full baseline, with exactly 252292 sets and counts (33969,64728,64728,88867). Its exact rate is independently reproduced in (c).

Set subtraction of the two complete families gives **252271 common members, 21 removed, and 32 added**, and both sorted difference lists equal `claimed_delta.json` exactly (`inspect_data.py`, `logs/data_comparison.json`). I additionally located the 21 baseline exceptions from their supports in the baseline itself: twenty lie wholly in bits 8–17, and the last is mask 268173364, the union of core bits 2,4,5 and all bits 18–27. Only after that classification is their equality with the removed list asserted.

The common family comprises 250659 members meeting both pendants and two groups of 806 lifted members. For each empty-pendant group, the masks form 15 core fibers: eleven with 46 distinct parts and four with 75, hence \(11\cdot46+4\cdot75=806\). `pendant_structure.py` independently constructs the 121-member family \(H\) from its three affine-orbit seeds and verifies **equality of each entire fiber** with the appropriate root-avoiding or root-containing projection family, not just its size (`logs/pendant_structure.json`). This confirms the substantive clarification in PR #322; “15 sets per pendant” without the lifting qualification would undercount.

The candidate JSON retained here is byte-identical to the supplied data and has SHA-256
`53381b5f52264c43d56343ab27d698c598462d5abfd83c043365afbae9efb1e8`.

## (e) Rejection controls

The full candidate was used for both controls. Neither result relies on accepting a malformed file or a duplicate as a surrogate for the intended defect.

1. **Sunflower control, still Sperner.** Add mask **218556764**. Existing masks 257280847 and 229432812, together with the new mask, have all three pairwise intersections equal to **218417484**. All three masks are distinct. The checker finds **6123** distinct sunflowers, zero proper containments, and exits 1. This added mask was found independently from the relation \(C=(A\cap B)\cup([28]\setminus(A\cup B))\); no producer control was used.
2. **Sperner control.** Add mask **0**. It is a proper subset of every original member, for example mask 16255. The checker finds **252303** proper containments and exits 1.

Evidence and explicit witnesses: `logs/controls.json:2`, `logs/controls.json:16`; the complete counts and exit codes are also retained in `logs/cross_checks.json`. The literal comparisons in (b) include non-Sperner random families, so the counting formulas are cross-checked outside the accepting regime as well.

## (f) Rounding, support, scope, and disposition

**Decimal caveat C1.** The task title's `C49 >= 1.5678643846`, taken as a literal rational lower bound, is **not established by this certificate**. Exact comparison proves the certificate's rate is smaller than that number (`logs/exact_rates.json:59`). This does not prove the capacity itself is smaller. The ten-place numeral is correct as a nearest-rounded approximation, provided it is marked as approximate. Use the exact surd expression, or the safe truncated inequality **C49 >= 1.5678643845** (`logs/exact_rates.json:60`). The longer claimed prefix `1.56786438457280697936...` is correct (`logs/exact_rates.json:61`). C1 is the only caveat; there is no finite-validity or gluing failure.

**Point and pendant support.** Every mask lies in `[0,2^28)`. The candidate's largest mask is 266598628, and the bitwise union of all masks is 268435455, so all 28 points, and no other point, occur. Every added member has size 7. Sixteen lie wholly in bits 8–17 and sixteen wholly in bits 18–27; all avoid the two chain ports and the rest of the core. All 1612 lifted members are retained. There is **no extra pendant-shape hypothesis in the chain gluing theorem**: the complete augmented block must be Sperner and sunflower-free, which was checked without structural shortcuts. One need not prove that the augmented block itself is an unaugmented gluing of F and H.

**What is and is not new.** Did this referee discover a new construction? **No.** It independently confirms an already supplied candidate. Does that candidate beat the printed exact Koshta bound under the same capacity definition? **Yes**, by the strict amount in (c). This is a numerical improvement within the existing construction and gluing method, not a new gluing theorem or a global-optimality result. `PRIOR_ART.md` records the live-table/PR/repository/paper evidence and limits of the broader prior-art search. No claim of global optimality or exhaustive worldwide novelty is made.

**Completeness and resources.** All finite properties requested in (a)–(f) are checked exhaustively or proved as specified above; samples only serve as cross-checks of the exhaustive method. The full-family decision-diagram checks used 7,684,096 bytes (baseline) and 7,766,016 bytes (candidate) peak RSS. The largest measured process in the sample/control runs used 79,675,392 bytes; at most two computational workers overlapped, both at nice 10, comfortably below the 4 GB job cap. The literal exceptional-region scan completed within the six-hour allowance; its timing and memory are recorded in `logs/baseline_exception_region_time.txt`. No requested check remains incomplete. The original 1997 typeset lemma was not directly inspected; the precise operative statement has instead been proved in (a). No external submission, commit, push, post, or message was made. Reproduction commands are in `REPORT.md`.

CONTROLS: Both full-size intended-defect controls reject with exit 1; the sunflower control remains Sperner. Evidence: `logs/controls.json` and section (e).
CONTRADICTING: No contradiction to the exact surd bound was found. The rounded-up title numeral is stronger than the certificate establishes; caveat C1 is proved in `logs/exact_rates.json:59`. The other requested full checks support the exact claim.
LABELS: Independent finite verification plus an explicit gluing proof; exact bound established, ten-place headline needs qualification; supplied construction reproduced, no optimality or new-method claim. Evidence: sections (a)–(f), `logs/candidate_check.json:1`, and `logs/exact_rates.json`.

VERDICT: HOLDS WITH CAVEATS
