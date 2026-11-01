**Overall verdict: PASS. The proof and independently replayed frozen certificate
establish C91 >= 0.256801. I found no counterexample or mathematical gap.
My subjective probability that the bound is correct is 99.5%.**
Started 2026-11-01 20:46 UTC. This probability assesses correctness, not novelty,
publication status, or optimality; it is separate from simulation confidence.

P denotes the reviewed [PROOF.md](sources/target_PROOF.md); R denotes the reviewed
[REPORT.md](sources/target_REPORT.md). Line numbers below refer to those frozen
copies, which match the target files at the start of review. No target file was
modified. This review concerns correctness, not novelty or optimality.

| Requested step | Verdict | Exact target lines | Finding |
|---|---|---|---|
| Typical-set counting and passage to expected distance | PASS | P 107–145, 158–161; R 13, 17 | Statistics belong to input strings; their path increments telescope even across gaps. Fixed-epsilon typicality proves the stated probability tends to zero. An o(1) discarded event is sufficient for the expectation limit. R 13 needs the tolerance clarification below for its literal exp(o(n)) wording. |
| Unbounded competitors, caps, and merging of scores | PASS | P 43–68, 72–103; R 14 | Each rejection produces an explicit strictly smaller canonical key. Width/score dropout only forgets tests. Equal-direction/equal-width buffers agree, so retaining the minimum score is sound. No rejected canonical optimum was found. |
| Weighted bisimulation and expansion to the full product | PASS | R 15, 21–31; P 149–161, 174–206 | The search quotient is mathematically sound by weighted partition refinement. The final certificate passes every row on the reconstructed, unmerged product, independent of that quotient. |

**Typicality: the probability space and every inequality.** Write

\[
H_j=F_j(X)+F_j(Y),\qquad Z(X,Y)=\prod_j z_j^{H_j},
\qquad C=\sum_j|\log z_j|.
\]

At each column, a consumed X bit updates only X's history, and a consumed Y bit
updates only Y's history. An absent coordinate contributes zero and keeps its
history unchanged. Thus the next bit after a gap still sees the preceding bits
of that input string. The lag and four-spin terms are counted exactly once,
when the last bit of their support is consumed. Initial histories emit no
incomplete block terms. For any labeled path consuming strings X,Y, the product
of its column factors is exactly

\[
2^{-|X|-|Y|}x^{|X|+|Y|}t^{\operatorname{cost}}Z(X,Y).
\]

This is an identity for each labeled path, not an independence assumption about
columns conditioned on acceptance or on a canonical path. It remains true for
adjacent gaps, although some such paths are rejected by other rules. Distinct
string pairs have distinct selected labeled canonical words. A pair can have
other accepted words; these only increase the all-path sum G. With strings
fixed, different alignments have the same Z factor. The tilts therefore apply
to the inputs, not to alignment-dependent correlations.

For equal-length n strings on T_n, Z is at least exp(-epsilon*n*C).
Because t<1 and canonical cost is at most a*n, t^cost is at least t^(a*n).
Selecting only those canonical words in the all-path sum gives

\[
G\ge x^{2n}t^{an}e^{-\epsilon nC}
       \Pr(\mathrm{ed}\le an, T_n).
\]

This rearranges to precisely P 138–139, with the signs as written. The factor
2^(-2n) is the probability of a complete pair; gaps do not introduce any extra
normalization. Unequal endpoints are merely extra nonnegative terms in G.
All states accept, including the empty state and terminal gaps.

For each fixed feature, the spin monomials have mean zero and variance O(n).
Indeed, distinct supports give orthogonal Walsh monomials even if they overlap,
so Var(H_j)<=2n. Chebyshev and a union bound for four features give
Pr(T_n^c)<=8/(epsilon^2*n). If delta=2 log x+a log t>0, choose fixed epsilon
with epsilon*C<delta; then Pr(ed<=an)<=G exp[-n(delta-epsilon*C)]+o(1), hence
it tends to zero. No exponential estimate for the discarded event is used.

Nonnegativity yields E[ed]/n >= a*Pr(ed>an), whose liminf is at least a.
Concatenating optimal alignments gives e_(m+n)<=e_m+e_n, so Fekete's lemma
supplies the limit C91=inf e_n/n. Thus C91>=a. There is no unjustified exchange
of limits and expectations and no need for the discarded event to be
exponentially unlikely.

