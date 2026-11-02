# Independent adversarial review of C44 round 5

**Overall mathematical verdict: PASS.** I found no counterexample or invalid
inference establishing **C44 < 3.1674542553**. My subjective probability that
this bound is correct is **99%**, including its inherited inputs. This is a
fresh mathematical and computational review, not a proof-assistant certificate
or independent human referee report. I did not modify the target.

My code, importing none of the target's programs, reproduces

    125475790246857326765951236155 / 39614081257132168796771975168
      = 3.167454255278645604364490105637827330171324002522007098545...

and the exact same-horizon, same-tail improvement **417/512 = 0.814453125**.
The suspiciously large improvement survives the attacks below.

There is one **source-coverage GAP**: the full body of the original 1976
Kasami–Tokura–Azumi paper was inaccessible. I read its original abstract and
the original 1970 theorem in its publisher abstract, and checked the precise
second-weight corollary against accessible published statements. The extra
1976 classification is unnecessary here. I also give an independent inductive
proof of the entire corollary in [SOURCE_NOTES.md](SOURCE_NOTES.md), together
with a separate proof of the control-count bound. This access limitation does
not leave a mathematical step unsupported. I do not claim to have verified
every normal form or enumerator in the inaccessible 1976 article.

**1. Verdict per step.** Line numbers refer to the reviewed
[target PROOF.md](../c44r5/PROOF.md), SHA256
`d93fb4b331f6d9a096fda60da9af1e0007e25d62ce21e7161af5a3da5e59e1a8`.
The root proof is byte-identical to the frozen proof. All 19 frozen static
hashes passed; see [artifact receipt](receipts/artifact_hashes.json).

