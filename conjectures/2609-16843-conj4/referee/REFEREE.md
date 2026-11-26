VERDICT: HOLDS WITH CAVEATS

Conjecture 4 of van Berkel and Bosma v2 is false as printed. Ultimate periodicity holds throughout the stated family. The minimal parameters are those in the producer's main theorem. The most consequential error in its supporting evidence is a machine-readable block that omits the seed 1 for every $d\ge6$. There are also false finite-sum statements in the written proof. The corrections below suffice. All line references to the producer's proof refer to the unchanged [PROOF.md](inputs/PROOF.md).

## Certified sequence

Each row gives every entry, in increasing order. Include the finite prefix once, then include the indicated block translated by every nonnegative multiple of $m$. Brackets denote inclusive integer intervals.

| $d$ | Minimal $(k,p,m)$ | Finite prefix | First periodic block |
|---|---|---|---|
| 3 | $(5,1,5)$ | $1,2,5,6,7$ | $11$ |
| 4 | $(7,3,27)$ | $1,3,7,8,9,10,15$ | $29,35,36$ |
| 5 | $(13,10,104)$ | $1,4,9,10,11,12,13,19,37,45,46,72,79$ | $80,81,114,115,116,123,149,150,158,176$ |
| $d\ge6$ | $(d+3,d,8d-3)$ | $1,d-1,[2d-1,3d-2],4d-1$ | $[10d-5,11d-6]$ |

At $d=6$ the prefix is $1,5,11,12,13,14,15,16,23$, and the first block is $55,56,57,58,59,60$. The next begins at 100. The proof below applies to unbounded integer $d$. The separate computation covers $d=3,\ldots,40,50,100$, including all 30 requested cases and the ten additional rows supplied for comparison.

## Statement and interpretation

The exact source text, including its examples and notation, is extracted verbatim in [PRIOR_ART.md](PRIOR_ART.md). TeX 51–58 and 718–722 fix the three seeds, strict distinctness and greedy order. TeX 72–118 and 1194–1196 identify the one-based indicator $C$, the gaps $D_i=s_{i+1}-s_i$, the least binary period $m$, the number $p$ of members per cycle, and the number $k$ of members in the least binary preperiod. $K$ below counts integer positions. Proof lines 7–16 paraphrase the definitions faithfully. Their membership criterion follows by induction on the candidate integer above the largest seed. TeX 164–169 and proof line 22 give the same typeset statement. The literal TeX changes only line wrapping and $d\geq 3$ to the equivalent $d \ge 3$. Only 3 and 5 are exempt from the parameter formula. The source leaves this family conjectural. The small-case breakdown is supplied by the producer.

TeX 278–289 is the labelled cutoff lemma. For three summands its bound really is $(Q-6)M\ge2K$, and TeX 328–329 gives continuation of the actual observed block. **Its v2 number is 7.** Six numbered environments precede it on the shared counter declared at TeX 12–20. In proof lines 17, 105–106, 154–155, 162, 165 and 176 replace “Lemma 3” by “Lemma 7 (Section 3, label `lemma`)”. The certificate key `lemma3` contains values for that correct criterion. A second numbering slip in the producer report, line 79, calls the discussion at TeX 1211 “Remark 10”. It is Remark 26 on the same counter.

Counting binary positions as the preperiod gives 15 at $d=4$ and 23 at $d=6$, whereas the printed entry counts are 7 and 9. This change cannot alter the recurring counterexamples. Two readings of “modulo” can be tested directly.

- For binary periods, every eventual shift is a multiple of the primitive shift. $27\nmid31$ and $45\nmid47$. Starting later or using a nonminimal preperiod cannot change either fact. For explicit recurring mismatches, $29+27j$ is present and $60+27j$ absent at $d=4$. At $d=6$, $60+45j$ is present and $107+45j$ absent.
- Even if one tests only $s_{i+p}\equiv s_i\pmod{8d-1}$, the claimed $p$ fails. At $d=4$, $s_8=29, s_{12}=62$ differ by $33\equiv2\pmod{31}$. Translating each by 27 gives arbitrarily late failures at the same index phase. At $d=6$, $s_{10}=55, s_{16}=100$ differ by $45\equiv-2\pmod{47}$ at every corresponding phase. The actual gap words are primitive and all their entries lie strictly below the proposed moduli, so periodicity of the reduced entries forces an index period divisible by 3 and 6 respectively. A shift of $3q$ or $6q$ entries advances by $27q$ or $45q$. The least eventual index periods of the reduced entries are therefore 93 and 282. At $d=4$ the displacements over four terms in the three phases are $27+6,27+1,27+20$. Their gcd is 1, so no modulus of at least 2 can make four entries a period even under this weaker interpretation. For every $d\ge6$, a shift of $d$ entries advances by $8d-3\equiv-2\pmod{8d-1}$.