The report's exp(o(n)) phrase at R 13 is imprecise if applied uniformly to the
proof's fixed-epsilon T_n: the written bound there is exp(O(epsilon*n)). To
obtain the literal phrase, use epsilon_n=n^(-1/4). The same Chebyshev bound gives
Pr(T_n^c)<=8/sqrt(n), and |log Z|<=C*n^(3/4)=o(n) on that event. Either version
proves the result. This is a wording correction, not a gap in P 115–143.

**Competitors: why a rejection is globally safe.** For a retained D-starting
segment, let m_X-m_Y=r>0. The reference alignment pairs its first m_Y symbols
diagonally, then deletes its last r X symbols. Its cost is the Hamming cost of
those pairs plus r. Appending D changes both actual and reference cost by one.
Appending a diagonal consumes the oldest residual X symbol in the reference,
giving the mismatch difference in P 80–82. Appending I removes one residual
gap while the actual segment pays one for I; this gives mismatch-2, not
mismatch-1. These are exactly changes in reference cost minus actual cost.

At a rejection, at least one opposite-coordinate symbol has been consumed.
The reference therefore begins with a diagonal while the actual segment begins
with a gap. Its residual gap count is |m_X-m_Y|, at most the actual gap count.
A negative S improves cost; S=0 with fewer gaps improves the second key; S=0
with equal gaps improves the first operation, diagonal<gap. This reasoning
also covers r=0 at the rejection. The symmetric I construction is identical.

Splicing this reference segment into the global path preserves both consumed
substrings. If cost and gap count agree, the number of columns agrees too:
columns=(m_X+m_Y+gaps)/2. A local lexicographic improvement therefore improves
the global operation word. The same one canonical global optimum obeys all
five run rules (P 19–39), all checked forbidden words, and all competitor tests.

For fixed direction and r, every residual buffer is exactly the last r input
symbols, independent of its segment's start. Future score increments coincide.
Keeping the smallest score cannot cause a false rejection: it belongs to an
actual candidate. Dropping a candidate at width or score caps, or after a
nonrejecting return to r=0, forgets a possible improvement. It never invents
one. The memory is finite but the segment length is unbounded.

**Independent adversarial evidence.** The pre-reading verifier source and its
hash are preserved in [the independence record](receipts/INDEPENDENCE.md).
The initial implementation was written from P alone before opening target code
or R. It used equivalent neutral run memories; after reading the target checker
I adapted only that memory representation to retain literal last diagonals and
match the frozen BFS IDs. The unchanged pre-reading file is retained. The final
verifier imports no target code. This post-reading numbering adaptation is an
explicit limit to implementation blindness.

The checks used my own whole-key suffix DP and, separately, a scalar cost/gap
suffix DP with forward greedy operation reconstruction. Both minimize
(edit cost, gap count, operation word). Literal enumeration of every alignment
validated the oracle on all 961 pairs with lengths 0..4.

- [Full-bank survival](receipts/full_paths.log): all 261,121 ordered pairs whose
  lengths each range from 0 to 8; 256 seeded uniform random pairs with lengths
  257..1024; 112 empty/constant/alternating endpoint cases through length 1024.
  Every canonical word survives the actual frozen pattern bank, run memory,
  competitor memory and input-history product.
- [Additional mixed inputs and features](receipts/canonical_audit.log): every
  equal-length pair through n=8, plus 3,000 random uniform, biased, periodic and
  perturbed-related pairs with lengths through 256. Feature totals agree with
  direct full-string calculations. Every one of the 299,593 labeled paths with
  at most six columns also passes the feature identity, independently of
  acceptance.
- [Explicit competitor witnesses](receipts/adversarial.log): all labeled paths
  through six columns plus 20,000 seeded paths through 512 columns, totaling
  319,593 paths and 1,155,904 inspected columns. The reference checker retains
  actual segment start positions, reconstructs substrings, and recomputes
  reference Hamming cost from scratch rather than using the score recurrence.
  It agrees with the compressed scores up to rejection, and every one of the
  292,624 rejected paths has a strictly smaller directly computed canonical key.
- [Long-segment stress](receipts/extra_checks.log): persistent width-one and
  width-two competitors in both directions through 10,000 diagonals survive
  their prefixes and correctly reject a closing opposite gap. These cover
  segment lengths far beyond the finite forbidden-word window.
