RESULT: no
STATEMENT: yes
KERNEL: no

**INCONCLUSIVE under the requested replay criteria.** The pinned Lean solution implies the frozen literature statement in every ambient dimension n ≥ 3. Both bridges compiled. All 1,019 named theorem axiom reports from the 141-module build contained exactly `propext`, `Classical.choice`, and `Quot.sound`, including all twelve public results. The stock comparator stopped at its first call to `landrun` on this Mac, before checking either export. Its enabled nanoda stage did not run. This records a missing verification step, with no mathematical mismatch found.

Shipped: A Lean-checked implication from the authors’ proved upper bound and cap-area identity to the literal double-cap conjecture, together with a local reproduction of the standard-axiom inventory and ten checked mathematical controls.

## Replay evidence

| Check | Observation |
|---|---|
| Frozen clean-room statement | SHA-256 `829ae43b2b95000f8f75bcac56801b4ac847264307d18d60b1ae797e2d315a0b` matched on resume. The first run recorded elaboration before fetching LeanShadow. [Seal](SPEC.sha256) |
| Pinned source and dependencies | Lean 4.33.0, LeanShadow `19deb3ed555cc8404958c1804f9b29898a918d10`. All eleven manifest checkouts matched their revisions. The Mathlib pin is an ancestor of the previously fetched origin/master. [Pins](logs/pins-resume.log) |
| Step A | PASS. The challenge has twelve intentional placeholders. The bridge reports `sorryAx` here as expected. [Challenge elaboration](logs/challenge-resume.log) · [Step A](logs/bridge-a-final.log) |
| Non-vacuity | PASS. Normalized measure is a probability for n ≥ 3; D is measurable, positive and avoids all orthogonal pairs. The proof of independence uses orthogonal residuals after removing the axial components, and the strict thresholds give a contradiction by Cauchy–Schwarz. [Proofs](NonVacuity.lean) · [Axioms](logs/axioms.log) |
| Offline proof compilation | PASS. All 140 files under LeanShadow/ and the root umbrella compiled against the local dependencies. One Mathlib module compiled during the earlier interrupted run; its 14 non-trace outputs matched the official cached archive byte for byte. This resume compiled no Mathlib source. [Build](logs/build-local.log) · [Cache comparison](logs/cache-bytecheck.log) |
| Ordinary Lake build | PASS. After verifying that all 8,705 Mathlib dependency targets were already current, the serial one-thread Lake build compiled the upstream targets and accepted the default library (8,847 jobs). It sampled 6,765,346,816 bytes peak group RSS. The earlier attempt with a nested Lake parent stopped at 6,979,338,240 bytes while compiling ComparatorDefinitions. [Memory-limited attempt](logs/lake-build.log) · [Recovered target](logs/lake-single.log) · [Completed Lake build](logs/lake-build-final.log.gz) |
| Step B and public axioms | PASS. The same bridge body, now importing ComparatorSolution, reports only the three standard axioms. All twelve public declarations were queried afresh after import. The full build also printed 1,019 distinct theorem reports, each with that same axiom set. [Step B](logs/bridge-b.log) · [Queries](Axioms.lean) · [Outputs](logs/axioms.log) |
| Fresh audit objects | PASS. Spec, NonVacuity, both bridges, the public axiom queries and Mutants all re-elaborated against the completed Lake build, starting with an empty directory for audit objects. The rebuilt Spec.olean and NonVacuity.olean matched their pre-checkout originals byte for byte. [Fresh source replay](logs/final-audit.log) · [Command sequence](recheck-audit.sh) |
| Source scan and duplicate definitions | Outside Shadow.lean, ten Lean hits comprised four comment mentions of “axiom” and six local maxHeartbeats settings of 800000. No other requested tokens occurred in Lean sources. All set_option names in the tracked Lean tree were autoImplicit, backward.isDefEq.respectTransparency and maxHeartbeats. The 18-hit repository scan also includes documentation and the verifier’s search expression. The definition diff has only two hunks, explained in the statement table. [Lean hits](logs/source-scan.log) · [Tree hits](logs/tree-scan.log) · [Diff](logs/definitions.diff) |
| Configured comparator, including nanoda | BLOCKED. Both pinned executables built. The comparator reached “Building ComparatorChallenges.Shadow” and then its call to landrun failed. Neither landrun nor nanoda_bin was on PATH. Upstream records a successful Linux run on 2026-09-11; that is a prior author result. [Local command output](logs/comparator-stock.log) · [Authors’ record](https://github.com/allenibiapina/LeanShadow/blob/19deb3ed555cc8404958c1804f9b29898a918d10/comparator-status.json) |
| Comparator functions on actual exports | PASS. The pinned lean4export produced 33,039 challenge and 62,956 solution declarations. The pinned Comparator.compareAt accepted all twelve configured theorem names, the allowed axioms and the driver’s primitive targets; Comparator.checkAxioms accepted the proof dependencies. The Lean kernel replayed the exported solution closure from an empty environment. Only the platform-specific driver and nanoda are missing from this path. [Driver](compare-exports.lean) · [Export log](logs/exports.log) · [Positive result](logs/comparator-functions.log) |
| Comparator corruption control | PASS for the pinned comparison function. An isolated copy changed exactly the denominator 4 to 3 in the definition of delta. Its rebuilt definitions and the original solution theorem objects produced an export of the same 62,956 declarations. Comparator.compareAt rejected **LeanShadow.Comparator.delta** by name. The negative control intentionally injects a stale solution object at the definition boundary. The comparator stopped before axiom or kernel checks, at the comparison being tested. [One-token diff](logs/corruption.diff) · [Comparison input generator](comparison-inputs.py) · [Rejection](logs/comparator-corruption.log) · [Export digests](logs/export-sha256.txt) |
| Final Lake exports | PASS. Re-exporting the ordinary Lake challenge, proved solution, and corrupted copy reproduced all three SHA-256 digests exactly. The comparison and empty-environment kernel results therefore apply to the final ordinary build byte for byte. The three temporary streams totaled about 1.10 GB and were removed after verification; the small logs and generator are retained. [Final exports](logs/exports-lake.log) · [Three digest matches](logs/lake-export-match.log) |
| Bundled leanchecker | PASS. A fresh run replayed all 140 modules beneath the imports-only umbrella, one process per module. Its scope is local declarations checked in their imported environments. It uses Lean’s kernel implementation. The separate export replay above starts from an empty environment. An earlier checker run stopped at a missing object after the memory-limited build interrupted that module; the final run includes it. [Complete replay](logs/leanchecker-final.log) · [Earlier stop](logs/leanchecker.log) · [Checker source at the pinned toolchain](https://github.com/leanprover/lean4/blob/v4.33.0/src/LeanChecker.lean) |

## What the proof establishes

Let A be a measurable subset of the unit sphere in ℝⁿ, with n ≥ 3. Suppose every x,y ∈ A has nonzero real inner product. For **every** unit vector a, the normalized surface measure of A is at most the measure of the open set D(a) = {x : |⟨a,x⟩| > cos(π/4)}. D(a) itself is measurable, has positive measure, and contains no orthogonal pair, so the bound is sharp. The authors’ input class includes sets measurable in the completion of uniform surface measure. Their equality theorem gives agreement almost everywhere with a double cap. [Frozen spec](Spec.lean) · [Geometric witness](NonVacuity.lean) · [Proved bridge](Bridge.lean) · [All twelve statements](STATEMENT_TABLE.md)

The bridge specializes the finite index type to Fin n and the ambient Haar measure to volume. The no-orthogonal-pair predicate and open-cap definitions agree by definitional reduction. Borel measurability gives completed measurability. The authors’ **caps_attain**, first conjunct, identifies their δ(n−2) with the real area of D(a). The independent probability proof makes conversion back to extended nonnegative measures order preserving. The bridge uses `double_cap_bound` and `caps_attain`. Its direction is exactly the one requested; the frozen upper bound alone would not imply the authors’ separate rigidity results. [Challenge bridge](BridgeChallenge.lean) · [Solution bridge](Bridge.lean)

## Mathematical controls

| Change | Local Lean result |
|---|---|
| Multiply the bound by 99/100 | Refuted on S² by D, whose normalized area is positive. |
| Radius π/5 | Refuted on S² by D. Cap area there is 1−cos r, strictly increasing across these two radii. |
| Strict inequality | Refuted by taking A = D, which would require μ(D) < μ(D). |
| Use the Sⁿ cap value where the domain is Sⁿ⁻¹ | Refuted for n=3. Lean evaluates the sine-power integrals on S² and S³ and compares their values strictly. The S³ cap has area 1/2−1/π, below 1−√2/2. |
| On S² subtract 1/1000 | Refuted by D at the original bound. |
| Closed caps avoid orthogonality | Refuted by the two unit vectors (1,1,0)/√2 and (1,−1,0)/√2 for axis (1,0,0). Their inner product is zero and both meet the boundary exactly. |
| Use unnormalized surface area | Refuted when raw area of A is compared to the stated probability bound. The raw S² total is 4π. Replacing the measure **on both sides** preserves the inequality in every allowed dimension; Lean proves that equivalence separately. |
| Radius π/3 | Derived from the proved bridge by cap inclusion and measure monotonicity. |
| Borel-measurable sets only | Derived from the proved bridge using the Borel measurable space on the sphere. |
| Restrict to n ≥ 4 | Derived from the proved bridge by arithmetic. |
| Drop measurability | **Undetermined.** The published theorem requires completed measurability. The outer measure is defined on arbitrary sets, but independence supplies no measurability hypothesis in this argument. No counterexample or extension was established. |

Every numerical refutation includes measurability and pointwise independence of its D witness. The explicit axis exists in both finite dimensions used for the comparisons. The closed-cap control uses the displayed boundary points since they are excluded from the open D. [Control proofs](Mutants.lean) · [Compiled controls and axioms](logs/mutants-final.log)

## Scope and prior art

This is a replay of Ibiapina, Gomes, Pio, Belo and Ferreira’s public LeanShadow proof. The prior-art record gives the claimed sharp S² value 1−1/√2 ≈ 0.292893, the previous 0.2953 upper bound, and the authors’ own comparator record. The job froze the literature-based spec before opening the repository. A proof certificate has a fixed universal proposition and deterministic checks of its declarations. There is no prediction, sampled score or statistical holdout. **New mathematical result? No.** [Prior art](PRIOR_ART.md) · [Paper](https://arxiv.org/abs/2610.27523) · [Pinned repository](https://github.com/allenibiapina/LeanShadow/tree/19deb3ed555cc8404958c1804f9b29898a918d10)

The initial bridge draft needed an explicit conversion from 3 ≤ n to 2 < n. The first control draft had elaboration errors in the cap-mass conversion, measure notation and witness terms. Those diagnostics are retained alongside the final successful runs. The geometric hypotheses, pass criteria and sealed source were held fixed. [Initial bridge](logs/bridge-a.log) · [Initial controls](logs/mutants-first.log)

## Reproduction

Use the pinned checkout, its manifest dependencies, and the official 4.33.0 toolchain already in this job. Run from the job root. The existing upstream.sh expands to nice -n 10 followed by the bounded, offline third_party.py run command with the pinned URL and commit. The original replay wrapper has an absolute cutoff of 03:03:56 UTC on 2026-11-23. A later authorized reproduction on macOS can start a new two-hour window with the line below. This run used the fixed original cutoff.

```bash
# For a later authorized run only, set this ONCE before all checks:
export LEANSHADOW_REPLAY_DEADLINE="$(date -u -v+2H +%s)"
shasum -a 256 -c SPEC.sha256
git -C deps/third_party/mathlib4-db584cd6d46c merge-base --is-ancestor \
  db584cd6d46c92f209a44c0f1c829460d327499d origin/master
./upstream.sh 180 "$PWD/own-lean.sh" -o Spec.olean Spec.lean
./upstream.sh 180 "$PWD/own-lean.sh" -o NonVacuity.olean NonVacuity.lean
./upstream.sh 180 lake env lean -j2 -o .lake/build/lib/lean/ComparatorChallenges/Shadow.olean ComparatorChallenges/Shadow.lean
./upstream.sh 180 lake env "$PWD/audit-lean.sh" -o BridgeChallenge.olean BridgeChallenge.lean
./upstream.sh 3400 lake env python3 "$PWD/build-local.py"
./upstream.sh 180 lake env "$PWD/audit-lean.sh" -o Bridge.olean Bridge.lean
./upstream.sh 180 lake env "$PWD/audit-lean.sh" Axioms.lean
./upstream.sh 300 lake env "$PWD/audit-lean.sh" -o Mutants.olean Mutants.lean
./upstream.sh 300 /bin/bash "$PWD/run-stock.sh"
```

The last command invokes the configured comparator and exits unsuccessfully on this Mac. The following commands reproduce the comparison of actual exports, including the expected rejection on the final input pair. The scratch exports can be regenerated from source and checked against the recorded SHA-256 values.

```bash
./upstream.sh 1200 lake env python3 "$PWD/comparison-inputs.py"
shasum -a 256 -c logs/export-sha256.txt
./upstream.sh 1000 lake env lean -j2 --run "$PWD/compare-exports.lean" \
  ComparatorChallenges/LeanShadow.json "$PWD/tmp/challenge.ndjson" "$PWD/tmp/solution.ndjson"
./upstream.sh 600 lake env lean -j2 --run "$PWD/compare-exports.lean" \
  ComparatorChallenges/LeanShadow.json "$PWD/tmp/challenge.ndjson" "$PWD/tmp/corrupt.ndjson"
```

The statement-level and proved bridges must run in separate Lean environments because the public challenge and solution intentionally use the same declaration names. No challenge placeholder can discharge Step B. [Step A output](logs/bridge-a-final.log) · [Step B output](logs/bridge-b.log)

For the ordinary Lake build, the bundled checker, and the final re-elaboration from a fresh directory of audit objects, use the following commands with the same wrapper:

```bash
./upstream.sh 3300 env LEAN_NUM_THREADS=1 MIMALLOC_PURGE_DELAY=0 python3 "$PWD/replay-standard-build.py"
./upstream.sh 2800 lake env python3 "$PWD/replay-kernel.py"
./upstream.sh 180 env LEAN_NUM_THREADS=1 MIMALLOC_PURGE_DELAY=0 lake build +ComparatorChallenges.Shadow
./upstream.sh 500 lake env "$PWD/recheck-audit.sh"
```

All executions of upstream code used the pinned offline sandbox. Heavy Lean processes ran serially, with at most two Lean threads and the prescribed nice increment. The host shell already had reduced priority. The largest sampled process-group RSS was 6.98 GB in the stopped attempt. The job occupied 12.75 GB immediately before removing the reproducible temporary streams. The resumed run finished inside its two-hour replay window. The final harness command is `/usr/bin/python3 -I ~/.local/share/research-harness/tools/third_party.py check "$PWD"`. [Harness check](logs/third-party-check.log)

## Referee verdict

**CONTROLS:** No assumption overrode a control. Lean refuted all seven specified strengthenings under the stated mixed-unit reading and derived all three positive controls. In particular, changing to raw area on *both* sides preserves the bound. The positive comparator input passed and the otherwise identical corrupted definition was rejected by name. [Mutant proofs](Mutants.lean) · [Axiom reports for controls](logs/mutants-final.log) · [Corruption result](logs/comparator-corruption.log)

**CONTRADICTING:** No contrary observation was omitted from the verdict. The stock command exited 1 before comparing the inputs, the challenge bridge exposes sorryAx, and the first ordinary Lake run hit the memory guard. Each has its own log. The full kernel-workflow verdict remains no despite the successful standard-axiom inventory and local kernel replays. [Stock comparator](logs/comparator-stock.log) · [Challenge axioms](logs/bridge-a-final.log) · [Interrupted Lake run](logs/lake-build.log)

**LABELS:** The verdict does not rely on the authors’ “passed” annotation. I checked the frozen spec hash, the 87 shared definition lines, 328 proof imports with zero challenge imports, the live twelve public axiom queries and the raw export comparison. The deliberate one-token mutation tests whether that comparison actually reads the definition of δ. [Source check](logs/source-scan-command.txt) · [Axioms](logs/axioms.log) · [Export comparison](logs/comparator-functions.log) · [Mutation](logs/corruption.diff)

**Remaining step.** For a complete reproduction of the authors’ workflow, run the exact pinned comparator configuration on an authorized Linux installation with landrun v0.1.17 and nanoda v0.4.17 at commit `4c544ed4099c8227f07d5de77ad1e69fb0740a27`. The test is `lake exe comparator ComparatorChallenges/LeanShadow.json` with nanoda enabled, followed by the corrupted-copy rejection. The missing executables were absent from both the job tree and its PATH on this arm64 Mac. That Linux run is the remaining condition for MATCH. [Local platform check](logs/platform.log) · [Upstream invocation](https://github.com/allenibiapina/LeanShadow/blob/19deb3ed555cc8404958c1804f9b29898a918d10/ComparatorChallenges/README.md)