## Corrections to the supplied proof and witness

1. **Wrong singleton in the symbolic witness.** The encoding at witness line 87 means $[c_1,c_0]=c_1d+c_0$. Lines 105–114 give both endpoints of `blocks.U1` as `[1,0]`. At $(d,n)=(6,1)$ the encoded union omits the first seed, and at $(6,6)$ it adds a nonseed below 11. Set both endpoints to `[0,1]`. Proof lines 196–203 already use 1. The original digest matches, but exact agreement with every scientific value in the original JSON fails. [Witness](inputs/witnesses.json)
2. **Coefficient cutoff at proof line 73.** Restrict the displayed coefficient sum to $0\le i\le\min(n,N_T)$, or explicitly set its coefficient to zero when $i>n$. The power-series expansion at line 81 has this restriction. With the polynomial convention for binomials, at $(d,n)=(3,8)$ the printed sum gives 12 instead of 6. The raw strict counts at $n=8,38,68,98$ are $1,6,16,32$, so $[x^{98}]T=6(32-3\cdot16+3\cdot6-1)=6$. The term at $i=98$ contributes a spurious $6\binom{-1}{2}=6$. The sole strict triple is $(1,2,5)$. Under the combinatorial zero-extension convention the formula is already correct.
3. **Necessity in proof lines 75–81.** Nonnegativity of the first and second Newton differences on gap progressions suffices. The parenthetical converse at line 81 needs justification beyond positivity of the quadratic on nonnegative integers. For example $2-j+\binom j2$ stays positive and has first difference $-1$ at zero. This is a logical gap in the general criterion, without a failing family instance. To retain the iff and the original sign tests, in line 74 take $n_{\rm start}=1+\max(N_T,b_p,3a_k,h)$, using $a_0=0$. For $n\ge n_{\rm start}$ each representing triple has largest member above $a_k$ and hence in the tail. Increasing that member by $L$ injects triples for $n$ into triples for $n+L$. This proves $\beta\ge0$. A quadratic with negative second difference eventually becomes negative, impossible for counts, so $\gamma\ge0$. The original and repaired cutoffs coincide in every tested case, including all 564 gap progressions at $d=5$. Alternatively the forward implication from the sign tests to the greedy identity suffices for all applications here.
4. **Two errors in the $d=4$ exclusion lists.** At proof line 130 the $+2$ list intersects $F_4$ in residues **10 and 15**. For instance $1+7+29=37\equiv10\pmod{27}$. All actual $+2$ sums are at least $1+3+29=33>15$. At lines 134–136 replace 21 with **25** in the list of ten sums. $3+7+15=25$ and no three distinct members of $F_4$ sum to 21. The corrected list is $11,14,18,19,20,23,25,26,28,32$ and remains disjoint from $A_4$.
5. **False covering condition at $d=5$, proof line 171(c).** The $c_r$ defined there is the *least* member of a progression. At $(5,221)$ the unique strict representation is $19+79+123$. Here $123=19+104$ and $79<19$ is false. Enumerating all $a<b<c_r$ at the ten specified starts misses residues $3,13,28,37,47\pmod{104}$. The first missing examples at or above 221 in these classes are 315, 221, 236, 245 and 255, respectively. Use a cover-specific base $c_0=c_r+104h$, $h\ge0$, and require $a<b<c_0$. Then $19+79+(123+104j)$ covers this example's progression. The 94 corrected covers have maximum threshold 221. For 171(a), interpret the finite-element test on **actual distinct lifts**. As bare numbers, $13+12+12=37$ and $13+12+54=79$, but the first repeats an element and the second uses 54 before its progression starts at 158. Actual strict lifts cannot hit these targets.
6. **Inequality annotation at proof line 237.** $7d-2<8d-3$ uses $d>1$. Replace “$d>-1$” there. At the tightest allowed parameter the upper sum $1+23+16=40<45$ is valid. There is no failing $d\ge6$ or omitted wrap here.
7. **False interval equality at proof line 288.** For $d=3$, the four listed sets are $[17,19],[18,20],\{18\},[22,24]$. Their union is $[17,20]\cup[22,24]$. Both 16 and **21** are missing from the seed-only sums in $[12,24]$. The first deviation remains 16. The sequence also contains 21. The elementary $d=3$ proof and the finite-cutoff proof determine its tail.