| Exact lines | Step | Verdict | Reason |
|---|---|---|---|
| 10–31 | Definitions, support bound, influence inequality, existence of maxima | PASS | Relevant coordinates have influence at least 2^(1-local degree). Parseval gives D<=I/2<=degree/2 and a finite count bound. Removing dummy variables leaves finitely many functions up to relabeling. |
| 33–54 | Corrected CHS identity W_d=R_d/2^d | PASS | Simultaneous duplication of **all** low-local-degree coordinates cancels the degree-(d+1) terms. Shared coordinates retain degree d, paired duplicated weights sum to their old weights, and the new relevant selector adds positive weight. The corrected proof is in Chiarelli's thesis, Proposition 8.5 and Corollary 8.6. |
| 56–61 | Every coordinate of a count maximizer has local degree d | PASS | A low-local-degree coordinate can be replaced by an AND of two fresh coordinates, staying within degree d and adding one relevant coordinate. Only count is claimed to increase. |
| 63–67 | External R3=10 and base caps | PASS | This applies to arbitrary Boolean functions of real degree at most three. The published class list, checked below, attains R3=10 and W3=5/4. W1<=1/2 and W2<=1 follow from influence. |
| 73–83 | Binary Reed–Muller second-weight corollary | PASS | For code order k with 2<=k<=n-2, the first two nonzero weights are Delta=2^(n-k) and 3 Delta/2. The distinction between this corollary and the stronger original classification, and the 1976 access limitation, is documented in SOURCE_NOTES.md. |
| 85–93 | Integer polynomial reduces to the support indicator | PASS | Integer ternary values give integer bit Möbius coefficients. Affine substitution from signs to bits preserves the real degree bound. Reducing those coefficients modulo two gives the values A mod 2, which are exactly 1 on A=±1 and 0 on A=0. This reduces A itself, not A squared. |
| 95–101 | Padding and application with degree at most k | PASS | Padding repeats the word and cube size by the same factor and preserves density. It ensures n>=k+2. Actual binary degree below k is allowed in RM(k,n); alternatively its minimum support is at least twice the claimed minimum. |
| 103–110 | No-minimum branch | PASS | If every relevant coordinate has influence at least 3/(2M), then summing and using I<=d gives count<=floor(d*2^d/3). The premise is essential. |
| 112–119 | Sharpness for genuine Boolean derivatives | PASS | The two quadratic branches share exactly one Fourier term, with correlation 1/4, so the selector has influence 3/8. Each lift halves it and raises degree by one. Exact checks through degree eight pass. |
| 123–146 | Minimum-support tensor classification and degrees | PASS | Valyuzhenich Theorem 2(2) applies to the real spectral interval [0,d-1]. Odd psi and even phi have degree m-1; the point indicator has degree r. Disjoint factors add degrees. The scalar is ±1. |
| 147–153 | Actual control count h<=2(d-1) | PASS | Remove constant singleton psi factors. Then h=k+b<=2k. General binary affine codimension alone would not imply this; the real-degree information is essential. An independent Fourier proof is in SOURCE_NOTES.md. |
| 157–160 | Active restrictions are dictators | PASS | Both x_i branches must be signs. If A_i=±1 this forces B=0 for every remaining input. Active control probability is exactly 1/M. |
| 162–168 | Controls hit every top monomial | PASS | A degree-d coefficient outside H cannot acquire contributions from strict supersets after fixing H: such supersets would exceed degree d. It must vanish because B vanishes on an active branch. Terms involving i also hit H. Every restriction therefore has degree at most d-1. |
| 170–179 | Weighted restriction inequality | PASS | For a coordinate outside H, survival in both branches cannot lower expected weight. If it survives only one branch, the original local degree is one larger and the factor 1/2 exactly compensates. Iteration is for each outside coordinate, retaining original control costs. |
| 181–188 | Minimum-case budget | PASS | Applied explicitly to the count maximizer, so every control costs 2^-d. Active branches cost 1/2; all others have D<=W_(d-1)<=c. This yields floor(2d-1+(2^d-2)c). |
| 190–199 | Combining cases, transfer to weighted caps, induction | PASS | The cases combine by **maximum**. CHS converts the count ceiling into a bound on W_d, which already includes all smaller degrees. c3 is external; each following c_d uses only established c_(d-1). There is no circularity with the final block recurrence. |
| 201–215 | All numerical cap rows and witness headrooms | PASS | Independently regenerated with exact fractions; see the table below and arithmetic receipt. Lower counts 22,46,94 are treated as witnesses, not exact values. |
| 216–223 | CHS/Shinkar–Tal construction | PASS | The two recursive copies are disjoint and exactly one branch is active. It is Boolean, homogeneous of degree d, and has 3*2^(d-1)-2 variables. |
| 231–239 | Block compression and symmetrization | PASS | Disjoint sensitive blocks become disjoint bit substitutions. Multilinear reduction cannot raise real degree. The endpoint values and integer-layer bounds on q are correct. |
| 241–254 | Fourier granularity, integer energy and dual inequality | PASS | Integer bit coefficients give M*fhat(S) integral before symmetrization. Parseval supplies sum z_S^2=M^2. The lattice supremum h(t) and lower functional have the stated directions and factors. No integrality is imposed on symmetrized coefficients. |
| 256–259 | Retained 37 spectral exclusions | PASS | Each raw dual passes an independently evaluated exact Krawtchouk/binomial functional and a strict rational margin. |
| 261–273 | Épi interpolation exclusions | PASS | All 48 certificates have the required distinct positive nodes, vanishing positive-degree moments and strict separating sign condition. The compressed bit polynomial has p(0)=0, p(1)=1, so the contradiction is valid. |
| 275–283 | Analytic block input and B8 | PASS | The quoted Wellens inequality is precisely Theorem 4.1, equation (4.3). Taking the minimum of valid bounds is legitimate. The actual B8 input is 33, never 32. |
| 287–295 | Top-monomial restriction drops block sensitivity | PASS | For every outside assignment the function on H stays nonconstant. At the point witnessing a restricted function's block sensitivity, changing a nonempty subset of H supplies one more disjoint sensitive block in the original function. |
| 297–308 | Two-parameter recurrence and freezing | PASS | Induction is on block budget. Each nonconstant child has some exact degree j<=d, hence the prefix maximum over all j. A top monomial's controls have local degree d without any extremizer assumption. Freezing at B_d reflects the unchanged actual function class. |
| 310–321 | Infinite tail | PASS | Repeated degree-d restrictions terminate within B_d block drops on every branch. Their total cost is at most d B_d/2^d. The bound B_d<=d^2 and the displayed geometric-series moments give the stated tail exactly. |
| 323–335 | Final rational, strict decimal and gain | PASS | Independent rows and rational columns agree at every finite degree at H=72 and H=96. Both totals are below the headline. The gain is exactly 417/512 with the same tail. |