- [Smaller replay and corruptions](receipts/mutations.log): the L=5/W=1/B=2
  certificate passes independently with 302 patterns, 3,655 states and 12,048
  edges at a=0.241210. Eight corruptions are rejected: canonical forbidden word,
  missing/extra/zero vector entry, invalid positive potential, false exponent,
  false tilt and wrong original-state count.

One supplementary test initially had an assertion in the wrong place for an
already rejecting negative score. I corrected it and retained its failed
first receipt. No target defect is being inferred from that reviewer-test bug.

**Weighted merging and the actual verification obligation.** In
[minimize_weighted.cpp](sources/target_minimize_weighted.cpp), lines 15–24 encode
each allowed edge by cost/length class, integer feature increments, and current
destination class, then sort the eight slots. Absent edges are zero; present
edges have destination-class-plus-one and cannot collide with zero. Sorting
preserves multiplicity, so equal signatures give equal weighted sums into
every class for all rational parameters. Starting from the single class, this
is monotone partition refinement; unchanged class count means stabilization.
All states have the same acceptance value. It defines a valid weighted quotient.

[freeze.py](sources/target_freeze.py), lines 6–8 expand v_i=small[mapping_i]
before integer rounding. Rounding can destroy a matrix inequality, so the
expanded vector alone must be checked. The target checker, lines 154–175,
reconstructs original and full product states and checks every reachable row;
it does not load the quotient map or trust an edge list. My replay independently
does the same using direct suffix membership, semantic histories and scores,
and rational weights computed directly from P 125. Even a faulty search
quotient cannot evade that full-product row test.

**Full frozen replay.** [The independent replay](receipts/independent_replay.log)
passed in 396.76 seconds. It checks all 1,282,850 forbidden words, reconstructs
all 1,299,053 original states, then all 7,206,135 full product states and
29,465,392 allowed labeled edges. The vector length agrees exactly and all
entries are positive integers. Every reachable row satisfies AV<V, including
initial and terminal states. No quotient graph or optimizer output is imported.
Certificate SHA-256 matches exactly:
472cb2e9a0bc3b377f0ea0bf4a8d052c93fa4be4a3c81d81566be92655165c67.
The maximum exact row ratio is

```text
865073640661142007481728205313442885467607547100691069 /
865075071492390299868836559374582632341847000000000000 < 1.
```

The minimum integer row slack is strictly positive and recorded in the receipt.
My denominator is formed from reduced rationals, so its numerical slack differs
from the target's unreduced-denominator receipt without affecting any inequality.
The exact exponent has already passed an independent 256-bit Arb check:
2 log x+a log t = 8.39512132606088543424279329920572424496...e-7 > 0;
the threshold is 0.25680176323107792832109235075448894572... .
The full verifier additionally uses an exact rational atanh logarithm series
with a geometric remainder, removing reliance on floating logarithms.

**Small-n expectations and simulations.** A separate plain Wagner–Fischer C++
program enumerated every ordered pair through n=11, without symmetry pruning.
Every histogram sums to 4^n; its results agree with my canonical DP at all
overlapping sizes. [Raw receipt](receipts/numerical.log):

| n | Exact e_n/n | Decimal |
|---|---|---|
| 1 | 1/2 | 0.500000000 |
| 2 | 1/2 | 0.500000000 |
| 3 | 47/96 | 0.489583333 |
| 4 | 243/512 | 0.474609375 |
| 5 | 1179/2560 | 0.460546875 |
| 6 | 2755/6144 | 0.448404948 |
| 7 | 12561/28672 | 0.438092913 |
| 8 | 56261/131072 | 0.429237366 |
| 9 | 41443/98304 | 0.421579997 |
| 10 | 2175407/5242880 | 0.414925957 |
| 11 | 589839/1441792 | 0.409101313 |

All exceed the claimed lower bound. They do not imply the asymptotic constant
is near 0.41: subadditivity gives C91<=e_n/n, and convergence is slow. My seeded
plain-DP simulations give normalized sample means 0.320251 at n=128 (128 pairs),
0.302505 at n=512 (128), 0.293121 at n=2048 (128), and 0.289738 at n=8192 (32).
These are sanity checks, not lower-bound certificates or asymptotic estimates.

