# Independent adversarial review — math_review_c91r3_1101

**Headline verdict: PASS for C91 >= 0.259407. Subjective probability that the
bound is correct: 99.5%.** I found no mathematical gap or false rejection of
a canonical optimum. My checker, written from the proof before opening the
round-3 verifier, reconstructed the entire frozen automaton and passed every
strict integer row inequality. One minor verifier interface GAP affects B=0;
the headline artifact uses B=1. An auxiliary 1283-bit size estimate is FALSE
by one bit; the checker's 1536-bit capacity remains sufficient. Diagnostic
search comparisons are outside the certified numerical verdict.

Reviewed certificate SHA-256:
`93a526ddfd3f8842822e696c1a08e89a71a0fe7019729936c0bb7bd78fde382f`.
The gain over the previously reviewed 0.256801 is exactly
0.002606 = 1303/500000. The artifact is 21,004,483 bytes. This review does not
establish priority, optimality, or convergence of the frontier family.

**Scope and independence.** P means the saved [round-3 proof](sources/target_PROOF.md),
R the saved [round-3 report](sources/target_REPORT.md). Supplied C++ and Python
refer to [verify_frontier.cpp](sources/target_verify_frontier.cpp) and
[verify_frontier.py](sources/target_verify_frontier.py). All line numbers below
refer to those exact copies, which are checked against the target at completion.
The comparison is with [round-2 PROOF.md](sources/round2_PROOF.md) and its
existing independent PASS in ../review_c91r2/REPORT.md. I accepted that review
as the baseline; I did not rerun round 2's entire matrix certificate.

The pre-reading source and hashes are preserved in [INDEPENDENCE.md](INDEPENDENCE.md)
and [the hash receipt](receipts/pre_target_code_read.sha256). The graph and row
checker in [independent.cpp](independent.cpp) stayed unchanged after target
code was first opened at 22:13:32 UTC. [prepare.py](prepare.py) independently
decodes the potential, computes coefficients with Python integers, and proves
the exponent positive with rational logarithm-series bounds. It imports no
target code, graph, partition, or search output. The first adapter run hit
Python's integer-to-string digit limit while saving the large rational receipt;
enabling those conversions fixed serialization before target code was read.
The failed first receipt is retained.

**Every substantive change since round 2.** PASS means the displayed argument
and its use in this certificate passed review; GAP identifies a stated limit
or defect. The frontier and lower-bound argument pass; one auxiliary arithmetic
size estimate is FALSE, as detailed below.