The matching [target REPORT.md](../c44r5/REPORT.md) claims pass: lines 3–9
(bound and gain), 21–39 (caps and headrooms), 41–48 (B8 and ablations),
52–93 (bridge, types and sequential budgets), and 97–124 (receipts and controls).
The frozen replay passed both original implementations, all 113 structural
cases and all 19 corruption controls. I cannot independently determine the
historical authorship of those two implementations; my arithmetic is separate
from both. Lines 154–158 should be read with the original-paper access
distinction in SOURCE_NOTES.md, rather than as verification of the full 1976 body.

**2. The points most likely to hide a false inference.**

The derivative bridge is stronger than an observation about coefficient
denominators. For bit inputs its coefficient at T is an alternating integer
sum of its values on subfaces. Consequently the real polynomial is literally
in Z[x], of degree at most d-1, and its coefficient reduction evaluates to the
integer value reduction at every bit input. Since -1=1 in F2, this is the
support indicator. There is no denominator reduction, real squaring, or
assumption that an arbitrary real polynomial stays Boolean modulo two.

All weight possibilities are covered. Zero words correspond to irrelevant
coordinates and are excluded. Nonzero words have minimum density 1/M. Above
that minimum the next possible density is at least 3/(2M), whether the weight
is below, equal to, or above twice the minimum. A binary polynomial of actual
degree below d-1 has even larger minimum density. Appending dummy coordinates
does not change any of these comparisons. The coding-theoretic affine normal
forms are used to count weights; arbitrary binary affine substitutions are
**not** assumed to preserve real degree.

The maximizer assumptions are correctly separated. The simultaneous CHS
duplication applies to a D-maximizer and proves W_d=R_d/2^d. The single AND
replacement proves a property of a count maximizer only. Section 4 explicitly
chooses that count maximizer before replacing every control weight by 2^-d.
Section 6 handles arbitrary functions, but its chosen controls are in an
actual degree-d monomial, so they automatically have local degree d. The
restriction inequality itself needs neither kind of maximizer.

The application to smaller degrees is valid precisely because W_d was defined
as the maximum of D over degree **at most** d. A ceiling on R_d alone would
not justify bounding the D of a lower-degree restriction by R_d/2^d. The
corrected identity supplies the missing implication. Within the block
recurrence, each smaller exact-degree column is explicitly included; neither
monotonicity of just the top column nor equality of exact-degree counts is
silently assumed.

Independent cap computation:

| d | input c_(d-1) | minimum-case ceiling | no-minimum ceiling | resulting R_d ceiling | c_d |
|---:|---:|---:|---:|---:|---:|
| 4 | 5/4 | 24 | 21 | 24 | 3/2 |
| 5 | 3/2 | 54 | 53 | 54 | 27/16 |
| 6 | 27/16 | 115 | 128 | 128 | 2 |
| 7 | 2 | 265 | 298 | 298 | 149/64 |
| 8 | 149/64 | 606 | 682 | 682 | 341/128 |
| 9 | 341/128 | 1375 | 1536 | 1536 | 3 |
| 10 | 3 | 3085 | 3413 | 3413 | 3413/1024 |
| 11 | 3413/1024 | 6840 | 7509 | 7509 | 7509/2048 |
| 12 | 7509/2048 | 15033 | 16384 | 16384 | 4 |

The first minimum-case expression is 49/2, so its floor is 24, not 25 or 23.
The degree-five expression is exactly 54; rounding it downward further would
be false reasoning. At degree six it is 925/8, but the other case permits 128.
Choosing the smaller case would be invalid. These are particularly sensitive
places where I attempted off-by-one and case-mixing attacks.

The minimum-support types have counts 7,12,19,30,45 at degrees 4 through 8,
total 113. I independently generated them as integer partitions of block costs
m-1 with remaining cost r. Only phi_2^k attains h=2k. Removing one control
from the worst budget lowers the quartic ceiling to 23 and quintic ceiling to
53, explaining the necessary exceptional types in target REPORT lines 80–82.

**3. Exhaustive and structured sanity attacks.**

[exhaustive.cpp](exhaustive.cpp) independently enumerates every Boolean truth
table through four inputs. It then constructs every degree-at-most-three
function on five inputs by pairing four-input restrictions with matching
degree-three Walsh coefficients, and repeats the same complete construction
from five to six inputs. This is exhaustive labeled enumeration, not random
sampling. Its counts, including constants, are:

    n=5:   807,980
    n=6: 16,750,860

