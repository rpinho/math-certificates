# C44 round eleven — candidate, unrefereed

**Final frozen replay: PASS. Results are local. All job workers have stopped.**

The candidate result is

    R5 <= 50, R6 <= 107, R7 <= 227, R8 <= 474,

    3/2 <= C44 <=
    39449672077327653986659243787 / 19807040628566084398385987584
    < 1.9916994577 < 2.

The exact gain over round ten is

    772489374956274618667741383 / 39614081257132168796771975168
    = approximately 0.0195003733632519 > 1/10000.

This meets the requested improvement bar through R7. The lower bound
remains 1.5. This is an unrefereed computer-assisted candidate with explicit
published and inherited premises. The two exact implementations were
written separately by the same agent; they are not independent human
refereeing or proof-assistant formalization. No novelty, priority,
optimality or public-record claim is made. Original rounds 9 and 10 are
unchanged.

## Accepted proof and checks

The final proof is [frozen_parity/PROOF.md](frozen_parity/PROOF.md), including
the complete preceding accepted proof and inherited premises. The frozen
manifest SHA256 is

    aceffcb6e28d793b37470b2a41e291ef2eb898c318d52ef3cdd26f21f1170ba8.

[receipts/parity/FINAL_RECEIPT.json](receipts/parity/FINAL_RECEIPT.json)
records PASS at 09:03:15 UTC. It includes the exact bound, all fifteen
partial-completion outputs from each checker, the positive controls and
the artifact hashes. The final replay rejected 120 corrupt artifacts:
96 scalar/dependency tests and 24 direct partial-artifact tests. Two valid
minimum-product controls and two true weaker-claim scalar controls passed.

A count-maximizing degree-d Boolean function has only Fourier sizes of
parity d: otherwise z^d f(zx) preserves degree and adds a relevant input.
Thus a degree-seven count maximizer is odd and its ternary cofactor is
even. At the two decisive weights 15/8 and 31/16, a 21-control degree-six
cofactor has integer norms 120 and 124. The norm gap leaves at least 18 or 17
minimum partials. Exact incidence loss forces a homogeneous minimum seed.
Coordinate permutations reduce the choices to six plus nine cases.

Two newly written acceptance implementations exhaust these cases. A uses
C++ sorted supports, low-pivot elimination and block profiles; B uses
Python immutable sets and highest-pivot span closures. They import neither
the proposer nor each other, use different label/tie conventions, and
both omit the proposer's extra cooccurrence filter. Each visits 78,066
nodes in total and returns zero unsigned leaves in all fifteen cases.
Both retain the actual 12-control minimum-product support in 16 nodes.
Signs and remaining coefficients are relaxed, so a zero leaf count is
sufficient. An integer component-variance argument justifies the closed-
component rejection; it does not presume isolated components are ternary.

The unchanged CHS/Wellens restriction budgets, with the two stronger
control ceilings, yield R7<=227. Two separately maintained exact scalar
implementations agree through degree 96 and add the exact 9508/2^96 tail.
A checks rational next-count exclusions and scalar witnesses; B derives
integer maxima and scans every energy-grid point through degree 16. The
first caps for degrees 5 through 12 are 50,107,227,474,975,1985,4014,8081.
A scalar witness is not a Boolean construction.

The preceding immutable packet in frozen_accepted/ also passed. It proves
a full minimum-energy deficit gap and a degree-six 22-control exclusion,
giving R7<=228,R8<=476,C44<1.9990234376. Its two checkers,76 rejections and
two true weaker-claim controls passed; its manifest is
c5cdbb5d10c52ea072ad2f4d093926a1863dd22415fc8ac370244aaeaa8d2581.
The final extension improves that packet by
580265466762722977564702471/79228162514264337593543950336.

All universal external/inherited dependencies remain explicit: the
minimum-support classification, integer Barnes–Wall gap, cross-polytope
link lemma, complete cubic catalogue, low-weight spectrum and restriction
budgets. Finite implementation agreement does not itself prove those
published completeness/lattice statements. The full-deficit and parity
arguments should receive mathematical refereeing before public use.

## Baseline and lower certificates

The unchanged full inherited replay passed. Both round-nine classifiers
exclude all 189 cases with zero unresolved leaves, visiting 42,853,514 and
43,046,684 nodes. The round-ten ordinary/sign packets and their inherited
controls passed. All 876 retrieved baseline receipt files were hash-checked,
including all 378 classifier outputs. Archive SHA256:

    fdb303660c9da202d27982ec785b6190b9db840f6319f99cffe4bf27ae38e5aa.

The lower certificates establish no improvement over 1.5:

- frozen_lower/: three known-count seeds(46,94,46), all 23 steps of a
  cofactor-splitting chain, two exact verifiers and 24 rejections.