| New or changed step | Exact locations | Verdict and reason |
|---|---|---|
| Minimize the inherited labeled automaton before forming the frontier product, preserving run memory | P 46–52; R 30–34; supplied C++ 78–90 | **PASS.** Ordered destination colors preserve labels and missing edges. Refinement from one color is monotone; stable cardinality means a stable equivalence relation. Equal colors have equal run memory and equal labeled continuation languages. My reconstruction also checks every class member's row against its representative. Counts are 1,299,053 → 370,749. |
| Replace pure-diagonal competitors by earlier full-prefix alternatives carrying a conservative gap bound | P 56–69; R 20–28 | **PASS.** Every retained minimum is one actual witness with cost difference c, gap difference <= -r, and an earlier first differing operation already inside both words. Forgetting additional gap savings does not invent eligibility. |
| Pending alternatives for suffixes of actual gap runs | P 71–78 | **PASS.** Before q actual gaps, the old actual prefix has cost and gap differences -q. Its first new diagonal determines an earlier operation than the actual gap. Capped run length identifies all pending origins retained by this definition. |
| Reject by closing a frontier witness with r residual gaps, including ties | P 80–85 | **PASS.** Closure changes the differences to c+r and at most zero gaps. Strict cost improvement wins; at equal cost fewer gaps win; at equal cost and gaps the already determined earlier operation wins. The argument applies to the canonical prefix and hence to the global optimum. |
| Diagonal transition: active sources and every diagonal placement | P 94–103, 110–111 | **PASS.** From vertical lag q to lag r, consume q-r+1 X symbols and one Y symbol. Any placement has one diagonal and q-r D gaps, giving the stated cost and gap differences. The horizontal case is symmetric. |
| Diagonal transition: pending sources | P 103–111 | **PASS.** Emit the diagonal first at X_ext[q], then q-r gaps. New cost difference is -r plus mismatch difference; new gap difference is exactly -r. Endpoint minima can be merged because both have genuine witnesses. |
| Actual-gap transitions and opposite-frontier propagation | P 113–126 | **PASS.** Same-side lag increases by one with no alternative operation and cost difference decreases by one. Across the other frontier, D plus q-r I gaps gives c+q-r; a diagonal plus q-r-1 I gaps gives c+q-r-2+mismatch. Gap differences are bounded by -r and -r-2. Opposite pending runs cannot accompany a permitted actual gap. |
| Rejection, score cap, minima merging, and finite memory | P 128–140 | **PASS.** Rejection is checked before score dropout. Surviving scores satisfy -r<c<=B. All minima remain individually witnessed; future increments depend on the vertex and retained histories. Width/score dropout only forgets witnesses. Positive-score endpoint witnesses may also be forgotten safely. |
| Input histories for the new frontier and unchanged four features | P 89–92, 153–156 | **PASS.** Short-prefix lengths prevent fictitious initial symbols. Last max(W,4) symbols suffice; all tested actual graph paths have exact direct-string feature totals, including initial and terminal gaps. |
| Explicit shrinking typicality tolerance and orthogonality estimate | P 144–151 | **PASS.** Distinct summands within each feature are distinct Walsh monomials, so variance <=n per input. Independence of X,Y gives variance <=2n for H_j. Chebyshev at n^(3/4), then a four-term union bound, gives 8/sqrt(n). Cross-feature independence is unnecessary. This makes the sublinear tilt penalty explicit. |
| Apply the inherited first moment to the new product language | P 163–180 | **PASS.** All states accept. Strict Av<v on the finite full graph yields a finite total path sum. Canonical-path survival provides the required injection from low-distance pairs. The positive linear exponent dominates the n^(3/4) tilt term. Subadditivity then supplies the limit. No equal-endpoint or terminal factor is omitted. |
| New schema and compressed potential indexed by reconstructed weighted colors | P 184–197; R 32–41 | **PASS.** Weighted color multisets retain multiplicity and missing-edge sentinels. First-appearance numbering fixes vector coordinates. Most importantly, I checked every full row after expanding the colors; correctness of a search quotient is not assumed. Counts are 29,006,665 states, 107,581,342 edges, 4,404,657 classes. |
| Binary32 potential interpreted as exact dyadic integers | P 199–205; supplied Python 24–36 | **PASS.** Decode sign, exponent, and implicit mantissa bit as integers; reject zero, negative, nonfinite, and subnormal entries; remove one common power of two. Actual exponents range from -53 to -23 and scaled potentials use at most 54 bits. Their floating origin is irrelevant after exact row checks. |
| C++ fixed-capacity exact arithmetic replaces round 2's Python integer rows | P 207–221, 223–225; supplied C++ 18–29, 161–167 | **PASS.** The weight formulas are inherited, not a new reduction. I independently form coefficients with Python integers and replay rows with different base-2^64 arithmetic, cross-checked against Python on 10,000 cases. The target's 1536-bit capacity exceeds even the corrected 1284-bit general row bound. Its overflow checks reject rather than wrap. |
| Universal claim that allowed 64-bit parameters/potentials require at most 1283 bits per row | P 222 | **FALSE.** An explicit initial-row input needs 1284 bits. This one-bit underestimate does not exhaust the 1536-bit capacity or affect the frozen replay. See the exact counterexample below. |
| New rational parameters and threshold | R 3–6, 36–41, 62–73 | **PASS.** Exact full-row replay and an independent rational logarithm enclosure certify the stated rounded-down a=259407/1000000. The strict exponent is approximately 1.4035407462031042196e-7 >0. |
| Explicit example beyond any fixed length-12 window and matched pure-diagonal tracker | R 98–104 | **PASS.** Independently reproduced the equal-cost/equal-gap earlier replacement, all windows of lengths <=12, pure W3/cap2 acceptance, new W3/B2 and W4/B1 rejection, and the inserted-match fixed state, through 10,013 columns. The fixed state justifies arbitrary extension of this family. |
| Other frontier variants, optimizer ablations, richer tilts, block-renewal experiments | R 108–153 | **GAP in independent numerical reproduction.** I inspected the supplied logs and the explicit qualification as floating diagnostics, but did not rerun these optimizations or block histograms. They are not used as certified bounds or as a convergence theorem; no defect in the headline follows. |

The canonical order, five run rules, forbidden-word mechanism, four statistics,
rational weights, all-states acceptance, and first-moment/Fekete reduction
are inherited. The ordered frozen forbidden bank is compared directly with
round 2, rather than trusting the inherited-bank description. Weighted search
minimization itself existed in round 2; storing only a palette in the frozen
artifact and independently reconstructing its coordinates are the new parts.

**Independent certificate result.** [Full receipt](receipts/independent_candidate.log):
every one of the 1,282,850 forbidden words has a strictly better canonical key;
all original, minimized, product, and palette counts agree; every complete
reachable row has strict positive integer slack. The minimum slack in my
unreduced common-denominator representation is the positive integer with hex
representation