[Bilardi–Schimd, Table 4](https://arxiv.org/html/2211.07644v2) give the raw binary
mean 0.28817 at n=32768 from 512 pairs. Their Table 6 reports the adjusted
asymptotic estimate 0.27496 and 99.9% confidence interval [0.26108,0.28884].
The number near 0.275 is therefore not the raw finite-n sample mean. The
statistical endpoint 0.26108 is numerically stronger than 0.256801, but has a
statistical guarantee. [Rosenfeld, Table 1(a)](https://arxiv.org/html/2407.18113v1)
gives deterministic upper bound 0.315514. The proposed deterministic interval
[0.256801,0.315514] is consistent with all these results and leaves substantial
room below the simulations. The increase over 0.254046 is exactly 0.002755.

**Literature scope.** [PRIOR_ART.md](PRIOR_ART.md) records fresh primary reads,
the official table/open-PR check, seven rival README refreshes and inherited
same-day search inventory. No stronger applicable public deterministic lower
certificate was identified. C91 is a proposed entry in PR #273, rather than a
merged row in the current main table. This review makes no priority claim.
Credit for the inherited method belongs to Jack's canonical first moment and
the prior canonical-script work cited by the target. The search optimizer and
the extrapolation fits in R 57–61 were not reproduced; they are not needed to
verify the frozen lower bound.

**Reproduction.** All heavy work ran under nohup on a rented pod, in this review's
own lane, with nice 10 and single-threaded BLAS. No more than four single-core
workers were running simultaneously. The existing pod Python environment was
used read-only. Keep assertions enabled. From the local review directory:

```sh
ssh a rented pod 'mkdir -p the job directory'
scp *.py numerical.cpp a rented pod:the job directory
scp run_review.sh a rented pod:the job directory
ssh a rented pod 'cp the job directory the job directory'
ssh a rented pod 'cp the job directory the job directory'
```

In that pod directory, launch each command below under nohup, redirecting to
its receipt and recording its PID as in the supplied run script. They may also
be run sequentially inside tmux:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
PY=the job directory
nice -n 10 "$PY" -u independent.py --certificate candidate.json.gz
nice -n 10 "$PY" -u independent_before_target_read.py --audit --short 8 --random 3000 --maxlen 256
nice -n 10 "$PY" -u full_paths.py
nice -n 10 "$PY" -u adversarial.py
nice -n 10 "$PY" -u mutations.py
nice -n 10 "$PY" -u extra_checks.py
nice -n 10 g++ -O3 -std=c++17 numerical.cpp -o numerical
nice -n 10 ./numerical
```

Retrieve with `scp -r a rented pod:the job directory .`.
The complete sequential detached replay can instead be launched directly with:

```sh
ssh a rented pod 'cd the job directory; nohup bash run_review.sh > receipts/runner.log 2>&1 < /dev/null & echo $! > receipts/runner.pid'
```

No deletion, commit, push, PR, post, email or external message was made. The
pod timer and all other jobs were untouched. Final process cleanup and artifact
integrity receipts are collected separately.

**What to do next.** No repair is needed for the stated bound. Before reusing
the exposition, clarify R 13 by specifying a shrinking tolerance or keeping the
fixed-epsilon estimate actually used in P. A human referee or formalized proof
would provide further assurance. Increasing the window, adding competitors or
using the search extrapolation to promise a stronger bound requires a new
certificate; none of those claims is part of this PASS verdict.

Completed 2026-11-01 20:57 UTC, about eleven minutes after starting, well before
the three-hour limit and pod shutdown. All receipts were pulled back. The
[final cleanup audit](receipts/final_cleanup.json) at 20:56:34 UTC found zero
remaining tracked processes and zero own-lane workers, using all ten tracked
PIDs, process working directories and `ps -axo pid,ppid,pcpu,command`.
It confirms both verifier hashes and the exact certificate hash. The reviewed
target proof and report still compare byte-for-byte equal to the saved copies.
The local process snapshot was also collected. Retained review files occupy
about 1.1 MB; the 36.49 MB frozen certificate remains read-only in the sibling
target directory and has not been duplicated locally. The pod and other jobs
were left running.

**Overall verdict: PASS. Subjective probability that C91 >= 0.256801 is correct:
99.5%.**
