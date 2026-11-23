RESULT: yes
Shipped: independent certificates prove F(n) ≤ 11n/2 for every n ≥ 1,000,000 and F(n) ≤ 5.03n for every n ≥ 1,000,000,000, including odd n.

This is AI work. No human has checked this replay. **Did this job find a new Ramsey bound? No.** It verifies the two constants claimed by Pravar Kataria with Claude and supplies conservative explicit sufficient orders. F is the problem page's universal edge budget for connected triangle-good graphs. The lower bound and the companion extremal function f are outside this verdict.

| Claim | Verdict | Explicit sufficient n₀ | Float maximum candidate | Worst certified upper exponent | Accepted numeric regions | Verified vertices |
|---|---|---:|---:|---:|---:|---:|
| F(n) ≤ 11n/2 | **HOLDS** | 1,000,000 | −0.105247216375770 | −0.0001800948 | 1,305 | 25,124 |
| F(n) ≤ 5.03n | **HOLDS** | 1,000,000,000 | −0.00136833437961620 | −0.0000003225 | 15,004 | 286,537 |

The certified upper endpoints are exact rationals. Both use the uniform cap 4001/10000. A strictly negative endpoint suffices, however close to zero. The uniform finite first-moment bounds at the stated n₀ have logarithms below −6.908 and −73.328, respectively, and decrease thereafter. The probability of a disconnected pairing is below 0.377. Thus for each order in the indicated range there exists a connected simple graph of the required size without a blue embedding in the specified colouring. The computations establish existence and do not identify the smallest threshold or a particular large graph. [Derivation](DERIVATION.md) · [Proof from the exponent to the graph](LEMMAS.md) · [Threshold calculations](finite.log)

## Controls and exact checks

| Check | Result | Evidence |
|---|---|---|
| d=10, no extra edges | Branch and bound could not close the box containing a positive rational witness. Certified primal value >0.00336347, already at cap 0.4. | control-0.json, points.json, controls.log |
| d=10, ⌊0.015n⌋ extra edges | Same failure, with certified primal value >0.0006610277 at the same point. | control-015.json, points.json, controls.log |
| Inner primal-dual gap | At the two reported target profiles, rounded to feasible rational coordinates within 2·10⁻¹², gaps <2.026·10⁻²⁸ and <6.596·10⁻²⁸. The verifier reconstructs symmetric Q with exact row sums. | float.json, points.json, controls.log |
| Exact finite pairing counts | Independent labelled-partner recursion and the factorial type formula agree on all six partitions: 63, 299295, 225, 0, 1890, 101745. All six lie below the finite coefficient upper bound. The fifth uses a single degree defect. | controls.py, controls.log |
| Corruption | Changed only numeric leaf 5's bound in a copy of the 5.03 certificate, subtracting 100. The checker rejected it at a vertex, exit 1. | cert-503-corrupt.json.gz, controls.log |
| Independent coverage | From the exact root the checker reconstructed both children of 1,474 and 16,107 splits. It verified 11 and 67 empty slices, and 159 and 1,037 strict symmetry exclusions. No uncovered or trailing child. | coverage-11.log, coverage-503.log |

For the two negative controls the producer followed the branch containing the preselected point until depth 24, leaving 24 siblings open. The rigorous positive primal on that very branch rules out closure at *any* subdivision depth. These controls establish a limitation of the first moment. They do not decide whether connected non-good graphs exist at those smaller budgets. The small primal-dual gaps concern the inner edge-distribution problem at a stated profile. Global negativity comes from the complete trees. [Control output](controls.log)

## Lemma verdicts