```text
17dc0958b319cfe48d1dcd59ac329bade184c95f29ec2d00b6e47b5ed345a9e8686ba812c65f73a3c95e3960b5669b2cf6620734d1c2ad2789785ed2a08d4a810dcfd1fe0000000000000
```

The [independent exponent receipt](receipts/independent_exponent.json) contains
exact lower/upper rationals using 160 terms of
log(u)=2 sum_k w^(2k+1)/(2k+1), w=(u-1)/(u+1), and the explicit absolute tail
bound 2|w|^(2N+1)/((2N+1)(1-w^2)). Both exponent endpoints are positive.
The small frozen integer-list certificate independently passes 27,401 states
and 4,551 classes as well. The supplied full-checker replay is recorded
separately in [target_replay.log](receipts/target_replay.log): it also PASSed,
in 469.39 seconds. [The cross-check](receipts/certificate_crosscheck.json)
confirms that both independent implementations compute exactly the same
minimum integer slack. [Direct bank comparison](receipts/bank_compare.json)
confirms equality of all ordered round-2 and round-3 forbidden words.

**Exhaustive soundness and adversarial tests.** There were zero rejected
canonical optima in either independent survival test.

- [Actual frozen graph audit](receipts/graph_audit.log): all **4,190,209**
  ordered rectangular pairs with each length in **0..10**, and **2,000** mixed
  random/constant/alternating/biased/related pairs with lengths through **1,024**.
  It traverses the actual independently reconstructed graph with the frozen
  bank, minimized matcher, run memory, histories and frontier. Every feature
  sum also agrees with its direct complete-string definition.
- [Literal-witness audit](receipts/audit.log): all **261,121** pairs with
  lengths 0..8, **299,593** labeled words through six columns, and **1,000**
  mixed pairs through length 256. It reconstructs physical alternative paths
  and checks inputs, costs, gap bounds, first differences and rejecting
  completions, totaling **3,393,520** witness checks. Every one of **278,960**
  rejected short labeled words has a strictly better independently computed
  canonical key. Literal enumeration of *all* alignments validates its suffix
  DP/greedy canonical oracle on all **961** pairs with lengths 0..4.
- [Arithmetic audit](receipts/arithmetic.log): 10,000 independent comparisons
  with Python integers, including multiplication by 64-bit integers, carries,
  addition, subtraction and comparisons through 1024-bit results.
- [Mutation/control suite](receipts/mutations.json): **29** expected outcomes,
  including **24 rejections** and **5 valid acceptances**. Corrupt canonical
  forbidden words, counts, vectors, exponent, tilt, malformed dyadics and mixed
  encodings fail. Integer and dyadic originals, homogeneous rescaling, and
  removal of a redundant forbidden word pass. That last case corrected an
  initially wrong harness expectation; [the first receipt](receipts/mutations_first.log)
  is retained. Acceptance after omitting a redundant restriction is sound.
- [Long-family audit](receipts/long_audit.log): direct strings/keys and all
  short windows pass for insertions 0..13, 100, 1,000 and 10,000. Both new
  parameter choices reject exactly at the closing column; the pure tracker
  accepts. The match-loop state stabilizes as claimed.

**One concrete interface GAP, outside the B=1 bound.** The supplied
[Python wrapper](sources/target_verify_frontier.py:12) permits `0<=B<=10`,
but its [serialization loop](sources/target_verify_frontier.py:49) requires
`0<d[k]` for every parameter, including B. Therefore it rejects every B=0
artifact before invoking the C++ checker. [Reproduction receipt](receipts/zero_cap.log).
The test changes B in the small fixture solely to reach this assertion; it
does not claim that the unchanged state counts/vector form a valid B=0
certificate. Repair the serialization condition to allow zero for B while
keeping the other required parameters positive. This is a verifier
completeness defect, not a false acceptance or a failure of the main artifact.

**Auxiliary FALSE claim at P 222.** Let M=2^64-1, choose p=M, q=M-1,
r=M-2, s=M-1, all four tilt pairs (u_j,v_j)=(M,M-1), and every source/destination
potential equal to M. These satisfy the 64-bit parameter restrictions,
x>1 and 0<t<1. The actual initial row has two matches, two substitutions,
four gaps, and h=(0,0,0,0) on each edge. Its exact integer sum is

```text
M^9 (M-1)^8 (2 p^2 s + 2 p^2 r + 8 p q r).
```

This has **1284 bits**, while D*M has 1282 bits. The row should be rejected
by Av<v, but the verifier must evaluate that sum to reject it. Therefore the
universal pre-rejection size bound is 1284, not 1283.
[The exact counterexample](receipts/capacity_counterexample.json) and
[its source](capacity_counterexample.py) reproduce this with Python integers.
More generally four diagonal contributions are each <2^1280 and four gap
contributions are each <2^1281, so their sum is <2^1284. The implemented
1536-bit capacity is comfortably sufficient. Correct the exposition's bit
count; no algorithm or frozen-certificate repair is needed. No target file
was edited.

