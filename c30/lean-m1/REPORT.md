# math_c30lean_1103 — milestone 1

Completed 2026-11-03, 18:02 UTC. **PASS on all five frozen pass-bar items.**
The two requested finite facts are proved and build on a pinned Lean/Mathlib
project. The clean source-export build exited 0; all 16 theorem axiom closures
contain only Lean's standard axioms. No proof placeholders or native reduction
uses occur in the six project Lean files.

This establishes the named finite core lemmas. It does **not** establish a
Lean proof of C30 ≥521/50, the actual-object marking/analytic bridges, the
infinite generating-function selection step or the H_j coefficientwise product
transfer. The whole-bound verification level is not upgraded by this milestone.

## Results and exact scope

* `C30Lean.strip_envelope`: for an ordered list of nonnegative integer strips,
  the prescribed total, at least B zeros and at most U twos, and explicit
  feasibility hypotheses, constructs natural e0…e3 with e0=B, e2=U or U−1,
  the required parity and the exact displayed e1/e3 formulas. The resulting
  vector has the same length and sum and no larger excess at **any real
  threshold**. `integer_strip_envelope` and `parity_envelope` expose the
  integer inequalities and count identities separately.
* `C30Lean.strip_envelope_application`: uses exactly
  L=ceil(555555m/10^6), B=ceil(185185m/10^6)+1,
  U=floor(7m/50), r=m−L+1. Its feasibility is proved for every m≥100.
  Actual strip-vector hypotheses remain explicit; this cutoff does not claim
  existence of the asymptotic domino families at every such size.
* `C30Lean.finite_weighted_markov`: proves the unnormalized finite weighted
  Markov bound for arbitrary nonnegative real weights/values and positive
  threshold.
* `C30Lean.finite_family_selection`: proves the exact finite
  n(n−1)-weighted bad-object estimate for arbitrary finite nonnegative weights,
  natural sizes and strip counts. Taking weight z^n and threshold 1/10 gives
  the finite form of the bound used in §4.

The general envelope exposes sufficient linear feasibility conditions and the
necessary zero-cap parity guard, rather than pretending that the prose's
“sufficiently large m” guarantees arbitrary-parameter nonnegativity.
`STATEMENTS.md` quotes the source lines, explains every Lean statement and
clause, and identifies every strengthening or scope restriction. Majorization
is encoded in its equal-total, all-real-threshold formulation; no sorted-sum or
transfer-sequence equivalence is asserted as an additional theorem.

## Frozen pass bar, item by item

`PASS_BAR.md` was never edited. Its SHA-256 remains
`aa9d35b7d36b6d053af4b12ba1b094f0aec2c1817905a6e5969c472a7b198ba5`.

| Item | Verdict | Evidence |
|---|---|---|
| 1. Pinned project; clean-checkout build; complete log, exit code and every Lean hash | **PASS** | `lean-toolchain`, `lake-manifest.json`, `receipts/pins.txt`, `receipts/clean-pins.txt`; `receipts/clean-build.log`, `clean-build.exit-code`, `lean.sha256`. A fresh source-only export into an initially empty directory was used, with fresh dependency checkouts and no copied project outputs; `clean-initial-state.txt` records initial absence of `.lake`. No Git commit was created. |
| 2. No sorry/sorryAx/admit; source scan and axiom output | **PASS** | `receipts/grep.txt`: grep exit 1, no matches in any of the six project `.lean` files. All 16 axiom reports in `receipts/axioms.txt` are free of a placeholder axiom. Documentation and the frozen pass bar necessarily name the prohibited tokens; they are not proof uses. |
| 3. Only declared/standard axioms; expected non-standard list empty | **PASS** | Every theorem is audited in `Audit.lean`. `AXIOMS.md` reproduces the output: only `propext`, `Classical.choice`, `Quot.sound`; **non-standard list empty**. There are no BBEP/Norton or numerical axioms. |
| 4. native_decide and Lean.ofReduceBool absent or explained | **PASS** | Both are absent from project source, as recorded in `receipts/grep.txt`; no theorem axiom closure contains a native reduction axiom. `AXIOMS.md` explains the kernel-checked tactic boundary. |
| 5. Statements match the two informal finite lemmas; line-by-line correspondence | **PASS** | `STATEMENTS.md` maps source §§4–5 to every declaration and main theorem clause, including exact parity, natural multiplicities, length/sum identities, all thresholds, finite weight assumptions and the explicit application cutoff. The T histogram identity is replaced by a directly proved sufficient count inequality, with this proof-level difference documented. |

## Pins, clean-build receipt and reproduction

Lean: `leanprover/lean4:v4.35.0`, compiler commit
`eb6cafb7290e8bd5f2937522d8d804f58f02bafc`.
Mathlib: `56a005855ea17e0b0958f73ec801ae140b0a1679` (matching v4.35.0).
The manifest also locks every transitive dependency. Both the working and clean
dependency checkouts report that exact Mathlib commit with no tracked changes.

The clean build ran on math-cpu-15 under
`/root/os/math_c30lean_1103/verification/clean-checkout-xaoSyYO8`.
It obtained oleans with `lake exe cache get`, then ran `lake build` from
18:00:26 to 18:01:00 UTC: **33.752 seconds, exit 0**. The resource wrapper
records largest-child RSS **1,822,024 KiB** (not a claim about aggregate RSS).
All compute was at nice 10 within an affinity mask of twelve allowed CPUs;
Lean thread count was four during final verification. No Lean builds ran on
the Mini.

From this directory, with elan installed:

```sh
lake exe cache get
lake build
lake env lean Audit.lean
python3 scripts/audit-receipts.py
```

For the exact Linux fresh-source verification workflow, see
`scripts/verify-clean.sh` and the command in `README.md`. The retained
`receipts/source-export.tar.gz` contains all six Lean files, toolchain,
Lake configuration and dependency lock, without build outputs. Its hash is in
`receipts/source-export.sha256`. `scripts/audit-receipts.py` verifies that this
archive and the delivered source tree agree, the frozen pass bar is intact,
every declared theorem has an axiom report, the axiom whitelist is respected,
and the clean-build/scan receipts pass. Its result is
`receipts/audit-summary.json`.

## Prior art, preservation and next step

`PRIOR_ART.md` was written before implementation. The existing C30r2/levels
audit was read and retained, including the five discovery categories. Fresh
reads reopened the table, public PR 313, the stable Lean release and relevant
Mathlib documentation/source. The table baseline remains the inherited 10.27;
PR 313 proposes Norton's unrefereed 10.412263. The supplied local 10.42 candidate
provides the finite lemmas formalized here. This job reproduces their finite
proofs, not their numerical or whole-bound claims, and makes no novelty or
record claim. Detailed credit, URLs, limitations and snapshots are in
`PRIOR_ART.md` and `sources/`.

All project sources and receipts have been pulled to this Mini directory; the
retained delivery is well below 50 MB. STATUS.md records the start, successful
working build and completion; the whole job took less than one hour.
`receipts/worker-check.json` and `mini-worker-check.json` report no remaining
workers for this job after a `ps -axo pid,ppid,pcpu,command` check. Shared L1
checker jobs were excluded and left untouched. No commits, pushes, PRs,
posts or external messages were made.

Next follow the L2 plan: formalize the actual-object value-word/marking
interfaces and the coefficientwise transfer adapter, then the analytic
first-moment and radius/subsequence bridges. This package supplies the finite
integer and finite selection components without adding paper axioms.