| Step checked | Verdict | Evidence |
|---|---|---|
| Triangle-free red graph on exactly 2n−1 vertices and partwise embedding equivalence | HOLDS | Exact capacities and falling factorials in DERIVATION.md |
| Uniform first-moment bound for the dependent pairing | HOLDS | Symmetric type entropy in DERIVATION.md, finite coefficient proof in LEMMAS.md |
| Dual upper bound, including zeros and the extra-edge term | HOLDS | Relative entropy, monotone Arb evaluation of x log x, and joint convexity proved in LEMMAS.md |
| Finite-cap coverage | HOLDS | Both vertex and stub profiles inside 4001/10000 for n≥7000, rotation and reflection valid for this uniform cap |
| Strict negativity everywhere | HOLDS | check-11.log, check-503.log, coverage-11.log, coverage-503.log |
| Odd orders | HOLDS | Single degree-10 vertex in the otherwise degree-11 sequence. Degree 10 itself works at every order. Entropy perturbation bounded explicitly. |
| Edge rounding and simplicity | HOLDS | ⌊3n/100⌋ draws with replacement across pairs. Loop removal and parallel collapse preserve valid part maps. |
| Connectivity | HOLDS | Cut union bound in LEMMAS.md, including the defective sequence. finite.log verifies the finite constant. |
| Simultaneous existence for every sufficiently large n | HOLDS | Markov and the union bound, with explicit n₀ and no independence assumption between bad events |
| Non-goodness and F(n) | HOLDS | No red triangle and no blue G imply R(K₃,G)>2n−1, hence F(n)≤e(G)−1 |

## Comparison with the supplied documents

The prompt and mandatory prior-art snapshot disclosed the claimant's headline counts at intake. The float derivation and profiles were hashed before certificate production. The independent trees, counts and bounds were added to OWN.sha256 before making this comparison. The producer and checker were written here from the supplied mathematics. No claimant program was fetched, read or run.

| Case | Supplied certificate | This certificate |
|---|---|---|
| 11-regular rate | Uniform cap 0.401, 5,555 accepted regions, worst −0.0500818189… | Uniform cap 0.4001, 1,305 accepted numeric regions, worst −0.0001800948 |
| 10 plus 0.03n | Uniform cap 0.4001, 74,710 accepted regions, worst −0.000500006371… | Same uniform cap, 15,004 accepted numeric regions, worst −0.0000003225 |

The runs certify different margins. Their box test uses a constant upper bound for the extra-edge factor, unreduced coordinates and a prescribed negative margin. This test uses dihedral symmetry, a normalised dual, convexity of the combined objective and the frozen strict-zero pass line. The looser worst leaf is consistent with stopping as soon as the sign is determined. Counts do not measure optimization accuracy. A post-freeze float comparison under the authors' caps gave −0.09854983 for d=11 at 0.401 and +0.00336353 for bare d=10 at 0.4, consistent with their reported approximations. [Matched-cap output](matched-caps.log)

In-scope differences in the documents and their interpretation are as follows.

- The preprint abstract and README describe counting embeddings. Section 3.2 actually counts part assignments. Injections extending an assignment contribute a profile-dependent product of falling factorials. Only the assignment first moment is asserted to decay.
- Section 3.2, Appendix A.4 and BOUNDS.md conflate the unrestricted pairing exponent and the assignment exponent in a sanity check. With A all ones, the pairing event has probability one and rate zero. The assignment rate at fixed profile is H(a), since every map works. In the appendix's printed test the expression is |Ψ+H|. The stated definition of Ψ instead gives Ψ=H in that control. The allowed C₅ calculation uses the correct map entropy.
- The table calls the overlay G(n,0.03n), conventionally a uniform fixed-size simple graph, while the text calls the extra edges independent. It also suppresses the integer rounding. This replay specifies independent unordered distinct-endpoint pairs, replacement across draws, and m=⌊3n/100⌋. The displayed upper rate also bounds uniform sampling without replacement from all pairs: each successive allowed draw has conditional success probability at most the initial allowed fraction. Repeated or overlapping edges cause no difficulty under simplification.
- The documents condition on simplicity for the regular base and describe hanging a pendant vertex from an even-order witness for odd n. The revised preprint explicitly enlarges the old graph's host capacities to those for n, which is essential to that argument. Here the odd degree sequence is handled directly. Degree 10 has no parity restriction. The note uses the looser 0.4+1/n cap estimate, and the TeX gives 0.4+3/(5n). Our common threshold 7000 includes stub imbalance and only controls the cap. The source's 600, 1001, 6000 and 10⁴ figures likewise concern capacity inequalities. The larger explicit existence thresholds above include finite prefactors and connectivity.
- The README and abstract say “exact decimal arithmetic”. Their appendix describes rounded 100-digit transcendental evaluations with a safety margin. This replay uses outward-rounded Arb balls at 160 bits, rational region boundaries and strict inequalities against saved rational upper bounds. The README calls the note four pages, while the staged PDF has six including appendices and references.
- BOUNDS.md also lists a 5.025n run. It is outside the two requested verdicts. The historical baseline in the staged survey is Brandt's proved 84n, with 11.75n announced without the refined proof. Nothing in this report relies on reproducing that announced bound.

