# Independent adversarial referee: C38

Job `math_c38ref_1104`, opened 2026-11-04 11:27 UTC. This is a referee
report on the exact fraction **8388608/3192535**, not an independent claim
of novelty. The fraction is 2.6275696272711184…; 2.62756963 is its rounded
display, not an exact equality.

**HOLDS WITH CAVEATS.** No mathematical defect or numerical mismatch was
found. Independent point/enclosure checks reach spans 1–15, exact
irreducible coefficients reach span 12 through length 40, and both full
rectangle sums pass. The final exact inequality has positive slack about
1.1437205719677353×10^−7. Five native evaluations at spans 16–18 remain
unverified by independent recount; they are explicitly listed below.
This is not an unconditional independent reconstruction of the entire
certificate. Enumeration finished and evidence was pulled by 13:48 UTC.

No producer enumerator or verifier was executed, imported, or linked.
Producer proof documents, source, JSON numbers and receipts were read as
claims to attack. All executable mathematical evidence in this directory
comes from the referee's own source. The baseline's large enumeration is
not silently promoted to an independently verified premise.

## (a) Definition and bridge renewal

**No definitional counterexample found.** The table asks for the ordinary
square-lattice vertex-self-avoiding-walk connective constant, rooted at a
fixed vertex: `../c44_release/tao/constants/38a.md:5–23`. The live
[table](https://teorth.github.io/optimizationproblems/constants/38a.html)
and fetched raw source `sources/table38a.md` agree on this definition.

The candidate's convention is

\[
x_0=0<x_i\le x_n=h\quad(1\le i\le n),\qquad h\ge1.
\]

This is a strict-at-start, weak-at-end bridge. Replacing either strictness
convention without changing the enumeration would be dangerous; the
candidate actually uses the convention above in both the statement and
its vertex rules (`../c38/frozen/c38_finite_strip/PROOF_FINITE_STRIP.md:16–22`,
`../c38/frozen/c38_finite_strip/verify_strip.cpp:48–61`).

Here is the cut argument independently. For every integer 1≤j<h, a path
starts left and ends right of x=j+1/2, so its crossing count is odd. If the
count is one, that crossing points right; before it, the entire prefix has
x≤j, and after it all vertices have x>j. Splitting at the vertex immediately
before that edge gives two positive-span strict bridges. Conversely, any
concatenation at a vertex of first coordinate j has exactly one crossing
of this cut. Thus **the irreducibility condition is exactly “every interior
cut has at least three crossings.”** It is not a test that every occupied
column contains three vertices, or that the endpoint is visited only once
as an x-coordinate. At span 1 the condition is vacuous; vertical segments
after the first horizontal step are correctly included.

Translation fixes the start, with no reflection quotient. The independent
span-1 control gives one length-1 bridge and two bridges of every length
n≥2. The exact finite sum with width w is

\[
B_1^{[w]}(b)=b+2\sum_{n=2}^{w}b^n.
\]

The referee's exact evaluation at w=41 equals this formula. This is a useful
orientation and width-off-by-one control (`results/b1_control.json:1`,
`independent_tm.cpp:106–155`).

The finite-family renewal implication does not require assuming the entire
critical Kesten identity. For P the generating polynomial of any finite
set of these irreducibles, unique factorization gives a distinct SAW for
every ordered factor sequence. Hence the sequence series ∑P(z)^k is
coefficientwise bounded by ∑c_n z^n. Factors have positive length, so each
coefficient counts finitely many sequences. If P(a)≥1 it diverges at a; if μ<1/a,
the SAW series converges there by the root test. Contradiction. Existence
of μ follows from c_(n+m)≤c_n c_m and Fekete's argument. This establishes
μ≥1/a with the required direction. The producer's corresponding argument
is in `../c38/frozen/c38_finite_strip/PROOF_FINITE_STRIP.md:48–94`.
[Jensen's treatment](https://arxiv.org/abs/cond-mat/0409381) supplies the
historical Kesten/irreducible-bridge context; it is not a substitute for
the explicit finite-family argument here.

## (b) Unique factorization and disjointness

**No collision found; there is a direct injectivity proof.** In a
concatenation of positive-span bridges, every noninitial vertex of a later
factor lies strictly to the right of the preceding factor's endpoint
column. Factors can share only their join. Within each irreducible factor
all its interior cuts have ≥3 crossings; the cuts at the joins have one.
Splitting a resulting walk at all singly crossed interior cuts therefore
recovers exactly its factor sequence, including each vertical displacement.
There is no possible ambiguity from transverse translations or reflected
copies.

The main family has spans 1–18, with ranges at most w_h−1. The supplement
has spans 19–30, range at most 22, and interior crossing counts in {3,5}.
Their spans separate them, irrespective of lengths or transverse ranges.
Within each family, different spans are also disjoint. See
`../c38/frozen/c38_finite_strip/packet.json:43–259` and
`../c38/frozen/c38_disjoint_extension/input/PROOF_DISJOINT_EXTENSION.md:9–19,42–44`.

The two normalization methods agree. Sweeping transverse columns and
removing the still-empty history after the first column selects minimum
transverse coordinate zero. In a fixed frame of rows 0,…,W, a walk of
range R has W−R+1 placements; in a frame of W rows it has W−R placements
when R<W and zero when R=W. Their difference is one. Neither operation
identifies reflections or reverses the oriented walk.

As an independent attack, literal vertex-list DFS checked the split at
every singly crossed cut for **1,843,794 bridges of length at most 16**,
including the strict inequalities in each recovered factor. No violation
occurred (`literal_walks.cpp:12–28`, `results/LITERAL.json:1`). This finite
test supports, but does not replace, the general injectivity proof.

## (c) Independent recount

**Completed point/enclosure scope: spans 1–15; no mismatch.** Exact
coefficient enumeration reaches span 12.

`independent_tm.cpp:25–102` constructs its own state graph from vertex
degrees and connected path components. It uses canonical component IDs
and *distinct* terminal labels, rather than the producer's bracket case
table or anonymous terminal encoding. A closed cycle is rejected; a
completed two-terminal path is counted only when no other component
remains. Reachability uses a growing graph work list. No producer transition
or graph was supplied as input.

Two numerical modes test different things:

1. **Exact finite generating values**, with arbitrary-size integers and
   denominator 2^(54t) after t processed vertices. An edge increment k
   multiplies the numerator by M^k 2^(54−27k). There is no rounding in this
   finite evaluation (`independent_tm.cpp:106–124`). All twelve specified widths
   were evaluated at both b=51081913/2^27 and c=51082227/2^27. Each exact
   value lies inside the producer's claimed finite interval.
2. **Exact coefficients through length 40**, using integer polynomials and
   41 transverse columns. Every length-40 walk has range at most 40, so this
   contains all such bridges. The exact formal-series recurrence
   A_h=B_h−∑_(j<h) A_j B_(h−j) then gives the irreducible counts. All 492
   bridge entries, including n=0, agree with Numaro's table; all 492
   corresponding irreducible coefficients agree with formal renewal of
   that table. These are related comparisons, not 984 independent tests.
   All 288 available producer prefix
   entries for these spans through length 24 agree as well
   (`independent_tm.cpp:159–175`, `compare_recount.py:14–38`).

The exact point evaluations in item 1 are **bridge** values B_h^[w], not
materialized full finite irreducible polynomials. The irreducible evidence
is the exact length-40 coefficient enumeration and the independently
certified finite irreducible lower bounds obtained from B and full smaller-
span upper bounds. The producer's α_h are lower enclosures, not exact
coefficient counts; comparing them in the required inequality direction is
therefore the appropriate test.

A separate literal DFS explores **158,517,706 strict half-plane walk
prefixes** through length 20. It records bridges and irreducibles by
looking at the actual vertex list and actual cut crossing counts. Every
overlapping coefficient agrees with the transfer-matrix result
(`literal_walks.cpp:27–46`). This checks the renewal conversion against
direct irreducibility, not merely against another use of the recurrence.

Representative independently recovered irreducible coefficients a_(40,h):

| h | a_(40,h) |
|---:|---:|
| 1 | 2 |
| 2 | 252983780 |
| 3 | 146576318038 |
| 4 | 3004932909600 |
| 5 | 12413953749600 |
| 6 | 19483674754334 |
| 7 | 14389607435312 |
| 8 | 4763146414350 |
| 9 | 595059402764 |
| 10 | 22970863600 |
| 11 | 223499180 |
| 12 | 414840 |

The referee also constructs all-width upper potentials with exact integer
ceilings at scale 2^−32 and checks every potential inequality explicitly
(`independent_tm.cpp:127–148`). For every completed span/point, its resulting
full bridge upper bound is **no larger** than the producer's. At b,
independently derived finite irreducible lower bounds are no smaller than
the claimed α_h, and full irreducible upper bounds are no larger than the
claimed β_h. Thus the comparison checks the dangerous direction, not only
overlap of decimal estimates. Machine-readable evidence:
`results/RECOUNT_COMPARISON.json:1`; exact values and logs: `results/pod/`.

For spans 13–15, `independent_interval.cpp:14–56` uses the same independently
constructed graph with rigorous 160-bit directed arithmetic and independently
checked 32-bit-scale upper potentials. All six point enclosures lie inside
the producer's finite intervals, and their full upper bounds are tighter.
See `results/EXTENSION_COMPARISON.json:1` and `METHOD.md`.
The rectangle implementation directly tracks bottom-row contact to count
each normalized walk once, rather than using subtraction of frame counts
(`independent_rectangle.cpp:39–82,111–148`). Its range-4, spans-3–5, cap-3
control agrees with a complete literal constrained DFS over 458,261
prefixes and is enclosed by the producer's control interval
(`results/CONTROL_AUDIT.json:1`, `control_audit.py:20–36`).

**Both complete rectangle recounts pass.** Their independently calculated
160-bit intervals are contained in the producer's 96-bit intervals:

| Family at b | Independent value, diagnostic only |
|---|---:|
| Range ≤22, spans 18–30, crossing cap 5 | 0.00009404901758443901 |
| Range ≤23, span 18, crossing cap 5 | 0.00004310725284341047 |
| Direct range-22 supplement, spans 19–30 | 0.000059429329831521866 |

The direct supplement lower endpoint is exactly

\[
\frac{2714251964195233862926154571118770180568885}
{45671926166590716193865151022383844364247891968}.
\]

Exact comparison confirms it exceeds the claimed e. Thus the supplement
survives both an independent reconstruction of the two subtraction inputs
and a direct normalized count of the genuine disjoint family. See
`compare_extensions.py:58–72`, `results/pod/rectangle22.json:1`, and
`results/pod/rectangle23.json:1`.

## (d) Analytic steps and upper-bound audit

**The four stated inequalities have the correct signs.**

**Secant extrapolation.** For t=(b−a)/(c−b)>0, b=(a+tc)/(1+t).
Convexity of z↦z^n on z≥0, including n=0,1, gives
(1+t)b^n≤a^n+tc^n. Multiplication by nonnegative coefficients and summation
therefore give F(a)≥(1+t)F(b)−tF(c). Substituting a lower bound L17 for
F(b) and an upper bound U for F(c) lowers the right side. Here c−b=314/2^27,
so t=k/314 exactly. U is an upper sum for *all-range* irreducibles of
spans ≤17 at c; it therefore bounds the finite subfamily F at c. No upper
bound at b is silently substituted for the required bound at c
(`exact_audit.py:47–54`,
`../c38/frozen/c38_power_secant/input/PROOF_POWER_SECANT.md:13–17,29–34`).

**The span-18 subtraction.** Every reducible finite-range span-18 bridge
injects into the disjoint union of a first irreducible span-j factor and
a full span-(18−j) bridge, for 1≤j≤17. Consequently

\[
R_{18}^{[72]}(b)\le\sum_{j=1}^{17}\beta_j U_{18-j},\qquad
I_{18}^{[72]}(b)\ge\max(0,b_{18}^{-}-\sum_{j=1}^{17}\beta_j U_{18-j}).
\]

All factors in the product bounds are nonnegative. Although the upper
product includes reducible walks outside the transverse cap, that makes
the subtraction conservative. It is not an assertion that finite-range
renewal is an exact product. The span-18 `num_tail=0` is marked
`infinite_tail_certified=false`; it is not used as an all-range span-18
upper bound (`../c38/frozen/c38_finite_strip/replay/span_18.json:1`,
`../c38/frozen/c38_finite_strip/PROOF_LAST_FINITE.md:20–44`).

**Degree power.** For r=(M−k)/M∈(0,1) and n≤N, r^n≥r^N. Thus
H(a)≥r^N H(b) for a polynomial with nonnegative coefficients and degree
≤N. There are at most h w_h noninitial vertices in a main-family bridge,
so G has degree ≤18·72=1296. The supplement has at most 30·23 noninitial
vertices, so its degree is ≤690. Multipliers r^1296 and r^690 are positive;
using lower bounds L18,e is safe. The source proof is
`../c38/frozen/c38_power_secant/input/PROOF_POWER_SECANT.md:23–29`.

**Supplement subtraction.** Let H22 be the span-18 part of F22. The true
supplement is E=F22−H22 with nonnegative integer coefficients. Increasing
range from 22 to 23 gives H22⊆H23. Therefore

\[
E(b)\ge F22(b)-H23(b)\ge (lo22-hi23)/2^{96}.
\]

The two input integers are 7451330849486838403732161 and
3415308433821208589119087. Their difference is positive. The certificate
does **not** use the potentially signed coefficient polynomial F22−H23
in the degree-power argument; it uses the genuine E. See
`../c38/frozen/c38_disjoint_extension/input/PROOF_DISJOINT_EXTENSION.md:21–37`.

**Why the input bounds are in the required direction.** For main spans
≤17, the source applies floor/ceiling separately to every nonnegative
transfer contribution. Its integer upper potential satisfies
u_r≥c_r+T_r^T u_(r+1). Pairing with any nonnegative frontier vector bounds
every finite future completion sum, hence the entire tail by monotone
convergence. A stabilized backward cycle supplies these inequalities;
the forced zero empty coordinate is used only after removing the empty
history. The source checks that nonempty states cannot enter that
coordinate. Renewal then uses upper×upper for lower bounds and
lower×lower for upper bounds. I found no reversed inequality in these
steps (`../c38/frozen/c38_finite_strip/verify_strip.cpp:153–195,196–243`,
`../c38/frozen/c38_finite_strip/PROOF_FINITE_STRIP.md:191–264`).

I inspected the fixed-width arithmetic: the three-limb weighted product,
discarded-bit ceiling test, accumulation guards, and packed graph indices.
The 128-bit potential sum has headroom under the asserted <2^60 entry
bound and at most three outgoing moves; a fixed-point or capacity failure
rejects. For the rectangles, the quotient/remainder multiplication and
frame normalization use A_lower−B_upper for the lower bound and
A_upper−B_lower for the upper bound. The partial crossing-cap filter counts
only already fixed right edges, so later updates cannot invalidate that
pruning argument (`../c38/frozen/rectangle_point/w22_h18_30_c5/input/verify_rectangle_point.cpp:63–112`).

Source inspection and replay receipts are not independent numerical
reconstruction. This distinction remains material for main spans beyond
the referee's completed recount; no saved upper-potential vectors for
those large spans have been independently checked here.

## (e) Final exact inequality at k=1353

**Exact arithmetic passes.** `exact_audit.py:14–77` reads the primitive
per-span JSON numerators, redoes both renewal brackets, derives L17,L18,U
and e, and computes the final rational using Python integers/Fractions.
It imports no producer program and does not take the seed's L17,L18,U,e
as numerical premises. Equality to all four seed values and to the entire
stored final rational is checked only after the independent reconstruction.

The diagnostic values are

| Component | Approximation |
|---|---:|
| L17 | 0.9997897701349937 |
| L18 | 0.0003558631102728467 |
| U at c | 0.9998323630850930 |
| e | 0.00005094176474102854 |

With M=51081913, k=1353, t=1353/314 and r=51080560/51081913,

\[
S=(1+t)L17-tU+r^{1296}L18+r^{690}e.
\]

The four terms are approximately 5.3078011045064795,
−4.3081948638666585, 0.00034385453232309206 and
0.00005001919991322891. Cancellation makes a decimal-only check inadequate.
The exact reduced rational in `results/EXACT_AUDIT.json` equals the one
claimed in `../c38/frozen/c38_power_secant/VERIFIED.json:8`. Independently,
exact cross-multiplication gives

\[
\frac{11437205719677}{10^{20}} < S-1 <
\frac{11437205719678}{10^{20}}.
\]

Thus S>1 with exact positive slack. At k=1354 the same expression is less
than 1 (diagnostic excess −3.067399832562139×10^−8). That is a failure of
this sufficient inequality, **not** an upper bound on μ. The exact reciprocal
is 2^27/51080560=8388608/3192535>1051/400.

## Reproduction, provenance and remaining scope

Read `PRIOR_ART.md` for the live table, public-code and paper checks.
`baseline_audit.py` independently reproduces Numaro's span-17/length-260
renewal arithmetic from its table; its exact slack at the stated public
fraction is about 2.046044770793534×10^−38. This checks the baseline
certificate arithmetic, not Numaro's original large enumeration, whose
generator is absent from the available archive.

Enumeration workers use nice priority ≥10. The initial pod batch has six
single-core workers; subsequent runs are capped at eight workers total.
The Mini literal/assembly checks use one process. No commits, pushes,
PRs, posts or messages were made. Only public-source reads and transfer
to/from the user-authorized compute pod were used.
All completed native runs used as evidence returned zero. The largest two
rectangle runs took 7,775 and 7,381 seconds; the span-15 runs took 4,955
and 4,928 seconds. Completion receipts are in `results/pod/HEAVY_BATCH.json`
and `results/pod/LARGE_BATCH.json`. Both machine process checks report no
remaining native workers (`results/COMPUTE_FINAL.json:1`,
`results/pod/COMPUTE_FINAL.json:1`). Transport interruptions and deliberately
stopped optional pilots are separately documented in `ATTEMPTS.md`.

Standalone enumeration commands (C++17, Boost headers, Python 3.11+).
These schedulers default to at most six workers on the pod. Set
`REFEREE_WORKERS=4` on the Mini and run the schedulers sequentially. Every
command below runs only referee source. If Boost is extracted under `deps`,
add `-I deps/usr/include` to the C++ compile commands.

```sh
mkdir -p results/pod
nice -n 10 g++ -O3 -std=c++17 independent_tm.cpp -o independent_tm
nice -n 10 g++ -O3 -std=c++17 independent_rectangle.cpp -o independent_rectangle
nice -n 10 g++ -O3 -std=c++17 independent_interval.cpp -o independent_interval
nice -n 10 g++ -O3 -std=c++17 independent_interval.cpp -o independent_interval_large
nice -n 10 c++ -O3 -std=c++17 literal_walks.cpp -o literal_walks
nice -n 10 ./literal_walks 20 results/LITERAL.json
nice -n 10 ./literal_walks 25 results/LITERAL_RECTANGLE.json 4 5 3 3
nice -n 10 python3 run_batch.py
nice -n 10 python3 run_heavy.py
nice -n 10 python3 run_span13.py
nice -n 10 python3 run_large.py
```

The actual bounded job overlapped schedulers after worker slots became
available, never exceeding eight native workers. Copy the generated native
JSON files from `results/` to `results/pod/` (or pull the pod's `results/`
directory there), then run the data-only audits:

```sh
nice -n 10 python3 exact_audit.py
nice -n 10 python3 compare_recount.py 12
nice -n 10 python3 compare_extensions.py
nice -n 10 python3 baseline_audit.py
nice -n 10 python3 artifact_audit.py
```

The scripts use only the Python standard library. On the Mini, use the
required shared virtual environment’s Python for these commands. Running the audit
commands on the retained results does not rerun any enumeration. The literal
small-rectangle and final-source controls are reproducibly compared by
`control_audit.py`; their output is `results/CONTROL_AUDIT.json`.

**Remaining caveat — UNVERIFIED BY INDEPENDENT RECOUNT.** These five
primitive evaluations were inspected as source/data/receipt claims, but
were not independently regenerated within this bounded referee job:

| Point and span | Width | Primitive record |
|---|---:|---|
| b, 16 | 376 | `../c38/frozen/c38_finite_strip/replay/span_16.json:1` |
| b, 17 | 401 | `../c38/frozen/c38_finite_strip/replay/span_17.json:1` |
| b, 18 | 72 | `../c38/frozen/c38_finite_strip/replay/span_18.json:1` |
| c, 16 | 376 | `../c38/frozen/span17_all_length_stop/replay_public/span_16.json:1` |
| c, 17 | 401 | `../c38/frozen/span17_all_length_stop/replay_public/span_17.json:1` |

For spans 16–17 this includes their all-width upper tails. At span 18 only
the finite value is used. The producer reports 1,613,562,216 graph states
for span 18; source inspection and matching hashes do not independently
verify that numerical run. The data-only audit checks 187 source/data hash
references (`results/ARTIFACT_AUDIT.json:1`), not 187 independent enumerations.

The verdict means that the definitions, injectivity, inequalities, exact
assembly and all completed independent recounts survived these attacks.
The numerical validity of the five remaining inputs is still a premise of
the full claimed bound. Closing that gap requires independently regenerating
those inputs, or checking separately supplied full potential/transition
certificates. No failed comparison has been excused as a resource limitation.

VERDICT: HOLDS WITH CAVEATS