## Independent computation and the small cases

`referee_verify.py` first generates the raw membership word from the seeds, without loading the witness. In descending order of cardinality it adds every old two-term sum plus the new entry to the strict three-term sumset, then updates the pairs from the old singles. This is a distinct-subset recurrence. At each candidate above the third seed its bit in the triple-sum set decides membership. A second, literal sieve enumerates the strict triples as each largest term enters. It reproduces the accepted terms through every certified cutoff. The program discovers a binary width from the generated bits, finds the last mismatch against that shift, and applies the v2 cutoff to the resulting word. It separately tests binary rotations, gap rotations, and the last boundary mismatch. A later shift of any multiple agrees with the same eventual phase, so these tests also prove earliest onset among multiples.

| $d$ | $K,M,Q$ | Last integer needed by the paper's lemma | Members through cutoff | Last integer tested before using the infinite residue complement | GF numerator degree / nonzero coefficients |
|---|---|---:|---:|---:|---|
| 3 | 7, 5, 9 | 52 | 14 | 20 | 104 / 68 |
| 4 | 15, 27, 8 | 231 | 31 | 61 | 518 / 420 |
| 5 | 79, 104, 8 | 911 | 93 | 221 | 2059 / 1706 |
| 6 | 23, 45, 8 | 383 | 57 | 99 | 859 / 694 |
| 7 | 27, 53, 8 | 451 | 66 | 117 | 1012 / 821 |
| 50 | 199, 397, 8 | 3375 | 453 | 891 | 7591 / 6131 |
| 100 | 399, 797, 8 | 6775 | 903 | 1791 | 15241 / 12304 |

For every $d\ge6$, the cutoff row has $K=4d-1$, $M=8d-3$, $Q=8$, last index $68d-25$ and exactly $9d+3$ members. Its slack in the lemma is $8d-4$. The repeated blocks start after the three compulsory seeds. At $d=3,4,5,6$ the last mismatching binary positions are respectively 7, 15, 79 and 23. Translating each by its $m$ gives an absent position (12, 42, 183 or 68) in the same eventual phase.

The independent residue test builds the entire triple-sum set. Choosing $s$ terms in one tail progression with base $b$ has minimum $sb+\binom{s}{2}m$. All higher sums in that residue are attained by increasing the largest chosen index. For each count through three, the program keeps exact sums of finite-only choices and the least attainable unbounded sum per residue. It processes each progression once with descending counts. After the largest finite point and the largest ray starts on both sides, it compares the two residue sets for exact complementation. Below that bound it tests each integer above the seeds. This argument proves both greediness directions independently of the finite-repetition lemma.

A third calculation uses integer coefficient arithmetic on $A(x)^3-3A(x)A(x^2)+2A(x^3)$ to count ordered distinct triples. Multiplication by $(1-x^{6m})^3$ recovers the numerator and its degree. Beyond that degree the counts on each class modulo $6m$ are quadratic. The verifier checks the finite section and all Newton coefficients on every residue. It reconstructs all 38 finite certificate records, including cutoff counts, both gap words and GF metadata. Serializing this full field reproduces 64,830 input bytes. Reconstructing the three small residue certificates reproduces a further 30,954 input bytes. The producer report mentions these spot-checks, but the supplied witness contains no rows for them.