Together with the smaller cubes it checked 17,624,652 tables, including the
degree-four tables on four inputs. It checked 99,894,696 derivatives against
the integer/mod-two bridge and influence gap, 25,774,416 minimum derivatives,
104,807,966 single-coordinate restrictions and 208,777,200 control branches.
See [labeled receipt](receipts/labeled.json).

Full degree-three coverage beyond six variables uses the
[published author data](https://gitlab.science.ru.nl/shahramr/ResilientFunctions)
from [Rasoolzadeh 2023](https://d-nb.info/1307299091/34). Multiplying the sign
function by full parity converts an (n-4)-resilient function to a real
degree-at-most-three function. Permutations, input flips and output
complementation preserve the properties tested, so a representative of each
class suffices. All 761 representatives at n=10 were checked, plus the smaller
lists, for 3,887 representative checks total. They recover maxima

    R1=1, R2=4, R3=10;
    W1=1/2, W2=1, W3=5/4.

This part relies on the published completeness of the class lists. I did not
independently regenerate the full classification or enumerate 2^1024 truth
tables. The separate labeled enumeration through six inputs is independent
of those lists. All class derivatives and restriction branches passed; exact
block-sensitivity computations checked 210,658 top-monomial restriction
branches. See [class receipt](receipts/classes.json).

A bibliographic discrepancy deserves explicit notice: Krotov–Valyuzhenich,
section 3.1(i), prints **961**, whereas Rasoolzadeh's Table 1 and the author's
actual ten-input list give **761**. The target does not use either class count,
and both sources state the ten-variable bound. I used the original author's
actual 761-class data, rather than repeating the 961 figure.

[ternary_rm.cpp](ternary_rm.cpp) checks all **43,046,721** four-input ternary
tables. It separately computes real Walsh degree and binary support ANF
degree. It directly checks integer bit coefficients for the 5,196,626 nonzero
tables of real degree at most three. It also enumerates all words in the small
RM codes, including all **67,108,864** words of RM(3,5). The first/second
weights are 4/6 in RM(2,4), 8/12 in RM(2,5), and 4/6 in RM(3,5), while the
affine and top-order endpoint controls have ratio 2. See
[ternary/RM receipt](receipts/ternary_rm.json).

[structured_attack.py](structured_attack.py) checks 152 structured functions,
including 50 quartics and 65 quintics, using exact sparse Fourier arithmetic.
It includes CHS/Shinkar–Tal witnesses, distinct-query complete decision trees,
ordinary address functions, Wegener's middle-layer address construction,
parities, ANDs, odd majorities, the Kushilevitz cubic block-sensitivity
construction and its lifts, disjoint compositions of CHS functions, mixed
degrees, shared-variable selectors, and the sharp influence-gap family through
degree eight. These cover the published construction families located in this
review, not an assertion that every possible quartic or quintic was enumerated.

The structured checks include Boolean convolution, coefficient integrality,
explicit bit expansions, support values modulo two, the influence dichotomy,
minimum-derivative block types, top-degree hitting, dictator branches, each
weighted restriction inequality, corrected CHS duplication and the count-only
AND argument. They checked 1,689 derivatives, 742 minimum derivatives,
54,160 control branches, and 32 instances each of the corrected duplication
and count-only AND argument. See [structured receipt](receipts/structured.json).

| Degree | CHS count | CHS D | total influence | minimum-influence coordinates | proposed count ceiling |
|---:|---:|---:|---:|---:|---:|
| 2 | 4 | 1 | 2 | 4 | 4, using the valid endpoint argument |
| 3 | 10 | 5/4 | 3 | 8 | 11 from this method alone; exact external value 10 |
| 4 | 22 | 11/8 | 4 | 16 | 24 |
| 5 | 46 | 23/16 | 5 | 32 | 54 |
| 6 | 94 | 47/32 | 6 | 64 | 128 |

Running the proof's logic at degree two gives minimum-case ceiling
3+(4-2)(1/2)=4. The no-minimum affine branch is even stronger: influence is
1 rather than 3/4, giving at most 2 variables. Even formally retaining the
weaker 3/4 threshold still gives 2. Combined, the bound is 4, agreeing with
R2=4. The target correctly does not cite its interior theorem at k=1.

At degree three, the two ceilings are floor(3*8/3)=8 and
floor(5+6*1)=11. Their maximum 11 is consistent with R3=10; it does not
reprove the exact value. The CHS ten-variable cubic has minimum-influence
coordinates, so it belongs to the second case. Treating the first case as
universal would falsely prove R3<=8, and at degree two would falsely prove
R2<=2. Those are successful falsification controls against an invalid variant,
not against the written proof.

Another invalid variant is that one AND substitution preserves D. The exact
example

    f=(1+z)x1*x2/2 + (1-z)y1*y2*y3/2

has degree four and D=1/2. Replacing x1 by a sign-AND of two fresh bits gives
D=7/16. The target explicitly disclaims this false shortcut in lines 59–60;
its simultaneous duplication construction passes instead.

The [live C44 table](https://teorth.github.io/optimizationproblems/constants/44a.html)
has lower bound 3/2. The proposed global bound is above it. The known finite
counts 22,46,94 are below 24,54,128. Wellens's older Table 2 gives **upper**
bounds W4<=2, W5<=5/2 and W6<=3, not larger lower constructions or exact maxima.
Its R8<=1008 also does not contradict the stronger proposed ceiling 682.
No contradictory published value was located.

**4. Independent rational calculation and retained block inputs.**

[independent_arithmetic.py](independent_arithmetic.py) reads raw JSON witnesses
only. It checks all 48 Épi power-moment certificates, all 37 spectral duals by
direct binomial sums and strict fractions, and the exact integer root of the
published quadratic block inequality. The block bounds at degrees 1 through
14 are

    1, 3, 6, 9, 14, 20, 26, 33, 42, 51, 61, 73, 85, 98.

Nothing about the new influence caps changes the compressed Boolean class
underlying these block certificates. In particular, B8=33 remains the input.

I evaluate the recurrence once using integer-scaled rows and once with
rational columns, comparing every terminal degree value. At H=96:

    finite = 62737895123428663382975382631
             / 19807040628566084398385987584
    tail   = 470893 / 39614081257132168796771975168.

At H=72 the total is

    7478939905575354700941 / 2361183241434822606848
      = 3.167454255278645688383889735201606741021862490015337243676...

The independently reproduced round-four H=96 total is

    157739602520732550180509661243 / 39614081257132168796771975168.

Both horizons give the same exact improvement 417/512. Individual cap
ablations, holding all other final caps fixed, give losses 0 at degree 4,
1/16 at degree 5, 93/512 at degree 6, 11/64 at degree 7, 41/512 at degree 8,
and 0 at degrees 9–12. These are not additive contributions to the total gain.
The improved quartic cap is needed in the proof of the quintic cap even though
it is inactive as a separate final recurrence input. All numbers and full
columns are in [arithmetic receipt](receipts/arithmetic.json).

I also reproduced the public table incumbent's exact rational
172624496193406565421448533795/39614081257132168796771975168, and the preceding
Épi rational, using the same raw Épi data and the public package's original
tail convention. That older tail is slightly smaller than the simple tail
used for rounds four/five; confusing the two produces a difference of about
6e-24, not a new error in the present bound.

The full original frozen reproduction was executed in this review's own copy
on the pod. Every step passed, including both verifiers at H=96, the second
verifier at H=72, the gap/witness controls and corruption controls. Its final
receipt matches the original bound, gain, B8 and static manifest. See
[replay receipt](receipts/target_replay_receipt.json) and
[tracked replay ledger](receipts/target_replay_ledger.json).

**5. Prior art and why the improvement could have been missed.**

[PRIOR_ART.md](PRIOR_ART.md) was the first file created here. The fresh audits
read the raw official table, open PRs and issues, named AI-result repository
metadata and indexes, and GitHub repository searches sorted by recent update.
They covered BakeLab/Épi, the two named DeepMind repositories, openai/math,
EinsteinArena, plasma-ai/erdos, kisonecat/openai-math and the public
Boolean-degree and C44 repositories. Recent-paper and indexed public community
searches were also made. This is bounded search coverage, not authenticated
global code search or access to private discussions.

The main table still lists Pinho's unrefereed 4.3576549226; open PR294 has
4.1225323803. A relevant newer public fact is that the
[C44 repository README](https://github.com/rpinho/c44-certificate) now advertises
the round-four **3.9819073803** result in its local-degree-caps directory. I
checked that public proof too. The best published journal bound located
remains [Wellens 2022, Theorem 1.1](https://arxiv.org/html/2005.00566), 4.394.
The proposed round-five 3.1674542553 was not located as a prior public result.

[Wellens 2019](https://arxiv.org/html/1903.08214v2), Table 2, still uses the
elementary caps d/2 at degrees 4–7 and 3.9375 at degree 8. Its method improves
block sensitivity and restriction accounting, rather than the derivative's
second possible influence. The recent
[Valyuzhenich 2026 paper](https://arxiv.org/html/2609.12540) concerns q>=3 and
still cites 4.394 for the binary problem; it supplies no stronger binary cap.
[Potapov 2024](https://arxiv.org/html/2410.21937) studies other degrees and
two/three-valued domains and also does not state these binary caps.

There is a concrete reason for the large numerical change. Round four's
nonminimum threshold is only (M+2)/M^2, approaching the minimum itself as M
grows. The coding gap replaces it by 3/(2M). At degree six this drops the
no-minimum ceiling from 180 to 128. Simultaneously, the new c4 propagates to
c5 and reduces the minimum branch at degree six from 166 to 115. Both cases
are needed; improving just one would not produce the quoted sextic cap.
Those low-degree caps affect the heavily weighted part of Wellens's recurrence.

However, saying that this combination is short does not establish that it was
unknown, and it does not explain historical authors' choices. All substantive
ingredients are old: integer-valued interpolation, binary code weight gaps,
minimum-support structure, and CHS/Wellens restrictions. The needed coding
corollary is sufficiently elementary to admit the separate induction in
SOURCE_NOTES.md. The actual extra argument is to separate minimum influence
from the other case, exploit the dictator branches, then transfer the count
bound to a universal weighted cap and iterate it across degrees. The located
papers do not carry out that combination. This makes a missed refinement
plausible, but I cannot prove novelty or say why no expert published it earlier.
The appropriate response to the unusually easy-looking improvement is the
dependency audit and falsification tests above, not an assumption that a
literature search proves it correct. No priority claim is certified here.

**6. Reproduction, compute discipline and remaining work.**

All substantial computation ran on a rented pod under
`the job directory`, under nohup, nice 10, with single-threaded
BLAS/OpenMP. The independent mathematical workers used one core each; the
job stayed below the ten-core limit. Source reading, code/file preparation,
small hash checks and receipt transfer were the only local operations.
The target's copied replay used its own sequential tracked runner. No other
job was changed and the pod was not terminated.

To reproduce the mathematical checks sequentially in the populated review
directory on the authorized pod:

```sh
ssh a rented pod 'cd the job directory; nohup bash run_review.sh > receipts/reproduction.log 2>&1 < /dev/null & echo $! > receipts/reproduction.pid'
```

The wrapper requires only Python's standard library, g++, the retained input
JSON, published class lists and the copied target snapshot. Its runner records
every child PID and exit status. The individual commands are
`python3 independent_arithmetic.py`, `./exhaustive labeled`,
`./exhaustive classes`, `python3 structured_attack.py`, and `./ternary_rm`,
after compiling the two C++ files with `g++ -O3 -std=c++17`. Run them under the
same nohup/nice/thread wrapper. Public-source audits can be repeated separately
with `source_audit.py`; they are not dependencies of the mathematical checks.

The most valuable next review would be expert scrutiny of the derivative
gap/control argument and the count-to-potential transfer. Obtaining the full
1976 original would close the source-access limitation, but is unnecessary
to derive the corollary independently. Further mathematical work could try
to exclude the exceptional phi_2^3 completion at count 24; nothing here proves
R4<=23, exact R4/R5/R6, B8<=32, or optimality of the final constant.

Final verdict remains **PASS**, with subjective correctness probability **99%**.

The final public refresh completed at 21:22 UTC with 71 successful requests
and no transport errors. The process audit found no remaining review worker;
local `ps -axo pid,ppid,pcpu,command` likewise showed no local mathematical
worker. The retained review is about 10 MB, below the 50 MB limit. The final
machine-readable check is [final review receipt](receipts/final_review_receipt.json).
No commits, pushes, PRs, posts, messages to others or pod termination occurred.
