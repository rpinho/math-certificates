# Finite block and capacity lower bound

Let f(n) be the largest size of a family of subsets of an n-point set with no three distinct members A,B,C satisfying A∩B=A∩C=B∩C. Define C49=limsup f(n)^(1/n). Sperner (no proper containment between members) is a hypothesis of the gluing construction; it is not an added restriction on the capacity definition.

## Finite certificate

`certificates/best_1.5678643845728069793620.json` supplies all 252303 integer masks, n=28 and ports [0,1]. Point i is bit i; a mask represents its set of 1 bits. The mask range is [0,2^28), the masks are distinct, and every point occurs. Bits 0–7 are the surviving core edges 01,02,12,13,14,23,24,34; bits 8–17 and 18–27 are the two pendants. The exact baseline difference removes 21 and adds 32 members, all added members having seven points and avoiding the two ports.

The complete family is Sperner and contains no three distinct sets with equal pairwise intersections. Two exhaustive implementations verify this directly from the masks. The producer's `checker.py` derives disjoint Cartesian boxes from the data and tests pair/triple existence on every factor. After the Sperner check, a sunflower with a repeated member must have all three members equal; cross-box triples therefore need no repetition subtraction. Within-box triples are explicitly tested for nonconstant witnesses. Details are in `SEARCH_NOTES.md`.

The clean-room referee's `referee/independent.cpp` derives a shared binary decision diagram from all masks. At each coordinate it counts containment patterns 00,01,11, and equal-intersection triple patterns 000,100,010,001,111. For M distinct members, ordered containment count P and ordered equal-intersection triple count Q obey Q=M+3(P−M)+6s, where s counts sunflowers of three distinct members. Both baseline and candidate have P=Q=M, so there are no proper containments or distinct sunflowers. This checker assumes neither the ingredient families nor a product decomposition. See the retained report, section (b), and `release_validation/referee_candidate.json`.

## Gluing lemma and its hypotheses

The operative DEGKM1997 Lemma 4.4 statement, quoted in `SOURCE_STATEMENTS.md` from the pinned MIT baseline format, is as follows. Let A and B be Sperner, sunflower-free families on disjoint ground sets X,Y, and let a∈X,b∈Y. Retain pairs (A,B) with opposite a,b memberships and send them to (A\{a})∪(B\{b}). The resulting family on (X∪Y)\{a,b} is Sperner and sunflower-free, and has |A_(a=1)||B_(b=0)|+|A_(a=0)||B_(b=1)| members.

Here is the referee's argument for the statement actually used. If one glued output is contained in another and the a-bits agree, restoring the deleted bits makes both factor projections inclusions, so Sperner forces equality. If the first a-bit is 0 and the second 1, restoring a gives a strict inclusion in A; if reversed, restoring b gives a strict inclusion in B. Both are impossible. This proves Sperner and injectivity of the retained-pair map, hence the cardinality formula.

In a Sperner, sunflower-free family, an equal-intersection triple allowing repetitions is necessarily all equal. Three distinct members are forbidden; two equal members would be contained in the third. Suppose three glued outputs have equal intersections. Let r be the number of 1s among their a-bits. If r=1, restoring a preserves the equal-intersection property in A, forcing three identical originals with different a-bits, a contradiction. If r=2, the complementary b-bits have one 1, giving the contradiction in B. If r=0 or 3, restoring the ports preserves equal intersections in both factors, forcing both triples of originals, and then all outputs, to be identical. Thus distinct output sunflowers are impossible.

The finite checker establishes all hypotheses on the candidate. Fresh copies are relabelled to disjoint ground sets, and input and output ports are distinct. No further pendant-shape hypothesis is needed for the augmented block. The original 1997 typeset lemma was not inspected by the producer or referee; the operative statement has the explicit proof above.

## Transfer matrix and rate

