# Double-cap conjecture (LeanShadow): clean-room audit of the Lean proof

**Status: AI work. No human has checked it. No new result is claimed. This is a replay of the authors' result.**

This folder records my audit of the Lean 4 proof of the double-cap conjecture by A. Ibiapina, C. A. Gomes, A. Pio, S. Belo and E. Ferreira
([arXiv:2610.27523](https://arxiv.org/abs/2610.27523); repository [allenibiapina/LeanShadow](https://github.com/allenibiapina/LeanShadow/tree/19deb3ed555cc8404958c1804f9b29898a918d10), pinned at commit `19deb3ed555cc8404958c1804f9b29898a918d10`).
It exists so that anyone can see what was and was not checked, and so that a note to the authors can link one pinned folder.
It contains no file from the authors' repository; links point to it at the pinned commit.

The audit was done by an AI model (GPT-6.2 Astra) in a clean room: the authors' code was never read. It was only built and run in an offline sandbox, and its declarations were queried and exported by Lean tools.

## 1. What was checked

The target statement was written down from the literature before the repository was opened, and sealed by its SHA-256 ([audit/Spec.lean](audit/Spec.lean), [audit/SPEC.sha256](audit/SPEC.sha256)):

> For every n ≥ 3, every unit vector a and every measurable subset A of the unit sphere in ℝⁿ such that no two points of A are orthogonal, the normalized surface measure of A is at most that of the open double cap D(a) = {x : |⟨a, x⟩| > cos(π/4)}.

On S² the bound is 1 − √2/2 ≈ 0.292893.

## 2. Verdict and its scope

| Question | Verdict |
|---|---|
| STATEMENT: does the authors' proved theorem imply the frozen statement? | **Matches.** A Lean bridge ([audit/Bridge.lean](audit/Bridge.lean)) derives the frozen `Conjecture` from the authors' `double_cap_bound` and the first part of `caps_attain`, in every dimension n ≥ 3. It compiles, and `#print axioms` reports only `propext`, `Classical.choice` and `Quot.sound`. |
| KERNEL: does the full proof check under the authors' configured workflow? | **Complete except one step.** Everything below passed. The one step not run is the authors' stock comparator driver and its nanoda stage: the driver calls `landrun`, a Linux-only sandbox, and stopped at that call on macOS before comparing anything ([audit/logs/comparator-stock.log](audit/logs/comparator-stock.log)). |

The kernel evidence that did run:

- **Build.** All 140 files under [LeanShadow/](https://github.com/allenibiapina/LeanShadow/tree/19deb3ed555cc8404958c1804f9b29898a918d10/LeanShadow) compiled offline against the pinned Mathlib with Lean 4.33.0, and the ordinary Lake build finished (8,847 jobs) ([audit/logs/build-local.log](audit/logs/build-local.log), [audit/logs/lake-build-final.log.gz](audit/logs/lake-build-final.log.gz)).
- **Axioms.** All twelve public theorems, queried afresh after import, depend only on `propext`, `Classical.choice` and `Quot.sound` ([audit/Axioms.lean](audit/Axioms.lean), [audit/logs/axioms.log](audit/logs/axioms.log)). The full build printed 1,019 theorem axiom reports, all with that same set.
- **leanchecker.** Lean's bundled checker replayed all 140 modules, one process per module ([audit/logs/leanchecker-final.log](audit/logs/leanchecker-final.log)).
- **Comparison functions on real exports.** The pinned `lean4export` exported 33,039 challenge and 62,956 solution declarations. The pinned `Comparator.compareAt` accepted all twelve configured theorems, `Comparator.checkAxioms` passed, and the Lean kernel replayed the exported proof closure from an empty environment ([audit/compare-exports.lean](audit/compare-exports.lean), [audit/logs/comparator-functions.log](audit/logs/comparator-functions.log)). This is the comparator's own logic run by a small driver; it is not the authors' driver, and nanoda was not run.
- **Corruption control.** In a copy, changing one denominator in the definition of δ (4 to 3) made `Comparator.compareAt` reject `LeanShadow.Comparator.delta` by name ([audit/logs/corruption.diff](audit/logs/corruption.diff), [audit/logs/comparator-corruption.log](audit/logs/comparator-corruption.log)).
- **Non-vacuity and mathematical controls.** D is measurable, has positive measure and contains no orthogonal pair ([audit/NonVacuity.lean](audit/NonVacuity.lean)). Seven strengthened statements (bound times 99/100, radius π/5, strict inequality, the wrong sphere's cap value, and others) are refuted in Lean, and three weakenings are derived from the bridge ([audit/Mutants.lean](audit/Mutants.lean), [audit/logs/mutants-final.log](audit/logs/mutants-final.log)). Dropping measurability is left undetermined.

What the twelve public statements say, and how they differ from the published claims, is in [audit/STATEMENT_TABLE.md](audit/STATEMENT_TABLE.md). The full audit report, with every log, is [audit/REPORT.md](audit/REPORT.md); its first lines read `RESULT: no`, `STATEMENT: yes`, `KERNEL: no` because the job's pass line required the stock comparator run.

## 3. What was not run

- The authors' comparator driver (`lake exe comparator` on [ComparatorChallenges/LeanShadow.json](https://github.com/allenibiapina/LeanShadow/blob/19deb3ed555cc8404958c1804f9b29898a918d10/ComparatorChallenges/LeanShadow.json)) with `landrun` v0.1.17 and nanoda v0.4.17. Neither tool was available on this arm64 Mac. The authors record a successful Linux run ([comparator-status.json](https://github.com/allenibiapina/LeanShadow/blob/19deb3ed555cc8404958c1804f9b29898a918d10/comparator-status.json)); that is their result, not mine. Running it on Linux, followed by the corrupted-copy rejection, is the remaining step.
- No second, independent kernel (nanoda or lean4lean). leanchecker and the export replay both use Lean's own kernel.
- No reading of the proof itself, by me or by a human.

## 4. How to replay

You need the pinned repository and its manifest dependencies, the official Lean 4.33.0 toolchain (via elan) and the Mathlib cache. The audit ran the authors' code inside an offline sandbox wrapper (`audit/upstream.sh`, which calls a local sandbox tool that is not in this folder). On your machine, run the authors' build in your own sandbox. The standard sequence is:

```sh
git clone https://github.com/allenibiapina/LeanShadow.git && cd LeanShadow
git checkout 19deb3ed555cc8404958c1804f9b29898a918d10
lake exe cache get                       # Mathlib build cache at the manifest pin
lake build                               # the authors' library
lake build +ComparatorChallenges.Shadow  # the challenge statements
cp PATH/TO/THIS/FOLDER/audit/*.lean .
export LEAN_PATH="$PWD:$(lake env printenv LEAN_PATH)"
lean -o Spec.olean Spec.lean
lean -o NonVacuity.olean NonVacuity.lean
lean -o BridgeChallenge.olean BridgeChallenge.lean  # reports sorryAx: the challenge's placeholders, as expected
lean -o Bridge.olean Bridge.lean                    # propext, Classical.choice, Quot.sound only
lean Axioms.lean
lean Mutants.lean
lake exe comparator ComparatorChallenges/LeanShadow.json  # the step I could not run: Linux, landrun and nanoda
```

Each `lean` call is its own process; the two bridges must not share an environment, because the challenge and the solution use the same declaration names. I wrote this sequence from the audit's scripts and have not run it in exactly this form. The commands the audit actually ran, including the export comparison and the corruption control, are in [audit/REPORT.md](audit/REPORT.md) (section "Reproduction") and the scripts beside it; they expect the audit's own directory layout.

## 5. What this rests on

- The authors' Lean proof and the Mathlib library at the manifest pins.
- Lean's kernel, run through `leanchecker` and the comparator's export replay.
- My frozen statement. It is my reading of the literature statement; the bridge shows the authors' theorem implies it, not that it is the only reasonable formalization.
- Sets measurable in the completion of surface measure are covered by the authors' theorem; the frozen statement uses Borel-measurable sets, which are a special case.

## 6. Credits

- **A. Ibiapina, C. A. Gomes, A. Pio, S. Belo, E. Ferreira**: the proof, the Lean formalization LeanShadow, its comparator challenge and configuration ([arXiv:2610.27523](https://arxiv.org/abs/2610.27523), [allenibiapina/LeanShadow](https://github.com/allenibiapina/LeanShadow/tree/19deb3ed555cc8404958c1804f9b29898a918d10)).
- **H. S. Witsenhausen and G. Kalai**: the problem and the double-cap conjecture.
- **The Lean and Mathlib community**: Lean, Mathlib, lean4export, the comparator, leanchecker and the checklist for auditing a formal proof that this audit follows.
- **AI**: GPT-6.2 Astra ran the clean-room audit; Claude Opus 5.5 packaged this folder.

Files: [PACKAGING.md](PACKAGING.md) lists every file and its source; [SHA256SUMS](SHA256SUMS) pins them.