- frozen_search_seeds/: all eight saved best search seeds passed two exact
  Fourier Booleanity checks and 18 rejections. Their verified lifts are 3/2.
- frozen_annihilator/: fourteen explicit Fourier mask banks,34,042 exact
  row inferences, two newly written exact checkers and 16 rejections.
  A uses signed disjoint sets; B substitutes signed free parameters.
  Both reconstruct every convolution row. The remaining kernel is exactly
  span(U), excluding a nontrivial new cofactor within those banks only.
  The manifest is442b33720d517b08c1d92d4242ec3ed4328ce58afa06f93ccb4832c2fc9a61c3.

The finite annihilator obstruction does not establish universal optimality
of 1.5 or classify companions outside the submitted banks.

## Exact reproduction

From this directory on a suitable Linux compute machine, with standard
Python 3 and a C++17 compiler:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  nice -n 10 python3 jobs/reproduce.py --workers 4
```

This sequentially replays the unchanged inherited ordinary/sign packets,
the first accepted round-eleven packet, the final parity packet, and all
three lower certificate families. It writes mutable outputs outside frozen
packets. The inherited historical date guard is bypassed only by its
explicit replay option; finite worker and timeout limits remain.

After the inherited and first accepted receipts exist, the final extension
can be replayed directly:

```sh
nice -n 10 python3 frozen_parity/replay.py
```

The final replay checks all frozen manifests and its accepted predecessor,
compiles both required native sources, runs the two partial checkers and
the two scalar checkers, and exercises all corruption/positive controls.
Search code is not needed for acceptance. Its commands, seeds, memory caps
and timeouts are recorded in jobs/*.json and the archived ledgers. For
example the final exploratory quartic sweep can be reproduced with:

```sh
nice -n 10 python3 jobs/run_batch.py jobs/parity_compile_v2.json --replay
nice -n 10 python3 jobs/run_batch.py jobs/quartic_even_fast.json --replay
```

The cofactor/top proposers additionally use igraph 1.0.0. Group completeness
is not an accepted proof dependency. Every returned map used to build a
saved seed is checked in integer polynomial arithmetic.

## Ranked routes, failures and limits

1. **Full-deficit and direct R7 exclusion succeeded.** The first packet
   already gave R8<=478,C44<2.0067748726. Completing lower-mask complexes
   strengthened its deficit threshold; the direct degree-six exclusion
   then gave R7<=228 and the first below-two packet. Constants and the
   exceptional-link divisibility cases are retained explicitly.
2. **Parity-restricted R7 completion succeeded.** Initial unsigned
   relaxations left closed or partially bridged components. The proven
   component-variance filter removed closed proper components. Completing
   a fresh selected partial by all minimum tensor types resolved the
   bridges. Direct labelled enumeration was superseded by exact fresh-pool
   permutation representatives. The final separately written (same agent) checkers,
   rather than those exploratory outcomes, certify the fifteen exclusions.
3. **R5 top-energy completion remains unfinished.** The target is the
   22-variable quartic energy envelope>=5/8 needed at budget 201/4.
   The original 120-shard sweep(600 seconds per shard,12 workers) finished
   with 29 prototype zero shards,90 timeouts and one assertion abort.
   Only four of the thirty remaining roots closed completely: q22_17,
   q22_20,q22_32,q22_42. The abort occurred when additional forced-minimum
   coordinates made the completed set a proper superset of the selected
   set. It is retained and is not counted as an exclusion. Exact-state
   caching had no useful hits and was dropped. Earlier controls compared
   342 old/flat domains and 1026 connected-component conditions.
   The new parity observation forces every 22-variable quartic to be even.
   A top norm below 5/8 then forces loss>=50 and at least 15 minimum partials,
   reducing the cover to 27 cases. A 60-second scout closed 17 in the
   prototype and timed out on 10. After fixing the completed-set predicate,
   specializing parity and passing 324 exact domain-equivalence controls,
   the remaining ten roots were split into 40 shards at 300 seconds each.
   They finished with 23 zero shards and 17 timeouts. Four additional roots
   closed: even_hom_02,even_hom_03,even_triple_11,even_triple_18. Six of
   the 27 parity roots remain unresolved. These are exploratory results,
   not a new R5 cap or independently certified nonexistence theorem.
4. **Squared-cofactor splitting recovered known counts.** For
   f=x_b U+V, signed permutations preserving U² propose U' and the exact
   split(U+U')/2,(U-U')/2 adds a selector when nontrivial. Xi5 ran 991 graph
   tests with 91 valid splits and best 46. Catalogue5 used 1734 tests with 4
   splits and best 46. Xi6 used 1271 attempts with 106 splits and best 94;
   it skipped 58 oversized graphs and timed out twice. Stalled generated
   groups preserve U up to sign. Skips/timeouts preclude exhaustiveness.
5. **Top-degree gluing recovered 46/94.** Companions with the same degree-d
   part can be joined on a selector without raising degree. Homogeneous
   seeds have no different such Boolean companion by Parseval. The
   complete cubic/Xi allocation baselines were reproduced:49,761 at
   degree 5 and 221,198 at degree 6; all 76/51 high-count allocations formed
   the banks. Finished top-only retries logged 24 top-stabilizer tests in
   each degree,51/31 parity glues, and 20 degree-five CHS duplications.
   No seed above 46/94 emerged. These are finite exploratory families.
6. **Rational cofactor banks gave the finite obstruction above.** A new
   cofactor R must satisfy RV=0 and R²=U². Six degree-five and eight
   degree-six explicit banks, capped at 3000 columns, already have
   ker(RV)=span(U). Only R=+/-U can satisfy the square equation within
   those banks. Coordinates were sampled by numerical signatures;
   those signatures are not asserted to classify all coordinate orbits.

Failures are preserved. Earlier scalar launches before artifact generation
finished ran no mathematical check. An initial trailing-zero histogram
mismatch was corrected before freezing. Earlier replay wrappers expected
the now-valid weaker claim 2 and an unchanged threshold 1 to be rejected;
those control definitions were corrected and every mutation was required
to change its artifact. Their mathematical files were not altered. The
superseded receipts remain in a verified compressed archive.

A transient pod ENOSPC interrupted an initial lower-bank stage. The next
check showed 39 GB free and this job 117 MB. No other-job files were touched.
Complete top-only banks were retried with atomic write retries and
finished. Old RUNNING fields are preserved as stale provenance; the final
process audit confirms that no such worker remains. No failure, timeout,
abort or single-implementation zero enters the accepted upper bound.

## Prior art and credits

PRIOR_ART.md was written before mathematical code. It records the live 44a
HTML/raw table, all 47 open PR diffs and 53 issue-feed entries, matching
comments, recently-updated GitHub searches, required AI-lab/result repos
and recursive trees, primary NS/CHS/Wellens sources, recent arXiv and
citing work since 2024, and indexed public community searches.

The final 09:01:59 UTC recheck found the raw/HTML table, all open PR/issue
metadata, relevant diffs 294/285/283 and all twelve result-repository HEADs
unchanged from the complete 07:55 UTC refresh. The official number remains
4.3576549226*, published Wellens 4.394, and PR 294's candidate 2.0417086280*.
No stronger applicable public result appeared in that bounded check.
X is unavailable. NS/Wellens OpenAlex citation queries were rate-limited;
the NS IAS PDF returned 403. These are explicit coverage limits, not
negative evidence or a basis for a priority claim.

Credits: Nisan–Szegedy; CHS/Wellens weighted restrictions;
Shinkar–Tal/CHS constructions; Rasoolzadeh's complete cubic catalogue;
Valyuzhenich; low-weight Reed–Muller results; Masuda–Panov; Barnes–Wall,
Broué–Enguehard and Nebe; and retained rounds 4–10. Exact source links and
normalizations are in PRIOR_ART.md and the frozen appendices.

## Retrieval, process audit and next work

All mathematical results and search receipts were local by 09:05:07 UTC,
before the 13:00 UTC deadline.
Every member of the 1756-file exploration/verification receipt archive was
hash-checked locally, including the final parity receipt and manifest.
Archive SHA256:

    95730dd0700a2309d6fd5dbcf3fc504f900423089719f6fab3b5c3d7b2c351f5.

See receipts/RETRIEVAL_EXPLORATION.json, EXPLORATION_INDEX.json and
EXPLORATION_RECEIPTS.tar.xz. The separately retrieved upper and full
baseline archives also passed their local hash audits. Duplicated mutable
receipts were moved to macOS Trash only after verified archival. All
frozen artifacts remain present. Retention is below 50 MB; exact accounting
is in receipts/RETENTION.json.

The final pod audit at 09:06:01 UTC and local ps/cwd audit at 09:06:00 UTC found
zero own workers. Computation used at most 14 numerical workers, nice 10,
single-threaded BLAS, within the dedicated pod directory. The pod was
left running; other jobs were not touched. No commits, pushes, PRs,
posts or external messages were made. Original frozen-file and current
manifest checks passed; see the closeout receipts.

Referee the parity-maximality reduction, the fresh-pool quotient and the
component-variance rejection first, then the full-deficit and inherited
universal premises. For R5, finish the six parity roots and write a pair
of independent quartic acceptance verifiers. For the lower bound, broaden
the annihilator bank beyond the submitted derivative/lower masks or use
a structurally different construction. A 47-variable degree-five or
95-variable degree-six seed would suffice; no such certified seed is
supplied here.