There is also an algebraic check on the GF degrees for the whole general family. Expand $A(x)$ at infinity. A ray beginning at $b$ contributes $-x^{b-m}-x^{b-2m}-\cdots$. The first backward layer $[2d-2,3d-3]$ cancels $[2d-1,3d-3]$ inside the initial interval, leaving positive $3d-2$ and negative $2d-2$. Thus $A=x^w+x^v+B$ with $w=4d-1,\ v=3d-2$, and the highest term of $B$ is $-x^{2d-2}$. Write $e_3(A)=(A^3-3A A(x^2)+2A(x^3))/6$ and $e_2(B)=(B^2-B(x^2))/2$. Expansion gives $e_3(A)=x^{w+v}B+(x^w+x^v)e_2(B)+e_3(B)$. Since $w>v>2d-2$, only the first term contributes at the highest degree $w+v+2d-2=9d-5$. Clearing the denominator adds $3L=18m$, giving $\deg T=153d-59$ for every $d\ge6$. This exceeds $3a_k=12d-3$ throughout the range, so the repaired converse argument uses the original cutoff even for uncomputed $d$.

For proof lines 48–64 the Bézout argument gives the primitive gap period as a divisor of every eventual index shift. Counting members in a translated window and summing the corresponding consecutive gaps then gives the binary modulus as a divisor of every eventual value shift. If $a_k\ne b_p-m$, the last disagreement of the actual indicator with the periodic extension is $K=\max(a_k,b_p-m)$. The last gap before the cycle also differs from the cyclic predecessor. This proves the asserted minimalities, including after permitting larger periods.

- **$d=3$, proof 87–106.** The split into the ray $1+5j$ and the points $2,5,7$ is exact. Among the ten unordered residue triples only $001$ and $222$ can sum to 1 modulo 5. Each exceeds an available multiplicity. No triplet reaches a seed, 6 or 7. The decompositions cover 8–10 and all four subsequent gap residues. At $j=0$ in lines 101–102, arrange 6 before 7. The incoming gap 4 differs from the periodic gap 5.
- **$d=4$, proof 110–155.** Using the split at lines 114–115, zero, one, two or three isolated summands exhausts the choices. The ten three-ray residues and the five translated two-ray sumsets miss $2,8,9$. Their smallest possible sums are 46 and 18, both above 15. For two isolated points, the ten pair sums at line 129 are correct. The three shifts miss the tail and the actual low triples miss the isolated points, after the correction to line 130. The fourth case uses the corrected finite list above. The written finite gap decompositions cover all 45 gaps in $[8,60]$, and the 24 ray formulas cover the missing classes from 61 on. The primitive gaps are $(6,1,20)$ and the incoming gap is 14.
- **$d=5$, proof 159–171.** The cutoff word has exactly ten members per 104 positions. Its gaps are $(1,33,1,1,7,26,1,8,18,8)$, with a single 33. The incoming gap is 1 and the cyclic predecessor is 8. The finite/ray split at 169–171 has the stated six isolated points and ten rays. Among the $220+330+150$ ray-containing residue patterns none hits a tail residue. Checking actual lifts handles all isolated-point targets. All 20 isolated triple sums agree with line 171(b), including 54 below its ray start. After the base correction at 171(c), the residue certificates cover 186 finite gaps and 94 infinite residue classes.
- **$d=6$, proof 175–178.** The directly regenerated data above and the general proof below both give the block 55–60 translated by 45. The first altered candidate term for the printed modulus appears at 100.

## General proof, checked for every integer $d\ge6$

### Interval lemma, seed agreement and the division into levels

At lines 184–191 the minimum and maximum pair sums are $2\alpha+1,2\beta-1$. The choice $u=\max(\alpha,s-\beta),v=s-u$ attains every intermediate value with $u<v$. For triples, fixing the least element $\alpha$ gives $[3\alpha+3,\alpha+2\beta-1]$. Above that, fixing $\beta$ leaves a pair sum from $\alpha+\beta$ through $2\beta-3$, inside the pair range of $[\alpha,\beta-1]$. The equality endpoint belongs to the first branch. A three-element interval gives a singleton triple range and needs no second branch.