For a block on n points with ports p,q, put N_ab=#{S: [p∈S]=a,[q∈S]=b}. If (u_k,w_k) counts a chain's members avoiding/containing its remaining output port, then opposite-bit pairing gives

\[
(u_{k+1},w_{k+1})=(u_k,w_k)T,\quad
T=\begin{pmatrix}N_{10}&N_{11}\\N_{00}&N_{01}\end{pmatrix},\quad
(u_1,w_1)=(N_{00}+N_{10},N_{01}+N_{11}).
\]

All four counts are positive. A positive Perron eigenvector bounds the positive start vector below by a positive multiple, so the total count is at least c rho(T)^k for c>0. The k-block chain occupies kn−2(k−1)=k(n−2)+2 points. The defining limsup yields C49≥rho(T)^(1/(n−2)). This is the IRSI exact chain-count argument applied to the same gluing lemma.

For the candidate, (N00,N01,N10,N11)=(33980,64728,64728,88867), so

\[
T=\begin{pmatrix}64728&88867\\33980&64728\end{pmatrix},\quad
\rho=64728+\sqrt{33980\cdot88867}=64728+\sqrt{3019700660}.
\]

Since n−2=26, the claimed exact rate follows. Koshta's same-size block has N00=33969 and the other three counts unchanged. Its radicand is 3018723123. Their difference 977537=11·88867 is strictly positive, so the candidate rate strictly exceeds the exact incumbent under the same definition and exponent.

Integer root isolation gives strict rational enclosures of both rates and their difference. For x=h/d>0, compare x^26 with a+sqrt(b): if z=h^26−a d^26 is nonpositive the comparison is negative; otherwise compare z² with b d^52. Binary search gives consecutive decimal endpoints without floating-point decisions. In particular R>1.5678643845. The retained and fresh `exact_rates.json` provide the full interval and the decimal caveat; this proof uses the exact algebraic expression.

## Sources and scope

`SOURCE_STATEMENTS.md`, `producer/REPORT.md`, `SEARCH_NOTES.md` and the byte-preserved `referee/REFEREE.md` are the source texts. The candidate is AI-refereed, has no human review and is not claimed optimal. No new gluing theorem is claimed.

- D. Koshta with Claude, incumbent two-pendant block: [certificate and mathematical proof](https://github.com/DennisKoshta/sunflower3-49a-certificate/blob/c4ee81737f9f6a4ae9793586a27004553a12d5c0/PROOF.md), commit `c4ee81737f9f6a4ae9793586a27004553a12d5c0`. Its table contribution was merged as teorth PR #260 at [commit `2d8eba58ea108f8cf746dbab8712ad317202d6c5`](https://github.com/teorth/optimizationproblems/commit/2d8eba58ea108f8cf746dbab8712ad317202d6c5).
- Aspect5 / Institute for Recursive Self Improvement (IRSI), [exact transfer construction](https://github.com/Aspect5/sunflower-free-capacity/tree/e478c81d8b57eba956fdaf621643eb6f0781f820). Cited only; no content from that unlicensed repository is included.
- joshua17-create with Claude, [F/H families](https://github.com/joshua17-create/sunflower-lower-bound/tree/6e34d78ab482f4cfd5a5ece62a6d06141e3e8c8d).
- Sylla, [pendant augmentation](https://github.com/xSyllaa/sunflower-pendant-chain/tree/8e21d0287711b4f0bfc23e9443523e2aa472cca1).
- W. A. Deuber, P. Erdős, D. S. Gunderson, A. V. Kostochka and A. G. Meyer, *Intersection statements for systems of sets*, J. Combin. Theory Ser. A 79 (1997), 118–132, Lemma 4.4. [DOI](https://doi.org/10.1006/jcta.1997.2778).
- [Tao table, pinned C49 definition and incumbent](https://github.com/teorth/optimizationproblems/blob/2d8eba58ea108f8cf746dbab8712ad317202d6c5/constants/49a.md).