The construction and entropy-certificate strategy are credited to Kataria with Claude, building on Brandt's random-regular counting approach. The source for the claims is the pinned repository at 6d4f78cfb15296297450618dde6fea8b15478ccc. The problem-page and community records are the supplied 2026-11-23 snapshots. Live novelty research was outside the permitted network policy. [Pinned source](https://github.com/Sovi11/erdos-1182/tree/6d4f78cfb15296297450618dde6fea8b15478ccc) · [Problem page](https://www.erdosproblems.com/1182) · [Local prior art](PRIOR_ART.md)

## Reproduction

From this job directory, the following verifies the original byte hashes, independently checks both trees, and replays the controls. The runner uses the installed scientific Python at nice 10 with single-thread numerical libraries. Versions used were Python 3.12.13, python-flint 0.9.0, NumPy 2.5.4 and SciPy 1.18.1. The standalone tree checker needs only Python and python-flint.

```sh
shasum -a 256 -c OWN.sha256
./run verify.py 11
./run verify.py 503
./run verify.py 11 --coverage
./run verify.py 503 --coverage
./run controls.py
./run finite.py
```

To regenerate the search products, use a working copy of the job directory. The gzip header carries the creation time. A regenerated archive can have different bytes and the same verified proof tree.

```sh
./run float_search.py
./run produce.py 11
./run verify.py 11 > check-11.log
./run produce.py 503
./run verify.py 503 > check-503.log
./run produce.py 0
./run produce.py 015
./run make_points.py
./run controls.py
./run finite.py
```

No prediction is being scored. The acceptance target was exhaustive certification of the sign over a compact set, so a statistical holdout and a simple-baseline score do not apply. The largest measured peak RSS for the two producers was 78,086,144 bytes on an Apple M5 Pro. The scientific deliverables finished in approximately 12 minutes of the four-hour allowance. The requested referee model was gpt-6.2-astra. The execution environment did not expose independent model-pin attestation. For human review, start with the Hessian estimate and the odd-order entropy prefactor in LEMMAS.md, then run the standalone verifier on the two shipped trees.

CONTROLS: No assumption overrode the controls. In controls.log the two target primal-dual gaps are below 7·10⁻²⁸. The actual control boxes in control-0.json and control-015.json contain rational primal witnesses with strictly positive rates.

CONTRADICTING: No contradictory control or quoted result was dropped. controls.log includes both positive controls and the zero allowed-pairing example. The unrestricted-entropy discrepancy in preprint_main.tex, Appendix A.4, is addressed above. matched-caps.log accounts for the effect of comparing different caps.

LABELS: The two HOLDS verdicts were checked against the tree contents. verify.py recomputed 25,124 and 286,537 vertex bounds and checked all split children. controls.py recomputed six pairing counts and rejected the corrupted bound at node 5 with exit 1.