At 195–205 the successive differences between the eight displayed endpoints are $d-2,d,d-1,d+1,6d-4,d-1,7d-2$. All are positive at 6 and increase with $d$. Thus the pieces are disjoint, the first three entries are exactly the seeds, and summand membership/exclusion above $2d-1$ determines the greedy set by induction.

At 211–227 write $x=qm+r$ with $m=8d-3$. At level zero the allowed set is $F=\{1,d-1,4d-1\}\cup I$, $I=[2d-1,3d-2]$. At every positive level it is $R=[2d-2,3d-3]$. The leftmost residue of $J=I\cup R$ is available only at positive levels, its rightmost only at level zero, and each interior residue at every level. The singleton residues outside $J$ occur only once. This description recovers the tail exactly by subtracting $m$ from its first block. The unreduced sum $\Sigma$ of any three residues satisfies $3\le\Sigma\le12d-3<2m$ since $2m-(12d-3)=4d-3>0$. Thus carries are exactly the two possibilities 0 and 1.

### Part A, exclusion

Use $u=1,v=d-1,w=4d-1$. Denote the sum of the three input levels by $Q$. At lines 229–231 each of $u,v,w$ may occur at most once. The number of $J$ letters can be 0, 1, 2 or 3, giving $1+3+3+1=8$ types. Equal residues in $J$ may represent distinct integers on different levels. The bounds below allow them. Within $J$, only its top residue $3d-2$ is forbidden twice.

| Proof lines | Type | Unreduced sum or range | Reason neither target is hit |
|---|---|---|---|
| 233 | $uvw$ | $5d-1$ | Strictly between $w$ and $m$. |
| 234–236 | $uvJ$ | $[3d-2,4d-2]$ | The lower endpoint requires $r=2d-2$, hence $Q\ge1$. Its output $3d-2$ is level-zero only. The rest lies strictly between $I$ and $w$. |
| 237 | $uwJ$ | $[6d-2,7d-2]$ | Entire range lies between $w$ and $m$, including its upper endpoint by $m-(7d-2)=d-1>0$. |
| 238 | $vwJ$ | $[7d-4,8d-4]$ | Lower endpoint exceeds $w$ by $3d-3$ and upper is $m-1$. |
| 239–241 | $uJJ$ | $[4d-3,6d-4]$ | No carry, and the lower bound exceeds $\max R$ by $d$. At level zero two distinct $I$ terms sum to at least $4d-1$ before adding $u$, so the result exceeds $w$. |
| 242 | $vJJ$ | $[5d-5,7d-6]$ | The lower endpoint exceeds $w$ by $d-4$, the upper lies below $m$ by $d+3$. |
| 243–245 | $wJJ$ | $[8d-5,10d-6]$ | Before the wrap the only possible values are $m-2,m-1$, both above $w$. After it the residue is $[0,2d-3]$ at a positive level, ending one below $R$. |
| 246–249 | $JJJ$ | $[6d-6,9d-8]$ | Without carry the lower bound exceeds $w$ by $2d-5$. With carry the residue is $[0,d-5]$, below $R$, and the output level is positive. |

For rows with two $J$ letters their sum is bounded above by $(3d-2)+(3d-3)=6d-5$. With three it is bounded above by $(3d-2)+2(3d-3)=9d-8$. These are bounds on residues irrespective of how widely separated the integers are. This accounts for every combination of initial and translated blocks. At $d=6$ the wrapped rows start from unreduced intervals $[43,54],[30,46]$ with $m=45$. At $d=7$ they are $[51,64],[36,55]$ with $m=53$. In particular, a wrapped residue 0 cannot enter either candidate set.

A second all-$d$ check in the verifier keeps $I$ and $T$ separate. Of the 35 three-letter multisets from $u,v,w,I,T$, 20 respect the singleton multiplicities. With singleton sum $s$, $i$ copies of $I$ and $t$ tail terms, the sum of the canonical residues before reduction lies between $s+i(2d-1)+\binom i2+t(2d-2)$ and $s+i(3d-2)-\binom i2+t(3d-3)$. If $t=0$, the upper bound precedes the first tail term and the interval avoids every initial piece. If $t>0$, the actual sum exceeds every prefix member and its unreduced residue interval must avoid $R$ and $R+m$ below $2m$. The code checks each separation as a strict affine inequality with positive value at 6 and nonnegative slope. These two conditions prove it throughout the half-line. This check allows tail elements from arbitrarily far apart translates. For the concrete residue count there are four single-use residues and $d$ repeatable residues. Choosing $h$ distinct single-use residues gives $\binom4h\binom{d+2-h}{3-h}$ multisets. Summing over $h=0,1,2,3$ gives respectively 180, 242, 316, 403, 504, 27,504 and 192,504 types at $d=6,7,8,9,10,50,100$, agreeing with the verifier's total 221,653.