**Literature check.** [PRIOR_ART.md](PRIOR_ART.md) distinguishes fresh reads,
inherited same-day inventories, and fetch failures. I refreshed the
[official table](https://raw.githubusercontent.com/teorth/optimizationproblems/main/README.md),
[open-PR list](https://github.com/teorth/optimizationproblems/pulls), the seven
named rival repository root pages, and primary
[Bilardi–Schimd](https://arxiv.org/abs/2211.07644) and
[Rosenfeld](https://arxiv.org/abs/2407.18113) abstracts. Direct PR #306/#273
browser requests failed with cache misses, so I make no fresh claim about
their exact live contents. The prior bounded audit credits Jack's canonical
first moment and the prior canonical-script literature; this review supplies
no independent search innovation. Statistical lower confidence endpoints
have a different guarantee and are not substituted for this deterministic
certificate. No stronger applicable certificate was identified within these
limited checks; absence was not proved.

**Reproduction.** All heavy work ran on a rented pod under nohup in
`the job directory`, nice 10, single-threaded BLAS. At most four
single-core compute branches were run concurrently, below the twelve-core
limit. The preexisting target Python environment was used read-only. From
this local review directory, copy the review sources and runner to that lane:

```sh
scp independent.cpp prepare.py audit.py graph_audit.cpp arithmetic.cpp test_arithmetic.py long_audit.cpp mutations.py interface_check.py bank_compare.py run_independent.sh a rented pod:the job directory
ssh a rented pod 'cd the job directory; nohup bash run_independent.sh > receipts/runner.log 2>&1 < /dev/null & echo $! > receipts/runner.pid'
```

The runner reconstructs the small and full certificate directly from the
read-only target frozen artifacts. Keep assertions enabled. Additional commands
below must also run under tmux or nohup on the pod, with output sent to receipts
and PIDs recorded; run sequentially or keep the aggregate core limit:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
PY=the job directory
nice -n 10 "$PY" -u audit.py --certificate the job directory --short 8 --arbitrary 6
nice -n 10 "$PY" -u test_arithmetic.py
nice -n 10 g++ -O3 -std=c++17 -UNDEBUG graph_audit.cpp -o graph_audit
nice -n 10 ./graph_audit tmp/candidate.bin
nice -n 10 g++ -O3 -std=c++17 -UNDEBUG long_audit.cpp -o long_audit
nice -n 10 ./long_audit
```

For the supplied checker and mutations, first copy `verify_frontier.py`,
`verify_frontier.cpp`, `candidate.json.gz`, `small.json.gz`, and
`small_dyadic.json.gz` from the target frozen directory into this lane's
`target_replay/`; this keeps its temporary writes inside the review lane.
Then run the following under the same detached/PID-tracked conditions:

```sh
nice -n 10 "$PY" -u target_replay/verify_frontier.py target_replay/candidate.json.gz
nice -n 10 "$PY" -u mutations.py
nice -n 10 "$PY" -u interface_check.py
```

For the exact bank comparison, finish copying the round-2 frozen artifact to
this lane as `round2.json.gz` before running `bank_compare.py`. An initial
comparison was launched before that transfer finished and failed at gzip EOF;
its receipt is retained and the comparison was rerun only after transfer
completion. Pull all receipts back with:

```sh
scp -r a rented pod:the job directory .
```

**Next action.** Fix the B=0 wrapper condition before advertising support for
that cap, and change P 222's auxiliary bound from 1283 to 1284 bits. The stated
B=1 bound needs no repair. Human refereeing or formal
verification of the frontier induction would further reduce residual risk.
Any stronger bound from larger widths, extra gap savings, or a search
extrapolation needs a separate certificate.

**Completion record.** Review began 2026-11-01 22:08 UTC and completed around
22:26 UTC, well within the three-hour limit. All receipts were pulled back.
The [final pod audit](receipts/final_cleanup.json) at 22:24:00 UTC found all
17 tracked PIDs gone and zero remaining own-lane workers; the later lightweight
capacity-counterexample command also exited before receipt collection.
The full `ps -axo pid,ppid,pcpu,command` snapshots are retained for the pod and
local machine. Source hashes still match the pre-reading record, and the
target proof/report compare byte-for-byte with the saved copies. Only
session-created temporary binary inputs and the temporary round-2 artifact
copy were removed; retained pod files total 29 MB and local review files are
under 1 MB. The pod, its shutdown timer and all other jobs were left running.
No commits, pushes, branches, PRs, posts or external messages were made.

**Overall: PASS for the frozen bound. Probability C91 >= 0.259407 is correct:
99.5% (subjective).**