The extension remark at line 251 is correct for the *candidate* even at 3–5. In the $vJJ$ row with $Q=0$ the minimum is $(d-1)+(2d-1)+2d=5d-2>w$ for $d\ge3$. With $Q>0$ the coarse minimum $5d-5$ exceeds $\max R=3d-3$. The other rows still separate their targets for these values (a carry range with a negative upper endpoint is empty). The same level check on the three small candidate sets leaves 56, 88 and 129 feasible residue multisets respectively, with zero exclusion collisions. The inclusion test below supplies the counterexamples to equality.

### Part B, inclusion

The pair and triple sumsets at 257–259 are $[4d-1,6d-5]$ and $[6d,9d-9]$ by the strict interval lemma. From the *complement of the claimed set*, the gaps above the last seed are $[3d-1,4d-2]$, $[4d,10d-6]$, and $[11d-5,18d-9]+jm$ for $j\ge0$. The last interval runs from $\max T_j+1$ through $\min T_{j+1}-1$. Below, $\mathcal P,\mathcal T$ use two or three distinct members of $I$.

| Proof lines | Summands | Covered interval, before any $jm$ translation |
|---|---|---|
| 263–266 | $1,\ d-1,\ x\in I$ | $[3d-1,4d-2]$ |
| 270 | $1+\mathcal P$ | $[4d,6d-4]$ |
| 271 | $(d-1)+\mathcal P$ | $[5d-2,7d-6]$ |
| 272 | $1+I+(4d-1)$ | $[6d-1,7d-2]$ |
| 273 | $\mathcal T$ | $[6d,9d-9]$ |
| 274 | $\mathcal P+(4d-1)$ | $[8d-2,10d-6]$ |
| 294 | $1+(d-1)+T_j$ | $[11d-5,12d-6]$ |
| 295 | $1+I+T_j$ | $[12d-5,14d-7]$ |
| 296 | $(d-1)+I+T_j$ | $[13d-7,15d-9]$ |
| 297 | $\mathcal P+T_j$ | $[14d-6,17d-11]$ |
| 298 | $I+(4d-1)+T_j$ | $[16d-7,18d-9]$ |

**Membership, ordering and size.** Each individual summand belongs to a displayed singleton, $I$, or $T_j$, all subsets of the proposed set. Within $I$ the strict interval lemma produces increasing indices. Across pieces the order is $1<d-1<\min I\le\max I<4d-1<\min T_j$. Sorting each triple therefore gives $a<b<c$. Every triple has $n-c=a+b\ge3$. In lines 292–298 adding $T_j$ to an entire pair-sum interval leaves no internal holes. For integer intervals $[l,h]$ and $[u,v]$, each $n\in[l+u,h+v]$ is reached using $x=\max(l,n-v)$ and $n-x\in[u,v]$. The chosen pair realizing $x$ stays strictly below the tail entry.

**Joins.** In lines 276–282 the four slacks “preceding upper endpoint plus one minus following lower endpoint” are $d-1,d-4,d-1,d-6$. Their nonnegativity and the extreme endpoints give precisely the second gap. The extra interval at 284 ends at $8d-4$, below the bridge integer $8d-3$, and the extra singleton is $5d-1$. In 300–307 the four slacks are $0,d-1,d-2,d-3$. The common $jm$ cancels, so every translated gap has the same coverage.

| Check at the boundary | $d=6$ | $d=7$ |
|---|---|---|
| First gap | 17–22 | 20–26 |
| Five intervals of the second gap | 24–32, 28–36, 35–40, 36–45, 46–54 | 28–38, 33–43, 41–47, 42–54, 54–64 |
| Five intervals of the first recurring gap | 61–66, 67–77, 71–81, 78–91, 89–99 | 72–78, 79–91, 84–96, 92–108, 105–117 |

At $(6,45)$ take $14+15+16$. At $(6,46)$ take $11+12+23$. At the shared endpoint $(7,54)$ either $17+18+19$ or $13+14+27$ works. The first recurring gap at $d=6$ begins at $61=1+5+55$ and ends at $99=16+23+60$, immediately before the next block at 100. These are distinct, smaller members even at equality in the interval bounds.

**Small-$d$ breakdown, lines 286–290.** After the three seeds, the least possible forbidden sum is $3d-1$. Hence the sequence fills $I$ first. The sums $1+(d-1)+I$ cover the next gap through $4d-2$. To hit $4d-1$ using two members of $I$ and a smaller seed would already require at least $1+(2d-1)+2d=4d$. Three from $I$ cost still more. Thus all three small cases reach the stated $S_0$. The seven classes of sums above $4d-1$ listed on line 287 exhaust triples from $S_0$ by how many of the three singletons they use. Directly subtracting these sums from $[4d,10d-6]$ gives $\{16,21\}$, $\{29\}$, $\{37\}$, respectively. Each *first* hole is forced into the true sequence because all smaller candidates since $4d-1$ already had representations. Later new entries must still be checked by the recurrence. The full small-case certificates above establish the subsequent tails. For $d\ge6$, Parts A and B give both membership directions and the common seeds give equality by induction (line 309).

### Part C, minimality

Proof 313–323 counts $1+1+d+1=d+3$ prefix entries and $d$ entries from $10d-5$ to $11d-6$. Direct subtraction gives the finite gap word
$$
(d-2,\ d,\ 1^{d-1},\ d+1,\ 6d-4)
$$
followed by repetitions of $(1^{d-1},7d-2)$. At 325–326 the single occurrence of $7d-2>1$ forces a primitive index period $d$. The displacement across it is $(d-1)+(7d-2)=8d-3$. For any other eventual binary period, every sufficiently far-out interval of that width contains the same number of members. It therefore gives a gap period and advances an integer multiple of $d$ members. Its displacement is the same multiple of $8d-3$.

At 327–329 the incoming gap $6d-4$ differs from its cyclic predecessor $7d-2$ by $d+2$. At any multiple of the period the same mismatch remains, so the least difference preperiod is $d+3$. The backwards periodic extension's latest member before the first tail block is $3d-3$. The actual final prefix member is $4d-1$ and all later positions agree with the extension. In particular $4d-1$ is present but has an absent eventual residue, so any earlier binary start fails for every period multiple. The least binary preperiod is $K=4d-1$, containing exactly $d+3$ ones. This proves Part C for the entire range.

## Referee checks

Run `nice -n 10 python3 -B referee_verify.py` from this directory. The verifier completes the mathematical checks and returns status 1 for the false symbolic witness field.

- CONTROLS: No. Both primary-source positive controls reproduced. The independent verifier rejected 5/5 supplied mutants. The wrong-set controls first disagree with greedy membership at 60, 100 and 23. The other two define the correct set, pass the greedy, residue and generating-function set tests, and fail minimality. It also rejected 969 later boundaries (every phase in each tested case), 40 earlier ones, 80 shifted blocks and 80 nonminimal multiples. The primitive-word and boundary arguments handle arbitrary multiples and shifts. [Verifier](referee_verify.py)
- CONTRADICTING: No. All 38 supplied rows, both additional spot-checks, the three small-case deviations, and 221,653 admissible concrete residue multisets were retained. The whole witness fails semantic equality at its singleton field. The proof's false statements at lines 130, 135, 171 and 288 remain visible in the corrections. [Original evidence](inputs/witnesses.json)
- LABELS: No. I counted the TeX environments, decoded the affine coefficients, reconstructed the greedy data from the three seeds, and regenerated the small witnesses including their exact triples. The four inputs establish the comparison against v2. A claim of external priority would require a separate literature check. [Source extracts](PRIOR_ART.md)

This is AI work. No human has checked it.
